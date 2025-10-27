# Social Media Content Strategy

**Skill Type**: Content Marketing
**Domain**: Social Media Strategy for Technical B2B Audiences
**Activation Rate**: 15-20% (occasional - only during social media planning)

---

## Discovery Metadata

```yaml
id: social-media-content-strategy
version: 2.0.0
description: |
  Evidence-first platform-specific social media content strategies for LinkedIn and
  Twitter/X targeting technical B2B audiences (developers, AI practitioners, technology
  decision-makers). CRITICAL: Enforces rigorous sourcing - metrics and claims must be
  verified before posting. Prevents fabricated engagement statistics and unsourced
  performance claims. Includes evidence verification (FIRST), 2025 algorithmic priorities,
  content structure frameworks (H-B-C-Q for LinkedIn, H-M-S-C for Twitter), engagement
  tactics, posting schedules, and content adaptation patterns. Activates when planning
  social media campaigns, creating LinkedIn posts, designing Twitter/X threads, discussing
  platform-specific strategies, or adapting content for multiple platforms. Use when
  developing social content calendars, writing technical posts for LinkedIn, crafting
  viral threads for X, or repurposing longform content for social channels.

keywords:
  - social media
  - LinkedIn post
  - Twitter thread
  - X thread
  - social campaign
  - content calendar
  - platform strategy
  - engagement tactics
  - viral thread
  - carousel post
  - document post
  - thread hook
  - social content

triggers:
  - "LinkedIn post"
  - "Twitter thread"
  - "X thread"
  - "social media strategy"
  - "social campaign"
  - "content calendar"
  - "viral thread"
  - "platform-specific content"
  - "multi-channel distribution"
```

---

## When This Activates

**Situational triggers** (15-20% of conversations):
- Planning social media content campaigns
- Creating LinkedIn posts for technical audiences
- Designing Twitter/X threads
- Discussing platform-specific content strategies
- Adapting long-form content for social platforms
- Reviewing social media engagement metrics
- Developing content calendars

**Does NOT activate during**:
- General software development work
- Writing documentation
- Code reviews
- API design
- Testing and debugging

**Validation**: If you're creating social content or planning social campaigns, this activates. If you're coding or doing technical work unrelated to content marketing, this stays dormant.

---

## Part 0: Evidence Verification for Social Claims (DO THIS FIRST)

### The Social Media Fabrication Problem

**Historical failure mode**: Agents write impressive-sounding metrics and claims for social posts without sources.

**Example of what NOT to do**:
```markdown
❌ "70-90% token reduction with our tool"
❌ "Used by 10,000+ developers worldwide"
❌ "3-10x productivity improvement"
❌ "183 bugs prevented (180:1 ROI)"
```

**If you cannot source these claims, DO NOT post them.**

### Critical Principle: Verify Before You Post

Social media amplifies both truth and falsehood. A fabricated claim in a viral thread damages credibility permanently.

### Step 1: Identify Claims in Planned Content

Before drafting social posts, list all claims you plan to make:

**Claims That Need Sources**:
- Performance metrics ("91% faster", "3x improvement")
- Usage statistics ("10,000 users", "500 companies")
- ROI/impact ("180:1 ROI", "saves 5 hours/week")
- Comparisons ("faster than X", "better than Y")
- Customer results (any specific outcomes)
- Growth/adoption ("50% month-over-month growth")

### Step 2: Verify EVERY Claim

**Tier 1 - Acceptable for Social**:
- ✅ Your own data: Analytics, logs, git history, benchmarks
- ✅ Published sources: Research papers, third-party reports (link to them)
- ✅ Customer quotes: Permission granted, attributed

