---
allowed-tools: [Read, Write, Grep, Bash, Glob, Task]
argument-hint: "[--update] [--refresh] [focus_area]"
description: Create and maintain persistent project understanding through comprehensive project mapping
---

# Index Project

Creates persistent project understanding that survives sessions by generating a comprehensive PROJECT_MAP.md file automatically imported into CLAUDE.md.

**Solves the core problem**: `/analyze` insights are lost between sessions, requiring constant "looking around" and re-exploration of codebases.

**Input**: $ARGUMENTS

## Implementation

```bash
#!/bin/bash

# Standard constants (must be copied to each command)
readonly CLAUDE_DIR=".claude"
readonly PROJECT_MAP="${CLAUDE_DIR}/PROJECT_MAP.md"
readonly CLAUDE_MD="CLAUDE.md"

# Error handling functions (must be copied to each command)
error_exit() {
    echo "ERROR: $1" >&2
    exit 1
}

warn() {
    echo "WARNING: $1" >&2
}

debug() {
    [ "${DEBUG:-false}" = "true" ] && echo "DEBUG: $1" >&2
}

# Safe directory creation
safe_mkdir() {
    local dir="$1"
    mkdir -p "$dir" || error_exit "Failed to create directory: $dir"
}

# Parse arguments
MODE="full"
FOCUS_AREA=""

if [[ "$ARGUMENTS" == *"--update"* ]]; then
    MODE="update"
elif [[ "$ARGUMENTS" == *"--refresh"* ]]; then
    MODE="refresh"
elif [ -n "$ARGUMENTS" ] && [[ "$ARGUMENTS" != --* ]]; then
    FOCUS_AREA="$ARGUMENTS"
fi

echo "🔍 Indexing Project"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Mode: $MODE"
if [ -n "$FOCUS_AREA" ]; then
    echo "Focus: $FOCUS_AREA"
fi
echo ""

# Ensure .claude directory exists
safe_mkdir "$CLAUDE_DIR"

# Check if PROJECT_MAP.md already exists
if [ -f "$PROJECT_MAP" ] && [ "$MODE" = "full" ]; then
    echo "📝 Existing PROJECT_MAP.md found. Use --update for incremental or --refresh for complete regeneration."
    MODE="update"
fi

# Analyze project structure
echo "📊 Analyzing project structure..."

# Get project name from directory
PROJECT_NAME=$(basename "$(pwd)")

# Detect primary language
PRIMARY_LANG="Unknown"
if ls *.py >/dev/null 2>&1; then
    PRIMARY_LANG="Python"
elif ls *.js >/dev/null 2>&1; then
    PRIMARY_LANG="JavaScript"
elif ls *.ts >/dev/null 2>&1; then
    PRIMARY_LANG="TypeScript"
elif ls *.go >/dev/null 2>&1; then
    PRIMARY_LANG="Go"
elif ls *.java >/dev/null 2>&1; then
    PRIMARY_LANG="Java"
fi

# Detect frameworks
FRAMEWORKS=""
if [ -f "package.json" ]; then
    if grep -q "react" package.json 2>/dev/null; then
        FRAMEWORKS="${FRAMEWORKS}React "
    fi
    if grep -q "express" package.json 2>/dev/null; then
        FRAMEWORKS="${FRAMEWORKS}Express "
    fi
    if grep -q "next" package.json 2>/dev/null; then
        FRAMEWORKS="${FRAMEWORKS}Next.js "
    fi
fi

if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    if grep -q "django" requirements.txt 2>/dev/null || grep -q "django" pyproject.toml 2>/dev/null; then
        FRAMEWORKS="${FRAMEWORKS}Django "
    fi
    if grep -q "flask" requirements.txt 2>/dev/null || grep -q "flask" pyproject.toml 2>/dev/null; then
        FRAMEWORKS="${FRAMEWORKS}Flask "
    fi
    if grep -q "fastapi" requirements.txt 2>/dev/null || grep -q "fastapi" pyproject.toml 2>/dev/null; then
        FRAMEWORKS="${FRAMEWORKS}FastAPI "
    fi
fi

# Create or update PROJECT_MAP.md
echo "📝 Creating PROJECT_MAP.md..."

cat > "$PROJECT_MAP" << EOF || error_exit "Failed to create PROJECT_MAP.md"
# Project Map: $PROJECT_NAME

*Generated: $(date -Iseconds)*
*Last Updated: $(date -Iseconds)*

## Quick Overview
- **Type**: [Project type to be determined]
- **Primary Language**: $PRIMARY_LANG
- **Frameworks**: ${FRAMEWORKS:-Not detected}
- **Location**: $(pwd)

## Directory Structure

### Main Application Code
EOF

# Add directory structure analysis
for dir in src lib app core; do
    if [ -d "$dir" ]; then
        FILE_COUNT=$(find "$dir" -type f -name "*.${PRIMARY_LANG,,}" 2>/dev/null | wc -l)
        echo "- \`$dir/\` - Main application code ($FILE_COUNT files)" >> "$PROJECT_MAP"
    fi
done

echo "" >> "$PROJECT_MAP"
echo "### Test Organization" >> "$PROJECT_MAP"
for dir in test tests __tests__ spec; do
    if [ -d "$dir" ]; then
        echo "- \`$dir/\` - Test files" >> "$PROJECT_MAP"
    fi
done

echo "" >> "$PROJECT_MAP"
echo "### Documentation" >> "$PROJECT_MAP"
if [ -f "README.md" ]; then
    echo "- \`README.md\` - Project documentation" >> "$PROJECT_MAP"
fi
if [ -d "docs" ]; then
    echo "- \`docs/\` - Additional documentation" >> "$PROJECT_MAP"
fi

# Add key files section
echo "" >> "$PROJECT_MAP"
echo "## Key Files" >> "$PROJECT_MAP"

# Find entry points
for file in main.py app.py server.py index.js server.js main.go; do
    if [ -f "$file" ]; then
        echo "- \`$file\` - Application entry point" >> "$PROJECT_MAP"
    fi
done

# Add patterns section
echo "" >> "$PROJECT_MAP"
echo "## Patterns & Conventions" >> "$PROJECT_MAP"
echo "- **Architecture**: [To be analyzed]" >> "$PROJECT_MAP"
echo "- **Testing**: [To be analyzed]" >> "$PROJECT_MAP"
echo "- **Code Style**: [To be analyzed]" >> "$PROJECT_MAP"

# Add to CLAUDE.md if not already imported
if [ -f "$CLAUDE_MD" ]; then
    if ! grep -q "@.claude/PROJECT_MAP.md" "$CLAUDE_MD" 2>/dev/null; then
        echo "" >> "$CLAUDE_MD"
        echo "## Project Understanding" >> "$CLAUDE_MD"
        echo "@.claude/PROJECT_MAP.md" >> "$CLAUDE_MD"
        echo "✅ Added PROJECT_MAP.md import to CLAUDE.md"
    else
        echo "✅ PROJECT_MAP.md already imported in CLAUDE.md"
    fi
else
    # Create CLAUDE.md with import
    cat > "$CLAUDE_MD" << EOF || error_exit "Failed to create CLAUDE.md"
# Project: $PROJECT_NAME

## Project Understanding
@.claude/PROJECT_MAP.md
EOF
    echo "✅ Created CLAUDE.md with PROJECT_MAP.md import"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Project indexed successfully!"
echo ""
echo "📋 PROJECT_MAP.md created at: $PROJECT_MAP"
echo "📋 Auto-imported into: $CLAUDE_MD"
echo ""
echo "💡 Next steps:"
echo "   - Review and enhance PROJECT_MAP.md with specific details"
echo "   - Run /analyze for deeper code analysis"
echo "   - Use /index --update after making changes"
```

