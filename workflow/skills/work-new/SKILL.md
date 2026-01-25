---
name: work-new
description: Create a project work unit and plan implementation. Use when starting new feature work, planning a task, or when user says "let's plan" or "new work unit".
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, EnterPlanMode]
---

# Create Work Unit with Planning

Create a project-local work unit and enter plan mode for thorough implementation planning.

## Trigger Phrases
- "let's plan [feature]"
- "start work on [feature]"
- "new work unit for [topic]"
- "I want to implement [feature]"

## Process

### 1. Generate Work Unit ID
```
Format: YYYY-MM-DD_NN_topic
Example: 2026-01-25_01_user_authentication
```
- Use current date
- Find next available counter for today
- Sanitize topic to lowercase slug with hyphens

### 2. Create Work Unit Directory
```
.claude/work/YYYY-MM-DD_NN_topic/
├── metadata.json
```

**metadata.json**:
```json
{
  "id": "2026-01-25_01_topic",
  "status": "planning",
  "created_at": "2026-01-25T10:30:00Z",
  "topic": "User provided topic description"
}
```

### 3. Set as Active Work
Write the work unit ID to `.claude/work/ACTIVE_WORK`

### 4. Enter Plan Mode
Use `EnterPlanMode` tool to begin thorough planning:
- Claude explores the codebase
- Analyzes requirements
- Proposes implementation plan
- User reviews and approves

### 5. After Plan Mode
Inform user:
```
Work unit created: .claude/work/2026-01-25_01_topic/
Status: planning

After plan approval, run: /work capture
This will import the plan and generate tasks for /next
```

## Example Flow

User: "Let's plan adding OAuth authentication"

1. Create `.claude/work/2026-01-25_01_oauth_authentication/`
2. Write metadata.json with status "planning"
3. Set as ACTIVE_WORK
4. Enter plan mode
5. (Plan mode does thorough exploration)
6. User approves plan
7. User runs `/work capture` to import

## Integration

- Creates work unit for project-local tracking
- Leverages Claude's built-in plan mode for quality planning
- Works with `/work capture` to import plans
- Works with `/next` to execute tasks
- Works with `/ship` to complete delivery
