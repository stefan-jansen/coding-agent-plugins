---
commandName: web-plan
description: Create implementation plan with agent assignments for web development task
category: workflow
version: 1.0.0
---

# Web Development Implementation Planning

Create a detailed implementation plan with specific agent assignments for each phase/task.

## Usage

```bash
/web-plan                    # Uses analysis from /web-explore
/web-plan @requirements.md   # Plan from requirements doc
```

## Prerequisites

Must have run `/web-explore` first to create work unit with task analysis.

## Process

You are creating an **implementation plan** for web development work. Your goal is to:

1. **Load task analysis** - Read metadata.json from work unit
2. **Break down into tasks** - Specific, measurable, testable tasks
3. **Assign agents** - Which specialized agent handles each task
4. **Define dependencies** - What must finish before what can start
5. **Set success criteria** - How to verify each task complete

## Implementation Plan Structure

```markdown
# Implementation Plan: [Task Name]

## Overview
- **Classification**: [Frontend | Backend | Full-stack]
- **Total Estimated Time**: [hours]
- **Agents Involved**: [frontend-engineer, backend-django]

## Tasks

### Task 1: [Task Name]
**Agent**: [frontend-engineer | backend-django]
**Estimated Time**: [hours]
**Dependencies**: None | Task X must be complete
**MCP Tools**: [Chrome DevTools, Serena, Context7]

**Implementation Steps**:
1. [Specific step]
2. [Specific step]
3. [Specific step]

**Success Criteria**:
- [ ] [Measurable criterion]
- [ ] [Verification method]

**Output Artifacts**:
- [File or documentation to create]

---

### Task 2: [Task Name]
**Agent**: [agent-name]
**Estimated Time**: [hours]
**Dependencies**: Task 1 complete
...

## Coordination Points

[If multi-agent work]

**Handoff 1: Backend → Frontend**
- **Trigger**: Backend Task X complete
- **Deliverable**: API contract documentation (endpoints, request/response format)
- **Location**: work_unit/api-contract.md
- **Frontend Dependency**: Must read API contract before starting integration

## Verification Plan

**Per-Task Verification**:
- Frontend tasks: Chrome DevTools verification (screenshots, console, performance)
- Backend tasks: Test output (pytest --verbose)

**Integration Verification** (if full-stack):
- End-to-end test with both frontend and backend
- Chrome DevTools network tab shows successful API calls
- No console errors

**Final Acceptance**:
- [ ] All tasks complete
- [ ] All tests pass
- [ ] Chrome DevTools verification complete (if frontend)
- [ ] Documentation updated
- [ ] Ready for production

## Timeline

**Phase 1**: [Tasks 1-3] - [X hours] - [backend-django]
**Phase 2**: [Tasks 4-6] - [X hours] - [frontend-engineer]
**Total**: [X hours] over [X days]

## Risk Assessment

**Potential Issues**:
- [Risk 1]: [Mitigation strategy]
- [Risk 2]: [Mitigation strategy]

**Blockers**:
- [Dependency on external service]
- [Need to install X package]
```

## Example Plans

### Example 1: Frontend-Only (Responsive Navbar)

