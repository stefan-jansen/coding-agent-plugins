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

echo
echo "Passed: $PASS  Failed: $FAIL"
[[ "$FAIL" -eq 0 ]]
