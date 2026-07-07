---
commandName: web-next
description: Execute next task with intelligent agent routing
category: workflow
version: 1.0.0
---

# Web Development Task Execution

Execute the next available task from the implementation plan, automatically invoking the appropriate specialized agent.

## Usage

```bash
/web-next          # Execute next pending task
/web-next --task 3 # Execute specific task by number
/web-next --agent frontend-engineer  # Override agent selection
```

## Process

You are **executing implementation tasks** with intelligent agent routing. Your goal is to:

1. **Load implementation plan** - Read from work unit
2. **Identify next task** - Find first pending task respecting dependencies
3. **Determine agent** - Which specialized agent should handle this?
4. **Invoke agent** - Execute task with appropriate agent
5. **Verify completion** - Check success criteria met
6. **Update state** - Mark task complete, move to next

## Agent Routing Logic

### Automatic Agent Selection

**Based on task.agent field in plan:**
- `task.agent === "frontend-engineer"` → Invoke frontend-engineer agent
- `task.agent === "backend-django"` → Invoke backend-django agent

**Agent Invocation:**
```markdown
For this task, I'm going to invoke the **[agent-name] agent** to handle the [frontend/backend] work.

**Task**: [task description]
**Agent**: [agent-name]
**Why this agent**: [frontend UI work | backend API work | database optimization | etc.]

[Agent execution begins...]
```

### Agent Context Provision

When invoking an agent, provide:

1. **Task Description** - What needs to be done
2. **Success Criteria** - How to verify it's done
3. **Implementation Steps** - Specific steps from plan
4. **Work Unit Location** - Where to save artifacts
5. **Dependencies** - What's already complete, what to build on

**Example Context for Frontend Agent:**
```markdown
I'm invoking the **frontend-engineer agent** for this task.

**Task**: Implement responsive navbar
**Success Criteria**:
- [ ] Mobile viewport shows hamburger menu
- [ ] Desktop viewport shows horizontal navigation
- [ ] Chrome DevTools verification (screenshots)

**Implementation Steps**:
1. Add DaisyUI drawer for mobile
2. Add horizontal nav for desktop
3. Verify with Chrome DevTools

**Work Unit**: .workspace/work/web/responsive-navbar/
**Artifacts to Create**: Updated base.html, screenshots for verification

---

[Frontend-engineer agent execution begins]

**You are the frontend-engineer agent.** Follow your agent guidelines:
- Use Tailwind CSS + DaisyUI
- Implement responsive design
- 🚨 **ALWAYS VERIFY WITH CHROME DEVTOOLS**
- Take screenshots at mobile and desktop viewports
- Check console for errors

[Implement the task following frontend-engineer.md guidelines...]
```

**Example Context for Backend Agent:**
```markdown
I'm invoking the **backend-django agent** for this task.

**Task**: Create user profile REST API
**Success Criteria**:
- [ ] All CRUD endpoints working
- [ ] Tests pass (pytest output)
- [ ] API documented

**Implementation Steps**:
1. Use Serena to locate User model
2. Create ProfileSerializer
3. Create ProfileViewSet with permissions
4. Write tests for all endpoints
5. Document API contract

**Work Unit**: .workspace/work/web/user-profile-api/
**Artifacts to Create**: serializers.py, views.py, tests.py, api-contract.md

---

[Backend-django agent execution begins]

**You are the backend-django agent.** Follow your agent guidelines:
- 🚨 **USE SERENA FOR CODE NAVIGATION**
- 🚨 **ALWAYS WRITE TESTS**
- Test all CRUD operations
- Test authentication and permissions
- Provide pytest output as evidence

[Implement the task following backend-django.md guidelines...]
```

## Task Execution Workflow

### Step 1: Load Implementation Plan

```bash
# Read from work unit
cat .workspace/work/web/[task-slug]/implementation-plan.md
cat .workspace/work/web/[task-slug]/state.json
```

**state.json format:**
```json
{
  "tasks": [
    {
      "id": 1,
      "name": "Implement mobile navbar",
      "agent": "frontend-engineer",
      "status": "completed",
      "completed_at": "2025-10-16T10:30:00Z"
    },
    {
      "id": 2,
      "name": "Implement desktop navbar",
      "agent": "frontend-engineer",
      "status": "in_progress",
      "started_at": "2025-10-16T11:00:00Z"
    },
    {
      "id": 3,
      "name": "Frontend verification",
      "agent": "frontend-engineer",
      "status": "pending",
      "dependencies": [1, 2]
    }
  ]
}
```

