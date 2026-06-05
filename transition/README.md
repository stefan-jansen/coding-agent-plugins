# Transition Plugin

**Purpose**: Session boundary management and context handoffs

This plugin handles transitions between Claude Code sessions, managing context preservation and continuation.

## The Value of Transitions

Beyond just session continuity, transitions create an **automatic project history**:

- **Audit trail**: Every session's decisions, changes, and reasoning are captured
- **Recovery**: Pick up work days or weeks later with full context
- **Accountability**: Understand *why* decisions were made, not just *what* was changed
- **Learning**: Review past approaches when solving similar problems

Over time, transitions become more valuable than commit history—they capture the *thinking* behind changes, not just the changes themselves.

**Storage location**: Hooks write to `.workspace/transitions/` (shared workspace for Claude Code and Codex). Run `/setup:existing` or `/setup:transitions` first to scaffold `.workspace/`.

---

## Hooks (plugin-owned, v1.1.0+)

The plugin registers its own `UserPromptSubmit` hook via `hooks/hooks.json`, so
projects no longer need to copy `init-transition.sh` into
`<project>/.claude/hooks/` or wire it into their `settings.json`.
Enabling `transition@local` (or the marketplace equivalent) is sufficient.

- **Script**: `hooks/init-transition.sh` — creates the current hourly
  `YYYY-MM-DD/HH.md` file under `.workspace/transitions/` if absent.
- **Routing**:
  - `.workspace/` exists → `.workspace/transitions/<date>/HH.md`
  - `.workspace/` absent → `.claude/transitions/<date>/HH.md`
    (pre-migration legacy fallback only).
- **Silence**: writes a file at most once per hour; no stdout in the happy
  path.

Pre-existing per-project copies of `init-transition.sh` can be removed
after the project enables this plugin. See the marketplace consolidation
notes for the migration sequence.

---

## Commands (2)

### `/transition:handoff`

**Purpose**: Create session handoff document with context analysis

Creates a comprehensive handoff document capturing:
- Current work state and progress
- Key decisions made during session
- Token usage across all components
- Next steps and pending tasks
- Files modified and their changes

**Usage**:
```bash
/transition:handoff
```

**Output**: Time-stamped handoff document in `.workspace/transitions/YYYY-MM-DD/HHMMSS.md`

**When to use**:
- Context usage >80% (quality degrading)
- End of work session (preserve state)
- Before switching tasks
- Regular checkpoints during long work

### `/transition:continue`

**Purpose**: Resume work from previous session handoff

Loads the most recent handoff document and provides:
- Summary of previous session
- Current state recap
- Pending tasks
- Recommended next actions

**Usage**:
```bash
/transition:continue
```

**When to use**:
- Start of new session
- After `/clear` to free conversation tokens
- Switching back to previous work
- Need recap of where you left off

---

## Why Separate from Memory Plugin?

**Session Transitions** (this plugin):
- Short-lived, time-bound documents
- Context window management
- Session-to-session continuity
- Tactical state preservation

**Persistent Memory** (memory plugin):
- Long-lived knowledge base
- Project understanding
- Accumulated insights
- Strategic knowledge capture

**Clear separation**: Transitions handle session boundaries, Memory handles knowledge persistence.

---

## Workflow Integration

**Typical flow**:

1. Work on task until context >80%
2. `/transition:handoff` - Create handoff
3. `/clear` - Free conversation tokens
4. `/transition:continue` - Resume with recap
5. Continue work with fresh context

**Key benefit**: Maintain work continuity across sessions without quality degradation.

---

## File Organization

```
.workspace/transitions/          # shared with Codex
├── 2026-05-08/
│   ├── 171530.md      # Handoff at 5:15:30 PM
│   ├── 194215.md      # Handoff at 7:42:15 PM
│   └── ...
├── 2026-05-09/
│   └── ...
```

**Format**: `YYYY-MM-DD/HHMMSS.md` (date-based directories, time-stamped files)

---

## Related

- **Memory plugin**: Persistent knowledge management
- **Workflow plugin**: Task and work unit management
- **System commands**: `/context` for token usage analysis

---

**Version**: 1.1.0
**License**: MIT
