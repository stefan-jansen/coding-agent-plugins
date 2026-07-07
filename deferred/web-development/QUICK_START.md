# Web Development Plugin - Quick Start Guide

**Version**: 1.0.0

## Installation (2 minutes)

### Step 1: Enable Plugin in Project

Edit `~/ml4t/website/.claude/settings.json`:

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

### Step 2: Restart Claude Code

```bash
cd ~/ml4t/website/
# Start Claude Code in this directory
```

### Step 3: Verify Commands Available

Type `/web-` and autocomplete should show:
- `/web-explore`
- `/web-plan`
- `/web-next`
- `/web-ship`

## Your First Task (5 minutes)

Let's create a simple responsive navbar:

```bash
# 1. Analyze task
/web-explore "Add a responsive navbar - hamburger menu on mobile, horizontal nav on desktop"

# Claude analyzes and suggests: frontend-engineer agent, ~1-2 hours

# 2. Create implementation plan
/web-plan

# Claude breaks down into 3 tasks:
# - Task 1: Mobile hamburger menu
# - Task 2: Desktop horizontal nav
# - Task 3: Chrome DevTools verification

# 3. Execute tasks one by one
/web-next

# Claude invokes frontend-engineer agent
# Implements mobile hamburger menu with DaisyUI drawer
# Verifies with Chrome DevTools
# Takes screenshot proof

# Continue with next task
/web-next

# Implements desktop horizontal nav
# Verifies responsiveness
# Takes screenshot proof

# Final verification
/web-next

# Comprehensive Chrome DevTools check
# Performance trace, console errors, responsive test

# 4. Deliver completed work
/web-ship

# Claude runs final verification
# Generates delivery documentation
# Archives work unit
# Provides deployment notes
```

## Workflow Patterns

### Pattern 1: Frontend-Only

**Use When**: UI changes, styling, layout, interactive elements

```bash
/web-explore "Make the contact form use htmx for AJAX submission"
/web-plan
/web-next  # (repeat until all tasks complete)
/web-ship
```

**Agent Used**: frontend-engineer
**MCP Tools**: Chrome DevTools (verification), Context7 (Tailwind/htmx docs)
**Verification**: Screenshots, console check, network tab

### Pattern 2: Backend-Only

**Use When**: API development, database changes, business logic

```bash
/web-explore "Create REST API for blog posts with CRUD operations"
/web-plan
/web-next  # (repeat until all tasks complete)
/web-ship
```

**Agent Used**: backend-django
**MCP Tools**: Serena (code navigation), Context7 (Django/DRF docs)
**Verification**: pytest output, coverage report, API documentation

### Pattern 3: Full-Stack

**Use When**: Complete features requiring both frontend and backend

```bash
/web-explore "Add real-time comment system with WebSocket"
/web-plan

# Backend phase
/web-next  # Task 1: Comment model
/web-next  # Task 2: WebSocket consumer
/web-next  # Task 3: REST API
/web-next  # Task 4: Tests
/web-next  # Task 5: API contract documentation

# Frontend phase (reads API contract)
/web-next  # Task 6: WebSocket client (htmx)
/web-next  # Task 7: Comment UI (DaisyUI)
/web-next  # Task 8: Chrome DevTools verification

/web-ship
```

**Agents Used**: backend-django → frontend-engineer
**Coordination**: Backend documents API contract, frontend implements client
**Verification**: Backend tests + frontend Chrome DevTools + integration test

## Command Reference

### /web-explore [description]

**Purpose**: Analyze task and suggest agent

**Input**: Task description or @requirements.md
**Output**: Task analysis with agent suggestion, complexity estimate, success criteria
**Creates**: Work unit directory structure

**Example**:
```bash
/web-explore "Add pagination to blog post list"
```

**Output**:
```
Classification: Frontend-only
Agent: frontend-engineer
Complexity: Medium (~2 hours)
Tasks: Implement infinite scroll with htmx, verify with Chrome DevTools
```

### /web-plan

**Purpose**: Create detailed implementation plan

**Input**: Uses analysis from /web-explore
**Output**: Task breakdown with agent assignments, dependencies, success criteria
**Creates**: implementation-plan.md

**Example Output**:
```
Task 1: Implement htmx infinite scroll trigger
  Agent: frontend-engineer
  Time: 1 hour
  Dependencies: None

Task 2: Create Django paginated view
  Agent: backend-django
  Time: 30 min
  Dependencies: None

Task 3: Integration verification
  Agent: frontend-engineer
  Time: 30 min
  Dependencies: Tasks 1-2
```

### /web-next

**Purpose**: Execute next available task

**Input**: Reads implementation-plan.md
**Output**: Task execution with agent invocation, verification evidence
**Updates**: state.json (task status)

**Intelligent Routing**:
- Checks dependencies
- Invokes appropriate agent (frontend-engineer or backend-django)
- Executes following agent's guidelines
- Verifies success criteria
- Marks complete or reports blockers

### /web-ship

**Purpose**: Deliver completed work

**Input**: Reads all completed tasks
**Output**: Delivery summary, verification evidence, deployment notes
**Creates**: delivery-summary.md

**Verification Steps**:
1. Check all tasks complete
2. Frontend: Final Chrome DevTools check
3. Backend: Final test suite run
4. Integration: End-to-end test (if full-stack)
5. Generate delivery documentation
6. Archive work unit

