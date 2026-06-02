#!/usr/bin/env bash
# test_fixtures.sh — fixture-driven integration harness for the memory bin/ scripts.
#
# Exercises the four shared scripts against the committed fixtures under
# bin/fixtures/ (complete, missing-entry, broken-anchor, oversized-file) plus a
# generated 50-file tree for the runtime bound:
#
#   measure_memory.sh      total under cap (complete) / over cap (oversized-file)
#   verify_index.sh        passes (complete) / flags missing entry (missing-entry)
#   check_anchors.sh       all present (complete) / reports missing (broken-anchor)
#   memory_init_index.sh   regenerates a valid index from memory files (round-trip)
#
# Scripts not yet present are SKIPPED, so this stays green while sibling M1 scripts
# are in flight and becomes fully meaningful as they land. Assertions key off
# spec-mandated vocabulary (present/missing, "0 missing entries") and observable
# artifacts (exit codes, files created, filenames echoed), not incidental wording.
#
# Each fixture is copied to a fresh temp dir before use: scripts that resolve the
# project root via `git rev-parse --show-toplevel` then fall back to the staged
# copy (outside any repo) instead of resolving to this plugin's repo root.
#
# Pure stdlib bash + Python 3. No network, no third-party deps.
# Run: bash memory/bin/test_fixtures.sh
set -uo pipefail

BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIX="$BIN_DIR/fixtures"

MEASURE="$BIN_DIR/measure_memory.sh"
VERIFY="$BIN_DIR/verify_index.sh"
ANCHORS="$BIN_DIR/check_anchors.sh"
INIT="$BIN_DIR/memory_init_index.sh"

PERF_BUDGET_SECS=30   # spec: GC proposal < 30s on a <=50-file project.

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

PASS=0; FAIL=0; SKIP=0
pass() { PASS=$((PASS + 1)); echo "  ok:   $1"; }
fail() { FAIL=$((FAIL + 1)); echo "  FAIL: $1"; }
skip() { SKIP=$((SKIP + 1)); echo "  skip: $1 (script not present yet)"; }

# want_lt/want_gt/want_le <desc> <value> <limit>: integer comparison assertions.
want_lt() { if [[ "$2" =~ ^[0-9]+$ && "$2" -lt "$3" ]]; then pass "$1 ($2 < $3)"; else fail "$1 (got '$2', want < $3)"; fi; }
want_gt() { if [[ "$2" =~ ^[0-9]+$ && "$2" -gt "$3" ]]; then pass "$1 ($2 > $3)"; else fail "$1 (got '$2', want > $3)"; fi; }
want_le() { if [[ "$2" =~ ^[0-9]+$ && "$2" -le "$3" ]]; then pass "$1 ($2 <= $3)"; else fail "$1 (got '$2', want <= $3)"; fi; }

have() { [[ -x "$1" ]]; }

# stage <fixture-name> -> prints a fresh temp copy of that fixture.
stage() {
    local name="$1" dest
    dest="$(mktemp -d "$WORK/${name}.XXXXXX")"
    cp -R "$FIX/$name/." "$dest/"
    echo "$dest"
}

# cap_of <staged-dir> -> auto_loaded_cap from the fixture's index frontmatter.
cap_of() {
    grep -m1 'auto_loaded_cap:' "$1/.workspace/memory/MEMORY_INDEX.md" 2>/dev/null \
        | grep -oE '[0-9]+' | head -1
}

echo "== measure_memory.sh =="
if have "$MEASURE"; then
    d="$(stage complete)"; cap="$(cap_of "$d")"
    total="$( (cd "$d" && "$MEASURE" --total-only) )"
    want_gt "complete: auto-loaded total is positive" "$total" 0
    want_lt "complete: index-only auto-load under cap" "$total" "$cap"

    d="$(stage oversized-file)"; cap="$(cap_of "$d")"
    total="$( (cd "$d" && "$MEASURE" --total-only) )"
    want_gt "oversized-file: auto-loaded total over cap" "$total" "$cap"
else
    skip "measure_memory.sh present"
fi

echo "== verify_index.sh =="
if have "$VERIFY"; then
    d="$(stage complete)"
    ( cd "$d" && "$VERIFY" ) >"$WORK/verify_complete.out" 2>&1; rc=$?
    if [[ "$rc" -eq 0 ]]; then pass "complete: index integrity passes (rc=0)"
    else fail "complete: index integrity should pass (rc=$rc)"; cat "$WORK/verify_complete.out"; fi

    d="$(stage missing-entry)"
    ( cd "$d" && "$VERIFY" ) >"$WORK/verify_missing.out" 2>&1; rc=$?
    if [[ "$rc" -ne 0 ]] || grep -qiE 'missing|absent|decisions\.md' "$WORK/verify_missing.out"; then
        pass "missing-entry: flags the un-indexed decisions.md (rc=$rc)"
    else
        fail "missing-entry: should flag decisions.md (rc=$rc)"; cat "$WORK/verify_missing.out"
    fi
else
    skip "verify_index.sh present"
fi

