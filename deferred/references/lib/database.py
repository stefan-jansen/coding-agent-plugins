"""
SQLite database operations for reference indexing.

Maintains a searchable index of all papers with metadata and summaries.
"""

import json
import re
import sqlite3
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .config import Config


def create_schema(conn: sqlite3.Connection):
    """Create the database schema."""
    cursor = conn.cursor()

    # Drop old tables if rebuilding
    cursor.execute("DROP TABLE IF EXISTS citation_lookups")
    cursor.execute("DROP TABLE IF EXISTS chapter_relevance")
    cursor.execute("DROP TABLE IF EXISTS summaries")
    cursor.execute("DROP TABLE IF EXISTS papers")

    # Papers table - core reference data
    cursor.execute("""
        CREATE TABLE papers (
            zotero_key TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            first_author TEXT,
            year INTEGER,
            doi TEXT,
            arxiv_id TEXT,
            s2_paper_id TEXT,
            citation_count INTEGER,
            citation_updated_at TIMESTAMP,
            has_markdown BOOLEAN DEFAULT FALSE,
            has_summary BOOLEAN DEFAULT FALSE,
            item_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Chapter relevance - which chapters cite which papers
    cursor.execute("""
        CREATE TABLE chapter_relevance (
            zotero_key TEXT,
            chapter INTEGER,
            relevance_score REAL DEFAULT 0,
            is_primary BOOLEAN DEFAULT FALSE,
            notes TEXT,
            PRIMARY KEY (zotero_key, chapter),
            FOREIGN KEY (zotero_key) REFERENCES papers(zotero_key)
        )
    """)

    # Citation lookups - track API call history
    cursor.execute("""
        CREATE TABLE citation_lookups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zotero_key TEXT,
            lookup_method TEXT,
            lookup_value TEXT,
            success BOOLEAN,
            s2_paper_id TEXT,
            citation_count INTEGER,
            error_message TEXT,
            looked_up_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (zotero_key) REFERENCES papers(zotero_key)
        )
    """)

    # Summaries - AI-generated summaries
    cursor.execute("""
        CREATE TABLE summaries (
            zotero_key TEXT PRIMARY KEY,
            summary_text TEXT,
            key_concepts TEXT,
            quotables TEXT,
            methodology TEXT,
            main_findings TEXT,
            relevance_notes TEXT,
            model_used TEXT,
            generated_at TIMESTAMP,
            FOREIGN KEY (zotero_key) REFERENCES papers(zotero_key)
        )
    """)

    # Create FTS table for full-text search
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS papers_fts USING fts5(
            zotero_key,
            title,
            first_author,
            summary_text,
            content='papers'
        )
    """)

    # Indexes
    cursor.execute("CREATE INDEX idx_papers_citations ON papers(citation_count DESC)")
    cursor.execute("CREATE INDEX idx_papers_year ON papers(year)")
    cursor.execute("CREATE INDEX idx_chapter_rel ON chapter_relevance(chapter)")

    conn.commit()


def extract_identifiers(md_path: Path) -> tuple[Optional[str], Optional[str]]:
    """Extract DOI and arXiv ID from markdown file."""
    try:
        content = md_path.read_text()[:5000]  # Just read first 5KB

        # Look for DOI in content
        doi_match = re.search(r'10\.\d{4,}/[^\s\]]+', content)
        doi = doi_match.group(0).rstrip('.,;)') if doi_match else None

        # Look for arXiv ID
        arxiv_match = re.search(r'arxiv[:/]?\s*(\d{4}\.\d{4,5})', content, re.I)
        arxiv_id = arxiv_match.group(1) if arxiv_match else None

        return doi, arxiv_id
    except Exception:
        return None, None


