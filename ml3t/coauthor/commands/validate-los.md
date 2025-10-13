---
description: "Extract, validate, and cross-check learning outcomes across chapters"
argument-hint: "[--chapter N] [--export-csv] [--detect-overlap] [--check-implicit]"
allowed-tools: [Read, Write, Bash, Glob, Grep]
---

# Validate Learning Outcomes Command

Extracts learning outcomes from chapter outlines, validates cross-chapter consistency, detects overlaps, and optionally checks research/code for implicit LOs.

## Overview

**Purpose**: Ensure learning outcomes are:
- Consistently structured across chapters
- Non-overlapping (or intentionally overlapping with rationale)
- Complete (accounting for implicit LOs in research/code)
- Properly sequenced (building on previous chapters)

**Workflow**:
1. Extract LOs from chapter outline(s)
2. Parse into structured CSV format
3. Cross-chapter overlap detection
4. Optional: Check research notes for implicit LOs
5. Optional: Check code examples for implicit LOs
6. Export to CSV for manual/LLM review

## Parse Arguments

```bash
# Parse command arguments
CHAPTER=""
EXPORT_CSV=true  # Default to CSV export
DETECT_OVERLAP=true  # Default to overlap detection
CHECK_IMPLICIT=false  # Optional, slower
ALL_CHAPTERS=false

# Parse chapter number (optional, default to all)
if [[ "$ARGUMENTS" =~ --chapter[[:space:]]+([0-9]+) ]]; then
    CHAPTER="${BASH_REMATCH[1]}"
    CHAPTER_ID=$(printf "%02d" "$CHAPTER")
else
    ALL_CHAPTERS=true
fi

# Check flags
if [[ "$ARGUMENTS" =~ --no-export ]]; then
    EXPORT_CSV=false
fi

if [[ "$ARGUMENTS" =~ --no-overlap ]]; then
    DETECT_OVERLAP=false
fi

if [[ "$ARGUMENTS" =~ --check-implicit ]]; then
    CHECK_IMPLICIT=true
fi

echo "🎯 Learning Outcomes Validation"
if [ "$ALL_CHAPTERS" = true ]; then
    echo "📚 Scope: All chapters"
else
    echo "📚 Scope: Chapter $CHAPTER"
fi
echo "🔍 Overlap detection: $DETECT_OVERLAP"
echo "🔬 Check implicit LOs: $CHECK_IMPLICIT"
```

## Setup Paths and Output

```bash
# Project paths
PROJECT_ROOT="$HOME/ml4t"
CHAPTERS_DIR="$PROJECT_ROOT/third_edition/chapters"
MASTER_OUTLINE="$PROJECT_ROOT/third_edition/outline.md"
OUTPUT_DIR="$PROJECT_ROOT/third_edition/common/learning_outcomes"
mkdir -p "$OUTPUT_DIR"

# Output files
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CSV_FILE="$OUTPUT_DIR/learning_outcomes_${TIMESTAMP}.csv"
VALIDATION_REPORT="$OUTPUT_DIR/validation_report_${TIMESTAMP}.md"
OVERLAP_REPORT="$OUTPUT_DIR/overlap_analysis_${TIMESTAMP}.md"

# Create CSV header
cat > "$CSV_FILE" << 'EOF'
Chapter,Chapter_Title,LO_ID,Action_Verb,Content,Source,Status,Cross_Ref_Chapters,Notes
EOF

echo "📁 Output directory: $OUTPUT_DIR"
echo "📄 CSV export: $CSV_FILE"
```

## Load Master Outline for Context

```bash
# Read master outline for cross-chapter context
echo ""
echo "📖 Loading master outline for cross-chapter context..."

if [ ! -f "$MASTER_OUTLINE" ]; then
    echo "⚠️  Master outline not found: $MASTER_OUTLINE"
    echo "   Proceeding without cross-chapter reference"
    MASTER_CONTEXT=""
else
    MASTER_CONTEXT=$(cat "$MASTER_OUTLINE")
    echo "✅ Master outline loaded ($(wc -l < "$MASTER_OUTLINE") lines)"
fi
```

