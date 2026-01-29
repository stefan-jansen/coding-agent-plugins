# Extraction Patterns

Detailed guidance for extracting actionable content from paper summaries.

## Summary.json Structure

Each paper has a `summary.json` with these extractable fields:

```json
{
  "reader_summary": { "tldr", "didactic_summary", "why_it_matters" },
  "hypothesis": { "main_claim", "research_question", "novelty" },
  "methodology": { "approach", "data", "technique", "identification" },
  "findings": [{ "claim", "evidence", "nuance", "section" }],
  "actionable_insights": [{ "insight", "context", "caveat" }],
  "key_exhibits": [{ "exhibit", "description", "key_number" }],
  "quotes": [{ "text", "section", "use_case" }],
  "limitations": ["..."],
  "chapter_relevance": { "primary", "secondary", "fit_explanation" }
}
```

## High-Value Fields (Extract These)

### 1. `findings[]` - The Core Content

**What it contains**: Specific claims with supporting evidence.

```json
{
  "claim": "Momentum strategies profitable over 3-12 month horizons",
  "evidence": "Portfolios formed on past 3-12 month returns outperform by 1% per month",
  "nuance": "Effect stronger for small-cap stocks but decays after 12 months",
  "section": "Empirical Results"
}
```

**How to use**:
- `claim` → Core statement to include in prose
- `evidence` → Specific number/result to cite
- `nuance` → Important qualification to mention
- `section` → Where in paper (for deep verification if needed)

**Example extraction → prose**:
> Momentum strategies generate significant returns over intermediate horizons. Jegadeesh and Titman (1993) [ref:ABCD1234] found that portfolios formed on 3-12 month past returns outperform by approximately 1% per month, with effects particularly pronounced for small-cap stocks.

### 2. `actionable_insights[]` - Implementation Guidance

**What it contains**: Practical takeaways a reader can implement.

```json
{
  "insight": "Use 1-month skip period between ranking and holding",
  "context": "When constructing momentum portfolios to avoid microstructure effects",
  "caveat": "Skip period may reduce returns but improves implementability"
}
```

**How to use**:
- `insight` → The technique/method to describe
- `context` → When/why to apply it
- `caveat` → Important limitation to note

**Example extraction → prose**:
> When implementing momentum strategies, practitioners typically skip the most recent month between the ranking period and portfolio formation. This skip period, documented by Jegadeesh and Titman (1993) [ref:ABCD1234], helps avoid microstructure contamination, though it may modestly reduce raw returns.

### 3. `key_exhibits[]` - Concrete Numbers

**What it contains**: Tables, figures, and specific statistics worth citing.

```json
{
  "exhibit": "Table 3: Monthly Returns by Formation Period",
  "description": "Shows momentum profits across different lookback windows",
  "key_number": "12-month/12-month strategy: 1.31% monthly excess return"
}
```

**How to use**:
- `key_number` → Specific statistic to include
- `exhibit` → Reference for readers who want to verify
- `description` → Context for the number

**Example extraction → prose**:
> The optimal configuration uses a 12-month lookback with a 12-month holding period, generating 1.31% monthly excess returns in the Jegadeesh and Titman (1993) [ref:ABCD1234] study.

### 4. `quotes[]` - Direct Authority

**What it contains**: Exact quotations for emphasis.

```json
{
  "text": "Adding more factors does not necessarily improve explanatory power",
  "section": "Factor Selection",
  "use_case": "Arguing for parsimony in factor models"
}
```

**How to use**:
- Use sparingly - 1-2 quotes per section maximum
- Best for controversial claims or memorable phrasing
- Always include page/section context

**Example extraction → prose**:
> As Rudin et al. (2024) [ref:25E4TU3C] caution: "Adding more factors does not necessarily improve explanatory power and may introduce noise that detracts from a model's effectiveness."

## Medium-Value Fields (Use Selectively)

### `reader_summary.why_it_matters`

Good for understanding paper relevance, but too academic for direct inclusion.

**Use for**: Deciding which papers to deep-dive on.
**Don't use for**: Direct prose inclusion.

### `methodology.technique`

Good for technical sections describing methods.

**Use for**: "The authors employ [technique]..." descriptions.
**Don't use for**: Unless the technique itself is the point.

### `limitations[]`

Good for honest caveats and scope notes.

**Use for**: "However, this approach assumes..." qualifications.
**Example**:
> These results assume frictionless trading; real-world implementation must account for transaction costs that can erode a significant portion of raw momentum profits.

## Low-Value Fields (Usually Skip)

### `didactic_summary`

Academic overview pitched for PhD students. Rarely actionable.

**Skip unless**: You need to understand paper's overall contribution.

### `builds_on[]`

Citation genealogy. Useful for literature review, not practical content.

**Skip unless**: Writing a "prior work" section.

### `hypothesis.novelty`

Academic framing of contribution. Not actionable.

**Skip unless**: Comparing papers' approaches.

## Synthesis Patterns

### Pattern 1: Converging Evidence

Multiple papers support the same finding:

```markdown
The momentum effect is robust across markets. Jegadeesh and Titman (1993)
[ref:ABCD1234] established the pattern in US equities, while Rouwenhorst
(1998) [ref:EFGH5678] confirmed it in European markets, and Chui et al.
(2010) [ref:IJKL9012] documented similar effects in Asia.
```

### Pattern 2: Conflicting Evidence

Papers disagree - note the tension:

```markdown
The source of momentum profits remains debated. Jegadeesh and Titman (1993)
[ref:ABCD1234] attribute returns to behavioral underreaction, while Conrad
and Kaul (1998) [ref:MNOP3456] argue the pattern reflects cross-sectional
variation in expected returns.
```

### Pattern 3: Evolution of Understanding

Papers build on each other:

```markdown
Understanding of momentum has evolved. Early work by Jegadeesh and Titman
(1993) [ref:ABCD1234] documented the anomaly. Carhart (1997) [ref:QRST7890]
formalized it as a risk factor. More recently, Daniel and Moskowitz (2016)
[ref:UVWX2345] explained the periodic crashes that plague the strategy.
```

## Anti-Patterns (Avoid)

### 1. Citation Stacking

❌ **Wrong**: "Momentum is important (Smith, 2010; Jones, 2012; Brown, 2015; etc.)."

✅ **Right**: Extract specific findings from 2-3 key papers.

### 2. Generic Attribution

❌ **Wrong**: "Research shows that momentum strategies work."

✅ **Right**: "Jegadeesh and Titman (1993) [ref:ABCD1234] found 1% monthly returns."

### 3. Decoration Citations

❌ **Wrong**: Write prose first, then search for papers to cite.

✅ **Right**: Extract paper findings first, then write prose shaped by them.

### 4. Summary Regurgitation

❌ **Wrong**: Copy `didactic_summary` into prose.

✅ **Right**: Extract specific `findings` and `actionable_insights`.

## Quick Reference: What to Extract

| Writing Need | Extract From | Detail Level |
|--------------|--------------|--------------|
| Core technique | `findings[].claim + evidence` | sections |
| Implementation guidance | `actionable_insights[]` | sections |
| Specific numbers | `key_exhibits[].key_number` | sections |
| Authority quote | `quotes[]` | sections |
| Context/relevance | `why_it_matters` | summary |
| Limitations | `limitations[]` | sections |
