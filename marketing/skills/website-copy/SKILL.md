# Website Copy & Landing Pages

**Skill Type**: Content Marketing
**Domain**: Conversion-Focused Website Content for Technical Audiences
**Activation Rate**: 5-10% (occasional - only when creating website copy)

---

## Discovery Metadata

```yaml
id: website-copy
version: 1.0.0
description: |
  Evidence-first framework for creating conversion-focused website copy (landing pages,
  hero sections, feature descriptions, pricing pages) for technical audiences. Enforces
  rigorous sourcing: you cannot write a claim you cannot source. Covers evidence
  inventory (FIRST), requirements validation, website templates (hero, features, social
  proof, FAQ, pricing), conversion copywriting formulas (PAS, AIDA, FAB), SEO
  optimization, and CTA patterns. Activates when creating landing pages, product pages,
  feature descriptions, or website content. Use when building marketing websites,
  product launches, or optimizing conversion pages.

keywords:
  - website copy
  - landing page
  - hero section
  - feature description
  - pricing page
  - product page
  - about page
  - FAQ page
  - conversion copy
  - sales page

triggers:
  - "landing page"
  - "website copy"
  - "hero section"
  - "feature description"
  - "pricing page"
  - "product page"
  - "about page"
  - "FAQ"
  - "write copy for"
```

---

## When This Activates

**Situational triggers** (5-10% of conversations):
- Creating landing pages (product launches, campaigns)
- Writing hero sections (homepage, product pages)
- Crafting feature descriptions
- Developing pricing page copy
- Creating About/Team pages
- Writing FAQ sections
- Optimizing existing website copy for conversion

**Does NOT activate during**:
- Blog post writing (use longform-technical-writing skill)
- Social media content (use social-media-content-strategy skill)
- Technical documentation (use development tools)
- Code implementation

**Validation**: If you're creating website pages focused on conversion and user action, this activates.

---

## Part 0: Evidence Inventory (DO THIS FIRST)

### Critical Principle: Evidence-First Architecture

**"You cannot write a claim you cannot source."**

Before writing ANY website copy, you must complete an evidence inventory. This prevents fabricated metrics and unsubstantiated claims.

### Step 1: Identify All Claims in Scope

For each section you plan to write, list the claims you intend to make:

**Example Claims**:
- "70-90% token reduction with semantic code understanding"
- "183 bugs prevented through automated quality gates"
- "Zero state corruption events in 6 months"
- "3-10x productivity improvement"
- "Used by 10,000+ developers"
- "50% faster than competitors"

### Step 2: Source EVERY Claim

For each claim, identify the source. If no source exists, **do not make the claim**.

**Evidence Hierarchy** (from strongest to weakest):

**Tier 1 - Direct Measurement** (USE THESE):
- ✅ Production logs/metrics: "Based on 6 months of production logs from [system]"
- ✅ Benchmark data: "Measured with [tool] on [date] using [methodology]"
- ✅ User analytics: "Google Analytics data from [date range] shows [metric]"
- ✅ Test results: "pytest output from [commit] shows [result]"
- ✅ Git history: "Analysis of commits in [repo] from [date range]"

**Tier 2 - Documented Evidence** (ACCEPTABLE):
- ✅ Case studies: "Customer X reported [metric] in [document/interview]"
- ✅ Published research: "[Author] found [result] in [paper/source]"
- ✅ Third-party reports: "[Organization] published [finding] in [report]"

**Tier 3 - Derived/Estimated** (USE WITH CAUTION):
- ⚠️ Calculated: "Estimated from [data source] using [methodology]"
- ⚠️ Extrapolated: "Based on [sample size] over [period], projected to [result]"
- ⚠️ Industry benchmarks: "[Organization] reports industry average of [metric]"

