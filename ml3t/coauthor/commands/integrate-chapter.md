---
description: "Integrate section drafts into coherent chapter"
argument-hint: "--chapter N [--sections SECTION1,SECTION2,...] [--revise] [--feedback 'text']"
allowed-tools: [Read, Write, Bash, mcp__sequential-thinking__sequentialthinking]
---

# Integrate Chapter Command

Combines multiple section drafts into a coherent, well-integrated chapter with smooth transitions, consistent terminology, and unified narrative flow.

## Parse Arguments

```bash
# Extract chapter, sections, and revision flags
CHAPTER=""
SECTIONS=""
REVISE=false
FEEDBACK=""

# Parse chapter number
if [[ "$ARGUMENTS" =~ --chapter[[:space:]]+([0-9]+) ]]; then
    CHAPTER="${BASH_REMATCH[1]}"
else
    echo "❌ Chapter number required: --chapter N"
    exit 1
fi

# Parse section list (comma-separated)
if [[ "$ARGUMENTS" =~ --sections[[:space:]]+([^[:space:]]+) ]]; then
    SECTIONS="${BASH_REMATCH[1]}"
fi

# Check for revision mode
if [[ "$ARGUMENTS" =~ --revise ]]; then
    REVISE=true
fi

# Extract feedback (for revision iterations)
if [[ "$ARGUMENTS" =~ --feedback[[:space:]]+'([^']+)' ]] || [[ "$ARGUMENTS" =~ --feedback[[:space:]]+\"([^\"]+)\" ]]; then
    FEEDBACK="${BASH_REMATCH[1]}"
fi

CHAPTER_ID=$(printf "%03d" "$CHAPTER")
echo "🔗 Integrating Chapter $CHAPTER"
if [ "$REVISE" == "true" ]; then
    echo "♻️  Revision mode with feedback: $FEEDBACK"
fi
```

## Load Chapter Context

```bash
# Load chapter metadata
MANIFEST_FILE=".claude/book/manifest.json"
CHAPTER_TITLE=$(jq -r ".chapters.\"$CHAPTER_ID\".title" "$MANIFEST_FILE")
TARGET_WORDS=$(jq -r ".chapters.\"$CHAPTER_ID\".target_words // 8000" "$MANIFEST_FILE")

if [ "$CHAPTER_TITLE" == "null" ]; then
    echo "❌ Chapter $CHAPTER not found in manifest"
    exit 1
fi

CHAPTER_DIR=".claude/book/chapters/$CHAPTER_ID"
DRAFT_DIR="$CHAPTER_DIR/drafts"

echo "📖 Chapter: $CHAPTER_TITLE"
echo "🎯 Target words: $TARGET_WORDS"
```

## Discover Section Drafts

```bash
# If sections not specified, auto-discover from drafts
if [ -z "$SECTIONS" ]; then
    echo "🔍 Auto-discovering section drafts..."

    # Find all *_latest.md symlinks (represents latest version of each section)
    SECTION_FILES=()
    while IFS= read -r latest_link; do
        if [ -L "$latest_link" ]; then
            SECTION_FILES+=("$latest_link")
        fi
    done < <(find "$DRAFT_DIR" -name "*_latest.md" -type l 2>/dev/null | sort)

    if [ ${#SECTION_FILES[@]} -eq 0 ]; then
        echo "❌ No section drafts found in $DRAFT_DIR"
        echo "Use /expand-section or /write to create section drafts first"
        exit 1
    fi

    echo "✅ Found ${#SECTION_FILES[@]} section drafts:"
    for file in "${SECTION_FILES[@]}"; do
        basename "$file" | sed 's/_latest.md$//' | sed 's/_/ /g'
    done
else
    # Parse comma-separated section list
    IFS=',' read -ra SECTION_NAMES <<< "$SECTIONS"
    SECTION_FILES=()

    echo "📋 Loading specified sections:"
    for section_name in "${SECTION_NAMES[@]}"; do
        # Convert to safe filename format
        safe_name=$(echo "$section_name" | sed 's/[^a-zA-Z0-9-]/_/g')
        latest_file="$DRAFT_DIR/${safe_name}_latest.md"

        if [ ! -L "$latest_file" ]; then
            echo "❌ Section draft not found: $section_name"
            echo "Expected file: $latest_file"
            exit 1
        fi

        SECTION_FILES+=("$latest_file")
        echo "  ✓ $section_name"
    done
fi

echo ""
```

