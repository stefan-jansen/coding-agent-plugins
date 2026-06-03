#!/usr/bin/env bash
# stamp_gc_run.sh — record that /memory-gc ran today in .index_state.json.
#
# Acceptance criterion 6 (M3 #11): the SessionStart nudge fires only when
# `last_gc_run` is older than 7 days. /memory-gc itself doesn't manage the
# sidecar; it shells out to this helper after a successful run so the nudge
# stays quiet for the next week.
#
# Idempotent. Re-stamping on the same day is a no-op for the timestamp; only
# the version/generated_by fields refresh if absent.
#
# Usage:
#   stamp_gc_run.sh                 Stamp the current project's sidecar.
#   stamp_gc_run.sh --dir DIR       Stamp the sidecar in memory directory DIR.
#   stamp_gc_run.sh --date YYYY-MM-DD  Use an explicit date (default: today UTC).
#   stamp_gc_run.sh -h | --help     Show this help.
set -euo pipefail

usage() {
    sed -n '2,17p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

MEMORY_DIR=""
STAMP_DATE=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dir)     MEMORY_DIR="${2:?--dir needs a directory}"; shift 2 ;;
        --date)    STAMP_DATE="${2:?--date needs a YYYY-MM-DD value}"; shift 2 ;;
        -h|--help) usage; exit 0 ;;
        *) echo "stamp_gc_run.sh: unknown argument '$1'" >&2; usage >&2; exit 2 ;;
    esac
done

if [[ -z "$MEMORY_DIR" ]]; then
    PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
    MEMORY_DIR="$PROJECT_ROOT/.workspace/memory"
fi

if [[ ! -d "$MEMORY_DIR" ]]; then
    echo "stamp_gc_run.sh: memory directory not found: $MEMORY_DIR" >&2
    exit 2
fi

if [[ -z "$STAMP_DATE" ]]; then
    STAMP_DATE="$(date -u +%Y-%m-%d)"
fi

SIDECAR="$MEMORY_DIR/.index_state.json"

python3 - "$SIDECAR" "$STAMP_DATE" <<'PY'
import json
import os
import sys
from pathlib import Path

sidecar = Path(sys.argv[1])
stamp_date = sys.argv[2]

if sidecar.exists():
    try:
        data = json.loads(sidecar.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        data = {}
else:
    data = {}

if not isinstance(data, dict):
    data = {}

data.setdefault("version", 1)
data.setdefault("generated_by", "stamp_gc_run.sh")
data.setdefault("files", {})
data["last_gc_run"] = stamp_date

tmp = sidecar.with_suffix(sidecar.suffix + ".tmp")
tmp.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
os.replace(tmp, sidecar)

print(f"stamp_gc_run: last_gc_run={stamp_date} ({sidecar})")
PY
