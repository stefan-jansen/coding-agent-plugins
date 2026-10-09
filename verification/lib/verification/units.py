"""Premises, claims and closure declared in issue bodies (plan.md or a single issue body).

An issue that computes over data carries, per input:

    ### Premises

    Input: hourly bars

    | Question | Answer | Kind |
    |---|---|---|
    | record | one exchange-hour of trades for one perpetual | definitional |
    | absent-record | exchange outage; no trades were possible | empirical |
    ...

Kind is `definitional` (resolved in the spec's term table) or `empirical` (to be tested).
An answer of `not-applicable: <reason>` needs no kind. An issue that computes over no data
writes `Premises: none - <reason>`. An issue that simulates trading writes
`Simulates trading: yes` and answers the simulation questions too.

    ### Claims

    | Id | Claim | How it could be false |
    |---|---|---|
    | ic-lag | IC falls with lag | a row lag is reported as a session lag |

    Closes: hourly-bars.spacing, ic-lag
    Advances: hourly-bars.known-at

Each item is `<input-slug>.<question>` for a premise and its Id for a claim.
"""

import json
import os
import re

from . import store

DEFAULT_QUESTIONS = [
    ("record", "data", "what one record means"),
    ("absent-record", "data", "what an absent record means"),
    ("ordering-spacing", "data", "what ordering and spacing the code relies on"),
    ("entity-identity", "data", "what identifies an entity across records"),
    ("known-at", "data", "when each value became known and could have been acted on"),
    ("institution", "data", "which institution or source's rules decide these answers"),
    ("information-arrival", "simulation", "when information arrives"),
    ("order-timing", "simulation", "when an order can be placed"),
    ("achievable-price", "simulation", "what price was achievable"),
]
KINDS = ("definitional", "empirical")
NA = "not-applicable:"

_ISSUE = re.compile(r"^\*\*Issue\s+(\d+)\s+(?:-|--|—)\s+(.+?)\*\*\s*$")


def questions(path):
    """The premise questions: the store's list when present, else the built-in one."""
    rows = []
    if path:
        for _, r, _ in store.read_rows(path, "premise_questions.jsonl"):
            if isinstance(r, dict):
                rows.append((r["id"], r["applies_to"], r["question"]))
    return rows or DEFAULT_QUESTIONS


def issues(text):
    """[(number, title, body)] from a plan.md; a text with no issue headings is one body."""
    out, cur = [], None
    for line in text.splitlines():
        m = _ISSUE.match(line)
        if m:
            cur = [int(m.group(1)), m.group(2), []]
            out.append(cur)
            continue
        if line.startswith("## "):
            cur = None
            continue
        if cur is not None:
            cur[2].append(line)
    if not out:
        return [(0, "issue", text)]
    return [(n, t, "\n".join(b)) for n, t, b in out]


def _slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def _table_rows(lines):
    for line in lines:
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if set("".join(cells)) <= set("-: ") or cells[0].lower() in ("question", "id"):
            continue
        yield cells


def _section(body, name):
    m = re.search(rf"^###\s+{name}\s*$(.*?)(?=^###\s|\Z)", body, re.M | re.S)
    return m.group(1) if m else None


def premises(body):
    """{input_slug: (input_name, {question: (answer, kind)})}, or None when absent."""
    sec = _section(body, "Premises")
    if sec is None:
        return None
    inputs, cur = {}, None
    for line in sec.splitlines():
        m = re.match(r"^Input:\s*(.+)$", line.strip())
        if m:
            cur = _slug(m.group(1))
            inputs[cur] = (m.group(1).strip(), {})
            continue
        if cur and line.strip().startswith("|"):
            for cells in _table_rows([line]):
                q = cells[0]
                answer = cells[1] if len(cells) > 1 else ""
                kind = cells[2] if len(cells) > 2 else ""
                inputs[cur][1][q] = (answer, kind)
    return inputs


def claims(body):
    """[(id, claim, how_false)] from the Claims section."""
    sec = _section(body, "Claims")
    if sec is None:
        return []
    out = []
    for cells in _table_rows(sec.splitlines()):
        cells = cells + [""] * (3 - len(cells))
        out.append((cells[0], cells[1], cells[2]))
    return out


def declared(body, label):
    m = re.search(rf"^{label}:\s*(.*)$", body, re.M)
    if not m:
        return None
    value = m.group(1).strip()
    if value.lower().startswith("none"):
        return []
    return [x.strip() for x in value.split(",") if x.strip()]


def items(body):
    """Every premise and claim id an issue body defines."""
    out = []
    for slug, (_, answers) in (premises(body) or {}).items():
        for q, (answer, _) in answers.items():
            if not answer.lower().startswith(NA):
                out.append(f"{slug}.{q}")
    out += [cid for cid, _, _ in claims(body)]
    return out


def check_premises(text, path=None):
    problems = []
    qs = questions(path)
    for n, title, body in issues(text):
        who = f"issue {n} ({title})"
        if re.search(r"^Premises:\s*none\s*-\s*\S", body, re.M):
            continue
        found = premises(body)
        if found is None:
            problems.append(f"{who}: no Premises section and no `Premises: none - <reason>`")
            continue
        if not found:
            problems.append(f"{who}: Premises section names no Input")
        sim = re.search(r"^Simulates trading:\s*yes", body, re.M | re.I) is not None
        wanted = [q for q, scope, _ in qs if scope == "data" or (sim and scope == "simulation")]
        for slug, (name, answers) in found.items():
            for q in wanted:
                answer, kind = answers.get(q, ("", ""))
                if not answer:
                    problems.append(f"{who}: input {name!r} does not answer {q}")
                elif answer.lower().startswith(NA):
                    if not answer[len(NA) :].strip():
                        problems.append(
                            f"{who}: input {name!r} {q} is not-applicable without reason"
                        )
                elif kind not in KINDS:
                    problems.append(f"{who}: input {name!r} {q} is not marked {' or '.join(KINDS)}")
    return problems


def check_claims(text):
    problems = []
    for n, title, body in issues(text):
        for cid, claim, how in claims(body):
            if not how or how in ("-", "?"):
                problems.append(f"issue {n} ({title}): claim {cid!r} has no way of being false")
    return problems


def check_closure(text):
    problems = []
    defined, closers = set(), {}
    for n, title, body in issues(text):
        who = f"issue {n} ({title})"
        defined.update(items(body))
        closes = declared(body, "Closes")
        if closes is None:
            problems.append(f"{who}: no `Closes:` line (write `Closes: none` if it closes none)")
            continue
        for item in closes:
            closers.setdefault(item, []).append(n)
    for item in sorted(defined - set(closers)):
        problems.append(f"{item}: defined but closed by no issue")
    for item in sorted(set(closers) - defined):
        problems.append(f"{item}: closed by issue {closers[item][0]} but defined nowhere")
    for item, ns in sorted(closers.items()):
        if len(ns) > 1:
            problems.append(f"{item}: closed by more than one issue ({', '.join(map(str, ns))})")
    return problems


def list_claims(text):
    return [(n, cid, claim, how) for n, _, body in issues(text) for cid, claim, how in claims(body)]


def seed_questions(path):
    """Write the built-in question set to the store, where misses can extend it."""
    file = os.path.join(path, "premise_questions.jsonl")
    with open(file, "w", encoding="utf-8") as fh:
        for q, scope, text in DEFAULT_QUESTIONS:
            fh.write(json.dumps({"id": q, "applies_to": scope, "question": text}) + "\n")
