---
description: Generate content paragraphs from outline topic sentences with evidence validation and Diátaxis template application
system_prompt_append: |
  You are working within the Structured Intelligence Framework (SIF), a hierarchical content creation system.

  **Current Phase**: Drafting (Phase 4 of 5)

  This command converts topic sentences from Phase 3 outlines into full content paragraphs, applying the appropriate Diátaxis template and validating evidence for all claims.

  **Critical Requirements**:
  1. **Evidence-First v2.0.0**: All claims must have Tier 1-3 evidence
  2. **Topic Sentences Lead**: Every paragraph starts with its topic sentence
  3. **Diátaxis Alignment**: Follow template for selected mode (Tutorial/HowTo/Reference/Explanation)
  4. **Hierarchical Flow**: Each paragraph supports parent message
  5. **DITA Snippets**: Insert reusable content where applicable
---

# SIF Command: Draft Section

## Purpose

Generate content paragraphs from topic sentences, applying Diátaxis templates and validating evidence for all claims made.

## Usage

```bash
/draft-section [section-name]

# Examples:
/draft-section introduction
/draft-section "core-concepts"
/draft-section methodology --all  # Draft all sections
```

## Prerequisites

- **Phase 3 Complete**: `writing-state.json` phase must be `"outline-expansion-complete"`
- **Outline Exists**: Section must exist in outline with topic sentences
- **Diátaxis Mode Selected**: Mode must be chosen in Phase 2

## What This Does

1. **Validates Prerequisites**: Checks Phase 3 completion and outline existence
2. **Loads Section Outline**: Retrieves topic sentences and bullet structure
3. **Invokes section-drafter Agent**: Generates paragraphs maintaining hierarchy
4. **Applies Diátaxis Template**: Uses mode-specific structure (Tutorial/HowTo/Reference/Explanation)
5. **Inserts DITA Snippets**: Reuses standardized content where applicable
6. **Validates Evidence**: Invokes evidence-validator to check Tier 1-3 compliance
7. **Updates State**: Records draft in `writing-state.json` with quality metrics
8. **Returns**: Draft content with evidence warnings if any

## State File

**Location**: `writing-state.json` in content project directory

**Updated Fields**:
```json
{
  "phase": "drafting-in-progress",
  "drafts": {
    "introduction": {
      "content": "# Introduction\n\n...",
      "word_count": 847,
      "topic_sentences_count": 5,
      "evidence_items": [
        {"claim": "...", "evidence": "...", "tier": 2}
      ],
      "evidence_violations": [],
      "diataxis_template_applied": "explanation",
      "snippets_used": ["cta-signup", "evidence-note"],
      "created_at": "2025-10-27T16:20:00Z"
    }
  }
}
```

## Command Flow

```
1. Load writing-state.json
2. Validate phase === "outline-expansion-complete"
3. Validate section exists in outline
4. Load Diátaxis mode and templates
5. Invoke section-drafter agent:
   - Provide outline bullets + topic sentences
   - Provide Diátaxis template
   - Provide evidence manifest (if exists)
   - Request paragraph generation
6. Receive draft content
7. Invoke evidence-validator agent:
   - Scan all claims in draft
   - Check against evidence manifest
   - Flag Tier 4 violations
8. Update writing-state.json:
   - Add draft to drafts object
   - Record word count, metrics
   - Store evidence violations
   - Update phase to "drafting-in-progress"
9. Display draft with evidence warnings
10. Prompt: Continue with next section or review?
```

## Example Execution

### Input

**State Context**:
```json
{
  "phase": "outline-expansion-complete",
  "sif_layers": {
    "layer1_frame": "SCQA",
    "layer2_mode": "explanation"
  },
  "outline": {
    "sections": [
      {
        "name": "introduction",
        "topic_sentence": "Content creation for technical audiences requires balancing depth with accessibility.",
        "bullets": [
          {
            "level": 2,
            "text": "Technical accuracy without jargon",
            "topic_sentence": "Technical accuracy means precise statements backed by evidence, not jargon that excludes readers."
          },
          {
            "level": 2,
            "text": "Progressive disclosure",
            "topic_sentence": "Progressive disclosure presents simple concepts first, then layers complexity as reader understanding builds."
          }
        ]
      }
    ]
  }
}
```

