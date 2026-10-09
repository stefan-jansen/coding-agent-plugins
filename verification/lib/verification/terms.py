"""The term table in a spec, and house definitions that resolve terms across repositories.

A spec carries a `## Terms` section:

    Context: xnys, us-equities

    | Term | Readings | Status | Basis |
    |---|---|---|---|
    | 20-day momentum | (a) 20 rows (b) 20 XNYS sessions | resolved-by-author | (b) |

Status is one of:
  house-definition    Basis names the store definition id that resolves it.
  readings-agree      Basis names the data the readings were computed on, and the result.
  resolved-by-author  Basis states the chosen reading.
"""

import datetime
import json
import os
import re

from . import store

STATUSES = ("house-definition", "readings-agree", "resolved-by-author")
NONE_LINE = "No term admits readings that would produce different code."


def _norm(term):
    return re.sub(r"\s+", " ", term.strip().lower())


def _slug(term):
    return re.sub(r"[^a-z0-9]+", "-", _norm(term)).strip("-")


def section(text):
    """The body of the `## Terms` section, or None."""
    m = re.search(r"^## Terms\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def context(body):
    m = re.search(r"^Context:\s*(.+)$", body, re.M)
    return [c.strip().lower() for c in m.group(1).split(",") if c.strip()] if m else []


def rows(body):
    """(line_index, {term, readings, status, basis}) for each table row."""
    out = []
    lines = body.splitlines()
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not line.strip().startswith("|") or len(cells) != 4:
            continue
        if cells[0].lower() == "term" or set(cells[0]) <= set("-: "):
            continue
        out.append((i, dict(zip(("term", "readings", "status", "basis"), cells))))
    return out


def definitions(path):
    if path is None:
        return []
    return [r for _, r, _ in store.read_rows(path, "definitions.jsonl") if isinstance(r, dict)]


def lookup(path, term, ctx):
    """The house definition for a term whose context overlaps the spec's, or None."""
    for d in definitions(path):
        if _norm(d["term"]) == _norm(term) and set(d["context"]) & set(ctx):
            return d
    return None


def _origin_is(d, spec_path):
    m = re.match(r"^([^:@]+):(.+)$", d.get("origin", ""))
    if not m or spec_path is None:
        return False
    origin = os.path.join(os.path.expanduser(m.group(1)), m.group(2))
    return os.path.realpath(origin) == os.path.realpath(spec_path)


def check(text, path, spec_path=None):
    """Problems with a spec's term table; empty means every term is resolved."""
    body = section(text)
    if body is None:
        return ["spec has no `## Terms` section"]
    found = rows(body)
    if not found:
        return (
            [] if NONE_LINE in body else [f"Terms table is empty; list terms or state: {NONE_LINE}"]
        )
    ctx = context(body)
    known = {d["id"] for d in definitions(path)}
    problems = []
    for _, r in found:
        name = r["term"]
        if r["status"] not in STATUSES:
            problems.append(f"{name}: unresolved (status {r['status']!r})")
            continue
        if not r["basis"] or r["basis"] in ("-", "?"):
            problems.append(f"{name}: {r['status']} with no basis")
        elif r["status"] == "house-definition" and r["basis"] not in known:
            problems.append(f"{name}: house definition {r['basis']!r} not in the store")
        d = lookup(path, name, ctx) if r["status"] == "resolved-by-author" else None
        if d and not _origin_is(d, spec_path):
            problems.append(
                f"{name}: a house definition ({d['id']}) exists; use it, not a question"
            )
    return problems


def apply(text, path):
    """Mark every row that a house definition covers. Returns (new_text, applied_terms)."""
    body = section(text)
    if body is None:
        return text, []
    ctx = context(body)
    lines = body.splitlines()
    applied = []
    for i, r in rows(body):
        if r["status"] == "house-definition":
            continue
        d = lookup(path, r["term"], ctx)
        if d:
            cells = [r["term"], r["readings"], "house-definition", d["id"]]
            lines[i] = "| " + " | ".join(cells) + " |"
            applied.append(r["term"])
    new_body = "\n".join(lines) + ("\n" if body.endswith("\n") else "")
    return text.replace(body, new_body, 1), applied


def define(path, term, ctx, definition, decided_by, origin, today=None):
    """Record an author's resolution as a house definition. Returns the new row."""
    if lookup(path, term, ctx):
        raise ValueError(f"{term!r} already has a house definition in context {ctx}")
    row = {
        "id": f"{_slug(term)}--{_slug('-'.join(ctx))}",
        "term": term,
        "context": [c.lower() for c in ctx],
        "definition": definition,
        "decided_by": decided_by,
        "decided_on": (today or datetime.date.today()).isoformat(),
        "origin": origin,
    }
    with open(os.path.join(path, "definitions.jsonl"), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row
