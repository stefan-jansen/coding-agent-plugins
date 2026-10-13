"""`verification review-table`: one table per issue for the author, built from the plan, the
term table and the coverage verdicts, with no test code in it."""

import json
import os
import re
import sys

from test_coverage import PLAN, cli, evidence, passing, write_evidence

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from verification import pointers  # noqa: E402

SPEC = """# Spec: labels

## Terms

Context: crypto

| Term | Readings | Status | Basis |
|---|---|---|---|
| 2-hour label | (a) 2 rows (b) 2 clock hours | resolved-by-author | (b) |
"""


def table(unit):
    (unit / "spec.md").write_text(SPEC)
    passing(unit)
    cli("coverage", unit / "plan.md", "--issue", "1")
    r = cli("review-table", unit / "plan.md", "--issue", "1")
    path = unit / "review" / "issue-1.md"
    return r, path


def test_the_table_has_a_row_per_item_and_the_term_reading(unit):
    r, path = table(unit)
    assert r.returncode == 0, r.stderr
    text = path.read_text()
    assert "| 2-hour label | (b) | resolved-by-author |" in text
    for item in ("horizon", "vendor-terms", "full-panel", "gap-label", "hand-built"):
        assert f"| {item} |" in text
    assert "the exit is counted in rows across a gap" in text
    assert "filed at ml4t/research-to-production-dev#302 (the unit's author, 2026-10-13)" in text


def test_every_row_points_to_a_test_and_a_verdict_that_resolve(unit):
    _, path = table(unit)
    text = path.read_text()
    found = re.findall(r"`([^`]+)`", text.split("| Item |", 1)[1])
    assert "repo/test_pipeline.py::test_labels_span_the_horizon" in found
    assert "results/horizon.json" in found
    # Prevents: a committed table whose pointers name one machine's absolute paths.
    assert str(unit) not in text
    for p in found:
        assert pointers.resolve(f"{unit}:{p}") is None, p


def test_the_table_carries_no_test_code(unit):
    # Prevents: handing the author the tests instead of what they check (criterion 11).
    _, path = table(unit)
    text = path.read_text()
    for marker in ("def test_", "assert ", "import "):
        assert marker not in text
    for decl in unit.glob("*.json"):
        mutation = json.loads(decl.read_text())["variant"]["mutation"]
        for line in (mutation["old"] + mutation["new"]).splitlines():
            assert line.strip() not in text, line


def test_an_issue_without_coverage_verdicts_is_refused(unit):
    r = cli("review-table", unit / "plan.md", "--issue", "1")
    assert r.returncode == 1
    assert "horizon: no verdict; run verification coverage first" in r.stderr
    assert not (unit / "review" / "issue-1.md").exists()


PREMISE_PLAN = PLAN.replace(
    "Premises: none - the claims below carry the issue",
    """### Premises

Input: hourly bars

| Question | Answer | Kind |
|---|---|---|
| ordering-spacing | consecutive rows may be hours apart | empirical |""",
).replace("Closes: horizon,", "Closes: hourly-bars.ordering-spacing, horizon,")


def test_a_tested_premise_must_say_what_error_its_test_targets(unit):
    (unit / "plan.md").write_text(PREMISE_PLAN)
    passing(unit)
    rows = evidence(unit)
    rows.append({**rows[0], "item": "hourly-bars.ordering-spacing"})
    write_evidence(unit, rows)
    cli("coverage", unit / "plan.md", "--issue", "1")
    r = cli("review-table", unit / "plan.md", "--issue", "1")
    assert r.returncode == 1
    assert "hourly-bars.ordering-spacing: say what error its test targets" in r.stderr
    rows[-1]["targets"] = "a label counted in rows reaches across a missing hour"
    write_evidence(unit, rows)
    cli("coverage", unit / "plan.md", "--issue", "1")
    r = cli("review-table", unit / "plan.md", "--issue", "1")
    assert r.returncode == 0, r.stderr
    text = (unit / "review" / "issue-1.md").read_text()
    assert "a label counted in rows reaches across a missing hour" in text
    assert "consecutive rows may be hours apart" in text
    json.loads((unit / "results" / "hourly-bars.ordering-spacing.json").read_text())
