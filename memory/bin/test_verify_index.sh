#!/usr/bin/env bash
# test_verify_index.sh — self-contained tests for verify_index.sh.
# Pure stdlib; builds fixtures in a temp dir, no network, no third-party deps.
# Run: bash memory/bin/test_verify_index.sh
set -euo pipefail

BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VERIFY="$BIN_DIR/verify_index.sh"

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

# rc <dir> [args...] -> echoes exit code of verify on that memory dir.
rc() {
    local dir="$1"; shift
    set +e
    "$VERIFY" --dir "$dir" "$@" >/dev/null 2>&1
    local code=$?
    set -e
    echo "$code"
}

# out <dir> [args...] -> echoes combined output (stdout+stderr).
out() {
    local dir="$1"; shift
    set +e
    "$VERIFY" --dir "$dir" "$@" 2>&1
    set -e
}

echo "== complete fixture: exit 0, 0 missing =="
M="$WORK/complete/.workspace/memory"
mkdir -p "$M"
cat > "$M/MEMORY_INDEX.md" <<'EOF'
---
auto_loaded_cap: 5000
---

# Memory Index

## project_state.md
- status: active
- last_referenced: 2026-06-01
- tokens: 120
- anchors: src/app.py, bin/run.sh

## conventions.md
- status: dormant
- last_referenced: 2026-05-01
- tokens: 80
- anchors:

## old_plan.md
- status: superseded-by: project_state.md
- last_referenced: 2026-04-01
- tokens: 40
- anchors: none
EOF
printf '# state\n' > "$M/project_state.md"
printf '# conv\n' > "$M/conventions.md"
printf '# old\n' > "$M/old_plan.md"
check "complete fixture exits 0" "0" "$(rc "$M")"
check "reports 0 missing" "1" "$(grep -c 'OK — 0 missing entries' <<<"$(out "$M")")"

echo "== missing entry: nonzero + clear list =="
M2="$WORK/missing/.workspace/memory"
mkdir -p "$M2"
cat > "$M2/MEMORY_INDEX.md" <<'EOF'
---
auto_loaded_cap: 5000
---

## a.md
- status: active
- last_referenced: 2026-06-01
- tokens: 10
- anchors:
EOF
printf 'a\n' > "$M2/a.md"
printf 'b\n' > "$M2/b.md"   # no entry -> must be flagged
check "missing entry exits 1" "1" "$(rc "$M2")"
check "names the missing file" "1" "$(grep -c 'b.md: no entry' <<<"$(out "$M2")")"
check "FAIL line counts 1 missing" "1" "$(grep -c 'FAIL — 1 missing entry,' <<<"$(out "$M2")")"

echo "== missing required field: failure =="
M3="$WORK/field/.workspace/memory"
mkdir -p "$M3"
cat > "$M3/MEMORY_INDEX.md" <<'EOF'
## a.md
- status: active
- tokens: 10
- anchors:
EOF
printf 'a\n' > "$M3/a.md"
check "missing field exits 1" "1" "$(rc "$M3")"
check "names missing field" "1" "$(grep -c 'missing field(s): last_referenced' <<<"$(out "$M3")")"

echo "== invalid status: failure =="
M4="$WORK/status/.workspace/memory"
mkdir -p "$M4"
cat > "$M4/MEMORY_INDEX.md" <<'EOF'
## a.md
- status: archived
- last_referenced: 2026-06-01
- tokens: 10
- anchors:
EOF
printf 'a\n' > "$M4/a.md"
check "invalid status exits 1" "1" "$(rc "$M4")"
check "explains valid vocabulary" "1" "$(grep -c "invalid status 'archived'" <<<"$(out "$M4")")"

echo "== frontmatter conflict: warning, still exits 0 (index wins) =="
M5="$WORK/conflict/.workspace/memory"
mkdir -p "$M5"
cat > "$M5/MEMORY_INDEX.md" <<'EOF'
## a.md
- status: dormant
- last_referenced: 2026-06-01
- tokens: 10
- anchors:
EOF
cat > "$M5/a.md" <<'EOF'
---
status: active
---
# a
EOF
check "conflict still exits 0" "0" "$(rc "$M5")"
check "warns + proposes sync to index value" "1" \
    "$(grep -c "index wins — sync file to 'dormant'" <<<"$(out "$M5")")"
