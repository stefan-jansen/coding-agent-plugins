#!/bin/bash
# SessionEnd hook: mark session exit in transition file
#
# Receives JSON on stdin with:
#   { "reason": "clear"|"logout"|"prompt_input_exit"|"other" }
#
# Appends a session-end marker to today's most-recent transition file under
# .workspace/transitions/YYYY-MM-DD/ (or does nothing if none exists).

INPUT=$(cat)

REASON=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.loads(sys.stdin.read())
    print(data.get('reason', 'unknown'))
except: print('unknown')
" 2>/dev/null)

# Append a session-end marker to today's most-recent transition file. If none
# exists (the session never compacted / wrote a handoff), do nothing — a bare
# "session ended" file is the thin-file anti-pattern that got the hourly-stub
# hook removed on 2026-08-05. The marker annotates a real record; it isn't one.
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
TODAY=$(date +%Y-%m-%d)
NOW=$(date +%H:%M:%S)
DIR="$PROJECT_ROOT/.workspace/transitions/$TODAY"

LATEST=$(ls -t "$DIR"/*.md 2>/dev/null | head -1)
[ -z "$LATEST" ] && exit 0

printf '\n## %s - Session ended (%s)\n' "$NOW" "$REASON" >> "$LATEST"

exit 0
