---
description: Run positioning session to establish strategic constraints before content creation
task_type: positioning
requires_agent: positioning-facilitator
---

# /position - Strategic Positioning Session

**Purpose**: Establish strategic constraints and positioning decisions BEFORE content generation begins.

**Philosophy**: Frameworks execute strategy, they don't create it. This command guides human strategic decisions, captures them in a positioning manifest, and provides that manifest as INPUT to all downstream commands.

---

## Usage

```bash
/position [content-piece-name] [optional: topic description]
```

**Examples**:
```bash
/position caf-white-paper "White paper on Claude Agent Framework"
/position landing-page "Homepage for Applied AI website"
/position blog-post "Blog post on positioning-first writing"
```

---

## What This Command Does

1. **Creates content work unit** in `.agents/work/content/[content-piece-name]/`
2. **Invokes positioning-facilitator agent** to guide 7-question session
3. **Captures answers** through interactive conversation
4. **Generates positioning manifest** (JSON file with strategic constraints)
5. **Initializes state** for content workflow

---

## The 7 Strategic Questions

The positioning-facilitator agent will ask:

### 1. What should the reader DO after reading this?
- Specific, measurable action
- Not passive understanding
- Example: "Clone repo and complete quick start tutorial"

### 2. What's the ONE thing they should remember tomorrow?
- Single core message (max 20 words)
- Not comprehensive understanding
- Example: "CAF prevents AI chaos through stateless, file-based architecture"

### 3. Who EXACTLY is this for?
- Specific audience with specific context
- Not broad categories
- Example: "Senior backend developers burned by unreliable AI tools"

### 4. What alternatives exist and why choose this?
- Clear positioning against alternatives
- Value proposition
- Example: "vs Raw Claude Code: We provide architecture, not just primitives"

### 5. What are we intentionally NOT covering?
- 3-5 explicit exclusions
- Scope discipline
- Example: "NOT covering comprehensive feature list"

### 6. What's the maximum length?
- Hard word count constraint
- Forces prioritization
- Example: "800 words max for landing page attention span"

### 7. How will we know if this worked?
- Measurable success metric
- Defines "good"
- Example: "Quick start tutorial completions within 24 hours"

---

## Output: Positioning Manifest

File: `.agents/work/content/[content-piece-name]/positioning-manifest.json`

```json
{
  "content_purpose": "desired action from Q1",
  "core_message": "one thing to remember from Q2",
  "target_audience": "specific audience from Q3",
  "audience_context": "their pain/situation",
  "positioning": "why us vs alternative from Q4",
  "not_covering": [
    "exclusion 1 from Q5",
    "exclusion 2 from Q5",
    "exclusion 3 from Q5"
  ],
  "max_length_words": 800,
  "length_rationale": "why this limit",
  "success_metric": "how we measure success from Q7",
  "tone": "technical|casual|formal|conversational",
  "reading_level": "general|technical|expert",
  "evidence_density": "high|medium|low"
}
```

---

## State Management

**Creates work unit structure**:
```
.agents/work/content/[content-piece-name]/
├── metadata.json                 # Content piece metadata
├── state.json                   # Current workflow phase
└── positioning-manifest.json    # Strategic constraints (OUTPUT)
```

**Initial state**:
```json
{
  "phase": "positioned",
  "timestamp": "2025-10-31T19:00:00Z",
  "next_command": "/research"
}
```

---

## Validation Rules

**Manifest must include**:
- ✅ Specific desired action (not vague understanding)
- ✅ Core message ≤ 20 words
- ✅ Specific audience (not broad category)
- ✅ Clear positioning vs alternatives
- ✅ 3-5 explicit NOT-covering exclusions
- ✅ Numeric word count limit
- ✅ Measurable success metric

**Positioning-facilitator enforces**:
- Push back on vague answers
- Request specificity
- Ensure exclusions are meaningful
- Validate success metrics are measurable

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Vague Purpose
**Bad**: "Inform readers about our framework"
**Good**: "Convince senior developers to clone repo and try quick start"

### ❌ Mistake 2: Broad Audience
**Bad**: "Developers interested in AI"
**Good**: "Senior backend developers burned by unreliable AI tools"

### ❌ Mistake 3: Multiple Core Messages
**Bad**: "Framework is reliable, flexible, powerful, easy to use..."
**Good**: "Production-grade architecture that prevents AI chaos"

