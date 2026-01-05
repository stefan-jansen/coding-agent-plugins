# Project Setup Templates

## .claude/settings.json

```json
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
    "development@local": true
  }
}
```

**Add hooks for session transitions**:
```json
{
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
}
```

## .claude/hooks/init-transition.sh

```bash
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
    cat > "$HOURLY_FILE" << EOF
# Session Progress: $TODAY ${HOUR}:00

---

EOF
fi
exit 0
```

Make executable: `chmod +x .claude/hooks/init-transition.sh`

## Directory Structure

```
.claude/
├── settings.json      # Plugin config
├── work/              # Work units
│   └── ACTIVE_WORK    # Current work pointer
├── memory/            # Project knowledge
│   ├── project_state.md
│   └── decisions.md
├── hooks/             # Session hooks
│   └── init-transition.sh
└── transitions/       # Session handoffs
    └── YYYY-MM-DD/
        └── HH.md
```

## CLAUDE.md Template

```markdown
# [Project Name]

[Brief project description]

## Project Knowledge
@.claude/memory/project_state.md
@.claude/memory/decisions.md

## Session Progress Tracking (MANDATORY)

**File**: `.claude/transitions/YYYY-MM-DD/HH.md` (hook creates automatically)

### When to Update (Every 15-20 minutes or at milestones)
Append progress with:
- What was accomplished
- Current state
- Next steps if interrupted

## Current Work
@.claude/work/ACTIVE_WORK
```

## Quick Setup Commands

```bash
# Create structure
mkdir -p .claude/{work,memory,hooks,transitions}

# Create settings.json (edit path for your system)
cat > .claude/settings.json << 'EOF'
[paste settings.json template above]
EOF

# Create hook
cat > .claude/hooks/init-transition.sh << 'HOOK'
[paste hook script above]
HOOK
chmod +x .claude/hooks/init-transition.sh

# Initialize git if needed
git init
echo ".claude/transitions/" >> .gitignore  # Optional: exclude transitions
```

## Language-Specific Additions

**Python**: Claude can generate pyproject.toml, .pre-commit-config.yaml, Makefile on demand.

**JavaScript**: Claude can generate package.json, tsconfig.json, eslint config on demand.

**Existing projects**: Just add .claude/ directory and CLAUDE.md to existing project.
