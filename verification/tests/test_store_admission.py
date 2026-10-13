"""Admission, consolidation and the source check for store entries (criteria 17 to 19).

Each case is a candidate as the intake produces it: a lesson written as the entry it would
become, with a reason for each acceptance test, sometimes with a criterion 7 declaration for
its content.
"""

import json
import sys

from test_store_check import entry, run, write_rows

PASSED = {
    "durability": {"pass": True, "reason": "the gap pattern recurs every weekend"},
    "specificity": {"pass": True, "reason": "names the window and the venue"},
    "decision-changing": {"pass": True, "reason": "changes how a later window is written"},
    "no-stronger-mechanism": {"pass": True, "reason": "no library builds these windows yet"},
    "no-duplicate": {"pass": True, "reason": "no entry covers session windows"},
}


def candidate(tmp, name, **fields):
    body = {"candidate": f"skill:{name}", "tests": PASSED, **fields}
    path = tmp / f"{name}.json"
    path.write_text(json.dumps(body))
    return path


def rows(path):
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def snapshot(store):
    return {p.name: p.read_text() for p in sorted(store.iterdir()) if p.is_file()}


def fresh(repo, **over):
    e = entry(repo, id="session-window", violation="window counts rows across a weekend gap")
    e.update(test="~/project:tests/test_gap.py", violated_variant="~/project:src/bars.py")
    return {**e, **over}


def test_an_admitted_candidate_becomes_an_entry_recording_its_tests(world, tmp_path):
    repo, store, env = world
    write_rows(store / "entries.jsonl", [])
    run(["store", "index"], env)
    r = run(["store", "admit", str(candidate(tmp_path, "windows", entry=fresh(repo)))], env)
    assert r.returncode == 0, r.stderr
    assert "admitted: session-window" in r.stdout
    (added,) = rows(store / "entries.jsonl")
    assert added["id"] == "session-window"
    decision = rows(store / "admissions.jsonl")[-1]
    assert decision["decision"] == "admitted" and decision["failed"] == []
    assert decision["entry"] == "session-window"
    assert decision["reasons"] == {name: t["reason"] for name, t in PASSED.items()}
    assert run(["store", "check"], env).returncode == 0


def test_a_prose_entry_with_no_reason_is_refused_and_nothing_is_written(world, tmp_path):
    # Prevents: a lesson kept as prose without saying why nothing stronger carries it.
    repo, store, env = world
    before = snapshot(store)
    prose = fresh(repo, enforcement={"level": "prose"})
    r = run(["store", "admit", str(candidate(tmp_path, "prose", entry=prose))], env)
    assert r.returncode == 1
    assert "why stronger levels failed" in r.stderr
    assert snapshot(store) == before


def test_a_failed_acceptance_test_rejects_with_its_reason(world, tmp_path):
    repo, store, env = world
    before = rows(store / "entries.jsonl")
    tests = {**PASSED, "durability": {"pass": False, "reason": "about one vendor's 2019 bug"}}
    r = run(
        ["store", "admit", str(candidate(tmp_path, "old", entry=fresh(repo), tests=tests))], env
    )
    assert r.returncode == 0, r.stderr
    assert "rejected: skill:old: durability" in r.stdout
    assert rows(store / "entries.jsonl") == before
    decision = rows(store / "admissions.jsonl")[-1]
    assert decision["failed"] == ["durability"]


def test_a_duplicate_candidate_revises_the_existing_entry(world, tmp_path):
    # Prevents: two entries for one lesson, retrieved twice and drifting apart.
    repo, store, env = world
    existing = rows(store / "entries.jsonl")[0]
    existing.update(fired=["r2p#32"], test="~/project:tests/test_gap.py")
    write_rows(store / "entries.jsonl", [existing])
    run(["store", "index"], env)
    same = fresh(repo, id="gap-hours", violation="window spans a weekend gap as one hour")
    same["test"] = existing["test"]
    same["fired"] = ["r2p#40"]
    r = run(["store", "admit", str(candidate(tmp_path, "dup", entry=same))], env)
    assert r.returncode == 0, r.stderr
    assert "revised: bar-gap" in r.stdout
    (revised,) = rows(store / "entries.jsonl")
    assert revised["id"] == "bar-gap"
    assert revised["violation"] == "window spans a weekend gap as one hour"
    assert revised["fired"] == ["r2p#32", "r2p#40"]
    assert rows(store / "admissions.jsonl")[-1]["decision"] == "revised"
    assert run(["store", "check"], env).returncode == 0


