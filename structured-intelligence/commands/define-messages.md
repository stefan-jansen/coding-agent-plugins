---
name: define-messages
description: "Phase 1: Define key messages using Pyramid Principle + evidence-first methodology. Brainstorm messages, verify evidence, and cluster into MECE hierarchy."
---

# Phase 1: Message Definition

**Purpose**: Brainstorm key messages, verify evidence, and build MECE message hierarchy

**When to use**:
- Starting new content piece (website hub, blog post, book chapter)
- Need to clarify core messages before writing
- Have topic but unclear about structure

**Inputs**:
- Topic or content description
- Content type (website-hub, book-chapter, blog-post, white-paper, documentation)
- Optional: evidence files or requirements document

**Outputs**:
- Brainstormed messages (10 candidates)
- Evidence verification for each message
- User-selected messages (4-5 for hub, 6-8 for chapter)
- MECE-clustered message hierarchy
- `writing-state.json` with Phase 1 complete

---

## Command Implementation

You are implementing **Phase 1** of the Structured Intelligence Framework (SIF).

### SIF Layer 1: Pyramid Principle

**Core Concept**: Answer first, then supporting arguments

**MECE Reasoning**: Mutually Exclusive, Collectively Exhaustive
- **Mutually Exclusive**: No overlap between messages
- **Collectively Exhaustive**: All important points covered

**Message Characteristics**:
- Single clear idea per message
- Evidence-backed (no Tier 4 claims)
- Audience-appropriate complexity
- Supports apex message

### Process

#### Step 1: Initialize State

Create or load `writing-state.json` in project directory:

```bash
# Check if state exists
STATE_FILE="$PWD/writing-state.json"

if [ -f "$STATE_FILE" ]; then
    echo "⚠️  Existing writing-state.json found. Loading..."
    # Load and display current state
    cat "$STATE_FILE" | jq '.'

    # Ask user if they want to continue or start fresh
    echo ""
    echo "Options:"
    echo "1. Continue from current phase"
    echo "2. Start fresh (overwrite existing state)"
    echo ""
    read -p "Choice (1 or 2): " choice

    if [ "$choice" = "2" ]; then
        echo "Starting fresh content..."
    else
        echo "Continuing from phase: $(cat $STATE_FILE | jq -r '.phase')"
        exit 0
    fi
fi
```

#### Step 2: Parse Arguments

```bash
# Parse command arguments
TOPIC="$1"
CONTENT_TYPE="${2:-website-hub}"

if [ -z "$TOPIC" ]; then
    echo "❌ Error: Topic required"
    echo ""
    echo "Usage: /define-messages [topic] [content-type]"
    echo ""
    echo "Content types:"
    echo "  - website-hub (800-2K words, 4-5 messages)"
    echo "  - book-chapter (6-8K words, 6-8 messages)"
    echo "  - blog-post (1.5-3K words, 4-6 messages)"
    echo "  - white-paper (5-15K words, 8-12 messages)"
    echo "  - documentation (varies, task-focused)"
    echo ""
    echo "Example: /define-messages \"Applied AI bridges strategy to execution\" website-hub"
    exit 1
fi

# Determine target message count based on content type
case "$CONTENT_TYPE" in
    website-hub)
        TARGET_MESSAGES="4-5"
        BRAINSTORM_COUNT=10
        ;;
    book-chapter)
        TARGET_MESSAGES="6-8"
        BRAINSTORM_COUNT=15
        ;;
    blog-post)
        TARGET_MESSAGES="4-6"
        BRAINSTORM_COUNT=12
        ;;
    white-paper)
        TARGET_MESSAGES="8-12"
        BRAINSTORM_COUNT=20
        ;;
    documentation)
        TARGET_MESSAGES="varies"
        BRAINSTORM_COUNT=12
        ;;
    *)
        echo "❌ Unknown content type: $CONTENT_TYPE"
        exit 1
        ;;
esac

echo "🎯 Topic: $TOPIC"
echo "📄 Content Type: $CONTENT_TYPE"
echo "💡 Target Messages: $TARGET_MESSAGES"
echo ""
```

