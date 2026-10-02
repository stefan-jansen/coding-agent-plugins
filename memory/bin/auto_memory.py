#!/usr/bin/env python3
"""Resolve and measure Claude Code's *auto memory* for a project.

Auto memory is the store Claude Code writes by itself: a `MEMORY.md` index
plus one file per fact. The harness loads `MEMORY.md` into every session, so
it spends the same context budget as the `@`-include closure that
`measure_memory.sh` reports - but it lives outside the repo by default and no
other script here looked at it. A project could sit at 30% of its cap with a
few thousand tokens of auto memory loaded on top, unmeasured.

Resolution, matching Claude Code v2.1.287 (verified 2026-10-02):

  1. `autoMemoryDirectory` from the settings chain, most specific first:
     `.claude/settings.local.json`, `.claude/settings.json`,
     `$CLAUDE_CONFIG_DIR/settings.json` (default `~/.claude/settings.json`).
  2. otherwise `<config dir>/projects/<slug>/memory`, where `<slug>` is the
     project's absolute path with every `/` replaced by `-`.

**The value must be absolute or start with `~/`.** A relative path such as
`./.workspace/memory-auto` is silently ignored and the default is used
instead - probed directly, not inferred from the docs. There is no variable
expansion either: `$CLAUDE_PROJECT_DIR/...` is also ignored. So an in-repo
auto-memory directory cannot be expressed portably in a committed
`settings.json`; it belongs in per-machine `.claude/settings.local.json`.

Pure stdlib. Usable as a module or as a CLI (`--json` for machine output).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from token_count import count_file  # noqa: E402

INDEX_NAME = "MEMORY.md"
SETTING = "autoMemoryDirectory"


def config_dir() -> Path:
    raw = (os.environ.get("CLAUDE_CONFIG_DIR") or "").strip()
    return Path(os.path.expanduser(raw)) if raw else Path.home() / ".claude"


def project_slug(project_root: Path) -> str:
    """The `projects/<slug>` directory name Claude Code derives from a path.

    Every `/` becomes `-`, which is why a path that already contains a `-`
    segment boundary yields `--`. Verified against the live store.
    """
    return str(Path(project_root).resolve()).replace(os.sep, "-")


def _setting_from(path: Path) -> str | None:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    value = data.get(SETTING)
    return value.strip() if isinstance(value, str) and value.strip() else None


def _accepted(value: str) -> Path | None:
    """The directory `value` names, or None when Claude Code would ignore it."""
    if value.startswith("~/") or value.startswith("~" + os.sep):
        return Path(os.path.expanduser(value))
    candidate = Path(value)
    return candidate if candidate.is_absolute() else None


def resolve(project_root: Path | str) -> tuple[Path, str, list[str]]:
    """(directory, source, ignored-settings) for `project_root`."""
    root = Path(project_root).resolve()
    ignored: list[str] = []
    chain = [
        (root / ".claude" / "settings.local.json", ".claude/settings.local.json"),
        (root / ".claude" / "settings.json", ".claude/settings.json"),
        (config_dir() / "settings.json", "user settings"),
    ]
    for path, label in chain:
        value = _setting_from(path)
        if value is None:
            continue
        accepted = _accepted(value)
        if accepted is not None:
            return accepted, f"{SETTING} in {label}", ignored
        ignored.append(f"{label}: {value!r} is not absolute and is ignored")
    return config_dir() / "projects" / project_slug(root) / "memory", "default (per-project store)", ignored


def summarize(project_root: Path | str) -> dict:
    """What auto memory costs and holds for `project_root`."""
    directory, source, ignored = resolve(project_root)
    index = directory / INDEX_NAME
    index_tokens = count_file(str(index)) if index.is_file() else 0
    bodies = sorted(
        p for p in directory.glob("*.md") if p.is_file() and p.name != INDEX_NAME
    ) if directory.is_dir() else []
    return {
        "dir": str(directory),
        "source": source,
        "ignored_settings": ignored,
        "exists": directory.is_dir(),
        "index_exists": index.is_file(),
        "index_tokens": index_tokens,
        "body_files": len(bodies),
        "body_tokens": sum(count_file(str(p)) for p in bodies),
        "in_repo": _is_within(directory, Path(project_root).resolve()),
    }


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root)
        return True
    except ValueError:
        return False


def report(info: dict, indent: str = "  ") -> list[str]:
    """Human lines describing `info`. `index_tokens` is the auto-loaded part."""
    lines = [f"{indent}Auto memory: {info['dir']}  [{info['source']}]"]
    if not info["exists"]:
        lines.append(f"{indent}  (no auto-memory directory yet)")
    else:
        lines.append(
            f"{indent}  {INDEX_NAME}: {info['index_tokens']} tokens (auto-loaded)"
            if info["index_exists"]
            else f"{indent}  {INDEX_NAME}: absent"
        )
        lines.append(
            f"{indent}  {info['body_files']} fact file(s), {info['body_tokens']} tokens (read on demand)"
        )
        lines.append(
            f"{indent}  in repo: {'yes' if info['in_repo'] else 'no - not committed, not synced to the other machine, not visible to Codex'}"
        )
    for note in info["ignored_settings"]:
        lines.append(f"{indent}  IGNORED {note}")
    return lines


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--project", default=None, help="project root (default: git root, else cwd)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--index-tokens", action="store_true",
                    help="print only the auto-loaded MEMORY.md token count")
    args = ap.parse_args(argv)

    root = Path(args.project) if args.project else _git_root()
    info = summarize(root)
    if args.index_tokens:
        print(info["index_tokens"])
    elif args.json:
        print(json.dumps(info, indent=2, sort_keys=True))
    else:
        print(f"Project: {root}")
        print("\n".join(report(info)))
    return 0


def _git_root() -> Path:
    import subprocess
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, timeout=5)
        if out.returncode == 0 and out.stdout.strip():
            return Path(out.stdout.strip())
    except (OSError, subprocess.SubprocessError):
        pass
    return Path.cwd()


if __name__ == "__main__":
    sys.exit(main())
