---
allowed-tools: [Read, Write, Bash]
argument-hint: ""
description: Add Claude Code framework to an existing project with auto-detection
skills: [shared-setup-patterns]
---

# Add Claude Framework to Existing Project

I'll add the Claude Code Framework to your existing project, auto-detecting the language and framework.

**Continuous review opt-in.** This setup enables [roborev](https://roborev.io)
by default — a local background reviewer that runs on every commit. Before
executing the bash, ask the user:

> Install roborev for continuous code review? [Y/n]

Default is yes. If they decline, prepend `ROBOREV_OPTIN=no` to the bash
invocation; everything else proceeds unchanged.

```bash
readonly CLAUDE_DIR=".claude"
readonly WORKSPACE_DIR=".workspace"

echo "🔧 Adding Claude Code Framework to existing project..."
echo ""

# Auto-detect project type using shared-setup-patterns skill
echo "Detecting project characteristics..."

# Use framework detection patterns from skill to identify:
# - Language (Python, JavaScript, Go, Rust)
# - Framework (FastAPI, Django, Next.js, Express, etc.)
# - Tools (pytest, Jest, etc.)

# Create .workspace/ structure (shared by Claude + Codex)
mkdir -p $WORKSPACE_DIR/memory
mkdir -p $WORKSPACE_DIR/memory/auto      # Claude auto-memory target (see settings.json below)
mkdir -p $WORKSPACE_DIR/transitions
mkdir -p $WORKSPACE_DIR/work
touch $WORKSPACE_DIR/memory/auto/.gitkeep
touch $WORKSPACE_DIR/transitions/.gitkeep
touch $WORKSPACE_DIR/work/.gitkeep

# Create .claude/ structure (Claude-specific only)
mkdir -p $CLAUDE_DIR/hooks
mkdir -p $CLAUDE_DIR/commands

# Create hourly transition hook (writes to .workspace/transitions/)
cat > $CLAUDE_DIR/hooks/init-transition.sh << 'HOOK_EOF'
#!/bin/bash
# Initialize hourly transition file for session progress tracking
# Format: .workspace/transitions/YYYY-MM-DD/HH.md
set -e
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
TRANSITIONS_DIR="$PROJECT_ROOT/.workspace/transitions"
TODAY=$(date +%Y-%m-%d)
HOUR=$(date +%H)
TODAY_DIR="$TRANSITIONS_DIR/$TODAY"
HOURLY_FILE="$TODAY_DIR/${HOUR}.md"
mkdir -p "$TODAY_DIR"
if [ ! -f "$HOURLY_FILE" ]; then
    echo "# Session Progress: $TODAY ${HOUR}:00" > "$HOURLY_FILE"
    echo "" >> "$HOURLY_FILE"
    echo "---" >> "$HOURLY_FILE"
    echo "" >> "$HOURLY_FILE"
fi
exit 0
HOOK_EOF
chmod +x $CLAUDE_DIR/hooks/init-transition.sh
echo "✅ Created .claude/hooks/init-transition.sh (writes to .workspace/transitions/)"

# Get absolute path for hook
HOOK_PATH="$(pwd)/$CLAUDE_DIR/hooks/init-transition.sh"

# Create settings.json with plugins and hooks
cat > $CLAUDE_DIR/settings.json << SETTINGS_EOF
{
  "extraKnownMarketplaces": {
    "local": {
      "source": {
        "source": "directory",
        "path": "~/path/to/coding-agent-plugins"
      }
    }
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
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "$HOOK_PATH"
          }
        ]
      }
    ]
  }
}
SETTINGS_EOF
echo "✅ Created .claude/settings.json with plugins + transition hook"
echo ""

# --- roborev (continuous code review) — opt-in, default Yes ---
# To opt out, set ROBOREV_OPTIN=no before invoking the command.
ROBOREV_OPTIN="${ROBOREV_OPTIN:-yes}"
if [ "$ROBOREV_OPTIN" = "yes" ]; then
  if command -v jq >/dev/null 2>&1; then
    tmp=$(mktemp) && jq '.enabledPlugins["roborev@local"] = true' $CLAUDE_DIR/settings.json > "$tmp" \
      && mv "$tmp" $CLAUDE_DIR/settings.json \
      && echo "✅ Enabled roborev@local in $CLAUDE_DIR/settings.json"
  else
    echo "⚠️  jq not found — manually add \"roborev@local\": true to enabledPlugins"
  fi
  if command -v roborev >/dev/null 2>&1; then
    roborev init >/dev/null 2>&1 \
      && echo "✅ roborev init: post-commit hook installed" \
      || echo "⚠️  roborev init failed; rerun manually after setup"
  else
    echo "ℹ️  Install roborev (https://roborev.io) and run 'roborev init' to enable continuous review."
  fi
fi
# --- end roborev ---

# Seed memory templates if missing (don't overwrite existing)
PROJECT_NAME=$(basename "$PWD")

if [ ! -f $WORKSPACE_DIR/memory/project_state.md ]; then
cat > $WORKSPACE_DIR/memory/project_state.md << EOF
# Project state — $PROJECT_NAME

## What's working

-

## What's stubbed or absent

-

## Decisions to make

-
EOF
fi

if [ ! -f $WORKSPACE_DIR/memory/conventions.md ]; then
cat > $WORKSPACE_DIR/memory/conventions.md << 'EOF'
# Conventions

## Code

-

## Commits

- Use `git safe-commit -m "..."`. Never `--no-verify`.
- Conventional-commit style: `feat:`, `fix:`, `chore:`, `docs:`.

## Infrastructure

- Memory + transitions live at `.workspace/` (shared by Claude and Codex). NOT `.claude/memory/`.
- `.claude/` holds only Claude-specific config: `settings.json`, `hooks/`, `commands/`.
- Every project session writes progress to `.workspace/transitions/YYYY-MM-DD/HH.md`.
EOF
fi

if [ ! -f $WORKSPACE_DIR/memory/decisions.md ]; then
cat > $WORKSPACE_DIR/memory/decisions.md << 'EOF'
# Decisions

Record load-bearing choices with the reasoning. Future agents read this
before suggesting alternatives.

## YYYY-MM-DD: <Decision title>

**Why**:

**Trade-off**:
EOF
fi

# Create AGENTS.md (skip if exists — don't overwrite)
if [ ! -f AGENTS.md ]; then
cat > AGENTS.md << EOF
# $PROJECT_NAME

## Purpose

<one-paragraph statement of what this project is and who it's for>

## Code vs data layout

| Path | Purpose |
|---|---|
| | |

## Common bash invocations

\`\`\`bash
\`\`\`

## Slash commands (Claude Code)

- See \`.claude/commands/\` for project-specific commands.

## Project memory

Persistent project state — survives \`/clear\` for Claude, read on demand by Codex:

@.workspace/memory/project_state.md
@.workspace/memory/conventions.md
@.workspace/memory/decisions.md

### Claude auto-memory (writer-asymmetric)

Claude Code writes autonomous learnings to \`.workspace/memory/auto/\` —
redirected here from the default \`~/.claude/projects/<slug>/memory/\` via
\`autoMemoryDirectory\` in \`.claude/settings.json\`. First 200 lines of
\`MEMORY.md\` load into every Claude session. Codex has no native equivalent
but reads the same file via \`@-include\`:

@.workspace/memory/auto/MEMORY.md

Model-authored memory accumulates through Claude sessions only.
Codex-only sessions rely on the human-curated files above.

### Session progress

Session progress goes to \`.workspace/transitions/YYYY-MM-DD/HH.md\` — the hook
auto-creates the hourly file on each prompt. Append progress every
15–20 min or at milestones; both Claude and Codex sessions share it.

\`\`\`bash
ls -r .workspace/transitions/\$(date +%Y-%m-%d)/*.md   # newest first
\`\`\`

## Agent infrastructure layout

\`\`\`
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
\`\`\`
EOF
fi

# CLAUDE.md is one line — single source of truth via AGENTS.md
# (overwrite is safe — content is canonical)
echo "@AGENTS.md" > CLAUDE.md

echo "✅ Claude Code Framework added!"
echo ""
echo "Created:"
echo "  AGENTS.md             - Canonical project doc (Claude + Codex)"
echo "  CLAUDE.md             - One-line @AGENTS.md include"
echo "  .workspace/memory/       - Persistent project state (project_state, conventions, decisions)"
echo "  .workspace/transitions/  - Hourly session progress (auto-created by hook)"
echo "  .workspace/work/         - Active work units"
echo "  .claude/settings.json - Plugins + UserPromptSubmit transition hook"
echo "  .claude/hooks/        - init-transition.sh (writes to .workspace/transitions/)"
echo ""
echo "Next: Edit AGENTS.md (purpose, layout, commands) and .workspace/memory/ files for your project."
```
