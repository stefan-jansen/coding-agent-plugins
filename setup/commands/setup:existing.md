---
allowed-tools: [Read, Write, Bash]
argument-hint: ""
description: Add Claude Code framework to an existing project with auto-detection
skills: [shared-setup-patterns]
---

# Add Claude Framework to Existing Project

I'll add the Claude Code Framework to your existing project, auto-detecting the language and framework.

```bash
readonly CLAUDE_DIR=".claude"
readonly AGENTS_DIR=".agents"

echo "🔧 Adding Claude Code Framework to existing project..."
echo ""

# Auto-detect project type using shared-setup-patterns skill
echo "Detecting project characteristics..."

# Use framework detection patterns from skill to identify:
# - Language (Python, JavaScript, Go, Rust)
# - Framework (FastAPI, Django, Next.js, Express, etc.)
# - Tools (pytest, Jest, etc.)

# Create .agents/ structure (shared by Claude + Codex)
mkdir -p $AGENTS_DIR/memory
mkdir -p $AGENTS_DIR/transitions
mkdir -p $AGENTS_DIR/work
touch $AGENTS_DIR/transitions/.gitkeep
touch $AGENTS_DIR/work/.gitkeep

# Create .claude/ structure (Claude-specific only)
mkdir -p $CLAUDE_DIR/hooks
mkdir -p $CLAUDE_DIR/commands

# Create hourly transition hook (writes to .agents/transitions/)
cat > $CLAUDE_DIR/hooks/init-transition.sh << 'HOOK_EOF'
#!/bin/bash
# Initialize hourly transition file for session progress tracking
# Format: .agents/transitions/YYYY-MM-DD/HH.md
set -e
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
TRANSITIONS_DIR="$PROJECT_ROOT/.agents/transitions"
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
echo "✅ Created .claude/hooks/init-transition.sh (writes to .agents/transitions/)"

# Get absolute path for hook
HOOK_PATH="$(pwd)/$CLAUDE_DIR/hooks/init-transition.sh"

# Create settings.json with plugins and hooks
cat > $CLAUDE_DIR/settings.json << SETTINGS_EOF
{
  "extraKnownMarketplaces": {
    "local": {
      "source": {
        "source": "directory",
        "path": "/home/stefan/agents/plugins"
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

# Seed memory templates if missing (don't overwrite existing)
PROJECT_NAME=$(basename "$PWD")

if [ ! -f $AGENTS_DIR/memory/project_state.md ]; then
cat > $AGENTS_DIR/memory/project_state.md << EOF
# Project state — $PROJECT_NAME

## What's working

-

## What's stubbed or absent

-

## Decisions to make

-
EOF
fi

if [ ! -f $AGENTS_DIR/memory/conventions.md ]; then
cat > $AGENTS_DIR/memory/conventions.md << 'EOF'
# Conventions

## Code

-

## Commits

- Use `git safe-commit -m "..."`. Never `--no-verify`.
- Conventional-commit style: `feat:`, `fix:`, `chore:`, `docs:`.

## Infrastructure

- Memory + transitions live at `.agents/` (shared by Claude and Codex). NOT `.claude/memory/`.
- `.claude/` holds only Claude-specific config: `settings.json`, `hooks/`, `commands/`.
- Every project session writes progress to `.agents/transitions/YYYY-MM-DD/HH.md`.
EOF
fi

if [ ! -f $AGENTS_DIR/memory/decisions.md ]; then
cat > $AGENTS_DIR/memory/decisions.md << 'EOF'
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

@.agents/memory/project_state.md
@.agents/memory/conventions.md
@.agents/memory/decisions.md

Session progress goes to \`.agents/transitions/YYYY-MM-DD/HH.md\` — the hook
auto-creates the hourly file on each prompt. Append progress every
15–20 min or at milestones; both Claude and Codex sessions share it.

\`\`\`bash
ls -r .agents/transitions/\$(date +%Y-%m-%d)/*.md   # newest first
\`\`\`

## Agent infrastructure layout

\`\`\`
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
echo "  .agents/memory/       - Persistent project state (project_state, conventions, decisions)"
echo "  .agents/transitions/  - Hourly session progress (auto-created by hook)"
echo "  .agents/work/         - Active work units"
echo "  .claude/settings.json - Plugins + UserPromptSubmit transition hook"
echo "  .claude/hooks/        - init-transition.sh (writes to .agents/transitions/)"
echo ""
echo "Next: Edit AGENTS.md (purpose, layout, commands) and .agents/memory/ files for your project."
```
