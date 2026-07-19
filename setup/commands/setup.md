---
allowed-tools: [Read, Write, Bash, AskUserQuestion]
argument-hint: "[project-name]"
description: Bootstrap a project's agent infrastructure (.workspace/ + AGENTS.md + CLAUDE.md) through a short interview. Detects language and existing setup; idempotent; produces the canonical Claude + Codex shared layout.
---

# /setup — bootstrap a project for Claude + Codex

You are running the **SETUP** step. Your job: take the current directory —
empty, or an existing repo — and bring it to the canonical agent layout that
both Claude Code and Codex expect, **through a short interview** so the
resulting `AGENTS.md` describes *this* project rather than a placeholder
skeleton.

This is the single, canonical setup command. There is no `/setup:python`,
`/setup:existing`, or `/setup:javascript` — this command subsumes all of them.
(`/setup:user` is separate: it sets up your *global* `~/AGENTS.md`, not a
project.)

## Principles

- **Dialogue-driven, but only for what the environment can't tell you.** Detect
  first; ask only the questions the files don't already answer. An empty folder
  needs more questions than a mature repo.
- **Idempotent.** Safe to re-run. Never overwrite an existing `AGENTS.md`,
  memory file, or `settings.json` — enrich or skip. `CLAUDE.md` is the one
  exception: it is always exactly `@AGENTS.md`, so rewriting it is safe.
- **Canonical layout.** `AGENTS.md` (root) + `CLAUDE.md` (`@AGENTS.md`) +
  `.workspace/{memory,transitions,work}` (shared state) + `.claude/`
  (Claude-only config). NEVER create `.claude/memory/`,
  `.claude/transitions/`, or `.claude/work/` — those are deprecated.
- **Self-contained.** Everything this command needs is inline. No sourcing of
  external scripts or shared template files.

---

## Phase 1 — Detect (read-only)

Run this block and read the report before asking anything.

```bash
echo "=== Project detection ==="
PROJECT_NAME="${1:-$(basename "$PWD")}"
echo "name: $PROJECT_NAME"
echo "cwd:  $PWD"

# Is this a git repo? Is it empty?
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "git: yes ($(git rev-parse --show-toplevel))"
else
  echo "git: no"
fi
FILECOUNT=$(find . -maxdepth 1 -mindepth 1 ! -name '.git' | wc -l | tr -d ' ')
echo "top-level entries (excl .git): $FILECOUNT"

# Already set up?
for f in AGENTS.md CLAUDE.md .workspace .claude/settings.json; do
  [ -e "$f" ] && echo "present: $f" || echo "absent:  $f"
done

# Language signals
echo "--- language signals ---"
[ -f pyproject.toml ] && echo "python: pyproject.toml"
[ -f setup.py ]       && echo "python: setup.py"
[ -f requirements.txt ] && echo "python: requirements.txt"
[ -f package.json ]   && echo "node: package.json"
[ -f go.mod ]         && echo "go: go.mod"
[ -f Cargo.toml ]     && echo "rust: Cargo.toml"
ls *.py >/dev/null 2>&1 && echo "python: loose .py files"

# Locate a plugin marketplace to wire into settings.json
echo "--- marketplace ---"
MARKET=""
for cand in "$HOME/agents/coding/plugins" "$HOME/coding-agent-plugins" "$HOME/agents/plugins"; do
  if [ -f "$cand/.claude-plugin/marketplace.json" ]; then MARKET="$cand"; break; fi
done
[ -n "$MARKET" ] && echo "marketplace: $MARKET" || echo "marketplace: not found (will use placeholder)"
```

Interpret the report:

- **Fully set up** (`AGENTS.md` + `.workspace` + `settings.json` all present):
  tell the user it's already bootstrapped, offer to *enrich* `AGENTS.md` via the
  interview instead of regenerating, and stop the mechanical phases unless they
  ask.
- **Partially set up:** run the generation phase — it only fills what's missing.
- **Empty / fresh:** run the full flow.

---

## Phase 2 — Interview (short, forceful, one question at a time)

Gather what `AGENTS.md` needs and the detector couldn't infer. **Ask one
question at a time**, react to each answer, and skip anything the environment
already answered. Do not batch. Do not accept vague answers — an `AGENTS.md`
built from "it's a tool for stuff" is worthless.

Cover, at minimum:

1. **Purpose** — one or two sentences: what is this project, who is it for, what
   is true when it works? Challenge fluff.
2. **What it deliberately is NOT** — the scope hedge. Force at least one
   exclusion; this is what keeps future agents from over-building.
3. **Hard rules** — load-bearing constraints an agent must not violate (pinned
   versions, "never touch X", data that must not be committed, a required tool).
   If there are none yet, say so explicitly rather than inventing them.
4. **Primary language / tooling** — only if detection was ambiguous or the folder
   is empty. Use `AskUserQuestion` for this discrete choice. If the project is
   Python (detected or chosen), ask whether to also scaffold Python tooling
   (Phase 5).

