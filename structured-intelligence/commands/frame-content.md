---
name: frame-content
description: "Phase 2: Apply narrative framing (SCQA or Pyramid) and select Diátaxis documentation mode based on user intent."
---

# Phase 2: Narrative Framing

**Purpose**: Apply narrative structure and map content to Diátaxis documentation mode

**When to use**:
- After Phase 1 (message definition) complete
- Have selected messages and MECE hierarchy
- Ready to define narrative arc and content type

**Inputs**:
- `writing-state.json` with Phase 1 complete
- Narrative frame choice: SCQA (persuasive) or Pyramid (explanatory)
- Diátaxis mode: Tutorial, How-To, Reference, or Explanation

**Outputs**:
- Narrative structure applied to messages
- Diátaxis mode selected and template identified
- Updated `writing-state.json` with Phase 2 complete
- Story arc for content

---

## Command Implementation

You are implementing **Phase 2** of the Structured Intelligence Framework (SIF).

### SIF Layers 1 & 2

**Layer 1 (Pyramid Principle)**: Provides logical structure (done in Phase 1)

**Layer 2 (Diátaxis Framework)**: Maps user intent to documentation mode

**Integration**: Narrative frame wraps Pyramid structure, Diátaxis determines presentation style

### Process

#### Step 1: Validate Phase 1 Complete

```bash
# Check if writing-state.json exists
STATE_FILE="$PWD/writing-state.json"

if [ ! -f "$STATE_FILE" ]; then
    echo "❌ Error: writing-state.json not found"
    echo ""
    echo "Run /define-messages first to complete Phase 1"
    exit 1
fi

# Check if Phase 1 complete
PHASE=$(cat "$STATE_FILE" | jq -r '.phase')

if [ "$PHASE" != "message-definition-complete" ]; then
    echo "❌ Error: Phase 1 not complete"
    echo "Current phase: $PHASE"
    echo ""
    echo "Complete /define-messages before framing content"
    exit 1
fi

# Load message data
APEX=$(cat "$STATE_FILE" | jq -r '.messages.hierarchy.apex')
MESSAGE_COUNT=$(cat "$STATE_FILE" | jq -r '.messages.selected | length')
CONTENT_TYPE=$(cat "$STATE_FILE" | jq -r '.content_type')

echo "✅ Phase 1 Complete"
echo ""
echo "Apex Message: $APEX"
echo "Selected Messages: $MESSAGE_COUNT"
echo "Content Type: $CONTENT_TYPE"
echo ""
```

#### Step 2: Parse Arguments

```bash
# Parse command arguments
FRAME="${1:-}"
DIATAXIS_MODE="${2:-}"

# Validate frame choice
if [ -z "$FRAME" ]; then
    echo "❌ Error: Narrative frame required"
    echo ""
    echo "Usage: /frame-content [SCQA|Pyramid] [Tutorial|HowTo|Reference|Explanation]"
    echo ""
    echo "Narrative Frames:"
    echo "  - SCQA: Situation-Complication-Question-Answer (persuasive, problem-focused)"
    echo "  - Pyramid: Top-down logical structure (explanatory, comprehensive)"
    echo ""
    echo "Diátaxis Modes:"
    echo "  - Tutorial: Learning-oriented (hands-on lessons)"
    echo "  - HowTo: Problem-oriented (step-by-step guides)"
    echo "  - Reference: Information-oriented (technical descriptions)"
    echo "  - Explanation: Understanding-oriented (discussion and clarification)"
    echo ""
    echo "Example: /frame-content SCQA explanation"
    exit 1
fi

case "$FRAME" in
    SCQA|scqa)
        FRAME="SCQA"
        ;;
    Pyramid|pyramid)
        FRAME="Pyramid"
        ;;
    *)
        echo "❌ Unknown narrative frame: $FRAME"
        echo "Valid frames: SCQA, Pyramid"
        exit 1
        ;;
esac

# Validate Diátaxis mode
if [ -z "$DIATAXIS_MODE" ]; then
    echo "❌ Error: Diátaxis mode required"
    echo ""
    echo "Modes:"
    echo "  - Tutorial: Learning-oriented"
    echo "  - HowTo: Problem-oriented"
    echo "  - Reference: Information-oriented"
    echo "  - Explanation: Understanding-oriented"
    echo ""
    echo "Example: /frame-content SCQA explanation"
    exit 1
fi

case "$DIATAXIS_MODE" in
    Tutorial|tutorial)
        DIATAXIS_MODE="tutorial"
        ;;
    HowTo|howto|how-to)
        DIATAXIS_MODE="howto"
        ;;
    Reference|reference)
        DIATAXIS_MODE="reference"
        ;;
    Explanation|explanation)
        DIATAXIS_MODE="explanation"
        ;;
    *)
        echo "❌ Unknown Diátaxis mode: $DIATAXIS_MODE"
        echo "Valid modes: Tutorial, HowTo, Reference, Explanation"
        exit 1
        ;;
esac

echo "🎭 Narrative Frame: $FRAME"
echo "📚 Diátaxis Mode: $DIATAXIS_MODE"
echo ""
```

