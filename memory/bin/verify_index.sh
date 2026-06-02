#!/usr/bin/env bash
# verify_index.sh — confirm every memory file has a complete MEMORY_INDEX.md entry.
#
# Index integrity check (Relay acceptance criterion 2). For a project's memory
# directory (default `.workspace/memory/`) it verifies that every `*.md` memory
# file has a corresponding entry in `MEMORY_INDEX.md` carrying all four required
# fields — `status`, `last_referenced`, `tokens`, `anchors`. The index is the
# single source of truth: where a memory file's own frontmatter disagrees with
# the index, the mismatch is reported as a warning that proposes syncing the file
# to the index value (the index wins).
#
# Exit status:
#   0  every memory file has a complete, valid entry (0 missing). Warnings, if
#      any, are printed but do not fail unless --strict is given.
#   1  integrity failure: a memory file has no entry, an entry is missing a
#      required field, or a status value is outside the vocabulary.
#   2  usage / environment error (no memory dir, no MEMORY_INDEX.md to verify).
#
# Usage:
#   verify_index.sh                 Verify the current project (git root, else CWD).
#   verify_index.sh --dir DIR       Verify the memory directory DIR directly.
#   verify_index.sh --strict        Treat warnings as failures (exit 1).
#   verify_index.sh --quiet         Suppress per-file OK lines; show problems only.
#   verify_index.sh -h | --help     Show this help.
#
# MEMORY_INDEX.md format is documented in the plugin README ("MEMORY_INDEX.md
# format"). Pure stdlib bash + Python 3. No third-party dependencies.
set -euo pipefail

BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
    sed -n '2,27p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

MEMORY_DIR=""
STRICT=0
QUIET=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dir)     MEMORY_DIR="${2:?--dir needs a directory}"; shift 2 ;;
        --strict)  STRICT=1; shift ;;
        --quiet)   QUIET=1; shift ;;
        -h|--help) usage; exit 0 ;;
        *) echo "verify_index.sh: unknown argument '$1'" >&2; usage >&2; exit 2 ;;
    esac
done

# Resolve the memory directory: explicit --dir wins; otherwise the conventional
# `.workspace/memory/` under the git root (or CWD when not in a repo).
if [[ -z "$MEMORY_DIR" ]]; then
    PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
    MEMORY_DIR="$PROJECT_ROOT/.workspace/memory"
fi

if [[ ! -d "$MEMORY_DIR" ]]; then
    echo "verify_index.sh: memory directory not found: $MEMORY_DIR" >&2
    exit 2
fi

PYTHONPATH="$BIN_DIR${PYTHONPATH:+:$PYTHONPATH}" python3 - "$MEMORY_DIR" "$STRICT" "$QUIET" <<'PY'
import glob
import os
import re
import sys

MEMORY_DIR = os.path.abspath(sys.argv[1])
STRICT = sys.argv[2] == "1"
QUIET = sys.argv[3] == "1"

INDEX_NAME = "MEMORY_INDEX.md"
INDEX_PATH = os.path.join(MEMORY_DIR, INDEX_NAME)

# Fields every index entry must carry (Relay acceptance criterion 2).
REQUIRED_FIELDS = ("status", "last_referenced", "tokens", "anchors")

# Memory files that are infrastructure, not managed memory entries.
EXCLUDED_FILES = {INDEX_NAME}

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# Claude's own auto-memory (~/.claude/projects/<slug>/memory). We recognize the
# shape for display but never manage it — writes/redirects are out of scope.
DISPLAY_ONLY_RE = re.compile(r"[\\/]\.claude[\\/]projects[\\/][^\\/]+[\\/]memory[\\/]?$")


def is_display_only(path):
    return bool(DISPLAY_ONLY_RE.search(path))


def parse_frontmatter(path):
    """Top-of-file `---` ... `---` block as a flat key->value dict (top level)."""
    out = {}
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    except (OSError, IOError):
        return out
    if not lines or lines[0].strip() != "---":
        return out
    for line in lines[1:]:
        if line.strip() == "---":
            break
        # Only top-level (unindented) key: value pairs.
        if line[:1] in (" ", "\t"):
            continue
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            out[m.group(1).strip().lower()] = m.group(2).strip()
    return out


def parse_index(path):
    """Parse MEMORY_INDEX.md.

    Returns (front, entries, dup_names) where:
      front      flat dict of frontmatter keys (e.g. auto_loaded_cap)
      entries    OrderedDict-like dict: filename -> {field: value}
      dup_names  list of filenames that appeared more than once
    """
    front = {}
    entries = {}
    dup_names = []
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    except (OSError, IOError):
        return front, entries, dup_names

    i = 0
    # Frontmatter (optional).
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", lines[i])
            if m and lines[i][:1] not in (" ", "\t"):
                front[m.group(1).strip().lower()] = m.group(2).strip()
            i += 1
        i += 1  # skip closing ---

    current = None
    for line in lines[i:]:
        head = re.match(r"^##\s+(.+?)\s*$", line)
        if head:
            name = head.group(1).strip()
            # Normalize: strip surrounding backticks/quotes that may decorate it.
            name = name.strip("`").strip('"').strip("'").strip()
            name = os.path.normpath(name)
            if name in entries:
                if name not in dup_names:
                    dup_names.append(name)
            else:
                entries[name] = {}
            current = name
            continue
        if current is None:
            continue
        # Field lines: "- key: value" or "key: value".
        body = line.lstrip()
        if body.startswith("- "):
            body = body[2:]
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", body)
        if m:
            key = m.group(1).strip().lower()
            if key in REQUIRED_FIELDS and key not in entries[current]:
                entries[current][key] = m.group(2).strip()
    return front, entries, dup_names


