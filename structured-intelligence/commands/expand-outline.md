---
name: expand-outline
description: "Phase 3: Convert messages to hierarchical bullets and generate topic sentences. Creates detailed outline structure ready for drafting."
---

# Phase 3: Outline Expansion

**Purpose**: Transform Phase 2 narrative structure into detailed hierarchical outline with topic sentences

**When to use**:
- After Phase 2 (narrative framing) complete
- Have narrative structure and Diátaxis mode defined
- Ready to create detailed outline before drafting

**Inputs**:
- `writing-state.json` with Phase 2 complete
- Messages with hierarchy
- Narrative structure (SCQA or Pyramid)
- Diátaxis mode selection

**Outputs**:
- Hierarchical bullet outline (2-4 levels deep)
- Topic sentences for each bullet
- Section mapping with evidence references
- Updated `writing-state.json` with Phase 3 complete

---

## Command Implementation

You are implementing **Phase 3** of the Structured Intelligence Framework (SIF).

### Process Overview

Phase 3 converts messages into a detailed outline structure:
- **Messages** (Phase 1) → **Bullets** (hierarchical expansion)
- **Bullets** → **Topic Sentences** (paragraph previews)
- **Outline** validated for MECE and logical flow

### Step 1: Validate Phase 2 Complete

```bash
# Check state file exists
STATE_FILE="$PWD/writing-state.json"

if [ ! -f "$STATE_FILE" ]; then
    echo "❌ Error: writing-state.json not found"
    echo ""
    echo "Run /define-messages and /frame-content first"
    exit 1
fi

# Check phase status
PHASE=$(cat "$STATE_FILE" | jq -r '.phase')

if [ "$PHASE" != "narrative-framing-complete" ]; then
    echo "❌ Error: Phase 2 not complete"
    echo "Current phase: $PHASE"
    echo ""
    echo "Run /frame-content to complete Phase 2 first"
    exit 1
fi

# Load context
CONTENT_ID=$(cat "$STATE_FILE" | jq -r '.content_id')
CONTENT_TYPE=$(cat "$STATE_FILE" | jq -r '.content_type')
FRAME=$(cat "$STATE_FILE" | jq -r '.sif_layers.layer1_frame')
MODE=$(cat "$STATE_FILE" | jq -r '.sif_layers.layer2_mode')

echo "✅ Phase 2 Complete"
echo ""
echo "Content: $CONTENT_ID"
echo "Type: $CONTENT_TYPE"
echo "Frame: $FRAME"
echo "Mode: $MODE"
echo ""
```

### Step 2: Invoke Outline Expander Agent

```bash
echo "📝 Invoking outline-expander agent..."
echo ""
```

Use the Task tool to invoke the `outline-expander` agent:

**Agent Task**:
- Load `topic-sentence-method` skill
- Review Phase 1 messages and Phase 2 narrative structure
- For each message, expand into hierarchical bullets (2-4 levels)
- For each bullet at each level, generate topic sentence
- Map bullets to Diátaxis mode structure
- Validate MECE at each level
- Create section outline with evidence references
- Update state with outline data

**Agent Inputs**:
- State file: `writing-state.json`
- Content type: $CONTENT_TYPE
- Narrative frame: $FRAME
- Diátaxis mode: $MODE

**Agent Outputs**:
- Hierarchical outline structure
- Topic sentences for all bullets
- Section mapping
- Evidence reference tracking
- MECE validation results

### Step 3: Update State

After agent completes:

```bash
# Agent will have updated state.json with outline data
# Verify completion
OUTLINE_SECTIONS=$(cat "$STATE_FILE" | jq -r '.outline.sections | length')

if [ "$OUTLINE_SECTIONS" -eq 0 ]; then
    echo "⚠️  Warning: No outline sections generated"
    echo "Check agent output for errors"
    exit 1
fi

# Update phase status
jq '.phase = "outline-expansion-complete" | .updated_at = "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'"' "$STATE_FILE" > temp_state.json
mv temp_state.json "$STATE_FILE"

echo "✅ State updated: $STATE_FILE"
echo ""
```

