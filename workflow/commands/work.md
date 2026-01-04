---
allowed-tools: [Read, Write, MultiEdit, Bash, Grep]
argument-hint: "[continue|checkpoint|switch] [args] OR [active|paused|completed|all]"
description: "Work unit management: list, continue, checkpoint, switch"
---

# Work Management

Manage work units: list status, continue work, save checkpoints, switch contexts.

**Input**: $ARGUMENTS

## Commands

| Command | Description |
|---------|-------------|
| `/work` | List all work units |
| `/work active` | List only active units |
| `/work continue` | Resume last active unit |
| `/work continue ID` | Resume specific unit |
| `/work checkpoint` | Save current progress |
| `/work checkpoint "msg"` | Save with message |
| `/work switch ID` | Switch to different unit |

## List Display

```
📋 WORK UNITS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🟢 2025-01-01_01_auth    [implementing]  3/5 tasks (60%)
⏸️  2025-01-01_02_api     [paused]        1/4 tasks (25%)
✅ 2024-12-31_01_setup   [completed]     4/4 tasks (100%)
```

## Operations

### Continue
1. Find target unit (last active or specified ID)
2. Load metadata and state from `.claude/work/{id}/`
3. Set as ACTIVE_WORK
4. Display current task and next steps

### Checkpoint
1. Verify active work unit exists
2. Create checkpoint in `{work_unit}/checkpoints/`
3. Record timestamp, message, and current state

### Switch
1. Auto-checkpoint current work (if any)
2. Validate target work unit exists
3. Set new unit as ACTIVE_WORK
4. Load new context

## Work Unit Location

```
.claude/work/
├── ACTIVE_WORK              # Current unit ID
├── 2025-01-01_01_topic/
│   ├── metadata.json        # Status, timestamps
│   ├── requirements.md
│   ├── state.json           # Task tracking
│   └── checkpoints/
└── 2025-01-01_02_other/
```

## Integration

- `/explore` creates new work units
- `/plan` generates state.json
- `/next` executes tasks
- `/ship` completes and archives
