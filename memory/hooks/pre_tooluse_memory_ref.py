#!/usr/bin/env python3
"""PreToolUse hook: capture references to `.workspace/memory/*.md` files.

Fired by Claude Code's PreToolUse hook layer (matcher: Read|Grep). Reads the
tool-invocation JSON from stdin, extracts any path it can see, and — if the
path identifies a memory file under `<project>/.workspace/memory/*.md` —
bumps that file's `last_referenced` (to today, UTC) and increments `references`
inside `<project>/.workspace/memory/.index_state.json`.

The hook is the source of M3 acceptance criterion 3 (signal capture): after a
session that reads a target memory file, that file's `last_referenced` should
have advanced to today.

Design constraints:
  - Pure stdlib (Python 3). Same baseline as the rest of the memory plugin.
  - Never blocks a tool call. Any error (bad JSON, missing project, sidecar
    write failure) is swallowed; we exit 0 and let the read proceed.
  - Idempotent — re-running for the same path on the same day is a no-op
    apart from incrementing the `references` counter.
  - Fast — single JSON parse + single sidecar rewrite. No project crawl,
    no token counts, no MEMORY_INDEX.md reads.
  - Best-effort race handling — read/modify/write under a sibling lockfile so
    concurrent Read/Grep tool calls don't drop updates. Lock failures fall
    through to a plain write rather than skipping the update.

The sidecar contract is documented in bin/memory_init_index.sh. We only touch:
  - `files.<name>.last_referenced` (set to today UTC)
  - `files.<name>.references`     (int, defaulted to 0 + 1)
  - `files.<name>.tokens`         (preserved if present; defaulted to 0 if a
                                   memory file appears here for the first time
                                   between init runs)

`last_gc_run` is owned by `bin/stamp_gc_run.sh`; we never touch it here.
"""

from __future__ import annotations

import datetime as _dt
import errno
import fcntl
import json
import os
import sys
from pathlib import Path
from typing import Iterable


def _today_utc() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d")


def _candidate_paths(tool_name: str, tool_input: dict) -> Iterable[str]:
    """Yield raw path strings present in the tool input.

    We deliberately stay tolerant — different Claude Code versions name fields
    slightly differently (e.g. `file_path` vs `path`). Each yielded string is
    later validated as a real `.workspace/memory/*.md` file before we touch
    the sidecar.
    """
    if not isinstance(tool_input, dict):
        return
    keys = ("file_path", "path", "filename")
    if tool_name == "Grep":
        # Grep `path` is a directory or file root; `glob` narrows further but
        # we only care about the path itself (Grep over `.workspace/memory/`
        # touches every memory file conceptually — we don't pick winners).
        keys = ("path", "file_path")
    for key in keys:
        value = tool_input.get(key)
        if isinstance(value, str) and value.strip():
            yield value


def _resolve(project_root: Path, raw: str) -> Path:
    p = Path(raw)
    if not p.is_absolute():
        p = project_root / p
    try:
        return p.resolve(strict=False)
    except OSError:
        return p


def _project_memory_match(resolved: Path) -> tuple[Path, str] | None:
    """If `resolved` is `<project>/.workspace/memory/<name>.md`, return
    `(<project>/.workspace/memory, <name>.md)`. Otherwise None.

    We accept symlinks and non-existing files (the read may be about to create
    one) — the check is purely structural on the path components.
    """
    parts = resolved.parts
    try:
        idx = len(parts) - 1 - parts[::-1].index(".workspace")
    except ValueError:
        return None
    if idx + 2 >= len(parts):
        return None
    if parts[idx + 1] != "memory":
        return None
    name = parts[idx + 2]
    if not name.endswith(".md") or name == "MEMORY_INDEX.md":
        # MEMORY_INDEX is auto-loaded on every session; reading it isn't a
        # signal about any specific memory file.
        return None
    memory_dir = Path(*parts[: idx + 2])
    return memory_dir, name


def _load_sidecar(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except FileNotFoundError:
        data = {}
    except (json.JSONDecodeError, OSError):
        # Corrupt or unreadable sidecar — start a fresh structure rather than
        # crashing the read. memory_init_index.sh is the canonical seeder.
        data = {}
    if not isinstance(data, dict):
        data = {}
    data.setdefault("version", 1)
    data.setdefault("generated_by", "pre_tooluse_memory_ref.py")
    files = data.get("files")
    if not isinstance(files, dict):
        files = {}
    data["files"] = files
    return data


def _write_sidecar(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, sort_keys=False)
        fh.write("\n")
    os.replace(tmp, path)


def _bump(memory_dir: Path, names: set[str]) -> None:
    if not names:
        return
    sidecar = memory_dir / ".index_state.json"
    lock_path = memory_dir / ".index_state.lock"
    memory_dir.mkdir(parents=True, exist_ok=True)

    # Best-effort lock; on EACCES / EPERM (read-only FS, etc.) fall through.
    lock_fh = None
    try:
        lock_fh = open(lock_path, "a+")
        try:
            fcntl.flock(lock_fh.fileno(), fcntl.LOCK_EX)
        except OSError:
            pass
    except OSError as exc:
        if exc.errno not in (errno.EACCES, errno.EPERM, errno.EROFS):
            return

    try:
        data = _load_sidecar(sidecar)
        today = _today_utc()
        files = data["files"]
        for name in names:
            entry = files.get(name)
            if not isinstance(entry, dict):
                entry = {}
            entry["last_referenced"] = today
            entry["references"] = int(entry.get("references") or 0) + 1
            entry.setdefault("tokens", 0)
            files[name] = entry
        _write_sidecar(sidecar, data)
    except Exception:
        # The hook must never block a tool call.
        return
    finally:
        if lock_fh is not None:
            try:
                fcntl.flock(lock_fh.fileno(), fcntl.LOCK_UN)
            except OSError:
                pass
            lock_fh.close()


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    if not isinstance(payload, dict):
        return 0

    tool_name = payload.get("tool_name")
    if tool_name not in ("Read", "Grep"):
        return 0
    tool_input = payload.get("tool_input") or {}

    cwd_raw = payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    project_root = Path(cwd_raw).resolve()

    # Group bumps by memory_dir so we issue one sidecar write per project.
    by_dir: dict[Path, set[str]] = {}
    for raw in _candidate_paths(tool_name, tool_input):
        resolved = _resolve(project_root, raw)
        match = _project_memory_match(resolved)
        if not match:
            continue
        memory_dir, name = match
        by_dir.setdefault(memory_dir, set()).add(name)

    for memory_dir, names in by_dir.items():
        _bump(memory_dir, names)

    return 0


if __name__ == "__main__":
    sys.exit(main())
