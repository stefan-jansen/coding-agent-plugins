---
commandName: web-ship
description: Deliver completed web development work with comprehensive verification
category: workflow
version: 1.0.0
---

# Web Development Delivery

Deliver completed web development work with full verification, documentation, and deployment readiness assessment.

## Usage

```bash
/web-ship                     # Deliver current work unit
/web-ship --skip-verification # Skip final verification (not recommended)
/web-ship --dry-run          # Preview what would be shipped
```

## Process

You are **delivering completed web development work**. Your goal is to:

1. **Verify all tasks complete** - Check state.json
2. **Run final verification** - Agent-specific checks
3. **Create delivery documentation** - What was built, how to use it
4. **Assess deployment readiness** - Production checklist
5. **Archive work unit** - Move to completed

## Delivery Checklist

### 1. Task Completion Verification

```markdown
## Task Completion Status

**Work Unit**: [name]
**Total Tasks**: [N]
**Completed**: [N]
**Incomplete**: [0]

**Task Summary**:
- Task 1: ✅ Complete - [name]
- Task 2: ✅ Complete - [name]
- Task 3: ✅ Complete - [name]

**Status**: ✅ ALL TASKS COMPLETE
```

**If tasks incomplete:**
```markdown
## Cannot Ship - Incomplete Tasks

**Incomplete Tasks**:
- Task 2: ⚠️ In Progress - [name]
- Task 4: ❌ Pending - [name]

**Required Actions**:
1. Complete Task 2 (run /web-next)
2. Complete Task 4 (run /web-next)
3. Then run /web-ship again

**Current Status**: NOT READY FOR DELIVERY
```

### 2. Frontend Verification (if applicable)

**Run final Chrome DevTools verification:**

```markdown
## Frontend Verification

**Chrome DevTools Final Checks**:

### Visual Verification
- [ ] Desktop (1920x1080): Screenshot shows correct layout
- [ ] Tablet (768x1024): Responsive behavior correct
- [ ] Mobile (375x667): Mobile layout correct
- [ ] Screenshots saved: desktop.png, tablet.png, mobile.png

### Console Check
```
list_console_messages()
```
- [ ] No errors in console
- [ ] No warnings (or warnings documented and acceptable)

### Performance Check
```
performance_start_trace(reload=true, autoStop=false)
navigate_page("http://localhost:8000/[page]")
performance_stop_trace()
```
- [ ] LCP < 2.5s (current: [X]s)
- [ ] CLS < 0.1 (current: [X])
- [ ] INP < 200ms (current: [X]ms)
- [ ] Performance issues documented in delivery-notes.md

### Network Check
```
list_network_requests()
```
- [ ] All API calls successful (200 status)
- [ ] No failed requests (404, 500)
- [ ] CORS working correctly
- [ ] WebSocket connected (if applicable)

### Accessibility Check
- [ ] Semantic HTML used
- [ ] ARIA labels present
- [ ] Keyboard navigation works
- [ ] Color contrast acceptable (manual check)

**Frontend Status**: ✅ VERIFIED / ⚠️ ISSUES FOUND / ❌ FAILED
```

### 3. Backend Verification (if applicable)

**Run final test suite:**

```markdown
## Backend Verification

**Test Suite**:
```bash
pytest myapp/tests/ --verbose --cov=myapp --cov-report=term
```

**Test Results**:
```
======================== test session starts ========================
collected 45 items

tests/test_models.py::test_profile_creation PASSED
tests/test_serializers.py::test_profile_serializer PASSED
tests/test_views.py::test_list_profiles PASSED
tests/test_views.py::test_create_profile PASSED
tests/test_views.py::test_update_own_profile PASSED
tests/test_views.py::test_update_others_profile PASSED
... (39 more tests)

======================== 45 passed in 3.21s =========================

Coverage:
myapp/models.py     95%
myapp/views.py      87%
myapp/serializers.py 100%
TOTAL               89%
```

**Backend Checklist**:
- [ ] All tests pass (45/45)
- [ ] Coverage >80% (current: 89%)
- [ ] No failing migrations
- [ ] API documentation complete (OpenAPI schema)
- [ ] Security review complete (CSRF, CORS, auth)

**Backend Status**: ✅ VERIFIED / ❌ FAILED
```

### 4. Integration Verification (if full-stack)

**Test frontend + backend together:**

