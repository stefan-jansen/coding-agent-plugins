"""`verification store check` against a store pointing into a real git repository.

Each failing case is produced the way it arises in use: an entry edited until it
outgrows its budget, a test file or function renamed in the repository the entry
points into, an entry added without the field its kind requires, or a store grown
past the index cap.
"""
import json
import os
import subprocess
import sys

import pytest

BIN = os.path.join(os.path.dirname(__file__), "..", "bin", "verification")


def run(args, env):
    return subprocess.run([sys.executable, BIN, *args], capture_output=True, text=True, env=env)


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def write_rows(path, rows):
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))


def entry(repo, **overrides):
    row = {
        "id": "bar-gap",
        "shape": ["rolling-window"],
        "context": ["crypto-perps"],
        "violation": "row offset read as elapsed hours across exchange gaps",
        "test": f"{repo}:tests/test_gap.py::test_gap",
        "violated_variant": f"{repo}:src/bars.py",
        "enforcement": {"level": "test"},
        "institutional": False,
        "fired": [],
        "admission": ["durability", "specificity"],
    }
    row.update(overrides)
    return row


@pytest.fixture
def world(tmp_path):
    repo = tmp_path / "project"
    (repo / "tests").mkdir(parents=True)
    (repo / "src").mkdir()
    (repo / "tests" / "test_gap.py").write_text("def test_gap():\n    pass\n")
    (repo / "src" / "bars.py").write_text("STEP = 1\n")
    git(repo, "init", "-q")
    git(repo, "-c", "user.email=t@t", "-c", "user.name=t", "add", ".")
    git(repo, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "init")
    sha = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    store = tmp_path / "store"
    store.mkdir()
    write_rows(store / "entries.jsonl", [entry(repo)])
    write_rows(
        store / "causes.jsonl",
        [
            {
                "id": "crypto-gap",
                "summary": "features computed across 49-73 hour gaps",
                "sources": ["audit:r2p-2026-09-28"],
                "pre_defect_commit": f"{repo}@{sha}",
                "classification": {"claude": "premise", "gpt": "premise"},
            }
        ],
    )
    write_rows(
        store / "keys.jsonl",
        [
            {"id": "rolling-window", "kind": "shape", "meaning": "window over an ordered series",
             "derived_from": ["crypto-gap"]},
            {"id": "crypto-perps", "kind": "context", "meaning": "crypto perpetuals",
             "derived_from": ["crypto-gap"]},
        ],
    )
    env = {**os.environ, "VERIFICATION_STORE": str(store), "HOME": str(tmp_path)}
    assert run(["store", "index"], env).returncode == 0
    return repo, store, env


def test_sound_store_passes(world):
    _, _, env = world
    r = run(["store", "check"], env)
    assert r.returncode == 0, r.stderr


def test_entry_grown_past_budget_fails(world):
    # Prevents: entries accreting narrative until the store stops being rows.
    repo, store, env = world
    long = entry(repo, violation="row offset read as elapsed hours " + "because " * 40)
    write_rows(store / "entries.jsonl", [long])
    run(["store", "index"], env)
    r = run(["store", "check"], env)
    assert r.returncode == 1
    assert "entries.jsonl:1" in r.stderr and "limit 120" in r.stderr


def test_test_file_renamed_in_target_repo_fails(world):
    # Prevents: an entry claiming enforcement by a test that no longer exists.
    repo, _, env = world
    git(repo, "mv", "tests/test_gap.py", "tests/test_bars.py")
    r = run(["store", "check"], env)
    assert r.returncode == 1
    assert "test does not resolve" in r.stderr


def test_test_function_renamed_fails(world):
    repo, _, env = world
    (repo / "tests" / "test_gap.py").write_text("def test_gap_hours():\n    pass\n")
    r = run(["store", "check"], env)
    assert r.returncode == 1
    assert "test_gap not defined" in r.stderr


