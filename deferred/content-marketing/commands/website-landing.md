---
description: Generate concise, SEO-optimized landing page copy for website sections. Uses positioning, research, and SEO skills to create scannable, high-converting web content.
---

# website-landing

Generate landing page copy for website sections using positioning and research context.

## Usage

```bash
# Generate landing page for specific service/topic
/website-landing "AI consulting services"

# Generate with specific positioning
/website-landing --positioning @positioning-doc.md "Enterprise AI transformation"

# Generate for homepage hero section
/website-landing --section hero "Applied AI - AI Strategy & Implementation"
```

## Process

This command follows a web-optimized content creation process:

1. **Load Context**
   - Read positioning documents from content-marketing repo
   - Review relevant research files
   - Load any existing website content

2. **Invoke Writing Skills**
   - `seo-copywriting` - Keyword optimization and search intent
   - `concise-web-copy` - Scannable, high-impact writing
   - `search-intent-alignment` - Match user search intent

3. **Generate Copy**
   - Headline (H1) - Clear value proposition
   - Subheadline - Supporting benefit statement
   - Body copy - 2-3 short paragraphs, scannable
   - Call-to-action - Clear next step

4. **Save to Website Directory**
   - Save to `website/[section]-landing.md`
   - Include metadata (keywords, intent, word count)
   - Version control with git

## Output Location

All website copy saves to: `~/path/to/your-site/content/website/`

**Structure**:
```
website/
  ├── homepage-hero.md
  ├── services-ai-consulting.md
  ├── about-team.md
  └── contact.md
```

## Best Practices

### Landing Page Copy Principles

1. **Lead with Value** - State benefit immediately
2. **Be Concise** - 50-100 words max per section
3. **Scannable** - Short paragraphs, bullet points
4. **Action-Oriented** - Clear CTAs
5. **SEO-Aware** - Natural keyword inclusion

### Example Output

```markdown
# Transform Your Business with Strategic AI Implementation

We help enterprises unlock competitive advantage through practical AI solutions
that deliver measurable ROI in months, not years.

Our proven methodology combines deep technical expertise with business strategy
to implement AI systems that actually work. From feasibility assessment to
production deployment, we guide you through every step.

**Ready to explore AI opportunities?** Schedule a free 30-minute discovery call.

---
Keywords: AI consulting, enterprise AI, AI implementation, AI strategy
Search Intent: Commercial - Looking for AI consulting services
Word Count: 87 words
```

## Integration with Editorial Workflow

Website copy uses the same positioning and research as long-form content:

```bash
# 1. Define positioning (if not done)
/position "Applied AI consulting services"

# 2. Research (if not done)
/research "AI consulting market, buyer personas, competitive landscape"

# 3. Generate website copy
/website-landing "AI consulting services"

# 4. Review and refine
/review website/services-ai-consulting.md
```

## SEO Optimization

The command automatically:
- Identifies target keywords from positioning/research
- Aligns with search intent (informational, commercial, transactional)
- Optimizes headline for click-through
- Includes semantic keywords naturally
- Suggests meta description

## Options

- `--positioning FILE` - Use specific positioning document
- `--research FILE` - Reference specific research
- `--section NAME` - Target specific website section
- `--keywords "kw1, kw2"` - Target specific keywords
- `--word-count N` - Target word count (default: 75-100)
- `--tone TONE` - Professional (default), friendly, technical, executive

## Tips

**For Homepage Hero**:
```bash
/website-landing --section hero --word-count 50 "Applied AI"
```

**For Service Pages**:
```bash
/website-landing --section services --keywords "AI consulting, enterprise AI" "AI Strategy"
```

**For About Page**:
```bash
/website-landing --section about --tone friendly "Applied AI team"
```

## Related Commands

- `/position` - Define positioning first
- `/research` - Gather context
- `/website-service` - Generate full service page
- `/review` - Review and refine copy

## Notes

- Website copy lives in content-marketing repo, not website repo
- This ensures copy is created with full positioning/research context
- Export to website via Wagtail CMS import/export (when available)
- All writing skills auto-invoke based on task context
