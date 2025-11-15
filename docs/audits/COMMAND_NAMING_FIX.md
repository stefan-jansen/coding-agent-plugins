# Command Naming Standardization - Fix Required

**Date**: 2025-11-01
**Issue**: Inconsistent command naming (namespaced vs non-namespaced)
**Impact**: User confusion about correct syntax

---

## Problem Identified

### Current State: Inconsistent Documentation

**Global CLAUDE.md** (`~/.claude/CLAUDE.md`):
```markdown
- `/analyze` - Deep codebase analysis
- `/test` - Run tests or create TDD workflow
- `/fix` - Debug errors and apply fixes
- `/review` - Code review and quality analysis
- `/status` - Current project and task status
```

**Content-Marketing CLAUDE.md**:
```markdown
/content-marketing:position
/content-marketing:research
/content-marketing:outline
/content-marketing:draft
/content-marketing:review
```

**Inconsistency**: Some docs show `/command`, others show `/plugin:command`

---

## How Claude Code Actually Works

**Plugin Command Registration**:
When a plugin is loaded via `.claude/settings.json`:
```json
{
  "enabledPlugins": {
    "system@local": true,
    "development@local": true
  }
}
```

Claude Code registers commands as: `/plugin-name:command-name`

**Examples**:
- Plugin: `system`, Command file: `status.md` → `/system:status`
- Plugin: `development`, Command file: `analyze.md` → `/development:analyze`
- Plugin: `content-marketing`, Command file: `position.md` → `/content-marketing:position`

**Shortcuts** (may work, but not guaranteed):
Claude Code MAY allow `/status` as shortcut for `/system:status` if no conflicts exist, but this is:
- ❌ Undocumented behavior
- ❌ Could break if another plugin adds same command name
- ❌ Creates ambiguity

---

## Audit Results

### Plugins Using Namespaced Format ✅

**content-marketing@local**: Consistently uses `/content-marketing:command`
- `/content-marketing:position`
- `/content-marketing:research`
- `/content-marketing:outline`
- `/content-marketing:draft`
- `/content-marketing:review`

### Plugins Using Non-Namespaced Format ❌

**Global CLAUDE.md documents these WITHOUT namespace**:
- `/analyze` (should be `/development:analyze`)
- `/test` (should be `/development:test`)
- `/fix` (should be `/development:fix`)
- `/review` (should be `/development:review`)
- `/status` (should be `/system:status`)
- `/audit` (should be `/system:audit`)
- `/cleanup` (should be `/system:cleanup`)
- `/setup` (should be `/system:setup`)
- `/explore` (should be `/workflow:explore`)
- `/plan` (should be `/workflow:plan`)
- `/next` (should be `/workflow:next`)
- `/ship` (should be `/workflow:ship`)
- `/index` (should be `/memory:index`)
- `/handoff` (should be `/memory:handoff`)

---

## Why This Matters

### 1. User Confusion
**Problem**: User sees `/status` in docs, types `/status`, may or may not work
**Correct**: Document as `/system:status` (explicit, guaranteed to work)

### 2. Plugin Conflicts
**Scenario**: Two plugins both have `status.md` command
- Plugin A: `system/commands/status.md`
- Plugin B: `monitoring/commands/status.md`

**Without namespace**: `/status` is ambiguous - which one runs?
**With namespace**:
- `/system:status` (clear)
- `/monitoring:status` (clear)

### 3. Documentation Accuracy
**Problem**: Docs showing `/analyze` when actual command is `/development:analyze`
**Impact**: Users type wrong command, get "command not found"

---

## Recommended Standard

### Universal Rule: ALWAYS Use Namespaced Format

**Documentation**: `/plugin-name:command-name`
**Examples**: `/system:status`, `/workflow:explore`, `/content-marketing:position`

