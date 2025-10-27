# Marketing Plugin

**Version**: 1.0.0
**Type**: Claude Code Plugin
**Purpose**: Content marketing skills for technical B2B audiences

---

## Overview

The Marketing plugin provides specialized content marketing skills for creating and distributing technical content to developer audiences. It includes platform-specific strategies, content frameworks, and progressive disclosure patterns that activate only when planning campaigns or creating content.

---

## Skills

### 1. social-media-content-strategy (20KB)

**Activation Rate**: 15-20% (occasional)
**Token Savings**: 80-85%

Platform-specific social media content strategies for LinkedIn and Twitter/X targeting technical B2B audiences (developers, AI practitioners, technology decision-makers).

**Activates when**:
- Planning social media campaigns
- Creating LinkedIn posts
- Designing Twitter/X threads
- Discussing platform-specific strategies
- Adapting content for multiple platforms

**Provides**:
- LinkedIn strategy (algorithm, H-B-C-Q structure, formatting, content types)
- Twitter/X strategy (algorithm, H-M-S-C threads, 20+ hook formulas, engagement)
- Cross-platform adaptation framework
- Content calendar planning
- Engagement metrics and success indicators

**Does NOT activate during**:
- General development work
- Code reviews or API design
- Testing and debugging

### 2. longform-technical-writing (33KB)

**Activation Rate**: 10-15% (occasional)
**Token Savings**: 85-90%

Comprehensive framework for creating authoritative long-form technical content (white papers, technical blogs, case studies, tutorials) for developer audiences.

**Activates when**:
- Writing blog posts (1,500-3,000 words)
- Creating white papers (4,000-6,000 words)
- Developing technical case studies
- Crafting step-by-step tutorials
- Planning content atomization (1 hub → many derivatives)

**Provides**:
- Structure & organization (layered complexity, atomization-ready design)
- Authority & credibility (working code, benchmarks, trade-offs)
- Technical presentation (code formatting, visuals, complexity management)
- SEO & discoverability (keywords, headlines, distribution)
- Engagement & conversion (hooks, CTAs, metrics)
- Content repurposing (1 hub → 10-20 spokes, 2.6x efficiency)

**Does NOT activate during**:
- Code implementation
- API design or architecture
- Testing and debugging
- Short documentation (README, inline comments)

### 3. content-marketing-campaign (26KB)

**Activation Rate**: 10-15% (occasional)
**Token Savings**: 85-90%

Comprehensive multi-channel campaign framework for launching and sustaining technical B2B products through strategic content marketing.

**Activates when**:
- Planning product launches
- Developing multi-channel campaign strategies
- Creating hub-and-spoke content clusters
- Coordinating content atomization workflows
- Building master content calendars
- Measuring campaign performance

**Provides**:
- Positioning & messaging hierarchy (3-level pyramid framework)
- Hub-and-spoke content model (pillar pages + 8-22 spoke articles)
- Content atomization workflows (1 core asset → 20+ derivatives)
- Multi-channel distribution (tiered channels: owned, community, social)
- Campaign coordination (master calendar, concurrent launches)
- Performance measurement (developer-centric KPIs, not traditional MQLs)

**Does NOT activate during**:
- Creating individual content pieces (activates longform-technical-writing)
- Writing social media posts (activates social-media-content-strategy)
- General development work
- Code implementation or testing

---

## Progressive Disclosure Pattern

Both skills follow the **occasional activation** principle:

**Startup overhead**: ~150 bytes metadata per skill (~300 bytes total)
**Runtime loading**: Full content (20KB or 33KB) only when situational context triggers activation
**Token efficiency**: 80-90% savings vs always-on embedding

**Example**:
- Developer working on API implementation: Skills dormant (300 bytes)
- Developer planning LinkedIn post about API: social-media-content-strategy activates (20KB)
- Developer writing blog post about API patterns: longform-technical-writing activates (33KB)

---

## Installation

### Option 1: Enable in Project Settings

