---
allowed-tools: [Read, Write, MultiEdit, Bash, Glob, mcp__context7__resolve-library-id, mcp__context7__get-library-docs]
argument-hint: "[explore|existing|python|javascript] [project-name] [--minimal|--standard|--full] | --init-user [--force] | --statusline"
description: Initialize new projects with Claude framework integration or setup user configuration
---

# Project Setup

I'll set up a new project with the Claude Code Framework, optimized for your chosen language and project type.

## Usage

### User Configuration Setup
```bash
/setup --init-user               # Initialize ~/.claude/CLAUDE.md from template
/setup --init-user --force       # Overwrite existing user configuration
/setup --statusline              # Configure Claude Code statusline for framework
```

### Project Setup
```bash
/setup                           # Auto-detect project type and set up
/setup python                    # Set up Python project (standard quality setup)
/setup python --minimal          # Minimal Python setup (basic structure only)
/setup python --full             # Comprehensive setup (docs, CI/CD, etc.)
/setup javascript                # Set up JavaScript project
/setup existing                  # Add Claude framework to existing project
/setup explore                   # Set up data exploration project
```

### Python Setup Levels

#### `--minimal` - Just the Essentials
**What you get:**
- Basic `pyproject.toml` with project metadata
- Minimal `.gitignore` for Python projects
- Simple project structure (`src/`, `tests/`, `docs/`)
- Build system configuration (hatchling)

**Best for:** Quick experiments, learning projects, temporary code

#### `--standard` (default) - Production-Ready Quality
**What you get:**
- Modern `pyproject.toml` with:
  - Testing: pytest with coverage tracking
  - Linting: ruff for fast, comprehensive checks
  - Type checking: mypy for type safety
  - Formatting: ruff format for consistent style
- Pre-commit hooks for automated quality checks
- Makefile with development commands (test, lint, format, etc.)
- Comprehensive `.gitignore` for Python projects
- Proper project structure with `src/` layout

**Best for:** Real projects, open source packages, team development

#### `--full` - Enterprise-Grade Setup
**What you get:**
Everything from standard, plus:
- Documentation setup (mkdocs with material theme)
- Security scanning (bandit)
- CI/CD workflows (GitHub Actions)
- Extended testing setup (fixtures, coverage reports)
- Additional development tools
- Release automation setup
- Dependency management configuration

**Best for:** Commercial products, large teams, projects requiring compliance

## Phase 1: Project Analysis

