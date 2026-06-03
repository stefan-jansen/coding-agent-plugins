#!/usr/bin/env python3
"""memory_review.py — index-aware summary for /memory-review.

Reads MEMORY_INDEX.md + .index_state.json and prints:

  * per-entry table: status, last_referenced, tokens, anchors-summary
  * counts by status (active / dormant / deprecated / superseded-by:*)
  * total auto-loaded tokens vs `auto_loaded_cap` (from the index frontmatter)
  * last_gc_run + age in days (for the SessionStart-nudge context)

Recognizes both `.workspace/memory/` (managed) and Claude's auto-memory
shape at `~/.claude/projects/<slug>/memory/` (display-only — listed but
not analyzed for status, because we don't manage it).

Pure stdlib. Exit 0 on success; 2 on missing memory dir / index.
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

# Reuse parse_index from gc_propose so the parsing logic is shared.
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
from gc_propose import parse_index, load_sidecar, _parse_date  # noqa: E402


DISPLAY_ONLY_RE = re.compile(r"[\\/]\.claude[\\/]projects[\\/][^\\/]+[\\/]memory[\\/]?$")


def _today_utc() -> _dt.date:
    return _dt.datetime.now(_dt.timezone.utc).date()


def _effective_last_ref(entry: dict, sidecar_files: dict, name: str) -> str | None:
    """Newer of (index entry's last_referenced) and (sidecar's)."""
    candidates: list[_dt.date] = []
    for source in (entry.get("last_referenced"), (sidecar_files.get(name) or {}).get("last_referenced") if isinstance(sidecar_files.get(name), dict) else None):
        d = _parse_date(source)
        if d:
            candidates.append(d)
    return max(candidates).isoformat() if candidates else None


def _is_display_only(memory_dir: Path) -> bool:
    return bool(DISPLAY_ONLY_RE.search(str(memory_dir)))


def review(memory_dir: Path, out=sys.stdout) -> int:
    if not memory_dir.is_dir():
        print(f"memory_review: no memory directory at {memory_dir}", file=sys.stderr)
        return 2

    index_path = memory_dir / "MEMORY_INDEX.md"

    if _is_display_only(memory_dir):
        files = sorted(p.name for p in memory_dir.glob("*.md") if p.name != "MEMORY_INDEX.md")
        print(f"Display-only memory shape (Claude auto-memory): {memory_dir}", file=out)
        print(f"  {len(files)} file(s); status/index not managed for this path.", file=out)
        for name in files:
            print(f"    - {name}", file=out)
        return 0

    if not index_path.is_file():
        print(f"memory_review: no MEMORY_INDEX.md in {memory_dir}", file=sys.stderr)
        print("  initialize with: bash bin/memory_init_index.sh", file=sys.stderr)
        return 2

    front, entries = parse_index(index_path)
    sidecar = load_sidecar(memory_dir)
    sidecar_files = sidecar.get("files") or {}
    if not isinstance(sidecar_files, dict):
        sidecar_files = {}

    cap_raw = front.get("auto_loaded_cap")
    try:
        cap = int(cap_raw) if cap_raw is not None else None
    except (TypeError, ValueError):
        cap = None

    counts: dict[str, int] = {"active": 0, "dormant": 0, "deprecated": 0, "superseded": 0, "other": 0}
    total_tokens = 0
    rows: list[tuple[str, str, str, str, str]] = []

    today = _today_utc()
    for name, entry in entries.items():
        status = (entry.get("status") or "").strip() or "(none)"
        if status == "active":
            counts["active"] += 1
        elif status == "dormant":
            counts["dormant"] += 1
        elif status == "deprecated":
            counts["deprecated"] += 1
        elif status.startswith("superseded-by:"):
            counts["superseded"] += 1
        else:
            counts["other"] += 1

        try:
            tokens = int(entry.get("tokens") or 0)
        except (TypeError, ValueError):
            tokens = 0
        total_tokens += tokens

        eff_last = _effective_last_ref(entry, sidecar_files, name) or "-"
        age = "-"
        d = _parse_date(eff_last) if eff_last != "-" else None
        if d:
            age = f"{(today - d).days}d"
        anchors = entry.get("anchors") or "-"
        rows.append((name, status, eff_last, f"{tokens}t", anchors if len(anchors) < 40 else anchors[:37] + "..."))

    # Output -----------------------------------------------------------------
    print(f"Memory Review @ {today.isoformat()} ({memory_dir})", file=out)
    print(f"  {len(entries)} index entries", file=out)
    print("", file=out)

    if rows:
        widths = [max(len(r[i]) for r in rows) for i in range(5)]
        # Header
        hdr = ["file", "status", "last_ref", "tokens", "anchors"]
        widths = [max(w, len(h)) for w, h in zip(widths, hdr)]
        fmt = "  " + "  ".join(f"{{:<{w}}}" for w in widths)
        print(fmt.format(*hdr), file=out)
        print("  " + "  ".join("-" * w for w in widths), file=out)
        for r in rows:
            print(fmt.format(*r), file=out)
        print("", file=out)

    print(
        f"Status counts: active={counts['active']}  "
        f"dormant={counts['dormant']}  deprecated={counts['deprecated']}  "
        f"superseded={counts['superseded']}"
        + (f"  other={counts['other']}" if counts["other"] else ""),
        file=out,
    )

    # Per-entry inventory total (what could be loaded on demand). Distinct
    # from the auto-loaded total — that's what measure_memory.sh reports
    # against the cap. We try to call measure_memory.sh for the auto-loaded
    # figure; fall back to the inventory total if it isn't reachable (e.g.
    # the script lives outside the bin/ dir we were imported from).
    print(f"Inventory tokens (all index entries): {total_tokens}", file=out)
    measure = _HERE / "measure_memory.sh"
    auto_loaded: int | None = None
    if measure.is_file():
        # measure_memory.sh reads from $PWD (or git root); invoke with cwd
        # set to the project root.
        project_root = memory_dir.parent.parent
        try:
            proc = subprocess.run(
                [str(measure), "--total-only"],
                cwd=str(project_root),
                capture_output=True, text=True, timeout=10,
            )
            if proc.returncode == 0 and proc.stdout.strip().isdigit():
                auto_loaded = int(proc.stdout.strip())
        except (OSError, subprocess.SubprocessError, ValueError):
            auto_loaded = None
    if cap is not None and auto_loaded is not None:
        pct = round(100 * auto_loaded / cap, 1) if cap else 0
        marker = "OK" if auto_loaded <= cap else "OVER CAP"
        print(f"Auto-loaded: {auto_loaded} / {cap} cap  ({pct}%)  [{marker}]", file=out)
    elif cap is not None:
        print(f"Auto-loaded: <unknown>  /  {cap} cap (measure_memory.sh unavailable)", file=out)
    elif auto_loaded is not None:
        print(f"Auto-loaded: {auto_loaded} (no auto_loaded_cap set in frontmatter)", file=out)
    else:
        print("Auto-loaded: <unknown> (no measure_memory.sh, no cap set)", file=out)

    last_gc = sidecar.get("last_gc_run") if isinstance(sidecar, dict) else None
    last_gc_d = _parse_date(last_gc)
    if last_gc_d:
        print(f"last_gc_run: {last_gc} ({(today - last_gc_d).days}d ago)", file=out)
    else:
        print("last_gc_run: never (run /memory-gc to refresh)", file=out)

    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dir", help="memory directory (default: <git root or cwd>/.workspace/memory)")
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

    return review(memory_dir)


if __name__ == "__main__":
    sys.exit(main())
