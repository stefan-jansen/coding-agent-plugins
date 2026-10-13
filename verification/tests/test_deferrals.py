"""Deferrals (criterion 13) and the milestone gate (criterion 15).

An item is deferred by naming the later issue that will verify it and the prerequisite missing
now. The issue gate lets a valid deferral through and holds the named issue to it; the
milestone gate refuses while any item is still deferred.
"""

from test_coverage import cli, evidence, passing, write_evidence

DEFERRED = {
    "item": "full-panel",
    "status": "deferred",
    "level": "pointed",
    "to_issue": 2,
    "prerequisite": "the full panel lands with issue 2's data load",
}


def defer(unit, **change):
    passing(unit)
    rows = [r for r in evidence(unit) if r["item"] != "full-panel"]
    write_evidence(unit, rows + [{**DEFERRED, **change}])


def test_a_deferral_to_a_later_issue_does_not_block_this_one(unit):
    defer(unit)
    r = cli("coverage", unit / "plan.md", "--issue", "1")
    assert r.returncode == 0, r.stderr
    assert "deferred=1" in r.stdout
    assert "full-panel: deferred to issue 2" in r.stdout


def test_a_deferral_must_name_a_later_issue_in_the_plan(unit):
    for target in (1, 7):
        defer(unit, to_issue=target)
        r = cli("coverage", unit / "plan.md", "--issue", "1")
        assert r.returncode == 1
        assert "full-panel: a deferral names a later issue in the plan" in r.stderr


def test_a_deferral_without_its_prerequisite_is_uncovered(unit):
    defer(unit, prerequisite="")
    r = cli("coverage", unit / "plan.md", "--issue", "1")
    assert r.returncode == 1
    assert "full-panel: prerequisite: name what is missing" in r.stderr


def test_the_named_issue_must_verify_what_was_deferred_to_it(unit):
    # Prevents: a deferral that moves an item to an issue whose gate never looks at it.
    defer(unit)
    r = cli("coverage", unit / "plan.md", "--issue", "2")
    assert r.returncode == 1
    assert "full-panel: deferred to this issue; verify it now" in r.stderr


def test_deferrals_reports_one_whose_test_already_runs(unit):
    defer(unit)
    r = cli("deferrals", unit / "plan.md")
    assert r.returncode == 0, r.stderr
    assert "full-panel\tissue 1 -> issue 2\tthe full panel lands with" in r.stdout
    defer(unit, declaration="horizon.json")
    r = cli("deferrals", unit / "plan.md")
    assert r.returncode == 1
    assert "full-panel: its test already runs on this branch; verify it now" in r.stderr


def test_deferrals_reports_one_naming_a_closed_issue(unit):
    defer(unit)
    r = cli("deferrals", unit / "plan.md", "--closed", "1 2")
    assert r.returncode == 1
    assert "full-panel: issue 2 closed without verifying it" in r.stderr


def test_the_milestone_cannot_close_with_an_open_deferral(unit):
    defer(unit)
    r = cli("milestone-check", unit / "plan.md")
    assert r.returncode == 1
    assert "full-panel: still deferred to issue 2" in r.stderr
    rows = [r for r in evidence(unit) if r["item"] != "full-panel"]
    verified = {
        "item": "full-panel",
        "status": "test-unreachable",
        "level": "pointed",
        "decided_by": "the unit's author",
        "date": "2026-10-13",
    }
    write_evidence(unit, rows + [{**verified, "prerequisite": "no full panel on this machine"}])
    assert cli("milestone-check", unit / "plan.md").returncode == 0
