---
allowed-tools: [Task, Bash, Read, Write, MultiEdit, Grep, Glob, TodoWrite]
argument-hint: "[--task TASK-ID | --preview | --status]"
description: "Execute the next available task from the implementation plan"
@import .claude/memory/conventions.md
@import .claude/memory/lessons_learned.md
@import .claude/memory/project_state.md
---

# Task Execution

I'll execute the next available task from your implementation plan, ensuring quality and updating progress.

**Input**: $ARGUMENTS

## Implementation

```bash
#!/bin/bash

# Standard constants (must be copied to each command)
readonly CLAUDE_DIR=".claude"
readonly WORK_DIR="${CLAUDE_DIR}/work"
readonly WORK_CURRENT="${WORK_DIR}/current"

# Error handling functions (must be copied to each command)
error_exit() {
    echo "ERROR: $1" >&2
    exit 1
}

warn() {
    echo "WARNING: $1" >&2
}

debug() {
    [ "${DEBUG:-false}" = "true" ] && echo "DEBUG: $1" >&2
}

# Check required tools
require_tool() {
    local tool="$1"
    if ! command -v "$tool" >/dev/null 2>&1; then
        error_exit "$tool is required but not installed"
    fi
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

echo "🚀 Task Execution"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check for active work unit
if [ ! -f "${WORK_DIR}/ACTIVE_WORK" ]; then
    error_exit "No active work unit found. Run /explore or /work continue first."
fi

ACTIVE_WORK=$(cat "${WORK_DIR}/ACTIVE_WORK" 2>/dev/null || echo "")
if [ -z "$ACTIVE_WORK" ]; then
    error_exit "Active work unit is empty"
fi

WORK_UNIT_DIR="${WORK_CURRENT}/${ACTIVE_WORK}"
if [ ! -d "$WORK_UNIT_DIR" ]; then
    error_exit "Work unit directory not found: $WORK_UNIT_DIR"
fi

# Check for state.json
STATE_FILE="${WORK_UNIT_DIR}/state.json"
if [ ! -f "$STATE_FILE" ]; then
    error_exit "No state.json found. Run /plan first to create task breakdown."
fi

# Verify jq is available for JSON parsing
if ! command -v jq >/dev/null 2>&1; then
    warn "jq not installed - some features may be limited"
    # Fallback to basic grep/sed parsing if needed
fi

echo "📁 Active Work Unit: $ACTIVE_WORK"

# Check work unit status
if command -v jq >/dev/null 2>&1; then
    STATUS=$(jq -r '.status // "unknown"' "$STATE_FILE" 2>/dev/null || echo "unknown")
    CURRENT_TASK=$(jq -r '.current_task // null' "$STATE_FILE" 2>/dev/null || echo "null")

    if [ "$STATUS" != "planning_complete" ] && [ "$STATUS" != "implementing" ]; then
        error_exit "Work unit status is '$STATUS'. Expected 'planning_complete' or 'implementing'."
    fi

    echo "📊 Status: $STATUS"
    if [ "$CURRENT_TASK" != "null" ] && [ -n "$CURRENT_TASK" ]; then
        echo "⏳ Current Task: $CURRENT_TASK"
    fi
fi

echo ""

case "$MODE" in
    preview)
        echo "📋 Available Tasks"
        echo "──────────────────"
        if command -v jq >/dev/null 2>&1; then
            jq -r '.tasks[]? | "\(.id) - \(.title) [\(.status)]"' "$STATE_FILE" 2>/dev/null || echo "Unable to parse tasks"
        else
            echo "Install jq for better task display"
        fi
        ;;

    status)
        echo "📊 Task Progress"
        echo "────────────────"
        if command -v jq >/dev/null 2>&1; then
            TOTAL=$(jq '.tasks | length' "$STATE_FILE" 2>/dev/null || echo "0")
            COMPLETED=$(jq '[.tasks[]? | select(.status == "completed")] | length' "$STATE_FILE" 2>/dev/null || echo "0")
            IN_PROGRESS=$(jq '[.tasks[]? | select(.status == "in_progress")] | length' "$STATE_FILE" 2>/dev/null || echo "0")
            PENDING=$(jq '[.tasks[]? | select(.status == "pending")] | length' "$STATE_FILE" 2>/dev/null || echo "0")

            echo "Total Tasks: $TOTAL"
            echo "✅ Completed: $COMPLETED"
            echo "🔄 In Progress: $IN_PROGRESS"
            echo "⏳ Pending: $PENDING"

            if [ $TOTAL -gt 0 ]; then
                PERCENT=$((COMPLETED * 100 / TOTAL))
                echo ""
                echo "Progress: ${PERCENT}%"
            fi
        else
            echo "Install jq for task status display"
        fi
        ;;

    execute)
        echo "🎯 Selecting next task..."
        # Task selection logic would go here
        # This is a simplified version - actual implementation would use jq to find next available task
        ;;
esac
```

