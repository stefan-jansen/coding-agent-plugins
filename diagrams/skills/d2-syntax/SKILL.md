---
name: d2-syntax
description: Complete D2 language reference for creating diagrams. Covers shapes, connections, containers, special types (SQL tables, sequences), icons, styling, and advanced features. Use for all D2 diagram generation tasks.
---

# D2 Syntax - Complete Language Reference

**Purpose**: Comprehensive D2 language knowledge for generating high-quality diagrams
**D2**: Declarative diagram language - describe what to diagram, D2 generates the image

---

## Core Concepts

**Declarative Approach**: You describe what you want diagrammed, not how to render it
**File Format**: `.d2` text files compile to SVG/PNG via `d2` CLI
**Philosophy**: Simple syntax, powerful layouts, professional themes

---

## Basic Syntax

### Shapes and Nodes

**Simple shapes**:
```d2
# Define a shape (creates rectangle by default)
server
database
cache

# With labels
server: Web Server
database: PostgreSQL
cache: Redis
```

**Shape types** (via `.shape` property):
- `rectangle` (default)
- `square`
- `circle`
- `oval`
- `diamond`
- `parallelogram`
- `hexagon`
- `cloud`
- `cylinder` (for databases)
- `queue` (for message queues)
- `package`
- `step` (for processes)
- `callout`
- `stored_data`
- `person`
- `document`
- `multiple_document`

**Example**:
```d2
users.shape: person
database.shape: cylinder
queue.shape: queue
api.shape: hexagon
```

### Connections

**Connection operators**:
- `->` Forward arrow
- `<-` Reverse arrow
- `<->` Bidirectional arrow
- `--` Straight line (no arrow)

**Basic connections**:
```d2
client -> server
server -> database
cache <-> server
api -- gateway
```

**Labeled connections**:
```d2
client -> server: HTTP requests
server -> database: SQL queries
cache <-> server: get/set
```

**Connection styling**:
```d2
a -> b: {
  style.stroke: "#ff0000"
  style.stroke-width: 3
  style.stroke-dash: 5
}
```

### Labels and Text

**Node labels**:
```d2
# Simple label
node: Label Text

# Multiline label (using \n or |)
node: |md
  # Heading
  Description line 1
  Description line 2
|
```

**Markdown in labels** (use `|md` for markdown):
```d2
explanation: |md
  # Overview
  - Point 1
  - Point 2

  **Bold** and *italic*
|
```

### Comments

```d2
# This is a comment
# Comments start with #

server -> database  # Inline comments work too
```

---

## Containers and Composition

**Containers organize related elements**:

```d2
# Container with elements
network: {
  server
  database
  cache

  server -> database
  server -> cache
}

# Nested containers
datacenter: {
  network: {
    web
    api
  }

  storage: {
    database
    backup
  }
}
```

**Container labels**:
```d2
system: System Architecture {
  frontend
  backend
}
```

**Connections between containers**:
```d2
frontend.ui -> backend.api
datacenter.network.web -> datacenter.storage.database
```

---

## Special Object Types

### SQL Tables

**sql_table shape**:
```d2
users: {
  shape: sql_table

  # Columns: name {constraint}: type
  id {primary_key}: int
  username {unique}: varchar
  email: varchar
  created_at: timestamp
}

posts: {
  shape: sql_table

  id {primary_key}: int
  user_id {foreign_key}: int
  title: varchar
  content: text
}

# Foreign key connection
posts.user_id -> users.id
```

**Constraint abbreviations**:
- `PK` or `primary_key`
- `FK` or `foreign_key`
- `UNQ` or `unique`

### UML Classes

**class shape**:
```d2
Animal: {
  shape: class

  # Fields
  +name: string
  -age: int
  #species: string

  # Methods
  +makeSound(): void
  +move(): void
}

Dog: {
  shape: class
  +bark(): void
}

# Inheritance
Dog -> Animal
```

**Visibility modifiers**:
- `+` public
- `-` private
- `#` protected
- `~` package

### Sequence Diagrams

**Sequence diagrams show temporal flow**:
```d2
shape: sequence_diagram

alice -> bob: Authentication Request
bob -> alice: Authentication Response

alice -> bob: Another authentication Request
alice <- bob: Another authentication Response
```

### Grid Layouts

**Grid layouts organize content in rows/columns**:
```d2
my-grid: {
  shape: grid

  row1: {
    a
    b
    c
  }

  row2: {
    d
    e
    f
  }
}
```

---

## Icons and Images

### Using Icons

