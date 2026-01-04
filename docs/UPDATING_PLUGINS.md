# Updating Plugins

This guide explains how Claude Code plugin caching works and how to update plugins when changes are made to the marketplace.

## How Plugin Caching Works

Claude Code caches plugins at installation time to ensure consistent behavior during sessions:

```
~/.claude/plugins/
├── cache/
│   └── local/              # Cached plugin contents
│       ├── system/1.1.0/
│       ├── workflow/1.0.0/
│       └── ...
├── installed_plugins.json  # Plugin registry
└── known_marketplaces.json # Marketplace config
```

**Key behavior**:
- Plugins load from cache at session start
- Cache does NOT auto-update when source changes
- Sessions must restart for changes to take effect

## When to Update Plugins

Update plugins when:
- Plugin versions change in the marketplace
- Commands or skills are added/modified
- You see unexpected behavior from old cached content

**Signs of stale cache**:
- Command behavior doesn't match documentation
- Missing new features
- `/context` shows old plugin versions

## How to Update Plugins

### Step 1: Clear the Plugin Cache

```bash
rm -rf ~/.claude/plugins/cache/
```

This removes all cached plugins. The cache rebuilds automatically on next session start.

### Step 2: Restart Claude Code

Close and reopen Claude Code. On startup:
1. Reads `.claude/settings.json` for enabled plugins
2. Rebuilds cache from current marketplace source
3. Loads fresh plugin versions

### Step 3: Verify Update

Check that new versions loaded:

```bash
# Compare source version
cat ~/agents/plugins/[plugin]/.claude-plugin/plugin.json | jq .version

# Check in session with /context
```

## Selective Cache Clearing

To update only specific plugins:

```bash
# Clear single plugin
rm -rf ~/.claude/plugins/cache/local/[plugin-name]/

# Clear multiple plugins
rm -rf ~/.claude/plugins/cache/local/{system,workflow,development}/
```

## Troubleshooting

### Plugin Not Loading

1. Check `.claude/settings.json` enables the plugin:
   ```json
   "enabledPlugins": {
     "plugin-name@local": true
   }
   ```

2. Verify marketplace config:
   ```json
   "extraKnownMarketplaces": {
     "local": {
       "source": { "source": "directory", "path": "/home/stefan/agents/plugins" }
     }
   }
   ```

3. Clear cache and restart

### Wrong Version Loading

1. Check source version:
   ```bash
   cat ~/agents/plugins/[plugin]/.claude-plugin/plugin.json | jq .version
   ```

2. Check cached version:
   ```bash
   ls ~/.claude/plugins/cache/local/[plugin]/
   ```

3. If mismatch, clear cache

### Cache Not Rebuilding

If cache doesn't rebuild after clearing:
1. Verify plugin manifest is valid JSON
2. Check marketplace path is correct
3. Look for errors in Claude Code startup

## Best Practices

1. **After marketplace updates**: Clear cache before testing
2. **Development workflow**: Clear cache when iterating on plugin changes
3. **Production use**: Document which plugin version is expected
4. **Team coordination**: Communicate when breaking changes are made

## Version History

- **2026-01-04**: Initial documentation
- Based on plugin cache investigation showing stale `writing-skills@1.1.0` vs source `@2.0.0`
