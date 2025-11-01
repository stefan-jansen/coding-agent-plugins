---
description: Generate complete service page copy including hero, benefits, process, and CTA sections. Creates comprehensive, SEO-optimized service descriptions.
---

# website-service

Generate complete service page copy with multiple sections optimized for conversion.

## Usage

```bash
# Generate full service page
/website-service "AI Strategy Consulting"

# Generate with positioning context
/website-service --positioning @positioning-doc.md "ML Implementation Services"

# Generate with custom sections
/website-service --sections "hero,benefits,approach,case-study,cta" "AI Transformation"
```

## Process

This command creates a complete service page with:

1. **Hero Section** (50-75 words)
   - Value proposition
   - Target audience signal
   - Primary CTA

2. **Benefits Section** (100-150 words)
   - 3-5 key benefits
   - Business outcomes focus
   - Scannable bullet points

3. **Process/Approach** (150-200 words)
   - 3-5 step methodology
   - Clear, jargon-free language
   - Confidence-building

4. **Social Proof** (Optional, 75-100 words)
   - Client results (if available)
   - Industry examples
   - Credibility signals

5. **CTA Section** (50-75 words)
   - Clear next step
   - Low-friction offer
   - Contact information

## Output Structure

Service pages save to: `website/services/[service-name]/`

```
website/
  └── services/
      ├── ai-strategy/
      │   ├── full-page.md       # Complete service page
      │   ├── hero.md            # Hero section only
      │   ├── benefits.md        # Benefits section only
      │   └── metadata.json      # SEO and analytics data
      ├── ml-implementation/
      └── data-engineering/
```

## Example Output

```markdown
# AI Strategy Consulting: Turn AI Potential into Business Reality

Many enterprises struggle to translate AI hype into practical ROI. We help you
cut through the noise, identify high-value opportunities, and build roadmaps
that deliver results in 3-6 months.

**Book a free AI readiness assessment** [CTA Button]

---

## Why AI Strategy Matters

- **Stop Wasting Budget** - Focus on AI projects with clear ROI paths
- **Accelerate Time-to-Value** - Launch pilots in weeks, not quarters
- **Build Competitive Moats** - Deploy AI where it creates lasting advantage
- **Scale with Confidence** - Infrastructure and teams that grow with demand

Most AI initiatives fail due to misaligned expectations and poor scoping. Our
strategy process ensures you invest in AI that actually moves your business
forward.

---

## Our Proven Approach

**1. AI Readiness Assessment** (1-2 weeks)
Evaluate your data, infrastructure, and organizational readiness for AI.

**2. Opportunity Mapping** (2-3 weeks)
Identify and prioritize AI use cases by business impact and feasibility.

**3. Roadmap Development** (2-3 weeks)
Create phased implementation plan with clear milestones and success metrics.

**4. Pilot Scoping** (1-2 weeks)
Define MVP scope, timeline, and resources for first high-value pilot.

---

## Ready to Build Your AI Strategy?

Schedule a free 30-minute discovery call to discuss your AI goals and challenges.
No sales pitch - just an honest conversation about whether AI can help your business.

[Book Discovery Call] [Download AI Strategy Guide]

---
Keywords: AI strategy consulting, enterprise AI consulting, AI roadmap
Search Intent: Commercial - Researching AI consulting services
Target Audience: VP/Director level at mid-market to enterprise companies
Word Count: 487 words
```

## Integration with Positioning

Service pages should align with positioning:

```bash
# 1. Define service positioning
/position "AI Strategy Consulting - helping enterprises..."

# 2. Research service demand
/research "AI strategy consulting, buyer pain points, competitive services"

# 3. Generate service page
/website-service "AI Strategy Consulting"

# 4. Review and refine
/review website/services/ai-strategy/full-page.md
```

## SEO Optimization

Service pages are optimized for:
- **Target Keywords** - Service name + intent modifiers
- **Long-tail Queries** - "How to...", "Best...", "[Service] for [Industry]"
- **Local SEO** - Location modifiers if applicable
- **Semantic Keywords** - Related terms and synonyms
- **Internal Linking** - Related services and resources

## Options

- `--positioning FILE` - Use specific positioning document
- `--research FILE` - Reference specific research
- `--sections LIST` - Specify sections (hero,benefits,process,proof,cta)
- `--keywords "kw1, kw2"` - Target specific keywords
- `--tone TONE` - Professional, technical, friendly, executive
- `--industry INDUSTRY` - Tailor examples to specific industry

## Section-Only Generation

Generate individual sections:

```bash
# Hero section only
/website-service --sections hero "AI Strategy"

# Benefits + Process only
/website-service --sections "benefits,process" "ML Implementation"
```

## Best Practices

### Service Page Copy Principles

1. **Lead with Outcomes** - What results can they expect?
2. **Address Skepticism** - Why should they believe you?
3. **Make Process Clear** - Remove uncertainty about what happens
4. **Reduce Friction** - Low-commitment first step
5. **Build Trust** - Credentials, social proof, guarantees

### Word Count Guidelines

- **Hero**: 50-75 words (stay concise)
- **Benefits**: 100-150 words (3-5 bullet points)
- **Process**: 150-200 words (4-5 steps)
- **Social Proof**: 75-100 words (2-3 examples)
- **CTA**: 50-75 words (clear, specific)

**Total**: 425-600 words per service page

### Common Mistakes to Avoid

- ❌ Starting with "We are..." (lead with value)
- ❌ Jargon-heavy descriptions (be clear)
- ❌ Vague benefits (be specific)
- ❌ Missing CTAs (always include next step)
- ❌ Too long (respect scanning behavior)

## Related Commands

- `/website-landing` - Generate landing page copy
- `/position` - Define service positioning
- `/research` - Research service demand
- `/review` - Review and refine

## Export to Website

Service page copy can be:
1. **Manually copied** to Wagtail CMS
2. **Imported via API** (when available)
3. **Version controlled** with git for tracking changes

All copy lives in content-marketing repo to maintain connection with
positioning and research context.

## Notes

- Service pages are longer than landing pages (400-600 vs 75-100 words)
- Each service should have dedicated positioning and research
- Use consistent structure across all service pages
- Test different CTAs and track conversion rates
- Update based on customer feedback and questions