Adapt the depth to the project: a throwaway needs two questions; a system
that will host real work deserves the full set. Play the answers back in
3-5 bullets and get an explicit "yes" before writing `AGENTS.md`.

---

## Phase 3 — Generate agent infrastructure (idempotent)

Run this once the interview is confirmed. It creates only what's missing.

```bash
set -e
WS=".workspace"; CL=".claude"
PROJECT_NAME="${1:-$(basename "$PWD")}"

# Shared state (Claude + Codex)
mkdir -p "$WS/memory/auto" "$WS/transitions" "$WS/work"
touch "$WS/memory/auto/.gitkeep" "$WS/transitions/.gitkeep" "$WS/work/.gitkeep"

# Claude-only config
mkdir -p "$CL/hooks" "$CL/commands"

# Hourly transition hook (writes to .workspace/transitions/)
if [ ! -f "$CL/hooks/init-transition.sh" ]; then
cat > "$CL/hooks/init-transition.sh" << 'HOOK_EOF'
#!/bin/bash
# Auto-create the hourly transition file: .workspace/transitions/YYYY-MM-DD/HH.md
set -e
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
DIR="$ROOT/.workspace/transitions/$(date +%Y-%m-%d)"
FILE="$DIR/$(date +%H).md"
mkdir -p "$DIR"
[ -f "$FILE" ] || printf '# Session Progress: %s %s:00\n\n---\n\n' "$(date +%Y-%m-%d)" "$(date +%H)" > "$FILE"
exit 0
HOOK_EOF
chmod +x "$CL/hooks/init-transition.sh"
echo "created: $CL/hooks/init-transition.sh"
fi
HOOK_PATH="$PWD/$CL/hooks/init-transition.sh"

# Resolve marketplace path (detected in Phase 1; placeholder if absent)
MARKET=""
for cand in "$HOME/agents/coding/plugins" "$HOME/coding-agent-plugins" "$HOME/agents/plugins"; do
  [ -f "$cand/.claude-plugin/marketplace.json" ] && { MARKET="$cand"; break; }
done
[ -n "$MARKET" ] || MARKET="~/path/to/coding-agent-plugins"

# settings.json — only if absent (never clobber a real one)
if [ ! -f "$CL/settings.json" ]; then
cat > "$CL/settings.json" << SETTINGS_EOF
{
  "extraKnownMarketplaces": {
    "local": { "source": { "source": "directory", "path": "$MARKET" } }
  },
  "enabledPlugins": {
    "system@local": true,
    "workflow@local": true,
    "memory@local": true,
    "development@local": true,
    "transition@local": true
  },
  "autoMemoryDirectory": "./.workspace/memory/auto",
  "hooks": {
    "UserPromptSubmit": [
      { "matcher": "", "hooks": [ { "type": "command", "command": "$HOOK_PATH" } ] }
    ]
  }
}
SETTINGS_EOF
echo "created: $CL/settings.json (marketplace: $MARKET)"
else
  echo "kept: $CL/settings.json (already present)"
fi

# Memory seeds — only if absent
if [ ! -f "$WS/memory/project_state.md" ]; then
cat > "$WS/memory/project_state.md" << EOF
# Project state — $PROJECT_NAME

## What's working

-

## What's stubbed or absent

-

## Decisions to make

-
EOF
fi

if [ ! -f "$WS/memory/conventions.md" ]; then
cat > "$WS/memory/conventions.md" << 'EOF'
# Conventions

## Code

-

## Commits

- Plain `git commit`. Where pre-commit is configured, run `pre-commit install`
  once so checks fire automatically. Never `--no-verify`.
- Conventional-commit style: `feat:`, `fix:`, `chore:`, `docs:`.

## Infrastructure

- Memory + transitions live at `.workspace/` (shared by Claude and Codex). NOT `.claude/memory/`.
- `.claude/` holds only Claude-specific config: `settings.json`, `hooks/`, `commands/`.
- Session progress goes to `.workspace/transitions/YYYY-MM-DD/HH.md`.
EOF
fi

if [ ! -f "$WS/memory/decisions.md" ]; then
cat > "$WS/memory/decisions.md" << 'EOF'
# Decisions

Record load-bearing choices with the reasoning. Future agents read this
before suggesting alternatives.

## YYYY-MM-DD: <Decision title>

**Why**:

**Trade-off**:
EOF
fi

# CLAUDE.md is always exactly the include (safe to rewrite)
echo "@AGENTS.md" > CLAUDE.md
echo "infrastructure ready."
```

---

## Phase 4 — Write AGENTS.md from the interview

If `AGENTS.md` already exists, do NOT overwrite it — offer to weave the
interview answers into the existing file instead, and show the diff first.

Otherwise, write `AGENTS.md` with the **Write** tool (not bash), filling
`Purpose`, `What this repo deliberately is NOT`, `Code vs data layout`, and
`Hard rules` from the interview. Keep the memory / session-progress / layout
sections verbatim — they are the canonical wiring and must not be paraphrased.

