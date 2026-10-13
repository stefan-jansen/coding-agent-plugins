"""Measured-number claims (criterion 4): a claim tagged `measured` answers the five checklist
questions, adapted from pstack's benchmark-checklist, or `claims list` fails."""

import pathlib
import subprocess
import sys

import pytest
from test_units import BIN, run

TEMPLATE = pathlib.Path(__file__).parent.parent / "templates" / "measured-number.md"

PLAN = """# Plan: export speed

### Milestone: `v1 - export`

**Issue 1 - Batch the parquet writer**

Premises: none - times a fixed fixture

### Claims

| Id | Claim | How it could be false | Kind |
|---|---|---|---|
| export-p50 | export is 30% faster at p50 on the 60k-row fixture | gap within run-to-run range | measured |
| same-rows | the batched writer writes the same rows | a batch boundary drops a row | |

### Measured: export-p50

| Question | Answer |
|---|---|
| limiter | JSON encoding on one core, py-spy on an unreported run |
| alternatives | page cache: both sides read the fixture warm after a discarded first run |
| work-happened | row count read back from the written file equals the fixture's |
| configured-alike | both sides at release settings, same pyarrow, compression and row group size |
| within-limits | the writer took 45% of the run, so at most an 82% speedup is possible |

Closes: export-p50, same-rows
"""

QUESTIONS = ("limiter", "alternatives", "work-happened", "configured-alike", "within-limits")


def test_a_measured_claim_answering_all_five_passes(tmp_path):
    r = run(["claims", "list"], tmp_path, PLAN)
    assert r.returncode == 0, r.stderr
    assert "export-p50" in r.stdout


@pytest.mark.parametrize("question", QUESTIONS)
def test_a_measured_claim_missing_an_answer_fails(tmp_path, question):
    # Prevents: a speedup reported without knowing what bounds it, what else it measured,
    # whether the work ran, whether both sides were alike, or whether it breaks arithmetic.
    lines = [x for x in PLAN.splitlines() if not x.startswith(f"| {question} |")]
    r = run(["claims", "list"], tmp_path, "\n".join(lines) + "\n")
    assert r.returncode == 1
    assert f"claim 'export-p50' is a measured number and does not answer {question}" in r.stderr


def test_a_blank_or_placeholder_answer_does_not_count(tmp_path):
    text = PLAN.replace(
        "| within-limits | the writer took 45% of the run, so at most an 82% speedup is possible |",
        "| within-limits | - |",
    )
    r = run(["claims", "list"], tmp_path, text)
    assert r.returncode == 1
    assert "does not answer within-limits" in r.stderr


def test_a_measured_claim_with_no_checklist_section_fails(tmp_path):
    text = PLAN.split("### Measured: export-p50")[0] + "Closes: export-p50, same-rows\n"
    r = run(["claims", "list"], tmp_path, text)
    assert r.returncode == 1
    assert "does not answer limiter" in r.stderr


def test_the_template_carries_the_questions_and_the_attribution():
    text = TEMPLATE.read_text()
    assert "Copyright (c) 2026 Lauren Tan" in text and "MIT" in text
    for q in QUESTIONS:
        assert f"| {q} |" in text


def test_claims_template_prints_the_section():
    r = subprocess.run([sys.executable, BIN, "claims", "template"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    assert "### Measured: <claim-id>" in r.stdout and "Lauren Tan" in r.stdout


def test_a_checklist_for_another_claim_does_not_answer_this_one(tmp_path):
    # Prevents: a checklist written for the p95 number taken as vetting the p50 claim.
    text = PLAN.replace("### Measured: export-p50", "### Measured: export-p95")
    r = run(["claims", "list"], tmp_path, text)
    assert r.returncode == 1
    assert "claim 'export-p50' is a measured number and does not answer limiter" in r.stderr
