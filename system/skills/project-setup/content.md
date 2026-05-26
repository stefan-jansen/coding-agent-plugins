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
AGENTS.md                  # canonical project doc (Codex reads natively)
CLAUDE.md                  # one line: @AGENTS.md
.agents/                   # SHARED state for both Claude and Codex
├── memory/
│   ├── project_state.md
│   ├── conventions.md
│   └── decisions.md
├── transitions/           # YYYY-MM-DD/HH.md (auto-created)
└── work/                  # active work units
.claude/                   # CLAUDE-SPECIFIC ONLY
├── settings.json          # plugins, hooks, permissions
├── hooks/
│   └── init-transition.sh
└── commands/              # project slash-commands
```

## AGENTS.md Template

```markdown
# [Project Name]

## Purpose

<one-paragraph statement>

## Code vs data layout

| Path | Purpose |
|---|---|
| | |

## Common bash invocations

```bash
```

## Slash commands (Claude Code)

- See `.claude/commands/`

## Project memory

@.agents/memory/project_state.md
@.agents/memory/conventions.md
@.agents/memory/decisions.md

Session progress goes to `.agents/transitions/YYYY-MM-DD/HH.md` — the hook
auto-creates the hourly file on each prompt.
```

## CLAUDE.md (one line)

```markdown
@AGENTS.md
```

## Quick Setup Commands

```bash
# Create structure
mkdir -p .agents/{memory,transitions,work}
mkdir -p .claude/{hooks,commands}
touch .agents/transitions/.gitkeep .agents/work/.gitkeep

# Create settings.json (edit path for your system)
cat > .claude/settings.json << 'EOF'
[paste settings.json template above]
EOF

# Create hook
cat > .claude/hooks/init-transition.sh << 'HOOK'
[paste hook script above]
HOOK
chmod +x .claude/hooks/init-transition.sh

# CLAUDE.md is one line
echo "@AGENTS.md" > CLAUDE.md

# Initialize git if needed
git init
echo ".agents/transitions/" >> .gitignore  # Optional: exclude transitions
```

## Language-Specific Additions

**Python**: Claude can generate pyproject.toml, .pre-commit-config.yaml, Makefile on demand.

**JavaScript**: Claude can generate package.json, tsconfig.json, eslint config on demand.

**Existing projects**: Add the structure above; existing source code stays put.