Use this structure:

```markdown
# <PROJECT_NAME>

## Purpose

<interview: one paragraph — what this project is and who it's for>

## What this repo deliberately is NOT

<interview: the scope hedge — at least one explicit exclusion>

## Code vs data layout

| Path | Purpose |
|---|---|
| <fill from detection + interview> | |

## Hard rules

- <interview: load-bearing constraints; omit the section only if the user
  confirmed there are none yet>

## Common bash invocations

​```bash
<fill if known — build/test/lint entry points; leave empty otherwise>
​```

## Slash commands (Claude Code)

- See `.claude/commands/` for project-specific commands.

## Project memory

Persistent project state — survives `/clear` for Claude, read on demand by Codex:

@.workspace/memory/project_state.md
@.workspace/memory/conventions.md
@.workspace/memory/decisions.md

### Claude auto-memory (writer-asymmetric)

Claude Code writes autonomous learnings to `.workspace/memory/auto/` —
redirected here from the default `~/.claude/projects/<slug>/memory/` via
`autoMemoryDirectory` in `.claude/settings.json`. First 200 lines of
`MEMORY.md` load into every Claude session. Codex has no native equivalent
but reads the same file via `@-include`:

@.workspace/memory/auto/MEMORY.md

Model-authored memory accumulates through Claude sessions only.
Codex-only sessions rely on the human-curated files above.

### Session progress

Session progress goes to `.workspace/transitions/YYYY-MM-DD/HH.md` — the hook
auto-creates the hourly file on each prompt. Append progress every
15-20 min or at milestones; both Claude and Codex sessions share it.

​```bash
ls -r .workspace/transitions/$(date +%Y-%m-%d)/*.md   # newest first
​```

## Agent infrastructure layout

​```
AGENTS.md                  # this file — Codex reads natively
CLAUDE.md                  # one line: @AGENTS.md
.workspace/                # SHARED state for both Claude and Codex
  memory/                  #   persistent context (referenced above via @-include)
    auto/                  #     Claude auto-memory (harness writes; Codex reads)
  transitions/             #   hourly session progress
  work/                    #   active work units / plans
.claude/                   # CLAUDE-SPECIFIC ONLY (different schema from Codex)
  settings.json            #   plugins, hooks, permissions, autoMemoryDirectory
  hooks/                   #   init-transition.sh
  commands/                #   project slash-commands
​```
```

(The three `​```` fences above carry a zero-width marker only so this template
nests inside the command file — emit normal ```` ``` ```` fences in the real
`AGENTS.md`.)

---

## Phase 5 — Optional Python tooling (only if Python + user opted in)

If the project is Python and the user wanted tooling scaffolded, create these
only when absent. Skip the whole phase otherwise.

```bash
set -e
PROJECT_NAME="${1:-$(basename "$PWD")}"

if [ ! -f pyproject.toml ]; then
cat > pyproject.toml << EOF
[project]
name = "$PROJECT_NAME"
version = "0.1.0"
description = ""
requires-python = ">=3.10"
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8.0", "pytest-cov>=5.0", "ruff>=0.5.0", "pre-commit>=3.7"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]

[tool.pytest.ini_options]
testpaths = ["tests"]
EOF
echo "created: pyproject.toml"
fi

if [ ! -f .pre-commit-config.yaml ]; then
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
EOF
echo "created: .pre-commit-config.yaml"
fi

grep -q '^\.venv/' .gitignore 2>/dev/null || cat >> .gitignore << 'EOF'
__pycache__/
*.py[cod]
.venv/
.pytest_cache/
.ruff_cache/
.coverage
dist/
*.egg-info/
.env
EOF
mkdir -p "src/$PROJECT_NAME" tests
[ -f "src/$PROJECT_NAME/__init__.py" ] || touch "src/$PROJECT_NAME/__init__.py"
echo "python tooling ready. Next: uv venv && uv pip install -e '.[dev]' && pre-commit install"
```

---

## Phase 6 — Continuous review (roborev), opt-in

Ask once: **"Enable roborev continuous code review on every commit? [Y/n]"**
Default yes. If yes:

```bash
if command -v jq >/dev/null 2>&1 && [ -f .claude/settings.json ]; then
  tmp=$(mktemp) && jq '.enabledPlugins["roborev@local"] = true' .claude/settings.json > "$tmp" && mv "$tmp" .claude/settings.json && echo "enabled: roborev@local"
fi
command -v roborev >/dev/null 2>&1 && roborev init >/dev/null 2>&1 && echo "roborev init: hook installed" || echo "install roborev (https://roborev.io) then run 'roborev init'"
```

---

## Done

Summarize what was created vs. skipped, then point the user at the next step:
- Fill any remaining blanks in `AGENTS.md` and `.workspace/memory/project_state.md`.
- If Python tooling was scaffolded: `uv venv && uv pip install -e '.[dev]' && pre-commit install`.
- Start work with `/align` for the first work unit.
