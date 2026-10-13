"""Blind replay: the replay sees the work as it began and nothing of the defect's record."""

import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from verification import replay  # noqa: E402


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


@pytest.fixture
def world(tmp_path):
    """A repository whose spec was written, then the defect found and the spec amended."""
    repo = tmp_path / "project"
    repo.mkdir()
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "t@t")
    git(repo, "config", "user.name", "t")
    (repo / "spec.md").write_text("Label each ETF over 21 sessions.\n")
    (repo / "labels.py").write_text("H = 21\n")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "start")
    before = git(repo, "rev-parse", "HEAD")
    (repo / "spec.md").write_text("Label each ETF over 21 sessions. Exits must precede 2024.\n")
    (repo / "audit.md").write_text("labels exit inside the holdout\n")
    git(repo, "add", ".")
    git(repo, "commit", "-qm", "fix holdout leak")
    store = tmp_path / "store"
    store.mkdir()
    cause = {
        "id": "holdout-exit",
        "summary": "labels exit inside the holdout",
        "sources": ["commit:abc"],
        "classification": {},
        "spec": f"{repo}:spec.md",
        "pre_defect_commit": f"{repo}@{before}",
        "reproduction": f"{repo}:audit.md",
    }
    (store / "causes.jsonl").write_text(json.dumps(cause) + "\n")
    return {"repo": repo, "store": store, "out": tmp_path / "out", "root": tmp_path / "w"}


def claude_transcript(items, reads=()):
    events = [
        {
            "type": "assistant",
            "message": {
                "content": [{"type": "tool_use", "name": "Read", "input": {"file_path": p}}]
            },
        }
        for p in reads
    ]
    events.append({"type": "result", "result": json.dumps({"items": items})})
    return "\n".join(json.dumps(e) for e in events)


def gpt_transcript(commands=()):
    return "\n".join(
        json.dumps({"type": "item.completed", "item": {"type": "command_execution", "command": c}})
        for c in commands
    )


ITEMS = [
    {
        "id": "exit-after-holdout",
        "kind": "failure-case",
        "text": "a label whose exit falls in the holdout",
    },
    {"id": "sessions", "kind": "term", "text": "21 sessions: rows or exchange sessions"},
]


def fake(world, claude_reads=(), gpt_commands=(), seen=None):
    def ask_in(family, prompt, cwd, timeout=0):
        if seen is not None:
            venv = os.path.realpath(os.path.join(cwd, ".venv"))
            seen.update(cwd=cwd, prompt=prompt, files=sorted(os.listdir(cwd)), venv=venv)
        if family == "claude":
            reads = [r.format(cwd=cwd) for r in claude_reads]
            return claude_transcript(ITEMS, reads), json.dumps({"items": ITEMS})
        return gpt_transcript([c.format(cwd=cwd) for c in gpt_commands]), json.dumps(
            {"items": ITEMS}
        )

    return ask_in


def judges(claude_ids, gpt_ids):
    def ask(family, prompt):
        ids = claude_ids if family == "claude" else gpt_ids
        return json.dumps(
            {"exposing": [f"{f}:{i}" for f in ("claude", "gpt") for i in ids], "reason": "r"}
        )

    return ask


def run(world, ask_in, ask):
    world["root"].mkdir(exist_ok=True)
    return replay.run(
        "holdout-exit",
        str(world["out"]),
        root=str(world["root"]),
        store_path=str(world["store"]),
        ask=ask,
        ask_in=ask_in,
    )


def test_the_replay_reads_the_spec_and_code_as_the_work_began(world):
    # Prevents: the amended spec or the fix reaching the replay, which then "catches" a defect
    # it was told about.
    seen = {}
    run(world, fake(world, seen=seen), judges([], []))
    assert "Exits must precede 2024" not in seen["prompt"]
    assert "Label each ETF over 21 sessions." in seen["prompt"]
    assert seen["files"] == ["labels.py", "spec.md"]
    assert "holdout" not in os.path.basename(seen["cwd"])


def test_a_replay_leaves_no_checkout_behind(world):
    # Prevents: every replay leaving a full checkout of the repository on disk; a book batch
    # left nine of 243 MB each.
    run(world, fake(world), judges([], []))
    assert list(world["root"].iterdir()) == []


def test_a_failed_agent_call_still_removes_the_checkout(world):
    def broken(family, prompt, cwd):
        raise RuntimeError("agent killed")

    with pytest.raises(RuntimeError):
        run(world, broken, judges([], []))
    assert list(world["root"].iterdir()) == []


