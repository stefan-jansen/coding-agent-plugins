"""`verification coverage` and the applied-entry half of `closure check`, on a unit whose items
are backed by real `violate` runs against the small pipeline from test_violate.py."""

import json
import os
import shutil
import subprocess
import sys

import pytest
from test_violate import LABELS, ROW_LABEL

BIN = os.path.join(os.path.dirname(__file__), "..", "bin", "verification")

# Asks for behaviour the labels do not have: a label whose exit falls in the gap is dropped.
FINDING_TEST = """\
import observations
from labels import label
from test_pipeline import RAW


def test_a_label_into_the_gap_is_kept():
    labels = label(observations.build(RAW), 2)
    assert any(x["t"] == 19 for x in labels)
"""

PLAN = """# Plan: labels

### Milestone: `v1 - labels`

**Issue 1 - Labels over gapped bars**

Premises: none - the claims below carry the issue

### Claims

| Id | Claim | How it could be false |
|---|---|---|
| horizon | every label exits two hours after entry | the exit is counted in rows across a gap |
| vendor-terms | contract terms match the vendor's | the vendor revises a multiplier |
| full-panel | no label crosses a gap on the full panel | a gap occurs only outside the fixture |
| gap-label | a label whose exit falls in a gap is kept | the label is dropped |
| hand-built | the gap check rejects a gapped frame | it is shown only on a hand-built frame |

Closes: horizon, vendor-terms, full-panel, gap-label, hand-built
Advances: none

**Issue 2 - Notebook text**

Closes: none
"""

TODAY = "2026-10-13"


def decl(unit, name, test, variant=None, producer="observations.py"):
    path = unit / f"{name}.json"
    path.write_text(
        json.dumps(
            {
                "test": test,
                "root": str(unit / "repo"),
                "command": [sys.executable, "-m", "pytest", "-q"],
                "producer": producer,
                "variant": variant or {"mutation": ROW_LABEL},
                "fixture": "RAW in test_pipeline.py",
            }
        )
    )
    return path.name


@pytest.fixture
def unit(tmp_path_factory, repo):
    u = tmp_path_factory.mktemp("unit")
    shutil.copytree(repo, u / "repo")
    (u / "repo" / "test_finding.py").write_text(FINDING_TEST)
    (u / "plan.md").write_text(PLAN)
    rows = [
        {
            "item": "horizon",
            "status": "test",
            "level": "test",
            "declaration": decl(u, "horizon", "test_pipeline.py::test_labels_span_the_horizon"),
        },
        {
            "item": "vendor-terms",
            "status": "waived",
            "level": "asserted",
            "reason": "the vendor publishes no contract terms; Stefan accepted the risk",
            "date": TODAY,
        },
        {
            "item": "full-panel",
            "status": "test-unreachable",
            "level": "pointed",
            "prerequisite": "the full 2015-2024 panel is not on this machine",
        },
        {
            "item": "gap-label",
            "status": "finding",
            "level": "asserted",
            "filed": "ml4t/research-to-production-dev#302",
            "declaration": decl(
                u, "gap-label", "test_finding.py::test_a_label_into_the_gap_is_kept"
            ),
        },
        {
            "item": "hand-built",
            "status": "test",
            "level": "test",
            "declaration": decl(
                u, "hand-built", "test_pipeline.py::test_check_on_a_hand_built_frame"
            ),
        },
    ]
    write_evidence(u, rows)
    return u


