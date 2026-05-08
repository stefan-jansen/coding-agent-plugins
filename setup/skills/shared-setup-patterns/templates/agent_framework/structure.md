# Agent Infrastructure Layout

This template defines the canonical project layout for projects that use both
Claude Code and Codex.

## Directory Layout

```
AGENTS.md                  # canonical project doc (Codex reads natively)
CLAUDE.md                  # one line: @AGENTS.md
.agents/                   # SHARED state for both Claude and Codex
├── memory/                #   persistent context (referenced from AGENTS.md via @-include)
│   ├── project_state.md
│   ├── conventions.md
│   └── decisions.md
├── transitions/           #   hourly session progress (YYYY-MM-DD/HH.md)
└── work/                  #   active work units / plans
.claude/                   # CLAUDE-SPECIFIC ONLY (different schema from Codex)
├── settings.json          #   plugins, hooks, permissions
├── hooks/                 #   init-transition.sh, etc.
└── commands/              #   project slash-commands
```

## Purpose of Each Path

### AGENTS.md
Canonical project instructions. Codex reads this natively; Claude reads it via
`CLAUDE.md` one-liner. Single source of truth, no duplication.

### CLAUDE.md
One line — `@AGENTS.md`. Just an include so Claude inherits the same content
Codex sees.

### .agents/memory/
Persistent project state. Survives `/clear` for Claude. Read on demand by
Codex. Three files: `project_state.md` (architecture / what's working),
`conventions.md` (code style, infrastructure), `decisions.md` (load-bearing
choices with reasoning).

### .agents/transitions/
Hourly session progress. The `init-transition.sh` hook auto-creates the
hourly file (`YYYY-MM-DD/HH.md`) on each prompt. Append progress every
15-20 min or at milestones; both Claude and Codex sessions share it.

### .agents/work/
Active work units / plans. Multi-session work tracking.

### .claude/settings.json
Claude Code configuration: plugin marketplace, enabled plugins, hooks,
permissions. Different schema from Codex; cannot be unified.

### .claude/hooks/
Claude Code hooks (UserPromptSubmit, PostToolUse, etc.). Schema is
Claude-specific.

### .claude/commands/
Project-specific Claude slash-commands. Schema is Claude-specific.

## Migration from Pre-Convention Layout

Old layout (deprecated for new projects):
- `.claude/memory/` → moved to `.agents/memory/`
- `.claude/transitions/` → moved to `.agents/transitions/`
- `.claude/work/` → moved to `.agents/work/`
- `CLAUDE.md` (long) → reduced to `@AGENTS.md`; content moved to `AGENTS.md`

For existing projects: leave the old `.claude/` data alone (still readable on
demand) but write new state to `.agents/`.
