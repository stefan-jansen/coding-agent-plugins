---
description: Sync references - parse new PDFs, generate summaries, rebuild database
allowed-tools: [Bash, Read, Write]
argument-hint: "[--dry-run] [--limit N] [--key ZOTERO_KEY]"
---

# Reference Sync

Synchronize references by parsing new PDFs, generating AI summaries, and rebuilding the database.

**Arguments**: $ARGUMENTS

## Configuration

Required environment variables (from `.env` or environment):
- `REFS_DIR` - Directory containing papers/ and databases
- `ZOTERO_LIBRARY_ID` - Zotero group library ID
- `GOOGLE_API_KEY` - For Gemini summarization (optional if summaries exist)
- `MARKER_BIN` - Path to Marker binary (default: ~/.local/share/marker/bin/marker_single)

## Process

1. **Parse Arguments**
   - `--dry-run`: Show what would be done without executing
   - `--limit N`: Process at most N items per stage
   - `--key ZOTERO_KEY`: Process only specified paper (e.g., KMJZ2VFD)

2. **Load Configuration**
   ```bash
   if [ -f .env ]; then source .env; fi
   ```

3. **Run Sync Workflow**
   ```bash
   python ~/agents/plugins/references/lib/cli.py sync $ARGUMENTS
   ```

   The sync workflow:
   1. **Parse PDFs**: Convert new PDFs to markdown using Marker
   2. **Generate Summaries**: Create AI summaries using Gemini
   3. **Rebuild Database**: Update SQLite index with new entries

4. **Report Results**
   Show counts of processed items and any errors.

## Examples

```bash
# Full sync
/ref-sync

# Dry run to see what would be processed
/ref-sync --dry-run

# Process only 5 papers
/ref-sync --limit 5

# Process specific paper
/ref-sync --key KMJZ2VFD
```

## Error Handling

- If `GOOGLE_API_KEY` not set, skip summarization with warning
- If Marker binary not found, report error with installation instructions
- Individual paper failures don't stop the batch - errors collected and reported at end
