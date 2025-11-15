---
title: memory-update
aliases: [remember, learn]
---

# Memory Update

Incrementally maintain project knowledge in permanent memory files.

## Purpose

Regular housekeeping to capture learnings and maintain accurate project state without cluttering documentation with verbose histories.

## What Gets Updated

### Core Memory Files
Located in `.claude/memory/`:

1. **project_state.md** - Current architecture, scope, key components
2. **conventions.md** - Code patterns, naming standards, practices
3. **dependencies.md** - External services, APIs, integrations
4. **decisions.md** - Architectural choices and rationale

### Update Triggers
- After implementing significant features
- When discovering important patterns
- Before conversation context fills (proactive)
- After resolving complex issues

## Usage

```bash
# Analyze and update all relevant memory files
/memory-update

# Update specific aspect
/memory-update "new authentication architecture"

# Quick update (only critical changes)
/memory-update --quick
```

## Memory Principles

### Keep It Concise
❌ "We initially tried approach X, then switched to Y because..."
✅ "Uses pattern Y for better performance"

### Focus on Current State
❌ "Previously the system used MySQL but we migrated..."
✅ "PostgreSQL database with TimescaleDB extension"

### Avoid Meta-Commentary
❌ "This was updated on Sept 15 after discussion about..."
✅ Just the fact/decision itself

### Use References, Not Duplication
❌ Copying full documentation into memory
✅ "See @.claude/reference/api-spec.md for details"

## Update Process

I'll:
1. **Analyze recent work** for durable learnings
2. **Update relevant memory files** with new knowledge
3. **Ensure CLAUDE.md references** are current
4. **Remove outdated information** if any

## Example Memory Structure

### project_state.md
```markdown
# Project State

## Architecture
- Microservices: auth, payments, analytics
- Event-driven with RabbitMQ
- PostgreSQL + Redis caching

## Current Scope
- Real-time data processing
- Business logic implementation
- Performance monitoring
```

### conventions.md
```markdown
# Conventions

## Code Style
- Type hints for all functions
- Async/await for I/O operations
- Factory pattern for service creation

## Testing
- pytest with fixtures
- Mock external services
- 80% coverage minimum
```

## Integration with CLAUDE.md

CLAUDE.md references memory files:
```markdown
## Project Knowledge
@.claude/memory/project_state.md
@.claude/memory/conventions.md
@.claude/memory/dependencies.md
@.claude/memory/decisions.md
```

This keeps CLAUDE.md lean while maintaining comprehensive knowledge.

## Benefits

- **Progressive Learning**: Knowledge accumulates properly
- **Clean Documentation**: No verbose histories
- **Quick Context**: New agents understand immediately
- **Sustainable Growth**: Documentation stays manageable

## When NOT to Use

Don't update memory for:
- Temporary debugging findings
- Session-specific workarounds
- Historical narratives
- Information already in README or docs

Use `/handoff` instead for session-specific context.

---

*Part of the memory management system - maintaining durable project knowledge*