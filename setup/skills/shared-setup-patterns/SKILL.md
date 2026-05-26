---
name: shared-setup-patterns
description: Shared configuration patterns for project setup commands. Provides security hooks, agent infrastructure templates (.agents/ + AGENTS.md + CLAUDE.md), and framework detection patterns used across multiple setup commands.
---

# Shared Setup Patterns

**Purpose**: Common configuration patterns and templates shared across all project setup commands.

**Used by**: `/setup:python`, `/setup:javascript`, `/setup:existing`, `/setup:explore`, `/setup:user`

**Token Impact**: Provides ~1,700 tokens of shared templates loaded once, avoiding duplication across 5+ commands (saves ~3,200 tokens through reuse).

---

## Contents

This skill contains ONLY patterns shared by multiple setup commands:

1. **Security Hooks** - PreToolUse and PostToolUse hooks for all project types
2. **Agent Infrastructure Layout** - `AGENTS.md` + `.agents/` + `.claude/` templates
3. **Framework Detection** - Patterns for auto-detecting project languages and frameworks

Language-specific templates (Python, JavaScript, etc.) are kept inline in their respective commands.

---

## 1. Settings Configuration (CRITICAL)

Located: `templates/settings.json`

**MUST be copied to `.claude/settings.json` for every project setup.**

Contains:
- Plugin marketplace configuration (local plugins at ~/agents/plugins)
- Core enabled plugins: system, workflow, memory, development, **transition**

**The transition plugin enables `/handoff` command** - essential for session continuity.

Used by: ALL setup commands that create projects

---

## 2. Security Hooks

Located: `templates/security_hooks.json`

Comprehensive security and quality hooks configuration:
- **PreToolUse**: Blocks dangerous commands (rm -rf, sudo, chmod 777)
- **PostToolUse**: Auto-formats code (ruff, prettier, eslint), validates JSON/markdown

Used by: ALL setup commands that create projects

---

## 3. Agent Infrastructure Layout

Located: `templates/agent_framework/`

Templates for the canonical agent layout:
- `structure.md` - Directory layout: `AGENTS.md` + `CLAUDE.md` + `.agents/` + `.claude/`
- `memory_templates/` - `project_state.md`, `conventions.md`, `decisions.md` (seed for `.agents/memory/`)
- `agents_md_template.md` - Skeleton for project-root `AGENTS.md`

**Path convention** (codified in `~/.claude/CLAUDE.md`):

| Path | Audience | Purpose |
|---|---|---|
| `AGENTS.md` | Codex (native), Claude (via `@AGENTS.md`) | Canonical project instructions |
| `CLAUDE.md` | Claude only | One line: `@AGENTS.md` |
| `.agents/memory/*.md` | Both | Persistent project state |
| `.agents/transitions/YYYY-MM-DD/HH.md` | Both | Hourly session progress |
| `.agents/work/` | Both | Active work units |
| `.claude/settings.json`, `.claude/hooks/`, `.claude/commands/` | Claude only | Claude-specific config |

Used by: ALL setup commands

---

## 4. Framework Detection Patterns

Located: `templates/framework_detection.md`

Patterns for auto-detecting:
- Languages: Python, JavaScript/TypeScript, Go, Rust
- Frameworks: FastAPI, Django, Flask, Next.js, React, Express
- Tools: pytest, Jest, Mocha, go test, cargo test

Used by: `/setup:existing`, `/setup` (if dispatcher exists)

---

## Usage Pattern

Commands reference this skill in frontmatter:
```yaml
skills: [shared-setup-patterns]
```

Then access specific templates:
- **Settings (REQUIRED)**: Copy `templates/settings.json` to `.claude/settings.json`
- Security hooks: Load from `templates/security_hooks.json`
- Agent infrastructure: Generate from `templates/agent_framework/` templates
- Detection: Use patterns from `templates/framework_detection.md`

---

## Design Principle

**Only truly shared content lives here.** Language-specific templates (Python pyproject.toml, JavaScript package.json) stay inline in their respective commands to avoid skill overhead for single-use templates.

This keeps each command self-contained while sharing common infrastructure patterns.
