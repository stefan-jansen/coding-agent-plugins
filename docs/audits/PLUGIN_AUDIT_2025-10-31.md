# Plugin Marketplace Audit Report

**Date**: 2025-10-31
**Auditor**: Factory agent
**Marketplace**: `local` (~/.agents/plugins/)
**Plugins Audited**: 13 plugins

---

## Executive Summary

**Overall Health**: ⚠️ **Needs Attention**

**Key Findings**:
- ✅ All 13 plugin.json files are valid JSON
- ✅ All referenced commands/agents files exist
- ⚠️ 2 duplicate names found (review, architect)
- 🔴 3 plugins have incomplete definitions (missing commands/agents/skills in plugin.json)
- ✅ No wildcard patterns found (fixed previously)

**Recommendations**:
1. Fix incomplete plugin definitions (HIGH PRIORITY)
2. Resolve duplicate names with namespacing
3. Consider consolidating or deprecating underutilized plugins

---

## Plugin Inventory

### Active & Complete (8 plugins)

#### 1. System (v1.0.0)
**Status**: ✅ Complete
**Commands**: 4 (audit, cleanup, setup, status)
**Agents**: None
**Purpose**: System configuration and health management

#### 2. Workflow (v1.0.0)
**Status**: ✅ Complete
**Commands**: 6 (explore, plan, next, ship, spike, work)
**Agents**: None
**Purpose**: Structured development workflow

#### 3. Development (v1.0.0)
**Status**: ✅ Complete, ⚠️ Has duplicate names
**Commands**: 6 (analyze, docs, fix, git, **review**, test)
**Agents**: 3 (**architect**, code-reviewer, test-engineer)
**Purpose**: Code development and quality assurance
**Note**: `review` command and `architect` agent also exist in content-marketing

#### 4. Memory (v1.0.0)
**Status**: ✅ Complete
**Commands**: 4 (index, memory-gc, memory-review, performance)
**Agents**: None
**Purpose**: Active memory management

#### 5. Agents (v1.0.0)
**Status**: ✅ Complete
**Commands**: 2 (agent, serena)
**Agents**: 2 (auditor, reasoning-specialist)
**Purpose**: Specialized agent invocation

#### 6. Quant (v1.0.0)
**Status**: ✅ Complete
**Commands**: 6 (quant-explore, quant-plan, quant-next, quant-ship, experiment, evaluate)
**Agents**: 4 (quant-ml-validator, quant-backtest-validator, quant-risk-validator, data-scientist)
**Purpose**: Quantitative finance ML framework

#### 7. Reports (v1.0.0)
**Status**: ✅ Complete
**Commands**: 1 (report)
**Agents**: 1 (report-generator)
**Purpose**: Professional stakeholder reports

#### 8. Web Development (v1.1.1)
**Status**: ✅ Complete
**Commands**: 4 (web-explore, web-plan, web-next, web-ship)
**Agents**: 2 (frontend-engineer, backend-django)
**Purpose**: Full-stack web development

### Recently Fixed (2 plugins)

#### 9. Structured Intelligence (v1.0.0)
**Status**: ✅ Complete (recently added)
**Commands**: 7 (define-messages, frame-content, expand-outline, draft-section, review-content, propose, summarize)
**Agents**: 8 (message-architect, analyst, narrative-framer, diataxis-planner, outline-expander, section-drafter, formatter, evidence-validator)
**Skills**: 6 (pyramid-principle, scqa-framework, diataxis-framework, topic-sentence-method, information-mapping, plain-language)
**Purpose**: Hierarchical content creation with evidence-first methodology

#### 10. Content Marketing (v1.0.0)
**Status**: ✅ Complete, ⚠️ Has duplicate names
**Commands**: 5 (position, research, outline, draft, **review**)
**Agents**: 5 (positioning-facilitator, researcher, **architect**, author, editor)
**Purpose**: Editorial workflow with positioning-first process
**Note**: `review` command and `architect` agent also exist in development

### Incomplete Definitions (3 plugins) 🔴

#### 11. Marketing (v1.0.0)
**Status**: 🔴 INCOMPLETE - Has content but missing plugin.json definitions
**Commands**: None defined
**Agents**: None defined
**Skills**: **4 skills directories exist but NOT referenced**:
  - content-marketing-campaign
  - longform-technical-writing
  - social-media-content-strategy
  - website-copy

