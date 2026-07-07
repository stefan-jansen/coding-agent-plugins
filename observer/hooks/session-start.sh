#!/bin/bash
# Observer: Inject past session context at startup
# SessionStart hook — queries SQLite, returns hookSpecificOutput
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Also process any orphaned buffers from previous sessions
# (handles case where SessionEnd processing failed)
BUFFER_DIR="$HOME/.claude-toolkit/observer/buffers"
if [ -d "$BUFFER_DIR" ]; then
    for buf in "$BUFFER_DIR"/*.jsonl; do
        [ -f "$buf" ] || continue
        # Only process buffers older than 60 seconds (avoid current session)
        if [ "$(find "$buf" -mmin +1 2>/dev/null)" ]; then
            SID=$(basename "$buf" .jsonl)
            # Extract cwd from first line of buffer
            BUF_CWD=$(head -1 "$buf" | python3 -c "import sys,json; print(json.loads(sys.stdin.read()).get('cwd',''))" 2>/dev/null)
            if [ -n "$BUF_CWD" ]; then
                nohup python3 "$SCRIPT_DIR/../scripts/process.py" "$SID" "$BUF_CWD" \
                    >> "$HOME/.claude-toolkit/observer/errors.log" 2>&1 &
            fi
        fi
    done
fi

# Generate context from database
CONTEXT=$(python3 "$SCRIPT_DIR/../scripts/inject.py" 2>/dev/null)

if [ -n "$CONTEXT" ]; then
    # Escape markdown for JSON embedding
    ESCAPED=$(python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))" <<< "$CONTEXT" 2>/dev/null)
    if [ -n "$ESCAPED" ]; then
        echo "{\"hookSpecificOutput\":{\"hookEventName\":\"SessionStart\",\"additionalContext\":${ESCAPED}}}"
    fi
fi

exit 0
