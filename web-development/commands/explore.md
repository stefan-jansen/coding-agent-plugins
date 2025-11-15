---
commandName: web-explore
description: Analyze web development task and suggest appropriate specialized agent
category: workflow
version: 1.0.0
---

# Web Development Task Exploration

Analyze a web development task and determine complexity, required expertise, and which specialized agent(s) should handle it.

## Usage

```bash
/web-explore "Add real-time notifications to dashboard"
/web-explore "Make navbar responsive"
/web-explore "Create user profile API"
/web-explore @requirements.md
```

## Process

You are performing **task analysis** for web development work. Your goal is to:

1. **Understand the task** - Read the description or requirements document
2. **Assess complexity** - Is this frontend, backend, or full-stack?
3. **Suggest agent(s)** - Which specialized agent(s) should handle this?
4. **Create work unit** - Set up work tracking structure

## Task Classification

### Frontend-Only Tasks
**Indicators:**
- UI/UX design, layout, styling
- Responsive design, mobile-first
- JavaScript interactions (without API)
- Component development
- Performance optimization (Core Web Vitals)
- Accessibility improvements

**Keywords:** navbar, layout, responsive, mobile, design, UI, component, animation, styling, theme, dark mode

**Suggested Agent:** `frontend-engineer`
**MCP Tools Needed:** Chrome DevTools (verification), Context7 (Tailwind/htmx docs)

**Example Tasks:**
- "Make navbar responsive"
- "Add dark mode toggle"
- "Optimize page load performance"
- "Fix layout on mobile"

### Backend-Only Tasks
**Indicators:**
- API design and implementation
- Database models and migrations
- Business logic and validation
- Authentication/authorization
- Real-time backend (WebSocket consumers)
- Performance optimization (queries, caching)

**Keywords:** API, endpoint, database, model, migration, authentication, WebSocket, consumer, query, Django

**Suggested Agent:** `backend-django`
**MCP Tools Needed:** Serena (code navigation), Context7 (Django/DRF docs)

**Example Tasks:**
- "Create user profile API"
- "Add database indexes for performance"
- "Implement JWT authentication"
- "Create WebSocket consumer for notifications"

### Full-Stack Tasks
**Indicators:**
- Requires both UI and API
- Real-time features (WebSocket client + server)
- Forms with backend validation
- End-to-end feature development

**Keywords:** feature, real-time, notifications, chat, dashboard with data, form submission

**Suggested Agents:** `backend-django` (Phase 1) → `frontend-engineer` (Phase 2)
**Coordination:** Sequential workflow with API contract handoff

**Example Tasks:**
- "Add real-time notifications"
  - Backend: WebSocket consumer, notification model
  - Frontend: WebSocket client, notification UI
- "Create contact form"
  - Backend: Form validation, email sending
  - Frontend: Form UI, AJAX submission (htmx)

### Ambiguous Tasks
**Indicators:**
- Performance issues (could be frontend OR backend)
- Bug fixes (need investigation)
- "Dashboard is slow" (could be rendering OR queries)

**Suggested Approach:** Start with `frontend-engineer` for investigation
- Run Chrome DevTools performance trace
- Identify bottleneck (frontend rendering or backend API)
- Hand off to `backend-django` if API optimization needed

## Task Analysis Template

After reading the task description, provide this analysis:

```markdown
# Web Development Task Analysis

**Task**: [Short description]

**Classification**: [Frontend-only | Backend-only | Full-stack | Ambiguous]

**Complexity**: [Low | Medium | High]
- Low: Single component/endpoint, <2 hours
- Medium: Multiple components/endpoints, 2-8 hours
- High: Complex feature, >8 hours

**Recommended Approach**:

[If Frontend-only]
**Agent**: frontend-engineer
**Tools**: Chrome DevTools (verification), Context7 (docs)
**Steps**:
1. [Step 1]
2. [Step 2]
3. Verify with Chrome DevTools (screenshots, console, performance)

[If Backend-only]
**Agent**: backend-django
**Tools**: Serena (code navigation), Context7 (docs)
**Steps**:
1. [Step 1]
2. [Step 2]
3. Write tests and verify pass

[If Full-stack]
**Phase 1 - Backend** (backend-django):
1. [Backend steps]
2. Document API contract

**Phase 2 - Frontend** (frontend-engineer):
1. [Frontend steps]
2. Consume backend API
3. Verify with Chrome DevTools

[If Ambiguous]
**Investigation Approach**:
1. Start with frontend-engineer
2. Run Chrome DevTools performance trace / debug
3. If backend bottleneck found → hand off to backend-django

**Estimated Timeline**: [hours/days]

**Success Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Verification complete (tests pass / Chrome DevTools verification)]

**Proceed with [agent-name]?** (yes to continue / override to specify different agent)
```

