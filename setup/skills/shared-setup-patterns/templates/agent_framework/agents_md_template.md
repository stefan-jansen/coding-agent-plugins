# $PROJECT_NAME

## Purpose

<one-paragraph statement of what this project is and who it's for>

## What this repo deliberately is NOT

<scope hedge: what shouldn't be added, to keep ambition bounded>

## Code vs data layout

| Path | Purpose |
|---|---|
| | |

## Hard rules

- (load-bearing constraints — e.g. "embedding model is X, pinned in script_y")

## Slash commands (Claude Code)

| Command | What it does |
|---|---|
| | |

## Common bash invocations

```bash
```

## Project memory

Persistent project state — survives `/clear` for Claude, read on demand by Codex:

@.workspace/memory/project_state.md
@.workspace/memory/conventions.md
@.workspace/memory/decisions.md

### Claude auto-memory (writer-asymmetric)

Claude Code writes autonomous learnings (user prefs, feedback, references) to
`.workspace/memory/auto/` — redirected here from the default `~/.claude/projects/<slug>/memory/`
via `autoMemoryDirectory` in `.claude/settings.json`. First 200 lines of
`MEMORY.md` load into every Claude session.

Codex has no native equivalent — it can **read** the same file via `@-include`
but does not write to it:

@.workspace/memory/auto/MEMORY.md

Consequence: model-authored memory accumulates through Claude sessions.
Codex-only sessions rely on the human-curated files above.

### Session progress

Session progress goes to `.workspace/transitions/YYYY-MM-DD/HH.md` — the hook
auto-creates the hourly file on each prompt. Append progress every
15-20 min or at milestones; both Claude and Codex sessions share it.

```bash
ls -r .workspace/transitions/$(date +%Y-%m-%d)/*.md   # newest first
```

## Agent infrastructure layout

```
AGENTS.md                  # this file — Codex reads natively
CLAUDE.md                  # one line: @AGENTS.md
.workspace/                # SHARED state for both Claude and Codex
  memory/                  #   persistent context (referenced above via @-include)
    auto/                  #     Claude auto-memory (harness writes here; Codex reads)
  transitions/             #   hourly session progress
  work/                    #   active work units / plans
.claude/                   # CLAUDE-SPECIFIC ONLY (different schema from Codex)
  settings.json            #   plugins, hooks, permissions, autoMemoryDirectory
  hooks/                   #   init-transition.sh
  commands/                #   project slash-commands
```

## Open issues

-