echo "== check_anchors.sh =="
if have "$ANCHORS"; then
    d="$(stage complete)"
    ( cd "$d" && "$ANCHORS" ) >"$WORK/anchors_complete.out" 2>&1; rc=$?
    if [[ "$rc" -eq 0 ]] && grep -qi 'present' "$WORK/anchors_complete.out"; then
        pass "complete: all anchors resolve present"
    else
        fail "complete: anchors should all be present (rc=$rc)"; cat "$WORK/anchors_complete.out"
    fi

    d="$(stage broken-anchor)"
    ( cd "$d" && "$ANCHORS" ) >"$WORK/anchors_broken.out" 2>&1
    if grep -qi 'missing' "$WORK/anchors_broken.out" && grep -q 'removed.py' "$WORK/anchors_broken.out"; then
        pass "broken-anchor: reports missing for src/removed.py"
    else
        fail "broken-anchor: should report missing src/removed.py"; cat "$WORK/anchors_broken.out"
    fi
else
    skip "check_anchors.sh present"
fi

echo "== memory_init_index.sh =="
if have "$INIT"; then
    # Round-trip: strip the index, regenerate it, expect an entry per memory file.
    d="$(stage complete)"
    rm -f "$d/.workspace/memory/MEMORY_INDEX.md"
    ( cd "$d" && "$INIT" ) >"$WORK/init.out" 2>&1; rc=$?
    idx="$d/.workspace/memory/MEMORY_INDEX.md"
    if [[ -f "$idx" ]] \
        && grep -q 'project_state.md' "$idx" \
        && grep -q 'conventions.md' "$idx" \
        && grep -q 'decisions.md' "$idx"; then
        pass "init: regenerates an index entry per memory file"
    else
        fail "init: should regenerate index covering every memory file (rc=$rc)"; cat "$WORK/init.out"
    fi
    if have "$VERIFY" && [[ -f "$idx" ]]; then
        ( cd "$d" && "$VERIFY" ) >/dev/null 2>&1
        if [[ $? -eq 0 ]]; then pass "init: regenerated index passes verify_index"
        else fail "init: regenerated index should pass verify_index"; fi
    fi
else
    skip "memory_init_index.sh present"
fi

echo "== runtime bound: <${PERF_BUDGET_SECS}s on a 50-file project =="
PERF="$WORK/perf50"
python3 - "$PERF" <<'PY'
import os, sys
root = sys.argv[1]
mem = os.path.join(root, ".workspace", "memory")
os.makedirs(os.path.join(root, "src"), exist_ok=True)
os.makedirs(mem, exist_ok=True)
with open(os.path.join(root, "CLAUDE.md"), "w") as fh:
    fh.write("@AGENTS.md\n")
with open(os.path.join(root, "AGENTS.md"), "w") as fh:
    fh.write("# 50-file perf fixture\n\n@.workspace/memory/MEMORY_INDEX.md\n")
with open(os.path.join(root, "src", "app.py"), "w") as fh:
    fh.write("def run():\n    return 'ok'\n")

N = 49  # 49 notes + MEMORY_INDEX.md == 50 *.md files (the <=50 bound).
idx = ["---", "auto_loaded_cap: 5000", "---", "", "# Memory Index", ""]
state = {"auto_loaded_cap": 5000, "last_gc_run": "2026-05-25", "files": {}}
for i in range(1, N + 1):
    name = "note_%02d.md" % i
    with open(os.path.join(mem, name), "w") as fh:
        fh.write("## Note %d\n\nA short memory note used for the runtime bound.\n" % i)
    idx += ["### %s" % name,
            "- status: active",
            "- last_referenced: 2026-05-20",
            "- tokens: 12",
            "- anchors: src/app.py",
            ""]
    state["files"][name] = {"last_referenced": "2026-05-20", "tokens": 12}
with open(os.path.join(mem, "MEMORY_INDEX.md"), "w") as fh:
    fh.write("\n".join(idx) + "\n")
import json
with open(os.path.join(mem, ".index_state.json"), "w") as fh:
    json.dump(state, fh, indent=2)
print(len(os.listdir(mem)))
PY
nfiles="$(find "$PERF/.workspace/memory" -name '*.md' | wc -l | tr -d ' ')"
want_le "fixture has <=50 memory files" "$nfiles" 50

timed=0
for entry in "measure_memory.sh:$MEASURE" "verify_index.sh:$VERIFY" \
             "check_anchors.sh:$ANCHORS" "memory_init_index.sh:$INIT"; do
    label="${entry%%:*}"; script="${entry#*:}"
    if have "$script"; then
        SECONDS=0
        ( cd "$PERF" && "$script" ) >/dev/null 2>&1 || true
        want_le "$label runs within budget on 50 files" "$SECONDS" "$PERF_BUDGET_SECS"
        timed=$((timed + 1))
    fi
done
if [[ "$timed" -eq 0 ]]; then skip "any script available to time on 50-file fixture"; fi
echo "  note: full GC-proposal perf test lands in M4; this bounds the shared scripts."

echo
echo "Passed: $PASS  Failed: $FAIL  Skipped: $SKIP"
[[ "$FAIL" -eq 0 ]]
