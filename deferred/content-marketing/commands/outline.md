---
description: Generate hierarchical outline using pyramid principle, constrained by positioning and informed by research
task_type: outlining
requires_agent: architect
requires_state: researched
requires_skill: pyramid-principle
---

# /outline - Pyramid Outline Generation

**Purpose**: Generate hierarchical outline that structures content using pyramid principle, constrained by positioning manifest, and informed by research findings.

**Philosophy**: Answer first, then supporting points. Core message at apex, evidence-based structure, every element serves positioning.

---

## Usage

```bash
/outline [content-piece-name]
```

**Examples**:
```bash
/outline caf-white-paper
/outline landing-page
/outline blog-post
```

---

## Prerequisites

**Required**:
- ✅ Positioning manifest must exist (from /position)
- ✅ Research report must exist (from /research)
- ✅ Work unit must be in "researched" state

**Checks**:
```bash
# Verify prerequisites
if [ ! -f positioning-manifest.json ]; then
  echo "Error: Run /position first"
  exit 1
fi

if [ ! -f research-report.md ]; then
  echo "Error: Run /research first"
  exit 1
fi
```

---

## What This Command Does

1. **Loads positioning manifest** (strategic constraints)
2. **Loads research report** (evidence and findings)
3. **Invokes architect agent** with pyramid-principle skill
4. **Generates hierarchical outline**:
   - Core message at apex (from positioning)
   - Supporting arguments (from research)
   - Evidence placement (from findings)
   - Logical flow toward desired action
5. **Validates against constraints**:
   - Estimated word count within max_length_words
   - NOT-covering topics excluded
   - Structure guides toward desired action
6. **Updates state** to "outlined"

---

## Pyramid Principle Structure

**Foundation**: Barbara Minto's pyramid principle

**Core concept**: Answer first, then supporting arguments, then details

**Structure**:
```
                  [Core Message]
                       |
        ┌──────────────┼──────────────┐
        |              |              |
   [Argument 1]   [Argument 2]   [Argument 3]
        |              |              |
    [Details]      [Details]      [Details]
```

**Applied to content**:
```
Level 1: Core message (what reader should remember)
Level 2: Major supporting arguments (why core message is true)
Level 3: Evidence and examples (what proves arguments)
Level 4: Details and elaboration (depth as needed)
```

**See**: skills/pyramid-principle.md for complete explanation

---

## Outline Output

**File**: `.workspace/work/content/[content-piece-name]/outline.md`

**Structure**:
```markdown
# Outline: [Content Piece Name]

## Positioning Constraints

**Core Message**: [From positioning manifest]
**Desired Action**: [From positioning manifest]
**Max Length**: [From positioning manifest]
**NOT Covering**: [From positioning manifest]

## Structure Overview

**Opening**: Hook + core message delivery
**Body**: 3-5 major supporting arguments
**Closing**: Reinforce message + call to action

**Estimated Word Count**: [Total estimate with breakdown]

## Detailed Outline

### Opening (Estimated: 150 words)

**Hook**: [How we capture attention]
- Audience pain point or intriguing question
- Source: [Research finding reference]

**Core Message Delivery**: [State core message clearly]
- Why this matters to reader
- What they'll gain from reading

**Transition**: [Bridge to first argument]

---

### Argument 1: [Argument Title] (Estimated: 400 words)

**Claim**: [What we're asserting]
**Evidence**: [Research findings that support this]
- Finding 1 from research (citation)
- Finding 2 from research (citation)

**Structure**:
1. State argument clearly
2. Provide evidence from research
3. Show relevance to core message
4. Include example if helpful

**Key Points**:
- Point 1
- Point 2
- Point 3

**Transition**: [Bridge to next argument]

---

### Argument 2: [Argument Title] (Estimated: 400 words)

[Same structure as Argument 1]

---

### Argument 3: [Argument Title] (Estimated: 400 words)

[Same structure as Argument 1]

---

### Closing (Estimated: 150 words)

**Reinforce Core Message**: [Restate core message with impact]

**Call to Action**: [Specific desired action from positioning]
- Make it clear and easy
- Remove friction
- Create urgency if appropriate

**Final Thought**: [Memorable closing]

---

## Research Mapping

**Finding 1**: Used in Argument 1, Section X
**Finding 2**: Used in Argument 2, Section Y
**Finding 3**: Used in Argument 3, Section Z
...

**Exclusions Applied**:
- [NOT-covering topic 1]: Excluded per positioning
- [NOT-covering topic 2]: Excluded per positioning

---

## Validation Checklist

Structure validates against positioning:
- [ ] Core message clearly delivered in opening
- [ ] Every argument supports core message
- [ ] Structure guides toward desired action
- [ ] Call to action matches positioning
- [ ] Estimated length within max_length_words (±10%)
- [ ] NOT-covering topics excluded
- [ ] Tone appropriate for target audience

Evidence validates against research:
- [ ] Every claim has supporting research
- [ ] Evidence citations mapped
- [ ] No unsupported assertions
- [ ] Research findings integrated, not tacked on

```

