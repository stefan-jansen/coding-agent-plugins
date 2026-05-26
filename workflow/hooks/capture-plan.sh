#!/bin/bash
# PostToolUse hook for ExitPlanMode
# Auto-captures the latest plan from ~/.claude/plans/ to the active work unit.
#
# Wired via project settings.json:
#   "PostToolUse": [{ "matcher": "ExitPlanMode", "hooks": [...] }]

set -e

PLAN_DIR="$HOME/.claude/plans"
WORK_DIR=".workspace/work"

# Find most recent plan (cross-platform: works on both Linux and macOS)
LATEST=$(ls -t "$PLAN_DIR"/*.md 2>/dev/null | head -1)
[ -z "$LATEST" ] && exit 0

# Get or create work unit
if [ -f "$WORK_DIR/ACTIVE_WORK" ]; then
  UNIT=$(cat "$WORK_DIR/ACTIVE_WORK")
else
  # Auto-create work unit from plan filename
  TOPIC=$(basename "$LATEST" .md | tr '_' '-')
  SEQ=$(ls -d "$WORK_DIR"/$(date +%Y-%m-%d)-* 2>/dev/null | wc -l)
  SEQ=$(printf "%02d" $((SEQ + 1)))
  UNIT="$(date +%Y-%m-%d)-${SEQ}-${TOPIC}"
  mkdir -p "$WORK_DIR/$UNIT"
  echo '{"status":"planning","topic":"'"$TOPIC"'"}' > "$WORK_DIR/$UNIT/metadata.json"
  echo "$UNIT" > "$WORK_DIR/ACTIVE_WORK"
fi

# Copy plan to work unit
mkdir -p "$WORK_DIR/$UNIT"
cp "$LATEST" "$WORK_DIR/$UNIT/plan.md"

echo "Plan captured: $WORK_DIR/$UNIT/plan.md"
