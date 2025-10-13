---
description: "Expand section with curated references and iterative refinement"
argument-hint: "--chapter N --section NAME [--style academic|conversational|tutorial] [--revise] [--feedback 'text'] [--quality-threshold N]"
allowed-tools: [Read, Write, Bash]
---

# Expand Section Command

Expands section content using curated references from the research corpus, with support for iterative refinement based on human feedback.

## Parse Arguments

```bash
# Extract chapter, section, style, and iteration parameters
CHAPTER=""
SECTION=""
STYLE="conversational"  # Default for technical books
REVISE=false
FEEDBACK=""
QUALITY_THRESHOLD=7.0  # Minimum quality score for curated references

# Parse chapter number
if [[ "$ARGUMENTS" =~ --chapter[[:space:]]+([0-9]+) ]]; then
    CHAPTER="${BASH_REMATCH[1]}"
else
    echo "❌ Chapter number required: --chapter N"
    exit 1
fi

# Parse section name
if [[ "$ARGUMENTS" =~ --section[[:space:]]+([^[:space:]]+) ]]; then
    SECTION="${BASH_REMATCH[1]}"
else
    echo "❌ Section name required: --section NAME"
    exit 1
fi

# Parse writing style
if [[ "$ARGUMENTS" =~ --style[[:space:]]+(academic|conversational|tutorial) ]]; then
    STYLE="${BASH_REMATCH[1]}"
fi

# Check for revision mode
if [[ "$ARGUMENTS" =~ --revise ]]; then
    REVISE=true
fi

# Extract feedback (for revision iterations)
if [[ "$ARGUMENTS" =~ --feedback[[:space:]]+'([^']+)' ]] || [[ "$ARGUMENTS" =~ --feedback[[:space:]]+\"([^\"]+)\" ]]; then
    FEEDBACK="${BASH_REMATCH[1]}"
fi

# Parse quality threshold
if [[ "$ARGUMENTS" =~ --quality-threshold[[:space:]]+([0-9.]+) ]]; then
    QUALITY_THRESHOLD="${BASH_REMATCH[1]}"
fi

CHAPTER_ID=$(printf "%03d" "$CHAPTER")
echo "✍️ Expanding Chapter $CHAPTER, Section: $SECTION"
echo "🎨 Style: $STYLE"
if [ "$REVISE" == "true" ]; then
    echo "♻️  Revision mode"
    [ -n "$FEEDBACK" ] && echo "💬 Feedback: $FEEDBACK"
fi
```

## Load Outline and Context

```bash
# Check outline exists
OUTLINE_FILE=".claude/book/chapters/$CHAPTER_ID/outline.md"
if [ ! -f "$OUTLINE_FILE" ]; then
    echo "❌ No outline found. Run: /outline --chapter $CHAPTER"
    exit 1
fi

# Load chapter metadata
MANIFEST_FILE=".claude/book/manifest.json"
CHAPTER_TITLE=$(jq -r ".chapters.\"$CHAPTER_ID\".title" "$MANIFEST_FILE")
TARGET_WORDS=$(jq -r ".chapters.\"$CHAPTER_ID\".target_words // 8000" "$MANIFEST_FILE")

# Extract section from outline
SECTION_CONTENT=$(awk "/### .*$SECTION/,/^###[^#]/ { print }" "$OUTLINE_FILE" | head -n -1)
if [ -z "$SECTION_CONTENT" ]; then
    echo "⚠️  Section '$SECTION' not found in outline"
    echo "Available sections:"
    grep "^### " "$OUTLINE_FILE" | sed 's/### /  - /'
    exit 1
fi

# Calculate section word target
SECTION_COUNT=$(grep -c "^### " "$OUTLINE_FILE")
SECTION_TARGET=$((TARGET_WORDS / SECTION_COUNT))

echo "📚 Found section in outline"
echo "🎯 Target words for section: ~$SECTION_TARGET"
```

## Load Curated References

