---
allowed-tools: [Read, Write, Grep, Bash, LS, Task, mcp__sequential-thinking__sequentialthinking, mcp__serena__find_symbol, mcp__serena__search_for_pattern, mcp__serena__get_symbols_overview, mcp__serena__find_referencing_symbols]
argument-hint: "[focus_area | @doc] [--with-thinking] [--semantic]"
description: "Analyze project structure and architecture"
---

# Analyze Project

Deep codebase analysis for architecture, patterns, and improvement opportunities.

**Input**: $ARGUMENTS

## Flags

- `--with-thinking`: Use Sequential Thinking for complex analysis
- `--semantic`: Use Serena for symbol-level understanding

## Process

1. **Determine Scope**
   - No args: Comprehensive review
   - Focus area: Targeted examination
   - @document: Requirements-based analysis

2. **Project Assessment**
   - Language/framework detection
   - Architecture style (monolith, microservices, layered)
   - Code organization and patterns
   - Testing approach and coverage
   - Documentation state
   - Technical debt indicators

3. **Deep Analysis**
   - Map core components and responsibilities
   - Trace dependency relationships
   - Identify design patterns in use
   - Find integration points and boundaries
   - Assess code quality and maintainability

4. **Semantic Analysis** (with Serena)
   - Symbol-level component mapping
   - Actual import/dependency tracking
   - Interface and API surface analysis
   - Cross-reference usage patterns

5. **Generate Report**
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
