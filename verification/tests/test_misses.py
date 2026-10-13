"""`verification miss record` and `miss report` (criterion 22).

A miss is a defect the author or a reader named that the process did not surface. It is
recorded against the one component that should have surfaced it, so the counts say which
component to change next.
"""

import json
import os

import pytest
from test_store_check import run


@pytest.fixture
def store(tmp_path):
    path = tmp_path / "store"
    path.mkdir()
    env = {**os.environ, "VERIFICATION_STORE": str(path), "HOME": str(tmp_path)}
    return path, env


def record(env, *extra, ident="weekend-gap"):
    args = ["miss", "record", ident, "--reported-by", "Stefan"]
    args += ["--defect", "vol_21d spans the weekend gap as one session", *extra]
    return run(args, env)


def misses(path):
    f = path / "misses.jsonl"
    return [json.loads(x) for x in f.read_text().splitlines()] if f.exists() else []


def test_a_miss_is_recorded_with_its_one_component(store):
    path, env = store
    r = record(env, "--classification", "premise")
    assert r.returncode == 0, r.stderr
    (row,) = misses(path)
    assert row["classification"] == "premise" and row["reported_by"] == "Stefan"
    assert run(["store", "check"], env).returncode == 0


@pytest.mark.parametrize("given", [[], ["--classification", "premise", "--classification", "term"]])
def test_a_miss_without_exactly_one_classification_is_refused(store, given):
    # Prevents: a miss counted against no component, or against two, so no count says
    # which component to change.
    path, env = store
    r = record(env, *given)
    assert r.returncode == 1
    assert "exactly one classification" in r.stderr
    assert misses(path) == []


def test_an_unknown_component_is_refused(store):
    path, env = store
    r = record(env, "--classification", "review")
    assert r.returncode == 1
    assert misses(path) == []


def test_a_second_miss_with_the_same_id_is_refused(store):
    path, env = store
    assert record(env, "--classification", "test").returncode == 0
    r = record(env, "--classification", "term")
    assert r.returncode == 1
    assert "weekend-gap already recorded" in r.stderr
    assert len(misses(path)) == 1


def test_report_counts_match_the_recorded_misses(store):
    path, env = store
    for ident, cls in (("a", "term"), ("b", "term"), ("c", "test"), ("d", "retrieval")):
        assert record(env, "--classification", cls, ident=ident).returncode == 0
    r = run(["miss", "report"], env)
    assert r.returncode == 0, r.stderr
    lines = dict(line.split("\t") for line in r.stdout.splitlines())
    assert lines == {"term": "2", "premise": "0", "claim": "0", "retrieval": "1", "test": "1"}
