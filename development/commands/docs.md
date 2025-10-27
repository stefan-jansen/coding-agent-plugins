---
allowed-tools: [Bash, Read, Write, MultiEdit, Grep, Glob, Task, WebFetch, mcp__context7__resolve-library-id, mcp__context7__get-library-docs]
argument-hint: "fetch|search|generate [arguments]"
description: Unified documentation operations - fetch external, search all, and generate project docs
---

# Documentation Operations Hub

Consolidated command for all documentation-related operations. Clear separation between fetching external docs, searching, and generating project documentation.

**Input**: $ARGUMENTS

## Usage

### Fetch External Documentation
```bash
/docs fetch                    # Fetch official Claude Code & library docs
/docs fetch --force            # Force complete re-fetch (clear cache)
/docs fetch --status           # Check cache status and last fetch time
/docs fetch --libraries        # Focus on project dependency docs
```

### Search Documentation
```bash
/docs search "command syntax"      # Search all cached documentation
/docs search "hooks examples"      # Find specific topics
/docs search "MCP integration"     # Search across all docs
/docs search "pytest fixtures"     # Search library-specific docs
```

### Generate Project Documentation
```bash
/docs generate "Added auth system"   # Generate/update docs after changes
/docs generate                       # Interactive documentation generation
/docs generate --api                 # Focus on API documentation
/docs generate --readme              # Update README only
```

## Phase 1: Determine Documentation Operation

Based on the arguments provided: $ARGUMENTS

I'll determine which documentation operation to perform:

- **Fetch Operations**: Arguments start with "fetch" - fetch external documentation into cache
- **Search Operations**: Arguments start with "search" - search all available documentation
- **Generate Operations**: Arguments start with "generate" - generate/update project documentation
- **Help Mode**: No arguments - show usage guidance with clear distinctions

## Phase 2: Execute Documentation Fetch

When handling fetch operations:

### Fetching External Documentation
1. **Source Identification**: Determine official Claude Code documentation sources
2. **Cache Management**: Create/update local documentation cache in `.claude/docs/`
3. **Version Tracking**: Track documentation versions and update timestamps
4. **Content Organization**: Organize docs by topic (commands, agents, hooks, MCP)
5. **Index Creation**: Create searchable index of documentation content

### Fetch Modes
1. **Incremental Fetch** (default): Fetch only changed or new documentation
2. **Force Fetch** (--force): Complete re-download and cache refresh
3. **Status Check** (--status): Report cache status and last fetch information
4. **Library Focus** (--libraries): Prioritize project dependency documentation

### Enhanced Fetch (with Context7 MCP)
When Context7 MCP is available, enhance documentation sync with intelligent library detection:

**Automatic Library Documentation Sync**:
1. **Dependency Detection**: Scan project files (package.json, requirements.txt, etc.) for libraries
2. **Library Resolution**: Use Context7 to resolve library names to official documentation
3. **Version-Aware Sync**: Fetch documentation matching exact dependency versions
4. **Intelligent Caching**: Cache frequently-used library documentation locally

**Context7 Fetch Process**:
- Automatically detect project dependencies
- Resolve each library using `mcp__context7__resolve-library-id`
- Fetch comprehensive documentation using `mcp__context7__get-library-docs`
- Organize documentation by library and version in `.claude/docs/libraries/`
- Create searchable index linking local project to relevant library docs

**Smart Documentation Features**:
- **Framework-Specific**: Automatically include framework-specific best practices
- **API-Complete**: Ensure complete API reference for all dependencies
- **Example-Rich**: Include usage examples and patterns from Context7
- **Update-Aware**: Check for documentation updates on library version changes

**Graceful Degradation**: When Context7 unavailable, falls back to manual documentation fetch using web fetch and local caching.

## Context7 MCP Availability Check

Before attempting Context7 operations, I'll check availability:
- Test Context7 MCP connection with simple library resolution
- On failure, automatically switch to fallback methods
- Provide clear user feedback about which mode is active
- Maintain full functionality regardless of MCP availability

## Phase 3: Execute Documentation Search

When handling search operations:

### Local Cache Search
1. **Index Search**: Use cached documentation index for fast search
2. **Content Search**: Full-text search across all cached documentation
3. **Topic Filtering**: Search within specific documentation categories
4. **Relevance Ranking**: Rank results by relevance and recency

### Advanced Search (with Context7 MCP)
When Context7 MCP is available, enhance search with library-specific intelligence:

**Context7 Library Documentation Search**:
1. **Automatic Library Resolution**: Identify libraries from project dependencies
2. **Version-Specific Documentation**: Access docs matching exact library versions
3. **Semantic Library Search**: Find relevant topics within library documentation
4. **API Reference Lookup**: Direct access to function/class documentation

**Context7 Enhanced Search Process**:
- When searching for library-specific topics, automatically resolve library names
- Fetch up-to-date documentation from Context7's knowledge base
- Provide focused, relevant results from official library documentation
- Fall back to cached local search when Context7 unavailable