### Step 2: Check Dependencies

Before executing task, verify dependencies met:

```python
def can_execute_task(task, completed_tasks):
    if not task.dependencies:
        return True
    return all(dep_id in completed_tasks for dep_id in task.dependencies)
```

**If dependencies not met:**
```markdown
Cannot execute Task 3 yet. Dependencies not complete:
- Task 1: ✅ Complete
- Task 2: ❌ Still in progress

Please complete Task 2 first, then run /web-next again.
```

### Step 3: Invoke Appropriate Agent

**Agent Invocation Pattern:**

```markdown
## Executing Task [N]: [Task Name]

**Agent**: [agent-name]
**Estimated Time**: [X hours]
**MCP Tools**: [tools list]

I'm now invoking the **[agent-name] agent** to handle this [frontend/backend] task.

---

[Agent-specific context and instructions]

**You are now operating as the [agent-name] agent.**

[Agent executes task following its own guidelines from agents/[agent-name].md]

---

[After agent completes task]

## Task [N] Completion Verification

**Success Criteria Check**:
- [✅/❌] [Criterion 1] - [Evidence]
- [✅/❌] [Criterion 2] - [Evidence]
- [✅/❌] [Criterion 3] - [Evidence]

**Artifacts Created**:
- [File 1]: [Description]
- [File 2]: [Description]

**Status**: [COMPLETE | INCOMPLETE | BLOCKED]

[If complete: Update state.json, proceed to next task]
[If incomplete: Document what's missing, request user input]
[If blocked: Document blocker, suggest resolution]
```

### Step 4: Verify Success Criteria

**Frontend Verification:**
```markdown
## Frontend Verification

**Chrome DevTools Evidence**:
1. Screenshot (mobile 375x667): ✅ Hamburger menu visible
2. Screenshot (desktop 1920x1080): ✅ Horizontal nav visible
3. Console messages: ✅ No errors
4. Performance trace: ✅ LCP 1.8s (< 2.5s target)

**Verification Files**:
- screenshots/mobile.png
- screenshots/desktop.png
- verification.md (Chrome DevTools report)

**Success Criteria**: ✅ ALL PASSED
```

**Backend Verification:**
```markdown
## Backend Verification

**Test Output**:
```
pytest tests/test_profiles.py --verbose

test_profile_creation PASSED
test_profile_list PASSED
test_profile_retrieve PASSED
test_profile_update_own PASSED
test_profile_update_others FAILED (403 Forbidden) ✅ Expected
test_unauthenticated_update FAILED (401) ✅ Expected

20 passed, 0 failed
```

**API Documentation**:
- api-contract.md: Complete
- OpenAPI schema: Generated
- Swagger UI: /api/docs/ accessible

**Success Criteria**: ✅ ALL PASSED
```

### Step 5: Update Task State

```json
{
  "id": 2,
  "name": "Implement desktop navbar",
  "agent": "frontend-engineer",
  "status": "completed",
  "started_at": "2025-10-16T11:00:00Z",
  "completed_at": "2025-10-16T11:45:00Z",
  "verification": {
    "method": "chrome-devtools",
    "evidence": [
      "screenshots/desktop.png",
      "verification.md"
    ]
  }
}
```

### Step 6: Multi-Agent Coordination

**For tasks requiring handoff:**

```markdown
## Task 5 Complete: API Contract Documentation

**Agent**: backend-django
**Status**: ✅ COMPLETE

**Deliverable Created**: api-contract.md

**Next Task Requires**: frontend-engineer agent
**Handoff**: Frontend agent will read api-contract.md to implement WebSocket client

**Coordination Point**:
- Backend has documented WebSocket URL: ws://localhost:8000/ws/notifications/
- Backend has documented message format (incoming/outgoing)
- Backend has documented authentication requirements
- Frontend can now implement client based on this contract

**Ready for Task 6**: Execute `/web-next` to start frontend implementation.
```

## Examples

### Example 1: Simple Frontend Task

```bash
/web-next
```