## Prepare Integration Directory

```bash
# Create integration directory for versioning
INTEGRATION_DIR="$CHAPTER_DIR/integrated"
mkdir -p "$INTEGRATION_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)

if [ "$REVISE" == "true" ]; then
    # Load previous integration for revision
    PREVIOUS_INTEGRATION=$(find "$INTEGRATION_DIR" -name "chapter_${CHAPTER_ID}_integrated_*.md" -type f | sort -r | head -1)

    if [ -z "$PREVIOUS_INTEGRATION" ]; then
        echo "⚠️  No previous integration found for revision. Creating first version."
        REVISE=false
    else
        echo "📄 Loading previous integration: $(basename "$PREVIOUS_INTEGRATION")"
    fi
fi

INTEGRATED_FILE="$INTEGRATION_DIR/chapter_${CHAPTER_ID}_integrated_${TIMESTAMP}.md"
echo "📁 Integration output: $INTEGRATED_FILE"
echo ""
```

## Use Sequential Thinking for Integration Analysis

```bash
# Create analysis prompt for Claude
cat > /tmp/integration_analysis_prompt.txt << EOF
I need to integrate ${#SECTION_FILES[@]} section drafts into a coherent chapter for a technical book on Machine Learning for Trading.

Chapter: $CHAPTER_TITLE (Chapter $CHAPTER)
Target words: $TARGET_WORDS

Section files to integrate:
$(for file in "${SECTION_FILES[@]}"; do echo "- $(basename "$file")"; done)

$(if [ "$REVISE" == "true" ]; then echo "This is a REVISION with feedback: $FEEDBACK"; fi)

Please analyze:
1. Reading order for sections (logical flow)
2. Potential redundancies (same concepts explained twice)
3. Terminology consistency needs (notation, abbreviations)
4. Transition requirements (where smooth bridges needed)
5. Cross-reference verification (forward/backward references)
6. Integration strategy (what to keep, what to consolidate, what to add)

$(if [ "$REVISE" == "true" ]; then echo "Focus especially on addressing: $FEEDBACK"; fi)
EOF

echo "🧠 Analyzing section integration requirements..."
echo "(Using Sequential Thinking for comprehensive analysis)"
```

## Analyze Sections for Integration

```bash
# Load all section content
echo "📚 Loading section contents..."
SECTION_CONTENTS=()
SECTION_WORD_COUNTS=()
TOTAL_SECTION_WORDS=0

for file in "${SECTION_FILES[@]}"; do
    # Resolve symlink to actual file
    actual_file=$(readlink -f "$file")

    # Read content (skip metadata header)
    content=$(tail -n +10 "$actual_file")
    SECTION_CONTENTS+=("$content")

    # Count words
    word_count=$(echo "$content" | wc -w)
    SECTION_WORD_COUNTS+=("$word_count")
    TOTAL_SECTION_WORDS=$((TOTAL_SECTION_WORDS + word_count))

    echo "  • $(basename "$file" | sed 's/_latest.md$//'): $word_count words"
done

echo ""
echo "📊 Total content: $TOTAL_SECTION_WORDS words (target: $TARGET_WORDS)"

# Check for significant deviation
if [ $TOTAL_SECTION_WORDS -lt $((TARGET_WORDS / 2)) ]; then
    echo "⚠️  Warning: Combined sections are much shorter than target"
elif [ $TOTAL_SECTION_WORDS -gt $((TARGET_WORDS * 2)) ]; then
    echo "⚠️  Warning: Combined sections significantly exceed target"
fi
echo ""
```

## Detect Integration Issues

