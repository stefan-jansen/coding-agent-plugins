#!/bin/bash
# Observer: Trigger background observation processing
# SessionEnd hook — spawns process.py in background, never blocks
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Read hook context from stdin
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read()).get('session_id',''))" 2>/dev/null)
CWD=$(echo "$INPUT" | python3 -c "import sys,json; print(json.loads(sys.stdin.read()).get('cwd',''))" 2>/dev/null)

# Skip if no session ID
[ -z "$SESSION_ID" ] && exit 0

BUFFER="$HOME/.claude-toolkit/observer/buffers/${SESSION_ID}.jsonl"

# Only process if buffer exists and has content
if [ -f "$BUFFER" ] && [ -s "$BUFFER" ]; then
    nohup python3 "$SCRIPT_DIR/../scripts/process.py" "$SESSION_ID" "$CWD" \
        >> "$HOME/.claude-toolkit/observer/errors.log" 2>&1 &
fi

exit 0
