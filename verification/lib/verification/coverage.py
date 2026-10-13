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
is uncovered.

A `deferred` row names the later plan issue that will verify the item (`to_issue`) and the
prerequisite missing now. It does not block the issue that closes the item; the named issue's
gate then requires it like one of its own items, and `verification milestone-check` refuses
while any row is still deferred.

When every item is covered, each verdict is written to
`<unit>/results/<item>.json` for the review table; a refusal writes nothing.
"""

import datetime
import json
import os
import re

from . import pointers, units, violate

EVIDENCE = "evidence.jsonl"
RESULTS = "results"
STATUSES = ("test", "waived", "test-unreachable", "finding", "deferred")
LEVELS = ("asserted", "pointed", "argued-unreachable", "test", "full-data")
STATES = ("covered", "waived", "test-unreachable", "finding", "uncovered", "deferred")
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
    if status == "deferred" and not isinstance(row.get("to_issue"), int):
        problems.append("to_issue: the plan number of the issue that will verify it")
    if status == "deferred" and row.get("declaration"):
        if not os.path.isfile(os.path.join(unit, row["declaration"])):
            problems.append(f"declaration: {row['declaration']} not found in the unit")
    if status in ("test", "finding"):
        decl = row.get("declaration") or ""
        if not decl or not os.path.isfile(os.path.join(unit, decl)):
            problems.append(f"declaration: {decl or '(missing)'} not found in the unit")
    if status == "waived":
        if not (row.get("reason") or "").strip():
            problems.append("reason: a waiver needs one")
        if not _date(row.get("date")):
            problems.append("date: must be an ISO date")
    if status in ("test-unreachable", "deferred") and not (row.get("prerequisite") or "").strip():
        problems.append("prerequisite: name what is missing")
    if status == "finding" and not (row.get("filed") or "").strip():
        problems.append("filed: name where the finding was filed")
    return problems


def assess(unit, item, row, number=None, later=(), own=True):
    """(state, problems, report) for one item, assessed at plan issue `number`; `later` holds the
    plan's issue numbers after it, and `own` says the issue closes the item itself rather than
    receiving it as a deferral."""
    if row is None:
        return "uncovered", ["no evidence row"], []
    problems = row_problems(unit, row)
    if problems:
        return "uncovered", problems, []
    status = row["status"]
    if status == "deferred":
        if not own:
            return "uncovered", ["deferred to this issue; verify it now"], []
        if row["to_issue"] not in later:
            return "uncovered", ["a deferral names a later issue in the plan"], []
        return "deferred", [], []
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


def result_name(item):
    return re.sub(r"[^A-Za-z0-9._-]", "_", item) + ".json"


def record(unit, verdicts):
    for item, state, problems, report in verdicts:
        _record(unit, item, state, problems, report)


def _record(unit, item, state, problems, report):
    os.makedirs(os.path.join(unit, RESULTS), exist_ok=True)
    with open(os.path.join(unit, RESULTS, result_name(item)), "w", encoding="utf-8") as fh:
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


def coverage(unit, body, number=None, plan_numbers=()):
    """({state: count}, [(item, state, problems, row, report)], refusal). Refusal is a reason the
    issue cannot be assessed at all, such as no `Closes:` line. Nothing is written here.

    The items are those the issue closes plus those deferred to it from earlier issues."""
    closes = units.declared(body, "Closes")
    if closes is None:
        return None, [], f"issue {number} has no `Closes:` line"
    rows, problems = read_evidence(unit)
    if problems:
        return None, [], "; ".join(problems)
    counts = dict.fromkeys(STATES, 0)
    out = []
    deferred_here = [
        i
        for i, r in rows.items()
        if r.get("status") == "deferred" and r.get("to_issue") == number and i not in closes
    ]
    later = {n for n in plan_numbers if number is not None and n > number}
    for item in closes + deferred_here:
        row = rows.get(item)
        state, problems, report = assess(unit, item, row, number, later, item in closes)
        counts[state] += 1
        out.append((item, state, problems, row, report))
    return counts, out, None


def closer(plan_text, item):
    for n, _, body in units.issues(plan_text):
        if item in (units.declared(body, "Closes") or []):
            return n
    return None


def deferrals(unit, plan_text, closed=()):
    """(lines, problems): every deferred item, and each one that should not stay deferred: its
    named issue has closed, or its prepared test already satisfies violate on this branch."""
    rows, problems = read_evidence(unit)
    lines = []
    for item, row in rows.items():
        if row.get("status") != "deferred":
            continue
        target = row.get("to_issue")
        lines.append(
            f"{item}\tissue {closer(plan_text, item)} -> issue {target}\t{row.get('prerequisite')}"
        )
        if target in closed:
            problems.append(f"{item}: issue {target} closed without verifying it")
        if row.get("declaration"):
            decl = violate.load(os.path.join(unit, row["declaration"]))
            if not violate.violate(decl)[1]:
                problems.append(f"{item}: its test already runs on this branch; verify it now")
    return lines, problems


def milestone_check(unit, closed=()):
    """Problems that stop the milestone closing: any item still deferred."""
    rows, problems = read_evidence(unit)
    for item, row in rows.items():
        if row.get("status") == "deferred":
            target = row.get("to_issue")
            why = " (closed without verifying it)" if target in closed else ""
            problems.append(f"{item}: still deferred to issue {target}{why}")
    return problems


def levels(unit):
    rows, problems = read_evidence(unit)
    counts = dict.fromkeys(LEVELS, 0)
    for row in rows.values():
        if row.get("level") in counts:
            counts[row["level"]] += 1
        else:
            problems.append(f"{row['item']}: level {row.get('level')!r} is not one of the five")
    return counts, problems