```bash
echo "🔍 Detecting integration issues..."

# 1. Check for redundant headings (same heading in multiple sections)
echo "Checking for redundant headings..."
ALL_HEADINGS=$(for content in "${SECTION_CONTENTS[@]}"; do
    echo "$content" | grep -E '^#{2,4} ' | sed 's/^#* //'
done | sort)

DUPLICATE_HEADINGS=$(echo "$ALL_HEADINGS" | uniq -d)
if [ -n "$DUPLICATE_HEADINGS" ]; then
    echo "⚠️  Found duplicate headings (may need consolidation):"
    echo "$DUPLICATE_HEADINGS" | sed 's/^/    - /'
else
    echo "✓ No duplicate headings"
fi
echo ""

# 2. Check for terminology variations (common inconsistencies)
echo "Checking terminology consistency..."
TERMINOLOGY_ISSUES=""

# Check backtesting variations
if echo "${SECTION_CONTENTS[@]}" | grep -qi "back-testing" && \
   echo "${SECTION_CONTENTS[@]}" | grep -qi "backtesting"; then
    TERMINOLOGY_ISSUES="${TERMINOLOGY_ISSUES}\n  - 'backtesting' vs 'back-testing'"
fi

# Check ML variations
if echo "${SECTION_CONTENTS[@]}" | grep -qi "machine-learning" && \
   echo "${SECTION_CONTENTS[@]}" | grep -qi "machine learning"; then
    TERMINOLOGY_ISSUES="${TERMINOLOGY_ISSUES}\n  - 'machine learning' vs 'machine-learning'"
fi

if [ -n "$TERMINOLOGY_ISSUES" ]; then
    echo "⚠️  Potential terminology inconsistencies:"
    echo -e "$TERMINOLOGY_ISSUES"
else
    echo "✓ No obvious terminology inconsistencies"
fi
echo ""

# 3. Check for transition words at section boundaries
echo "Checking section transitions..."
MISSING_TRANSITIONS=0
for ((i=0; i<${#SECTION_CONTENTS[@]}-1; i++)); do
    # Get last paragraph of section i
    last_para=$(echo "${SECTION_CONTENTS[$i]}" | tail -5)

    # Get first paragraph of section i+1
    first_para=$(echo "${SECTION_CONTENTS[$((i+1))]}" | head -5)

    # Check if either has transition words (Next, Now, Having, Building on, etc.)
    if ! echo "$last_para" | grep -qiE "(next|now|having|building on|with this|given)" && \
       ! echo "$first_para" | grep -qiE "(previously|earlier|as we|building on|recall)"; then
        MISSING_TRANSITIONS=$((MISSING_TRANSITIONS + 1))
    fi
done

if [ $MISSING_TRANSITIONS -gt 0 ]; then
    echo "⚠️  $MISSING_TRANSITIONS section boundary(ies) may need transition paragraphs"
else
    echo "✓ Section transitions appear adequate"
fi
echo ""
```

## Generate Integrated Chapter

