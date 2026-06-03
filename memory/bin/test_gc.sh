#!/usr/bin/env bash
# test_gc.sh — self-contained tests for gc_propose.py + gc_apply.py.
#
# Covers M4 acceptance criterion 5: dry-run produces a readable diff and
# writes nothing; --execute (gc_apply.py) applies exactly the diff;
# last_gc_run advances on apply; <30s runtime on a 50-file fixture; a
# second dry-run is a no-op (idempotence).
#
# Pure stdlib bash + Python 3. Run: bash memory/bin/test_gc.sh
set -uo pipefail

BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROPOSE="$BIN_DIR/gc_propose.py"
APPLY="$BIN_DIR/gc_apply.py"

PASS=0
FAIL=0
check() { if [[ "$2" == "$3" ]]; then PASS=$((PASS+1)); echo "  ok: $1"; else FAIL=$((FAIL+1)); echo "  FAIL: $1 (expected '$2', got '$3')"; fi }
ok()  { PASS=$((PASS+1)); echo "  ok: $1"; }
bad() { FAIL=$((FAIL+1)); echo "  FAIL: $1"; }

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

MEM="$WORK/.workspace/memory"
mkdir -p "$MEM"
cat > "$MEM/MEMORY_INDEX.md" <<'EOF'
---
auto_loaded_cap: 5000
---

# Memory Index

## fresh.md
- status: active
- last_referenced: 2026-06-01
- tokens: 100
- anchors: -

## stale.md
- status: active
- last_referenced: 2025-12-01
- tokens: 200
- anchors: -

## old_dormant.md
- status: dormant
- last_referenced: 2025-01-01
- tokens: 50
- anchors: -

## superseded.md
- status: superseded-by:newer.md
- last_referenced: 2025-01-01
- tokens: 30
- anchors: -

## already_deprecated.md
- status: deprecated
- last_referenced: 2025-01-01
- tokens: 40
- anchors: -
EOF
touch "$MEM/fresh.md" "$MEM/stale.md" "$MEM/old_dormant.md" "$MEM/superseded.md" "$MEM/already_deprecated.md"
cat > "$MEM/.index_state.json" <<'EOF'
{"version":1,"files":{
  "fresh.md":{"last_referenced":"2026-06-01","references":3},
  "stale.md":{"last_referenced":"2025-12-01","references":0},
  "old_dormant.md":{"last_referenced":"2025-01-01","references":0},
  "superseded.md":{"references":0},
  "already_deprecated.md":{"references":0}
}}
EOF

# --------------------------------------------------------------------------
echo "== gc_propose: dry-run produces transitions; writes nothing =="
BEFORE_HASH="$(python3 -c "import hashlib; print(hashlib.sha256(open('$MEM/MEMORY_INDEX.md','rb').read()).hexdigest())")"
DRY="$(python3 "$PROPOSE" --dir "$MEM" --today 2026-06-03)"
echo "$DRY" | grep -q "stale.md: active -> deprecated" \
    && ok "active>180d -> deprecated" || bad "active>180d -> deprecated"
echo "$DRY" | grep -q "old_dormant.md: dormant -> deprecated" \
    && ok "dormant>180d -> deprecated" || bad "dormant>180d -> deprecated"
echo "$DRY" | grep -q "Summary: 2 transition" \
    && ok "summary line correct" || bad "summary line (got: $DRY)"
echo "$DRY" | grep -q "superseded.md" \
    && bad "superseded entries should NOT appear as transitions" \
    || ok "superseded entries skipped in transitions list"
AFTER_HASH="$(python3 -c "import hashlib; print(hashlib.sha256(open('$MEM/MEMORY_INDEX.md','rb').read()).hexdigest())")"
check "dry-run did not write" "$BEFORE_HASH" "$AFTER_HASH"

echo "== gc_propose: --json schema =="
JSON="$(python3 "$PROPOSE" --dir "$MEM" --today 2026-06-03 --json)"
echo "$JSON" | python3 -c "
import json, sys
d = json.load(sys.stdin)
assert d['version'] == 1, d
assert len(d['transitions']) == 2, d
assert d['summary']['transitions'] == 2, d
assert d['summary']['skipped_superseded'] == 1, d
print('ok')
" >/dev/null && ok "JSON schema validates" || bad "JSON schema validates"

echo "== gc_apply: applies exactly the diff (transactional) =="
echo "$JSON" > "$WORK/diff.json"
OUT="$(python3 "$APPLY" --diff "$WORK/diff.json" --memory-dir "$MEM" 2>&1)"
echo "$OUT" | grep -q "applied: stale.md" && ok "applied stale.md" || bad "applied stale.md (got: $OUT)"
echo "$OUT" | grep -q "applied: old_dormant.md" && ok "applied old_dormant.md" || bad "applied old_dormant.md"
# Verify the new status values.
check "stale.md is now deprecated" "deprecated" \
    "$(awk '/^## stale.md$/{flag=1} flag && /^- status:/{print $3; exit}' "$MEM/MEMORY_INDEX.md")"
check "old_dormant.md is now deprecated" "deprecated" \
    "$(awk '/^## old_dormant.md$/{flag=1} flag && /^- status:/{print $3; exit}' "$MEM/MEMORY_INDEX.md")"
