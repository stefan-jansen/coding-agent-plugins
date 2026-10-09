"""`verification corpus check`: every source maps to exactly one cause, both families classify."""
import json
import os
import subprocess
import sys

import pytest

BIN = os.path.join(os.path.dirname(__file__), "..", "bin", "verification")


def run(args, env):
    return subprocess.run([sys.executable, BIN, *args], capture_output=True, text=True, env=env)


def write(path, rows):
    path.write_text("".join(json.dumps(r) + "\n" for r in rows))


def cause(cid, sources, claude="premise", gpt="premise"):
    return {
        "id": cid,
        "summary": f"{cid} summary",
        "sources": sources,
        "unrecoverable_reason": "not traced",
        "classification": {"claude": claude, "gpt": gpt},
    }


@pytest.fixture
def corpus(tmp_path):
    origin = tmp_path / "errata.md"
    origin.write_text("## E5.1\n## E5.2\n")
    sources = [
        {"id": s, "title": s, "origin": f"{tmp_path}:errata.md"}
        for s in ("errata:E5.1", "errata:E5.2", "issue:o/r#7")
    ]
    write(tmp_path / "sources.jsonl", sources)
    write(
        tmp_path / "causes.jsonl",
        [
            cause("ch05-scaling", ["errata:E5.1", "errata:E5.2"]),
            cause("lib-drawdown", ["issue:o/r#7"], gpt="test"),
        ],
    )
    env = {**os.environ, "VERIFICATION_STORE": str(tmp_path)}
    assert run(["corpus", "disagreements"], env).returncode == 0
    return tmp_path, env


def test_complete_corpus_passes(corpus):
    _, env = corpus
    r = run(["corpus", "check"], env)
    assert r.returncode == 0, r.stderr


def test_new_erratum_not_grouped_fails(corpus):
    # Prevents: an erratum added to the inventory after grouping silently missing from the corpus.
    path, env = corpus
    rows = [json.loads(x) for x in (path / "sources.jsonl").read_text().splitlines()]
    rows.append({"id": "errata:E5.3", "title": "new", "origin": f"{path}:errata.md"})
    write(path / "sources.jsonl", rows)
    r = run(["corpus", "check"], env)
    assert r.returncode == 1
    assert "errata:E5.3: maps to 0 causes" in r.stderr


def test_erratum_grouped_twice_fails(corpus):
    # Prevents: two grouping passes claiming the same erratum, double-counting a defect.
    path, env = corpus
    rows = [json.loads(x) for x in (path / "causes.jsonl").read_text().splitlines()]
    rows.append(cause("ch05-other", ["errata:E5.2"]))
    write(path / "causes.jsonl", rows)
    r = run(["corpus", "check"], env)
    assert r.returncode == 1
    assert "errata:E5.2: maps to 2 causes" in r.stderr


def test_cause_missing_a_family_fails(corpus):
    path, env = corpus
    rows = [json.loads(x) for x in (path / "causes.jsonl").read_text().splitlines()]
    del rows[0]["classification"]["gpt"]
    write(path / "causes.jsonl", rows)
    r = run(["corpus", "check"], env)
    assert r.returncode == 1
    assert "ch05-scaling: not classified by gpt" in r.stderr


def test_disagreement_file_stale_after_reclassification_fails(corpus):
    # Prevents: the author resolving a list that no longer matches the families' answers.
    path, env = corpus
    rows = [json.loads(x) for x in (path / "causes.jsonl").read_text().splitlines()]
    rows[0]["classification"]["gpt"] = "term"
    write(path / "causes.jsonl", rows)
    r = run(["corpus", "check"], env)
    assert r.returncode == 1
    assert "disagreements.tsv" in r.stderr
    run(["corpus", "disagreements"], env)
    lines = (path / "disagreements.tsv").read_text().splitlines()
    assert [x.split("\t")[0] for x in lines[1:]] == ["ch05-scaling", "lib-drawdown"]
    assert run(["corpus", "check"], env).returncode == 0