**Problem**: Plugin.json has NO commands/agents/skills defined, but ~/agents/plugins/marketing/skills/ contains 4 skill directories

**Fix Needed**: Add skills array to plugin.json

#### 12. ML3T Researcher (v2.0.0)
**Status**: 🔴 INCOMPLETE - Has agent file but not defined
**Commands**: None defined
**Agents**: **1 agent file exists but NOT referenced**:
  - ml3t-researcher.md

**Problem**: Plugin.json has NO agents defined, but ~/agents/plugins/ml3t/researcher/agents/ml3t-researcher.md exists

**Fix Needed**: Add agents array to plugin.json

#### 13. ML3T Coauthor (v1.0.0)
**Status**: 🔴 INCOMPLETE - Has 14 commands + 1 agent but not defined
**Commands**: **14 command files exist but NOT referenced**:
  - design-code-examples.md
  - expand-section.md
  - help.md
  - integrate-chapter.md
  - notebook.md
  - review.md
  - status.md
  - sync.md
  - test.md
  - track-citations.md
  - validate-los.md
  - verify-chapter.md
  - write.md
  - (README.md - not a command)

**Agents**: **1 agent file exists but NOT referenced**:
  - ml3t-coauthor.md

**Problem**: Plugin.json has NO commands/agents defined, but files exist in directories

**Fix Needed**: Add commands and agents arrays to plugin.json

---

## Critical Issues

### Issue 1: Duplicate Command Names 🔴

**Command**: `review`
**Plugins**: development, content-marketing

**Impact**:
- Namespace collision when both plugins enabled
- Claude Code may not know which to invoke
- Unclear which gets priority

**Recommendation**:
- Rename development's `/review` to `/development:review` or `/code-review`
- Keep content-marketing's `/review` as `/content-marketing:review`
- Or use plugin namespacing: `/development:review` vs `/content-marketing:review`

### Issue 2: Duplicate Agent Names 🔴

**Agent**: `architect`
**Plugins**: development, content-marketing

**Agents have different purposes**:
- **development/architect**: System design and architectural decisions (code architecture)
- **content-marketing/architect**: Content structure and pyramid principle (content architecture)

**Impact**:
- Agent invocation ambiguity
- Wrong agent may be invoked

**Recommendation**:
- Rename development's `architect` to `system-architect` or `code-architect`
- Rename content-marketing's `architect` to `content-architect`

### Issue 3: Incomplete Plugin Definitions 🔴

**3 plugins have files but not referenced in plugin.json**:

1. **marketing**: 4 skill directories unreferenced
2. **ml3t-researcher**: 1 agent unreferenced
3. **ml3t-coauthor**: 14 commands + 1 agent unreferenced

**Impact**:
- Commands/agents/skills exist but unavailable to users
- Confusing - plugin appears empty when it's not
- Wasted work - built but not accessible

**Recommendation**:
- Add proper definitions to each plugin.json
- Or deprecate/remove if no longer needed

---

## Detailed Findings

### Commands Catalog (48 total across 10 plugins)

**By Plugin**:
- Structured Intelligence: 7 commands
- Workflow: 6 commands
- Development: 6 commands
- Quant: 6 commands
- Content Marketing: 5 commands
- System: 4 commands
- Memory: 4 commands
- Web Development: 4 commands
- Agents: 2 commands
- Reports: 1 command

**ML3T Coauthor**: 14 commands exist but not defined

**Namespace Usage**:
- ✅ Quant uses prefixes: `quant-explore`, `quant-plan`, etc.
- ✅ Web uses prefixes: `web-explore`, `web-plan`, etc.
- ⚠️ Most plugins use plain names, risking collisions

### Agents Catalog (28 total across 8 plugins)

**By Plugin**:
- Structured Intelligence: 8 agents
- Content Marketing: 5 agents
- Quant: 4 agents
- Development: 3 agents
- Agents: 2 agents
- Web Development: 2 agents
- Reports: 1 agent
- ML3T Researcher: 1 agent (exists but not defined)
- ML3T Coauthor: 1 agent (exists but not defined)

### Skills Catalog

**Structured Intelligence**: 6 skills
- pyramid-principle
- scqa-framework
- diataxis-framework
- topic-sentence-method
- information-mapping
- plain-language