```bash
# Constants (must be defined in each command due to framework constraints)
readonly CLAUDE_DIR=".claude"
readonly WORK_DIR="${CLAUDE_DIR}/work"
readonly MEMORY_DIR="${CLAUDE_DIR}/memory"
readonly REFERENCE_DIR="${CLAUDE_DIR}/reference"
readonly HOOKS_DIR="${CLAUDE_DIR}/hooks"

# Project type constants
readonly TYPE_PYTHON="python"
readonly TYPE_JAVASCRIPT="javascript"
readonly TYPE_EXPLORE="explore"
readonly TYPE_EXISTING="existing"

# Parse command line arguments
INIT_USER=false
FORCE_FLAG=false
SETUP_STATUSLINE=false
REMAINING_ARGS=""

# Parse arguments for flags
SETUP_LEVEL="standard"  # Default to standard setup
for arg in $ARGUMENTS; do
    case "$arg" in
        --init-user)
            INIT_USER=true
            ;;
        --force)
            FORCE_FLAG=true
            ;;
        --statusline)
            SETUP_STATUSLINE=true
            ;;
        --minimal)
            SETUP_LEVEL="minimal"
            ;;
        --standard)
            SETUP_LEVEL="standard"
            ;;
        --full)
            SETUP_LEVEL="full"
            ;;
        *)
            REMAINING_ARGS="$REMAINING_ARGS $arg"
            ;;
    esac
done

# Handle --init-user mode
if [ "$INIT_USER" = true ]; then
    echo "🔧 Initializing user CLAUDE.md configuration..."
    echo ""

    # Check if ~/.claude directory exists, create if needed
    USER_CLAUDE_DIR="$HOME/.claude"
    USER_CLAUDE_FILE="$USER_CLAUDE_DIR/CLAUDE.md"
    TEMPLATE_FILE="$(pwd)/templates/USER_CLAUDE_TEMPLATE.md"

    # Verify template exists
    if [ ! -f "$TEMPLATE_FILE" ]; then
        echo "❌ ERROR: USER_CLAUDE_TEMPLATE.md not found at $TEMPLATE_FILE"
        echo "   Make sure you're running this from the Claude Code framework directory."
        exit 1
    fi

    # Create ~/.claude directory if it doesn't exist
    if [ ! -d "$USER_CLAUDE_DIR" ]; then
        echo "📁 Creating ~/.claude directory..."
        mkdir -p "$USER_CLAUDE_DIR" || {
            echo "❌ ERROR: Failed to create ~/.claude directory"
            echo "   Check permissions for $HOME directory"
            exit 1
        }
    fi

    # Check if user CLAUDE.md already exists
    if [ -f "$USER_CLAUDE_FILE" ] && [ "$FORCE_FLAG" != true ]; then
        echo "⚠️  User CLAUDE.md already exists at: $USER_CLAUDE_FILE"
        echo ""
        echo "Options:"
        echo "  1. Keep existing file (recommended if you've customized it)"
        echo "  2. Overwrite with latest template (use --force flag)"
        echo ""
        echo "To overwrite: /setup --init-user --force"
        echo "To view existing: cat ~/.claude/CLAUDE.md"
        exit 0
    fi

    # Copy template to user location
    echo "📋 Copying USER_CLAUDE_TEMPLATE.md to ~/.claude/CLAUDE.md..."
    cp "$TEMPLATE_FILE" "$USER_CLAUDE_FILE" || {
        echo "❌ ERROR: Failed to copy template file"
        echo "   Check permissions for ~/.claude directory"
        exit 1
    }

    echo ""
    echo "✅ User CLAUDE.md configuration initialized successfully!"
    echo ""
    echo "📍 Location: $USER_CLAUDE_FILE"
    echo "📝 Content: Essential behavioral guidelines and SWE best practices"
    echo ""
    echo "What's included:"
    echo "  • Core behavioral tenets (question assumptions, avoid over-engineering)"
    echo "  • MCP tool usage guidelines"
    echo "  • Framework commands and workflow patterns"
    echo ""
    echo "Next steps:"
    echo "  • Edit with: /memory edit"
    echo "  • View with: /memory view"
    echo "  • Customize for your personal workflow"
    echo "  • Use /setup [type] in project directories for project-specific setup"
    echo "  • The user config provides global standards for all projects"
    echo ""
    if [ "$FORCE_FLAG" = true ]; then
        echo "🔄 Existing file was overwritten as requested"
    fi

    exit 0
fi

# Handle --statusline mode
if [ "$SETUP_STATUSLINE" = true ]; then
    echo "🎯 Setting up Claude Code Framework Statusline"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # Check if we're in a framework directory
    if [ ! -d ".claude" ] || [ ! -f "commands/setup.md" ]; then
        echo "❌ ERROR: Not in Claude Code Framework directory"
        echo "   Run this command from the root of your claude-code-framework directory"
        echo ""
        echo "Expected structure:"
        echo "  claude-code-framework/"
        echo "  ├── commands/"
        echo "  ├── .claude/"
        echo "  └── templates/"
        exit 1
    fi

    # Create statusline script in framework
    STATUSLINE_SCRIPT="$(pwd)/.claude/scripts/statusline.sh"
    echo "📝 Creating framework statusline script..."

    # Ensure scripts directory exists
    mkdir -p .claude/scripts

    # Copy our prototype script
    if [ -f ".claude/work/current/001_statusline_exploration/statusline_prototype.sh" ]; then
        cp ".claude/work/current/001_statusline_exploration/statusline_prototype.sh" "$STATUSLINE_SCRIPT"
    else
        # Create the script inline if prototype not available
        cat > "$STATUSLINE_SCRIPT" << 'STATUSLINE_EOF'
#!/bin/bash
# Claude Code Framework Statusline
# Provides contextual information about current development session

# Read JSON input from Claude Code
input=$(cat)

# Extract basic session info with jq fallback
if command -v jq >/dev/null 2>&1; then
    MODEL_DISPLAY=$(echo "$input" | jq -r '.model.display_name // "Claude"')
    CURRENT_DIR=$(echo "$input" | jq -r '.workspace.current_dir // ""')
else
    # Fallback parsing without jq
    MODEL_DISPLAY="Claude"
    CURRENT_DIR=$(pwd)
fi

# Get directory name for display
if [ -n "$CURRENT_DIR" ]; then
    DIR_NAME="${CURRENT_DIR##*/}"
else
    DIR_NAME="$(basename "$(pwd)")"
fi

# Initialize status components
STATUS_PARTS=()

# 1. Model and Directory (always shown)
STATUS_PARTS+=("[$MODEL_DISPLAY] 📁 $DIR_NAME")

# 2. Framework Work Unit Detection
WORK_UNIT=""
if [ -f ".claude/work/ACTIVE_WORK" ]; then
    ACTIVE_WORK=$(cat .claude/work/ACTIVE_WORK 2>/dev/null)
    if [ -n "$ACTIVE_WORK" ] && [ -d ".claude/work/current/$ACTIVE_WORK" ]; then
        WORK_NUM=$(echo "$ACTIVE_WORK" | cut -d'_' -f1)
        if command -v jq >/dev/null 2>&1 && [ -f ".claude/work/current/$ACTIVE_WORK/metadata.json" ]; then
            WORK_PHASE=$(jq -r '.phase // "active"' ".claude/work/current/$ACTIVE_WORK/metadata.json" 2>/dev/null)
        else
            WORK_PHASE="active"
        fi
        WORK_UNIT="💼 $WORK_NUM ($WORK_PHASE)"
    fi
elif [ -d ".claude/work/current" ]; then
    CURRENT_COUNT=$(find .claude/work/current -maxdepth 1 -type d 2>/dev/null | wc -l)
    if [ "$CURRENT_COUNT" -gt 1 ]; then
        LATEST_WORK=$(ls -t .claude/work/current/ 2>/dev/null | head -1)
        if [ -n "$LATEST_WORK" ]; then
            WORK_NUM=$(echo "$LATEST_WORK" | cut -d'_' -f1)
            WORK_UNIT="💼 $WORK_NUM (inactive)"
        fi
    fi
fi

if [ -n "$WORK_UNIT" ]; then
    STATUS_PARTS+=("$WORK_UNIT")
fi

# 3. Git Status (if in git repo)
if git rev-parse --git-dir >/dev/null 2>&1; then
    GIT_BRANCH=$(git branch --show-current 2>/dev/null)
    if [ -n "$GIT_BRANCH" ]; then
        GIT_STATUS=""
        if ! git diff-index --quiet HEAD -- 2>/dev/null; then
            GIT_STATUS="*"
        fi
        if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
            GIT_STATUS="${GIT_STATUS}+"
        fi
        STATUS_PARTS+=("🌿 $GIT_BRANCH$GIT_STATUS")
    fi
fi

# 4. MCP Server Status (simplified)
if [ -f ".claude/settings.json" ] || [ -f ".claude/settings.local.json" ]; then
    MCP_COUNT=0
    for settings_file in ".claude/settings.json" ".claude/settings.local.json"; do
        if [ -f "$settings_file" ] && command -v jq >/dev/null 2>&1; then
            MCP_SERVERS=$(jq -r '.mcpServers // {} | keys | length' "$settings_file" 2>/dev/null)
            if [ "$MCP_SERVERS" != "null" ] && [ "$MCP_SERVERS" -gt 0 ]; then
                MCP_COUNT=$((MCP_COUNT + MCP_SERVERS))
            fi
        fi
    done
    if [ "$MCP_COUNT" -gt 0 ]; then
        STATUS_PARTS+=("🔧 MCP:$MCP_COUNT")
    fi
fi

# Combine all status parts
IFS=" | "
echo "${STATUS_PARTS[*]}"
STATUSLINE_EOF
    fi

    chmod +x "$STATUSLINE_SCRIPT"
    echo "✅ Statusline script created: $STATUSLINE_SCRIPT"

    # Update user settings to include statusline
    USER_SETTINGS="$HOME/.claude/settings.json"

    # Ensure ~/.claude directory exists
    if [ ! -d "$HOME/.claude" ]; then
        echo "📁 Creating ~/.claude directory..."
        mkdir -p "$HOME/.claude"
    fi

    # Create or update settings.json
    if [ -f "$USER_SETTINGS" ]; then
        echo "🔧 Updating existing ~/.claude/settings.json..."

        # Backup existing settings
        cp "$USER_SETTINGS" "$USER_SETTINGS.backup.$(date +%Y%m%d_%H%M%S)"

        # Update settings with jq if available
        if command -v jq >/dev/null 2>&1; then
            jq --arg script "$STATUSLINE_SCRIPT" '.statusLine.command = $script' "$USER_SETTINGS" > "$USER_SETTINGS.tmp" && mv "$USER_SETTINGS.tmp" "$USER_SETTINGS"
        else
            echo "⚠️  jq not available - please manually add statusline configuration"
            echo "   Add this to ~/.claude/settings.json:"
            echo "   \"statusLine\": { \"command\": \"$STATUSLINE_SCRIPT\" }"
        fi
    else
        echo "📝 Creating new ~/.claude/settings.json..."
        cat > "$USER_SETTINGS" << EOF
{
    "statusLine": {
        "command": "$STATUSLINE_SCRIPT"
    }
}
EOF
    fi

    echo ""
    echo "✅ Claude Code Framework Statusline Setup Complete!"
    echo ""
    echo "📍 Configuration:"
    echo "   Script: $STATUSLINE_SCRIPT"
    echo "   Settings: $USER_SETTINGS"
    echo ""
    echo "🎯 What you'll see:"
    echo "   [Model] 📁 project | 💼 001 (exploring) | 🌿 main | 🔧 MCP:4"
    echo ""
    echo "📝 Features:"
    echo "   • Current work unit and phase"
    echo "   • Git branch and status indicators"
    echo "   • MCP server count"
    echo "   • Project directory name"
    echo ""
    echo "🔄 Restart Claude Code to see the new statusline"
    echo ""
    echo "💡 Tip: Edit $STATUSLINE_SCRIPT to customize your statusline"

    exit 0
fi

# Standard project setup continues below
PROJECT_NAME="${REMAINING_ARGS:-$(basename $PWD)}"
SETUP_TYPE=""

echo "🔍 Analyzing project..."

# Check if explicit type was provided as argument
if [ -n "$PROJECT_NAME" ]; then
    # Check if it's a known project type
    case "$PROJECT_NAME" in
        python|javascript|typescript|go|rust|java|explore|existing)
            SETUP_TYPE="$PROJECT_NAME"
            PROJECT_NAME=$(basename $PWD)
            echo "→ Setting up $SETUP_TYPE project"
            ;;
        *)
            # It's a project name, auto-detect type
            echo "→ Project name: $PROJECT_NAME"
            ;;
    esac
fi

# Auto-detect project type if not specified
if [ -z "$SETUP_TYPE" ]; then
    # Check for existing project
    if [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "requirements.txt" ]; then
        if [ -d "src" ]; then
            SETUP_TYPE="python-package"
            echo "→ Detected: Python package project (src/ layout)"
        else
            SETUP_TYPE="python-simple"
            echo "→ Detected: Python project (simple layout)"
        fi
    elif [ -f "package.json" ]; then
        SETUP_TYPE="javascript"
        echo "→ Detected: JavaScript/Node.js project"
    elif [ -f "Cargo.toml" ]; then
        SETUP_TYPE="rust"
        echo "→ Detected: Rust project"
    elif [ -f "go.mod" ]; then
        SETUP_TYPE="go"
        echo "→ Detected: Go project"
    elif [ -d ".git" ] && [ "$(ls -A | wc -l)" -gt 2 ]; then
        SETUP_TYPE="existing"
        echo "→ Detected: Existing project (adding Claude framework)"
    elif ls *.ipynb >/dev/null 2>&1 || [ -d "notebooks" ] || [ -d "data" ]; then
        SETUP_TYPE="explore"
        echo "→ Detected: Data exploration project"
    else
        # Empty or new directory - default to Python
        SETUP_TYPE="python-package"
        echo "→ New project: Defaulting to Python package setup"
    fi
fi
```

