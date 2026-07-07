---
allowed-tools: [Read, Write, Bash]
argument-hint: "[project-name]"
description: Set up a new JavaScript/Node.js project with modern tooling and Claude framework integration
skills: [shared-setup-patterns]
---

# JavaScript Project Setup

I'll set up a new JavaScript/Node.js project with Jest, ESLint, Prettier, and the Claude Code Framework.

**Continuous review opt-in.** This setup enables [roborev](https://roborev.io)
by default — a local background reviewer that runs on every commit. Before
executing the bash, ask the user:

> Install roborev for continuous code review? [Y/n]

Default is yes. If they decline, prepend `ROBOREV_OPTIN=no` to the bash
invocation; everything else proceeds unchanged.

```bash
# Constants
readonly CLAUDE_DIR=".claude"
readonly WORKSPACE_DIR=".workspace"
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

# Create transition hook (writes to .workspace/transitions/)
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
echo "✅ Created .claude/settings.json with core plugins + transition hook"

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

# Seed memory templates
cat > $WORKSPACE_DIR/memory/project_state.md << EOF
# Project state — $PROJECT_NAME

## What's working

-

## What's stubbed or absent

-

## Decisions to make

-
EOF

cat > $WORKSPACE_DIR/memory/conventions.md << 'EOF'
# Conventions

## Code

- **JavaScript**: Node 20+, ESLint + Prettier. `git safe-commit` (NOT `git commit`).

## Commits

- Use `git safe-commit -m "..."`. Never `--no-verify`.
- Conventional-commit style: `feat:`, `fix:`, `chore:`, `docs:`.

## Infrastructure

- Memory + transitions live at `.workspace/` (shared by Claude and Codex). NOT `.claude/memory/`.
- `.claude/` holds only Claude-specific config: `settings.json`, `hooks/`, `commands/`.
- Every project session writes progress to `.workspace/transitions/YYYY-MM-DD/HH.md`.
EOF

cat > $WORKSPACE_DIR/memory/decisions.md << 'EOF'
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
echo "  .workspace/     - Shared agent state (memory, transitions, work)"
echo "  .claude/     - Claude-specific (settings, hooks, commands)"
```