## Usage

```bash
/next                    # Execute next available task
/next --preview          # Show available tasks without executing
/next --task TASK-003    # Execute specific task
/next --status           # Show current task progress
```

## Phase 1: Load Work Context and Validate State

I'll check the work environment before proceeding:

1. **Verify `.claude` directory exists** - Ensure we're in a Claude Code project
2. **Check for active work unit** - Look for `.claude/work/current/ACTIVE_WORK`
3. **Validate state file** - Ensure `state.json` exists and contains tasks
4. **Confirm readiness** - Work unit must be in `planning_complete` or `in_progress` status

If any validation fails, I'll provide clear error messages and guidance on how to proceed.

### Work Unit Context Loading
I'll load the current work context to understand the project state:

1. **Find Active Work Unit**: Look for `.claude/work/current/ACTIVE_WORK` and associated work unit directory
2. **Load Work Metadata**: Read `metadata.json` to understand work unit phase and status
3. **Validate State File**: Ensure `state.json` exists and contains valid task breakdown
4. **Check Phase Readiness**: Verify work unit is in a phase that allows task execution

### State Validation Requirements
- Work unit must be in `implementing` or `planning_complete` phase
- Valid `state.json` with task definitions and dependencies
- No corrupted metadata or state files
- Previous work should be committed to git

## Phase 2: Task Selection and Analysis

### Task Selection Strategy
I'll identify the next task to execute using this priority order:

1. **Resume In-Progress Task**: If a task is currently marked as `in_progress`
2. **High-Priority Available Tasks**: Tasks with all dependencies satisfied, ordered by priority
3. **Critical Path Tasks**: Tasks that unblock the most other work
4. **Parallel Opportunities**: Independent tasks that can be done concurrently

### Task Information Analysis
For the selected task, I'll analyze:

- **Task Type**: feature, bug, refactor, test, or documentation
- **Dependencies**: Verify all prerequisite tasks are completed
- **Acceptance Criteria**: Understand what constitutes task completion
- **Integration Points**: Identify how this task connects to other work
- **Estimated Effort**: Review time estimates and complexity assessment

### Task Display Format
```
## Selected Task: TASK-XXX

**Title**: [Descriptive task title]
**Type**: feature|bug|refactor|test|docs
**Description**: [What needs to be accomplished]
**Dependencies**: [List of completed prerequisite tasks]
**Estimated Time**: X hours
**Priority**: High|Medium|Low

### Acceptance Criteria
- [ ] [Specific criterion 1]
- [ ] [Specific criterion 2]
- [ ] [Specific criterion 3]
```

## Phase 3: Pre-Execution Validation

### Environment Readiness Checks
Before starting task execution:

1. **Dependency Verification**: Confirm all dependent tasks are truly complete
2. **Git Status Check**: Ensure working directory is clean or changes are committed
3. **Tool Availability**: Verify required development tools are available
4. **Context Preparation**: Load necessary project context and documentation

