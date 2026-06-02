#!/usr/bin/env bash
# check_anchors.sh — resolve each MEMORY_INDEX.md entry's anchors against the tree.
#
# Anchor validity is the second cheap relevance signal (Relay acceptance
# criterion 4). For every `## <file>` entry in MEMORY_INDEX.md it reads the
# `anchors` field and resolves each anchor against the working tree, reporting
# one of:
#   present  the anchor resolves (file exists / command on PATH / symbol found)
#   missing  the anchor is a code reference that no longer resolves
#   n/a      the anchor is a non-code reference (URL / ticket) — out of scope in
#            v0.1, so neither present nor missing.
#
# Anchor types (v0.1 = file paths / commands / symbols). An optional `type:`
# prefix disambiguates; otherwise the type is inferred:
#   file:PATH     present if PATH exists under the working tree.
#   cmd:CMDLINE   present if the first word of CMDLINE is on PATH.
#   symbol:NAME   present if NAME occurs (whole word) anywhere in the tree.
#   url:… / ticket:…  always n/a (non-code, out of scope).
# Bare anchors are inferred: a `://` makes it a URL (n/a); an ABC-123 shape a
# ticket (n/a); an existing path or a path-shaped token a file; whitespace makes
# it a command; anything else a symbol. Use an explicit prefix when the
# inference would guess wrong (e.g. a single-word command -> `cmd:make`).
#
# Exit status:
#   0  every code anchor resolved (no missing). n/a anchors never fail.
#   1  --strict given and at least one anchor is missing.
#   2  usage / environment error (no MEMORY_INDEX.md to check).
#
# Usage:
#   check_anchors.sh                 Check the current project (git root, else CWD).
#   check_anchors.sh --dir DIR       Check the memory directory DIR (index inside it).
#   check_anchors.sh --index FILE    Check a specific MEMORY_INDEX.md file.
#   check_anchors.sh --root DIR      Working tree root for resolution (default: git root/CWD).
#   check_anchors.sh --json          Emit machine-readable JSON instead of a table.
#   check_anchors.sh --strict        Exit 1 if any anchor is missing.
#   check_anchors.sh --quiet         Show only entries that have a missing anchor.
#   check_anchors.sh -h | --help     Show this help.
#
# MEMORY_INDEX.md format is documented in the plugin README ("MEMORY_INDEX.md
# format"). Pure stdlib bash + Python 3. No third-party dependencies.
set -euo pipefail

BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
    sed -n '2,38p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

MEMORY_DIR=""
INDEX_PATH=""
ROOT_DIR=""
JSON=0
STRICT=0
QUIET=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dir)     MEMORY_DIR="${2:?--dir needs a directory}"; shift 2 ;;
        --index)   INDEX_PATH="${2:?--index needs a file}"; shift 2 ;;
        --root)    ROOT_DIR="${2:?--root needs a directory}"; shift 2 ;;
        --json)    JSON=1; shift ;;
        --strict)  STRICT=1; shift ;;
        --quiet)   QUIET=1; shift ;;
        -h|--help) usage; exit 0 ;;
        *) echo "check_anchors.sh: unknown argument '$1'" >&2; usage >&2; exit 2 ;;
    esac
done

# Resolve the working-tree root (where anchors are looked up).
if [[ -z "$ROOT_DIR" ]]; then
    ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
fi

# Resolve the index file: explicit --index wins; else MEMORY_INDEX.md inside the
# memory directory (explicit --dir, else the conventional .workspace/memory/).
if [[ -z "$INDEX_PATH" ]]; then
    if [[ -z "$MEMORY_DIR" ]]; then
        MEMORY_DIR="$ROOT_DIR/.workspace/memory"
    fi
    INDEX_PATH="$MEMORY_DIR/MEMORY_INDEX.md"
fi

if [[ ! -f "$INDEX_PATH" ]]; then
    echo "check_anchors.sh: no MEMORY_INDEX.md to check: $INDEX_PATH" >&2
    exit 2
fi

PYTHONPATH="$BIN_DIR${PYTHONPATH:+:$PYTHONPATH}" python3 - "$INDEX_PATH" "$ROOT_DIR" "$JSON" "$STRICT" "$QUIET" <<'PY'
import json
import os
import re
import shutil
import subprocess
import sys

