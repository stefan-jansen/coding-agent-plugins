"""`verification violate` against a small repository with a producing module and its tests.

Each rejected case is a test as it is actually written: a check handed a frame built by hand,
a check that repeats the producer's own assignment, a mutation that never runs, a perturbation
the test never applies, and a mutation that breaks the import instead of reaching the test.
"""
import json
import os
import subprocess
import sys

import pytest

BIN = os.path.join(os.path.dirname(__file__), "..", "bin", "verification")

OBSERVATIONS = '''\
BAR = 1


def build(raw):
    """Hourly bars, one per input hour, stamped at the open."""
    return [{"t": t, "close_t": t + BAR, "price": p} for t, p in sorted(raw)]


def unused():
    return 0
'''

LABELS = '''\
def label(obs, horizon):
    """Exit the bar exactly `horizon` hours later; no exit across a gap."""
    by_time = {o["t"]: o for o in obs}
    out = []
    for o in obs:
        exit_bar = by_time.get(o["t"] + horizon)
        if exit_bar is not None:
            out.append({"t": o["t"], "exit_t": exit_bar["t"]})
    return out
'''

PERTURB = '''\
def drop_window(obs, start, end):
    kept = [o for o in obs if not start <= o["t"] < end]
    if len(kept) == len(obs):
        raise ValueError("nothing to remove")
    return kept
'''

TESTS = '''\
import os

import observations
from labels import label
from ml4t.diagnostic.evaluation.violations import drop_window

RAW = [(t, 100.0 + t) for t in range(48) if not 20 <= t < 23]


def test_labels_span_the_horizon():
    labels = label(observations.build(RAW), 2)
    assert labels and all(x["exit_t"] - x["t"] == 2 for x in labels)


def test_check_on_a_hand_built_frame():
    labels = label([{"t": 0, "price": 1.0}, {"t": 3, "price": 1.0}], 3)
    assert all(x["exit_t"] - x["t"] == 3 for x in labels)


def test_bar_closes_one_bar_after_it_opens():
    obs = observations.build(RAW)
    assert all(o["close_t"] == o["t"] + observations.BAR for o in obs)


def no_gaps(obs):
    assert all(b["t"] - a["t"] == 1 for a, b in zip(obs, obs[1:]))


def test_gap_check_on_perturbed_bars():
    obs = observations.build([(t, 1.0) for t in range(48)])
    if os.environ.get("VERIFICATION_VARIANT") == "violated":
        obs = drop_window(obs, 10, 13)
    no_gaps(obs)


def test_gap_check_swapping_in_a_built_frame():
    if os.environ.get("VERIFICATION_VARIANT") == "violated":
        obs = drop_window([{"t": 0}, {"t": 2}, {"t": 3}], 1, 3)
    else:
        obs = observations.build([(t, 1.0) for t in range(48)])
    no_gaps(obs)


def test_gap_check_that_never_perturbs():
    no_gaps(observations.build([(t, 1.0) for t in range(48)]))
'''

ROW_LABEL = {
    "file": "labels.py",
    "old": '        exit_bar = by_time.get(o["t"] + horizon)\n',
    "new": '        i = obs.index(o)\n'
           '        exit_bar = obs[i + horizon] if i + horizon < len(obs) else None\n',
}


@pytest.fixture
def repo(tmp_path):
    files = {
        "observations.py": OBSERVATIONS,
        "labels.py": LABELS,
        "test_pipeline.py": TESTS,
        "ml4t/__init__.py": "",
        "ml4t/diagnostic/__init__.py": "",
        "ml4t/diagnostic/evaluation/__init__.py": "",
        "ml4t/diagnostic/evaluation/violations.py": PERTURB,
    }
    for name, text in files.items():
        (tmp_path / name).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / name).write_text(text)
    return tmp_path


def violate(repo, test, variant, producer="observations.py"):
    decl = {
        "test": f"test_pipeline.py::{test}",
        "root": str(repo),
        "command": [sys.executable, "-m", "pytest", "-q"],
        "producer": producer,
        "variant": variant,
        "fixture": "RAW in test_pipeline.py",
    }
    path = repo / "violation.json"
    path.write_text(json.dumps(decl))
    env = {**os.environ, "PYTHONPATH": str(repo)}
    return subprocess.run(
        [sys.executable, BIN, "violate", str(path)], capture_output=True, text=True, env=env
    )


def test_row_counted_horizon_on_gapped_bars_is_accepted(repo):
    r = violate(repo, "test_labels_span_the_horizon", {"mutation": ROW_LABEL})
    assert r.returncode == 0, r.stdout + r.stderr
    assert "fixture (both runs): RAW in test_pipeline.py" in r.stdout
    assert "violated run: exit 1" in r.stdout
    assert (repo / "labels.py").read_text() == LABELS


def test_check_on_a_hand_built_frame_is_rejected(repo):
    # Prevents: a check proven only on a frame the producer cannot emit.
    r = violate(repo, "test_check_on_a_hand_built_frame", {"mutation": ROW_LABEL})
    assert r.returncode == 1
    assert "producer observations.py never executed" in r.stderr


def test_check_repeating_the_producers_assignment_is_rejected(repo):
    # Prevents: a check that compares a value with one derived from the same source.
    bar = {"mutation": {"file": "observations.py", "old": "BAR = 1\n", "new": "BAR = 2\n"}}
    r = violate(repo, "test_bar_closes_one_bar_after_it_opens", bar)
    assert r.returncode == 1
    assert "passes on the violated variant" in r.stderr


def test_mutation_in_code_the_test_never_runs_is_rejected(repo):
    dead = {"mutation": {"file": "observations.py", "old": "    return 0\n", "new": "    return 1\n"}}
    r = violate(repo, "test_labels_span_the_horizon", dead)
    assert r.returncode == 1
    assert "mutated lines of observations.py never executed" in r.stderr


def test_mutation_that_breaks_the_import_is_rejected(repo):
    broken = {"mutation": {"file": "observations.py", "old": "BAR = 1\n", "new": "BAR = = 1\n"}}
    r = violate(repo, "test_labels_span_the_horizon", broken)
    assert r.returncode == 1
    assert "not a test failure" in r.stderr


def test_perturbed_producer_output_is_accepted(repo):
    r = violate(repo, "test_gap_check_on_perturbed_bars", {"perturbation": "drop_window"})
    assert r.returncode == 0, r.stdout + r.stderr


def test_perturbation_the_test_never_applies_is_rejected(repo):
    r = violate(repo, "test_gap_check_that_never_perturbs", {"perturbation": "drop_window"})
    assert r.returncode == 1
    assert "perturbation drop_window was never called" in r.stderr
    assert "passes on the violated variant" in r.stderr


def test_ambiguous_mutation_is_refused_before_anything_runs(repo):
    # Atomicity: an invalid declaration edits no file and runs no test.
    twice = {"mutation": {"file": "observations.py", "old": "t", "new": "u"}}
    before = (repo / "observations.py").stat().st_mtime_ns
    r = violate(repo, "test_labels_span_the_horizon", twice)
    assert r.returncode == 1
    assert "need exactly 1" in r.stderr
    assert "correct run" not in r.stdout
    assert (repo / "observations.py").stat().st_mtime_ns == before


def test_violated_input_built_by_hand_is_rejected(repo):
    # Prevents: a test that runs the producer for its passing half and hands the check a built
    # frame for its failing half.
    r = violate(repo, "test_gap_check_swapping_in_a_built_frame", {"perturbation": "drop_window"})
    assert r.returncode == 1
    assert "violated run: producer observations.py never executed" in r.stderr