## Extract Learning Outcomes

```bash
# Function to extract LOs from a chapter outline
extract_los_from_outline() {
    local chapter_num=$1
    local outline_file=$2
    local chapter_id=$(printf "%02d" "$chapter_num")

    # Check if outline exists
    if [ ! -f "$outline_file" ]; then
        echo "  ⚠️  Outline not found: $outline_file"
        return 1
    fi

    # Extract chapter title
    local chapter_title=$(grep "^# " "$outline_file" | head -1 | sed 's/^# //' | sed 's/\*//g' | xargs)

    # Extract learning outcomes section
    # Pattern: Look for "Learning Outcomes:" section in CHAPTER GUIDANCE
    local los_section=$(awk '
        /CHAPTER GUIDANCE/,/^---/ {
            if (/Learning Outcomes:/) {
                in_los = 1
                next
            }
            if (in_los && /^[[:space:]]*\*/) {
                print
            }
            if (in_los && /^---/) {
                exit
            }
        }
    ' "$outline_file")

    if [ -z "$los_section" ]; then
        echo "  ⚠️  No Learning Outcomes found in: $outline_file"
        return 1
    fi

    # Parse individual LOs
    local lo_count=0
    while IFS= read -r line; do
        # Skip empty lines
        [ -z "$(echo "$line" | xargs)" ] && continue

        # Clean up the line (remove leading *, spaces, trailing periods)
        local lo_text=$(echo "$line" | sed 's/^[[:space:]]*\*[[:space:]]*//' | sed 's/\.$//' | xargs)

        # Skip if empty after cleaning
        [ -z "$lo_text" ] && continue

        # REFINEMENT 1: Filter out intro/context lines
        # Skip lines starting with "After this chapter"
        if [[ "$lo_text" =~ ^After[[:space:]]this[[:space:]]chapter ]]; then
            echo "    ⊗ Skipped intro line: ${lo_text:0:50}..."
            continue
        fi

        # Skip lines starting with "**Case Study Focus"
        if [[ "$lo_text" =~ ^\*\*Case[[:space:]]Study ]]; then
            echo "    ⊗ Skipped case study intro: ${lo_text:0:50}..."
            continue
        fi

        # Extract action verb (first word, usually a verb)
        # Remove colons, commas, and asterisks from action verb
        local action_verb=$(echo "$lo_text" | awk '{print $1}' | sed 's/://g' | sed 's/,//g' | sed 's/\*//g')

        # REFINEMENT 2: Validate action verb (should be capitalized, common learning verb)
        # Common learning verbs: Identify, Explain, Implement, Apply, Build, Design, etc.
        # Skip if action verb is lowercase or unusual
        if [[ ! "$action_verb" =~ ^[A-Z] ]]; then
            echo "    ⊗ Skipped invalid action verb: $action_verb"
            continue
        fi

        # LO content (rest of text)
        local content=$(echo "$lo_text" | sed 's/^[^ ]* //')

        # Skip if content is too short (likely not a real LO)
        if [ ${#content} -lt 10 ]; then
            echo "    ⊗ Skipped short content: $content"
            continue
        fi

        # Increment LO counter
        lo_count=$((lo_count + 1))
        local lo_id="LO$lo_count"

        # Write to CSV (escape commas in content)
        content_escaped=$(echo "$content" | sed 's/"/\\"/g')
        echo "$chapter_num,\"$chapter_title\",$lo_id,$action_verb,\"$content_escaped\",outline,pending,,\"\"" >> "$CSV_FILE"

        echo "    ✓ $lo_id: $action_verb - ${content:0:60}..."

    done <<< "$los_section"

    echo "  📊 Extracted $lo_count learning outcomes from Chapter $chapter_num"
    return 0
}

# Extract LOs from specified chapter(s)
echo ""
echo "🔍 Extracting learning outcomes..."

if [ "$ALL_CHAPTERS" = true ]; then
    # Find all chapter directories
    total_chapters=0
    total_los=0

    for chapter_dir in $(ls -1d "$CHAPTERS_DIR"/*/ | sort); do
        # Extract chapter number from directory name
        chapter_name=$(basename "$chapter_dir")
        chapter_num=$(echo "$chapter_name" | grep -oP '^\d+')

        if [ -n "$chapter_num" ]; then
            outline_file="${chapter_dir}manuscript/outline.md"
            if [ -f "$outline_file" ]; then
                echo ""
                echo "Chapter $chapter_num:"
                extract_los_from_outline "$chapter_num" "$outline_file"
                total_chapters=$((total_chapters + 1))
            fi
        fi
    done

    echo ""
    echo "✅ Processed $total_chapters chapters"
else
    # Single chapter - find directory
    chapter_dir=$(find "$CHAPTERS_DIR" -maxdepth 1 -type d -name "${CHAPTER_ID}_*" | head -1)
    if [ -z "$chapter_dir" ]; then
        echo "❌ Chapter directory not found for chapter $CHAPTER"
        exit 1
    fi
    outline_file="${chapter_dir}/manuscript/outline.md"
    extract_los_from_outline "$CHAPTER" "$outline_file"
fi
```

