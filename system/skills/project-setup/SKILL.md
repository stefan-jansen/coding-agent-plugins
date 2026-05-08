---
name: project-setup
description: This skill should be used when the user asks to "set up a project", "initialize Claude Code", "add Claude framework", "configure project", "create .claude directory", or when starting a new project that needs Claude Code infrastructure (CLAUDE.md, settings, hooks).
invocation: "/system:setup [python|javascript|existing]"
---

# Project Setup Skill

Initialize agent infrastructure for new projects following the Claude + Codex
shared-state convention.

**When to use**: New project or adding agent infrastructure to existing project.

**What it creates**:
- `AGENTS.md` - Canonical project doc (Claude reads via `@AGENTS.md`; Codex reads natively)
- `CLAUDE.md` - One line: `@AGENTS.md`
- `.agents/memory/` - Persistent project state (project_state.md, conventions.md, decisions.md)
- `.agents/transitions/` - Hourly session progress (auto-created by hook)
- `.agents/work/` - Active work units / plans
- `.claude/settings.json` - Plugin marketplace + enabled plugins + transition hook
- `.claude/hooks/init-transition.sh` - Writes hourly file to `.agents/transitions/`
- `.claude/commands/` - Project-specific slash-commands (empty initially)

**Invocation**: Ask Claude to set up the project, or use @project-setup/content.md

@project-setup/content.md
