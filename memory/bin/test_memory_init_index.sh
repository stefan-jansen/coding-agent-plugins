#!/usr/bin/env bash
# test_memory_init_index.sh — self-contained tests for memory_init_index.sh.
# Pure stdlib; builds fixtures in a temp dir, no network, no third-party deps.
# Run: bash memory/bin/test_memory_init_index.sh
set -euo pipefail

BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INIT="$BIN_DIR/memory_init_index.sh"
TOKEN_PY="$BIN_DIR/token_count.py"
VERIFY="$BIN_DIR/verify_index.sh"   # sibling M1 deliverable; used if present.

# Deterministic dates so seeded last_referenced / generated_at are predictable.
export MEMORY_TODAY="2026-06-01"

PASS=0
FAIL=0
check() { # check <desc> <expected> <actual>
    if [[ "$2" == "$3" ]]; then
        PASS=$((PASS + 1)); echo "  ok: $1"
    else
        FAIL=$((FAIL + 1)); echo "  FAIL: $1 (expected '$2', got '$3')"
    fi
}
ok() { PASS=$((PASS + 1)); echo "  ok: $1"; }
bad() { FAIL=$((FAIL + 1)); echo "  FAIL: $1"; }

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

MEM="$WORK/.workspace/memory"
mkdir -p "$MEM"
printf '# Project State\n\nAuth flow tested end to end.\n' > "$MEM/project_state.md"   # 44 chars
printf '# Conventions\n\nUse conventional commits.\n'        > "$MEM/conventions.md"
# Pin mtimes so the seeded last_referenced is deterministic.
touch -d "2026-05-20T00:00:00" "$MEM/project_state.md" "$MEM/conventions.md"

INDEX="$MEM/MEMORY_INDEX.md"
SIDECAR="$MEM/.index_state.json"

echo "== first run seeds index + sidecar =="
OUT="$("$INIT" --dir "$MEM")"
[[ -f "$INDEX" ]]   && ok "MEMORY_INDEX.md created"      || bad "MEMORY_INDEX.md created"
[[ -f "$SIDECAR" ]] && ok ".index_state.json created"   || bad ".index_state.json created"
check "summary reports 2 entries (2 new)" "1" "$(grep -c '2 entries (2 new, 0 kept, 0 dropped)' <<<"$OUT")"

echo "== index has a complete entry per file =="
for name in project_state.md conventions.md; do
    check "entry heading for $name" "1" "$(grep -c "^## $name\$" "$INDEX")"
done
# All four required fields present, exactly twice (once per file).
for field in status last_referenced tokens anchors; do
    check "field '$field' present twice" "2" "$(grep -c "^- $field: " "$INDEX")"
done
check "default status is active" "2" "$(grep -c '^- status: active$' "$INDEX")"
check "last_referenced seeded from mtime" "2" "$(grep -c '^- last_referenced: 2026-05-20$' "$INDEX")"
check "anchors stubbed with -" "2" "$(grep -c '^- anchors: -$' "$INDEX")"
# Tokens in the index match the shared helper exactly.
PS_TOK="$(python3 "$TOKEN_PY" "$MEM/project_state.md")"
check "tokens match token_count.py" "1" "$(grep -c "^- tokens: $PS_TOK\$" "$INDEX")"

echo "== sidecar contract =="
check "sidecar version is 1" "1" \
    "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["version"])' "$SIDECAR")"
check "last_gc_run starts null" "None" \
    "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["last_gc_run"])' "$SIDECAR")"
check "generated_at honours MEMORY_TODAY" "2026-06-01" \
    "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["generated_at"])' "$SIDECAR")"
check "per-file last_referenced seeded" "2026-05-20" \
    "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["files"]["project_state.md"]["last_referenced"])' "$SIDECAR")"
check "per-file references starts at 0" "0" \
    "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["files"]["project_state.md"]["references"])' "$SIDECAR")"
check "sidecar is gitignored" "1" "$(grep -c '^.index_state.json$' "$MEM/.gitignore")"

echo "== idempotency: re-run preserves GC-owned state + signals =="
# Simulate GC marking a file dormant + the hook advancing a signal.
python3 - "$INDEX" <<'PY'
import sys
p = sys.argv[1]
src = open(p).read().replace(
    "## conventions.md\n- status: active",
    "## conventions.md\n- status: dormant")