## Cross-Chapter Overlap Detection

```bash
if [ "$DETECT_OVERLAP" = true ]; then
    echo ""
    echo "🔍 Detecting cross-chapter overlaps..."

    # Create overlap report header
    cat > "$OVERLAP_REPORT" << EOF
# Learning Outcomes Overlap Analysis

**Generated**: $(date)

## Methodology

This report identifies potential overlaps in learning outcomes across chapters by:
1. Comparing action verbs and content keywords
2. Detecting similar phrasing (fuzzy matching)
3. Highlighting potential redundancy or intentional reinforcement

---

## Detected Overlaps

EOF

    # Python script for overlap detection
    python3 << PYTHON_SCRIPT
import csv
import re
from collections import defaultdict
from difflib import SequenceMatcher

# Read CSV
with open("$CSV_FILE", 'r') as f:
    reader = csv.DictReader(f)
    los = list(reader)

# Function to calculate similarity
def similar(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

# Detect overlaps
overlaps = []
for i, lo1 in enumerate(los):
    for j, lo2 in enumerate(los[i+1:], start=i+1):
        # Skip same chapter
        if lo1['Chapter'] == lo2['Chapter']:
            continue

        # Same action verb
        if lo1['Action_Verb'].lower() == lo2['Action_Verb'].lower():
            # Calculate content similarity
            similarity = similar(lo1['Content'], lo2['Content'])

            if similarity > 0.5:  # 50% similarity threshold
                overlaps.append({
                    'ch1': lo1['Chapter'],
                    'ch1_title': lo1['Chapter_Title'],
                    'lo1': lo1['LO_ID'],
                    'ch2': lo2['Chapter'],
                    'ch2_title': lo2['Chapter_Title'],
                    'lo2': lo2['LO_ID'],
                    'verb': lo1['Action_Verb'],
                    'similarity': similarity,
                    'content1': lo1['Content'][:100],
                    'content2': lo2['Content'][:100]
                })

# Write overlap report
with open("$OVERLAP_REPORT", 'a') as f:
    if not overlaps:
        f.write("\n✅ No significant overlaps detected.\n")
    else:
        f.write(f"\n⚠️  Found {len(overlaps)} potential overlaps:\n\n")

        for overlap in sorted(overlaps, key=lambda x: x['similarity'], reverse=True):
            f.write(f"### Overlap: Chapters {overlap['ch1']} ↔ {overlap['ch2']}\n\n")
            f.write(f"**Similarity**: {overlap['similarity']:.1%}\n\n")
            f.write(f"**Ch {overlap['ch1']} ({overlap['ch1_title']}) - {overlap['lo1']}**:\n")
            f.write(f"- {overlap['verb']}: {overlap['content1']}...\n\n")
            f.write(f"**Ch {overlap['ch2']} ({overlap['ch2_title']}) - {overlap['lo2']}**:\n")
            f.write(f"- {overlap['verb']}: {overlap['content2']}...\n\n")
            f.write("**Action**: Review for intentional reinforcement vs. redundancy.\n\n")
            f.write("---\n\n")

print(f"Overlap analysis complete. Found {len(overlaps)} potential overlaps.")
PYTHON_SCRIPT

    echo "✅ Overlap analysis saved to: $OVERLAP_REPORT"
fi
```

