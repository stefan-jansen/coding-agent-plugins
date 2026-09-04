#!/bin/bash
# Initialize hourly transition file for session progress tracking.
# Runs on UserPromptSubmit; idempotent and silent in the happy path.
# Routes to $CLAUDE_TRANSITIONS_DIR when set, else .workspace/transitions/
# (shared with Codex); falls back to .claude/transitions/ only when
# .workspace/ is absent (legacy projects).

set -e

PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"

# $CLAUDE_TRANSITIONS_DIR (absolute, or relative to the project root) wins;
# then .workspace/transitions/; then the legacy .claude/transitions/. Mirrors
# memory/bin/memory_dir.py's $CLAUDE_MEMORY_DIR rule, kept inline so this
# script stands alone.
if [ -n "${CLAUDE_TRANSITIONS_DIR:-}" ]; then
    case "$CLAUDE_TRANSITIONS_DIR" in
        /*) TRANSITIONS_DIR="$CLAUDE_TRANSITIONS_DIR" ;;
        *)  TRANSITIONS_DIR="$PROJECT_ROOT/$CLAUDE_TRANSITIONS_DIR" ;;
    esac
elif [ -d "$PROJECT_ROOT/.workspace" ]; then
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
