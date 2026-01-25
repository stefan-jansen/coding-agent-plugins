---
allowed-tools: [Read, Write, Bash, Grep, Glob]
argument-hint: "[list|continue|checkpoint|switch] [args]"
description: "List and manage work units (use work-new skill for new work)"
---

# Work Unit Management

List and manage existing work units. For creating new work units with planning, use the `work-new` skill (auto-triggers on "let's plan [topic]").

**Input**: $ARGUMENTS

## Commands

| Command | Description |
|---------|-------------|
| `/work` | List all work units |
| `/work active` | List only active/in-progress units |
| `/work continue [ID]` | Resume work unit |
| `/work checkpoint [msg]` | Save progress |
| `/work switch ID` | Switch active unit |

## Skills (Recommended)

| Skill | Trigger | Purpose |
|-------|---------|---------|
| `work-new` | "let's plan [topic]" | Create unit + enter plan mode |
| `work-capture` | "capture the plan" | Import plan into work unit |

## List Display

```
📋 WORK UNITS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 2025-01-25_01_feature  [planning]      awaiting plan capture
📋 2025-01-25_02_api      [planned]       5 tasks ready
🟢 2025-01-24_01_auth     [implementing]  3/5 tasks (60%)
⏸️  2025-01-23_01_refactor [paused]        1/4 tasks (25%)
✅ 2025-01-22_01_setup    [completed]     4/4 tasks (100%)
```

## Status Values

| Status | Icon | Meaning |
|--------|------|---------|
| planning | 📝 | Awaiting plan capture |
| planned | 📋 | Tasks ready for /next |
| implementing | 🟢 | Tasks in progress |
| paused | ⏸️ | Temporarily suspended |
| completed | ✅ | All tasks done |

## Operations

### Continue
1. Find target unit (last active or specified ID)
2. Load metadata and state
3. Set as ACTIVE_WORK
4. Display current task and next steps

### Checkpoint
1. Verify active work unit
2. Save current state to `checkpoints/`
3. Record timestamp and message

### Switch
1. Auto-checkpoint current work
2. Set new unit as ACTIVE_WORK
3. Load new context

## Work Unit Location

```
.claude/work/
├── ACTIVE_WORK           # Current unit ID
├── 2025-01-25_01_topic/
│   ├── metadata.json     # Status, timestamps
│   ├── plan.md           # Captured plan
│   ├── state.json        # Task tracking
│   └── checkpoints/
```

## Typical Workflow

```
1. "Let's plan adding OAuth"     → work-new skill triggers
2. (plan mode runs)
3. "Capture the plan"            → work-capture skill triggers
4. /next                         → Execute tasks
5. /work checkpoint "auth done"  → Save progress
6. /ship                         → Complete delivery
```
