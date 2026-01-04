---
allowed-tools: [Read, Write, Grep, Bash, Glob, Task]
argument-hint: "[--update] [--refresh] [focus_area]"
description: "Create persistent project understanding via PROJECT_MAP.md"
---

# Index Project

Create persistent project understanding that survives sessions.

**Input**: $ARGUMENTS

## Modes

- *(no args)*: Full project scan
- `--update`: Incremental changes only
- `--refresh`: Complete regeneration
- `"focus area"`: Targeted analysis

## Process

1. **Analyze Structure**
   - Detect language (Python/JS/TS/Go)
   - Identify frameworks (Django, React, FastAPI, etc.)
   - Map directories: src/, lib/, tests/, docs/
   - Find entry points: main.py, index.js, app.py

2. **Generate PROJECT_MAP.md**
   ```markdown
   # Project Map: [Name]

   ## Quick Overview
   - Type: [web app/library/service]
   - Language: [primary]
   - Frameworks: [detected]

   ## Directory Structure
   - `src/` - Main application
   - `tests/` - Test files

   ## Key Files
   - `main.py` - Entry point
   - `config.yaml` - Configuration

   ## Patterns
   - Architecture: [pattern]
   - Testing: [approach]
   ```

3. **Auto-import to CLAUDE.md**
   - Add `@.claude/PROJECT_MAP.md` import
   - Create CLAUDE.md if doesn't exist

## Output

- `.claude/PROJECT_MAP.md` - Project understanding
- CLAUDE.md updated with import

## Benefits

- `/analyze` has persistent context
- `/explore` starts with project knowledge
- New sessions understand codebase immediately
