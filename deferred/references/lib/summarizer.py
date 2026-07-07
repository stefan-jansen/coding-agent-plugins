"""
AI summarization using Gemini.

Generates structured summaries of parsed papers.
"""

import json
import re
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .config import Config


def find_missing_summaries(config: "Config") -> list[dict]:
    """Find paper directories that have parsed content but no summary.json."""
    missing = []

    if not config.papers_dir.exists():
        return missing

    for paper_dir in config.papers_dir.iterdir():
        if not paper_dir.is_dir():
            continue

        # Skip if summary already exists
        if (paper_dir / "summary.json").exists():
            continue

        # Check for parsed content (multiple possible formats)
        content_file = None
        if (paper_dir / "parsed.md").exists():
            content_file = paper_dir / "parsed.md"
        elif (paper_dir / "extraction.md").exists():
            content_file = paper_dir / "extraction.md"
        elif (paper_dir / "paper.json").exists():
            content_file = paper_dir / "paper.json"

        if content_file:
            missing.append({
                'key': paper_dir.name,
                'dir': paper_dir,
                'content_file': content_file
            })

    return missing


def extract_text(content_file: Path) -> str:
    """Extract text from parsed content file."""
    if content_file.suffix == '.md':
        text = content_file.read_text()
        # Remove reference section if present
        for marker in ['## References', '# References', '## Bibliography', '# Bibliography']:
            if marker in text:
                text = text[:text.index(marker)]
        return text.strip()

    elif content_file.suffix == '.json':
        # Extract from marker JSON format
        data = json.loads(content_file.read_text())
        texts = []

        def walk(node):
            if isinstance(node, dict):
                if 'html' in node and node.get('block_type') in ['Text', 'SectionHeader', 'ListItem']:
                    text = re.sub(r'<[^>]+>', '', node['html']).strip()
                    if text:
                        texts.append(text)
                for key, value in node.items():
                    if key in ['children', 'blocks']:
                        walk(value)
            elif isinstance(node, list):
                for item in node:
                    walk(item)

        walk(data)
        return '\n\n'.join(texts)

    return ""


def get_default_prompt() -> str:
    """Return default summarization prompt."""
    return """You are an expert academic researcher summarizing papers for a machine learning textbook.

Generate a JSON summary with these fields:
{
    "title": "Paper title",
    "authors": "Author list",
    "year": "Publication year",
    "abstract": "Brief abstract (2-3 sentences)",
    "key_contributions": ["contribution 1", "contribution 2", ...],
    "methodology": "Brief description of methodology",
    "main_findings": ["finding 1", "finding 2", ...],
    "relevance": "Why this paper is relevant to ML for trading",
    "quotables": ["Notable quote 1", "Notable quote 2"]
}

Focus on aspects relevant to quantitative finance and algorithmic trading.
Be concise but comprehensive."""


def summarize_paper(
    text: str,
    prompt: str,
    api_key: str
) -> Optional[dict]:
    """
    Generate summary using Gemini.

    Args:
        text: Paper text content
        prompt: Summarization prompt
        api_key: Google API key

    Returns:
        Parsed JSON summary or None on failure
    """
    try:
        import google.generativeai as genai
        from json_repair import repair_json
    except ImportError:
        print("Required packages not installed: pip install google-generativeai json-repair")
        return None

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(
        'gemini-2.5-flash',
        generation_config={
            'max_output_tokens': 8000,
            'temperature': 0.2,
            'response_mime_type': 'application/json'
        }
    )

    full_prompt = f"{prompt}\n\n---\n\nPlease summarize this paper:\n\n{text}"

    try:
        response = model.generate_content(full_prompt)
        content = response.text

        # Try parsing JSON
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Try repair
            repaired = repair_json(content)
            return json.loads(repaired)

    except Exception as e:
        print(f"Summarization error: {e}")
        return None


def summarize_missing(
    config: "Config",
    dry_run: bool = False,
    limit: int = 0,
    key: str = None
) -> dict:
    """
    Generate summaries for all papers missing them.

    Args:
        config: Plugin configuration
        dry_run: If True, only show what would be done
        limit: Maximum number to process (0 = unlimited)
        key: If specified, only summarize this specific key

    Returns:
        dict with success count, failed count, and errors
    """
    results = {"success": 0, "failed": 0, "errors": []}

    if not config.google_api_key:
        results["errors"].append("GOOGLE_API_KEY not configured")
        print("Warning: GOOGLE_API_KEY not set, skipping summarization")
        return results

    # Find missing summaries
    missing = find_missing_summaries(config)

    # Filter to specific key if requested
    if key:
        missing = [m for m in missing if m['key'] == key]
        if not missing:
            # Check if already summarized
            summary_file = config.papers_dir / key / "summary.json"
            if summary_file.exists():
                print(f"{key} already has summary")
                return results
            else:
                results["errors"].append(f"Key {key} not found or not parsed")
                return results

    print(f"Found {len(missing)} papers needing summaries")

    if dry_run:
        for p in missing[:20]:
            print(f"  {p['key']}: {p['content_file'].name}")
        if len(missing) > 20:
            print(f"  ... and {len(missing) - 20} more")
        return results

    # Load prompt
    prompt_file = config.prompts_dir / "single_pass_summary_v4.md"
    if prompt_file.exists():
        prompt = prompt_file.read_text()
    else:
        prompt = get_default_prompt()

    # Process
    to_process = missing[:limit] if limit else missing

    for i, p in enumerate(to_process, 1):
        k = p['key']
        print(f"[{i}/{len(to_process)}] {k}: ", end="", flush=True)

        try:
            text = extract_text(p['content_file'])

            if len(text) < 500:
                print(f"too short ({len(text)} chars), skipping")
                continue

            print(f"summarizing ({len(text):,} chars)...", end=" ", flush=True)

            summary = summarize_paper(text, prompt, config.google_api_key)

            if summary:
                output_file = p['dir'] / "summary.json"
                with open(output_file, 'w') as f:
                    json.dump(summary, f, indent=2)
                print("done")
                results["success"] += 1
            else:
                print("failed to parse response")
                results["failed"] += 1
                results["errors"].append(f"Failed to summarize {k}")

        except Exception as e:
            print(f"ERROR: {e}")
            results["failed"] += 1
            results["errors"].append(f"Error summarizing {k}: {e}")

    return results