```markdown
## Integration Verification

**End-to-End Tests**:

### Scenario 1: [Feature Name]
1. Frontend: User clicks button
2. Backend: API receives POST request
3. Backend: Data saved to database
4. Frontend: UI updates via htmx/WebSocket
5. Verification: Chrome DevTools shows success

**Test Results**:
- ✅ Frontend UI responds correctly
- ✅ Backend API processes request (logs show success)
- ✅ Database updated (verified via admin)
- ✅ Frontend receives response and updates UI
- ✅ Chrome DevTools shows successful network request

### Scenario 2: [Another Feature]
...

**Integration Status**: ✅ VERIFIED / ❌ FAILED
```

## Delivery Documentation

### delivery-summary.md

Create comprehensive delivery summary:

```markdown
# Delivery Summary: [Feature Name]

**Delivered**: 2025-10-16
**Work Unit**: .workspace/work/web/[task-slug]/
**Classification**: [Frontend | Backend | Full-stack]
**Total Time**: [X] hours over [Y] days

## What Was Built

### Frontend Components (if applicable)
- **Responsive Navbar**: Mobile hamburger + desktop horizontal nav
  - File: templates/base.html (lines 45-89)
  - DaisyUI drawer component for mobile
  - Tailwind responsive classes for breakpoints
  - Verified: Mobile (375x667) and Desktop (1920x1080)

- **Notification UI**: Real-time notification display
  - File: templates/notifications/widget.html
  - htmx WebSocket integration
  - DaisyUI toast components
  - Verified: Chrome DevTools network tab shows WS connection

### Backend Components (if applicable)
- **User Profile API**: Full CRUD REST API
  - File: accounts/views.py (ProfileViewSet, lines 45-78)
  - File: accounts/serializers.py (ProfileSerializer, lines 12-30)
  - Endpoints: GET/POST/PUT/DELETE /api/profiles/
  - Authentication: Token + Session
  - Tests: 20 tests, all passing, 89% coverage

- **Notification WebSocket**: Real-time notifications via Channels
  - File: notifications/consumers.py (NotificationConsumer, lines 15-55)
  - URL: ws://localhost:8000/ws/notifications/
  - Channel layer: Redis
  - Tests: 8 WebSocket tests, all passing

## How to Use

### For Users
[Step-by-step guide for using the feature]

### For Developers
**Frontend**:
- Templates: templates/[files]
- Static files: static/[files]
- htmx extensions: [ws, sse, etc.]

**Backend**:
- Models: [app]/models.py
- Views: [app]/views.py
- Serializers: [app]/serializers.py
- Consumers: [app]/consumers.py
- URLs: [app]/urls.py
- Tests: [app]/tests/

## Verification Evidence

**Frontend**:
- Screenshots: work_unit/screenshots/ (6 images)
- Chrome DevTools report: work_unit/verification.md
- Performance trace: LCP 1.8s, CLS 0.02, INP 45ms

**Backend**:
- Test output: work_unit/test-results.txt (45 tests passed)
- Coverage report: work_unit/coverage.html (89%)
- API documentation: /api/docs/ (Swagger UI)

## Known Issues

[If any issues found during verification]

- **Issue 1**: [Description]
  - Severity: [Low | Medium | High]
  - Impact: [What's affected]
  - Workaround: [If available]
  - Tracked in: [GitHub issue #123]

## Deployment Notes

**Environment Variables** (if needed):
```bash
REDIS_URL=redis://localhost:6379  # For Channels
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

**Dependencies Added**:
```bash
pip install channels channels-redis drf-spectacular
npm install htmx.org
```

**Database Migrations**:
```bash
python manage.py migrate  # Applies 2 new migrations
```

**Static Files**:
```bash
python manage.py collectstatic  # Collect Tailwind CSS
```

## Next Steps

[Optional improvements or follow-up work]

- [ ] Add email notifications (in addition to WebSocket)
- [ ] Implement notification preferences (user can choose channels)
- [ ] Add pagination to notification list (currently showing all)

---

*Delivered by: Claude (web-development plugin)*
*Frontend Agent: frontend-engineer (Tailwind + htmx + Chrome DevTools)*
*Backend Agent: backend-django (Django + DRF + Channels)*
```

## Deployment Readiness Assessment

### Production Checklist

```markdown
## Deployment Readiness

