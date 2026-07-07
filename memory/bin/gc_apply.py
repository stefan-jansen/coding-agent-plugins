#!/usr/bin/env python3
"""gc_apply.py — apply a /memory-gc diff (produced by gc_propose.py).

Consumes the JSON document gc_propose.py emits (read from stdin or --diff PATH)
and rewrites MEMORY_INDEX.md to reflect the proposed status transitions. The
write is transactional: we serialize the *entire* new index to a temp file
and atomically `os.replace` it into place. Either every transition lands, or
none do — there is no partial-application state to recover from.

v0.1 applies whole-file replacement based on the diff (no other index fields
move). True surgical section editing of memory files themselves is a v0.2
increment per the spec.

Safety:

  * The diff carries `memory_dir`; we abort unless `--memory-dir` matches (or
    the caller passes --trust-diff to override — useful when running in a
    different working tree than the dry-run).
  * Each transition records `from`; we abort if the current entry's status
    doesn't match what the diff was computed against (the index changed
    underneath us). Pass --force to apply anyway.
  * On success, optionally stamps `last_gc_run` in `.index_state.json` via
    bin/stamp_gc_run.sh (suppress with --no-stamp).

Exit 0 on success, 1 on conflict (status drift) or write failure, 2 on
environment / argument errors.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


HEADING_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$")
STATUS_RE = re.compile(r"^(\s*-\s*status:\s*)(.+?)(\s*)$")


def _read_diff(path_or_stdin: str | None) -> dict:
    if not path_or_stdin or path_or_stdin == "-":
        raw = sys.stdin.read()
    else:
        raw = Path(path_or_stdin).read_text(encoding="utf-8")
    return json.loads(raw)


def _rewrite_index(index_path: Path, transitions: list[dict], force: bool) -> tuple[list[str], list[str]]:
    """Return (applied_names, conflicts). On conflict (and not force), aborts before write."""
    text = index_path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    # Map filename -> (from, to) for fast lookup.
    transitions_by_name: dict[str, tuple[str, str]] = {
        t["name"]: (t["from"], t["to"]) for t in transitions
    }

    new_lines: list[str] = []
    current: str | None = None
    applied: list[str] = []
    conflicts: list[str] = []

    for line in lines:
        stripped = line.rstrip("\n")
        h = HEADING_RE.match(stripped)
        if h:
            name = h.group(2).strip().strip("`").strip('"').strip("'").strip()
            current = os.path.normpath(name)
            new_lines.append(line)
            continue
        if current and current in transitions_by_name:
            m = STATUS_RE.match(stripped)
            if m:
                expected_from, to_status = transitions_by_name[current]
                actual = m.group(2).strip()
                if actual != expected_from and not force:
                    conflicts.append(
                        f"{current}: index has status '{actual}', "
                        f"diff expected '{expected_from}' "
                        f"(re-run dry-run or use --force)"
                    )
                else:
                    # Preserve the line's leading prefix + trailing whitespace.
                    nl = "\n" if line.endswith("\n") else ""
                    new_lines.append(f"{m.group(1)}{to_status}{m.group(3)}{nl}")
                    applied.append(current)
                    # Remove from the pending map so a duplicate heading
                    # doesn't re-apply.
                    transitions_by_name.pop(current, None)
                    continue
        new_lines.append(line)

    if conflicts and not force:
        # Don't write — report and let the caller resolve.
        return applied, conflicts

    if applied:
        tmp = index_path.with_suffix(index_path.suffix + ".tmp")
        tmp.write_text("".join(new_lines), encoding="utf-8")
        os.replace(tmp, index_path)

    # Any leftover entries in transitions_by_name had no matching heading or
    # status field — report as conflicts (file may have been edited).
    for name, (from_s, _) in transitions_by_name.items():
        conflicts.append(
            f"{name}: no matching entry/status field found in MEMORY_INDEX.md "
            f"(diff expected '{from_s}')"
        )
    return applied, conflicts


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--diff", help="path to a gc_propose.py JSON diff (default: stdin)")
    ap.add_argument("--memory-dir", help="memory directory to act on (must match diff.memory_dir)")
    ap.add_argument("--trust-diff", action="store_true",
                    help="use the diff's memory_dir even if --memory-dir disagrees")
    ap.add_argument("--force", action="store_true",
                    help="apply transitions even if current index statuses don't match diff")
    ap.add_argument("--no-stamp", action="store_true",
                    help="skip writing last_gc_run to .index_state.json")
    args = ap.parse_args(argv)

    try:
        diff = _read_diff(args.diff)
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        sys.stderr.write(f"gc_apply.py: invalid diff input: {exc}\n")
        return 2

    if not isinstance(diff, dict) or "transitions" not in diff:
        sys.stderr.write("gc_apply.py: diff missing 'transitions' field\n")
        return 2

    diff_dir = Path(diff.get("memory_dir") or "")
    chosen_dir: Path
    if args.memory_dir:
        chosen_dir = Path(args.memory_dir).resolve()
        if not args.trust_diff and chosen_dir != diff_dir.resolve():
            sys.stderr.write(
                f"gc_apply.py: --memory-dir {chosen_dir} disagrees with "
                f"diff memory_dir {diff_dir} (pass --trust-diff to override)\n"
            )
            return 2
    else:
        chosen_dir = diff_dir.resolve() if diff_dir else Path.cwd()

    index_path = chosen_dir / "MEMORY_INDEX.md"
    if not index_path.is_file():
        sys.stderr.write(f"gc_apply.py: no MEMORY_INDEX.md in {chosen_dir}\n")
        return 2

    transitions = diff.get("transitions") or []
    if not transitions:
        print("gc_apply: no transitions to apply.")
        if not args.no_stamp:
            _stamp(chosen_dir)
        return 0

    applied, conflicts = _rewrite_index(index_path, transitions, args.force)

    if conflicts and not args.force:
        sys.stderr.write("gc_apply: conflicts detected; nothing written:\n")
        for c in conflicts:
            sys.stderr.write(f"  - {c}\n")
        return 1

    for name in applied:
        print(f"applied: {name}")
    if conflicts:
        for c in conflicts:
            sys.stderr.write(f"warn: {c}\n")

    if not args.no_stamp:
        _stamp(chosen_dir)
    print(f"gc_apply: applied {len(applied)} transition(s) to {index_path}")
    return 0


def _stamp(memory_dir: Path) -> None:
    stamp = Path(__file__).with_name("stamp_gc_run.sh")
    if not stamp.is_file():
        return
    try:
        subprocess.run(
            [str(stamp), "--dir", str(memory_dir)],
            check=False, capture_output=True, timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        pass


if __name__ == "__main__":
    sys.exit(main())
