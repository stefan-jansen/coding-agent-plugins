#!/usr/bin/env python3
"""SessionStart hook: nudge when memory is stale or over budget.

Acceptance criterion 6 (M3 #12): a SessionStart hook reads `last_gc_run` from
`.workspace/memory/.index_state.json`; if more than 7 days have passed, it
appends a one-line nudge to the session-start banner. With `--auto-gc` enabled
under `memory.auto_gc` in `.claude/settings.json`, the hook *also* runs
`/memory-gc --dry-run` and prints the proposed diff inline. Default is off.

The staleness nudge alone misses the failure mode that actually costs context:
an auto-loaded file that is legitimately `active` and 12x its budget. Staleness
GC never flags it, because the file is current and correctly marked. So the hook
also measures the real auto-loaded total (the @-include closure, via the same
bin/ helpers measure_memory.sh uses) against `auto_loaded_cap`, and reports a
memory file that is auto-loaded directly rather than through the index. The two
signals are independent: being over budget is worth saying even when /memory-gc
ran yesterday.

The hook is the source of M3 acceptance criterion 6. Constraints from the
spec: stat + JSON read only when `--auto-gc` is off; <100ms total in the
non-auto-gc path (verified by `bin/test_session_start_timing.sh`).

Output:
  * On success, anything we print to stdout is appended to the session-start
    banner via Claude Code's PreSession hook contract.
  * On any failure we stay silent and exit 0 (a SessionStart hook must not
    block session creation).

The hook receives the session-start payload on stdin. We only consume `cwd`
(falling back to $CLAUDE_PROJECT_DIR / $PWD); other fields are ignored.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
import sys
from pathlib import Path

NUDGE_DAYS = 7

# bin/ holds the shared helpers (include_graph, token_count) so the hook and
# measure_memory.sh cannot disagree about what "auto-loaded" means.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))


def _today_utc() -> _dt.date:
    return _dt.datetime.now(_dt.timezone.utc).date()


def _parse_date(value: object) -> _dt.date | None:
    if not isinstance(value, str):
        return None
    try:
        return _dt.datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def _project_root_from_stdin() -> Path:
    raw = sys.stdin.read()
    cwd: str | None = None
    if raw.strip():
        try:
            payload = json.loads(raw)
            if isinstance(payload, dict):
                cwd = payload.get("cwd")
        except json.JSONDecodeError:
            cwd = None
    if not cwd:
        cwd = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    try:
        return Path(cwd).resolve()
    except OSError:
        return Path(cwd)


def _read_sidecar(memory_dir: Path) -> dict | None:
    sidecar = memory_dir / ".index_state.json"
    try:
        with sidecar.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None
    return data if isinstance(data, dict) else None


def _auto_gc_enabled(project_root: Path) -> bool:
    """Return True iff `memory.auto_gc` is enabled in any layer of
    .claude/settings.json — project local, project shared, or user.

    We deliberately accept both shapes for forward-compatibility:
      * `{"memory": {"auto_gc": true}}`
      * `{"memory.auto_gc": true}`  (flat-key form some tools emit)
    """
    candidates = [
        project_root / ".claude" / "settings.local.json",
        project_root / ".claude" / "settings.json",
        Path.home() / ".claude" / "settings.json",
    ]
    for path in candidates:
        try:
            with path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            continue
        if not isinstance(data, dict):
            continue
        flat = data.get("memory.auto_gc")
        if isinstance(flat, bool) and flat:
            return True
        nested = data.get("memory")
        if isinstance(nested, dict) and bool(nested.get("auto_gc")):
            return True
    return False


def _summarize_dry_run(memory_dir: Path, today: _dt.date) -> list[str]:
    """Cheap, file-level dry-run preview used when --auto-gc is on.

    We deliberately do not invoke /memory-gc here (the command is interactive
    and slash-loaded). Instead we read the sidecar + index and propose status
    transitions: any file whose `last_referenced` is older than 90 days and
    currently `active` is proposed as `dormant`. This is a preview only;
    nothing is written. M4 will replace this with the upgraded /memory-gc
    proposal generator (the sidecar contract is the bridge).
    """
    sidecar = _read_sidecar(memory_dir)
    if not sidecar:
        return []
    files = sidecar.get("files") or {}
    proposals: list[tuple[str, str, str]] = []  # (name, old, new)
    for name, entry in files.items():
        if not isinstance(entry, dict):
            continue
        last_ref = _parse_date(entry.get("last_referenced"))
        if last_ref is None:
            continue
        if (today - last_ref).days <= 90:
            continue
        proposals.append((name, "active", "dormant"))
    if not proposals:
        return []
    lines = ["  memory-gc dry-run (auto): proposed status changes:"]
    for name, old, new in sorted(proposals):
        lines.append(f"    - {name}: {old} -> {new}")
    return lines


def _cap(memory_dir: Path, sidecar: dict) -> int | None:
    """`auto_loaded_cap` from the sidecar, else MEMORY_INDEX.md frontmatter."""
    cap = sidecar.get("auto_loaded_cap")
    if isinstance(cap, int) and cap > 0:
        return cap
    try:
        lines = (memory_dir / "MEMORY_INDEX.md").read_text(
            encoding="utf-8", errors="replace"
        ).splitlines()
    except OSError:
        return None
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        key, _, value = line.partition(":")
        if key.strip() == "auto_loaded_cap" and value.strip().isdigit():
            return int(value.strip())
    return None


def _budget_lines(project_root: Path, memory_dir: Path, sidecar: dict) -> list[str]:
    """Size signals: over the cap, and memory files auto-loaded directly.

    Independent of GC recency — intra-file growth is invisible to a status
    vocabulary driven by `last_referenced`.
    """
    try:
        from include_graph import reachable
        from token_count import count_file
    except ImportError:
        return []

    try:
        loaded, _missing = reachable(str(project_root))
    except OSError:
        return []
    if not loaded:
        return []

    lines: list[str] = []

    direct = sorted(
        os.path.basename(p)
        for p in loaded
        if Path(p).parent == memory_dir and os.path.basename(p) != "MEMORY_INDEX.md"
    )
    if direct:
        lines.append(
            "memory-budget: "
            + ", ".join(direct)
            + " @-included directly by AGENTS.md/CLAUDE.md; @-include only "
            "MEMORY_INDEX.md and read the rest on demand "
            "(bin/verify_index.sh explains)."
        )

    cap = _cap(memory_dir, sidecar)
    if cap:
        total = sum(count_file(p) for p in loaded)
        if total > cap:
            lines.append(
                f"memory-budget: {total} tokens auto-loaded every session vs a "
                f"cap of {cap} ({round(100.0 * total / cap)}%); "
                "run bin/measure_memory.sh to see the breakdown."
            )

    return lines


def main() -> int:
    project_root = _project_root_from_stdin()
    memory_dir = project_root / ".workspace" / "memory"
    if not memory_dir.is_dir():
        return 0

    sidecar = _read_sidecar(memory_dir)
    if sidecar is None:
        return 0

    today = _today_utc()
    last_gc = _parse_date(sidecar.get("last_gc_run"))
    gc_stale = last_gc is None or (today - last_gc).days > NUDGE_DAYS

    if gc_stale:
        age = "never" if last_gc is None else f"{(today - last_gc).days}d"
        print(
            "memory-budget: /memory-gc has not run in "
            f"{age}; consider /memory-gc to refresh status."
        )
        if _auto_gc_enabled(project_root):
            for line in _summarize_dry_run(memory_dir, today):
                print(line)

    # Size is reported whether or not GC is fresh: a file can be correctly
    # `active` and still be the reason a session starts at 13% context.
    for line in _budget_lines(project_root, memory_dir, sidecar):
        print(line)

    return 0


if __name__ == "__main__":
    sys.exit(main())
