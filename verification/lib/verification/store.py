"""The private store: where it is, how it is read, and the integrity check."""

import json
import os

from . import formats, pointers

DEFAULT_STORE = "~/agents/verification-store"
INDEX_FILE = "index.tsv"
INDEX_TOKEN_CAP = 4000
CHARS_PER_TOKEN = 4  # same estimate as memory/bin/token_count.py


def count_tokens(text):
    return (len(text) + CHARS_PER_TOKEN - 1) // CHARS_PER_TOKEN


def location():
    """The store directory, or None when no store is present."""
    path = os.path.expanduser(os.environ.get("VERIFICATION_STORE") or DEFAULT_STORE)
    return path if os.path.isdir(path) else None


def read_rows(store, name):
    """Yield (line_number, row_or_None, raw_line) for each non-blank line."""
    path = os.path.join(store, name)
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                yield n, json.loads(line), line.rstrip("\n")
            except json.JSONDecodeError as exc:
                yield n, None, f"invalid JSON: {exc.msg}"


def render_index(store):
    """One tab-separated line per entry: the text that sessions load."""
    lines = ["id\tshape\tcontext\tviolation\tenforcement"]
    for _, row, _ in read_rows(store, "entries.jsonl"):
        if not isinstance(row, dict):
            continue
        lines.append(
            "\t".join(
                [
                    row.get("id", ""),
                    ",".join(row.get("shape") or []),
                    ",".join(row.get("context") or []),
                    row.get("violation", ""),
                    (row.get("enforcement") or {}).get("level", ""),
                ]
            )
        )
    return "\n".join(lines) + "\n"


def check(store):
    """Return a list of problems, each naming file:line. Empty means the store is sound."""
    problems = []
    for name, fmt in formats.FORMATS.items():
        key = "run_id" if name == "replays.jsonl" else "id"
        seen = {}
        for n, row, raw in read_rows(store, name):
            where = f"{name}:{n}"
            if row is None:
                problems.append(f"{where}: {raw}")
                continue
            for reason in formats.validate_row(name, row):
                problems.append(f"{where}: {reason}")
            if name != "replays.jsonl":
                ident = row.get(key)
                if ident in seen:
                    problems.append(
                        f"{where}: duplicate {key} {ident!r} (first at line {seen[ident]})"
                    )
                seen.setdefault(ident, n)
            limit = fmt.get("token_limit")
            if limit:
                compact = json.dumps(row, separators=(",", ":"), ensure_ascii=False)
                tokens = count_tokens(compact)
                if tokens > limit:
                    problems.append(f"{where}: {tokens} tokens, limit {limit}")
            for field, value in formats.pointer_values(name, row):
                reason = pointers.resolve(value)
                if reason:
                    problems.append(f"{where}: {field} does not resolve: {reason}")
    index = render_index(store)
    tokens = count_tokens(index)
    if tokens > INDEX_TOKEN_CAP:
        problems.append(f"{INDEX_FILE}: {tokens} tokens, cap {INDEX_TOKEN_CAP}")
    on_disk = os.path.join(store, INDEX_FILE)
    if os.path.exists(on_disk):
        with open(on_disk, encoding="utf-8") as fh:
            if fh.read() != index:
                problems.append(f"{INDEX_FILE}: stale; run `verification store index`")
    return problems