```bash
# Check if citation curation has been run for this chapter
CURATION_METADATA=".claude/research/curation/chapter_${CHAPTER_ID}_metadata.json"
CURATED_REFS=""
CURATED_COUNT=0

if [ -f "$CURATION_METADATA" ]; then
    echo "🔍 Loading curated references for Chapter $CHAPTER, Section: $SECTION"

    # Query curated references for this chapter/section with quality threshold
    # Format: chapter=03, section=backtesting, quality_score >= 7.0
    SAFE_SECTION_TAG=$(echo "$SECTION" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/_/g')

    # Load references from curation metadata
    # (Note: When citation curation pipeline is complete, this will query Qdrant)
    # For now, check if metadata file has section-tagged references
    CURATED_REFS=$(jq -r --arg sect "$SAFE_SECTION_TAG" --arg qt "$QUALITY_THRESHOLD" \
        '.references[] | select(.section == $sect and (.quality_score // 0) >= ($qt | tonumber)) |
         "- \(.authors) (\(.year)). \(.title). \(.source). Quality: \(.quality_score)"' \
        "$CURATION_METADATA" 2>/dev/null || echo "")

    if [ -n "$CURATED_REFS" ]; then
        CURATED_COUNT=$(echo "$CURATED_REFS" | wc -l)
        echo "✅ Found $CURATED_COUNT curated references (quality >= $QUALITY_THRESHOLD)"
        echo "📄 References:"
        echo "$CURATED_REFS" | head -5  # Show first 5
        if [ $CURATED_COUNT -gt 5 ]; then
            echo "   ... and $((CURATED_COUNT - 5)) more"
        fi
    else
        echo "⚠️  No curated references found for section: $SECTION (quality >= $QUALITY_THRESHOLD)"
        echo "💡 Tip: Run citation curation pipeline on Gemini Deep Research report first"
        echo "    ./manage.sh research curate <report.md> --chapter $CHAPTER --section $SAFE_SECTION_TAG"
    fi
else
    echo "ℹ️  No curation metadata found for Chapter $CHAPTER"
    echo "💡 Tip: Process Gemini Deep Research report with:"
    echo "    ./manage.sh research curate <report.md> --chapter $CHAPTER"
    echo ""
    echo "Proceeding without curated references..."
fi
echo ""
```

## Prepare Draft Directory

```bash
# Create draft directory
DRAFT_DIR=".claude/book/chapters/$CHAPTER_ID/drafts"
mkdir -p "$DRAFT_DIR"

# Generate timestamp for version control
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SAFE_SECTION=$(echo "$SECTION" | sed 's/[^a-zA-Z0-9-]/_/g')

# Handle revision mode
if [ "$REVISE" == "true" ]; then
    # Load previous draft for revision
    LATEST_LINK="$DRAFT_DIR/${SAFE_SECTION}_latest.md"

    if [ -L "$LATEST_LINK" ]; then
        PREVIOUS_DRAFT=$(readlink -f "$LATEST_LINK")
        echo "📄 Loading previous draft: $(basename "$PREVIOUS_DRAFT")"

        # Read previous content (skip metadata)
        PREVIOUS_CONTENT=$(tail -n +10 "$PREVIOUS_DRAFT")
        PREVIOUS_WORD_COUNT=$(echo "$PREVIOUS_CONTENT" | wc -w)

        echo "   Previous word count: $PREVIOUS_WORD_COUNT"
        [ -n "$FEEDBACK" ] && echo "   Addressing: $FEEDBACK"
    else
        echo "⚠️  No previous draft found for revision. Creating first version."
        REVISE=false
    fi
fi

DRAFT_FILE="$DRAFT_DIR/${SAFE_SECTION}_${TIMESTAMP}.md"
echo "📁 Draft location: $DRAFT_FILE"
```

## Generate Content Structure

```bash
# Initialize draft with metadata
cat > "$DRAFT_FILE" << EOF
# Chapter $CHAPTER: $CHAPTER_TITLE
## Section: $SECTION

---
**Draft Version**: $TIMESTAMP
**Style**: $STYLE
**Target Words**: $SECTION_TARGET
**Curated References**: $CURATED_COUNT (quality >= $QUALITY_THRESHOLD)
$(if [ "$REVISE" == "true" ]; then echo "**Revision**: Yes"; fi)
$(if [ -n "$FEEDBACK" ]; then echo "**Feedback Addressed**: $FEEDBACK"; fi)
$(if [ "$REVISE" == "true" ]; then echo "**Previous Version**: $(basename "$PREVIOUS_DRAFT")"; fi)
**Status**: draft
---

$(if [ $CURATED_COUNT -gt 0 ]; then
    echo "## Curated References for This Section"
    echo ""
    echo "$CURATED_REFS"
    echo ""
    echo "---"
    echo ""
fi)

$(if [ "$REVISE" == "true" ]; then
    echo "## Revision Notes"
    echo ""
    echo "**Previous draft word count**: $PREVIOUS_WORD_COUNT"
    if [ -n "$FEEDBACK" ]; then
        echo "**Feedback to address**: $FEEDBACK"
    fi
    echo ""
    echo "**Revision strategy**: [To be filled by LLM/human]"
    echo ""
    echo "---"
    echo ""
fi)

EOF
```

## Write Content Based on Style