#### Step 3: Check for Evidence Files

```bash
# Look for evidence files in project
EVIDENCE_FILES=$(find . -maxdepth 2 -name "*evidence*" -o -name "*sources*" -o -name "*references*" 2>/dev/null | head -5)

if [ -n "$EVIDENCE_FILES" ]; then
    echo "📚 Found evidence files:"
    echo "$EVIDENCE_FILES" | sed 's/^/  - /'
    echo ""
else
    echo "⚠️  No evidence files found. You'll need sources to verify messages."
    echo ""
    echo "Recommended: Create evidence-manifest.md with:"
    echo "  - Direct measurements (Tier 1)"
    echo "  - Case studies / research papers (Tier 2)"
    echo "  - Calculated estimates with sources (Tier 3)"
    echo ""
fi
```

#### Step 4: Invoke Message Architect Agent

```bash
echo "🏗️  Invoking message-architect agent with Sequential Thinking..."
echo ""
```

Now use the Task tool to invoke the `message-architect` agent:

**Agent Task**:
- Load `pyramid-principle` skill for deep methodology
- Brainstorm $BRAINSTORM_COUNT key messages for topic
- Use Sequential Thinking MCP for MECE analysis
- For each message:
  - Verify evidence availability (Tier 1-3 only)
  - Rate confidence (high/medium/low)
  - Identify gaps or overlaps
- Present messages to user with evidence status
- Guide user to select $TARGET_MESSAGES verified messages
- Cluster selected messages into MECE hierarchy
- Identify apex message (top of pyramid)

**Agent Inputs**:
- Topic: "$TOPIC"
- Content type: "$CONTENT_TYPE"
- Target message count: $TARGET_MESSAGES
- Evidence files: $EVIDENCE_FILES (if available)

**Agent Outputs** (saved to state):
- Brainstormed messages (all $BRAINSTORM_COUNT)
- Evidence verification status per message
- User-selected messages ($TARGET_MESSAGES)
- MECE hierarchy (apex + supporting)
- Identified evidence gaps

#### Step 5: Save State

After agent completes and user selects messages:

```bash
# Generate content ID from topic
CONTENT_ID=$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-' | cut -c1-50)

# Create writing-state.json
cat > "$STATE_FILE" << EOF
{
  "content_id": "$CONTENT_ID",
  "topic": "$TOPIC",
  "content_type": "$CONTENT_TYPE",
  "phase": "message-definition-complete",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "updated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",

  "sif_layers": {
    "layer1_frame": null,
    "layer2_mode": null,
    "layer3_snippets_used": [],
    "layer4_readability_target": 65
  },

  "evidence": {
    "manifest_file": "evidence-manifest.md",
    "verified_claims": 0,
    "needs_verification": 0,
    "tier1_sources": 0,
    "tier2_sources": 0,
    "tier3_sources": 0
  },

  "messages": {
    "brainstormed": [],
    "selected": [],
    "hierarchy": {
      "apex": "",
      "supporting": []
    }
  },

  "outline": {
    "sections": []
  },

  "drafts": {},

  "quality": {
    "overall_readability": null,
    "pyramid_compliant": null,
    "diataxis_aligned": null,
    "evidence_coverage": null,
    "mece_validated": true
  }
}
EOF

echo "✅ State initialized: $STATE_FILE"
echo ""
```

The message-architect agent will update this state with actual message data.