## Work Unit Creation

After task analysis, create work unit structure:

```bash
# Work unit directory
.claude/work/web/[task-slug]/

# Files
metadata.json       # Task metadata, agent assignments
requirements.md     # Full task requirements
state.json         # Task state (pending/in_progress/completed)
implementation.md  # Implementation notes (created during /web-next)
verification.md    # Verification evidence (screenshots, test output)
```

**metadata.json example:**
```json
{
  "task": "Add real-time notifications",
  "classification": "full-stack",
  "agents": ["backend-django", "frontend-engineer"],
  "phases": [
    {
      "phase": 1,
      "agent": "backend-django",
      "status": "pending",
      "description": "WebSocket consumer and notification model"
    },
    {
      "phase": 2,
      "agent": "frontend-engineer",
      "status": "pending",
      "description": "WebSocket client and notification UI"
    }
  ],
  "created": "2025-10-16T10:30:00Z"
}
```

## Examples

### Example 1: Frontend-Only Task

**Input:**
```bash
/web-explore "Make the navbar responsive - currently breaks on mobile"
```

**Output:**
```markdown
# Web Development Task Analysis

**Task**: Make navbar responsive for mobile devices

**Classification**: Frontend-only

**Complexity**: Low (~1-2 hours)

**Recommended Approach**:

**Agent**: frontend-engineer
**Tools**: Chrome DevTools (verification), Context7 (Tailwind docs)

**Implementation Steps**:
1. Use Tailwind responsive classes (hidden lg:flex for desktop nav)
2. Add DaisyUI drawer component for mobile hamburger menu
3. Test with Chrome DevTools:
   - Resize to mobile (375x667) → hamburger visible
   - Resize to desktop (1920x1080) → horizontal nav visible
   - Take screenshots for verification

**Success Criteria**:
- [ ] Mobile viewport shows hamburger menu
- [ ] Desktop viewport shows horizontal navigation
- [ ] No console errors
- [ ] Chrome DevTools screenshots prove correctness

**Estimated Timeline**: 1-2 hours

**Proceed with frontend-engineer?** (yes/override)
```

### Example 2: Backend-Only Task

**Input:**
```bash
/web-explore "Create REST API for user profiles with CRUD operations"
```

**Output:**
```markdown
# Web Development Task Analysis

**Task**: Create user profile REST API

**Classification**: Backend-only

**Complexity**: Medium (~3-4 hours)

**Recommended Approach**:

**Agent**: backend-django
**Tools**: Serena (code navigation), Context7 (DRF docs)

**Implementation Steps**:
1. Use Serena to locate existing User model and serializers
2. Create UserProfileSerializer with validation
3. Create UserProfileViewSet (CRUD operations)
4. Add authentication (IsAuthenticated + IsOwnerOrReadOnly)
5. Register with router: `/api/profiles/`
6. Write tests:
   - Test GET /api/profiles/ (list)
   - Test GET /api/profiles/{id}/ (retrieve)
   - Test PUT /api/profiles/{id}/ (update own profile)
   - Test PUT /api/profiles/{id}/ (cannot update others' profiles)
7. Run pytest and verify all tests pass

**Success Criteria**:
- [ ] All CRUD endpoints working
- [ ] Authentication enforced
- [ ] Users can only modify own profiles
- [ ] All tests pass (pytest output)
- [ ] API documented (OpenAPI schema)

**Estimated Timeline**: 3-4 hours

**Proceed with backend-django?** (yes/override)
```

