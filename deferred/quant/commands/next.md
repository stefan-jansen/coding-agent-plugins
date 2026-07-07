---
allowed-tools: [Task, Bash, Read, Write, MultiEdit, Grep, Glob, TodoWrite]
argument-hint: "[--task TASK-ID | --preview | --status]"
description: "Execute next task with phase-appropriate quant validation"
---

# Quant Task Execution with Validation Gates

I'll execute the next task from the quant strategy implementation plan, running phase-appropriate validators at checkpoints to catch issues early.

**Input**: $ARGUMENTS

## Quant-Specific Execution Flow

Standard task execution with validation gates:

1. **Execute Task**: Implement the planned functionality
2. **API Verification** (Critical): Use Serena to verify APIs BEFORE writing code
3. **Self-Check**: Validate task acceptance criteria met
4. **Phase Validation**: Run appropriate validator based on task phase
5. **Update State**: Mark complete and progress to next task

### Validation Gate Mapping

| Phase | Validator | What It Checks |
|-------|-----------|----------------|
| data_infrastructure | quant-ml-validator | Survivorship bias, UTC handling, corporate actions |
| feature_engineering | quant-ml-validator | Look-ahead leakage, rolling windows, preprocessing |
| backtesting | quant-backtest-validator | Transaction costs, execution lag, market impact |
| model_training | quant-ml-validator | Time-series CV, multiple testing, overfitting |
| risk_management | quant-risk-validator | Position sizing, risk limits, kill switches |
| deployment | quant-risk-validator | Reproducibility, monitoring, audit trails |

## Implementation

```bash
#!/bin/bash

# Standard constants
readonly CLAUDE_DIR=".claude"
readonly WORK_DIR="${CLAUDE_DIR}/work"
readonly WORK_CURRENT="${WORK_DIR}/current"

error_exit() {
    echo "ERROR: $1" >&2
    exit 1
}

warn() {
    echo "WARNING: $1" >&2
}

# Parse arguments
MODE="execute"
TASK_ID=""

if [[ "$ARGUMENTS" == *"--preview"* ]]; then
    MODE="preview"
elif [[ "$ARGUMENTS" == *"--status"* ]]; then
    MODE="status"
elif [[ "$ARGUMENTS" =~ --task[[:space:]]+([A-Z0-9-]+) ]]; then
    TASK_ID="${BASH_REMATCH[1]}"
fi

echo "💹 Quant Task Execution with Validation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check for active work unit
if [ ! -f "${WORK_DIR}/ACTIVE_WORK" ]; then
    error_exit "No active work unit. Run /quant-explore first."
fi

ACTIVE_WORK=$(cat "${WORK_DIR}/ACTIVE_WORK" 2>/dev/null || echo "")
WORK_UNIT_DIR="${WORK_CURRENT}/${ACTIVE_WORK}"

if [ ! -d "$WORK_UNIT_DIR" ]; then
    error_exit "Work unit not found: $WORK_UNIT_DIR"
fi

# Check for state.json
STATE_FILE="${WORK_UNIT_DIR}/state.json"
if [ ! -f "$STATE_FILE" ]; then
    error_exit "No state.json found. Run /quant-plan first."
fi

echo "📁 Work Unit: $ACTIVE_WORK"

# Require jq for quant workflows (complex state management)
if ! command -v jq >/dev/null 2>&1; then
    error_exit "jq required for quant workflows. Install: sudo apt-get install jq"
fi

STATUS=$(jq -r '.status // "unknown"' "$STATE_FILE")
if [ "$STATUS" != "planning_complete" ] && [ "$STATUS" != "implementing" ]; then
    error_exit "Status is '$STATUS'. Run /quant-plan first."
fi

echo "📊 Status: $STATUS"
echo ""

case "$MODE" in
    preview)
        echo "📋 Available Tasks"
        echo "──────────────────"
        jq -r '.tasks[]? | "\(.id) - \(.title) [\(.status)] (Phase: \(.phase // "N/A"))"' "$STATE_FILE"
        ;;

    status)
        echo "📊 Task Progress"
        echo "────────────────"
        TOTAL=$(jq '.tasks | length' "$STATE_FILE")
        COMPLETED=$(jq '[.tasks[]? | select(.status == "completed")] | length' "$STATE_FILE")
        IN_PROGRESS=$(jq '[.tasks[]? | select(.status == "in_progress")] | length' "$STATE_FILE")
        PENDING=$(jq '[.tasks[]? | select(.status == "pending")] | length' "$STATE_FILE")

        echo "Total Tasks: $TOTAL"
        echo "✅ Completed: $COMPLETED"
        echo "🔄 In Progress: $IN_PROGRESS"
        echo "⏳ Pending: $PENDING"

        if [ $TOTAL -gt 0 ]; then
            PERCENT=$((COMPLETED * 100 / TOTAL))
            echo ""
            echo "Progress: ${PERCENT}%"

            # Show next validation gate
            NEXT_GATE=$(jq -r '.validation_gates[]? | select(.completed != true) | .phase' "$STATE_FILE" 2>/dev/null | head -1)
            if [ -n "$NEXT_GATE" ]; then
                echo "Next Validation Gate: $NEXT_GATE"
            fi
        fi
        ;;

    execute)
        echo "🎯 Executing next quant task with validation..."
        echo ""
        # Task selection and execution happens in Phase 2 below
        ;;
esac
```