**Example Context7 Usage**:
```bash
/docs search "react hooks"     # → Uses Context7 to find React hooks documentation
/docs search "express middleware" # → Fetches Express.js middleware docs via Context7
/docs search "pytest fixtures"   # → Gets current pytest fixture documentation
```

### Traditional Search (Fallback)
When Context7 MCP is unavailable:

1. **Local Cache Search**: Use cached documentation index for fast search
2. **Live Web Search**: Search current online documentation via Firecrawl when available
3. **Cross-Reference Search**: Find related concepts in cached documentation
4. **Code Example Search**: Find relevant code examples from local cache

### Search Result Presentation
1. **Relevant Excerpts**: Show context around matching content
2. **Source Attribution**: Clear indication of documentation source
3. **Direct Links**: Provide links to full documentation when available
4. **Related Topics**: Suggest related documentation sections

## Phase 4: Execute Documentation Generation

When handling generate operations:

### Project Documentation Generation
1. **Current State Assessment**: Analyze existing project documentation
2. **Gap Identification**: Identify missing or outdated documentation
3. **Change Impact Analysis**: Understand what documentation needs updating
4. **Content Planning**: Plan what documentation to create or update

### Generation Operations
1. **API Documentation**: Generate API docs from code analysis
2. **README Generation**: Update README with new features and changes
3. **Code Comments**: Generate missing docstrings and comments
4. **Usage Examples**: Create usage examples from test cases
5. **Migration Guides**: Generate migration guides for breaking changes

### Enhanced Generation (with MCP Tools)
When MCP servers are available:

1. **Automated API Docs**: Generate API documentation from code analysis
2. **Intelligent Examples**: Create relevant usage examples automatically
3. **Cross-Platform Docs**: Ensure documentation works across different platforms
4. **Documentation Testing**: Verify documentation examples actually work

## Phase 5: Documentation Quality Assurance

For all documentation operations:

### Content Validation
1. **Accuracy Verification**: Ensure documentation matches actual implementation
2. **Link Checking**: Validate all internal and external links work
3. **Code Example Testing**: Verify all code examples execute correctly
4. **Formatting Consistency**: Ensure consistent formatting and style

### Organization and Accessibility
1. **Logical Structure**: Organize documentation in intuitive hierarchy
2. **Navigation Aids**: Create table of contents and cross-references
3. **Search Optimization**: Ensure content is easily searchable
4. **Version Compatibility**: Mark documentation with applicable versions

## Phase 6: Cache and State Management

### Documentation Cache Structure
```
.claude/docs/
├── official/          # Official Claude Code documentation
│   ├── commands/      # Command documentation
│   ├── agents/        # Agent documentation
│   ├── hooks/         # Hook documentation
│   └── api/           # API reference
├── libraries/         # Third-party library documentation
├── project/           # Project-specific documentation
└── cache_metadata.json  # Cache status and timestamps
```

### Cache Maintenance
1. **Size Management**: Keep cache size reasonable for performance
2. **Staleness Detection**: Identify and refresh outdated documentation
3. **Cleanup Operations**: Remove unnecessary or duplicate documentation
4. **Index Rebuilding**: Maintain searchable index of documentation content

## Success Indicators

### Fetch Operations Success
- ✅ External documentation cached locally
- ✅ Cache index updated and searchable
- ✅ Version information tracked
- ✅ Dependencies documentation fetched (when MCP available)

### Search Operations Success
- ✅ Relevant results found and presented
- ✅ Context provided with search results
- ✅ Source attribution clear
- ✅ Related topics suggested

### Generate Operations Success
- ✅ Project documentation generated and current
- ✅ API documentation reflects latest code
- ✅ Examples created and tested
- ✅ Migration guides generated for changes

## Common Documentation Patterns

### API Documentation
- Clear endpoint descriptions with parameters
- Request/response examples
- Error code documentation
- Authentication requirements

### User Guides
- Step-by-step instructions
- Screenshots and examples
- Common use cases
- Troubleshooting sections

### Developer Documentation
- Architecture explanations
- Contributing guidelines
- Development setup instructions
- Testing procedures

## Examples

### Fetch Latest Documentation
```bash
/docs fetch
# → Downloads and caches latest official Claude Code & library documentation
```

### Search for Specific Topics
```bash
/docs search "hook examples"
# → Finds and displays relevant hook documentation and examples
```

### Generate Project Documentation
```bash
/docs generate "Added authentication system with JWT tokens"
# → Generates/updates README, API docs, and creates usage examples
```

### Force Complete Documentation Refresh
```bash
/docs fetch --force
# → Completely refreshes external documentation cache
```

## Integration Benefits

- **MCP Intelligence**: Leverages Context7 for library docs and Firecrawl for web content
- **Automated Updates**: Keeps documentation synchronized with code changes
- **Smart Search**: Intelligent search across all documentation sources
- **Version Awareness**: Matches documentation to actual dependency versions
- **Quality Assurance**: Validates documentation accuracy and completeness

---

*Unified documentation command with clear operations: fetch external docs, search everything, and generate project documentation.*