### Step 4: Display Outline Summary

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Phase 3 Complete: Outline Expansion"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Show outline structure
echo "📋 Outline Structure:"
echo ""

# Display sections with topic sentences
cat "$STATE_FILE" | jq -r '.outline.sections[] | "## \(.id): \(.message)\n\nTopic Sentence: \(.topic_sentence)\n\nBullets (\(.bullets | length)):\n\(.bullets | map("  - " + .) | join("\n"))\n"'

echo ""
echo "Sections: $OUTLINE_SECTIONS"
echo "Total Bullets: $(cat $STATE_FILE | jq '[.outline.sections[].bullets | length] | add')"
echo "Evidence References: $(cat $STATE_FILE | jq '[.outline.sections[].evidence_refs | length] | add')"
echo ""
echo "Next Phase: /draft-section [section-id]"
echo ""
echo "💡 Tip: Review outline structure in writing-state.json before drafting"
echo ""
```

---

## Outline Expansion Strategy

### Content Type Adaptations

#### Website Hub (800-2K words)
**Outline Depth**: 2-3 levels
**Bullets per Section**: 3-5
**Topic Sentence Style**: Engaging, persuasive

**Example Structure**:
```
1. Introduction (Situation/Context)
   - Hook statement
   - Context setting
   - Preview of value

2. The Challenge (Complication)
   - Problem definition
   - Impact quantified
   - Why it matters

3. Our Approach (Answer/Apex)
   - Solution overview
   - Key differentiators
   - Value proposition

4. How It Works (Supporting Messages)
   4.1 Technical Excellence
       - Architecture approach
       - Production focus
   4.2 Business Pragmatism
       - Outcome measurement
       - ROI tracking

5. What You Can Expect (Benefits)
   - Deliverables
   - Timeline
   - Next steps
```

#### Book Chapter (6-8K words)
**Outline Depth**: 3-4 levels
**Bullets per Section**: 5-8
**Topic Sentence Style**: Educational, clear

**Example Structure**:
```
1. Chapter Overview
   - Learning objectives
   - Prerequisites
   - Chapter structure

2. Core Concepts (Theme 1)
   2.1 Concept A
       - Definition
       - Why it matters
       - Key properties
   2.2 Concept B
       - Definition
       - Relationship to A
       - Common mistakes

3. Mathematical Foundations (Theme 2)
   3.1 Approach 1
       - Formula
       - Derivation
       - Assumptions
   3.2 Approach 2
       - Formula
       - When to use
       - Limitations

4. Practical Applications (Theme 3)
   4.1 Use Case 1
       - Scenario
       - Implementation
       - Results
   4.2 Common Pitfalls
       - Mistake 1
       - Mistake 2
       - How to avoid

5. Summary and Next Steps
   - Key takeaways
   - Practice exercises
   - Next chapter preview
```

#### Blog Post (1.5-3K words)
**Outline Depth**: 2-3 levels
**Bullets per Section**: 3-4
**Topic Sentence Style**: Conversational, punchy

**Example Structure**:
```
1. Hook (Situation + Complication)
   - Attention grabber
   - Problem statement
   - Why you should care

2. The Insight (Answer)
   - Main point
   - Why it works
   - Evidence

3. Key Points (Supporting)
   3.1 Point 1
       - Explanation
       - Example
   3.2 Point 2
       - Explanation
       - Example
   3.3 Point 3
       - Explanation
       - Example

4. Takeaway and Action
   - Summary
   - What to do next
   - Call to action
