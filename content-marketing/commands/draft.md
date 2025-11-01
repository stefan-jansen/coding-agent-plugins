---
description: Generate full draft from outline, constrained by positioning, informed by research, using format-specific skills
task_type: drafting
requires_agent: author
requires_state: outlined
requires_skill: excellent-writing
---

# /draft - Draft Generation

**Purpose**: Generate complete draft from outline, operating within positioning constraints, incorporating research evidence, and applying format-specific writing skills.

**Philosophy**: Author is EXECUTOR not STRATEGIST. Positioning defines strategy, outline defines structure, author executes within constraints.

---

## Usage

```bash
/draft [content-piece-name] [optional: format-skill]
```

**Examples**:
```bash
/draft caf-white-paper
/draft landing-page website-copy
/draft blog-post longform-technical-writing
/draft social-post social-media-content-strategy
```

---

## Prerequisites

**Required**:
- ✅ Positioning manifest exists (from /position)
- ✅ Research report exists (from /research)
- ✅ Outline exists (from /outline)
- ✅ Work unit in "outlined" state

---

## What This Command Does

1. **Loads all inputs**:
   - Positioning manifest (strategic constraints)
   - Research report (evidence and citations)
   - Outline (structural blueprint)
2. **Invokes author agent** with excellent-writing skill + optional format skill
3. **Generates draft section by section**:
   - Follows outline structure exactly
   - Stays within word count estimates (±10%)
   - Integrates research citations
   - Applies tone/reading-level from positioning
   - Uses format-specific patterns
4. **Validates during generation**:
   - Core message prominent
   - Desired action clear
   - NOT-covering topics excluded
   - Max length not exceeded
5. **Updates state** to "drafted"

---

## Draft Output

**File**: `.claude/work/content/[content-piece-name]/draft-v1.md`

**Structure** (follows outline):
```markdown
# [Title] - Draft v1

## Metadata
- **Created**: [Timestamp]
- **Word Count**: [Actual count]
- **Target**: [Max from positioning]
- **Format**: [Format skill used]

---

[Full content following outline structure]

## Opening
[Hook and core message delivery]

## [Argument 1 Title]
[Content with integrated research citations]

## [Argument 2 Title]
[Content with integrated research citations]

## [Argument 3 Title]
[Content with integrated research citations]

## Closing
[Core message reinforcement + call to action]

---

## Draft Notes

**Positioning Adherence**:
- Core message delivered: [Yes/No + location]
- Desired action included: [Yes/No + location]
- NOT-covering topics excluded: [Yes/No]
- Length constraint met: [Yes/No + actual vs target]

**Research Integration**:
- Citations used: [Count]
- Evidence density: [High/Medium/Low per positioning]
- Unsupported claims: [None expected]

**Writing Quality** (self-assessment):
- Clarity: [Notes]
- Flow: [Notes]
- Engagement: [Notes]
- Technical accuracy: [Notes]
```

---

## Author Agent Responsibilities

**The author agent**:
1. Operates as EXECUTOR within constraints (not strategist)
2. Reads positioning manifest (never deviates)
3. Follows outline structure precisely
4. Integrates research evidence with citations
5. Applies excellent-writing skill (clarity, engagement, precision)
6. Applies format skill if specified (white paper, blog, social, etc.)
7. Maintains tone/reading-level from positioning
8. Monitors word count continuously
9. Self-validates against positioning during generation
10. Documents draft notes for editor review

**Quality checks**:
- Every section follows outline
- Word counts within ±10% of estimates
- Research citations integrated naturally
- Core message and CTA prominent
- NO scope creep beyond positioning

---

## Format Skills

**excellent-writing** (always applied):
- Clarity and precision
- Active voice preference
- Topic sentences and transitions
- Paragraph coherence
- See skills/excellent-writing.md

**longform-technical-writing** (optional):
- White papers, deep dives, technical reports
- Formal tone, high evidence density
- Technical depth appropriate for expert audience

**website-copy** (optional):
- Landing pages, hub content
- Scannable structure, clear CTAs
- Benefit-focused, concise

**social-media-content-strategy** (optional):
- LinkedIn posts, Twitter threads
- Hook-first, engagement-optimized
- Platform-specific patterns

**pyramid-principle** (optional):
- Structured business communication
- Answer-first approach
- Executive-friendly

**scqa-framework** (optional):
- Situation-Complication-Question-Answer
- Narrative structure for complex topics
- See skills/scqa-framework.md

---

## State Management

**Updates work unit state**:
```json
{
  "phase": "drafted",
  "timestamp": "2025-10-31T22:00:00Z",
  "draft_version": 1,
  "word_count": 3150,
  "target_word_count": 3500,
  "format_skill": "longform-technical-writing",
  "next_command": "/review"
}
```

**Preserves files**:
- All inputs unchanged
- draft-v1.md created

---

## Drafting Quality Standards

**Positioning adherence**:
- ✅ Core message delivered prominently
- ✅ Structure guides to desired action
- ✅ NOT-covering topics excluded
- ✅ Length within max_length_words
- ✅ Tone matches positioning
- ❌ NOT strategic deviations
- ❌ NOT scope creep

**Research integration**:
- ✅ Claims supported by citations
- ✅ Evidence integrated naturally (not listed)
- ✅ Density matches positioning (high/medium/low)
- ❌ NOT unsupported assertions
- ❌ NOT citation-free claims