**Output:**
```markdown
## Executing Task 1: Implement Mobile Navbar

**Agent**: frontend-engineer
**Estimated Time**: 30 minutes
**MCP Tools**: Chrome DevTools, Context7

I'm invoking the **frontend-engineer agent** to implement the mobile hamburger menu navigation.

---

**You are now operating as the frontend-engineer agent.**

**Task**: Add responsive mobile navigation with DaisyUI drawer component

**Success Criteria**:
- [ ] Hamburger icon visible on mobile (< 1024px)
- [ ] Drawer opens on click
- [ ] Navigation links work
- [ ] Chrome DevTools verification complete

**Implementation Steps**:
1. Add DaisyUI drawer to base template
2. Style with Tailwind responsive classes
3. Test with Chrome DevTools (resize to 375x667)
4. Take screenshot for verification

**Critical Rule**: 🚨 ALWAYS VERIFY WITH CHROME DEVTOOLS

Let me implement this task...

[Reading base.html template...]
[Adding DaisyUI drawer component...]
[Testing with Chrome DevTools...]

**Chrome DevTools Verification**:
```
resize_page(375, 667)  # Mobile viewport
take_screenshot("mobile-navbar.png")
list_console_messages()  # Check for errors
```

**Verification Results**:
- Mobile screenshot: ✅ Hamburger visible, drawer works
- Console: ✅ No errors
- Keyboard navigation: ✅ Tab key works

---

## Task 1 Completion Verification

**Success Criteria Check**:
- ✅ Hamburger icon visible on mobile - Evidence: mobile-navbar.png
- ✅ Drawer opens on click - Evidence: Chrome DevTools interaction test
- ✅ Navigation links work - Evidence: Tested all links
- ✅ Chrome DevTools verification - Evidence: verification.md

**Artifacts Created**:
- templates/base.html: Updated with DaisyUI drawer
- screenshots/mobile-navbar.png: Mobile verification
- work_unit/verification.md: Chrome DevTools report

**Status**: ✅ COMPLETE

Task 1 marked complete. Ready for Task 2.

Run `/web-next` to continue with Task 2: Implement Desktop Navbar.
```

### Example 2: Backend Task with Serena

```bash
/web-next
```

**Output:**
```markdown
## Executing Task 1: Create Profile Model and Serializer

**Agent**: backend-django
**Estimated Time**: 1 hour
**MCP Tools**: Serena (code navigation), Context7 (DRF docs)

I'm invoking the **backend-django agent** to create the Profile model and serializer.

---

**You are now operating as the backend-django agent.**

**Task**: Create Profile model extending User with bio, avatar, website fields

**Success Criteria**:
- [ ] Profile model created with migrations
- [ ] ProfileSerializer handles all fields
- [ ] Validation rules enforced

**Implementation Steps**:
1. Use Serena find_symbol("User") to locate User model
2. Create OneToOne Profile model
3. Create ProfileSerializer
4. Run migrations

**Critical Rules**:
- 🚨 USE SERENA FOR CODE NAVIGATION
- 🚨 Only call methods verified via Serena

Let me start by using Serena to locate the existing User model...

[Using Serena find_symbol("User", "accounts/models.py")...]
[Found User model at accounts/models.py:15]

Now creating Profile model...
[Writing models.py...]

Creating serializer...
[Writing serializers.py...]

Running migrations...
```bash
python manage.py makemigrations
python manage.py migrate
```

**Migration Output**:
```
Migrations for 'accounts':
  accounts/migrations/0002_profile.py
    - Create model Profile
Operations to perform:
  Apply all migrations: accounts
Running migrations:
  Applying accounts.0002_profile... OK
```

---

## Task 1 Completion Verification

**Success Criteria Check**:
- ✅ Profile model created - Evidence: accounts/models.py:45
- ✅ Migrations applied - Evidence: Migration output above
- ✅ ProfileSerializer created - Evidence: accounts/serializers.py:23
- ✅ Validation rules enforced - Evidence: Bio max_length=500, URL validation

**Artifacts Created**:
- accounts/models.py: Profile model (lines 45-60)
- accounts/serializers.py: ProfileSerializer (lines 23-35)
- accounts/migrations/0002_profile.py: Migration file

**Status**: ✅ COMPLETE

Task 1 marked complete. Ready for Task 2: Create ViewSet and Routing.

Run `/web-next` to continue.
```

### Example 3: Multi-Agent Full-Stack (Backend → Frontend Handoff)

```bash
/web-next  # Task 5 (Backend: API Documentation)
```

**Output:**
```markdown
## Executing Task 5: Document API Contract for Frontend

**Agent**: backend-django
**Estimated Time**: 30 minutes

I'm invoking the **backend-django agent** to document the WebSocket API contract.

---

[Backend agent documents API...]

**API Contract Created**: work_unit/api-contract.md

**Content**:
```markdown
# Notification WebSocket API

URL: ws://localhost:8000/ws/notifications/
Auth: Session (must be authenticated)