```markdown
# Implementation Plan: Responsive Navbar

## Overview
- **Classification**: Frontend-only
- **Total Estimated Time**: 1-2 hours
- **Agents Involved**: frontend-engineer

## Tasks

### Task 1: Implement Mobile Navbar (Hamburger Menu)
**Agent**: frontend-engineer
**Estimated Time**: 30 minutes
**Dependencies**: None
**MCP Tools**: Chrome DevTools (verification), Context7 (DaisyUI docs)

**Implementation Steps**:
1. Add DaisyUI drawer component to base template
2. Add hamburger menu button (visible only on mobile: `lg:hidden`)
3. Add navigation links inside drawer
4. Style with Tailwind classes

**Success Criteria**:
- [ ] Hamburger icon visible on mobile (< 1024px width)
- [ ] Hamburger icon hidden on desktop (>= 1024px width)
- [ ] Drawer opens when hamburger clicked
- [ ] Navigation links work correctly

**Output Artifacts**:
- Updated `base.html` template
- Screenshots (mobile view)

---

### Task 2: Implement Desktop Navbar (Horizontal)
**Agent**: frontend-engineer
**Estimated Time**: 30 minutes
**Dependencies**: Task 1 complete (same template)
**MCP Tools**: Chrome DevTools (verification)

**Implementation Steps**:
1. Add horizontal navbar (hidden on mobile: `hidden lg:flex`)
2. Add navigation links with Tailwind styling
3. Ensure brand logo visible on all viewports
4. Add hover states for links

**Success Criteria**:
- [ ] Horizontal nav visible on desktop (>= 1024px)
- [ ] Horizontal nav hidden on mobile (< 1024px)
- [ ] Hover states work correctly
- [ ] Brand logo always visible

**Output Artifacts**:
- Updated `base.html` template
- Screenshots (desktop view)

---

### Task 3: Verification and Testing
**Agent**: frontend-engineer
**Estimated Time**: 30 minutes
**Dependencies**: Tasks 1-2 complete
**MCP Tools**: Chrome DevTools (required)

**Implementation Steps**:
1. Test mobile viewport (375x667): Hamburger menu works
2. Test tablet viewport (768x1024): Transition point works
3. Test desktop viewport (1920x1080): Horizontal nav works
4. Check console for errors
5. Test keyboard navigation (accessibility)

**Success Criteria**:
- [ ] Screenshots at 3 viewports show correct layouts
- [ ] No console errors (`list_console_messages`)
- [ ] Keyboard navigation works (Tab key)
- [ ] ARIA labels present for hamburger button

**Output Artifacts**:
- Screenshots: mobile.png, tablet.png, desktop.png
- verification.md with Chrome DevTools evidence

## Verification Plan

**Per-Task Verification**:
- Task 1: Chrome DevTools mobile viewport screenshot
- Task 2: Chrome DevTools desktop viewport screenshot
- Task 3: Comprehensive verification report

**Final Acceptance**:
- [ ] All 3 tasks complete
- [ ] Responsive behavior verified at all breakpoints
- [ ] No console errors
- [ ] Keyboard accessible
- [ ] Screenshots prove correctness

## Timeline

**Phase 1**: Tasks 1-3 - 1.5 hours - frontend-engineer
**Total**: 1.5 hours

## Risk Assessment

**Potential Issues**:
- DaisyUI theme not configured: Check tailwind.config.js for DaisyUI plugin
- JavaScript not loading: Verify static files served correctly

**Blockers**: None
```

### Example 2: Backend-Only (User Profile API)

