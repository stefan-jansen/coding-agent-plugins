#!/bin/bash
# PostCompact hook: save the compact summary to a transition file
#
# Receives JSON on stdin with:
#   { "trigger": "manual"|"auto", "compact_summary": "..." }
#
# Writes the summary to a timestamped .workspace/transitions/YYYY-MM-DD/HHMMSS.md
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

# Write to a timestamped transition file at .workspace/transitions/.
# Timestamped (HHMMSS.md) is the standard for all transition files, matching
# /handoff — one file per event, no hour-based grouping.
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
TODAY=$(date +%Y-%m-%d)
STAMP=$(date +%H%M%S)
NOW=$(date +%H:%M:%S)
DIR="$PROJECT_ROOT/.workspace/transitions/$TODAY"
FILE="$DIR/${STAMP}.md"

mkdir -p "$DIR"

cat > "$FILE" << EOF
# Compact summary ($TRIGGER) - $TODAY $NOW

$SUMMARY
EOF

exit 0