### Security
- [ ] CSRF protection enabled
- [ ] CORS configured (allowed origins specified)
- [ ] Authentication enforced on sensitive endpoints
- [ ] Input validation on all forms/APIs
- [ ] No secrets in code (use environment variables)
- [ ] HTTPS configured (WSS for WebSockets)

### Performance
- [ ] Database indexes on filtered/sorted fields
- [ ] Static files optimized (Tailwind purged)
- [ ] Images optimized (WebP, responsive sizes)
- [ ] Caching configured (Redis, browser caching)
- [ ] No N+1 queries (verified in tests)

### Reliability
- [ ] Error handling comprehensive
- [ ] Logging configured (errors, warnings)
- [ ] Tests pass (100% pass rate)
- [ ] Coverage acceptable (>80%)
- [ ] Health check endpoint available

### Monitoring
- [ ] Performance metrics tracked (Core Web Vitals)
- [ ] Error tracking configured (Sentry, etc.)
- [ ] WebSocket connection monitoring (if applicable)
- [ ] Database query performance monitoring

### Documentation
- [ ] API documentation complete (OpenAPI/Swagger)
- [ ] Deployment guide written
- [ ] Environment variables documented
- [ ] Known issues documented

**Deployment Readiness**: ✅ READY / ⚠️ READY WITH NOTES / ❌ NOT READY

**Blockers** (if not ready):
- [Item 1]: [What needs to be done]
- [Item 2]: [What needs to be done]
```

## Cleanup and Archival

### Move to Archives

```bash
# Archive work unit
mv .workspace/work/web/[task-slug]/ .workspace/work/archives/web-[task-slug]-2025-10-16/

# Update ACTIVE_WORK pointer (if this was active)
# [Handled automatically by framework]
```

### Git Commit (Optional)

```markdown
## Git Status

**Files Changed**:
- templates/base.html
- accounts/views.py
- accounts/serializers.py
- accounts/tests/test_profiles.py
- static/css/output.css

**Commit Message**:
```
feat: Add user profile API and responsive navbar

- Add Profile model with bio, avatar, website fields
- Create ProfileViewSet with CRUD operations
- Add responsive navbar (mobile hamburger + desktop horizontal)
- Implement real-time notifications via WebSocket
- Add comprehensive tests (45 tests, 89% coverage)
- Verify with Chrome DevTools (LCP 1.8s, no errors)

Tests: All passing
Verification: Chrome DevTools + pytest
Deployment: Ready for production

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**Commit command**:
```bash
git add templates/ accounts/ static/
git commit -m "$(cat work_unit/commit-message.txt)"
```
```

## Example Deliveries

### Example 1: Frontend-Only Delivery

```markdown
# Delivery: Responsive Navbar

**Status**: ✅ READY FOR PRODUCTION
**Time**: 1.5 hours
**Agent**: frontend-engineer

## What Was Built

Fully responsive navigation:
- Mobile: DaisyUI drawer with hamburger menu
- Tablet: Collapsed to hamburger at <1024px
- Desktop: Horizontal navigation bar

**Files Modified**:
- templates/base.html (added responsive navbar)

## Verification

**Chrome DevTools**:
- ✅ Mobile (375x667): Hamburger visible, drawer works
- ✅ Tablet (768x1024): Transition smooth
- ✅ Desktop (1920x1080): Horizontal nav displays
- ✅ Console: No errors
- ✅ Performance: LCP 1.2s (excellent)

**Accessibility**:
- ✅ Keyboard navigation works
- ✅ ARIA labels on hamburger button
- ✅ Semantic HTML (nav element)

## Deployment

**No dependencies**: Works with existing Tailwind + DaisyUI setup
**No migrations**: Frontend-only change
**Deploy**: Just deploy updated template

**Status**: ✅ READY FOR PRODUCTION
```

### Example 2: Backend-Only Delivery

