---
title: "Serena Project Management"
description: "Activate and manage Serena semantic code understanding for projects"
author: "Lean MCP Framework"
version: "1.0.0"
---

# Serena Project Management

Activate Serena's semantic code understanding for efficient, token-optimized code operations.

## Usage
- `/serena` - Show available projects and current status
- `/serena [project]` - Activate specific project

$ARGUMENTS_PRESENT$
I'll activate Serena project: **$ARGUMENTS**

Let me activate the project and show you the available context. I'll use the Serena MCP tools to:

1. Activate the project: $ARGUMENTS
2. Check if onboarding was performed
3. List available memories
4. Show current project status

This will enable semantic code operations with 75% token reduction on code tasks.
$END_ARGUMENTS_PRESENT$

$ARGUMENTS_ABSENT$
Let me show you the current Serena status and available projects.

I'll check your Serena configuration and list all available projects that you can activate.
$END_ARGUMENTS_ABSENT$

## Serena Benefits

When activated, you get:

### 🎯 Semantic Operations (75% token reduction)
- **find_symbol**: Locate functions/classes by name, not text search
- **get_symbols_overview**: See file structure without reading entire file
- **replace_symbol_body**: Edit entire functions/methods precisely
- **find_referencing_symbols**: Track what uses your code

### 📊 Token Savings Example
Traditional approach (high tokens):
```bash
grep -r "function_name" .  # Searches all files
cat entire_file.py         # Reads 1000+ lines
```

Serena approach (low tokens):
```bash
find_symbol("function_name")  # Returns just the function
```

### 💾 Persistent Memory
- Project understanding persists across sessions
- Task progress tracked in memories
- Code conventions remembered

## Your Project Quick Reference

Based on your Serena configuration:

- **my-api** - Your API project
- **my-frontend** - Your frontend project

### Quick Commands:
```bash
/serena my-api         # Activate API project
/serena my-frontend    # Activate frontend project
/serena /new/path      # Activate new project by path
```

---

*Part of the Lean MCP Framework - Evidence-based 75% token reduction on code operations*