"""
PDF parsing using Marker.

Converts PDFs to markdown for indexing and summarization.
"""

import shutil
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .config import Config


def get_missing_pdfs(config: "Config") -> list[dict]:
    """Find Zotero items with PDFs that haven't been parsed yet."""
    try:
        from .zotero import get_items_with_pdfs
    except ImportError:
        from zotero import get_items_with_pdfs

    items_with_pdfs = get_items_with_pdfs(config)
    existing_dirs = set()

    if config.papers_dir.exists():
        existing_dirs = {d.name for d in config.papers_dir.iterdir() if d.is_dir()}

    missing = []
    for item in items_with_pdfs:
        key = item['key']
        # Skip if already parsed
        if key in existing_dirs:
            continue
        # Skip known large books
        if key in config.skip_keys:
            continue
        missing.append(item)

    return missing


def parse_pdf(config: "Config", key: str, pdf_path: Path) -> bool:
    """
    Parse a single PDF using Marker.

    Args:
        config: Plugin configuration
        key: Zotero key for the paper
        pdf_path: Path to the PDF file

    Returns:
        True if successful, False otherwise
    """
    output_dir = config.papers_dir / key
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "parsed.md"

    # Skip if already parsed
    if output_file.exists():
        return True

    # Check Marker binary exists
    if not config.marker_bin.exists():
        print(f"Marker binary not found: {config.marker_bin}")
        print("Install Marker: pip install marker-pdf")
        return False

    try:
        result = subprocess.run(
            [str(config.marker_bin), str(pdf_path), '--output_dir', str(output_dir)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        # Marker creates a subdirectory - find the md file recursively
        md_files = list(output_dir.rglob('*.md'))
        if md_files:
            # Copy to parsed.md at top level
            shutil.copy(md_files[0], output_file)
            return True
        else:
            return False

    except subprocess.TimeoutExpired:
        print(f"Timeout parsing {key}")
        return False
    except Exception as e:
        print(f"Error parsing {key}: {e}")
        return False


def parse_new(
    config: "Config",
    dry_run: bool = False,
    limit: int = 0,
    key: str = None
) -> dict:
    """
    Parse all missing PDFs.

    Args:
        config: Plugin configuration
        dry_run: If True, only show what would be done
        limit: Maximum number to process (0 = unlimited)
        key: If specified, only parse this specific key

    Returns:
        dict with success count, failed count, and errors
    """
    results = {"success": 0, "failed": 0, "errors": []}

    # Get missing PDFs
    missing = get_missing_pdfs(config)

    # Filter to specific key if requested
    if key:
        missing = [m for m in missing if m['key'] == key]
        if not missing:
            # Check if already parsed
            paper_dir = config.papers_dir / key
            if paper_dir.exists() and list(paper_dir.glob("*.md")):
                print(f"{key} is already parsed")
                return results
            else:
                results["errors"].append(f"Key {key} not found in Zotero library with PDF")
                return results

    print(f"Found {len(missing)} PDFs to parse")

    if dry_run:
        for p in missing[:30]:
            print(f"  {p['key']}: {p['title'][:60]}")
        if len(missing) > 30:
            print(f"  ... and {len(missing) - 30} more")
        return results

    # Process
    to_process = missing[:limit] if limit else missing

    for i, p in enumerate(to_process, 1):
        k = p['key']
        print(f"[{i}/{len(to_process)}] {k}: {p['title'][:50]}...", end=" ", flush=True)

        if parse_pdf(config, k, p['pdf_path']):
            print("done")
            results["success"] += 1
        else:
            print("failed")
            results["failed"] += 1
            results["errors"].append(f"Failed to parse {k}")

    return results