**Command**:
```bash
/draft-section introduction
```

### Agent Invocation

**To section-drafter**:
```
Generate content paragraphs for the "introduction" section using the Explanation Diátaxis template.

**Section Topic Sentence**: "Content creation for technical audiences requires balancing depth with accessibility."

**Outline Structure**:
1. Technical accuracy without jargon
   Topic Sentence: "Technical accuracy means precise statements backed by evidence, not jargon that excludes readers."

2. Progressive disclosure
   Topic Sentence: "Progressive disclosure presents simple concepts first, then layers complexity as reader understanding builds."

**Diátaxis Mode**: Explanation (understanding-oriented)
**Template**: explanation.md (analogies, deep dives, connections)

**Evidence Requirement**: All claims must cite Tier 1-3 evidence.

**Output Format**:
- Start each paragraph with its topic sentence
- Provide 3-5 sentences supporting topic sentence
- Include evidence citations: (Author Year) or [Source]
- Maintain hierarchical flow (support parent message)
- Apply Explanation template patterns
```

### Agent Output

```markdown
# Introduction

Content creation for technical audiences requires balancing depth with accessibility. Writers must communicate complex ideas accurately while remaining comprehensible to readers who lack specialized knowledge. This tension between precision and clarity shapes every decision in technical communication.

Technical accuracy means precise statements backed by evidence, not jargon that excludes readers. When we say "our system handles 10,000 requests per second," we're making a falsifiable claim anyone can verify. When we say "our system leverages synergistic paradigms for optimal throughput," we're hiding behind buzzwords that sound technical but mean nothing. Nielsen Norman Group's 2021 usability study found jargon reduces comprehension by 43% while adding zero informational value. Choose simple words that convey exact meaning over complex words that obscure it.

Progressive disclosure presents simple concepts first, then layers complexity as reader understanding builds. Like a teacher starting with addition before algebra, technical writers establish foundational concepts before introducing advanced topics. Mayer's Cognitive Load Theory demonstrates that presenting all information simultaneously overwhelms working memory, which can only process 5-9 chunks at once (Miller 1956). Structure content so each section builds on previous understanding, allowing readers to construct complete mental models incrementally rather than confronting the full complexity upfront.
```

### Evidence Validation

**To evidence-validator**:
```
Scan the following draft for all factual claims and validate evidence tier:

[Draft content above]

Check against evidence manifest:
- Nielsen Norman Group 2021 usability study
- Mayer's Cognitive Load Theory
- Miller 1956 working memory study

Flag any Tier 4 violations (fabricated metrics, unsupported claims).
```

**Validator Response**:
```json
{
  "claims_found": 5,
  "evidence_items": [
    {
      "claim": "handles 10,000 requests per second",
      "status": "example_only",
      "tier": "N/A",
      "note": "Illustrative example, not factual claim"
    },
    {
      "claim": "jargon reduces comprehension by 43%",
      "evidence": "Nielsen Norman Group 2021 usability study",
      "tier": 1,
      "status": "valid"
    },
    {
      "claim": "working memory can only process 5-9 chunks",
      "evidence": "Miller 1956",
      "tier": 1,
      "status": "valid"
    },
    {
      "claim": "Cognitive Load Theory demonstrates presenting all information overwhelms working memory",
      "evidence": "Mayer's Cognitive Load Theory",
      "tier": 1,
      "status": "valid"
    }
  ],
  "violations": [],
  "summary": "All claims properly evidenced. No Tier 4 violations."
}
```

### Output

**Draft Content** (shown above)

**Evidence Report**:
```
✅ Evidence Validation: PASSED

Claims Found: 5
- 4 claims with Tier 1-2 evidence
- 1 illustrative example (not factual claim)
- 0 Tier 4 violations

All factual claims properly supported.
```