**From icons.terrastruct.com**:
```d2
server: Web Server {
  icon: https://icons.terrastruct.com/tech/server.svg
}

database: PostgreSQL {
  icon: https://icons.terrastruct.com/tech/postgresql.svg
}

# Common tech icons available:
# - aws/*, gcp/*, azure/*
# - tech/* (kubernetes, docker, redis, etc.)
# - dev/* (github, gitlab, vscode, etc.)
```

**Local images**:
```d2
logo: {
  icon: ./images/company-logo.png
}
```

**Icon-only shapes** (shape: image):
```d2
kubernetes-icon: {
  shape: image
  icon: https://icons.terrastruct.com/tech/kubernetes.svg
}
```

**Icon placement**:
- Containers: Top-left corner
- Non-containers: Centered in shape

---

## Styling

### Style Properties

**Available properties**:
- `opacity`: 0.0 to 1.0
- `stroke`: Border color (CSS color, hex, or gradient)
- `fill`: Fill color
- `stroke-width`: Border thickness
- `stroke-dash`: Dashed border (number or pattern)
- `border-radius`: Rounded corners
- `shadow`: Drop shadow (boolean)
- `3d`: 3D effect (rectangles/squares only)
- `multiple`: Multiple shape effect
- `double-border`: Double border (rectangles/ovals)
- `font`: Font family
- `font-size`: Text size
- `font-color`: Text color
- `bold`, `italic`, `underline`: Text styling
- `text-transform`: none, uppercase, lowercase, capitalize
- `animated`: Animate connections

### Applying Styles

**Inline styling**:
```d2
server: {
  style.fill: "#4CAF50"
  style.stroke: "#2E7D32"
  style.font-color: "#FFFFFF"
  style.shadow: true
}
```

**Connection styling**:
```d2
a -> b: {
  style.stroke: "#FF5722"
  style.stroke-width: 3
  style.animated: true
}
```

**Classes (reusable styles)**:
```d2
classes: {
  primary: {
    style.fill: "#2196F3"
    style.stroke: "#1976D2"
    style.font-color: "#FFFFFF"
  }

  secondary: {
    style.fill: "#FFC107"
    style.stroke: "#FFA000"
  }
}

# Apply class
button.class: primary
header.class: primary
footer.class: secondary
```

**Global styling (globs)**:
```d2
*.style.font-size: 16
*.style.border-radius: 8
```

---

## Themes

**Built-in themes** (via CLI flag `-t` or `--theme`):
```bash
d2 --theme 0 input.d2 output.svg   # Neutral default
d2 --theme 200 input.d2 output.svg # Grape soda
d2 --theme 300 input.d2 output.svg # Mixed berry blue
```

**Popular themes**:
- `0-7`: Neutral themes
- `100-107`: Cool blue themes
- `200-207`: Grape/purple themes
- `300-307`: Mixed berry themes
- `400-407`: Vanilla/warm themes

**Theme in diagram** (vars block):
```d2
vars: {
  d2-config: {
    theme-id: 200
  }
}
```

**Dark mode**:
```d2
vars: {
  d2-config: {
    dark-theme-id: 200
  }
}
```

---

## Layouts

**Layout engines** (via CLI flag `--layout` or env var):
- `dagre` (default): Fast, hierarchical
- `elk`: Better for complex graphs, fewer edge crossings
- `tala`: Newest, designed for software architecture diagrams

**Set layout**:
```bash
d2 --layout=elk input.d2 output.svg
d2 --layout=tala input.d2 output.svg
```

**Direction** (via `direction` property):
```d2
direction: down  # or up, left, right

a -> b -> c
```

**Per-container direction** (TALA only):
```d2
container1: {
  direction: right
  a -> b -> c
}

container2: {
  direction: down
  x -> y -> z
}
```

---

## Advanced Features

### Near Positioning (TALA only)

**Position shapes near each other**:
```d2
a
b
c

# Position b near a
b.near: a

# Position c at top-left of container
c.near: top-left
```

**Near positions**:
- Object reference: `near: other-object`
- Container corners: `top-left`, `top-center`, `top-right`, `center-left`, `center-right`, `bottom-left`, `bottom-center`, `bottom-right`

### Width and Height

**TALA and ELK support explicit sizing**:
```d2
box: {
  width: 200
  height: 100
}

# On containers (controls container size)
container: {
  width: 500
  height: 300

  a
  b
  c
}
```

### Variables

**Define and use variables**:
```d2
vars: {
  primary-color: "#2196F3"
  server-icon: "https://icons.terrastruct.com/tech/server.svg"
}

server: {
  style.fill: ${primary-color}
  icon: ${server-icon}
}
```

### Imports