**Tier 4 - NEVER USE**:
- ❌ Assumptions: "We expect...", "Should be...", "Likely..."
- ❌ Aspirational: "Up to...", "As much as...", "Could achieve..."
- ❌ Vague: "Significant improvement", "Much faster", "Highly effective"
- ❌ Unsourced: "10x better" (than what? measured how? when?)

### Step 3: Document Evidence Sources

Create an evidence manifest BEFORE writing:

```markdown
## Evidence Manifest

### Claim: "70-90% token reduction with semantic code understanding"
**Source**: Production logs from [project name]
**Location**: ~/path/to/logs or [file:line]
**Date**: [When measured]
**Methodology**: Compared token usage with/without Serena MCP across 50 sessions
**Confidence**: High (direct measurement)
**Notes**: Range represents variance across different task types

### Claim: "183 bugs prevented through automated quality gates"
**Source**: Git commit history analysis
**Location**: [repo] commits [date range]
**Methodology**: Grep for "prevented" in pre-commit hook logs
**Confidence**: High (direct count)
**Notes**: Specific bug types documented in [file]

### Claim: "Zero state corruption events in 6 months"
**Source**: Production system logs
**Location**: ~/path/to/error-logs
**Methodology**: Grep for "corruption|state mismatch|invalid state" = 0 results
**Date Range**: [start] to [end]
**Confidence**: High (absence of evidence)
**Notes**: No user-reported state issues in support tickets either

### Claim: "3-10x productivity improvement"
**Source**: User self-reported surveys (3 users)
**Location**: [survey results file]
**Methodology**: Before/after task completion time
**Confidence**: Medium (small sample, self-reported, domain-dependent)
**Notes**: Range reflects different domains (ML book: 8-10x, web dev: 3-5x)
```

### Step 4: Validation Checklist

Before proceeding to write, verify:

- [ ] **Every quantitative claim** has a documented source
- [ ] **Every comparison** has a baseline ("70% faster than [what]?")
- [ ] **Every benchmark** includes methodology and date
- [ ] **Every case study** cites customer/project name or is anonymized with permission
- [ ] **No aspirational claims** without explicit "estimated" or "projected" language
- [ ] **Evidence manifest created** and reviewed

**If ANY checkbox is unchecked**: STOP. Go gather evidence or remove the claim.

### Red Flags (Require Immediate Clarification)

**Fabricated Metrics** (CRITICAL):
- 🚩 Specific numbers without source ("91% improvement" - from where?)
- 🚩 Industry comparisons without third-party data ("faster than competitors" - which ones? measured how?)
- 🚩 User counts without analytics ("used by 10,000 developers" - source?)
- 🚩 Time savings without before/after measurement ("saves 5 hours per week" - based on what?)

**Vague Claims** (UNACCEPTABLE):
- 🚩 "Significant improvement" (quantify or remove)
- 🚩 "Industry-leading performance" (measured how? says who?)
- 🚩 "Best-in-class" (according to whom?)
- 🚩 "Revolutionary" / "Game-changing" (marketing fluff, delete)

**Unsupported Comparisons** (MISSING CONTEXT):
- 🚩 "3x faster" (than what? when? how measured?)
- 🚩 "Reduces costs" (by how much? over what period?)
- 🚩 "Improves productivity" (quantify or provide case study)

### What to Do When Evidence Doesn't Exist

**Option 1: Remove the Claim** (PREFERRED)
- Better to say nothing than make unsourced claims
- Focus on claims you CAN source

**Option 2: Gather Evidence** (IF FEASIBLE)
- Run benchmarks to get data
- Analyze logs/git history
- Survey users if needed
- Document methodology

**Option 3: Qualify Heavily** (LAST RESORT)
- "Based on internal testing..." (not "93% improvement")
- "Early results suggest..." (not "10x productivity")
- "One customer reported..." (not "significant adoption")
- Include sample size, date, limitations

**NEVER Option 4**: Make it up, use aspirational language, or claim without source

---

## Part 1: Requirements Validation

### Question Unclear Specifications

After completing evidence inventory, validate requirements:

**Red Flags** (require clarification):
- 🚩 Multiple conflicting audiences (developers vs. business buyers)
- 🚩 Vague value proposition ("helps developers work better")
- 🚩 No clear conversion goal (what should user DO?)
- 🚩 Competing messages (trying to say too much)
- 🚩 Assumed brand voice without guidelines

**Questions to Ask**:
1. **Who is this page for?** (can you describe the ideal visitor in detail?)
2. **What action do we want them to take?** (signup, purchase, download, contact?)
3. **What's the ONE core message?** (if they remember nothing else, what should it be?)
4. **What's the evidence?** (completed in Part 0)
5. **What's the brand voice?** (technical, conversational, formal, playful?)

**Don't Start Writing Until**:
- ✅ Evidence manifest completed (Part 0)
- ✅ Single clear audience defined
- ✅ One primary conversion goal identified
- ✅ Core message articulated (one sentence)
- ✅ Brand voice guidelines provided or confirmed

---

## Part 2: Website Section Templates

### Hero Section (Above the Fold)

**Purpose**: Communicate value in 5 seconds, drive to CTA

**Structure**:
```markdown
1. Headline (8-12 words)
   - Benefit-focused, not feature-focused
   - Clear, specific, action-oriented
   - Front-load primary keyword (SEO)

2. Subheadline (15-25 words)
   - Expand on headline
   - Address primary pain point
   - Include supporting evidence (1 key metric)

3. Primary CTA (2-4 words)
   - Action verb + benefit
   - High contrast, prominent placement
   - Above the fold, no scrolling required

4. Hero Image/Video (optional)
   - Show product in use (not abstract)
   - Real screenshot > stock photo
   - Annotate key features if complex

5. Trust Indicators (social proof)
   - Customer logos (if applicable)
   - User count (if significant and sourced)
   - Awards/recognition (if legitimate)
```

**Example** (Technical Product):
```markdown
Headline: "Build Production-Ready AI Coding Agents in Days, Not Months"

Subheadline: "Proven patterns from 6+ months production use. Zero state
corruption events. 183 bugs prevented through automated quality gates."

CTA: "View Patterns →"

Trust: "Used by ML researchers, quant traders, and web development teams"
```

**Hero Section Formulas**:

**Formula 1 - Problem → Solution → Proof**:
- Problem: "Tired of [pain point]?"
- Solution: "[Product] lets you [benefit]"
- Proof: "[Metric] in [timeframe]"

**Formula 2 - Outcome → How → Evidence**:
- Outcome: "[Achieve X] with [Product]"
- How: "Using [unique approach]"
- Evidence: "[Case study or metric]"

**Formula 3 - Before/After**:
- Before: "Stop [current painful method]"
- After: "Start [better approach with Product]"
- Evidence: "[Customer] achieved [result]"

### Features Section

**Purpose**: Explain HOW it works, detail capabilities

**Structure** (Per Feature):
```markdown
1. Feature Name (3-5 words)
   - Descriptive, benefit-oriented
   - "Connection Pooling" → "Automatic Connection Management"

2. Benefit Statement (1 sentence)
   - What the user gains
   - Use evidence from manifest

3. How It Works (2-3 sentences)
   - Simple explanation
   - Technical depth appropriate for audience
   - Progressive disclosure (link to docs for details)

4. Code Example or Visual (optional)
   - 5-10 lines of code
   - Screenshot of feature in action
   - Diagram showing workflow

5. Supporting Metric (if available)
   - From evidence manifest only
   - "91% latency reduction in production"
```

**Feature Copywriting Formula (FAB)**:
- **F**eature: What it is
- **A**dvantage: How it's different
- **B**enefit: Why the user cares

**Example**:
```markdown
Feature: "Semantic code search finds functions 90% faster than grep"
Advantage: "Uses AST parsing instead of text matching"
Benefit: "Spend less time searching, more time building"
```

### Social Proof Section

