---
allowed-tools: [Task, Bash, Read, Write, Grep, MultiEdit, mcp__firecrawl__firecrawl_search, mcp__firecrawl__firecrawl_scrape, mcp__sequential-thinking__sequentialthinking]
argument-hint: "[@file | #issue | description | empty] [--work-unit ID]"
description: "Explore requirements and codebase before planning"
---

# Requirements Exploration

Analyze requirements and codebase context. First step in "Explore → Plan → Code → Commit" workflow.

**Input**: $ARGUMENTS

## Sources

- `@file.md` - Read and analyze document
- `#123` - Fetch GitHub issue
- `"description"` - Natural language requirement
- *(empty)* - General codebase exploration

## Process

1. **Create Work Unit**
   - Generate ID: `YYYY-MM-DD_NN_topic`
   - Create `.claude/work/{id}/` with: metadata.json, requirements.md, exploration.md
   - Set as ACTIVE_WORK

2. **Analyze Source**
   - Documents: Extract requirements, identify gaps, assess complexity
   - Issues: Fetch details, understand context, map technical needs
   - Description: Clarify scope, define success criteria, identify constraints

3. **Explore Codebase**
   - Understand architecture and patterns
   - Identify integration points
   - Map affected components
   - Use Serena for semantic analysis when available

4. **Generate Output**
   - `requirements.md`: Functional/non-functional requirements, acceptance criteria, risks
   - `exploration.md`: Architecture analysis, implementation approach, key files

5. **Smart Planning**
   - Simple requirements → Generate complete plan + state.json → Ready for /next
   - Complex requirements → Generate outline → Recommend /plan

## Work Unit Structure

```
.claude/work/YYYY-MM-DD_NN_topic/
├── metadata.json      # Status, created_at, requirement_type
├── requirements.md    # Captured requirements
├── exploration.md     # Analysis findings
└── state.json        # Tasks (if plan auto-generated)
```

## Next Steps

- **Clear plan generated**: "Run /next to implement"
- **Needs refinement**: "Run /plan for detailed breakdown"
- **Has ambiguities**: List clarifying questions first
