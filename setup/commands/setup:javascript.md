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
echo "🔧 Adding Claude Code Framework..."

# Create .claude directory structure (using shared-setup-patterns skill)
mkdir -p $CLAUDE_DIR/work
mkdir -p $CLAUDE_DIR/memory
mkdir -p $CLAUDE_DIR/reference
mkdir -p $CLAUDE_DIR/hooks

# Create settings.json with plugins (from shared-setup-patterns skill template)
cat > $CLAUDE_DIR/settings.json << 'SETTINGS_EOF'
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
  }
}
SETTINGS_EOF
echo "✅ Created .claude/settings.json with core plugins (including transition for /handoff)"

# Create project CLAUDE.md
cat > CLAUDE.md << EOF
# $PROJECT_NAME

JavaScript/Node.js project with modern tooling.

## Project Knowledge
@.claude/memory/project_state.md
@.claude/memory/dependencies.md
@.claude/memory/conventions.md
@.claude/memory/decisions.md

## Current Work
@.claude/work/current/README.md
EOF

# Generate memory files from shared skill templates
echo "I'll create memory files (.claude/memory/*) using templates from the shared-setup-patterns skill."

# Create work README
cat > $CLAUDE_DIR/work/current/README.md << 'EOF'
# Current Work

Track active development tasks here. Use work units for larger features:

```
.claude/work/current/
├── 001_feature_name/
│   ├── requirements.md
│   ├── implementation.md
│   └── notes.md
```
EOF

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
echo "  .claude/     - Claude framework"
```