check "--strict turns warning into failure" "1" "$(rc "$M5" --strict)"

echo "== orphan index entry: warning, not a failure =="
M6="$WORK/orphan/.workspace/memory"
mkdir -p "$M6"
cat > "$M6/MEMORY_INDEX.md" <<'EOF'
## ghost.md
- status: deprecated
- last_referenced: 2026-01-01
- tokens: 10
- anchors:
EOF
check "orphan-only index exits 0" "0" "$(rc "$M6")"
check "warns about orphan entry" "1" \
    "$(grep -c 'ghost.md: index entry has no matching file' <<<"$(out "$M6")")"

echo "== no index file: environment error (exit 2) =="
M7="$WORK/noindex/.workspace/memory"
mkdir -p "$M7"
printf 'a\n' > "$M7/a.md"
check "no MEMORY_INDEX.md exits 2" "2" "$(rc "$M7")"

echo "== missing memory dir: environment error (exit 2) =="
check "nonexistent dir exits 2" "2" "$(rc "$WORK/does-not-exist")"

echo "== display-only Claude auto-memory shape: recognized, exit 0 =="
M8="$WORK/home/.claude/projects/some-slug/memory"
mkdir -p "$M8"
printf 'x\n' > "$M8/note.md"   # no MEMORY_INDEX.md -> unmanaged, must not fail
check "display-only shape exits 0" "0" "$(rc "$M8")"
check "notes display-only recognition" "1" \
    "$(grep -c 'display-only, not managed' <<<"$(out "$M8")")"

echo "== empty memory dir with index: exit 0 =="
M9="$WORK/empty/.workspace/memory"
mkdir -p "$M9"
printf '%s\n' '---' 'auto_loaded_cap: 5000' '---' > "$M9/MEMORY_INDEX.md"
check "empty (index only) exits 0" "0" "$(rc "$M9")"

# --------------------------------------------------------------------------
# @-include target: the memory-budget invariant. A project may @-include
# MEMORY_INDEX.md and nothing else from the memory dir.
#
# mkproj <name> <agents-md-body...> -> echoes the memory dir, index + one
# well-formed memory file already in place.
mkproj() {
    local name="$1"; shift
    local root="$WORK/$name" mem="$WORK/$name/.workspace/memory"
    mkdir -p "$mem"
    cat > "$mem/MEMORY_INDEX.md" <<'EOF'
---
auto_loaded_cap: 5000
---

# Memory Index

## project_state.md
- status: active
- last_referenced: 2026-06-01
- tokens: 12
- anchors: (none)
EOF
    printf 'state\n' > "$mem/project_state.md"
    printf '%s\n' "$@" > "$root/AGENTS.md"
    printf '@AGENTS.md\n' > "$root/CLAUDE.md"
    echo "$mem"
}

echo "== @-include target: index only is the passing shape =="
MI1="$(mkproj inc-ok '# ok' '@.workspace/memory/MEMORY_INDEX.md')"
check "index-only include exits 0" "0" "$(rc "$MI1")"

echo "== @-include target: a memory file included directly is a failure =="
MI2="$(mkproj inc-bad '# half-migrated' \
    '@.workspace/memory/MEMORY_INDEX.md' '@.workspace/memory/project_state.md')"
check "direct memory-file include exits 1" "1" "$(rc "$MI2")"
check "names the offending file" "1" \
    "$(grep -c 'project_state.md is @-included directly' <<<"$(out "$MI2")")"
check "points at the migration step" "1" \
    "$(grep -c 'memory-budget-migration.md step 3' <<<"$(out "$MI2")")"
check "counted as an @-include violation, not a field error" "1" \
    "$(grep -c '0 field/status error(s), 1 @-include violation' <<<"$(out "$MI2")")"

echo "== @-include target: transitive include is caught too =="
MI3="$(mkproj inc-transitive '# root' '@docs/extra.md')"
mkdir -p "$WORK/inc-transitive/docs"
printf '@../.workspace/memory/project_state.md\n' > "$WORK/inc-transitive/docs/extra.md"
check "include reached via another file exits 1" "1" "$(rc "$MI3")"

