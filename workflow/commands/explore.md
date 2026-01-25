---
allowed-tools: [Task, Bash, Read, Write, Grep, mcp__sequential-thinking__sequentialthinking]
argument-hint: "[@file | #issue | description]"
description: "Quick exploration without plan mode (use /work new for full planning)"
---

# Quick Exploration

Light-weight requirements analysis. For full planning with plan mode integration, use `/work new [topic]` instead.

**Input**: $ARGUMENTS

## When to Use

| Command | Use Case |
|---------|----------|
| `/work new [topic]` | Full planning with Claude's plan mode (recommended) |
| `/explore [source]` | Quick analysis without entering plan mode |

## Process

1. **Analyze Source**
   - `@file.md` - Extract requirements from document
   - `#123` - Fetch and analyze GitHub issue
   - `"description"` - Clarify natural language requirement

2. **Explore Codebase**
   - Understand architecture and patterns
   - Identify integration points
   - Map affected components

3. **Output Summary**
   - Key requirements identified
   - Complexity assessment
   - Recommended approach

## Recommendation

For tracked work with task management:
```
/work new "add user authentication"
```
This creates a work unit, enters plan mode for thorough planning, then you capture the plan for `/next` execution.

## Legacy Support

This command previously created work units directly. That workflow still works:
- Creates `.claude/work/YYYY-MM-DD_NN_topic/` if no active unit
- Generates requirements.md and exploration.md
- For simple tasks, auto-generates state.json

But `/work new` with plan mode produces better plans.