```markdown
# Implementation Plan: User Profile REST API

## Overview
- **Classification**: Backend-only
- **Total Estimated Time**: 3-4 hours
- **Agents Involved**: backend-django

## Tasks

### Task 1: Model and Serializer
**Agent**: backend-django
**Estimated Time**: 1 hour
**Dependencies**: None
**MCP Tools**: Serena (locate existing User model), Context7 (DRF docs)

**Implementation Steps**:
1. Use Serena `find_symbol("User")` to locate User model
2. Extend User with OneToOne Profile model (bio, avatar, website)
3. Create ProfileSerializer with validation
4. Add read-only computed fields (full_name, member_since)

**Success Criteria**:
- [ ] Profile model created with migrations
- [ ] Migrations applied successfully
- [ ] ProfileSerializer handles all fields
- [ ] Validation rules enforced (bio max length, URL validation)

**Output Artifacts**:
- `models.py`: Profile model
- `serializers.py`: ProfileSerializer
- Migration files

---

### Task 2: ViewSet and Routing
**Agent**: backend-django
**Estimated Time**: 45 minutes
**Dependencies**: Task 1 complete
**MCP Tools**: Serena (locate existing routers)

**Implementation Steps**:
1. Create ProfileViewSet (ModelViewSet)
2. Add permissions: IsAuthenticatedOrReadOnly + IsOwnerOrReadOnly
3. Override perform_update to ensure user can only modify own profile
4. Register with router: `/api/profiles/`
5. Add custom action: `/api/profiles/me/` (current user's profile)

**Success Criteria**:
- [ ] CRUD endpoints available
- [ ] Authentication enforced
- [ ] Users can only modify own profiles
- [ ] `/api/profiles/me/` returns current user profile

**Output Artifacts**:
- `views.py`: ProfileViewSet
- `urls.py`: Router registration

---

### Task 3: Testing
**Agent**: backend-django
**Estimated Time**: 1.5 hours
**Dependencies**: Task 2 complete
**MCP Tools**: None (pytest)

**Implementation Steps**:
1. Write model tests (Profile creation, str method, relationships)
2. Write serializer tests (validation, read-only fields)
3. Write API tests:
   - GET /api/profiles/ (list, pagination)
   - GET /api/profiles/{id}/ (retrieve)
   - PUT /api/profiles/{id}/ (update own profile → 200)
   - PUT /api/profiles/{other_id}/ (update others → 403)
   - GET /api/profiles/me/ (current user → 200)
   - Unauthenticated PUT → 401
4. Run tests: `pytest myapp/tests/test_profiles.py --verbose`
5. Check coverage: `pytest --cov=myapp.models --cov=myapp.views`

**Success Criteria**:
- [ ] All model tests pass
- [ ] All serializer tests pass
- [ ] All API tests pass (15+ tests)
- [ ] Coverage >80%
- [ ] No test warnings or errors

**Output Artifacts**:
- `tests/test_profiles.py`: All tests
- Test output (pytest --verbose)
- Coverage report

---

### Task 4: Documentation
**Agent**: backend-django
**Estimated Time**: 30 minutes
**Dependencies**: Tasks 1-3 complete
**MCP Tools**: Context7 (drf-spectacular docs)

**Implementation Steps**:
1. Add docstrings to ProfileViewSet and actions
2. Configure drf-spectacular schema generation
3. Generate OpenAPI schema: `/api/schema/`
4. View Swagger UI: `/api/docs/`
5. Document example requests/responses

**Success Criteria**:
- [ ] OpenAPI schema generates without errors
- [ ] Swagger UI displays all endpoints
- [ ] Example requests shown for each endpoint
- [ ] Authentication requirements documented

**Output Artifacts**:
- OpenAPI schema (auto-generated)
- `api-contract.md`: Manual API documentation

## Verification Plan

**Per-Task Verification**:
- Task 1: Migrations apply successfully
- Task 2: Manual API testing with curl/Postman
- Task 3: Pytest output shows all tests pass
- Task 4: Swagger UI loads correctly

**Final Acceptance**:
- [ ] All 4 tasks complete
- [ ] All tests pass (pytest output)
- [ ] API documented (OpenAPI + manual)
- [ ] Security reviewed (permissions correct)
- [ ] Ready for frontend integration

## Timeline

**Phase 1**: Tasks 1-4 - 3.5 hours - backend-django
**Total**: 3.5 hours

## Risk Assessment

**Potential Issues**:
- User model already has profile: Use Serena to check before creating
- Permission issues: Test thoroughly with authenticated/unauthenticated users

**Blockers**:
- Need drf-spectacular installed: `pip install drf-spectacular`
```

### Example 3: Full-Stack (Real-time Notifications)