open(p, "w").write(src)
PY
python3 - "$SIDECAR" <<'PY'
import json, sys
p = sys.argv[1]
d = json.load(open(p))
d["files"]["project_state.md"]["last_referenced"] = "2026-05-31"
d["files"]["project_state.md"]["references"] = 7
d["last_gc_run"] = "2026-05-30"
json.dump(d, open(p, "w"), indent=2, sort_keys=True)
PY
OUT2="$("$INIT" --dir "$MEM")"
check "re-run keeps both entries (0 new)" "1" "$(grep -c '2 entries (0 new, 2 kept, 0 dropped)' <<<"$OUT2")"
check "dormant status preserved" "1" "$(grep -c '^- status: dormant$' "$INDEX")"
check "signal last_referenced preserved in index" "1" "$(grep -c '^- last_referenced: 2026-05-31$' "$INDEX")"
check "last_gc_run preserved in sidecar" "2026-05-30" \
    "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["last_gc_run"])' "$SIDECAR")"
check "reference count preserved" "7" \
    "$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["files"]["project_state.md"]["references"])' "$SIDECAR")"

echo "== idempotency: byte-stable index when nothing changes =="
BEFORE="$(cat "$INDEX")"
"$INIT" --dir "$MEM" >/dev/null
AFTER="$(cat "$INDEX")"
check "index unchanged on no-op re-run" "same" "$([[ "$BEFORE" == "$AFTER" ]] && echo same || echo different)"

echo "== new + removed files reflected on re-run =="
printf '# Decisions\n\nPostgres over Mongo.\n' > "$MEM/decisions.md"
touch -d "2026-05-25T00:00:00" "$MEM/decisions.md"
rm "$MEM/conventions.md"
OUT3="$("$INIT" --dir "$MEM")"
check "added decisions.md (new)" "1" "$(grep -c '^## decisions.md$' "$INDEX")"
check "dropped conventions.md from index" "0" "$(grep -c '^## conventions.md$' "$INDEX")"
check "conventions.md gone from sidecar" "False" \
    "$(python3 -c 'import json,sys; print("conventions.md" in json.load(open(sys.argv[1]))["files"])' "$SIDECAR")"
check "summary reports new + dropped" "1" "$(grep -c '2 entries (1 new, 1 kept, 1 dropped)' <<<"$OUT3")"

echo "== --cap sets frontmatter; preserved on re-run without --cap =="
"$INIT" --dir "$MEM" --cap 3000 >/dev/null
check "auto_loaded_cap written" "1" "$(grep -c '^auto_loaded_cap: 3000$' "$INDEX")"
"$INIT" --dir "$MEM" >/dev/null
check "auto_loaded_cap preserved" "1" "$(grep -c '^auto_loaded_cap: 3000$' "$INDEX")"

echo "== empty memory dir => valid empty index, no crash =="
EMPTY="$WORK/empty/.workspace/memory"
mkdir -p "$EMPTY"
OUT4="$("$INIT" --dir "$EMPTY")"
[[ -f "$EMPTY/MEMORY_INDEX.md" ]] && ok "empty index created" || bad "empty index created"
check "summary reports 0 entries" "1" "$(grep -c '0 entries (0 new, 0 kept, 0 dropped)' <<<"$OUT4")"

echo "== missing memory dir => exit 2 =="
if "$INIT" --dir "$WORK/does-not-exist" >/dev/null 2>&1; then
    bad "missing dir should exit non-zero"
else
    rc=$?
    check "missing dir exits 2" "2" "$rc"
fi

echo "== produced index passes verify_index.sh (acceptance criterion) =="
if [[ -x "$VERIFY" ]]; then
    if "$VERIFY" --dir "$MEM" >/dev/null 2>&1; then
        ok "verify_index.sh passes on the generated index"
    else
        bad "verify_index.sh failed on the generated index"
    fi
else
    echo "  skip: verify_index.sh not present on this branch (sibling M1 deliverable)"
fi

echo
echo "Passed: $PASS  Failed: $FAIL"
[[ "$FAIL" -eq 0 ]]
