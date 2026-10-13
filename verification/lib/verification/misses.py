"""Misses: defects the author or a reader named that the process did not surface (criterion 22).

Each is recorded against the one component that should have surfaced it, so that the counts
per component say which one to change next.
"""

import datetime
import json
import os

from . import formats, store

FILE = "misses.jsonl"


def record(path, ident, defect, classifications, reported_by, pointer=None, today=None):
    """Problems; none means the row was appended."""
    if len(classifications) != 1:
        given = ", ".join(classifications) or "none"
        return [
            f"exactly one classification is required (given: {given}); choose the component "
            f"that should have surfaced it: {', '.join(formats.CATEGORIES)}"
        ]
    row = {
        "id": ident,
        "date": (today or datetime.date.today()).isoformat(),
        "reported_by": reported_by,
        "defect": defect,
        "classification": classifications[0],
    }
    if pointer:
        row["pointer"] = pointer
    problems = store.row_problems(FILE, row)
    if any(r.get("id") == ident for _, r, _ in store.read_rows(path, FILE) if r):
        problems.append(f"{ident} already recorded")
    if problems:
        return problems
    with open(os.path.join(path, FILE), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    return []


def report(path):
    counts = dict.fromkeys(formats.CATEGORIES, 0)
    for _, row, _ in store.read_rows(path, FILE):
        if isinstance(row, dict) and row.get("classification") in counts:
            counts[row["classification"]] += 1
    return counts