def load_papers_from_index(config: "Config", conn: sqlite3.Connection):
    """Load papers from papers_index.json into database."""
    if not config.papers_index.exists():
        print(f"Papers index not found: {config.papers_index}")
        return 0

    with open(config.papers_index) as f:
        index = json.load(f)

    cursor = conn.cursor()
    count = 0

    for zotero_key, info in index.items():
        # Check if markdown file exists
        md_path = config.papers_dir / zotero_key / "parsed.md"
        has_markdown = md_path.exists()

        # Check for summary
        has_summary = (config.papers_dir / zotero_key / "summary.json").exists()

        # Extract DOI from markdown frontmatter if available
        doi = None
        arxiv_id = None
        if has_markdown:
            doi, arxiv_id = extract_identifiers(md_path)

        # Handle authors that might be a list
        authors = info.get('authors', 'Unknown')
        if isinstance(authors, list):
            authors = ', '.join(authors)

        cursor.execute("""
            INSERT OR REPLACE INTO papers
            (zotero_key, title, first_author, year, doi, arxiv_id,
             has_markdown, has_summary, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            zotero_key,
            info.get('title', 'Unknown'),
            authors,
            info.get('year'),
            doi,
            arxiv_id,
            has_markdown,
            has_summary
        ))
        count += 1

    conn.commit()
    print(f"Loaded {count} papers from index")
    return count


def load_papers_from_directory(config: "Config", conn: sqlite3.Connection):
    """Load papers from papers directory that aren't in the index."""
    if not config.papers_dir.exists():
        return 0

    cursor = conn.cursor()

    # Get existing keys
    cursor.execute("SELECT zotero_key FROM papers")
    existing_keys = {row[0] for row in cursor.fetchall()}

    count = 0
    for paper_dir in config.papers_dir.iterdir():
        if not paper_dir.is_dir():
            continue

        zotero_key = paper_dir.name
        if zotero_key in existing_keys:
            continue

        # Check for summary.json to get metadata
        summary_path = paper_dir / "summary.json"
        title = 'Unknown'
        authors = 'Unknown'
        year = None

        if summary_path.exists():
            try:
                summary = json.loads(summary_path.read_text())

                # Handle nested metadata structure (new format)
                if 'metadata' in summary:
                    meta = summary['metadata']
                    title = meta.get('title', 'Unknown')
                    authors = meta.get('authors', 'Unknown')
                    year = meta.get('year')
                else:
                    # Old flat format
                    title = summary.get('title', 'Unknown')
                    authors = summary.get('authors', 'Unknown')
                    year = summary.get('year')

                if isinstance(authors, list):
                    authors = ', '.join(authors)
            except Exception:
                pass

        # Check for markdown
        md_files = list(paper_dir.glob("*.md"))
        has_markdown = len(md_files) > 0
        has_summary = summary_path.exists()

        # Extract identifiers
        doi = None
        arxiv_id = None
        if has_markdown:
            doi, arxiv_id = extract_identifiers(md_files[0])

        cursor.execute("""
            INSERT OR REPLACE INTO papers
            (zotero_key, title, first_author, year, doi, arxiv_id,
             has_markdown, has_summary, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            zotero_key,
            title,
            authors,
            year,
            doi,
            arxiv_id,
            has_markdown,
            has_summary
        ))
        count += 1

    conn.commit()
    if count > 0:
        print(f"Loaded {count} additional papers from directory")
    return count


def load_chapter_relevance_from_zotero(config: "Config", conn: sqlite3.Connection):
    """
    Load chapter assignments from Zotero collections.

    Collections named 'NN_*' (e.g., '15_causal_inference') are treated as
    chapter assignments. These are PRIMARY (manual) assignments that take
    precedence over AI-generated assignments.
    """
    import sqlite3 as sqlite

    if not config.zotero_db.exists():
        print(f"Zotero database not found: {config.zotero_db}")
        return 0

    cursor = conn.cursor()
    count = 0

    # Connect to Zotero (read-only)
    zotero_conn = sqlite.connect(f'file:{config.zotero_db}?mode=ro', uri=True)
    zotero_cursor = zotero_conn.cursor()

    # Find chapter collections (NN_* pattern)
    zotero_cursor.execute('''
        SELECT collectionID, collectionName
        FROM collections
        WHERE libraryID = ?
        AND collectionName GLOB '[0-9][0-9]_*'
    ''', (config.zotero_library_id,))

    for coll_id, coll_name in zotero_cursor.fetchall():
        # Extract chapter number from name (e.g., "15_causal_inference" → 15)
        try:
            chapter = int(coll_name[:2])
        except ValueError:
            continue

        # Get items in this collection
        zotero_cursor.execute('''
            SELECT i.key
            FROM collectionItems ci
            JOIN items i ON ci.itemID = i.itemID
            WHERE ci.collectionID = ?
            AND i.libraryID = ?
        ''', (coll_id, config.zotero_library_id))

        for (zotero_key,) in zotero_cursor.fetchall():
            # Insert as primary (Zotero = manual = ground truth)
            # Use INSERT OR IGNORE to not overwrite existing entries
            # (AI assignments loaded first, Zotero overwrites with UPDATE)
            cursor.execute('''
                INSERT INTO chapter_relevance
                (zotero_key, chapter, relevance_score, is_primary, notes)
                VALUES (?, ?, 100, 1, 'Zotero collection')
                ON CONFLICT(zotero_key, chapter) DO UPDATE SET
                    relevance_score = 100,
                    is_primary = 1,
                    notes = 'Zotero collection (manual)'
            ''', (zotero_key, chapter))
            count += 1

    zotero_conn.close()
    conn.commit()
    print(f"Loaded {count} chapter assignments from Zotero collections")
    return count


def load_chapter_relevance(config: "Config", conn: sqlite3.Connection):
    """Extract chapter_relevance from summary.json files and populate table."""
    if not config.papers_dir.exists():
        return 0

    cursor = conn.cursor()
    count = 0

    for paper_dir in config.papers_dir.iterdir():
        if not paper_dir.is_dir():
            continue

        summary_path = paper_dir / "summary.json"
        if not summary_path.exists():
            continue

        try:
            summary = json.loads(summary_path.read_text())
            ch_rel = summary.get("chapter_relevance", {})

            if not ch_rel:
                continue

            zotero_key = paper_dir.name
            primary = ch_rel.get("primary")
            secondary = ch_rel.get("secondary", [])
            fit_explanation = ch_rel.get("fit_explanation", "")

            # Insert primary chapter (relevance=100, is_primary=True)
            if primary:
                cursor.execute("""
                    INSERT OR REPLACE INTO chapter_relevance
                    (zotero_key, chapter, relevance_score, is_primary, notes)
                    VALUES (?, ?, 100, 1, ?)
                """, (zotero_key, primary, fit_explanation))
                count += 1

            # Insert secondary chapters (relevance=5, is_primary=False)
            for ch in secondary:
                cursor.execute("""
                    INSERT OR REPLACE INTO chapter_relevance
                    (zotero_key, chapter, relevance_score, is_primary, notes)
                    VALUES (?, ?, 5, 0, ?)
                """, (zotero_key, ch, fit_explanation))
                count += 1

        except Exception as e:
            print(f"Warning: Could not process {paper_dir.name}: {e}")
            continue

    conn.commit()
    print(f"Loaded {count} chapter relevance entries from summaries")
    return count


def rebuild_db(config: "Config"):
    """Rebuild the SQLite database from scratch."""
    print(f"Rebuilding database at {config.db_path}")

    conn = sqlite3.connect(config.db_path)

    print("Creating schema...")
    create_schema(conn)

    print("Loading papers from index...")
    load_papers_from_index(config, conn)

    print("Scanning papers directory for additional entries...")
    load_papers_from_directory(config, conn)

    print("Extracting chapter relevance from summaries (AI)...")
    load_chapter_relevance(config, conn)

    print("Loading chapter assignments from Zotero collections (manual, overrides AI)...")
    load_chapter_relevance_from_zotero(config, conn)

    conn.close()
    print("Database rebuild complete")


def get_db_refs(config: "Config") -> set:
    """Get keys that exist in the reference database."""
    db_refs = set()

    if not config.db_path.exists():
        return db_refs

    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT zotero_key FROM papers")
        db_refs = {row[0] for row in cursor.fetchall()}
    except sqlite3.OperationalError:
        # Table might not exist
        pass

    conn.close()
    return db_refs


def search_papers(
    config: "Config",
    query: str,
    chapter: Optional[int] = None,
    limit: int = 10
) -> list[dict]:
    """
    Search papers by keyword.

    Args:
        config: Plugin configuration
        query: Search query
        chapter: Optional chapter filter
        limit: Maximum results

    Returns:
        List of matching papers
    """
    if not config.db_path.exists():
        print(f"Database not found: {config.db_path}")
        return []

    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    # Simple LIKE search (FTS could be added later)
    search_term = f"%{query}%"

    if chapter:
        cursor.execute("""
            SELECT p.zotero_key, p.title, p.first_author, p.year, p.citation_count
            FROM papers p
            JOIN chapter_relevance cr ON p.zotero_key = cr.zotero_key
            WHERE cr.chapter = ?
            AND (p.title LIKE ? OR p.first_author LIKE ?)
            ORDER BY p.citation_count DESC NULLS LAST
            LIMIT ?
        """, (chapter, search_term, search_term, limit))
    else:
        cursor.execute("""
            SELECT zotero_key, title, first_author, year, citation_count
            FROM papers
            WHERE title LIKE ? OR first_author LIKE ?
            ORDER BY citation_count DESC NULLS LAST
            LIMIT ?
        """, (search_term, search_term, limit))

    results = []
    for row in cursor.fetchall():
        results.append({
            'key': row[0],
            'title': row[1],
            'author': row[2],
            'year': row[3],
            'citations': row[4]
        })

    conn.close()
    return results


def get_chapter_papers(
    config: "Config",
    chapter: int,
    primary_only: bool = False,
    limit: int = 50
) -> list[dict]:
    """
    Get papers most relevant to a chapter.

    Args:
        config: Plugin configuration
        chapter: Chapter number
        primary_only: Only return primary references
        limit: Maximum results

    Returns:
        List of papers sorted by relevance
    """
    if not config.db_path.exists():
        return []

    conn = sqlite3.connect(config.db_path)
    cursor = conn.cursor()

    query = """
        SELECT cr.is_primary, cr.relevance_score, p.zotero_key, p.title,
               p.first_author, p.year, p.has_summary
        FROM chapter_relevance cr
        JOIN papers p ON cr.zotero_key = p.zotero_key
        WHERE cr.chapter = ?
    """
    params = [chapter]

    if primary_only:
        query += " AND cr.is_primary = 1"

    query += " ORDER BY cr.is_primary DESC, cr.relevance_score DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)

    results = []
    for row in cursor.fetchall():
        results.append({
            'is_primary': bool(row[0]),
            'relevance': row[1],
            'key': row[2],
            'title': row[3],
            'author': row[4],
            'year': row[5],
            'has_summary': bool(row[6])
        })

    conn.close()
    return results


def get_paper(config: "Config", key: str) -> Optional[dict]:
    """Get a single paper by Zotero key."""
    # First try database
    if config.db_path.exists():
        conn = sqlite3.connect(config.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT zotero_key, title, first_author, year, citation_count,
                   has_markdown, has_summary
            FROM papers WHERE zotero_key = ?
        """, (key,))
        row = cursor.fetchone()
        conn.close()

        if row:
            paper = {
                'key': row[0],
                'title': row[1],
                'author': row[2],
                'year': row[3],
                'citations': row[4],
                'has_markdown': row[5],
                'has_summary': row[6]
            }

            # Load summary if available
            summary_path = config.papers_dir / key / "summary.json"
            if summary_path.exists():
                paper['summary'] = json.loads(summary_path.read_text())

            return paper

    # Fall back to direct file access
    paper_dir = config.papers_dir / key
    if paper_dir.exists():
        paper = {'key': key}

        summary_path = paper_dir / "summary.json"
        if summary_path.exists():
            summary = json.loads(summary_path.read_text())
            paper['title'] = summary.get('title', 'Unknown')
            paper['author'] = summary.get('authors', 'Unknown')
            paper['year'] = summary.get('year')
            paper['summary'] = summary

        return paper

    return None
