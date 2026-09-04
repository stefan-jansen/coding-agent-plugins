#!/usr/bin/env bash
# Behavioral test: the transition hooks must honour $CLAUDE_TRANSITIONS_DIR and
# fall back to .workspace/transitions/ (then legacy .claude/transitions/).
# Runs the real hooks against throwaway project roots and asserts where the
# files actually land.
set -uo pipefail

HOOKS="$(cd "$(dirname "${BASH_SOURCE[0]}")/../hooks" && pwd)"
TODAY=$(date +%Y-%m-%d)
PASS=0; FAIL=0

check() {  # check <label> <expected-path-glob>
    if compgen -G "$2" > /dev/null; then
        echo "  ok   $1"; PASS=$((PASS+1))
    else
        echo "  FAIL $1 (nothing at $2)"; FAIL=$((FAIL+1))
    fi
}
refute() {
    if compgen -G "$2" > /dev/null; then
        echo "  FAIL $1 (unexpected file at $2)"; FAIL=$((FAIL+1))
    else
        echo "  ok   $1"; PASS=$((PASS+1))
    fi
}

newroot() { local d; d=$(mktemp -d); mkdir -p "$d/.workspace"; echo "$d"; }
SUMMARY='{"trigger":"manual","compact_summary":"test summary body"}'

echo "post-compact.sh"
R=$(newroot)
CLAUDE_PROJECT_DIR="$R" bash "$HOOKS/post-compact.sh" <<<"$SUMMARY" >/dev/null
check "default -> .workspace/transitions" "$R/.workspace/transitions/$TODAY/*.md"
rm -rf "$R"

R=$(newroot)
CLAUDE_PROJECT_DIR="$R" CLAUDE_TRANSITIONS_DIR="transitions" \
    bash "$HOOKS/post-compact.sh" <<<"$SUMMARY" >/dev/null
check  "relative override -> <root>/transitions" "$R/transitions/$TODAY/*.md"
refute "relative override leaves .workspace empty" "$R/.workspace/transitions/$TODAY/*.md"
rm -rf "$R"

R=$(newroot); ABS=$(mktemp -d)
CLAUDE_PROJECT_DIR="$R" CLAUDE_TRANSITIONS_DIR="$ABS" \
    bash "$HOOKS/post-compact.sh" <<<"$SUMMARY" >/dev/null
check "absolute override -> that path" "$ABS/$TODAY/*.md"
rm -rf "$R" "$ABS"

echo "session-end.sh"
R=$(newroot)
CLAUDE_PROJECT_DIR="$R" CLAUDE_TRANSITIONS_DIR="transitions" \
    bash "$HOOKS/post-compact.sh" <<<"$SUMMARY" >/dev/null
CLAUDE_PROJECT_DIR="$R" CLAUDE_TRANSITIONS_DIR="transitions" \
    bash "$HOOKS/session-end.sh" <<<'{"reason":"clear"}' >/dev/null
if grep -q "Session ended (clear)" "$R"/transitions/"$TODAY"/*.md 2>/dev/null; then
    echo "  ok   annotates the overridden dir"; PASS=$((PASS+1))
else
    echo "  FAIL annotates the overridden dir"; FAIL=$((FAIL+1))
fi
rm -rf "$R"

echo "init-transition.sh"
R=$(newroot)
CLAUDE_PROJECT_DIR="$R" CLAUDE_TRANSITIONS_DIR="transitions" bash "$HOOKS/init-transition.sh"
check "override wins over .workspace" "$R/transitions/$TODAY/*.md"
rm -rf "$R"

R=$(mktemp -d)   # no .workspace/ -> legacy fallback
CLAUDE_PROJECT_DIR="$R" bash "$HOOKS/init-transition.sh"
check "no .workspace -> legacy .claude/transitions" "$R/.claude/transitions/$TODAY/*.md"
rm -rf "$R"

echo
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
