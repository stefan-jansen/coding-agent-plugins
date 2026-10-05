"""The defect corpus: causes deduplicated from their sources, with replay starting points."""

from . import store


def causes(path):
    return [row for _, row, _ in store.read_rows(path, "causes.jsonl") if isinstance(row, dict)]


def report(path):
    """Counts for the corpus: recoverable pre-defect commits and classification agreement."""
    rows = causes(path)
    families = sorted({f for r in rows for f in (r.get("classification") or {})})
    recoverable = sum(1 for r in rows if r.get("pre_defect_commit"))
    complete = [r for r in rows if all(f in (r.get("classification") or {}) for f in families)]
    disagree = [r["id"] for r in complete if len(set(r["classification"].values())) > 1]
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
