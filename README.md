# coding-agent-plugins

Plugin marketplace for [coding-agent-toolkit](https://github.com/stefan-jansen/coding-agent-toolkit).

Provides a small set of workflow, memory, and code-quality plugins that a Claude Code project can enable via `.claude/settings.json`. Each plugin is a directory with a `plugin.json` and its own README documenting the skills/commands it ships.

## Getting started

### 1. Clone the marketplace

```bash
git clone git@github.com:stefan-jansen/coding-agent-plugins.git ~/path/to/coding-agent-plugins
```

### 2. Register it and enable plugins in a project

Add to that project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "local": {
      "source": {
        "source": "directory",
        "path": "~/path/to/coding-agent-plugins"
      }
    }
  },
  "enabledPlugins": {
    "workflow@local": true,
    "memory@local": true,
    "transition@local": true,
    "development@local": true,
    "system@local": true
  }
}
```

### 3. Restart Claude Code

Plugins load from cache at session start; the cache does not auto-update when marketplace source changes. Restart the session (or `Cmd/Ctrl+Shift+P → Claude Code: Restart` in VS Code) after enabling or editing plugins.

## Plugins

**Foundation** — generic infrastructure most projects want:

| Plugin | Ships | Description |
|---|---|---|
| `workflow` | `/align` `/plan-issues` `/next-issue` `/ship` `/explore` `/plan` `/next` `/work` | Structured task execution — spec → issues → implement → deliver |
| `memory` | `/memory-gc` `/memory-review` `/memory-index` `/handoff` `/continue` | Persistent project memory + session handoffs |
| `transition` | SessionStart / SessionEnd hooks | Auto-create hourly `.workspace/transitions/YYYY-MM-DD/HH.md` progress files |
| `development` | `/analyze` `/review` `/test` `/fix` `/git` `/docs` | Code analysis, review, TDD, debugging |
| `system` | `/audit` `/cleanup` `/status` | Framework health, cleanup, unified status view |
| `setup` | `/setup` `/setup:user` | Project initialization (interview-driven) + global user config — enable once, disable after |
| `codex` | `/codex:*` commands | Delegate work to OpenAI Codex from Claude Code |
| `roborev` | SessionStart summary | Open roborev review status for the current branch |

**Extras** — additional plugins registered in the manifest:

| Plugin | Description |
|---|---|
| `observer` | Cross-session memory via batched `claude -p` observation processing |

Every plugin directory has its own README with skill/command details.

## Deferred plugins

More opinionated / narrower plugins live in [`deferred/`](./deferred/) and are **not** in the top-level manifest. They're functional but need generalizing or de-coupling from private dependencies before shipping in v1. See [`deferred/README.md`](./deferred/README.md) for the list and how to enable them individually.

## Per-project selection

Enable plugins on a per-project basis in `.claude/settings.json`. A typical setup:

```json
{
  "enabledPlugins": {
    "workflow@local": true,
    "memory@local": true,
    "transition@local": true,
    "development@local": true,
    "system@local": true
  }
}
```

For a project that also does content work:

```json
{
  "enabledPlugins": {
    "workflow@local": true,
    "memory@local": true,
    "transition@local": true,
    "development@local": true,
    "content-marketing@local": true,
    "writing-skills@local": true
  }
}
```

## Troubleshooting

**Commands not appearing after enabling a plugin.** Restart Claude Code. Plugins are cached at session start.

**Wrong plugin version loaded.** Delete `~/.claude/plugins/cache/local/<plugin>/` and restart.

**Marketplace not found.** Verify the `path` in `extraKnownMarketplaces` points at the directory containing `.claude-plugin/marketplace.json` (i.e., the repo root of this clone).

## License

MIT