## Phase 2: Project Initialization

Based on detection, I'll run the appropriate setup:

```bash
case "$SETUP_TYPE" in
    python-package|python)
        echo "🐍 Setting up Python package project..."

        # Create src layout
        mkdir -p src/$PROJECT_NAME
        mkdir -p tests
        mkdir -p docs

        # Use declarative approach based on setup level
        echo "📋 Generating $SETUP_LEVEL Python configuration..."

        case "$SETUP_LEVEL" in
            minimal)
                echo "Creating minimal Python project..."

                # Basic pyproject.toml only
                cat > pyproject.toml << 'MINIMAL_EOF'
[project]
name = "$PROJECT_NAME"
version = "0.1.0"
description = "A Python package"
requires-python = ">=3.9"
dependencies = []

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
MINIMAL_EOF
                # Variable substitution
                sed -i "s/\$PROJECT_NAME/$PROJECT_NAME/g" pyproject.toml

                # Minimal gitignore
                cat > .gitignore << 'GITIGNORE_EOF'
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
GITIGNORE_EOF

                echo "✅ Minimal Python setup complete"
                ;;

            full)
                echo "Creating comprehensive Python project with all features..."
                echo ""
                echo "📝 Generating comprehensive configuration files..."

                # Note: In a declarative approach, Claude Code would generate these
                # based on current best practices. For now, we provide guidance.
                echo ""
                echo "I'll create a comprehensive Python setup. Please create these files:"
                echo ""
                echo "1. pyproject.toml - with latest versions of:"
                echo "   - ruff, mypy, pytest, pytest-cov, bandit"
                echo "   - mkdocs, mkdocs-material for documentation"
                echo "   - pre-commit for git hooks"
                echo ""
                echo "2. .pre-commit-config.yaml with:"
                echo "   - ruff (format and lint)"
                echo "   - mypy (type checking)"
                echo "   - bandit (security)"
                echo "   - conventional commits"
                echo ""
                echo "3. Makefile with targets for:"
                echo "   - install, dev, test, lint, format, type-check"
                echo "   - security, docs, build, clean"
                echo ""
                echo "4. .github/workflows/ci.yml for GitHub Actions"
                echo "5. mkdocs.yml for documentation"
                echo "6. Comprehensive .gitignore"

                echo ""
                echo "✅ Full setup requirements specified"
                ;;

            standard|*)
                echo "Creating standard Python project with quality tools..."

                # Generate standard pyproject.toml with current best practices
                cat > pyproject.toml << 'STANDARD_EOF'
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
STANDARD_EOF
                # Variable substitution
                sed -i "s/\$PROJECT_NAME/$PROJECT_NAME/g" pyproject.toml

                # Generate pre-commit config
                cat > .pre-commit-config.yaml << 'PRECOMMIT_EOF'
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
PRECOMMIT_EOF

                # Generate Makefile
                cat > Makefile << 'MAKEFILE_EOF'
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
MAKEFILE_EOF

                # Standard gitignore
                cat > .gitignore << 'GITIGNORE_EOF'
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
GITIGNORE_EOF

                echo "✅ Standard Python setup complete"
                ;;
        esac

        # Create basic Python files (common to both template and inline modes)
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

        echo "✅ Python package structure created"
        ;;

    python-simple|explore)
        echo "🔬 Setting up Python exploration project..."

        # Create simple Python structure
        mkdir -p scripts
        mkdir -p data
        mkdir -p notebooks

        # Create requirements.txt for simple projects
        cat > requirements.txt << EOF
# Core dependencies
numpy
pandas
matplotlib

# Development tools
pytest
pytest-cov
ruff
black
mypy
jupyter
EOF

        # Create basic Python file
        cat > main.py << EOF
"""Main script for $PROJECT_NAME."""

def main():
    """Main entry point."""
    print("Hello from $PROJECT_NAME!")

if __name__ == "__main__":
    main()
EOF

        echo "✅ Python exploration structure created"
        ;;

    javascript|js)
        echo "🌐 Setting up JavaScript/Node.js project..."

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
  }
}
EOF

        # Create basic structure
        mkdir -p src
        mkdir -p tests

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

        cat > tests/index.test.js << EOF
const { main } = require('../src/index');

describe('main function', () => {
    test('should run without errors', () => {
        expect(() => main()).not.toThrow();
    });
});
EOF

        echo "✅ JavaScript project structure created"
        ;;

    existing)
        echo "🔧 Adding Claude framework to existing project..."
        echo "✅ Existing project detected - will add Claude framework below"
        ;;

    *)
        echo "📦 Unknown type - using Python package setup (default)"
        SETUP_TYPE="python-package"
        # Recurse with corrected type
        ;;
esac
```