INDEX_PATH = os.path.abspath(sys.argv[1])
ROOT_DIR = os.path.abspath(sys.argv[2])
# The memory directory holds the index, which names the anchors verbatim; a
# symbol search must skip it so an anchor token isn't "found" in its own index.
MEMORY_DIR = os.path.dirname(INDEX_PATH)
JSON = sys.argv[3] == "1"
STRICT = sys.argv[4] == "1"
QUIET = sys.argv[5] == "1"

# Anchors that explicitly declare "no anchors".
EMPTY_TOKENS = {"", "none", "n/a", "na", "-", "—"}

# Recognized explicit type prefixes -> canonical type.
TYPE_PREFIXES = {
    "file": "file", "path": "file",
    "cmd": "cmd", "command": "cmd",
    "symbol": "symbol", "sym": "symbol",
    "url": "url",
    "ticket": "ticket",
}

# File extensions that mark a bare token as a path even when it does not exist
# (so a deleted-file anchor still classifies as `file` -> `missing`).
CODE_EXTS = {
    "py", "pyi", "js", "jsx", "ts", "tsx", "sh", "bash", "zsh", "md", "rst",
    "txt", "json", "yaml", "yml", "toml", "ini", "cfg", "conf", "go", "rs",
    "c", "h", "cc", "cpp", "hpp", "java", "kt", "rb", "php", "cs", "swift",
    "sql", "html", "css", "scss", "lua", "pl", "r", "scala", "clj", "ex",
    "exs", "env", "lock", "mk", "make", "dockerfile", "gradle", "xml",
}

# Directories never worth descending into when searching for a symbol.
PRUNE_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__", ".mypy_cache",
    ".pytest_cache", ".tox", "dist", "build", ".next", ".cache", ".idea",
}

TICKET_RE = re.compile(r"^[A-Z][A-Z0-9]+-\d+$")
# Bare token shaped like name.ext (single extension, no path separator).
EXT_RE = re.compile(r"\.([A-Za-z0-9]+)$")


