---
allowed-tools: [Task, Bash, Read, Write, Grep, MultiEdit, mcp__sequential-thinking__sequentialthinking]
argument-hint: "[--from-requirements | --from-issue #123 | description]"
description: "Create implementation plan with ordered tasks and dependencies"
---

# Implementation Planning

Create comprehensive task breakdown from requirements.

**Input**: $ARGUMENTS

## Sources

- `--from-requirements`: Use existing requirements.md
- `--from-issue #123`: Plan for GitHub issue
- `description`: Plan from provided text
- *(empty)*: Plan for active work unit

## Process

1. **Validate Context**
   - Check for active work unit in `.claude/work/ACTIVE_WORK`
   - Verify `requirements.md` exists
   - Warn if overwriting existing plan

2. **Analyze Requirements**
   - Identify core functionality
   - Map integration points
   - Define quality requirements
   - Use Sequential Thinking for complex analysis

3. **Create Task Breakdown**
   - 2-4 hours per task
   - Single responsibility per task
   - Clear acceptance criteria
   - Testable outcomes

4. **Sequence Tasks**
   - Map dependencies (no circular refs)
   - Identify parallel opportunities
   - Define critical path

5. **Generate Outputs**

## Task Sizing

| Type | Scope |
|------|-------|
| Foundation | Setup, infrastructure, core architecture |
| Feature | User-facing functionality |
| Integration | External systems, APIs |
| Testing | Test implementation |
| Documentation | Guides, API docs |

## Output Files

**state.json**:
```json
{
  "status": "planning_complete",
  "current_task": null,
  "tasks": [
    {
      "id": "TASK-001",
      "title": "Setup foundation",
      "type": "foundation",
      "status": "pending",
      "dependencies": [],
      "acceptance_criteria": ["..."],
      "estimated_hours": 3,
      "priority": "high"
    }
  ],
  "completed_tasks": [],
  "next_available": ["TASK-001"]
}
```

**implementation-plan.md**: Human-readable plan with:
- Project overview and scope
- Technical architecture
- Task execution plan
- Quality assurance strategy

## Next Steps

After planning: Run `/next` to start first task
