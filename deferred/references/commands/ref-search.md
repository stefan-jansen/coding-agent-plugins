---
description: Search references by keyword or semantic similarity
allowed-tools: [Bash, Read]
argument-hint: "<query> [--chapter N] [--limit N] [--full]"
---

# Reference Search

Search the local reference database by keyword, title, author, or content.

**Query**: $ARGUMENTS

## Configuration

Required:
- `REFS_DIR` - Directory containing papers/ and ml4t_refs.db

## Process

1. **Parse Arguments**
   - `<query>`: Search terms (required)
   - `--chapter N`: Filter by chapter relevance
   - `--limit N`: Maximum results (default: 10)
   - `--full`: Show full summary instead of snippet

2. **Load Configuration**
   ```bash
   if [ -f .env ]; then source .env; fi
   ```

3. **Run Search**
   ```bash
   python ~/agents/plugins/references/lib/cli.py search "$ARGUMENTS"
   ```

4. **Display Results**
   For each matching paper:
   - Zotero key (for citation: `[ref:KEY]`)
   - Title
   - Authors, Year
   - Citation count (if available)
   - Summary snippet or full summary

## Examples

```bash
# Search by topic
/ref-search "asset embeddings"

# Search and filter by chapter
/ref-search "momentum factor" --chapter 9

# Get more results
/ref-search "machine learning trading" --limit 20

# Show full summaries
/ref-search "attention mechanism" --full
```

## Output Format

```
=== Search Results for "asset embeddings" ===

[1] KMJZ2VFD - Asset Embeddings (2024)
    Authors: Some Author et al.
    Citations: 45
    Summary: Introduces a method for learning vector representations
             of financial assets using return correlations...

[2] ABCD1234 - Related Paper Title (2023)
    ...

Found 2 results. Use [ref:KEY] format for citations.
```

## Citation Format

When citing papers in chapters, use:
```
Author (Year) [ref:ZOTEROKEY]
```

Example: "As shown by Smith (2024) [ref:KMJZ2VFD], asset embeddings..."
