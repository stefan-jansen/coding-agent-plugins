#!/usr/bin/env bash
set -euo pipefail

# Vendor the shared workflow steps from coding-agent-toolkit into this
# marketplace's `workflow` plugin.
#
# The toolkit (https://github.com/stefan-jansen/coding-agent-toolkit) is the
# single source of truth for these steps. This repo ships a self-contained
# real copy - never a symlink - so `coding-agent-plugins` can be cloned and
# enabled on its own without the toolkit present (Constraint: Duplication >
# dependency). Edit the steps in the toolkit, then run this to re-vendor.
#
# Usage:
#   scripts/sync-from-toolkit.sh            # copy toolkit -> workflow/skills/
#   scripts/sync-from-toolkit.sh --check    # verify in sync; nonzero on drift
#
# The toolkit is located via $TOOLKIT_DIR, else the sibling
# ../coding-agent-toolkit. In --check mode a missing toolkit is a skip (pass),
# so contributors who cloned only this repo are not blocked.

STEPS=(align continue handoff next-issue plan-issues ship)

PLUGINS_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="$PLUGINS_ROOT/workflow/skills"
TOOLKIT_DIR="${TOOLKIT_DIR:-$PLUGINS_ROOT/../coding-agent-toolkit}"
SRC="$TOOLKIT_DIR/skills"

CHECK=0
[[ "${1:-}" == "--check" ]] && CHECK=1

if [[ ! -d "$SRC" ]]; then
  if [[ $CHECK -eq 1 ]]; then
    echo "sync-from-toolkit: toolkit not found at $TOOLKIT_DIR; skipping drift check." >&2
    exit 0
  fi
  echo "sync-from-toolkit: ERROR toolkit not found at $TOOLKIT_DIR" >&2
  echo "  Set TOOLKIT_DIR, or clone coding-agent-toolkit as a sibling of this repo." >&2
  exit 1
fi

drift=0
for s in "${STEPS[@]}"; do
  if [[ ! -d "$SRC/$s" ]]; then
    echo "sync-from-toolkit: ERROR source step missing: $SRC/$s" >&2
    exit 1
  fi
  if [[ $CHECK -eq 1 ]]; then
    if ! diff -r "$SRC/$s" "$DEST/$s" >/dev/null 2>&1; then
      echo "DRIFT: workflow/skills/$s differs from toolkit source" >&2
      diff -r "$SRC/$s" "$DEST/$s" >&2 || true
      drift=1
    fi
  else
    rm -rf "$DEST/$s"
    cp -R "$SRC/$s" "$DEST/$s"
    echo "synced: workflow/skills/$s"
  fi
done

if [[ $CHECK -eq 1 ]]; then
  if [[ $drift -ne 0 ]]; then
    echo "sync-from-toolkit: DRIFT detected. Run scripts/sync-from-toolkit.sh to re-vendor." >&2
    exit 1
  fi
  echo "sync-from-toolkit: workflow/skills/ in sync with toolkit."
fi
