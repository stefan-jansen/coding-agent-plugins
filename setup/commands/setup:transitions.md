---
allowed-tools: [Read, Write, Edit, Bash]
argument-hint: ""
description: Add hourly session progress tracking to existing project (migration command - retire when all projects updated)
---

# Add Session Progress Tracking

This command adds automatic hourly transition file tracking to your project.

**What it does:**
1. Creates `.claude/hooks/init-transition.sh` - Hook that creates hourly progress files
2. Updates `.claude/settings.json` - Adds UserPromptSubmit hook
3. Updates `CLAUDE.md` - Adds progress tracking instructions

## Implementation

```bash
# Check we're in a project with .claude directory
if [ ! -d ".claude" ]; then
    echo "❌ No .claude directory found. Run /setup:existing first."
    exit 1
fi

echo "🔄 Adding session progress tracking..."
echo ""

# Create hooks directory
mkdir -p .claude/hooks

# Create the transition hook
cat > .claude/hooks/init-transition.sh << 'HOOK_EOF'
#!/bin/bash
# Initialize hourly transition file for session progress tracking
# This hook runs on UserPromptSubmit to ensure the hourly file exists
# Format: .claude/transitions/YYYY-MM-DD/HH.md (e.g., 19.md for 7pm hour)

set -e

# Get project root (where .claude/ directory is)
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
TRANSITIONS_DIR="$PROJECT_ROOT/.claude/transitions"
TODAY=$(date +%Y-%m-%d)
HOUR=$(date +%H)
TODAY_DIR="$TRANSITIONS_DIR/$TODAY"
HOURLY_FILE="$TODAY_DIR/${HOUR}.md"

# Create today's transition directory if it doesn't exist
mkdir -p "$TODAY_DIR"

# Initialize hourly file if it doesn't exist
if [ ! -f "$HOURLY_FILE" ]; then
    cat > "$HOURLY_FILE" << EOF
# Session Progress: $TODAY ${HOUR}:00

---

EOF
fi

# Exit silently (hook output not visible to Claude anyway)
exit 0
HOOK_EOF

chmod +x .claude/hooks/init-transition.sh
echo "✅ Created .claude/hooks/init-transition.sh"
```

Now update settings.json to add the hook:

```bash
# Get absolute path to hook
HOOK_PATH="$(pwd)/.claude/hooks/init-transition.sh"

# Check if settings.json exists
if [ ! -f ".claude/settings.json" ]; then
    echo "❌ No .claude/settings.json found. Run /setup:existing first."
    exit 1
fi

echo "📝 Updating .claude/settings.json..."
```

I'll update the settings.json to add the UserPromptSubmit hook configuration. Let me read the current settings and merge the hook configuration.

```bash
# Show what will be added
echo ""
echo "Hook configuration to add:"
echo '  "UserPromptSubmit": [{'
echo '    "matcher": "",'
echo '    "hooks": [{"type": "command", "command": "PATH/.claude/hooks/init-transition.sh"}]'
echo '  }]'
echo ""
```

Now I'll add the progress tracking instructions to CLAUDE.md:

**Progress Tracking Section for CLAUDE.md:**

```markdown
## 🔄 Session Progress Tracking (MANDATORY)

**Write progress to the current hourly transition file throughout the session.**

**File**: `.claude/transitions/YYYY-MM-DD/HH.md` (hook creates this automatically)

Example: `.claude/transitions/2025-12-15/19.md` for the 7pm hour

### When to Update (Every 15-20 minutes or at milestones)

Append to the **current hour's file** with:
```markdown
## HH:MM - [Brief Title]
- What was accomplished
- Current state
- Next steps if interrupted
```

### Why Hourly Files
- 20+ auto-compact events can happen per day
- Easier to pinpoint specific time windows
- Read files in reverse order to find latest context
- Smaller files = faster to scan

### Quick Update Command
```bash
cat >> .claude/transitions/$(date +%Y-%m-%d)/$(date +%H).md << 'EOF'
## HH:MM - Title
- Progress notes here
EOF
```
```

## Final Steps

After running this command:

1. **Manually add the hook to settings.json** if not auto-merged:
```json
"hooks": {
  "UserPromptSubmit": [
    {
      "matcher": "",
      "hooks": [
        {
          "type": "command",
          "command": "/absolute/path/to/project/.claude/hooks/init-transition.sh"
        }
      ]
    }
  ]
}
```

2. **Add the progress tracking section** to the top of your CLAUDE.md (after the title)

3. **Test**: Send a message - hook should create `.claude/transitions/YYYY-MM-DD/HH.md`

---

**Migration Note**: This command can be retired once all projects have been updated and new projects include this by default via `/setup:existing`.
