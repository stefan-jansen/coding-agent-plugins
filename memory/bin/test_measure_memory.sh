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

# --------------------------------------------------------------------------
# Budget: auto_loaded_cap read from the sidecar / index frontmatter, reported
# always, enforced only under --check.
#
# mkbudget <name> <filler-bytes> -> echoes the project root. AGENTS.md
# @-includes one memory file of the requested size, so the total is tunable
# against a fixed cap of 1000 tokens.
mkbudget() {
    local name="$1" bytes="$2"
    local root="$WORK/$name" mem="$WORK/$name/.workspace/memory"
    mkdir -p "$mem"
    printf '@.workspace/memory/big.md\n' > "$root/AGENTS.md"
    head -c "$bytes" /dev/zero | tr '\0' 'x' > "$mem/big.md"
    echo "$root"
}

# rcm <dir> [args...] -> exit code of measure on that project.
rcm() {
    local dir="$1"; shift
    set +e
    (cd "$dir" && "$MEASURE" "$@") >/dev/null 2>&1
    local code=$?
    set -e
    echo "$code"
}

echo "== budget: no cap configured =="
B0="$(mkbudget nocap 400)"
check "no cap exits 0" "0" "$(rcm "$B0")"
check "no cap under --check exits 0" "0" "$(rcm "$B0" --check)"
check "says no cap is set" "1" \
    "$(cd "$B0" && "$MEASURE" | grep -c 'no auto_loaded_cap set')"

echo "== budget: cap from .index_state.json =="
B1="$(mkbudget sidecar-under 400)"   # 400 bytes -> 100 tokens, under 1000
printf '{"auto_loaded_cap": 1000}\n' > "$B1/.workspace/memory/.index_state.json"
check "under cap exits 0 with --check" "0" "$(rcm "$B1" --check)"
check "reports within cap" "1" \
    "$(cd "$B1" && "$MEASURE" | grep -c 'within cap')"

B2="$(mkbudget sidecar-over 8000)"   # 8000 bytes -> 2000 tokens, over 1000
printf '{"auto_loaded_cap": 1000}\n' > "$B2/.workspace/memory/.index_state.json"
check "over cap still exits 0 without --check" "0" "$(rcm "$B2")"
check "over cap exits 1 with --check" "1" "$(rcm "$B2" --check)"
check "over cap exits 1 with --total-only --check" "1" "$(rcm "$B2" --total-only --check)"
check "--total-only alone stays exit 0" "0" "$(rcm "$B2" --total-only)"
check "reports OVER CAP" "1" "$(cd "$B2" && "$MEASURE" | grep -c 'OVER CAP')"

echo "== budget: index frontmatter is the fallback when no sidecar =="
B3="$(mkbudget frontmatter-over 8000)"
printf '%s\n' '---' 'auto_loaded_cap: 1000' '---' > "$B3/.workspace/memory/MEMORY_INDEX.md"
check "frontmatter cap enforced" "1" "$(rcm "$B3" --check)"

echo "== budget: sidecar wins over frontmatter =="
B4="$(mkbudget both 8000)"
printf '%s\n' '---' 'auto_loaded_cap: 1000' '---' > "$B4/.workspace/memory/MEMORY_INDEX.md"
printf '{"auto_loaded_cap": 999999}\n' > "$B4/.workspace/memory/.index_state.json"
check "sidecar cap takes precedence" "0" "$(rcm "$B4" --check)"

echo "== budget: --cap overrides both =="
check "--cap raises the ceiling" "0" "$(rcm "$B2" --cap 999999 --check)"
check "--cap lowers the ceiling" "1" "$(rcm "$B1" --cap 1 --check)"
check "--cap rejects non-numeric" "2" "$(rcm "$B1" --cap abc)"

echo "== budget: --all-projects flags over-cap rows and gates on --check =="
AROOT="$WORK/allbudget"
mkdir -p "$AROOT"
cp -r "$B1" "$AROOT/under"
cp -r "$B2" "$AROOT/over"
ALLOUT="$("$MEASURE" --all-projects --root "$AROOT")"
check "marks the over-cap project" "1" "$(grep -c 'OVER CAP' <<<"$ALLOUT")"
check "counts 1 over cap" "1" "$(grep -c '2 project(s), 1 over cap' <<<"$ALLOUT")"
set +e
"$MEASURE" --all-projects --root "$AROOT" --check >/dev/null 2>&1
ALLRC=$?
set -e
check "--all-projects --check exits 1" "1" "$ALLRC"

echo
echo "Passed: $PASS  Failed: $FAIL"
[[ "$FAIL" -eq 0 ]]
