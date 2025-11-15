---
title: Verify Chapter
aliases: [verify, check]
---

# Verify Chapter

Citation and fact verification before finalizing to prevent post-draft rework.

## Usage

```bash
/verify-chapter "Chapter 3"              # Verify chapter draft
/verify-chapter @drafts/chapter-3.md     # Verify from file path
/verify-chapter --report                 # Show all verification reports
```

## What This Command Does

**Problem Solved**: "After drafting, realize citations are incomplete", "citations get forgotten", and "code examples untested, errors slip through"

**Proactive Verification Process**:
1. Checks citations for completeness against draft content
2. Flags unsupported factual claims needing verification
3. Tests code examples for errors
4. Validates learning outcomes structure (with backward compatibility)
   - Checks for learning_outcomes.md (new structure)
   - Falls back to outline.md (old structure)
   - Verifies outline references learning_outcomes.md correctly
5. Generates verification checklist
6. Creates verification report with issues found

**Backward Compatibility**: Supports both the new canonical structure (standalone learning_outcomes.md) and the old structure (LOs embedded in outline.md).

**Integration**: Third phase of ML4T workflow (Research → Draft → Verify)

## Prerequisites

- Chapter draft completed (via `/draft-chapter`)
- Draft file exists in `.claude/work/drafts/`
- Code examples present in draft (Python code blocks)

## Implementation

```bash
#!/bin/bash

# Standard constants
readonly CLAUDE_DIR=".claude"
readonly WORK_DIR="${CLAUDE_DIR}/work"
readonly DRAFTS_DIR="${WORK_DIR}/drafts"
readonly VERIFICATION_DIR="${WORK_DIR}/verification"

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
CHAPTER_TITLE=""
REPORT_MODE=false

if [[ "$ARGUMENTS" == "--report" ]]; then
    REPORT_MODE=true
else
    CHAPTER_TITLE="$ARGUMENTS"
    if [[ "$CHAPTER_TITLE" == @* ]]; then
        DRAFT_FILE="${CHAPTER_TITLE#@}"
        if [ ! -f "$DRAFT_FILE" ]; then
            error_exit "Draft file not found: $DRAFT_FILE"
        fi
        CHAPTER_TITLE=$(basename "$DRAFT_FILE" .md)
    fi
fi

echo "🔍 Verify Chapter"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Ensure directories exist
mkdir -p "$VERIFICATION_DIR"

# Report mode: Show all verification reports
if [ "$REPORT_MODE" = true ]; then
    if [ ! -d "$VERIFICATION_DIR" ] || [ -z "$(ls -A "$VERIFICATION_DIR" 2>/dev/null)" ]; then
        warn "No verification reports found. Run /verify-chapter [chapter] first."
        exit 0
    fi

    echo "📋 Verification Reports"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    for report in "$VERIFICATION_DIR"/*-report.md; do
        if [ -f "$report" ]; then
            chapter=$(basename "$report" -report.md)
            status=$(grep "^Status:" "$report" 2>/dev/null | cut -d: -f2- | xargs)
            echo "- $chapter: $status"
        fi
    done

    exit 0
fi

# Validate chapter provided
if [ -z "$CHAPTER_TITLE" ]; then
    error_exit "Chapter title required. Usage: /verify-chapter \"Chapter Title\""
fi

# Find draft file
CHAPTER_SLUG=$(echo "$CHAPTER_TITLE" | tr '[:upper:]' '[:lower:]' | tr -cs '[:alnum:]' '-' | sed 's/-$//')
DRAFT_FILE="${DRAFTS_DIR}/${CHAPTER_SLUG}.md"

if [ ! -f "$DRAFT_FILE" ]; then
    error_exit "Draft not found: $DRAFT_FILE. Run /draft-chapter first."
fi

VERIFICATION_REPORT="${VERIFICATION_DIR}/${CHAPTER_SLUG}-report.md"

echo "Verifying: $CHAPTER_TITLE"
echo "Draft: $DRAFT_FILE"
echo ""

# Initialize verification report
cat > "$VERIFICATION_REPORT" <<EOF
# Verification Report: $CHAPTER_TITLE

**Draft File**: $DRAFT_FILE
**Verified**: $(date +"%Y-%m-%d %H:%M:%S")
**Status**: In Progress

---

## Verification Checklist

EOF

# Check 1: Citation Completeness
echo "📚 Checking Citations..."
echo ""

CITATION_ISSUES=0

# Look for citation markers or references
CITATIONS=$(grep -c "\[.*\]" "$DRAFT_FILE" 2>/dev/null || echo "0")
REFERENCE_SECTION=$(grep -c "^## References" "$DRAFT_FILE" 2>/dev/null || echo "0")

cat >> "$VERIFICATION_REPORT" <<EOF
### 1. Citation Completeness

**Citations Found**: $CITATIONS potential citations
**Reference Section**: $([ "$REFERENCE_SECTION" -gt 0 ] && echo "Present" || echo "Missing")

EOF

if [ "$CITATIONS" -gt 0 ] && [ "$REFERENCE_SECTION" -eq 0 ]; then
    warn "Citations found but no References section"
    echo "⚠️  ISSUE: Citations present but no References section" >> "$VERIFICATION_REPORT"
    CITATION_ISSUES=$((CITATION_ISSUES + 1))
else
    success "Citation structure OK"
    echo "✅ Citation structure appears complete" >> "$VERIFICATION_REPORT"
fi

echo ""
echo "" >> "$VERIFICATION_REPORT"

# Check 2: Code Examples Validation
echo "💻 Checking Code Examples..."
echo ""

CODE_ISSUES=0

# Extract Python code blocks
CODE_BLOCKS=$(grep -c "^\`\`\`python" "$DRAFT_FILE" 2>/dev/null || echo "0")

cat >> "$VERIFICATION_REPORT" <<EOF
### 2. Code Example Validation

**Code Blocks Found**: $CODE_BLOCKS Python code blocks

EOF

if [ "$CODE_BLOCKS" -gt 0 ]; then
    info "Found $CODE_BLOCKS code blocks to validate"

    # Extract and test each code block
    awk '/^```python/,/^```/' "$DRAFT_FILE" | grep -v '^```' > /tmp/chapter_code_$$.py 2>/dev/null

    if [ -s /tmp/chapter_code_$$.py ]; then
        # Basic syntax check with Python (if available)
        if command -v python3 >/dev/null 2>&1; then
            if python3 -m py_compile /tmp/chapter_code_$$.py 2>/dev/null; then
                success "Code syntax validation passed"
                echo "✅ All code blocks have valid Python syntax" >> "$VERIFICATION_REPORT"
            else
                warn "Code syntax errors detected"
                echo "⚠️  ISSUE: Syntax errors in code examples" >> "$VERIFICATION_REPORT"
                CODE_ISSUES=$((CODE_ISSUES + 1))
            fi
        else
            info "Python not available for code validation (install python3 for validation)"
            echo "ℹ️  Python not available for validation" >> "$VERIFICATION_REPORT"
        fi
    fi

    rm -f /tmp/chapter_code_$$.py
