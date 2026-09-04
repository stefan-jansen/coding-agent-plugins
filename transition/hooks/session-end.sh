#!/bin/bash
# SessionEnd hook: mark session exit in transition file
#
# Receives JSON on stdin with:
#   { "reason": "clear"|"logout"|"prompt_input_exit"|"other" }
#
# Appends a session-end marker to today's most-recent transition file under
# <transitions>/YYYY-MM-DD/ (or does nothing if none exists), where
# <transitions> is $CLAUDE_TRANSITIONS_DIR or .workspace/transitions/.

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

LATEST=$(ls -t "$DIR"/*.md 2>/dev/null | head -1)
[ -z "$LATEST" ] && exit 0

printf '\n## %s - Session ended (%s)\n' "$NOW" "$REASON" >> "$LATEST"

exit 0