### Quality Gate: Pre-Start
- ✅ All task dependencies satisfied
- ✅ Development environment ready
- ✅ Previous work properly committed
- ✅ Clean working directory state
- ✅ Required tools accessible

## Phase 4: Task Execution

### Execution Strategy by Task Type

#### Feature Development Tasks
1. **Test-Driven Development**: Write failing tests first that define the feature
2. **Minimal Implementation**: Implement just enough to make tests pass
3. **Refactoring**: Improve code quality while keeping tests green
4. **Integration**: Ensure feature integrates properly with existing code
5. **Documentation**: Update relevant documentation and examples

#### Bug Fix Tasks
1. **Issue Reproduction**: Create reliable reproduction steps for the bug
2. **Test Creation**: Write tests that fail due to the bug
3. **Root Cause Analysis**: Identify the underlying cause of the issue
4. **Fix Implementation**: Apply minimal fix that resolves the root cause
5. **Regression Prevention**: Ensure fix doesn't break other functionality

#### Refactoring Tasks
1. **Test Coverage Verification**: Ensure adequate tests exist before refactoring
2. **Incremental Changes**: Make small, safe changes while maintaining functionality
3. **Test Validation**: Run tests frequently to catch any breaking changes
4. **Quality Improvement**: Improve code clarity, performance, or maintainability
5. **Documentation Updates**: Update any documentation affected by changes

#### Testing Tasks
For comprehensive test creation, leverage test-engineer agent:

**Agent Invocation Parameters**:
- **subagent_type**: test-engineer
- **description**: Create comprehensive test suite for [component]
- **prompt**: Develop thorough testing including:
  - Unit tests with edge cases and boundary conditions
  - Integration tests for component interactions
  - Test data fixtures and mock setups
  - Performance benchmarks where applicable
  - Coverage analysis and gap identification

#### Documentation Tasks
1. **Content Analysis**: Review what documentation needs creation or updates
2. **Accuracy Verification**: Ensure documentation matches current implementation
3. **Example Creation**: Develop practical usage examples and tutorials
4. **Integration Updates**: Update README, API docs, and setup instructions
5. **Quality Review**: Verify documentation is clear and helpful

## Phase 5: Continuous Quality Validation

### During Execution
Throughout task execution, maintain quality through:

- **API Verification First**: Use Serena to verify APIs BEFORE writing code
  - `get_symbols_overview()` to understand available methods
  - `find_symbol()` to get exact signatures
  - Never call methods you haven't verified exist
- **Frequent Testing**: Run relevant test suites after each significant change
- **Code Quality Checks**: Ensure linting and formatting standards are maintained
- **Type Safety**: Verify type annotations and type checking (where applicable)
- **Security Scanning**: Check for potential security vulnerabilities
- **Performance Monitoring**: Ensure changes don't negatively impact performance

### Enhanced Validation (with MCP Tools)

#### Sequential Thinking Validation
When complex reasoning is needed, use structured analysis to:
- Systematically verify each acceptance criterion
- Analyze potential edge cases and failure modes
- Evaluate integration points and dependencies
- Plan testing strategies for complex functionality

#### Semantic Code Analysis (with Serena MCP)
When Serena is available, enhance validation with:
- Symbol-level impact analysis to understand affected code
- Dependency tracking to identify integration risks
- Type flow analysis to catch type-related issues
- API surface validation for public interface changes

## Phase 6: Post-Execution Validation and State Updates

### Quality Gate: Post-Execution
- ✅ All acceptance criteria met and verified
- ✅ Test suite passes completely
- ✅ Code quality checks pass (linting, formatting, types)
- ✅ Documentation updated appropriately
- ✅ Changes committed with descriptive messages
- ✅ Integration verified with existing codebase

### State Management Updates
After successful task completion:

