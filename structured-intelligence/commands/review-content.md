---
description: Quality assurance command with readability metrics, Pyramid compliance, and evidence validation dashboard
system_prompt_append: |
  You are working within the Structured Intelligence Framework (SIF), a hierarchical content creation system.

  **Current Phase**: Review (Phase 5 of 5)

  This command provides comprehensive quality metrics for drafted content, validating Pyramid compliance, Diátaxis alignment, evidence coverage, and readability.
---

# SIF Command: Review Content

## Purpose

Generate comprehensive quality dashboard for drafted content, including readability metrics, Pyramid compliance validation, Diátaxis alignment check, and evidence coverage analysis.

## Usage

```bash
/review-content [section-name]
/review-content --all          # Review all drafted sections
/review-content --summary      # Quick overview only
```

## Prerequisites

- **Phase 4 Complete**: At least one section drafted in `writing-state.json`

## What This Does

1. **Validates Drafts Exist**: Checks sections have been drafted
2. **Calculates Readability**: Flesch-Kincaid Reading Ease and Grade Level
3. **Validates Pyramid Compliance**: Checks hierarchical message flow
4. **Validates Diátaxis Alignment**: Ensures mode-appropriate patterns used
5. **Reviews Evidence Coverage**: All claims have Tier 1-3 evidence
6. **Invokes Formatter Agent**: Information Mapping and plain language checks
7. **Generates Dashboard**: Comprehensive quality metrics
8. **Provides Recommendations**: Specific improvement suggestions

## State File

**Location**: `writing-state.json` in content project directory

**Updated Fields**:
```json
{
  "phase": "review-complete",
  "quality": {
    "readability": {
      "flesch_reading_ease": 65.2,
      "flesch_kincaid_grade": 8.5,
      "target_audience": "general_public"
    },
    "pyramid_compliance": {
      "score": 0.92,
      "violations": [],
      "recommendations": []
    },
    "diataxis_alignment": {
      "mode": "explanation",
      "score": 0.88,
      "pattern_adherence": "strong"
    },
    "evidence_coverage": {
      "claims_total": 15,
      "claims_with_evidence": 15,
      "tier_4_violations": 0,
      "coverage_percentage": 100
    },
    "overall_score": 0.90,
    "recommendations": []
  }
}
```

## Command Flow

```
1. Load writing-state.json
2. Validate drafts exist
3. For each section:
   a. Calculate readability metrics
   b. Validate Pyramid compliance
   c. Validate Diátaxis alignment
   d. Review evidence coverage
   e. Invoke formatter agent for Information Mapping check
4. Compile quality dashboard
5. Generate recommendations
6. Update writing-state.json
7. Display dashboard
8. Prompt: Ready to finalize or make improvements?
```

## Quality Metrics

### 1. Readability (Flesch-Kincaid)

**Flesch Reading Ease** (0-100 scale):
- 90-100: Very easy (5th grade)
- 80-89: Easy (6th grade)
- 70-79: Fairly easy (7th grade)
- 60-69: Standard (8th-9th grade)
- 50-59: Fairly difficult (10th-12th grade)
- 30-49: Difficult (college)
- 0-29: Very difficult (graduate)

**Flesch-Kincaid Grade Level**: U.S. school grade required to understand text

**Calculation**:
```
Reading Ease = 206.835 - (1.015 × ASL) - (84.6 × ASW)
Grade Level = (0.39 × ASL) + (11.8 × ASW) - 15.59

Where:
ASL = Average Sentence Length (words per sentence)
ASW = Average Syllables per Word
```

**Target Ranges by Content Type**:
- Website/Blog: 60-70 (8th-9th grade)
- Technical Documentation: 50-60 (10th-12th grade)
- Academic Paper: 30-50 (college)
- Book Chapter: 55-65 (9th-11th grade)

### 2. Pyramid Compliance

**Checks**:
- ✅ Each paragraph supports parent message
- ✅ MECE structure maintained (no overlap or gaps)
- ✅ Answer-first, support-second ordering
- ✅ Hierarchical depth appropriate (2-4 levels typically)

**Scoring**: 0-1.0 scale
- 0.90-1.0: Excellent compliance
- 0.75-0.89: Good, minor issues
- 0.60-0.74: Fair, needs improvement
- <0.60: Poor, major restructuring needed

### 3. Diátaxis Alignment

**Checks per Mode**:

**Tutorial**:
- Action-oriented topic sentences
- Step-by-step progression
- Verification at each stage
- Encouraging tone

**How-To**:
- Problem-solution structure
- Minimal explanation
- Troubleshooting included
- Direct, imperative

**Reference**:
- Comprehensive coverage
- Neutral tone
- Types and constraints specified
- Edge cases documented

**Explanation**:
- Concept + Analogy patterns
- "Why" addressed
- Historical/theoretical context
- Thought-provoking

**Scoring**: 0-1.0 scale based on pattern adherence

### 4. Evidence Coverage

**Metrics**:
- Total claims found
- Claims with Tier 1-3 evidence
- Tier 4 violations
- Coverage percentage
- Evidence quality distribution (Tier 1 vs 2 vs 3)

**Passing**: 100% of claims with Tier 1-3 evidence, 0 Tier 4 violations

### 5. Information Mapping

**Checks** (via formatter agent):
- F-shaped reading pattern optimization
- Chunking (5-9 items per group)
- Scannability (headings, lists, bold)
- Visual hierarchy
- Whitespace usage

**Scoring**: Qualitative assessment (Excellent/Good/Fair/Poor)

### 6. Plain Language

**Checks** (via formatter agent):
- Active voice percentage (target: >80%)
- Sentence length (target: <25 words average)
- Jargon usage (technical terms explained on first use)
- Clarity issues (nominalization, passive voice, weak verbs)