echo "== @-include target: index loaded by nobody is a warning, not a failure =="
MI4="$(mkproj inc-orphan '# includes nothing')"
check "unreferenced index exits 0" "0" "$(rc "$MI4")"
check "warns the index is not @-included" "1" \
    "$(grep -c 'MEMORY_INDEX.md is not @-included' <<<"$(out "$MI4")")"
check "--strict turns it into a failure" "1" "$(rc "$MI4" --strict)"

echo "== @-include target: no seed file at all is not judged =="
MI5="$(mkproj inc-noseed '# placeholder')"
rm -f "$WORK/inc-noseed/AGENTS.md" "$WORK/inc-noseed/CLAUDE.md"
check "no AGENTS.md/CLAUDE.md exits 0" "0" "$(rc "$MI5")"
check "stays silent about includes" "0" \
    "$(grep -c '@-include' <<<"$(out "$MI5")")"

echo "== @-include target: a same-named file outside the memory dir is fine =="
MI6="$(mkproj inc-lookalike '# ok' \
    '@.workspace/memory/MEMORY_INDEX.md' '@docs/project_state.md')"
mkdir -p "$WORK/inc-lookalike/docs"
printf 'unrelated doc that happens to share a name\n' > "$WORK/inc-lookalike/docs/project_state.md"
check "lookalike outside memory dir exits 0" "0" "$(rc "$MI6")"

# --------------------------------------------------------------------------
# Stale `tokens`: a size field that no longer tracks its file is worse than no
# field, because it looks maintained.
#
# mktokens <name> <indexed-tokens> <file-bytes> -> echoes the memory dir.
mktokens() {
    local name="$1" indexed="$2" bytes="$3"
    local mem="$WORK/$name/.workspace/memory"
    mkdir -p "$mem"
    head -c "$bytes" /dev/zero | tr '\0' 'x' > "$mem/project_state.md"
    cat > "$mem/MEMORY_INDEX.md" <<EOF
---
auto_loaded_cap: 5000
---

## project_state.md
- status: active
- last_referenced: 2026-06-01
- tokens: $indexed
- anchors: (none)
EOF
    echo "$mem"
}

echo "== stale tokens: large drift warns and names both numbers =="
T1="$(mktokens tok-stale 33363 400)"   # 400 bytes -> 100 tokens
check "stale tokens still exits 0" "0" "$(rc "$T1")"
check "reports indexed and actual" "1" \
    "$(grep -c 'index says 33363 tokens, file is 100' <<<"$(out "$T1")")"
check "points at the refresh command" "1" \
    "$(grep -c 'memory_init_index.sh' <<<"$(out "$T1")")"
check "--strict promotes it to a failure" "1" "$(rc "$T1" --strict)"

echo "== stale tokens: an accurate entry is silent =="
T2="$(mktokens tok-fresh 100 400)"
check "accurate tokens exits 0" "0" "$(rc "$T2")"
check "no drift warning" "0" "$(grep -c 'index says' <<<"$(out "$T2")")"

echo "== stale tokens: small edits stay under the tolerance =="
T3="$(mktokens tok-small 100 560)"   # 560 bytes -> 140 tokens, +40 < 50 floor
check "40-token drift is not reported" "0" "$(grep -c 'index says' <<<"$(out "$T3")")"

echo "== stale tokens: a big file needs proportional drift, not 50 tokens =="
T4="$(mktokens tok-prop 10000 40800)"  # 10200 actual vs 10000 indexed = 2%
check "2% drift on a large file is not reported" "0" \
    "$(grep -c 'index says' <<<"$(out "$T4")")"
T5="$(mktokens tok-prop-big 10000 60000)"  # 15000 actual vs 10000 = 50%
check "50% drift on a large file is reported" "1" \
    "$(grep -c 'index says' <<<"$(out "$T5")")"