---

## Architect Agent Responsibilities

**The architect agent**:
1. Reads positioning manifest (core message, desired action, constraints)
2. Reads research report (findings, evidence, citations)
3. Applies pyramid-principle skill (hierarchical structure)
4. Generates outline structure:
   - Places core message at apex
   - Identifies 3-5 major supporting arguments from research
   - Maps evidence to arguments
   - Estimates word counts per section
   - Ensures total within max_length_words
5. Validates against positioning:
   - Does structure serve content_purpose?
   - Does it guide toward desired action?
   - Are NOT-covering topics excluded?
6. Documents research mapping (what findings go where)
7. Creates smooth transitions between sections

**Quality checks**:
- Pyramid structure maintained (answer first, support second)
- Every element traces to positioning or research
- Word count estimates realistic
- Flow is logical and compelling

---

## State Management

**Updates work unit state**:
```json
{
  "phase": "outlined",
  "timestamp": "2025-10-31T21:00:00Z",
  "outline_structure": {
    "sections": 5,
    "arguments": 3,
    "estimated_words": 1500
  },
  "next_command": "/draft"
}
```

**Preserves files**:
- positioning-manifest.json (unchanged)
- research-report.md (unchanged)
- outline.md (created)

---

## Outline Quality Standards

**Hierarchical clarity**:
- ✅ Clear levels (core message → arguments → evidence → details)
- ✅ Logical progression
- ✅ Each level supports level above
- ❌ NOT flat list of topics
- ❌ NOT chronological without hierarchy

**Evidence-based**:
- ✅ Every argument backed by research
- ✅ Citations mapped to sections
- ✅ Research findings integrated
- ❌ NOT opinion without evidence
- ❌ NOT assertions without support

**Positioning-constrained**:
- ✅ Core message central
- ✅ Structure guides to desired action
- ✅ Length within constraints
- ✅ Exclusions respected
- ❌ NOT scope creep
- ❌ NOT deviations from positioning

**Readable and clear**:
- ✅ Section titles descriptive
- ✅ Transitions smooth
- ✅ Flow is compelling
- ❌ NOT jargon without explanation
- ❌ NOT disjointed sections

---

## Common Outline Patterns

### Pattern 1: Problem-Solution-Benefit
**Structure**:
1. Opening: Problem statement (audience pain)
2. Argument 1: Solution overview (our approach)
3. Argument 2: How it works (mechanism)
4. Argument 3: Benefits and evidence (outcomes)
5. Closing: Call to action

**Good for**: Product content, framework explanations, tool introductions

### Pattern 2: Positioning-Evidence-Action
**Structure**:
1. Opening: Positioning statement (vs alternatives)
2. Argument 1: What alternatives provide
3. Argument 2: What we provide differently
4. Argument 3: Evidence of effectiveness
5. Closing: How to get started

**Good for**: Competitive positioning, "why us" content

### Pattern 3: Question-Investigation-Answer
**Structure**:
1. Opening: Provocative question
2. Argument 1: Common beliefs (what people think)
3. Argument 2: Reality (what research shows)
4. Argument 3: Implications (what this means)
5. Closing: Answer to opening question

**Good for**: Thought leadership, educational content, myth-busting

### Pattern 4: Current-Future-Path
**Structure**:
1. Opening: Current state (where we are)
2. Argument 1: Limitations of current approaches
3. Argument 2: Vision of better approach
4. Argument 3: How to transition
5. Closing: First steps

**Good for**: Vision content, transformation narratives, adoption guidance

---

## Length Estimation Guidelines

**Estimation by section type**:
- Opening (hook + message): 10-15% of total
- Major argument section: 20-30% of total each
- Closing (message + CTA): 10-15% of total

**Example for 1500-word blog post**:
- Opening: 200 words (13%)
- Argument 1: 400 words (27%)
- Argument 2: 400 words (27%)
- Argument 3: 400 words (27%)
- Closing: 100 words (7%)
- **Total**: 1500 words

