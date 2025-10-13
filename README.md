# Stefan's Claude Code Plugins

**Type**: Claude Code Plugin Marketplace
**Purpose**: Personal plugin library for AI-assisted development
**Created**: 2025-10-13

## Overview

This is a plugin marketplace for Claude Code, containing modular plugins for various development workflows and domains.

## Plugin Categories

### Core Plugins
- **core** - Universal utilities (cleanup, docs, status, etc.)
- **memory** - Memory management and knowledge persistence
- **workflow** - Task workflow (explore, plan, next, ship)

### Development Plugins
- **development** - Development tools (analyze, review, test, fix)
- **git** - Git operations and version control

### Domain Plugins
- **ml3t/** - ML for Trading infrastructure
  - **researcher** - Academic research with paper search and citations
  - **coauthor** - Book co-authoring assistance
- **quant** - Quantitative finance workflows
- **reports** - Report generation tools

## Usage

### Install Marketplace

In your project's `.claude/settings.json`:

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
    "core@stefan-plugins": true,
    "workflow@stefan-plugins": true,
    "development@stefan-plugins": true
  }
}
```

### Browse Plugins

```bash
/plugin list
/plugin
```

### Enable/Disable Plugins

Use the interactive `/plugin` menu or edit `settings.json`.

## Plugin Structure

Each plugin follows the official Claude Code plugin structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json        # Required manifest
├── commands/              # Slash commands (optional)
├── agents/                # Specialized agents (optional)
├── hooks/                 # Event handlers (optional)
└── .mcp.json             # MCP servers (optional)
```

## Development

Plugins are developed in the Factory workspace (`~/agents/factory/.claude/work/`) and published here when ready.

## Versioning

All plugins use semantic versioning (MAJOR.MINOR.PATCH):
- Git tags: `plugin-name-vX.Y.Z`
- Breaking changes increment MAJOR version
- New features increment MINOR version
- Bug fixes increment PATCH version

## References

- [Claude Code Plugin Documentation](https://docs.claude.com/claude-code/plugins)
- [Factory Development Workspace](https://github.com/stefan-jansen/factory)

---

**Maintained by**: Stefan
**Last Updated**: 2025-10-13
