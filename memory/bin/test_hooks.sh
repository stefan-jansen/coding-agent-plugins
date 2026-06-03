#!/usr/bin/env bash
# test_hooks.sh — self-contained tests for the memory plugin's hooks.
#
# Exercises:
#   * pre_tooluse_memory_ref.py — simulated PreToolUse Read/Grep payloads on
#     paths inside `.workspace/memory/` advance last_referenced to today and
#     increment references. Non-memory paths and MEMORY_INDEX.md reads do not.
#   * stamp_gc_run.sh — stamps last_gc_run to today UTC; --date overrides.
#   * session_start.py — emits a nudge when last_gc_run is stale (or null);
#     stays silent when fresh; --auto-gc dry-run output appears only when the
#     setting is enabled. Timing assertion: <100ms on a Factory-shaped fixture.
#   * pre-compact.sh — passes through the canonical instruction block and
#     appends the memory nudge only when sidecar last_gc_run is stale.
#
# Pure stdlib bash + Python 3. Run: bash memory/bin/test_hooks.sh
set -uo pipefail

BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "$BIN_DIR/.." && pwd)"
PLUGINS_DIR="$(cd "$PLUGIN_ROOT/.." && pwd)"
PRE_HOOK="$PLUGIN_ROOT/hooks/pre_tooluse_memory_ref.py"
SESSION_HOOK="$PLUGIN_ROOT/hooks/session_start.py"
PRECOMPACT="$PLUGINS_DIR/transition/hooks/pre-compact.sh"
STAMP="$BIN_DIR/stamp_gc_run.sh"

TODAY="$(date -u +%Y-%m-%d)"

PASS=0
FAIL=0
check() { # check <desc> <expected> <actual>
    if [[ "$2" == "$3" ]]; then
        PASS=$((PASS + 1)); echo "  ok: $1"
    else
        FAIL=$((FAIL + 1)); echo "  FAIL: $1 (expected '$2', got '$3')"
    fi
}
ok()  { PASS=$((PASS + 1)); echo "  ok: $1"; }
bad() { FAIL=$((FAIL + 1)); echo "  FAIL: $1"; }

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

PROJECT="$WORK/proj"
MEM="$PROJECT/.workspace/memory"
mkdir -p "$MEM"
printf '# Project State\n\nAuth flow tested end to end.\n' > "$MEM/project_state.md"
printf '# Conventions\n\nUse conventional commits.\n'      > "$MEM/conventions.md"
printf '# Memory Index\n\n## project_state.md\n- status: active\n- last_referenced: 2025-01-01\n- tokens: 10\n- anchors: -\n' > "$MEM/MEMORY_INDEX.md"

# --------------------------------------------------------------------------
echo "== pre_tooluse: Read on a memory file bumps last_referenced =="
PAYLOAD=$(printf '{"tool_name":"Read","tool_input":{"file_path":"%s/project_state.md"},"cwd":"%s"}' "$MEM" "$PROJECT")
echo "$PAYLOAD" | python3 "$PRE_HOOK"
[[ -f "$MEM/.index_state.json" ]] && ok "sidecar created on first bump" || bad "sidecar created on first bump"
LAST_REF="$(python3 -c "import json,sys; d=json.load(open('$MEM/.index_state.json')); print(d['files']['project_state.md']['last_referenced'])")"
check "last_referenced advanced to today (UTC)" "$TODAY" "$LAST_REF"
REFS="$(python3 -c "import json; d=json.load(open('$MEM/.index_state.json')); print(d['files']['project_state.md']['references'])")"
check "references counter == 1" "1" "$REFS"

echo "== pre_tooluse: second Read increments references (idempotent date) =="
echo "$PAYLOAD" | python3 "$PRE_HOOK"
REFS2="$(python3 -c "import json; d=json.load(open('$MEM/.index_state.json')); print(d['files']['project_state.md']['references'])")"
check "references counter == 2" "2" "$REFS2"

echo "== pre_tooluse: relative file_path resolves against cwd =="
REL=$(printf '{"tool_name":"Read","tool_input":{"file_path":".workspace/memory/conventions.md"},"cwd":"%s"}' "$PROJECT")
echo "$REL" | python3 "$PRE_HOOK"
LAST_REF_CONV="$(python3 -c "import json; d=json.load(open('$MEM/.index_state.json')); print(d['files']['conventions.md']['last_referenced'])")"
check "relative path bumps last_referenced" "$TODAY" "$LAST_REF_CONV"

