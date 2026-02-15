---
name: plan-start
description: This skill should be used when the user asks to "let's plan", "help me plan", "plan this feature", "plan out", "start planning", or when needing to create a tracked work unit and enter plan mode for systematic planning BEFORE coding begins. Do NOT use when user just wants to execute, not plan.
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, EnterPlanMode]
---

# Start Planning

Create a tracked work unit and enter plan mode for implementation planning.

## Trigger Phrases
- "let's plan [feature]"
- "start planning [task]"
- "plan out [feature]"
- "I want to implement [feature]"

## Process

### 1. Create Work Unit
Generate ID: `YYYY-MM-DD_NN_topic`

```
.claude/work/YYYY-MM-DD_NN_topic/
└── metadata.json  {"status": "planning", "topic": "..."}
```

### 2. Set Active
Write ID to `.claude/work/ACTIVE_WORK`

### 3. Enter Plan Mode
Use EnterPlanMode - Claude will:
- Explore codebase thoroughly
- Analyze requirements
- Propose implementation plan
- Present for approval

### 4. After Approval
Tell user:
```
Work unit: .claude/work/2026-01-25_01_feature/

Say "capture the plan" to import and generate tasks.
Then /next to execute.
```

## Why This Skill

Plan mode stores plans in `~/.claude/plans/` with random names (e.g., "abstract-twilight.md").
This creates project-local tracking so plans persist with meaningful names.

## Flow

```
"Let's plan adding OAuth" → plan-start triggers
  → Creates work unit
  → Enters plan mode
  → (exploration and planning)
  → User approves

"Capture the plan" → plan-capture triggers
  → Imports plan.md
  → Generates state.json

/next → executes tasks
/ship → completes work
```