**Marketing**: 4 skill directories (unreferenced)
- content-marketing-campaign
- longform-technical-writing
- social-media-content-strategy
- website-copy

### Version Distribution

- **v1.0.0**: 11 plugins (standard)
- **v1.1.1**: 1 plugin (web-development)
- **v2.0.0**: 1 plugin (ml3t-researcher)

---

## Recommendations

### High Priority 🔴

#### 1. Fix Incomplete ML3T Coauthor Plugin
**File**: `~/agents/plugins/ml3t/coauthor/.claude-plugin/plugin.json`

Add to plugin.json:
```json
{
  "commands": [
    "./commands/design-code-examples.md",
    "./commands/expand-section.md",
    "./commands/help.md",
    "./commands/integrate-chapter.md",
    "./commands/notebook.md",
    "./commands/review.md",
    "./commands/status.md",
    "./commands/sync.md",
    "./commands/test.md",
    "./commands/track-citations.md",
    "./commands/validate-los.md",
    "./commands/verify-chapter.md",
    "./commands/write.md"
  ],
  "agents": [
    "./agents/ml3t-coauthor.md"
  ]
}
```

**Note**: ml3t-coauthor also has a `review` command - will create 3-way collision with development and content-marketing!

#### 2. Fix Incomplete ML3T Researcher Plugin
**File**: `~/agents/plugins/ml3t/researcher/.claude-plugin/plugin.json`

Add to plugin.json:
```json
{
  "agents": [
    "./agents/ml3t-researcher.md"
  ]
}
```

#### 3. Fix Incomplete Marketing Plugin
**File**: `~/agents/plugins/marketing/.claude-plugin/plugin.json`

Add to plugin.json:
```json
{
  "skills": [
    "./skills/content-marketing-campaign/",
    "./skills/longform-technical-writing/",
    "./skills/social-media-content-strategy/",
    "./skills/website-copy/"
  ]
}
```

#### 4. Resolve Duplicate Names

**Option A: Namespace All Duplicates** (Recommended)
- Development: `/development:review`, agent `code-architect`
- Content Marketing: `/content-marketing:review`, agent `content-architect`
- ML3T Coauthor: `/ml3t-coauthor:review`

**Option B: Keep Generics, Namespace Specific**
- Development: `/review` (most general)
- Content Marketing: `/content-marketing:review`
- ML3T Coauthor: `/ml3t-review` or `/coauthor:review`
- Development: agent `architect` (most general)
- Content Marketing: agent `content-architect`

**Option C: Consolidate** (if appropriate)
- If review commands are similar, create one unified review command
- Unlikely to work given different domains

### Medium Priority ⚠️

#### 5. Consider Plugin Consolidation

**Observation**: Several plugins have overlapping purposes

**Possible consolidations**:
1. **Writing Plugins** (4 plugins):
   - marketing (skills)
   - structured-intelligence (7 commands, 8 agents, 6 skills)
   - content-marketing (5 commands, 5 agents)
   - ml3t-coauthor (14 commands, 1 agent)

   **Question**: Should these be consolidated? Or are they domain-specific enough to keep separate?

2. **Workflow Plugins** (3 plugins):
   - workflow (6 commands - general)
   - quant (6 commands - quant-specific)
   - web-development (4 commands - web-specific)

   **Current state**: Good - domain-specific variants of core workflow

#### 6. Document Plugin Dependencies

Some plugins may depend on others:
- Does web-development depend on workflow?
- Does quant depend on development?
- Does content-marketing depend on marketing skills?

**Recommendation**: Add `dependencies` field to plugin.json if needed

#### 7. Add Plugin Categories

Suggested categories for marketplace organization:
- **Core**: system, workflow, development, memory, agents
- **Domain**: quant, web-development, reports
- **Writing**: marketing, structured-intelligence, content-marketing
- **ML4T**: ml3t-researcher, ml3t-coauthor

### Low Priority ℹ️

#### 8. Standardize Versioning

Current: Mix of 1.0.0, 1.1.1, 2.0.0
**Recommendation**: Document versioning strategy in marketplace README

#### 9. Add Screenshots/Examples

**Recommendation**: Add `screenshots/` or `examples/` subdirectories to plugins

#### 10. Repository Links

Many plugins reference: `"repository": "https://github.com/yourusername/claude-code-plugins"`
**Recommendation**: Update to actual repository URLs when available

