---
name: plan-capture
description: Capture the latest plan into a tracked work unit. Use after plan mode completes, when user says "capture the plan", "import the plan", or "save the plan".
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Capture Plan

Import the latest plan from `~/.claude/plans/` into a project work unit for tracked execution.

## Trigger Phrases
- "capture the plan"
- "import the plan"
- "save the plan"
- "track this plan"

## Process

### 1. Find Latest Plan
```bash
ls -t ~/.claude/plans/*.md | head -1
```

### 2. Check/Create Work Unit
- If active work unit with status "planning" → use it
- If no work unit → ask for topic, create one

### 3. Import Plan
Copy plan to `.claude/work/{id}/plan.md`

### 4. Generate Tasks
Extract from plan structure:
- Numbered lists → tasks
- `## Phase N` headings → tasks
- `- [ ]` checkboxes → tasks

### 5. Create state.json
```json
{
  "status": "planned",
  "tasks": [
    {"id": "TASK-001", "title": "...", "status": "pending"}
  ],
  "next_available": ["TASK-001"]
}
```

### 6. Confirm
```
✅ Plan captured: .claude/work/2026-01-25_01_feature/
Tasks: 5
Ready for /next
```

## Error Handling

**No plans**: "No plans in ~/.claude/plans/. Use plan mode first."
**No work unit**: "No active work unit. What topic is this for?"

## Integration

```
plan-start → (plan mode) → plan-capture → /next → /ship
```