#### Step 6: Summary and Next Steps

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Phase 1 Complete: Message Definition"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Selected Messages: $(cat $STATE_FILE | jq -r '.messages.selected | length')"
echo "Apex Message: $(cat $STATE_FILE | jq -r '.messages.hierarchy.apex')"
echo "Evidence Status: $(cat $STATE_FILE | jq -r '.evidence.verified_claims') verified"
echo ""
echo "Next Phase: /frame-content [SCQA|Pyramid] [Tutorial|HowTo|Reference|Explanation]"
echo ""
echo "💡 Tip: Review writing-state.json to see your message hierarchy"
echo ""
```

---

## Evidence-First Enforcement

**Critical**: Every message must have evidence BEFORE user selection.

### Evidence Hierarchy

**Tier 1: Direct Measurement** ✅ Always acceptable
- System logs, benchmarks, analytics
- Example: "Reduced build time from 45s to 12s (73% improvement)"

**Tier 2: Documented Evidence** ✅ Cite sources
- Case studies, research papers, published data
- Example: "Pyramid Principle increases comprehension 25% (McKinsey 2018)"

**Tier 3: Derived/Estimated** ⚠️ Heavy qualification required
- Calculations from Tier 1/2 data
- Example: "~15-20 hours saved monthly (3 hrs/week × 4 weeks)"

**Tier 4: NEVER USE** ❌ Automatic rejection
- Assumptions, aspirational, vague, fabricated
- ❌ "Dramatically improves productivity"
- ❌ "Industry-leading performance"
- ❌ "Significant ROI"

### Red Flags (Agent Must Catch)

Agent must flag and reject:
- Vague quantifiers: "significant", "substantial", "dramatic"
- Unsourced comparisons: "faster than competitors", "best in class"
- Aspirational language: "will revolutionize", "transforms"
- Round numbers without measurement: "saves 50% time"
- Fabricated metrics: "70-90% improvement" without source

### Pre-Selection Checklist

Before user selects messages, agent verifies:
- [ ] Every message has Tier 1-3 evidence
- [ ] No Tier 4 violations
- [ ] Sources cited for Tier 2/3
- [ ] Quantified claims have measurement basis
- [ ] Confidence ratings include evidence quality

---

## Content Type Adaptations

### Website Hub (800-2K words)
- **Message Count**: 4-5 (concise, persuasive)
- **Apex Messages**: 1 primary
- **Tone**: Persuasive, action-oriented
- **Evidence**: High Tier 1/2 ratio (build trust)

### Book Chapter (6-8K words)
- **Message Count**: 6-8 (comprehensive, educational)
- **Apex Messages**: 2-3 per chapter
- **Tone**: Educational, thorough
- **Evidence**: Mixed Tier 1-3 (show work)

### Blog Post (1.5-3K words)
- **Message Count**: 4-6 (engaging, insightful)
- **Apex Messages**: 1-2
- **Tone**: Conversational, practical
- **Evidence**: Tier 1-2 (credibility)

### White Paper (5-15K words)
- **Message Count**: 8-12 (authoritative, comprehensive)
- **Apex Messages**: 3-5
- **Tone**: Formal, analytical
- **Evidence**: Heavy Tier 2 (research-backed)

### Documentation (varies)
- **Message Count**: Task-focused (varies)
- **Apex Messages**: Clear action per section
- **Tone**: Instructional, precise
- **Evidence**: Tier 1 (direct measurements)

---

## MCP Tools

### Sequential Thinking (Preferred)
Use for:
- MECE validation (check mutual exclusivity and exhaustiveness)
- Message clustering (optimal hierarchy)
- Evidence gap analysis (identify missing sources)

**Invocation**: Invoke via message-architect agent

### Context7 (Optional)
Use for:
- Researching Pyramid Principle methodology
- Finding evidence sources for claims
- Validating messaging frameworks

---

## Error Handling

### No topic provided
```
❌ Error: Topic required

Usage: /define-messages [topic] [content-type]

Example: /define-messages "ML for trading fundamentals" book-chapter
```

### Invalid content type
```
❌ Unknown content type: [type]

Valid types: website-hub, book-chapter, blog-post, white-paper, documentation
```

### Evidence verification failures
```
⚠️  Evidence Verification Issues:

Message 3: "Dramatically improves performance"
  - Issue: Tier 4 violation (vague quantifier)
  - Fix: Replace with measured improvement or remove

Message 7: "70-90% token reduction"
  - Issue: Unsourced metric
  - Fix: Provide measurement source or reframe as estimate

Cannot proceed to user selection until all messages have Tier 1-3 evidence.
```

### State file exists
```
⚠️  Existing writing-state.json found.

Current phase: [phase]
Content: [topic]