else
    info "No code blocks found (may be expected for this chapter)"
    echo "ℹ️  No code blocks to validate" >> "$VERIFICATION_REPORT"
fi

echo ""
echo "" >> "$VERIFICATION_REPORT"

# Check 3: Factual Claims Review
echo "🔬 Checking Factual Claims..."
echo ""

# Look for strong claims that need citations
STRONG_CLAIMS=$(grep -Ei "always|never|proven|guaranteed|impossible|all |every " "$DRAFT_FILE" 2>/dev/null | wc -l)

cat >> "$VERIFICATION_REPORT" <<EOF
### 3. Factual Claims Review

**Strong Claims Detected**: $STRONG_CLAIMS instances

EOF

if [ "$STRONG_CLAIMS" -gt 10 ]; then
    warn "Many strong claims detected - verify each has citation support"
    echo "⚠️  WARNING: $STRONG_CLAIMS strong claims detected - verify citation support" >> "$VERIFICATION_REPORT"
else
    success "Moderate use of strong claims"
    echo "✅ Reasonable number of strong claims ($STRONG_CLAIMS)" >> "$VERIFICATION_REPORT"
fi

echo ""
echo "" >> "$VERIFICATION_REPORT"

# Check 4: Learning Outcomes Structure
echo "🎯 Checking Learning Outcomes Structure..."
echo ""

LO_ISSUES=0