```markdown
# Implementation Plan: Real-time Notification System

## Overview
- **Classification**: Full-stack
- **Total Estimated Time**: 10-12 hours
- **Agents Involved**: backend-django, frontend-engineer

## Tasks

### Backend Phase (backend-django, 6-7 hours)

#### Task 1: Notification Model and Admin
**Agent**: backend-django
**Estimated Time**: 1 hour
**Dependencies**: None
**MCP Tools**: Serena (locate User model)

**Implementation Steps**:
1. Create Notification model (message, user, is_read, created_at)
2. Add indexes on user and created_at
3. Create admin interface for notifications
4. Run migrations

**Success Criteria**:
- [ ] Model created with proper relationships
- [ ] Migrations applied
- [ ] Admin interface works
- [ ] Can create test notifications

---

#### Task 2: WebSocket Consumer
**Agent**: backend-django
**Estimated Time**: 2 hours
**Dependencies**: Task 1 complete
**MCP Tools**: Serena (locate existing consumers), Context7 (Channels docs)

**Implementation Steps**:
1. Create NotificationConsumer (AsyncJsonWebsocketConsumer)
2. Implement connect (authenticate, join user group)
3. Implement disconnect (leave group)
4. Implement receive_json (handle mark_read messages)
5. Implement notification_message (send to WebSocket)
6. Configure routing and channel layer (Redis)

**Success Criteria**:
- [ ] Consumer connects successfully
- [ ] User joins correct group (notifications_{user_id})
- [ ] Consumer sends notifications to WebSocket
- [ ] Mark as read functionality works

---

#### Task 3: Notification Creation Endpoint
**Agent**: backend-django
**Estimated Time**: 1.5 hours
**Dependencies**: Tasks 1-2 complete
**MCP Tools**: Serena

**Implementation Steps**:
1. Create NotificationSerializer
2. Create NotificationViewSet with custom actions:
   - list (user's notifications)
   - mark_read (mark single as read)
   - mark_all_read (mark all as read)
   - unread_count (get count of unread)
3. Create background function to send notification via Channels
4. Register with router: `/api/notifications/`

**Success Criteria**:
- [ ] Can create notifications via API
- [ ] Notifications sent to WebSocket automatically
- [ ] Mark as read endpoints work
- [ ] Unread count accurate

---

#### Task 4: Backend Testing
**Agent**: backend-django
**Estimated Time**: 2 hours
**Dependencies**: Tasks 1-3 complete
**MCP Tools**: None (pytest)

**Implementation Steps**:
1. Write model tests
2. Write WebSocket consumer tests (channels.testing.WebsocketCommunicator)
3. Write API tests (CRUD, mark_read, unread_count)
4. Test end-to-end: Create notification → Verify WebSocket receives
5. Run full test suite

**Success Criteria**:
- [ ] All model tests pass
- [ ] WebSocket connection tests pass
- [ ] WebSocket message delivery tests pass
- [ ] API tests pass (20+ tests)
- [ ] Coverage >80%

---

#### Task 5: API Contract Documentation
**Agent**: backend-django
**Estimated Time**: 30 minutes
**Dependencies**: Tasks 1-4 complete
**MCP Tools**: None

**Implementation Steps**:
1. Document REST API endpoints
2. Document WebSocket protocol
3. Provide example requests/responses
4. Document authentication requirements

**Success Criteria**:
- [ ] API contract complete and clear
- [ ] Frontend can implement from documentation alone
- [ ] Example curl commands provided

**Output Artifacts**:
- `work_unit/api-contract.md`

**API Contract Example**:
```markdown
# Notification API Contract

## REST Endpoints

GET /api/notifications/
- List user's notifications (paginated)
- Auth: Required
- Response: { "results": [{"id": 1, "message": "...", "is_read": false}] }

POST /api/notifications/{id}/mark_read/
- Mark notification as read
- Auth: Required
- Response: { "id": 1, "is_read": true }

GET /api/notifications/unread_count/
- Get count of unread notifications
- Auth: Required
- Response: { "count": 5 }

## WebSocket

URL: ws://localhost:8000/ws/notifications/
Auth: Session (must be authenticated)

Incoming Messages (Server → Client):
{
  "type": "notification",
  "id": 123,
  "message": "You have a new message",
  "created_at": "2025-10-16T10:30:00Z"
}