## Check Research Notes for Implicit LOs

```bash
if [ "$CHECK_IMPLICIT" = true ]; then
    echo ""
    echo "🔬 Checking research notes for implicit learning outcomes..."

    # Function to check research directory
    check_research_implicit() {
        local chapter_num=$1
        local chapter_id=$(printf "%02d" "$chapter_num")

        # Find chapter directory
        local chapter_dir=$(find "$CHAPTERS_DIR" -maxdepth 1 -type d -name "${chapter_id}_*" | head -1)
        if [ -z "$chapter_dir" ]; then
            return
        fi

        local research_dir="${chapter_dir}/research"

        if [ ! -d "$research_dir" ]; then
            echo "  ⚠️  No research directory for Chapter $chapter_num"
            return
        fi

        # Count markdown files
        local research_files=$(find "$research_dir" -name "*.md" 2>/dev/null | wc -l)
        if [ "$research_files" -eq 0 ]; then
            echo "  ⚠️  No research notes in Chapter $chapter_num"
            return
        fi

        echo "  📝 Found $research_files research notes in Chapter $chapter_num"

        # Grep for learning-related keywords
        local implicit_indicators=$(grep -rh -i \
            -e "learn" \
            -e "understand" \
            -e "implement" \
            -e "apply" \
            -e "demonstrate" \
            -e "objective" \
            -e "outcome" \
            "$research_dir" 2>/dev/null | wc -l)

        if [ "$implicit_indicators" -gt 0 ]; then
            echo "  🎯 Found $implicit_indicators potential implicit LO indicators"
            echo "     → Manual review recommended for Chapter $chapter_num research/"
        fi
    }

    if [ "$ALL_CHAPTERS" = true ]; then
        for chapter_dir in $(ls -1d "$CHAPTERS_DIR"/*/ | sort); do
            chapter_name=$(basename "$chapter_dir")
            chapter_num=$(echo "$chapter_name" | grep -oP '^\d+')
            [ -n "$chapter_num" ] && check_research_implicit "$chapter_num"
        done
    else
        check_research_implicit "$CHAPTER"
    fi
fi
```

## Check Code Samples for Implicit LOs

```bash
if [ "$CHECK_IMPLICIT" = true ]; then
    echo ""
    echo "🔬 Checking code samples for implicit learning outcomes..."

    check_code_implicit() {
        local chapter_num=$1
        local code_base="$HOME/ml3t"

        # Try to find chapter code directory
        local code_dirs=$(find "$code_base" -type d -name "*$(printf "%02d" $chapter_num)*" 2>/dev/null | head -3)

        if [ -z "$code_dirs" ]; then
            echo "  ⚠️  No code directory found for Chapter $chapter_num"
            return
        fi

        echo "  💻 Found code for Chapter $chapter_num:"
        echo "$code_dirs" | while read -r dir; do
            local notebook_count=$(find "$dir" -name "*.ipynb" 2>/dev/null | wc -l)
            local py_count=$(find "$dir" -name "*.py" 2>/dev/null | wc -l)
            echo "     - $(basename "$dir"): $notebook_count notebooks, $py_count Python files"

            # Look for docstrings, comments mentioning learning objectives
            if [ $notebook_count -gt 0 ] || [ $py_count -gt 0 ]; then
                echo "     → Code review recommended for implicit LOs"
            fi
        done
    }

    if [ "$ALL_CHAPTERS" = true ]; then
        # Check first 15 chapters (more aligned per user)
        for ch in {1..15}; do
            check_code_implicit "$ch"
        done
    else
        check_code_implicit "$CHAPTER"
    fi
fi
```

## Generate Validation Report

