# Plugin Format Fix - Wildcard Issue

**Date**: 2025-10-31
**Issue**: Claude Code doesn't support wildcard patterns in plugin.json
**Plugins Fixed**: 3 (web-development, reports, quant)

---

## The Problem

Claude Code's plugin system expects **explicit file paths**, not wildcard patterns.

### What Doesn't Work

```json
{
  "commands": [
    "./commands/*.md"  // ❌ Not supported
  ],
  "agents": {
    "agent-name": {    // ❌ Not supported (object format)
      "description": "...",
      "metadata": "..."
    }
  }
}
```

### What Works

```json
{
  "commands": [
    "./commands/command1.md",  // ✅ Explicit paths
    "./commands/command2.md",
    "./commands/command3.md"
  ],
  "agents": [
    "./agents/agent1.md",      // ✅ Simple array
    "./agents/agent2.md"
  ]
}
```

---

## Plugins Fixed

### 1. web-development (v1.1.1)

**Before**:
```json
"commands": ["./commands/*.md"]
```

**After**:
```json
"commands": [
  "./commands/web-explore.md",
  "./commands/web-plan.md",
  "./commands/web-next.md",
  "./commands/web-ship.md"
],
"agents": [
  "./agents/frontend-engineer.md",
  "./agents/backend-django.md"
]
```

### 2. reports (v1.0.0)

**Before**:
```json
"commands": ["./commands/*.md"],
"agents": {
  "report-generator": {
    "description": "...",
    "notebook_support": true
  }
}
```

**After**:
```json
"commands": [
  "./commands/report.md"
],
"agents": [
  "./agents/report-generator.md"
]
```

### 3. quant (v1.0.0)

**Before**:
```json
"commands": ["./commands/*.md"],
"agents": {
  "quant-ml-validator": { "description": "..." },
  "quant-backtest-validator": { "description": "..." },
  "quant-risk-validator": { "description": "..." },
  "data-scientist": { "description": "..." }
}
```

**After**:
```json
"commands": [
  "./commands/quant-explore.md",
  "./commands/quant-plan.md",
  "./commands/quant-next.md",
  "./commands/quant-ship.md",
  "./commands/experiment.md",
  "./commands/evaluate.md"
],
"agents": [
  "./agents/quant-ml-validator.md",
  "./agents/quant-backtest-validator.md",
  "./agents/quant-risk-validator.md",
  "./agents/data-scientist.md"
]
```

---

## Claude Code Plugin Format Requirements

Based on fixes and official plugins:

### Required Format

```json
{
  "name": "plugin-name",
  "version": "1.0.0",
  "description": "Plugin description",
  "author": {
    "name": "Author Name"  // Must be object, not string
  },
  "commands": [
    "./commands/file1.md",  // Explicit paths only
    "./commands/file2.md"
  ],
  "agents": [
    "./agents/agent1.md",   // Simple array of paths
    "./agents/agent2.md"
  ]
}
```

### Optional Fields

```json
{
  "keywords": ["tag1", "tag2"],
  "repository": "https://github.com/...",
  "license": "MIT"
}
```

---

## Error Messages

If you see this error:
```
✘ Plugin plugin-name from plugin-name@marketplace
commands path not found: /path/to/commands/*.md
```

**Fix**: Replace wildcard patterns with explicit file paths in plugin.json

---

## Validation Script

To check all plugins for this issue:

```bash
# Find plugins using wildcards
find ~/agents/plugins -name "plugin.json" -exec grep -l '\*\.md' {} \;

# Validate all plugin.json files
find ~/agents/plugins -name "plugin.json" -exec python3 -m json.tool {} \; > /dev/null
```

---

## Prevention

When creating new plugins:

1. **List files explicitly** - No wildcards
2. **Use simple arrays** - For both commands and agents
3. **Validate JSON** - `python3 -m json.tool plugin.json`
4. **Test loading** - Enable in a test project first

---

## References

- **Working example**: `content-marketing@local` (fixed Oct 31)
- **Claude Code docs**: https://docs.claude.com/claude-code/plugins
- **Marketplace location**: `~/agents/plugins/.claude-plugin/marketplace.json`

---

**Status**: All plugins in marketplace now use correct format
**Last checked**: 2025-10-31
