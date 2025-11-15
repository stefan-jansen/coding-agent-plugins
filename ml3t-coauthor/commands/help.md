---
description: "Display help for available commands"
argument-hint: "[command name]"
allowed-tools: [Read, Write]
---

# Help Command

Display information about available commands in the ML3T co-authoring framework.

## Available Commands

### Core Workflow Commands

**Planning & Design** (NEW)
- `/validate-los` - Extract, validate, and cross-check learning outcomes across chapters
- `/design-code-examples` - Design pedagogically-aligned code examples for a chapter

**Section Expansion & Integration**
- `/expand-section` - Expand section with curated references and iterative refinement
- `/integrate-chapter` - Combine section drafts into coherent chapter

**Code Management**
- `/notebook` - Create and manage Jupyter notebooks with JupyText sync
- `/test` - Validate code examples for reproducibility
- `/sync` - Ensure code-text alignment across chapter and notebooks

**Citation & Verification**
- `/track-citations` - Track which papers cited in which chapters
- `/verify-chapter` - Citation and code quality verification before finalization

### Collaboration & Progress
- `/review` - Create Git PR for collaborative review (multi-LLM workflow)
- `/status` - View project progress, metrics, and intelligent next steps

### Utility
- `/help` - Display this help or command-specific help

## Archived Commands

The following commands have been archived (not used in current workflow):
- `/outline` - User uses external LLMs for outlines
- `/cite` - Replaced by `/track-citations`
- `/research` - Replaced by citation curation pipeline + `/expand-section`
- `/publish` - Deferred to Q3-Q4 2025

## Workflow Overview

**Your Workflow: Curated Sources → Iterative Expansion → Integration**

1. **Curate Sources** (per chapter/section)
   ```bash
   # Process Gemini Deep Research report with quality scoring
   ./manage.sh research curate ~/Dropbox/ML4T/drafts/03/research/gemini_01.md --chapter 03
   ```

2. **Expand Sections** (with curated refs, iterate with human-in-loop)
   ```bash
   # First iteration
   /expand-section --chapter 03 --section "Backtesting Methodology"

   # Human reviews, provides feedback
   # Revise based on feedback
   /expand-section --chapter 03 --section "Backtesting Methodology" \
     --revise --feedback "Add more on overfitting risks"
   ```

3. **Integrate Chapter** (combine sections with coherence checks)
   ```bash
   # Auto-discover and integrate all sections
   /integrate-chapter --chapter 03

   # Or specify section order
   /integrate-chapter --chapter 03 --sections "Introduction,Methodology,Case Study"
   ```

4. **Develop Code Examples** (parallel with writing)
   ```bash
   /notebook --chapter 03 "backtesting_walkforward.ipynb" --template ml
   /sync --chapter 03 --check
   /test --chapter 03 --notebook "backtesting_walkforward.ipynb"
   ```

5. **Verify & Track** (before finalizing)
   ```bash
   /track-citations "Chapter 03" --add
   /verify-chapter "Chapter 03"
   ```

6. **Collaborative Review** (Git PR with multiple LLMs)
   ```bash
   /review --chapter 03
   # Creates PR for multi-LLM review
   ```

## Command Examples

### Validate Learning Outcomes (NEW)
```bash
# Validate all chapters (recommended first run)
/validate-los

# Validate specific chapter
/validate-los --chapter 3

# Deep analysis (includes research/code check)
/validate-los --check-implicit

# Skip overlap detection (faster)
/validate-los --no-overlap
```

**Output**:
- CSV: All LOs structured for review (`~/ml4t/third_edition/common/learning_outcomes/`)
- Validation report with statistics
- Overlap analysis with similarity scores

### Design Code Examples (NEW)
```bash
# Design code examples for chapter 3
/design-code-examples --chapter 3

# Design only free content
/design-code-examples --chapter 5 --style free

# Design only premium content
/design-code-examples --chapter 12 --style premium
```

**Output**:
- Design proposal with LO-aligned example structure
- Skeleton Jupyter notebooks with TODO markers
- Code-to-LO mapping documentation

### Expand Section (Core Command)
```bash
# First expansion with curated references
/expand-section --chapter 3 --section "Backtesting Methodology"

# Expand with higher quality threshold
/expand-section --chapter 3 --section "Walk-Forward" --quality-threshold 8.0

# Tutorial style
/expand-section --chapter 2 --section "Implementation" --style tutorial

# Revision with feedback
/expand-section --chapter 3 --section "Backtesting Methodology" \
  --revise --feedback "Add concrete code example of train/test split"
```

### Integrate Chapter
```bash
# Auto-discover all section drafts
/integrate-chapter --chapter 3

# Specify section order
/integrate-chapter --chapter 5 --sections "Introduction,Math,Implementation"

# Revise integration
/integrate-chapter --chapter 3 --revise \
  --feedback "Transition between sections 2 and 3 too abrupt"
```

### Track Citations
```bash
# Track all citations in chapter
/track-citations "Chapter 03" --add

# Lookup where a paper is cited
/track-citations "Heaton2016" --lookup

# Generate master bibliography
/track-citations --generate-bibliography
```

### Verify Chapter
```bash
# Full verification
/verify-chapter "Chapter 03"

# Citation-only check
/verify-chapter "Chapter 03" --citations-only

# Code-only check
/verify-chapter "Chapter 03" --code-only
```

### Status & Progress
```bash
# Comprehensive project status
/status

# Show intelligent next steps
/status --suggest

# Filter by chapter
/status --chapter 3
```

## Command Structure

Commands follow this pattern:
```
/command --required value [--optional value]
```

## Citation Curation Pipeline

**Location**: `~/agents/ml3t/researcher/`

**Purpose**: Process Gemini Deep Research reports → quality-scored curated sources

**6-Stage Pipeline**:
1. Extract citations from markdown
2. Validate links (HTTP HEAD)
3. Classify source type (academic/industry/blog/GitHub)
4. Quality scoring (Google Scholar + LLM + GitHub metrics)
5. Content extraction (Marker VLM, trafilatura, GitHub API)
6. Integration (Zotero + Qdrant + SQLite)

**Usage**:
```bash
cd ~/agents/ml3t/researcher
./manage.sh research curate <gemini_report.md> --chapter XX --section tag
```

**Status**: 13/40 tasks complete, 3-4 weeks remaining

## Configuration

**Project Structure**:
- `.claude/commands/` - Command definitions
- `.claude/book/manifest.json` - Project state and progress
- `.claude/research/curation/` - Curated references metadata
- `content/chapters/` - Chapter drafts
- `code/notebooks/` - Jupyter notebooks (JupyText synced)

**Research Infrastructure**:
- ML3T Researcher MCP server: `http://localhost:8000`
- Qdrant vector DB: 456 papers indexed
- Citation curation pipeline: Quality scoring + multi-collection architecture

## Getting Help

For detailed help on a specific command:
```bash
/help expand-section
/help integrate-chapter
/help track-citations
```

---

**Framework Version**: ML3T Consolidated (2025-10-08)
**Total Commands**: 11 (8 core workflow + 3 supporting)
**Key Features**: LO validation, code design, curated sources, iterative refinement, citation tracking, multi-LLM review

*Use `/help [command]` for detailed information about any specific command.*
