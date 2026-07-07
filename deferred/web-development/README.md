# Web Development Plugin

**Version**: 1.4.0
**Author**: Stefan
**Created**: 2025-10-16

Full-stack web development plugin with intelligent agent routing for Django + Tailwind CSS projects.

## Design guidance

Design quality (anti-AI-slop aesthetic discipline) is now provided by
the Anthropic-maintained `frontend-design@claude-plugins-official`
plugin — broader auto-trigger, kept current upstream. Enable it
alongside `web-development` for any project that needs design work:

```json
"enabledPlugins": {
  "web-development@local": true,
  "frontend-design@claude-plugins-official": true
}
```

Project-specific design systems (e.g. Applied AI's "Analytical
Warmth") live in the project's `.workspace/memory/design_system.md`,
not in this plugin. The deprecated `distinctive-design` skill was
removed in v1.4.0 (2026-05-14); see
`~/applied-ai/website/.workspace/memory/design_system.md` for the
project-specific overlay pattern.

## Overview

This plugin provides specialized agents and workflow commands for full-stack web development:

- **Frontend Engineering**: Tailwind CSS + htmx + DaisyUI + Chrome DevTools verification
- **Backend Engineering**: Django + DRF + Channels + Serena semantic code navigation
- **Intelligent Routing**: Commands automatically invoke appropriate specialist agents

## Features

### Specialized Agents

1. **frontend-engineer**
   - Tailwind CSS 3.4.4 utility-first design
   - DaisyUI 4.12.2 component library
   - htmx for dynamic interactions
   - Alpine.js for reactive components
   - Chrome DevTools verification (26 tools)
   - Performance optimization (Core Web Vitals)
   - Accessibility compliance (WCAG)

2. **backend-django**
   - Django framework and ORM
   - Django REST Framework APIs
   - Django Channels WebSocket/real-time
   - Serena MCP for code navigation (70-90% token savings)
   - Database optimization
   - pytest-django testing

### Workflow Commands

1. **/web-explore** - Task analysis and agent recommendation
   - Classifies tasks (frontend, backend, full-stack, ambiguous)
   - Suggests appropriate agent(s)
   - Estimates complexity and timeline
   - Creates work unit structure

2. **/web-plan** - Implementation planning with agent assignments
   - Breaks down into specific tasks
   - Assigns agents to each task
   - Defines dependencies
   - Sets success criteria

3. **/web-next** - Intelligent task execution with agent routing
   - Loads implementation plan
   - Checks dependencies
   - Invokes appropriate specialized agent
   - Verifies success criteria
   - Updates task state

4. **/web-ship** - Comprehensive delivery verification
   - Frontend: Chrome DevTools verification
   - Backend: Test suite execution
   - Integration: End-to-end testing
   - Documentation generation
   - Deployment readiness assessment

## Installation

### 1. Add Plugin to Project

In your project's `.claude/settings.json`:

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
  }
}
```

### 2. Configure MCP Tools

For frontend work, enable Chrome DevTools:

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-context7"]
    }
  }
}
```

For backend work, enable Serena:

```json
{
  "mcpServers": {
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

**Token Optimization**: Load only needed MCPs (frontend OR backend) per project to save ~40% tokens vs loading all MCPs.

## Quick Start

### Example 1: Frontend Task (Responsive Navbar)

```bash
cd ~/ml4t/website/

# Task analysis
/web-explore "Make the navbar responsive on mobile"

# Output: "Suggests frontend-engineer agent, ~1-2 hours"

# Create implementation plan
/web-plan

# Execute tasks
/web-next  # Task 1: Mobile hamburger menu
/web-next  # Task 2: Desktop horizontal nav
/web-next  # Task 3: Chrome DevTools verification

# Deliver
/web-ship
```

### Example 2: Backend Task (REST API)

```bash
cd ~/ml4t/website/

# Task analysis
/web-explore "Create user profile API with CRUD operations"

# Output: "Suggests backend-django agent, ~3-4 hours"

# Create implementation plan
/web-plan

