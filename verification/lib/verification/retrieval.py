"""Retrieve store entries for a unit of work by shape and context, and track their disposition.

`<unit>/retrieval.jsonl` holds one row per retrieved entry:
    {"entry": "<id>", "disposition": "applies"|"does-not-apply"|null, "reason": "..."}
and one row per item derived beyond the retrieved set:
    {"item": "<premise, claim or failure-case id>", "origin": "new"}
"""

import json
import os

from . import store

FILE = "retrieval.jsonl"
DISPOSITIONS = ("applies", "does-not-apply")


def entries(path):
    return [r for _, r, _ in store.read_rows(path, "entries.jsonl") if isinstance(r, dict)]


def query(path, shapes, contexts, moved_from=None):
    """Entries matching any shape or context. For a move from one context to another, also the
    entries tied to exactly one of the two contexts: what holds in one may not hold in the other."""
    shapes, contexts = set(shapes), set(contexts)
    out = []
    for e in entries(path or ""):
        es, ec = set(e.get("shape") or []), set(e.get("context") or [])
        hit = bool(es & shapes) or bool(ec & contexts)
        if moved_from:
            pair = {moved_from} | contexts
            hit = hit or len(ec & pair) == 1
        if hit:
            out.append(e)
    return out


def read(unit):
    file = os.path.join(unit, FILE)
    if not os.path.exists(file):
        return []
    with open(file, encoding="utf-8") as fh:
        return [json.loads(x) for x in fh if x.strip()]


def write(unit, rows):
    with open(os.path.join(unit, FILE), "w", encoding="utf-8") as fh:
        fh.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))


def record(unit, retrieved):
    """Add newly retrieved entries undisposed; keep every disposition already made."""
    rows = read(unit)
    have = {r.get("entry") for r in rows}
    rows += [
        {"entry": e["id"], "disposition": None, "reason": ""}
        for e in retrieved
        if e["id"] not in have
    ]
    write(unit, rows)
    return rows


def report(unit):
    rows = read(unit)
    retrieved = [r for r in rows if "entry" in r]
    problems = []
    for r in retrieved:
        if r.get("disposition") not in DISPOSITIONS:
            problems.append(f"{r['entry']}: not disposed (applies or does-not-apply)")
        elif not (r.get("reason") or "").strip():
            problems.append(f"{r['entry']}: {r['disposition']} with no reason")
    counts = {
        "retrieved": len(retrieved),
        "applied": sum(r.get("disposition") == "applies" for r in retrieved),
        "dismissed": sum(r.get("disposition") == "does-not-apply" for r in retrieved),
        "new": sum(r.get("origin") == "new" for r in rows),
    }
    return counts, problems
