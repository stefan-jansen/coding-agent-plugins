---
name: docs
description: This skill should be used when the user asks to "document this", "add documentation", "write docs", "update the README", "generate API docs", "fetch library docs", or when working with project documentation, external library references, or documentation generation.
allowed-tools: [Bash, Read, Write, MultiEdit, Grep, Glob, Task, WebFetch, mcp__context7__resolve-library-id, mcp__context7__get-library-docs]
---

# Documentation Operations

Unified documentation: fetch external docs, search references, and generate project docs.

## When This Triggers

- "Document this code"
- "Add documentation"
- "Write docs for this"
- "Update the README"
- "Generate API docs"
- "Fetch library docs"
- "Search documentation"
- Working with project documentation

## Operations

### Fetch External Documentation

Download and cache external documentation:

```bash
# Fetch official Claude Code & library docs
/docs fetch

# Force complete re-fetch
/docs fetch --force

# Focus on project dependency docs
/docs fetch --libraries
```

**With Context7**: Auto-detect dependencies → resolve library IDs → fetch version-matched docs

### Search Documentation

Query cached and live documentation:

```bash
# Search all cached documentation
/docs search "command syntax"
```

**With Context7**: Resolve library names → fetch live documentation → return focused results

### Generate Project Documentation

Create or update project documentation:

```bash
# Generate/update docs after changes
/docs generate "Added auth"

# Focus on API documentation
/docs generate --api
```

## Process

### 1. Determine Operation

- **fetch**: Download external documentation to `.claude/docs/`
- **search**: Query cached documentation and library docs
- **generate**: Create/update project documentation
- **Auto-triggered**: Assess documentation needs based on context

### 2. Fetch Operations

- Identify documentation sources (official + dependencies)
- Create/update cache in `.claude/docs/`
- Track versions and timestamps
- Create searchable index

### 3. Search Operations

- Index search for fast results
- Full-text search across cache
- Rank by relevance

### 4. Generate Operations

- Assess existing documentation
- Identify gaps and outdated content
- Generate API docs, README updates, migration guides
- Test code examples

## Cache Structure

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
