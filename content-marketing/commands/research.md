---
description: Conduct deep, curated research to provide foundation for content creation
task_type: research
requires_agent: researcher
requires_state: positioned
---

# /research - Deep Research Phase

**Purpose**: Conduct deep, curated research that provides evidence-based foundation for content creation, constrained by positioning manifest.

**Philosophy**: Research is curated and purposeful, not random web scraping. Quality > quantity. Pre-filtered ideas that support core message and positioning.

---

## Usage

```bash
/research [content-piece-name] [optional: specific focus areas]
```

**Examples**:
```bash
/research caf-white-paper
/research landing-page "agent frameworks,stateless patterns"
/research blog-post "positioning-first approach"
```

---

## Prerequisites

**Required**:
- ✅ Positioning manifest must exist (run /position first)
- ✅ Work unit must be in "positioned" state

**Checks**:
```bash
# Verify positioning manifest exists
if [ ! -f .claude/work/content/${CONTENT_PIECE}/positioning-manifest.json ]; then
  echo "Error: Positioning manifest not found. Run /position first."
  exit 1
fi
```

---

## What This Command Does

1. **Loads positioning manifest** to understand research constraints
2. **Invokes researcher agent** with manifest + focus areas
3. **Conducts curated research**:
   - Web search for authoritative sources
   - Documentation lookup (Context7 MCP if available)
   - Web content extraction (Firecrawl MCP if available)
   - Existing reference materials
4. **Compiles research report** (deep, structured, evidence-based)
5. **Updates state** to "researched"

---

## Research Constraints from Positioning Manifest

**Core message guides research**:
- Research must support or provide evidence for core message
- Example: Core message = "CAF prevents AI chaos" → Research stateless patterns, constraint enforcement, failure prevention

**Positioning guides depth**:
- Research positioning alternatives mentioned in manifest
- Gather evidence for "why us vs them" claims
- Example: "vs Raw Claude Code" → Research what raw Claude Code provides, what it lacks

**NOT-covering list constrains scope**:
- Explicitly exclude research on NOT-covering topics
- Example: NOT-covering "development history" → Don't research how framework was built

**Success metric influences evidence**:
- Research what makes desired action likely
- Example: Metric = "tutorial completions" → Research what makes tutorials effective

**Audience context guides sources**:
- Technical audience → Technical depth, peer-reviewed sources
- General audience → Accessible explanations, case studies
- Example: "Senior developers" → Research papers, technical blogs, GitHub repos

---

## Research Output: Research Report

**File**: `.claude/work/content/[content-piece-name]/research-report.md`

**Structure**:
```markdown
# Research Report: [Content Piece Name]

## Executive Summary
- Core findings (3-5 bullet points)
- How findings support core message
- Implications for positioning

## Research Questions
(Derived from positioning manifest)
1. Question 1
2. Question 2
3. Question 3

## Findings

### Finding 1: [Topic]
**Source**: [URL or reference]
**Relevance**: How this supports core message
**Key Points**:
- Point 1
- Point 2
- Point 3

**Evidence**:
- Specific data, quotes, examples

### Finding 2: [Topic]
...

## Positioning Evidence
### vs Alternative 1
- Evidence for our approach
- Evidence for their limitations

### vs Alternative 2
...

## Exclusions
(Topics researched but excluded per NOT-covering list)
- Topic 1: Why excluded
- Topic 2: Why excluded

## Research Gaps
- What we didn't find
- What needs further investigation
- What assumptions remain unverified

## Citations
1. [Source 1 with full citation]
2. [Source 2 with full citation]
...

## Synthesis for Outline
- How findings map to potential outline structure
- Which findings are most important for core message
- Suggested organizational pattern
```

---

## Research Quality Standards

**Curated, not comprehensive**:
- ✅ Purposeful source selection
- ✅ Pre-filtered for quality and relevance
- ❌ NOT exhaustive literature review
- ❌ NOT random web scraping