def write_evidence(u, rows):
    (u / "evidence.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))


def evidence(u):
    return [json.loads(x) for x in (u / "evidence.jsonl").read_text().splitlines()]


def cli(*args, cwd=None):
    env = {k: v for k, v in os.environ.items() if k != "VERIFICATION_STORE"}
    env["HOME"] = str(cwd or os.getcwd())
    return subprocess.run(
        [sys.executable, BIN, *map(str, args)], capture_output=True, text=True, env=env, cwd=cwd
    )


def test_one_item_at_each_status_is_counted(unit):
    r = cli("coverage", unit / "plan.md", "--issue", "1")
    assert r.returncode == 1, r.stdout + r.stderr
    assert "covered=1 waived=1 test-unreachable=1 finding=1 uncovered=1" in r.stdout
    assert "hand-built: correct run: producer observations.py never executed" in r.stderr
    assert "gap-label: filed at ml4t/research-to-production-dev#302" in r.stdout
    assert (unit / "repo" / "labels.py").read_text() == LABELS


def passing(unit):
    """Resolve the one uncovered item the way the author would: a waiver."""
    rows = [r for r in evidence(unit) if r["item"] != "hand-built"]
    rows += [
        {
            "item": "hand-built",
            "status": "waived",
            "level": "asserted",
            "reason": "superseded by horizon",
            "date": TODAY,
        }
    ]
    write_evidence(unit, rows)


def test_the_gate_opens_once_the_uncovered_item_is_resolved(unit):
    passing(unit)
    r = cli("coverage", unit / "plan.md", "--issue", "1")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "covered=1 waived=2 test-unreachable=1 finding=1 uncovered=0" in r.stdout


def test_an_item_with_no_evidence_is_uncovered(unit):
    write_evidence(unit, [r for r in evidence(unit) if r["item"] != "full-panel"])
    r = cli("coverage", unit / "plan.md", "--issue", "1")
    assert r.returncode == 1
    assert "full-panel: no evidence row" in r.stderr


def test_a_verdict_is_recorded_for_the_review_table(unit):
    passing(unit)
    cli("coverage", unit / "plan.md", "--issue", "1")
    verdict = json.loads((unit / "results" / "horizon.json").read_text())
    assert verdict["state"] == "covered"
    assert "violated run: exit 1" in verdict["report"]


def test_a_finding_whose_test_passes_is_uncovered(unit):
    # Prevents: parking a passing (or never-run) test as a finding to get it out of the gate.
    rows = evidence(unit)
    rows[0] = {**rows[0], "status": "finding", "level": "asserted", "filed": "x/y#1"}
    write_evidence(unit, rows)
    r = cli("coverage", unit / "plan.md", "--issue", "1")
    assert r.returncode == 1
    assert "horizon: the finding's test passes on the current code" in r.stderr


def test_a_waiver_without_a_date_is_uncovered(unit):
    rows = evidence(unit)
    del rows[1]["date"]
    write_evidence(unit, rows)
    r = cli("coverage", unit / "plan.md", "--issue", "1")
    assert r.returncode == 1
    assert "vendor-terms: date: must be an ISO date" in r.stderr


def test_a_test_item_must_carry_a_test_level(unit):
    rows = evidence(unit)
    rows[0]["level"] = "asserted"
    write_evidence(unit, rows)
    r = cli("coverage", unit / "plan.md", "--issue", "1")
    assert r.returncode == 1
    assert "horizon: level asserted does not match status test" in r.stderr


def test_levels_prints_the_distribution(unit):
    r = cli("coverage", unit / "plan.md", "--levels")
    assert r.returncode == 0, r.stderr
    assert "asserted=2 pointed=1 argued-unreachable=0 test=2 full-data=0" in r.stdout


def applied(unit, entry="check-can-fail"):
    row = {"entry": entry, "disposition": "applies", "reason": "issue 1 adds a label check"}
    (unit / "retrieval.jsonl").write_text(json.dumps(row) + "\n")


def test_an_applied_entry_no_issue_closes_fails_closure(unit):
    # Prevents: a retrieved lesson marked as applying and then never verified by any issue.
    applied(unit)
    r = cli("closure", "check", unit / "plan.md")
    assert r.returncode == 1
    assert "entry:check-can-fail: defined but closed by no issue" in r.stderr


def test_an_applied_entry_closed_without_a_test_is_uncovered(unit):
    applied(unit)
    (unit / "plan.md").write_text(
        PLAN.replace("hand-built\n", "hand-built, entry:check-can-fail\n")
    )
    assert cli("closure", "check", unit / "plan.md").returncode == 0
    r = cli("coverage", unit / "plan.md", "--issue", "1")
    assert r.returncode == 1
    assert "entry:check-can-fail: no evidence row" in r.stderr


def test_an_issue_without_a_closes_line_is_refused(unit):
    (unit / "plan.md").write_text(PLAN.replace("Closes: none\n", ""))
    r = cli("coverage", unit / "plan.md", "--issue", "2")
    assert r.returncode == 1
    assert "issue 2 has no `Closes:` line" in r.stderr


def snapshot(directory):
    return {
        str(p.relative_to(directory)): p.read_bytes()
        for p in sorted(directory.rglob("*"))
        if p.is_file() and "__pycache__" not in p.parts and ".pytest_cache" not in p.parts
    }


def test_a_refusal_writes_nothing(unit):
    # Prevents: a refused gate leaving files behind, so git status differs after the refusal
    # (criterion 16).
    before = snapshot(unit)
    r = cli("coverage", unit / "plan.md", "--issue", "1")
    assert r.returncode == 1
    assert snapshot(unit) == before
