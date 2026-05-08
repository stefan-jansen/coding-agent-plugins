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

@.agents/memory/project_state.md
@.agents/memory/conventions.md
@.agents/memory/decisions.md

Session progress goes to `.agents/transitions/YYYY-MM-DD/HH.md` — the hook
auto-creates the hourly file on each prompt. Append progress every
15-20 min or at milestones; both Claude and Codex sessions share it.

```bash
ls -r .agents/transitions/$(date +%Y-%m-%d)/*.md   # newest first
```

## Agent infrastructure layout

```
AGENTS.md                  # this file — Codex reads natively
CLAUDE.md                  # one line: @AGENTS.md
.agents/                   # SHARED state for both Claude and Codex
  memory/                  #   persistent context (referenced above via @-include)
  transitions/             #   hourly session progress
  work/                    #   active work units / plans
.claude/                   # CLAUDE-SPECIFIC ONLY (different schema from Codex)
  settings.json            #   plugins, hooks, permissions
  hooks/                   #   init-transition.sh
  commands/                #   project slash-commands
```

## Open issues

-
