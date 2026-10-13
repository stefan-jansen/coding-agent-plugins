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

Instead of `fixture`, a declaration may list `fixtures`, smallest first:

      "fixtures": [
        {"name": "2015", "files": {"tests/fixtures/x.parquet": "<reduced copy>"}},
        {"name": "committed", "files": {}}
      ]

For each, its files are copied over their targets for both runs and restored afterwards. The
first fixture on which both runs hold is the one the test is accepted on; a reduction that
dropped the rows the violation needs is rejected and the next larger fixture is tried (criterion
8). A reduced copy may be at most 10 MB unless the fixture is marked `"full": true`.

The test is run twice. In the correct run it must pass. In the violated run it must fail as a
test failure (pytest exit 1), not as a crash. In both runs the producer must execute, so the
violated input comes from the producing code rather than from a frame built by hand. A
mutation's lines must execute in the violated run; a perturbation must be called in it, from
`ml4t.diagnostic.evaluation.violations`. The test reads $VERIFICATION_VARIANT ("correct" or
"violated") when its variant is a perturbation; a mutation is applied to the file and needs no
cooperation from the test.

The trace covers every Python process the test run starts, so a producer that a pipeline
runner executes as a stage subprocess counts as run. It records which functions ran, not which
object reached the check. A test that calls
the producer and then hands the check a frame it built anyway is not caught here; reviewing the
declared test is still required.
"""

import glob
import json
import os
import shutil
import subprocess
import tempfile

TRACE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "trace")
PERTURBATIONS_FILE = os.path.join("diagnostic", "evaluation", "violations.py")
TEST_FAILED = 1
FIXTURE_LIMIT = 10 * 1024 * 1024


def load(path):
    with open(path, encoding="utf-8") as fh:
        decl = json.load(fh)
    here = os.path.dirname(os.path.abspath(path))
    decl["root"] = os.path.normpath(os.path.join(here, os.path.expanduser(decl.get("root") or ".")))
    decl.setdefault("command", ["python", "-m", "pytest"])
    return decl


def _abs(decl, rel):
    return os.path.realpath(os.path.join(decl["root"], os.path.expanduser(rel)))


def validate(decl):
    """Everything wrong with the declaration, found before anything runs or is edited."""
    problems = []
    for field in ("test", "producer", "variant"):
        if not decl.get(field):
            problems.append(f"declaration: {field} missing")
    if bool(decl.get("fixture")) == bool(decl.get("fixtures")):
        problems.append("declaration: give exactly one of fixture or fixtures")
    if problems:
        return problems
    for fx in _fixtures(decl):
        problems += _fixture_problems(decl, fx)
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
                problems.append(
                    f"mutation text occurs {count} times in {m['file']}; need exactly 1"
                )
    elif set(variant) != {"perturbation"} or not variant["perturbation"]:
        problems.append("variant: give exactly one of mutation or perturbation")
    return problems


def _fixtures(decl):
    if decl.get("fixtures"):
        return decl["fixtures"]
    return [{"name": decl["fixture"], "files": {}}]


def _fixture_problems(decl, fx):
    name = fx.get("name")
    if not name or not isinstance(fx.get("files"), dict):
        return [f"fixture {name or '?'}: needs a name and a files map"]
    problems = []
    for target, source in fx["files"].items():
        if not os.path.isfile(_abs(decl, target)):
            problems.append(f"fixture {name}: target {target} does not exist")
        source = _abs(decl, source)
        if not os.path.isfile(source):
            problems.append(f"fixture {name}: {os.path.basename(source)} does not exist")
        elif not fx.get("full") and os.path.getsize(source) > FIXTURE_LIMIT:
            problems.append(f"fixture {name}: {os.path.basename(source)} is over 10 MB")
    return problems


def _swap(decl, files):
    """Copy each source over its target; return what to restore."""
    saved = []
    try:
        for target, source in files.items():
            target = _abs(decl, target)
            with open(target, "rb") as fh:
                saved.append((target, fh.read()))
            shutil.copyfile(_abs(decl, source), target)
    except BaseException:
        _restore(saved)
        raise
    return saved


def _restore(saved):
    for target, data in saved:
        with open(target, "wb") as fh:
            fh.write(data)


def _mutated_lines(text, old, new):
    """1-based lines the mutation occupies in the mutated text; for a deletion, the line before."""
    start = text.index(old)
    first = text.count("\n", 0, start) + 1
    if not new.strip():
        return [max(first - 1, 1)]
    return list(range(first, first + new.count("\n") + (0 if new.endswith("\n") else 1)))


def _run(decl, variant, watch_lines):
    """Run the test once. Every Python process it starts, the test process and any stage it
    launches as a child, loads trace/sitecustomize.py and records what it executed."""
    trace_dir = tempfile.mkdtemp(prefix="verification-trace-")
    env = {
        **os.environ,
        "VERIFICATION_VARIANT": variant,
        "VERIFICATION_TRACE_DIR": trace_dir,
        "VERIFICATION_TRACE_LINES": ",".join(f"{p}:{n}" for p, n in watch_lines),
        "PYTHONPATH": os.pathsep.join(filter(None, [TRACE_DIR, os.environ.get("PYTHONPATH")])),
    }
    cmd = [*decl["command"], "-p", "no:cacheprovider", decl["test"]]
    functions, lines = set(), set()
    try:
        proc = subprocess.run(cmd, cwd=decl["root"], env=env, capture_output=True, text=True)
        for path in glob.glob(os.path.join(trace_dir, "*.json")):
            try:
                with open(path, encoding="utf-8") as fh:
                    trace = json.load(fh)
            except (OSError, ValueError):
                continue
            functions |= {tuple(f) for f in trace["functions"]}
            lines |= {tuple(x) for x in trace["lines"]}
    finally:
        shutil.rmtree(trace_dir, ignore_errors=True)
    return proc, functions, lines


def run_once(decl, variant):
    """Run the test once on the code as it stands, without judging it."""
    return _run(decl, variant, [])[0]


def _producer_ran(functions, producer):
    """A function of the producer ran. Importing it runs only its module body, which emits
    nothing, so a test that imports the producer and checks a hand-built frame does not count."""
    return any(path == producer and name != "<module>" for path, name in functions)


def violate(decl):
    """Return (verdict lines, problems). No problems means the test satisfies criterion 7, on
    the first fixture where both runs hold."""
    problems = validate(decl)
    if problems:
        return [], problems
    fixtures = _fixtures(decl)
    report = [f"test: {decl['test']}"]
    rejected = []
    for fx in fixtures:
        saved = _swap(decl, fx["files"])
        try:
            lines, problems = _judge(decl)
        finally:
            _restore(saved)
        if not problems or decl.get("fixture"):
            return report + [f"fixture (both runs): {fx['name']}", *lines], problems
        report.append(f"fixture {fx['name']}: rejected: {'; '.join(problems)}")
        rejected += [f"fixture {fx['name']}: {p}" for p in problems]
    return report, ["no fixture satisfies both runs", *rejected]


def _judge(decl):
    """Both runs on whatever fixture is in place."""
    problems = []
    producer = _abs(decl, decl["producer"])
    variant = decl["variant"]
    report = []

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
