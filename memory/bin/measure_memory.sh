#!/usr/bin/env bash
# measure_memory.sh — sum the tokens Claude/Codex auto-load for a project.
#
# "Auto-loaded" = CLAUDE.md and AGENTS.md at the project root plus every file
# reachable from them via @-include (transitively). Token counts come from the
# shared helper token_count.py, so this script and all downstream memory tooling
# report the same numbers.
#
# The per-project budget (`auto_loaded_cap`) is read from
# `.workspace/memory/.index_state.json`, falling back to `MEMORY_INDEX.md`
# frontmatter. Human-readable output always reports the total against it.
# `--check` additionally makes exceeding the cap a non-zero exit, so the budget
# can gate a pre-commit hook or CI. Without `--check` the exit status is
# unchanged (0), so existing `--total-only` callers keep working.
#
# Usage:
#   measure_memory.sh                 Measure the current project (git root, else CWD).
#   measure_memory.sh --total-only    Print just the integer token total (for scripts).
#   measure_memory.sh --check         Exit 1 if the total exceeds the cap.
#   measure_memory.sh --cap N         Use N as the cap instead of the project's.
#   measure_memory.sh --all-projects  Per-project totals under the search root.
#   measure_memory.sh --root DIR      Search root for --all-projects (default: $HOME).
#   measure_memory.sh --max-depth N   Max directory depth to scan in --all-projects (default 6).
#   measure_memory.sh -h | --help     Show this help.
#
# Exit status:
#   0  measured (and, with --check, within cap or no cap configured)
#   1  --check given and the auto-loaded total exceeds the cap
#   2  usage error
#
# Pure stdlib bash + Python 3. No third-party dependencies.
set -euo pipefail

BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
    # Print the header comment block: every leading `#` line after the shebang,
    # stopping at the first non-comment line. Derived rather than hardcoded, so
    # editing the header cannot silently truncate --help.
    sed -n '2,${/^#/!q;p;}' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

MODE="single"
TOTAL_ONLY=0
CHECK=0
CAP_OVERRIDE=""
SEARCH_ROOT="${MEMORY_PROJECTS_ROOT:-$HOME}"
MAX_DEPTH=6

while [[ $# -gt 0 ]]; do
    case "$1" in
        --all-projects) MODE="all"; shift ;;
        --total-only)   TOTAL_ONLY=1; shift ;;
        --check)        CHECK=1; shift ;;
        --cap)          CAP_OVERRIDE="${2:?--cap needs a number}"; shift 2 ;;
        --root)         SEARCH_ROOT="${2:?--root needs a directory}"; shift 2 ;;
        --max-depth)    MAX_DEPTH="${2:?--max-depth needs a number}"; shift 2 ;;
        -h|--help)      usage; exit 0 ;;
        *) echo "measure_memory.sh: unknown argument '$1'" >&2; usage >&2; exit 2 ;;
    esac
done

if [[ -n "$CAP_OVERRIDE" && ! "$CAP_OVERRIDE" =~ ^[0-9]+$ ]]; then
    echo "measure_memory.sh: --cap needs a non-negative integer, got '$CAP_OVERRIDE'" >&2
    exit 2
fi

if [[ "$MODE" == "single" ]]; then
    PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
    PY_MODE=$([[ "$TOTAL_ONLY" == "1" ]] && echo "single-total" || echo "single")
    TARGET="$PROJECT_ROOT"
else
    PY_MODE="all"
    TARGET="$SEARCH_ROOT"
fi

PYTHONPATH="$BIN_DIR${PYTHONPATH:+:$PYTHONPATH}" python3 - \
    "$PY_MODE" "$TARGET" "$MAX_DEPTH" "$CHECK" "$CAP_OVERRIDE" <<'PY'
import json
import os
import re
import sys

from include_graph import SEED_FILES, reachable
from token_count import count_file

MODE, TARGET, MAX_DEPTH = sys.argv[1], sys.argv[2], int(sys.argv[3])
CHECK = sys.argv[4] == "1"
CAP_OVERRIDE = int(sys.argv[5]) if sys.argv[5] else None

# Directories never worth descending into when discovering projects.
PRUNE_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__", ".mypy_cache",
    ".pytest_cache", ".tox", "dist", "build", ".next", ".cache", ".idea",
}

CAP_RE = re.compile(r"^auto_loaded_cap:\s*(\d+)\s*$")


