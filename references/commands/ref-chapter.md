---
description: Get most relevant papers for a chapter
allowed-tools: [Bash, Read]
argument-hint: "<chapter-number> [--primary] [--full]"
---

# Chapter References

Get papers most relevant to a specific chapter, sorted by relevance score.

**Chapter**: $ARGUMENTS

## Configuration

Required:
- `REFS_DIR` - Directory containing ml4t_refs.db

## Process

1. **Run Chapter Query**
   ```bash
   python3 ~/agents/plugins/references/lib/cli.py chapter $ARGUMENTS
   ```

2. **Display Results**
   Shows papers with:
   - ★ for primary references
   - Relevance score (1-5, or 100 for top)
   - Zotero key for citations

## Options

- `--primary`: Show only primary references (★)
- `--full`: Include summary TLDRs
- `--limit N`: Maximum results (default: 30)

## Examples

```bash
# All papers for Chapter 5
/ref-chapter 5

# Only primary references
/ref-chapter 5 --primary

# With summaries
/ref-chapter 9 --primary --full
```

## Citation Format

Use the Zotero key from results:
```
Author (Year) [ref:ZOTEROKEY]
```

Example: "Ball and Brown (1968) [ref:38R6RWI8] established..."