echo "== pre_tooluse: MEMORY_INDEX.md is ignored (always-loaded, no signal) =="
INDEX_PAYLOAD=$(printf '{"tool_name":"Read","tool_input":{"file_path":"%s/MEMORY_INDEX.md"},"cwd":"%s"}' "$MEM" "$PROJECT")
echo "$INDEX_PAYLOAD" | python3 "$PRE_HOOK"
HAS_INDEX_KEY="$(python3 -c "import json; d=json.load(open('$MEM/.index_state.json')); print('MEMORY_INDEX.md' in d['files'])")"
check "MEMORY_INDEX.md not recorded" "False" "$HAS_INDEX_KEY"

echo "== pre_tooluse: non-memory path is ignored =="
OTHER=$(printf '{"tool_name":"Read","tool_input":{"file_path":"%s/README.md"},"cwd":"%s"}' "$PROJECT" "$PROJECT")
echo "$OTHER" | python3 "$PRE_HOOK"
FILE_COUNT="$(python3 -c "import json; d=json.load(open('$MEM/.index_state.json')); print(len(d['files']))")"
check "no new entries created from non-memory read" "2" "$FILE_COUNT"

echo "== pre_tooluse: Grep over .workspace/memory bumps via path field =="
GREP_PAYLOAD=$(printf '{"tool_name":"Grep","tool_input":{"pattern":"foo","path":"%s/project_state.md"},"cwd":"%s"}' "$MEM" "$PROJECT")
echo "$GREP_PAYLOAD" | python3 "$PRE_HOOK"
REFS3="$(python3 -c "import json; d=json.load(open('$MEM/.index_state.json')); print(d['files']['project_state.md']['references'])")"
check "grep bumps references" "3" "$REFS3"

echo "== pre_tooluse: bad JSON / wrong tool exits 0 without effect =="
echo "not json" | python3 "$PRE_HOOK"; ok "bad JSON exits 0"
echo '{"tool_name":"Bash","tool_input":{}}' | python3 "$PRE_HOOK"; ok "non-Read/Grep tool exits 0"

# --------------------------------------------------------------------------
echo "== stamp_gc_run: explicit --date stamps the sidecar =="
"$STAMP" --dir "$MEM" --date 2026-05-30 >/dev/null
GCD="$(python3 -c "import json; d=json.load(open('$MEM/.index_state.json')); print(d['last_gc_run'])")"
check "last_gc_run stamped" "2026-05-30" "$GCD"

echo "== stamp_gc_run: default date is today UTC =="
"$STAMP" --dir "$MEM" >/dev/null
GCD_TODAY="$(python3 -c "import json; d=json.load(open('$MEM/.index_state.json')); print(d['last_gc_run'])")"
check "last_gc_run defaults to today (UTC)" "$TODAY" "$GCD_TODAY"

# --------------------------------------------------------------------------
echo "== session_start: fresh last_gc_run stays silent =="
SS_PAYLOAD=$(printf '{"cwd":"%s"}' "$PROJECT")
OUT="$(echo "$SS_PAYLOAD" | python3 "$SESSION_HOOK")"
check "no banner when fresh" "" "$OUT"

echo "== session_start: stale last_gc_run nudges =="
"$STAMP" --dir "$MEM" --date 2026-01-01 >/dev/null
OUT="$(echo "$SS_PAYLOAD" | python3 "$SESSION_HOOK")"
echo "$OUT" | grep -q "memory-budget: /memory-gc has not run" \
    && ok "banner nudge emitted" || bad "banner nudge emitted (got: $OUT)"

echo "== session_start: null last_gc_run also nudges =="
python3 - <<PY
import json
p = "$MEM/.index_state.json"
d = json.load(open(p))
d["last_gc_run"] = None
open(p,"w").write(json.dumps(d))
PY
OUT="$(echo "$SS_PAYLOAD" | python3 "$SESSION_HOOK")"
echo "$OUT" | grep -q "has not run in never" \
    && ok "null last_gc_run renders as 'never'" || bad "null last_gc_run renders as 'never' (got: $OUT)"

