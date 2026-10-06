"""The defect corpus: causes deduplicated from their sources, with replay starting points."""

import os

from . import store


def causes(path):
    return [row for _, row, _ in store.read_rows(path, "causes.jsonl") if isinstance(row, dict)]


def report(path):
    """Counts for the corpus: recoverable pre-defect commits and classification agreement."""
    rows = causes(path)
    families = sorted({f for r in rows for f in (r.get("classification") or {})})
    recoverable = sum(1 for r in rows if r.get("pre_defect_commit"))
    complete = [r for r in rows if all(f in (r.get("classification") or {}) for f in families)]
    disagree = [cid for cid, _, _ in disagreements(path)]
    return {
        "causes": len(rows),
        "recoverable": recoverable,
        "families": families,
        "classified_by_all": len(complete),
        "disagreements": disagree,
    }


def format_report(r):
    share = f"{r['recoverable'] / r['causes']:.0%}" if r["causes"] else "n/a"
    lines = [
        f"causes: {r['causes']}",
        f"pre-defect commit recoverable: {r['recoverable']} of {r['causes']} ({share})",
        f"families: {', '.join(r['families']) or 'none'}",
        f"classified by every family: {r['classified_by_all']} of {r['causes']}",
        f"disagreements: {len(r['disagreements'])}",
    ]
    lines += [f"  {cid}" for cid in r["disagreements"]]
    return "\n".join(lines)


FAMILIES = ("claude", "gpt")
DISAGREEMENTS = "disagreements.tsv"


def disagreements(path):
    """Causes the two families classified differently, as (id, {family: category}, summary)."""
    out = []
    for r in causes(path):
        cls = r.get("classification") or {}
        if all(f in cls for f in FAMILIES) and len({cls[f] for f in FAMILIES}) > 1:
            out.append((r["id"], cls, r.get("summary", "")))
    return out


def render_disagreements(path):
    """The file put to the author: one row per disagreement, with any decision already taken."""
    lines = ["id\tclaude\tgpt\tdecision\tsummary"]
    resolved = {r["id"]: r.get("resolved", "") for r in causes(path)}
    for cid, cls, summary in disagreements(path):
        lines.append("\t".join([cid, cls["claude"], cls["gpt"], resolved.get(cid) or "", summary]))
    return "\n".join(lines) + "\n"


def check(path):
    """Mapping and classification problems; empty means the corpus is complete."""
    problems = []
    known = [r for _, r, _ in store.read_rows(path, "sources.jsonl") if isinstance(r, dict)]
    known_ids = {r["id"] for r in known}
    owners = {}
    for r in causes(path):
        for src in r.get("sources") or []:
            owners.setdefault(src, []).append(r["id"])
            if src.startswith(("errata:", "issue:")) and src not in known_ids:
                problems.append(f"{r['id']}: source {src} is not in sources.jsonl")
        missing = [f for f in FAMILIES if f not in (r.get("classification") or {})]
        if missing:
            problems.append(f"{r['id']}: not classified by {', '.join(missing)}")
    for src in sorted(known_ids):
        n = len(owners.get(src, []))
        if n != 1:
            where = ", ".join(owners.get(src, [])) or "no cause"
            problems.append(f"{src}: maps to {n} causes ({where})")
    file = os.path.join(path, DISAGREEMENTS)
    expected = render_disagreements(path)
    if not os.path.exists(file):
        if disagreements(path):
            problems.append(f"{DISAGREEMENTS}: missing; run `verification corpus disagreements`")
    else:
        with open(file, encoding="utf-8") as fh:
            got = [line.split("\t")[0] for line in fh.read().splitlines()[1:]]
        want = [line.split("\t")[0] for line in expected.splitlines()[1:]]
        if sorted(got) != sorted(want):
            problems.append(
                f"{DISAGREEMENTS}: lists {sorted(got)}, families differ on {sorted(want)}"
            )
    return problems