# Execute tasks
/web-next  # Task 1: Model and serializer
/web-next  # Task 2: ViewSet and routing
/web-next  # Task 3: Testing (pytest)
/web-next  # Task 4: API documentation

# Deliver
/web-ship
```

### Example 3: Full-Stack Feature (Real-time Notifications)

```bash
cd ~/ml4t/website/

# Task analysis
/web-explore "Add real-time notification system"

# Output: "Full-stack task, backend-django → frontend-engineer"

# Create implementation plan
/web-plan

# Backend phase
/web-next  # Task 1: Notification model
/web-next  # Task 2: WebSocket consumer
/web-next  # Task 3: REST API endpoints
/web-next  # Task 4: Backend testing
/web-next  # Task 5: API contract documentation

# Frontend phase (reads API contract from Task 5)
/web-next  # Task 6: WebSocket client (htmx)
/web-next  # Task 7: Notification UI (DaisyUI)
/web-next  # Task 8: Chrome DevTools verification

# Deliver
/web-ship
```

## How It Works

### Intelligent Agent Routing

The `/web-next` command analyzes each task and invokes the appropriate specialist:

```markdown
## Task: Implement responsive navbar

**Analysis**: Frontend-only (UI/layout/styling)
**Agent**: frontend-engineer
**MCP Tools**: Chrome DevTools, Context7

Invoking frontend-engineer agent...

[Agent executes following frontend-engineer.md guidelines]
- Uses Tailwind CSS utilities
- Implements DaisyUI components
- Verifies with Chrome DevTools
- Takes screenshots at mobile + desktop viewports
- Checks console for errors

[Verification complete]
✅ Mobile (375x667): Hamburger menu works
✅ Desktop (1920x1080): Horizontal nav works
✅ No console errors
```

### Multi-Agent Coordination

For full-stack tasks, agents hand off via documented API contracts:

```markdown
## Task 5 Complete (backend-django)

**Deliverable**: api-contract.md
**Content**:
- WebSocket URL: ws://localhost:8000/ws/notifications/
- Message format: { "type": "notification", "id": 123, ... }
- Authentication: Session required

## Task 6 Starting (frontend-engineer)

