---
description: Generate Pyramid-based summaries extracting apex message and supporting structure
system_prompt_append: |
  You are working within the Structured Intelligence Framework (SIF).

  This utility command generates hierarchical summaries using Pyramid Principle to extract and organize key messages.
---

# SIF Utility: Summarize

## Purpose

Generate Pyramid-structured summaries from long documents, extracting apex message and MECE-grouped supporting points.

## Usage

```bash
/summarize document.md
/summarize @long-article.md
/summarize --length short   # 100-200 words
/summarize --length medium  # 300-500 words
/summarize --length long    # 800-1000 words
```

## What This Does

1. **Invokes analyst agent** - Pyramid Principle expert
2. **Extracts apex message** - Top-level conclusion or main point
3. **Identifies supporting messages** - MECE-grouped arguments
4. **Validates hierarchy** - Ensures each level supports level above
5. **Generates summary** - Pyramid-structured output

## Pyramid Structure

```
Apex Message (Main Point)
├─ Supporting Message 1
│  ├─ Detail 1a
│  └─ Detail 1b
├─ Supporting Message 2
│  ├─ Detail 2a
│  └─ Detail 2b
└─ Supporting Message 3
   ├─ Detail 3a
   └─ Detail 3b
```

## Output Structure

### Short Summary (100-200 words)
- Apex message (1 sentence)
- 3 supporting messages (1 sentence each)
- No details

### Medium Summary (300-500 words)
- Apex message (1-2 sentences)
- 3-5 supporting messages (1-2 sentences each)
- Key details for each (1-2 sentences)

### Long Summary (800-1000 words)
- Apex message (1 paragraph)
- 4-6 supporting messages (1 paragraph each)
- Details and evidence for each

## Integration

**Uses**:
- `agents/analyst.md` (TASK-018) - Pyramid structure expert
- `skills/pyramid-principle/SKILL.md` - MECE methodology
- **Sequential Thinking MCP** - Complex summarization analysis

**Output**: Summary markdown (console or file)

## Example

```bash
/summarize long-article.md --length medium
```

**Input** (5000 words on progressive disclosure)

**Output**:
```markdown
# Summary: Progressive Disclosure in Technical Writing

## Apex Message
Progressive disclosure respects working memory limits by building complexity
gradually, improving comprehension by 35% (Nielsen 2021).

## Supporting Messages

### 1. Working Memory Constraints Drive Need
Human working memory holds only 5-9 chunks (Miller 1956), making
simultaneous presentation of complex information cognitively overwhelming.

### 2. Incremental Building Enables Understanding
Like teaching addition before algebra, progressive disclosure establishes
foundational concepts before introducing advanced topics.

### 3. Proven Benefits Across Domains
Studies show 35% comprehension improvement (Nielsen), 40% faster task
completion (Mayer), and 60% reduction in cognitive load (Sweller 2005).
```

---

**Status**: Utility command (optional but useful)
**Dependencies**: TASK-001 (Pyramid skill), TASK-018 (analyst agent)