## Phase 1: API Verification (CRITICAL)

Before implementing any task, I'll use Serena (if available) to verify that all APIs, classes, and methods exist:

### Verification Process
1. **Identify Dependencies**: What classes/functions will this task use?
2. **Serena Symbol Lookup**: `find_symbol()` to verify each dependency exists
3. **API Signature Check**: Confirm method signatures match expectations
4. **Cite Line Numbers**: Reference actual code locations (file:line)

### Hard Rule
**If Serena can't find it, it doesn't exist. Don't call methods you haven't verified.**

This prevents the common failure mode where we write code against assumed APIs that don't actually exist.

## Phase 2: Task Execution

### Task Selection Logic
1. **Resume in-progress task** if one exists
2. **Select next available task** based on dependencies
3. **Validate dependencies satisfied** before starting

### Execution Strategy by Phase

#### Data Infrastructure Tasks
**Focus**: Survivorship bias, timezone handling, corporate actions

**Validation**: After completion, run:
```
/agent quant-ml-validator "Review data pipeline in [files] for survivorship and timing issues"
```

**Common Issues**:
- Loading current universe for historical backtest
- Timezone-naive datetime objects
- Unadjusted price data

#### Feature Engineering Tasks
**Focus**: Look-ahead leakage, rolling window safety, CV setup

**Validation**: After completion, run:
```
/agent quant-ml-validator "Review feature engineering in [files] for temporal leakage"
```

**Common Issues**:
- Preprocessing fit on full dataset before split
- Center-aligned rolling windows
- Standard k-fold instead of time-series CV

#### Backtesting Infrastructure Tasks
**Focus**: Transaction costs, execution lag, market impact

**Validation**: After completion, run:
```
/agent quant-backtest-validator "Review backtest engine in [files] for execution realism"
```

**Common Issues**:
- Zero transaction costs
- Same-bar signal and execution
- Instant fills at mid-price

#### Model Training Tasks
**Focus**: Time-series CV, multiple testing, overfitting

**Validation**: After completion, run:
```
/agent quant-ml-validator "Review model training in [files] for overfitting risks"
```

**Common Issues**:
- No purging/embargo in CV
- Testing 100+ parameters without correction
- Re-using holdout set

#### Risk Management Tasks
**Focus**: Position sizing, hard limits, kill switches

**Validation**: After completion, run:
```
/agent quant-risk-validator "Review risk controls in [files] for production safety"
```

**Common Issues**:
- Fixed position sizing (no volatility scaling)
- Missing drawdown circuit breaker
- No emergency halt mechanism