Incoming (Server → Client):
{
  "type": "notification",
  "id": 123,
  "message": "You have a new message",
  "created_at": "2025-10-16T10:30:00Z"
}

Outgoing (Client → Server):
{
  "type": "mark_read",
  "id": 123
}
```

---

## Task 5 Complete

**Status**: ✅ COMPLETE
**Handoff**: API contract ready for frontend implementation

**Next Task**: Task 6 (Frontend: WebSocket Client)
**Agent**: frontend-engineer
**Dependency**: Must read api-contract.md

Run `/web-next` to start frontend implementation.
```

```bash
/web-next  # Task 6 (Frontend: WebSocket Client)
```

**Output:**
```markdown
## Executing Task 6: Implement WebSocket Client

**Agent**: frontend-engineer
**Estimated Time**: 1.5 hours
**MCP Tools**: Chrome DevTools (network tab)

I'm invoking the **frontend-engineer agent** to implement the WebSocket client.

**Handoff Received**: Reading api-contract.md from Task 5...

---

**You are now operating as the frontend-engineer agent.**

**API Contract** (from backend):
- WebSocket URL: ws://localhost:8000/ws/notifications/
- Auth: Session required
- Incoming format: { "type": "notification", "id": 123, "message": "..." }

**Task**: Implement WebSocket client with htmx

Let me implement the WebSocket connection...

[Adding htmx ws extension...]
[Creating WebSocket connection element...]
[Testing with Chrome DevTools...]

**Chrome DevTools Verification**:
```
navigate_page("http://localhost:8000/")
list_network_requests(resourceTypes=["websocket"])
```

**Network Tab**:
```
ws://localhost:8000/ws/notifications/ websocket [101 Switching Protocols]
Status: Connected
Messages: 3 received
```

**Console Messages**: ✅ No errors

---

## Task 6 Complete

**Success Criteria Check**:
- ✅ WebSocket connection established - Evidence: Chrome DevTools network tab
- ✅ Receives notifications - Evidence: 3 test messages received
- ✅ No console errors - Evidence: list_console_messages() output

**Status**: ✅ COMPLETE

Task 6 marked complete. Ready for Task 7: Notification UI Component.

Run `/web-next` to continue.
```

## Special Cases

### Case 1: Task Blocked

```markdown
## Task 3: Backend Testing

**Status**: ❌ BLOCKED

**Blocker**: Redis not running (required for Channels testing)

**Error**:
```
django.core.exceptions.ImproperlyConfigured: CHANNEL_LAYERS
setting must define a "default" channel layer
```

**Resolution**:
1. Install Redis: `docker run -d -p 6379:6379 redis`
2. Verify connection: `redis-cli ping`
3. Re-run `/web-next`

**Task status**: Marked as blocked in state.json
```

### Case 2: Partial Success

```markdown
## Task 2: API Endpoint Testing

**Status**: ⚠️ INCOMPLETE

**Success Criteria Check**:
- ✅ GET /api/profiles/ test passes
- ✅ POST /api/profiles/ test passes
- ❌ Permission test fails (IsOwnerOrReadOnly not enforced)

**Issue**: Users can modify other users' profiles (security issue!)

**Remaining Work**:
1. Fix permission class in ViewSet
2. Re-run tests
3. Verify all tests pass

**Task status**: Remains in_progress. Fix required before marking complete.

Run `/web-next` again after fixing permissions.
```

### Case 3: Agent Override

```bash
/web-next --agent frontend-engineer
```

**When to Override**:
- Task could be handled by either agent
- User prefers specific agent
- Plan agent assignment wrong

**Example**:
```markdown
**Plan suggested**: backend-django (database optimization)
**User override**: --agent frontend-engineer

Overriding plan. Using frontend-engineer agent instead.

**Reason for override**: User wants to optimize frontend rendering first,
then backend queries if still slow.

Proceeding with frontend-engineer...
```

## Notes

- **One task at a time** - Complete before moving to next
- **Verify before marking complete** - Evidence required
- **Respect dependencies** - Can't skip ahead
- **Document handoffs** - Multi-agent work needs clear communication
- **Agent switching is OK** - Claude Code can invoke different agents mid-task if needed

## Integration with /web-ship

After all tasks complete:
- Run `/web-ship` to deliver work
- Performs final verification
- Creates deployment documentation
- Archives work unit

---

*Web Next Command - Intelligent Task Execution with Agent Routing*
*Version 1.0.0*
