"""Premise statements, claims and closure in a plan, using the crypto gap case as the fixture."""
import os
import subprocess
import sys

BIN = os.path.join(os.path.dirname(__file__), "..", "bin", "verification")

PREMISES = """### Premises

Input: hourly bars

| Question | Answer | Kind |
|---|---|---|
| record | one exchange-hour of trades for one perpetual | definitional |
| absent-record | no trades in that hour, including multi-day exchange outages | empirical |
| ordering-spacing | sorted by open time; consecutive rows may be up to 73 hours apart | empirical |
| entity-identity | exchange symbol; never reused | empirical |
| known-at | at bar close, one hour after open | definitional |
| institution | the exchange's published trading status | definitional |
"""

PLAN = f"""# Plan: crypto features

### Milestone: `v1 - crypto`

**Issue 1 - Hourly returns and 7-day volatility**

{PREMISES}
### Claims

| Id | Claim | How it could be false |
|---|---|---|
| vol-7d | price_vol_7d is the volatility of the last 168 hours | the window counts rows across a gap |

Closes: hourly-bars.ordering-spacing, hourly-bars.absent-record, vol-7d
Advances: none

**Issue 2 - Notebook text**

Premises: none - writes prose from issue 1's outputs only

Closes: hourly-bars.record, hourly-bars.entity-identity, hourly-bars.known-at, hourly-bars.institution
"""


def run(args, tmp_path, text):
    f = tmp_path / "plan.md"
    f.write_text(text)
    env = {k: v for k, v in os.environ.items() if k != "VERIFICATION_STORE"}
    env["HOME"] = str(tmp_path)
    return subprocess.run([sys.executable, BIN, *args, str(f)], capture_output=True, text=True, env=env)


def test_complete_plan_passes(tmp_path):
    for cmd in (["premises", "check"], ["claims", "list"], ["closure", "check"]):
        r = run(cmd, tmp_path, PLAN)
        assert r.returncode == 0, (cmd, r.stderr)


def test_spacing_left_unstated_fails(tmp_path):
    # Prevents: the crypto defect itself - rows counted as hours because spacing was never stated.
    text = PLAN.replace(
        "| ordering-spacing | sorted by open time; consecutive rows may be up to 73 hours apart "
        "| empirical |\n",
        "",
    )
    r = run(["premises", "check"], tmp_path, text)
    assert r.returncode == 1
    assert "'hourly bars' does not answer ordering-spacing" in r.stderr


def test_answer_without_kind_fails(tmp_path):
    text = PLAN.replace("never reused | empirical |", "never reused | |")
    r = run(["premises", "check"], tmp_path, text)
    assert r.returncode == 1 and "entity-identity is not marked" in r.stderr


def test_not_applicable_without_reason_fails(tmp_path):
    text = PLAN.replace(
        "| institution | the exchange's published trading status | definitional |",
        "| institution | not-applicable: | |",
    )
    r = run(["premises", "check"], tmp_path, text)
    assert r.returncode == 1 and "not-applicable without reason" in r.stderr


def test_simulation_must_state_achievable_price(tmp_path):
    # Prevents: a backtest filling at the decision bar's close because nobody said what was achievable.
    text = PLAN.replace("{PREMISES}", "").replace(
        "**Issue 1 - Hourly returns and 7-day volatility**\n",
        "**Issue 1 - Hourly returns and 7-day volatility**\n\nSimulates trading: yes\n",
    )
    r = run(["premises", "check"], tmp_path, text)
    assert r.returncode == 1
    assert "does not answer achievable-price" in r.stderr


def test_issue_without_premises_or_reason_fails(tmp_path):
    text = PLAN.replace("Premises: none - writes prose from issue 1's outputs only\n", "")
    r = run(["premises", "check"], tmp_path, text)
    assert r.returncode == 1 and "issue 2" in r.stderr


def test_claim_without_way_of_being_false_fails(tmp_path):
    text = PLAN.replace("| the window counts rows across a gap |", "| - |")
    r = run(["claims", "list"], tmp_path, text)
    assert r.returncode == 1 and "'vol-7d' has no way of being false" in r.stderr


def test_item_closed_by_no_issue_fails(tmp_path):
    # Prevents: a premise stated in planning that no issue ever verifies.
    text = PLAN.replace(", hourly-bars.institution", "")
    r = run(["closure", "check"], tmp_path, text)
    assert r.returncode == 1 and "hourly-bars.institution: defined but closed by no issue" in r.stderr


def test_item_closed_twice_or_undefined_fails(tmp_path):
    text = PLAN.replace("Closes: hourly-bars.record,", "Closes: vol-7d, holdout.exit, hourly-bars.record,")
    r = run(["closure", "check"], tmp_path, text)
    assert r.returncode == 1
    assert "vol-7d: closed by more than one issue" in r.stderr
    assert "holdout.exit: closed by issue 2 but defined nowhere" in r.stderr


def test_missing_closes_line_fails(tmp_path):
    text = PLAN.replace("Closes: hourly-bars.record, hourly-bars.entity-identity, "
                        "hourly-bars.known-at, hourly-bars.institution\n", "")
    r = run(["closure", "check"], tmp_path, text)
    assert r.returncode == 1 and "no `Closes:` line" in r.stderr