### ❌ Mistake 4: No Exclusions
**Bad**: [empty NOT-covering list]
**Good**: ["Comprehensive feature list", "Deep theory", "Development history"]

### ❌ Mistake 5: No Length Limit
**Bad**: "As long as it needs to be"
**Good**: "800 words max"

### ❌ Mistake 6: Vague Success Metric
**Bad**: "Readers understand the framework"
**Good**: "Quick start tutorial completions"

---

## How Downstream Commands Use Manifest

**All subsequent commands validate against manifest**:

**/research**:
- Research must support core message
- Research must inform positioning vs alternatives
- Research scope constrained by NOT-covering list

**/outline**:
- Structure must guide toward desired action
- Core message must be central organizing principle
- Length must fit within max_length_words constraint

**/draft**:
- Every paragraph serves content_purpose
- Tone/reading_level from manifest
- Evidence density from manifest

**/review**:
- Does this serve positioning?
- Does this stay within NOT-covering boundaries?
- Does this guide toward desired action?
- Is length within constraint?

---

## When to Use This Command

**Always use for**:
- Landing pages
- Website hub content
- Marketing materials
- Blog posts
- White papers
- Documentation intro pages

**Helpful for**:
- Technical documentation (when positioning matters)
- Tutorials (to define desired outcome)
- Case studies (to clarify purpose)

**Skip for**:
- Internal notes (no external audience)
- Meeting summaries (structure-first is fine)
- Personal drafts (positioning may be implicit)

**Rule of thumb**: If content serves external audience with specific goal, run /position first.

---

## Integration with Content Workflow

**Standard workflow**:
```
/position → /research → /outline → /draft → /review → /revise → /approve
```

**Positioning is prerequisite**:
- Cannot run /research without positioning-manifest.json
- Cannot run /outline without positioning-manifest.json
- Cannot run /draft without positioning-manifest.json

**Rationale**: Strategic decisions must precede execution.

---

## Example Session

```bash
$ /position caf-white-paper "White paper on Claude Agent Framework"

Creating content work unit: .agents/work/content/caf-white-paper/

Invoking positioning-facilitator agent to guide strategic session...

[Agent asks 7 questions, user provides answers]

Q1: What should readers DO after reading?
A: Clone the GitHub repo and start experimenting with domain-specific agents

Q2: What's the ONE thing they should remember?
A: Transform Claude Code from out-of-box coding agent into specialized domain agents

... [continues for all 7 questions]

Generating positioning manifest...

✓ Positioning manifest created: .agents/work/content/caf-white-paper/positioning-manifest.json
✓ Workflow state initialized
✓ Next command: /research

Content piece "caf-white-paper" is now positioned and ready for research phase.
```

---

## Technical Notes

**Agent Invocation**:
- Uses positioning-facilitator agent (see agents/positioning-facilitator.md)
- Interactive session via conversation
- Agent validates answers for specificity and clarity

**File-Based Persistence**:
- All answers captured in positioning-manifest.json
- Stateless execution (can resume if interrupted)
- Manifest is version-controllable

**Idempotency**:
- Safe to re-run positioning session
- Updates existing manifest if work unit exists
- Preserves existing research/outline if present

---

## Success Criteria

**Positioning session succeeds when**:
- ✅ All 7 questions answered with specificity
- ✅ Positioning manifest generated and valid
- ✅ User approves manifest
- ✅ Clear next steps (proceed to /research)

**Positioning session fails when**:
- ❌ Answers remain vague after prompting
- ❌ User cannot articulate core message
- ❌ No measurable success metric defined
- ❌ NOT-covering list is empty

**In failure case**: Continue probing, suggest alternatives, explain why specificity matters.

---

## Meta-Principle

**Good writing is as much about what you DON'T say as what you do say.**

This command forces explicit decisions about:
- What to say (core message, positioning)
- Who to say it to (audience)
- Why to say it (desired action)
- What NOT to say (scope exclusions)

**Without positioning**: Frameworks produce comprehensive but unfocused content.

**With positioning**: Frameworks execute focused, purposeful content.

---

**Command Version**: 1.0
**Created**: 2025-10-31
**Agent**: positioning-facilitator
**Next Command**: /research
**Key Innovation**: Strategic decisions BEFORE execution, not during