# --------------------------------------------------------------------------
# Per-file caps: "this entry is active and over budget" is the state /memory-gc
# cannot express, because its unit is the whole entry and its signal is
# last_referenced.
#
# mkcap <name> <bytes> <frontmatter-extra> <entry-extra> -> echoes the memory dir.
mkcap() {
    local name="$1" bytes="$2" fm="$3" extra="$4"
    local mem="$WORK/$name/.workspace/memory"
    mkdir -p "$mem"
    head -c "$bytes" /dev/zero | tr '\0' 'x' > "$mem/project_state.md"
    {
        echo '---'
        echo 'auto_loaded_cap: 5000'
        [[ -n "$fm" ]] && echo "$fm"
        echo '---'
        echo
        echo '## project_state.md'
        echo '- status: active'
        echo '- last_referenced: 2026-06-01'
        echo "- tokens: $((bytes / 4))"
        [[ -n "$extra" ]] && echo "$extra"
        echo '- anchors: (none)'
    } > "$mem/MEMORY_INDEX.md"
    echo "$mem"
}

echo "== per-file cap: no cap configured => silent =="
C1="$(mkcap cap-none 4000 '' '')"
check "no cap is silent" "0" "$(grep -c 'over budget' <<<"$(out "$C1")")"

echo "== per-file cap: default_file_cap flags an oversized active entry =="
C2="$(mkcap cap-default 4000 'default_file_cap: 500' '')"
check "over default cap warns" "1" "$(grep -c 'over budget' <<<"$(out "$C2")")"
check "names the archive target" "1" \
    "$(grep -c 'project_state_archive.md' <<<"$(out "$C2")")"
check "says memory-gc will not catch it" "1" \
    "$(grep -c 'memory-gc will not catch this' <<<"$(out "$C2")")"
check "over budget is a warning, not a failure" "0" "$(rc "$C2")"
check "--strict promotes it" "1" "$(rc "$C2" --strict)"

echo "== per-file cap: a file within the default is silent =="
C3="$(mkcap cap-under 400 'default_file_cap: 500' '')"
check "under default cap is silent" "0" "$(grep -c 'over budget' <<<"$(out "$C3")")"

echo "== per-file cap: per-entry cap overrides the project default =="
C4="$(mkcap cap-entry 4000 'default_file_cap: 500' '- cap: 2000')"
check "entry cap raises the ceiling" "0" "$(grep -c 'over budget' <<<"$(out "$C4")")"
C5="$(mkcap cap-entry-low 4000 '' '- cap: 100')"
check "entry cap works without a default" "1" "$(grep -c 'over budget' <<<"$(out "$C5")")"

echo "== per-file cap: cap is not a required field =="
check "absent cap is not reported missing" "0" \
    "$(grep -c 'missing field' <<<"$(out "$C1")")"

echo "== per-file cap: memory_init_index.sh preserves cap fields =="
INIT="$BIN_DIR/memory_init_index.sh"
C6="$(mkcap cap-roundtrip 4000 'default_file_cap: 500' '- cap: 2000')"
printf '@.workspace/memory/MEMORY_INDEX.md\n' > "$WORK/cap-roundtrip/AGENTS.md"
(cd "$WORK/cap-roundtrip" && "$INIT" >/dev/null 2>&1)
check "per-entry cap survives a re-run" "1" "$(grep -c '^- cap: 2000$' "$C6/MEMORY_INDEX.md")"
check "default_file_cap survives a re-run" "1" \
    "$(grep -c '^default_file_cap: 500$' "$C6/MEMORY_INDEX.md")"

# --------------------------------------------------------------------------
# Subdirectories. verify_index.sh globbed `*.md`, so a note under `_inbox/`
# was neither required to have an entry nor reported as missing one.
echo "== subdirectories: an unindexed subdirectory note is a failure =="
SUB="$WORK/subdirs/.workspace/memory"
mkdir -p "$SUB/_inbox" "$SUB/_archive"
printf '# Flat\n' > "$SUB/flat.md"
printf '# Inbox\n' > "$SUB/_inbox/note.md"
printf '# Archived\n' > "$SUB/_archive/old.md"
cat > "$SUB/MEMORY_INDEX.md" <<'EOF'
---
auto_loaded_cap: 5000
---

# Memory Index

## flat.md
- status: active
- last_referenced: 2026-06-01
- tokens: 3
- anchors: -
EOF
set +e
SOUT="$("$VERIFY" --dir "$SUB" 2>&1)"; SRC=$?
set -e
check "missing subdirectory entry fails" "1" "$SRC"
check "the subdirectory note is named by relative path" "1" \
    "$(echo "$SOUT" | grep -c '_inbox/note.md: no entry')"
