---
description: Editorial review of draft against positioning, quality standards, and effectiveness criteria
task_type: review
requires_agent: editor
requires_state: drafted
---

# /review - Editorial Review

**Purpose**: Conduct editorial review of draft against positioning manifest, quality standards, and effectiveness criteria. Provide specific, actionable feedback.

**Philosophy**: Editor enforces standards and positioning, suggests improvements, but doesn't rewrite. Author retains ownership.

---

## Usage

```bash
/review [content-piece-name] [optional: draft-version]
```

**Examples**:
```bash
/review caf-white-paper
/review landing-page v2
/review blog-post
```

---

## Prerequisites

**Required**:
- ✅ Positioning manifest exists
- ✅ Draft exists (draft-v1.md or specified version)
- ✅ Work unit in "drafted" state

---

## What This Command Does

1. **Loads all context**:
   - Positioning manifest (validation criteria)
   - Research report (evidence checking)
   - Outline (structure comparison)
   - Draft (content to review)
2. **Invokes editor agent** to conduct systematic review
3. **Evaluates draft across dimensions**:
   - Positioning adherence
   - Quality standards
   - Evidence and accuracy
   - Writing effectiveness
4. **Generates editorial feedback** with specific suggestions
5. **Assigns severity** (critical, important, minor, optional)
6. **Updates state** to "reviewed"

---

## Editorial Review Output

**File**: `.claude/work/content/[content-piece-name]/editorial-review-v1.md`

**Structure**:
```markdown
# Editorial Review: [Content Piece Name] - Draft v1

**Reviewer**: editor agent
**Date**: [Timestamp]
**Draft Word Count**: [Count]
**Overall Assessment**: [Pass with minor revisions / Requires revision / Requires substantial rework]

---

## Executive Summary

**Strengths**:
- [3-5 key strengths]

**Areas for Improvement**:
- [3-5 key areas]

**Recommendation**: [Pass with revisions / Revise and re-review / Substantial rework needed]

---

## Positioning Adherence

### Core Message Delivery
**Status**: ✓ Pass / ⚠ Needs improvement / ✗ Issue
**Assessment**: [How well core message is delivered]
**Location**: [Where core message appears]
**Feedback**: [Specific suggestions if needed]

### Desired Action Clarity
**Status**: ✓ Pass / ⚠ Needs improvement / ✗ Issue
**Assessment**: [How clear and compelling the CTA is]
**Location**: [Where CTA appears]
**Feedback**: [Specific suggestions if needed]

### Scope Discipline
**Status**: ✓ Pass / ⚠ Needs improvement / ✗ Issue
**Assessment**: [Whether NOT-covering topics excluded]
**Violations**: [Any scope creep identified]
**Feedback**: [What to cut or reframe]

### Length Constraint
**Status**: ✓ Pass / ⚠ Needs improvement / ✗ Issue
**Word Count**: [Actual] / [Max from positioning]
**Assessment**: [Within limit or needs cutting]
**Feedback**: [Where to cut if needed]

### Tone and Reading Level
**Status**: ✓ Pass / ⚠ Needs improvement / ✗ Issue
**Expected**: [From positioning manifest]
**Actual**: [What draft delivers]
**Feedback**: [Adjustments needed]

---

## Quality Standards

### Clarity and Precision
**Assessment**: [How clear and precise the writing is]
**Issues**: [Specific sections with clarity problems]
**Suggestions**: [How to improve]

### Evidence and Support
**Assessment**: [How well claims are supported]
**Unsupported Claims**: [List any found]
**Citation Quality**: [How well research integrated]
**Suggestions**: [What evidence to add/improve]

### Structure and Flow
**Assessment**: [How well content flows]
**Issues**: [Jarring transitions, disjointed sections]
**Suggestions**: [How to improve flow]

### Engagement
**Assessment**: [How engaging content is]
**Issues**: [Boring sections, weak hooks]
**Suggestions**: [How to increase engagement]

### Technical Accuracy
**Assessment**: [Factual correctness]
**Issues**: [Any inaccuracies found]
**Suggestions**: [Corrections needed]

### Visual Elements
**Existing Visuals Assessment**: [Quality and effectiveness of any diagrams, charts, or images already present]
**Visualization Opportunities**: [Sections where visuals would significantly improve comprehension]
**Suggestions**: [Describe WHAT to visualize and WHY - tool selection handled separately]

---

## Detailed Feedback by Section

### Opening
**Assessment**: [Strength and effectiveness]
**Issues**:
- [Issue 1 - Severity: Critical/Important/Minor]
- [Issue 2 - Severity: Critical/Important/Minor]
**Suggestions**:
- [Suggestion 1]
- [Suggestion 2]

### [Argument 1 Title]
**Assessment**: [Strength and effectiveness]
**Issues**:
- [Issue 1 - Severity: Critical/Important/Minor]
**Suggestions**:
- [Suggestion 1]

### [Argument 2 Title]
[Same structure]

### [Argument 3 Title]
[Same structure]

### Closing
**Assessment**: [Strength and effectiveness]
**Issues**:
- [Issue 1 - Severity: Critical/Important/Minor]
**Suggestions**:
- [Suggestion 1]

---

## Action Items for Revision

### Critical (Must address before approval)
1. [Critical issue 1]
2. [Critical issue 2]

### Important (Should address)
1. [Important issue 1]
2. [Important issue 2]

### Minor (Optional improvements)
1. [Minor issue 1]
2. [Minor issue 2]

---

## Effectiveness Assessment

**Does this serve the content purpose?**
[Yes/Partially/No + explanation]

**Would target audience take desired action?**
[Yes/Probably/Unlikely + reasoning]

**Is positioning clear vs alternatives?**
[Yes/Partially/No + assessment]

**Does core message stick?**
[Yes/Probably/No + why]

---

## Recommendation

**Action**: [Pass with minor edits / Revise per feedback / Substantial rework]

**Rationale**: [Why this recommendation]

**Next Steps**: [What author should do]

**Timeline**: [Expected revision duration]
```

