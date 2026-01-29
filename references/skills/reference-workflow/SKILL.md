---
name: reference-workflow
description: This skill should be used when the user asks about "citing papers", "adding references", "Zotero", "bibliography", "academic citations", "manage references", or when working with citation formats, paper lookups, or reference synchronization.
---

# Reference Workflow

This skill provides knowledge about managing academic references using Zotero integration.

## Citation Format

When citing papers in chapters or documentation, use this format:

```
Author (Year) [ref:ZOTEROKEY]
```

Examples:
- Single author: `Harvey (2016) [ref:TVE8UM2C] showed that...`
- Multiple authors: `Gu et al. (2020) [ref:ABCD1234] demonstrated...`
- Parenthetical: `...requires validation (Harvey, 2016) [ref:TVE8UM2C]`

The 8-character Zotero key (uppercase letters + numbers) makes references:
- Grepable: `grep -oE '\[ref:[A-Z0-9]{8}\]'`
- Linkable to Zotero library
- Stable across renames

## Adding New References

1. **Add to Zotero**: Import paper via DOI, arXiv, or manual entry
2. **Attach PDF**: Ensure PDF is attached to Zotero item
3. **Run sync**: `/ref-sync` to parse PDF and generate summary
4. **Cite**: Use `[ref:KEY]` format in chapters

## Available Commands

- `/ref-status` - Check sync status between Zotero and local files
- `/ref-sync` - Parse new PDFs, generate summaries, update database
- `/ref-search <query>` - Search references by keyword

## Finding a Reference

To find a paper for citation:

1. **By topic**: `/ref-search "asset embeddings"`
2. **By author**: `/ref-search "Harvey"`
3. **By key** (if known): Read `$REFS_DIR/papers/KEYHERE/summary.json`

## Reference Directory Structure

```
$REFS_DIR/
├── papers/
│   ├── KMJZ2VFD/
│   │   ├── paper.pdf       # Original PDF
│   │   ├── paper.md        # Parsed markdown
│   │   └── summary.json    # AI summary
│   └── ...
├── papers_index.json       # Zotero sync index
└── ml4t_refs.db           # SQLite database
```

## Configuration

Projects using this plugin need `.env` with:
```bash
REFS_DIR=/path/to/references
ZOTERO_LIBRARY_ID=3  # Your Zotero group/library ID
```

See [citation-format.md](citation-format.md) for detailed citation guidelines.