def read_cap(project_root):
    """The project's `auto_loaded_cap`, or None when it has not set one.

    Migration step 2 says "choose a cap"; this is where the chosen number is
    read back. The runtime sidecar wins over the index frontmatter, since
    /memory-gc maintains it; the frontmatter is the committed fallback for a
    project whose gitignored sidecar has not been written yet.
    """
    if CAP_OVERRIDE is not None:
        return CAP_OVERRIDE

    memory_dir = os.path.join(project_root, ".workspace", "memory")

    try:
        with open(os.path.join(memory_dir, ".index_state.json"),
                  "r", encoding="utf-8") as fh:
            data = json.load(fh)
        cap = data.get("auto_loaded_cap") if isinstance(data, dict) else None
        if isinstance(cap, int) and cap > 0:
            return cap
    except (OSError, IOError, ValueError):
        pass

    try:
        with open(os.path.join(memory_dir, "MEMORY_INDEX.md"),
                  "r", encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except (OSError, IOError):
        return None
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = CAP_RE.match(line.strip())
        if m:
            return int(m.group(1))
    return None


def measure(project_root):
    files, missing = reachable(project_root)
    counted = [(f, count_file(f)) for f in files]
    total = sum(n for _, n in counted)
    return counted, missing, total


def rel(path, root):
    try:
        return os.path.relpath(path, root)
    except ValueError:
        return path


def find_projects(root, max_depth):
    """Project roots under `root`: directories containing CLAUDE.md or AGENTS.md."""
    root = os.path.abspath(root)
    projects = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in PRUNE_DIRS and not d.startswith(".git")]
        depth = dirpath[len(root):].count(os.sep)
        if depth >= max_depth:
            dirnames[:] = []
        if any(name in filenames for name in SEED_FILES):
            projects.append(dirpath)
    return sorted(set(projects))


def print_budget(total, cap, indent="  "):
    """Report the total against the cap. Returns True when over."""
    if cap is None:
        print("%sBudget: no auto_loaded_cap set "
              "(see docs/memory-budget-migration.md step 2)." % indent)
        return False
    pct = round(100.0 * total / cap) if cap else 0
    verdict = "OVER CAP" if total > cap else "within cap"
    print("%sBudget: %d / %d tokens (%d%% of cap) — %s"
          % (indent, total, cap, pct, verdict))
    return total > cap


def print_single(project_root):
    counted, missing, total = measure(project_root)
    cap = read_cap(project_root)
    print("Project: %s" % project_root)
    if not counted:
        print("  (no CLAUDE.md / AGENTS.md — nothing auto-loaded)")
        print("  Total auto-loaded: 0 tokens (0 files)")
        return False
    width = max(len(rel(f, project_root)) for f, _ in counted)
    for f, n in counted:
        print("  %-*s  %6d tokens" % (width, rel(f, project_root), n))
    print("  %s" % ("-" * (width + 16)))
    print("  Total auto-loaded: %d tokens (%d files)" % (total, len(counted)))
    over = print_budget(total, cap)
    if over:
        print("  Trim the auto-loaded set: @-include only MEMORY_INDEX.md and "
              "read memory files on demand, or shrink what is included.")
    if missing:
        print("  Unresolved @-includes (%d):" % len(missing))
        for m in missing:
            print("    - %s" % rel(m, project_root))
    return over


over_cap = False

if MODE == "single-total":
    _, _, total = measure(TARGET)
    print(total)
    cap = read_cap(TARGET)
    over_cap = cap is not None and total > cap
elif MODE == "single":
    over_cap = print_single(TARGET)
elif MODE == "all":
    projects = find_projects(TARGET, MAX_DEPTH)
    print("Per-project auto-loaded memory under %s" % os.path.abspath(TARGET))
    print("%9s  %9s  %5s  %s" % ("TOKENS", "CAP", "FILES", "PROJECT"))
    grand = 0
    rows = []
    for p in projects:
        counted, _, total = measure(p)
        cap = read_cap(p)
        rows.append((total, cap, len(counted), p))
        grand += total
    n_over = 0
    for total, cap, nfiles, p in sorted(rows, key=lambda r: r[0], reverse=True):
        over = cap is not None and total > cap
        n_over += 1 if over else 0
        print("%9d  %9s  %5d  %s%s"
              % (total, "-" if cap is None else cap, nfiles, p,
                 "  <- OVER CAP" if over else ""))
    print("%9s  %9s  %5s  %s" % ("-" * 9, "-" * 9, "-" * 5, "-" * 7))
    print("%9d  %9s  %5d  %d project(s), %d over cap"
          % (grand, "", sum(r[2] for r in rows), len(rows), n_over))
    over_cap = n_over > 0
else:
    sys.stderr.write("measure_memory.sh: unknown mode %r\n" % MODE)
    sys.exit(2)

# The budget is advisory unless --check asks it to gate.
sys.exit(1 if (CHECK and over_cap) else 0)
PY