## Example Output

### Dashboard Display

```
============================================
   SIF QUALITY DASHBOARD
============================================

Document: ML4T Chapter 01 - Introduction
Mode: Explanation
Sections Reviewed: 1
Word Count: 2,847

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 READABILITY METRICS

Flesch Reading Ease:     62.3  [Standard]
Flesch-Kincaid Grade:    9.2   [9th grade]
Target Audience:         General Technical (8th-10th grade)

✅ On target for book content (target: 55-65)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔺 PYRAMID COMPLIANCE

Score: 0.92  [Excellent]

✅ Hierarchical flow maintained
✅ MECE structure validated
✅ Answer-first ordering present
⚠️  1 minor issue found

Issues:
  - Paragraph 8 (line 143): Could strengthen connection to section message
    Suggestion: Add transition sentence referencing "balancing depth with accessibility"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📐 DIÁTAXIS ALIGNMENT

Mode: Explanation
Score: 0.88  [Strong Adherence]

✅ Concept + Analogy patterns used (9 instances)
✅ "Why" questions addressed throughout
✅ Historical context provided
✅ Thought-provoking insights present
⚠️  Could add 1-2 more analogies for abstract concepts

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ EVIDENCE COVERAGE

Claims Found:            15
Claims with Evidence:    15
Tier 4 Violations:       0
Coverage:                100%  ✅

Evidence Quality:
  Tier 1 (Peer-reviewed):  8  (53%)
  Tier 2 (Industry):       5  (33%)
  Tier 3 (Internal):       2  (13%)

✅ All claims properly evidenced

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 INFORMATION MAPPING

Visual Hierarchy:   Excellent
Scannability:       Good
Chunking:           Good
F-Pattern Opt:      Good

Notes:
  - Strong use of headings and subheadings
  - Lists used appropriately for bullet points
  - Consider adding 1-2 more visual breaks in longest section

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✍️  PLAIN LANGUAGE

Active Voice:       84%  ✅ (target: 80%+)
Avg Sentence:       18.3 words  ✅ (target: <25)
Jargon Explained:   Yes  ✅
Clarity Issues:     2 flagged

Issues:
  - Line 87: Nominalization "utilization of" → "using"
  - Line 143: Weak verb "facilitate" → "enable" or "allow"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⭐ OVERALL SCORE: 0.90  [Excellent]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 RECOMMENDATIONS

Priority: High
  • None

Priority: Medium
  • Strengthen paragraph 8 connection to section message
  • Add 1-2 analogies for abstract concepts (lines 87, 143)

Priority: Low
  • Replace "utilization of" with "using" (line 87)
  • Replace "facilitate" with "enable" (line 143)
  • Add visual break in long section (after paragraph 12)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next Actions:
  • /draft-section [next-section]  # Continue drafting
  • Apply recommended improvements  # Manual edits
  • Export final draft              # Ready for publication

============================================
```

## Integration with Other Commands

### Prerequisites
- `/draft-section` - Generates content to review

### Next Steps
- Apply recommendations manually
- `/draft-section [next-section]` - Continue if more sections needed
- Export final content when satisfied

## Flags

### `--all`
Review all drafted sections:
```bash
/review-content --all
```

### `--summary`
Quick overview only (no detailed issues):
```bash
/review-content --summary
```

### `--export`
Export quality report to markdown file:
```bash
/review-content --all --export quality-report.md
```

## Agent Invocation

### formatter Agent (TASK-012)

**Purpose**: Information Mapping and plain language analysis

**Input**:
- Draft content markdown
- Target readability level
- Diátaxis mode

**Output**:
- Information Mapping score
- Plain language metrics
- Specific formatting recommendations

## Notes

### Readability Calculation

**Simple Bash Implementation** (no external dependencies):

```bash
#!/bin/bash
# Calculate Flesch-Kincaid metrics

text="$1"

# Count sentences (. ! ?)
sentences=$(echo "$text" | grep -o '[.!?]' | wc -l)

# Count words
words=$(echo "$text" | wc -w)

# Count syllables (approximate: vowel groups)
syllables=$(echo "$text" | tr '[:upper:]' '[:lower:]' | grep -o '[aeiouy]\+' | wc -l)

# Calculate metrics
asl=$(echo "scale=2; $words / $sentences" | bc)
asw=$(echo "scale=2; $syllables / $words" | bc)

reading_ease=$(echo "scale=1; 206.835 - (1.015 * $asl) - (84.6 * $asw)" | bc)
grade_level=$(echo "scale=1; (0.39 * $asl) + (11.8 * $asw) - 15.59" | bc)

echo "Reading Ease: $reading_ease"
echo "Grade Level: $grade_level"
```

**Alternative**: Use Python with `textstat` library if available (more accurate)

### Performance

- **Single Section**: 1-2 minutes
- **Full Document** (5 sections): 5-10 minutes
- **Dashboard Generation**: <30 seconds

### Iteration

Can re-run after making improvements to see updated scores.

## Summary

**review-content** provides comprehensive quality assurance by:
1. Calculating Flesch-Kincaid readability metrics
2. Validating Pyramid Principle compliance
3. Checking Diátaxis mode alignment
4. Reviewing evidence coverage (Tier 1-3 only)
5. Invoking formatter agent for Information Mapping and plain language
6. Generating actionable recommendations
7. Producing visual quality dashboard

**Output**: Comprehensive quality report with specific improvement recommendations.

---

**Phase**: 5 (Review & Quality)
**Dependencies**: Phase 4 complete (drafts exist)
**Tools**: formatter agent (TASK-012), readability calculation
