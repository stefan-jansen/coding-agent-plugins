---
title: Track Citations
aliases: [citations, cite]
---

# Track Citations

Centralized citation tracking across all chapters to prevent duplicate tracking and enable quick lookups.

## Usage

```bash
/track-citations "Chapter 3" --add                # Add chapter citations to tracker
/track-citations "Heaton2016" --lookup            # Check if paper already cited
/track-citations --summary                        # Show all citations across chapters
/track-citations --bibliography                   # Generate master bibliography
```

## What This Command Does

**Problem Solved**: "Manually tracking citations across chapters is repetitive and error-prone" (3+ hours spent on manual tracking across Chapters 3-5)

**Centralized Citation Management**:
1. Tracks which papers cited in which chapters
2. Detects duplicate citations across chapters
3. Provides quick lookup for paper citation status
4. Generates master bibliography from all tracked citations
5. Prevents citation tracking errors and mismatches

**Integration**: Used after drafting and during verification phase (Research → Draft → **Track** → Verify)

## Prerequisites

- Chapter draft completed (via `/draft-chapter`)
- Citations present in draft (paper references)
- Draft file exists in `.claude/work/drafts/`

## Implementation

```bash
#!/bin/bash

# Standard constants
readonly CLAUDE_DIR=".claude"
readonly WORK_DIR="${CLAUDE_DIR}/work"
readonly DRAFTS_DIR="${WORK_DIR}/drafts"
readonly CITATIONS_DIR="${WORK_DIR}/citations"
readonly CITATIONS_DB="${CITATIONS_DIR}/citations.json"

# Error handling
error_exit() {
    echo "ERROR: $1" >&2
    exit 1
}

warn() {
    echo "WARNING: $1" >&2
}

info() {
    echo "INFO: $1"
}

success() {
    echo "✅ $1"
}

# Parse arguments
MODE=""
CHAPTER_OR_PAPER=""

if [[ "$ARGUMENTS" == *"--add"* ]]; then
    MODE="add"
    CHAPTER_OR_PAPER=$(echo "$ARGUMENTS" | sed 's/--add//g' | xargs)
elif [[ "$ARGUMENTS" == *"--lookup"* ]]; then
    MODE="lookup"
    CHAPTER_OR_PAPER=$(echo "$ARGUMENTS" | sed 's/--lookup//g' | xargs)
elif [[ "$ARGUMENTS" == "--summary" ]]; then
    MODE="summary"
elif [[ "$ARGUMENTS" == "--bibliography" ]]; then
    MODE="bibliography"
else
    error_exit "Usage: /track-citations [chapter/paper] [--add|--lookup|--summary|--bibliography]"
fi

echo "📚 Track Citations"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Ensure directories exist
mkdir -p "$CITATIONS_DIR"

# Initialize citations database if not exists
if [ ! -f "$CITATIONS_DB" ]; then
    cat > "$CITATIONS_DB" <<EOF
{
  "created_at": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "chapters": {},
  "papers": {}
}
EOF
    info "Initialized citations database: $CITATIONS_DB"
fi

# Helper: Extract paper IDs from draft file
extract_citations() {
    local draft_file="$1"
    local chapter_name="$2"

    # Look for citation patterns: [AuthorYear], (Author et al., Year), etc.
    # This regex catches common academic citation formats
    grep -oE '\[([A-Za-z]+[0-9]{4}[a-z]?)\]|\(([A-Za-z]+( et al\.)?,? [0-9]{4}[a-z]?)\)' "$draft_file" | \
        sed -E 's/[\[\(\)]//g; s/ et al\.//g; s/,? //g' | \
        sort -u
}

# Mode: Add chapter citations
if [ "$MODE" = "add" ]; then
    if [ -z "$CHAPTER_OR_PAPER" ]; then
        error_exit "Chapter title required for --add mode"
    fi

    CHAPTER_TITLE="$CHAPTER_OR_PAPER"
    CHAPTER_SLUG=$(echo "$CHAPTER_TITLE" | tr '[:upper:]' '[:lower:]' | tr -cs '[:alnum:]' '-' | sed 's/-$//')
    DRAFT_FILE="${DRAFTS_DIR}/${CHAPTER_SLUG}.md"

    if [ ! -f "$DRAFT_FILE" ]; then
        error_exit "Draft not found: $DRAFT_FILE. Run /draft-chapter first."
    fi

    echo "Adding citations from: $CHAPTER_TITLE"
    echo "Draft: $DRAFT_FILE"
    echo ""

    # Extract citations from draft
    CITATIONS_FOUND=$(extract_citations "$DRAFT_FILE" "$CHAPTER_TITLE")
    CITATION_COUNT=$(echo "$CITATIONS_FOUND" | grep -v '^$' | wc -l)

    if [ "$CITATION_COUNT" -eq 0 ]; then
        warn "No citations found in draft (looking for [AuthorYear] or (Author, Year) patterns)"
        exit 0
    fi

    info "Found $CITATION_COUNT citations in draft"
    echo ""

    # Update citations database
    # Note: Using basic JSON manipulation since jq may not be available
    TEMP_DB=$(mktemp)

    # Read existing database
    EXISTING_DATA=$(cat "$CITATIONS_DB")

    # For each citation, update database
    echo "$CITATIONS_FOUND" | grep -v '^$' | while read -r citation; do
        echo "  - Tracking: $citation"

        # Create citation entry file (simple approach without jq dependency)
        CITATION_FILE="${CITATIONS_DIR}/${citation}.txt"

        # Check if already tracked
        if [ -f "$CITATION_FILE" ]; then
            # Append chapter if not already listed
            if ! grep -q "^$CHAPTER_TITLE$" "$CITATION_FILE"; then
                echo "$CHAPTER_TITLE" >> "$CITATION_FILE"
                info "    Added $CHAPTER_TITLE to existing citation $citation"
            else
                info "    Already tracked in $CHAPTER_TITLE"
            fi
        else
            # Create new citation tracking file
            echo "$CHAPTER_TITLE" > "$CITATION_FILE"
            success "    New citation tracked: $citation"
        fi
    done

    # Create chapter citation summary
    CHAPTER_CITATION_FILE="${CITATIONS_DIR}/chapter-${CHAPTER_SLUG}.txt"
    echo "$CITATIONS_FOUND" | grep -v '^$' > "$CHAPTER_CITATION_FILE"

    echo ""
    success "Tracked $CITATION_COUNT citations for $CHAPTER_TITLE"
    echo ""
    echo "📁 Citation tracking: $CITATIONS_DIR"
    echo ""
    info "Next: Run /track-citations --summary to see all citations"

# Mode: Lookup paper citation status
elif [ "$MODE" = "lookup" ]; then
    if [ -z "$CHAPTER_OR_PAPER" ]; then
        error_exit "Paper ID required for --lookup mode"
    fi

    PAPER_ID="$CHAPTER_OR_PAPER"
    CITATION_FILE="${CITATIONS_DIR}/${PAPER_ID}.txt"

    echo "Looking up: $PAPER_ID"
    echo ""

    if [ ! -f "$CITATION_FILE" ]; then
        warn "Paper not yet cited: $PAPER_ID"
        echo ""
        echo "This paper has not been tracked in any chapter yet."
        exit 0
    fi

    CHAPTER_COUNT=$(wc -l < "$CITATION_FILE")

    echo "📊 Citation Status: $PAPER_ID"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Cited in $CHAPTER_COUNT chapter(s):"
    echo ""

    while read -r chapter; do
        echo "  - $chapter"
    done < "$CITATION_FILE"

    echo ""
    success "Paper is tracked across $CHAPTER_COUNT chapter(s)"

# Mode: Summary of all citations
elif [ "$MODE" = "summary" ]; then
    if [ ! -d "$CITATIONS_DIR" ] || [ -z "$(ls -A "$CITATIONS_DIR" 2>/dev/null)" ]; then
        warn "No citations tracked yet. Run /track-citations [chapter] --add first."
        exit 0
    fi

    echo "📊 Citation Summary"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # Count total unique papers
    TOTAL_PAPERS=$(find "$CITATIONS_DIR" -name "*.txt" ! -name "chapter-*.txt" | wc -l)

    # Count total chapters with citations
    TOTAL_CHAPTERS=$(find "$CITATIONS_DIR" -name "chapter-*.txt" | wc -l)

    echo "Total Papers Cited: $TOTAL_PAPERS"
    echo "Total Chapters Tracked: $TOTAL_CHAPTERS"
    echo ""

    # Show papers cited multiple times (duplicates across chapters)
    echo "Papers Cited Multiple Times:"
    echo ""

    DUPLICATES_FOUND=false
    for citation_file in "$CITATIONS_DIR"/*.txt; do
        if [ -f "$citation_file" ] && [[ ! "$(basename "$citation_file")" =~ ^chapter- ]]; then
            citation=$(basename "$citation_file" .txt)
            chapter_count=$(wc -l < "$citation_file")

            if [ "$chapter_count" -gt 1 ]; then
                echo "  - $citation: Cited in $chapter_count chapters"
                DUPLICATES_FOUND=true
            fi
        fi
    done

    if [ "$DUPLICATES_FOUND" = false ]; then
        echo "  (No papers cited in multiple chapters yet)"
    fi

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # Show chapter-by-chapter breakdown
    echo "Chapter Citation Counts:"
    echo ""

    for chapter_file in "$CITATIONS_DIR"/chapter-*.txt; do
        if [ -f "$chapter_file" ]; then
            chapter_slug=$(basename "$chapter_file" | sed 's/^chapter-//; s/\.txt$//')
            citation_count=$(wc -l < "$chapter_file")
            echo "  - $chapter_slug: $citation_count citations"
        fi
    done

    echo ""
    info "Use /track-citations [paper-id] --lookup to see where specific paper is cited"

# Mode: Generate bibliography
elif [ "$MODE" = "bibliography" ]; then
    if [ ! -d "$CITATIONS_DIR" ] || [ -z "$(ls -A "$CITATIONS_DIR" 2>/dev/null)" ]; then
        warn "No citations tracked yet. Run /track-citations [chapter] --add first."
        exit 0
    fi

    BIBLIOGRAPHY_FILE="${CITATIONS_DIR}/master-bibliography.md"

    echo "📖 Generating Master Bibliography"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # Create bibliography file
    cat > "$BIBLIOGRAPHY_FILE" <<EOF
# Master Bibliography

**Generated**: $(date +"%Y-%m-%d %H:%M:%S")
**Total Papers**: $(find "$CITATIONS_DIR" -name "*.txt" ! -name "chapter-*.txt" | wc -l)

---

## Citations by Paper

EOF

    # List all papers alphabetically with chapter references
    for citation_file in "$CITATIONS_DIR"/*.txt; do
        if [ -f "$citation_file" ] && [[ ! "$(basename "$citation_file")" =~ ^chapter- ]]; then
            citation=$(basename "$citation_file" .txt)
            chapter_count=$(wc -l < "$citation_file")

            echo "### $citation" >> "$BIBLIOGRAPHY_FILE"
            echo "" >> "$BIBLIOGRAPHY_FILE"
            echo "**Cited in $chapter_count chapter(s)**:" >> "$BIBLIOGRAPHY_FILE"

            while read -r chapter; do
                echo "- $chapter" >> "$BIBLIOGRAPHY_FILE"
            done < "$citation_file"

            echo "" >> "$BIBLIOGRAPHY_FILE"
            echo "**Full Reference**: [Add full citation details here]" >> "$BIBLIOGRAPHY_FILE"
            echo "" >> "$BIBLIOGRAPHY_FILE"
            echo "---" >> "$BIBLIOGRAPHY_FILE"
            echo "" >> "$BIBLIOGRAPHY_FILE"
        fi
    done

    success "Master bibliography generated: $BIBLIOGRAPHY_FILE"
    echo ""
    echo "📁 Bibliography: $BIBLIOGRAPHY_FILE"
    echo ""
    info "Edit the bibliography file to add full citation details for each paper"
fi
```

