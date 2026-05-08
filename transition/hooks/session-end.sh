#!/bin/bash
# SessionEnd hook: mark session exit in transition file
#
# Receives JSON on stdin with:
#   { "reason": "clear"|"logout"|"prompt_input_exit"|"other" }
#
# Appends a session-end marker to the current transition file at
# .agents/transitions/YYYY-MM-DD/HH.md.

INPUT=$(cat)

REASON=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.loads(sys.stdin.read())
    print(data.get('reason', 'unknown'))
except: print('unknown')
" 2>/dev/null)

PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
TODAY=$(date +%Y-%m-%d)
HOUR=$(date +%H)
NOW=$(date +%H:%M)
DIR="$PROJECT_ROOT/.agents/transitions/$TODAY"
FILE="$DIR/${HOUR}.md"

mkdir -p "$DIR"

# Initialize file if it doesn't exist
if [ ! -f "$FILE" ]; then
    echo "# Session Progress: $TODAY ${HOUR}:00" > "$FILE"
    echo "" >> "$FILE"
    echo "---" >> "$FILE"
    echo "" >> "$FILE"
fi

# Append session-end marker
echo "" >> "$FILE"
echo "## $NOW - Session ended ($REASON)" >> "$FILE"
echo "" >> "$FILE"

exit 0
