# Setup Plugin

**Version**: 2.0.0
**Purpose**: Project initialization and Claude Code configuration

## Overview

Two commands, one job each:

- **`/setup`** — bootstrap *this* project (the current directory) to the
  canonical Claude + Codex layout, through a short interview.
- **`/setup:user`** — set up your *global* `~/AGENTS.md` (a different scope:
  cross-agent user config, not a project).

There used to be six overlapping setup commands (`python`, `javascript`,
`existing`, `statusline`, `transitions`, plus a `system:project-setup` skill and
a legacy user-level `setup-project` command). They produced drifted copies of
the same templates and it was never clear which to run. `/setup` subsumes all of
them: it detects the environment, asks only what the files can't tell it, and is
idempotent.

## Commands

### `/setup [project-name]`

Bootstrap the current directory. Works on an empty folder or an existing repo.

**What it does**:
1. **Detects** — git or not, empty or populated, already set up or not, language
   (Python / Node / Go / Rust), and a local plugin marketplace to wire in.
2. **Interviews** — a short, one-question-at-a-time pass to capture the project's
   purpose, what it deliberately is NOT, and any hard rules. Skips anything the
   detection already answered.
3. **Generates** (idempotent — never clobbers existing files):
   - `AGENTS.md` — canonical project doc, filled from the interview (not a
     placeholder skeleton)
   - `CLAUDE.md` — one line, `@AGENTS.md`
   - `.workspace/{memory,transitions,work}` — shared Claude + Codex state,
     including `memory/auto/` for Claude auto-memory
   - `.claude/{settings.json,hooks/init-transition.sh,commands/}` — Claude-only config
   - Optional Python tooling (pyproject/ruff/pre-commit) when the project is Python
   - Optional roborev continuous review

**Usage**:
```bash
cd ~/my-new-project
/setup
/setup my-project      # name override (defaults to the directory name)
```

### `/setup:user [--force] [--from-existing] [--claude-only] [--codex-only] [--opencode]`

Install the "single canonical `~/AGENTS.md`, symlink fanout" pattern: one
user-level doc becomes the source of truth, symlinked into each agent's config
path (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, optional opencode). Edit once,
every agent sees it. This is user/global scope — it does not touch any project.

## Installation

Enable in a project's `.claude/settings.json`:
```json
{
  "extraKnownMarketplaces": {
    "local": { "source": { "source": "directory", "path": "~/agents/coding/plugins" } }
  },
  "enabledPlugins": { "setup@local": true }
}
```

For a truly empty folder, `/setup` needs the setup plugin available before any
project `settings.json` exists — so enable `setup@local` in your *global*
`~/.claude/settings.json`, and `/setup` is then reachable in any new directory.

## Related Plugins

- **system** — health monitoring (`/system:audit`, `/system:status`, `/system:cleanup`)
- **workflow** — development workflow (`/align`, `/plan`, `/next`, `/ship`)
- **memory** — knowledge management (`/index`, `/handoff`)