**Reads**: api-contract.md from Task 5
**Implements**: WebSocket client based on contract
**Verifies**: Chrome DevTools shows WS connection
```

## Agent Guidelines

### Frontend Engineer Critical Rules

🚨 **ALWAYS USE CHROME DEVTOOLS TO VERIFY**

Before marking ANY task complete:
1. Take screenshot (visual verification)
2. Check console for errors
3. Test responsive behavior (mobile + desktop)
4. Run performance trace (for user-facing features)
5. Check network requests (AJAX/API calls)

### Backend Django Critical Rules

🚨 **USE SERENA FOR CODE NAVIGATION**

Before reading files or calling methods:
1. Use `find_symbol()` to locate classes/functions
2. Cite line numbers for all code references
3. Only call methods verified via Serena

🚨 **ALWAYS WRITE TESTS**

Before marking ANY API task complete:
1. Unit tests for models and business logic
2. API tests for all endpoints (CRUD)
3. Test authentication/authorization
4. Test validation and error cases
5. Run tests and verify they pass

## Tech Stack Supported

**Frontend**:
- Tailwind CSS 3.4.4 (utility-first)
- DaisyUI 4.12.2 (component library)
- htmx (declarative AJAX)
- Alpine.js (lightweight reactivity)
- Django templates (server-side rendering)
- Vanilla JavaScript (ES6+)

**Backend**:
- Django (framework)
- Django REST Framework (APIs)
- Django Channels (WebSocket/real-time)
- PostgreSQL (production) / SQLite (dev)
- Redis (channel layer for WebSocket)
- pytest-django (testing)

## MCP Tools Integration

**Frontend**: Chrome DevTools MCP (26 tools)
- Navigation, screenshots, snapshots
- Console monitoring, network inspection
- Performance analysis (Core Web Vitals + AI insights)
- Responsive testing, interaction simulation

**Backend**: Serena MCP (semantic code navigation)
- 70-90% token reduction vs grep/read
- Semantic understanding (not text search)
- Precise symbol manipulation
- `find_symbol()`, `get_symbols_overview()`, `replace_symbol_body()`

**Both**: Context7 MCP (documentation)
- Up-to-date library docs (Tailwind, Django, DRF, htmx)
- `resolve-library-id()` → `get-library-docs()`

## Memory Patterns

Shared knowledge base for common patterns:

**tailwind-htmx-patterns.md** (10+ patterns):
- Dynamic content loading
- Form submission with AJAX
- Real-time updates (polling)
- Infinite scroll
- Modal dialogs
- Search with debouncing
- Delete confirmation
- Loading states
- Optimistic updates
- File upload

**django-drf-patterns.md** (10+ patterns):
- Model-Serializer-ViewSet trio
- Custom permissions
- Nested serializers
- Pagination strategies
- Filtering and search
- Bulk operations
- File upload
- API versioning
- Documentation (drf-spectacular)
- Rate limiting

## File Structure

```
~/agents/plugins/web-development/
├── .claude-plugin/
│   ├── plugin.json              # Plugin manifest
│   ├── commands/                # Workflow commands
│   │   ├── web-explore.md       # Task analysis + routing
│   │   ├── web-plan.md          # Implementation planning
│   │   ├── web-next.md          # Task execution + agent routing
│   │   └── web-ship.md          # Delivery + verification
│   ├── agents/                  # Specialized agents
│   │   ├── frontend-engineer.md # Tailwind + htmx + Chrome DevTools
│   │   └── backend-django.md    # Django + DRF + Channels + Serena
│   └── memory/                  # Shared patterns
│       ├── tailwind-htmx-patterns.md
│       └── django-drf-patterns.md
└── README.md                    # This file
```

## Success Criteria

**Frontend Delivery**:
- [ ] Visual appearance correct (screenshot proof)
- [ ] No console errors (Chrome DevTools proof)
- [ ] Responsive on mobile and desktop (screenshot proof)
- [ ] Performance acceptable (LCP < 2.5s if user-facing)
- [ ] Accessibility compliant (semantic HTML, ARIA labels)
- [ ] htmx AJAX calls work (network request proof)

**Backend Delivery**:
- [ ] All tests pass (pytest output)
- [ ] Coverage >80%
- [ ] API documented (OpenAPI/Swagger)
- [ ] Security reviewed (CSRF, CORS, auth, permissions)
- [ ] Performance acceptable (no N+1 queries)
- [ ] All endpoints verified via tests

**Integration Delivery** (Full-Stack):
- [ ] Backend tests pass
- [ ] Frontend Chrome DevTools verification complete
- [ ] End-to-end integration test successful
- [ ] API contract documented and followed
- [ ] No console or server errors

## Philosophy

**Build for Real Users**:
- Mobile-first (most traffic is mobile)
- Performance matters (slow sites lose users)
- Accessibility is not optional
- Progressive enhancement (works without JS)

**Simplicity Over Complexity**:
- htmx before React (unless React truly needed)
- Tailwind utilities before custom CSS
- DaisyUI components before custom components
- Server-side rendering before SPA

**Evidence-Based Development**:
- Screenshots prove it works
- Performance traces prove it's fast
- Console logs prove no errors
- Test output proves correctness

**Never Say "Looks Good" Without Evidence.**

## Version History

- **1.0.0** (2025-10-16): Initial release
  - frontend-engineer agent (Tailwind + htmx + Chrome DevTools)
  - backend-django agent (Django + DRF + Channels + Serena)
  - 4 workflow commands (explore, plan, next, ship)
  - 2 pattern libraries (tailwind-htmx, django-drf)
  - Intelligent agent routing
  - MCP tool integration

## License

MIT License - See LICENSE file for details

---

*Web Development Plugin - Full-Stack Development with Intelligent Agent Routing*
*Version 1.0.0*