### Example 3: Full-Stack Task

**Input:**
```bash
/web-explore "Add real-time notification system - users should see notifications without page refresh"
```

**Output:**
```markdown
# Web Development Task Analysis

**Task**: Real-time notification system via WebSocket

**Classification**: Full-stack

**Complexity**: High (~8-12 hours)

**Recommended Approach**:

**Phase 1 - Backend** (backend-django, ~5-6 hours):
1. Create Notification model (message, user, read status, timestamp)
2. Create Django Channels WebSocket consumer
3. Set up channel layer (Redis)
4. Create notification creation endpoint (POST /api/notifications/)
5. Implement group messaging (send to specific users)
6. Write tests:
   - Test WebSocket connection
   - Test notification creation
   - Test notification delivery via WebSocket
7. Document WebSocket API contract for frontend

**Phase 2 - Frontend** (frontend-engineer, ~3-4 hours):
1. Implement WebSocket client with htmx ws extension
2. Design notification UI component (DaisyUI toast/alert)
3. Add notification badge with unread count
4. Handle connection errors and reconnection
5. Verify with Chrome DevTools:
   - WebSocket connection successful (network tab)
   - Notifications display correctly
   - No console errors
   - Test on mobile and desktop

**API Contract** (backend documents for frontend):
```
WebSocket URL: ws://localhost:8000/ws/notifications/
Auth: Session (must be authenticated)

Incoming: { "type": "notification", "message": "...", "id": 123 }
Outgoing: { "type": "mark_read", "id": 123 }
```

**Success Criteria**:
- [ ] Backend: WebSocket consumer working, tests pass
- [ ] Backend: API contract documented
- [ ] Frontend: Notifications display in real-time
- [ ] Frontend: Chrome DevTools verification complete
- [ ] Integration: End-to-end test successful

**Estimated Timeline**: 8-12 hours (2 phases)

**Proceed with Phase 1 (backend-django)?** (yes/override)
```

### Example 4: Ambiguous Task

**Input:**
```bash
/web-explore "Dashboard is really slow, takes 10+ seconds to load"
```

**Output:**
```markdown
# Web Development Task Analysis

**Task**: Optimize dashboard performance

**Classification**: Ambiguous (could be frontend OR backend)

**Complexity**: Medium (~4-6 hours)

**Recommended Approach**:

**Investigation Phase** (frontend-engineer, ~1 hour):
1. Run Chrome DevTools performance trace
2. Identify bottleneck:
   - High LCP (>2.5s)? → Frontend rendering issue
   - Slow network requests? → Backend API issue
   - Many API calls? → Frontend or backend optimization needed

**Outcome A: Frontend Bottleneck**
- Agent: frontend-engineer
- Fix: Lazy loading, code splitting, image optimization
- Verify: Chrome DevTools shows LCP < 2.5s

**Outcome B: Backend Bottleneck**
- Agent: backend-django (hand off)
- Fix: Database indexes, select_related, caching
- Verify: API response time < 500ms

**Outcome C: Both**
- Phase 1: backend-django optimizes APIs
- Phase 2: frontend-engineer optimizes rendering

**Success Criteria**:
- [ ] Performance trace identifies bottleneck
- [ ] Appropriate agent handles optimization
- [ ] Dashboard loads in <3 seconds
- [ ] Chrome DevTools verification shows improvement

**Estimated Timeline**: 4-6 hours (investigation + fix)

**Proceed with investigation (frontend-engineer)?** (yes/override)
```

## Integration with /web-plan

After task analysis, user can:
1. Approve → `/web-plan` creates detailed implementation plan
2. Override → Specify different agent or approach
3. Refine → Ask questions, adjust scope

The analysis becomes input for `/web-plan` which breaks down into specific tasks.

## Notes

- **Always suggest agent** - Don't leave user guessing
- **Explain rationale** - Why this agent? Why this approach?
- **Estimate timeline** - Helps user understand scope
- **Define success criteria** - What does "done" mean?
- **Offer override** - User can disagree with suggestion

---

*Web Explore Command - Intelligent Task Analysis and Agent Routing*
*Version 1.0.0*
