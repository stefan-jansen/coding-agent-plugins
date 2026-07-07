"""
Zotero database queries.

Reads from the local Zotero SQLite database to get library items.
"""

import sqlite3
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .config import Config


def get_zotero_items(config: "Config") -> dict:
    """
    Get all items from Zotero library.

    Returns dict mapping Zotero key → {title, date_added}
    """
    if not config.zotero_db.exists():
        print(f"Zotero database not found: {config.zotero_db}")
        return {}

    conn = sqlite3.connect(f"file:{config.zotero_db}?mode=ro", uri=True)
    cursor = conn.cursor()

    # Get items with their titles
    # Exclude attachments (itemTypeID=3) and notes (itemTypeID=28)
    cursor.execute("""
        SELECT DISTINCT i.key, idv.value as title, i.dateAdded
        FROM items i
        LEFT JOIN itemData id ON i.itemID = id.itemID
        LEFT JOIN itemDataValues idv ON id.valueID = idv.valueID
        LEFT JOIN fields f ON id.fieldID = f.fieldID
        WHERE i.libraryID = ?
        AND i.itemTypeID NOT IN (3, 28)
        AND i.itemID NOT IN (SELECT itemID FROM deletedItems)
        AND f.fieldName = 'title'
    """, (config.zotero_library_id,))

    items = {}
    for key, title, date_added in cursor.fetchall():
        items[key] = {
            'title': title,
            'date_added': date_added
        }

    conn.close()
    return items


def get_items_with_pdfs(config: "Config") -> list[dict]:
    """
    Get Zotero items that have PDF attachments.

    Returns list of {key, title, attach_key, pdf_path}
    """
    if not config.zotero_db.exists():
        return []

    conn = sqlite3.connect(f"file:{config.zotero_db}?mode=ro", uri=True)
    cursor = conn.cursor()

    # Get items WITH PDF attachments
    cursor.execute('''
        SELECT DISTINCT parent.key, idv.value as title, attach.key as attach_key
        FROM items parent
        JOIN itemAttachments ia ON parent.itemID = ia.parentItemID
        JOIN items attach ON ia.itemID = attach.itemID
        LEFT JOIN itemData id ON parent.itemID = id.itemID
        LEFT JOIN itemDataValues idv ON id.valueID = idv.valueID
        LEFT JOIN fields f ON id.fieldID = f.fieldID
        WHERE parent.libraryID = ?
        AND parent.itemTypeID NOT IN (3, 28)
        AND parent.itemID NOT IN (SELECT itemID FROM deletedItems)
        AND ia.contentType = 'application/pdf'
        AND f.fieldName = 'title'
    ''', (config.zotero_library_id,))

    results = []
    for key, title, attach_key in cursor.fetchall():
        # Find actual PDF path
        pdf_dir = config.zotero_storage / attach_key
        if pdf_dir.exists():
            pdfs = list(pdf_dir.glob('*.pdf'))
            if pdfs:
                results.append({
                    'key': key,
                    'title': title,
                    'attach_key': attach_key,
                    'pdf_path': pdfs[0]
                })

    conn.close()

    # Deduplicate by key
    seen = set()
    deduped = []
    for item in results:
        if item['key'] not in seen:
            seen.add(item['key'])
            deduped.append(item)

    return deduped


def get_parsed_refs(config: "Config") -> set:
    """Get keys that have markdown files in papers directory."""
    parsed = set()

    if not config.papers_dir.exists():
        return parsed

    for paper_dir in config.papers_dir.iterdir():
        if paper_dir.is_dir():
            # Check for any markdown file (parsed content)
            md_files = list(paper_dir.glob("*.md"))
            if md_files:
                parsed.add(paper_dir.name)

    return parsed


def get_summarized_refs(config: "Config") -> set:
    """Get keys that have summary.json files."""
    summarized = set()

    if not config.papers_dir.exists():
        return summarized

    for summary_file in config.papers_dir.glob("*/summary.json"):
        summarized.add(summary_file.parent.name)

    return summarized