Options:
1. Continue from current phase
2. Start fresh (overwrite existing state)

Choice (1 or 2):
```

---

## Examples

### Example 1: Website Hub

```bash
/define-messages "Applied AI bridges strategy and execution" website-hub
```

**Agent Output** (after brainstorming):
```
🏗️  Brainstormed 10 Messages:

1. "Applied AI connects business strategy to technical execution" [Evidence: ✅ Tier 1]
2. "We architect AI systems aligned with business outcomes" [Evidence: ✅ Tier 2]
3. "Our clients see measurable ROI within 90 days" [Evidence: ⚠️ Tier 3 - needs calculation]
4. "We build production-grade AI, not prototypes" [Evidence: ✅ Tier 1]
5. "Strategy without execution is hallucination" [Evidence: ✅ Original insight]
6. "We've delivered 15 AI systems to production" [Evidence: ✅ Tier 1 - portfolio]
7. "Dramatically transforms business operations" [Evidence: ❌ Tier 4 - REJECT]
8. "Clients achieve industry-leading performance" [Evidence: ❌ Tier 4 - REJECT]
9. "We measure outcomes, not just outputs" [Evidence: ✅ Tier 2 - case studies]
10. "Technical excellence meets business pragmatism" [Evidence: ✅ Philosophy]

✅ Verified Messages: 8/10 (2 rejected for Tier 4 violations)

Select 4-5 messages:
```

**User Selection**: 1, 2, 4, 5, 9

**MECE Clustering**:
```
Apex: "Applied AI bridges strategy and execution" (Message 1)

Supporting:
├─ Technical Excellence (Messages 2, 4)
│  ├─ Architecture aligned with outcomes
│  └─ Production-grade systems
└─ Business Pragmatism (Messages 5, 9)
   ├─ Strategy must execute
   └─ Measure real outcomes

MECE Validation: ✅ Mutually exclusive, collectively exhaustive
```

### Example 2: Book Chapter

```bash
/define-messages "Chapter 3: Time series analysis fundamentals" book-chapter
```

**Agent Output**:
```
🏗️  Brainstormed 15 Messages:

[15 messages with evidence verification...]

✅ Verified Messages: 13/15

Select 6-8 messages:
```

**User Selection**: [6-8 messages]

**MECE Clustering**:
```
Apex: "Time series analysis reveals patterns in sequential data"

Supporting:
├─ Core Concepts (3 messages)
├─ Mathematical Foundations (2 messages)
├─ Practical Applications (2 messages)
└─ Common Pitfalls (1 message)
```

---

## Quality Checklist

Before completing Phase 1:

- [ ] Topic clearly defined
- [ ] Content type selected and appropriate
- [ ] Target message count achieved
- [ ] All messages have Tier 1-3 evidence
- [ ] No Tier 4 violations
- [ ] MECE hierarchy validated
- [ ] Apex message identified
- [ ] User approved selected messages
- [ ] State saved to writing-state.json
- [ ] Evidence gaps documented (if any)

---

## Troubleshooting

**Agent stuck on message generation?**
- Check if Sequential Thinking MCP is available
- Ensure pyramid-principle skill is loaded
- Verify evidence files are readable

**Too many Tier 4 rejections?**
- Review evidence manifest first
- Gather more Tier 1/2 sources before brainstorming
- Adjust messaging to match available evidence

**MECE validation failing?**
- Look for overlapping messages (merge them)
- Check for coverage gaps (add messages)
- Ensure each message serves single purpose

**User can't decide which messages to select?**
- Show evidence quality per message
- Recommend high-confidence, high-evidence messages
- Explain how each supports apex message

---

## Next Steps

After Phase 1 completion:

**Phase 2**: `/frame-content [frame] [mode]`
- Apply SCQA or Pyramid framing
- Select Diátaxis documentation mode
- Create narrative structure

**Alternative**: Add more evidence
- If evidence gaps identified
- Before proceeding to framing
- Update evidence-manifest.md

---

**Remember**: You cannot write a claim you cannot source. Evidence-first is non-negotiable.
