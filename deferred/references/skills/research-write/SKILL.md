---
name: research-write
description: This skill should be used when the user asks to "write with research", "research-driven draft", "use papers to shape content", "write section with papers", "incorporate research into writing", or when writing ML4T book sections that should be shaped by academic paper findings rather than decorated with citations.
allowed-tools: Read, Write, Bash, mcp__ml4t-refs__search_papers, mcp__ml4t-refs__get_paper, mcp__ml4t-refs__get_chapter_references, mcp__ml4t-refs__find_insights
---

# Research-Write Workflow

Write chapter sections where **papers shape content** rather than decorating pre-written claims.

## The Problem This Solves

**Current pattern (wrong)**:
1. Write prose based on existing knowledge
2. Search for papers vaguely related
3. Add citations to support pre-written claims
4. Papers become "post-hoc decoration"

**Research-write pattern (correct)**:
1. Pull chapter's assigned references
2. Extract findings, insights, exhibits from papers
3. Synthesize into practical takeaways
4. Write content SHAPED BY what papers actually say
5. Citations naturally integrated (evidence → prose)

## Workflow Steps

### Step 1: PULL - Get Chapter References

```
Use: mcp__ml4t-refs__get_chapter_references(chapter=N)
```

This returns papers assigned to the chapter (both AI-assigned and manually curated in Zotero).

**What you get**: List of Zotero keys with basic info (author, year, title, primary/secondary status)

### Step 2: FILTER - Identify Relevant Papers

From the chapter references, identify 3-7 papers most relevant to the **specific section** being written.

**Selection criteria**:
- Primary references (★) for the chapter
- Papers whose `fit_explanation` mentions the section topic
- Papers tagged with relevant keywords

### Step 3: EXTRACT - Get Actionable Content

For each selected paper, use appropriate detail level:

```
# For 2-3 most important papers (deep dive):
mcp__ml4t-refs__get_paper(key="ZOTEROKEY", detail="sections")
# Returns: ~1500 tokens with findings, insights, exhibits, quotes

# For supporting papers (context):
mcp__ml4t-refs__get_paper(key="ZOTEROKEY", detail="summary")
# Returns: ~500 tokens with TLDR, why_it_matters
```

**What to extract** (see [extraction-patterns.md](extraction-patterns.md)):

| Field | What it contains | Use for |
|-------|------------------|---------|
| `findings[]` | Claims + evidence + nuance | Core content, specific techniques |
| `actionable_insights[]` | Practical takeaways + context + caveats | Implementation guidance |
| `key_exhibits[]` | Tables, figures, key numbers | Concrete examples |
| `quotes[]` | Direct quotations | Emphasis, authority |

**What to IGNORE**:
- `didactic_summary` - Academic overview, not actionable
- `builds_on` - Citation genealogy, not content
- Theoretical confirmations without practical implications

### Step 4: SYNTHESIZE - Find the Narrative

Before writing, synthesize extracted content:

1. **Group by theme**: What patterns emerge across papers?
2. **Identify conflicts**: Do papers disagree? (Note this - it's valuable)
3. **Extract techniques**: What specific methods can readers implement?
4. **Note caveats**: What limitations should readers know?

**Output**: A mental map of "what the research actually says" about this section topic.

### Step 5: WRITE - Shape Content from Research

Write the section with research findings as the **foundation**, not decoration:

**Structure**:
1. Open with practical framing (not "Research shows...")
2. Present findings as practical guidance
3. Integrate citations naturally: `Author (Year) [ref:KEY]`
4. Include specific numbers/techniques from papers
5. Note caveats and limitations honestly

**Voice**: See the project's style guide for tone. Research-write produces informed, practical prose - not academic literature reviews.

### Step 6: CITE - Verify Citations

Ensure every paper used is cited with the correct format:
```
Author (Year) [ref:ZOTEROKEY]
```

The 8-character Zotero key enables:
- Grep-based tracking: `grep -oE '\[ref:[A-Z0-9]{8}\]' draft.md`
- Direct links to Zotero library
- Stable references across renames

## Example Usage

**User request**: "Write the section on momentum factors for chapter 7, using research-write"

**Agent workflow**:
```python
# 1. PULL
chapter_refs = get_chapter_references(chapter=7)
# Returns: 45 papers assigned to chapter 7

# 2. FILTER
# Identify papers relevant to "momentum factors":
# - ABCD1234: Jegadeesh & Titman (1993) - Momentum strategies (PRIMARY)
# - EFGH5678: Carhart (1997) - Four-factor model
# - IJKL9012: Daniel & Moskowitz (2016) - Momentum crashes

# 3. EXTRACT
jt_paper = get_paper("ABCD1234", detail="sections")
# Extract: findings on 3-12 month horizon profitability,
#          actionable insight on portfolio formation,
#          exhibit with return statistics

carhart = get_paper("EFGH5678", detail="summary")
# Extract: TLDR on momentum factor construction

# 4. SYNTHESIZE
# Theme: Momentum works but has crash risk
# Techniques: 3-12 month lookback, 1-month skip
# Caveat: High drawdowns during reversals

# 5. WRITE
# Content shaped by actual paper findings, not generic momentum description

# 6. CITE
# "Jegadeesh and Titman (1993) [ref:ABCD1234] demonstrated..."
```

## Token Budget Guidance

| Papers | Detail Level | Approximate Tokens |
|--------|--------------|-------------------|
| 5 papers | summary | ~2,500 tokens |
| 3 papers | sections | ~4,500 tokens |
| Mixed (2 deep + 3 summary) | mixed | ~4,500 tokens |

**Recommendation**: 2-3 deep dives + 3-4 summaries for supporting context.

## Quality Checks

After writing, verify:

- [ ] Content reflects what papers ACTUALLY say (not assumptions)
- [ ] Specific findings/numbers from papers appear in prose
- [ ] Actionable insights are incorporated (not just citations)
- [ ] Limitations and caveats are noted
- [ ] Citations use correct format: `Author (Year) [ref:KEY]`
- [ ] Draft differs meaningfully from "cite as needed" approach

## When NOT to Use

- **No chapter refs available**: Use `/ref-search` first to find relevant papers
- **Pure code examples**: Code sections may not need research integration
- **Quick edits**: Minor revisions don't need full workflow
- **Already research-shaped**: If section was previously written with this workflow

## Related Commands

- `/ref-chapter N` - View chapter's assigned references
- `/ref-search query` - Find papers on a topic
- `/ref-status` - Check sync status

## Supporting Files

- [extraction-patterns.md](extraction-patterns.md) - Detailed patterns for extracting actionable content from summary.json fields
