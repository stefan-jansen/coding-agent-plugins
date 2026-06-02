#!/usr/bin/env bash
# measure_memory.sh — sum the tokens Claude/Codex auto-load for a project.
#
# "Auto-loaded" = CLAUDE.md and AGENTS.md at the project root plus every file
# reachable from them via @-include (transitively). Token counts come from the
# shared helper token_count.py, so this script and all downstream memory tooling
# report the same numbers.
#
# Usage:
#   measure_memory.sh                 Measure the current project (git root, else CWD).
#   measure_memory.sh --total-only    Print just the integer token total (for scripts).
#   measure_memory.sh --all-projects  Per-project totals under the search root.
#   measure_memory.sh --root DIR      Search root for --all-projects (default: $HOME).
#   measure_memory.sh --max-depth N   Max directory depth to scan in --all-projects (default 6).
#   measure_memory.sh -h | --help     Show this help.
#
# Pure stdlib bash + Python 3. No third-party dependencies.
set -euo pipefail

BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
    sed -n '2,17p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

MODE="single"
TOTAL_ONLY=0
SEARCH_ROOT="${MEMORY_PROJECTS_ROOT:-$HOME}"
MAX_DEPTH=6

while [[ $# -gt 0 ]]; do
    case "$1" in
        --all-projects) MODE="all"; shift ;;
        --total-only)   TOTAL_ONLY=1; shift ;;
        --root)         SEARCH_ROOT="${2:?--root needs a directory}"; shift 2 ;;
        --max-depth)    MAX_DEPTH="${2:?--max-depth needs a number}"; shift 2 ;;
        -h|--help)      usage; exit 0 ;;
        *) echo "measure_memory.sh: unknown argument '$1'" >&2; usage >&2; exit 2 ;;
    esac
done

if [[ "$MODE" == "single" ]]; then
    PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
    PY_MODE=$([[ "$TOTAL_ONLY" == "1" ]] && echo "single-total" || echo "single")
    TARGET="$PROJECT_ROOT"
else
    PY_MODE="all"
    TARGET="$SEARCH_ROOT"
fi

PYTHONPATH="$BIN_DIR${PYTHONPATH:+:$PYTHONPATH}" python3 - "$PY_MODE" "$TARGET" "$MAX_DEPTH" <<'PY'
import os
import sys

from token_count import count_file

MODE, TARGET, MAX_DEPTH = sys.argv[1], sys.argv[2], int(sys.argv[3])

# Files Claude/Codex read on every session before any @-include expansion.
SEED_FILES = ("CLAUDE.md", "AGENTS.md")

# Directories never worth descending into when discovering projects.
PRUNE_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__", ".mypy_cache",
    ".pytest_cache", ".tox", "dist", "build", ".next", ".cache", ".idea",
}


def parse_includes(path):
    """@-include targets declared in `path`, as absolute, normalized paths.

    An include is a line whose entire content is `@<relative-path>` (optionally
    surrounded by whitespace) — the canonical Claude Code / Codex form. Mentions
    of @path inside prose or fenced code blocks are deliberately ignored, since
    Claude does not expand those either.
    """
    out = []
    base = os.path.dirname(path)
    in_fence = False
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                stripped = line.strip()
                if stripped.startswith("```") or stripped.startswith("~~~"):
                    in_fence = not in_fence
                    continue
                if in_fence or not stripped.startswith("@"):
                    continue
                ref = stripped[1:]
                if not ref or any(c.isspace() for c in ref):
                    continue
                out.append(os.path.normpath(os.path.join(base, ref)))
    except (OSError, IOError):
        pass
    return out


def reachable(project_root):
    """(ordered existing files, missing-include paths) auto-loaded for a project.

    Breadth-first from the seed files, following @-includes transitively and
    de-duplicating. Missing include targets are reported separately rather than
    silently dropped.
    """
    seen, order, missing = set(), [], []
    queue = []
    for name in SEED_FILES:
        p = os.path.normpath(os.path.join(project_root, name))
        if os.path.isfile(p):
            queue.append(p)
    while queue:
        cur = queue.pop(0)
        if cur in seen:
            continue
        seen.add(cur)
        order.append(cur)
        for inc in parse_includes(cur):
            if inc in seen:
                continue
            if os.path.isfile(inc):
                queue.append(inc)
            elif inc not in missing:
                missing.append(inc)
    return order, missing


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


def print_single(project_root):
    counted, missing, total = measure(project_root)
    print("Project: %s" % project_root)
    if not counted:
        print("  (no CLAUDE.md / AGENTS.md — nothing auto-loaded)")
        print("  Total auto-loaded: 0 tokens (0 files)")
        return
    width = max(len(rel(f, project_root)) for f, _ in counted)
    for f, n in counted:
        print("  %-*s  %6d tokens" % (width, rel(f, project_root), n))
    print("  %s" % ("-" * (width + 16)))
    print("  Total auto-loaded: %d tokens (%d files)" % (total, len(counted)))
    if missing:
        print("  Unresolved @-includes (%d):" % len(missing))
        for m in missing:
            print("    - %s" % rel(m, project_root))


if MODE == "single-total":
    _, _, total = measure(TARGET)
    print(total)
elif MODE == "single":
    print_single(TARGET)
elif MODE == "all":
    projects = find_projects(TARGET, MAX_DEPTH)
    print("Per-project auto-loaded memory under %s" % os.path.abspath(TARGET))
    print("%9s  %5s  %s" % ("TOKENS", "FILES", "PROJECT"))
    grand = 0
    rows = []
    for p in projects:
        counted, _, total = measure(p)
        rows.append((total, len(counted), p))
        grand += total
    for total, nfiles, p in sorted(rows, key=lambda r: r[0], reverse=True):
        print("%9d  %5d  %s" % (total, nfiles, p))
    print("%9s  %5s  %s" % ("-" * 9, "-" * 5, "-" * 7))
    print("%9d  %5d  %d project(s)" % (grand, sum(r[1] for r in rows), len(rows)))
else:
    sys.stderr.write("measure_memory.sh: unknown mode %r\n" % MODE)
    sys.exit(2)
PY
