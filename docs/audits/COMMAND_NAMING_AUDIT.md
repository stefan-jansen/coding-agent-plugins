# Command Naming Consistency Audit

**Date**: 2025-11-01
**Issue**: User noted `/status` is not namespaced like `/system:status`
**Question**: Should all commands be namespaced consistently?

---

## How Claude Code Command Naming Works

**Plugin-Level Namespacing**:
When a plugin is loaded, Claude Code creates namespaced commands:
- Plugin name: `system`
- Command file: `commands/status.md` (with `name: status`)
- Available as: `/system:status`

**Global vs Namespaced**:
- **Namespaced**: `/plugin-name:command-name` (e.g., `/system:status`)
- **Global**: `/command-name` (only if no namespace conflict)

---

## Current Plugin Commands

### system@local (4 commands)
- `/system:status` ✅ Namespaced
- `/system:audit` ✅ Namespaced
- `/system:cleanup` ✅ Namespaced
- `/system:setup` ✅ Namespaced

**Files**:
- `status.md` (name: status)
- `audit.md` (name: audit)
- `cleanup.md` (name: cleanup)
- `setup.md` (name: setup)

### workflow@local (6 commands)
- `/workflow:explore` ✅ Namespaced
- `/workflow:plan` ✅ Namespaced
- `/workflow:next` ✅ Namespaced
- `/workflow:ship` ✅ Namespaced
- `/workflow:spike` ✅ Namespaced
- `/workflow:work` ✅ Namespaced

**Files**:
- `explore.md`, `plan.md`, `next.md`, `ship.md`, `spike.md`, `work.md`

### memory@local (7 commands)
- `/memory:continue` ✅ Namespaced
- `/memory:handoff` ✅ Namespaced
- `/memory:index` ✅ Namespaced
- `/memory:memory-gc` ✅ Namespaced
- `/memory:memory-review` ✅ Namespaced
- `/memory:memory-update` ✅ Namespaced
- `/memory:performance` ✅ Namespaced

**Files**:
- `continue.md`, `handoff.md`, `index.md`, `memory-gc.md`, `memory-review.md`, `memory-update.md`, `performance.md`

### development@local (6 commands)
**Need to check**: Are these namespaced?
- Expected: `/development:analyze`, `/development:test`, `/development:fix`, `/development:review`, `/development:git`, `/development:docs`

### content-marketing@local (5 commands)
- `/content-marketing:position` ✅ Namespaced
- `/content-marketing:research` ✅ Namespaced
- `/content-marketing:outline` ✅ Namespaced
- `/content-marketing:draft` ✅ Namespaced
- `/content-marketing:review` ✅ Namespaced

**Files**:
- `position.md`, `research.md`, `outline.md`, `draft.md`, `review.md`

---

## The `/status` Question

**User observation**: "`/status` is not namespaced like `/system:status`"

**Likely scenario**:
1. User tried `/status` and it worked
2. But documentation shows `/system:status`
3. Question: Which is correct?

**Hypothesis**: Both may work due to how Claude Code handles commands:
- Primary: `/system:status` (explicit namespace)
- Shortcut: `/status` (if no conflict, Claude Code may allow unnamespaced access)

**The issue**: Inconsistent documentation/usage patterns

---

## Investigation Needed

### 1. Check Development Plugin Commands

Let me check development plugin structure:

**Expected commands** (based on global CLAUDE.md):
- `/development:analyze` or `/analyze`?
- `/development:test` or `/test`?
- `/development:fix` or `/fix`?
- `/development:review` or `/review`?
- `/development:git` or `/git`?
- `/development:docs` or `/docs`?

Need to:
1. List actual command files in development plugin
2. Check command names in frontmatter
3. Verify how they're documented in global CLAUDE.md

### 2. Check All Plugins for Consistency

Need to audit:
- agents@local
- quant@local
- reports@local
- marketing@local
- web-development@local
- ml3t-researcher@local
- ml3t-coauthor@local
- structured-intelligence@local

### 3. Verify Actual Behavior

**Test in Claude Code**:
- Does `/status` work?
- Does `/system:status` work?
- Are they the same command?
- What about other plugins?

---

## Recommended Standard

**Recommendation**: ALWAYS use namespaced format in documentation

**Why**:
1. **Explicit**: Clear which plugin provides the command
2. **Unambiguous**: No confusion about command source
3. **Conflict-free**: Multiple plugins can have same command name
4. **Consistent**: Same pattern across all documentation

**Format**: `/plugin-name:command-name`

**Examples**:
- ✅ `/system:status` (clear)
- ✅ `/workflow:explore` (clear)
- ✅ `/content-marketing:position` (clear)
- ❌ `/status` (ambiguous - which plugin?)
- ❌ `/explore` (ambiguous)
- ❌ `/position` (ambiguous)

---

## Action Items

### Immediate
1. [ ] List all development plugin commands
2. [ ] Check how they're documented in ~/.claude/CLAUDE.md
3. [ ] Verify naming consistency across all plugins
4. [ ] Test actual command behavior in Claude Code

### Documentation Updates
1. [ ] Update all CLAUDE.md files to use namespaced format
2. [ ] Update plugin README.md files to show namespaced format
3. [ ] Ensure marketplace.json descriptions use namespaced format

### Plugin Standards
1. [ ] Document namespacing convention in plugin development guide
2. [ ] Add to plugin audit checklist
3. [ ] Verify all 13 plugins follow convention

---

## Expected Findings

**Likely issues**:
1. Global CLAUDE.md may show both `/analyze` and `/development:analyze`
2. Content-marketing CLAUDE.md may be inconsistent
3. Plugin READMEs may use shortcut notation
4. Command examples in various docs may be inconsistent

**Resolution**: Standardize on namespaced format everywhere

---

## Next Steps

1. Complete command audit across all 13 plugins
2. Document actual naming in comprehensive table
3. Identify inconsistencies
4. Create fix plan
5. Update all documentation to use namespaced format

---

**Status**: Investigation started, audit incomplete
**Priority**: Medium (documentation consistency)
**Impact**: User confusion about correct command syntax