#### Step 3: Validate Frame-Mode Compatibility

```bash
# Check if frame and mode are compatible
case "$CONTENT_TYPE-$FRAME-$DIATAXIS_MODE" in
    website-hub-SCQA-explanation|website-hub-SCQA-howto)
        echo "✅ Compatible: Website hubs work well with SCQA + explanation/howto"
        ;;
    book-chapter-Pyramid-tutorial|book-chapter-Pyramid-explanation)
        echo "✅ Compatible: Book chapters work well with Pyramid + tutorial/explanation"
        ;;
    blog-post-SCQA-explanation|blog-post-SCQA-howto)
        echo "✅ Compatible: Blog posts work well with SCQA + explanation/howto"
        ;;
    white-paper-Pyramid-reference|white-paper-Pyramid-explanation)
        echo "✅ Compatible: White papers work well with Pyramid + reference/explanation"
        ;;
    documentation-*-tutorial|documentation-*-howto|documentation-*-reference)
        echo "✅ Compatible: Documentation supports all modes"
        ;;
    *)
        echo "⚠️  Warning: Unusual combination detected"
        echo ""
        echo "Frame: $FRAME"
        echo "Mode: $DIATAXIS_MODE"
        echo "Content Type: $CONTENT_TYPE"
        echo ""
        echo "Typical combinations:"
        echo "  - Website/Blog: SCQA + explanation/howto"
        echo "  - Book Chapter: Pyramid + tutorial/explanation"
        echo "  - White Paper: Pyramid + reference/explanation"
        echo ""
        read -p "Continue anyway? (y/n): " confirm
        if [ "$confirm" != "y" ]; then
            echo "Aborted. Choose different frame/mode combination."
            exit 1
        fi
        ;;
esac
echo ""
```

#### Step 4: Invoke Narrative Framer Agent

```bash
echo "🎨 Invoking narrative-framer agent..."
echo ""
```

Now use the Task tool to invoke the `narrative-framer` agent:

**Agent Task**:
- Load `scqa-framework` skill (if frame=SCQA)
- Load `diataxis-framework` skill
- Review Phase 1 messages and hierarchy
- Apply selected narrative frame to message structure
- Map messages to Diátaxis mode structure
- Define story arc (beginning, middle, end)
- Identify section transitions
- Create content flow

**Agent Inputs**:
- State file: `writing-state.json`
- Frame: $FRAME
- Mode: $DIATAXIS_MODE
- Content type: $CONTENT_TYPE

**Agent Outputs**:
- Narrative structure (SCQA elements or Pyramid flow)
- Diátaxis template selection
- Section mapping (messages → sections)
- Story arc definition

#### Step 5: Invoke Diátaxis Planner Agent

```bash
echo "📋 Invoking diataxis-planner agent..."
echo ""
```

Use the Task tool to invoke the `diataxis-planner` agent:

