"""`verification coverage`: is every item an issue closes covered?

Evidence for a unit's items lives beside its plan, in `<unit>/evidence.jsonl`, one row per item:

    {"item": "vol-7d", "status": "test", "level": "test", "declaration": "vol-7d.json"}
    {"item": "terms", "status": "waived", "level": "asserted", "reason": "...", "date": "..."}
    {"item": "panel", "status": "test-unreachable", "level": "pointed", "prerequisite": "..."}
    {"item": "gap", "status": "finding", "level": "asserted", "filed": "<repo>#<n>",
     "declaration": "gap.json"}

An item is covered when its test satisfies `verification violate`, which coverage runs rather
than trusting a recorded verdict. A waiver needs a reason and a date; `test-unreachable` names
the missing prerequisite. A `finding` is a test that fails on the current code: the code lacks
what the item asks for, so there is no correct version for violate to pass. Coverage confirms
the test fails there, counts the finding and does not block on it. A finding whose test passes
is uncovered. Each verdict is written to `<unit>/results/<item>.json` for the review table.
"""

import datetime
import json
import os
import re

from . import pointers, units, violate

EVIDENCE = "evidence.jsonl"
RESULTS = "results"
STATUSES = ("test", "waived", "test-unreachable", "finding")
LEVELS = ("asserted", "pointed", "argued-unreachable", "test", "full-data")
STATES = ("covered", "waived", "test-unreachable", "finding", "uncovered")
TEST_LEVELS = ("test", "full-data")


def read_evidence(unit):
    """({item: row}, problems). A duplicate or malformed row is a problem, not a silent pick."""
    rows, problems = {}, []
    path = os.path.join(unit, EVIDENCE)
    if not os.path.exists(path):
        return rows, problems
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                problems.append(f"{EVIDENCE}:{n}: invalid JSON: {exc.msg}")
                continue
            item = row.get("item") if isinstance(row, dict) else None
            if not item:
                problems.append(f"{EVIDENCE}:{n}: no item")
            elif item in rows:
                problems.append(f"{EVIDENCE}:{n}: second row for {item}")
            else:
                rows[item] = row
    return rows, problems


def _date(value):
    try:
        datetime.date.fromisoformat(value)
        return True
    except (TypeError, ValueError):
        return False


def row_problems(unit, row):
    """What is wrong with the row itself, before anything runs."""
    status, level = row.get("status"), row.get("level")
    if status not in STATUSES:
        return [f"status: must be one of {', '.join(STATUSES)}"]
    if level not in LEVELS:
        return [f"level: must be one of {', '.join(LEVELS)}"]
    problems = []
    if (status == "test") != (level in TEST_LEVELS):
        problems.append(f"level {level} does not match status {status}")
    if level == "full-data":
        reason = pointers.resolve(row.get("full_data") or "")
        if reason:
            problems.append(f"full_data: {reason}")
    if status in ("test", "finding"):
        decl = row.get("declaration") or ""
        if not decl or not os.path.isfile(os.path.join(unit, decl)):
            problems.append(f"declaration: {decl or '(missing)'} not found in the unit")
    if status == "waived":
        if not (row.get("reason") or "").strip():
            problems.append("reason: a waiver needs one")
        if not _date(row.get("date")):
            problems.append("date: must be an ISO date")
    if status == "test-unreachable" and not (row.get("prerequisite") or "").strip():
        problems.append("prerequisite: name what is missing")
    if status == "finding" and not (row.get("filed") or "").strip():
        problems.append("filed: name where the finding was filed")
    return problems


def assess(unit, item, row):
    """(state, problems, report) for one item."""
    if row is None:
        return "uncovered", ["no evidence row"], []
    problems = row_problems(unit, row)
    if problems:
        return "uncovered", problems, []
    status = row["status"]
    if status in ("waived", "test-unreachable"):
        return status, [], []
    decl = violate.load(os.path.join(unit, row["declaration"]))
    if status == "test":
        report, problems = violate.violate(decl)
        return ("uncovered" if problems else "covered"), problems, report
    problems = violate.validate(decl)
    if problems:
        return "uncovered", problems, []
    proc = violate.run_once(decl, "correct")
    report = [f"test: {decl['test']}", f"current code: exit {proc.returncode}"]
    if proc.returncode == 0:
        return "uncovered", ["the finding's test passes on the current code: it is a test"], report
    if proc.returncode != violate.TEST_FAILED:
        return "uncovered", [f"the finding's test crashed (exit {proc.returncode})"], report
    return "finding", [], report


def _record(unit, item, state, problems, report):
    os.makedirs(os.path.join(unit, RESULTS), exist_ok=True)
    name = re.sub(r"[^A-Za-z0-9._-]", "_", item) + ".json"
    with open(os.path.join(unit, RESULTS, name), "w", encoding="utf-8") as fh:
        json.dump(
            {
                "item": item,
                "state": state,
                "problems": problems,
                "report": report,
                "date": datetime.date.today().isoformat(),
            },
            fh,
            indent=1,
        )


def issue_body(text, number):
    """The body of issue `number` in a plan, or the whole text when it holds one issue."""
    for n, _, body in units.issues(text):
        if number is None or n == number:
            return body
    raise ValueError(f"issue {number} not found")


def coverage(unit, body, number=None):
    """({state: count}, [(item, state, problems, row)], refusal). Refusal is a reason the issue
    cannot be assessed at all, such as no `Closes:` line."""
    closes = units.declared(body, "Closes")
    if closes is None:
        return None, [], f"issue {number} has no `Closes:` line"
    rows, problems = read_evidence(unit)
    if problems:
        return None, [], "; ".join(problems)
    counts = dict.fromkeys(STATES, 0)
    out = []
    for item in closes:
        row = rows.get(item)
        state, problems, report = assess(unit, item, row)
        _record(unit, item, state, problems, report)
        counts[state] += 1
        out.append((item, state, problems, row))
    return counts, out, None


def levels(unit):
    rows, problems = read_evidence(unit)
    counts = dict.fromkeys(LEVELS, 0)
    for row in rows.values():
        if row.get("level") in counts:
            counts[row["level"]] += 1
        else:
            problems.append(f"{row['item']}: level {row.get('level')!r} is not one of the five")
    return counts, problems
