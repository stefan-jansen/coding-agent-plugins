"""`verification review-table`: the one table per issue the author reviews instead of the tests.

Written to `<unit>/review/issue-<n>.md`, in the domain's language: the requirement, the term
readings the spec settled, then one row per item the issue closes, with what must hold, the
error it guards against, its evidence, and pointers to the test and to the verdict
`verification coverage` recorded. Mutations, assertions and other test code stay out; the
pointers lead there for whoever wants them.

A tested premise has no stated way of being false in the plan, so its evidence row carries
`targets`, one line naming the error its test exists to catch.
"""

import os
import re

from . import coverage, retrieval, store, terms, units


def _cell(text):
    return " ".join(str(text or "-").split()).replace("|", "/")


def requirement(body):
    """The issue's opening paragraph, before its sections and declarations."""
    lines = []
    for line in body.strip().splitlines():
        if line.startswith(("###", "Closes:", "Advances:", "Premises:", "Simulates")):
            break
        if not line.strip() and lines:
            break
        if line.strip():
            lines.append(line.strip())
    return " ".join(lines)


def _statements(unit, body):
    """{item: (kind, what must hold, error it guards against or None)}."""
    out = {}
    for slug, (name, answers) in (units.premises(body) or {}).items():
        for q, (answer, _) in answers.items():
            out[f"{slug}.{q}"] = ("premise", f"{name}, {q}: {answer}", None)
    for cid, claim, how in units.claims(body):
        out[cid] = ("claim", claim, how)
    path = store.location()
    entries = {e["id"]: e for e in retrieval.entries(path)} if path else {}
    for item in units.applied_entries(unit):
        e = entries.get(item.split(":", 1)[1], {})
        out[item] = ("lesson", e.get("violation", "store entry"), e.get("violation"))
    return out


def _test_pointer(unit, row):
    decl = coverage.violate.load(os.path.join(unit, row["declaration"]))
    path, _, name = decl["test"].partition("::")
    name = re.sub(r"\[.*\]$", "", name)
    return f"{decl['root']}:{path}" + (f"::{name}" if name else "")


def _evidence(row):
    status = row.get("status")
    by = f" ({row.get('decided_by')}, {row.get('date')})"
    if status == "waived":
        return f"waived: {row.get('reason')}{by}"
    if status == "test-unreachable":
        return f"not testable yet: {row.get('prerequisite')}{by}"
    if status == "finding":
        return f"finding, filed at {row.get('filed')}{by}"
    if status == "deferred":
        return f"deferred to issue {row.get('to_issue')}: {row.get('prerequisite')}"
    return f"test ({row.get('level')})"


def build(unit, plan_text, number, spec_text=None):
    """(markdown, problems). Nothing is written while there are problems."""
    title, body = next(
        ((t, b) for n, t, b in units.issues(plan_text) if number is None or n == number),
        (None, None),
    )
    if body is None:
        return None, [f"issue {number} not found"]
    closes = units.declared(body, "Closes") or []
    rows, problems = coverage.read_evidence(unit)
    statements = _statements(unit, body)
    lines = [
        f"# Issue {number}: {title}",
        "",
        f"Requirement: {_cell(requirement(body))}",
        "",
    ]
    term_rows = [r for _, r in terms.rows(terms.section(spec_text) or "")] if spec_text else []
    if term_rows:
        lines += ["| Term | Reading used | Settled by |", "|---|---|---|"]
        for t in term_rows:
            lines.append(f"| {_cell(t['term'])} | {_cell(t['basis'])} | {_cell(t['status'])} |")
        lines.append("")
    lines += [
        "| Item | Kind | What must hold | Error it guards against | Evidence | Test | Verdict |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in closes:
        kind, what, error = statements.get(item, ("item", "not stated in the plan", None))
        row = rows.get(item) or {}
        error = row.get("targets") or error
        if row.get("status") in ("test", "finding") and not error:
            problems.append(f"{item}: say what error its test targets (`targets` in evidence)")
        test = verdict = "-"
        if row.get("declaration"):
            test = f"`{_test_pointer(unit, row)}`"
        result = os.path.join(unit, coverage.RESULTS, coverage.result_name(item))
        if os.path.exists(result):
            verdict = f"`{os.path.abspath(unit)}:{coverage.RESULTS}/{coverage.result_name(item)}`"
        else:
            problems.append(f"{item}: no verdict; run verification coverage first")
        evidence = _evidence(row) if row else "none"
        lines.append(
            f"| {item} | {kind} | {_cell(what)} | {_cell(error)} | {_cell(evidence)} "
            f"| {test} | {verdict} |"
        )
    return "\n".join(lines) + "\n", problems


def write(unit, number, markdown):
    os.makedirs(os.path.join(unit, "review"), exist_ok=True)
    path = os.path.join(unit, "review", f"issue-{number}.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(markdown)
    return path