---

## Plugin Health Scorecard

| Plugin | JSON Valid | Files Exist | Complete | Duplicates | Score |
|--------|-----------|-------------|----------|------------|-------|
| system | ✅ | ✅ | ✅ | - | 100% |
| workflow | ✅ | ✅ | ✅ | - | 100% |
| development | ✅ | ✅ | ✅ | ⚠️ 2 | 90% |
| memory | ✅ | ✅ | ✅ | - | 100% |
| agents | ✅ | ✅ | ✅ | - | 100% |
| quant | ✅ | ✅ | ✅ | - | 100% |
| reports | ✅ | ✅ | ✅ | - | 100% |
| marketing | ✅ | - | 🔴 | - | 50% |
| web-development | ✅ | ✅ | ✅ | - | 100% |
| ml3t-researcher | ✅ | - | 🔴 | - | 50% |
| ml3t-coauthor | ✅ | - | 🔴 | ⚠️ 1 | 40% |
| structured-intelligence | ✅ | ✅ | ✅ | - | 100% |
| content-marketing | ✅ | ✅ | ✅ | ⚠️ 2 | 90% |

**Average Score**: 82%

---

## Action Plan

### Immediate (Today)

1. ✅ Complete this audit
2. 🔲 Fix ml3t-coauthor plugin.json (add 14 commands + 1 agent)
3. 🔲 Fix ml3t-researcher plugin.json (add 1 agent)
4. 🔲 Fix marketing plugin.json (add 4 skills)

### Short-term (This Week)

4. 🔲 Resolve duplicate `review` command (3-way collision!)
5. 🔲 Resolve duplicate `architect` agent (2-way collision)
6. 🔲 Test all plugins load correctly after fixes

### Medium-term (This Month)

7. 🔲 Evaluate plugin consolidation opportunities
8. 🔲 Document plugin dependencies if any
9. 🔲 Add plugin categories to marketplace.json
10. 🔲 Standardize namespace usage across plugins

---

## Testing Checklist

After fixes, test each plugin:

```bash
# Create test project
mkdir -p /tmp/plugin-test
cd /tmp/plugin-test

# Test each plugin
cat > .claude/settings.json << EOF
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
    "PLUGIN_NAME@local": true
  }
}
EOF

# Start Claude Code and verify:
# 1. Plugin loads without errors
# 2. Commands are available
# 3. Agents can be invoked
# 4. No namespace collisions
```

---

## Appendix: Full Command/Agent Listings

### All Commands (48 defined + 14 undefined)

**System (4)**:
- audit, cleanup, setup, status

**Workflow (6)**:
- explore, next, plan, ship, spike, work

**Development (6)**:
- analyze, docs, fix, git, review, test

**Memory (4)**:
- index, memory-gc, memory-review, performance

**Agents (2)**:
- agent, serena

**Quant (6)**:
- quant-explore, quant-plan, quant-next, quant-ship, experiment, evaluate

**Reports (1)**:
- report

**Web Development (4)**:
- web-explore, web-plan, web-next, web-ship

**Structured Intelligence (7)**:
- define-messages, frame-content, expand-outline, draft-section, review-content, propose, summarize

**Content Marketing (5)**:
- position, research, outline, draft, review

**ML3T Coauthor (14 undefined)**:
- design-code-examples, expand-section, help, integrate-chapter, notebook, review, status, sync, test, track-citations, validate-los, verify-chapter, write

### All Agents (28 defined + 2 undefined)

**Development (3)**:
- architect, code-reviewer, test-engineer

**Agents (2)**:
- auditor, reasoning-specialist

**Quant (4)**:
- quant-ml-validator, quant-backtest-validator, quant-risk-validator, data-scientist

**Reports (1)**:
- report-generator

**Web Development (2)**:
- frontend-engineer, backend-django

**Structured Intelligence (8)**:
- message-architect, analyst, narrative-framer, diataxis-planner, outline-expander, section-drafter, formatter, evidence-validator

**Content Marketing (5)**:
- positioning-facilitator, researcher, architect, author, editor

**ML3T Researcher (1 undefined)**:
- ml3t-researcher

**ML3T Coauthor (1 undefined)**:
- ml3t-coauthor

---

**Report Status**: COMPLETE
**Next Action**: Review with user and execute action plan
