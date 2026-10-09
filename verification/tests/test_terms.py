"""Term tables: unresolved terms block decompose; a resolution in one repository is reused in
another without a question, within the context it was decided for."""
import os
import subprocess
import sys

import pytest

BIN = os.path.join(os.path.dirname(__file__), "..", "bin", "verification")

SPEC = """# Spec: {title}

## Objective

Rank ETFs by 20-day momentum.

## Terms

Context: {context}

| Term | Readings | Status | Basis |
|---|---|---|---|
| 20-day momentum | (a) 20 rows back (b) 20 exchange sessions back | {status} | {basis} |

## Why

x
"""


def run(args, env):
    return subprocess.run([sys.executable, BIN, *args], capture_output=True, text=True, env=env)


@pytest.fixture
def world(tmp_path):
    store = tmp_path / "store"
    store.mkdir()
    a = tmp_path / "course" / ".workspace" / "work" / "u1"
    b = tmp_path / "client" / ".workspace" / "work" / "u7"
    a.mkdir(parents=True)
    b.mkdir(parents=True)
    env = {**os.environ, "VERIFICATION_STORE": str(store), "HOME": str(tmp_path)}
    return store, a / "spec.md", b / "spec.md", env


def spec(path, context="xnys, us-etfs", status="?", basis="-"):
    path.write_text(SPEC.format(title=path.parent.name, context=context, status=status, basis=basis))


def test_unresolved_term_fails(world):
    # Prevents: decompose running on a spec whose term the code will read one way silently.
    _, a, _, env = world
    spec(a)
    r = run(["terms", "check", str(a)], env)
    assert r.returncode == 1
    assert "20-day momentum: unresolved" in r.stderr


def test_missing_section_fails(world):
    _, a, _, env = world
    a.write_text("# Spec\n\n## Objective\n\nx\n")
    assert run(["terms", "check", str(a)], env).returncode == 1


def test_readings_agree_without_data_fails(world):
    # Prevents: "the readings agree" asserted without naming what it was computed on.
    _, a, _, env = world
    spec(a, status="readings-agree", basis="-")
    r = run(["terms", "check", str(a)], env)
    assert r.returncode == 1 and "no basis" in r.stderr


def test_resolution_in_one_repo_resolves_the_other_without_a_question(world):
    store, a, b, env = world
    spec(a, status="resolved-by-author", basis="(b) sessions")
    origin = f"{a.parents[3]}:.workspace/work/u1/spec.md"
    r = run(
        [
            "terms", "define", "--term", "20-day momentum", "--context", "xnys,us-etfs",
            "--definition", "20 exchange sessions on the venue's calendar, reindexed onto the "
            "session grid so a missing session is a gap, not a skipped row",
            "--decided-by", "stefan", "--origin", origin,
        ],
        env,
    )
    assert r.returncode == 0, r.stderr
    assert run(["terms", "check", str(a)], env).returncode == 0

    spec(b, context="us-etfs")
    assert run(["terms", "check", str(b)], env).returncode == 1
    r = run(["terms", "apply", str(b)], env)
    assert "house-definition: 20-day momentum" in r.stdout
    assert "| house-definition | 20-day-momentum--xnys-us-etfs |" in b.read_text()
    assert run(["terms", "check", str(b)], env).returncode == 0


def test_author_asked_again_despite_house_definition_fails(world):
    # Prevents: the author being asked to re-decide a term the store already resolves.
    store, a, b, env = world
    origin = f"{a.parents[3]}:.workspace/work/u1/spec.md"
    spec(a, status="resolved-by-author", basis="(b)")
    run(["terms", "define", "--term", "20-day momentum", "--context", "xnys", "--definition",
         "sessions", "--decided-by", "stefan", "--origin", origin], env)
    spec(b, context="xnys", status="resolved-by-author", basis="(b)")
    r = run(["terms", "check", str(b)], env)
    assert r.returncode == 1 and "use it, not a question" in r.stderr


def test_definition_does_not_cross_into_another_context(world):
    # Prevents: an XNYS session definition being applied to a CME spec, whose sessions differ.
    store, a, b, env = world
    origin = f"{a.parents[3]}:.workspace/work/u1/spec.md"
    spec(a, status="resolved-by-author", basis="(b)")
    run(["terms", "define", "--term", "20-day momentum", "--context", "xnys", "--definition",
         "sessions", "--decided-by", "stefan", "--origin", origin], env)
    spec(b, context="cme")
    r = run(["terms", "apply", str(b)], env)
    assert "0 term(s)" in r.stdout
    assert run(["terms", "check", str(b)], env).returncode == 1