def test_a_read_of_the_live_repository_invalidates_the_replay(world):
    # The live repository holds the fix and the audit; reading it is reading the answer.
    r = run(
        world,
        fake(world, claude_reads=[str(world["repo"] / "audit.md")]),
        judges(["exit-after-holdout"], ["exit-after-holdout"]),
    )
    assert r["blind"] is False and "claude" in r["invalid"]


def test_a_gpt_command_that_reads_the_store_invalidates_the_replay(world):
    r = run(world, fake(world, gpt_commands=[f"cat {world['store']}/causes.jsonl"]), judges([], []))
    assert r["blind"] is False and "gpt" in r["invalid"]


def test_reads_inside_the_checkout_keep_the_replay_blind(world):
    r = run(
        world,
        fake(world, claude_reads=["{cwd}/labels.py"], gpt_commands=["cat {cwd}/spec.md"]),
        judges([], []),
    )
    assert r["blind"] is True


def test_a_component_counts_only_when_both_judges_name_its_item(world):
    one = run(world, fake(world), judges(["exit-after-holdout"], []))
    assert one["surfaced_by"] == "none"
    both = run(world, fake(world), judges(["exit-after-holdout"], ["exit-after-holdout"]))
    assert both["components"] == ["test"]


def test_report_counts_valid_replays_and_fails_on_an_invalid_one(world):
    run(world, fake(world), judges(["sessions"], ["sessions"]))
    counts, _ = replay.report(str(world["out"]))
    assert counts["replayed"] == 1 and counts["term"] == 1 and counts["invalid"] == 0
    run(world, fake(world, claude_reads=[str(world["store"])]), judges([], []))
    counts, _ = replay.report(str(world["out"]))
    assert counts["invalid"] == 1 and counts["replayed"] == 0


def test_a_spec_renamed_after_the_work_began_is_read_under_its_old_name(world):
    # Prevents: a replay skipped, or fed the current text, because the spec moved since.
    repo = world["repo"]
    (repo / "docs").mkdir()
    git(repo, "mv", "spec.md", "docs/spec.md")
    git(repo, "commit", "-qm", "move spec")
    cause = json.loads((world["store"] / "causes.jsonl").read_text())
    cause["spec"] = f"{repo}:docs/spec.md"
    text, provenance = replay.spec_text(cause)
    assert text == "Label each ETF over 21 sessions.\n"


def test_a_banned_path_in_command_output_does_not_invalidate(world):
    # The checkout's own notes can name the live repository; printing them is not reading it.
    def ask_in(family, prompt, cwd, timeout=0):
        if family == "claude":
            return claude_transcript(ITEMS), json.dumps({"items": ITEMS})
        event = {
            "type": "item.completed",
            "item": {
                "type": "command_execution",
                "command": "cat AGENTS.md",
                "aggregated_output": f"see {world['repo']}",
            },
        }
        return json.dumps(event), json.dumps({"items": ITEMS})

    assert run(world, ask_in, judges([], []))["blind"] is True


def test_the_checkout_runs_with_the_repository_environment(world):
    # Prevents: an agent invoking the live repository's interpreter, which voids the replay.
    (world["repo"] / ".venv").mkdir()
    seen = {}
    run(world, fake(world, seen=seen), judges([], []))
    assert seen["venv"] == os.path.realpath(world["repo"] / ".venv")
    # Removing the checkout removes the link, never the environment it points to.
    assert (world["repo"] / ".venv").is_dir()


def test_the_prompt_asks_the_premise_questions_of_the_current_process(world):
    # Prevents: a replay that measures an older process than the one sessions run, so a
    # change to the question set never shows up in the catch rate.
    rows = [
        {
            "id": "ordering-spacing",
            "applies_to": "data",
            "question": "what spacing the code relies on",
        },
        {
            "id": "order-timing",
            "applies_to": "simulation",
            "question": "when an order can be placed",
        },
    ]
    (world["store"] / "premise_questions.jsonl").write_text(
        "".join(json.dumps(r) + "\n" for r in rows)
    )
    seen = {}
    run(world, fake(world, seen=seen), judges([], []))
    assert "ordering-spacing: what spacing the code relies on" in seen["prompt"]
    assert "order-timing: when an order can be placed" in seen["prompt"]
    assert "what bounds it" in seen["prompt"]  # the measured-number checklist