**State Update**:
```json
{
  "phase": "drafting-in-progress",
  "drafts": {
    "introduction": {
      "content": "[Draft content above]",
      "word_count": 247,
      "paragraph_count": 3,
      "topic_sentences_count": 3,
      "evidence_items": 3,
      "evidence_violations": [],
      "diataxis_template_applied": "explanation",
      "snippets_used": [],
      "created_at": "2025-10-27T16:20:00Z"
    }
  }
}
```

**Prompt**:
```
Section "introduction" drafted successfully.

Next actions:
- /draft-section [section-name]  # Continue drafting
- /review-content introduction   # Review quality metrics
- /review-content --all          # Review all drafts (when complete)

Remaining sections: 4
```

## Flags

### `--all`
Draft all sections in outline sequentially:
```bash
/draft-section --all
```

### `--skip-evidence-check`
Skip evidence validation (NOT RECOMMENDED):
```bash
/draft-section introduction --skip-evidence-check
```
**Warning**: Only use during rapid iteration. Always validate before finalizing.

### `--use-snippets`
Force DITA snippet insertion where applicable:
```bash
/draft-section conclusion --use-snippets
```

## Integration with Other Commands

### Prerequisites
- `/frame-content` - Sets Diátaxis mode
- `/expand-outline` - Provides topic sentences and structure

### Next Steps
- `/review-content [section]` - Quality metrics and validation
- `/draft-section [next-section]` - Continue drafting
- When all sections done → Phase 5: Review

## Diátaxis Template Application

### Tutorial Mode
**Pattern**: Step-by-step learning, action-oriented
**Example Structure**:
```
Topic Sentence (Action + Result pattern)
1. Concrete step with example
2. Expected outcome
3. What you learned
4. Connection to next concept
```

### How-To Mode
**Pattern**: Problem-solving, solution-focused
**Example Structure**:
```
Topic Sentence (Problem + Solution pattern)
1. Problem context
2. Solution approach
3. Implementation steps
4. Outcome/benefit
```

### Reference Mode
**Pattern**: Information delivery, comprehensive
**Example Structure**:
```
Topic Sentence (Definition + Importance pattern)
1. Precise definition
2. Key characteristics
3. Usage context
4. Related concepts
```

### Explanation Mode
**Pattern**: Understanding-oriented, concept exploration
**Example Structure**:
```
Topic Sentence (Concept + Analogy pattern)
1. Concept explanation
2. Analogy or concrete example
3. Why it matters
4. Connections to broader context
```

## Evidence-First Enforcement

### Tier 1-3 Evidence Required
All factual claims must be supported by:
- **Tier 1**: Peer-reviewed research, official documentation
- **Tier 2**: Industry reports, expert testimony, benchmark studies
- **Tier 3**: Case studies, documented experiences, A/B tests

### Tier 4 Prohibited
**Tier 4** = Fabricated metrics, "up to X%", vague claims, unsupported assertions

**Example Violations**:
- ❌ "Reduces errors by up to 90%"
- ❌ "Industry-leading performance"
- ❌ "Users love our product"

**Fixes**:
- ✅ "Reduces errors by 73% in our A/B test of 5,000 users (Q3 2024)"
- ✅ "Processes 50,000 req/sec, 2x faster than nearest competitor (TechBench 2024)"
- ✅ "Net Promoter Score of 68 (n=1,200 respondents, Oct 2024)"

### Evidence Manifest Integration
If `evidence-manifest.json` exists in project:
```json
{
  "sources": [
    {
      "id": "nielsen-2021",
      "citation": "Nielsen Norman Group (2021). Jargon and Comprehension Study.",
      "tier": 1,
      "key_findings": [
        "Jargon reduces comprehension by 43%",
        "Plain language increases task completion by 35%"
      ]
    }
  ]
}
```

The section-drafter agent will cite from this manifest, and evidence-validator will verify citations exist.

## DITA Snippet Library Integration

### Reusable Content
If `resources/snippets/` directory exists with reusable content:

