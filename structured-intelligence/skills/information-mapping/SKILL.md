# Information Mapping

**Purpose**: Apply cognitive science principles (F-pattern reading, chunking, visual hierarchy) to optimize content scannability and comprehension.

**Origin**: Horn (1969), refined by Nielsen eye-tracking studies (2006)

**Use When**: Formatting drafted content for maximum reader comprehension (Phase 5)

---

## Core Principle

**Information Mapping optimizes content for how humans actually read**: F-shaped eye movement patterns and working memory limits (5-9 chunks).

### Why It Matters

- **F-Pattern Reading** (Nielsen 2006): Readers scan first 2 paragraphs, then left edge
- **Working Memory Limit** (Miller 1956): Can only hold 5-9 chunks simultaneously
- **Scannability**: 79% of web users scan, don't read word-for-word (Nielsen)

---

## The Four Pillars

### 1. Chunking (5-9 Rule)

**Principle**: Group information into 5-9 item chunks matching working memory capacity.

**Application**:
- Lists: 5-9 items max; >9 items → create categories
- Paragraphs: 3-6 sentences typically
- Sections: 3-5 paragraphs before subheading

**Examples**:
```markdown
❌ TOO MANY (12 items):
## Configuration Options
- option1, option2, option3, option4, option5, option6,
  option7, option8, option9, option10, option11, option12

✅ CHUNKED (3 categories of 4 items):
## Configuration Options
### Connection Settings (4 items)
- minConnections, maxConnections, timeout, retries

### Performance Settings (4 items)
- poolSize, cacheSize, bufferSize, queueDepth

### Security Settings (4 items)
- encryption, authentication, authorization, auditing
```

### 2. Labeling (Descriptive Headings)

**Principle**: Headings describe content, not generic placeholders.

**Application**:
- ❌ "Introduction", "Overview", "Section 2"
- ✅ "Why Progressive Disclosure Matters", "Three Common Mistakes"

**Examples**:
```markdown
❌ GENERIC:
## Introduction
This section introduces the concept...

✅ DESCRIPTIVE:
## Progressive Disclosure Prevents Cognitive Overload
Progressive disclosure respects working memory limits...
```

### 3. Visual Hierarchy (Consistent Structure)

**Principle**: Heading levels create clear document structure; no skipped levels.

**Application**:
- H1: Document title (one per document)
- H2: Major sections
- H3: Subsections within H2
- Never skip: H1 → H3 (skip H2) ❌

**Validation**:
```
✅ VALID:
H1: Guide Title
├─ H2: Section 1
│  ├─ H3: Subsection 1.1
│  └─ H3: Subsection 1.2
└─ H2: Section 2

❌ INVALID:
H1: Guide Title
└─ H3: Skipped H2! ❌
```

### 4. Scannability (F-Pattern Optimization)

**Principle**: Readers read first paragraphs fully, then scan left edge. Optimize for this pattern.

**F-Pattern (Nielsen Eye-Tracking)**:
```
█████████████████ ← Read fully (heading)
████████████      ← Read fully (first paragraph)
████████          ← Read partially (second paragraph)
█                 ← Scan left edge only
█                 ← Scan left edge only
█                 ← Scan left edge only
```

**Optimization**:
1. **Front-load important info**: First 2 paragraphs most-read
2. **Descriptive first words**: Readers scan left edge of paragraphs
3. **Keywords in headings**: Readers scan headings fully
4. **Bold key terms**: Draws eye on scan
5. **Lists over prose**: Easier to scan bullets than continuous text

**Examples**:
```markdown
❌ BURIED LEAD:
After extensive research and consideration of multiple
frameworks over several months, we determined React
offers the best balance.

✅ FRONT-LOADED:
React offers the best balance of performance and
ecosystem. Our evaluation of 5 frameworks over 3 months
ranked React highest across 12 criteria.
```

---

## Application Guidelines

### By Content Type

**Website Content** (800-2K words):
- Short paragraphs (2-4 sentences)
- Frequent headings (every 3-4 paragraphs)
- Heavy use of lists
- Bold liberally

**Technical Documentation**:
- Medium paragraphs (4-6 sentences)
- Structured with H2/H3 hierarchy
- Tables for reference info
- Code blocks for examples

**Book Chapters** (5-8K words):
- Longer paragraphs acceptable (5-8 sentences)
- Clear heading hierarchy (H1/H2/H3)
- Moderate chunking (sections can be 5-7 paragraphs)
- Scannability via topic sentences

### By Diátaxis Mode

**Tutorial**: Maximum scannability (short sections, visual breaks, steps)
**How-To**: High scannability (numbered steps, minimal prose)
**Reference**: Tables/lists preferred (dense info acceptable)
**Explanation**: Longer sections okay (but maintain hierarchy)

---

## Common Patterns

### Pattern 1: List vs. Prose

**When to use lists**:
- Enumeration: "There are three approaches..."
- Options: "You can configure X, Y, or Z"
- Steps: "First do A, then B, then C"

**When to use prose**:
- Narrative explanation
- Causation: "X causes Y because..."
- Comparison: "Unlike A, B does..."

### Pattern 2: Heading Frequency

**Too Few** (poor scannability):
```
H1: Long Article Title
(50 paragraphs of continuous text) ❌
```

**Good Balance**:
```
H1: Article Title
H2: Section (5-7 paragraphs)
H2: Section (4-6 paragraphs)
H2: Section (6-8 paragraphs)
```

**Too Many** (fragmented):
```
H1: Article
H2: Intro (1 paragraph)
H2: Point 1 (1 paragraph)
H2: Point 2 (1 paragraph)  ← Too granular
```

### Pattern 3: Visual Breaks

Use to prevent walls of text:
- Headings
- Lists
- Code blocks
- Tables
- Blockquotes
- Horizontal rules (sparingly)
- Images/diagrams

**Target**: Visual break every 4-6 paragraphs maximum

---

## Quality Checklist

**Information Mapping compliance**:

- [ ] Lists limited to 5-9 items (or chunked)
- [ ] Paragraphs 3-6 sentences typically
- [ ] Sections 3-5 paragraphs before subheading
- [ ] Headings descriptive, not generic
- [ ] Heading levels consistent (no skipped levels)
- [ ] Important info in first 2 paragraphs
- [ ] Topic sentences front-load keywords
- [ ] Bold used for key terms (not overused)
- [ ] Lists used where enumeration appropriate
- [ ] Visual breaks every 4-6 paragraphs

---

## References

- Horn, R.E. (1969). *Information Mapping*. Original methodology.
- Miller, G.A. (1956). "The Magical Number Seven, Plus or Minus Two". Working memory limits.
- Nielsen, J. (2006). *F-Shaped Pattern for Reading Web Content*. Eye-tracking study.
- Nielsen, J. (1997). "How Users Read on the Web". 79% scan vs. read.
