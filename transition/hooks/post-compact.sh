#!/bin/bash
# PostCompact hook: save the compact summary to a transition file
#
# Receives JSON on stdin with:
#   { "trigger": "manual"|"auto", "compact_summary": "..." }
#
# Writes the summary to .workspace/transitions/YYYY-MM-DD/HH.md
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

# Write to transition file at .workspace/transitions/
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
TODAY=$(date +%Y-%m-%d)
HOUR=$(date +%H)
NOW=$(date +%H:%M)
DIR="$PROJECT_ROOT/.workspace/transitions/$TODAY"
FILE="$DIR/${HOUR}.md"

mkdir -p "$DIR"

# Initialize file if it doesn't exist
if [ ! -f "$FILE" ]; then
    echo "# Session Progress: $TODAY ${HOUR}:00" > "$FILE"
    echo "" >> "$FILE"
    echo "---" >> "$FILE"
    echo "" >> "$FILE"
fi

# Append compact summary
cat >> "$FILE" << EOF

## $NOW - Compact Summary ($TRIGGER)

$SUMMARY

---

EOF

exit 0