# Untouched entries.
check "fresh.md untouched" "active" \
    "$(awk '/^## fresh.md$/{flag=1} flag && /^- status:/{print $3; exit}' "$MEM/MEMORY_INDEX.md")"
check "superseded.md untouched" "superseded-by:newer.md" \
    "$(awk '/^## superseded.md$/{flag=1} flag && /^- status:/{print $3; exit}' "$MEM/MEMORY_INDEX.md")"

echo "== gc_apply: stamps last_gc_run =="
TODAY="$(date -u +%Y-%m-%d)"
GCD="$(python3 -c "import json; print(json.load(open('$MEM/.index_state.json'))['last_gc_run'])")"
check "last_gc_run advanced to today" "$TODAY" "$GCD"

echo "== second dry-run is empty (idempotent) =="
DRY2="$(python3 "$PROPOSE" --dir "$MEM" --today 2026-06-03)"
echo "$DRY2" | grep -q "No status transitions proposed" \
    && ok "second dry-run reports no transitions" \
    || bad "second dry-run not empty (got: $DRY2)"

echo "== gc_apply: refuses on status drift; --force overrides =="
# Build a fresh fixture so we have a transition-pending entry to drift.
DMEM="$WORK/drift/.workspace/memory"
mkdir -p "$DMEM"
cat > "$DMEM/MEMORY_INDEX.md" <<'EOF'
## stale_drift.md
- status: active
- last_referenced: 2025-12-01
- tokens: 100
- anchors: -
EOF
touch "$DMEM/stale_drift.md"
echo '{"version":1,"files":{"stale_drift.md":{"last_referenced":"2025-12-01","references":0}}}' > "$DMEM/.index_state.json"
DJSON="$(python3 "$PROPOSE" --dir "$DMEM" --today 2026-06-03 --json)"
echo "$DJSON" > "$WORK/drift_diff.json"
# Mutate the index so the diff's expected `from` no longer matches.
sed -i 's/^- status: active$/- status: dormant/' "$DMEM/MEMORY_INDEX.md"
set +e
OUT="$(python3 "$APPLY" --diff "$WORK/drift_diff.json" --memory-dir "$DMEM" 2>&1)"
RC=$?
set -e
[[ "$RC" -eq 1 ]] && ok "exit 1 on drift" || bad "exit 1 on drift (got rc=$RC, out: $OUT)"
echo "$OUT" | grep -qi "conflict" && ok "reports conflict" || bad "reports conflict (got: $OUT)"
# --force overrides.
set +e
OUT2="$(python3 "$APPLY" --diff "$WORK/drift_diff.json" --memory-dir "$DMEM" --force 2>&1)"
RC2=$?
set -e
[[ "$RC2" -eq 0 ]] && ok "--force applies despite drift" || bad "--force applies (rc=$RC2, out: $OUT2)"

# --------------------------------------------------------------------------
echo "== gc_propose: under 30s on a 50-file fixture =="
BIGMEM="$WORK/big/.workspace/memory"
mkdir -p "$BIGMEM"
{
    echo "---"
    echo "auto_loaded_cap: 5000"
    echo "---"
    echo
    for i in $(seq 1 50); do
        echo "## file${i}.md"
        echo "- status: active"
        echo "- last_referenced: 2025-01-01"
        echo "- tokens: 100"
        echo "- anchors: -"
        echo
    done
} > "$BIGMEM/MEMORY_INDEX.md"
python3 - <<'PY' > "$BIGMEM/.index_state.json"
import json
files = {f"file{i}.md": {"last_referenced": "2025-01-01", "references": 0} for i in range(1, 51)}
print(json.dumps({"version": 1, "files": files}))
PY
for i in $(seq 1 50); do touch "$BIGMEM/file${i}.md"; done
T0=$(python3 -c "import time; print(time.time())")
python3 "$PROPOSE" --dir "$BIGMEM" --today 2026-06-03 --json >/dev/null
T1=$(python3 -c "import time; print(time.time())")
ELAPSED=$(python3 -c "print(round($T1 - $T0, 2))")
echo "  elapsed: ${ELAPSED}s"
python3 -c "import sys; sys.exit(0 if $ELAPSED < 30 else 1)" \
    && ok "50-file propose <30s (${ELAPSED}s)" || bad "50-file propose <30s (${ELAPSED}s)"

# --------------------------------------------------------------------------
echo "== environment errors =="
set +e
python3 "$PROPOSE" --dir "$WORK/nonexistent" 2>/dev/null; RC=$?
set -e
[[ "$RC" -eq 2 ]] && ok "missing memory_dir exits 2" || bad "missing memory_dir exits 2 (got $RC)"

# A memory dir without MEMORY_INDEX.md
mkdir -p "$WORK/noindex/.workspace/memory"
set +e
python3 "$PROPOSE" --dir "$WORK/noindex/.workspace/memory" 2>/dev/null; RC=$?
set -e
[[ "$RC" -eq 2 ]] && ok "missing MEMORY_INDEX.md exits 2" || bad "missing MEMORY_INDEX.md exits 2 (got $RC)"

echo
echo "test_gc.sh: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 ]]
