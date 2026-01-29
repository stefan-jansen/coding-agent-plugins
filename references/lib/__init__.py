"""
References Plugin - Academic reference management with Zotero.

Public API:
    get_status()         → dict with sync counts
    sync_all()           → full sync workflow
    parse_new()          → parse missing PDFs
    summarize_missing()  → generate AI summaries
    rebuild_db()         → rebuild SQLite index
    search()             → query references
    load_paper()         → get single paper by key
"""

from .config import get_config, Config
from .zotero import get_zotero_items, get_items_with_pdfs
from .parser import get_missing_pdfs, parse_pdf, parse_new
from .summarizer import find_missing_summaries, summarize_paper, summarize_missing
from .database import rebuild_db, search_papers, get_paper, get_chapter_papers

__all__ = [
    # Config
    "get_config",
    "Config",
    # Zotero
    "get_zotero_items",
    "get_items_with_pdfs",
    # Parser
    "get_missing_pdfs",
    "parse_pdf",
    "parse_new",
    # Summarizer
    "find_missing_summaries",
    "summarize_paper",
    "summarize_missing",
    # Database
    "rebuild_db",
    "search_papers",
    "get_paper",
    "get_chapter_papers",
]


def get_status() -> dict:
    """Get comprehensive status of reference sync."""
    from .zotero import get_zotero_items, get_parsed_refs, get_summarized_refs
    from .database import get_db_refs

    config = get_config()

    zotero_items = get_zotero_items(config)
    parsed = get_parsed_refs(config)
    summarized = get_summarized_refs(config)
    db_refs = get_db_refs(config)

    return {
        "zotero_count": len(zotero_items),
        "parsed_count": len(parsed),
        "summarized_count": len(summarized),
        "db_count": len(db_refs),
        "not_parsed": list(set(zotero_items.keys()) - parsed),
        "not_summarized": list(parsed - summarized),
        "not_in_db": list(set(zotero_items.keys()) - db_refs),
    }


def sync_all(dry_run: bool = False, limit: int = 0, key: str = None) -> dict:
    """Run full sync workflow: parse → summarize → rebuild database."""
    results = {
        "parsed": 0,
        "summarized": 0,
        "db_updated": False,
        "errors": []
    }

    config = get_config()

    # Parse new PDFs
    parse_results = parse_new(config, dry_run=dry_run, limit=limit, key=key)
    results["parsed"] = parse_results.get("success", 0)
    results["errors"].extend(parse_results.get("errors", []))

    if dry_run:
        return results

    # Generate summaries
    summary_results = summarize_missing(config, dry_run=dry_run, limit=limit, key=key)
    results["summarized"] = summary_results.get("success", 0)
    results["errors"].extend(summary_results.get("errors", []))

    # Rebuild database
    try:
        rebuild_db(config)
        results["db_updated"] = True
    except Exception as e:
        results["errors"].append(f"Database rebuild failed: {e}")

    return results


def load_paper(key: str) -> dict | None:
    """Load a single paper by Zotero key."""
    config = get_config()
    return get_paper(config, key)
