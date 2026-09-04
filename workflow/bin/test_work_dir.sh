#!/usr/bin/env bash
# Behavioral test: capture-plan.sh must honour $CLAUDE_WORK_DIR and otherwise
# fall back to .workspace/work/ relative to the cwd. Runs the real hook.
set -uo pipefail

HOOK="$(cd "$(dirname "${BASH_SOURCE[0]}")/../hooks" && pwd)/capture-plan.sh"
PASS=0; FAIL=0

check()  { if compgen -G "$2" >/dev/null; then echo "  ok   $1"; PASS=$((PASS+1)); else echo "  FAIL $1 (nothing at $2)"; FAIL=$((FAIL+1)); fi; }
refute() { if compgen -G "$2" >/dev/null; then echo "  FAIL $1 (unexpected $2)"; FAIL=$((FAIL+1)); else echo "  ok   $1"; PASS=$((PASS+1)); fi; }

payload() { printf '{"tool_response":{"plan":"# %s\\n\\nbody\\n"}}' "$1"; }

echo "capture-plan.sh"
R=$(mktemp -d)
( cd "$R" && CLAUDE_PROJECT_DIR="$R" bash "$HOOK" <<<"$(payload default-case)" ) 2>/dev/null
check "default -> .workspace/work/<unit>/plan.md" "$R/.workspace/work/"*"/plan.md"
rm -rf "$R"

R=$(mktemp -d)
( cd "$R" && CLAUDE_PROJECT_DIR="$R" CLAUDE_WORK_DIR="work" bash "$HOOK" <<<"$(payload rel-case)" ) 2>/dev/null
check  "relative override -> <root>/work/<unit>/plan.md" "$R/work/"*"/plan.md"
refute "relative override leaves .workspace/work unwritten" "$R/.workspace/work/"*"/plan.md"
rm -rf "$R"

R=$(mktemp -d); ABS=$(mktemp -d)
( cd "$R" && CLAUDE_PROJECT_DIR="$R" CLAUDE_WORK_DIR="$ABS" bash "$HOOK" <<<"$(payload abs-case)" ) 2>/dev/null
check "absolute override -> that path" "$ABS/"*"/plan.md"
rm -rf "$R" "$ABS"

# The override must be resolved against the project root, not the cwd, so a
# hook firing from a subdirectory still lands in one place.
R=$(mktemp -d); mkdir -p "$R/sub/dir"
( cd "$R/sub/dir" && CLAUDE_PROJECT_DIR="$R" CLAUDE_WORK_DIR="work" bash "$HOOK" <<<"$(payload subdir-case)" ) 2>/dev/null
check  "override anchors to project root, not cwd" "$R/work/"*"/plan.md"
refute "no stray unit under the subdirectory" "$R/sub/dir/work/"*"/plan.md"
rm -rf "$R"

# ACTIVE_WORK in the overridden directory must be the one that is honoured.
R=$(mktemp -d); mkdir -p "$R/work/pinned-unit"; echo "pinned-unit" > "$R/work/ACTIVE_WORK"
( cd "$R" && CLAUDE_PROJECT_DIR="$R" CLAUDE_WORK_DIR="work" bash "$HOOK" <<<"$(payload pinned)" ) 2>/dev/null
check "ACTIVE_WORK read from the overridden dir" "$R/work/pinned-unit/plan.md"
rm -rf "$R"

echo
echo "$PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
