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


def vocabulary(store):
    """{kind: set of keys} from keys.jsonl, the only shapes and contexts entries may use."""
    vocab = {kind: set() for kind in formats.KEY_KINDS}
    for _, row, _ in read_rows(store, "keys.jsonl"):
        if isinstance(row, dict) and row.get("kind") in vocab:
            vocab[row["kind"]].add(row.get("id"))
    return vocab


def unknown_keys(vocab, shapes, contexts):
    """Reasons for every shape or context outside the vocabulary."""
    return [
        f"{kind} {key!r} is not in keys.jsonl"
        for kind, keys in (("shape", shapes), ("context", contexts))
        for key in keys
        if key not in vocab[kind]
    ]


def check_keys(store):
    """Entries use only vocabulary keys, and every key cites causes the corpus holds.

    A synonym ("rolling-window" for "trailing-window") makes an entry unreachable by any
    retrieval that uses the vocabulary, so it is refused here rather than missed later.
    """
    vocab = vocabulary(store)
    causes = {r.get("id") for _, r, _ in read_rows(store, "causes.jsonl") if isinstance(r, dict)}
    problems = []
    for n, row, _ in read_rows(store, "keys.jsonl"):
        for cause in (row or {}).get("derived_from") or []:
            if cause not in causes:
                problems.append(f"keys.jsonl:{n}: derived_from {cause!r} is not in causes.jsonl")
    for n, row, _ in read_rows(store, "entries.jsonl"):
        if isinstance(row, dict):
            for reason in unknown_keys(vocab, row.get("shape") or [], row.get("context") or []):
                problems.append(f"entries.jsonl:{n}: {reason}")
    return problems


def row_problems(name, row):
    """Format, size and pointer problems of one row, without its line number."""
    problems = list(formats.validate_row(name, row))
    limit = formats.FORMATS[name].get("token_limit")
    if limit:
        tokens = count_tokens(json.dumps(row, separators=(",", ":"), ensure_ascii=False))
        if tokens > limit:
            problems.append(f"{tokens} tokens, limit {limit}")
    for field, value in formats.pointer_values(name, row):
        reason = pointers.resolve(value)
        if reason:
            problems.append(f"{field} does not resolve: {reason}")
    return problems


def write_rows(store, name, rows):
    with open(os.path.join(store, name), "w", encoding="utf-8") as fh:
        fh.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)


def write_index(store):
    with open(os.path.join(store, INDEX_FILE), "w", encoding="utf-8") as fh:
        fh.write(render_index(store))


def check_admitted(store):
    """Every entry has an admission row: knowledge enters only through the acceptance tests.

    The tests an entry passed, and their reasons, are on that row in admissions.jsonl rather
    than on the entry, which is loaded into sessions and held to 120 tokens."""
    admitted = {
        r.get("entry")
        for _, r, _ in read_rows(store, "admissions.jsonl")
        if isinstance(r, dict) and r.get("decision") in ("admitted", "revised")
    }
    return [
        f"entries.jsonl:{n}: {row.get('id')} has no admission row; enter it with "
        "`verification store admit`"
        for n, row, _ in read_rows(store, "entries.jsonl")
        if isinstance(row, dict) and row.get("id") not in admitted
    ]


def check(store):
    """Return a list of problems, each naming file:line. Empty means the store is sound."""
    problems = []
    for name, fmt in formats.FORMATS.items():
        key = fmt.get("key", "id")
        seen = {}
        for n, row, raw in read_rows(store, name):
            where = f"{name}:{n}"
            if row is None:
                problems.append(f"{where}: {raw}")
                continue
            problems += [f"{where}: {reason}" for reason in row_problems(name, row)]
            if key:
                ident = row.get(key)
                if ident in seen:
                    problems.append(
                        f"{where}: duplicate {key} {ident!r} (first at line {seen[ident]})"
                    )
                seen.setdefault(ident, n)
    problems += check_keys(store)
    problems += check_admitted(store)
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