check "the declined _archive file is reported, not required" "1" \
    "$(echo "$SOUT" | grep -c 'skip: _archive/old.md')"

echo "== subdirectories: adding the entry clears it =="
cat >> "$SUB/MEMORY_INDEX.md" <<'EOF'

## _inbox/note.md
- status: active
- last_referenced: 2026-06-01
- tokens: 3
- anchors: -
EOF
set +e
SOUT2="$("$VERIFY" --dir "$SUB" 2>&1)"; SRC2=$?
set -e
check "indexed subdirectory note passes" "0" "$SRC2"

# --------------------------------------------------------------------------
# A project may maintain its index by hand under another name. The invariant is
# that exactly one memory file is auto-loaded and that it is an index of
# pointers, not that the file is called MEMORY_INDEX.md.
echo "== auto_loaded: a declared index satisfies the include check =="
AL="$WORK/autoloaded"
mkdir -p "$AL/.workspace/memory"
ALM="$AL/.workspace/memory"
printf '# Notes\n' > "$ALM/notes.md"
printf '# Curated index\n\n- [notes](notes.md) - what they say\n' > "$ALM/MEMORY.md"
cat > "$ALM/MEMORY_INDEX.md" <<'EOF'
---
auto_loaded_cap: 5000
auto_loaded: MEMORY.md
---

# Memory Index

## MEMORY.md
- status: active
- last_referenced: 2026-06-01
- tokens: 10
- anchors: -

## notes.md
- status: active
- last_referenced: 2026-06-01
- tokens: 3
- anchors: -
EOF
printf '# Project\n\n@.workspace/memory/MEMORY.md\n' > "$AL/AGENTS.md"
set +e
ALOUT="$(cd "$AL" && "$VERIFY" 2>&1)"; ALRC=$?
set -e
check "declared index is accepted, not a violation" "0" "$ALRC"
check "no @-include violation is reported" "0" \
    "$(echo "$ALOUT" | grep -c '@-include violation')"
check "MEMORY_INDEX.md is not demanded once another index is declared" "0" \
    "$(echo "$ALOUT" | grep -c 'MEMORY_INDEX.md is not @-included')"

echo "== auto_loaded: a memory file that is not the declared index still fails =="
printf '# Project\n\n@.workspace/memory/MEMORY.md\n@.workspace/memory/notes.md\n' > "$AL/AGENTS.md"
set +e
ALOUT2="$(cd "$AL" && "$VERIFY" 2>&1)"; ALRC2=$?
set -e
check "including a memory body alongside the index fails" "1" "$ALRC2"
check "the body is the one named" "1" \
    "$(echo "$ALOUT2" | grep -c 'notes.md is @-included directly')"

echo "== auto_loaded: the declaration survives a re-seed =="
(cd "$AL" && "$INIT" >/dev/null 2>&1)
check "auto_loaded frontmatter is preserved" "1" \
    "$(grep -c '^auto_loaded: MEMORY.md$' "$ALM/MEMORY_INDEX.md")"

echo "== auto_loaded: absent, MEMORY_INDEX.md is still what must be included =="
DEF="$WORK/defaultidx"
mkdir -p "$DEF/.workspace/memory"
printf '# Notes\n' > "$DEF/.workspace/memory/notes.md"
cat > "$DEF/.workspace/memory/MEMORY_INDEX.md" <<'EOF'
---
auto_loaded_cap: 5000
---

# Memory Index

## notes.md
- status: active
- last_referenced: 2026-06-01
- tokens: 3
- anchors: -
EOF
printf '# Project\n\n@.workspace/memory/notes.md\n' > "$DEF/AGENTS.md"
set +e
DOUT="$(cd "$DEF" && "$VERIFY" 2>&1)"; DRC=$?
set -e
check "undeclared project still fails on a direct memory include" "1" "$DRC"
check "the default index is the one named in the advice" "1" \
    "$(echo "$DOUT" | grep -c '@-include only MEMORY_INDEX.md')"

echo
echo "Passed: $PASS  Failed: $FAIL"
[[ "$FAIL" -eq 0 ]]