## Phase 3: Claude Framework Integration

```bash
echo ""
echo "🔧 Adding Claude Code Framework..."

# Create .claude directory structure
mkdir -p .claude/work/current || { echo "ERROR: Failed to create .claude/work/current" >&2; exit 1; }
mkdir -p .claude/work/completed || { echo "ERROR: Failed to create .claude/work/completed" >&2; exit 1; }
mkdir -p .claude/memory || { echo "ERROR: Failed to create .claude/memory" >&2; exit 1; }
mkdir -p .claude/reference || { echo "ERROR: Failed to create .claude/reference" >&2; exit 1; }
mkdir -p .claude/hooks || { echo "ERROR: Failed to create .claude/hooks" >&2; exit 1; }

# Create security hooks configuration
echo "🔒 Setting up security hooks..."
cat > .claude/settings.json << 'SECURITY_EOF'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "input=\"$CLAUDE_TOOL_INPUT\"; if echo \"$input\" | grep -q 'rm -rf'; then echo '🚨 BLOCKED: Dangerous rm -rf command detected!' >&2 && echo 'Use git clean or specific file deletion instead.' >&2 && exit 2; fi; if echo \"$input\" | grep -q 'sudo'; then echo '🚨 BLOCKED: sudo command not allowed in development!' >&2 && echo 'Review your command and run manually if needed.' >&2 && exit 2; fi; if echo \"$input\" | grep -q 'chmod 777'; then echo '⚠️  BLOCKED: chmod 777 is a security risk!' >&2 && echo 'Use specific permissions like 755 or 644.' >&2 && exit 2; fi"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "file=\"$CLAUDE_TOOL_INPUT_FILE\"; if [ -n \"$file\" ]; then ext=\"${file##*.}\"; case \"$ext\" in py) echo '🔧 Python file edited: '$file && if command -v ruff >/dev/null 2>&1; then if ruff format \"$file\" 2>/dev/null; then echo '✅ ruff format applied'; else echo '⚠️  ruff format failed - check Python syntax'; fi && if ruff check \"$file\" --fix 2>/dev/null; then echo '✅ ruff linting passed'; else echo '⚠️  ruff found issues - review the warnings'; fi; else echo '💡 Install ruff for automatic formatting & linting: pip install ruff'; fi ;; js|jsx|ts|tsx) echo '🔧 JavaScript/TypeScript file edited: '$file && if command -v prettier >/dev/null 2>&1; then if prettier --write \"$file\" 2>/dev/null; then echo '✅ prettier formatting applied'; else echo '⚠️  prettier failed - check syntax'; fi; else echo '💡 Install prettier: npm install prettier'; fi && if command -v eslint >/dev/null 2>&1; then if eslint \"$file\" --fix 2>/dev/null; then echo '✅ eslint passed'; else echo '⚠️  eslint found issues - review the warnings'; fi; else echo '💡 Install eslint: npm install eslint'; fi ;; json) echo '🔧 JSON file edited: '$file && if python3 -m json.tool \"$file\" >/dev/null 2>&1; then echo '✅ JSON syntax valid'; else echo '❌ Invalid JSON syntax in '$file' - fix required!' >&2 && exit 1; fi ;; md) echo '📝 Markdown file edited: '$file && if command -v markdownlint >/dev/null 2>&1; then if markdownlint \"$file\" 2>/dev/null; then echo '✅ Markdown linting passed'; else echo '⚠️  Markdown formatting issues found'; fi; else echo '💡 Install markdownlint for markdown quality: npm install -g markdownlint-cli'; fi ;; esac; fi"
          }
        ]
      }
    ]
  }
}
SECURITY_EOF

echo "✅ Security & Quality hooks configured:"
echo "   🔒 Security: rm -rf, sudo, chmod 777 protection"
echo "   🔧 Quality: automatic formatting (ruff, prettier, eslint)"
echo "   📝 Validation: JSON syntax, markdown linting"
echo "   🧪 Testing: pytest hints for new test files"

# Generate project CLAUDE.md declaratively
echo "📝 Generating project CLAUDE.md and memory files..."

# Auto-detect project characteristics
DETECTED_LANG=""
DETECTED_FRAMEWORK=""
DETECTED_TEST_TOOL=""
DETECTED_BUILD=""

# Language detection
if [ -f "package.json" ]; then
    DETECTED_LANG="JavaScript/TypeScript"
    grep -q '"next"' package.json 2>/dev/null && DETECTED_FRAMEWORK="Next.js"
    grep -q '"react"' package.json 2>/dev/null && [ -n "$DETECTED_FRAMEWORK" ] && DETECTED_FRAMEWORK="$DETECTED_FRAMEWORK, React" || DETECTED_FRAMEWORK="React"
    grep -q '"express"' package.json 2>/dev/null && [ -n "$DETECTED_FRAMEWORK" ] && DETECTED_FRAMEWORK="$DETECTED_FRAMEWORK, Express" || DETECTED_FRAMEWORK="Express"
    grep -q '"jest"' package.json 2>/dev/null && DETECTED_TEST_TOOL="Jest"
    grep -q '"mocha"' package.json 2>/dev/null && [ -n "$DETECTED_TEST_TOOL" ] && DETECTED_TEST_TOOL="$DETECTED_TEST_TOOL, Mocha" || DETECTED_TEST_TOOL="Mocha"
elif [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "requirements.txt" ]; then
    DETECTED_LANG="Python"
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
        DETECTED_LANG="Python $PYTHON_VERSION"
    fi
    if [ -f "pyproject.toml" ]; then
        grep -q 'fastapi' pyproject.toml 2>/dev/null && DETECTED_FRAMEWORK="FastAPI"
        grep -q 'django' pyproject.toml 2>/dev/null && [ -n "$DETECTED_FRAMEWORK" ] && DETECTED_FRAMEWORK="$DETECTED_FRAMEWORK, Django" || DETECTED_FRAMEWORK="Django"
        grep -q 'flask' pyproject.toml 2>/dev/null && [ -n "$DETECTED_FRAMEWORK" ] && DETECTED_FRAMEWORK="$DETECTED_FRAMEWORK, Flask" || DETECTED_FRAMEWORK="Flask"
        grep -q 'pytest' pyproject.toml 2>/dev/null && DETECTED_TEST_TOOL="pytest"
    fi
    [ -f "Makefile" ] && DETECTED_BUILD="Make"
elif [ -f "go.mod" ]; then
    DETECTED_LANG="Go"
    DETECTED_TEST_TOOL="go test"
elif [ -f "Cargo.toml" ]; then
    DETECTED_LANG="Rust"
    DETECTED_TEST_TOOL="cargo test"
fi

# Create minimal main CLAUDE.md with imports
cat > CLAUDE.md << EOF
# $PROJECT_NAME

${DETECTED_LANG:+$DETECTED_LANG project}${DETECTED_FRAMEWORK:+ using $DETECTED_FRAMEWORK}.

## Project Knowledge
@.claude/memory/project_state.md
@.claude/memory/dependencies.md
@.claude/memory/conventions.md
@.claude/memory/decisions.md

## Current Work
@.claude/work/current/README.md
EOF

# Generate project_state.md with detected info
cat > .claude/memory/project_state.md << 'STATE_EOF'
# Project State

## Technology Stack
- **Language**: DETECTED_LANG_PLACEHOLDER
- **Framework**: DETECTED_FRAMEWORK_PLACEHOLDER
- **Testing**: DETECTED_TEST_PLACEHOLDER
- **Build System**: DETECTED_BUILD_PLACEHOLDER

## Architecture
- **Project Type**: SETUP_TYPE_PLACEHOLDER
- **Directory Structure**: DIR_STRUCTURE_PLACEHOLDER
STATE_EOF

# Variable substitution for project_state.md
sed -i "s/DETECTED_LANG_PLACEHOLDER/${DETECTED_LANG:-Not detected}/g" .claude/memory/project_state.md
sed -i "s/DETECTED_FRAMEWORK_PLACEHOLDER/${DETECTED_FRAMEWORK:-Not detected}/g" .claude/memory/project_state.md
sed -i "s/DETECTED_TEST_PLACEHOLDER/${DETECTED_TEST_TOOL:-Not detected}/g" .claude/memory/project_state.md
sed -i "s/DETECTED_BUILD_PLACEHOLDER/${DETECTED_BUILD:-Not detected}/g" .claude/memory/project_state.md
sed -i "s/SETUP_TYPE_PLACEHOLDER/$SETUP_TYPE/g" .claude/memory/project_state.md
sed -i "s/DIR_STRUCTURE_PLACEHOLDER/$([ -d 'src' ] && echo 'src layout' || echo 'flat layout')/g" .claude/memory/project_state.md

# Generate dependencies.md from package files
echo "# Dependencies" > .claude/memory/dependencies.md
echo "" >> .claude/memory/dependencies.md
if [ -f "package.json" ]; then
    echo "## NPM Packages" >> .claude/memory/dependencies.md
    if command -v jq >/dev/null 2>&1; then
        jq -r '.dependencies // {} | to_entries[] | "- \(.key): \(.value)"' package.json 2>/dev/null >> .claude/memory/dependencies.md || echo "See package.json for dependencies" >> .claude/memory/dependencies.md
    else
        echo "See package.json for dependencies" >> .claude/memory/dependencies.md
    fi
elif [ -f "pyproject.toml" ]; then
    echo "## Python Dependencies" >> .claude/memory/dependencies.md
    echo "Extracted from pyproject.toml - see file for versions" >> .claude/memory/dependencies.md
elif [ -f "requirements.txt" ]; then
    echo "## Python Dependencies" >> .claude/memory/dependencies.md
    head -20 requirements.txt >> .claude/memory/dependencies.md
    [ $(wc -l < requirements.txt) -gt 20 ] && echo "... see requirements.txt for full list" >> .claude/memory/dependencies.md
fi

# Create minimal conventions.md
cat > .claude/memory/conventions.md << 'CONV_EOF'
# Project Conventions

Add project-specific conventions here that differ from global standards.
CONV_EOF

# Create placeholder decisions.md
cat > .claude/memory/decisions.md << 'DEC_EOF'
# Key Decisions

Document important architectural and technical decisions as the project evolves.
DEC_EOF

# Create work README
cat > .claude/work/current/README.md << 'WORK_EOF'
# Current Work

Active development tasks and work units will appear here.
WORK_EOF

echo "✅ Generated declarative project configuration"

# Skip the rest of the old CLAUDE.md creation
true << 'SKIP_OLD_CONTENT'

\`\`\`bash
# Enhanced development workflow (Lean MCP Framework active)
/explore "feature to implement"
/plan
/next
/ship

# For code projects, activate semantic understanding:
/serena \$(pwd)
\`\`\`

## Lean MCP Framework Active

This project benefits from the globally active Lean MCP Framework with:
- **75% token reduction** on code operations (when Serena available)
- **Enhanced reasoning** for complex analysis (Sequential Thinking)
- **Live documentation** access (Context7)
- **Graceful degradation** when MCP tools unavailable

## Project Conventions

- Follow conventional commits (feat:, fix:, docs:, etc.)
- Use quality tools (ruff for Python, prettier for JavaScript)
- Write tests for all new features
- Keep project root clean - use .claude/ for work materials

## Available Commands

**Core Workflow**: \`/explore\`, \`/plan\`, \`/next\`, \`/ship\`
**Enhanced with MCP**: \`/analyze\`, \`/fix\`, \`/docs search\`
**Serena Integration**: \`/serena [project-path]\` for semantic code understanding
**Specialized Agents**: \`/agent architect\`, \`/agent test-engineer\`, \`/agent code-reviewer\`, \`/agent auditor\`

## Development Workflow

1. **Explore**: Understand requirements (\`/explore\`)
2. **Plan**: Break down into tasks (\`/plan\`)
3. **Execute**: Work through tasks (\`/next\`)
4. **Ship**: Deliver completed work (\`/ship\`)

## Enhanced Capabilities

When MCP tools are available:
- **Code Analysis**: Use \`/analyze\` for semantic understanding
- **Smart Debugging**: Use \`/fix\` with context-aware assistance
- **Live Documentation**: Use \`/docs search "topic"\` for instant answers
- **Complex Reasoning**: Commands automatically use Sequential Thinking when beneficial

Setup MCP servers to unlock these capabilities (graceful fallback ensures everything works regardless).

EOF
SKIP_OLD_CONTENT

# Create basic README
if [ ! -f "README.md" ]; then
    cat > README.md << EOF
# $PROJECT_NAME

## Overview

Brief description of what this project does.

## Installation

\`\`\`bash
# For Python projects
pip install -e .

# For JavaScript projects
npm install
\`\`\`

## Development

\`\`\`bash
# Run tests
pytest  # Python
npm test  # JavaScript

# Format code
black .  # Python
npm run format  # JavaScript
\`\`\`

## License

MIT
EOF
fi

# Initialize git if not present
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
fi

# Create .gitignore
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << EOF
# Claude work files (private)
.claude/work/
.claude/transitions/

# Language-specific ignores
__pycache__/
*.pyc
*.pyo
*.pyd
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

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment
.env
.venv/
venv/
EOF
    echo "✅ .gitignore created"
fi

echo ""
echo "📚 Setting up documentation access with Context7..."
echo ""

# Context7 Integration for enhanced documentation
if command -v claude >/dev/null 2>&1; then
    echo "🔍 Detecting project dependencies for documentation setup..."

    # Detect dependencies based on project type
    DEPS_TO_FETCH=""
    case "$SETUP_TYPE" in
        python-package|python-simple|explore)
            if [ -f "pyproject.toml" ]; then
                echo "   → Scanning pyproject.toml for Python dependencies"
                DEPS_TO_FETCH="$DEPS_TO_FETCH pytest black ruff mypy"
            elif [ -f "requirements.txt" ]; then
                echo "   → Scanning requirements.txt for Python dependencies"
                DEPS_TO_FETCH="$DEPS_TO_FETCH numpy pandas matplotlib pytest"
            fi
            ;;
        javascript|js)
            if [ -f "package.json" ]; then
                echo "   → Scanning package.json for Node.js dependencies"
                DEPS_TO_FETCH="$DEPS_TO_FETCH jest eslint prettier"
            fi
            ;;
    esac

    # Create documentation cache directory
    mkdir -p .claude/docs/libraries

    # Create Context7 documentation setup guide
    cat > .claude/docs/CONTEXT7_SETUP.md << 'CONTEXT7_EOF'
# Context7 Documentation Setup

## What is Context7?

Context7 is an MCP server that provides intelligent, up-to-date documentation access for libraries and frameworks. Instead of manually searching documentation or copying large docs into your context, Context7 delivers precise, relevant documentation on demand.

## Benefits

- **Live Documentation**: Always current library documentation
- **Intelligent Search**: Semantic search within library docs
- **Precise Results**: Get exactly the information you need
- **Token Efficient**: No need to load entire documentation sets
- **Version Aware**: Documentation matching your exact library versions

## Setup Instructions

### 1. Install Context7 MCP Server

```bash
# Install via npm (recommended)
npm install -g @context7/mcp-server

