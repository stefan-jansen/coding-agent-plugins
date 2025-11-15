---
description: "Draft chapter content from outline"
argument-hint: "--chapter N --section NAME [--style academic|conversational|tutorial]"
allowed-tools: [Read, Write, Bash]
---

# Write Command

Drafts chapter content based on outlines, research, and style guidelines.

## Parse Arguments

```bash
# Extract chapter, section, and style
CHAPTER=""
SECTION=""
STYLE="conversational"  # Default for technical books

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

CHAPTER_ID=$(printf "%03d" "$CHAPTER")
echo "✍️ Writing Chapter $CHAPTER, Section: $SECTION"
echo "🎨 Style: $STYLE"
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

## Prepare Draft Directory

```bash
# Create draft directory
DRAFT_DIR=".claude/book/chapters/$CHAPTER_ID/drafts"
mkdir -p "$DRAFT_DIR"

# Generate timestamp for version control
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SAFE_SECTION=$(echo "$SECTION" | sed 's/[^a-zA-Z0-9-]/_/g')
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
**Status**: draft
---

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
echo "\n✅ Draft Created Successfully!"
echo "───────────────────────────────────────"
echo "  Chapter: $CHAPTER - $CHAPTER_TITLE"
echo "  Section: $SECTION"
echo "  Draft: $DRAFT_FILE"
echo "  Words written: $WORD_COUNT / ~$SECTION_TARGET target"
echo "  Total book progress: $TOTAL_WORDS words"
echo ""
echo "Next steps:"
echo "  • Review and expand the draft"
echo "  • Use /notebook to create code examples"
echo "  • Use /cite to add references"
echo "  • Use /review when section is complete"
echo ""
echo "Quick edit: code $DRAFT_FILE"
```

## Auto-save Feature

```bash
# Set up auto-save reminder
echo "\n💾 Auto-save enabled. Draft location:"
echo "   $DRAFT_FILE"
echo ""
echo "Version history maintained in:"
echo "   $DRAFT_DIR/"
```

---

## Examples

```bash
# Write introduction section for chapter 1
/write --chapter 1 --section Introduction

# Write implementation section with tutorial style
/write --chapter 3 --section Implementation --style tutorial

# Write mathematical foundations with academic style
/write --chapter 5 --section "Mathematical Foundations" --style academic
```

*The write command creates versioned drafts with style-appropriate content templates.*