---
allowed-tools: [Read, Write, Bash]
argument-hint: "[--force] [--from-existing] [--claude-only] [--codex-only] [--opencode]"
description: Initialize user-level agent configuration as a single canonical ~/AGENTS.md symlinked into each agent's config location. Cross-agent by design (Claude + Codex + optionally opencode).
---

# User Configuration Setup

Installs the "single AGENTS.md, symlink fanout" pattern popularized by
kunchenguid. One canonical `~/AGENTS.md` becomes the source of truth; each
agent's config path (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`,
`~/.config/opencode/AGENTS.md`) is a symlink to it. Edit once, all agents see it.

Flags:

- `--force`             Overwrite existing `~/AGENTS.md` or replace non-symlink targets.
- `--from-existing`     If a target is already a real file, back it up (append `.pre-symlink-TIMESTAMP`) then symlink. Default: refuse and warn.
- `--claude-only`       Only link `~/.claude/CLAUDE.md`.
- `--codex-only`        Only link `~/.codex/AGENTS.md`.
- `--opencode`          Also link `~/.config/opencode/AGENTS.md`. Off by default.

```bash
CANONICAL="$HOME/AGENTS.md"
CLAUDE_TARGET="$HOME/.claude/CLAUDE.md"
CODEX_TARGET="$HOME/.codex/AGENTS.md"
OPENCODE_TARGET="$HOME/.config/opencode/AGENTS.md"

FORCE=false
FROM_EXISTING=false
LINK_CLAUDE=true
LINK_CODEX=true
LINK_OPENCODE=false

for arg in "$@"; do
    case "$arg" in
        --force)          FORCE=true ;;
        --from-existing)  FROM_EXISTING=true ;;
        --claude-only)    LINK_CODEX=false ;;
        --codex-only)     LINK_CLAUDE=false ;;
        --opencode)       LINK_OPENCODE=true ;;
    esac
done

TS=$(date -u +%Y-%m-%dT%H%M%S)

# --- Step 1: canonical ~/AGENTS.md --------------------------------------

if [ -f "$CANONICAL" ] && [ "$FORCE" != true ]; then
    echo "SKIP $CANONICAL already exists. Use --force to overwrite, or edit manually."
else
    cat > "$CANONICAL" << 'EOF'
# Personal Agent Guidelines

Canonical user-level rules for all coding agents. This file is the single source
of truth; `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, and any future agent
config paths are symlinks to it.

## Style

- Never use the em dash "—". Use plain dash "-" instead.
- Do not repeat what the codebase already shows; point to the authoritative file or command instead. Prefer rewriting or pruning existing entries over appending new ones.

## Making technical decisions

- Do not give much weight to development cost when choosing between approaches. Prefer quality, simplicity, robustness, scalability, and long-term maintainability. Agents run continuously; human calendar estimates ("this will take weeks") do not apply.

## Bug fixes

- Always start with reproducing the bug in an E2E setting as closely aligned with how an end user would experience it as possible. Only then diagnose and fix.

## Engineering excellence

- Apply high standards to engineering hygiene: lint, test failures, and test flakiness. If you see one, even if it is not caused by what you are working on right now, still get it fixed along the way.
- For UI work, be picky about pixel perfection. Fix visible defects even when unrelated to the current task.

## Git

- Use plain `git commit`. Where a repo has pre-commit configured, run `pre-commit install` once so the quality checks fire on every commit.
- Never bypass checks with `--no-verify` / `-n`. If a hook fails, investigate and fix the underlying cause.
- Do NOT auto-add agent name as co-author in commit messages. No `Co-Authored-By: Claude ...` or `Generated with Claude Code` footer.

## Do not modify auto-generated files

- Never manually edit `CHANGELOG.md` or any file marked as auto-generated. Regenerate via the appropriate tool.

## Agent interop convention

Most projects are worked on with multiple agents. Agent infrastructure follows
a shared path convention so state stays in one place:

| Path | Audience | Purpose |
|---|---|---|
| `AGENTS.md` (project root) | All agents | Canonical project instructions. Codex reads natively; Claude includes via `CLAUDE.md` one-liner (`@AGENTS.md`). |
| `CLAUDE.md` (project root) | Claude only | One line: `@AGENTS.md`. |
| `.workspace/memory/*.md` | All | Persistent project state. `project_state.md`, `conventions.md`, `decisions.md`. |
| `.workspace/transitions/YYYY-MM-DD/HH.md` | All | Hourly session progress. Hook auto-creates the file. Shared across agents. |
| `.workspace/work/` | All | Active work units. Multi-session tracking. |
| `.claude/settings.json`, `.claude/hooks/`, `.claude/commands/` | Claude only | Claude Code config. |
| `~/.codex/` | Codex only | Codex global config. |

**New projects**: scaffold `.workspace/`-shaped from day one. Setup commands
(`/setup:python`, `/setup:javascript`, `/setup:existing`) produce this layout.
Do NOT seed `.claude/memory/`, `.claude/transitions/`, or `.claude/work/`.

**Existing projects**: leave pre-migration data in `.claude/` alone (still
readable); write new state to `.workspace/`.

## File hygiene

- Do not create documentation files (`*.md`, `README`) unless explicitly requested.
- Do not add comments, docstrings, or type annotations to unchanged code.
- Avoid over-engineering: only make the changes directly requested.

## Security

- Never commit `.env`, `credentials.json`, or files containing secrets.

## Context management

- At 80%+ context: create handoff with `/handoff`.
- Handoff format: `.workspace/transitions/YYYY-MM-DD/HHMMSS.md`.

## Goal-driven execution

Before non-trivial work, restate the task as a verifiable goal, not an imperative:

- "Add validation" -> "Write tests for invalid inputs, then make them pass"
- "Fix the bug" -> "Write a test that reproduces it, then make it pass"
- "Refactor X" -> "Tests pass before and after; no behavior change"

Self-test before finishing: would a senior engineer call this overcomplicated?
If yes, simplify before declaring done.

## Working conventions

Add your language/tooling preferences here. Examples:

- Python: `uv`, `ruff` (100-char), `pytest` via `uv run pytest`.
- JavaScript: preferred package manager, formatter, test runner.
- Type checking: which tool and where it runs.
EOF
    echo "WROTE $CANONICAL"
fi

# --- Step 2: symlink each requested target -------------------------------

link_target() {
    local target="$1"
    local label="$2"
    local dir=$(dirname "$target")
    mkdir -p "$dir"

    if [ -L "$target" ]; then
        local current=$(readlink "$target")
        if [ "$current" = "$CANONICAL" ]; then
            echo "SKIP $target already points at $CANONICAL"
            return 0
        fi
        if [ "$FORCE" = true ]; then
            rm "$target"
        else
            echo "WARN $target is a symlink to $current. Use --force to replace."
            return 1
        fi
    elif [ -f "$target" ]; then
        if [ "$FROM_EXISTING" = true ] || [ "$FORCE" = true ]; then
            local backup="${target}.pre-symlink-${TS}"
            mv "$target" "$backup"
            echo "BACKUP $target -> $backup"
        else
            echo "WARN $target is a real file. Use --from-existing to back up and symlink, or --force to replace unconditionally."
            return 1
        fi
    fi

    ln -s "$CANONICAL" "$target"
    echo "SYMLINK $target -> $CANONICAL"
}

[ "$LINK_CLAUDE"   = true ] && link_target "$CLAUDE_TARGET"   "Claude"
[ "$LINK_CODEX"    = true ] && link_target "$CODEX_TARGET"    "Codex"
[ "$LINK_OPENCODE" = true ] && link_target "$OPENCODE_TARGET" "opencode"

echo ""
echo "Done. Edit $CANONICAL to add personal preferences."
echo "The interop convention sections should stay; setup commands rely on them."
```
