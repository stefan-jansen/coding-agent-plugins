"""Derive premises, claims and failure cases for a unit on each model family, then mark the
items both families raised independently as convergent.

Each family sees the same inputs and never the other's list. A matching pass, run after both
lists exist, pairs items that state the same thing.
"""

import json
import os

from . import families

KINDS = ("premise", "claim", "failure-case")
MERGED = "derivation.jsonl"

PROMPT = """Below is the specification for a piece of quantitative work{extra}.

List what the work silently relies on and what it asserts, as three kinds of item:
- premise: something the code relies on about the data or the world: what a record or an
  absent record means, ordering and spacing, entity identity, when a value was known,
  an institution's rules.
- claim: a number, comparison or property the output asserts to a reader.
- failure-case: a specific way the work could be wrong that a test should catch, produced the
  way it would actually arise (a code defect, or input the real pipeline could emit).

Reply with only a JSON object: {{"items": [{{"id": "<short-slug>", "kind": "premise|claim|failure-case",
"text": "<one line>"}}]}}

--- specification ---
{spec}
"""

MATCH = """Two independent reviewers listed items for the same work. Pair the items that state the
same thing (same premise, same claim, or same failure), even if worded differently. Leave an item
unpaired when no item on the other list states it.

List A:
{a}

List B:
{b}

Reply with only a JSON object: {{"pairs": [["<id from A>", "<id from B>"], ...]}}"""


def _lines(items):
    return "\n".join(f"- {i['id']} ({i['kind']}): {i['text']}" for i in items)


def raise_items(family, spec_text, extra="", ask=families.ask):
    reply = families.parse_json_object(ask(family, PROMPT.format(spec=spec_text, extra=extra)))
    items = []
    for i in reply.get("items", []):
        if i.get("kind") in KINDS and i.get("id") and i.get("text"):
            items.append({"id": i["id"], "kind": i["kind"], "text": i["text"]})
    if not items:
        raise ValueError(f"{family} raised no valid items")
    return items


def merge(a_items, b_items, pairs, a="claude", b="gpt"):
    """One row per distinct item, carrying every family that raised it."""
    a_by, b_by = {i["id"]: i for i in a_items}, {i["id"]: i for i in b_items}
    rows, paired_b = [], set()
    paired = {x: y for x, y in pairs if x in a_by and y in b_by}
    for i in a_items:
        row = {**i, "families": [a]}
        if i["id"] in paired:
            row["families"].append(b)
            row["also"] = paired[i["id"]]
            paired_b.add(paired[i["id"]])
        rows.append(row)
    for i in b_items:
        if i["id"] not in paired_b:
            rows.append(
                {**i, "id": i["id"] if i["id"] not in a_by else f"{i['id']}-{b}", "families": [b]}
            )
    return rows


def derive(unit, spec_path, ask=families.ask):
    with open(spec_path, encoding="utf-8") as fh:
        spec_text = fh.read()
    a = raise_items("claude", spec_text, ask=ask)
    b = raise_items("gpt", spec_text, ask=ask)
    reply = families.parse_json_object(ask("claude", MATCH.format(a=_lines(a), b=_lines(b))))
    rows = merge(a, b, reply.get("pairs", []))
    with open(os.path.join(unit, MERGED), "w", encoding="utf-8") as fh:
        fh.write("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    return rows


def report(unit):
    file = os.path.join(unit, MERGED)
    with open(file, encoding="utf-8") as fh:
        rows = [json.loads(x) for x in fh if x.strip()]
    problems = [f"{r.get('id')}: no family marker" for r in rows if not r.get("families")]
    counts = {
        "items": len(rows),
        "claude": sum("claude" in r.get("families", []) for r in rows),
        "gpt": sum("gpt" in r.get("families", []) for r in rows),
        "convergent": sum(len(set(r.get("families", []))) > 1 for r in rows),
    }
    return counts, problems
