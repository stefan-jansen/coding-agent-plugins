---
description: Show reference sync status between Zotero and local papers
allowed-tools: [Bash, Read]
---

# Reference Status

Show the current synchronization status between Zotero library and local reference files.

## Configuration

Load configuration from project `.env` file or environment variables:
- `REFS_DIR` - Directory containing papers/ and databases (required)
- `ZOTERO_LIBRARY_ID` - Zotero group library ID (required)
- `ZOTERO_DB` - Path to Zotero SQLite database (default: ~/.zotero/zotero/*/zotero.sqlite)

## Process

1. **Load Configuration**
   ```bash
   # Load from project .env if exists
   if [ -f .env ]; then source .env; fi
   ```

2. **Run Status Script**
   ```bash
   python ~/agents/plugins/references/lib/cli.py status
   ```

3. **Display Results**
   Show counts for:
   - Total Zotero items with PDF attachments
   - Papers with parsed markdown
   - Papers with AI summaries
   - Papers indexed in database

4. **Action Items**
   List papers needing attention:
   - NOT PARSED: Have PDF but no markdown
   - NO SUMMARY: Have markdown but no summary.json
   - NOT INDEXED: Not in SQLite database

## Example Output

```
=== Reference Status ===
Zotero Items (Library 3): 245
  With PDF attachments: 198

Local Papers: 195
  Parsed (markdown): 192
  Summarized: 190
  In database: 192

Action Items:
  NOT PARSED: 6 papers
  NO SUMMARY: 2 papers

Run /ref-sync to process pending items.
```
