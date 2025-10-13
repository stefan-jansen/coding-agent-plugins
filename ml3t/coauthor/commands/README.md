# Claude Code Commands

This directory contains slash commands for the co-authoring framework.

## Command Structure

Each command is a Markdown file with:
- YAML frontmatter for configuration
- Instructions for Claude to execute

## Available Commands

### Core Workflow
- `/research` - Find and fetch research materials
- `/outline` - Generate chapter outlines
- `/write` - Draft chapter content
- `/review` - Create pull request for review

### Code Management
- `/notebook` - Manage Jupyter notebooks
- `/test` - Run code tests
- `/sync` - Synchronize code and text

### Utilities
- `/status` - View project progress
- `/cite` - Manage citations
- `/publish` - Prepare for publication

## Creating Commands

```markdown
---
description: "Brief command description"
argument-hint: "[expected arguments]"
allowed-tools: [Read, Write, Edit, Bash]
---

# Command Name

Instructions for Claude...

Use $ARGUMENTS for user input.
```

## Best Practices

- Keep commands focused (single responsibility)
- Use clear, descriptive names
- Document expected arguments
- Include error handling
- Provide feedback to user