def test_commit_missing_after_history_rewrite_fails(world):
    # Prevents: a corpus cause pointing to a pre-defect commit that is gone.
    repo, store, env = world
    rows = [json.loads(line) for line in (store / "causes.jsonl").read_text().splitlines()]
    rows[0]["pre_defect_commit"] = f"{repo}@{'0' * 40}"
    write_rows(store / "causes.jsonl", rows)
    r = run(["store", "check"], env)
    assert r.returncode == 1
    assert "causes.jsonl:1" in r.stderr and "pre_defect_commit" in r.stderr


def test_institutional_entry_without_source_fails(world):
    # Prevents: venue rules entering the store from model recall.
    repo, store, env = world
    cme = entry(repo, id="cme-sessions", context=["cme"], institutional=True)
    write_rows(store / "entries.jsonl", [entry(repo), cme])
    run(["store", "index"], env)
    r = run(["store", "check"], env)
    assert r.returncode == 1
    assert "entries.jsonl:2" in r.stderr and "authoritative source" in r.stderr


def test_prose_entry_without_reason_fails(world):
    repo, store, env = world
    prose = entry(repo, enforcement={"level": "prose"})
    write_rows(store / "entries.jsonl", [prose])
    run(["store", "index"], env)
    r = run(["store", "check"], env)
    assert r.returncode == 1
    assert "why stronger levels failed" in r.stderr


def test_index_past_cap_fails(world):
    # Prevents: the loaded index growing without bound as entries accumulate.
    repo, store, env = world
    rows = [entry(repo, id=f"e{i}") for i in range(200)]
    write_rows(store / "entries.jsonl", rows)
    run(["store", "index"], env)
    r = run(["store", "check"], env)
    assert r.returncode == 1
    assert "cap 4000" in r.stderr


def test_entry_added_without_reindex_fails(world):
    repo, store, env = world
    write_rows(store / "entries.jsonl", [entry(repo), entry(repo, id="second")])
    r = run(["store", "check"], env)
    assert r.returncode == 1
    assert "stale" in r.stderr


def test_absent_store_is_reported_and_passes(tmp_path):
    # Prevents: the public plugin depending on the private store.
    env = {k: v for k, v in os.environ.items() if k != "VERIFICATION_STORE"}
    env["HOME"] = str(tmp_path)
    r = run(["store", "check"], env)
    assert r.returncode == 0
    assert "store absent" in r.stdout


def test_corpus_report_counts_recoverable_and_disagreements(world):
    # Prevents: a corpus whose replay starting points or family split are misreported.
    repo, store, env = world
    rows = [json.loads(line) for line in (store / "causes.jsonl").read_text().splitlines()]
    lost = dict(rows[0], id="lost", pre_defect_commit=None, unrecoverable_reason="squashed")
    lost["classification"] = {"claude": "premise", "gpt": "term"}
    write_rows(store / "causes.jsonl", rows + [lost])
    r = run(["corpus", "report"], env)
    assert r.returncode == 0, r.stderr
    assert "recoverable: 1 of 2 (50%)" in r.stdout
    assert "disagreements: 1\n  lost" in r.stdout


def test_entry_written_with_a_synonym_key_fails(world):
    # Prevents: an entry keyed "trailing-window" that no retrieval for "rolling-window" reaches.
    repo, store, env = world
    write_rows(store / "entries.jsonl", [entry(repo, shape=["trailing-window"])])
    assert run(["store", "index"], env).returncode == 0
    r = run(["store", "check"], env)
    assert r.returncode == 1
    assert "shape 'trailing-window' is not in keys.jsonl" in r.stderr


def test_key_citing_a_renamed_cause_fails(world):
    # Prevents: a vocabulary key whose evidence no longer exists in the corpus.
    repo, store, env = world
    causes = [json.loads(x) for x in (store / "causes.jsonl").read_text().splitlines()]
    causes[0]["id"] = "crypto-row-gaps"
    write_rows(store / "causes.jsonl", causes)
    r = run(["store", "check"], env)
    assert r.returncode == 1
    assert "derived_from 'crypto-gap' is not in causes.jsonl" in r.stderr
