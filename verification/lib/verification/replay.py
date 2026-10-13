"""Replay a corpus cause blind: redo the spec-time process at the commit before the defect and
record which component, if any, surfaced it.

For one cause, `run` exports the pre-defect commit with `git archive` (no history, so the fix
and the defect record are not in it) into a directory whose name says nothing about the task.
Each family reads the specification the work was done from, may read that checkout, and lists
terms, premises, claims and failure cases. Its transcript is scanned for any read of the store,
the cause, or the record of the defect; a replay with such a read is invalid. Both families
then judge, independently, which listed items would have exposed the defect, given its summary.

The retrieval component is not exercised: the store is withheld. A failure case counts for the
test component; the replay does not write or run the test.
"""

import json
import os
import re
import secrets
import subprocess
import tempfile
from datetime import date, datetime, timezone

from . import families, formats, store, units

COMPONENT = {"term": "term", "premise": "premise", "claim": "claim", "failure-case": "test"}
RESULTS = "replays.jsonl"

PROMPT = """You are starting a piece of quantitative work. The specification is below. The
repository as it stands before the work begins is the current directory; read whatever in it
helps you.

Before any code is written, list:
- term: a word or phrase in the specification with more than one reading that would produce
  different code or different numbers ("20-day": rows or sessions). Give the readings.
- premise: for each input the work reads, the answer to each of these questions{simulation}:
{questions}
- claim: a number, comparison or property the output will assert to a reader, and how it
  could be false. For a measured number (a time, throughput, speedup or size), also
  what bounds it, what else it could be measuring, whether the work ran inside the measured region, whether
  both sides ran configured alike, and the arithmetic limit it must respect.
- failure-case: a specific way the work could be wrong that a test should catch, produced the
  way it would actually arise (a code defect, or input the real pipeline could emit).

Reply with only a JSON object: {{"items": [{{"id": "<short-slug>", "kind":
"term|premise|claim|failure-case", "text": "<one or two lines>"}}]}}

--- specification ---
{spec}
"""

JUDGE = """A defect was later found in the work below. Here is what it was:

{defect}

Before the work was done, a reviewer listed these items:

{items}

Which items, if acted on, would have exposed this defect: the item names the same condition or
a condition that directly implies it, so a check written from the item would fail on the
defect? Be strict: an item about a different column, step or error does not count.

Reply with only a JSON object: {{"exposing": ["<item id>", ...], "reason": "<one line>"}}"""

COMMANDS = {
    "claude": lambda prompt, cwd, out: [
        "claude",
        "-p",
        "--restricted",
        "--tools",
        "Read,Glob,Grep",
        "--output-format",
        "stream-json",
        "--verbose",
        prompt,
    ],
    "gpt": lambda prompt, cwd, out: [
        "codex",
        "exec",
        "--json",
        "--sandbox",
        "read-only",
        "--skip-git-repo-check",
        "--ephemeral",
        "-C",
        cwd,
        "-o",
        out,
        prompt,
    ],
}


def prompt(spec, store_path):
    """The spec-time listing as the process now defines it: the premise questions come from the
    store's question set (criterion 3), claims carry the measured-number checklist."""
    qs = units.questions(store_path)
    lines = [f"  - {q}: {text}" for q, scope, text in qs if scope == "data"]
    lines += [
        f"  - {q}: {text} (if the work simulates trading)"
        for q, scope, text in qs
        if scope != "data"
    ]
    sim = (
        "; the last ones only if it simulates trading" if any(s != "data" for _, s, _ in qs) else ""
    )
    return PROMPT.format(spec=spec, questions="\n".join(lines), simulation=sim)


def _cause(path, cause_id):
    for _, row, _ in store.read_rows(path, "causes.jsonl"):
        if isinstance(row, dict) and row.get("id") == cause_id:
            return row
    raise KeyError(f"cause {cause_id!r} is not in causes.jsonl")


def _git(repo, *args):
    return subprocess.run(
        ["git", "-C", repo, *args], capture_output=True, text=True, check=True
    ).stdout