def test_an_overlapping_candidate_must_name_the_entries_it_was_checked_against(world, tmp_path):
    # Prevents: a near-duplicate admitted because nobody compared it with what is stored.
    repo, store, env = world
    near = fresh(repo, shape=["rolling-window"], id="weekend-window")
    r = run(["store", "admit", str(candidate(tmp_path, "near", entry=near))], env)
    assert r.returncode == 1
    assert "overlaps bar-gap" in r.stderr
    named = {**PASSED, "no-duplicate": {"pass": True, "reason": "bar-gap is hourly bars only"}}
    r = run(["store", "admit", str(candidate(tmp_path, "near", entry=near, tests=named))], env)
    assert r.returncode == 0, r.stderr
    assert "admitted: weekend-window" in r.stdout


def test_institutional_content_without_a_source_is_rejected(world, tmp_path):
    repo, store, env = world
    cme = fresh(repo, id="cme-close", context=["crypto-perps"], institutional=True)
    r = run(["store", "admit", str(candidate(tmp_path, "cme", entry=cme))], env)
    assert r.returncode == 0, r.stderr
    assert "rejected: skill:cme: no-source" in r.stdout


def test_content_that_fails_its_own_test_is_rejected_with_the_test(world, tmp_path):
    # Prevents: a skill's prescribed pattern entering the store when it computes the wrong value.
    repo, store, env = world
    (repo / "src" / "ratio.py").write_text("def ratio(n, d):\n    return n / (d - 1)\n")
    (repo / "tests" / "test_ratio.py").write_text(
        "import sys\nsys.path.insert(0, 'src')\nfrom ratio import ratio\n\n"
        "def test_ratio():\n    assert ratio(1, 6) == 1 / 6\n"
    )
    decl = tmp_path / "ratio.decl.json"
    decl.write_text(
        json.dumps(
            {
                "test": "tests/test_ratio.py::test_ratio",
                "root": str(repo),
                "command": [sys.executable, "-m", "pytest", "-q"],
                "producer": "src/ratio.py",
                "variant": {"mutation": {"file": "src/ratio.py", "old": "d - 1", "new": "d + 1"}},
                "fixture": "src/ratio.py",
            }
        )
    )
    path = candidate(tmp_path, "ratio", entry=fresh(repo), declaration=str(decl))
    r = run(["store", "admit", str(path)], env)
    assert r.returncode == 0, r.stderr
    assert "rejected: skill:ratio: fails-its-test" in r.stdout
    decision = rows(store / "admissions.jsonl")[-1]
    assert decision["failing_test"] == f"{repo}:tests/test_ratio.py::test_ratio"
    assert "fails on correct code" in decision["detail"]


def ratio_case(repo, tmp_path, d="d - 1"):
    (repo / "src" / "ratio.py").write_text(f"def ratio(n, d):\n    return n / ({d})\n")
    (repo / "tests" / "test_ratio.py").write_text(
        "import sys\nsys.path.insert(0, 'src')\nfrom ratio import ratio\n\n"
        "def test_ratio():\n    assert ratio(1, 6) == 1 / 6\n"
    )
    decl = tmp_path / "ratio.decl.json"
    decl.write_text(
        json.dumps(
            {
                "test": "tests/test_ratio.py::test_ratio",
                "root": str(repo),
                "command": [sys.executable, "-m", "pytest", "-q"],
                "producer": "src/ratio.py",
                "variant": {
                    "mutation": {"file": "src/ratio.py", "old": f"({d})", "new": "(d + 1)"}
                },
                "fixture": "src/ratio.py",
            }
        )
    )
    return decl


