#!/usr/bin/env python3
"""Discover the memory files a memory directory manages.

One walk, one set of rules, shared by the seeder (`memory_init_index.sh`), the
verifier (`verify_index.sh`), the GC proposer (`gc_propose.py`) and the
PreToolUse reference hook. Before this module each of those globbed
`<memory_dir>/*.md` on its own, so anything in a subdirectory was invisible to
all of them at once - not indexed, not verified, and not credited with a read.

Rules:

  * Recurse. A note in `_inbox/` is a memory file.
  * Key every file by its path relative to the memory directory, POSIX-style
    (`_inbox/holdout-fold.md`). Basenames collide across subdirectories; paths
    do not.
  * `MEMORY_INDEX.md` at the top level is index infrastructure, not an entry.
  * Decline `_archive/` (superseded by convention) and dot-directories, and
    say so. Every declined file is returned with a reason so callers can report
    it: silence is what let 25 notes sit outside the system in ~/ml4t/agents.
"""

from __future__ import annotations

import os

INDEX_NAME = "MEMORY_INDEX.md"
ARCHIVE_DIR = "_archive"

REASON_ARCHIVE = "under %s/ (superseded by convention)" % ARCHIVE_DIR
REASON_HIDDEN = "inside a dot-directory"


def _rel(memory_dir: str, path: str) -> str:
    return os.path.relpath(path, memory_dir).replace(os.sep, "/")


def discover(memory_dir) -> tuple[list[str], list[tuple[str, str]]]:
    """Return (managed, skipped).

    `managed` is a sorted list of relative POSIX paths this plugin indexes.
    `skipped` is a sorted list of `(relative path, reason)` for `.md` files
    found under the directory that were deliberately left out. `MEMORY_INDEX.md`
    is in neither: it is the artifact, not an input.
    """
    memory_dir = os.path.abspath(str(memory_dir))
    managed: list[str] = []
    skipped: list[tuple[str, str]] = []

    for dirpath, dirnames, filenames in os.walk(memory_dir):
        # Record what we are about to prune, then prune it.
        pruned = [d for d in dirnames
                  if d == ARCHIVE_DIR or d.startswith(".")]
        for d in pruned:
            reason = REASON_ARCHIVE if d == ARCHIVE_DIR else REASON_HIDDEN
            for sub, _, subfiles in os.walk(os.path.join(dirpath, d)):
                for fn in subfiles:
                    if fn.endswith(".md"):
                        skipped.append((_rel(memory_dir, os.path.join(sub, fn)), reason))
        dirnames[:] = [d for d in dirnames if d not in pruned]

        for fn in sorted(filenames):
            if not fn.endswith(".md"):
                continue
            full = os.path.join(dirpath, fn)
            rel = _rel(memory_dir, full)
            if rel == INDEX_NAME:
                continue
            managed.append(rel)

    return sorted(managed), sorted(skipped)


def relative_key(resolved, memory_dir) -> str | None:
    """Key for a path under `memory_dir`, or None if it is not a managed file.

    Used by the reference hook, which sees paths one at a time and must not
    walk the tree. Applies the same rules as `discover` without touching disk,
    so a file that is about to be created still resolves.
    """
    resolved = os.path.abspath(str(resolved))
    memory_dir = os.path.abspath(str(memory_dir))
    if resolved == memory_dir:
        return None
    rel = _rel(memory_dir, resolved)
    if rel.startswith("../") or rel == "..":
        return None
    if not rel.endswith(".md"):
        return None
    if rel == INDEX_NAME:
        return None
    # A glob is not a file. Paths pulled out of a shell command reach here
    # unexpanded, and an entry keyed `_inbox/*.md` is a phantom.
    if any(ch in rel for ch in "*?["):
        return None
    parts = rel.split("/")[:-1]
    if any(p == ARCHIVE_DIR or p.startswith(".") for p in parts):
        return None
    return rel