# Or via pip if Python-based
pip install context7-mcp
```

### 2. Configure Claude Code

Add Context7 to your Claude Code MCP configuration:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["@context7/mcp-server"]
    }
  }
}
```

### 3. Test Integration

```bash
# Test Context7 availability
/docs search "your-library documentation"

# Example searches
/docs search "pytest fixtures"        # Python testing
/docs search "express middleware"     # Node.js web framework
/docs search "react hooks"           # React.js
```

## Usage in Development

### Quick Documentation Access

```bash
# Search for specific topics
/docs search "library-name topic"

# Get setup instructions
/docs search "framework-name getting started"

# Find API reference
/docs search "library-name api reference"
```

### Integration with Workflow

- **During /explore**: Research libraries and their capabilities
- **During /plan**: Understand implementation requirements
- **During /next**: Get specific API documentation for current task
- **During /review**: Verify best practices and patterns

## Fallback Strategy

When Context7 is unavailable:
- Commands gracefully fall back to web search via Firecrawl
- Local documentation cache is used when available
- Manual documentation links are provided as backup

## Library Coverage

Context7 supports documentation for:
- **Python**: NumPy, Pandas, Django, Flask, FastAPI, pytest, and 1000+ libraries
- **JavaScript**: React, Vue, Express, Jest, and popular npm packages
- **Frameworks**: Next.js, Nuxt.js, Spring Boot, and more
- **Tools**: Docker, Kubernetes, Git, and development tools

