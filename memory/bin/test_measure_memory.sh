#!/usr/bin/env bash
# test_measure_memory.sh — self-contained tests for token_count.py and
# measure_memory.sh. Pure stdlib; builds fixtures in a temp dir, no network,
# no third-party deps. Run: bash memory/bin/test_measure_memory.sh
set -euo pipefail

BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOKEN_PY="$BIN_DIR/token_count.py"
MEASURE="$BIN_DIR/measure_memory.sh"

PASS=0
FAIL=0
check() { # check <desc> <expected> <actual>
    if [[ "$2" == "$3" ]]; then
        PASS=$((PASS + 1)); echo "  ok: $1"
    else
        FAIL=$((FAIL + 1)); echo "  FAIL: $1 (expected '$2', got '$3')"
    fi
}

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

echo "== token_count.py =="
# 8 chars -> ceil(8/4) = 2 tokens; trailing newline from printf? use -n.
printf 'abcdefgh' > "$WORK/eight.txt"
check "8 chars => 2 tokens" "2" "$(python3 "$TOKEN_PY" "$WORK/eight.txt")"
# 9 chars -> ceil(9/4) = 3 tokens (rounds up).
printf '123456789' > "$WORK/nine.txt"
check "9 chars => 3 tokens (round up)" "3" "$(python3 "$TOKEN_PY" "$WORK/nine.txt")"
# Empty file => 0 tokens.
: > "$WORK/empty.txt"
check "empty => 0 tokens" "0" "$(python3 "$TOKEN_PY" "$WORK/empty.txt")"
# Missing file => 0, no crash.
check "missing => 0 tokens" "0" "$(python3 "$TOKEN_PY" "$WORK/nope.txt")"
# Summed total over multiple files = 2 + 3 = 5.
check "sum of files" "5" "$(python3 "$TOKEN_PY" "$WORK/eight.txt" "$WORK/nine.txt")"
# stdin path.
check "stdin counting" "2" "$(printf 'abcdefgh' | python3 "$TOKEN_PY")"

echo "== measure_memory.sh single project (@-include walk) =="
PROJ="$WORK/proj"
mkdir -p "$PROJ/.workspace/memory"
# CLAUDE.md just includes AGENTS.md (the convention).
printf '@AGENTS.md\n' > "$PROJ/CLAUDE.md"
# AGENTS.md: two real includes + a prose mention + a fenced mention + a missing include.
cat > "$PROJ/AGENTS.md" <<'EOF'
# Project

Prose mentioning @.workspace/memory/decoy.md should NOT be followed.

@.workspace/memory/a.md
@.workspace/memory/b.md
@.workspace/memory/missing.md

```
@.workspace/memory/decoy.md
```
EOF
printf 'aaaaaaaa' > "$PROJ/.workspace/memory/a.md"       # 2 tokens
printf 'bbbbbbbbbbbb' > "$PROJ/.workspace/memory/b.md"   # 3 tokens
printf 'DECOY-SHOULD-NOT-COUNT-EVER' > "$PROJ/.workspace/memory/decoy.md"

# Expected set = CLAUDE.md + AGENTS.md + a.md + b.md (decoy & missing excluded).
EXPECTED="$(python3 "$TOKEN_PY" \
    "$PROJ/CLAUDE.md" "$PROJ/AGENTS.md" \
    "$PROJ/.workspace/memory/a.md" "$PROJ/.workspace/memory/b.md")"
ACTUAL="$(cd "$PROJ" && "$MEASURE" --total-only)"
check "total matches exact reachable set" "$EXPECTED" "$ACTUAL"

# Decoy must not be counted: total+decoy must differ from actual.
WITH_DECOY="$(python3 "$TOKEN_PY" \
    "$PROJ/CLAUDE.md" "$PROJ/AGENTS.md" \
    "$PROJ/.workspace/memory/a.md" "$PROJ/.workspace/memory/b.md" \
    "$PROJ/.workspace/memory/decoy.md")"
if [[ "$WITH_DECOY" == "$ACTUAL" ]]; then
    FAIL=$((FAIL + 1)); echo "  FAIL: decoy appears to be counted"
else
    PASS=$((PASS + 1)); echo "  ok: decoy excluded"
fi

# Human-readable mode reports the missing include and the file count (4).
REPORT="$(cd "$PROJ" && "$MEASURE")"
check "reports 4 files" "1" "$(grep -c '4 files)' <<<"$REPORT")"
check "reports unresolved include" "1" "$(grep -c 'missing.md' <<<"$REPORT")"

echo "== measure_memory.sh --all-projects (incl. project lacking memory) =="
ROOT="$WORK/tree"
mkdir -p "$ROOT/with/.workspace/memory" "$ROOT/without"
printf '@AGENTS.md\n' > "$ROOT/with/CLAUDE.md"
printf '@.workspace/memory/x.md\n' > "$ROOT/with/AGENTS.md"
printf 'xxxxxxxx' > "$ROOT/with/.workspace/memory/x.md"
# A project with AGENTS.md but no memory includes at all -> must not crash.
printf '# no includes here\n' > "$ROOT/without/AGENTS.md"
ALL="$("$MEASURE" --all-projects --root "$ROOT")"
check "lists project with memory" "1" "$(grep -c "$ROOT/with\$" <<<"$ALL")"
check "lists project lacking memory" "1" "$(grep -c "$ROOT/without\$" <<<"$ALL")"
check "enumerated 2 projects" "1" "$(grep -c '2 project(s)' <<<"$ALL")"

echo
echo "Passed: $PASS  Failed: $FAIL"
[[ "$FAIL" -eq 0 ]]