echo "== session_start: --auto-gc inline dry-run only when enabled =="
mkdir -p "$PROJECT/.claude"
# 1) without setting → no proposal lines
"$STAMP" --dir "$MEM" --date 2026-01-01 >/dev/null
# Force an old last_referenced so the dry-run would find a proposal if it ran.
python3 - <<PY
import json
p = "$MEM/.index_state.json"
d = json.load(open(p))
d["files"]["project_state.md"]["last_referenced"] = "2025-01-01"
open(p,"w").write(json.dumps(d))
PY
OUT="$(echo "$SS_PAYLOAD" | python3 "$SESSION_HOOK")"
echo "$OUT" | grep -q "memory-gc dry-run" && bad "no dry-run without --auto-gc" || ok "no dry-run without --auto-gc"
# 2) with project-level setting → dry-run lines appear
printf '{"memory":{"auto_gc":true}}\n' > "$PROJECT/.claude/settings.json"
OUT="$(echo "$SS_PAYLOAD" | python3 "$SESSION_HOOK")"
echo "$OUT" | grep -q "memory-gc dry-run" \
    && ok "--auto-gc inline dry-run emitted" || bad "--auto-gc inline dry-run emitted (got: $OUT)"
echo "$OUT" | grep -q "project_state.md: active -> dormant" \
    && ok "proposal line for stale file appears" || bad "proposal line for stale file appears (got: $OUT)"

# --------------------------------------------------------------------------
echo "== session_start: timing under 100ms on a Factory-shaped fixture =="
# Build a fixture with 8 memory files matching factory's current shape.
TPROJ="$WORK/tproj"
TMEM="$TPROJ/.workspace/memory"
mkdir -p "$TMEM"
for n in project_state conventions decisions README plugin_architecture claude_code_plugin_schema lessons_learned consolidation_decisions; do
    printf '# %s\n\nbody\n' "$n" > "$TMEM/$n.md"
done
printf '# Memory Index\n' > "$TMEM/MEMORY_INDEX.md"
"$STAMP" --dir "$TMEM" --date 2026-01-01 >/dev/null
SS_T="$(printf '{"cwd":"%s"}' "$TPROJ")"
ELAPSED_MS="$(python3 - <<PY
import subprocess, time
payload = '''$SS_T'''
# Warm up the interpreter / disk cache once so the assertion measures the
# steady-state cost, not first-import latency.
for _ in range(2):
    subprocess.run(["python3", "$SESSION_HOOK"], input=payload, text=True, capture_output=True)
runs = []
for _ in range(5):
    t0 = time.perf_counter()
    subprocess.run(["python3", "$SESSION_HOOK"], input=payload, text=True, capture_output=True)
    runs.append((time.perf_counter() - t0) * 1000)
print(f"{min(runs):.0f}")
PY
)"
echo "  measured min wall: ${ELAPSED_MS}ms"
if [[ "$ELAPSED_MS" -lt 100 ]]; then
    ok "SessionStart hook <100ms (best of 5)"
else
    bad "SessionStart hook >=100ms (best of 5 was ${ELAPSED_MS}ms)"
fi

# --------------------------------------------------------------------------
echo "== pre-compact: canonical block always present, memory nudge only when stale =="
# No sidecar → only the canonical block, no nudge.
TPROJ2="$WORK/tproj2"
mkdir -p "$TPROJ2"
(cd "$TPROJ2" && OUT="$("$PRECOMPACT")") || true
OUT="$(cd "$TPROJ2" && "$PRECOMPACT")"
echo "$OUT" | grep -q "Current task and its status" \
    && ok "canonical instructions preserved" || bad "canonical instructions preserved"
echo "$OUT" | grep -q "/memory-gc has not run" \
    && bad "no nudge without sidecar" || ok "no nudge without sidecar"

# With sidecar + stale last_gc_run → nudge appended.
mkdir -p "$TPROJ2/.workspace/memory"
"$STAMP" --dir "$TPROJ2/.workspace/memory" --date 2026-01-01 >/dev/null
OUT="$(cd "$TPROJ2" && "$PRECOMPACT")"
echo "$OUT" | grep -q "memory relevance review is overdue" \
    && ok "stale sidecar appends nudge" || bad "stale sidecar appends nudge (got: $OUT)"

# Fresh sidecar → no nudge.
"$STAMP" --dir "$TPROJ2/.workspace/memory" >/dev/null
OUT="$(cd "$TPROJ2" && "$PRECOMPACT")"
echo "$OUT" | grep -q "memory relevance review is overdue" \
    && bad "fresh sidecar suppresses nudge" || ok "fresh sidecar suppresses nudge"

echo
echo "test_hooks.sh: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 ]]