**Buffer**:
- Always estimate 10-20% under max_length_words
- Allows for expansion during drafting
- Prevents exceeding constraint

---

## MCP Tool Usage

**Sequential Thinking MCP** (optional, enhanced):
- Complex outline reasoning
- Multi-dimensional structure analysis
- Trade-off evaluation (which arguments strongest)
- Fallback: Standard analytical reasoning

**Graceful degradation**:
- Core outline generation works without MCP
- Sequential thinking enhances quality and speed
- No MCP dependency for core functionality

---

## Example Session

```bash
$ /outline caf-white-paper

Loading positioning manifest...
✓ Core message: Transform Claude Code into specialized domain agents
✓ Max length: 3500 words
✓ NOT covering: Deep theory, development history

Loading research report...
✓ 8 findings loaded
✓ 18 sources available for citation

Invoking architect agent with pyramid-principle skill...

Applying pyramid principle:
✓ Core message at apex: "Transform Claude Code..."
✓ Identifying supporting arguments from research
  - Argument 1: Customization spectrum (out-of-box → CAF → SDK)
  - Argument 2: Domain-specific transformation (content management example)
  - Argument 3: Proven patterns and constraints
✓ Mapping evidence to arguments
✓ Estimating word counts

Validating against positioning:
✓ Structure guides toward "clone repo and experiment"
✓ Estimated length: 3200 words (within 3500 limit)
✓ NOT-covering topics excluded
✓ All arguments support core message

Outline created: .workspace/work/content/caf-white-paper/outline.md
✓ 5 sections, 3 major arguments
✓ Research mapping complete
✓ Next command: /draft

Outline generation complete. Ready for drafting.
```

---

## Validation Rules

**Outline must include**:
- ✅ Core message clearly stated
- ✅ 3-5 major supporting arguments
- ✅ Evidence mapping from research
- ✅ Word count estimates per section
- ✅ Total estimate within max_length_words (±10%)
- ✅ Transition points identified
- ✅ Call to action specified

**Quality checks**:
- Pyramid structure maintained
- All arguments trace to research findings
- NOT-covering topics excluded
- Flow guides toward desired action

---

## When to Revise Outline

**Revise when**:
- Word count estimate exceeds max_length_words by >10%
- Arguments don't clearly support core message
- Research findings poorly integrated
- Flow doesn't guide to desired action
- Feedback from stakeholder review

**Don't revise when**:
- Minor wording tweaks (save for draft)
- Small word count adjustments (handle in draft)
- Detailed evidence selection (architect just maps findings)

**Outline is blueprint, not final product**: Some iteration expected, but major structure should be stable.

---

## Integration with Content Workflow

**Standard workflow**:
```
/position → /research → /outline → /draft → /review
```

**Outline enables draft**:
- Author agent receives outline as structure
- Section word counts guide drafting
- Evidence citations ready for integration
- Flow already designed

**Outline validates positioning**:
- Forces structural decisions before writing
- Makes scope clear (prevents drift)
- Ensures research is usable (not orphaned findings)

---

## Success Criteria

**Outline succeeds when**:
- ✅ Pyramid structure clear and logical
- ✅ Core message prominently positioned
- ✅ All arguments supported by research
- ✅ Word count within constraints
- ✅ NOT-covering topics excluded
- ✅ Flow guides to desired action
- ✅ Ready for drafting without major questions

**Outline fails when**:
- ❌ Structure is flat (no hierarchy)
- ❌ Arguments unsupported by research
- ❌ Word count exceeds constraints
- ❌ Scope includes NOT-covering topics
- ❌ Flow doesn't serve positioning
- ❌ Major questions remain before drafting

**In failure case**: Revisit research, clarify positioning, restructure with pyramid principle.

---

## Technical Notes

**File-Based Persistence**:
- Outline stored as structured markdown
- Research mapping preserved
- Version-controllable
- Human-readable and editable

**Idempotency**:
- Safe to re-run outline generation
- Can refine existing outline
- Preserves downstream work if draft exists

**Agent Invocation**:
- Uses architect agent (see agents/architect.md)
- Uses pyramid-principle skill (see skills/pyramid-principle.md)
- Moderate duration (30-60 minutes typical)

---

**Command Version**: 1.0
**Created**: 2025-10-31
**Agent**: architect
**Skill**: pyramid-principle
**Previous Command**: /research
**Next Command**: /draft
**Key Innovation**: Positioning-constrained, evidence-based hierarchical structure
