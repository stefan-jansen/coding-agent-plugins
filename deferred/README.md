# deferred/

Plugins that ship in the repo but are **not registered in the top-level marketplace** for v1. Each is functional but narrow enough that v1 doesn't include them by default.

To use one, register it as its own marketplace source in a project's `.claude/settings.json`, e.g.:

```json
{
  "extraKnownMarketplaces": {
    "content-marketing": {
      "source": {
        "source": "directory",
        "path": "~/path/to/coding-agent-plugins/deferred/content-marketing"
      }
    }
  },
  "enabledPlugins": {
    "content-marketing@content-marketing": true
  }
}
```

Or copy the plugin directory into your project's `.claude/plugins/`.

## What's here

| Plugin | Description | Deferred because |
|---|---|---|
| `quant` | Quantitative finance / ML strategy scaffolding | Imports private `ml4t.*` packages; not usable without them |
| `references` | Academic reference management (Zotero + MCP) | Needs `ml4t_refs.db` and a private MCP server |
| `reports` | Stakeholder report generation | Single-command; narrow use case |
| `content-marketing` | Editorial workflow for technical B2B | Highly opinionated editorial process |
| `writing-skills` | Shared writing methodology library | Companion to content-marketing |
| `web-development` | Django + Tailwind full-stack scaffolding | Framework-opinionated; needs generalizing |
| `diagrams` | D2 diagram generation | Thin; single skill |

These may graduate back to the top-level manifest as they get generalized or de-coupled from private dependencies.
