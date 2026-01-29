#!/usr/bin/env python3
"""
CLI entry point for references plugin.

Commands:
    status  - Show sync status
    sync    - Run sync workflow
    search  - Search references
"""

import argparse
import sys
from pathlib import Path

# Add lib to path for standalone execution
sys.path.insert(0, str(Path(__file__).parent))

from config import get_config, validate_config


def cmd_status(args):
    """Show reference sync status."""
    from zotero import get_zotero_items, get_parsed_refs, get_summarized_refs
    from database import get_db_refs

    try:
        config = get_config()
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    # Validate config
    issues = validate_config(config)
    if issues:
        print("Configuration warnings:")
        for issue in issues:
            print(f"  - {issue}")
        print()

    print("Scanning Zotero library...")
    zotero_items = get_zotero_items(config)

    print("Scanning papers directory...")
    parsed_keys = get_parsed_refs(config)
    summarized_keys = get_summarized_refs(config)
    db_keys = get_db_refs(config)

    # Compute sets
    zotero_keys = set(zotero_items.keys())

    # Categories
    not_parsed = zotero_keys - parsed_keys
    parsed_no_summary = parsed_keys - summarized_keys
    not_in_db = zotero_keys - db_keys

    # Summary
    print("\n" + "=" * 60)
    print("REFERENCE STATUS SUMMARY")
    print("=" * 60)
    print(f"Zotero items (Library {config.zotero_library_id}): {len(zotero_keys):>5}")
    print(f"Parsed (have markdown):          {len(parsed_keys):>5}")
    print(f"Summarized (have summary.json):  {len(summarized_keys):>5}")
    print(f"In reference database:           {len(db_keys):>5}")
    print()
    print(f"NOT PARSED (need Marker):        {len(not_parsed):>5}")
    print(f"PARSED but NO SUMMARY:           {len(parsed_no_summary):>5}")
    print(f"NOT IN DATABASE:                 {len(not_in_db):>5}")
    print("=" * 60)

    if len(not_parsed) == 0 and len(parsed_no_summary) == 0:
        print("\n✅ All references are processed!")
    else:
        print("\nRun /ref-sync to process pending items.")


def cmd_sync(args):
    """Run sync workflow."""
    from parser import parse_new
    from summarizer import summarize_missing
    from database import rebuild_db

    try:
        config = get_config()
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    print("=== Reference Sync ===\n")

    # Parse new PDFs
    print("--- Stage 1: Parse PDFs ---")
    parse_results = parse_new(
        config,
        dry_run=args.dry_run,
        limit=args.limit,
        key=args.key
    )
    print(f"Parsed: {parse_results['success']} success, {parse_results['failed']} failed\n")

    if args.dry_run:
        print("Dry run - no changes made")
        return

    # Generate summaries
    print("--- Stage 2: Generate Summaries ---")
    summary_results = summarize_missing(
        config,
        dry_run=args.dry_run,
        limit=args.limit,
        key=args.key
    )
    print(f"Summarized: {summary_results['success']} success, {summary_results['failed']} failed\n")

    # Rebuild database
    print("--- Stage 3: Rebuild Database ---")
    try:
        rebuild_db(config)
        print("Database updated successfully\n")
    except Exception as e:
        print(f"Database error: {e}\n")

    # Summary
    print("=== Sync Complete ===")
    print(f"Parsed: {parse_results['success']}")
    print(f"Summarized: {summary_results['success']}")

    all_errors = parse_results.get('errors', []) + summary_results.get('errors', [])
    if all_errors:
        print(f"\nErrors ({len(all_errors)}):")
        for err in all_errors[:10]:
            print(f"  - {err}")


def cmd_chapter(args):
    """Get papers for a chapter."""
    from database import get_chapter_papers, get_paper

    try:
        config = get_config()
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    chapter = args.chapter

    print(f"=== Papers for Chapter {chapter} ===\n")

    papers = get_chapter_papers(
        config,
        chapter,
        primary_only=args.primary,
        limit=args.limit
    )

    if not papers:
        print("No papers found for this chapter.")
        return

    for i, paper in enumerate(papers, 1):
        primary = "★" if paper['is_primary'] else " "
        rel = paper['relevance']
        title = (paper['title'] or 'Unknown')[:55]
        year = paper['year'] or '?'
        print(f"{primary} [{rel:3.0f}] {paper['key']}: {title}")
        if args.full and paper['has_summary']:
            full = get_paper(config, paper['key'])
            if full and 'summary' in full:
                summary = full['summary']
                if 'metadata' in summary and 'authors' in summary['metadata']:
                    print(f"       Authors: {', '.join(summary['metadata']['authors'][:3])}")
                if 'reader_summary' in summary and 'tldr' in summary['reader_summary']:
                    tldr = summary['reader_summary']['tldr'][:150]
                    print(f"       {tldr}...")
        print()

    primary_count = sum(1 for p in papers if p['is_primary'])
    print(f"Found {len(papers)} papers ({primary_count} primary). Use [ref:KEY] for citations.")


def cmd_search(args):
    """Search references."""
    from database import search_papers, get_paper

    try:
        config = get_config()
    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    query = ' '.join(args.query)

    print(f"=== Search Results for \"{query}\" ===\n")

    results = search_papers(
        config,
        query,
        chapter=args.chapter,
        limit=args.limit
    )

    if not results:
        print("No results found.")
        return

    for i, paper in enumerate(results, 1):
        citations = f"({paper['citations']} citations)" if paper['citations'] else ""
        print(f"[{i}] {paper['key']} - {paper['title'][:60]}")
        print(f"    {paper['author']}, {paper['year']} {citations}")

        # Show summary snippet if --full
        if args.full:
            full_paper = get_paper(config, paper['key'])
            if full_paper and 'summary' in full_paper:
                summary = full_paper['summary']
                if 'abstract' in summary:
                    print(f"    {summary['abstract'][:200]}...")
        print()

    print(f"Found {len(results)} results. Use [ref:KEY] format for citations.")


def main():
    parser = argparse.ArgumentParser(
        description="References Plugin CLI",
        prog="refs"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Status command
    status_parser = subparsers.add_parser("status", help="Show sync status")

    # Sync command
    sync_parser = subparsers.add_parser("sync", help="Run sync workflow")
    sync_parser.add_argument("--dry-run", action="store_true", help="Preview only")
    sync_parser.add_argument("--limit", type=int, default=0, help="Limit items to process")
    sync_parser.add_argument("--key", type=str, help="Process specific Zotero key")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search references")
    search_parser.add_argument("query", nargs="+", help="Search terms")
    search_parser.add_argument("--chapter", type=int, help="Filter by chapter")
    search_parser.add_argument("--limit", type=int, default=10, help="Max results")
    search_parser.add_argument("--full", action="store_true", help="Show full summaries")

    # Chapter command
    chapter_parser = subparsers.add_parser("chapter", help="Get papers for a chapter")
    chapter_parser.add_argument("chapter", type=int, help="Chapter number")
    chapter_parser.add_argument("--primary", action="store_true", help="Primary refs only")
    chapter_parser.add_argument("--limit", type=int, default=30, help="Max results")
    chapter_parser.add_argument("--full", action="store_true", help="Show summaries")

    args = parser.parse_args()

    if args.command == "status":
        cmd_status(args)
    elif args.command == "sync":
        cmd_sync(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "chapter":
        cmd_chapter(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