**Example snippets**:
- `cta-signup.md` - Call-to-action signup form
- `code-block-python.md` - Standard Python code block template
- `evidence-note.md` - Evidence disclosure note
- `next-steps-tutorial.md` - Tutorial "Next Steps" section
- `api-endpoint-template.md` - API documentation structure

### Snippet Insertion
section-drafter agent checks outline for snippet markers:
```markdown
• Call to action
  [SNIPPET: cta-signup]
  Topic Sentence: "Sign up to receive updates on new content."
```

Agent inserts snippet content:
```markdown
## Get Updates

Sign up to receive updates on new content.

[Reusable signup form content inserted here]
```

**Benefits**:
- Consistent CTAs across content
- Standardized code examples
- Uniform evidence disclosures
- Faster drafting (no rewriting)

## Quality Metrics

### Recorded in State
```json
{
  "drafts": {
    "section-name": {
      "word_count": 847,
      "paragraph_count": 5,
      "topic_sentences_count": 5,
      "average_paragraph_length": 169,
      "evidence_items": 8,
      "evidence_violations": 0,
      "snippets_used": ["cta-signup"],
      "diataxis_template_applied": "explanation"
    }
  }
}
```

### Phase 5 Review
These metrics feed into `/review-content` command (Phase 5):
- Flesch-Kincaid readability calculation
- Pyramid compliance validation
- Diátaxis alignment check
- Evidence coverage dashboard

## Error Handling

### Phase Not Ready
```
❌ Error: Phase 3 (outline expansion) must be complete before drafting.

Current phase: "narrative-framing-complete"
Required phase: "outline-expansion-complete"

Run: /expand-outline
```

### Section Not Found
```
❌ Error: Section "methodology" not found in outline.

Available sections:
- introduction
- core-concepts
- implementation
- conclusion

Run: /expand-outline to create section
```

### Evidence Violations
```
⚠️ Warning: Draft contains 2 Tier 4 evidence violations:

1. Line 47: "reduces costs by up to 80%" - No evidence provided
   Fix: Provide specific study or remove claim

2. Line 93: "industry-leading performance" - Vague claim
   Fix: Quantify with benchmark data

Continue drafting? (y/n)
```

## Agent Prompts

### section-drafter Agent

See: `agents/section-drafter.md`

**Responsibility**: Generate paragraphs from topic sentences using Diátaxis templates

**Input**:
- Section topic sentence
- Outline bullets with topic sentences
- Diátaxis mode and template
- Evidence manifest (if available)

**Output**:
- Full markdown content
- Topic sentences preserved as paragraph leads
- Evidence citations included
- Template structure applied

### evidence-validator Agent

See: `agents/evidence-validator.md`

**Responsibility**: Verify all claims have Tier 1-3 evidence

**Input**:
- Draft content
- Evidence manifest (if available)

**Output**:
- Claim inventory
- Evidence tier per claim
- Violations list (Tier 4 or missing evidence)
- Remediation suggestions

## Notes

### Performance
- **Average Section**: 500-1000 words, 3-5 minutes
- **Complex Section**: 1500-3000 words, 5-10 minutes
- **Full Document** (5 sections): 15-30 minutes total

### Iterative Refinement
Can re-run `/draft-section` to regenerate:
```bash
/draft-section introduction --force
```
Previous draft overwritten, new version saved.

### Multiple Diátaxis Modes
Some documents mix modes per section:
```json
{
  "sections": [
    {"name": "introduction", "diataxis_mode": "explanation"},
    {"name": "tutorial", "diataxis_mode": "tutorial"},
    {"name": "api-reference", "diataxis_mode": "reference"}
  ]
}
```

Override per section:
```bash
/draft-section api-reference --mode reference
```

## Summary

**draft-section** converts Phase 3 outlines into Phase 4 content by:
1. Loading topic sentences and bullets from outline
2. Invoking section-drafter agent with Diátaxis template
3. Generating paragraphs that maintain hierarchical message flow
4. Inserting DITA snippets for reusable content
5. Validating evidence with evidence-validator agent
6. Recording drafts and metrics in writing-state.json

**Output**: Evidence-validated content ready for Phase 5 review and formatting.