**Purpose**: Build trust through evidence of usage and results

**Types** (Priority Order):

**1. Case Studies** (HIGHEST IMPACT):
```markdown
"[Company/Person] achieved [specific result] using [Product]"

Example: "A quant trading team prevented 8 critical bugs in production
using automated validators, maintaining 100% uptime over 6 months."

Requirements:
- Real customer (named or anonymized with permission)
- Specific, sourced metrics
- Relevant to target audience
```

**2. Testimonials** (HIGH IMPACT):
```markdown
Direct quotes from real users, with attribution:

"[Quote about specific benefit]"
— [Name, Title, Company]

Requirements:
- Permission to use quote
- Real person (no fake names)
- Specific benefit (not generic praise)
- Optional: photo, company logo
```

**3. Usage Statistics** (MEDIUM IMPACT):
```markdown
"Used by [N] [type of users]" OR "[N] [entity] created"

Requirements:
- Sourced from analytics (evidence manifest)
- Significant number (100+ ideally)
- Updated regularly (show growth)

Examples:
- "156 citations managed across 8 book chapters"
- "127 React components generated across 3 projects"
```

**4. Logos/Recognition** (LOW-MEDIUM IMPACT):
```markdown
"Used by teams at:" [Logo grid]

Requirements:
- Permission to display logos
- Actually used by those companies (not "someone at Google tried it once")
- Relevant prestige (unknown startups don't help)
```

### Pricing Page

**Purpose**: Communicate value tiers, enable purchase decision

**Structure**:
```markdown
1. Tier Name (1-2 words)
   - Descriptive: "Starter", "Professional", "Enterprise"
   - NOT: "Bronze", "Silver", "Gold" (meaningless)

2. Target User (1 sentence)
   - "For [type of user] who [use case]"
   - Helps visitor self-select

3. Price (Prominent)
   - Clear, large, high contrast
   - Include currency, billing period
   - "$49/month" NOT "$49" (ambiguity)

4. Key Features (4-6 bullet points)
   - Differentiate from other tiers
   - Start with most valuable
   - Specific quantities ("10 projects" not "multiple projects")

5. CTA Button
   - Tier-appropriate action
   - Free tier: "Start Free"
   - Paid tier: "Start Trial" or "Buy Now"
   - Enterprise: "Contact Sales"

6. Feature Comparison Table (optional)
   - All tiers side-by-side
   - Check marks for included features
   - Highlight recommended tier
```

**Pricing Psychology**:
- **Anchor high**: Show expensive tier first (makes others seem reasonable)
- **Highlight recommended**: Visual prominence on middle tier
- **Annual discount**: "Save 20% with annual billing"
- **Remove barriers**: "No credit card required" for trials

### FAQ Section

**Purpose**: Overcome objections, provide quick answers

**Structure**:
```markdown
1. Question (Natural language, common phrasing)
   - How users actually ask
   - "How does billing work?" NOT "What is the billing methodology?"

2. Answer (2-4 sentences)
   - Direct, clear response
   - Link to docs for details
   - Include example if helpful

3. Categorization (for long FAQs)
   - Pricing & Billing
   - Technical Questions
   - Getting Started
   - Support & Community
```

**FAQ Content Strategy**:
- **Real questions**: From support tickets, sales calls, community
- **Objection handling**: Address common concerns (security, complexity, cost)
- **SEO benefit**: Each Q&A targets long-tail keywords
- **Progressive disclosure**: Link to detailed docs, don't exhaust topic

---

## Part 3: Conversion Copywriting Formulas

### PAS (Problem-Agitate-Solve)

**Use For**: Landing pages, hero sections, feature descriptions

**Structure**:
1. **Problem**: State the pain point clearly
2. **Agitate**: Make the problem feel urgent/costly
3. **Solve**: Present your solution

