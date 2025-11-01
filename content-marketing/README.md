---
name: Content Marketing Framework
version: 1.2.0
type: Claude Agent Framework (CAF) for Editorial Workflows
created: 2025-10-31
purpose: Transform Claude Code into world-class editorial author-editor collaboration system
---

# Content Marketing Framework

**Version**: 1.2.0
**Type**: CAF for editorial workflows
**Purpose**: Professional content production with positioning-first process

---

## Overview

The Content Marketing Framework is a Claude Agent Framework (CAF) that transforms Claude Code into a professional editorial system. It implements the positioning-first approach where strategic decisions precede execution, enabling focused, purposeful content creation.

**Key Innovation**: Frameworks execute strategy, they don't create it. This framework operates within positioning constraints established by humans.

---

## Architecture

### Components

**5 Commands** (Workflow phases):
- `/position` - Strategic positioning session (7 questions → manifest)
- `/research` - Deep, curated research constrained by positioning
- `/outline` - Hierarchical outline using pyramid principle
- `/draft` - Full draft generation within constraints
- `/review` - Editorial review with actionable feedback

**5 Agents** (Specialized roles):
- `positioning-facilitator` - Guide positioning session, validate answers
- `researcher` - Conduct curated research, compile evidence
- `architect` - Create pyramid-structured outlines
- `author` - Generate drafts (executor, not strategist)
- `editor` - Review drafts, provide specific feedback

**3 Skills** (Behavioral patterns):
- `excellent-writing` - Clarity, precision, engagement (15 principles)
- `pyramid-principle` - Hierarchical structure (answer first)
- `scqa-framework` - Narrative structure (Situation-Complication-Question-Answer)

---

## Philosophy

### Positioning-First Process

**Traditional approach** (framework-first):
```
Topic → Framework generates structure → Framework creates content → Hope it's focused
```
**Problem**: Framework doesn't know business strategy, produces comprehensive but unfocused content.

**Our approach** (positioning-first):
```
Topic → Positioning session (7 questions) → Manifest → Framework executes within constraints
```
**Benefit**: Strategic decisions made by humans, framework executes with discipline.

### The 7 Strategic Questions

1. **What should reader DO?** (Desired action, not passive understanding)
2. **What's ONE thing to remember?** (Core message, ≤20 words)
3. **Who EXACTLY is this for?** (Specific audience + context)
4. **Why us vs alternatives?** (Clear positioning)
5. **What are we NOT covering?** (3-5 explicit exclusions for scope discipline)
6. **What's the max length?** (Hard constraint forces prioritization)
7. **How will we measure success?** (Observable metric)

**Output**: Positioning manifest (JSON) - the contract that constrains all downstream work.

---

## Standard Workflow

```
/position → /research → /outline → /draft → /review → /revise → /approve
```

**Phase 1: Positioning** (15-30 minutes)
- Run /position command
- Answer 7 strategic questions
- Generate positioning manifest
- Manifest becomes immutable contract

**Phase 2: Research** (1-4 hours depending on content type)
- Run /research command
- Curated research constrained by positioning
- Deep report with citations
- Evidence mapped to potential structure

**Phase 3: Outline** (30-60 minutes)
- Run /outline command
- Pyramid principle structure
- Core message at apex
- Research mapped to arguments
- Word count estimates per section

**Phase 4: Draft** (1-3 hours)
- Run /draft command
- Author generates complete draft
- Follows outline precisely
- Integrates research citations
- Operates within positioning constraints

**Phase 5: Review** (30-60 minutes)
- Run /review command
- Systematic editorial review
- Positioning validation
- Quality assessment
- Actionable feedback with severity levels

**Phase 6: Revision** (1-2 hours)
- Address editorial feedback
- Maintain positioning constraints
- Re-review if substantial changes

**Phase 7: Approval & Production**
- Mark approved when ready
- Prepare for publication

---

## Installation

### As Plugin (Recommended for Multiple Projects)

