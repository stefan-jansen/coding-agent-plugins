#!/usr/bin/env python3
"""Apply an approved batch of instruction-file edits, atomically.

Reads a JSON batch on stdin:

    {"edits": [
       {"path": "/abs/path/AGENTS.md",
        "old": "<exact text to replace>",
        "new": "<replacement, may be empty to delete>",
        "sha256": "<digest of the file when it was read>",
        "finding": "cat1-3"}
    ]}

Validates every edit before writing any of them. A batch either lands whole or
not at all: with N files, applying one at a time leaves a half-edited set
behind the first failure, which is exactly the state the approval was not
given for.

Two rules with teeth:

  * Writes go to the resolved real path. An instruction file is often a
    symlink into a dotfiles repo, and writing through the link with a
    temp-file rename would replace the link with a regular file.
  * Nothing here commits. A commit runs the project's pre-commit hooks, and
    a hook failure is a stop for the caller to fix, never a --no-verify.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
from pathlib import Path


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def validate(edits: list[dict]) -> tuple[list[dict], dict[str, str], list[str]]:
    """Resolve and check every edit.

    Returns (plan, staged, errors) where `staged` maps a real path to its
    fully-updated content. Nothing is written here.
    """
    plan, errors = [], []
    by_real: dict[str, str] = {}

    for i, e in enumerate(edits):
        tag = e.get("finding") or f"edit[{i}]"
        p = Path(e["path"]).expanduser()
        if not p.exists():
            errors.append(f"{tag}: no such file: {p}")
            continue
        real = p.resolve()
        if not os.access(real, os.W_OK):
            errors.append(f"{tag}: not writable: {real}")
            continue

        current = by_real.get(str(real))
        if current is None:
            current = real.read_text(encoding="utf-8")

        if e.get("sha256") and digest(current) != e["sha256"]:
            errors.append(
                f"{tag}: {p} changed since it was read - re-run the audit"
            )
            continue

        old, new = e["old"], e.get("new", "")
        if old and old not in current:
            errors.append(f"{tag}: text to replace not found in {p}")
            continue
        if old and current.count(old) > 1:
            errors.append(
                f"{tag}: text to replace appears {current.count(old)} times "
                f"in {p} - widen it until it is unique"
            )
            continue

        updated = current.replace(old, new, 1) if old else current + new
        if updated == current:
            errors.append(f"{tag}: edit is a no-op on {p}")
            continue

        by_real[str(real)] = updated
        plan.append({"link": str(p), "real": str(real), "finding": tag})

    return plan, by_real, errors


def write_all(staged: dict[str, str]) -> list[str]:
    """Write every staged file through a same-directory temp + os.replace."""
    written = []
    for real, content in staged.items():
        target = Path(real)
        fd, tmp = tempfile.mkstemp(dir=target.parent, prefix=f".{target.name}.",
                                   suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(content)
            os.replace(tmp, target)
            written.append(real)
        except OSError:
            Path(tmp).unlink(missing_ok=True)
            raise
    return written


def main() -> int:
    try:
        batch = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(f"apply: batch is not valid JSON: {exc}", file=sys.stderr)
        return 2

    edits = batch.get("edits") or []
    if not edits:
        print("apply: empty batch, nothing to do")
        return 0

    plan, staged, errors = validate(edits)
    if errors:
        print("apply: NOTHING WRITTEN. Validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    before = {p["real"]: Path(p["real"]).is_symlink() for p in plan}
    written = write_all(staged)

    for real, was_link in before.items():
        if Path(real).is_symlink() != was_link:
            print(f"apply: WARNING symlink state changed at {real}",
                  file=sys.stderr)

    for p in plan:
        via = f" (via {p['link']})" if p["link"] != p["real"] else ""
        print(f"applied {p['finding']}: {p['real']}{via}")
    print(f"\n{len(written)} file(s) written, {len(plan)} edit(s) applied.")
    print("Not committed. Run the project's own commit; never --no-verify.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
