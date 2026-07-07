#!/usr/bin/env bash
# test_check_anchors.sh — self-contained tests for check_anchors.sh. Pure stdlib;
# builds an index + working tree in a temp dir, no network, no third-party deps.
# Run: bash memory/bin/test_check_anchors.sh
set -euo pipefail

BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CHECK="$BIN_DIR/check_anchors.sh"

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

# Working tree: a couple of real files and a symbol that exists in source.
ROOT="$WORK/proj"
MEM="$ROOT/.workspace/memory"
mkdir -p "$MEM" "$ROOT/src" "$ROOT/bin"
printf 'def login(self):\n    return AuthService.token\n' > "$ROOT/src/auth.py"
printf 'class AuthService: pass\n' > "$ROOT/src/service.py"
printf '#!/bin/sh\necho hi\n' > "$ROOT/bin/migrate.sh"

INDEX="$MEM/MEMORY_INDEX.md"
# project_state.md: an existing file, a command on PATH, a real symbol -> all present.
# stale.md: a deleted/never-existed file path + a missing symbol -> missing.
# refs.md: a URL and a ticket -> both n/a. Plus an empty-anchors entry.
cat > "$INDEX" <<'EOF'
---
auto_loaded_cap: 5000
---

# Memory Index

## project_state.md
- status: active
- last_referenced: 2026-06-01
- tokens: 100
- anchors: src/auth.py, cmd:sh, symbol:AuthService

## stale.md
- status: dormant
- last_referenced: 2026-04-01
- tokens: 50
- anchors: src/deleted.py, symbol:NoSuchThing

## refs.md
- status: active
- last_referenced: 2026-05-01
- tokens: 30
- anchors: https://example.com/doc, JIRA-123

## empty.md
- status: dormant
- last_referenced: 2026-03-01
- tokens: 10
- anchors: none
EOF

run() { "$CHECK" --index "$INDEX" --root "$ROOT" "$@"; }

echo "== present / missing / n/a classification (JSON) =="
J="$(run --json)"
# Pull each anchor's result with a tiny python helper for robust assertions.
field() { # field <file> <anchor> -> result
    python3 - "$J" "$1" "$2" <<'PY'
import json, sys
data = json.loads(sys.argv[1])
for e in data["entries"]:
    if e["file"] == sys.argv[2]:
        for a in e["anchors"]:
            if a["anchor"] == sys.argv[3]:
                print(a["result"]); sys.exit(0)
print("NOTFOUND")
PY
}
typ() { # typ <file> <anchor> -> type
    python3 - "$J" "$1" "$2" <<'PY'
import json, sys
data = json.loads(sys.argv[1])
for e in data["entries"]:
    if e["file"] == sys.argv[2]:
        for a in e["anchors"]:
            if a["anchor"] == sys.argv[3]:
                print(a["type"]); sys.exit(0)
print("NOTFOUND")
PY
}

check "existing file => present" "present" "$(field project_state.md src/auth.py)"
check "file inferred as type file" "file" "$(typ project_state.md src/auth.py)"
check "command on PATH => present" "present" "$(field project_state.md cmd:sh)"
check "real symbol => present" "present" "$(field project_state.md symbol:AuthService)"
check "deleted file => missing" "missing" "$(field stale.md src/deleted.py)"
check "absent symbol => missing" "missing" "$(field stale.md symbol:NoSuchThing)"
check "URL => n/a" "n/a" "$(field refs.md https://example.com/doc)"
check "ticket => n/a" "n/a" "$(field refs.md JIRA-123)"

SUMMARY="$(python3 -c 'import json,sys; s=json.loads(sys.argv[1])["summary"]; print(s["present"],s["missing"],s["n/a"])' "$J")"
check "summary counts present/missing/n/a" "3 2 2" "$SUMMARY"

echo "== break / restore cycle (acceptance criterion 4) =="
# A fresh fixture whose single anchor points at a file we toggle.
ROOT2="$WORK/cycle"
MEM2="$ROOT2/.workspace/memory"
mkdir -p "$MEM2"
printf 'data\n' > "$ROOT2/target.txt"
cat > "$MEM2/MEMORY_INDEX.md" <<'EOF'
# Memory Index

## note.md
- status: active
- last_referenced: 2026-06-01
- tokens: 5
- anchors: target.txt
EOF
present_now() { "$CHECK" --dir "$MEM2" --root "$ROOT2" --json \
    | python3 -c 'import json,sys; print(json.load(sys.stdin)["entries"][0]["anchors"][0]["result"])'; }
check "anchor present initially" "present" "$(present_now)"
rm "$ROOT2/target.txt"                       # deliberately break the anchor
check "anchor missing after removal" "missing" "$(present_now)"
printf 'data\n' > "$ROOT2/target.txt"        # restore it
check "anchor present after restore" "present" "$(present_now)"

echo "== exit codes & flags =="
# Default: exit 0 even with missing anchors (it is a reporter).
if run >/dev/null 2>&1; then RC=0; else RC=$?; fi
check "default exit 0 despite missing" "0" "$RC"
# --strict: exit 1 when any anchor is missing.
if run --strict >/dev/null 2>&1; then RC=0; else RC=$?; fi
check "--strict exit 1 on missing" "1" "$RC"
# --strict on an all-clean index exits 0.
if "$CHECK" --dir "$MEM2" --root "$ROOT2" --strict >/dev/null 2>&1; then RC=0; else RC=$?; fi
check "--strict exit 0 when clean" "0" "$RC"
# Missing index => exit 2.
if "$CHECK" --index "$WORK/nope/MEMORY_INDEX.md" >/dev/null 2>&1; then RC=0; else RC=$?; fi
check "missing index => exit 2" "2" "$RC"

echo "== table + --quiet output =="
TABLE="$(run)"
check "table reports a missing line" "1" "$(grep -c 'missing  file    src/deleted.py' <<<"$TABLE")"
check "table summary line present" "1" "$(grep -c 'Summary: 3 present, 2 missing, 2 n/a' <<<"$TABLE")"
QOUT="$(run --quiet)"
check "--quiet hides all-present entry" "0" "$(grep -c '^project_state.md$' <<<"$QOUT")"
check "--quiet keeps entry with missing" "1" "$(grep -c '^stale.md$' <<<"$QOUT")"

echo
echo "Passed: $PASS  Failed: $FAIL"
[[ "$FAIL" -eq 0 ]]
