---
title: cleanup
aliases: [housekeeping, organize, tidy, clean]
description: Clean up Claude-generated clutter and consolidate documentation
allowed-tools: [Bash, Read, Write, Glob, MultiEdit]
argument-hint: "[--dry-run | --auto | root | tests | reports | work | all]"
---

# Smart Project Cleanup

Clean up clutter from Claude development sessions.

**Arguments**: $ARGUMENTS

## Modes

| Mode | Description |
|------|-------------|
| `reports` | Consolidate .md reports into README/work units |
| `reports --auto` | Auto-consolidate without prompts |
| `root` | Clean misplaced files from root directory |
| `tests` | Move test files to tests/ |
| `work` | Clean .agents/work directory |
| `all` | Full cleanup (default) |
| `--dry-run` | Preview without changes |

## What Gets Cleaned

**Root clutter**: Random .md files, one-off scripts, misplaced configs
**Test files outside tests/**: `test_*.py`, `debug_*.py`, `temp_*.py`
**Report proliferation**: `*_REPORT.md`, `*_ANALYSIS.md`, `*_PLAN.md`
**Work directory**: Completed work >7 days, abandoned units (`.agents/work/`)

## Consolidation Logic

Reports classified by content and filename:
- **Work-related** (`analysis`, `findings`) → `.agents/work/current/`
- **Architecture docs** (`design`, `pattern`) → `.agents/reference/`
- **General insights** → Append to `README.md`

## Process

1. Scan for clutter by category
2. Show preview with suggested action
3. Interactive (default) or auto mode
4. Archive originals to `.archive/cleanup_TIMESTAMP/`
5. Report changes made

## Target Structure

```
project/
├── README.md              # Main docs
├── AGENTS.md              # Canonical agent doc (Claude + Codex)
├── CLAUDE.md              # one-liner: @AGENTS.md
├── .agents/
│   ├── memory/            # Persistent project state
│   ├── transitions/       # Session progress
│   └── work/              # All work units
├── .claude/
│   ├── settings.json      # Plugins, hooks, permissions
│   ├── hooks/             # Claude-specific hooks
│   └── commands/          # Project slash-commands
├── tests/                 # ALL test files
├── scripts/               # Utility scripts
└── src/                   # Source code
```

## Preserved

Core docs, source code, formal tests, structured work units

## Removed/Archived

Debug scripts, one-off tests, duplicate docs, misplaced files
