# ML3T Researcher Plugin

Academic research assistant plugin for Machine Learning for Trading (ML4T) projects.

## Overview

This is a **lightweight plugin** that provides access to the ML3T researcher agent. The actual research infrastructure (Qdrant vector database, Zotero library, API server) remains in `~/ml4t/agents/researcher/` and must be set up separately.

## Architecture: Hybrid Approach

**In Plugin** (distributable, ~100KB):
- Agent definition file
- MCP server configuration for Qdrant
- Documentation and setup instructions

**Separate Infrastructure** (stays in ~/ml4t/agents/researcher/, gigabytes):
- Qdrant vector database with 10,000+ indexed papers
- Zotero library integration
- FastAPI research server
- Python processing pipeline
- Extracted paper data and caches

## Prerequisites

### 1. Qdrant Vector Database

**Required**: YES
**Port**: 6333
**Purpose**: Semantic search across academic papers

**Setup**:
```bash
# Option A: Docker Compose (recommended)
cd ~/ml4t/agents/researcher
docker-compose up -d qdrant

# Option B: Standalone Docker
docker run -p 6333:6333 qdrant/qdrant

# Verify running
curl http://localhost:6333/collections
```

**Health Check**:
```bash
# Should return list of collections
curl http://localhost:6333/collections

# Expected collections:
# - ml3t_papers_local (main paper collection)
```

### 2. Zotero Integration

**Required**: YES
**Purpose**: Bibliography management and paper metadata

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

### 3. Research API Server

**Required**: YES
**Port**: 8000
**Purpose**: Paper processing and research operations

**Setup**:
```bash
cd ~/ml4t/agents/researcher

# Install dependencies (using uv)
uv sync

# Start server
uv run python run_api_server.py

# Or use make command
make run-api
```

**Health Check**:
```bash
# Should return {"status": "healthy"}
curl http://localhost:8000/health

# Check metrics
curl http://localhost:8000/metrics
```

## Installation

1. **Plugin Installation** (automatic via marketplace):
   ```bash
   # Plugin is loaded from ~/agents/claude_code/plugins/ml3t-researcher/
   # No manual installation needed if using marketplace
   ```

2. **Infrastructure Setup**:
   ```bash
   # Navigate to researcher directory
   cd ~/ml4t/agents/researcher

   # Start all services
   docker-compose up -d qdrant    # Start Qdrant
   uv run python run_api_server.py   # Start API server

   # Verify all services
   curl http://localhost:6333/collections  # Qdrant
   curl http://localhost:8000/health        # API server
   ```

3. **Enable in Project**:
   ```json
   // Add to your project's .claude/settings.json
   {
     "plugins": {
       "enabled": ["core", "workflow", "ml3t-researcher"]
     }
   }
   ```

## Usage

### From ML4T Book Project

```bash
# Invoke researcher agent
/agent ml3t-researcher "Find papers on portfolio optimization published after 2020"

# The agent will:
# 1. Verify Qdrant is running (port 6333)
# 2. Query vector store via MCP
# 3. Return relevant papers with citations
# 4. Cache results for future queries
```

### API Endpoints

The researcher exposes REST endpoints:

```python
import requests

# Search for papers
response = requests.post(
    "http://localhost:8000/api/research/search",
    json={"query": "portfolio optimization", "chapter": 5}
)
papers = response.json()

# Verify a claim
response = requests.post(
    "http://localhost:8000/api/research/verify",
    json={"claim": "LSTM networks outperform ARIMA for time series"}
)
verification = response.json()
```

## MCP Integration

This plugin includes Qdrant MCP server configuration:

```json
{
  "mcpServers": {
    "qdrant": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-qdrant"],
      "env": {
        "QDRANT_URL": "http://localhost:6333"
      }
    }
  }
}
```

The MCP server provides direct vector database access for efficient semantic search.

## Troubleshooting

### Qdrant Not Running

**Error**: "Connection refused to localhost:6333"

**Solution**:
```bash
cd ~/ml4t/agents/researcher
docker-compose up -d qdrant
curl http://localhost:6333/collections  # Verify
```

### API Server Not Running

**Error**: "Connection refused to localhost:8000"

**Solution**:
```bash
cd ~/ml4t/agents/researcher
uv run python run_api_server.py
curl http://localhost:8000/health  # Verify
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

### Empty Collections

**Error**: "Collection ml3t_papers_local not found"

**Solution**:
```bash
# Run initial paper ingestion
cd ~/ml4t/agents/researcher
uv run python scripts/zotero/ingest_zotero.py
```

## Performance

Expected performance baselines:

| Metric | Target | Current |
|--------|--------|---------|
| RAG Processing | <0.5s/paper | ✅ 0.49s |
| Success Rate | >85% | ✅ 86.7% |
| Cache Hit Rate | >70% | ✅ 75% |
| API Response | <1s | ✅ 500ms |

## Integration with Coauthor

The researcher plugin works with the ml3t-coauthor plugin:

- **Shared Qdrant**: Both use same vector database (port 6333)
- **API Integration**: Coauthor calls researcher API endpoints
- **Coordinated Access**: Managed through shared environment config

## Maintenance

### Update Paper Index

```bash
cd ~/ml4t/agents/researcher
uv run python scripts/zotero/ingest_zotero.py
```

### Run Quality Checks

```bash
cd ~/ml4t/agents/researcher
make quality  # Linting, formatting, type checking
make test     # Run test suite
```

### Monitor Performance

```bash
# View Prometheus metrics
curl http://localhost:8000/metrics

# Check Qdrant stats
curl http://localhost:6333/collections/ml3t_papers_local
```

## Limitations

1. **Not Portable**: Infrastructure must be set up on each machine
2. **Requires Running Services**: Cannot function without Qdrant and API server
3. **Resource Intensive**: Vector database and API server consume significant resources
4. **Shared State**: Coordinated access needed when coauthor also active

## Documentation

- **Full Agent Docs**: `~/ml4t/agents/researcher/.claude/CLAUDE.md`
- **API Documentation**: `~/ml4t/agents/researcher/README.md`
- **Setup Guide**: This file

## Support

For issues with:
- **Plugin**: Check Claude Code plugin system documentation
- **Infrastructure**: See `~/ml4t/agents/researcher/.claude/CLAUDE.md`
- **Qdrant**: https://qdrant.tech/documentation/
- **Zotero**: https://www.zotero.org/support/

---

**Plugin Type**: Hybrid (lightweight definition + separate infrastructure)
**Version**: 2.0.0
**Last Updated**: 2025-10-11
