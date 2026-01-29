# References Plugin

Academic reference management with Zotero integration for Claude Code.

## Features

- **Sync references** from Zotero library to local storage
- **Parse PDFs** to markdown using Marker
- **Generate AI summaries** using Gemini
- **Search references** by keyword
- **Citation format** support with Zotero keys

## Installation

Add to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "local": {
      "source": {
        "source": "directory",
        "path": "/home/stefan/agents/plugins"
      }
    }
  },
  "enabledPlugins": {
    "references@local": true
  }
}
```

## Configuration

Create a `.env` file in your project root:

```bash
# Required
REFS_DIR=/path/to/references        # Where papers/ and *.db live
ZOTERO_LIBRARY_ID=3                 # Zotero group library ID

# Optional
ZOTERO_DB=~/.zotero/zotero.sqlite   # Zotero database path
MARKER_BIN=~/.local/share/marker/bin/marker_single
GOOGLE_API_KEY=...                  # For Gemini summarization
```

## Commands

### `/ref-status`

Show sync status between Zotero and local files.

```
=== Reference Status ===
Zotero Items (Library 3): 245
  Parsed (markdown): 192
  Summarized: 190

Action Items:
  NOT PARSED: 6 papers
  NO SUMMARY: 2 papers
```

### `/ref-sync [options]`

Sync references: parse PDFs, generate summaries, rebuild database.

Options:
- `--dry-run`: Preview without changes
- `--limit N`: Process at most N items
- `--key ZOTEROKEY`: Process specific paper

### `/ref-chapter <chapter> [options]`

Get papers most relevant to a chapter.

```bash
/ref-chapter 15 --primary      # Primary refs only
/ref-chapter 7 --primary --full  # With summaries
```

Options:
- `--primary`: Only show primary references (★)
- `--full`: Include TLDR summaries
- `--limit N`: Maximum results (default: 30)

### `/ref-search <query> [options]`

Search references by keyword.

Options:
- `--chapter N`: Filter by chapter relevance
- `--limit N`: Maximum results (default: 10)
- `--full`: Show complete summaries

## Citation Format

When citing papers, use:

```
Author (Year) [ref:ZOTEROKEY]
```

Examples:
- `Harvey (2016) [ref:TVE8UM2C] showed that...`
- `...requires validation (Harvey, 2016) [ref:TVE8UM2C]`

The 8-character Zotero key makes citations:
- Grepable: `grep -oE '\[ref:[A-Z0-9]{8}\]'`
- Linkable to Zotero library
- Stable across renames

## Chapter Relevance

Papers are assigned to chapters from two sources:

### 1. AI-Generated (automatic)

During summarization, Gemini assigns papers to chapters based on content:

```json
// summary.json
{
  "chapter_relevance": {
    "primary": 15,
    "secondary": [9, 7],
    "fit_explanation": "Core causal inference methodology"
  }
}
```

The prompt (`prompts/single_pass_summary_v4.md`) contains the chapter mapping.

### 2. Zotero Collections (manual, overrides AI)

Collections named `NN_*` are treated as chapter assignments:

```
Zotero Collections:
├── 07_alpha_factor_engineering (139 papers)
├── 15_causal_inference (61 papers)
└── ...
```

**To manually assign a paper to a chapter:**
1. In Zotero: drag paper to `NN_chapter_name` collection
2. Run `/ref-sync` or rebuild database
3. Paper appears as primary for that chapter

Manual Zotero assignments **override** AI assignments.

## Directory Structure

```
$REFS_DIR/
├── papers/
│   ├── KMJZ2VFD/
│   │   ├── paper.pdf       # Original PDF (from Zotero)
│   │   ├── parsed.md       # Marker output
│   │   └── summary.json    # AI summary
│   └── ...
├── papers_index.json       # Zotero sync index
├── prompts/                # Summarization prompts
└── ml4t_refs.db           # SQLite database
```

## Skills

### reference-workflow

Auto-discovered knowledge about citation format, adding references, and reference workflow. Triggers when you mention papers, citations, Zotero, or bibliographies.

### research-write (New)

**Research-driven chapter writing** - uses papers to SHAPE content rather than decorate pre-written claims.

**Triggers**: "research-driven draft", "write with research", "use papers to shape content"

**Workflow**:
1. **PULL**: Get chapter's assigned references via MCP
2. **FILTER**: Identify 3-7 papers relevant to specific section
3. **EXTRACT**: Get findings, actionable insights, key exhibits from papers
4. **SYNTHESIZE**: Find the narrative across papers
5. **WRITE**: Draft content shaped by extracted findings
6. **CITE**: Verify citations use `Author (Year) [ref:KEY]` format

**Example**:
```
"Write the momentum factors section for chapter 7 using research-write"
```

**Key difference from "cite as needed"**:

| Aspect | Cite as Needed | Research-Write |
|--------|---------------|----------------|
| When papers consulted | After prose written | Before/during |
| What's extracted | Title + TLDR | Findings, insights, exhibits |
| How content shaped | Claims → find papers | Papers → develop claims |
| Output value | Citation credibility | Paper content in chapter |

**Requires**: `ml4t-refs` MCP server for paper access.

See `skills/research-write/SKILL.md` for full workflow documentation.

## CLI Usage

The plugin includes a CLI for direct invocation:

```bash
python ~/agents/plugins/references/lib/cli.py status
python ~/agents/plugins/references/lib/cli.py sync --dry-run
python ~/agents/plugins/references/lib/cli.py search "asset embeddings"
```

## Dependencies

Core functionality requires no dependencies (uses SQLite and subprocess).

Optional features:
- `pip install google-generativeai json-repair` for AI summaries
- Marker must be installed separately for PDF parsing

## License

MIT
