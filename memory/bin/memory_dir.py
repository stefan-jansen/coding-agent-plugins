#!/usr/bin/env python3
"""Resolve a project's memory directory.

`.workspace/memory/` is the convention and stays the default. Projects that
predate it, or that carry hundreds of `memory/...` path references in their
prose, can point the plugin at the directory they already use instead of
relocating those files.

Resolution order:

  1. an explicit `--dir` on the command line (callers handle this themselves)
  2. `$CLAUDE_MEMORY_DIR` — absolute, or relative to the project root
  3. `<project_root>/.workspace/memory`

Set it per project through the `env` block of `.claude/settings.json`, which
reaches both the hooks and any shell the agent runs:

    {"env": {"CLAUDE_MEMORY_DIR": "memory"}}

The shell scripts in this directory implement the same three rules inline
rather than sourcing this file, so each stays runnable on its own.
"""

from __future__ import annotations

import os
from pathlib import Path

ENV_VAR = "CLAUDE_MEMORY_DIR"
DEFAULT_PARTS = (".workspace", "memory")


def resolve(project_root: Path | str, env: dict | None = None) -> Path:
    """Return the memory directory for `project_root`."""
    root = Path(project_root)
    environ = os.environ if env is None else env
    raw = (environ.get(ENV_VAR) or "").strip()
    if not raw:
        return root.joinpath(*DEFAULT_PARTS)
    candidate = Path(os.path.expanduser(raw))
    if not candidate.is_absolute():
        candidate = root / candidate
    return candidate