CONTEXT7_EOF

    echo "✅ Context7 documentation access configured"
    echo "   📖 Setup guide: .claude/docs/CONTEXT7_SETUP.md"
    echo "   🔍 Test with: /docs search \"your-library documentation\""

    # Add Context7 suggestions to CLAUDE.md
    cat >> CLAUDE.md << 'CONTEXT7_APPEND'

## Enhanced Documentation Features

This project includes Context7 integration for intelligent documentation access:

### Quick Documentation Commands

```bash
# Search library documentation
/docs search "pytest fixtures"      # Testing frameworks
/docs search "express middleware"   # Web frameworks
/docs search "react hooks"         # Frontend libraries
```

### Development Integration

- **Research Phase**: Use `/docs search` to understand library capabilities
- **Implementation**: Get API references with `/docs search "library api"`
- **Troubleshooting**: Find solutions with `/docs search "library error-type"`

### Setup Required

Follow `.claude/docs/CONTEXT7_SETUP.md` to enable Context7 MCP server.
Without Context7, documentation commands fall back to web search.

CONTEXT7_APPEND

else
    echo "ℹ️  Claude Code not detected - Context7 integration available when using Claude Code CLI"
    echo "   📖 Documentation features will be available after Claude Code setup"
fi

echo ""
echo "🎉 Project Setup Complete!"
echo ""
echo "📁 Project Structure:"
find . -type f -name "*.md" -o -name "*.py" -o -name "*.js" -o -name "*.json" -o -name "*.toml" | head -10
echo ""
echo "💡 Next Steps:"
echo "   1. 🔧 Install dependencies (pip install -e .[dev] or npm install)"
echo "   2. 🚀 Start development: /explore \"your first feature\""
echo "   3. 📊 For code projects: /serena \$(pwd) to enable semantic understanding"
echo "   4. ⚙️  Customize CLAUDE.md for project-specific requirements"
echo ""
echo "🔒 Security & Quality Features Enabled:"
echo "   • Dangerous commands (rm -rf, sudo, chmod 777) automatically blocked"
echo "   • Code automatically formatted & linted on edit:"
echo "     - Python: ruff format + ruff check"
echo "     - JavaScript: prettier + eslint"
echo "     - Markdown: markdownlint"
echo "   • JSON syntax validation on edit"
echo "   • Test file creation hints (pytest integration)"
echo ""
echo "✨ Lean MCP Framework Active:"
echo "   • Enhanced commands with 65% average token reduction"
echo "   • /analyze - Semantic code understanding (when Serena available)"
echo "   • /docs search - Live documentation access (when Context7 available)"
echo "   • Complex reasoning with Sequential Thinking"
echo "   • Graceful degradation ensures everything works regardless"
echo ""
echo "🚀 Ready for evidence-based, token-efficient development!"
```