## Agent Behaviors

### When frontend-engineer is Invoked

**Tech Stack**:
- Tailwind CSS (utility-first)
- DaisyUI (component library)
- htmx (declarative AJAX)
- Alpine.js (optional reactivity)

**Critical Rule**: 🚨 ALWAYS VERIFY WITH CHROME DEVTOOLS

**Process**:
1. Implement feature using Tailwind + htmx
2. Take screenshot (visual verification)
3. Check console for errors
4. Test responsive behavior (mobile + desktop)
5. Run performance trace (if user-facing)
6. Check network requests (if AJAX)
7. Document verification evidence

**Deliverables**:
- Updated templates/static files
- Screenshots (mobile.png, desktop.png)
- verification.md (Chrome DevTools report)

### When backend-django is Invoked

**Tech Stack**:
- Django (framework)
- Django REST Framework (APIs)
- Django Channels (WebSocket)
- pytest-django (testing)

**Critical Rules**:
- 🚨 USE SERENA FOR CODE NAVIGATION
- 🚨 ALWAYS WRITE TESTS

**Process**:
1. Use Serena to locate existing code
2. Implement feature (models, views, serializers)
3. Write comprehensive tests
4. Run pytest and verify all pass
5. Document API contract (if frontend integration)
6. Generate API documentation (OpenAPI)

**Deliverables**:
- Code files (models.py, views.py, serializers.py, tests.py)
- Test output (pytest --verbose)
- Coverage report
- api-contract.md (if full-stack)

## MCP Tool Usage

### Chrome DevTools (Frontend)

**Core Functions**:
```bash
navigate_page("http://localhost:8000/")
take_screenshot()                    # Visual verification
list_console_messages()               # Error checking
resize_page(375, 667)                # Mobile viewport
resize_page(1920, 1080)              # Desktop viewport
performance_start_trace(reload=true)
performance_stop_trace()             # Core Web Vitals + AI insights
list_network_requests()              # AJAX verification
```

**When to Use**:
- After any UI change (screenshot proof)
- Before marking task complete (verification)
- Performance optimization (trace analysis)
- Debugging AJAX/WebSocket (network tab)

### Serena (Backend)

**Core Functions**:
```bash
find_symbol("User", "accounts/models.py")       # Locate classes
get_symbols_overview("accounts/views.py")       # Module structure
replace_symbol_body("ProfileViewSet", ...)      # Precise editing
```

**When to Use**:
- Before reading files (locate symbols)
- Before calling methods (verify they exist)
- Refactoring code (precise symbol manipulation)

**Token Savings**: 70-90% vs grep/read for code operations

### Context7 (Both)

**Core Functions**:
```bash
resolve-library-id("tailwindcss")
get-library-docs("/tailwindlabs/tailwindcss", topic="responsive design")
```

**When to Use**:
- Looking up Tailwind utility classes
- htmx attribute reference
- Django/DRF API documentation
- DaisyUI component usage

## Common Issues

### Issue: Commands not showing

**Solution**: Check settings.json has plugin enabled:
```json
{
  "enabledPlugins": {
    "web-development@stefan-plugins": true
  }
}
```

### Issue: Agent not invoking Chrome DevTools

**Solution**: Enable chrome-devtools MCP in settings.json:
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

### Issue: Serena not finding symbols

**Solution**:
1. Activate project: `activate_project("~/ml4t/website/")`
2. Wait for indexing to complete
3. Use correct file paths (relative to project root)

### Issue: Task dependencies blocking

**Solution**: Complete prerequisite tasks first
```bash
# Can't execute Task 3 (depends on Tasks 1-2)
# Must complete Task 1 and Task 2 first
/web-next  # Completes Task 1
/web-next  # Completes Task 2
/web-next  # Now Task 3 can execute
```

## Tips & Best Practices

1. **Start with /web-explore**: Always analyze first, don't jump to coding
2. **Read the plan**: Review /web-plan output before executing
3. **One task at a time**: Don't skip ahead, follow dependencies
4. **Trust verification**: Screenshots and tests are evidence, not optional
5. **Document as you go**: API contracts and notes help future tasks
6. **Archive when done**: /web-ship creates permanent record

## Next Steps

1. **Try simple task**: Responsive navbar (this guide)
2. **Try backend task**: Simple REST API
3. **Try full-stack**: Real-time feature with WebSocket
4. **Review patterns**: Read memory/tailwind-htmx-patterns.md and django-drf-patterns.md
5. **Customize**: Adjust agent guidelines for your specific stack

## Getting Help

**Review Documentation**:
- README.md - Full plugin documentation
- agents/frontend-engineer.md - Frontend agent guidelines
- agents/backend-django.md - Backend agent guidelines
- memory/tailwind-htmx-patterns.md - Frontend patterns
- memory/django-drf-patterns.md - Backend patterns

**Check Work Units**:
```bash
ls -la .workspace/work/web/
# Review previous tasks to see patterns
```

**Ask Claude**:
```
"How does /web-next determine which agent to invoke?"
"Show me an example of htmx infinite scroll"
"How do I add a custom validator to DRF serializer?"
```

---

*You're ready to build full-stack features with intelligent agent routing!*
*Start with /web-explore and let the agents guide you.*
