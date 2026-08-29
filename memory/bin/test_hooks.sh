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
# Size signal: independent of GC recency, because a file can be correctly
# `active` and still be the reason the context window starts full.
#
# mksize <name> <bytes> <agents-md-lines...> -> echoes the project root, with a
# fresh last_gc_run so any output must come from the size check alone.
mksize() {
    local name="$1" bytes="$2"; shift 2
    local root="$WORK/$name" mem="$WORK/$name/.workspace/memory"
    mkdir -p "$mem"
    head -c "$bytes" /dev/zero | tr '\0' 'x' > "$mem/project_state.md"
    printf '# index\n' > "$mem/MEMORY_INDEX.md"
    printf '%s\n' "$@" > "$root/AGENTS.md"
    printf '{"last_gc_run": "%s", "auto_loaded_cap": 1000, "files": {}}\n' \
        "$TODAY" > "$mem/.index_state.json"
    echo "$root"
}
ss() { printf '{"cwd":"%s"}' "$1" | python3 "$SESSION_HOOK"; }

echo "== session_start: over-cap nudge fires even when /memory-gc is fresh =="
SZ1="$(mksize size-over 8000 '# p' '@.workspace/memory/project_state.md')"
OUT="$(ss "$SZ1")"
echo "$OUT" | grep -q "tokens auto-loaded every session vs a cap" \
    && ok "over-cap nudge with fresh gc" || bad "over-cap nudge with fresh gc (got: $OUT)"
echo "$OUT" | grep -q "/memory-gc has not run" \
    && bad "no staleness nudge when gc is fresh" || ok "no staleness nudge when gc is fresh"

echo "== session_start: direct memory-file include is named =="
echo "$OUT" | grep -q "project_state.md @-included directly" \
    && ok "names the directly-included file" || bad "names the directly-included file (got: $OUT)"

echo "== session_start: index-only project under cap stays silent =="
SZ2="$(mksize size-ok 100 '# p' '@.workspace/memory/MEMORY_INDEX.md')"
check "healthy project emits nothing" "" "$(ss "$SZ2")"

echo "== session_start: no cap configured => no size nudge =="
SZ3="$(mksize size-nocap 8000 '# p' '@.workspace/memory/project_state.md')"
printf '{"last_gc_run": "%s", "files": {}}\n' "$TODAY" \
    > "$SZ3/.workspace/memory/.index_state.json"
OUT3="$(ss "$SZ3")"
echo "$OUT3" | grep -q "vs a cap" \
    && bad "silent about size without a cap" || ok "silent about size without a cap"
echo "$OUT3" | grep -q "@-included directly" \
    && ok "still reports the direct include" || bad "still reports the direct include"

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
# Assert the contract, not the wording: the block must ask for current task +
# status and must state what to leave out. Exact phrasing is free to change
# (it did in transition 1.4.0, which broke the old literal-string assertion).
echo "$OUT" | grep -qi "current task" \
    && echo "$OUT" | grep -qi "do not include" \
    && ok "canonical instructions preserved" || bad "canonical instructions preserved (got: $OUT)"
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

# --------------------------------------------------------------------------
# $CLAUDE_MEMORY_DIR: a project whose memory is not under `.workspace/`.
# Without this the hook matched on the literal `.workspace/memory` path
# components, so such a project recorded no reads at all and GC saw an empty
# index no matter how much memory it had.
echo "== pre_tooluse: CLAUDE_MEMORY_DIR relocates the memory directory =="
ALTPROJ="$WORK/altproj"
ALTMEM="$ALTPROJ/memory"
mkdir -p "$ALTMEM"
printf '# Notes\n' > "$ALTMEM/notes.md"

ALT_PAYLOAD=$(printf '{"tool_name":"Read","tool_input":{"file_path":"%s/notes.md"},"cwd":"%s"}' "$ALTMEM" "$ALTPROJ")

# Unset: the relocated directory is not memory, so nothing is recorded.
echo "$ALT_PAYLOAD" | python3 "$PRE_HOOK"
[[ -f "$ALTMEM/.index_state.json" ]] \
    && bad "no sidecar without CLAUDE_MEMORY_DIR" \
    || ok "no sidecar without CLAUDE_MEMORY_DIR"

