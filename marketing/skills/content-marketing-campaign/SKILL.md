# Content Marketing Campaign

**Skill Type**: Content Marketing
**Domain**: Multi-Channel Campaign Strategy for Technical B2B Products
**Activation Rate**: 10-15% (occasional - only during campaign planning)

---

## Discovery Metadata

```yaml
id: content-marketing-campaign
version: 2.0.0
description: |
  Evidence-first multi-channel campaign framework for launching and sustaining technical
  B2B products. CRITICAL: Enforces rigorous sourcing across all campaign materials - every
  claim must be verified before distribution. Prevents fabricated metrics from propagating
  across channels. Covers evidence verification (FIRST), positioning and messaging hierarchy,
  hub-and-spoke content model, content atomization workflows (1 core → 20+ derivatives),
  multi-channel distribution strategy (tiered channels: owned, community, social), campaign
  coordination (master calendar, dual launches), and performance measurement (developer-centric
  KPIs). Activates when planning product launches, developing campaign strategies, coordinating
  multi-channel content distribution, creating master content calendars, or measuring campaign
  performance. Use when launching products, building topic authority through hub-and-spoke
  clusters, executing content atomization, or managing concurrent marketing campaigns.

keywords:
  - campaign strategy
  - product launch
  - multi-channel campaign
  - content calendar
  - hub and spoke
  - pillar content
  - topic cluster
  - content atomization
  - campaign coordination
  - launch plan
  - campaign measurement

triggers:
  - "campaign strategy"
  - "product launch"
  - "launch plan"
  - "multi-channel campaign"
  - "content calendar"
  - "campaign coordination"
  - "hub and spoke"
  - "pillar content"
  - "topic cluster"
  - "content atomization"
  - "measure campaign"
```

---

## When This Activates

**Situational triggers** (10-15% of conversations):
- Planning product launches (technical B2B products)
- Developing multi-channel campaign strategies
- Creating hub-and-spoke content clusters
- Coordinating content atomization workflows
- Building master content calendars
- Measuring campaign performance
- Managing concurrent product launches

**Does NOT activate during**:
- Creating individual content pieces (activates longform-technical-writing)
- Writing social media posts (activates social-media-content-strategy)
- General development work
- API design or code implementation
- Testing and debugging

**Validation**: If you're planning comprehensive campaigns, coordinating multi-channel launches, or measuring marketing performance, this activates. If you're creating specific content or doing development work, other skills activate or none activate.

---

## Part 0: Campaign Evidence Foundation (DO THIS FIRST)

### The Multi-Channel Amplification Problem

**Critical failure mode**: Fabricated metrics in hub content get amplified across 20+ derivative pieces, permanently damaging credibility across all channels.

**Example cascade**:
```
White paper (unsourced): "70-90% token reduction"
  ↓ Atomized to →
LinkedIn post: "70-90% token reduction"
Twitter thread: "70-90% token reduction"
Blog post: "70-90% token reduction"
Email campaign: "70-90% token reduction"
Product page: "70-90% token reduction"
Press release: "70-90% token reduction"
```

**One fabricated claim → Dozens of channels → Permanent reputation damage**

### Critical Principle: Evidence at the Hub

**Hub-and-spoke model requires evidence-first hub creation:**

1. **Verify ALL claims in hub content** (white paper, pillar post) BEFORE atomization
2. **Create evidence manifest** documenting every metric source
3. **Only atomize verified content** (fabrications amplify exponentially)
4. **Track evidence across derivatives** (maintain source consistency)

### Step 1: Pre-Campaign Evidence Audit

**Before planning ANY campaign, verify:**

**Product Claims**:
- [ ] Performance metrics: Sourced from benchmarks/logs (methodology documented)
- [ ] Usage statistics: Sourced from analytics (date range specified)
- [ ] Customer results: Permission granted, quotes verified
- [ ] Comparisons: Your own testing (not competitor claims)
- [ ] ROI calculations: Methodology transparent, assumptions stated