def result(out, cause, components, blind=True):
    out.mkdir(parents=True, exist_ok=True)
    row = {
        "run_id": f"{cause}-{out.name}",
        "cause_id": cause,
        "date": "2026-10-13",
        "surfaced_by": (components or ["none"])[0],
        "components": components,
        "blind": blind,
        "transcript": str(out / f"{cause}.claude.jsonl"),
    }
    (out / f"{cause}.json").write_text(json.dumps(row))
    (out / f"{cause}.claude.jsonl").write_text("")


def history_store(tmp_path):
    store = tmp_path / "hstore"
    store.mkdir()
    causes = [("a", "premise"), ("b", "premise"), ("c", "test"), ("d", "claim")]
    (store / "causes.jsonl").write_text(
        "".join(
            json.dumps(
                {
                    "id": i,
                    "summary": i,
                    "sources": ["audit:x"],
                    "classification": {"claude": c, "gpt": c},
                }
            )
            + "\n"
            for i, c in causes
        )
    )
    return store


def test_history_names_the_component_that_did_not_improve_and_the_uncaught_category(tmp_path):
    # Prevents: a process change shipped without anyone seeing that a component's catch rate
    # stood still, or that a whole category of shipped defect is caught by nothing.
    runs = tmp_path / "replays"
    result(runs / "2026-10-09", "a", [])
    result(runs / "2026-10-09", "b", ["term"])
    result(runs / "2026-10-09", "c", ["test"])
    result(runs / "2026-10-13", "a", ["premise"])
    result(runs / "2026-10-13", "b", ["term"])
    result(runs / "2026-10-13", "c", ["test"])
    result(runs / "2026-10-13", "d", [])
    hist = replay.history(str(runs), str(history_store(tmp_path)))
    assert [r["run"] for r in hist["runs"]] == ["2026-10-09", "2026-10-13"]
    assert hist["runs"][1]["rates"]["premise"] == 0.25
    assert hist["common"] == 3
    assert {"premise"} == set(hist["improved"])
    assert set(hist["next"]["components"]) == {"term", "claim", "test"}
    assert hist["next"]["uncaught_categories"] == ["claim"]


def test_an_invalid_replay_is_left_out_of_the_rates(tmp_path):
    runs = tmp_path / "replays"
    result(runs / "r1", "a", ["premise"], blind=False)
    result(runs / "r1", "c", [])
    hist = replay.history(str(runs), str(history_store(tmp_path)))
    assert hist["runs"][0]["replayed"] == 1 and hist["runs"][0]["invalid"] == 1
    assert hist["runs"][0]["rates"]["premise"] == 0.0


def test_record_appends_each_result_once(tmp_path):
    store = history_store(tmp_path)
    result(tmp_path / "replays" / "r1", "a", ["premise"])
    assert replay.record(str(tmp_path / "replays" / "r1"), str(store)) == 1
    assert replay.record(str(tmp_path / "replays" / "r1"), str(store)) == 0
    (row,) = [json.loads(x) for x in (store / "replays.jsonl").read_text().splitlines()]
    assert row["surfaced_by"] == "premise" and row["blind"] is True


def test_a_run_that_adds_easier_causes_does_not_count_as_an_improvement(tmp_path):
    # Prevents: a rerun that also replays newly sampled causes the process happens to catch
    # reporting a better catch rate for a component that caught nothing more on the same causes.
    runs = tmp_path / "replays"
    result(runs / "r1", "a", [])
    result(runs / "r1", "b", ["term"])
    result(runs / "r2", "a", [])
    result(runs / "r2", "b", ["term"])
    result(runs / "r2", "c", ["term"])
    hist = replay.history(str(runs), str(history_store(tmp_path)))
    assert hist["runs"][1]["rates"]["term"] > hist["runs"][0]["rates"]["term"]
    assert "term" not in hist["improved"] and "term" in hist["next"]["components"]


def test_a_cause_written_with_home_relative_pointers_replays(world, monkeypatch):
    # Prevents: causes traced into the store as ~/repo@sha (the store's pointer form) failing
    # every replay because git is handed an unexpanded ~.
    monkeypatch.setenv("HOME", str(world["repo"].parent))
    cause = json.loads((world["store"] / "causes.jsonl").read_text())
    for field in ("spec", "pre_defect_commit", "reproduction"):
        cause[field] = cause[field].replace(str(world["repo"]), "~/project")
    (world["store"] / "causes.jsonl").write_text(json.dumps(cause) + "\n")
    seen = {}
    r = run(world, fake(world, seen=seen, claude_reads=["~/project/audit.md"]), judges([], []))
    assert "Label each ETF over 21 sessions." in seen["prompt"]
    assert r["blind"] is False  # ~/project is the live repository, banned in either spelling