1. **Update Task Status**: Mark task as completed in `state.json`
2. **Record Completion Time**: Log actual time spent vs. estimate
3. **Document Deliverables**: Record files changed and output produced
4. **Update Dependencies**: Mark any newly available tasks
5. **Archive Task Summary**: Create completion summary in work unit

### Progress Tracking
Using TodoWrite tool to maintain visible progress:
- Mark current task as completed
- Update overall work unit progress percentage
- Identify next available tasks
- Show critical path status

## Phase 7: Automated Git Integration

### Commit Strategy
For each completed task:

1. **Stage Relevant Changes**: Add files modified during task execution
2. **Generate Commit Message**: Create descriptive conventional commit message
3. **Include Task Reference**: Link commit to specific task ID
4. **Quality Attribution**: Include Claude Code attribution in commit
5. **Verify Commit**: Ensure commit succeeds and meets quality standards

### Commit Message Format
```
feat: Complete TASK-XXX - [Task Title]

Acceptance criteria met:
- [Criterion 1] ✅
- [Criterion 2] ✅
- [Criterion 3] ✅

Files modified: [list of key files]
Tests: [new tests or test status]

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Phase 8: Work Unit Health and Next Steps

### Health Monitoring
After each task completion:

1. **Work Unit Integrity**: Validate work unit structure and metadata
2. **State Consistency**: Ensure task states and dependencies are logical
3. **Progress Accuracy**: Verify progress calculations reflect reality
4. **Context Health**: Check session memory and import links

### Next Action Recommendations
Based on completion, provide clear guidance:

#### More Tasks Available
```
🎯 NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Task TASK-XXX completed successfully
📊 Progress: X/Y tasks complete (Z%)
→ Run `/next` again to continue with next task
→ Next available: [TASK-YYY - Description]
```

#### All Tasks Complete
```
🎉 WORK UNIT COMPLETED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ All tasks completed successfully!
📊 Final progress: Y/Y tasks complete (100%)
→ Run `/ship` to finalize and deliver work
→ Consider running `/review` for final quality check
```

#### Blocked Tasks Detected
```
⚠️ ATTENTION NEEDED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Task TASK-XXX completed
⚠️ Remaining tasks are blocked by: [dependency/issue]
→ Resolve blocker: [specific action needed]
→ Then run `/next` to continue
```

## Command Options

### Preview Mode (`--preview`)
Shows available tasks and their status without executing:
- List all tasks with current status
- Show dependency relationships
- Estimate remaining effort
- Identify any blockers

### Specific Task (`--task TASK-ID`)
Execute a specific task if dependencies are satisfied:
- Validate task exists and is available
- Check all prerequisites are met
- Execute specified task directly
- Useful for parallel development

### Status Check (`--status`)
Display current progress and work unit health:
- Show overall progress percentage
- List recent completions
- Identify current task in progress
- Display next available tasks

## Success Indicators

Task execution is successful when:
- ✅ Task selected based on dependencies and priority
- ✅ All acceptance criteria met and verified
- ✅ Quality gates passed (tests, linting, documentation)
- ✅ Changes automatically committed with proper attribution
- ✅ Work unit state accurately updated
- ✅ Progress tracking maintained
- ✅ Clear next steps provided

## Error Handling

When task execution encounters issues:

1. **Document the Problem**: Capture error details and context
2. **Preserve Progress**: Save any partially completed work
3. **Mark Task Appropriately**: Set status to blocked or in-progress as appropriate
4. **Identify Resolution Path**: Suggest specific steps to resolve the issue
5. **Update State Safely**: Ensure work unit remains in valid state

## Integration Benefits

- **MCP Enhancement**: Leverages Sequential Thinking and Serena for complex tasks
- **Quality Automation**: Automated testing, linting, and formatting checks
- **Progress Transparency**: Clear visibility into work completion and next steps
- **Git Integration**: Seamless version control with meaningful commit history
- **Context Preservation**: Maintains work unit context across task executions

---

*Systematic task execution maintaining quality standards and clear progress tracking throughout implementation workflows.*