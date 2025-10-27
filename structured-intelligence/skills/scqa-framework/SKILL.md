# SCQA Framework Skill

**Developer**: Barbara Minto (McKinsey & Company)
**Category**: Persuasive Communication & Problem Framing
**SIF Layer**: Layer 1 (Interaction - Narrative Framing)

## Overview

SCQA (Situation-Complication-Question-Answer) is a narrative framework for persuasive communication. It builds tension through a problem, then resolves it with your solution.

**Core Insight**: "People pay attention when you present a familiar situation, disrupt it with a complication, and offer a solution."

## When to Use

- Persuasive content (proposals, recommendations, marketing)
- Problem-focused content
- Need to build case for action
- Audience may resist or need convincing
- Website hubs, blog posts, pitch decks

## The Four Elements

### S - Situation (Context)

**Purpose**: Establish common ground, set the stage

**Characteristics**:
- Non-controversial
- Familiar to audience
- Current state or common scenario
- No evidence needed (generally accepted)

**Examples**:
- ✅ "Companies invest millions in AI strategy"
- ✅ "Most developers struggle with database optimization"
- ✅ "Time series data is fundamental to trading"

**Don't**:
- ❌ Make controversial claims
- ❌ Start with the problem
- ❌ Assume specialized knowledge

### C - Complication (Problem)

**Purpose**: Create tension, make audience care

**Characteristics**:
- Disrupts the situation
- Evidence-backed (MUST cite Tier 1-3 source)
- Quantified when possible
- Creates gap or problem

**Examples**:
- ✅ "But 70% of AI projects fail to reach production (Gartner 2024)"
- ✅ "Queries slow to 2.3s, causing 15% user churn (analytics)"
- ✅ "Non-stationary series yield 40% prediction error (research)"

**Evidence Requirements**:
- **Tier 1** (Direct measurement): Preferred
- **Tier 2** (Documented): Acceptable with citation
- **Tier 3** (Derived): With clear calculation
- **Tier 4** (Vague): NEVER - "significantly worse", "dramatically failing"

**Don't**:
- ❌ Vague problems: "things could be better"
- ❌ Unsourced claims: "most initiatives fail"
- ❌ Weak tension: "sometimes doesn't work perfectly"

### Q - Question (Focus)

**Purpose**: Direct audience attention to solution

**Characteristics**:
- Often implicit (audience asks themselves)
- Can be explicit when needed
- Natural consequence of complication
- Points toward answer

**Examples**:
- ✅ Implicit: "How do we bridge this gap?"
- ✅ Explicit: "What's the solution?"
- ✅ Implied: [Complication naturally raises question]

**Types**:
- **How** questions: "How do we solve X?"
- **What** questions: "What should we do?"
- **Why** questions: "Why does this happen?"

**Don't**:
- ❌ Multiple questions (confuses focus)
- ❌ Rhetorical questions without answers
- ❌ Questions not addressed by answer

### A - Answer (Solution)

**Purpose**: Resolve tension, provide solution

**Characteristics**:
- Your apex message (from Pyramid)
- Directly answers question
- Supported by evidence
- Actionable or conclusive

**Structure**: Answer becomes your Pyramid
```
Answer (Apex): [Main solution]
├─ Support 1: [Why it works]
├─ Support 2: [How it works]
└─ Support 3: [Evidence it works]
```

**Examples**:
- ✅ "Applied AI bridges strategy and execution"
- ✅ "Indexing reduces query time 73% (from 2.3s to 0.6s)"
- ✅ "Differencing transforms non-stationary to stationary"

**Don't**:
- ❌ Vague answers: "We can help"
- ❌ Multiple answers (pick one apex)
- ❌ Unsupported claims

## SCQA Patterns

### Pattern 1: External Problem

```
S: Industry standard practice
C: Practice has hidden flaw (evidence)
Q: How to avoid flaw?
A: Our approach solves it
```