**Step 1: Copy to plugins directory**
```bash
cp -r framework/ ~/agents/plugins/content-marketing/
```

**Step 2: Create plugin manifest**
```bash
cat > ~/agents/plugins/content-marketing/.claude-plugin/plugin.json << 'EOF'
{
  "name": "content-marketing",
  "version": "1.2.0",
  "description": "Editorial workflow framework for professional content production with positioning-first process - enhanced with writing-skills methodologies (v1.2)",
  "author": "Factory",
  "commands_dir": "commands",
  "agents_dir": "agents",
  "dependencies": ["writing-skills@local"]
}
EOF
```

**Step 3: Enable in project**

In each content project's `.claude/settings.json`:
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
    "writing-skills@local": true,
    "content-marketing@local": true
  }
}
```

**Note**: content-marketing v1.2.0 requires writing-skills plugin for shared writing methodologies.

---

## Usage

### Quick Start

**1. Create content project directory**
```bash
mkdir -p ~/applied-ai/content-marketing/my-content-piece/
cd ~/applied-ai/content-marketing/my-content-piece/
```

**2. Enable framework** (see Installation above)

**3. Run positioning session**
```bash
/position my-content-piece "White paper on [topic]"
```

Answer 7 strategic questions. Positioning manifest created at:
`.claude/work/content/my-content-piece/positioning-manifest.json`

**4. Conduct research**
```bash
/research my-content-piece
```

Research report created with evidence and citations.

**5. Generate outline**
```bash
/outline my-content-piece
```

Hierarchical outline created using pyramid principle.

**6. Generate draft**
```bash
/draft my-content-piece
```

Complete draft created following outline and positioning.

**7. Editorial review**
```bash
/review my-content-piece
```

Editorial feedback with specific, actionable suggestions.

**8. Revise and iterate**

Address feedback, re-run /review if needed, approve when ready.

---

## Parallel Projects

**Multiple content pieces simultaneously**: Each project gets own Claude Code window.

**Setup**:
```bash
# Project 1
cd ~/applied-ai/content-marketing/claude-agent-framework/
claude  # Window 1: Author + Editor for CAF white paper

# Project 2
cd ~/applied-ai/content-marketing/automation-discovery/
claude  # Window 2: Author + Editor for ADF content

