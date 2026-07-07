#!/bin/bash
# PostToolUse hook for ExitPlanMode.
#
# Reads the hook payload JSON from stdin and writes the approved plan
# content into the active .workspace/work unit. Handles two Claude Code
# ExitPlanMode payload shapes:
#
#   Legacy (pre-2026-06):  {"tool_response": {"plan": "...markdown...", "filePath": "..."}}
#   Current (2026-06+):    {"tool_response": {"filePath": "/path/to/plan.md"}}  — plan content lives in the file
#
# Fix history:
#   2026-06-15  v2 — fall through to reading filePath when .plan is empty;
#               added ROBORUN_WORK_UNIT env override for cross-repo capture;
#               added ROBORUN_DEBUG_HOOKS payload logging for API-drift detection.
#
# Wired via project settings.json:
#   "PostToolUse": [{ "matcher": "ExitPlanMode", "hooks": [...] }]

set -e

WORK_DIR=".workspace/work"

if ! command -v jq >/dev/null 2>&1; then
  echo "capture-plan: jq not on PATH — payload cannot be parsed; skipping" >&2
  exit 0
fi

PAYLOAD=$(cat)

# Drift-detector: when ROBORUN_DEBUG_HOOKS=1, snapshot every payload so we
# can diff shapes after a Claude Code release. Cheap, off by default, and
# the only mechanism we have today to spot API changes proactively.
if [ -n "$ROBORUN_DEBUG_HOOKS" ]; then
  DEBUG_DIR="${ROBORUN_DEBUG_DIR:-$HOME/.claude/hooks/debug}"
  mkdir -p "$DEBUG_DIR"
  TS=$(date +%Y%m%dT%H%M%S)
  printf '%s' "$PAYLOAD" > "$DEBUG_DIR/exitplanmode-${TS}.json"
  echo "capture-plan: debug payload saved to $DEBUG_DIR/exitplanmode-${TS}.json" >&2
fi

PLAN=$(printf '%s' "$PAYLOAD" | jq -r '.tool_response.plan // empty')
PLAN_FILE=$(printf '%s' "$PAYLOAD" | jq -r '.tool_response.filePath // empty')

# New API: plan content lives in the file at filePath.
if [ -z "$PLAN" ] && [ -n "$PLAN_FILE" ] && [ -f "$PLAN_FILE" ]; then
  PLAN=$(cat "$PLAN_FILE")
fi

# Still nothing → payload shape we don't understand. Surface it loudly when
# debug is on, exit silently otherwise (must never break the host session).
if [ -z "$PLAN" ]; then
  if [ -n "$ROBORUN_DEBUG_HOOKS" ]; then
    KEYS=$(printf '%s' "$PAYLOAD" | jq -r '.tool_response | keys[]?' 2>/dev/null | paste -sd, -)
    echo "capture-plan: no plan content found. tool_response keys: [$KEYS]" >&2
    echo "capture-plan: this may indicate an ExitPlanMode API change — check debug payload" >&2
  fi
  exit 0
fi

# Env override: cross-repo planning. When set, write plan directly to the
# named work unit and skip cwd-based resolution. Allows planning in one
# session while the target work unit lives in a different repository.
if [ -n "$ROBORUN_WORK_UNIT" ]; then
  if [ ! -d "$ROBORUN_WORK_UNIT" ]; then
    echo "capture-plan: ROBORUN_WORK_UNIT does not exist: $ROBORUN_WORK_UNIT" >&2
    exit 0
  fi
  printf '%s' "$PLAN" > "$ROBORUN_WORK_UNIT/plan.md"
  echo "capture-plan: wrote $ROBORUN_WORK_UNIT/plan.md (env override)" >&2
  exit 0
fi

# Default path: resolve or create the active work unit under cwd.
if [ -f "$WORK_DIR/ACTIVE_WORK" ]; then
  UNIT=$(cat "$WORK_DIR/ACTIVE_WORK")
else
  if [ -n "$PLAN_FILE" ]; then
    TOPIC=$(basename "$PLAN_FILE" .md | tr '_' '-')
  else
    TOPIC=$(printf '%s' "$PLAN" | grep -m1 '^# ' | \
            sed 's/^# //; s/[^a-zA-Z0-9_-]/-/g; s/-\+/-/g; s/^-*//; s/-*$//' | \
            cut -c1-50)
  fi
  [ -z "$TOPIC" ] && TOPIC="session"
  SEQ=$(ls -d "$WORK_DIR"/$(date +%Y-%m-%d)-* 2>/dev/null | wc -l)
  SEQ=$(printf "%02d" $((SEQ + 1)))
  UNIT="$(date +%Y-%m-%d)-${SEQ}-${TOPIC}"
  mkdir -p "$WORK_DIR/$UNIT"
  printf '{"status":"planning","topic":"%s"}\n' "$TOPIC" > "$WORK_DIR/$UNIT/metadata.json"
  echo "$UNIT" > "$WORK_DIR/ACTIVE_WORK"
fi

mkdir -p "$WORK_DIR/$UNIT"
printf '%s' "$PLAN" > "$WORK_DIR/$UNIT/plan.md"

echo "capture-plan: wrote $WORK_DIR/$UNIT/plan.md" >&2
