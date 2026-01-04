# Migrating Active Agents to Updated Plugins

This guide helps update active agents to use the latest plugin versions after the January 2026 plugin consolidation.

## What Changed

### Writing-Skills Consolidation (v2.0.0)

**Before** (10 skills, 123KB):
- pyramid-principle, scqa-framework, topic-sentence-method
- excellent-writing, plain-language, information-mapping
- seo-copywriting, concise-web-copy, search-intent-alignment
- diataxis-framework

**After** (3 skills, 21KB - 83% reduction):
- `structured-writing` - Combines pyramid, SCQA, topic-sentence frameworks
- `clear-writing` - Combines excellent-writing, plain-language, information-mapping
- `diataxis-framework` - Unchanged

**SEO skills moved** to content-marketing plugin:
- seo-copywriting, concise-web-copy, search-intent-alignment

### Command Compression (87% reduction)

All core plugin commands compressed from ~58k tokens to ~5.5k tokens total.

## Update Checklist

For each active agent/project:

- [ ] Close Claude Code session
- [ ] Clear plugin cache: `rm -rf ~/.claude/plugins/cache/`
- [ ] Verify `.claude/settings.json` has correct plugins enabled
- [ ] Restart Claude Code
- [ ] Verify with `/context` that correct versions load

## Per-Agent Instructions

### ML4T Agents

**Researcher** (`~/ml4t/agents/researcher/`)

Current config should have:
```json
{
  "enabledPlugins": {
    "system@local": true,
    "workflow@local": true,
    "memory@local": true,
    "development@local": true,
    "ml3t-researcher@local": true
  }
}
```

No changes needed - researcher doesn't use writing-skills.

**Coauthor** (`~/ml4t/agents/coauthor/`)

Current config should have:
```json
{
  "enabledPlugins": {
    "system@local": true,
    "workflow@local": true,
    "memory@local": true,
    "development@local": true,
    "ml3t-coauthor@local": true,
    "writing-skills@local": true  // Optional but recommended
  }
}
```

**Action**: If using writing-skills, clear cache to get v2.0.0 with consolidated skills.

### ML4T Main Project (`~/ml4t/`)

```json
{
  "enabledPlugins": {
    "system@local": true,
    "workflow@local": true,
    "memory@local": true,
    "development@local": true,
    "quant@local": true,
    "transition@local": true
  }
}
```

No changes needed - doesn't use writing-skills.

### Content-Marketing Projects

**Before**: Required both content-marketing AND writing-skills plugins

**After**: SEO skills bundled in content-marketing; writing-skills optional

```json
{
  "enabledPlugins": {
    "system@local": true,
    "workflow@local": true,
    "memory@local": true,
    "development@local": true,
    "content-marketing@local": true
    // writing-skills@local: optional for structured/clear writing skills
  }
}
```

**Action**: Can remove writing-skills if only using SEO features.

### Wyden Projects (ml-strategies, dashboard, etc.)

Standard core plugins only:
```json
{
  "enabledPlugins": {
    "system@local": true,
    "workflow@local": true,
    "memory@local": true,
    "development@local": true
  }
}
```

No changes needed - doesn't use writing-skills.

### Factory (`~/agents/factory/`)

```json
{
  "enabledPlugins": {
    "system@local": true,
    "workflow@local": true,
    "memory@local": true,
    "development@local": true,
    "transition@local": true
  }
}
```

No changes needed - Factory builds plugins, doesn't use writing-skills.

## Verifying Updates

After clearing cache and restarting:

1. **Check plugin version**:
   ```
   /context
   ```
   Look for plugin tokens and versions loaded.

2. **Test a command**:
   ```
   /system:status
   ```
   Should run without errors.

3. **For writing-skills users**, verify skills available:
   - `structured-writing` (was pyramid + scqa + topic-sentence)
   - `clear-writing` (was excellent + plain + information)

## Troubleshooting

### "Skill not found" errors

If you see errors about missing skills (e.g., "pyramid-principle not found"):
1. Clear cache: `rm -rf ~/.claude/plugins/cache/`
2. Restart Claude Code
3. Use new consolidated skill names: `structured-writing`, `clear-writing`

### Old command behavior

If commands behave differently than expected:
1. Check if command was compressed (most were)
2. Clear cache to get latest version
3. Compressed commands produce same results with less tokens

### Mixed versions in team

If team members have different behaviors:
1. Everyone should clear cache
2. Verify same marketplace path in settings
3. Ensure git repo (~/agents/plugins) is at same commit

## Version Reference

| Plugin | Old Version | New Version | Changes |
|--------|-------------|-------------|---------|
| writing-skills | 1.1.0 | 2.0.0 | Consolidated 10→3 skills, 83% smaller |
| content-marketing | 1.3.0 | 1.3.0 | Added SEO skills from writing-skills |
| system | 1.1.0 | 1.1.0 | Commands compressed |
| workflow | 1.0.0 | 1.0.0 | Commands compressed |
| development | 1.0.0 | 1.0.0 | Commands compressed |
| memory | 1.0.0 | 1.0.0 | Commands compressed |

## Support

If issues persist after following this guide:
1. Check `~/agents/plugins/docs/UPDATING_PLUGINS.md` for detailed troubleshooting
2. Review git log for recent changes: `cd ~/agents/plugins && git log --oneline -10`
3. Verify plugin JSON is valid: `python3 -m json.tool [plugin]/plugin.json`