```bash
# Style-specific content generation
case "$STYLE" in
    academic)
        cat >> "$DRAFT_FILE" << 'EOF'
[INTRODUCTION - Establish theoretical foundation]

In this section, we examine $SECTION from a rigorous analytical perspective. The mathematical foundations underlying this concept are essential for understanding its application in quantitative trading systems.

### Theoretical Background

[Present formal definitions, theorems, and proofs]

Let us begin by establishing the formal framework. Consider a trading system $S$ operating over a time horizon $T$...

### Mathematical Formulation

[Include equations, derivations, and algorithmic complexity]

$$
\text{Objective Function: } J = \sum_{t=1}^{T} \gamma^t R_t
$$

where $\gamma$ represents the discount factor and $R_t$ denotes the reward at time $t$.

### Empirical Analysis

[Present research findings and statistical validation]

Recent studies (Author, 2023) have demonstrated that...

EOF
        ;;
    
    conversational)
        cat >> "$DRAFT_FILE" << 'EOF'
[INTRODUCTION - Engage with practical problem]

Let's dive into $SECTION and see how it can transform your trading strategies. If you've ever wondered how professional quant traders approach this problem, you're in the right place.

### The Big Picture

Imagine you're managing a portfolio worth millions. Every decision matters, and you need tools that work reliably under pressure. That's where $SECTION comes in.

### Breaking It Down

Here's what actually happens behind the scenes:

1. **First Step**: We start by...
   - Why this matters: [explain practical impact]
   - Common mistake to avoid: [highlight pitfall]

2. **Key Insight**: The secret is...
   - Real example: [concrete scenario]
   - What this means for you: [practical application]

### Let's Build Something

```python
# Here's how you actually implement this
import pandas as pd
import numpy as np

# Start with real market data
data = pd.read_csv('market_data.csv')

# The magic happens here
# [Add working code with comments]
```

### What Could Go Wrong?

[Discuss edge cases and failure modes with solutions]

EOF
        ;;
    
    tutorial)
        cat >> "$DRAFT_FILE" << 'EOF'
[INTRODUCTION - Set up hands-on exercise]

## What You'll Build

By the end of this section, you'll have a working implementation of $SECTION that you can immediately apply to your trading strategies.

### Prerequisites

✅ You should have:
- Python 3.8+ installed
- Basic understanding of [prerequisite concepts]
- Access to market data (we'll show you how)

### Step 1: Environment Setup

```bash
# Create project directory
mkdir ml_trading_$SECTION
cd ml_trading_$SECTION

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install pandas numpy matplotlib yfinance backtrader
```

### Step 2: Data Preparation

```python
# File: 01_prepare_data.py
import yfinance as yf
import pandas as pd

# Download sample data
data = yf.download('SPY', start='2020-01-01', end='2023-12-31')
print(f"Downloaded {len(data)} days of data")

# Save for later use
data.to_csv('spy_data.csv')
```

💻 **Try it yourself**: Run this code and verify you see the data.

### Step 3: Core Implementation

[Incremental code building with explanations]

### Step 4: Testing Your Implementation

```python
# File: test_implementation.py
def test_basic_functionality():
    # Your test here
    assert result == expected, "Test failed!"
    print("✅ All tests passed!")
```

### Your Turn: Exercises

1. **Easy**: Modify the code to...
2. **Medium**: Extend the functionality to...
3. **Challenge**: Optimize the performance by...

EOF
        ;;
esac
```

## Add Section-Specific Content

```bash
# Append section outline details
echo "\n## Detailed Content\n" >> "$DRAFT_FILE"
echo "$SECTION_CONTENT" >> "$DRAFT_FILE"
echo "\n---\n" >> "$DRAFT_FILE"

# Add placeholder for code notebooks
echo "## Associated Notebooks\n" >> "$DRAFT_FILE"
echo "- [ ] Create notebook: ${SAFE_SECTION}_implementation.ipynb" >> "$DRAFT_FILE"
echo "- [ ] Create notebook: ${SAFE_SECTION}_exercises.ipynb" >> "$DRAFT_FILE"
echo "\n## Research Integration\n" >> "$DRAFT_FILE"
echo "[To be populated from research assets]" >> "$DRAFT_FILE"
```

## Create Latest Symlink

```bash
# Create symlink to latest draft
LATEST_LINK="$DRAFT_DIR/${SAFE_SECTION}_latest.md"
ln -sf "$(basename "$DRAFT_FILE")" "$LATEST_LINK"
echo "🔗 Latest draft linked: $LATEST_LINK"
```

## Update Progress Tracking

