---
title: handoff
aliases: [transition]
---

# Conversation Handoff

Prepare a smooth transition for the next conversation when approaching context limits or switching focus.

## Purpose

Creates a structured handoff document that:
1. **Extracts session-specific context** for immediate continuation
2. **Updates permanent memory** with durable learnings
3. **Prepares clean transition** for the next agent

## What Gets Created

### Transition Document
**Location**: `.claude/transitions/YYYY-MM-DD_NNN/handoff.md`

Contains:
- **Current Work Context**: What was being worked on, why, and current state
- **Recent Decisions**: Important choices made this session (not yet in permanent docs)
- **Active Challenges**: Current blockers, open questions, debugging context
- **Next Steps**: Specific, actionable tasks ready for immediate execution
- **Session-Specific State**: File changes, test results, temporary findings

### Memory Updates (if needed)
Updates `.claude/memory/` files with durable knowledge:
- **project_state.md**: Architecture changes, new components
- **conventions.md**: Discovered patterns, coding standards
- **dependencies.md**: New integrations, API changes

## Usage

```bash
# Standard handoff - analyzes conversation and creates transition
/handoff

# With specific focus for next session
/handoff "focusing on performance optimization"

# Quick handoff (minimal extraction)
/handoff --quick
```

## Handoff Process

I'll analyze our conversation and execute these steps:

1. **Identify Durable Knowledge** → Update `.claude/memory/` files if needed
2. **Extract Session Context** → Create comprehensive transition document
3. **Verify Symlink** → Ensure `.claude/transitions/latest/handoff.md` is correct
4. **Inform User** → Tell user to run `/clear` manually (auto-clear not available via SlashCommand)

**IMPORTANT**: After I complete the handoff document, you must manually continue:

1. Run `/clear` (the CLI command, not a slash command)
2. Say: "continue from .claude/transitions/latest/handoff.md"

**Note**: Auto-continue after `/clear` is NOT supported. You must explicitly tell me to continue from the handoff document.

## User Continuation Steps

After I create the handoff document and verify the symlink:

**Step 1**: Run `/clear` to reset conversation context
```bash
/clear
```

**Step 2**: Explicitly tell me to continue from handoff
```
continue from .claude/transitions/latest/handoff.md
```

**Manual intervention required** - There is no automatic detection or loading after `/clear`.

## Intelligence Guidelines

### What Goes in Permanent Memory
- Architectural decisions and rationale
- Discovered patterns and conventions
- Integration points and dependencies
- Long-term project goals

### What Stays in Transition
- Current debugging context
- Today's specific task progress
- Temporary workarounds
- Session-specific file edits

### What's Excluded
- Verbose narratives about changes
- Historical context ("we tried X then Y")
- Meta-discussion about process
- Redundant information already in docs

## Example Transition Structure

```markdown
# Handoff: 2025-09-18_001

## Active Work
Implementing MCP memory system with two-flow approach

## Current State
- Created /handoff and /memory-update commands
- Serena configured and working for semantic operations
- 4 MCP tools operational (Sequential Thinking, Context7, Serena, Firecrawl)

## Recent Decisions
- Use .claude/memory/ for durable knowledge referenced by CLAUDE.md
- Transition documents in .claude/transitions/ for session handoffs
- Keep README.md deliberately concise

## Next Steps
1. Test /handoff command with real scenario
2. Configure .claude/memory/ structure
3. Update CLAUDE.md to reference memory modules

## Session Context
Working in: /home/stefan/agents/claude_code
Last focus: Memory system design
Open PR: feature/sophisticated-hook-system
```

## Implementation Notes

### Symlink Verification
**Critical**: Always verify the `latest` symlink points to the newest handoff document.

```bash
# Find newest transition directory
NEWEST=$(ls -1d .claude/transitions/2025-* 2>/dev/null | sort -r | head -1)

# Update symlink (force overwrite)
ln -sf "$NEWEST/handoff.md" .claude/transitions/latest/handoff.md

# Verify it's correct
readlink -f .claude/transitions/latest/handoff.md
```

This prevents the issue where an older handoff document gets linked instead of the newest one.

### Manual Continuation Workflow
After creating handoff and verifying symlink, I will tell you:

```
✅ Handoff complete!

To continue:
1. Run /clear (the CLI command)
2. Say: "continue from .claude/transitions/latest/handoff.md"
```

**Important**: Auto-continuation is NOT supported. You must explicitly tell me to read the handoff document after `/clear`.

## Benefits

- **No Context Loss**: Smooth continuation across conversation boundaries (with manual continue step)
- **Clean Documentation**: Permanent docs stay concise and relevant
- **Efficient Startup**: Next agent gets exactly what they need
- **Progressive Learning**: Project knowledge accumulates properly
- **Symlink Convenience**: `.claude/transitions/latest/handoff.md` always points to newest handoff

---

*Part of the memory management system - ensuring continuous project understanding across sessions*