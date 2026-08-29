#!/usr/bin/env python3
"""PreToolUse hook: capture references to a project's memory files.

Fired by Claude Code's PreToolUse hook layer (matcher: Read|Grep|Bash). Reads
the tool-invocation JSON from stdin, extracts any path it can see, and - if the
path identifies a managed `*.md` under the project's memory directory - bumps
that file's `last_referenced` (to today, UTC) and increments `references`
inside that directory's `.index_state.json`.

`Bash` is matched because a session running with bypassed permissions is
instructed to read files with `cat` / `sed -n` / `head` and search with `grep`,
so restricting capture to the Read and Grep tools measured which tool the
harness happened to prefer rather than which memory files were used. Paths are
recovered from the command string with a regex; every candidate is validated
against the memory directory before anything is written, so the imprecision
costs a missed bump, never a wrong one.

Managed means what bin/memory_files.py says it means: any `*.md` under the
memory directory except `MEMORY_INDEX.md`, `_archive/` and dot-directories,
keyed by its path relative to that directory (`_inbox/note.md`). Keying by
relative path is what lets a note in a subdirectory accumulate signal at all.

The memory directory is `.workspace/memory/` unless `$CLAUDE_MEMORY_DIR` says
otherwise; see bin/memory_dir.py.

The hook is the source of M3 acceptance criterion 3 (signal capture): after a
session that reads a target memory file, that file's `last_referenced` should
have advanced to today.

Design constraints:
  - Pure stdlib (Python 3). Same baseline as the rest of the memory plugin.
  - Never blocks a tool call. Any error (bad JSON, missing project, sidecar
    write failure) is swallowed; we exit 0 and let the read proceed.
  - Idempotent — re-running for the same path on the same day is a no-op
    apart from incrementing the `references` counter.
  - Fast - single JSON parse + single sidecar rewrite. No project crawl,
    no token counts, no MEMORY_INDEX.md reads. Bash payloads that cannot
    contain a memory path are rejected on a substring test before any work.
  - Best-effort race handling — read/modify/write under a sibling lockfile so
    concurrent Read/Grep tool calls don't drop updates. Lock failures fall
    through to a plain write rather than skipping the update.

The sidecar contract is documented in bin/memory_init_index.sh. We only touch:
  - `files.<path>.last_referenced` (set to today UTC)
  - `files.<path>.references`     (int, defaulted to 0 + 1)
  - `files.<path>.tokens`         (preserved if present; defaulted to 0 if a
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
import re
import sys
from pathlib import Path
from typing import Iterable

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
try:
    from memory_dir import resolve as resolve_memory_dir
    from memory_files import relative_key
except ImportError:  # pragma: no cover - plugin tree is incomplete
    resolve_memory_dir = None
    relative_key = None


def _today_utc() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d")


# A shell word that ends in `.md`, with surrounding quotes and shell
# metacharacters excluded. Deliberately loose: anything it over-matches is
# thrown away by the memory-directory check in `_project_memory_match`.
_MD_IN_COMMAND = re.compile(r"""[^\s'"`;|&<>()$]*\.md""")


def _candidate_paths(tool_name: str, tool_input: dict) -> Iterable[str]:
    """Yield raw path strings present in the tool input.

    We deliberately stay tolerant - different Claude Code versions name fields
    slightly differently (e.g. `file_path` vs `path`). Each yielded string is
    later validated as a memory file before we touch the sidecar.
    """
    if not isinstance(tool_input, dict):
        return
    if tool_name == "Bash":
        # `cat memory/foo.md`, `sed -n '1,40p' memory/foo.md`, `grep -n x
        # memory/*.md`. A path assembled from a variable is invisible to us;
        # that is a missed bump, not a wrong one.
        command = tool_input.get("command")
        if not isinstance(command, str) or ".md" not in command:
            return
        for match in _MD_IN_COMMAND.findall(command):
            if match and match != ".md":
                yield match
        return
    keys = ("file_path", "path", "filename")
    if tool_name == "Grep":
        # Grep `path` is a directory or file root; `glob` narrows further but
        # we only care about the path itself (Grep over `.workspace/memory/`
        # touches every memory file conceptually - we don't pick winners).
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


def _project_memory_match(resolved: Path, memory_dir: Path) -> tuple[Path, str] | None:
    """If `resolved` is a managed memory file, return `(memory_dir, <key>)`.

    The key is the path relative to `memory_dir` (`_inbox/note.md` for a note
    in a subdirectory), matching how bin/memory_init_index.sh keys the index
    and the sidecar. `MEMORY_INDEX.md` is excluded: it is auto-loaded on every
    session, so reading it is not a signal about any specific memory file.

    `memory_dir` comes from bin/memory_dir.py, so a project that keeps its
    memory somewhere other than `.workspace/memory/` still registers reads.
    We accept non-existing files (the read may be about to create one) - the
    check is on the path, not on the file existing.
    """
    key = relative_key(resolved, memory_dir)
    if key is None:
        return None
    return memory_dir, key


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
    if tool_name not in ("Read", "Grep", "Bash"):
        return 0
    tool_input = payload.get("tool_input") or {}

    cwd_raw = payload.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    project_root = Path(cwd_raw).resolve()

    if resolve_memory_dir is None or relative_key is None:
        return 0
    try:
        memory_dir = resolve_memory_dir(project_root).resolve(strict=False)
    except OSError:
        return 0

    # Group bumps by memory_dir so we issue one sidecar write per project.
    by_dir: dict[Path, set[str]] = {}
    for raw in _candidate_paths(tool_name, tool_input):
        resolved = _resolve(project_root, raw)
        match = _project_memory_match(resolved, memory_dir)
        if not match:
            continue
        target_dir, name = match
        by_dir.setdefault(target_dir, set()).add(name)

    for memory_dir, names in by_dir.items():
        _bump(memory_dir, names)

    return 0


if __name__ == "__main__":
    sys.exit(main())