def test_a_skill_whose_content_fails_its_test_needs_no_entry(world, tmp_path):
    # Prevents: a wrong skill having to be written up as a store entry before it can be rejected.
    repo, store, env = world
    decl = ratio_case(repo, tmp_path)
    note = "WRONG block describes holidays as gaps"
    path = candidate(tmp_path, "cal", declaration=str(decl), detail=note)
    r = run(["store", "admit", str(path)], env)
    assert r.returncode == 0, r.stderr
    assert "rejected: skill:cal: fails-its-test" in r.stdout
    decision = rows(store / "admissions.jsonl")[-1]
    assert "entry" not in decision and note in decision["detail"]


def test_an_entryless_candidate_whose_test_passes_is_refused(world, tmp_path):
    repo, store, env = world
    before = snapshot(store)
    decl = ratio_case(repo, tmp_path, d="d")
    r = run(["store", "admit", str(candidate(tmp_path, "ok", declaration=str(decl)))], env)
    assert r.returncode == 1
    assert "give the entry it would become" in r.stderr
    assert snapshot(store) == before


def test_rejections_are_counted_by_reason(world, tmp_path):
    repo, store, env = world
    stale = {**PASSED, "durability": {"pass": False, "reason": "one-off"}}
    vague = {**stale, "specificity": {"pass": False, "reason": "applies to everything"}}
    for name, tests in (("a", stale), ("b", vague)):
        run(["store", "admit", str(candidate(tmp_path, name, entry=fresh(repo), tests=tests))], env)
    r = run(["store", "rejections"], env)
    assert r.returncode == 0, r.stderr
    assert "durability\t2" in r.stdout and "specificity\t1" in r.stdout
    assert "rejected\t2" in r.stdout


def test_consolidate_removes_an_entry_made_unrepresentable(world, tmp_path):
    # Prevents: the loaded store carrying lessons whose violation can no longer be written.
    repo, store, env = world
    (repo / "src" / "window.py").write_text("class SessionWindow:\n    pass\n")
    stored = rows(store / "entries.jsonl")[0]
    stored["enforcement"] = {
        "level": "unrepresentable",
        "where": f"{repo}:src/window.py::SessionWindow",
        "library": "bars",
    }
    write_rows(store / "entries.jsonl", [stored])
    run(["store", "index"], env)
    r = run(["store", "library-enforced"], env)
    assert "bar-gap\tunrepresentable\tbars\tentries" in r.stdout
    r = run(["store", "consolidate"], env)
    assert r.returncode == 0, r.stderr
    assert "retired: bar-gap" in r.stdout
    assert rows(store / "entries.jsonl") == []
    assert rows(store / "retired.jsonl")[0]["entry"]["id"] == "bar-gap"
    assert (
        "bar-gap\tunrepresentable\tbars\tretired" in run(["store", "library-enforced"], env).stdout
    )
    assert run(["store", "check"], env).returncode == 0


def test_consolidate_keeps_an_entry_whose_enforcing_code_is_gone(world):
    repo, store, env = world
    stored = rows(store / "entries.jsonl")[0]
    stored["enforcement"] = {"level": "unrepresentable", "where": f"{repo}:src/gone.py"}
    write_rows(store / "entries.jsonl", [stored])
    before = snapshot(store)
    r = run(["store", "consolidate"], env)
    assert r.returncode == 1
    assert "bar-gap: enforcement.where does not resolve" in r.stderr
    assert snapshot(store) == before


def test_sources_exits_non_zero_on_a_sourceless_institutional_entry(world):
    repo, store, env = world
    cme = entry(repo, id="cme-sessions", context=["crypto-perps"], institutional=True)
    write_rows(store / "entries.jsonl", [entry(repo), cme])
    r = run(["store", "sources"], env)
    assert r.returncode == 1
    assert "cme-sessions: institutional, no source" in r.stderr
    cme["source"] = "https://www.cmegroup.com/trading-hours.html"
    write_rows(store / "entries.jsonl", [entry(repo), cme])
    assert run(["store", "sources"], env).returncode == 0
