---
description: Generate SCQA-based proposals for decision-making or persuasive communication
system_prompt_append: |
  You are working within the Structured Intelligence Framework (SIF).

  This utility command generates structured proposals using SCQA framework (Situation-Complication-Question-Answer) with evidence-first enforcement.
---

# SIF Utility: Propose

## Purpose

Generate persuasive proposals using SCQA framework with Pyramid Principle structure and evidence-first v2.0.0 compliance.

## Usage

```bash
/propose [topic]
/propose "Migrate to TypeScript"
/propose --template business  # Business proposal template
/propose --template technical  # Technical proposal template
```

## What This Does

1. **Invokes analyst agent** - Pyramid Principle expert for SCQA structure
2. **Applies SCQA framework** - Situation → Complication → Question → Answer
3. **Enforces evidence-first** - All claims require Tier 1-3 evidence
4. **Generates proposal document** - Markdown format with proper structure
5. **Validates pyramid compliance** - Hierarchical message flow

## SCQA Framework

**Situation**: Establish context (what's the current state?)
**Complication**: Identify problem (what's wrong or what's changing?)
**Question**: Pose the key question (what should we do?)
**Answer**: Provide recommendation (here's what to do and why)

## Output Structure

```markdown
# Proposal: [Topic]

## Situation
[Current state, context, background - 2-3 paragraphs]

## Complication
[Problem, challenge, or opportunity - 2-3 paragraphs]

## Question
[Key decision question - 1-2 sentences]

## Answer (Recommendation)
[Recommended action with supporting arguments - 3-5 paragraphs]

### Supporting Arguments
1. **Argument 1**: [Evidence-backed reasoning]
2. **Argument 2**: [Evidence-backed reasoning]
3. **Argument 3**: [Evidence-backed reasoning]

### Implementation
[High-level approach - 2-3 paragraphs]

### Risks and Mitigation
[Anticipated risks and how to address - bullets]

## Evidence
[All cited sources with tiers]
```

## Templates

### Business Proposal
- Focuses on ROI, business impact
- Financial evidence preferred
- Executive summary included

### Technical Proposal
- Focuses on architecture, implementation
- Technical evidence (benchmarks, case studies)
- Implementation details included

## Integration

**Uses**:
- `agents/analyst.md` (TASK-018) - SCQA structure expert
- `agents/evidence-validator.md` - Tier 1-3 enforcement
- `skills/scqa-framework/SKILL.md` - SCQA methodology
- `skills/pyramid-principle/SKILL.md` - Hierarchical structure

**Output**: Proposal markdown file in current directory

## Example

```bash
/propose "Adopt React for frontend development"
```

**Generated**:
```markdown
# Proposal: Adopt React for Frontend Development

## Situation
Our current frontend uses jQuery with custom JavaScript, built over 5 years...
[Evidence: codebase metrics]

## Complication
Maintenance costs are increasing 20% annually. New feature development
takes 3x longer than industry benchmarks...
[Evidence: internal metrics, industry data]

## Question
Should we migrate to React for our frontend framework?

## Answer (Recommendation)
Yes. Migrate to React incrementally over 12 months...

### Supporting Arguments
1. **Developer productivity**: React reduces development time by 40% (Stack Overflow 2024)
2. **Ecosystem**: 200K+ React packages, vs. 50K jQuery plugins
3. **Maintainability**: Component model reduces code duplication by 60% (internal analysis)

...
```

---

**Status**: Utility command (optional but useful)
**Dependencies**: TASK-002 (SCQA skill), TASK-018 (analyst agent)
