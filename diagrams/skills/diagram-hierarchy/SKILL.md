---
name: diagram-hierarchy
description: Visual hierarchy principles for effective diagrams. Use size, color, placement, and typography to guide the viewer's eye and communicate importance. Increases understanding by up to 73%. Apply to all diagrams for clarity.
---

# Diagram Hierarchy - Visual Design Principles

**Purpose**: Create visual hierarchy in diagrams to communicate importance and guide the viewer's eye
**Research**: Visual hierarchy increases understanding by up to 73%
**Core Principle**: Most important elements carry the biggest visual weight

---

## What is Visual Hierarchy?

**Definition**: Guiding the eye through the diagram so it attends to different elements in order of their importance

**Why It Matters**:
- Helps viewers understand quickly what's most important
- Creates clear reading order and flow
- Reduces cognitive load
- Makes complex systems easier to comprehend

**How to Create It**: Variations in size, color, placement, typography, and spacing

---

## Technique 1: Size and Scale

**Principle**: Important elements should be larger

### In D2 Diagrams:

**Use larger shapes for key components**:
```d2
# Important: API Gateway (entry point)
gateway: API Gateway {
  width: 200
  height: 100
}

# Less important: Individual services
auth: Auth {
  width: 120
  height: 80
}

data: Data {
  width: 120
  height: 80
}
```

**Size relationships communicate importance**:
- **Large**: Primary components, entry points, key systems
- **Medium**: Secondary services, supporting components
- **Small**: Utilities, helpers, peripheral elements

**Font size for labels**:
```d2
# Critical component - larger text
gateway: API GATEWAY {
  style.font-size: 20
  style.bold: true
}

# Regular components - standard text
service: Service {
  style.font-size: 14
}

# Details - smaller text
util: utility {
  style.font-size: 12
}
```

### Guidelines:

✅ **Make entry points and primary components 30-50% larger**
✅ **Use 2-3 size levels (not more)**
✅ **Size differences should be obvious (not subtle)**
❌ **Don't make everything the same size (no hierarchy)**
❌ **Don't use too many size levels (creates chaos)**

---

## Technique 2: Color and Contrast

**Principle**: Strategic color use attracts attention and shows relationships

### In D2 Diagrams:

**Limit colors to 2-3 + theme defaults**:
```d2
# Use theme as base, accent strategically
classes: {
  # Critical path - bold color
  critical: {
    style.fill: "#FF5722"
    style.stroke: "#D32F2F"
    style.font-color: "#FFFFFF"
  }

  # Primary components - theme color
  primary: {
    style.fill: "#2196F3"
    style.stroke: "#1976D2"
  }

  # Secondary - muted
  secondary: {
    style.fill: "#B0BEC5"
    style.stroke: "#78909C"
  }
}

api-gateway.class: critical
auth-service.class: primary
data-service.class: primary
logger.class: secondary
metrics.class: secondary
```

**Contrast for emphasis**:
```d2
# Problem area - high contrast red
bottleneck: Bottleneck {
  style.fill: "#F44336"
  style.stroke: "#C62828"
  style.font-color: "#FFFFFF"
  style.bold: true
}

# Normal components - low contrast
normal-service: Service {
  # Use theme defaults (subtle)
}
```

**Color meanings** (be consistent):
- **Red/Orange**: Critical path, problems, warnings
- **Blue**: Primary components, services
- **Green**: Success states, healthy systems
- **Gray**: Supporting, less important

### Guidelines:

✅ **Limit to 2-3 accent colors plus theme**
✅ **High contrast for critical elements**
✅ **Consistent color = consistent meaning**
✅ **Use theme colors for most elements (don't over-color)**
❌ **Don't use many colors (creates visual noise)**
❌ **Don't use color without meaning (must signify something)**

---

## Technique 3: Typography

**Principle**: Text size and weight communicate importance levels

### In D2 Diagrams:

**Use 2-3 typography levels**:
```d2
# Level 1: System/Container titles (largest, bold)
system: PRODUCTION SYSTEM {
  style.font-size: 20
  style.bold: true
  style.text-transform: uppercase
}

# Level 2: Component names (medium)
api: API Gateway {
  style.font-size: 16
  style.bold: true
}

# Level 3: Details (smallest)
config: config.yaml {
  style.font-size: 12
  style.italic: true
}
```

**Bold for emphasis**:
```d2
# Important service - bold
auth: Authentication Service {
  style.bold: true
}

# Supporting service - regular
logging: Logging {
  # Default weight
}
```

### Guidelines:

✅ **2-3 text sizes (not more)**
✅ **Bold for important elements**
✅ **UPPERCASE for top-level containers (sparingly)**
✅ **Consistent typography across similar elements**
❌ **Don't use many font sizes (creates chaos)**
❌ **Don't overuse bold (loses impact)**

---

## Technique 4: Placement and Position

**Principle**: Dominant positions for key elements

### In D2 Diagrams:

**Top-left = highest importance** (Western reading pattern):
```d2
direction: down

# Most important at top
user: User {
  shape: person
}

# Entry point next
frontend: Frontend

# Then supporting layers
backend: Backend
database: Database

user -> frontend -> backend -> database
```

**Center = focal point**:
```d2
# Center key component in layout
network: {
  # Peripheral services
  auth
  data
  analytics

  # Central component
  gateway: API Gateway {
    # Let layout engine center it naturally
  }

  auth -> gateway
  data -> gateway
  analytics -> gateway
}
```

**Use near positioning (TALA)** for precise hierarchy:
```d2
# Primary component
main-api: Main API

# Secondary component near primary
cache: Cache {
  near: main-api
}

# Supporting component at edge
monitoring: Monitoring {
  near: top-right
}
```

### Guidelines:

✅ **Top-left or center for most important elements**
✅ **Flow follows reading pattern (left-to-right, top-to-bottom)**
✅ **Group related items together (proximity = relationship)**
❌ **Don't scatter important elements randomly**
❌ **Don't ignore natural reading flow**

---

## Technique 5: White Space and Balance

**Principle**: Breathing room helps elements stand out

### In D2 Diagrams:

**Use containers to create white space**:
```d2
# Container creates visual separation
frontend: Frontend Layer {
  ui
  components
  routing
}

# Space between containers
backend: Backend Layer {
  api
  services
  middleware
}

# Not: All elements at same level (cramped)
```

**Avoid overcrowding**:
```d2
# GOOD: Grouped with space
system: {
  direction: right

  clients: Clients {
    web
    mobile
  }

  services: Services {
    auth
    data
  }
}

# BAD: Too many ungrouped elements
# web; mobile; auth; data; api; db; cache; queue; etc...
```

**Balance element density**:
```d2
# Left side - detailed
detailed-system: {
  component-a
  component-b
  component-c
  a -> b -> c
}

# Right side - simpler (balance)
external: External API {
  # Just the interface
}

detailed-system.c -> external
```

### Guidelines:

✅ **Use containers to create separation**
✅ **Balance detailed and simple areas**
✅ **Leave room around important elements**
❌ **Don't cram everything together**
❌ **Don't have all areas equally dense**

---

## Technique 6: Grouping and Containers

**Principle**: Visual grouping shows relationships and creates hierarchy

### In D2 Diagrams:

**Container hierarchy** (levels of importance):
```d2
# Top level: System (most important)
production: PRODUCTION ENVIRONMENT {
  style.font-size: 18
  style.bold: true

  # Second level: Layers (important)
  application: Application {
    style.font-size: 16

    # Third level: Components (normal)
    api: API
    workers: Workers
    scheduler: Scheduler
  }

  data: Data Layer {
    style.font-size: 16

    postgres
    redis
    s3
  }
}
```

**Visual differentiation of containers**:
```d2
classes: {
  # Top-level containers - distinctive
  system-container: {
    style.stroke: "#1976D2"
    style.stroke-width: 3
    style.fill: "#E3F2FD"
  }

  # Sub-containers - subtle
  sub-container: {
    style.stroke: "#90CAF9"
    style.stroke-width: 1
    style.fill: "#F5F5F5"
  }
}

production.class: system-container
production.application.class: sub-container
production.data.class: sub-container
```

### Guidelines:

✅ **Use nesting to show hierarchy (parent-child relationships)**
✅ **Visual distinction between container levels**
✅ **Group related elements together**
❌ **Don't over-nest (max 2-3 levels)**
❌ **Don't mix unrelated elements in same container**

---

## Applying Multiple Techniques Together

**Combine techniques for maximum hierarchy**:

```d2
direction: down

# Apply ALL hierarchy techniques to critical component
api-gateway: API GATEWAY {
  # Size - larger than others
  width: 250
  height: 120

  # Color - distinctive
  style.fill: "#FF5722"
  style.stroke: "#D32F2F"
  style.font-color: "#FFFFFF"

  # Typography - bold, larger
  style.font-size: 20
  style.bold: true
  style.text-transform: uppercase

  # Icon for emphasis
  icon: https://icons.terrastruct.com/tech/gateway.svg
}

# Secondary components use fewer techniques
auth: Auth Service {
  # Smaller
  width: 150
  height: 80

  # Theme default color

  # Normal typography
  style.font-size: 14

  icon: https://icons.terrastruct.com/tech/auth.svg
}

data: Data Service {
  width: 150
  height: 80
  style.font-size: 14
  icon: https://icons.terrastruct.com/tech/database.svg
}

# Utilities - minimal styling
logger: logger {
  # Small, default everything
}
```

---

## Hierarchy Checklist

**Before finalizing diagram, verify**:

- [ ] **Size**: Important elements 30-50% larger?
- [ ] **Color**: Limited to 2-3 accent colors + theme?
- [ ] **Typography**: 2-3 text sizes used consistently?
- [ ] **Placement**: Key elements in dominant positions?
- [ ] **White Space**: Adequate separation and balance?
- [ ] **Grouping**: Related elements in containers?
- [ ] **Clear focal point**: Eye knows where to start?
- [ ] **Reading flow**: Natural progression through diagram?

---

## Common Hierarchy Mistakes

### Mistake 1: Everything Same Size

**Problem**: No visual hierarchy, all elements compete for attention

```d2
# BAD: All same size
gateway
auth
data
cache
logger
metrics
```

**Solution**: Vary sizes based on importance

```d2
# GOOD: Size hierarchy
gateway: API Gateway {
  width: 200
  height: 100
}

auth: Auth { width: 120; height: 80 }
data: Data { width: 120; height: 80 }

cache: cache
logger: logger
```

### Mistake 2: Too Many Colors

**Problem**: Visual noise, unclear meaning

```d2
# BAD: Rainbow diagram
a: { style.fill: "#FF0000" }
b: { style.fill: "#00FF00" }
c: { style.fill: "#0000FF" }
d: { style.fill: "#FFFF00" }
e: { style.fill: "#FF00FF" }
```

**Solution**: Limit colors, use consistently

```d2
# GOOD: 2 accent colors + theme
classes: {
  critical: { style.fill: "#FF5722" }
  normal: { style.fill: "#2196F3" }
}

a.class: critical  # Important
b.class: normal
c.class: normal
d.class: normal
```

### Mistake 3: No Grouping

**Problem**: Flat structure, hard to parse

```d2
# BAD: Everything at same level
web; mobile; api; auth; data; analytics; postgres; redis; s3
```

**Solution**: Use containers for hierarchy

```d2
# GOOD: Grouped hierarchy
clients: { web; mobile }
services: { api; auth; data; analytics }
storage: { postgres; redis; s3 }
```

---

## Research-Based Guidelines

**Studies show**:
- Visual hierarchy increases understanding by **up to 73%**
- Viewers process **size first**, then **color**, then **position**
- **2-3 levels** of visual hierarchy is optimal (more creates confusion)
- **Consistent application** of hierarchy rules improves retention

**Apply to D2**:
- Use size variations (width/height)
- Use strategic color (limit to 2-3 + theme)
- Use positioning (near, top-left priority)
- Use typography (2-3 sizes, bold for emphasis)

---

*This skill provides visual hierarchy principles. Combine with d2-syntax (language) and diagram-clarity (simplicity) for professional, effective diagrams.*