# Relative to the project root.
echo "$ALT_PAYLOAD" | CLAUDE_MEMORY_DIR=memory python3 "$PRE_HOOK"
[[ -f "$ALTMEM/.index_state.json" ]] \
    && ok "relative CLAUDE_MEMORY_DIR records the read" \
    || bad "relative CLAUDE_MEMORY_DIR records the read"
ALT_REF="$(python3 -c "import json; d=json.load(open('$ALTMEM/.index_state.json')); print(d['files']['notes.md']['last_referenced'])")"
check "relocated last_referenced is today" "$TODAY" "$ALT_REF"

# Absolute path.
echo "$ALT_PAYLOAD" | CLAUDE_MEMORY_DIR="$ALTMEM" python3 "$PRE_HOOK"
ALT_REFS="$(python3 -c "import json; d=json.load(open('$ALTMEM/.index_state.json')); print(d['files']['notes.md']['references'])")"
check "absolute CLAUDE_MEMORY_DIR increments too" "2" "$ALT_REFS"

# The default still works when the variable is set to something else: a read
# under `.workspace/memory` must NOT be recorded once memory moved.
OFF_PAYLOAD=$(printf '{"tool_name":"Read","tool_input":{"file_path":"%s/conventions.md"},"cwd":"%s"}' "$MEM" "$PROJECT")
BEFORE_N="$(python3 -c "import json; d=json.load(open('$MEM/.index_state.json')); print(len(d['files']))")"
echo "$OFF_PAYLOAD" | CLAUDE_MEMORY_DIR=somewhere-else python3 "$PRE_HOOK"
AFTER_N="$(python3 -c "import json; d=json.load(open('$MEM/.index_state.json')); print(len(d['files']))")"
check "override redirects away from .workspace/memory" "$BEFORE_N" "$AFTER_N"

# --------------------------------------------------------------------------
# Reference capture through Bash. A bypass-permissions session is instructed to
# read with cat/sed/head and search with grep, so a hook that only matched the
# Read and Grep tools recorded nothing at all in the sessions that do the most
# reading. See issues/2026-08-29-memory-gc-reports-current-on-inputs-it-never-
# collected.md.
echo "== pre_tooluse: Bash cat on a memory file bumps last_referenced =="
BPROJ="$WORK/bash"; BMEM="$BPROJ/.workspace/memory"
mkdir -p "$BMEM/_inbox" "$BMEM/_archive"
printf '# State\n' > "$BMEM/project_state.md"
printf '# Finding\n' > "$BMEM/_inbox/holdout.md"
printf '# Old\n' > "$BMEM/_archive/ancient.md"
refs() { # refs <key>
    python3 -c "import json,sys; d=json.load(open('$BMEM/.index_state.json')); print(d['files'].get(sys.argv[1],{}).get('references',0))" "$1" 2>/dev/null || echo 0
}
bash_payload() { printf '{"tool_name":"Bash","tool_input":{"command":"%s"},"cwd":"%s"}' "$1" "$BPROJ"; }

bash_payload "cat $BMEM/project_state.md" | python3 "$PRE_HOOK"
check "cat bumps references" "1" "$(refs project_state.md)"
LR="$(python3 -c "import json; d=json.load(open('$BMEM/.index_state.json')); print(d['files']['project_state.md']['last_referenced'])")"
check "cat advances last_referenced to today" "$TODAY" "$LR"

bash_payload "sed -n '1,40p' .workspace/memory/project_state.md" | python3 "$PRE_HOOK"
check "relative path in a Bash command resolves against cwd" "2" "$(refs project_state.md)"

bash_payload "grep -rn 'auth' $BMEM/project_state.md $BMEM/_inbox/holdout.md" | python3 "$PRE_HOOK"
check "one command naming two files bumps both (first)" "3" "$(refs project_state.md)"
check "one command naming two files bumps both (second)" "1" "$(refs _inbox/holdout.md)"

