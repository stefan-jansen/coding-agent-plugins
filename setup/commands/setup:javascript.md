---
allowed-tools: [Read, Write, Bash]
argument-hint: "[project-name]"
description: Set up a new JavaScript/Node.js project with modern tooling and Claude framework integration
skills: [shared-setup-patterns]
---

# JavaScript Project Setup

I'll set up a new JavaScript/Node.js project with Jest, ESLint, Prettier, and the Claude Code Framework.

```bash
# Constants
readonly CLAUDE_DIR=".claude"
readonly AGENTS_DIR=".agents"
PROJECT_NAME="${1}"

# If no project name provided, use current directory name
if [ -z "$PROJECT_NAME" ]; then
    PROJECT_NAME=$(basename "$PWD")
fi

echo "🌐 Setting up JavaScript/Node.js project: $PROJECT_NAME"
echo ""

# Create directory structure
mkdir -p src
mkdir -p tests

# Create package.json
cat > package.json << EOF
{
  "name": "$PROJECT_NAME",
  "version": "0.1.0",
  "description": "A JavaScript project",
  "main": "src/index.js",
  "scripts": {
    "start": "node src/index.js",
    "test": "jest",
    "lint": "eslint src/",
    "format": "prettier --write src/"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0",
    "@types/node": "^20.0.0"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
EOF

# Create main source file
cat > src/index.js << EOF
/**
 * Main entry point for $PROJECT_NAME
 */

function main() {
    console.log("Hello from $PROJECT_NAME!");
}

if (require.main === module) {
    main();
}

module.exports = { main };
EOF

# Create test file
cat > tests/index.test.js << EOF
const { main } = require('../src/index');

describe('main function', () => {
    test('should run without errors', () => {
        expect(() => main()).not.toThrow();
    });
});
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
package-lock.json
yarn.lock

# Testing
coverage/
.nyc_output/

# Build
dist/
build/
*.tgz

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
.env.*.local

# Logs
logs/
*.log
EOF

echo "✅ JavaScript project structure created"
echo ""
echo "🔧 Adding agent infrastructure..."

# Create .agents/ structure (shared by Claude + Codex)
mkdir -p $AGENTS_DIR/memory
mkdir -p $AGENTS_DIR/transitions
mkdir -p $AGENTS_DIR/work
touch $AGENTS_DIR/transitions/.gitkeep
touch $AGENTS_DIR/work/.gitkeep

# Create .claude/ structure (Claude-specific only)
mkdir -p $CLAUDE_DIR/hooks
mkdir -p $CLAUDE_DIR/commands

# Create transition hook (writes to .agents/transitions/)
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
    cat > "$HOURLY_FILE" << EOF
# Session Progress: $TODAY ${HOUR}:00

---

EOF
fi
exit 0
HOOK_EOF
chmod +x $CLAUDE_DIR/hooks/init-transition.sh

# Get absolute path for hook
HOOK_PATH="$(pwd)/$CLAUDE_DIR/hooks/init-transition.sh"

# Create settings.json with plugins + transition hook
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
echo "✅ Created .claude/settings.json with core plugins + transition hook"

# Seed memory templates
cat > $AGENTS_DIR/memory/project_state.md << EOF
# Project state — $PROJECT_NAME

## What's working

-

## What's stubbed or absent

-

## Decisions to make

-
EOF

cat > $AGENTS_DIR/memory/conventions.md << 'EOF'
# Conventions

## Code

- **JavaScript**: Node 20+, ESLint + Prettier. `git safe-commit` (NOT `git commit`).

## Commits

- Use `git safe-commit -m "..."`. Never `--no-verify`.
- Conventional-commit style: `feat:`, `fix:`, `chore:`, `docs:`.

## Infrastructure

- Memory + transitions live at `.agents/` (shared by Claude and Codex). NOT `.claude/memory/`.
- `.claude/` holds only Claude-specific config: `settings.json`, `hooks/`, `commands/`.
- Every project session writes progress to `.agents/transitions/YYYY-MM-DD/HH.md`.
EOF

cat > $AGENTS_DIR/memory/decisions.md << 'EOF'
# Decisions

Record load-bearing choices with the reasoning. Future agents read this
before suggesting alternatives.

## YYYY-MM-DD: <Decision title>

**Why**:

**Trade-off**:
EOF

# Create AGENTS.md (canonical project doc)
cat > AGENTS.md << EOF
# $PROJECT_NAME

## Purpose

<one-paragraph statement of what this project is and who it's for>

## Code vs data layout

| Path | Purpose |
|---|---|
| \`src/\` | Source code |
| \`tests/\` | Tests (Jest) |

## Common bash invocations

\`\`\`bash
npm install       # install dependencies
npm test          # run tests
npm run lint      # eslint
npm run format    # prettier
npm start         # run app
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

# CLAUDE.md is one line — single source of truth via AGENTS.md
echo "@AGENTS.md" > CLAUDE.md

echo ""
echo "✅ JavaScript project setup complete!"
echo ""
echo "Next steps:"
echo "  1. cd into project directory (if not already there)"
echo "  2. npm install  (or: yarn install, pnpm install)"
echo "  3. npm test"
echo "  4. npm start"
echo ""
echo "Project structure:"
echo "  src/         - Source code"
echo "  tests/       - Test files"
echo "  AGENTS.md    - Canonical project doc (Claude + Codex)"
echo "  CLAUDE.md    - One-line @AGENTS.md include"
echo "  .agents/     - Shared agent state (memory, transitions, work)"
echo "  .claude/     - Claude-specific (settings, hooks, commands)"
```