# Project 3
cd ~/applied-ai/content-marketing/landing-page/
claude  # Window 3: Author + Editor for website
```

**Benefits**:
- True parallelism (no bottleneck)
- Context isolation (each project focused)
- Independent workflows
- Same framework (via plugin)

---

## Content Types

### White Paper (10-15 pages, 3500-5000 words)
- **Research depth**: Deep (30+ page report, 20-30 sources, 2-4 hours)
- **Outline**: 5-7 major sections with detailed structure
- **Draft time**: 2-3 hours
- **Review**: Thorough (positioning, quality, effectiveness)
- **Format skill**: longform-technical-writing
- **Typical flow**: All 7 phases

### Blog Post (2,500 words)
- **Research depth**: Moderate (10-15 page report, 8-12 sources, 1-2 hours)
- **Outline**: 3-5 major sections
- **Draft time**: 1-2 hours
- **Review**: Standard
- **Format skill**: longform-technical-writing or website-copy
- **Typical flow**: All 7 phases

### Landing Page (800 words)
- **Research depth**: Light (5-7 page report, 5-8 sources, 30-60 min)
- **Outline**: 3 major sections (problem, solution, CTA)
- **Draft time**: 30-60 minutes
- **Review**: Focused on positioning and CTA
- **Format skill**: website-copy
- **Typical flow**: Positioning → Research → Draft → Review → Revise

### Social Media (400 words, LinkedIn/Twitter)
- **Research depth**: Minimal (2-3 page notes, 2-4 sources, 15-30 min)
- **Outline**: Simple structure (hook, point, CTA)
- **Draft time**: 15-30 minutes
- **Review**: Quick (positioning, engagement)
- **Format skill**: social-media-content-strategy
- **Typical flow**: Often derived from longer content, or Positioning → Draft → Review

---

## Positioning Manifest Examples

### Example 1: Technical White Paper
```json
{
  "content_purpose": "convince_senior_developers_to_try_caf",
  "core_message": "Transform Claude Code into domain-specific agents through markdown customization",
  "target_audience": "Senior software engineers familiar with Claude Code",
  "audience_context": "Frustrated by generic AI responses, want domain customization",
  "positioning": "Between out-of-box IDE (Claude Code) and programmatic API (Agent SDK)",
  "not_covering": [
    "Comprehensive feature list",
    "Development history",
    "Deep theoretical foundations"
  ],
  "max_length_words": 3500,
  "length_rationale": "White paper attention span, 15-20 page PDF",
  "success_metric": "GitHub stars and tutorial completions",
  "tone": "technical",
  "reading_level": "expert",
  "evidence_density": "high"
}
```

### Example 2: Landing Page
```json
{
  "content_purpose": "drive_quick_start_tutorial_completions",
  "core_message": "CAF prevents AI chaos through proven architecture",
  "target_audience": "Backend developers evaluating AI tools",
  "audience_context": "Burned by unreliable AI, skeptical but interested",
  "positioning": "Production-grade architecture vs raw Claude Code primitives",
  "not_covering": [
    "All plugin details",
    "Advanced customization",
    "Comparison matrix of all alternatives"
  ],
  "max_length_words": 800,
  "length_rationale": "Landing page attention span, 2-3 minute read",
  "success_metric": "Quick start completions within 24 hours",
  "tone": "technical",
  "reading_level": "technical",
  "evidence_density": "medium"
}
```

---

## Command Reference

### /position [content-piece-name] [description]
**Purpose**: Strategic positioning session
**Output**: positioning-manifest.json
**Duration**: 15-30 minutes
**Agent**: positioning-facilitator
**Next**: /research

### /research [content-piece-name] [focus-areas]
**Purpose**: Curated research
**Input**: positioning-manifest.json
**Output**: research-report.md
**Duration**: 1-4 hours (depends on content type)
**Agent**: researcher
**Next**: /outline

### /outline [content-piece-name]
**Purpose**: Hierarchical outline
**Input**: positioning-manifest.json, research-report.md
**Output**: outline.md
**Duration**: 30-60 minutes
**Agent**: architect
**Skill**: pyramid-principle
**Next**: /draft

### /draft [content-piece-name] [format-skill]
**Purpose**: Generate complete draft
**Input**: positioning-manifest.json, research-report.md, outline.md
**Output**: draft-v1.md
**Duration**: 1-3 hours
**Agent**: author
**Skills**: excellent-writing (required), format skill (optional)
**Next**: /review

### /review [content-piece-name] [draft-version]
**Purpose**: Editorial review
**Input**: positioning-manifest.json, research-report.md, outline.md, draft
**Output**: editorial-review-v1.md
**Duration**: 30-60 minutes
**Agent**: editor
**Next**: /revise or /approve

---

## Skills Reference

### excellent-writing (Core writing principles)
**15 principles for clarity, precision, engagement**
- Active voice preference
- Topic sentences
- Concrete examples
- Smooth transitions
- Paragraph coherence
- See: skills/excellent-writing.md

### pyramid-principle (Hierarchical structure)
**Answer first, then supporting points, then details**
- Core message at apex
- 3-5 major arguments
- Evidence and examples
- Logical ordering
- See: skills/pyramid-principle.md

### scqa-framework (Narrative structure)
**Situation → Complication → Question → Answer**
- Engage with familiar situation
- Create tension with complication
- Raise question reader wants answered
- Deliver answer with impact
- See: skills/scqa-framework.md

---

## Best Practices

### DO
- ✅ Run /position FIRST, always (no exceptions)
- ✅ Answer positioning questions specifically (not vague)
- ✅ Enforce NOT-covering list strictly (scope discipline)
- ✅ Stay within max_length_words (hard constraint)
- ✅ Integrate research with citations (evidence-based)
- ✅ Follow outline structure precisely (blueprint set)
- ✅ Address editorial feedback systematically (prioritize by severity)

### DON'T
- ❌ Skip positioning (framework can't make strategic decisions)
- ❌ Accept vague positioning answers (specificity matters)
- ❌ Add NOT-covering topics (positioning is contract)
- ❌ Exceed max_length_words (constraint forces prioritization)
- ❌ Make unsupported claims (research provides evidence)
- ❌ Deviate from outline during drafting (structure is set)
- ❌ Ignore critical editorial feedback (must address before approval)

---

## Troubleshooting

### Issue: Positioning manifest feels restrictive
**Solution**: That's the point. Constraints force focus and prioritization. If manifest doesn't fit, re-run /position with adjusted answers.

### Issue: Research takes too long
**Solution**: Adjust depth to content type. Landing pages need 30-60 min research, not 4 hours. See Content Types section for guidelines.

### Issue: Draft exceeds max_length_words
**Solution**: Author must cut during generation. Editor will flag in review. Cut nice-to-have examples, condense redundancy, never cut core message or key evidence.

### Issue: Editorial feedback overwhelming
**Solution**: Prioritize by severity. Critical issues MUST be addressed. Important SHOULD be addressed. Minor are optional improvements.

### Issue: Need to change positioning mid-draft
**Solution**: If positioning genuinely wrong, re-run /position and start over. Don't try to retrofit new positioning onto old content. Better to restart than force misaligned content.

### Issue: Multiple authors on same content
**Solution**: Not recommended. This framework designed for single author-editor collaboration per piece. For multi-author, coordinate externally and use framework for final integration.

---

## Migration from Other Approaches

### From Manual Process
**Advantages**: Systematic, repeatable, scalable
**Keep**: Subject matter expertise, strategic judgment
**Gain**: Structured workflow, positioning discipline, editorial consistency

### From Generic Writing Frameworks
**Advantages**: Positioning-first (not structure-first)
**Keep**: Writing skills, domain knowledge
**Gain**: Strategic clarity, scope discipline, focused execution

### From Template-Based Systems
**Advantages**: Flexible, adapts to positioning
**Keep**: Format templates (as skills)
**Gain**: Strategic foundation, evidence-based content, quality standards

---

## Version History

**v1.2.0** (2025-11-01):
- Added writing-skills@local dependency (shared skills library)
- Enhanced architect agent with optional Diátaxis mode selection
- Enhanced author agent with topic-sentence-method and information-mapping techniques
- Skills moved to shared library (no duplication)
- All enhancements optional (fully backward compatible with v1.1)

**v1.1.0** (2025-10-31):
- Editor fabrication prevention (70-90% reduction in metric fabrication)
- Enhanced priority framework (data-dependent recommendations marked as Optional)
- Added IF-THEN template pattern for data-dependent claims
- Added Step 5: Self-Validation Checkpoint to editor agent
- Critical constraint against fabrication added

**v1.0.0** (2025-10-31):
- Initial release
- 5 commands (position, research, outline, draft, review)
- 5 agents (positioning-facilitator, researcher, architect, author, editor)
- 3 skills (excellent-writing, pyramid-principle, scqa-framework)
- Positioning-first process
- Systematic editorial workflow

---

## Support & Evolution

**Documentation**: See individual command/agent/skill files for detailed guides

**Questions**: Review positioning manifest if unclear about scope or constraints

**Improvements**: Framework will evolve based on actual use. Current version (1.2.0) builds on MVF with optional writing methodology enhancements. Add commands, agents, or skills as patterns emerge from use.

**Philosophy**: Build for observed needs, not anticipated ones. This framework has what's proven necessary. Don't add features "just in case."

---

**Framework Version**: 1.2.0
**Created**: 2025-10-31
**Purpose**: World-class editorial workflow as CAF instantiation
**Key Innovation**: Positioning-first process where strategic decisions precede execution
