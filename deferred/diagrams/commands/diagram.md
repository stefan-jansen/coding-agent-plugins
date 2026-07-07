---
description: "Create high-quality D2 diagram with visual design expertise"
argument-hint: "[description] [--type TYPE] [--layout ENGINE] [--theme THEME] [--output FORMAT]"
allowed-tools: [Write, Bash]
---

# Create D2 Diagram

Generate professional, visually appealing D2 diagrams with encoded visual design expertise.

**Skills Applied**:
- **d2-syntax**: Complete D2 language proficiency
- **diagram-hierarchy**: Visual hierarchy principles (size, color, placement)
- **diagram-clarity**: Clarity and simplicity principles

## Usage

```bash
# Simple architecture diagram
/diagram "Web app with API, database, and cache"

# Specific diagram type
/diagram "User login authentication flow" --type sequence

# With layout engine
/diagram "Microservices with 5 services" --type architecture --layout tala

# With theme
/diagram "ERD for blog system" --type erd --theme 200

# Full options
/diagram "OAuth2 flow" --type sequence --layout elk --theme 300 --output svg
```

## Load Skills

This command automatically loads diagram generation skills:
- **d2-syntax** skill provides complete D2 language reference
- **diagram-hierarchy** skill applies visual design principles
- **diagram-clarity** skill ensures clear, simple diagrams

## Generate Diagram

**Based on your description and options**, I'll:

1. **Analyze requirements** - Understand what to diagram
2. **Apply hierarchy principles** - Size, color, placement for importance
3. **Apply clarity principles** - Simplicity, consistency, grouping
4. **Generate D2 code** - Using proper D2 syntax
5. **Compile to image** - Using D2 CLI
6. **Display result** - Show the diagram

## Arguments

**Description** (required):
- What to diagram
- Can be high-level ("system architecture") or specific ("OAuth login flow")

**--type** (optional):
- `architecture` - System/software architecture (default)
- `sequence` - Sequence/flow diagrams
- `erd` - Entity-relationship diagrams (database schemas)
- `class` - UML class diagrams
- `flow` - Process flow diagrams

**--layout** (optional):
- `dagre` - Fast, hierarchical (default) - bundled
- `elk` - Better for complex graphs, fewer edge crossings - bundled
- `tala` - Precise control for architecture (requires separate install, not bundled)

**--theme** (optional):
- Theme number (0-407) or name
- Popular: 0 (neutral), 200 (grape), 300 (berry), 400 (vanilla)
- Default: Uses D2's default theme

**--output** (optional):
- `svg` - Scalable vector (default)
- `png` - Raster image
- `pdf` - PDF document

## Examples

### Example 1: Simple Architecture

```bash
/diagram "Web application with frontend, API, and PostgreSQL database"
```

**Generates**:
```d2
direction: down

frontend: Frontend {
  shape: hexagon
  icon: https://icons.terrastruct.com/tech/react.svg
}

api: API {
  width: 150
  height: 90
}

database: PostgreSQL {
  shape: cylinder
  icon: https://icons.terrastruct.com/tech/postgresql.svg
}

frontend -> api: HTTP requests
api -> database: SQL queries
```

### Example 2: Sequence Diagram

```bash
/diagram "User login with authentication server" --type sequence
```

**Generates**:
```d2
shape: sequence_diagram

user -> frontend: Enter credentials
frontend -> api: POST /login
api -> auth-server: Validate user
auth-server -> api: JWT token
api -> frontend: Login success
frontend -> user: Show dashboard
```

### Example 3: Complex Architecture

```bash
/diagram "Microservices: API gateway, auth service, data service, payment service, with PostgreSQL and Redis" --type architecture --layout tala --theme 200
```

**Generates** (with visual hierarchy):
- API gateway: Larger, emphasized (entry point)
- Services: Medium, grouped
- Databases: Appropriate shapes and icons
- Clear grouping and relationships

## Design Principles Applied

### Visual Hierarchy (diagram-hierarchy skill)

**Size and scale**:
- Important components (gateways, entry points): 30-50% larger
- Services: Medium size
- Utilities: Smaller

**Color and contrast**:
- Critical path: Accent color
- Normal components: Theme defaults
- Supporting: Muted colors
- Limited to 2-3 accent colors

**Typography**:
- 2-3 text sizes
- Bold for emphasis
- Clear, readable labels

### Clarity (diagram-clarity skill)

**Simplicity**:
- 5-15 components per diagram
- Single abstraction level
- Multiple diagrams if needed

**Consistency**:
- Same connection type = same relationship
- Same color = same meaning
- Same shape = same component type

**Grouping**:
- Related elements in containers
- Max 2-3 nesting levels
- Clear organization

## Prerequisites

**D2 CLI required**:

```bash
# Install D2
# Mac:
brew install d2

# Linux:
curl -fsSL https://d2lang.com/install.sh | sh -s --

# Verify
d2 --version
```

**If D2 not installed**, the command will provide installation instructions.

## Output

**Files created**:
- `diagram.d2` - D2 source file
- `diagram.svg` (or .png, .pdf) - Compiled diagram

**Location**: Current working directory

## Error Handling

**Common issues**:

**D2 not installed**:
```
Error: d2 command not found
Install D2: https://d2lang.com/
```

**Compilation error**:
```
Error: D2 compilation failed
Check diagram.d2 for syntax errors
```

**Invalid arguments**:
```
Error: Unknown diagram type 'xyz'
Valid types: architecture, sequence, erd, class, flow
```

## Quality Guarantees

**Visual hierarchy** (from diagram-hierarchy skill):
- ✅ Size variations show importance
- ✅ Strategic color use (2-3 accent colors)
- ✅ Clear focal points
- ✅ Proper placement and balance

**Clarity** (from diagram-clarity skill):
- ✅ Limited colors (2-3 + theme)
- ✅ Appropriate shapes for components
- ✅ Consistent connection types
- ✅ Logical grouping with containers
- ✅ Clear, concise labels
- ✅ Single abstraction level
- ✅ Meaningful icons only
- ✅ Minimal custom styling

**D2 syntax** (from d2-syntax skill):
- ✅ Valid D2 code
- ✅ Compiles without errors
- ✅ Proper use of D2 features
- ✅ Appropriate layout engine for diagram type
- ✅ Professional theme application

## Tips for Best Results

**Be specific in description**:
- ❌ "System diagram"
- ✅ "Web app with React frontend, Node.js API, PostgreSQL database, Redis cache"

**Specify diagram type for clarity**:
- Architecture: Use `--type architecture`
- Flows: Use `--type sequence`
- Databases: Use `--type erd`

**Choose layout for complex diagrams**:
- Simple: Use default (dagre)
- Complex graphs: Use `--layout elk`
- Software architecture: Use `--layout tala`

**Use themes for professional look**:
- Don't customize colors manually
- Pick a theme (`--theme 200`) and use it

## Iteration

**If diagram needs refinement**:
1. Review generated `diagram.d2` file
2. Run `/diagram` again with adjusted description
3. Or manually edit `diagram.d2` and recompile:
   ```bash
   d2 diagram.d2 diagram.svg
   ```

**For complex projects**:
- Create multiple focused diagrams
- Each diagram = one aspect/question
- 5-15 components per diagram ideal

---

*This command combines D2 language expertise with visual design principles to produce professional, clear diagrams automatically.*