```

---

## Topic Sentence Generation

### What is a Topic Sentence?

A topic sentence is the first sentence of a paragraph that:
- **States the main point** of the paragraph
- **Previews content** that follows
- **Connects** to the overall message
- **Engages** the reader

**Formula**: `[Main point] + [Preview of support]`

### Examples by Diátaxis Mode

#### Tutorial Mode
**Bullet**: "Set up development environment"
**Topic Sentence**: "Before writing code, you'll configure your development environment with the required tools and dependencies."

**Characteristics**: Action-oriented, encouraging, step-focused

#### How-To Mode
**Bullet**: "Optimize database queries"
**Topic Sentence**: "Slow queries can be optimized using three proven techniques: indexing, query restructuring, and caching."

**Characteristics**: Direct, solution-focused, efficient

#### Reference Mode
**Bullet**: "API authentication parameters"
**Topic Sentence**: "The authentication endpoint accepts three parameters: api_key (string, required), expires_at (timestamp, optional), and scope (array, optional)."

**Characteristics**: Factual, comprehensive, precise

#### Explanation Mode
**Bullet**: "Why stationarity matters"
**Topic Sentence**: "Stationarity is fundamental to time series forecasting because models assume statistical properties remain constant over time."

**Characteristics**: Clarifying, insightful, "why"-focused

---

## MECE Validation

### At Each Outline Level

**Mutually Exclusive**: No overlapping bullets at same level
**Collectively Exhaustive**: All important aspects covered

**Validation Questions**:
1. Do any bullets overlap in content?
2. Are all key points addressed?
3. Is there clear distinction between bullets?
4. Any gaps in coverage?

**Example Validation**:
```
Section: "How It Works"

Bullets:
✅ Technical Excellence (distinct)
✅ Business Pragmatism (distinct)

MECE Check: ✅ Passed
- No overlap (technical vs business)
- Exhaustive (covers both aspects of "bridge")
```

---

## Evidence Reference Mapping

### Linking Evidence to Outline

Each bullet that makes a claim must reference evidence:

**Format**:
```json
{
  "section_id": "how-it-works-1",
  "bullet": "We architect AI aligned with business outcomes",
  "topic_sentence": "Our architecture approach ensures AI systems deliver measurable business value, not just technical sophistication.",
  "evidence_refs": [2, 5],
  "evidence_notes": "Case studies from Phase 1"
}
```

**Evidence Reference Types**:
- **Tier 1**: Direct measurements from evidence manifest
- **Tier 2**: Published case studies or research
- **Tier 3**: Derived calculations with sources
- **None**: Definitional or philosophical statements (no evidence needed)

---

## Quality Checklist

Before completing Phase 3:

- [ ] Phase 2 validated as complete
- [ ] All messages expanded into hierarchical bullets
- [ ] Topic sentences generated for all bullets
- [ ] Outline depth appropriate for content type
- [ ] MECE validated at each level
- [ ] Evidence references mapped
- [ ] Diátaxis mode structure respected
- [ ] Narrative flow maintained
- [ ] State updated with outline data

---

## Error Handling

### Phase 2 Not Complete
```
❌ Error: Phase 2 not complete

Current phase: message-definition-complete

Complete /frame-content before expanding outline.
```

### No Messages to Expand
```
❌ Error: No messages found in state

Ensure Phase 1 (define-messages) completed successfully.
```

### MECE Validation Failure
```
⚠️  MECE Validation Issues Detected

Section: "Core Concepts"
Issue: Bullets 2 and 4 overlap (both discuss stationarity)

Recommendation: Merge overlapping bullets or clarify distinction.

Proceed anyway? (y/n):
```

---

## Integration with Phases

### From Phase 2 (Narrative)
- Narrative structure guides outline organization
- SCQA elements map to outline sections
- Diátaxis mode determines outline style

### To Phase 4 (Drafting)
- Topic sentences become paragraph openings
- Bullets expand into supporting sentences
- Evidence references insert into paragraphs

---

## Next Steps

After Phase 3 completion:

**Phase 4**: `/draft-section [section-id]`
- Generate paragraphs from topic sentences
- Insert evidence references
- Apply Diátaxis template
- Validate claims

**Alternative**: Refine outline
- If structure unclear
- If MECE issues detected
- Before committing to drafting

---

**Remember**: Outline is your blueprint. Invest time here to save revision cycles later. Topic sentences are paragraph previews - make them clear and engaging.
