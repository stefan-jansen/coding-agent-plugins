---
allowed-tools: [Task, Bash, Read, Write, Grep, EnterPlanMode, mcp__sequential-thinking__sequentialthinking]
argument-hint: "[description] (or use /work new for integrated workflow)"
description: "Enter plan mode (consider /work new for tracked planning)"
---

# Planning

Enter Claude's plan mode for thorough implementation planning.

**Input**: $ARGUMENTS

## Recommended Workflow

For tracked work with automatic plan capture:
```
/work new "feature description"
```

This command (`/plan`) enters plan mode directly but doesn't create a work unit. Use `/work capture` afterward to import the plan.

## When to Use Each

| Command | Creates Work Unit | Enters Plan Mode | Auto-tracks |
|---------|-------------------|------------------|-------------|
| `/work new [topic]` | Yes | Yes | Yes |
| `/plan [description]` | No | Yes | No |
| `/work capture` | Optional | No | Imports plan |

## Direct Plan Mode

If you just want to enter plan mode without work unit tracking:

1. **Enter Plan Mode**
   - Invokes EnterPlanMode tool
   - You approve entry
   - Claude explores codebase thoroughly
   - Claude proposes implementation plan

2. **Review and Approve**
   - Plan presented for your approval
   - Modify as needed
   - Approve via ExitPlanMode

3. **Plan Storage**
   - Saved to `~/.claude/plans/[random-name].md`
   - To track: run `/work capture` after

## After Planning

- **With work unit**: Run `/next` to execute tasks
- **Without work unit**: Run `/work capture` to create tracked unit

## Legacy Support

This command still supports direct task generation:
- `--from-requirements`: Generate tasks from existing requirements.md
- `--from-issue #123`: Plan for GitHub issue
- Creates state.json in active work unit if one exists
