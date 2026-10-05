"""Independent classification of corpus causes by each model family."""

import json
import os

from . import families, formats, store

PROMPT = """You are given defects that shipped in quantitative finance code or teaching material.
For each, decide which step of a development process should have prevented it. Exactly one of:

- term: a term in the specification or request admitted readings that produce different code or
  numbers, and the wrong reading was used (e.g. "outside the holdout" read on the decision date
  rather than the label's exit).
- premise: the code relied on an unstated assumption about the data or the world: what a record
  or an absent record means, ordering or spacing, what identifies an entity, when a value was
  known, or an institution's rules (e.g. a row offset taken as a fixed span of time).
- claim: a result was asserted to a reader (a number, a comparison, a property) with no stated way
  it could be false and no check that it holds.
- retrieval: the lesson was already known and recorded elsewhere, and was not applied.
- test: a test or check existed for the error but could not fail on it (compared a value with
  something derived from the same source, or ran only on inputs the code cannot produce).
- other: none of these; give a one-line description.

Defects:
{items}

Reply with only a JSON object mapping each id to {{"category": "<one of the six>",
"other_description": "<one line, only when category is other>"}}."""


def pending(path, family):
    rows = [(n, r) for n, r, _ in store.read_rows(path, "causes.jsonl") if isinstance(r, dict)]
    return [(n, r) for n, r in rows if family not in (r.get("classification") or {})]


def render(rows):
    items = []
    for _, r in rows:
        text = f"- id: {r['id']}\n  summary: {r['summary']}"
        if r.get("detail"):
            text += f"\n  detail: {r['detail']}"
        items.append(text)
    return PROMPT.format(items="\n".join(items))


def classify(path, family, batch=25, ask=families.ask):
    """Classify every cause this family has not classified. Rows are rewritten once, at the end."""
    todo = pending(path, family)
    answers = {}
    for i in range(0, len(todo), batch):
        chunk = todo[i : i + batch]
        reply = families.parse_json_object(ask(family, render(chunk)))
        for _, r in chunk:
            got = reply.get(r["id"])
            cat = got.get("category") if isinstance(got, dict) else None
            if cat not in formats.CATEGORIES + ("other",):
                raise ValueError(f"{family} gave no valid category for {r['id']}: {got!r}")
            answers[r["id"]] = got
    file = os.path.join(path, "causes.jsonl")
    with open(file, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    out = []
    for line in lines:
        if not line.strip():
            continue
        row = json.loads(line)
        got = answers.get(row["id"])
        if got:
            row.setdefault("classification", {})[family] = got["category"]
            if got["category"] == "other" and got.get("other_description"):
                desc = f"{family}: {got['other_description']}"
                row["other_description"] = "; ".join(
                    x for x in (row.get("other_description"), desc) if x
                )
        out.append(json.dumps(row, ensure_ascii=False))
    with open(file, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
    return len(answers)