#### Deployment Tasks
**Focus**: Reproducibility, monitoring, audit trails

**Validation**: After completion, run:
```
/agent quant-risk-validator "Review deployment setup for reproducibility and monitoring"
```

**Common Issues**:
- Unseeded randomness
- No config/hyperparameter logging
- Missing data lineage tracking

## Phase 3: Quality Validation

### Acceptance Criteria Verification
For each task, verify all acceptance criteria met:
- [ ] Implementation complete
- [ ] Tests passing (if applicable)
- [ ] APIs verified with Serena
- [ ] Code follows quant best practices
- [ ] No obvious data leakage or timing issues

### Validation Gate Execution
Based on task phase, run appropriate validator:

```bash
# Determine task phase
TASK_PHASE=$(jq -r '.tasks[] | select(.status == "completed") | .phase' "$STATE_FILE" | tail -1)

# Select validator
case "$TASK_PHASE" in
    data_infrastructure|feature_engineering|model_training)
        VALIDATOR="quant-ml-validator"
        ;;
    backtesting)
        VALIDATOR="quant-backtest-validator"
        ;;
    risk_management|deployment)
        VALIDATOR="quant-risk-validator"
        ;;
esac

# Run validation if at phase boundary
if [ -n "$VALIDATOR" ]; then
    echo ""
    echo "🔍 Running phase validation: $VALIDATOR"
    # Validator invocation happens here
fi
```

## Phase 4: State Updates and Progress

### Update state.json
1. Mark current task as completed
2. Record completion timestamp
3. Add any new blockers or notes
4. Update next_available tasks based on dependencies

### Progress Reporting
```
✅ TASK-003 completed: Setup PIT universe database
🔍 Validation passed: No survivorship bias detected
📊 Progress: 3/24 tasks (12%)
→ Next: TASK-004 - Implement corporate actions pipeline
```

### Validation Gate Tracking
Update validation_gates in state.json:
```json
{
  "validation_gates": [
    {
      "phase": "data_infrastructure",
      "agent": "quant-ml-validator",
      "completed": true,
      "timestamp": "2025-01-24T15:30:00Z",
      "issues_found": 0
    }
  ]
}
```

## Phase 5: Next Action Recommendation

### More Tasks Available
```
✅ Task completed successfully
🔍 Phase validation passed
→ Run `/quant-next` to continue with TASK-004
→ Next phase validation at: feature_engineering completion
```

### Phase Validation Required
```
⚠️  Phase checkpoint reached: feature_engineering
🔍 Running quant-ml-validator for feature pipeline review...
→ [Validation results]
→ Fix any issues before proceeding to next phase
```

### All Tasks Complete
```
🎉 All implementation tasks completed!
🔍 Final validation gates passed
→ Run `/quant-ship` for deployment readiness check
```

## Success Indicators

- ✅ APIs verified with Serena before coding
- ✅ Task implemented meeting acceptance criteria
- ✅ Phase-appropriate validator invoked
- ✅ Validation passed (or issues documented)
- ✅ State updated correctly
- ✅ Progress toward next task or phase
- ✅ No data leakage introduced
- ✅ Execution realism maintained

## Critical Reminders

### API Verification First
**NEVER** write code against assumed APIs. Always:
1. Use `get_symbols_overview()` to see what exists
2. Use `find_symbol()` to verify specific classes/methods
3. Cite line numbers: `ClassName` found at `file.py:123`

### Validation Not Optional
Every phase must pass validation before proceeding. This prevents:
- Data leakage accumulating through pipeline
- Unrealistic backtests giving false confidence
- Missing risk controls discovered in production

### Fail Fast
If validation finds Critical issues:
1. **STOP** - Don't continue to next task
2. **FIX** - Address the issue immediately
3. **RE-VALIDATE** - Confirm fix works
4. **THEN PROCEED** - Continue implementation

---

*Quant task execution with validation gates ensuring data integrity, execution realism, and production safety at every step*
