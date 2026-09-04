#!/bin/bash
# PostCompact hook: save the compact summary to a transition file
#
# Receives JSON on stdin with:
#   { "trigger": "manual"|"auto", "compact_summary": "..." }
#
# Writes the summary to a timestamped <transitions>/YYYY-MM-DD/HHMMSS.md, where
# <transitions> is $CLAUDE_TRANSITIONS_DIR or .workspace/transitions/.
# The hook script does the file I/O — no Claude permissions needed.
#
# Exit 0: stdout shown to user (we stay silent)

INPUT=$(cat)

# Extract fields
SUMMARY=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.loads(sys.stdin.read())
    print(data.get('compact_summary', ''))
except: pass
" 2>/dev/null)

TRIGGER=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.loads(sys.stdin.read())
    print(data.get('trigger', 'unknown'))
except: print('unknown')
" 2>/dev/null)

# Skip if no summary
[ -z "$SUMMARY" ] && exit 0

# Write to a timestamped transition file under the transitions directory.
# Timestamped (HHMMSS.md) is the standard for all transition files, matching
# /handoff — one file per event, no hour-based grouping.
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
TODAY=$(date +%Y-%m-%d)
STAMP=$(date +%H%M%S)
NOW=$(date +%H:%M:%S)
# Resolve the transitions directory: $CLAUDE_TRANSITIONS_DIR (absolute, or
# relative to the project root), then the conventional `.workspace/transitions/`.
# Mirrors memory/bin/memory_dir.py's $CLAUDE_MEMORY_DIR rule; kept inline so
# each hook stands alone (no sourcing).
if [ -n "${CLAUDE_TRANSITIONS_DIR:-}" ]; then
    case "$CLAUDE_TRANSITIONS_DIR" in
        /*) TRANSITIONS_DIR="$CLAUDE_TRANSITIONS_DIR" ;;
        *)  TRANSITIONS_DIR="$PROJECT_ROOT/$CLAUDE_TRANSITIONS_DIR" ;;
    esac
else
    TRANSITIONS_DIR="$PROJECT_ROOT/.workspace/transitions"
fi

DIR="$TRANSITIONS_DIR/$TODAY"
FILE="$DIR/${STAMP}.md"

mkdir -p "$DIR"

cat > "$FILE" << EOF
# Compact summary ($TRIGGER) - $TODAY $NOW

$SUMMARY
EOF

exit 0
