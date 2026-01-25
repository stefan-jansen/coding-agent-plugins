---
name: work-capture
description: Capture a plan from ~/.claude/plans/ into the active work unit. Use after plan mode completes, or when user says "capture plan" or "import plan".
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Capture Plan into Work Unit

Import a plan from Claude's plan storage into a project work unit for tracked execution.

## Trigger Phrases
- "capture the plan"
- "import the plan"
- "save plan to work unit"
- after plan mode: "now let's track this"

## Process

### 1. Find Latest Plan
```bash
ls -t ~/.claude/plans/*.md | head -1
```
Get the most recently modified plan file.

### 2. Verify Active Work Unit
Check `.claude/work/ACTIVE_WORK` exists and has status "planning".

If no active work unit:
- Ask user for topic
- Create new work unit with provided topic

### 3. Copy Plan Content
Read the plan file and write to:
```
.claude/work/{id}/plan.md
```

### 4. Parse Plan for Tasks
Extract task structure from plan:
- Look for numbered lists, headings like "## Phase 1", "### Step 1"
- Each major item becomes a task
- Preserve hierarchy as dependencies

### 5. Generate state.json
```json
{
  "status": "planned",
  "current_task": null,
  "tasks": [
    {
      "id": "TASK-001",
      "title": "Task from plan",
      "status": "pending",
      "dependencies": [],
      "source_section": "## Phase 1"
    }
  ],
  "next_available": ["TASK-001"]
}
```

### 6. Update Metadata
Update `metadata.json`:
```json
{
  "status": "planned",
  "plan_captured_at": "2026-01-25T11:00:00Z",
  "plan_source": "~/.claude/plans/abstract-twilight.md",
  "task_count": 5
}
```

### 7. Confirm to User
```
✅ Plan captured to: .claude/work/2026-01-25_01_feature/

Plan: abstract-twilight.md
Tasks identified: 5
Status: planned

Run /next to begin implementation
```

## Task Extraction Heuristics

**From numbered lists**:
```markdown
1. Set up database schema → TASK-001
2. Create API endpoints  → TASK-002
3. Build frontend forms  → TASK-003
```

**From headings**:
```markdown
## Phase 1: Foundation    → TASK-001
## Phase 2: Core Logic    → TASK-002
## Phase 3: Integration   → TASK-003
```

**From task markers**:
```markdown
- [ ] Implement auth     → TASK-001
- [ ] Add validation     → TASK-002
```

## Error Handling

**No plans found**:
```
No plans found in ~/.claude/plans/
Run /plan or use plan mode first to create a plan.
```

**No active work unit**:
```
No active work unit found.
Create one with: /work new [topic]
Or provide a topic and I'll create one now.
```

## Integration

- Works with `work-new` skill for full workflow
- Generates state.json compatible with `/next`
- Updates metadata for `/work` listing
- Enables `/ship` completion tracking
