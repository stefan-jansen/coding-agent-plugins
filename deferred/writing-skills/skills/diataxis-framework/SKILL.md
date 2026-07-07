---
name: diataxis-framework
description: Documentation mode selection based on user intent. Use when writing technical documentation or educational content. Covers 4 modes: Tutorial (learning), How-To (tasks), Reference (information), Explanation (understanding).
---

# Diátaxis Framework Skill

**Developer**: Daniele Procida
**Category**: Documentation Architecture & User Intent Mapping
**SIF Layer**: Layer 2 (Architecture)

## Overview

Diátaxis is a systematic approach to technical documentation that maps user needs to four distinct documentation modes. Each mode serves a different user intent and has unique characteristics.

**Core Insight**: "Documentation serves users with different needs. Match structure to intent."

## The Four Modes

```
              Action-Oriented
                    │
         Tutorial   │   How-To
        (Learning)  │   (Goals)
                    │
────────────────────┼────────────────────
                    │
       Explanation  │  Reference
      (Understanding)│ (Information)
                    │
           Knowledge-Oriented
```

### Tutorial (Learning-Oriented)

**User Says**: "Teach me"
**You Provide**: Hands-on lesson

**Characteristics**:
- Learning by doing
- Step-by-step progression
- Safe environment
- Clear outcomes
- Encouraging tone

**Structure**:
1. What you'll learn
2. Prerequisites
3. Step 1: Action + why
4. Step 2: Action + why
5. Verification
6. Next steps

**Example**: "Build Your First ML Trading Strategy"

**When**: Onboarding, education, skill-building

### How-To (Problem-Oriented)

**User Says**: "Help me solve X"
**You Provide**: Recipe for solution

**Characteristics**:
- Goal-focused
- Assumes knowledge
- Minimal explanation
- Action verbs
- Direct tone

**Structure**:
1. Goal statement
2. Prerequisites
3. Steps (actions only)
4. Verification

**Example**: "How to Optimize Database Queries"

**When**: Task completion, troubleshooting, specific problems

### Reference (Information-Oriented)

**User Says**: "Tell me the facts"
**You Provide**: Technical description

**Characteristics**:
- Comprehensive coverage
- Neutral, dry tone
- Organized for lookup
- No teaching
- Factual

**Structure**:
1. Overview
2. Parameters/Properties
3. Behavior
4. Examples (minimal)
5. Related items

**Example**: "API Endpoint Reference"

**When**: Technical specs, API docs, parameters

### Explanation (Understanding-Oriented)

**User Says**: "Help me understand"
**You Provide**: Conceptual discussion

**Characteristics**:
- Clarifies "why" and "how it works"
- Context and background
- Conversational tone
- No step-by-step
- Insightful

**Structure**:
1. Overview
2. Context (why it matters)
3. How it works
4. Trade-offs
5. When to use
6. Conclusion

**Example**: "Understanding Time Series Stationarity"

**When**: Concepts, design decisions, background

## Mode Selection Matrix

| Content Type | Primary Mode | Secondary Mode |
|--------------|--------------|----------------|
| Website Hub | Explanation | How-To |
| Book Chapter | Tutorial | Explanation |
| Blog Post | Explanation | How-To |
| White Paper | Explanation | Reference |
| API Docs | Reference | How-To |
| Getting Started | Tutorial | - |
| Troubleshooting | How-To | Explanation |

## Mode Characteristics Comparison

| Aspect | Tutorial | How-To | Reference | Explanation |
|--------|----------|--------|-----------|-------------|
| **Tone** | Encouraging | Direct | Neutral | Conversational |
| **Focus** | Learning | Goal | Information | Understanding |
| **Steps** | Yes (detailed) | Yes (minimal) | No | No |
| **Why** | Yes | No | No | Yes (primary) |
| **Audience** | Beginners | Practitioners | All levels | Interested readers |

## Integration with SIF Layers

**Layer 1 (Pyramid)**: Provides logical structure
**Layer 2 (Diátaxis)**: Provides mode-specific template
**Layer 3 (DITA)**: Provides reusable snippets per mode
**Layer 4 (Info Mapping)**: Provides formatting per mode

## Content Adaptation Examples

### Same Content, Different Modes

**Topic**: Database Indexing

**Tutorial**:
"Let's add an index to improve query performance. You'll learn how indexes work and build your first index..."

**How-To**:
"To add an index: 1. Identify slow queries 2. Run CREATE INDEX 3. Verify performance..."

**Reference**:
"CREATE INDEX syntax: CREATE INDEX idx_name ON table(column). Parameters: idx_name (string, required)..."

**Explanation**:
"Indexes improve query speed by creating lookup structures. Think of them like a book's index..."

## Anti-Patterns

### ❌ Mixed Modes

**Bad**: Tutorial that suddenly becomes reference
**Good**: Pick one mode per section

### ❌ Wrong Mode for Intent

**Bad**: Tutorial when user needs quick answer
**Good**: How-To for quick solutions

### ❌ Mode Mismatch with Content Type

**Bad**: Reference mode for website hub
**Good**: Explanation mode for website hub

## Remember

**Match mode to user intent, not your preference**

Four modes cover all documentation needs. Don't invent new modes.

Stay consistent within sections. Mode switches confuse readers.

Evidence-first applies to ALL modes. Quantified claims need sources.