```bash
echo "✨ Generating integrated chapter..."

# Initialize integrated chapter with metadata
cat > "$INTEGRATED_FILE" << EOF
# Chapter $CHAPTER: $CHAPTER_TITLE

---
**Integrated Version**: $TIMESTAMP
**Source Sections**: ${#SECTION_FILES[@]}
**Total Words**: $TOTAL_SECTION_WORDS
**Target Words**: $TARGET_WORDS
**Status**: integrated
$(if [ "$REVISE" == "true" ]; then echo "**Revision**: Addressing feedback - $FEEDBACK"; fi)
---

EOF

# Add chapter introduction (if revising, use previous; otherwise create new)
if [ "$REVISE" == "true" ] && [ -f "$PREVIOUS_INTEGRATION" ]; then
    echo "♻️  Reusing chapter introduction from previous integration"
    # Extract introduction (everything before first ## heading after metadata)
    awk '/^---$/,/^##[^#]/ {
        if (/^##[^#]/) exit;
        if (p) print;
        if (/^---$/) p=1
    }' "$PREVIOUS_INTEGRATION" >> "$INTEGRATED_FILE"
else
    echo "📝 Generating new chapter introduction"
    cat >> "$INTEGRATED_FILE" << EOF

## Introduction

This chapter explores $CHAPTER_TITLE, covering the essential concepts, methodologies, and practical implementations that quantitative traders need to master.

**Learning Objectives:**
- Understand the core principles of $CHAPTER_TITLE
- Implement practical trading strategies using these techniques
- Recognize common pitfalls and how to avoid them
- Apply best practices for production-ready systems

**Chapter Structure:**
$(for file in "${SECTION_FILES[@]}"; do
    section_name=$(basename "$file" | sed 's/_latest.md$//' | sed 's/_/ /g')
    echo "- $section_name"
done)

---

EOF
fi

# Integrate sections with transitions
echo "🔗 Merging sections with transitions..."

for ((i=0; i<${#SECTION_FILES[@]}; i++)); do
    file="${SECTION_FILES[$i]}"
    section_name=$(basename "$file" | sed 's/_latest.md$//' | sed 's/_/ /g')

    echo "  • Integrating: $section_name"

    # Add section content (skip metadata header)
    actual_file=$(readlink -f "$file")
    tail -n +10 "$actual_file" >> "$INTEGRATED_FILE"

    # Add transition paragraph between sections (except after last section)
    if [ $i -lt $((${#SECTION_FILES[@]} - 1)) ]; then
        next_section=$(basename "${SECTION_FILES[$((i+1))]}" | sed 's/_latest.md$//' | sed 's/_/ /g')

        echo "" >> "$INTEGRATED_FILE"
        echo "---" >> "$INTEGRATED_FILE"
        echo "" >> "$INTEGRATED_FILE"

        # Add transition hint for human review/LLM revision
        cat >> "$INTEGRATED_FILE" << EOF
<!-- TRANSITION NEEDED: From "$section_name" to "$next_section" -->
<!-- Suggested: Summarize key takeaways from previous section, preview next section -->

EOF
    fi
done

# Add chapter conclusion
echo "" >> "$INTEGRATED_FILE"
echo "---" >> "$INTEGRATED_FILE"
echo "" >> "$INTEGRATED_FILE"
cat >> "$INTEGRATED_FILE" << EOF

## Chapter Summary

In this chapter, we covered $CHAPTER_TITLE, exploring:

$(for file in "${SECTION_FILES[@]}"; do
    section_name=$(basename "$file" | sed 's/_latest.md$//' | sed 's/_/ /g')
    echo "- **$section_name**: [Key takeaway - to be filled]"
done)

**Key Takeaways:**
1. [Main concept 1]
2. [Main concept 2]
3. [Main concept 3]

**Looking Ahead:**
In the next chapter, we'll build on these foundations to explore [preview next chapter topic].

---

## References

[To be populated from citation tracking]

## Exercises

1. **Conceptual**: [Question testing understanding]
2. **Implementation**: [Coding exercise]
3. **Research**: [Paper analysis or extension]

EOF

echo "✅ Integration complete"
```

## Create Latest Symlink

```bash
# Create symlink to latest integration
LATEST_LINK="$INTEGRATION_DIR/chapter_${CHAPTER_ID}_latest.md"
ln -sf "$(basename "$INTEGRATED_FILE")" "$LATEST_LINK"
echo "🔗 Latest integration linked: $LATEST_LINK"
```

## Update Manifest

```bash
# Count words in integrated chapter
INTEGRATED_WORD_COUNT=$(wc -w < "$INTEGRATED_FILE")

# Update manifest
jq --arg ch "$CHAPTER_ID" \
   --arg wc "$INTEGRATED_WORD_COUNT" \
   --arg file "$INTEGRATED_FILE" \
   --arg ts "$TIMESTAMP" \
   '.chapters[$ch].status = "integrated" |
    .chapters[$ch].word_count = ($wc | tonumber) |
    .chapters[$ch].files.integrated = $file |
    .chapters[$ch].integration_date = ($ts + "Z")' \
   "$MANIFEST_FILE" > "${MANIFEST_FILE}.tmp" && \
   mv "${MANIFEST_FILE}.tmp" "$MANIFEST_FILE"

# Update project word count
TOTAL_WORDS=$(jq '[.chapters[].word_count // 0] | add' "$MANIFEST_FILE")
jq --arg tw "$TOTAL_WORDS" '.project.current_words = ($tw | tonumber)' \
   "$MANIFEST_FILE" > "${MANIFEST_FILE}.tmp" && \
   mv "${MANIFEST_FILE}.tmp" "$MANIFEST_FILE"
```