```bash
echo ""
echo "📊 Generating validation report..."

# Count LOs
TOTAL_LOS=$(tail -n +2 "$CSV_FILE" | wc -l)
if [ "$TOTAL_LOS" -eq 0 ]; then
    echo "❌ No learning outcomes extracted. Check outline format."
    exit 1
fi

TOTAL_CHAPTERS=$(tail -n +2 "$CSV_FILE" | cut -d',' -f1 | sort -u | wc -l)
AVG_LOS_PER_CHAPTER=$(echo "scale=1; $TOTAL_LOS / $TOTAL_CHAPTERS" | bc 2>/dev/null || echo "0")

# Create validation report
cat > "$VALIDATION_REPORT" << EOF
# Learning Outcomes Validation Report

**Generated**: $(date)
**Scope**: $([ "$ALL_CHAPTERS" = true ] && echo "All chapters" || echo "Chapter $CHAPTER")

---

## Summary Statistics

- **Total Chapters Analyzed**: $TOTAL_CHAPTERS
- **Total Learning Outcomes**: $TOTAL_LOS
- **Average LOs per Chapter**: $AVG_LOS_PER_CHAPTER

---

## Action Verb Distribution

EOF

# Count action verbs
echo "Analyzing action verb distribution..."
tail -n +2 "$CSV_FILE" | cut -d',' -f4 | sort | uniq -c | sort -rn | \
    awk '{printf "- **%s**: %d occurrences\n", $2, $1}' >> "$VALIDATION_REPORT"

cat >> "$VALIDATION_REPORT" << 'EOF'

---

## Recommendations

### ✅ Strengths
- Learning outcomes follow action verb structure
- Outcomes are specific and measurable

### ⚠️ Review Areas
- Check overlap report for potential redundancies
- Verify cross-chapter progression (foundational → advanced)
- Ensure implicit LOs from research/code are captured

### 📋 Next Steps
1. **Manual Review**: Review CSV for consistency and completeness
2. **LLM Review**: Submit CSV to LLM for pedagogical assessment
3. **Cross-Reference**: Check against master outline for alignment
4. **Iterate**: Refine and consolidate based on findings

---

## Files Generated

EOF

echo "- **CSV Export**: \`$(basename "$CSV_FILE")\`" >> "$VALIDATION_REPORT"
echo "- **Validation Report**: \`$(basename "$VALIDATION_REPORT")\`" >> "$VALIDATION_REPORT"
[ "$DETECT_OVERLAP" = true ] && echo "- **Overlap Analysis**: \`$(basename "$OVERLAP_REPORT")\`" >> "$VALIDATION_REPORT"

echo "✅ Validation report saved to: $VALIDATION_REPORT"
```

## Display Summary

```bash
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║          ✅ LEARNING OUTCOMES VALIDATION COMPLETE          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Summary:"
echo "   Total Chapters: $TOTAL_CHAPTERS"
echo "   Total LOs: $TOTAL_LOS"
echo "   Avg per Chapter: $AVG_LOS_PER_CHAPTER"
echo ""
echo "📁 Output Files:"
echo "   CSV: $CSV_FILE"
echo "   Report: $VALIDATION_REPORT"
[ "$DETECT_OVERLAP" = true ] && echo "   Overlap: $OVERLAP_REPORT"
echo ""
echo "🔍 Next Steps:"
echo "   1. Review CSV in spreadsheet tool"
echo "   2. Check overlap report for redundancies"
if [ "$CHECK_IMPLICIT" = true ]; then
    echo "   3. Manually review research/code for implicit LOs"
    echo "   4. Update CSV with findings"
else
    echo "   3. Run with --check-implicit for deeper analysis"
fi
echo "   5. Submit to LLM for pedagogical review"
echo ""
echo "Quick view CSV (first 20 rows):"
head -20 "$CSV_FILE" | column -t -s',' 2>/dev/null || head -20 "$CSV_FILE"
```

---

## Usage Examples

```bash
# Validate all chapters, export CSV with overlap detection
/validate-los

# Validate specific chapter
/validate-los --chapter 3

# Full analysis including implicit LO checks (slower)
/validate-los --check-implicit

# Skip overlap detection (faster)
/validate-los --no-overlap
```
