# Web Development Plugin - Enabled Projects

**Plugin Version**: 1.0.0
**Enabled**: 2025-10-16

## Projects with Plugin Enabled

### 1. ML4T Website
**Path**: `~/ml4t/website/`
**Settings**: `.claude/settings.json`
**Stack**:
- Django (backend)
- Tailwind CSS 3.4.4 (frontend)
- DaisyUI 4.12.2 (components)
- htmx (interactions)

**Available Commands**:
```bash
cd ~/ml4t/website/
/web-explore "Your task"
/web-plan
/web-next
/web-ship
```

**MCP Tools**:
- ✅ Chrome DevTools (frontend verification)
- ✅ Serena (backend code navigation)
- ✅ Context7 (documentation)

---

### 2. Applied AI Website
**Path**: `~/applied-ai/website/`
**Settings**: `.claude/settings.json`
**Stack**:
- Django (backend)
- Tailwind CSS (frontend)
- htmx (interactions)

**Available Commands**:
```bash
cd ~/applied-ai/website/
/web-explore "Your task"
/web-plan
/web-next
/web-ship
```

**MCP Tools**:
- ✅ Chrome DevTools (frontend verification)
- ✅ Serena (backend code navigation)
- ✅ Context7 (documentation)

---

## Quick Start

### Try Your First Task

**ML4T Website**:
```bash
cd ~/ml4t/website/
/web-explore "Make the navbar responsive on mobile devices"
```

**Applied AI Website**:
```bash
cd ~/applied-ai/website/
/web-explore "Add a search feature to the blog posts"
```

### Workflow

1. **Explore**: `/web-explore "task description"`
   - Analyzes task complexity
   - Suggests appropriate agent (frontend vs backend)
   - Estimates timeline

2. **Plan**: `/web-plan`
   - Breaks down into specific tasks
   - Assigns agents to each task
   - Defines success criteria

3. **Execute**: `/web-next` (repeat until all tasks complete)
   - Invokes appropriate specialized agent
   - Executes with verification
   - Updates task state

4. **Ship**: `/web-ship`
   - Final verification (Chrome DevTools + tests)
   - Generates delivery documentation
   - Deployment readiness check

### Agent Routing

The commands automatically invoke the right specialist:

**Frontend Tasks** → `frontend-engineer` agent:
- Tailwind CSS layouts
- htmx interactions
- DaisyUI components
- Chrome DevTools verification
- Responsive design
- Performance optimization

**Backend Tasks** → `backend-django` agent:
- Django models and migrations
- DRF REST APIs
- Django Channels WebSocket
- Serena code navigation
- pytest testing
- API documentation

**Full-Stack Tasks** → Both agents sequentially:
- Backend creates API + documents contract
- Frontend reads contract + implements client
- Integration verification

## Settings Details

Both projects have identical settings:

```json
{
  "extraKnownMarketplaces": {
    "stefan-plugins": {
      "source": {
        "source": "directory",
        "path": "~/path/to/coding-agent-plugins"
      }
    }
  },
  "enabledPlugins": {
    "web-development@stefan-plugins": true
  },
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    },
    "serena": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-serena"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-context7"]
    }
  }
}
```

## Next Steps

1. **Start Claude Code** in either project directory
2. **Try a simple task** (e.g., responsive navbar)
3. **Observe the workflow** (explore → plan → next → ship)
4. **Review verification** (screenshots, tests, performance)
5. **Use for real work** and provide feedback

## Troubleshooting

**Commands not showing?**
- Restart Claude Code after adding settings.json
- Verify settings.json is valid JSON
- Check plugin path in settings matches actual location

**MCP tools not loading?**
- Wait for session start to complete
- Check ~/.claude/settings.json for global MCP conflicts
- Verify npx can access the MCP packages

**Agent not verifying with Chrome DevTools?**
- Ensure chrome-devtools MCP is in settings.json
- Check browser is accessible
- Try navigating to localhost manually first

## Resources

**Plugin Documentation**:
- `~/agents/plugins/web-development/README.md` - Complete reference
- `~/agents/plugins/web-development/QUICK_START.md` - Quick start guide
- `~/agents/plugins/web-development/PLUGIN_SUMMARY.md` - Creation summary

**Pattern Libraries**:
- `~/agents/plugins/web-development/.claude-plugin/memory/tailwind-htmx-patterns.md` - 10 frontend patterns
- `~/agents/plugins/web-development/.claude-plugin/memory/django-drf-patterns.md` - 10 backend patterns

**Agent Guidelines**:
- `~/agents/plugins/web-development/.claude-plugin/agents/frontend-engineer.md` - Frontend agent
- `~/agents/plugins/web-development/.claude-plugin/agents/backend-django.md` - Backend agent

---

*Web Development Plugin - Ready for use in both projects!*
*Version 1.0.0 - Enabled 2025-10-16*
