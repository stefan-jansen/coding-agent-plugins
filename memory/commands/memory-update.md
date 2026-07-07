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
Located in `.workspace/memory/`:

1. **project_state.md** - Current architecture, scope, key components
2. **conventions.md** - Code patterns, naming standards, practices
3. **decisions.md** - Architectural choices and rationale

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
✅ "See @.workspace/reference/api-spec.md for details"

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

## Integration with AGENTS.md

AGENTS.md references memory through the index (Claude reads it via
`CLAUDE.md → @AGENTS.md`):

```markdown
## Project memory
@.workspace/memory/MEMORY_INDEX.md
```

Index-only auto-load keeps the session-start context tax bounded —
individual memory files are read on demand when their topic is relevant.
Codex reads the same `AGENTS.md` natively.

## Keep the index current (mandatory step)

After **any** write to `.workspace/memory/` — adding a new file,
editing an existing one, or relocating — refresh `MEMORY_INDEX.md` so
its `tokens` field stays accurate and any new file gets an entry:

```bash
BIN="${CLAUDE_PLUGIN_ROOT}/bin"
[[ -z "$CLAUDE_PLUGIN_ROOT" ]] && BIN="$HOME/agents/coding/plugins/memory/bin"
bash "$BIN/memory_init_index.sh" --quiet
```

`memory_init_index.sh` is idempotent: it recomputes tokens, adds entries
for new files, drops entries for deleted files from the sidecar, and
preserves manually-set fields (status / anchors / supersession links).
Then verify integrity:

```bash
bash "$BIN/verify_index.sh"
```

A clean exit means the index is internally consistent (every memory file
has a complete entry; statuses are in the allowed vocabulary). Without
this step, downstream tools (`/memory-gc`, the SessionStart nudge,
`/memory-review`) will under-report or skip the new content.

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