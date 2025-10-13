# ML3T Co-Authoring Plugin

Book production orchestration framework for Machine Learning for Trading (ML4T) 3rd edition.

## Overview

This is a **lightweight plugin** that provides access to the ML3T co-authoring agent. The actual authoring infrastructure (Git repository, chapter content, state files, notebooks) remains in `~/ml4t/agents/coauthor/` and must be set up separately.

## Architecture: Hybrid Approach

**In Plugin** (distributable, ~100KB):
- Agent definition file
- Workflow configuration
- Documentation and setup instructions

**Separate Infrastructure** (stays in ~/ml4t/agents/coauthor/):
- Chapter content and state files
- Jupyter notebooks and code examples
- Git repository structure
- Python environment and dependencies

## Prerequisites

### 1. Git Repository

**Required**: YES
**Purpose**: Version control and pull request workflow

**Setup**:
```bash
cd ~/ml4t/agents/coauthor
git init
git remote add origin [repository-url]
```

**Verification**:
```bash
git status  # Should show clean repository
```

### 2. Zotero Integration

**Required**: YES
**Purpose**: Bibliography management and citations

**Setup**:
```bash
# Add to ~/.zshrc or ~/.bashrc:
export ZOTERO_LIBRARY_ID="your_library_id"
export ZOTERO_API_KEY="your_api_key"

# Get credentials from:
# https://www.zotero.org/settings/keys
```

**Verification**:
```bash
echo $ZOTERO_LIBRARY_ID
echo $ZOTERO_API_KEY
```

### 3. ML3T Researcher Agent

**Required**: YES
**Plugin Dependency**: ml3t-researcher
**Purpose**: Paper discovery and research integration

**Setup**:
```bash
# Ensure researcher plugin is enabled in settings.json
# Researcher must have Qdrant running (port 6333)
# See ml3t-researcher plugin documentation
```

**Verification**:
```bash
# Check Qdrant is running
curl http://localhost:6333/collections

# Check researcher API
curl http://localhost:8000/health
```

### 4. Python Environment

**Required**: YES
**Version**: Python 3.9+
**Purpose**: Jupyter notebook execution

**Setup**:
```bash
cd ~/ml4t/agents/coauthor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Verification**:
```bash
python --version  # Should show 3.9 or higher
jupyter --version  # Verify Jupyter installed
```

## Installation

1. **Plugin Installation** (automatic via marketplace):
   ```bash
   # Plugin is loaded from ~/agents/claude_code/plugins/ml3t-coauthor/
   # No manual installation needed if using marketplace
   ```

2. **Infrastructure Setup**:
   ```bash
   # Navigate to coauthor directory
   cd ~/ml4t/agents/coauthor

   # Initialize Git if not already
   git init

   # Set up Python environment
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Enable in Project**:
   ```json
   // Add to your ML4T book project's .claude/settings.json
   {
     "plugins": {
       "enabled": [
         "core",
         "workflow",
         "ml3t-researcher",
         "ml3t-coauthor"
       ]
     }
   }
   ```

## Usage

### 4-Phase Workflow

The coauthor agent orchestrates book production through 4 phases:

#### 1. Research Phase
```bash
/agent ml3t-coauthor "Research portfolio optimization techniques for Chapter 5"

# Behind the scenes:
# - Invokes ml3t-researcher agent
# - Queries Qdrant for relevant papers
# - Organizes research materials
# - Creates research summary
```

#### 2. Outline Phase
```bash
/agent ml3t-coauthor "Generate outline for Chapter 5 based on research"

# Creates structured outline:
# - Main sections and subsections
# - Key concepts to cover
# - Code examples needed
# - Citations to include
```

#### 3. Writing Phase
```bash
/agent ml3t-coauthor "Draft Section 5.2: Mean-Variance Optimization"

# Generates draft content:
# - Academic prose
# - Integrated citations
# - Code snippets
# - Figures and tables
```

#### 4. Review Phase
```bash
/agent ml3t-coauthor "Create pull request for Chapter 5 review"

# Git workflow:
# - Commits draft to feature branch
# - Creates pull request
# - Adds review checklist
# - Notifies reviewers
```

### Command Examples

```bash
# Check progress
/agent ml3t-coauthor "Show status of Chapter 5"

# Manage notebooks
/agent ml3t-coauthor "Create notebook for backtesting examples"

# Validate code
/agent ml3t-coauthor "Test all notebooks in Chapter 5"

# Manage citations
/agent ml3t-coauthor "Add citation for Sharpe 1994 paper"

# Sync content
/agent ml3t-coauthor "Ensure code and text are aligned"
```

## Integration with Researcher

The coauthor plugin depends on and integrates with ml3t-researcher:

```
Research Integration Flow:
┌──────────────┐
│  Coauthor    │
│    Agent     │
└──────┬───────┘
       │ invokes
       ▼
┌──────────────┐    queries    ┌──────────────┐
│  Researcher  │───────────────▶│   Qdrant     │
│    Agent     │                │  (port 6333) │
└──────────────┘                └──────────────┘
       │
       │ returns papers
       ▼
┌──────────────┐
│  Chapter     │
│  Outline     │
└──────────────┘
```