## Usage

### Full Project Mapping (Initial Use)
```bash
/index
```
Performs comprehensive project scan, creates `.claude/PROJECT_MAP.md`, and auto-imports into `CLAUDE.md`.

### Incremental Updates
```bash
/index --update
```
Updates existing PROJECT_MAP.md with recent changes, new files, and structural modifications.

### Complete Refresh
```bash
/index --refresh
```
Force complete re-scan and regeneration of PROJECT_MAP.md, useful after major refactoring.

### Focused Analysis
```bash
/index "authentication system"
```
Generate project map with special focus on authentication-related components and patterns.

## Phase 1: Determine Analysis Mode

Based on arguments: $ARGUMENTS

I'll determine the appropriate indexing approach:

- **Full Scan**: No arguments or new project - comprehensive analysis
- **Update Mode**: `--update` specified - incremental changes only
- **Refresh Mode**: `--refresh` specified - complete regeneration
- **Focused Mode**: Focus area specified - targeted analysis

## Phase 2: Project Structure Analysis

### Directory Structure Discovery
1. **Source Code Organization**: Identify main code directories (src/, lib/, app/, etc.)
2. **Test Organization**: Locate test directories and their relationship to source
3. **Documentation Structure**: Find docs/, README files, and documentation patterns
4. **Configuration Files**: Map config files, environment files, and settings
5. **Build and Deployment**: Identify build directories, deployment configs, and artifacts

