---
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, EnterPlanMode]
argument-hint: "[new|capture|continue|checkpoint|switch] [args]"
description: "Work unit management: create with plan mode, capture plans, list, continue"
---

# Work Management

Manage work units with integrated plan mode support.

**Input**: $ARGUMENTS

## Commands

| Command | Description |
|---------|-------------|
| `/work` | List all work units |
| `/work new [topic]` | Create work unit and enter plan mode |
| `/work capture [topic]` | Capture latest plan into new/active work unit |
| `/work from-plan [file]` | Import specific plan file |
| `/work continue [ID]` | Resume work unit |
| `/work checkpoint [msg]` | Save progress |
| `/work switch ID` | Switch active unit |

## New Work Unit with Plan Mode

`/work new [topic]`

1. **Generate Work Unit ID**
   - Format: `YYYY-MM-DD_NN_topic`
   - Sanitize topic to slug (lowercase, hyphens)

2. **Create Directory Structure**
   ```
   .claude/work/YYYY-MM-DD_NN_topic/
   ├── metadata.json   # status: "planning"
   └── (plan.md will be added after planning)
   ```

3. **Set as ACTIVE_WORK**

4. **Enter Plan Mode**
   - Use EnterPlanMode tool
   - User approves plan mode entry
   - Plan mode does exploration and planning
   - User approves plan via ExitPlanMode

5. **After Plan Mode**
   - Run `/work capture` to import the plan
   - Or: auto-capture hook handles it (if enabled)

## Capture Plan

`/work capture [topic]`

1. **Find Latest Plan**
   - Check `~/.claude/plans/` for most recent .md file
   - Sort by modification time

2. **Create/Use Work Unit**
   - If topic provided: create new work unit
   - If no topic: use ACTIVE_WORK (must have status "planning")

3. **Import Plan**
   - Copy plan content to `{work_unit}/plan.md`
   - Parse plan structure for tasks

4. **Generate state.json**
   - Extract tasks from plan headings/structure
   - Create task entries with pending status
   - Update metadata status to "planned"

5. **Confirm**
   ```
   ✅ Plan captured to: .claude/work/2025-01-25_01_feature/
   Tasks identified: 5
   Run /next to begin implementation
   ```

## Import Specific Plan

`/work from-plan [file-or-name]`

- If path: import that file
- If name fragment: find matching plan in ~/.claude/plans/
- Create new work unit with imported plan

## List Display

```
📋 WORK UNITS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 2025-01-25_01_feature  [planning]      awaiting plan capture
🟢 2025-01-24_01_auth     [implementing]  3/5 tasks (60%)
⏸️  2025-01-23_01_api      [paused]        1/4 tasks (25%)
✅ 2025-01-22_01_setup    [completed]     4/4 tasks (100%)
```

## Status Values

| Status | Icon | Meaning |
|--------|------|---------|
| planning | 📝 | Work unit created, awaiting plan |
| planned | 📋 | Plan captured, ready for /next |
| implementing | 🟢 | Tasks in progress |
| paused | ⏸️ | Temporarily suspended |
| completed | ✅ | All tasks done |

## Work Unit Location

```
.claude/work/
├── ACTIVE_WORK              # Current unit ID
├── 2025-01-25_01_topic/
│   ├── metadata.json        # Status, timestamps
│   ├── plan.md              # Captured plan
│   ├── state.json           # Task tracking
│   └── checkpoints/
```

## metadata.json Format

```json
{
  "id": "2025-01-25_01_feature",
  "status": "planning",
  "created_at": "2025-01-25T10:30:00Z",
  "topic": "Add user authentication",
  "plan_source": "~/.claude/plans/abstract-twilight.md"
}
```

## Integration

- `/work new` → creates unit, enters plan mode
- `/work capture` → imports plan, generates tasks
- `/next` → executes tasks
- `/ship` → completes and archives