**Example**:
```markdown
Problem: "Debugging state corruption in AI agents wastes hours per incident"

Agitate: "Each bug investigation takes 2-4 hours. With 50+ incidents over
6 months, that's 100-200 hours of lost development time—equivalent to
one full month of work."

Solve: "Stateless execution eliminates state corruption entirely. Zero
corruption events over 6 months in production."
```

### AIDA (Attention-Interest-Desire-Action)

**Use For**: Full landing pages, sales pages, product launches

**Structure**:
1. **Attention**: Grab with headline/stat
2. **Interest**: Build with features/benefits
3. **Desire**: Create urgency/FOMO
4. **Action**: Drive to CTA

**Example**:
```markdown
Attention: "70-90% Token Reduction in Production AI Agents"

Interest: "Semantic code understanding replaces text search, dramatically
reducing context overhead. Real production data from 6+ months across
ML research, quant trading, and web development."

Desire: "Teams using these patterns report 3-10x productivity improvements.
Join researchers, traders, and engineers already benefiting."

Action: "Download Patterns → [CTA Button]"
```

### FAB (Feature-Advantage-Benefit)

**Use For**: Feature sections, comparison pages, product pages

**Structure**:
1. **Feature**: What it is (technical capability)
2. **Advantage**: How it's different (vs alternatives)
3. **Benefit**: Why user cares (outcome/value)

**Example**:
```markdown
Feature: "File-based persistence using JSON and Markdown"

Advantage: "No database setup or infrastructure required. Everything is
human-readable and git-native."

Benefit: "Start building immediately. Full version history. Debug issues
by reading plain text files."
```

---

## Part 4: SEO Optimization

### Meta Elements (CRITICAL)

**Title Tag** (50-60 characters):
- Most important SEO element
- Keyword front-loaded
- Include benefit or outcome

```html
✅ <title>AI Coding Agent Patterns - Production-Ready Frameworks</title>
❌ <title>Welcome to Our Website - Product Name</title>
```

**Meta Description** (150-160 characters):
- Appears in search results
- Include primary keyword
- Include CTA or benefit
- Avoid duplication across pages

```html
✅ <meta name="description" content="Build production-ready AI coding
agents using proven patterns. 70-90% token reduction. Zero state
corruption. Download framework docs.">

❌ <meta name="description" content="Learn about our product and how
it can help you with your projects.">
```

### H1 Optimization

**Rules**:
- One H1 per page (hero headline)
- Include primary keyword
- 8-12 words optimal
- Match or closely align with title tag

**Examples**:
```markdown
✅ H1: "Production-Ready AI Agent Frameworks for Developers"
❌ H1: "Welcome" (vague, no keywords)
❌ H1: "The Ultimate Revolutionary AI Agent Development Platform for
Modern Cloud-Native Enterprise Teams" (keyword stuffing, too long)
```

### URL Structure

**Best Practices**:
- Descriptive, keyword-rich
- Hyphen-separated (not underscores)
- Lowercase only
- Avoid dynamic parameters when possible

```markdown
✅ /patterns/stateless-execution
✅ /pricing
✅ /case-studies/ml-research

❌ /page?id=123
❌ /patterns_stateless_execution (underscores)
❌ /Patterns/Stateless-Execution (mixed case)
```

### Internal Linking

**Strategy**:
- Link from high-traffic pages to important pages
- Use descriptive anchor text (not "click here")
- 3-5 internal links per page minimum
- Create topic clusters (pillar page + supporting pages)

**Example**:
```markdown
✅ "Learn more about [stateless execution patterns](link)"
❌ "Click [here](link) for more information"
```

---

## Part 5: CTA Patterns

### CTA Hierarchy

**Primary CTA** (One per page):
- Most prominent visually
- Above the fold (hero section)
- Main conversion goal
- Large button, high contrast

**Secondary CTA** (1-2 per page):
- Alternative action
- Less visually prominent
- "Learn More" vs "Start Free Trial"

**Tertiary CTA** (Multiple):
- Inline text links
- Footer links
- "Read documentation"

