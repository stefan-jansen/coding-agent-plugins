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
📝 2025-01-25-01-feature  [planning]      awaiting capture
📋 2025-01-25-02-api      [planned]       5 tasks
🟢 2025-01-24-01-auth     [implementing]  3/5 (60%)
✅ 2025-01-22-01-setup    [completed]     4/4
```

## Work Unit Location

```
.agents/work/
├── ACTIVE_WORK
└── YYYY-MM-DD-NN-topic/
    ├── metadata.json
    ├── plan.md
    └── state.json
```
