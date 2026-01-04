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

echo "🔧 Adding Claude Code Framework to existing project..."
echo ""

# Auto-detect project type using shared-setup-patterns skill
echo "Detecting project characteristics..."

# Use framework detection patterns from skill to identify:
# - Language (Python, JavaScript, Go, Rust)
# - Framework (FastAPI, Django, Next.js, Express, etc.)
# - Tools (pytest, Jest, etc.)

# Create .claude directory structure
mkdir -p $CLAUDE_DIR/work
mkdir -p $CLAUDE_DIR/memory
mkdir -p $CLAUDE_DIR/reference
mkdir -p $CLAUDE_DIR/hooks
mkdir -p $CLAUDE_DIR/transitions

# Create hourly transition hook
cat > $CLAUDE_DIR/hooks/init-transition.sh << 'HOOK_EOF'
#!/bin/bash
# Initialize hourly transition file for session progress tracking
set -e
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
TRANSITIONS_DIR="$PROJECT_ROOT/.claude/transitions"
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
echo "✅ Created .claude/hooks/init-transition.sh (hourly progress tracking)"

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
echo "I'll also create:"
echo "  - .claude/memory/* (project knowledge files)"
echo "  - CLAUDE.md (project instructions)"
echo ""

# Create project CLAUDE.md with progress tracking
PROJECT_NAME=$(basename "$PWD")
cat > CLAUDE.md << 'CLAUDE_EOF'
# PROJECT_NAME_PLACEHOLDER

## 🔄 Session Progress Tracking (MANDATORY)

**Write progress to the current hourly transition file throughout the session.**

**File**: `.claude/transitions/YYYY-MM-DD/HH.md` (hook creates this automatically)

### When to Update (Every 15-20 minutes or at milestones)

Append to the **current hour's file** with:
```markdown
## HH:MM - [Brief Title]
- What was accomplished
- Current state
- Next steps if interrupted
```

### Why This Matters
- Context can be lost unexpectedly (auto-compact, /clear)
- CLAUDE.md persists but conversation history does not
- Progress file enables seamless continuation

### Quick Update
```bash
cat >> .claude/transitions/$(date +%Y-%m-%d)/$(date +%H).md << 'EOF'
## HH:MM - Title
- Progress notes
EOF
```

---

## Project Knowledge
@.claude/memory/project_state.md
@.claude/memory/dependencies.md
@.claude/memory/conventions.md
@.claude/memory/decisions.md

## Current Work
@.claude/work/README.md
CLAUDE_EOF

# Replace placeholder with actual project name
sed -i "s/PROJECT_NAME_PLACEHOLDER/$PROJECT_NAME/" CLAUDE.md

# Create work README
cat > $CLAUDE_DIR/work/README.md << 'EOF'
# Work Units

Active development work units are organized here with date-prefixed directories:
- YYYY-MM-DD_NN_topic/ - Work unit format with date and running counter

Each work unit contains:
- metadata.json - Work unit metadata and status
- state.json - Task tracking and implementation plan
- Other relevant files for the work

See workflow plugin commands (/explore, /plan, /next, /ship) for managing work units.
EOF

echo "✅ Claude Code Framework added!"
echo ""
echo "Created:"
echo "  .claude/              - Framework directory"
echo "  .claude/hooks/        - Transition hook (auto-creates hourly progress files)"
echo "  .claude/transitions/  - Session progress tracking"
echo "  CLAUDE.md             - Project instructions (with progress tracking)"
echo ""
echo "Features:"
echo "  - Hourly progress files: .claude/transitions/YYYY-MM-DD/HH.md"
echo "  - Auto-created on each prompt via UserPromptSubmit hook"
echo "  - CLAUDE.md instructions persist after /clear"
echo ""
echo "Next: Review and customize CLAUDE.md and .claude/memory/ files for your project."
```
