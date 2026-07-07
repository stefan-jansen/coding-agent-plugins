#!/bin/bash
# Initialize hourly transition file for session progress tracking.
# Runs on UserPromptSubmit; idempotent and silent in the happy path.
# Routes to .workspace/transitions/ (shared with Codex); falls back to
# .claude/transitions/ only when .workspace/ is absent (legacy projects).

set -e

PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

if [ -d "$PROJECT_ROOT/.workspace" ]; then
    TRANSITIONS_DIR="$PROJECT_ROOT/.workspace/transitions"
else
    TRANSITIONS_DIR="$PROJECT_ROOT/.claude/transitions"
fi

TODAY=$(date +%Y-%m-%d)
HOUR=$(date +%H)
TODAY_DIR="$TRANSITIONS_DIR/$TODAY"
HOURLY_FILE="$TODAY_DIR/${HOUR}.md"

mkdir -p "$TODAY_DIR"

if [ ! -f "$HOURLY_FILE" ]; then
    cat > "$HOURLY_FILE" << EOF
# Session Progress: $TODAY ${HOUR}:00

---

EOF
fi

exit 0
