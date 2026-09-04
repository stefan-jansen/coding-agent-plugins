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

**Storage location**: Hooks write to `.workspace/transitions/` (shared workspace for Claude Code and Codex). Run `/setup` first to scaffold `.workspace/`.

Set `CLAUDE_TRANSITIONS_DIR` to put them somewhere else - absolute, or relative
to the project root. Same rule as the memory plugin's `CLAUDE_MEMORY_DIR`, and
set the same way, in the `env` block of the project's `.claude/settings.json`:

```json
{"env": {"CLAUDE_TRANSITIONS_DIR": "transitions"}}
```

A project that keeps its agent state at the root rather than under `.workspace/`
needs this, or the hooks recreate `.workspace/transitions/` after every move.
`bin/test_transitions_dir.sh` runs the hooks against throwaway roots and asserts
where the files land.

---

## Hooks (plugin-owned, v1.2.0+)

The plugin registers its own compaction and session-end hooks via
`hooks/hooks.json`, so enabling `transition@local` (or the marketplace
equivalent) is sufficient — no per-project wiring in `settings.json`. All three
resolve their target from `$CLAUDE_PROJECT_DIR` (the top-level project dir Claude
Code always sets for hooks), which is why they are safe to register at the plugin
level.

- **`PreCompact`** (`auto|manual`) → `hooks/pre-compact.sh` — emits custom
  instructions telling Claude what to preserve in the compaction summary
  (current task, decisions, active files, blockers). Additively surfaces a
  `/memory-gc` staleness nudge when the memory plugin's sidecar is present and
  overdue.
- **`PostCompact`** (`auto|manual`) → `hooks/post-compact.sh` — writes the
  compaction summary to a timestamped `<transitions>/YYYY-MM-DD/HHMMSS.md`
  (one file per event - the same convention `/handoff` uses).
- **`SessionEnd`** → `hooks/session-end.sh` — appends a session-exit marker to
  today's most-recent transition file, or does nothing if none exists (a bare
  marker file would be the thin-file anti-pattern below).

`hooks/init-transition.sh` is retained but **unregistered**. The old
`UserPromptSubmit` hourly-stub hook was removed on 2026-08-05: it created an
empty `HH.md` per hour that nothing filled in, and it resolved its destination
from the shell cwd, so a command run inside a nested repository scattered a
stray `.workspace/` there. Do not recreate a per-hour auto-stub.

---

## Manual handoffs

Automatic capture covers compaction and session end. For the cases with no
compaction event — before `/clear`, a Claude↔Codex host swap, or a deliberate
milestone checkpoint — use the **`workflow` plugin's host-neutral skills**:

- `/handoff` — write a durable transition at
  `.workspace/transitions/YYYY-MM-DD/HHMMSS.md`
- `/continue` — resume from the most recent handoff (runs its verification
  snapshot, reports drift, surfaces suggested next steps)

This plugin no longer ships its own `handoff`/`continue` commands; the workflow
skills are the single, richer implementation.

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

1. Work on task until context >80% (or reach a milestone / a host swap)
2. `/handoff` (workflow plugin) — create a durable handoff
3. `/clear` — free conversation tokens
4. `/continue` (workflow plugin) — resume with recap
5. Continue work with fresh context

Between those manual checkpoints, auto-capture fires on every compaction and at
session end with no action needed.

---

## File Organization

```
.workspace/transitions/          # shared with Codex
├── 2026-05-08/
│   ├── 143002.md      # auto-capture: a compaction summary
│   ├── 171530.md      # manual /handoff at 5:15:30 PM
│   └── ...
├── 2026-05-09/
│   └── ...
```

**Format**: every transition file is timestamped `YYYY-MM-DD/HHMMSS.md`, whether
written by auto-capture (compaction) or by manual `/handoff` — one file per event.

---

## Related

- **Memory plugin**: Persistent knowledge management
- **Workflow plugin**: `/handoff`, `/continue`, task and work unit management
- **System commands**: `/context` for token usage analysis

---

**Version**: 1.2.0
**License**: MIT