**Campaign Messaging**:
- [ ] Value props backed by evidence (not aspirational)
- [ ] Customer pain points documented (surveys, support tickets, interviews)
- [ ] Solution fit verified (case studies, pilot results)
- [ ] Differentiation claims testable (feature comparison documented)

**If ANY checkbox unchecked**: STOP campaign planning. Gather evidence FIRST.

### Step 2: Hub Content Evidence Manifest

**Before creating hub content (white paper, pillar blog post):**

Create comprehensive evidence manifest (see longform-technical-writing skill Part 0 for full template):

```markdown
## Campaign Evidence Manifest

### Core Value Proposition
**Claim**: [Your main value prop]
**Evidence**: [Source with location, date, methodology]
**Confidence**: [High/Medium/Low]
**Approved for**: [Which channels - all/some/qualified only]

### Key Metrics (for atomization)
**Metric 1**: "70-90% token reduction"
**Status**: NEEDS VERIFICATION or VERIFIED
**Source**: [Specific location, methodology]
**Usage rules**: [Can use in all channels / Requires qualification / Remove]

**Metric 2**: "183 bugs prevented"
**Status**: VERIFIED
**Source**: Git history analysis [repo, date range, command]
**Usage rules**: Can use in all channels with attribution

[... all campaign claims documented ...]
```

### Step 3: Atomization Verification Rules

**When creating derivative content from hub:**

**Tier 1 - Verified metrics** (use freely across channels):
- Documented in evidence manifest
- High confidence (direct measurement)
- Consistent attribution across derivatives

**Tier 2 - Qualified metrics** (use with caveats):
- Medium confidence (small sample, estimates)
- MUST include qualification in ALL derivatives
- "Early testing (N=3) suggests..." NOT "Proven results show..."

**Tier 3 - Unverified claims** (REMOVE from hub AND all derivatives):
- No source found
- Aspirational or theoretical
- Better to omit than fabricate

### Step 4: Cross-Channel Consistency Check

**Before campaign launch:**

