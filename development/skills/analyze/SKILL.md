---
name: analyze
description: This skill should be used when the user asks to "analyze this code", "understand the architecture", "examine the codebase", "project structure", "how is this organized", or when exploring an unfamiliar codebase to understand its patterns, components, and design. Do NOT use for simple file reads or grep searches.
allowed-tools: [Read, Write, Grep, Bash, LS, Task, mcp__sequential-thinking__sequentialthinking, mcp__serena__find_symbol, mcp__serena__search_for_pattern, mcp__serena__get_symbols_overview, mcp__serena__find_referencing_symbols]
---

# Code Analysis

Deep codebase analysis for architecture, patterns, and improvement opportunities.

## When This Triggers

- "Analyze this code" / "analyze the project"
- "What's the architecture?"
- "How is this codebase organized?"
- "Understand this codebase"
- "Examine the structure"
- Exploring unfamiliar codebases

## Flags (if explicitly passed)

- `--with-thinking`: Use Sequential Thinking for complex analysis
- `--semantic`: Use Serena for symbol-level understanding

## Process

### 1. Determine Scope

- No specific focus: Comprehensive review
- Focus area mentioned: Targeted examination
- Document referenced: Requirements-based analysis

### 2. Project Assessment

- Language/framework detection
- Architecture style (monolith, microservices, layered)
- Code organization and patterns
- Testing approach and coverage
- Documentation state
- Technical debt indicators

### 3. Deep Analysis

- Map core components and responsibilities
- Trace dependency relationships
- Identify design patterns in use
- Find integration points and boundaries
- Assess code quality and maintainability

### 4. Semantic Analysis (with Serena)

When Serena MCP is available:
- Symbol-level component mapping
- Actual import/dependency tracking
- Interface and API surface analysis
- Cross-reference usage patterns

### 5. Generate Report

- Architecture overview diagram (ASCII/Mermaid)
- Component inventory
- Quality assessment
- Improvement recommendations
- Risk areas

## Output

Write findings to `exploration.md` or return structured summary:
- Architecture type and patterns
- Key components and relationships
- Quality metrics
- Actionable recommendations