**Deep, not shallow**:
- ✅ 30-page report if needed
- ✅ Synthesis and analysis, not just summaries
- ✅ Evidence-based conclusions
- ❌ NOT surface-level overviews

**Evidence-based, not opinion**:
- ✅ Citations for all claims
- ✅ Data, examples, authoritative sources
- ✅ Multiple perspectives on contested topics
- ❌ NOT unsupported assertions

**Positioned, not neutral**:
- ✅ Research supports positioning
- ✅ Evidence for "why us vs them"
- ✅ Clear relevance to core message
- ❌ NOT academic neutrality

---

## Researcher Agent Responsibilities

**The researcher agent**:
1. Reads positioning manifest to understand constraints
2. Generates research questions from manifest
3. Conducts web search (WebSearch tool)
4. Extracts content from promising sources (Firecrawl MCP if available)
5. Looks up documentation (Context7 MCP if available)
6. Synthesizes findings with clear relevance statements
7. Identifies positioning evidence
8. Documents exclusions per NOT-covering list
9. Notes research gaps
10. Suggests organizational patterns for outline phase

**Quality checks**:
- Every finding includes relevance to core message
- All claims have citations
- Exclusions are documented with rationale
- Research depth matches content importance (white paper > blog post > landing page)

---

## State Management

**Updates work unit state**:
```json
{
  "phase": "researched",
  "timestamp": "2025-10-31T20:00:00Z",
  "research_depth": "deep|moderate|light",
  "sources_count": 15,
  "findings_count": 8,
  "next_command": "/outline"
}
```

**Preserves files**:
- positioning-manifest.json (unchanged)
- research-report.md (created)
- metadata.json (updated with research info)

---

## MCP Tool Usage

**WebSearch** (always available):
- Primary research tool
- Query formulation from positioning manifest
- Source discovery

**Firecrawl MCP** (optional, enhanced):
- Fast web content extraction
- Cleaner markdown output
- Caching for repeated access
- Fallback: WebFetch tool

**Context7 MCP** (optional, enhanced):
- Documentation lookup (resolve-library-id, get-library-docs)
- API reference research
- Technical documentation access
- Fallback: Web search + manual docs

**Graceful degradation**:
- All research possible with core tools
- MCP enhances speed and quality
- No MCP dependency for core functionality

---

## Research Depth Guidance

**White paper** (10-15 pages):
- Deep research (30+ page report expected)
- 20-30 sources
- Multiple perspectives
- Original synthesis
- Research time: 2-4 hours

**Blog post** (2,500 words):
- Moderate research (10-15 page report)
- 8-12 sources
- Focused investigation
- Research time: 1-2 hours

**Landing page** (800 words):
- Light research (5-7 page report)
- 5-8 key sources
- Targeted facts
- Research time: 30-60 minutes

**Social media** (400 words):
- Minimal research (2-3 page notes)
- 2-4 supporting sources
- Quick fact-checking
- Research time: 15-30 minutes

---

## Common Research Patterns

### Pattern 1: Technical Product Research
**For**: Framework, tool, product content
**Research questions**:
- What problem does this solve?
- What alternatives exist?
- What evidence supports effectiveness?
- What are common objections?
- What makes adoption successful?

### Pattern 2: Positioning Research
**For**: Competitive positioning content
**Research questions**:
- What do alternatives provide?
- Where do alternatives fall short?
- What unique value do we provide?
- What evidence supports our positioning?
- What would make someone switch?

### Pattern 3: Educational Content Research
**For**: How-to, tutorial, explanation
**Research questions**:
- What does audience already know?
- What are common misconceptions?
- What are proven teaching methods for this topic?
- What examples are most effective?
- What mistakes do people make?

### Pattern 4: Domain Expertise Research
**For**: Deep-dive, analysis, thought leadership
**Research questions**:
- What's the current state of knowledge?
- What are emerging trends?
- What controversies exist?
- What gaps exist in current understanding?
- What novel insights can we provide?

