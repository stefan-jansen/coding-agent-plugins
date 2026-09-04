#!/bin/bash
# PreCompact hook: inject custom instructions for the compact summary, and —
# situationally — also surface a memory-relevance nudge so compaction counts as
# an effective trigger for the memory-budget review (M3 acceptance criterion 6).
#
# Stdout becomes custom_instructions for the compaction — tells Claude what to
# emphasize in the summary it generates. We append the memory nudge as an
# extra instruction *only* when the project has the memory plugin's sidecar
# and last_gc_run is older than 7 days. The original custom-instructions
# output is unchanged in the common case.
#
# Exit 0: stdout appended as custom compact instructions
# Exit 2: block compaction (not used here)

cat << 'EOF'
Write the summary as a cold-startable handoff for the next agent, following the
same discipline as the `/handoff` skill (workflow plugin) — same target, so the
auto summary and a manual handoff read alike. Curate, do not transcribe.

Include: current task + status (done / in progress / next); key decisions and
their rationale; exact file paths touched and what changed in each; verification
state (tested / run / pushed vs pending, with evidence); open threads, blockers,
and anything waiting on the user.

Do NOT include (this is where auto-summaries bloat):
- Verbatim or message-by-message replay of the conversation.
- Routine tool mechanics — permission denials, retries, keystrokes, shell
  quoting, dead ends that were resolved and left no lasting state.
- Anything the next agent would re-derive from one `git log` / `gh issue list`,
  or that is already captured in "current state".

Terse but complete beats exhaustive. If a fact would not change what the next
agent does, leave it out.
EOF

# Memory-relevance nudge (additive — only emits when the project opts in by
# having a memory plugin sidecar, and only when /memory-gc is stale).
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
# $CLAUDE_MEMORY_DIR (absolute, or relative to the project root) then
# `.workspace/memory/`. Mirrors memory/bin/stamp_gc_run.sh and bin/memory_dir.py:
# a project that relocates its memory directory must not be read here at the
# default path, or the nudge reports the age of a directory nothing maintains.
if [[ -n "${CLAUDE_MEMORY_DIR:-}" ]]; then
    case "$CLAUDE_MEMORY_DIR" in
        /*) MEMORY_DIR="$CLAUDE_MEMORY_DIR" ;;
        *)  MEMORY_DIR="$PROJECT_ROOT/$CLAUDE_MEMORY_DIR" ;;
    esac
else
    MEMORY_DIR="$PROJECT_ROOT/.workspace/memory"
fi
SIDECAR="$MEMORY_DIR/.index_state.json"
if [[ -f "$SIDECAR" ]]; then
    python3 - "$SIDECAR" <<'PY' 2>/dev/null || true
import datetime as dt
import json
import sys
from pathlib import Path

sidecar = Path(sys.argv[1])
try:
    data = json.loads(sidecar.read_text(encoding="utf-8"))
except Exception:
    sys.exit(0)

last_gc = data.get("last_gc_run") if isinstance(data, dict) else None
try:
    last_gc_date = dt.datetime.strptime(last_gc, "%Y-%m-%d").date() if last_gc else None
except (TypeError, ValueError):
    last_gc_date = None

today = dt.datetime.now(dt.timezone.utc).date()
stale = last_gc_date is None or (today - last_gc_date).days > 7
if not stale:
    sys.exit(0)

age = "never" if last_gc_date is None else f"{(today - last_gc_date).days} days ago"
print()
print(
    "Additionally, note that /memory-gc has not run in this project "
    f"({age}); flag in the compact summary that a memory relevance "
    "review is overdue so the next session picks it up."
)
PY
fi

exit 0
