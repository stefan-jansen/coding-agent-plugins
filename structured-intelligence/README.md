# Structured Intelligence Framework (SIF) Plugin

**Version**: 1.0.0
**Type**: Claude Code Plugin
**Category**: Content Creation & Technical Writing

## Overview

The Structured Intelligence Framework (SIF) plugin implements a comprehensive, evidence-based system for hierarchical content creation. It combines proven methodologies from consulting (Pyramid Principle), technical communication (Diátaxis), and information architecture (DITA) into a unified workflow for creating technical content at scale.

## Core Philosophy

**"Structure exists to serve the information-seeking behavior of a time-constrained user"**

SIF enforces:
- **Evidence-First**: Every claim must have verifiable evidence before writing
- **Top-Down Structure**: Answer first, then supporting arguments (Pyramid Principle)
- **User Intent Mapping**: Content type driven by user needs (Diátaxis)
- **Modular Content**: Reusable snippets with variable management (DITA-inspired)
- **Cognitive Load Reduction**: Chunking, signaling, and readability optimization

## Architecture: 4 Layers

### Layer 1: Interaction (Pyramid Principle)
- **Answer-first** communication
- **MECE** (Mutually Exclusive, Collectively Exhaustive) reasoning
- Top-down logical structure
- SCQA framing (Situation-Complication-Question-Answer)

### Layer 2: Architecture (Diátaxis)
- **Tutorial**: Learning-oriented (hands-on lessons)
- **How-To**: Problem-oriented (step-by-step guides)
- **Reference**: Information-oriented (technical descriptions)
- **Explanation**: Understanding-oriented (discussion and clarification)

### Layer 3: Content Management (DITA-Inspired)
- Topic-based modular content
- Reusable snippets (conrefs)
- Variable management (keyrefs)
- Separation of content and presentation

### Layer 4: Presentation (Information Mapping)
- Chunking, labeling, consistency
- F-shaped reading pattern optimization
- Scannability and visual hierarchy
- Plain language principles

## Workflow: 5 Phases

### Phase 1: Message Definition
**Command**: `/define-messages [topic] [content-type]`

1. Brainstorm 10 key messages using Pyramid Principle
2. Verify evidence for each message (Evidence-First)
3. User selects 4-5 verified messages
4. MECE clustering into hierarchy

**Agent**: `message-architect` (with Sequential Thinking for deep analysis)

### Phase 2: Narrative Framing
**Command**: `/frame-content [SCQA|Pyramid] [Tutorial|HowTo|Reference|Explanation]`

1. Apply SCQA (if persuasive) or Pyramid (if explanatory)
2. Select Diátaxis mode based on user intent
3. Create story structure
4. Map messages to narrative arc

**Agents**: `narrative-framer`, `diataxis-planner`, `analyst`

### Phase 3: Outline Expansion
**Command**: `/expand-outline`

1. Convert messages → hierarchical bullets
2. Generate topic sentences per bullet
3. Validate MECE structure
4. Check evidence coverage

**Agent**: `outline-expander`

### Phase 4: Content Generation
**Command**: `/draft-section [section-id]`

1. Apply Diátaxis template for mode
2. Insert DITA snippets if applicable
3. Generate paragraphs maintaining message hierarchy
4. Format with Information Mapping rules
5. Validate claims against evidence manifest

**Agents**: `section-drafter`, `evidence-validator`

### Phase 5: Quality Assurance
**Command**: `/review-content [section-id]`

1. Readability metrics (Flesch-Kincaid)
2. Structural integrity (Pyramid/Diátaxis/MECE)
3. Evidence verification
4. Plain language compliance
5. Generate quality dashboard

**Agent**: `formatter`

## Utility Commands

### `/propose [idea]`
Use SCQA framework to propose ideas persuasively:
- **Situation**: Current state
- **Complication**: Problem or gap
- **Question**: What should we do?
- **Answer**: Your proposal with evidence

**Agent**: `analyst` (Pyramid Principle expert)

### `/summarize [@file]`
Generate executive summary using Pyramid Principle:
- Apex message (1-2 sentences)
- Supporting arguments (MECE grouped)
- Evidence-backed conclusions

**Agent**: `analyst`

## Content Types

SIF adapts behavior based on `content_type`:

### Website Hub (`website-hub`)
- **Length**: 800-2,000 words
- **Apex Messages**: 1-2 max
- **Frame**: SCQA + Pyramid (persuasive)
- **Iteration**: Fast, minimal editing
- **Diátaxis Mode**: Usually Explanation or How-To

### Book Chapter (`book-chapter`)
- **Length**: 6,000-8,000 words
- **Apex Messages**: 2-4 per chapter
- **Frame**: Pyramid + Topic Sentences (educational)
- **Iteration**: Multi-pass editing
- **Diátaxis Mode**: Tutorial or Explanation

### Blog Post (`blog-post`)
- **Length**: 1,500-3,000 words
- **Apex Messages**: 1-3
- **Frame**: SCQA (attention-grabbing)
- **Iteration**: Medium
- **Diátaxis Mode**: Explanation or How-To