**Example**:
```
S: Most companies separate strategy and execution teams
C: This causes 70% of AI initiatives to fail in production (Gartner)
Q: How do we prevent this disconnect?
A: Applied AI integrates strategy and execution from day one
```

### Pattern 2: Gap Analysis

```
S: Current state
C: Desired state far from current (evidence)
Q: How to close gap?
A: Specific strategy
```

**Example**:
```
S: Our query response time is 2.3 seconds
C: Industry standard is <1s, users expect sub-second (UX research)
Q: How do we meet expectations?
A: Implement caching and query optimization
```

### Pattern 3: Opportunity

```
S: Status quo
C: New opportunity available (evidence)
Q: How to capitalize?
A: Action plan
```

**Example**:
```
S: We manually review code for bugs
C: AI tools now catch 85% of bugs automatically (GitHub study)
Q: How do we leverage this?
A: Integrate AI code review in CI/CD pipeline
```

## Integration with Pyramid Principle

SCQA provides the **narrative wrapper** around Pyramid structure:

```
SCQA Frame:
  Situation → Context
  Complication → Problem (evidence-backed)
  Question → Focus
  Answer → Pyramid Structure
            Apex: [Answer to Q]
            ├─ Support 1
            ├─ Support 2
            └─ Support 3
```

## Content Type Application

### Website Hub

```
S: What visitors know/experience
C: Problem visitors face (with evidence)
Q: How to solve it?
A: Your solution (apex)
   ├─ Why it works
   ├─ How it works
   └─ Proof it works
```

**Tone**: Engaging, action-oriented

### Blog Post

```
S: Hook with familiar scenario
C: Surprising insight or problem (evidence)
Q: What should we do?
A: Your recommendation
   ├─ Rationale
   ├─ Implementation
   └─ Results
```

**Tone**: Conversational, practical

### Proposal

```
S: Current business context
C: Business problem/opportunity (evidence)
Q: How do we address it?
A: Proposed solution
   ├─ Approach
   ├─ Benefits
   └─ Implementation
```

**Tone**: Professional, persuasive

## Evidence Requirements

### Situation: No Evidence Needed
- Generally accepted facts
- Common knowledge
- Undisputed current state

### Complication: Evidence REQUIRED
- **Must have Tier 1-3 source**
- Quantify when possible
- Cite specific source

**Red Flags** (Tier 4 - REJECT):
- "significantly worse"
- "dramatically failing"
- "most projects fail" (without source)
- "industry-leading" (without benchmark)

### Answer: Supported by Phase 1
- Messages verified in Phase 1
- Evidence carried forward
- Pyramid supports answer

## SCQA Anti-Patterns

### ❌ Weak Complication
**Bad**: "Things could be better"
**Good**: "70% fail (Gartner 2024)"

Vague complications don't create tension.

### ❌ Situation = Complication
**Bad**: Starting with the problem
**Good**: Context first, then problem

Need common ground before disruption.

### ❌ Answer Doesn't Answer Question
**Bad**: Q: "How?" A: "It's important"
**Good**: Q: "How?" A: "Follow these steps"

Answer must directly address question.

### ❌ Multiple Questions
**Bad**: "How do we fix this? What tools? When?"
**Good**: "How do we fix this?"

One question, one focus.

## Quick Reference

**Situation**:
- What: Context, current state
- Tone: Familiar, non-controversial
- Evidence: None needed

**Complication**:
- What: Problem, disruption
- Tone: Urgent, important
- Evidence: **REQUIRED** (Tier 1-3)

**Question**:
- What: Natural inquiry
- Tone: Focused
- Evidence: None needed

**Answer**:
- What: Your pyramid
- Tone: Confident, actionable
- Evidence: From Phase 1 messages

## Remember

**SCQA builds tension, Pyramid provides resolution**

Complication MUST have evidence. No vague problems allowed.

Question should be implicit when possible (reader asks it themselves).

Answer is your Pyramid - don't just state solution, prove it.