Add to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "stefan-plugins": {
      "source": {
        "source": "directory",
        "path": "/home/stefan/agents/plugins"
      }
    }
  },
  "enabledPlugins": {
    "marketing@stefan-plugins": true
  }
}
```

### Option 2: Copy to Project

Copy skills directly to your project:

```bash
mkdir -p .claude/skills/
cp -r ~/agents/plugins/marketing/skills/* .claude/skills/
```

---

## Usage Examples

### Social Media Content

**Scenario**: Planning LinkedIn post about your open source project

```
User: "I want to create a LinkedIn post announcing our new Claude Code plugin collection"

Claude: [social-media-content-strategy skill activates]
Based on LinkedIn's 2025 algorithm priorities, here's a high-performing post structure:

Hook (first 210 chars - visible before "see more"):
"We built 9 Claude Code plugins and made them open source. 2 months of work,
zero cost to use. Here's what we learned about plugin architecture:"

Body (1,200-1,500 chars):
[Uses H-B-C-Q framework from skill...]
```

### Long-Form Content

**Scenario**: Writing technical blog post

```
User: "Help me write a blog post about connection pooling in Python"

Claude: [longform-technical-writing skill activates]
Let's structure this as a 2,000-word technical blog post:

## Title
"Python Connection Pooling: Cut API Latency 91%"

## Executive Summary (300 words)
[Applies structure template from skill...]

## Main Body
[Uses P-A-R-I framework, working code examples, benchmarks with methodology...]
```

---

## Content Marketing Formula

Both skills implement the proven formula for developer content:

```
Technical Expertise + Working Code + Honest Trade-offs
+ Strategic Atomization + Multi-Channel Distribution
= Authority + Reach + Conversions
```

**Key Principles**:
1. **Technical authenticity** - Engineers detect fluff immediately
2. **Practical value** - Must be actionable
3. **Honest communication** - Acknowledge failures and limitations
4. **Progressive disclosure** - Activate only when needed (80-90% token savings)
5. **Content atomization** - 1 comprehensive piece → 10-20+ derivatives (2.6x efficiency)

---

## Validation

Both skills validated against occasional activation criteria:

| Criterion | social-media | longform-writing | Status |
|-----------|-------------|-----------------|--------|
| **Activation Rate (10-25%)** | 15-20% ✅ | 10-15% ✅ | PASS |
| **Clear Triggers** | Keywords + situational ✅ | Keywords + situational ✅ | PASS |
| **Non-Trivial Expertise** | 20KB ✅ | 33KB ✅ | PASS |
| **High Value** | Prevents wasted campaigns ✅ | 2.6x content efficiency ✅ | PASS |
| **Not Redundant** | No existing commands ✅ | No existing commands ✅ | PASS |

Full validation: `.claude/work/current/010_content_marketing_framework/SKILL_VALIDATION.md`

---

## Comparison to Development Skills

**error-recovery-patterns** (development plugin, 24KB):
- Activates when task execution fails (10-20% rate)
- Prevents cascade failures, data corruption

**data-modeling-patterns** (development plugin, 25KB):
- Activates when designing schemas (15-20% rate)
- Prevents costly migrations, performance issues

**social-media-content-strategy** (marketing plugin, 20KB):
- Activates when planning social content (15-20% rate)
- Prevents algorithmic suppression, maximizes reach

**longform-technical-writing** (marketing plugin, 33KB):
- Activates when creating long-form content (10-15% rate)
- Establishes credibility, 2.6x content efficiency

**Pattern**: All follow same occasional activation design (10-25% rate, 70-90% token savings)

---

## Development Context

**Created**: 2025-10-20
**Work Unit**: `.claude/work/current/010_content_marketing_framework/`
**Research Base**: 182KB across 3 comprehensive reports
  - CONTENT_MARKETING.md (72KB)
  - SOCIAL_MEDIA.md (94KB)
  - LONGFORM.md (16KB)

**Design Framework**: SKILL_DESIGN_GUIDE.md (occasional activation principles)

---

## Version History

### 1.0.0 (2025-10-20)
- Initial release
- 2 skills: social-media-content-strategy, longform-technical-writing
- Validated against occasional activation criteria
- Progressive disclosure pattern (80-90% token savings)

---

## License

MIT License - Free to use, modify, and distribute

---

## Contributing

Skills designed using consultative approach:
1. Deep investigation (182KB research)
2. Evidence-based design (validation against criteria)
3. Progressive disclosure (occasional activation 10-25%)
4. Token efficiency (80-90% savings)

To add new content marketing skills:
1. Research thoroughly (50KB+ evidence base)
2. Validate against occasional activation criteria
3. Ensure 10-25% activation rate (not constant)
4. Document token efficiency gains

---

**Contact**: Stefan
**Repository**: ~/agents/plugins/marketing/
**Documentation**: This README + skill SKILL.md files
