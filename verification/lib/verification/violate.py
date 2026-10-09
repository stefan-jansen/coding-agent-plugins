"""`verification violate`: run a test against its violated variant and against correct code.

A declaration (JSON) names the test and how its violation arises:

    {
      "test": "tests/test_bars.py::test_gap",
      "root": "<repository the test runs in>",
      "command": ["uv", "run", "pytest"],
      "producer": "src/bars.py",
      "variant": {"mutation": {"file": "src/bars.py", "old": "...", "new": "..."}}
                 | {"perturbation": "drop_window"},
      "fixture": "<the data both runs read>"
    }

The test is run twice. In the correct run it must pass. In the violated run it must fail as a
test failure (pytest exit 1), not as a crash. In both runs the producer must execute, so the
violated input comes from the producing code rather than from a frame built by hand. A
mutation's lines must execute in the violated run; a perturbation must be called in it, from
`ml4t.diagnostic.evaluation.violations`. The test reads $VERIFICATION_VARIANT ("correct" or
"violated") when its variant is a perturbation; a mutation is applied to the file and needs no
cooperation from the test.

The trace records which functions ran, not which object reached the check. A test that calls
the producer and then hands the check a frame it built anyway is not caught here; reviewing the
declared test is still required.
"""

import json
import os
import subprocess
import tempfile

PLUGIN_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "pytest_plugin")
PERTURBATIONS_FILE = os.path.join("diagnostic", "evaluation", "violations.py")
TEST_FAILED = 1


def load(path):
    with open(path, encoding="utf-8") as fh:
        decl = json.load(fh)
    root = os.path.expanduser(decl.get("root") or os.path.dirname(os.path.abspath(path)))
    decl["root"] = root
    decl.setdefault("command", ["python", "-m", "pytest"])
    return decl


def _abs(decl, rel):
    return os.path.realpath(os.path.join(decl["root"], os.path.expanduser(rel)))


def validate(decl):
    """Everything wrong with the declaration, found before anything runs or is edited."""
    problems = []
    for field in ("test", "producer", "variant", "fixture"):
        if not decl.get(field):
            problems.append(f"declaration: {field} missing")
    if problems:
        return problems
    if not os.path.isfile(_abs(decl, decl["producer"])):
        problems.append(f"producer {decl['producer']} does not exist under {decl['root']}")
    variant = decl["variant"]
    if set(variant) == {"mutation"}:
        m = variant["mutation"]
        path = _abs(decl, m.get("file", ""))
        if not os.path.isfile(path):
            problems.append(f"mutation file {m.get('file')!r} does not exist")
        else:
            with open(path, encoding="utf-8") as fh:
                count = fh.read().count(m.get("old") or "\0")
            if count != 1:
                problems.append(f"mutation text occurs {count} times in {m['file']}; need exactly 1")
    elif set(variant) != {"perturbation"} or not variant["perturbation"]:
        problems.append("variant: give exactly one of mutation or perturbation")
    return problems


def _mutated_lines(text, old, new):
    """1-based lines the mutation occupies in the mutated text; for a deletion, the line before."""
    start = text.index(old)
    first = text.count("\n", 0, start) + 1
    if not new.strip():
        return [max(first - 1, 1)]
    return list(range(first, first + new.count("\n") + (0 if new.endswith("\n") else 1)))


def _run(decl, variant, watch_lines):
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
        trace_out = fh.name
    env = {
        **os.environ,
        "VERIFICATION_VARIANT": variant,
        "VERIFICATION_TRACE_OUT": trace_out,
        "VERIFICATION_TRACE_LINES": ",".join(f"{p}:{n}" for p, n in watch_lines),
        "PYTHONPATH": os.pathsep.join(filter(None, [PLUGIN_DIR, os.environ.get("PYTHONPATH")])),
    }
    cmd = [*decl["command"], "-p", "verification_trace", "-p", "no:cacheprovider", decl["test"]]
    proc = subprocess.run(cmd, cwd=decl["root"], env=env, capture_output=True, text=True)
    try:
        with open(trace_out, encoding="utf-8") as fh:
            trace = json.load(fh)
    except (OSError, ValueError):
        trace = {"functions": [], "lines": []}
    finally:
        os.unlink(trace_out)
    functions = {tuple(f) for f in trace["functions"]}
    lines = {tuple(x) for x in trace["lines"]}
    return proc, functions, lines


def _producer_ran(functions, producer):
    """A function of the producer ran. Importing it runs only its module body, which emits
    nothing, so a test that imports the producer and checks a hand-built frame does not count."""
    return any(path == producer and name != "<module>" for path, name in functions)


def violate(decl):
    """Return (verdict lines, problems). No problems means the test satisfies criterion 7."""
    problems = validate(decl)
    if problems:
        return [], problems
    producer = _abs(decl, decl["producer"])
    variant = decl["variant"]
    report = [f"test: {decl['test']}", f"fixture (both runs): {decl['fixture']}"]

    correct, functions, _ = _run(decl, "correct", [])
    report.append(f"correct run: exit {correct.returncode}")
    if correct.returncode != 0:
        problems.append(f"the test fails on correct code (exit {correct.returncode})")
    if not _producer_ran(functions, producer):
        problems.append(f"correct run: producer {decl['producer']} never executed")

    if "mutation" in variant:
        m = variant["mutation"]
        path = _abs(decl, m["file"])
        with open(path, encoding="utf-8") as fh:
            original = fh.read()
        mutated = original.replace(m["old"], m["new"], 1)
        watch = [(path, n) for n in _mutated_lines(original, m["old"], m["new"])]
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(mutated)
        try:
            violated, functions, lines = _run(decl, "violated", watch)
        finally:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(original)
        if not lines:
            problems.append(f"violated run: the mutated lines of {m['file']} never executed")
    else:
        violated, functions, _ = _run(decl, "violated", [])
        name = variant["perturbation"]
        called = any(p.endswith(PERTURBATIONS_FILE) and f == name for p, f in functions)
        if not called:
            problems.append(f"violated run: perturbation {name} was never called")
    report.append(f"violated run: exit {violated.returncode}")
    if violated.returncode == 0:
        problems.append("the test passes on the violated variant: it cannot catch this violation")
    elif violated.returncode != TEST_FAILED:
        problems.append(
            f"the violated run ended with exit {violated.returncode}, not a test failure: "
            "the variant broke the run instead of reaching the test"
        )
    if not _producer_ran(functions, producer):
        problems.append(
            f"violated run: producer {decl['producer']} never executed, so the violated input "
            "was not produced by the producing code"
        )
    return report, problems
