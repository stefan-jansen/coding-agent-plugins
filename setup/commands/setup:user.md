---
allowed-tools: [Read, Write, Bash]
argument-hint: "[--force] [--claude-only|--codex-only]"
description: Initialize user-level Claude and/or Codex configuration with the interop convention
---

# User Configuration Setup

I'll initialize your user-level agent configuration files (`~/.claude/CLAUDE.md`,
`~/.codex/AGENTS.md`) with the Claude+Codex interop convention baked in.

By default seeds both. Use `--claude-only` or `--codex-only` to limit. Use
`--force` to overwrite existing files.

```bash
USER_CLAUDE_DIR="$HOME/.claude"
USER_CLAUDE_FILE="$USER_CLAUDE_DIR/CLAUDE.md"
USER_CODEX_DIR="$HOME/.codex"
USER_CODEX_FILE="$USER_CODEX_DIR/AGENTS.md"

FORCE_FLAG=false
SEED_CLAUDE=true
SEED_CODEX=true

for arg in "$@"; do
    case "$arg" in
        --force)        FORCE_FLAG=true ;;
        --claude-only)  SEED_CODEX=false ;;
        --codex-only)   SEED_CLAUDE=false ;;
    esac
done

echo "🔧 Initializing user-level agent configuration..."
echo ""

write_if_safe() {
    local target="$1"
    local label="$2"
    if [ -f "$target" ] && [ "$FORCE_FLAG" != true ]; then
        echo "⚠️  $label already exists at: $target"
        echo "   Use --force to overwrite, or edit manually."
        return 1
    fi
    return 0
}

# --- Claude user config ---------------------------------------------------
if [ "$SEED_CLAUDE" = true ]; then
    mkdir -p "$USER_CLAUDE_DIR"
    if write_if_safe "$USER_CLAUDE_FILE" "Claude user config"; then
        cat > "$USER_CLAUDE_FILE" << 'EOF'
# Claude Code - User Guidelines

## Git

**Always use `git safe-commit`** instead of `git commit` (when available):
```bash
git safe-commit -m "feat: message"
```
This runs pre-commit hooks and quality checks. Never bypass with `--no-verify`.

## Agent interop convention (Claude + Codex)

Most projects are worked on with both Claude and Codex. To avoid duplicated /
out-of-sync state, agent infrastructure follows a strict path convention:

| Path | Audience | Purpose |
|---|---|---|
| `AGENTS.md` (project root) | Codex (native), Claude (via `@AGENTS.md` include) | **Canonical project instructions.** Codex reads natively; Claude includes via `CLAUDE.md` one-liner. |
| `CLAUDE.md` (project root) | Claude only | One line: `@AGENTS.md`. Single source of truth, both agents see it. |
| `.agents/memory/*.md` | Claude (via `@-include` from AGENTS.md), Codex (read-on-demand) | **Persistent project state.** `project_state.md`, `conventions.md`, `decisions.md`. Survives `/clear`. |
| `.agents/transitions/YYYY-MM-DD/HH.md` | Both | **Hourly session progress.** Hook auto-creates the file; append every 15-20 min. Shared between Claude and Codex sessions. |
| `.agents/work/` | Both | **Active work units / plans.** Multi-session work tracking. |
| `.claude/settings.json`, `.claude/hooks/`, `.claude/commands/` | Claude only | Claude Code config, hooks, slash-commands. Different schema from Codex; cannot be unified. |
| `~/.codex/` | Codex only | Codex global config + per-machine state. |

**Rule for new projects**: agent infrastructure is `.agents/`-shaped from
day one. Setup commands (`/setup:python`, `/setup:javascript`, `/setup:existing`)
produce this layout. Do NOT seed `.claude/memory/`, `.claude/transitions/`, or
`.claude/work/` for new projects.

**Rule for existing projects**: leave pre-migration data in `.claude/` alone
(still readable on demand) but write new state to `.agents/`. The first time
work touches an old project, scaffold `.agents/` and update `AGENTS.md` /
`CLAUDE.md` accordingly.

## Context Management

- At 80%+ context: create handoff with `/handoff`
- Handoff format: `.agents/transitions/YYYY-MM-DD/HHMMSS.md`

## Working Style

Add personal preferences here:

- Code style preferences
- Communication preferences
- Project organization preferences
EOF
        echo "✅ Created Claude user config at: $USER_CLAUDE_FILE"
    fi
fi

# --- Codex user config ----------------------------------------------------
if [ "$SEED_CODEX" = true ]; then
    mkdir -p "$USER_CODEX_DIR"
    if write_if_safe "$USER_CODEX_FILE" "Codex user config"; then
        cat > "$USER_CODEX_FILE" << 'EOF'
# Codex - User Guidelines

## Git

**Use `git safe-commit`** when available (repos with pre-commit hooks):
```bash
git safe-commit -m "feat: message"
```
Falls back to `git commit` if safe-commit is not on PATH.
Never bypass hooks with `--no-verify`.

## Agent interop convention (Claude + Codex)

Most projects are worked on with both Codex and Claude. Agent infrastructure
follows a shared path convention so both agents access the same memory:

| Path | Audience | Purpose |
|---|---|---|
| `AGENTS.md` (project root) | Codex (native), Claude (via `@AGENTS.md` include) | Canonical project instructions. |
| `CLAUDE.md` (project root) | Claude only | One line: `@AGENTS.md`. |
| `.agents/memory/*.md` | Both | Persistent project state — `project_state.md`, `conventions.md`, `decisions.md`. AGENTS.md `@-includes` them so Codex sees them on every run. |
| `.agents/transitions/YYYY-MM-DD/HH.md` | Both | Hourly session progress. Append every 15-20 min. |
| `.agents/work/` | Both | Active work units. |
| `.codex/` | Codex only | Codex per-project state if any. |
| `.claude/` | Claude only | Claude Code settings, hooks, slash-commands. |
| `~/.codex/` | Codex only | Codex global config. |
| `~/.claude/` | Claude only | Claude Code global config. |

**Rule for new projects**: scaffold `AGENTS.md` + `.agents/` from day one.
**Rule for existing projects**: read pre-migration data in `.claude/` if
present; write new state to `.agents/`.

## Working Conventions

- **Package manager**: `uv` for Python projects (not pip/conda)
- **Linter / formatter**: `ruff`
- **Testing**: `pytest` via `uv run pytest`
- **Type hints**: on public interfaces

## File Hygiene

- Do not create documentation files (*.md, README) unless explicitly requested
- Do not add comments, docstrings, or type annotations to unchanged code
- Avoid over-engineering: only make changes directly requested

## Security

- Never commit `.env`, `credentials.json`, or files containing secrets

## Context Management

- Project memory lives at `.agents/memory/` — read on demand
- Session progress at `.agents/transitions/YYYY-MM-DD/HH.md` — shared with Claude
EOF
        echo "✅ Created Codex user config at: $USER_CODEX_FILE"
    fi
fi

echo ""
echo "Next: edit your user config(s) to add personal preferences."
echo "      The interop convention sections should stay — projects rely on them."
```