---

## Example Session

```bash
$ /research caf-white-paper

Loading positioning manifest...
✓ Core message: Transform Claude Code into specialized domain agents
✓ Target audience: Claude Code users (software engineers)
✓ Positioning: Out-of-box → CAF → Agent SDK spectrum

Invoking researcher agent...

Generating research questions from positioning:
1. What capabilities does base Claude Code provide?
2. What is the Agent SDK and its capabilities?
3. What customization patterns exist for Claude Code?
4. What evidence exists for domain-specific agent effectiveness?
5. How do markdown-based frameworks compare to programmatic APIs?

Conducting research...
✓ Web search: Claude Code capabilities [12 sources found]
✓ Web search: Agent SDK documentation [8 sources found]
✓ Documentation lookup: Claude Code docs (Context7)
✓ Web extraction: Key technical articles (Firecrawl)

Synthesizing findings...
✓ 8 major findings compiled
✓ Positioning evidence gathered (CAF vs alternatives)
✓ Exclusions documented per NOT-covering list
✓ Research gaps identified

Research report created: .claude/work/content/caf-white-paper/research-report.md
✓ 28 pages, 18 sources cited
✓ Next command: /outline

Research phase complete. Ready for outline generation.
```

---

## Validation Rules

**Research report must include**:
- ✅ Executive summary with core findings
- ✅ Research questions derived from positioning
- ✅ Findings with clear relevance statements
- ✅ Positioning evidence for alternatives
- ✅ Documented exclusions per NOT-covering list
- ✅ Citations for all sources
- ✅ Synthesis section for outline phase

**Quality checks**:
- Every finding connects to core message
- Sources are authoritative and current
- Evidence > opinion
- Depth matches content importance

---

## When to Skip or Simplify Research

**Skip research when**:
- Content is purely opinion/personal experience
- Topic is well-understood by author
- Positioning doesn't require external validation
- Time constraints demand faster iteration

**Simplify research when**:
- Short-form content (social media, brief blog)
- Internal audience (shared context)
- Iterative drafting with research as needed
- Testing positioning with minimal viable content

**Full research when**:
- External audience with high stakes
- Complex or contested topic
- Positioning requires evidence
- Long-form authoritative content

---

## Integration with Content Workflow

**Standard workflow**:
```
/position → /research → /outline → /draft → /review
```

**Research enables outline**:
- Architect agent receives both positioning manifest AND research report
- Outline structure emerges from findings
- Evidence placement pre-planned
- Core message supported by research

**Research informs draft**:
- Author agent has research citations ready
- Evidence-based writing, not speculation
- Claims backed by sources
- Examples drawn from research

---

## Success Criteria

**Research succeeds when**:
- ✅ Core message has supporting evidence
- ✅ Positioning claims are validated
- ✅ Exclusions are documented
- ✅ Research depth matches content importance
- ✅ Findings synthesized, not just listed
- ✅ Clear path to outline visible

**Research fails when**:
- ❌ Findings don't support core message
- ❌ Research is random/unfocused
- ❌ No synthesis or relevance statements
- ❌ Shallow when deep research needed
- ❌ Sources are low-quality or uncited

**In failure case**: Revisit research questions, refocus on positioning, seek higher-quality sources.

---

## Technical Notes

**File-Based Persistence**:
- Research report stored as markdown
- Citations tracked for later use
- Resumable if interrupted
- Version-controllable

**Idempotency**:
- Safe to re-run research
- Can update/expand existing research
- Preserves downstream work (outline, draft)

**Agent Invocation**:
- Uses researcher agent (see agents/researcher.md)
- Long-running operation (1-4 hours typical)
- Background execution supported

---

**Command Version**: 1.0
**Created**: 2025-10-31
**Agent**: researcher
**Previous Command**: /position
**Next Command**: /outline
**Key Innovation**: Curated research constrained by positioning, not exhaustive exploration