# Determine chapter directory from draft file path or chapter title
CHAPTER_NUM=$(echo "$CHAPTER_SLUG" | grep -oP '^\d+' || echo "")
if [ -n "$CHAPTER_NUM" ]; then
    CHAPTER_DIR=$(find ~/ml4t/third_edition/chapters -maxdepth 1 -type d -name "${CHAPTER_NUM}_*" | head -1)

    if [ -n "$CHAPTER_DIR" ]; then
        LEARNING_OUTCOMES_FILE="$CHAPTER_DIR/manuscript/learning_outcomes.md"
        OUTLINE_FILE="$CHAPTER_DIR/manuscript/outline.md"

        # Check for learning_outcomes.md (new structure)
        if [ -f "$LEARNING_OUTCOMES_FILE" ]; then
            info "✅ Found learning_outcomes.md (new structure)"

            LO_COUNT=$(grep -c "^[0-9]\+\." "$LEARNING_OUTCOMES_FILE" 2>/dev/null || echo "0")

            cat >> "$VERIFICATION_REPORT" <<EOF
### 4. Learning Outcomes Structure

**Structure**: New (standalone learning_outcomes.md)
**Learning Outcomes Found**: $LO_COUNT

EOF

            # Check if outline.md references learning_outcomes.md
            if [ -f "$OUTLINE_FILE" ]; then
                if grep -q "learning_outcomes\.md" "$OUTLINE_FILE"; then
                    success "Outline correctly references learning_outcomes.md"
                    echo "✅ Outline structure correct - references learning_outcomes.md" >> "$VERIFICATION_REPORT"
                else
                    warn "Outline does not reference learning_outcomes.md"
                    echo "⚠️  ISSUE: Outline should reference learning_outcomes.md but doesn't" >> "$VERIFICATION_REPORT"
                    LO_ISSUES=$((LO_ISSUES + 1))
                fi
            fi

            success "Learning outcomes structure validated ($LO_COUNT LOs)"

        # Fall back to outline.md (old structure)
        elif [ -f "$OUTLINE_FILE" ]; then
            info "📄 Using outline.md (old structure - backward compatibility)"

            # Extract LO count from outline
            LO_COUNT=$(awk '
                /CHAPTER GUIDANCE/,/^---/ {
                    if (/Learning Outcomes:/) {
                        in_los = 1
                        next
                    }
                    if (in_los && /^[[:space:]]*\*/) {
                        count++
                    }
                    if (in_los && /^---/) {
                        exit
                    }
                }
                END {
                    print count
                }
            ' "$OUTLINE_FILE" 2>/dev/null || echo "0")

            cat >> "$VERIFICATION_REPORT" <<EOF
### 4. Learning Outcomes Structure

**Structure**: Old (LOs embedded in outline.md)
**Learning Outcomes Found**: $LO_COUNT
**Recommendation**: Consider migrating to standalone learning_outcomes.md

EOF

            if [ "$LO_COUNT" -gt 0 ]; then
                success "Learning outcomes found in outline ($LO_COUNT LOs)"
                echo "✅ Learning outcomes present in outline" >> "$VERIFICATION_REPORT"
            else
                warn "No learning outcomes found in outline"
                echo "⚠️  ISSUE: No learning outcomes found" >> "$VERIFICATION_REPORT"
                LO_ISSUES=$((LO_ISSUES + 1))
            fi

        else
            warn "Neither learning_outcomes.md nor outline.md found"
            cat >> "$VERIFICATION_REPORT" <<EOF
### 4. Learning Outcomes Structure

**Structure**: Not found
**Issue**: Neither learning_outcomes.md nor outline.md found in chapter directory

EOF
            echo "⚠️  ISSUE: Learning outcomes structure not found" >> "$VERIFICATION_REPORT"
            LO_ISSUES=$((LO_ISSUES + 1))
        fi
    else
        info "Chapter directory not found (chapter number: $CHAPTER_NUM)"
        cat >> "$VERIFICATION_REPORT" <<EOF
### 4. Learning Outcomes Structure

**Status**: Skipped (chapter directory not found)

EOF
    fi
else
    info "Cannot determine chapter number from draft file"
    cat >> "$VERIFICATION_REPORT" <<EOF
### 4. Learning Outcomes Structure

**Status**: Skipped (cannot determine chapter number)

EOF
fi

echo ""
echo "" >> "$VERIFICATION_REPORT"

# Verification Summary
TOTAL_ISSUES=$((CITATION_ISSUES + CODE_ISSUES + LO_ISSUES))

cat >> "$VERIFICATION_REPORT" <<EOF
---

## Verification Summary

**Total Issues Found**: $TOTAL_ISSUES
- Citation Issues: $CITATION_ISSUES
- Code Issues: $CODE_ISSUES
- Learning Outcomes Issues: $LO_ISSUES

**Status**: $([ "$TOTAL_ISSUES" -eq 0 ] && echo "✅ PASS - No issues found" || echo "⚠️  NEEDS ATTENTION - $TOTAL_ISSUES issues to resolve")

---

## Recommendations

EOF

if [ "$CITATION_ISSUES" -gt 0 ]; then
    echo "### Citation Completeness" >> "$VERIFICATION_REPORT"
    echo "- Add References section with full citations" >> "$VERIFICATION_REPORT"
    echo "- Verify all [citation markers] have corresponding references" >> "$VERIFICATION_REPORT"
    echo "" >> "$VERIFICATION_REPORT"
fi

if [ "$CODE_ISSUES" -gt 0 ]; then
    echo "### Code Examples" >> "$VERIFICATION_REPORT"
    echo "- Fix syntax errors in code blocks" >> "$VERIFICATION_REPORT"
    echo "- Test code examples manually to ensure correctness" >> "$VERIFICATION_REPORT"
    echo "" >> "$VERIFICATION_REPORT"
fi

if [ "$LO_ISSUES" -gt 0 ]; then
    echo "### Learning Outcomes Structure" >> "$VERIFICATION_REPORT"
    echo "- Ensure learning outcomes are properly defined" >> "$VERIFICATION_REPORT"
    echo "- For new structure: Verify outline.md references learning_outcomes.md" >> "$VERIFICATION_REPORT"
    echo "- For old structure: Consider migrating to standalone learning_outcomes.md" >> "$VERIFICATION_REPORT"
    echo "" >> "$VERIFICATION_REPORT"
fi

if [ "$TOTAL_ISSUES" -eq 0 ]; then
    echo "✅ Chapter appears ready for finalization" >> "$VERIFICATION_REPORT"
    echo "- All verification checks passed" >> "$VERIFICATION_REPORT"
    echo "- Review manual content for quality" >> "$VERIFICATION_REPORT"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Display summary
if [ "$TOTAL_ISSUES" -eq 0 ]; then
    success "Verification PASSED - No issues found"
else
    warn "Verification found $TOTAL_ISSUES issues to address"
fi

echo ""
echo "📊 Verification Results:"
echo "  - Citations: $([ "$CITATION_ISSUES" -eq 0 ] && echo "✅ OK" || echo "⚠️  $CITATION_ISSUES issues")"
echo "  - Code: $([ "$CODE_ISSUES" -eq 0 ] && echo "✅ OK" || echo "⚠️  $CODE_ISSUES issues")"
echo "  - Learning Outcomes: $([ "$LO_ISSUES" -eq 0 ] && echo "✅ OK" || echo "⚠️  $LO_ISSUES issues")"
echo "  - Claims: ℹ️  $STRONG_CLAIMS strong claims to verify"
echo ""
echo "📁 Verification Report: $VERIFICATION_REPORT"
echo ""

if [ "$TOTAL_ISSUES" -gt 0 ]; then
    info "Review report for details and fix issues before finalizing"
else
    success "Chapter ready for finalization!"
fi
```

## Success Indicators

Verification succeeds when:
- ✅ Citations checked for completeness
- ✅ Code examples validated for syntax errors
- ✅ Factual claims reviewed (strong claims identified)
- ✅ Verification report generated with findings
- ✅ Issues discovered proactively (not reactively after publishing)

## Troubleshooting

### "Draft not found"
**Problem**: Chapter draft doesn't exist
**Solution**: Run `/draft-chapter [chapter-title]` first to create draft

### "Python not available"
**Problem**: Code validation requires Python but not installed
**Solution**: Install python3 for code validation, or skip automatic validation

### "Many strong claims"
**Problem**: High number of strong claims detected
**Solution**: Review each claim for citation support, moderate language if needed

## Integration with Workflow

**Position**: Phase 3 (Research → Draft → Verify)

**Inputs**:
- Chapter title or draft file path
- Draft content with potential citations and code

**Outputs**:
- Verification report: `.claude/work/verification/[chapter]-report.md`
- Issue summary (citations, code, factual claims)
- Recommendations for fixes

**Next Step**: Address issues in draft, re-verify until clean, then finalize chapter

## Verification Checklist

Before finalizing chapter, ensure:
- ✅ All citations have corresponding references
- ✅ Reference section complete and properly formatted
- ✅ Code examples tested and working
- ✅ Strong factual claims supported by citations
- ✅ No syntax errors in code blocks
- ✅ Verification report shows PASS status
