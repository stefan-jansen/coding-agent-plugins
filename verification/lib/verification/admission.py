"""Admission of candidates to the store, and the passes that keep it current (criteria 17-19).

A candidate is a JSON file:

    {
      "candidate": "skill:calendar-ops",        where the lesson came from
      "entry": {...},                            the entry it would become
      "tests": {"durability": {"pass": true, "reason": "..."}, ...},   all five tests
      "revises": "<entry id>",                   optional: the stored entry it replaces
      "declaration": "<violate declaration>",    optional: a criterion 7 test of its content
      "detail": "..."                            optional: a note kept on the decision row
    }

A candidate whose content is tested by its declaration may omit the entry: if the content
fails, the rejection needs none, and if it passes, the candidate is refused until it gives one.

A malformed candidate is refused and nothing is written: a missing test or reason, or an entry
the store would not hold, such as a prose entry that does not say why stronger levels failed.
Otherwise one decision row is appended to `admissions.jsonl`:

- rejected: a test failed, the entry is about an institution and cites no source, or the
  content fails its own test (the declaration's correct run is the lesson's prescription);
- revised: the candidate names an entry it revises, or shares an id, test or violated variant
  with one. The stored row takes the candidate's content and keeps its id and where it fired;
- admitted: a new entry. A candidate that shares a shape and a context with stored entries
  must name each of them in its no-duplicate reason, or set `revises`.
"""

import datetime
import json
import os

from . import formats, pointers, store, violate

LIBRARY = "library"
SOURCE_RULE = "source: an institutional entry"  # a rejection (no-source), not a refusal


def _load(path):
    with open(path, encoding="utf-8") as fh:
        cand = json.load(fh)
    decl = cand.get("declaration")
    if decl:
        here = os.path.dirname(os.path.abspath(path))
        cand["declaration"] = os.path.join(here, os.path.expanduser(decl))
    return cand


def _entries(path):
    return [r for _, r, _ in store.read_rows(path, "entries.jsonl") if isinstance(r, dict)]


def _refusals(path, cand):
    tests = cand.get("tests")
    problems = []
    if not isinstance(cand.get("candidate"), str) or not cand["candidate"].strip():
        problems.append("candidate: name where the lesson came from")
    if not isinstance(tests, dict):
        return problems + ["tests: give a pass and a reason for each acceptance test"]
    for name in formats.ADMISSION_TESTS:
        t = tests.get(name)
        if not isinstance(t, dict) or not isinstance(t.get("pass"), bool):
            problems.append(f"tests.{name}: pass must be true or false")
        elif not isinstance(t.get("reason"), str) or not t["reason"].strip():
            problems.append(f"tests.{name}: reason missing")
    entry = cand.get("entry")
    if entry is None:
        failing = problems or all(tests[n]["pass"] for n in formats.ADMISSION_TESTS)
        if failing and not cand.get("declaration"):
            problems.append("entry: only a candidate that fails a test may omit its entry")
        return problems
    row = dict(entry)
    problems += [
        f"entry: {p}"
        for p in store.row_problems("entries.jsonl", row)
        if not p.startswith(SOURCE_RULE)
    ]
    vocab = store.vocabulary(path)
    problems += [
        f"entry: {p}" for p in store.unknown_keys(vocab, row.get("shape"), row.get("context"))
    ]
    decl = cand.get("declaration")
    if decl and not os.path.isfile(decl):
        problems.append(f"declaration: {decl} not found")
    revises = cand.get("revises")
    if revises and revises not in {e.get("id") for e in _entries(path)}:
        problems.append(f"revises: no stored entry {revises!r}")
    return problems


def _same(stored, entry):
    keys = ("id", "test", "violated_variant")
    return [e for e in stored if any(entry.get(k) and e.get(k) == entry.get(k) for k in keys)]


def _overlapping(stored, entry):
    return [
        e
        for e in stored
        if set(e.get("shape") or []) & set(entry.get("shape") or [])
        and set(e.get("context") or []) & set(entry.get("context") or [])
    ]


def _failing_test(decl):
    root, home = decl["root"], os.path.expanduser("~")
    if root == home or root.startswith(home + os.sep):
        root = "~" + root[len(home) :]
    path, _, symbol = decl["test"].partition("::")
    return f"{root}:{path}" + (f"::{symbol.split('::')[-1]}" if symbol else "")


def _rejection(cand):
    """(failed reasons, failing test pointer, detail) for a candidate that does not pass."""
    failed = [n for n in formats.ADMISSION_TESTS if not cand["tests"][n]["pass"]]
    entry = cand.get("entry") or {}
    if entry.get("institutional") is True and not entry.get("source"):
        failed.append("no-source")
    failing, detail = None, None
    if cand.get("declaration"):
        decl = violate.load(cand["declaration"])
        _, problems = violate.violate(decl)
        if problems:
            failed.append("fails-its-test")
            failing = _failing_test(decl)
            detail = "; ".join(problems)
    return failed, failing, detail