def valid_status(value):
    if value in ("active", "dormant", "deprecated"):
        return True
    if value.startswith("superseded-by:"):
        return len(value[len("superseded-by:"):].strip()) > 0
    return False


def is_empty_anchor(value):
    return value.lower() in ("", "none", "n/a", "na", "-")


def main():
    failures = []   # hard integrity problems -> exit 1
    warnings = []   # advisory -> exit 0 unless --strict
    ok_files = []

    display_only = is_display_only(MEMORY_DIR)

    memory_files = sorted(
        os.path.basename(p)
        for p in glob.glob(os.path.join(MEMORY_DIR, "*.md"))
        if os.path.basename(p) not in EXCLUDED_FILES
    )

    print("Memory directory: %s" % MEMORY_DIR)

    if display_only:
        print("Note: this is Claude's auto-memory shape "
              "(~/.claude/projects/.../memory) — display-only, not managed.")
        if not os.path.isfile(INDEX_PATH):
            # No managed index here; recognize and list, but do not fail.
            print("  %d memory file(s) recognized; no %s (unmanaged shape)."
                  % (len(memory_files), INDEX_NAME))
            for name in memory_files:
                print("    - %s" % name)
            return 0

    if not os.path.isfile(INDEX_PATH):
        sys.stderr.write(
            "verify_index.sh: no %s in %s — nothing to verify against.\n"
            "  Initialize one with bin/memory_init_index.sh (see README).\n"
            % (INDEX_NAME, MEMORY_DIR)
        )
        return 2

    front, entries, dup_names = parse_index(INDEX_PATH)
    print("Index: %s" % INDEX_PATH)
    if "auto_loaded_cap" in front:
        print("auto_loaded_cap: %s" % front["auto_loaded_cap"])
    else:
        warnings.append("MEMORY_INDEX.md frontmatter has no 'auto_loaded_cap' "
                        "(recommended; set per-project cap).")

    for name in dup_names:
        warnings.append("%s: duplicate index entry (only the first is used)." % name)

    # 1. Every memory file must have a complete, valid entry.
    for name in memory_files:
        entry = entries.get(name)
        if entry is None:
            failures.append("%s: no entry in %s" % (name, INDEX_NAME))
            continue

        missing_fields = [f for f in REQUIRED_FIELDS if f not in entry]
        if missing_fields:
            failures.append("%s: entry missing field(s): %s"
                            % (name, ", ".join(missing_fields)))

        status = entry.get("status")
        if status is not None and not valid_status(status):
            failures.append(
                "%s: invalid status %r (expected active|dormant|deprecated|"
                "superseded-by:<slug>)" % (name, status))

        # Soft value checks (warnings, not failures).
        tokens = entry.get("tokens")
        if tokens is not None and not tokens.isdigit():
            warnings.append("%s: tokens value %r is not an integer." % (name, tokens))
        lref = entry.get("last_referenced")
        if lref is not None and lref.lower() != "never" and not DATE_RE.match(lref):
            warnings.append("%s: last_referenced %r is not YYYY-MM-DD or 'never'."
                            % (name, lref))

        # Index-vs-file-frontmatter authority (index wins). Report mismatches.
        fm = parse_frontmatter(os.path.join(MEMORY_DIR, name))
        for field in ("status", "tokens", "last_referenced"):
            if field in fm and field in entry and fm[field] != entry[field]:
                warnings.append(
                    "%s: file frontmatter %s=%r conflicts with index %s=%r; "
                    "index wins — sync file to %r."
                    % (name, field, fm[field], field, entry[field], entry[field]))

        if not missing_fields and (status is None or valid_status(status)):
            ok_files.append(name)

    # 2. Orphan entries (index entry with no corresponding file) — advisory.
    for name in entries:
        if name not in memory_files:
            status = entries[name].get("status", "")
            note = ""
            if status == "deprecated" or status.startswith("superseded-by:"):
                note = " (status=%s — may intentionally outlive the file)" % status
            warnings.append("%s: index entry has no matching file%s" % (name, note))

    # Report.
    if not QUIET:
        for name in ok_files:
            print("  ok: %s" % name)

    missing_count = sum(1 for f in failures if "no entry in" in f)

    if warnings:
        print("Warnings (%d):" % len(warnings))
        for w in warnings:
            print("  - %s" % w)

    if failures:
        print("Failures (%d):" % len(failures))
        for f in failures:
            print("  - %s" % f)

    field_errors = len(failures) - missing_count
    if failures:
        print("Result: FAIL — %d missing entr%s, %d field/status error(s)."
              % (missing_count, "y" if missing_count == 1 else "ies", field_errors))
        return 1
    if STRICT and warnings:
        print("Result: FAIL (--strict) — 0 missing entries, %d warning(s)."
              % len(warnings))
        return 1
    print("Result: OK — 0 missing entries, %d file(s) verified." % len(ok_files))
    return 0


sys.exit(main())
PY