---

## Editor Agent Responsibilities

**The editor agent**:
1. Reviews draft systematically across all dimensions
2. Validates against positioning manifest strictly
3. Checks research integration and evidence
4. Evaluates writing quality (clarity, engagement, flow)
5. Assesses effectiveness (would reader take desired action?)
6. Provides specific, actionable feedback (not just critique)
7. Assigns severity to issues (critical/important/minor)
8. Suggests concrete improvements
9. Maintains encouraging tone (author collaboration, not adversarial)
10. Documents all findings in structured review

**NOT the editor's job**:
- ❌ Rewrite content (suggest, don't do)
- ❌ Change positioning (that's fixed, enforce it)
- ❌ Add scope (enforce NOT-covering list)
- ❌ Be vague ("improve this section" → "Add transition sentence connecting to previous point")

---

## Review Dimensions

### 1. Positioning Adherence (Pass/Fail Criteria)
**Must pass**:
- ✅ Core message delivered prominently
- ✅ Desired action clear and compelling
- ✅ NOT-covering topics excluded
- ✅ Length ≤ max_length_words
- ✅ Tone matches positioning

**Failure in any = revision required**

### 2. Quality Standards (Improvement Criteria)
**Evaluate**:
- Clarity (can audience understand?)
- Evidence (are claims supported?)
- Structure (does it flow logically?)
- Engagement (will audience keep reading?)
- Accuracy (are facts correct?)
- Visual support (do visuals aid comprehension?)

**Score per dimension, suggest improvements**

### 3. Effectiveness (Purpose Criteria)
**Ultimate test**:
- Does this achieve content_purpose?
- Would target audience take desired action?
- Is positioning clear and compelling?
- Does core message stick?

**If "no" to any, identify why and suggest fixes**

---

## Severity Levels

**Critical** (Must fix before approval):
- Positioning violations (scope creep, wrong tone)
- Factual inaccuracies
- Exceeds length constraint
- Core message unclear or missing
- CTA weak or missing

**Important** (Should fix):
- Unclear sections
- Unsupported claims
- Flow problems
- Weak transitions
- Evidence gaps
- Missing visualizations for complex concepts

**Minor** (Optional improvements):
- Wordsmithing
- Style consistency
- Citation formatting
- Nice-to-have examples
- Visual polish for existing diagrams

**Optional** (Suggestions only):
- Alternative phrasings
- Additional examples
- Stylistic preferences

---

## State Management

**Updates work unit state**:
```json
{
  "phase": "reviewed",
  "timestamp": "2025-10-31T23:00:00Z",
  "review_version": 1,
  "overall_assessment": "pass_with_revisions",
  "critical_issues": 2,
  "important_issues": 5,
  "minor_issues": 3,
  "next_command": "/revise"
}
```

**Preserves files**:
- All inputs unchanged
- Draft unchanged
- editorial-review-v1.md created

---

## Example Session

```bash
$ /review caf-white-paper

Loading context...
✓ Positioning manifest loaded
✓ Research report loaded
✓ Outline loaded
✓ Draft v1 loaded (3150 words)

Invoking editor agent for systematic review...

Evaluating positioning adherence:
✓ Core message: Delivered in opening and reinforced in closing
⚠ Desired action: CTA present but could be more prominent
✓ Scope discipline: NOT-covering topics excluded
✓ Length: 3150 / 3500 (within limit)
✓ Tone: Technical, appropriate for audience

Evaluating quality standards:
✓ Clarity: Generally clear, 2 sections need improvement
⚠ Evidence: 3 claims need better support
✓ Structure: Flow is logical
✓ Engagement: Strong, minor improvements possible
✓ Accuracy: Factually correct

Evaluating effectiveness:
✓ Serves content purpose: Yes
✓ Would drive action: Probably (CTA could be stronger)
✓ Positioning clear: Yes
✓ Core message sticks: Yes

Overall assessment: PASS WITH REVISIONS
- Critical issues: 0
- Important issues: 4 (CTA prominence, 3 evidence gaps)
- Minor issues: 5 (clarity tweaks, flow improvements)

Editorial review created: .claude/work/content/caf-white-paper/editorial-review-v1.md
✓ Recommendation: Revise per feedback, no re-review needed
✓ Next command: /revise

Editorial review complete. Ready for author revision.
```

---

## Validation Rules

**Review must include**:
- ✅ Assessment across all positioning dimensions
- ✅ Assessment across all quality dimensions
- ✅ Specific issues identified (not vague)
- ✅ Concrete suggestions (actionable)
- ✅ Severity assignments
- ✅ Overall recommendation
- ✅ Action items for revision

**Quality checks**:
- Every issue has specific location
- Every suggestion is actionable
- Feedback is constructive, not just critical
- Encourages author, maintains collaboration

---

## Common Review Patterns

### Pattern 1: Positioning Violation
**Issue**: Draft includes NOT-covering topic "development history"
**Severity**: Critical
**Feedback**: "Section 2.3 discusses framework development process. This violates NOT-covering list from positioning. Cut this section and expand section 2.2 on usage patterns instead."

### Pattern 2: Evidence Gap
**Issue**: Claim unsupported by research
**Severity**: Important
**Feedback**: "Claim 'domain-specific agents improve productivity by 30%' needs citation. Research report Finding 3 supports this - add citation and brief explanation."

### Pattern 3: Clarity Problem
**Issue**: Jargon-heavy explanation
**Severity**: Minor
**Feedback**: "Paragraph 2 in section 3.1 uses 'stateless execution model' without explanation. Add one-sentence clarification for readers unfamiliar with term."

### Pattern 4: Flow Issue
**Issue**: Jarring transition
**Severity**: Important
**Feedback**: "Transition from section 2 to section 3 is abrupt. Add transition sentence: 'Having established what CAF provides, let's examine how it works in practice.'"

### Pattern 5: Weak CTA
**Issue**: Call to action buried
**Severity**: Critical
**Feedback**: "CTA is one sentence in final paragraph. Create dedicated section with: (1) Clear next step (2) GitHub link (3) Expected time investment (5 minutes). Make this prominent and easy to act on."

### Pattern 6: Missing Visualization
**Issue**: Dense conceptual content without visual aid
**Severity**: Important
**Feedback**: "Section 2.1 describes three-tier architecture with multiple components and data flows. This would benefit from an architecture diagram showing: (1) the three tiers (2) component relationships (3) data flow direction. Readers need a mental model before diving into details."

### Pattern 7: Visualization Opportunity - Decision Framework
**Issue**: Complex decision logic described in prose
**Severity**: Important
**Feedback**: "Section 3.2 walks through 'if X then Y, otherwise Z' decision logic across 4 paragraphs. Replace with a decision tree or flowchart showing: starting question, branch conditions, and recommended outcomes. This is the 'TL;DR' readers will remember."

### Pattern 8: Visualization Opportunity - Comparison
**Issue**: Multiple options compared in text
**Severity**: Minor
**Feedback**: "Section 4 compares three approaches across five dimensions. Consider a comparison table or matrix showing: approaches as columns, evaluation criteria as rows, with clear indicators (checkmarks, ratings, or brief notes)."

### Pattern 9: Visualization Opportunity - Process/Sequence
**Issue**: Multi-step process buried in paragraphs
**Severity**: Important
**Feedback**: "The deployment workflow in section 5.1 has 6 steps with branching. A sequence diagram or numbered flowchart would make this scannable. Show: actors involved, step sequence, decision points, and outcomes."

### Pattern 10: Visualization Opportunity - Data/Metrics
**Issue**: Numerical evidence presented as prose
**Severity**: Minor
**Feedback**: "Section 3.3 cites benchmark results across 4 systems. Consider a bar chart or data table showing: system names, metric values, and baseline comparison. Visual comparison is more impactful than 'System A achieved 87% while System B achieved 72%...'"

### Pattern 11: Ineffective Existing Visual
**Issue**: Diagram doesn't serve its purpose
**Severity**: Important
**Feedback**: "The architecture diagram in section 2 is too complex - 15+ components with crossing lines. Split into: (1) high-level overview showing main subsystems (2) detailed views for each subsystem. One diagram per concept."

---

## Visualization Suggestion Guidelines

**When suggesting visualizations, specify:**

1. **Location**: Which section/paragraph needs the visual
2. **Purpose**: What comprehension problem it solves
3. **Content**: What concepts/relationships to show
4. **Type suggestion** (optional): diagram, chart, table, infographic

**Do NOT specify:**
- Tool or technology (D2, matplotlib, Figma)
- Detailed styling (colors, fonts, layout engine)
- File formats or dimensions

**Example good suggestion:**
> "Section 3.2 would benefit from a decision tree showing the XAI method selection process. Show: starting question ('What are you explaining?'), main branches (tabular vs LLM/GenAI), and recommended methods at leaf nodes. Include common pitfalls as warning callouts."

**Example poor suggestion:**
> "Add a diagram here using D2 with --layout elk and theme 200."

The author/tooling will determine the best implementation approach.

---

## When to Request Re-Review

**Re-review needed when**:
- Multiple critical issues found
- Substantial rework required
- Positioning violations widespread
- Author requested second review after major revision

**Re-review NOT needed when**:
- Minor issues only
- Feedback is clear and actionable
- Author capable of addressing without guidance
- One revision cycle sufficient

**Editor signals**: "Recommendation: Revise and re-review" vs "Recommendation: Revise per feedback, approval expected"

---

## Integration with Content Workflow

**Standard workflow**:
```
/position → /research → /outline → /draft → /review → /revise → /approve
```

**Iteration if needed**:
```
/draft → /review → /revise → /review → /revise → /approve
```

**Review enables revision**:
- Author receives specific, actionable feedback
- Severity guides prioritization
- Revision addresses feedback systematically

---

## Success Criteria

**Review succeeds when**:
- ✅ Systematic evaluation across all dimensions
- ✅ Specific issues identified with locations
- ✅ Actionable suggestions provided
- ✅ Severity assigned to prioritize work
- ✅ Clear recommendation given
- ✅ Author knows exactly what to do next

**Review fails when**:
- ❌ Vague feedback ("improve section 2")
- ❌ No severity assignment (what's critical vs nice-to-have?)
- ❌ Missing dimensions (forgot to check positioning?)
- ❌ Adversarial tone (demoralizing author)
- ❌ Rewriting instead of suggesting

**In failure case**: Editor agent revisits with focus on specificity and actionability.

---

## Technical Notes

**File-Based Persistence**:
- Review stored as markdown
- All feedback documented
- Version-controllable
- Tracks review history

**Idempotency**:
- Can review same draft multiple times
- Creates new review file (review-v2.md)
- Useful after partial revisions

**Agent Invocation**:
- Uses editor agent (see agents/editor.md)
- Moderate duration (30-60 minutes for thorough review)

---

**Command Version**: 1.0
**Created**: 2025-10-31
**Agent**: editor
**Previous Command**: /draft
**Next Command**: /revise or /approve (if minor)
**Key Innovation**: Systematic review with severity assignment and specific, actionable feedback
