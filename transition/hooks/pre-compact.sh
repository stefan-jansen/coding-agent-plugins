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
When compacting this conversation, ensure the summary preserves:
1. Current task and its status (what's done, what's in progress, what's next)
2. Key decisions made and their rationale
3. File paths actively being modified
4. Any errors or blockers encountered and their resolution status
5. Open questions or items waiting on user input
These details are critical for session continuity after compaction.
EOF

# Memory-relevance nudge (additive — only emits when the project opts in by
# having a memory plugin sidecar, and only when /memory-gc is stale).
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
SIDECAR="$PROJECT_ROOT/.workspace/memory/.index_state.json"
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
