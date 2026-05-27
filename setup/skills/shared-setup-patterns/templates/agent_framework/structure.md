# Agent Infrastructure Layout

This template defines the canonical project layout for projects that use both
Claude Code and Codex.

## Directory Layout

```
AGENTS.md                  # canonical project doc (Codex reads natively)
CLAUDE.md                  # one line: @AGENTS.md
.workspace/                # SHARED state for both Claude and Codex (writable; not a protected name)
├── memory/                #   persistent context (referenced from AGENTS.md via @-include)
│   ├── project_state.md
│   ├── conventions.md
│   └── decisions.md
├── transitions/           #   hourly session progress (YYYY-MM-DD/HH.md)
└── work/                  #   active work units / plans
.agents/                   # CODEX-NATIVE skills/roles only (Codex protects read-only) — NOT for state
└── skills/                #   optional Codex skills
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

### .workspace/memory/
Persistent project state. Survives `/clear` for Claude. Read on demand by
Codex. Three files: `project_state.md` (architecture / what's working),
`conventions.md` (code style, infrastructure), `decisions.md` (load-bearing
choices with reasoning).

### .workspace/transitions/
Hourly session progress. The `init-transition.sh` hook auto-creates the
hourly file (`YYYY-MM-DD/HH.md`) on each prompt. Append progress every
15-20 min or at milestones; both Claude and Codex sessions share it.

### .workspace/work/
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
- `.claude/memory/` → moved to `.workspace/memory/`
- `.claude/transitions/` → moved to `.workspace/transitions/`
- `.claude/work/` → moved to `.workspace/work/`
- `CLAUDE.md` (long) → reduced to `@AGENTS.md`; content moved to `AGENTS.md`

For existing projects: leave the old `.claude/` data alone (still readable on
demand) but write new state to `.workspace/`.