def path_at(repo, sha, path):
    """The name `path` had at `sha`, following renames made after it."""
    log = _git(repo, "log", "--follow", "--name-status", "--format=@%H", "--", path)
    current, commit = path, None
    for line in log.splitlines():
        if line.startswith("@"):
            commit = line[1:]
        elif line.startswith("R") and commit:
            _, old, new = line.split("\t")
            ancestor = subprocess.run(
                ["git", "-C", repo, "merge-base", "--is-ancestor", commit, sha]
            )
            if new == current and ancestor.returncode != 0:
                current = old
    return current


def spec_text(cause):
    """The specification as it stood when the work began, and where it came from.

    A path is read at the pre-defect commit. An issue is read as it is now, with its last edit
    time, so a body edited after the work began is flagged rather than silently used."""
    repo, sha = cause["pre_defect_commit"].split("@")
    ref = cause.get("spec") or ""
    started = _git(repo, "show", "-s", "--format=%cI", sha).strip()
    if ref.startswith("https://github.com/"):
        m = re.match(r"https://github.com/([^/]+/[^/]+)/issues/(\d+)", ref)
        owner, name = m.group(1).split("/")
        query = (
            "query($o:String!,$n:String!,$i:Int!){repository(owner:$o,name:$n)"
            "{issue(number:$i){title body lastEditedAt}}}"
        )
        data = json.loads(
            subprocess.run(
                [
                    "gh",
                    "api",
                    "graphql",
                    "-f",
                    f"query={query}",
                    "-f",
                    f"o={owner}",
                    "-f",
                    f"n={name}",
                    "-F",
                    f"i={m.group(2)}",
                ],
                capture_output=True,
                text=True,
                check=True,
            ).stdout
        )["data"]["repository"]["issue"]
        edited = data.get("lastEditedAt")
        late = bool(edited) and datetime.fromisoformat(
            edited.replace("Z", "+00:00")
        ) > datetime.fromisoformat(started)
        return f"# {data['title']}\n\n{data['body']}", {"spec": ref, "edited_after_start": late}
    if ":" in ref:
        spec_repo, path = ref.split(":", 1)
        if os.path.realpath(spec_repo) == os.path.realpath(repo):
            try:
                return _git(repo, "show", f"{sha}:{path_at(repo, sha, path)}"), {
                    "spec": ref,
                    "at": sha,
                }
            except subprocess.CalledProcessError:
                return None, {"spec": ref, "missing": f"not in {sha[:7]}"}
        before = _git(spec_repo, "rev-list", "-1", f"--before={started}", "HEAD").strip()
        try:
            return _git(spec_repo, "show", f"{before}:{path}"), {"spec": ref, "at": before}
        except subprocess.CalledProcessError:
            return None, {"spec": ref, "missing": f"not in {spec_repo} before {started}"}
    return None, {"spec": ref, "missing": "no specification recorded"}


def forbidden(cause, store_path):
    """Paths and names whose appearance in a tool call means the replay read what it must not:
    the store, the cause, the live repository (which holds the fix), and the record of the
    defect. Reads inside the exported checkout are the point of the replay and are allowed."""
    repo = cause["pre_defect_commit"].split("@")[0]
    banned = {
        os.path.realpath(store_path),
        "verification-store",
        cause["id"],
        os.path.expanduser("~/agents/factory"),
        os.path.expanduser("~/ml4t/agents/errata"),
        os.path.realpath(repo),
    }
    for field in ("reproduction", "evidence"):
        ref = cause.get(field) or ""
        if ":" in ref and not ref.startswith("http"):
            banned.add(os.path.join(*ref.split(":", 1)))
    return sorted(banned)


def tool_calls(family, transcript):
    """The text of every tool call or command in a transcript."""
    calls = []
    for line in transcript.splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if family == "claude" and ev.get("type") == "assistant":
            for block in ev.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    calls.append(json.dumps(block.get("input")))
        elif family == "gpt":
            item = ev.get("item") or {}
            if item.get("type") in ("command_execution", "file_read", "mcp_tool_call"):
                # What was asked for, not what came back: a file in the checkout may mention a
                # banned path without the replay having read it.
                calls.append(
                    json.dumps({k: v for k, v in item.items() if k != "aggregated_output"})
                )
    return calls


def leaks(family, transcript, banned):
    return sorted({b for call in tool_calls(family, transcript) for b in banned if b in call})


def _final_text(family, transcript, out):
    if family == "gpt":
        with open(out, encoding="utf-8") as fh:
            return fh.read()
    for line in reversed(transcript.splitlines()):
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "result":
            return ev.get("result") or ""
    return ""