### White Paper (`white-paper`)
- **Length**: 5,000-15,000 words
- **Apex Messages**: 3-5
- **Frame**: Pyramid (comprehensive)
- **Iteration**: Heavy editing
- **Diátaxis Mode**: Reference or Explanation

### Documentation (`documentation`)
- **Length**: Varies by section
- **Apex Messages**: Task-focused
- **Frame**: Pyramid (clarity)
- **Iteration**: Continuous
- **Diátaxis Mode**: All four (mapped to sections)

## State Management

SIF maintains state in `writing-state.json` in the content project directory:

```json
{
  "content_id": "hub-strategy-execution",
  "content_type": "website-hub",
  "phase": "outline-expansion",

  "sif_layers": {
    "layer1_frame": "SCQA",
    "layer2_mode": "explanation",
    "layer3_snippets_used": ["intro-applied-ai", "cta-contact"],
    "layer4_readability_target": 65
  },

  "evidence": {
    "manifest_file": "evidence-manifest.md",
    "verified_claims": 4,
    "needs_verification": 0,
    "tier1_sources": 2,
    "tier2_sources": 2
  },

  "messages": {
    "brainstormed": ["...10 messages..."],
    "selected": ["...4 verified messages..."],
    "hierarchy": {
      "apex": "Applied AI bridges strategy and execution",
      "supporting": [
        "We architect technical solutions aligned with business goals",
        "We build production systems that scale",
        "We measure outcomes to prove ROI"
      ]
    }
  },

  "outline": {
    "sections": [
      {
        "id": "intro",
        "message": "Applied AI bridges strategy and execution",
        "bullets": ["...", "...", "..."],
        "topic_sentences": ["...", "...", "..."],
        "evidence_refs": [1, 3, 4]
      }
    ]
  },

  "drafts": {
    "intro": {
      "version": 1,
      "word_count": 287,
      "readability_score": 67,
      "evidence_verified": true,
      "status": "draft"
    }
  },

  "quality": {
    "overall_readability": 65,
    "pyramid_compliant": true,
    "diataxis_aligned": true,
    "evidence_coverage": 1.0,
    "mece_validated": true
  }
}
```

## Skills (Progressive Disclosure)

Skills provide deep methodology expertise:

### `pyramid-principle/`
- MECE reasoning
- Top-down structuring
- Supporting argument grouping
- Logical flow validation

### `scqa-framework/`
- Situation analysis
- Complication identification
- Question framing
- Answer formulation

### `diataxis-framework/`
- User intent classification
- Documentation quadrant mapping
- Template selection
- Mode-specific guidance

### `topic-sentence-method/`
- Bullet → topic sentence conversion
- Paragraph preview generation
- Logical connection maintenance

### `information-mapping/`
- Chunking strategies
- Labeling conventions
- Visual hierarchy
- Scannability optimization

### `plain-language/`
- Active voice conversion
- Sentence simplification
- Jargon elimination
- Readability improvement

## Evidence Hierarchy (Enforced)

**Tier 1: Direct Measurement** (Always acceptable)
- System logs, benchmarks, analytics
- Example: "Reduced build time from 45s to 12s (73% improvement, measured via CI logs)"

**Tier 2: Documented Evidence** (Cite sources)
- Case studies, research papers, published benchmarks
- Example: "Pyramid Principle increases comprehension 25% (McKinsey 2018 study)"

**Tier 3: Derived/Estimated** (Heavy qualification required)
- Calculations from Tier 1/2 data
- Example: "Estimated 15-20 hours saved per month (based on 3 hours/week × 4 weeks)"

**Tier 4: NEVER USE**
- Assumptions, aspirational claims, vague language, fabricated metrics
- ❌ "Dramatically improves productivity"
- ❌ "Industry-leading performance"
- ❌ "Significant ROI"

## Agents

### `message-architect.md`
Brainstorms and clusters key messages using Pyramid Principle + MECE reasoning. Uses Sequential Thinking MCP for deep analysis.

### `analyst.md`
Pyramid Principle expert for summaries and proposals. Structures arguments top-down with evidence.

### `narrative-framer.md`
Applies SCQA framework to create persuasive narrative structure.

### `diataxis-planner.md`
Maps user intent to Diátaxis documentation modes. Selects appropriate templates.

### `outline-expander.md`
Converts messages and bullets into topic sentences. Maintains logical flow and MECE structure.

### `section-drafter.md`
Generates paragraphs from topic sentences. Inserts DITA snippets. Validates evidence.

### `formatter.md`
Applies Information Mapping principles. Optimizes for F-shaped reading. Checks plain language compliance.

### `evidence-validator.md`
Verifies all claims have evidence. Flags Tier 4 violations. Generates evidence manifest.

## MCP Integration

### Preferred Tools
- **Sequential Thinking**: Deep reasoning for message architecture and MECE validation
- **Context7**: Research documentation and methodology references