### CTA Copywriting

**Action Verb + Benefit**:
```markdown
✅ "Start Building Free"
✅ "Download Patterns"
✅ "See How It Works"

❌ "Submit" (no benefit)
❌ "Click Here" (not descriptive)
❌ "Learn More" (vague, overused)
```

**Reduce Friction**:
```markdown
✅ "Start Free Trial - No Credit Card Required"
✅ "Download Now - Takes 2 Minutes"

❌ "Buy Now" (without trial or demo)
❌ "Request Demo" (when self-serve possible)
```

### CTA Placement Strategy

**Hero Section**: Primary CTA (main conversion)
**After Each Major Section**: Secondary CTA (contextual)
**Bottom of Page**: Primary CTA again (for scrollers)
**Sticky Header/Footer**: Persistent access (for long pages)

---

## Part 6: Brand Voice Guidelines

### Applied AI Brand Voice (Example)

If no brand voice provided, ask for these elements:

**Tone**:
- Technical (assumes competence, provides depth)
- Evidence-based (numbers over adjectives)
- Direct (zero marketing fluff, no buzzwords)
- Honest (acknowledges limitations)

**Language**:
- Active voice ("reduces latency" not "latency is reduced")
- Specific numbers ("70-90%" not "significant")
- Short sentences (15-20 words average)
- Technical terms defined on first use

**Avoid**:
- Buzzwords: "revolutionary", "game-changing", "disruptive"
- Hyperbole: "best", "fastest", "most powerful"
- Vague claims: "improves productivity" (quantify or remove)
- Marketing speak: "synergy", "leverage", "optimize" (overused)

**Voice Examples**:
```markdown
✅ "Reduces API latency 91% through connection pooling"
❌ "Dramatically improves performance with cutting-edge optimization"

✅ "Zero state corruption events in 6 months production use"
❌ "Ensures unparalleled reliability and stability"

✅ "Used by ML researchers, quant traders, web development teams"
❌ "Trusted by industry leaders worldwide"
```

---

## Summary: Website Copy Checklist

Before publishing ANY website copy:

### Evidence & Requirements
- [ ] Evidence manifest completed (every claim sourced)
- [ ] No fabricated metrics or unsourced statistics
- [ ] Target audience clearly defined
- [ ] Single primary conversion goal identified
- [ ] Brand voice guidelines confirmed

### Content Quality
- [ ] Hero section communicates value in 5 seconds
- [ ] Features use FAB formula (Feature-Advantage-Benefit)
- [ ] Social proof from real customers/data (sourced)
- [ ] All comparisons include baseline and methodology
- [ ] No marketing fluff or unsupported superlatives

### SEO Optimization
- [ ] Title tag: 50-60 chars, keyword front-loaded
- [ ] Meta description: 150-160 chars, includes CTA
- [ ] H1 matches title tag intent
- [ ] URL is descriptive and keyword-rich
- [ ] 3-5 internal links with descriptive anchors

### Conversion Optimization
- [ ] Primary CTA above the fold, high contrast
- [ ] CTA uses action verb + benefit
- [ ] Secondary CTAs provide alternative actions
- [ ] Friction reduced ("No credit card", "2-min setup")
- [ ] Page has clear conversion flow

### Technical Accuracy
- [ ] All code examples tested and working
- [ ] All metrics include date and methodology
- [ ] All claims verifiable from evidence manifest
- [ ] Limitations acknowledged where relevant

---

## Progressive Disclosure Benefit

**Token efficiency**: This skill's ~7KB content loaded only when creating website copy (5-10% of time) vs embedding in every /write or /plan command (100% overhead).

**Impact**: 90-95% token reduction through occasional activation.

**When active**: Provides evidence-first architecture, website templates, conversion formulas, SEO optimization, and CTA patterns exactly when creating landing pages or website content.

**When dormant**: Only 150-byte metadata consumes context, not full 7KB knowledge base.