Outgoing Messages (Client → Server):
{
  "type": "mark_read",
  "id": 123
}
```

---

### Frontend Phase (frontend-engineer, 4-5 hours)

#### Task 6: WebSocket Client Setup
**Agent**: frontend-engineer
**Estimated Time**: 1.5 hours
**Dependencies**: Task 5 complete (API contract documented)
**MCP Tools**: Chrome DevTools (network tab), Context7 (htmx docs)

**Implementation Steps**:
1. Read API contract from work_unit/api-contract.md
2. Add htmx WebSocket extension to base template
3. Create WebSocket connection element
4. Handle incoming notifications (append to notification list)
5. Test connection with Chrome DevTools network tab

**Success Criteria**:
- [ ] WebSocket connection establishes (Chrome DevTools shows WS upgrade)
- [ ] Incoming notifications received
- [ ] No console errors
- [ ] Connection reconnects on disconnect

---

#### Task 7: Notification UI Component
**Agent**: frontend-engineer
**Estimated Time**: 2 hours
**Dependencies**: Task 6 complete
**MCP Tools**: Chrome DevTools (screenshots, console), Context7 (DaisyUI docs)

**Implementation Steps**:
1. Create notification dropdown (DaisyUI dropdown + badge)
2. Display unread count badge
3. Style notifications (DaisyUI alert components)
4. Add mark as read functionality (htmx POST)
5. Add "Mark all as read" button
6. Implement notification toast/popup for new notifications

**Success Criteria**:
- [ ] Notification dropdown shows list
- [ ] Unread count badge displays correctly
- [ ] Mark as read updates UI immediately
- [ ] New notifications show toast popup
- [ ] Responsive on mobile and desktop

---

#### Task 8: Frontend Verification
**Agent**: frontend-engineer
**Estimated Time**: 1 hour
**Dependencies**: Tasks 6-7 complete
**MCP Tools**: Chrome DevTools (required)

**Implementation Steps**:
1. Test WebSocket connection (network tab shows WS)
2. Test notification creation → UI updates in real-time
3. Test mark as read → badge count decreases
4. Test responsive behavior (mobile + desktop)
5. Test error handling (disconnect/reconnect)
6. Check console for errors
7. Take screenshots for verification

**Success Criteria**:
- [ ] WebSocket connected (Chrome DevTools network tab proof)
- [ ] Real-time notifications work
- [ ] Mark as read works
- [ ] No console errors
- [ ] Screenshots prove correctness (mobile + desktop)

**Output Artifacts**:
- verification.md with Chrome DevTools evidence
- Screenshots (notification-dropdown.png, mobile-view.png)

---

## Coordination Points

**Handoff: Backend → Frontend**
- **Trigger**: Backend Task 5 complete (API contract documented)
- **Deliverable**: work_unit/api-contract.md
- **Frontend Dependency**: Task 6 reads API contract before starting
- **Communication**: Backend documents WebSocket URL, message format, auth requirements

## Verification Plan

**Backend Verification**:
- All backend tests pass (pytest output)
- WebSocket consumer tested with WebsocketCommunicator
- API endpoints tested with APIClient

**Frontend Verification**:
- Chrome DevTools WebSocket connection proof
- Screenshots show correct UI behavior
- No console errors

**Integration Verification**:
- End-to-end test: Backend creates notification → Frontend receives and displays
- Chrome DevTools network tab shows successful WebSocket communication
- Unread count accurate across sessions

**Final Acceptance**:
- [ ] All 8 tasks complete
- [ ] All backend tests pass
- [ ] Chrome DevTools frontend verification complete
- [ ] End-to-end real-time notification works
- [ ] Documentation complete
- [ ] Ready for production

## Timeline

**Phase 1 - Backend**: Tasks 1-5 - 7 hours - backend-django
**Phase 2 - Frontend**: Tasks 6-8 - 4.5 hours - frontend-engineer
**Total**: 11.5 hours over 2-3 days

## Risk Assessment

**Potential Issues**:
- Redis not installed for channel layer: Install Redis before Task 2
- WebSocket connection fails due to HTTPS: Configure WebSocket over WSS in production
- Session authentication not working: Verify CSRF and session cookies

**Blockers**:
- Need Redis for channel layer: `docker run -d redis`
- Need channels and channels-redis: `pip install channels channels-redis`
- Need htmx WebSocket extension: `<script src="htmx.org/dist/ext/ws.js">`
```

## Notes

- **Break down tasks** - Each task should be ~30min-2 hours (testable increment)
- **Assign agents explicitly** - No ambiguity about who does what
- **Document handoffs** - For multi-agent work, be explicit about coordination
- **Define success criteria** - Measurable, verifiable criteria
- **Estimate realistically** - Better to overestimate than underestimate

## Integration with /web-next

After planning, `/web-next` will:
1. Load this implementation plan
2. Execute tasks in dependency order
3. Invoke appropriate agent for each task
4. Verify success criteria before proceeding
5. Create handoff documentation for multi-agent tasks

---

*Web Plan Command - Detailed Implementation Planning with Agent Assignments*
*Version 1.0.0*