```markdown
# Delivery: User Profile REST API

**Status**: ✅ READY FOR PRODUCTION
**Time**: 3.5 hours
**Agent**: backend-django

## What Was Built

Complete CRUD API for user profiles:
- GET /api/profiles/ - List profiles (paginated)
- GET /api/profiles/{id}/ - Retrieve profile
- PUT /api/profiles/{id}/ - Update own profile
- GET /api/profiles/me/ - Current user's profile

**Files Created/Modified**:
- accounts/models.py: Profile model
- accounts/serializers.py: ProfileSerializer
- accounts/views.py: ProfileViewSet
- accounts/tests/test_profiles.py: 20 tests

## Verification

**Tests**:
```
45 tests passed, 0 failed
Coverage: 89%
```

**Security**:
- ✅ Authentication required
- ✅ Users can only modify own profiles
- ✅ CSRF protection active
- ✅ Input validation enforced

**API Documentation**:
- ✅ OpenAPI schema generated
- ✅ Swagger UI available at /api/docs/
- ✅ Example requests documented

## Deployment

**Dependencies**:
```bash
pip install djangorestframework drf-spectacular
```

**Migrations**:
```bash
python manage.py migrate  # Applies accounts.0002_profile
```

**Environment Variables**: None required

**Status**: ✅ READY FOR PRODUCTION
```

### Example 3: Full-Stack Delivery

```markdown
# Delivery: Real-time Notification System

**Status**: ⚠️ READY WITH NOTES
**Time**: 11.5 hours over 2 days
**Agents**: backend-django, frontend-engineer

## What Was Built

Complete real-time notification system:

**Backend** (backend-django):
- Notification model (message, user, is_read, timestamp)
- WebSocket consumer (Django Channels)
- REST API (/api/notifications/)
- Real-time delivery via WebSocket

**Frontend** (frontend-engineer):
- WebSocket client (htmx ws extension)
- Notification dropdown UI (DaisyUI)
- Unread count badge
- Toast popups for new notifications

## Verification

**Backend Tests**:
```
45 tests passed, 0 failed
Coverage: 91%
WebSocket tests: 8 passed
```

**Frontend Verification**:
- ✅ WebSocket connection established (Chrome DevTools network tab)
- ✅ Notifications display in real-time
- ✅ Mark as read works
- ✅ Unread count badge updates
- ✅ Responsive on mobile and desktop
- ✅ Performance: LCP 2.1s

**Integration**:
- ✅ End-to-end test: Backend sends → Frontend receives
- ✅ Mark as read: Frontend → Backend → Database updated

## Known Issues

**Issue 1**: WebSocket disconnects after 5 minutes of inactivity
- Severity: Low
- Impact: Users must refresh page to reconnect
- Workaround: Implement heartbeat ping/pong (TODO)
- Tracked in: GitHub issue #42

## Deployment

**Dependencies**:
```bash
pip install channels channels-redis
npm install htmx.org
```

**Infrastructure**:
- Redis required for channel layer
- ASGI server (Daphne or Uvicorn)
- WebSocket support (Nginx config)

**Environment Variables**:
```bash
REDIS_URL=redis://localhost:6379
CHANNEL_LAYERS_BACKEND=channels_redis.core.RedisChannelLayer
```

**Migrations**:
```bash
python manage.py migrate  # Applies notifications.0001_initial
```

**Deployment Steps**:
1. Install Redis: `docker run -d redis`
2. Apply migrations
3. Configure ASGI server
4. Update Nginx for WebSocket (ws:// → wss://)
5. Deploy static files (htmx.js)

**Status**: ⚠️ READY WITH NOTES
**Note**: Requires Redis infrastructure. WebSocket heartbeat improvement recommended but not blocking.
```

## Final Output

After all verification complete:

```markdown
# 🚀 Web Development Delivery Complete

**Work Unit**: [task-name]
**Classification**: [Frontend | Backend | Full-stack]
**Time**: [X] hours
**Status**: ✅ READY FOR PRODUCTION

## Summary
[Brief description of what was built]

## Verification
- Frontend: ✅ Chrome DevTools verified
- Backend: ✅ All tests pass (45/45, 89% coverage)
- Integration: ✅ End-to-end tested

## Deployment
**Readiness**: ✅ READY / ⚠️ READY WITH NOTES / ❌ NOT READY
**Documentation**: delivery-summary.md

## Next Steps
1. Review delivery-summary.md
2. Deploy to staging environment
3. Run smoke tests
4. Deploy to production

---

Work unit archived to: .workspace/work/archives/web-[task-slug]-2025-10-16/

**Want to deploy now?** Review deployment notes in delivery-summary.md
```

## Notes

- **Comprehensive verification** - Don't skip checks
- **Evidence required** - Screenshots, test output, performance metrics
- **Document issues** - Known issues better than hidden issues
- **Deployment-ready** - Provide all information needed to deploy
- **Archive properly** - Preserve work history

---

*Web Ship Command - Comprehensive Delivery and Verification*
*Version 1.0.0*