## Success Indicators

Citation tracking succeeds when:
- ✅ Citations extracted from chapter drafts automatically
- ✅ Duplicate citations across chapters detected
- ✅ Quick lookup shows where paper is cited
- ✅ Master bibliography generated from tracked citations
- ✅ No manual spreadsheet tracking needed (saves 45-90 min per chapter)

## Troubleshooting

### "No citations found"
**Problem**: Citation extraction finds no citations in draft
**Solution**: Ensure citations follow standard format: [AuthorYear] or (Author, Year)

### "Draft not found"
**Problem**: Chapter draft doesn't exist for --add mode
**Solution**: Run `/draft-chapter [chapter-title]` first to create draft

### "Paper not yet cited"
**Problem**: Lookup for paper that hasn't been tracked
**Solution**: Normal behavior - paper not used yet. Track it when drafting chapter that cites it.

## Integration with Workflow

**Position**: Between Draft and Verify phases (Research → Draft → **Track** → Verify)

**Inputs**:
- Chapter title (for --add mode)
- Paper ID (for --lookup mode)
- Draft file with citations

**Outputs**:
- Citation tracking database: `.claude/work/citations/`
- Per-paper tracking files: `[PaperID].txt` (lists chapters citing it)
- Per-chapter tracking files: `chapter-[slug].txt` (lists papers cited)
- Master bibliography: `master-bibliography.md`

**Next Command**: `/verify-chapter [chapter-title]` to check citation completeness

## Evidence for Command Addition

**Pattern Observed**: Manual citation tracking across Chapters 3-5 (3 occurrences)

**Time Cost**:
- Chapter 3: 45 minutes manual tracking
- Chapter 4: 1 hour cross-referencing
- Chapter 5: 1.5 hours citation management
- **Total**: 3+ hours on repetitive citation work

**Repetitive Tasks Eliminated**:
- Manual spreadsheet updates per chapter
- Cross-chapter reference checking
- Duplicate detection
- Citation ID management
- Bibliography compilation preparation

**Value Proposition**: Saves 3+ hours over 12-chapter book, prevents citation tracking errors (2 mismatches found during manual tracking)