**Why**:
1. ✅ Explicit (clear which plugin provides command)
2. ✅ Unambiguous (no conflicts possible)
3. ✅ Consistent (same pattern everywhere)
4. ✅ Guaranteed to work (official syntax)
5. ✅ Maintainable (adding new plugins won't break docs)

---

## Required Fixes

### 1. Global CLAUDE.md (~/.claude/CLAUDE.md)

**Section: Framework Commands**

**Current** (lines 154-170):
```markdown
- `/explore` - Analyze requirements and create work breakdown
- `/plan` - Create implementation plan with dependencies
- `/next` - Execute next available task
- `/ship` - Deliver completed work

### Development (5) - MCP Enhanced
- `/analyze` - Deep codebase analysis (70-90% faster with Serena)
- `/test` - Run tests or create TDD workflow
- `/fix` - Debug errors and apply fixes (semantic with Serena)
- `/run` - Execute scripts with monitoring
- `/review` - Code review and quality analysis
```

**Should be**:
```markdown
- `/workflow:explore` - Analyze requirements and create work breakdown
- `/workflow:plan` - Create implementation plan with dependencies
- `/workflow:next` - Execute next available task
- `/workflow:ship` - Deliver completed work

### Development (6) - MCP Enhanced
- `/development:analyze` - Deep codebase analysis (70-90% faster with Serena)
- `/development:test` - Run tests or create TDD workflow
- `/development:fix` - Debug errors and apply fixes (semantic with Serena)
- `/development:run` - Execute scripts with monitoring
- `/development:review` - Code review and quality analysis
- `/development:git` - Git operations (commit, pr, issue)
```

**Section: Project Management** (line 188):
```markdown
- `/status` - Current project and task status
```

**Should be**:
```markdown
- `/system:status` - Current project and task status
```

**Section: Git & Documentation** (line 167-168):
```markdown
- `/git` - Unified git operations (commit, pr, issue)
- `/docs` - Documentation operations (fetch, search, update)
```

**Should be**:
```markdown
- `/development:git` - Unified git operations (commit, pr, issue)
- `/development:docs` - Documentation operations (fetch, search, update)
```

**Section: Quality & Configuration** (line 170-172):
```markdown
- `/audit` - Framework compliance and setup validation
- `/agent` - Invoke specialized agents
- `/config` - Manage settings and preferences
```

**Should be**:
```markdown
- `/system:audit` - Framework compliance and setup validation
- `/agents:agent` - Invoke specialized agents
- `/system:config` - Manage settings and preferences
```

**Section: Session Management** (line 193-194):
```markdown
- `/context` - Display token usage across all components (built-in)
- `/handoff` - Create transition documents with context analysis
```

**Should be**:
```markdown
- `/context` - Display token usage across all components (built-in Claude Code)
- `/memory:handoff` - Create transition documents with context analysis
```

### 2. Content-Marketing CLAUDE.md

**Already correct** ✅ - uses namespaced format throughout

### 3. Plugin README Files

Each plugin's README.md should document commands with namespace:

**Example** (system plugin):
```markdown
## Commands

- `/system:status` - View work, system, and memory state
- `/system:audit` - Validate framework setup
- `/system:cleanup` - Clean up generated clutter
- `/system:setup` - Initialize new projects
```

### 4. Plugin Marketplace (marketplace.json)

Already correct - describes plugins, not individual commands

---

## Implementation Plan

### Phase 1: Update Global CLAUDE.md ✅ High Priority

**File**: `~/.claude/CLAUDE.md`
**Lines to change**: ~30 command references
**Impact**: All users see correct syntax

**Changes**:
1. Workflow commands: Add `workflow:` prefix
2. Development commands: Add `development:` prefix
3. System commands: Add `system:` prefix
4. Memory commands: Add `memory:` prefix
5. Agent commands: Add `agents:` prefix

### Phase 2: Update Plugin READMEs ⚠️ Medium Priority

**Files**: `~/agents/plugins/*/README.md`
**Count**: 13 plugins
**Impact**: Plugin documentation clarity

**For each plugin**:
1. Check README.md exists
2. Verify command documentation format
3. Update to namespaced format if needed

### Phase 3: Audit Command Files ℹ️ Low Priority

**Files**: `~/agents/plugins/*/commands/*.md`
**Check**: Command examples within command files use namespace

**Note**: This is cosmetic - the command files themselves work correctly, but examples within them should show namespaced format.

---

## Testing After Fix

**Verify these work**:
```bash
/system:status
/workflow:explore "test"
/development:analyze
/memory:handoff
/content-marketing:position "test"
```

**Verify these DON'T work (or give deprecation warning)**:
```bash
/status
/explore
/analyze
```

**If shortcuts still work**: Document them as aliases but discourage use

---

## Long-term Standard

### Plugin Development Guidelines

**When creating new plugin commands**:

1. ✅ Command will be invoked as: `/plugin-name:command-name`
2. ✅ Document it that way in all examples
3. ✅ Never show non-namespaced version
4. ✅ Plugin name should be descriptive but concise

**Command naming best practices**:
- Use descriptive names: `analyze`, `review`, `cleanup`
- Use verb-first: `/workflow:explore`, not `/workflow:exploration`
- Keep plugin names short: `system`, not `system-utilities`

---

## Recommendation

**Immediate action**: Fix global CLAUDE.md command references

**Why urgent**:
- Most referenced documentation file
- Used by all projects
- Inconsistent with content-marketing (which is correct)
- User confusion (this issue)

**Estimated time**: 20-30 minutes
**Risk**: Low (just documentation, doesn't change actual functionality)
**Benefit**: Consistent, accurate command documentation across entire framework

---

**Next Steps**:
1. Update ~/.claude/CLAUDE.md with namespaced format
2. Test commands still work after reference change
3. Update plugin READMEs as time permits
4. Document standard for future plugin development
