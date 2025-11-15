# ML3T Research Assistant Agent

**Type**: Academic Research & RAG System
**Version**: 2.0.0
**Infrastructure**: Requires running Qdrant server and Zotero integration

## Purpose

Advanced academic research assistant specialized in Machine Learning for Trading domain. Provides sophisticated paper discovery, fact-checking, code extraction, and knowledge synthesis for ML4T book development.

## Capabilities

### Core Research Functions
- **Paper Discovery**: Semantic search across 10,000+ academic papers via Qdrant vector store
- **Fact Verification**: Validate claims and citations with source tracking
- **Code Extraction**: Extract and analyze code examples from research papers
- **Update Tracking**: Identify changes and developments since previous editions

### Integration Features
- **Zotero Integration**: Manages academic bibliography with 10,000+ paper capacity
- **ar5iv HTML Extraction**: High-quality extraction from arXiv papers with automatic PDF fallback
- **LaTeXML Processing**: Preserves formulas, tables, and section structure
- **Shared Vector Store**: Qdrant database shared with coauthor agent

## API Endpoints

The researcher agent exposes REST API endpoints for integration:

```python
POST /api/research/search       # Find relevant papers
POST /api/research/verify       # Fact-check claims
POST /api/research/extract-code # Get code examples
POST /api/research/find-updates # Changes since 2020
```

## Infrastructure Requirements

**CRITICAL**: This agent requires separate infrastructure that must be running:

### 1. Qdrant Vector Database
```bash
# Must be running on port 6333
docker-compose up -d qdrant
# Verify: curl http://localhost:6333/collections
```

### 2. Zotero Library
```bash
# Environment variables required:
ZOTERO_LIBRARY_ID=xxx
ZOTERO_API_KEY=xxx
```

### 3. Research API Server
```bash
# Start the researcher service
cd ~/ml4t/agents/researcher
uv run python run_api_server.py
# Verify: curl http://localhost:8000/health
```

## Agent Location

**Full Implementation**: `~/ml4t/agents/researcher/`
**Plugin Definition**: This lightweight agent definition file only
**Working Files**: Data, vector stores, and processing remain in agent directory

## Usage from ML4T Projects

When invoked from ML4T book or related projects, this agent:

1. Verifies Qdrant connection (port 6333)
2. Checks API server availability (port 8000)
3. Delegates research tasks to running infrastructure
4. Returns structured results with citations

## Performance Baselines

| Metric | Target | Current |
|--------|--------|---------|
| RAG Processing | <0.5s/paper | ✅ 0.49s |
| Success Rate | >85% | ✅ 86.7% |
| Cache Hit Rate | >70% | ✅ 75% |
| API Response | <1s | ✅ 500ms |

## MCP Integration

This agent uses MCP servers defined in plugin.json:
- **Qdrant MCP**: Direct vector database access
- **Sequential Thinking**: Complex research reasoning (optional)

## Graceful Degradation

If infrastructure is unavailable:
- Agent invocation will fail with clear error message
- Error will specify which component is not running
- Provides setup instructions for missing services

## Quality Standards

- Linting: `ruff check app tests --fix`
- Formatting: `ruff format app tests`
- Type checking: `mypy app --ignore-missing-imports`
- Tests: `uv run pytest tests/unit`

## Integration with Coauthor

The researcher agent works closely with the coauthor agent:
- Shares Qdrant vector database (same port 6333)
- Provides research API for coauthor's use
- Coordinated through shared environment configuration

## Invocation Example

```python
# From ML4T book project
/agent ml3t-researcher "Find papers on portfolio optimization published after 2020"

# The agent will:
# 1. Check Qdrant is running
# 2. Query vector store via MCP
# 3. Return relevant papers with citations
# 4. Cache results for future queries
```

## Setup Verification

Before first use, verify infrastructure:

```bash
# Check Qdrant
curl http://localhost:6333/collections

# Check API server
curl http://localhost:8000/health

# Check Zotero credentials
echo $ZOTERO_LIBRARY_ID
echo $ZOTERO_API_KEY
```

## Known Limitations

1. **Requires Running Services**: Cannot function without Qdrant and API server
2. **Not Portable**: Infrastructure stays in ~/ml4t/agents/researcher/
3. **Shared Resources**: Coordinated access needed when coauthor also active

## Documentation

- **Full Agent Docs**: `~/ml4t/agents/researcher/.claude/CLAUDE.md`
- **API Documentation**: `~/ml4t/agents/researcher/README.md`
- **Integration Guide**: See coauthor agent for usage patterns

---

**Note**: This is a lightweight plugin definition. The actual researcher implementation lives in `~/ml4t/agents/researcher/` and must be set up separately.