```bash
# Count words in draft
WORD_COUNT=$(wc -w < "$DRAFT_FILE")

# Update manifest with progress
jq --arg ch "$CHAPTER_ID" \
   --arg wc "$WORD_COUNT" \
   --arg sect "$SECTION" \
   --arg file "$DRAFT_FILE" \
   '.chapters[$ch].sections[$sect] = {
       "status": "drafted",
       "word_count": ($wc | tonumber),
       "draft_file": $file,
       "last_updated": now | todate
   } |
   .chapters[$ch].status = "drafting" |
   .chapters[$ch].word_count = (
       [.chapters[$ch].sections[].word_count // 0] | add
   )' \
   "$MANIFEST_FILE" > "${MANIFEST_FILE}.tmp" && \
   mv "${MANIFEST_FILE}.tmp" "$MANIFEST_FILE"

# Update project word count
TOTAL_WORDS=$(jq '[.chapters[].word_count // 0] | add' "$MANIFEST_FILE")
jq --arg tw "$TOTAL_WORDS" '.project.current_words = ($tw | tonumber)' \
   "$MANIFEST_FILE" > "${MANIFEST_FILE}.tmp" && \
   mv "${MANIFEST_FILE}.tmp" "$MANIFEST_FILE"
```

## Generate Writing Summary

```bash
if [ "$REVISE" == "true" ]; then
    echo "\n✅ Section Revision Complete!"
else
    echo "\n✅ Section Expansion Complete!"
fi
echo "═══════════════════════════════════════════════════════"
echo "  Chapter: $CHAPTER - $CHAPTER_TITLE"
echo "  Section: $SECTION"
echo "  Draft: $DRAFT_FILE"
echo "  Words written: $WORD_COUNT / ~$SECTION_TARGET target"
if [ "$REVISE" == "true" ]; then
    WORD_DELTA=$((WORD_COUNT - PREVIOUS_WORD_COUNT))
    echo "  Word change: $WORD_DELTA (was $PREVIOUS_WORD_COUNT)"
fi
echo "  Curated references: $CURATED_COUNT"
echo "  Total book progress: $TOTAL_WORDS words"
echo ""
echo "📝 Next steps:"
if [ "$REVISE" != "true" ]; then
    echo "  • Review draft and iterate: /expand-section --chapter $CHAPTER --section \"$SECTION\" --revise --feedback 'your feedback'"
fi
echo "  • Create code examples: /notebook --chapter $CHAPTER"
echo "  • Integrate sections: /integrate-chapter --chapter $CHAPTER"
echo "  • Track citations: /track-citations \"Chapter $CHAPTER\" --add"
echo "  • Verify quality: /verify-chapter \"Chapter $CHAPTER\""
echo ""
echo "Quick edit: code $DRAFT_FILE"
echo "═══════════════════════════════════════════════════════"
```

## Auto-save Feature

```bash
# Set up auto-save reminder
echo "\n💾 Version history maintained in: $DRAFT_DIR/"
echo "   Latest: $(basename "$LATEST_LINK")"
if [ "$REVISE" == "true" ]; then
    echo "   Previous: $(basename "$PREVIOUS_DRAFT")"
fi
```

---

## Examples

```bash
# First iteration: Expand section with curated references
/expand-section --chapter 3 --section "Backtesting Methodology"
# Loads curated refs: chapter=03, section=backtesting, quality >= 7.0

# Expand with specific quality threshold
/expand-section --chapter 3 --section "Walk-Forward Analysis" --quality-threshold 8.0

# Expand with tutorial style
/expand-section --chapter 2 --section "Implementation" --style tutorial

# Revision iteration with human feedback
/expand-section --chapter 3 --section "Backtesting Methodology" \
  --revise --feedback "Add more on overfitting risks and how to mitigate them"

# Second revision iteration
/expand-section --chapter 3 --section "Backtesting Methodology" \
  --revise --feedback "Include concrete code example of train/test split"

# Academic style expansion
/expand-section --chapter 5 --section "Mathematical Foundations" --style academic
```

---

## Notes

**Curated References Integration:**
- Loads references from `.claude/research/curation/chapter_XX_metadata.json`
- Filters by section tag (e.g., "backtesting", "walk_forward")
- Quality threshold defaults to 7.0 (adjustable with `--quality-threshold`)
- When citation curation pipeline is complete, will query Qdrant directly

**Iteration Workflow:**
1. First pass: `/expand-section --chapter N --section "Name"`
2. Human reviews draft
3. Revise: `/expand-section --chapter N --section "Name" --revise --feedback "specific issue"`
4. Repeat until satisfied

**Integration with Citation Curation Pipeline:**
- Run curation first: `./manage.sh research curate <gemini_report.md> --chapter XX --section tag`
- Curated refs auto-loaded when available
- Gracefully falls back if no curation metadata found

*The expand-section command creates versioned section drafts using curated references with iterative refinement support.*