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
**Location**: `.workspace/transitions/YYYY-MM-DD/HHMMSS.md` (UTC timestamps) — shared with Codex.

Contains:
- **Current Work Context**: What was being worked on, why, and current state
- **Recent Decisions**: Important choices made this session (not yet in permanent docs)
- **Active Challenges**: Current blockers, open questions, debugging context
- **Next Steps**: Specific, actionable tasks ready for immediate execution
- **Session-Specific State**: File changes, test results, temporary findings

### Memory Updates (if needed)
Updates `.workspace/memory/` files with durable knowledge:
- **project_state.md**: Architecture changes, new components
- **conventions.md**: Discovered patterns, coding standards
- **decisions.md**: Load-bearing choices and rationale

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

### Step 1: Verify Working Directory (CRITICAL)

```bash
# ALWAYS check PWD first
pwd

# Verify .workspace/ exists
if [ ! -d .agents ]; then
    echo "ERROR: No .workspace/ directory found at $(pwd)."
    echo "Run /setup:existing or /setup:transitions to scaffold .workspace/"
    exit 1
fi

TRANSITIONS_ROOT=".workspace/transitions"
```

**Stop if not in correct directory** - Do not proceed with file creation.

### Step 2: Create Transition File

```bash
# Get UTC timestamp
UTC_DATE=$(date -u +%Y-%m-%d)
UTC_TIME=$(date -u +%H%M%S)

# Create date directory
mkdir -p "$TRANSITIONS_ROOT/$UTC_DATE"

# Create transition file
TRANSITION_FILE="$TRANSITIONS_ROOT/$UTC_DATE/$UTC_TIME.md"
```

### Step 3: Write Handoff Content

1. **Identify Durable Knowledge** → Update `.workspace/memory/` files if needed
2. **Extract Session Context** → Write comprehensive transition document
3. **Include UTC Timestamp** → Header: `# Handoff: YYYY-MM-DD HH:MM:SS UTC`

### Step 3b: Keep MEMORY_INDEX.md current (if memory was touched)

If Step 3.1 wrote/edited any file under `.workspace/memory/`, refresh
the index so its `tokens` field and any new entries are picked up
before the next session loads it:

```bash
# Memory plugin's index seeder is idempotent — safe to re-run.
BIN="$HOME/agents/coding/plugins/memory/bin"
[[ -d "$BIN" ]] && bash "$BIN/memory_init_index.sh" --quiet
```

This keeps `MEMORY_INDEX.md` consistent with the files on disk so the
SessionStart nudge, `/memory-review`, and `/memory-gc` all see the
updated state at the next session. Skip the call if Step 3.1 didn't
touch memory.

### Step 4: Inform User

**IMPORTANT**: After I complete the handoff document, you must manually continue:

1. Run `/clear` (the CLI command, not a slash command)
2. Use `/transition:continue` OR say: "continue from .workspace/transitions/YYYY-MM-DD/HHMMSS.md"

**Note**: Claude Code may ignore the continue command and check running processes first (internal command structure behavior). If this happens, run the command again or provide the explicit transition file path.

## User Continuation Steps

After I create the handoff document:

**Step 1**: Run `/clear` to reset conversation context
```bash
/clear
```

**Step 2**: Resume work using ONE of these methods:
```
# Option 1: Use the continue command (searches for latest transition)
/transition:continue

# Option 2: Provide explicit file path (more reliable)
continue from .workspace/transitions/YYYY-MM-DD/HHMMSS.md
```

⚠️ **Note**: `/transition:continue` may sometimes prioritize other activities before loading the transition. If this happens, either run it again or use Option 2 with the explicit file path.

**Recommendation**: Always copy the transition file location when it's created, so you can provide it explicitly if needed for a smooth transition.

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
# Handoff: 2026-05-08 14:32:15 UTC

## Active Work
Implementing MCP memory system with two-flow approach

## Current State
- Created /handoff and /memory-update commands
- Serena configured and working for semantic operations
- 4 MCP tools operational (Sequential Thinking, Context7, Serena, Firecrawl)

## Recent Decisions
- Use .workspace/memory/ for durable knowledge referenced by AGENTS.md
- Transition documents in .workspace/transitions/ for session handoffs
- Keep AGENTS.md deliberately concise

## Next Steps
1. Test /handoff command with real scenario
2. Configure .workspace/memory/ structure
3. Update AGENTS.md to reference memory modules

## Session Context
Working in: ~/path/to/project
Last focus: Memory system design
Open PR: feature/sophisticated-hook-system
```

## Implementation Notes

### Critical: Working Directory Verification

**BEFORE creating any files**, verify you're in a project directory with transition infrastructure:

```bash
# Step 1: Check current directory
pwd