def parse_index(path):
    """MEMORY_INDEX.md -> list of (filename, [anchor strings]) in file order.

    Mirrors verify_index.sh's parser: optional YAML frontmatter, then one
    `## <file>` heading per entry with `- key: value` fields. The `anchors`
    value is the comma-separated inline list (the documented form); an empty
    inline value followed by indented `- item` bullets is also collected, for
    forward compatibility.
    """
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            lines = fh.read().splitlines()
    except (OSError, IOError):
        return []

    i = 0
    if lines and lines[0].strip() == "---":  # skip frontmatter
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            i += 1
        i += 1

    entries = []
    current = None          # (name, [anchors])
    in_anchors = False      # are we collecting anchor sub-bullets?
    for line in lines[i:]:
        head = re.match(r"^##\s+(.+?)\s*$", line)
        if head:
            name = head.group(1).strip().strip("`").strip('"').strip("'").strip()
            current = (os.path.normpath(name), [])
            entries.append(current)
            in_anchors = False
            continue
        if current is None:
            continue
        # Top-level field line: "- key: value" or "key: value" (no indent).
        m = re.match(r"^(?:- )?([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m and line[:1] not in (" ", "\t"):
            key = m.group(1).strip().lower()
            if key == "anchors":
                in_anchors = True
                current[1].extend(_split_anchors(m.group(2)))
            else:
                in_anchors = False
            continue
        # Indented sub-bullet under `anchors:`.
        sub = re.match(r"^\s+[-*]\s+(.+?)\s*$", line)
        if sub and in_anchors:
            current[1].extend(_split_anchors(sub.group(1)))
    return entries


def _split_anchors(value):
    """Split a comma-separated anchors value into cleaned tokens."""
    out = []
    for raw in value.split(","):
        tok = raw.strip().strip("`").strip()
        if tok and tok.lower() not in EMPTY_TOKENS:
            out.append(tok)
    return out


def classify(anchor):
    """Return (type, value): type in file|cmd|symbol|url|ticket; value resolved."""
    # Explicit prefix wins, but only for recognized keywords (so `https://x`
    # and `Foo::bar` fall through to inference rather than splitting wrong).
    if ":" in anchor:
        prefix, rest = anchor.split(":", 1)
        key = prefix.strip().lower()
        if key in TYPE_PREFIXES:
            return TYPE_PREFIXES[key], rest.strip()
    # Inference for bare anchors.
    if "://" in anchor:
        return "url", anchor
    if TICKET_RE.match(anchor):
        return "ticket", anchor
    if os.path.exists(os.path.join(ROOT_DIR, anchor)):
        return "file", anchor
    if any(c.isspace() for c in anchor):
        return "cmd", anchor
    if "/" in anchor:
        return "file", anchor
    ext = EXT_RE.search(anchor)
    if ext and ext.group(1).lower() in CODE_EXTS:
        return "file", anchor
    return "symbol", anchor


def resolve(atype, value):
    """Return present|missing|n/a for a classified anchor."""
    if atype in ("url", "ticket"):
        return "n/a"
    if atype == "file":
        return "present" if os.path.exists(os.path.join(ROOT_DIR, value)) else "missing"
    if atype == "cmd":
        exe = value.split()[0] if value.split() else value
        return "present" if shutil.which(exe) else "missing"
    if atype == "symbol":
        return "present" if symbol_found(value) else "missing"
    return "n/a"


_GIT_OK = None


def _git_available():
    global _GIT_OK
    if _GIT_OK is None:
        _GIT_OK = (
            shutil.which("git") is not None
            and subprocess.call(
                ["git", "-C", ROOT_DIR, "rev-parse", "--is-inside-work-tree"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            ) == 0
        )
    return _GIT_OK


def symbol_found(name):
    """True if `name` occurs as a whole word anywhere in the working tree."""
    if _git_available():
        # Fixed-string, whole-word, binary-skipping, quiet — fast on big trees.
        # Exclude the memory dir so the index doesn't match its own anchors.
        cmd = ["git", "-C", ROOT_DIR, "grep", "-qIFw", "-e", name, "--", "."]
        rel = os.path.relpath(MEMORY_DIR, ROOT_DIR)
        if not rel.startswith(".."):
            cmd.append(":(exclude)%s" % rel)
        rc = subprocess.call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if rc in (0, 1):
            return rc == 0
        # rc > 1: git grep errored (e.g. detached state) — fall back to a walk.
    pat = re.compile(r"(?<!\w)" + re.escape(name) + r"(?!\w)")
    for dirpath, dirnames, filenames in os.walk(ROOT_DIR):
        dirnames[:] = [d for d in dirnames if d not in PRUNE_DIRS]
        if os.path.abspath(dirpath) == MEMORY_DIR:
            continue
        for fn in filenames:
            fp = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(fp) > 2_000_000:  # skip very large files
                    continue
                with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                    if pat.search(fh.read()):
                        return True
            except (OSError, IOError):
                continue
    return False


def main():
    entries = parse_index(INDEX_PATH)
    results = []  # [{file, anchors:[{anchor,type,result}]}]
    n_present = n_missing = n_na = 0
    for name, anchors in entries:
        checked = []
        for a in anchors:
            atype, value = classify(a)
            result = resolve(atype, value)
            if result == "present":
                n_present += 1
            elif result == "missing":
                n_missing += 1
            else:
                n_na += 1
            checked.append({"anchor": a, "type": atype, "result": result})
        results.append({"file": name, "anchors": checked})

    if JSON:
        print(json.dumps({
            "index": INDEX_PATH,
            "root": ROOT_DIR,
            "entries": results,
            "summary": {
                "present": n_present, "missing": n_missing, "n/a": n_na,
                "entries": len(results),
            },
        }, indent=2))
    else:
        print("Index: %s" % INDEX_PATH)
        print("Working tree: %s" % ROOT_DIR)
        shown = 0
        for entry in results:
            has_missing = any(a["result"] == "missing" for a in entry["anchors"])
            if QUIET and not has_missing:
                continue
            shown += 1
            print("\n%s" % entry["file"])
            if not entry["anchors"]:
                print("  (no anchors)")
                continue
            for a in entry["anchors"]:
                print("  %-7s  %-6s  %s" % (a["result"], a["type"], a["anchor"]))
        if QUIET and shown == 0:
            print("\n(no entries with missing anchors)")
        print("\nSummary: %d present, %d missing, %d n/a (across %d entr%s)"
              % (n_present, n_missing, n_na, len(results),
                 "y" if len(results) == 1 else "ies"))

    if STRICT and n_missing:
        return 1
    return 0


sys.exit(main())
PY