echo "== pre_tooluse: Bash commands with no memory path are a no-op =="
BEFORE="$(python3 -c "import json; d=json.load(open('$BMEM/.index_state.json')); print(sorted(d['files']))")"
bash_payload "ls -la $BMEM" | python3 "$PRE_HOOK"
bash_payload "cat $BPROJ/README.md" | python3 "$PRE_HOOK"
bash_payload "git log --oneline" | python3 "$PRE_HOOK"
AFTER="$(python3 -c "import json; d=json.load(open('$BMEM/.index_state.json')); print(sorted(d['files']))")"
check "non-memory Bash commands record nothing" "$BEFORE" "$AFTER"

echo "== pre_tooluse: subdirectories are keyed by relative path =="
printf '{"tool_name":"Read","tool_input":{"file_path":"%s/_inbox/holdout.md"},"cwd":"%s"}' "$BMEM" "$BPROJ" \
    | python3 "$PRE_HOOK"
check "Read of a subdirectory note bumps its relative key" "2" "$(refs _inbox/holdout.md)"
HAS_BASENAME="$(python3 -c "import json; d=json.load(open('$BMEM/.index_state.json')); print('holdout.md' in d['files'])")"
check "the basename is not used as a key" "False" "$HAS_BASENAME"

echo "== pre_tooluse: _archive/ and MEMORY_INDEX.md stay unrecorded =="
bash_payload "cat $BMEM/_archive/ancient.md" | python3 "$PRE_HOOK"
bash_payload "cat $BMEM/MEMORY_INDEX.md" | python3 "$PRE_HOOK"
KEYS="$(python3 -c "import json; d=json.load(open('$BMEM/.index_state.json')); print(','.join(sorted(d['files'])))")"
check "archive and index reads are ignored" "_inbox/holdout.md,project_state.md" "$KEYS"

# --------------------------------------------------------------------------
# Paths recovered from a Bash command are guesses. Recording one that is not a
# file put an entry keyed `_inbox/*.md` into a real project's sidecar, and
# creating the memory directory on the way materialized `memory/_inbox/memory/`
# out of nothing. Both observed in ~/ml4t/agents on 2026-08-29.
echo "== pre_tooluse: an unexpanded glob is not a file =="
BEFORE_KEYS="$(python3 -c "import json; d=json.load(open('$BMEM/.index_state.json')); print(','.join(sorted(d['files'])))")"
bash_payload "grep -l holdout $BMEM/_inbox/*.md" | python3 "$PRE_HOOK"
AFTER_KEYS="$(python3 -c "import json; d=json.load(open('$BMEM/.index_state.json')); print(','.join(sorted(d['files'])))")"
check "a glob records no entry" "$BEFORE_KEYS" "$AFTER_KEYS"

echo "== pre_tooluse: a path that is not a file records nothing =="
bash_payload "cat $BMEM/never-written.md" | python3 "$PRE_HOOK"
printf '{"tool_name":"Read","tool_input":{"file_path":"%s/also-absent.md"},"cwd":"%s"}' "$BMEM" "$BPROJ" \
    | python3 "$PRE_HOOK"
AFTER_KEYS2="$(python3 -c "import json; d=json.load(open('$BMEM/.index_state.json')); print(','.join(sorted(d['files'])))")"
check "absent files record nothing" "$BEFORE_KEYS" "$AFTER_KEYS2"

echo "== pre_tooluse: the hook never creates a memory directory =="
NOPROJ="$WORK/nodir"
mkdir -p "$NOPROJ"
printf '# Note\n' > "$NOPROJ/stray.md"
printf '{"tool_name":"Bash","tool_input":{"command":"cat .workspace/memory/x.md"},"cwd":"%s"}' "$NOPROJ" \
    | python3 "$PRE_HOOK"
[[ -d "$NOPROJ/.workspace" ]] \
    && bad "a read in a project with no memory dir must not create one" \
    || ok "a read in a project with no memory dir must not create one"

echo
echo "test_hooks.sh: $PASS passed, $FAIL failed"
[[ "$FAIL" -eq 0 ]]