**Import other .d2 files**:
```d2
# Import entire file
...@common/styles.d2

# Import specific path
...@common/network.d2.network

# Import and merge
network: {
  ...@common/base-network.d2

  # Add local elements
  custom-server
}
```

### Links (interactive diagrams)

**Add clickable links**:
```d2
docs: Documentation {
  link: https://docs.example.com
}

# Tooltip on hover
support: Support {
  link: https://support.example.com
  tooltip: Contact our support team
}
```

---

## Best Practices

### DO:

✅ **Use containers for organization**:
```d2
system: {
  frontend: {
    ui
    components
  }

  backend: {
    api
    services
  }
}
```

✅ **Use appropriate shapes**:
```d2
users.shape: person
database.shape: cylinder
queue.shape: queue
process.shape: step
```

✅ **Use icons for clarity**:
```d2
api: API Gateway {
  icon: https://icons.terrastruct.com/tech/gateway.svg
}
```

✅ **Use classes for consistency**:
```d2
classes: {
  service: {
    style.fill: "#4CAF50"
    style.stroke: "#2E7D32"
  }
}

auth.class: service
payment.class: service
```

✅ **Choose right layout engine**:
- Simple hierarchies → `dagre` (fast)
- Complex graphs → `elk` (fewer crossings)
- Software architecture → `tala` (precise control)

### DON'T:

❌ **Over-style**: Use themes, avoid excessive custom styling
❌ **Inconsistent connections**: Same relationship = same arrow type
❌ **Too many colors**: Limit to 2-3 colors + theme
❌ **Decorative icons**: Icons must add meaning
❌ **Deep nesting**: Keep containers 2-3 levels max

---

## Common Patterns

### Simple Architecture

```d2
direction: right

user: User {
  shape: person
}

frontend: Web App {
  icon: https://icons.terrastruct.com/tech/react.svg
}

backend: API {
  icon: https://icons.terrastruct.com/tech/nodejs.svg
}

database: Database {
  shape: cylinder
  icon: https://icons.terrastruct.com/tech/postgresql.svg
}

user -> frontend: browse
frontend -> backend: API calls
backend -> database: queries
```

### Microservices with Grouping

```d2
direction: down

clients: Clients {
  web.shape: person
  mobile.shape: person
}

gateway: API Gateway {
  icon: https://icons.terrastruct.com/tech/gateway.svg
}

services: Services {
  auth: Auth Service
  data: Data Service
  analytics: Analytics Service
}

data-layer: Data Layer {
  postgres.shape: cylinder
  redis.shape: cylinder
  s3.shape: stored_data
}

clients.web -> gateway
clients.mobile -> gateway
gateway -> services.auth
gateway -> services.data
gateway -> services.analytics
services.data -> data-layer.postgres
services.data -> data-layer.redis
services.analytics -> data-layer.s3
```

### ERD with Foreign Keys

```d2
direction: right

users: {
  shape: sql_table
  id {primary_key}: int
  email {unique}: varchar
  name: varchar
}

posts: {
  shape: sql_table
  id {primary_key}: int
  user_id {foreign_key}: int
  title: varchar
  content: text
}

comments: {
  shape: sql_table
  id {primary_key}: int
  post_id {foreign_key}: int
  user_id {foreign_key}: int
  text: varchar
}

posts.user_id -> users.id
comments.post_id -> posts.id
comments.user_id -> users.id
```

---

## Compilation and Output

### CLI Usage

**Basic compilation**:
```bash
d2 diagram.d2 output.svg
d2 diagram.d2 output.png
d2 diagram.d2 output.pdf
```

**With options**:
```bash
# Layout engine
d2 --layout=elk diagram.d2 output.svg

# Theme
d2 --theme=200 diagram.d2 output.svg

# Watch mode (recompile on changes)
d2 --watch diagram.d2 output.svg

# Combined
d2 --layout=tala --theme=300 diagram.d2 output.svg
```

**Verify installation**:
```bash
d2 --version
d2 --help
```

---

## Quick Reference

**Shapes**: `rectangle`, `circle`, `cylinder`, `person`, `cloud`, `hexagon`, `diamond`
**Connections**: `->`, `<-`, `<->`, `--`
**Containers**: `name: { elements }`
**Special types**: `sql_table`, `class`, `sequence_diagram`, `grid`
**Icons**: `icon: URL` or `icon: ./path`
**Styling**: `style.property: value`
**Classes**: `classes: { name: { styles } }` then `obj.class: name`
**Layout engines**: `dagre` (default), `elk`, `tala`
**Themes**: `--theme 0-407`

---

*This skill provides complete D2 syntax knowledge for generating professional diagrams. Combine with diagram-hierarchy and diagram-clarity skills for visually effective results.*
