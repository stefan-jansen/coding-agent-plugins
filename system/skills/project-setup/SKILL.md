---
name: project-setup
description: Initialize Claude Code framework infrastructure for any project
invocation: "/system:setup [python|javascript|existing]"
---

# Project Setup Skill

Initialize `.claude/` infrastructure for Claude Code projects.

**When to use**: New project or adding Claude framework to existing project.

**What it creates**:
- `.claude/settings.json` - Plugin marketplace + enabled plugins
- `.claude/work/` - Work unit tracking
- `.claude/memory/` - Project knowledge persistence
- `.claude/hooks/` - Session hooks (transitions)
- `CLAUDE.md` - Project instructions

**Invocation**: Ask Claude to set up the project, or use @project-setup/content.md

@project-setup/content.md