def _ask_in(family, prompt, cwd, timeout=3600):
    out = os.path.join(tempfile.mkdtemp(prefix="o-"), "reply.txt")
    r = subprocess.run(
        COMMANDS[family](prompt, cwd, out),
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=timeout,
        stdin=subprocess.DEVNULL,
    )
    if r.returncode != 0:
        raise RuntimeError(f"{family} exited {r.returncode}: {r.stderr[-2000:]}")
    return r.stdout, _final_text(family, r.stdout, out)


def _items(text):
    items = families.parse_json_object(text).get("items", [])
    return [i for i in items if i.get("kind") in COMPONENT and i.get("id") and i.get("text")]


def run(cause_id, out_dir, root=None, store_path=None, ask=families.ask, ask_in=_ask_in):
    """Replay one cause on both families; write transcripts and the result under out_dir."""
    store_path = store_path or store.location()
    cause = _cause(store_path, cause_id)
    if not cause.get("pre_defect_commit"):
        return {"cause_id": cause_id, "skipped": "no pre-defect commit"}
    spec, provenance = spec_text(cause)
    if spec is None:
        return {"cause_id": cause_id, "skipped": provenance["missing"], **provenance}
    repo, sha = cause["pre_defect_commit"].split("@")
    work = os.path.join(root or tempfile.gettempdir(), "w" + secrets.token_hex(4))
    os.makedirs(work)
    archive = subprocess.run(["git", "-C", repo, "archive", sha], capture_output=True, check=True)
    subprocess.run(["tar", "-x", "-C", work], input=archive.stdout, check=True)
    # The environment is not in git. Without it an agent reaches for the live repository's
    # interpreter, which the scan must then count as a read of the live repository.
    venv = os.path.join(repo, ".venv")
    if os.path.isdir(venv) and not os.path.lexists(os.path.join(work, ".venv")):
        os.symlink(venv, os.path.join(work, ".venv"))
    banned = forbidden(cause, store_path)
    run_id = f"{cause_id}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')}"
    os.makedirs(out_dir, exist_ok=True)
    listed, invalid = [], {}
    for family in ("claude", "gpt"):
        transcript, final = ask_in(family, prompt(spec, store_path), work)
        path = os.path.join(out_dir, f"{run_id}.{family}.jsonl")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(transcript)
        bad = leaks(family, transcript, banned)
        if bad:
            invalid[family] = bad
            continue
        listed += [{**i, "id": f"{family}:{i['id']}", "family": family} for i in _items(final)]
    defect = cause["summary"] + ("\n" + cause["detail"] if cause.get("detail") else "")
    item_text = "\n".join(f"- {i['id']} ({i['kind']}): {i['text']}" for i in listed)
    verdicts = {}
    for judge in ("claude", "gpt"):
        reply = families.parse_json_object(ask(judge, JUDGE.format(defect=defect, items=item_text)))
        ids = {i["id"] for i in listed}
        verdicts[judge] = {
            "exposing": [x for x in reply.get("exposing", []) if x in ids],
            "reason": reply.get("reason", ""),
        }
    agreed = set(verdicts["claude"]["exposing"]) & set(verdicts["gpt"]["exposing"])
    kinds = {i["id"]: COMPONENT[i["kind"]] for i in listed}
    surfaced = sorted({kinds[x] for x in agreed}, key=formats.CATEGORIES.index)
    result = {
        "run_id": run_id,
        "cause_id": cause_id,
        "date": date.today().isoformat(),
        "surfaced_by": surfaced[0] if surfaced else "none",
        "components": surfaced,
        "agreed_items": sorted(agreed),
        "verdicts": verdicts,
        "items": listed,
        "invalid": invalid,
        "blind": not invalid,
        "workdir": work,
        **provenance,
        "transcript": os.path.join(out_dir, f"{run_id}.claude.jsonl"),
    }
    with open(os.path.join(out_dir, f"{run_id}.json"), "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=1, ensure_ascii=False)
    return result


def report(out_dir):
    """Catch counts per component over the latest valid replay of each cause."""
    latest = {}
    for name in sorted(os.listdir(out_dir)):
        if name.endswith(".json"):
            with open(os.path.join(out_dir, name), encoding="utf-8") as fh:
                r = json.load(fh)
            latest[r["cause_id"]] = r
    valid = [r for r in latest.values() if r.get("blind")]
    counts = {c: sum(c in r.get("components", []) for r in valid) for c in formats.CATEGORIES}
    counts["none"] = sum(not r.get("components") for r in valid)
    return {"replayed": len(valid), "invalid": len(latest) - len(valid), **counts}, latest


def _results(out_dir):
    rows = []
    for name in sorted(os.listdir(out_dir)):
        if name.endswith(".json"):
            with open(os.path.join(out_dir, name), encoding="utf-8") as fh:
                rows.append(json.load(fh))
    return rows


def _category(cause):
    if cause.get("resolved"):
        return cause["resolved"]
    seen = set((cause.get("classification") or {}).values())
    return seen.pop() if len(seen) == 1 else "disagree"


COMPARED = tuple(c for c in formats.CATEGORIES if c != "retrieval")  # the store is withheld


def _rates(results):
    n = len(results)
    return {
        c: (sum(c in r.get("components", []) for r in results) / n if n else 0.0) for c in COMPARED
    }


def history(runs_dir, store_path):
    """Catch rates per component for each run (each subdirectory of runs_dir, in name order),
    and what to change next: each component whose rate on the causes common to the last two runs
    did not rise, and each category of cause that no component caught in the latest run."""
    causes = {r.get("id"): r for _, r, _ in store.read_rows(store_path, "causes.jsonl") if r}
    runs = []
    for name in sorted(d for d in os.listdir(runs_dir) if os.path.isdir(os.path.join(runs_dir, d))):
        latest = {r["cause_id"]: r for r in _results(os.path.join(runs_dir, name))}
        valid = {c: r for c, r in latest.items() if r.get("blind")}
        runs.append(
            {
                "run": name,
                "replayed": len(valid),
                "invalid": len(latest) - len(valid),
                "rates": _rates(list(valid.values())),
                "none": sum(not r.get("components") for r in valid.values()),
                "_valid": valid,
            }
        )
    improved, common = [], 0
    if len(runs) >= 2:
        prev, last = runs[-2]["_valid"], runs[-1]["_valid"]
        shared = sorted(set(prev) & set(last))
        common = len(shared)
        before = _rates([prev[c] for c in shared])
        after = _rates([last[c] for c in shared])
        improved = [c for c in COMPARED if after[c] > before[c]]
    uncaught = []
    if runs:
        by_cat = {}
        for cid, r in runs[-1]["_valid"].items():
            by_cat.setdefault(_category(causes.get(cid, {})), []).append(r)
        uncaught = sorted(k for k, rs in by_cat.items() if not any(r.get("components") for r in rs))
    for r in runs:
        r.pop("_valid")
    return {
        "runs": runs,
        "common": common,
        "improved": improved,
        "next": {
            "components": [c for c in COMPARED if c not in improved],
            "uncaught_categories": uncaught,
        },
    }


def _pointer(path):
    path = os.path.abspath(path)
    top = subprocess.run(
        ["git", "-C", os.path.dirname(path), "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    base = top or os.path.dirname(path)
    home = os.path.expanduser("~")
    shown = "~" + base[len(home) :] if base.startswith(home + os.sep) else base
    return f"{shown}:{os.path.relpath(path, base)}"


def record(out_dir, store_path):
    """Append a store row for each result in out_dir not already recorded; return how many."""
    seen = {r.get("run_id") for _, r, _ in store.read_rows(store_path, RESULTS) if r}
    rows = []
    for r in _results(out_dir):
        if r["run_id"] in seen:
            continue
        row = {
            "run_id": r["run_id"],
            "cause_id": r["cause_id"],
            "date": r["date"],
            "surfaced_by": r["surfaced_by"],
            "transcript": _pointer(r["transcript"]),
            "blind": r["blind"],
        }
        problems = store.row_problems(RESULTS, row)
        if problems:
            raise ValueError(f"{r['run_id']}: {'; '.join(problems)}")
        rows.append(row)
    with open(os.path.join(store_path, RESULTS), "a", encoding="utf-8") as fh:
        fh.writelines(json.dumps(x, ensure_ascii=False) + "\n" for x in rows)
    return len(rows)
