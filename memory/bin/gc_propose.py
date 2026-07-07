#!/usr/bin/env python3
"""gc_propose.py — compute a /memory-gc dry-run diff (proposed status transitions).

This is the heart of M4 acceptance criterion 5. It reads three sources:

  * `MEMORY_INDEX.md`             current statuses + anchors + tokens
  * `.index_state.json` sidecar   per-file `last_referenced` + `references`
                                  + project-level `last_gc_run`
  * working tree                  to resolve each entry's anchors via
                                  `check_anchors.sh` (best-effort: missing
                                  anchors signal possible staleness)

…and emits a structured diff of proposed status transitions. It never writes
to MEMORY_INDEX.md. `gc_apply.py` consumes the same diff format.

Rules (v0.1, deliberately heuristic — LLM-grounded relevance is out of scope):

  active  -> dormant       last_referenced > STALE_DAYS days ago and
                           references == 0, OR every anchor is `missing`
  dormant -> deprecated    last_referenced > DEPRECATED_DAYS days ago and
                           references == 0
  superseded-by:<slug>     never touched by GC (user-owned signal)
  deprecated -> deprecated never demoted further (stable terminal status)

Defaults: STALE_DAYS=90, DEPRECATED_DAYS=180. Override with --stale / --deprecated.

Output (when --json): a transactional diff document:
  {
    "version": 1,
    "generated_at": "YYYY-MM-DD",
    "memory_dir": "/abs/path/.workspace/memory",
    "today": "YYYY-MM-DD",
    "stale_days": 90, "deprecated_days": 180,
    "transitions": [
      {"name": "<file>.md", "from": "active", "to": "dormant", "reason": "..."},
      ...
    ],
    "kept": [
      {"name": "...", "status": "active", "reason": "fresh"}, ...
    ],
    "summary": {"transitions": N, "kept": M, "skipped_superseded": K}
  }

Without --json: a readable summary written to stdout.

Exit 0 on success (whether or not any transitions were proposed). Exit 2 on
environment errors (no memory dir, no MEMORY_INDEX.md). Pure stdlib.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path


REQUIRED_FIELDS = ("status", "last_referenced", "tokens", "anchors")
HEADING_RE = re.compile(r"^#{2,3}\s+(.+?)\s*$")
FIELD_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*)$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DEFAULT_STALE_DAYS = 90
DEFAULT_DEPRECATED_DAYS = 180


def _today_utc() -> _dt.date:
    return _dt.datetime.now(_dt.timezone.utc).date()


def _parse_date(value: object) -> _dt.date | None:
    if not isinstance(value, str) or not DATE_RE.match(value):
        return None
    try:
        return _dt.datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def parse_index(path: Path) -> tuple[dict, dict]:
    """Return (front, entries). Entries keyed by filename, in document order."""
    front: dict[str, str] = {}
    entries: dict[str, dict] = {}
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return front, entries

    i = 0
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            m = FIELD_RE.match(lines[i])
            if m and lines[i][:1] not in (" ", "\t"):
                front[m.group(1).strip().lower()] = m.group(2).strip()
            i += 1
        i += 1

    current: str | None = None
    for line in lines[i:]:
        h = HEADING_RE.match(line)
        if h:
            name = h.group(1).strip().strip("`").strip('"').strip("'").strip()
            name = os.path.normpath(name)
            if name not in entries:
                entries[name] = {}
            current = name
            continue
        if current is None:
            continue
        body = line.lstrip()
        if body.startswith("- "):
            body = body[2:]
        m = FIELD_RE.match(body)
        if m:
            key = m.group(1).strip().lower()
            if key in REQUIRED_FIELDS and key not in entries[current]:
                entries[current][key] = m.group(2).strip()
    return front, entries


def load_sidecar(memory_dir: Path) -> dict:
    sidecar = memory_dir / ".index_state.json"
    try:
        return json.loads(sidecar.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def anchor_signal(memory_dir: Path) -> dict[str, dict]:
    """Best-effort: call check_anchors.sh and parse its summary.

    Returns map: filename -> {"missing": int, "present": int, "na": int}.
    Falls back to an empty map if the helper isn't usable; absence of anchor
    data should not block GC proposals.
    """
    helper = Path(__file__).with_name("check_anchors.sh")
    if not helper.is_file():
        return {}
    try:
        proc = subprocess.run(
            [str(helper), "--dir", str(memory_dir), "--json"],
            capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return {}
    if proc.returncode not in (0, 1):
        # Exit 1 means it found broken anchors — still parseable.
        return {}
    raw = (proc.stdout or "").strip()
    if not raw:
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    result: dict[str, dict] = {}
    for entry in data.get("entries", []) if isinstance(data, dict) else []:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name")
        if not isinstance(name, str):
            continue
        result[name] = {
            "missing": int(entry.get("missing") or 0),
            "present": int(entry.get("present") or 0),
            "na": int(entry.get("na") or 0),
        }
    return result


def effective_last_ref(entry: dict, sidecar_files: dict, name: str) -> _dt.date | None:
    """Pick the newer of (index entry's last_referenced) and (sidecar's)."""
    candidates: list[_dt.date] = []
    d = _parse_date(entry.get("last_referenced"))
    if d:
        candidates.append(d)
    s = sidecar_files.get(name)
    if isinstance(s, dict):
        d2 = _parse_date(s.get("last_referenced"))
        if d2:
            candidates.append(d2)
    return max(candidates) if candidates else None


def propose(
    memory_dir: Path,
    stale_days: int,
    deprecated_days: int,
    today: _dt.date | None = None,
) -> dict:
    today = today or _today_utc()
    index_path = memory_dir / "MEMORY_INDEX.md"
    front, entries = parse_index(index_path)
    sidecar = load_sidecar(memory_dir)
    sidecar_files = sidecar.get("files") if isinstance(sidecar, dict) else {}
    if not isinstance(sidecar_files, dict):
        sidecar_files = {}
    anchors = anchor_signal(memory_dir)

    transitions: list[dict] = []
    kept: list[dict] = []
    skipped_superseded: list[str] = []

    for name, entry in entries.items():
        status = (entry.get("status") or "").strip()
        if not status:
            kept.append({"name": name, "status": "", "reason": "no status field"})
            continue
        if status.startswith("superseded-by:"):
            skipped_superseded.append(name)
            kept.append({"name": name, "status": status, "reason": "user-set supersession"})
            continue
        if status == "deprecated":
            kept.append({"name": name, "status": status, "reason": "deprecated is terminal"})
            continue

        last_ref = effective_last_ref(entry, sidecar_files, name)
        age_days = (today - last_ref).days if last_ref else None
        refs = 0
        s = sidecar_files.get(name)
        if isinstance(s, dict):
            refs = int(s.get("references") or 0)
        a = anchors.get(name) or {}
        all_anchors_missing = (
            a.get("present", 0) == 0
            and a.get("missing", 0) > 0
        )

        new_status: str | None = None
        reason: str = ""

        if status == "active":
            if age_days is not None and age_days > deprecated_days and refs == 0:
                new_status = "deprecated"
                reason = (
                    f"unused for {age_days}d (>{deprecated_days}d) and no references — "
                    "demoting active -> deprecated"
                )
            elif age_days is not None and age_days > stale_days and refs == 0:
                new_status = "dormant"
                reason = (
                    f"unused for {age_days}d (>{stale_days}d) and no references"
                )
            elif all_anchors_missing:
                new_status = "dormant"
                reason = (
                    f"all {a.get('missing', 0)} anchor(s) missing in the working tree"
                )
            elif age_days is None and refs == 0:
                new_status = "dormant"
                reason = "no last_referenced date and no captured references"
            else:
                kept.append({
                    "name": name,
                    "status": status,
                    "reason": (
                        f"fresh ({age_days}d, refs={refs})"
                        if age_days is not None else f"refs={refs}"
                    ),
                })
                continue
        elif status == "dormant":
            if age_days is not None and age_days > deprecated_days and refs == 0:
                new_status = "deprecated"
                reason = (
                    f"dormant >{deprecated_days}d ({age_days}d) with no references"
                )
            else:
                kept.append({
                    "name": name,
                    "status": status,
                    "reason": "dormant within threshold",
                })
                continue
        else:
            kept.append({
                "name": name,
                "status": status,
                "reason": "unknown status (not transitioned)",
            })
            continue

        transitions.append({
            "name": name,
            "from": status,
            "to": new_status,
            "reason": reason,
            "last_referenced": last_ref.isoformat() if last_ref else None,
            "references": refs,
            "anchors": a,
        })

    return {
        "version": 1,
        "generated_at": today.isoformat(),
        "memory_dir": str(memory_dir),
        "today": today.isoformat(),
        "stale_days": stale_days,
        "deprecated_days": deprecated_days,
        "auto_loaded_cap": front.get("auto_loaded_cap"),
        "transitions": transitions,
        "kept": kept,
        "summary": {
            "transitions": len(transitions),
            "kept": len(kept),
            "skipped_superseded": len(skipped_superseded),
        },
    }


def print_human(diff: dict, out=sys.stdout) -> None:
    today = diff["today"]
    summary = diff["summary"]
    print(f"Memory GC dry-run @ {today} ({diff['memory_dir']})", file=out)
    print(
        f"  thresholds: stale > {diff['stale_days']}d, "
        f"deprecated > {diff['deprecated_days']}d",
        file=out,
    )
    cap = diff.get("auto_loaded_cap")
    if cap:
        print(f"  auto_loaded_cap: {cap}", file=out)
    print("", file=out)
    if not diff["transitions"]:
        print("No status transitions proposed. Index is current.", file=out)
    else:
        print(f"Proposed transitions ({summary['transitions']}):", file=out)
        for t in diff["transitions"]:
            print(f"  - {t['name']}: {t['from']} -> {t['to']}", file=out)
            print(f"      reason: {t['reason']}", file=out)
    print("", file=out)
    print(
        f"Summary: {summary['transitions']} transition(s), "
        f"{summary['kept']} kept "
        f"({summary['skipped_superseded']} superseded — user-owned).",
        file=out,
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dir", help="memory directory (default: <git root or cwd>/.workspace/memory)")
    ap.add_argument("--stale", type=int, default=DEFAULT_STALE_DAYS,
                    help=f"days after which active -> dormant (default: {DEFAULT_STALE_DAYS})")
    ap.add_argument("--deprecated", type=int, default=DEFAULT_DEPRECATED_DAYS,
                    help=f"days after which dormant -> deprecated (default: {DEFAULT_DEPRECATED_DAYS})")
    ap.add_argument("--today", help="override today's date (YYYY-MM-DD, for tests)")
    ap.add_argument("--json", action="store_true", help="emit the diff as JSON")
    args = ap.parse_args(argv)

    memory_dir = Path(args.dir) if args.dir else None
    if memory_dir is None:
        try:
            root = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True, text=True, check=True,
            ).stdout.strip()
        except (OSError, subprocess.CalledProcessError):
            root = os.getcwd()
        memory_dir = Path(root) / ".workspace" / "memory"
    memory_dir = memory_dir.resolve()

    if not memory_dir.is_dir():
        sys.stderr.write(f"gc_propose.py: memory directory not found: {memory_dir}\n")
        return 2
    if not (memory_dir / "MEMORY_INDEX.md").is_file():
        sys.stderr.write(
            f"gc_propose.py: no MEMORY_INDEX.md in {memory_dir} — "
            "run bin/memory_init_index.sh first.\n"
        )
        return 2

    today = _parse_date(args.today) if args.today else None
    diff = propose(memory_dir, args.stale, args.deprecated, today=today)

    if args.json:
        json.dump(diff, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print_human(diff)
    return 0


if __name__ == "__main__":
    sys.exit(main())