### Technology Stack Detection
1. **Primary Language**: Determine main programming language from file extensions
2. **Framework Identification**: Detect frameworks from package files and imports
3. **Database Technology**: Identify database systems and ORM patterns
4. **Build Tools**: Find build systems, task runners, and automation tools
5. **Deployment Platform**: Detect containerization, cloud configs, and deployment targets

### Entry Points and Key Files
1. **Application Entry Points**: main.py, index.js, app.py, server.go, etc.
2. **Configuration Entry Points**: settings files, environment configs
3. **API Definitions**: Route files, API specs, schema definitions
4. **Data Models**: Entity definitions, database schemas, type definitions
5. **Core Business Logic**: Key service files, domain models, controllers

## Phase 3: Code Pattern Analysis

### Architectural Patterns
1. **Project Structure**: Analyze directory organization and naming conventions
2. **Code Organization**: Identify layering patterns (MVC, clean architecture, etc.)
3. **Dependency Patterns**: Map how modules import and depend on each other
4. **Design Patterns**: Identify common patterns (factory, singleton, observer, etc.)
5. **Testing Patterns**: Understand test organization and coverage approach

### Development Conventions
1. **Naming Conventions**: File naming, variable naming, function naming patterns
2. **Code Style**: Formatting, documentation, and comment patterns
3. **Error Handling**: How errors are managed and propagated
4. **Logging and Monitoring**: Logging patterns and monitoring setup
5. **Security Practices**: Authentication, authorization, and security patterns

### Integration Points
1. **External APIs**: Third-party service integrations and API clients
2. **Database Connections**: How data persistence is handled
3. **Message Queues**: Async communication and event handling
4. **Caching Systems**: Caching strategies and implementations
5. **File Storage**: File handling and storage systems

## Phase 4: Enhanced Analysis (with MCP Tools)

### Sequential Thinking Analysis (when available)
For complex projects, use structured reasoning to understand:

1. **System Architecture**: Step-by-step analysis of how components interact
2. **Data Flow**: Systematic tracing of data through the system
3. **Business Logic**: Understanding of core functionality and workflows
4. **Integration Points**: Analysis of external dependencies and interfaces
5. **Scalability Considerations**: Assessment of performance and scaling patterns

### Semantic Code Analysis (with Serena MCP)
When Serena is connected, enhance analysis with:

