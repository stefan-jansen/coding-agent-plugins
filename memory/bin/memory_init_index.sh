#!/usr/bin/env bash
# memory_init_index.sh — seed MEMORY_INDEX.md + .index_state.json from an
# existing `.workspace/memory/`.
#
# One-shot migration / initialization command (Relay M1 deliverable). It walks a
# project's memory directory, counts tokens via the shared helper token_count.py,
# and writes two artifacts:
#
#   MEMORY_INDEX.md     The auto-loaded index (committed; source of truth).
#                       One `## <file>.md` entry per memory file, each carrying
#                       status / last_referenced / tokens / anchors. This is the
#                       single file a project should @-include going forward.
#   .index_state.json   Gitignored runtime sidecar (see "Sidecar contract"
#                       below) holding the fast-moving signals: per-file
#                       last_referenced + reference counts and the project-level
#                       last_gc_run. Missing sidecar == empty/initial state.
#
# The walk is recursive (bin/memory_files.py owns the rules): a note in a
# subdirectory such as `_inbox/` is a memory file, and every entry is keyed by
# its path relative to the memory directory, so two notes with the same basename
# in different subdirectories do not collide. `_archive/` and dot-directories
# are declined, and each declined file is printed with its reason rather than
# passed over in silence.
#
# Idempotent. Re-running preserves work already done: existing index statuses
# and anchors are kept (GC owns those), accumulated signal state in the sidecar
# is retained, and tokens are recomputed from the current file contents. New
# files are added as status `active`; entries whose file disappeared are dropped
# from the sidecar (and reported). Per-project rollout is out of scope - projects
# run this when they choose to opt in.
#
# Sidecar contract (.workspace/memory/.index_state.json):
#   {
#     "version": 1,                      schema version (int)
#     "generated_by": "memory_init_index.sh",
#     "generated_at": "YYYY-MM-DD",      last time this script wrote the sidecar
#     "last_gc_run": null | "YYYY-MM-DD",  null until /memory-gc first runs
#     "files": {
#       "<path>.md": {                   key is relative to the memory dir
#         "last_referenced": "YYYY-MM-DD" | "never",
#         "references": <int>            count of captured read/grep signals
#       }, ...
#     }
#   }
#   - Runtime state, NOT a source of truth: gitignored; MEMORY_INDEX.md wins on
#     any conflict. A missing sidecar is treated as initial/empty state.
#   - The PreToolUse reference hook bumps files.<path>.last_referenced to today
#     and increments references; /memory-gc stamps last_gc_run. Unknown keys
#     (top-level or per-file) added by other tooling are preserved across re-runs.
#
# Usage:
#   memory_init_index.sh                Initialize the current project (git root, else CWD).
#   memory_init_index.sh --dir DIR      Operate on the memory directory DIR directly.
#   memory_init_index.sh --cap N        Set auto_loaded_cap: N in the index frontmatter.
#   memory_init_index.sh --quiet        Print only the summary line.
#   memory_init_index.sh -h | --help    Show this help.
#
# Existing `auto_loaded_cap`, `default_file_cap` and `auto_loaded` frontmatter in
# MEMORY_INDEX.md is preserved; --cap overrides the first. The cap value itself is decided downstream (Relay M2); init does
# not invent one. Pure stdlib bash + Python 3. No third-party dependencies.
set -euo pipefail

BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
    sed -n '2,60p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

MEMORY_DIR=""
CAP=""
QUIET=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dir)     MEMORY_DIR="${2:?--dir needs a directory}"; shift 2 ;;
        --cap)     CAP="${2:?--cap needs a number}"; shift 2 ;;
        --quiet)   QUIET=1; shift ;;
        -h|--help) usage; exit 0 ;;
        *) echo "memory_init_index.sh: unknown argument '$1'" >&2; usage >&2; exit 2 ;;
    esac
done