### Optional Tools
- **Serena**: Code example validation (for technical content)
- **Firecrawl**: Web research for evidence gathering

### Graceful Degradation
All commands work without MCP. MCP tools enhance but never required.

## Installation

Add to project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "local": {
      "source": {
        "source": "directory",
        "path": "/home/stefan/agents/plugins"
      }
    }
  },
  "enabledPlugins": {
    "structured-intelligence@local": true
  }
}
```

## Quick Start

### For Website Content
```bash
# Phase 1: Define messages
/define-messages "Applied AI bridges strategy and execution" website-hub

# Review brainstormed messages, select 4-5

# Phase 2: Frame narrative
/frame-content SCQA explanation

# Phase 3: Expand outline
/expand-outline

# Phase 4: Draft sections
/draft-section intro
/draft-section body-1
/draft-section body-2
/draft-section conclusion

# Phase 5: Quality review
/review-content all
```

### For Book Chapters
```bash
# Phase 1: Define messages
/define-messages "Chapter 3: Time series analysis fundamentals" book-chapter

# Review and select messages

# Phase 2: Frame narrative
/frame-content Pyramid tutorial

# Phase 3: Expand outline
/expand-outline

# Phase 4: Draft sections
/draft-section 3.1-introduction
/draft-section 3.2-concepts
/draft-section 3.3-implementation
/draft-section 3.4-examples

# Phase 5: Quality review
/review-content all
```

## Configuration

Optional configuration in `.claude/sif-config.json`:

```json
{
  "readability_target": 65,
  "evidence_strictness": "strict",
  "default_content_type": "website-hub",
  "snippet_library": ".claude/snippets/",
  "quality_thresholds": {
    "min_readability": 60,
    "max_readability": 70,
    "evidence_coverage": 1.0
  }
}
```

## Cognitive Science Foundation

SIF is built on proven cognitive principles:

### F-Shaped Reading Pattern (Nielsen Norman Group)
Users scan in F-shaped pattern. SIF optimizes:
- First paragraph most important
- Headings scanned vertically
- Front-load important words

### Cognitive Load Theory (Mayer)
Working memory limited to 5-9 chunks. SIF reduces load:
- Chunking information
- Signaling with headings
- Excluding extraneous information
- Progressive disclosure

### Chunking Principle (Miller 1956)
Information grouped improves retention. SIF applies:
- Hierarchical organization
- MECE clustering
- Topic-based modules

## Proven Methodologies

### Pyramid Principle (Barbara Minto, McKinsey)
- **Status**: Near-universal in consulting
- **Evidence**: McKinsey standard since 1970s
- **Benefit**: 25% comprehension improvement (McKinsey 2018)

### Diátaxis (Daniele Procida)
- **Status**: Widely adopted in tech
- **Evidence**: Vonage, Gatsby, Cloudflare documentation
- **Benefit**: Reduced support tickets (Cloudflare case study)

### Information Mapping (Robert Horn)
- **Status**: Mixed empirical evidence, strong anecdotal
- **Evidence**: US military, IBM adoption
- **Benefit**: 47% time reduction in task completion (Horn 1969)

## Quality Metrics

SIF tracks and reports:

### Structural Metrics
- Pyramid compliance (answer-first, MECE)
- Diátaxis alignment (correct mode for user intent)
- MECE validation (no gaps or overlaps)

### Readability Metrics
- Flesch-Kincaid Reading Ease (target: 60-70)
- Average sentence length (target: <20 words)
- Passive voice percentage (target: <10%)

### Evidence Metrics
- Evidence coverage (target: 100%)
- Tier 1/2 ratio (target: >80%)
- Uncited claims (target: 0)

### Efficiency Metrics
- Word count vs. target
- Time to first draft
- Revision cycles required

## Troubleshooting

### Message brainstorming stuck?
- Use Sequential Thinking MCP for deeper analysis
- Review evidence manifest first (verify you have sources)
- Try different content_type (changes message quantity/depth)

### MECE validation failing?
- Check for overlapping arguments (merge or split)
- Look for gaps in coverage (add supporting messages)
- Ensure each message serves single purpose

### Evidence verification errors?
- Review evidence hierarchy (Tier 1-4)
- Replace Tier 4 with Tier 1-2 sources
- Quantify vague claims or remove them

### Readability score too low?
- Shorten sentences (target: <20 words)
- Use active voice
- Replace jargon with plain language
- Break up long paragraphs

## Contributing

See main plugins repository: https://github.com/switwicki/claude-code-plugins

## License

MIT License - See LICENSE file

## Version History

### 1.0.0 (2025-10-27)
- Initial release
- Full SIF implementation (all 4 layers)
- 7 commands, 8 agents, 6 skills
- Evidence-first architecture integrated
- Quality metrics dashboard
- DITA-inspired snippet library

---

**Remember**: Structure exists to serve the reader. Start with evidence, build top-down, map to user intent, and optimize for cognitive ease.
