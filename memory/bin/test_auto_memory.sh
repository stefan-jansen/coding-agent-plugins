#!/usr/bin/env bash
# test_auto_memory.sh — self-contained tests for auto_memory.py.
#
# The resolution rules under test were probed against Claude Code v2.1.287 on
# 2026-10-02, not read off the docs: a relative `autoMemoryDirectory` is
# silently ignored, `$CLAUDE_PROJECT_DIR` is not expanded, and an absolute path
# or a `~/` path is honored. If a future version starts accepting relative
# paths, the "relative is ignored" cases below are what will catch it.
#
# Pure stdlib; builds fixtures in a temp dir, no network. Run:
#   bash memory/bin/test_auto_memory.sh
set -euo pipefail

BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AM="$BIN_DIR/auto_memory.py"

PASS=0
FAIL=0
check() { # check <desc> <expected> <actual>
    if [[ "$2" == "$3" ]]; then
        PASS=$((PASS + 1)); echo "  ok: $1"
    else
        FAIL=$((FAIL + 1)); echo "  FAIL: $1 (expected '$2', got '$3')"
    fi
}
contains() { # contains <desc> <needle> <haystack>
    if [[ "$3" == *"$2"* ]]; then
        PASS=$((PASS + 1)); echo "  ok: $1"
    else
        FAIL=$((FAIL + 1)); echo "  FAIL: $1 (no '$2' in: $3)"
    fi
}

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

CFG="$WORK/config"
mkdir -p "$CFG"
export CLAUDE_CONFIG_DIR="$CFG"

# field <project> <key> -> that key from --json
field() { python3 "$AM" --project "$1" --json | python3 -c \
    "import json,sys; print(json.load(sys.stdin)[sys.argv[1]])" "$2"; }

newproj() { # newproj <name> -> project root
    local root="$WORK/$1"
    mkdir -p "$root/.claude"
    echo "$root"
}

echo "== default: the per-project store under the config dir =="
P1="$(newproj proj1)"
check "slug replaces every / with -" \
    "$CFG/projects/${P1//\//-}/memory" "$(field "$P1" dir)"
check "source names the default" "default (per-project store)" "$(field "$P1" source)"

echo "== an absolute autoMemoryDirectory is honored =="
P2="$(newproj proj2)"
printf '{"autoMemoryDirectory": "%s/.workspace/memory-auto"}\n' "$P2" \
    > "$P2/.claude/settings.json"
check "absolute path accepted" "$P2/.workspace/memory-auto" "$(field "$P2" dir)"
contains "source names the settings file" ".claude/settings.json" "$(field "$P2" source)"
check "in_repo is true for a path inside the project" "True" "$(field "$P2" in_repo)"

echo "== a ~/ autoMemoryDirectory is honored =="
P3="$(newproj proj3)"
printf '{"autoMemoryDirectory": "~/elsewhere/mem"}\n' > "$P3/.claude/settings.json"
check "tilde expanded" "$HOME/elsewhere/mem" "$(field "$P3" dir)"
check "in_repo is false for a path outside the project" "False" "$(field "$P3" in_repo)"

echo "== a relative autoMemoryDirectory is ignored, and said so =="
P4="$(newproj proj4)"
printf '{"autoMemoryDirectory": "./.workspace/memory-auto"}\n' > "$P4/.claude/settings.json"
check "falls back to the default store" \
    "$CFG/projects/${P4//\//-}/memory" "$(field "$P4" dir)"
contains "the ignored value is reported" "is not absolute and is ignored" \
    "$(python3 "$AM" --project "$P4")"

echo "== \$CLAUDE_PROJECT_DIR is not expanded either =="
P5="$(newproj proj5)"
printf '{"autoMemoryDirectory": "$CLAUDE_PROJECT_DIR/.workspace/memory-auto"}\n' \
    > "$P5/.claude/settings.json"
check "variable form falls back to the default store" \
    "$CFG/projects/${P5//\//-}/memory" "$(field "$P5" dir)"

echo "== settings.local.json wins over settings.json =="
P6="$(newproj proj6)"
printf '{"autoMemoryDirectory": "%s/shared"}\n' "$P6" > "$P6/.claude/settings.json"
printf '{"autoMemoryDirectory": "%s/local"}\n' "$P6" > "$P6/.claude/settings.local.json"
check "local layer wins" "$P6/local" "$(field "$P6" dir)"

echo "== user settings apply when the project sets nothing =="
P7="$(newproj proj7)"
printf '{"autoMemoryDirectory": "%s/user-wide"}\n' "$WORK" > "$CFG/settings.json"
check "user layer used" "$WORK/user-wide" "$(field "$P7" dir)"
rm -f "$CFG/settings.json"

echo "== MEMORY.md is the auto-loaded part; fact files are on demand =="
P8="$(newproj proj8)"
MEM="$P8/.workspace/memory-auto"
mkdir -p "$MEM"
printf '{"autoMemoryDirectory": "%s"}\n' "$MEM" > "$P8/.claude/settings.json"
head -c 400 /dev/zero | tr '\0' 'x' > "$MEM/MEMORY.md"
head -c 800 /dev/zero | tr '\0' 'y' > "$MEM/fact_one.md"
head -c 800 /dev/zero | tr '\0' 'z' > "$MEM/fact_two.md"
check "index_exists" "True" "$(field "$P8" index_exists)"
check "two fact files counted" "2" "$(field "$P8" body_files)"
INDEX_TOKENS="$(python3 "$AM" --project "$P8" --index-tokens)"
[[ "$INDEX_TOKENS" -gt 0 ]] \
    && { PASS=$((PASS + 1)); echo "  ok: --index-tokens is positive"; } \
    || { FAIL=$((FAIL + 1)); echo "  FAIL: --index-tokens is positive (got $INDEX_TOKENS)"; }
BODY_TOKENS="$(field "$P8" body_tokens)"
[[ "$BODY_TOKENS" -gt "$INDEX_TOKENS" ]] \
    && { PASS=$((PASS + 1)); echo "  ok: fact files are counted apart from the index"; } \
    || { FAIL=$((FAIL + 1)); echo "  FAIL: fact files are counted apart from the index"; }

echo "== an absent store reports exists=false, not an error =="
P9="$(newproj proj9)"
printf '{"autoMemoryDirectory": "%s/never-created"}\n' "$P9" > "$P9/.claude/settings.json"
check "exists is false" "False" "$(field "$P9" exists)"
check "index_tokens is 0" "0" "$(field "$P9" index_tokens)"

echo "== malformed settings do not crash the resolver =="
P10="$(newproj proj10)"
printf 'not json at all' > "$P10/.claude/settings.json"
check "bad JSON falls back to the default store" \
    "$CFG/projects/${P10//\//-}/memory" "$(field "$P10" dir)"

echo ""
echo "test_auto_memory.sh: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 ]]
