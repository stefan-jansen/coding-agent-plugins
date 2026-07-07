#!/usr/bin/env python3
"""Search observer database using FTS5.

Usage:
    python3 search.py <query> [--project <name>] [--limit <n>] [--type <type>]
"""
import argparse
import json
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path.home() / ".claude-toolkit" / "observer" / "observer.db"


def search(query: str, project: str = None, limit: int = 20, obs_type: str = None):
    if not DB_PATH.exists():
        print("No observer database found. Complete a session first to populate it.")
        return

    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA busy_timeout = 2000")

    # Build FTS5 query — quote the user query for safety
    fts_query = '"' + query.replace('"', '""') + '"'

    sql = """
        SELECT o.id, o.type, o.title, o.narrative, o.project, o.created_at,
               o.facts, o.files_modified
        FROM observations o
        JOIN observations_fts fts ON o.id = fts.rowid
        WHERE observations_fts MATCH ?
    """
    params: list = [fts_query]

    if project:
        sql += " AND o.project = ?"
        params.append(project)

    if obs_type:
        sql += " AND o.type = ?"
        params.append(obs_type)

    sql += " ORDER BY o.created_at DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    if not rows:
        print(f"No observations found matching '{query}'")
        return

    print(f"## Observer Search: '{query}' ({len(rows)} results)\n")

    for row in rows:
        obs_id, obs_type, title, narrative, proj, created_at, facts, files = row
        print(f"**#{obs_id}** [{obs_type}] {title or '(untitled)'}")
        print(f"  Project: {proj} | {created_at}")
        if narrative:
            display = narrative[:200] + "..." if len(narrative) > 200 else narrative
            print(f"  {display}")
        if facts:
            try:
                fact_list = json.loads(facts)
                if fact_list:
                    for fact in fact_list[:3]:
                        print(f"  - {fact}")
            except (json.JSONDecodeError, TypeError):
                pass
        if files:
            try:
                file_list = json.loads(files)
                if file_list:
                    print(f"  Files: {', '.join(file_list[:5])}")
            except (json.JSONDecodeError, TypeError):
                pass
        print()


def main():
    parser = argparse.ArgumentParser(description="Search observer observations")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--project", "-p", help="Filter by project name")
    parser.add_argument("--limit", "-l", type=int, default=20, help="Max results")
    parser.add_argument("--type", "-t", dest="obs_type",
                        choices=["action", "discovery", "decision", "bugfix", "feature", "refactor"],
                        help="Filter by observation type")
    args = parser.parse_args()

    search(args.query, args.project, args.limit, args.obs_type)


if __name__ == "__main__":
    main()