## Generate Integration Report

```bash
echo ""
echo "✅ Chapter Integration Complete!"
echo "═══════════════════════════════════════════════════════"
echo "  Chapter: $CHAPTER - $CHAPTER_TITLE"
echo "  Sections integrated: ${#SECTION_FILES[@]}"
echo "  Total words: $INTEGRATED_WORD_COUNT (target: $TARGET_WORDS)"
echo "  Output: $INTEGRATED_FILE"
echo "  Latest: $LATEST_LINK"
echo ""
echo "📊 Integration Quality Checks:"
if [ -n "$DUPLICATE_HEADINGS" ]; then
    echo "  ⚠️  Duplicate headings found (see above)"
else
    echo "  ✓ No duplicate headings"
fi
if [ -n "$TERMINOLOGY_ISSUES" ]; then
    echo "  ⚠️  Terminology inconsistencies found (see above)"
else
    echo "  ✓ Terminology appears consistent"
fi
if [ $MISSING_TRANSITIONS -gt 0 ]; then
    echo "  ⚠️  $MISSING_TRANSITIONS transition(s) may need work"
else
    echo "  ✓ Section transitions appear adequate"
fi
echo ""
echo "📝 Manual Review Needed:"
echo "  • Check TRANSITION NEEDED comments in integrated file"
echo "  • Fill in chapter summary key takeaways"
echo "  • Review and consolidate any duplicate content"
echo "  • Verify cross-references (Section X, Figure Y)"
echo "  • Ensure mathematical notation consistency"
echo ""
echo "Next steps:"
echo "  • Review integrated chapter: code $INTEGRATED_FILE"
if [ "$REVISE" != "true" ]; then
    echo "  • Revise with feedback: /integrate-chapter --chapter $CHAPTER --revise --feedback 'your feedback'"
fi
echo "  • Track citations: /track-citations \"Chapter $CHAPTER\" --add"
echo "  • Verify quality: /verify-chapter \"Chapter $CHAPTER\""
echo "  • Create review PR: /review --chapter $CHAPTER"
echo ""
echo "Total book progress: $TOTAL_WORDS words"
echo "═══════════════════════════════════════════════════════"
```

---

## Examples

```bash
# Auto-discover and integrate all section drafts for chapter 3
/integrate-chapter --chapter 3

# Integrate specific sections in order
/integrate-chapter --chapter 5 --sections "Introduction,Mathematical Framework,Implementation,Case Study"

# Revise integration based on feedback
/integrate-chapter --chapter 3 --revise --feedback "Transition between backtesting and walk-forward is too abrupt"

# Revise with focus on terminology consistency
/integrate-chapter --chapter 2 --revise --feedback "Standardize 'machine learning' vs 'ML' usage"
```

---

## Notes

**What This Command Does:**
- Loads all section drafts (auto-discover or specified)
- Analyzes for integration issues (redundancies, inconsistencies, missing transitions)
- Combines sections with transition placeholders
- Adds chapter introduction and conclusion
- Creates versioned integrated chapter
- Tracks quality issues for manual review

**What This Command Does NOT Do:**
- Does not use LLM to auto-write transitions (placeholders for human/LLM review)
- Does not auto-resolve terminology conflicts (flags for review)
- Does not merge duplicate content (flags for manual consolidation)

**Human-in-Loop Expected:**
- Review TRANSITION NEEDED comments
- Fill in key takeaways in summary
- Consolidate any flagged duplicates
- Verify cross-references

**Iteration Workflow:**
1. First integration: `/integrate-chapter --chapter N`
2. Human reviews, provides feedback
3. Revise: `/integrate-chapter --chapter N --revise --feedback "specific issue"`
4. Repeat until satisfied

*The integrate-chapter command prepares a coherent chapter draft from sections, flagging integration issues for human/LLM review and revision.*