**Agent Task**:
- Confirm Diátaxis mode selection is appropriate for user intent
- Identify template for selected mode
- Map messages to mode structure
- Define mode-specific guidance
- Validate alignment with content goals

**Agent Inputs**:
- Mode: $DIATAXIS_MODE
- Messages from state
- Content type: $CONTENT_TYPE

**Agent Outputs**:
- Template path for mode
- Section structure per mode
- Mode-specific writing guidance
- User intent validation

#### Step 6: Update State

After agents complete:

```bash
# Update state file with Phase 2 results
# (Agents will update, but command confirms)

cat > temp_update.json << EOF
{
  "layer1_frame": "$FRAME",
  "layer2_mode": "$DIATAXIS_MODE"
}
EOF

jq ".sif_layers.layer1_frame = \"$FRAME\" | .sif_layers.layer2_mode = \"$DIATAXIS_MODE\" | .phase = \"narrative-framing-complete\" | .updated_at = \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"" "$STATE_FILE" > temp_state.json

mv temp_state.json "$STATE_FILE"
rm -f temp_update.json

echo "✅ State updated: $STATE_FILE"
echo ""
```

#### Step 7: Summary and Next Steps

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Phase 2 Complete: Narrative Framing"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Frame: $FRAME"
echo "Mode: $DIATAXIS_MODE"
echo ""

# Show narrative structure
if [ "$FRAME" = "SCQA" ]; then
    echo "SCQA Structure:"
    cat "$STATE_FILE" | jq -r '.narrative.scqa | "Situation: \(.situation)\nComplication: \(.complication)\nQuestion: \(.question)\nAnswer: \(.answer)"'
else
    echo "Pyramid Structure:"
    cat "$STATE_FILE" | jq -r '.narrative.pyramid | "Flow: \(.flow_type)\nProgression: \(.progression)"'
fi

echo ""
echo "Diátaxis Template: $(cat $STATE_FILE | jq -r '.diataxis.template_path')"
echo ""
echo "Next Phase: /expand-outline"
echo ""
echo "💡 Tip: Review narrative structure in writing-state.json before outlining"
echo ""
```

---

## Narrative Frames

### SCQA (Situation-Complication-Question-Answer)

**When to use**:
- Persuasive content (proposals, recommendations)
- Problem-focused content
- Need to build case for action
- Audience may resist or need convincing

**Structure**:
- **Situation**: Current state (establishes context)
- **Complication**: Problem disrupting situation (creates tension)
- **Question**: What should we do? (focuses reader)
- **Answer**: Your pyramid of messages (provides solution)

**Example (Website Hub)**:
```
Situation: "Companies invest millions in AI strategy"
Complication: "But 70% of AI initiatives fail in production"
Question: "How do we bridge strategy and execution?"
Answer (Apex): "Applied AI connects business strategy to technical execution"
  └─ Supporting messages follow...
```

**Tone**: Engaging, problem-aware, solution-oriented

### Pyramid (Top-Down Logical)

**When to use**:
- Explanatory content (teaching, informing)
- Comprehensive content
- Audience wants depth, not persuasion
- Content is educational

**Structure**:
- **Apex**: Main point (stated immediately)
- **Supporting**: Themes that explain/defend apex
- **Details**: Evidence and examples

**Example (Book Chapter)**:
```
Apex: "Time series analysis reveals patterns in sequential data for ML trading"
├─ Core Concepts (stationarity, autocorrelation, signal vs noise)
├─ Mathematical Foundations (AR models, moving averages)
└─ Practical Applications (feature engineering, common pitfalls)
```

**Tone**: Authoritative, thorough, educational

---

## Diátaxis Framework (Layer 2)

### Overview

**Diátaxis** maps user intent to documentation mode.

**Four Modes** (quadrants):
```
         Action-Oriented
               │
    Tutorial   │   How-To
 (Learning)    │   (Goals)
               │
───────────────┼───────────────
               │
  Explanation  │  Reference
(Understanding)│ (Information)
               │
      Knowledge-Oriented