**Writing quality**:
- ✅ Clear and engaging
- ✅ Logical flow and transitions
- ✅ Format-appropriate style
- ✅ Technically accurate
- ❌ NOT jargon-heavy
- ❌ NOT disjointed sections

---

## Citation Integration

**Research citations** from research-report.md:
```markdown
Domain-specific agents show 30% productivity improvement over generic approaches [1].

[1] Research Report, Finding 3: "Agent customization effectiveness"
```

**Inline references** (preferred):
```markdown
The Agent SDK provides programmatic control for production use cases,
while CAF offers accessible markdown-based customization for rapid
experimentation (Claude Agent SDK Documentation, 2025).
```

**Footnotes** (when appropriate):
```markdown
CAF demonstrates the middle ground between no-code IDE customization
and full programmatic control[^1].

[^1]: See "Claude Agent Framework: Positioning Analysis" for spectrum details.
```

---

## Length Management

**Monitoring during generation**:
- Track running word count
- Compare to outline estimates per section
- Adjust remaining sections if needed
- Never exceed max_length_words from positioning

**Cutting strategy** (if approaching limit):
1. Remove nice-to-have examples
2. Condense redundant explanations
3. Tighten prose (fewer words, same meaning)
4. Keep core message and CTA intact
5. Preserve evidence for key claims

**Never cut**:
- Core message delivery
- Call to action
- Key evidence for positioning claims

---

## Example Session

```bash
$ /draft caf-white-paper longform-technical-writing

Loading inputs...
✓ Positioning manifest loaded
✓ Research report loaded (18 citations available)
✓ Outline loaded (3200 words estimated)

Invoking author agent...
✓ Skills: excellent-writing + longform-technical-writing
✓ Constraints: 3500 words max, technical tone, high evidence density

Generating draft section by section:
✓ Opening (250 words, target 200) - Core message delivered
✓ Argument 1 (720 words, target 700) - 4 citations integrated
✓ Argument 2 (680 words, target 700) - 3 citations integrated
✓ Argument 3 (710 words, target 700) - 5 citations integrated
✓ Closing (180 words, target 150) - CTA prominent

Validating against positioning:
✓ Core message: "Transform Claude Code into specialized agents" - Delivered in opening, reinforced in closing
✓ Desired action: "Clone repo and experiment" - Clear CTA with GitHub link
✓ NOT-covering: "Deep theory, development history" - Excluded
✓ Length: 3150 words (90% of 3500 max) ✓

Draft created: .claude/work/content/caf-white-paper/draft-v1.md
✓ Word count: 3150 / 3500 target
✓ Citations: 12 integrated
✓ Next command: /review

Draft generation complete. Ready for editorial review.
```

---

## MCP Tool Usage

**No MCP required** for core functionality:
- Drafting uses Read tool for inputs
- Write tool for output
- Pure generation based on loaded content

**Optional enhancements**:
- Context7: Verify technical claims during drafting
- WebSearch: Quick fact-checking if needed
- All gracefully degraded if unavailable

---

## Validation Rules

**Draft must include**:
- ✅ Core message from positioning (prominent placement)
- ✅ All major arguments from outline
- ✅ Research citations for claims
- ✅ Call to action from positioning
- ✅ Word count ≤ max_length_words
- ✅ Tone/reading-level from positioning

**Quality checks**:
- Outline structure followed
- Word counts per section reasonable (±20%)
- Evidence integrated naturally
- Flow is compelling
- No scope creep

---

## When to Re-Draft

**Re-draft when**:
- Exceeded max_length_words (must cut)
- Core message not prominent enough
- Research poorly integrated
- Tone mismatches positioning
- Editor feedback requires substantial changes (use /revise instead for minor)

**Don't re-draft when**:
- Minor wording issues (editorial polish)
- Small structural tweaks (can address in revision)
- Citation formatting (editorial cleanup)

**Draft is foundation, not perfection**: Editorial review and revision are separate phases.

---

## Integration with Content Workflow

**Standard workflow**:
```
/position → /research → /outline → /draft → /review → /revise
```

**Draft sets up review**:
- Editor receives complete first draft
- Positioning manifest for validation
- Research report for evidence checking
- Outline for structure comparison

---

## Success Criteria

**Draft succeeds when**:
- ✅ Positioning constraints honored
- ✅ Outline structure followed
- ✅ Research integrated with citations
- ✅ Writing is clear and engaging
- ✅ Length within constraints
- ✅ Format-appropriate style
- ✅ Ready for editorial review

**Draft fails when**:
- ❌ Exceeds max_length_words
- ❌ Deviates from positioning
- ❌ Includes NOT-covering topics
- ❌ Lacks research support for claims
- ❌ Poor writing quality
- ❌ Doesn't follow outline

**In failure case**: Identify specific issue (length, positioning, quality) and address systematically.

---

## Technical Notes

**File-Based Persistence**:
- Draft stored as versioned markdown (draft-v1.md, draft-v2.md, etc.)
- All inputs preserved
- Version-controllable

**Idempotency**:
- Re-running creates new version (draft-v2.md)
- Preserves previous drafts
- Can revert if needed

**Agent Invocation**:
- Uses author agent (see agents/author.md)
- Uses excellent-writing skill (always)
- Optional format skill specified in command
- Long-running (1-3 hours typical for substantial content)

---

**Command Version**: 1.0
**Created**: 2025-10-31
**Agent**: author
**Skills**: excellent-writing (required), format skills (optional)
**Previous Command**: /outline
**Next Command**: /review
**Key Innovation**: Execution within positioning constraints, not strategic generation
