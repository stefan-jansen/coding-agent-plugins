---
name: project-setup
description: This skill should be used when the user asks to "set up a project", "initialize Claude Code", "add Claude framework", "configure project", "create .claude directory", or when starting a new project that needs Claude Code infrastructure (CLAUDE.md, settings, hooks).
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