def admit(path, candidate_path, today=None):
    """(decision line, problems). Problems mean a refusal: nothing was written."""
    cand = _load(candidate_path)
    problems = _refusals(path, cand)
    if problems:
        return None, problems
    stored = _entries(path)
    entry = cand.get("entry")
    decision = {
        "candidate": cand["candidate"],
        "date": (today or datetime.date.today()).isoformat(),
        "reasons": {n: cand["tests"][n]["reason"] for n in formats.ADMISSION_TESTS},
    }
    failed, failing, detail = _rejection(cand)
    detail = "; ".join(x for x in (detail, cand.get("detail")) if x) or None
    if not failed and entry is None:
        return None, ["entry: its declaration passed, so give the entry it would become"]
    if failed:
        decision.update(decision="rejected", failed=failed)
        if failing:
            decision["failing_test"] = failing
        if detail:
            decision["detail"] = detail
        if entry:
            decision["entry"] = entry["id"]
        _append(path, decision)
        return f"rejected: {cand['candidate']}: {', '.join(failed)}", []

    row = dict(entry)
    target = cand.get("revises")
    if not target:
        same = _same(stored, entry)
        if len(same) > 1:
            ids = ", ".join(e["id"] for e in same)
            return None, [f"matches several entries ({ids}): set revises to the one it replaces"]
        target = same[0]["id"] if same else None
    if target:
        old = next(e for e in stored if e["id"] == target)
        fired = list(dict.fromkeys((old.get("fired") or []) + (row.get("fired") or [])))
        row.update(id=target, fired=fired)
        rows = [row if e["id"] == target else e for e in stored]
        verb = "revised"
    else:
        reason = cand["tests"]["no-duplicate"]["reason"]
        unnamed = [e["id"] for e in _overlapping(stored, entry) if e["id"] not in reason]
        if unnamed:
            return None, [
                f"overlaps {', '.join(unnamed)}: set revises, or name each in the "
                "no-duplicate reason with why it does not cover this lesson"
            ]
        rows = stored + [row]
        verb = "admitted"
    decision.update(decision=verb, failed=[], entry=row["id"])
    store.write_rows(path, "entries.jsonl", rows)
    store.write_index(path)
    _append(path, decision)
    return f"{verb}: {row['id']}", []


def _append(path, row):
    with open(os.path.join(path, "admissions.jsonl"), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def rejections(path):
    """{decision: count} and {reason: count} over every rejection."""
    decisions = dict.fromkeys(formats.DECISIONS, 0)
    reasons = dict.fromkeys(formats.REJECTION_REASONS, 0)
    for _, row, _ in store.read_rows(path, "admissions.jsonl"):
        if not isinstance(row, dict):
            continue
        decisions[row.get("decision")] = decisions.get(row.get("decision"), 0) + 1
        if row.get("decision") == "rejected":
            for reason in row.get("failed") or []:
                reasons[reason] = reasons.get(reason, 0) + 1
    return decisions, reasons


def consolidate(path, today=None):
    """(retired ids, problems). Moves every entry whose violation is unrepresentable to
    `retired.jsonl`; when one's enforcing code does not resolve, nothing moves."""
    stored = _entries(path)
    gone = [e for e in stored if (e.get("enforcement") or {}).get("level") == "unrepresentable"]
    problems = []
    for e in gone:
        reason = pointers.resolve(e["enforcement"].get("where"))
        if reason:
            problems.append(f"{e['id']}: enforcement.where does not resolve: {reason}")
    if problems or not gone:
        return [], problems
    date = (today or datetime.date.today()).isoformat()
    retired = [r for _, r, _ in store.read_rows(path, "retired.jsonl") if isinstance(r, dict)]
    retired += [
        {
            "entry": e,
            "retired_on": date,
            "reason": f"violation unrepresentable at {e['enforcement']['where']}",
        }
        for e in gone
    ]
    store.write_rows(path, "entries.jsonl", [e for e in stored if e not in gone])
    store.write_rows(path, "retired.jsonl", retired)
    store.write_index(path)
    return [e["id"] for e in gone], []


def library_enforced(path):
    """(id, level, library, file) for every stored or retired entry enforced in a library."""
    out = []
    retired = [r.get("entry") for _, r, _ in store.read_rows(path, "retired.jsonl")]
    for where, rows in (("entries", _entries(path)), ("retired", retired)):
        for e in rows:
            enf = (e or {}).get("enforcement") or {}
            if enf.get(LIBRARY):
                out.append((e["id"], enf["level"], enf[LIBRARY], where))
    return out


def sourceless(path):
    return [
        e["id"] for e in _entries(path) if e.get("institutional") is True and not e.get("source")
    ]
