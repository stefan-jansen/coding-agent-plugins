---
allowed-tools: [Read, Write, Bash]
argument-hint: "[project-name] [--minimal|--standard|--full]"
description: Set up a new Python project with quality tools and Claude framework integration
skills: [shared-setup-patterns]
---

# Python Project Setup

I'll set up a new Python project with modern tooling and the Claude Code Framework.

**Continuous review opt-in.** This setup enables [roborev](https://roborev.io)
by default — a local background reviewer that runs on every commit. Before
executing the bash, ask the user:

> Install roborev for continuous code review? [Y/n]

Default is yes. If they decline, prepend `ROBOREV_OPTIN=no` to the bash
invocation; everything else proceeds unchanged.

## Setup Levels

**`--minimal`** - Just the essentials (pyproject.toml, basic .gitignore)
**`--standard`** (default) - Production-ready (pytest, ruff, mypy, pre-commit, Makefile)
**`--full`** - Enterprise-grade (docs, CI/CD, security scanning)

```bash
# Constants
readonly CLAUDE_DIR=".claude"
readonly WORKSPACE_DIR=".workspace"
readonly SETUP_LEVEL="${2:-standard}"  # Default to standard
PROJECT_NAME="${1}"

# If no project name provided, use current directory name
if [ -z "$PROJECT_NAME" ]; then
    PROJECT_NAME=$(basename "$PWD")
fi

echo "🐍 Setting up Python project: $PROJECT_NAME"
echo "📋 Setup level: $SETUP_LEVEL"
echo ""

# Create directory structure
mkdir -p src/$PROJECT_NAME
mkdir -p tests
mkdir -p docs

# Generate configuration based on level
case "$SETUP_LEVEL" in
    --minimal|minimal)
        echo "Creating minimal Python project..."

        # Basic pyproject.toml
        cat > pyproject.toml << 'EOF'
[project]
name = "$PROJECT_NAME"
version = "0.1.0"
description = "A Python package"
requires-python = ">=3.9"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
EOF
        sed -i "s/\$PROJECT_NAME/$PROJECT_NAME/g" pyproject.toml

        # Minimal .gitignore
        cat > .gitignore << 'EOF'
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.pytest_cache/
.mypy_cache/
.ruff_cache/
venv/
.venv/
*.log
.DS_Store
EOF
        echo "✅ Minimal Python setup complete"
        ;;

    --full|full)
        echo "Creating comprehensive Python project..."
        echo ""
        echo "For a full setup, I'll create:"
        echo "  1. pyproject.toml with documentation and security tools"
        echo "  2. .pre-commit-config.yaml with all quality checks"
        echo "  3. Makefile with comprehensive targets"
        echo "  4. CI/CD workflow templates"
        echo "  5. mkdocs.yml for documentation"
        echo ""
        echo "Please install these tools for full functionality:"
        echo "  - mkdocs, mkdocs-material (documentation)"
        echo "  - bandit (security scanning)"
        echo "  - GitHub Actions (CI/CD automation)"
        echo ""
        echo "✅ Full setup guidance provided"
        ;;

    --standard|standard|*)
        echo "Creating standard Python project with quality tools..."

        # Standard pyproject.toml
        cat > pyproject.toml << 'EOF'
[project]
name = "$PROJECT_NAME"
version = "0.1.0"
description = "A Python package"
requires-python = ">=3.9"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "ruff>=0.5.0",
    "mypy>=1.10",
    "pre-commit>=3.7",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 88
target-version = "py39"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP"]
ignore = ["E501"]  # Line length handled by formatter

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src --cov-report=term-missing"

[tool.coverage.run]
source = ["src"]
EOF
        sed -i "s/\$PROJECT_NAME/$PROJECT_NAME/g" pyproject.toml

        # Pre-commit configuration
        cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        files: ^src/
EOF

        # Makefile
        cat > Makefile << 'EOF'
.PHONY: help install dev test lint format type-check clean

help:
	@echo "Available commands:"
	@echo "  make install    Install package"
	@echo "  make dev        Install with dev dependencies"
	@echo "  make test       Run tests"
	@echo "  make lint       Run linting"
	@echo "  make format     Format code"
	@echo "  make type-check Run type checking"
	@echo "  make clean      Clean build artifacts"

install:
	pip install -e .

dev:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

type-check:
	mypy src/

clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
EOF

        # Standard .gitignore
        cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.mypy_cache/
.ruff_cache/

# Virtual Environment
venv/
.venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project
*.log
.env
EOF
        echo "✅ Standard Python setup complete"
        ;;
esac

# Create basic Python files
touch src/$PROJECT_NAME/__init__.py
cat > src/$PROJECT_NAME/main.py << EOF
"""Main module for $PROJECT_NAME."""

def main():
    """Main entry point."""
    print("Hello from $PROJECT_NAME!")

if __name__ == "__main__":
    main()
EOF

# Create basic test
cat > tests/test_main.py << EOF
"""Tests for main module."""
import pytest
from $PROJECT_NAME.main import main

def test_main():
    """Test main function."""
    # Add your tests here
    assert True
EOF

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

# Seed memory templates (.workspace/memory/)
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

- **Python**: 3.9+, formatted by ruff. Pre-commit enforces. `git safe-commit` (NOT `git commit`).

## Data

-

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

# Create AGENTS.md (canonical project doc, shared by Claude + Codex)
cat > AGENTS.md << EOF
# $PROJECT_NAME

## Purpose

<one-paragraph statement of what this project is and who it's for>

## Code vs data layout

| Path | Purpose |
|---|---|
| \`src/$PROJECT_NAME/\` | Source code |
| \`tests/\` | Tests (pytest) |
| \`docs/\` | Documentation |

## Common bash invocations

\`\`\`bash
make dev          # install with dev dependencies
make test         # run tests
make lint         # ruff check
make format       # ruff format
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
echo "✅ Python project setup complete!"
echo ""
echo "Next steps:"
echo "  1. cd into project directory (if not already there)"
echo "  2. python -m venv .venv"
echo "  3. source .venv/bin/activate"
echo "  4. make dev  (or: pip install -e '.[dev]')"
echo "  5. pre-commit install"
echo "  6. make test"
echo ""
echo "Project structure:"
echo "  src/$PROJECT_NAME/   - Source code"
echo "  tests/               - Test files"
echo "  AGENTS.md            - Canonical project doc (Claude + Codex)"
echo "  CLAUDE.md            - One-line @AGENTS.md include"
echo "  .workspace/             - Shared agent state (memory, transitions, work)"
echo "  .claude/             - Claude-specific (settings, hooks, commands)"
```