```

### Tutorial (Learning-Oriented)

**User Intent**: "Teach me"

**Characteristics**:
- Hands-on lessons
- Step-by-step progression
- Safe environment (can't break things)
- Learning by doing
- Clear outcomes

**Structure**:
```
1. Introduction (what will you learn)
2. Prerequisites (what you need)
3. Steps (detailed, sequential)
4. Verification (did it work?)
5. Next steps (what's next)
```

**Example**: "Building your first ML trading strategy"

**Tone**: Encouraging, patient, educational

### How-To (Problem-Oriented)

**User Intent**: "Help me solve this specific problem"

**Characteristics**:
- Goal-focused (specific outcome)
- Assumes some knowledge
- Practical steps
- Minimal explanation (focus on "how", not "why")

**Structure**:
```
1. Goal statement (what you'll achieve)
2. Prerequisites (what you need)
3. Steps (action-oriented)
4. Verification (success criteria)
```

**Example**: "How to optimize database query performance"

**Tone**: Direct, practical, efficient

### Reference (Information-Oriented)

**User Intent**: "Tell me the facts"

**Characteristics**:
- Technical descriptions
- Complete, accurate information
- Dry, factual tone
- Organized for lookup (not reading cover-to-cover)

**Structure**:
```
1. Overview (what it is)
2. Parameters / Properties (specifications)
3. Behavior (what it does)
4. Examples (optional, minimal)
```

**Example**: "API endpoint reference documentation"

**Tone**: Neutral, precise, comprehensive

### Explanation (Understanding-Oriented)

**User Intent**: "Help me understand"

**Characteristics**:
- Discuss concepts and context
- Clarify and illuminate
- Provide background and connections
- Answer "why" and "how it works"

**Structure**:
```
1. Overview (big picture)
2. Context (why it matters)
3. Concepts (how it works)
4. Alternatives / Trade-offs (when to use)
5. Conclusion (key takeaways)
```

**Example**: "Understanding time series stationarity and why it matters"

**Tone**: Conversational, insightful, thoughtful

---

## Content Type Adaptations

### Website Hub (800-2K words)

**Recommended**:
- Frame: SCQA (persuasive, engaging)
- Mode: Explanation or How-To

**Why**: Website hubs need to engage and convert. SCQA builds case for action.

**Structure Example**:
```
SCQA Frame:
  Situation → Complication → Question → Answer (Pyramid)

Explanation Mode:
  1. Overview (Situation)
  2. The Problem (Complication)
  3. Why It Matters (Context)
  4. Our Approach (Answer / Apex)
  5. How It Works (Supporting messages)
  6. What You Can Expect (Outcomes)
```

### Book Chapter (6-8K words)

**Recommended**:
- Frame: Pyramid (educational, comprehensive)
- Mode: Tutorial or Explanation

**Why**: Chapters teach and build knowledge systematically.

**Structure Example**:
```
Pyramid Frame:
  Apex → Supporting Themes → Details

Tutorial Mode:
  1. Chapter Overview (Apex)
  2. What You'll Learn (Supporting messages preview)
  3. Prerequisites
  4. Core Concepts (Theme 1)
  5. Hands-On Example (Theme 2)
  6. Advanced Topics (Theme 3)
  7. Summary and Next Steps
```

### Blog Post (1.5-3K words)

**Recommended**:
- Frame: SCQA (engaging, problem-focused)
- Mode: Explanation or How-To

**Why**: Blogs need to grab attention and provide value quickly.

**Structure Example**:
```
SCQA Frame + How-To Mode:
  1. The Problem (Situation + Complication)
  2. What We'll Solve (Question)
  3. The Solution (Answer / Apex)
  4. Step 1: [Action]
  5. Step 2: [Action]
  6. Step 3: [Action]
  7. Conclusion
```

### White Paper (5-15K words)

**Recommended**:
- Frame: Pyramid (authoritative, comprehensive)
- Mode: Reference or Explanation

**Why**: White papers establish authority through depth and rigor.

**Structure Example**:
```
Pyramid Frame + Reference Mode:
  1. Executive Summary (Apex)
  2. Introduction (Context)
  3. Current Landscape (Theme 1)
  4. Technical Approach (Theme 2)
  5. Implementation Details (Theme 3)
  6. Results and Evidence (Theme 4)
  7. Conclusion
```

### Documentation (varies)

**Recommended**:
- Frame: Pyramid (clear, structured)
- Mode: ALL (map sections to modes)

**Why**: Documentation serves multiple user intents.

**Structure Example**:
```
Getting Started → Tutorial
How-To Guides → How-To
API Reference → Reference
Concepts → Explanation
```

---

## MCP Tools

### Context7 (Optional)
Use for:
- Researching SCQA framework best practices
- Finding Diátaxis case studies
- Validating narrative patterns

---

## Error Handling

### Phase 1 Not Complete
```
❌ Error: Phase 1 not complete

Current phase: [phase]

Complete /define-messages before framing content
```

### Invalid Frame
```
❌ Unknown narrative frame: [frame]

Valid frames:
  - SCQA: Situation-Complication-Question-Answer
  - Pyramid: Top-down logical structure
```

### Invalid Mode
```
❌ Unknown Diátaxis mode: [mode]

Valid modes:
  - Tutorial: Learning-oriented
  - HowTo: Problem-oriented
  - Reference: Information-oriented
  - Explanation: Understanding-oriented
```

### Incompatible Frame-Mode Combination
```
⚠️  Warning: Unusual combination detected

Frame: Pyramid
Mode: How-To
Content Type: book-chapter

Typical combinations:
  - Book Chapter: Pyramid + tutorial/explanation
  - Website Hub: SCQA + explanation/howto

Continue anyway? (y/n):
```

---

## Examples

### Example 1: Website Hub (SCQA + Explanation)

```bash
/frame-content SCQA explanation
```

**Agent Output**:
```
🎭 Applying SCQA Framework...

Situation: "Companies invest millions in AI strategy"
Complication: "70% of AI initiatives fail in production (Gartner 2024)"
Question: "How do we bridge strategy and execution?"
Answer: "Applied AI connects business strategy to technical execution"

📚 Mapping to Explanation Mode...

Structure:
1. Overview (Situation)
2. The Challenge (Complication)
3. Why This Matters (Context)
4. Our Approach (Answer / Apex)
   ├─ Technical Excellence
   └─ Business Pragmatism
5. How It Works (Supporting messages)
6. What You Can Expect

Template: resources/templates/diataxis/explanation.md
```

### Example 2: Book Chapter (Pyramid + Tutorial)

```bash
/frame-content Pyramid tutorial
```

**Agent Output**:
```
🎭 Applying Pyramid Framework...

Apex: "Time series analysis reveals patterns in sequential data for ML trading"

Supporting Themes:
├─ Core Concepts
├─ Mathematical Foundations
└─ Practical Applications

📚 Mapping to Tutorial Mode...

Structure:
1. Chapter Overview (Apex)
2. What You'll Learn
3. Prerequisites
4. Lesson 1: Core Concepts
5. Lesson 2: Mathematical Foundations
6. Lesson 3: Hands-On Practice
7. Verification and Summary

Template: resources/templates/diataxis/tutorial.md
```

---

## Quality Checklist

Before completing Phase 2:

- [ ] Phase 1 validated as complete
- [ ] Narrative frame selected and appropriate
- [ ] Diátaxis mode selected and appropriate
- [ ] Frame-mode compatibility validated
- [ ] SCQA elements defined (if applicable)
- [ ] Pyramid flow defined (if applicable)
- [ ] Messages mapped to Diátaxis structure
- [ ] Template identified
- [ ] Story arc clear
- [ ] State updated with Phase 2 data

---

## Next Steps

After Phase 2 completion:

**Phase 3**: `/expand-outline`
- Convert messages to hierarchical bullets
- Generate topic sentences
- Validate structure

**Alternative**: Refine narrative
- If story arc unclear
- If frame-mode mismatch detected
- Adjust before outlining

---

**Remember**: Frame provides narrative flow, Diátaxis provides structure. Together they transform messages into content blueprint.