**Shared Resources**:
- Qdrant vector database (port 6333)
- Zotero library
- Environment configuration

## Project Structure

The coauthor manages this structure:

```
~/ml4t/agents/coauthor/.claude/
├── book/
│   ├── chapters/           # Chapter content by ID
│   │   ├── 001_intro/
│   │   └── 002_data/
│   ├── research/           # Research materials
│   ├── state/             # State management
│   └── manifest.json      # Single source of truth
├── commands/              # Slash commands (12 total)
├── agents/               # Specialized agents (4 total)
└── memory/              # CLAUDE.md files
```

## Performance Targets

| Metric | Target | Purpose |
|--------|--------|---------|
| Draft Generation | 1,500-2,000 words/day | Production rate |
| Review Cycle | <7 days/chapter | Human review time |
| Command Response | <30 seconds | User experience |
| Code Success Rate | >95% | Notebook execution |

## Quality Standards

- **Content Approval**: 90%+ first-pass approval rate
- **Notebook Execution**: 95%+ success rate
- **Citation Accuracy**: 100% required
- **Style Consistency**: Enforced across chapters

## Troubleshooting

### Git Not Initialized

**Error**: "Not a git repository"

**Solution**:
```bash
cd ~/ml4t/agents/coauthor
git init
```

### Researcher Not Available

**Error**: "ml3t-researcher agent not found"

**Solution**:
```bash
# Enable researcher plugin in settings.json
# Ensure Qdrant is running
curl http://localhost:6333/collections

# Check researcher API
curl http://localhost:8000/health
```

### Zotero Credentials Missing

**Error**: "ZOTERO_LIBRARY_ID not set"

**Solution**:
```bash
# Add to shell config
export ZOTERO_LIBRARY_ID="your_id"
export ZOTERO_API_KEY="your_key"

# Reload shell
source ~/.zshrc  # or ~/.bashrc
```

### Python Environment Issues

**Error**: "ModuleNotFoundError: No module named 'jupyter'"

**Solution**:
```bash
cd ~/ml4t/agents/coauthor
source venv/bin/activate
pip install -r requirements.txt
```

### Notebook Execution Failures

**Error**: "Kernel died while executing notebook"

**Solution**:
```bash
# Check Python version
python --version  # Must be 3.9+

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check notebook syntax
jupyter nbconvert --execute [notebook].ipynb
```

## Stateless Architecture

Key design principle of the coauthor framework:

- **Every operation is discrete**: No persistent connections
- **File-based persistence**: All state in JSON and Git
- **No background processes**: Commands complete and exit
- **Idempotent operations**: Safe to re-run commands

## Git-Based Collaboration Workflow

1. **Draft Generation**: Coauthor creates content
2. **Feature Branch**: Content committed to `chapter-X` branch
3. **Pull Request**: Created with review checklist
4. **Human Review**: Expert reviews and comments
5. **Revision**: Coauthor addresses feedback
6. **Approval**: Reviewer approves PR
7. **Merge**: Content integrated into main

## Integration with ML4T Book

When used from the ML4T book project:

```
~/ml4t/book/
├── .claude/settings.json  # Enable coauthor plugin
├── chapters/              # Generated content
│   ├── 01-introduction/
│   ├── 02-data-sources/
│   └── ...
├── code/                  # Notebooks and examples
└── references/            # Zotero bibliography
```

## Limitations

1. **Requires Researcher**: Cannot function without ml3t-researcher agent
2. **Git Required**: Must be in Git repository
3. **Python 3.9+**: Notebook execution requires modern Python
4. **Human Review**: AI generates drafts, humans must approve
5. **Zotero Library**: Requires configured Zotero account

## Performance Optimization

For optimal performance:

1. **Keep researcher running**: Avoids startup overhead
2. **Cache research results**: Qdrant caching improves speed
3. **Incremental commits**: Don't wait for full chapters
4. **Parallel workflows**: Work on multiple chapters concurrently

## Documentation

- **Full Agent Docs**: `~/ml4t/agents/coauthor/README.md`
- **Architecture Guide**: `~/ml4t/agents/coauthor/architecture.md`
- **Requirements Spec**: `~/ml4t/agents/coauthor/requirements.md`
- **Implementation Tasks**: `~/ml4t/agents/coauthor/implementation_tasks.json`

## Support

For issues with:
- **Plugin**: Check Claude Code plugin system documentation
- **Infrastructure**: See `~/ml4t/agents/coauthor/README.md`
- **Git**: https://git-scm.com/doc
- **Zotero**: https://www.zotero.org/support/
- **Researcher Integration**: See ml3t-researcher plugin README

---

**Plugin Type**: Hybrid (lightweight definition + separate infrastructure)
**Version**: 1.0.0
**Dependencies**: ml3t-researcher ^2.0.0
**Last Updated**: 2025-10-11
