---
allowed-tools: [Task, Bash, Read, Write, MultiEdit, Grep, Glob, TodoWrite]
argument-hint: "[--task ID | --parallel [N|auto] | --preview | --status]"
description: "Execute next task(s) from implementation plan"
---

# Execute Next Task

Execute pending tasks from `.claude/work/ACTIVE_WORK` work unit.

**Arguments**: $ARGUMENTS

## Modes

- `--preview`: List available tasks
- `--status`: Show progress (completed/pending/blocked)
- `--task TASK-ID`: Execute specific task
- `--parallel N`: Execute N independent tasks concurrently
- `--parallel auto`: Execute all independent tasks (max 5)
- *(no args)*: Execute next pending task

## Process

1. **Load State**: Read `ACTIVE_WORK`, verify `state.json` exists with status `planning_complete` or `implementing`

2. **Find Tasks**: Query state.json for pending tasks with satisfied dependencies

3. **Execute**:
   - Single task: Work directly on the task
   - Parallel: Launch Task agents concurrently (single message with multiple Task tool calls)

4. **Validate**: Run tests, verify acceptance criteria met

5. **Update State**: Mark task completed in state.json, update `current_task`

6. **Commit**: Create atomic commit with task ID and description

## Parallel Execution

For `--parallel`, find independent tasks (no unmet dependencies), launch as concurrent Task agents:
- Each agent gets: task ID, title, description, acceptance criteria
- Collect results, update state for each
- Handle partial failures gracefully (some succeed, some fail)

## State File Format

```json
{
  "status": "implementing",
  "current_task": "TASK-003",
  "tasks": [
    {"id": "TASK-001", "title": "...", "status": "completed", "dependencies": []},
    {"id": "TASK-002", "title": "...", "status": "pending", "dependencies": ["TASK-001"]}
  ]
}
```

## Error Handling

- No active work unit → "Run /explore first"
- No state.json → "Run /plan first"
- All tasks blocked → Show blocked reasons
- Partial parallel failure → Complete successful tasks, report failures