# Step 2: Verify .workspace/ exists
if [ ! -d .agents ]; then
    echo "ERROR: Not in a project with .workspace/ infrastructure"
    echo "Current directory: $(pwd)"
    exit 1
fi

# Step 3: Proceed with handoff creation
TRANSITIONS_ROOT=".workspace/transitions"
```

**Common mistake**: Claude creates transition files in random directories when not checking PWD first. Always verify location before writing files.

### Timestamp-Based Organization

**Directory Structure** (UTC timestamps):
```bash
TRANSITIONS_ROOT=".workspace/transitions"

# Get current UTC timestamp
UTC_DATE=$(date -u +%Y-%m-%d)
UTC_TIME=$(date -u +%H%M%S)

# Create date directory if needed
mkdir -p "$TRANSITIONS_ROOT/$UTC_DATE"

# Create transition file
TRANSITION_FILE="$TRANSITIONS_ROOT/$UTC_DATE/$UTC_TIME.md"
```

**Benefits**:
- ✅ No counter management needed
- ✅ No symlink complexity or permission issues
- ✅ Naturally chronological (sort by filename)
- ✅ Easy time-based queries ("5 hours ago")
- ✅ Date-based archiving (delete old date directories)
- ✅ No timezone confusion (always UTC)

### Finding Latest Transition

**Dynamic lookup** (no symlink needed):

```bash
TRANSITIONS_ROOT=".workspace/transitions"

# Find most recent date directory
LATEST_DATE=$(ls -1 "$TRANSITIONS_ROOT/" | grep -E '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' | sort -r | head -1)

# Find most recent timestamp in that directory
LATEST_TIME=$(ls -1 "$TRANSITIONS_ROOT/$LATEST_DATE/" | grep -E '^[0-9]{6}\.md$' | sort -r | head -1)

# Full path to most recent transition
LATEST_TRANSITION="$TRANSITIONS_ROOT/$LATEST_DATE/$LATEST_TIME"
```

**Why no symlink**:
- Avoids permission issues with symlink creation
- Reduces token usage (no symlink verification needed)
- Two simple `ls | tail` commands are more reliable
- Transparent and easy to understand

### Manual Continuation Workflow
After creating handoff, I will tell you:

```
✅ Handoff complete!

Location: .workspace/transitions/YYYY-MM-DD/HHMMSS.md

To continue this work:
1. Run /clear (the CLI command)
2. Use /transition:continue command OR say: "continue from .workspace/transitions/YYYY-MM-DD/HHMMSS.md"

⚠️ **Note**: /transition:continue may sometimes prioritize other activities first. If this happens, run it again or provide the explicit file path above.
```

**Important**: You must explicitly tell me to continue after `/clear`.

## Benefits

- **No Context Loss**: Smooth continuation across conversation boundaries (with manual continue step)
- **Clean Documentation**: Permanent docs stay concise and relevant
- **Efficient Startup**: Next agent gets exactly what they need
- **Progressive Learning**: Project knowledge accumulates properly
- **No Symlink Issues**: Dynamic lookup avoids permission problems
- **UTC Timestamps**: No timezone confusion, easy time-based queries
- **Date Organization**: Simple archival by date directory
- **Transparent**: Two simple `ls` commands, easy to understand and debug

## Helpful Queries

### Find Recent Transitions

```bash
# List today's transitions
ls -lh .workspace/transitions/$(date -u +%Y-%m-%d)/

# List all transitions from last 3 days
find .workspace/transitions/ -type f -name "*.md" -mtime -3

# Find transitions from specific date
ls -lh .workspace/transitions/2026-05-08/
```

### Time-Based Lookups

```bash
# Transitions from last 5 hours (approximately)
FIVE_HOURS_AGO=$(date -u -d '5 hours ago' +%Y-%m-%d)
find .workspace/transitions/$FIVE_HOURS_AGO/ -type f -name "*.md"

# Most recent 5 transitions
find .workspace/transitions/ -type f -name "*.md" | sort -r | head -5
```

### Archive Old Transitions

```bash
# Archive transitions older than 30 days
find .workspace/transitions/ -type d -name "2026-*" -mtime +30 -exec mv {} .workspace/transitions/archive/ \;

# Or delete old date directories
find .workspace/transitions/ -type d -name "2026-*" -mtime +90 -exec rm -rf {} \;
```

### Compare Transitions

```bash
# Compare two transitions
diff .workspace/transitions/2026-05-08/143022.md .workspace/transitions/2026-05-08/165530.md

# See what changed in last transition
LATEST=$(find .workspace/transitions/ -type f -name "*.md" | sort -r | head -1)
PREVIOUS=$(find .workspace/transitions/ -type f -name "*.md" | sort -r | sed -n '2p')
diff "$PREVIOUS" "$LATEST"
```

---

*Part of the memory management system - ensuring continuous project understanding across sessions*
