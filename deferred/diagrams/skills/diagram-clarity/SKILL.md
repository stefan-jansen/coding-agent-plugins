---
name: diagram-clarity
description: Clarity and simplicity principles for effective diagrams. Focus on essential elements, minimize visual noise, maintain consistency, and use single abstraction levels. Ensures diagrams communicate clearly without clutter.
---

# Diagram Clarity - Simplicity and Communication Principles

**Purpose**: Ensure diagrams communicate clearly through simplicity and consistency
**Core Principle**: Simplicity over complexity - model key components, not every detail
**Goal**: Viewers understand quickly without confusion

---

## Fundamental Principles

### 1. Simplicity Over Complexity

**Rule**: Model key components at a single abstraction level

**Why**: Diagrams are for understanding, not comprehensive documentation
- Focus on essential elements only
- Use multiple diagrams if needed (don't cram everything into one)
- Each diagram should answer one question or show one aspect

**In Practice**:
```d2
# GOOD: Focus on data flow
user -> app: requests
app -> database: queries
database -> app: results
app -> user: responses

# BAD: Mixing abstractions
user -> app.frontend.component.method() -> app.backend.api.endpoint.handler() -> ...
```

### 2. Consistency

**Rule**: Same visual treatment = same meaning; visual differences must be meaningful

**Why**: Viewers learn patterns; inconsistency creates confusion

**Apply**:
- Same connection type = same relationship type
- Same color = same category/status
- Same shape = same component type
- Same size = same importance level

### 3. Minimal Visual Noise

**Rule**: Limit colors, simplify shapes, avoid unnecessary styling

**Why**: Every visual element should add information, not decoration

**Limits**:
- **Colors**: 2-3 accent colors + theme defaults
- **Shapes**: Use D2 standard shapes, customize only when needed
- **Styles**: Use theme, override sparingly
- **Connections**: 2-3 arrow types maximum

---

## Clarity Technique 1: Limit Colors

**Principle**: 2-3 colors maximum (plus theme defaults)

### In D2:

**Strategic color use**:
```d2
classes: {
  # Color 1: Critical path
  critical: {
    style.fill: "#FF5722"
    style.stroke: "#D32F2F"
  }

  # Color 2: Normal components (use theme)
  # Let theme handle this

  # Color 3: External/supporting
  external: {
    style.fill: "#90A4AE"
    style.stroke: "#607D8B"
  }
}

# Apply consistently
payment-gateway.class: critical
auth-service.class: critical

# No class = theme default for normal components
user-service
data-service

external-api.class: external
third-party.class: external
```

**Color meanings** (be consistent):
- **Red/Orange**: Critical, errors, warnings, bottlenecks
- **Blue** (theme): Normal services, primary components
- **Gray**: External, less important, infrastructure
- **Green**: Optional - healthy/success states

### Guidelines:

✅ **Limit to 2-3 accent colors**
✅ **Let theme provide base colors**
✅ **Consistent color = consistent meaning**
✅ **Color must add information (not decoration)**
❌ **Don't use colors randomly**
❌ **Don't use rainbow palette**

---

## Clarity Technique 2: Appropriate Shapes

**Principle**: Use standard shapes, customize only when it adds meaning

### In D2:

**Use semantic shapes**:
```d2
# People
users.shape: person
admin.shape: person

# Data stores
database.shape: cylinder
cache.shape: cylinder

# Message passing
queue.shape: queue
event-bus.shape: queue

# Processes
worker.shape: step
pipeline.shape: step

# Cloud/network
cloud-storage.shape: cloud
api-gateway.shape: hexagon

# Default rectangle for services (don't specify)
auth-service  # Rectangle by default
data-service  # Rectangle by default
```

**Avoid over-customization**:
```d2
# GOOD: Standard shapes
api.shape: hexagon
db.shape: cylinder

# BAD: Custom shapes without meaning
api.shape: parallelogram  # Why? No semantic value
db.shape: diamond  # Confusing
```

### Guidelines:

✅ **Use semantic shapes** (cylinder=database, person=user, etc.)
✅ **Rectangle default** for generic services/components
✅ **Shape differences must be meaningful**
❌ **Don't customize shapes for decoration**
❌ **Don't use exotic shapes without reason**

---

## Clarity Technique 3: Consistent Connection Types

**Principle**: Same arrow type = same relationship type

### In D2:

**Define relationship types**:
```d2
# API calls - solid arrow
client -> server
server -> database

# Data flow - solid arrow
input -> process
process -> output

# Optional/conditional - dashed
service -- optional-cache: optional

# Bidirectional - when truly bidirectional
cache <-> service: read/write
```

**Avoid mixing without meaning**:
```d2
# BAD: Inconsistent
a -> b  # Why arrow?
c -- d  # Why line?
e <-> f  # Why bidirectional?
# No clear pattern

# GOOD: Consistent meaning
# All API calls use arrows
api-gateway -> auth-service
api-gateway -> data-service
auth-service -> database

# All dependencies use lines
service -- config
service -- secrets
```

### Guidelines:

✅ **Consistent arrow type for same relationship**
✅ **`->` for most directed flows** (API calls, data flow)
✅ **`--` for dependencies** (configs, optional components)
✅ **`<->` only when truly bidirectional** (cache read/write)
❌ **Don't mix arrow types randomly**
❌ **Don't use `<->` for everything** (loses meaning)

---

## Clarity Technique 4: Effective Grouping

**Principle**: Use containers to organize related elements

### In D2:

**Group by layer**:
```d2
frontend: Frontend Layer {
  ui
  components
  routing
}

backend: Backend Layer {
  api
  services
  middleware
}

data: Data Layer {
  database.shape: cylinder
  cache.shape: cylinder
}
```

**Group by domain**:
```d2
auth-domain: Authentication {
  login-service
  oauth-service
  token-manager
}

payment-domain: Payment {
  payment-gateway
  transaction-service
  fraud-detection
}
```

**Group by environment**:
```d2
production: Production {
  app-servers
  databases
}

staging: Staging {
  app-servers
  databases
}
```

### Guidelines:

✅ **Group related elements in containers**
✅ **Container names should be descriptive**
✅ **Max 2-3 nesting levels** (not deeper)
✅ **Consistent grouping criteria** (by layer OR by domain, not mixed)
❌ **Don't have flat structure** (everything at top level)
❌ **Don't over-nest** (too many levels)

---

## Clarity Technique 5: Clear, Concise Labels

**Principle**: Labels should be descriptive but brief

### In D2:

**Good labels**:
```d2
# Descriptive noun phrases
api: API Gateway
auth: Authentication Service
db: PostgreSQL Database

# Action verbs on connections
user -> api: HTTP requests
api -> db: SQL queries
db -> api: query results
```

**Avoid verbose labels**:
```d2
# BAD: Too wordy
api: The API Gateway Component That Handles All Incoming Requests

# GOOD: Concise
api: API Gateway

# BAD: Unclear
x: Thing
y: Stuff

# GOOD: Specific
auth: Auth Service
data: Data Service
```

**Connection labels**:
```d2
# GOOD: Brief but clear
frontend -> api: HTTPS
api -> database: SQL
cache -> api: cache hits

# BAD: Too detailed
frontend -> api: Makes HTTP requests over port 443 using TLS 1.3
```

### Guidelines:

✅ **Noun phrases for components** (API Gateway, User Service)
✅ **Action verbs for connections** (requests, queries, publishes)
✅ **1-4 words per label** (not sentences)
✅ **Specific and descriptive**
❌ **Don't write sentences in labels**
❌ **Don't use vague names** (thing, stuff, component)

---

## Clarity Technique 6: Single Abstraction Level

**Principle**: Each diagram should stay at one level of detail

### In D2:

**High-level system overview**:
```d2
# All at same abstraction - system level
user.shape: person
web-app
mobile-app
api
database.shape: cylinder

user -> web-app
user -> mobile-app
web-app -> api
mobile-app -> api
api -> database
```

**Detailed component view**:
```d2
# All at same abstraction - component level
api: API Layer {
  router
  middleware
  controllers
  validators
}

router -> middleware
middleware -> controllers
controllers -> validators
```

**Avoid mixing levels**:
```d2
# BAD: Mixed abstractions
system: System {
  user.shape: person
  frontend  # High level

  backend: Backend {
    express-app  # Implementation detail
    routes  # Code level
    controllers  # Code level
    models  # Code level
  }

  postgres-database-version-14.2  # Too specific
}

# Frontend is high-level, backend is code-level, database is version-level
# Confusing!
```

### Guidelines:

✅ **Choose one abstraction level per diagram**
✅ **System level**: Components, not code
✅ **Component level**: Modules, not functions
✅ **Use multiple diagrams for different levels**
❌ **Don't mix system-level and code-level in same diagram**
❌ **Don't show implementation details in architecture diagrams**

---

## Clarity Technique 7: Meaningful Icon Usage

**Principle**: Icons must add semantic meaning, not just decoration

### In D2:

**Good icon usage**:
```d2
# Icons clarify component type
users.shape: person
database: PostgreSQL {
  shape: cylinder
  icon: https://icons.terrastruct.com/tech/postgresql.svg
}

kubernetes: K8s Cluster {
  icon: https://icons.terrastruct.com/tech/kubernetes.svg
}

# Icon adds information about technology
redis: Cache {
  shape: cylinder
  icon: https://icons.terrastruct.com/tech/redis.svg
}
```

**Avoid decorative icons**:
```d2
# BAD: Icons on everything, no added meaning
service1: Service {
  icon: https://some-random-icon.svg  # Why this icon?
}

service2: Service {
  icon: https://another-random-icon.svg  # Just decoration
}

# GOOD: Icons only where they add information
auth: Auth Service  # No icon needed - clear from label

postgres: Database {
  shape: cylinder
  icon: https://icons.terrastruct.com/tech/postgresql.svg  # Shows it's PostgreSQL
}
```

### Guidelines:

✅ **Use icons to show technology** (PostgreSQL, Redis, Kubernetes)
✅ **Use person icon for users/actors**
✅ **Icons should clarify, not decorate**
✅ **Consistent icon style** (from same library)
❌ **Don't add icons everywhere**
❌ **Don't use icons that don't add information**

---

## Clarity Technique 8: Avoid Over-Styling

**Principle**: Use theme, override sparingly

### In D2:

**Prefer themes**:
```bash
# Use built-in themes for professional look
d2 --theme=200 diagram.d2 output.svg
```

**Override only when needed**:
```d2
# GOOD: Minimal custom styling for critical elements
critical-path: Bottleneck {
  style.fill: "#FF5722"  # Only override to show problem
  style.stroke: "#D32F2F"
}

# Rest use theme defaults
service1
service2
service3
```

**Avoid excessive customization**:
```d2
# BAD: Over-styled
service: Service {
  style.fill: "#CUSTOM1"
  style.stroke: "#CUSTOM2"
  style.font-color: "#CUSTOM3"
  style.font-size: 17
  style.border-radius: 12
  style.shadow: true
  style.3d: true
  style.opacity: 0.85
  # Too much!
}

# GOOD: Let theme handle it
service: Service {
  # Theme provides professional defaults
}
```

### Guidelines:

✅ **Use built-in themes** (professional, consistent)
✅ **Override only for critical elements** (errors, warnings, emphasis)
✅ **Use classes for consistent custom styles**
❌ **Don't customize every element**
❌ **Don't mix too many custom styles**

---

## Clarity Checklist

**Before finalizing, verify**:

- [ ] **Colors limited**: 2-3 accent colors + theme?
- [ ] **Shapes semantic**: Appropriate for component types?
- [ ] **Connections consistent**: Same type = same meaning?
- [ ] **Grouped logically**: Related elements in containers?
- [ ] **Labels clear**: Concise and descriptive?
- [ ] **Single abstraction**: One level of detail throughout?
- [ ] **Icons meaningful**: Add information, not decoration?
- [ ] **Minimal styling**: Theme-based, not over-customized?
- [ ] **No clutter**: Every element serves a purpose?
- [ ] **Quick to understand**: Viewer gets it in <30 seconds?

---

## Common Clarity Mistakes

### Mistake 1: Too Many Elements

**Problem**: Trying to show everything in one diagram

```d2
# BAD: Information overload
# 50+ elements, 100+ connections, impossible to parse
```

**Solution**: Use multiple focused diagrams

```d2
# Diagram 1: High-level architecture (5-10 components)
# Diagram 2: Authentication flow (8 components)
# Diagram 3: Data layer detail (6 components)
```

### Mistake 2: Inconsistent Styling

**Problem**: Visual differences without meaning

```d2
# BAD: Random styling
a: { style.fill: "#FF0000" }
b: { style.fill: "#00FF00" }
c: { style.fill: "#FF0000" }  # Same as 'a' but unrelated
d: { style.fill: "#0000FF" }
```

**Solution**: Consistent styling = consistent meaning

```d2
classes: {
  critical: { style.fill: "#FF5722" }
  normal: {}  # Use theme
}

a.class: critical
c.class: critical  # Same class = same meaning
b  # Theme default
d  # Theme default
```

### Mistake 3: Unclear Labels

**Problem**: Vague or overly technical labels

```d2
# BAD
svc1: Svc
comp_auth_v2: CAUTHV2
x: Thing

# GOOD
auth-service: Authentication Service
database: User Database
api: Public API
```

### Mistake 4: No Grouping

**Problem**: Flat structure, hard to understand relationships

```d2
# BAD: All at top level
web; mobile; api; auth; data; analytics; postgres; redis; s3; logging; metrics

# GOOD: Grouped
clients: { web; mobile }
services: { api; auth; data; analytics }
storage: { postgres; redis; s3 }
observability: { logging; metrics }
```

---

## Multiple Diagrams > One Complex Diagram

**When to split**:
- Diagram has >15 components (getting complex)
- Multiple concerns/aspects being shown
- Different audiences need different views
- Single diagram takes >1 minute to understand

**How to split**:
```d2
# Overview diagram: High-level (5-8 components)
overview.d2: System architecture

# Detail diagrams: Focused views
auth-flow.d2: Authentication flow
data-layer.d2: Data architecture
deployment.d2: Deployment topology
```

**Benefits**:
- Each diagram has clear purpose
- Easier to understand
- Different abstraction levels
- Can show to different audiences

---

## Research-Based Guidelines

**Studies show**:
- **Simplicity**: Diagrams with 5-10 elements understood fastest
- **Consistency**: Viewers learn patterns; inconsistency slows comprehension
- **Grouping**: Containers improve understanding by organizing information
- **Abstraction**: Single level = faster understanding; mixed levels = confusion

**Apply to D2**:
- Keep diagrams to 5-15 elements
- Use consistent styling (classes, themes)
- Group with containers
- Stay at one abstraction level

---

*This skill provides clarity principles. Combine with d2-syntax (language) and diagram-hierarchy (visual hierarchy) for professional, clear diagrams.*
