"""Retrieval with dispositions, and two-family derivation with convergence."""
import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from verification import derive, retrieval  # noqa: E402

BIN = os.path.join(os.path.dirname(__file__), "..", "bin", "verification")


def run(args, env):
    return subprocess.run([sys.executable, BIN, *args], capture_output=True, text=True, env=env)


def entry(eid, shape, context):
    return {"id": eid, "shape": shape, "context": context, "violation": f"{eid} violation",
            "enforcement": {"level": "prose", "reason": "r"}, "institutional": False,
            "fired": [], "admission": []}


@pytest.fixture
def world(tmp_path):
    store = tmp_path / "store"
    store.mkdir()
    rows = [
        entry("row-offset-as-time", ["rolling-window"], ["crypto-perps"]),
        entry("xnys-half-days", ["session-calendar"], ["xnys"]),
        entry("cme-sunday-open", ["session-calendar"], ["cme"]),
        entry("ticker-reuse", ["entity-join"], ["us-equities"]),
    ]
    (store / "entries.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    keys = [("rolling-window", "shape"), ("session-calendar", "shape"), ("entity-join", "shape"),
            ("crypto-perps", "context"), ("xnys", "context"), ("cme", "context"),
            ("us-equities", "context")]
    (store / "keys.jsonl").write_text("".join(
        json.dumps({"id": k, "kind": kind, "meaning": k, "derived_from": ["c"]}) + "\n"
        for k, kind in keys))
    unit = tmp_path / "unit"
    unit.mkdir()
    env = {**os.environ, "VERIFICATION_STORE": str(store)}
    return unit, env


def test_undisposed_entry_fails_then_passes(world):
    # Prevents: a retrieved lesson silently ignored in the derivation.
    unit, env = world
    r = run(["retrieve", "--unit", str(unit), "--shape", "rolling-window"], env)
    assert "row-offset-as-time" in r.stdout
    r = run(["retrieve", "--unit", str(unit), "--report"], env)
    assert r.returncode == 1 and "row-offset-as-time: not disposed" in r.stderr
    rows = retrieval.read(str(unit))
    rows[0].update(disposition="applies", reason="hourly bars have gaps")
    rows.append({"item": "bars.spacing-across-outage", "origin": "new"})
    retrieval.write(str(unit), rows)
    r = run(["retrieve", "--unit", str(unit), "--report"], env)
    assert r.returncode == 0, r.stderr
    assert "retrieved=1 applied=1 dismissed=0 new=1" in r.stdout


def test_dismissal_without_reason_fails(world):
    unit, env = world
    run(["retrieve", "--unit", str(unit), "--context", "xnys"], env)
    rows = retrieval.read(str(unit))
    rows[0]["disposition"] = "does-not-apply"
    retrieval.write(str(unit), rows)
    r = run(["retrieve", "--unit", str(unit), "--report"], env)
    assert r.returncode == 1 and "with no reason" in r.stderr


def test_rerun_keeps_dispositions(world):
    unit, env = world
    run(["retrieve", "--unit", str(unit), "--shape", "rolling-window"], env)
    rows = retrieval.read(str(unit))
    rows[0].update(disposition="applies", reason="x")
    retrieval.write(str(unit), rows)
    run(["retrieve", "--unit", str(unit), "--shape", "rolling-window,entity-join"], env)
    got = {r["entry"]: r["disposition"] for r in retrieval.read(str(unit))}
    assert got == {"row-offset-as-time": "applies", "ticker-reuse": None}


def test_retrieval_with_a_synonym_key_fails_and_records_nothing(world):
    # Prevents: a unit declaring "trailing-window" retrieving nothing and reading as clean.
    unit, env = world
    r = run(["retrieve", "--unit", str(unit), "--shape", "trailing-window"], env)
    assert r.returncode == 1
    assert "shape 'trailing-window' is not in keys.jsonl" in r.stderr
    assert not (unit / "retrieval.jsonl").exists()


def test_move_between_contexts_retrieves_what_differs(world):
    # Prevents: a method ported from XNYS to CME carrying XNYS session rules unexamined.
    unit, env = world
    r = run(["retrieve", "--unit", str(unit), "--context", "cme", "--moved-from", "xnys"], env)
    assert "xnys-half-days" in r.stdout and "cme-sunday-open" in r.stdout
    assert "ticker-reuse" not in r.stdout


SPEC = "Rank perpetuals by 7-day volatility of hourly returns."


def fake_ask(replies, prompts):
    def ask(family, prompt):
        prompts.append((family, prompt))
        return json.dumps(replies[len(prompts) - 1])

    return ask


def test_families_raise_independently_and_convergence_is_counted(tmp_path):
    a = {"items": [
        {"id": "gap", "kind": "premise", "text": "bars are one hour apart"},
        {"id": "vol-claim", "kind": "claim", "text": "vol is over 168 hours"},
    ]}
    b = {"items": [
        {"id": "hourly-spacing", "kind": "premise", "text": "consecutive rows are an hour apart"},
        {"id": "symbol-reuse", "kind": "failure-case", "text": "a delisted symbol is relisted"},
    ]}
    pairs = {"pairs": [["gap", "hourly-spacing"]]}
    spec = tmp_path / "spec.md"
    spec.write_text(SPEC)
    prompts = []
    derive.derive(str(tmp_path), str(spec), ask=fake_ask([a, b, pairs], prompts))
    # The second family's prompt holds the spec and nothing the first family raised.
    assert prompts[1][0] == "gpt" and "bars are one hour apart" not in prompts[1][1]
    counts, problems = derive.report(str(tmp_path))
    assert problems == []
    assert counts == {"items": 3, "claude": 2, "gpt": 2, "convergent": 1}


def test_item_without_family_fails(tmp_path):
    (tmp_path / derive.MERGED).write_text(json.dumps({"id": "x", "kind": "premise", "text": "t"}) + "\n")
    r = run(["derive", "--unit", str(tmp_path), "--report"], dict(os.environ))
    assert r.returncode == 1 and "x: no family marker" in r.stderr
