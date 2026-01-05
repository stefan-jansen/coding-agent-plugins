---
allowed-tools: [Bash, Read, Write, MultiEdit, Grep, Glob, Task, WebFetch, mcp__context7__resolve-library-id, mcp__context7__get-library-docs]
argument-hint: "fetch|search|generate [arguments]"
description: Unified documentation operations - fetch external, search all, and generate project docs
---

# Documentation Operations

**Input**: $ARGUMENTS

## Usage

```bash
/docs fetch                    # Fetch official Claude Code & library docs
/docs fetch --force            # Force complete re-fetch
/docs fetch --libraries        # Focus on project dependency docs
/docs search "command syntax"  # Search all cached documentation
/docs generate "Added auth"    # Generate/update docs after changes
/docs generate --api           # Focus on API documentation
```

## Process

### 1. Determine Operation
- **fetch**: Download external documentation to `.claude/docs/`
- **search**: Query cached documentation and library docs
- **generate**: Create/update project documentation
- **No args**: Show usage guidance

### 2. Fetch Operations
- Identify documentation sources (official + dependencies)
- Create/update cache in `.claude/docs/`
- Track versions and timestamps
- Create searchable index

**With Context7**: Auto-detect dependencies → resolve library IDs → fetch version-matched docs

### 3. Search Operations
- Index search for fast results
- Full-text search across cache
- Rank by relevance

**With Context7**: Resolve library names → fetch live documentation → return focused results

### 4. Generate Operations
- Assess existing documentation
- Identify gaps and outdated content
- Generate API docs, README updates, migration guides
- Test code examples

### Cache Structure
```
.claude/docs/
├── official/          # Claude Code documentation
├── libraries/         # Third-party library docs
├── project/           # Project-specific docs
└── cache_metadata.json
```

## MCP Enhancement

**Context7** (when available):
- `resolve-library-id` → find library documentation
- `get-library-docs` → fetch comprehensive docs
- Fallback: WebFetch with manual caching
