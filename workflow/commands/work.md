---
allowed-tools: [Read, Write, Bash, Grep, Glob]
argument-hint: "[list|continue|checkpoint|switch]"
description: "List and manage work units"
---

# Work Unit Management

List and manage tracked work units.

**Input**: $ARGUMENTS

## Commands

| Command | Description |
|---------|-------------|
| `/work` | List all work units |
| `/work continue [ID]` | Resume work unit |
| `/work checkpoint [msg]` | Save progress |
| `/work switch ID` | Switch active unit |

## Recommended Flow (Skills)

```
"Let's plan [feature]"  → plan-start skill
(plan mode runs)
"Capture the plan"      → plan-capture skill
/next                   → Execute tasks
/ship                   → Complete
```

## List Display

```
📝 2025-01-25_01_feature  [planning]      awaiting capture
📋 2025-01-25_02_api      [planned]       5 tasks
🟢 2025-01-24_01_auth     [implementing]  3/5 (60%)
✅ 2025-01-22_01_setup    [completed]     4/4
```

## Work Unit Location

```
.claude/work/
├── ACTIVE_WORK
└── YYYY-MM-DD_NN_topic/
    ├── metadata.json
    ├── plan.md
    └── state.json
```