1. **Symbol-Level Understanding**: Actual class and function relationships
2. **Import Graph Analysis**: Real dependency tracking and circular dependency detection
3. **Type Flow Analysis**: Understanding of data types and contracts
4. **API Surface Mapping**: Public interfaces and their usage patterns
5. **Dead Code Detection**: Unused functions, classes, and modules

## Phase 5: Generate PROJECT_MAP.md

### Project Map Structure
Create comprehensive project map with the following sections:

```markdown
# Project Map: [Project Name]

*Generated: [timestamp]*
*Last Updated: [timestamp]*

## Quick Overview
- **Type**: [web app/library/service/tool]
- **Primary Language**: [language]
- **Frameworks**: [key frameworks]
- **Location**: [project path]

## Directory Structure

### Main Application Code
- `src/` - [description]
- `lib/` - [description]
- `app/` - [description]

### Test Organization
- `tests/` - [description]
- `test/` - [description]

### Documentation
- `docs/` - [description]
- `README.md` - [description]

## Key Files
- `[entry-point]` - [description and purpose]
- `[config-file]` - [configuration and settings]
- `[key-module]` - [core functionality]

## Patterns & Conventions
- **Architecture**: [architectural pattern]
- **Testing**: [testing approach]
- **Code Style**: [formatting and conventions]
- **Error Handling**: [error management pattern]

## Dependencies

### External Dependencies
- **Production**: [key production dependencies]
- **Development**: [development and testing tools]

### Internal Dependencies
- **Core Modules**: [main internal dependencies]
- **Utilities**: [helper and utility modules]

## Entry Points & Common Tasks

### Development Workflow
- **Start Dev Server**: [command]
- **Run Tests**: [command]
- **Build Production**: [command]
- **Deploy**: [command or process]

### Key Workflows
- **Adding Features**: [typical process]
- **Testing**: [testing workflow]
- **Deployment**: [deployment process]

## Focus Areas (if specified)
[Detailed analysis of specified focus area]
```

### Auto-Import Setup
1. **Update CLAUDE.md**: Add `@.claude/PROJECT_MAP.md` import
2. **Verify Import**: Ensure import syntax is correct
3. **Test Loading**: Validate the import works in Claude Code sessions

## Phase 6: Validation and Updates

### Validation Checks
1. **File Accessibility**: Ensure all referenced files exist and are readable
2. **Import Syntax**: Verify CLAUDE.md import syntax is correct
3. **Content Accuracy**: Validate project map reflects actual codebase
4. **Size Management**: Keep project map under 10KB for context efficiency

### Update Strategy
1. **Incremental Updates**: For `--update` mode, focus on changed files only
2. **Timestamp Tracking**: Update modification timestamps appropriately
3. **Change Detection**: Identify what has changed since last indexing
4. **Selective Refresh**: Update only affected sections for efficiency

## Success Indicators

- ✅ PROJECT_MAP.md created/updated in `.claude/` directory
- ✅ Auto-import added to CLAUDE.md file
- ✅ Project map accurately reflects codebase structure
- ✅ Key patterns and conventions documented
- ✅ Entry points and workflows clearly identified
- ✅ Dependencies and integrations mapped
- ✅ Focus area analysis completed (if specified)
- ✅ File size optimized for context window

## Common Use Cases

### New Project Onboarding
```bash
/index
# → Comprehensive project map for new team members
```

### After Major Refactoring
```bash
/index --refresh
# → Complete regeneration to reflect structural changes
```

### Focused Component Analysis
```bash
/index "user authentication"
# → Detailed analysis of auth-related components
```

### Incremental Updates
```bash
/index --update
# → Quick update after adding new features
```

## Integration with Other Commands

- **Analyze**: `/analyze` now has persistent context from PROJECT_MAP.md
- **Explore**: `/explore` benefits from existing project understanding
- **Review**: `/review` uses project map for focused code review
- **Fix**: `/fix` leverages architecture understanding for better debugging

---

*Creates persistent project understanding that survives sessions and accelerates development workflows.*