# Resolve the memory directory: explicit --dir wins, then $CLAUDE_MEMORY_DIR
# (absolute, or relative to the project root), then the conventional
# `.workspace/memory/` under the git root (or CWD when not in a repo).
# Mirrors bin/memory_dir.py; kept inline so this script stands alone.
if [[ -z "$MEMORY_DIR" ]]; then
    PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
    if [[ -n "${CLAUDE_MEMORY_DIR:-}" ]]; then
        case "$CLAUDE_MEMORY_DIR" in
            /*) MEMORY_DIR="$CLAUDE_MEMORY_DIR" ;;
            *)  MEMORY_DIR="$PROJECT_ROOT/$CLAUDE_MEMORY_DIR" ;;
        esac
    else
        MEMORY_DIR="$PROJECT_ROOT/.workspace/memory"
    fi
fi

if [[ ! -d "$MEMORY_DIR" ]]; then
    echo "memory_init_index.sh: memory directory not found: $MEMORY_DIR" >&2
    echo "  Nothing to initialize. Create $MEMORY_DIR first." >&2
    exit 2
fi

if [[ -n "$CAP" && ! "$CAP" =~ ^[0-9]+$ ]]; then
    echo "memory_init_index.sh: --cap must be a non-negative integer, got '$CAP'" >&2
    exit 2
fi

PYTHONPATH="$BIN_DIR${PYTHONPATH:+:$PYTHONPATH}" python3 - "$MEMORY_DIR" "$CAP" "$QUIET" <<'PY'
import datetime
import json
import os
import re
import sys

from memory_files import discover
from token_count import count_file

MEMORY_DIR = os.path.abspath(sys.argv[1])
CAP = sys.argv[2]            # "" if not given
QUIET = sys.argv[3] == "1"

INDEX_NAME = "MEMORY_INDEX.md"
SIDECAR_NAME = ".index_state.json"
LOCK_NAME = ".index_state.lock"
GITIGNORE_NAME = ".gitignore"
INDEX_PATH = os.path.join(MEMORY_DIR, INDEX_NAME)
SIDECAR_PATH = os.path.join(MEMORY_DIR, SIDECAR_NAME)
GITIGNORE_PATH = os.path.join(MEMORY_DIR, GITIGNORE_NAME)

SIDECAR_VERSION = 1
REQUIRED_FIELDS = ("status", "last_referenced", "tokens", "anchors")

# Optional per-entry fields. Not seeded, but preserved verbatim across
# re-runs: a schema field this script silently dropped would be worse
# than no field at all.
OPTIONAL_FIELDS = ("cap",)
KNOWN_FIELDS = REQUIRED_FIELDS + OPTIONAL_FIELDS
EMPTY_ANCHOR = "-"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def today():
    """Today as YYYY-MM-DD; MEMORY_TODAY overrides it for deterministic tests."""
    override = os.environ.get("MEMORY_TODAY", "").strip()
    if DATE_RE.match(override):
        return override
    return datetime.date.today().isoformat()


def mtime_date(path):
    """File modification time as YYYY-MM-DD (a sensible last_referenced seed)."""
    try:
        ts = os.path.getmtime(path)
    except OSError:
        return today()
    return datetime.date.fromtimestamp(ts).isoformat()


def valid_status(value):
    if value in ("active", "dormant", "deprecated"):
        return True
    return value.startswith("superseded-by:") and bool(
        value[len("superseded-by:"):].strip())


def parse_existing_index(path):
    """Existing MEMORY_INDEX.md as (frontmatter dict, {name: {field: value}}).

    Mirrors the parser in verify_index.sh so init and verify agree on the
    format: optional `---` frontmatter, then `## <name>` headings followed by
    `- key: value` field lines.
    """
    front = {}
    entries = {}
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    except (OSError, IOError):
        return front, entries

    i = 0
    if lines and lines[0].strip() == "---":
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            if lines[i][:1] not in (" ", "\t"):
                m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", lines[i])
                if m:
                    front[m.group(1).strip().lower()] = m.group(2).strip()
            i += 1
        i += 1  # skip closing ---

    current = None
    for line in lines[i:]:
        head = re.match(r"^#{2,3}\s+(.+?)\s*$", line)
        if head:
            name = head.group(1).strip().strip("`").strip('"').strip("'").strip()
            name = os.path.normpath(name)
            entries.setdefault(name, {})
            current = name
            continue
        if current is None:
            continue
        body = line.lstrip()
        if body.startswith("- "):
            body = body[2:]
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", body)
        if m:
            key = m.group(1).strip().lower()
            if key in KNOWN_FIELDS and key not in entries[current]:
                entries[current][key] = m.group(2).strip()
    return front, entries


def load_sidecar(path):
    """Existing sidecar dict, or {} when missing/unreadable (initial state)."""
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, dict) else {}
    except (OSError, IOError, ValueError):
        return {}


def render_index(cap, default_file_cap, auto_loaded, entries_in_order):
    """Build the MEMORY_INDEX.md text. Deterministic: no volatile fields."""
    out = []
    out.append("---")
    out.append("# Auto-generated by memory_init_index.sh and maintained by /memory-gc.")
    if auto_loaded != "":
        out.append("# %s is what this project @-includes; nothing else from this" % auto_loaded)
        out.append("# directory may be auto-loaded. This file holds the status of every entry.")
    else:
        out.append("# This is the single auto-loaded memory artifact; @-include only this file.")
    out.append("# Edit statuses through /memory-gc, not by hand. The index is the source of")
    out.append("# truth: it wins over individual memory-file frontmatter on any conflict.")
    if cap != "":
        out.append("auto_loaded_cap: %s" % cap)
    if default_file_cap != "":
        out.append("default_file_cap: %s" % default_file_cap)
    if auto_loaded != "":
        out.append("auto_loaded: %s" % auto_loaded)
    out.append("---")
    out.append("")
    out.append("# Memory Index")
    out.append("")
    if not entries_in_order:
        out.append("_No memory files found in this directory yet._")
        out.append("")
        return "\n".join(out) + "\n"
    for name, e in entries_in_order:
        out.append("## %s" % name)
        out.append("- status: %s" % e["status"])
        out.append("- last_referenced: %s" % e["last_referenced"])
        out.append("- tokens: %d" % e["tokens"])
        if e.get("cap"):
            out.append("- cap: %s" % e["cap"])
        out.append("- anchors: %s" % e["anchors"])
        out.append("")
    return "\n".join(out) + "\n"


def ensure_gitignored():
    """Ignore the runtime sidecar and its lockfile from within the memory dir.

    The lockfile is created by the PreToolUse hook next to the sidecar; it was
    left out of the original rule and showed up as untracked in every project.
    """
    wanted = [SIDECAR_NAME, LOCK_NAME]
    existing = []
    if os.path.isfile(GITIGNORE_PATH):
        try:
            with open(GITIGNORE_PATH, "r", encoding="utf-8") as fh:
                existing = fh.read().splitlines()
        except (OSError, IOError):
            existing = []
    have = {l.strip() for l in existing}
    missing = [l for l in wanted if l not in have]
    if not missing:
        return False
    with open(GITIGNORE_PATH, "a", encoding="utf-8") as fh:
        if existing and existing[-1].strip() != "":
            fh.write("\n")
        if SIDECAR_NAME in missing:
            fh.write("# Runtime signal sidecar - not a source of truth (Relay memory index).\n")
        for line in missing:
            fh.write(line + "\n")
    return True


def main():
    now = today()
    cap = CAP

    old_front, old_entries = parse_existing_index(INDEX_PATH)
    if cap == "" and "auto_loaded_cap" in old_front:
        cap = old_front["auto_loaded_cap"]   # preserve a previously-set cap
    # Project-wide per-file budget. Never seeded, only preserved.
    default_file_cap = old_front.get("default_file_cap", "")
    # The memory file this project @-includes as its index. Defaults to this
    # index; a project that maintains a richer one by hand names it here so
    # verify_index.sh checks the right file. Never seeded, only preserved.
    auto_loaded = old_front.get("auto_loaded", "")

    sidecar = load_sidecar(SIDECAR_PATH)
    old_files = sidecar.get("files")
    if not isinstance(old_files, dict):
        old_files = {}

    memory_files, skipped_files = discover(MEMORY_DIR)

    index_entries = []
    new_files_state = {}
    added, kept = [], []

    for name in memory_files:
        full = os.path.join(MEMORY_DIR, name)
        tokens = count_file(full)

        prior_index = old_entries.get(name, {})
        prior_sig = old_files.get(name) if isinstance(old_files.get(name), dict) else {}

        # Status / anchors: keep whatever the index already recorded (GC owns
        # these); default new files to active with a stubbed anchor.
        status = prior_index.get("status", "")
        if not valid_status(status):
            status = "active"
        anchors = prior_index.get("anchors", "").strip() or EMPTY_ANCHOR

        # last_referenced: sidecar signal first, then prior index, then file mtime.
        lref = prior_sig.get("last_referenced")
        if not (isinstance(lref, str) and (DATE_RE.match(lref) or lref == "never")):
            lref = prior_index.get("last_referenced", "")
        if not (DATE_RE.match(lref) or lref == "never"):
            lref = mtime_date(full)

        references = prior_sig.get("references")
        if not isinstance(references, int) or references < 0:
            references = 0

        index_entries.append((name, {
            "status": status,
            "last_referenced": lref,
            "tokens": tokens,
            "cap": prior_index.get("cap", "").strip(),
            "anchors": anchors,
        }))

        # Preserve any extra signal fields other tooling may have added.
        state = dict(prior_sig)
        state["last_referenced"] = lref
        state["references"] = references
        new_files_state[name] = state

        (added if name not in old_entries else kept).append(name)

    dropped = sorted(set(old_files) - set(memory_files))

    # Write the index.
    with open(INDEX_PATH, "w", encoding="utf-8") as fh:
        fh.write(render_index(cap, default_file_cap, auto_loaded, index_entries))

    # Write the sidecar, preserving unknown top-level keys and last_gc_run.
    last_gc_run = sidecar.get("last_gc_run", None)
    if not (last_gc_run is None or (isinstance(last_gc_run, str) and DATE_RE.match(last_gc_run))):
        last_gc_run = None
    new_sidecar = dict(sidecar)
    new_sidecar.update({
        "version": SIDECAR_VERSION,
        "generated_by": "memory_init_index.sh",
        "generated_at": now,
        "last_gc_run": last_gc_run,
        "files": new_files_state,
    })
    with open(SIDECAR_PATH, "w", encoding="utf-8") as fh:
        json.dump(new_sidecar, fh, indent=2, sort_keys=True)
        fh.write("\n")

    gitignore_added = ensure_gitignored()

    if not QUIET:
        print("Memory directory: %s" % MEMORY_DIR)
        print("Index:   %s" % INDEX_PATH)
        print("Sidecar: %s" % SIDECAR_PATH)
        if cap != "":
            print("auto_loaded_cap: %s" % cap)
        for name, e in index_entries:
            tag = "new" if name not in old_entries else "kept"
            print("  %-4s %-32s %6d tokens  [%s]" % (tag, name, e["tokens"], e["status"]))
        for name in dropped:
            print("  drop %-32s (file gone - removed from sidecar)" % name)
        for name, reason in skipped_files:
            print("  skip %-32s (%s)" % (name, reason))
        if gitignore_added:
            print("Updated %s (sidecar + lockfile ignored)" % GITIGNORE_PATH)
    print("Initialized index: %d entr%s (%d new, %d kept, %d dropped%s)."
          % (len(index_entries), "y" if len(index_entries) == 1 else "ies",
             len(added), len(kept), len(dropped),
             ", %d skipped" % len(skipped_files) if skipped_files else ""))
    return 0


sys.exit(main())
PY