**Tier 2 - Use With Qualification**:
- ⚠️ Small samples: "3 early users reported..." (state N, don't generalize)
- ⚠️ Estimates: "Estimated..." or "Projected..." (show methodology)

**Tier 3 - NEVER Use on Social**:
- ❌ Aspirational: "Up to 10x", "As much as..."
- ❌ Vague: "Significant improvement", "Much better"
- ❌ Fabricated: Made-up numbers
- ❌ Unsourced: "Fastest solution" (says who?)

### Step 3: Quick Evidence Checklist

**Before posting ANY social content:**

- [ ] Every number has a source (analytics, logs, research)
- [ ] Every comparison has baseline + methodology
- [ ] Every customer claim has permission
- [ ] No aspirational language without qualification
- [ ] No vague superlatives ("best", "fastest", "most")

**If ANY checkbox unchecked**: Remove claim or gather evidence.

### Red Flags for Social Media

**Fabricated Engagement Metrics** (CRITICAL):
- 🚨 "Viral on Twitter" (define: how many impressions? engagement rate?)
- 🚨 "10,000 users" (source: analytics with date?)
- 🚨 "Trending in tech community" (measured how?)
- 🚨 "Industry-leading results" (compared to whom? by whom?)

**Unsourced Product Claims** (DAMAGES CREDIBILITY):
- 🚩 "70-90% improvement" (measured when? how? in what?)
- 🚩 "Saves hours per day" (based on what data?)
- 🚩 "Trusted by enterprises" (which ones? with permission to say?)
- 🚩 "ROI of 180:1" (calculated how? over what period?)

**ACTION**: Either source the claim with evidence OR remove it.

### What Makes Social Different

**Permanent amplification**: Unlike drafts, social posts spread and persist
**Screenshot culture**: Your claims will be scrutinized and shared
**Reputation stakes**: Technical audiences fact-check aggressively
**Viral risk**: Fabrications exposed publicly damage brand permanently

**Therefore**: Higher standard than internal docs. If uncertain, omit.

### Example: Handling Claims in Social Content

**Scenario**: Planning LinkedIn post about productivity tool

**WRONG approach**:
```markdown
"Our tool delivers 3-10x productivity improvements, with 70-90% token
reduction and 183 bugs prevented. Join 10,000+ developers already benefiting."
```
(All unsourced - unverifiable - damages credibility if questioned)

**RIGHT approach** (with source verification):

**Option A** (If evidence exists):
```markdown
"In 6 months production use across 3 projects (ML research, quant trading,
web dev), we've prevented 183 bugs through automated quality gates (git log
analysis, verified [date]). Early results from 3 users suggest 3-10x productivity
improvements, though sample size is limited and results vary by domain."
```
(Every claim sourced, limitations acknowledged)

**Option B** (If evidence doesn't exist):
```markdown
"Production-ready patterns for building AI coding agents. Stateless execution
eliminates state corruption. File-based persistence removes infrastructure overhead.
MCP integration provides optional enhancements."
```
(Describes features/mechanisms, no unsourced metrics)

---

## Content Strategy Framework

### Platform Dichotomy (2025)

**LinkedIn** = "Digital Library" for durable authority
- Goal: Build foundational credibility, generate high-quality leads
- Mindset: Professional development, deep learning, career networking
- Optimal format: Document/Carousel posts (1.45x reach), long-form text (1,200-1,900 chars)
- Lifespan: 24-72 hours with long tail
- Key metric: Dwell time, meaningful comments (15+ words = 2x value), saves (5x > likes)

**Twitter/X** = "Real-Time Laboratory" for rapid dialogue
- Goal: Drive conversation, build community, amplify brand voice
- Mindset: News consumption, trend discovery, peer-to-peer dialogue
- Optimal format: Threads (5-10 tweets), short video, image posts
- Lifespan: 15-45 minutes (with viral spike potential)
- Key metric: Engagement velocity, replies, quote tweets, retweets
- **Critical**: X Premium subscription = 10x median reach (mandatory for meaningful visibility)

---

## LinkedIn Strategy

### Algorithm Priorities (2025)

**Four-stage distribution**:
1. **Quality check (0-60 min)**: AI flags spam (>5 hashtags, <24h between posts, engagement bait, links in body)
2. **Golden window (0-2 hours)**: Shown to 1st-degree connections, early engagement determines wider distribution
3. **Audience matching (8+ hours)**: Expanded to 2nd/3rd connections based on relevance and relationship strength
4. **Final push (24+ hours)**: High performers continue distribution via hashtags and recommendations

**Prioritized signals**:
- **Dwell time** (most critical): How long users stay on post
- **Meaningful engagement**: Comments (2x > likes), long comments (15+ words), saves (5x > likes), reposts with thoughts
- **Golden hour effect**: Engagement in first 60-120 minutes triggers wider distribution
- **Niche authority**: Consistent topic focus rewards targeted reach

### Post Structure: H-B-C-Q Framework

**Hook (First 210 chars)** - Visible before "...see more":
- Create curiosity gap: "I spent three days debugging a race condition that turned out to be a single misplaced await"
- Counterintuitive claim: "Most developers are using Kubernetes wrong. Here's why."
- Promise valuable lesson: "I failed my first system design interview. Here are the 3 mistakes I made so you don't have to."

**Body (800-1,500 chars)** - Sweet spot for mobile readability:
- Short paragraphs (1-3 sentences max)
- Generous white space between paragraphs
- Scannable structure guides eye down page
- Technical depth with clarity

**Conclusion/Takeaway** - Reinforce value:
- Clear, concise summary of main point
- Memorable core message

**Question** - Elicit substantive comments:
- Specific, open-ended (not "What do you think?")
- Invites expertise sharing: "What's the most counterintuitive performance optimization you've ever implemented?"

**Length**: 1,200-1,900 characters total (algorithm's sweet spot for value assessment)

### Formatting for Technical Content

**Lists & Bullet Points**:
- Use symbols: ● (solid circle), → (arrow), ✅ (checkmark)
- Copy/paste required (no native bullet function)

**Code Snippets**:
- **Option 1**: Monospace text generators (Unicode converters) for single-line snippets
- **Option 2**: Screenshot images (Carbon, Pika) with syntax highlighting for multi-line blocks
- Never paste raw code (unreadable)

**Emojis**:
- Use sparingly, professionally
- End of sentences for visual breaks, not bullet replacements
- Overuse appears unprofessional and harms accessibility (screen readers announce each)

**Accessibility**:
- PascalCase hashtags: #MachineLearning (not #machinelearning) for screen readers
- Alt text on all images
- Avoid fancy font generators (screen readers can't parse)

### Content Types That Perform

1. **Lessons Learned / Failure Stories**:
   - Structure: Problem → Failed attempts → Realization → Actionable lesson
   - Builds authenticity and trust

2. **Technical Deep Dives / How-To**:
   - Best as carousel (document) format
   - Complex topics broken into digestible steps
   - CI/CD pipelines, architecture patterns, framework tutorials

3. **Personal Narrative + Technical Insight**:
   - Emotional context (why) + Technical details (what)
   - Start with high-stakes story, deliver technical insight
   - Example: Production outage → Performance optimization discovery

4. **Data & Benchmarks**:
   - Quantitative support for claims
   - Original data or synthesized industry reports
   - Performance comparisons, research findings

### Storytelling Framework: P-A-R-I

**Problem**: Specific, relatable technical challenge (concrete, not vague)
- Bad: "We had scaling issues"
- Good: "Database response times exceeded 500ms under peak load, causing cascading failures"

**Action**: Journey to solution (include failures and dead ends)
- Show what didn't work (often as valuable as what did)

**Result**: Quantifiable outcome (before/after metrics)
- "Reduced P95 latency to <50ms, eliminated cascading failures"

**Insight**: Generalizable principle others can apply
- "Key insight: Initial focus on application-level caching was premature optimization; real bottleneck was database query level"

### Visuals: Carousels Are King

**Content format performance** (2025 data):

| Format | Personal Profile Reach | Company Page Reach | Use Case |
|--------|----------------------|-------------------|----------|
| **Carousel (Document)** | 1.45x | 1.40x | Tutorials, deep dives, repurposed content |
| **Polls** | 1.64x | 1.19x | Quick feedback (can appear spammy if overused) |
| **Image (1-5)** | 1.18x | 1.21x | Diagrams, charts, behind-the-scenes |
| **Video** | 1.10x | 1.05x | Quick explainers, personal brand (60-90s, vertical, captions) |
| **Text-Only** | 0.88x | 0.42x | Lowest performer (needs exceptional hook) |

**Carousel best practices**:
- 6-12 slides optimal
- <50 words per slide
- First slide = compelling title/hook
- Final slide = clear CTA
- Unparalleled for code snippets as images

### External Links Strategy

**The cardinal rule**: NEVER put external links in post body
- Penalty: Up to 90% reach reduction
- Algorithm interprets as off-platform driver

**Workaround methods**:
1. **Link in first comment**: Post without links → Immediately comment with link → Edit post to say "Link in comments"
2. **Delayed edit**: Post without link → Wait 1 hour for traction → Edit to add link (riskier)

### Hashtag Strategy

**Optimal number**: 3-5 hashtags
- <3 limits discoverability
- >5 triggers spam filter

**Placement**: End of post (improves readability)

**Strategic mix**:
- 1-2 broad (#AI, #SoftwareEngineering) for max reach
- 2-3 niche (#AgentFrameworks, #RustLang, #ClaudeCode) for targeted audience

### Top 10 Mistakes to Avoid

1. External links in post body (kills reach)
2. Walls of text (unreadable on mobile)
3. Hashtag stuffing (>5-6 = spam)
4. Boring hook ("Excited to announce..." fails)
5. Generic CTAs ("Thoughts?" invites low-effort responses)
6. Posting and ghosting (no replies in first hours kills momentum)
7. Engagement bait ("Like if you agree!" = penalized)
8. Overly promotional (5:1 value-to-promotion ratio)
9. Inconsistent posting (2-3 quality posts/week optimal)
10. Ignoring mobile (90% engagement is mobile, format accordingly)

---

## Twitter/X Strategy

### Algorithm Priorities (2025)

**Core ranking signals**:
- **Engagement velocity**: Rapid engagement (likes, replies, reposts) in first hours
- **Relevance**: Matched to user interest profiles and past interactions
- **Rich media**: Images/videos = 2x more likely to be shown
- **Recency**: Real-time platform, visibility decays after 6-12 hours

**X Premium multiplier** (critical for 2025):
- Premium accounts: 10x median reach vs non-subscribed
- Premium+: 2x reach of standard Premium
- Reply prioritization: Premium replies boosted in conversations
- Monetization access: Requires Premium + 500 followers + 5M impressions/3mo
- **Strategic implication**: Treat X as paid distribution platform, subscription = cost of entry

### Thread Structure: H-M-S-C Framework

**Hook (Tweet 1)** - Solely responsible for "Show this thread" clicks:
- Bold promise, strong curiosity gap, or controversial/counterintuitive take
- Signal it's a thread: "A thread 🧵"
- Example: "99% of developers are using environment variables insecurely. I audited 100+ production apps and found the same critical mistake. Here's how to fix it in 5 minutes: A thread 🧵"

**Main Points (Tweets 2-N)** - Optimal length 5-10 tweets:
- One distinct idea per tweet
- Each tweet stands alone (understandable + valuable if retweeted solo)
- Connect logically to surrounding tweets

**Summary (Penultimate Tweet)** - TL;DR:
- Concise recap of main takeaways
- Reinforces value, provides shareable summary
- Improves retention

**CTA (Final Tweet)** - Clear, specific action:
- Ask question to spark replies: "What's one VS Code extension you can't live without?"
- Encourage follow: "Follow me for more on Python and performance engineering"
- Drive action: "If this helped, give the repo a star on GitHub ⭐ [link]"

### Thread Hook Formulas (20+ Proven Templates)

**Problem-Solving & How-To**:
1. "Struggling with [common dev problem]? Here's the step-by-step guide to fixing it."
2. "How to [achieve goal] without [pain point]." (e.g., "scalable API without boilerplate")
3. "I spent [number] hours debugging [issue]. Here's the simple fix so you don't have to."
4. "The definitive guide to [complex topic]. A thread 🧵"
5. "Stop wasting time on [ineffective method]. Do this instead."

**Counterintuitive & Controversial**:
6. "Unpopular opinion: [Best practice] is actually an anti-pattern. Here's why."
7. "Everything you know about [technology] is wrong."
8. "Why 90% of [developer type] fail at [task]."
9. "You've been lied to about [myth]. Let me explain."
10. "The harsh reality about [framework/tool]: [bold statement]."

**Listicle & Curation**:
11. "[Number] tools that saved me [number] hours of development time last week."
12. "[Number] underrated [language] libraries you should be using."
13. "I've reviewed [number] [product category]. Here are the top 3 and when to use each."
14. "The [number] mistakes to avoid when building your first [application type]."
15. "10 simple ways to improve your [skill] starting today."

**Storytelling & Credibility**:
16. "I went from [humble beginning] to [achievement] in [timeframe]. It wasn't luck. It was a system. Here it is:"
17. "Last year, I made a [mistake] that took down production. Here's the biggest lesson I learned."
18. "After [number] years as a [job title], these are my top [number] takeaways on [topic]."
19. "I analyzed [large number] of [data source]. They all have these [number] things in common."
20. "How I grew my open-source project from 0 to [number] stars in [timeframe]."

### Visual Elements

**Code screenshots**:
- Use Pika or Carbon for syntax-highlighted, formatted images
- Never post raw text code
- Font size large enough for mobile (no zoom needed)

**Diagrams & charts**:
- System architecture, data flows, performance benchmarks
- Tools: Excalidraw, Figma
- Break up text-heavy threads, clarify complex concepts

**GIFs & memes**:
- Use with cultural awareness and moderation
- Relevant programming memes add personality
- Avoid in serious technical deep-dives (detracts from credibility)

### Link Placement

**Primary link**: Final CTA tweet (most important external link)
- GitHub repo, blog post, product landing page

**Supplemental links**: Reply to main thread after publication

**Penalty note**: Less severe than LinkedIn for Premium users, but still exists

### Engagement Mechanics

**Quote Tweets vs. Replies**:
- For **conversation/community**: Ask question, prompt **replies**
  - "What's your favorite open-source alternative? Let me know in the replies."
- For **amplification/reach**: Ask takeaway, prompt **Quote Tweets**
  - "QT this thread with the one tip that surprised you most."

**Posting cadence**: All at once (atomic unit)
- Use native thread composer, TweetDeck, or Buffer
- Don't stagger over time (disrupts UX, breaks narrative, harms algorithm)

### Top 10 Thread-Killing Mistakes

1. Weak hook (generic/boring first tweet)
2. Lack of clear focus (rambling without central point)
3. Tweets don't stand alone (just connectors like "And then...")
4. Wall of text (no line breaks, emojis, visuals)
5. Excessive length (>10-12 tweets = significant drop-off)
6. Burying the lede (most valuable info too deep)
7. Inconsistent formatting (jarring style changes)
8. Ignoring engagement (no replies kills conversation)
9. Overly promotional (sales pitch from start)
10. Hashtag overuse (1-2 relevant hashtags max, otherwise spammy)

---

## Cross-Platform Content Adaptation

### The Repurpose Framework

**Core principle**: Repurpose, Don't Re-post
- Cross-posting identical content is inefficient
- Ignores platform consumption differences
- Start with pillar content (blog post, white paper, README)
- Derive platform-specific adaptations

**Content Adaptation Map**:

| Pillar Element | LinkedIn Adaptation | Twitter/X Adaptation |
|---------------|-------------------|-------------------|
| **Main thesis** | Long-form text post (1,200+ chars) with personal story, structured paragraphs, thoughtful question | Hook for thread (bold, concise statement in first tweet) |
| **Key data point** | Single-image post with visualized statistic, context in text | Single punchy tweet with stat + visual + debate question |
| **Step-by-step process** | Carousel (6-10 slides, each = 1 step, heading + explanation + visual) | Numbered thread (each tweet = 1 step, code as images) |
| **Single lesson/mistake** | Story-driven text using P-A-R-I framework | 3-5 tweet story using MRS (Mistake → Realization → Shift) |
| **Tools/resources list** | Listicle text with bullet points (●, ➤), brief descriptions | Curation thread (1 tool per tweet, tag official accounts) |

**Efficiency gain**: 1 piece of pillar content → Full week of platform-native social content

---

## Universal Principles (Both Platforms)

1. **Value over promotion**: Technical audiences hate marketing fluff (80/20 value-to-promotion)
2. **Authenticity**: Share failures and lessons learned (builds trust)
3. **Specificity**: Concrete details (metrics, technologies) > buzzwords
4. **Link strategy**: Never in main body (algorithm suppression on both platforms)
5. **Mobile-first**: 90%+ engagement is mobile (format accordingly)
6. **Engagement reciprocity**: Reply to comments/engage with community (signals active value)
7. **Consistency**: Regular cadence (LinkedIn: 2-3/week, X: 3-5/week)
8. **Data-driven**: Quantify impact (benchmarks, metrics, research findings)

---

## Decision Framework: When to Use Which Platform

**Use LinkedIn when**:
- Building long-term authority and credibility
- Targeting decision-makers and career professionals
- Sharing in-depth tutorials and educational content
- Showcasing expertise through detailed case studies
- Generating high-quality B2B leads

**Use Twitter/X when**:
- Participating in real-time technical conversations
- Building community and peer relationships
- Sharing breaking news or timely insights
- Testing ideas quickly and getting rapid feedback
- Amplifying content with viral potential

**Use both when**:
- Launching product/project (adapt single announcement)
- Repurposing comprehensive content (blog → carousel + thread)
- Building personal brand across developer ecosystem
- Maximizing reach for important insights

---

## Content Calendar Framework

**Weekly cadence example**:
- **Monday**: LinkedIn deep dive (carousel or long-form post)
- **Tuesday**: X thread (how-to or lessons learned)
- **Wednesday**: LinkedIn text post (personal narrative + insight)
- **Thursday**: X curation thread (tools/resources)
- **Friday**: LinkedIn data/benchmark post + X summary thread

**Pillar content strategy**:
1. Create 1 comprehensive piece weekly (blog post, white paper, video)
2. Atomize into 5-10 platform-specific social posts
3. Schedule throughout week for consistent presence
4. Engage with community comments/replies daily
5. Track metrics: saves/comments (LinkedIn), QTs/replies (X)

---

## Anti-Patterns to Avoid

❌ **Cross-posting identical content** (ignores platform differences)
❌ **Link-first strategy** (algorithmic suppression on both platforms)
❌ **Inconsistent voice** (switching between casual and corporate)
❌ **Ignoring engagement** (posting without replying kills momentum)
❌ **Buzzword overload** ("revolutionary," "game-changing" = ignored by developers)
❌ **Feature lists without context** (no problem/solution framing)
❌ **Generic advice** ("use best practices" = no value)
❌ **Pure self-promotion** (no educational value = no engagement)
❌ **Hashtag stuffing** (>5 LinkedIn, >2 X = spam filter)
❌ **Posting without strategy** (random timing, inconsistent cadence)

---

## Success Metrics

**LinkedIn** (measure depth and authority):
- Dwell time proxy: Long comments (15+ words)
- Saves (5x more valuable than likes)
- Meaningful comments and replies
- Connection requests from target audience
- Inbound leads referencing specific posts

**Twitter/X** (measure velocity and reach):
- Engagement velocity (first 2 hours)
- Quote tweets with added value
- Genuine replies (not just reactions)
- Profile visits and follows
- Click-through to external content

**Both platforms**:
- Follower growth rate in target audience
- Engagement rate (interactions / impressions)
- Content atomization efficiency (1 pillar → N social posts)
- Time to create (should decrease with templates/frameworks)
- Conversion to desired action (website visit, repo star, demo request)

---

## Progressive Disclosure Benefit

**Token efficiency**: This skill's 8.5KB content loaded only when planning social campaigns (15-20% of time) vs embedding in every /plan or /write command (100% overhead).

**Impact**: 75-80% token reduction through occasional activation.

**When active**: Provides comprehensive platform-specific strategies exactly when creating social content.

**When dormant**: Only 150-byte metadata consumes context, not full 8.5KB knowledge base.