- [ ] All channels use same verified metrics (no drift/embellishment)
- [ ] All sources cited consistently (white paper = Twitter = landing page)
- [ ] Qualified claims remain qualified across channels (don't drop caveats)
- [ ] No channel makes stronger claims than hub content
- [ ] Evidence manifest shared with all content creators

### Red Flags for Campaigns

**Amplification Risk** (CRITICAL):
- 🚨 Hub content with unsourced metrics (will amplify to 20+ pieces)
- 🚨 Different numbers across channels ("70%" in blog, "90%" on Twitter)
- 🚨 Qualified claim in hub, unqualified in social (drops limitations)
- 🚨 Press release with claims not in evidence manifest

**ACTION**: Audit ALL campaign content, remove unsourced claims, ensure consistency.

**Differentiation Claims** (VERIFY OR REMOVE):
- 🚩 "Faster than X" (did YOU test? when? methodology?)
- 🚩 "Only solution that..." (verified? competitors checked?)
- 🚩 "Industry-leading" (measured by whom? criteria?)

**ACTION**: Either run competitive analysis OR remove comparison.

### Campaign Launch Checklist

**STOP. Do not launch until ALL verified:**

- [ ] Evidence manifest created for all hub content
- [ ] Every quantitative claim sourced and documented
- [ ] Hub content (white paper/pillar post) verified FIRST
- [ ] Atomization rules defined (which metrics for which channels)
- [ ] All derivative content cross-checked against manifest
- [ ] No channel makes stronger claims than hub
- [ ] Qualified claims remain qualified across all channels
- [ ] Competitive claims based on YOUR testing (not assumptions)
- [ ] Customer quotes/case studies have written permission
- [ ] Legal/compliance review completed (if required)

**If ANY checkbox unchecked**: Delay launch, gather evidence, or remove claims.

### Example: Evidence-First Campaign Planning

**Scenario**: Launching AI coding framework

**WRONG approach** (evidence-last):
1. Write white paper with impressive metrics
2. Atomize to 20 pieces
3. Launch campaign
4. Get asked for sources → Cannot provide → Credibility damaged

**RIGHT approach** (evidence-first):
1. **Evidence audit**: What data do we have? (git logs, benchmarks, user surveys)
2. **Evidence manifest**: Document every claim with source
3. **Hub creation**: Write white paper using ONLY verified claims
4. **Atomization rules**: Define which metrics for which channels
5. **Derivative verification**: Cross-check all content against manifest
6. **Launch**: Every claim sourced, consistent across channels

---

## Part 1: Strategic Foundation

### Brand Positioning & Value Proposition

**Core principle**: Position around problems solved, not feature lists

**Positioning statement structure**:
- Technical product: "The fastest way to [achieve outcome]"
- Example: "The fastest way to debug production AI models"
- Example: "The most practical, code-first guide to production ML"

**Focus**: Outcomes (speed, flexibility, practicality) not features

### Defining Process

1. **Internal content workshops**:
   - Cross-functional: Sales, engineering, product, support
   - Identify unique angles, pain points, differentiators
   - Avoid marketing-only perspective

2. **Competitor content analysis**:
   - Goal: Find "white space" (uncovered topics, underserved perspectives)
   - Don't mimic competitors
   - Add unique, valuable voice

3. **Brand promise articulation**:
   - Single most essential message
   - Core value encapsulation
   - Memorable positioning

### Messaging Hierarchy Framework

**The Messaging Pyramid** (3 levels):

**Level 1 - Core Promise** (top rung):
- Single, overarching value proposition
- Concise, compelling, instant communication
- Placement: Hero section, ad headline, social bio
- Example: "Build, test, and deploy AI applications twice as fast"

**Level 2 - Supporting Pillars** (middle rung):
- 3-5 key benefits/differentiators
- Support and reinforce core promise
- Placement: Product page subheadings, presentation bullets, short videos
- Examples:
  - "Real-time debugging in production"
  - "Seamless CI/CD integration for ML models"
  - "Extensive library of pre-built models"

**Level 3 - Proof Points** (bottom rung):
- Specific features, specs, performance data
- Case studies, testimonials, evidence
- Placement: Blog body, whitepapers, technical docs
- Examples:
  - "Reduces model debugging time by 40%"
  - "Natively supports Python, C++, Java SDKs"
  - "Trusted by Company X and Company Y"

### Dynamic Message Prominence

**Audience awareness stages** (map hierarchy to stage):

**Problem-Aware** (recognizes challenge, unaware of solutions):
- Highlight: Level 2 (Supporting Pillars)
- Articulate clear benefits

**Solution-Aware** (actively comparing tools):
- Highlight: Level 3 (Proof Points)
- Provide technical benchmarks, integration guides, feature comparisons

**Product-Aware** (familiar with your product):
- Highlight: Level 1 (Core Promise) for reinforcement
- Plus Level 3 for decision support

---

## Part 2: B2B Funnel Mapping

### Three-Stage Funnel

**Top of Funnel (ToFu - Awareness)**:
- **Objective**: Attract broad but relevant audience
- **Focus**: Educational content, thought leadership, industry problems
- **Formats**: High-level blog posts, trend reports, infographics, podcasts, guest articles
- **Example (AI tool)**: "The 5 Biggest Challenges in MLOps for 2026"
- **Example (ML textbook)**: "The Evolution of Neural Network Architectures" (infographic)

**Middle of Funnel (MoFu - Consideration/Evaluation)**:
- **Objective**: Nurture interest with solution-oriented content
- **Focus**: Demonstrate expertise, show problem-solving capability
- **Formats**: Whitepapers, webinars, case studies, comparison guides, e-books, tutorials
- **Example (AI tool)**: "Practical Guide to Automating AI Model Deployment"
- **Example (ML textbook)**: Downloadable sample chapter on "Implementing Transformers from Scratch"

**Bottom of Funnel (BoFu - Decision)**:
- **Objective**: Build final trust, remove friction to adoption
- **Focus**: Enable user to start or purchase
- **Formats**: Product demos, free trials, API docs with code samples, implementation guides, testimonials, pricing
- **Example (AI tool)**: Interactive "Getting Started" tutorial with copy-paste code
- **Example (ML textbook)**: Public GitHub repo with all book code, one-click cloud run

---

## Part 3: Hub-and-Spoke Content Model

### Model Overview

**Structure**: Central "hub" (pillar page) + multiple "spokes" (cluster articles)
- Hub: Comprehensive coverage of broad topic (3,000-5,000+ words)
- Spokes: Detailed subtopic articles (each 1,500-3,000 words)
- Linking: Hub links to spokes, spokes link back to hub

### Benefits

**SEO Authority**:
- Interconnected structure signals expertise, authoritativeness, trustworthiness (E-E-A-T)
- Improved search rankings for hub AND entire cluster
- Internal linking passes authority between pages

**User Experience**:
- Logical, intuitive site architecture
- High-level overview (hub) → Deep dive (spokes)
- Reduces bounce rates, increases time on site

### Selecting Pillar Topics

**Criteria**:
- Broad enough: Support 8-22 spoke articles
- Specific enough: Directly relevant to product and value proposition
- High search volume: Target short-tail keyword
- Audience alignment: Core problems and interests

**Examples**:
- AI developer tool: "Machine Learning Operations (MLOps)"
- ML textbook: "Deep Learning Fundamentals"

### Pillar Page Elements

**Essential components**:

1. **Ungated access**: Freely accessible (no form fill)
   - Maximizes SEO value
   - Builds initial trust

2. **Comprehensive overview**: A-to-Z topic coverage
   - Define key terminology
   - Cover all major subtopics at high level
   - Answer top-level questions

3. **Scannable design**: Prioritize readability
   - Strong visual hierarchy (clear headings)
   - Short paragraphs (3-4 sentences max)
   - Generous white space
   - Visuals (diagrams, infographics)
   - Sticky table of contents

4. **Strategic interlinking**: Act as directory
   - Contextual links to spoke articles
   - Structural glue holding cluster together
   - Distributes SEO authority

5. **Contextual CTAs**: Middle-of-funnel calls to action
   - Example: Model monitoring section → Link to webinar on same topic
   - Example: After deep technical section → Link to case study

### Topic Cluster Mapping

**Process**:
1. **Keyword research** (Ahrefs, SEMrush):
   - Long-tail keywords
   - User questions ("People Also Ask")
   - Related search queries

2. **Identify spoke opportunities**:
   - Each keyword/question = potential spoke article
   - Address specific niche within broad subject

**Example cluster (MLOps pillar)**:
- **Hub**: "The Ultimate Guide to MLOps: From Development to Production"
- **Spokes**:
  - "What is CI/CD for Machine Learning?"
  - "Model Versioning and Experiment Tracking Deep Dive"
  - "How to Monitor ML Models in Production"
  - "Kubernetes for MLOps: A Beginner's Guide"
  - "Comparing MLOps Platforms: Open Source vs Managed"
  - "Strategies for Automating ML Model Retraining"
  - "Feature Store Architectures Explained"
  - "Best Practices for AI Observability and Model Drift Detection"

**Content generation engine**: Cluster mapping creates multi-month content calendar

---

## Part 4: Content Atomization Workflow

### Atomization vs Repurposing

**Repurposing**: Adapting content into new format (blog post → video script)

**Atomization**: Systematic deconstruction of one large asset into many smaller standalone "atomic units"
- More strategic than simple repurposing
- Atomic units can then be repurposed into various formats

### Benefits

- **Maximize reach**: Single content investment → Multi-channel distribution
- **Improve efficiency**: Reduce "start from scratch" content creation
- **Boost SEO**: Target wider array of niche keywords
- **Cater to diversity**: Different learning styles and platform preferences

### 5-Step Atomization Workflow

**Step 1: Start with high-impact core asset**:
- Substantial, information-dense content
- Best candidates: Pillar pages, in-depth spokes, whitepapers, webinar recordings, book chapters
- Comprehensive, data-rich, evergreen

**Step 2: Deconstruct into atomic units**:
- Key themes
- Compelling statistics
- Insightful expert quotes
- Useful code snippets
- Distinct procedural steps
- Each unit has value when separated from whole

**Step 3: Match atomic units to formats and channels**:
- Complex process → Infographic
- Powerful statistic → Tweet
- Code snippet → GitHub Gist
- Expert quote → Quote graphic
- Tutorial section → Video
- Creative brainstorming: Multiple formats per unit

**Step 4: Create and optimize each derived asset**:
- Adapt for specific platform
- Optimize: Character limits, image dimensions, hashtags, native tone
- Include CTA linking back to comprehensive core asset
- Create pathway for deeper engagement

**Step 5: Schedule and distribute via content calendar**:
- Plan rollout over days/weeks
- Create sustained "surround-sound" effect
- Keep topic top-of-mind
- Drive continuous traffic to pillar

### Atomization Matrix Example

**Core asset**: "A Deep Dive into Model Versioning" (spoke article)

| Atomic Unit | Derived Format | Channel | Headline/Hook | CTA |
|-------------|----------------|---------|---------------|-----|
| **Core concept definition** | Short video (60s) | YouTube Shorts, LinkedIn, TikTok | "What is ML Model Versioning in 60 seconds?" | "Watch our full webinar on MLOps best practices" |
| **Key statistic** | Static image/infographic | Twitter, LinkedIn | "Teams without proper model versioning are 3x more likely to experience production failures" | "Read our full State of MLOps report" |
| **Best practice checklist** | LinkedIn carousel | LinkedIn | "5 Best Practices for ML Model Versioning You Need to Implement Today" | "Get the full guide on our blog" |
| **Code snippet** | Gist/technical blog | GitHub, company blog | "Simple Python Snippet for Versioning TensorFlow Models with Git-LFS" | "Explore our open-source tool for advanced versioning" |
| **Expert quote** | Quote graphic | Twitter, LinkedIn | "'Without rigorous versioning, you're not doing data science; you're just doing data art.' - [Expert Name]" | "Learn more in our latest whitepaper" |
| **Section on "Git vs DVC"** | Standalone blog post | Company blog, Medium | "Model Versioning Tools: Why Git Alone Isn't Enough for Your ML Projects" | "Try our AI developer tool for free" |
| **Entire article audio** | Podcast segment | Company podcast | "This week: the critical importance of model versioning for reliable AI systems" | "Find all code and resources on our blog" |

**ROI**: 1 core asset (10-15 hours) → 20+ derivatives (5-8 hours) = 2.5-3x content output

---

## Part 5: Multi-Channel Distribution

### Tiered Channel Strategy

**Tier 1: Owned & Foundational** (center of gravity):

**Company blog/resource center**:
- Primary home for pillar pages and spoke articles
- Central SEO authority building
- Houses comprehensive content for atomization

**Technical documentation**:
- For developers: Documentation IS marketing
- Often first and most important touchpoint
- Primary trust driver
- Critical adoption factor

**Email newsletter**:
- Direct line to most engaged audience
- Distribute new content, product updates
- Educational nurture sequences

**Tier 2: Community & Code-Centric** (building credibility):

**GitHub**:
- Non-negotiable for open-source tools
- Well-maintained repo = marketing asset
- Excellent READMEs, clear contribution guidelines
- Active, responsive issue/PR management

**Stack Overflow**:
- Engage by helpfully answering questions
- Avoid direct promotion unless product is explicit solution
- Build reputation on expertise, not advertising

**Reddit**:
- Participate in relevant subreddits (r/MachineLearning, r/datascience, r/programming)
- Community-first mindset
- Provide value, share helpful content
- Transparent about branded content (educational merit focus)

**Hacker News**:
- High-risk, high-reward
- "Show HN" can drive massive qualified traffic
- Community critical of marketing-speak
- Requires genuine technical merit, authentic presentation

**Tier 3: Professional & Social** (amplification & reach):

**LinkedIn**:
- Primary B2B professional networking
- Thought leadership, case studies, webinar announcements
- Target engineering managers, team leads, CTOs

**Twitter/X**:
- Real-time pulse of tech community
- Quick insights, code snippets, industry influencer engagement
- Timely conversations and trends

**YouTube**:
- World's second-largest search engine
- Video tutorials, webinar recordings, conceptual explainers, product demos

### Educational vs Promotional Balance

**80/20 Rule**:
- 80% educational/informative/entertaining content
- 20% promotional content (framed around value)

**Blending techniques**:

**Contextual CTAs**: Highly relevant, not generic
- Tutorial on debugging ML models → CTA to try debugging tool
- Not: Generic "Request a Demo" buttons

**"Powered by" mentions**: Subtle attribution
- Create valuable open-source resource (dataset, CLI utility)
- Include mention: "Created and maintained by team behind [tool]"

**Case studies as problem-solving narratives**: Educational deep dives
- Frame customer success as technical problem-solving
- Product = enabling tool helping hero (customer) succeed
- Not: Product as hero itself

**Cross-promotion synergy**: Mutually reinforcing products
- Textbook examples → "Run this with our AI tool"
- Tool tutorials → "Learn foundations in our textbook"

---

## Part 6: Campaign Measurement

### Performance Dashboard Structure

**Four KPI categories** (map to campaign objectives):

1. **Awareness & consumption**: "Is content being seen by right audience?"
   - Reach and visibility metrics

2. **Engagement**: "Is content resonating and providing value?"
   - Interaction metrics

3. **Lead & conversion**: "Is content driving meaningful action?"
   - Next-stage movement metrics

4. **Business & revenue**: "Is content influencing bottom line?"
   - Direct business outcome metrics

### Developer-Centric KPIs

**Critical insight**: Traditional B2B KPIs (MQLs from whitepaper downloads) are poor indicators for developer marketing

**Technical conversions** (more significant than marketing actions):
- API key sign-up
- GitHub repo starring
- First successful API call
- SDK download
- "Time to First Hello, World" achievement

**Priority shift**: Track developer actions, not traditional marketing actions

### Developer Marketing KPI Dashboard

| Funnel Stage | Objective | Standard B2B KPIs | Developer-Specific KPIs (AI Tool) | Educational KPIs (ML Textbook) |
|--------------|-----------|-------------------|-----------------------------------|-------------------------------|
| **Awareness (ToFu)** | Increase visibility & reach | Organic traffic, impressions, search rankings, social reach | GitHub repo views/clones, Stack Overflow/Reddit impressions, technical blog referral traffic | Book landing page views, infographic social shares, podcast downloads |
| **Engagement (MoFu)** | Build trust & demonstrate value | Time on page, scroll depth, video watch time, social engagement | Documentation page views, time on docs, GitHub stars/forks, code sample downloads, webinar attendance | Chapter download rate, code notebook opens, tutorial page time |
| **Conversion (BoFu)** | Drive adoption & capture leads | Form conversion rate, MQLs, demo requests, cost per lead | **Free tier/OSS sign-ups**, API key generation, SDK downloads, first API call, sandbox usage | **Book sales**, email sign-ups for code updates, book code repo stars |
| **Advocacy & Retention** | Foster community & loyalty | Customer lifetime value, NPS, repeat visitors | Active users (DAU/MAU), community forum contributions, GitHub issues/PRs submitted, positive mentions | Positive reviews (Amazon, Goodreads), university course adoption, community mentions |

**Success metrics**: Technical engagement milestones, not marketing vanity metrics

---

## Part 7: Campaign Coordination

### Principles for Multiple Campaigns

**Centralization**: Unified master content calendar
- Single source of truth for all campaign activities
- Maps every content piece, social post, email, paid ad
- Provides visibility across campaigns
- Identifies and prevents conflicts (messaging, targeting, timing)

**Standardization**: Reusable templates
- Campaign briefs, content outlines, execution checklists
- Ensures consistency in quality and messaging
- Reduces repetitive work
- Focus on creative execution, not process reinvention

**Clear ownership**: Defined roles
- Each campaign and major deliverable has owner
- Establishes accountability
- Streamlines cross-functional collaboration
- Everyone understands responsibilities and deadlines

**Agile execution**: Data-driven optimization
- Flexibility in dynamic market
- Regular check-ins, real-time analytics monitoring
- Informed adjustments on the fly
- Reallocate budget to what works, pivot from underperforming tactics

### Example Campaign Structure

**Campaign A: Open-Source AI Developer Tool**:
- **Primary goal**: Drive adoption, foster active community
- **Primary audience**: Mid-level to senior MLOps engineers, data scientists, AI researchers
- **Pillar content**: "The Ultimate Guide to MLOps"
- **Key channels**: GitHub, Hacker News, guest posts, Reddit, Twitter, LinkedIn
- **Core BoFu conversion**: Tool download/installation, GitHub repo star, first project creation

**12-Week launch sequence**:
- **Weeks 1-4 (Pre-launch)**: 2-3 spoke articles, tease on social, beta tester engagement
- **Weeks 5-8 (Launch)**: Pillar page, "Show HN" post, coordinated social launch, targeted paid ads
- **Weeks 9-12 (Post-launch)**: YouTube tutorial, beta user case study, live webinar/Q&A, continued spoke publishing

**Campaign B: Machine Learning Textbook**:
- **Primary goal**: Drive book sales, establish author thought leadership
- **Primary audience**: Data science students, junior ML engineers, academics
- **Pillar content**: "Deep Learning Fundamentals"
- **Key channels**: Amazon, Goodreads, university outreach, Reddit, Medium, YouTube, author profiles
- **Core BoFu conversion**: Book purchase

**12-Week launch sequence**:
- **Weeks 1-4 (Pre-launch)**: Pillar page, free sample chapter, atomized sample content
- **Weeks 5-8 (Launch)**: Official announcement with purchase links, launch promotion, guest post, Reddit AMA
- **Weeks 9-12 (Post-launch)**: YouTube tutorial series, GitHub code repo release, solicit expert reviews

### Cross-Promotional Synergy

**Principle**: Make 1+1=3 (mutually reinforcing products)

**From textbook to tool**:
- Book code examples include "Run this with our AI tool"
- Book's GitHub repo has tool implementation branch
- Concluding chapter recommends tool for production application

**From tool to textbook**:
- Tool documentation includes "Learn fundamentals in our textbook"
- Tool tutorials reference textbook chapters
- Tool blog posts feature textbook code examples

**Coordinated timing**: Stagger launches to avoid audience fatigue, create momentum

---

## Part 8: Campaign Calendar Framework

### Master Calendar Components

**Content pieces** (all campaigns):
- Pillar pages (hub)
- Spoke articles
- Whitepapers
- Webinars
- Case studies
- Video content
- Atomized derivatives

**Social posts** (by platform):
- LinkedIn posts/carousels
- Twitter/X threads
- GitHub updates
- Reddit posts
- YouTube videos

**Email sends**:
- Newsletter editions
- Product announcements
- Nurture sequences
- Webinar invitations

**Paid advertising** (if applicable):
- LinkedIn ads
- Twitter/X promoted posts
- Google search ads
- Retargeting campaigns

### Scheduling Strategy

**Pre-launch phase** (4 weeks):
- Build SEO foundation (spoke articles)
- Tease on social (behind-the-scenes content)
- Engage beta testers/early users
- Build anticipation

**Launch phase** (4 weeks):
- Pillar page publication
- Major announcement (Show HN, social coordination)
- Paid advertising surge
- High-volume atomized content

**Post-launch phase** (4+ weeks):
- Sustained content cadence (spokes, derivatives)
- Case studies and testimonials
- Community engagement (webinars, AMAs)
- Long-tail SEO building

**Ongoing maintenance**:
- Regular spoke article publication
- Continuous atomization of core assets
- Community participation
- Performance monitoring and optimization

---

## Part 9: Decision Frameworks

### When to Launch Multiple Products

**Simultaneous launch** (complex coordination):
- ✅ Products complement each other (tool + textbook)
- ✅ Shared target audience overlap
- ✅ Cross-promotional opportunities exist
- ✅ Team capacity sufficient
- ⚠️ Requires master calendar and clear ownership

**Staggered launch** (reduced risk):
- ✅ Different target audiences
- ✅ Limited team capacity
- ✅ Learning from first launch informs second
- ✅ Avoid audience fatigue

### When to Create Hub-and-Spoke Cluster

**Ideal scenarios**:
- ✅ Topic broad enough (8-22 spokes)
- ✅ Directly relevant to product/value prop
- ✅ High search volume (short-tail keyword)
- ✅ Evergreen content (long-term value)
- ✅ Sufficient content creation capacity

**Not ideal**:
- ❌ Topic too narrow (<8 spokes)
- ❌ Tangential to product value
- ❌ Low search volume
- ❌ Rapidly changing topic (frequent updates needed)

### When to Atomize Content

**High-value atomization candidates**:
- ✅ Comprehensive, data-rich core asset (3,000+ words)
- ✅ Multiple distinct concepts/sections
- ✅ Evergreen content (long shelf life)
- ✅ Multi-channel campaign planned
- ✅ 10+ derivative assets possible

**Low-value atomization**:
- ❌ Short-form content (<1,500 words)
- ❌ Single-concept content
- ❌ Time-sensitive/dated content
- ❌ Single-channel distribution
- ❌ <5 derivative assets possible

---

## Success Metrics Summary

### Campaign-Level Success

**Awareness success**:
- Organic traffic growth (month-over-month)
- Search ranking improvements (target keywords)
- Social reach and impressions
- Brand mention volume

**Engagement success**:
- Time on page (3-5 min pillar, 2-4 min spokes)
- Scroll depth (70%+ reaching conclusion)
- Video watch time (50%+ completion)
- Documentation page views (for tools)

**Conversion success**:
- Developer-specific actions (API keys, GitHub stars, first API calls)
- Email list growth (3-5% conversion rate)
- Free trial/OSS sign-ups
- Book sales or product purchases

**Business success**:
- Customer acquisition cost (CAC)
- Customer lifetime value (CLV)
- Revenue attribution (content-assisted)
- Community growth (active users, contributors)

### Content Performance

**Pillar page success**:
- Ranks top 3 for target keyword
- Drives 500-2,000 views/month
- 5-10 min average time on page
- 50-100 backlinks (year 1)

**Spoke article success**:
- Ranks top 10 for long-tail keywords
- Drives 100-500 views/month
- 3-5 min average time on page
- Links back to pillar (internal SEO juice)

**Atomized content success**:
- High engagement rate (likes, shares, comments)
- Drives traffic back to core asset
- Multi-platform reach (same content, multiple channels)
- Sustained "surround-sound" effect

---

## Progressive Disclosure Benefit

**Token efficiency**: This skill's 7KB content loaded only when planning multi-channel campaigns or coordinating product launches (10-15% of time) vs embedding in every /plan or /execute command (100% overhead).

**Impact**: 85-90% token reduction through occasional activation.

**When active**: Provides comprehensive campaign strategy, hub-and-spoke model, atomization workflows, multi-channel coordination, and measurement frameworks exactly when planning campaigns.

**When dormant**: Only 150-byte metadata consumes context, not full 7KB framework.

**Complementary skills**:
- Use with longform-technical-writing when creating pillar pages/spokes
- Use with social-media-content-strategy when distributing atomized content
- This skill = strategic orchestration; others = tactical execution
