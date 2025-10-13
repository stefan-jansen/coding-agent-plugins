# Claude Code Workflow Plugin

**Version**: 1.0.0
**Category**: Workflow
**Author**: Claude Code Framework

## Overview

The Workflow Plugin provides a structured four-phase development cycle: **Explore → Plan → Implement → Deliver**. This systematic approach ensures thorough understanding, careful planning, tracked execution, and validated delivery.

## The Four-Phase Workflow

```
┌─────────┐     ┌──────┐     ┌──────┐     ┌──────┐
│ EXPLORE │ --> │ PLAN │ --> │ NEXT │ --> │ SHIP │
└─────────┘     └──────┘     └──────┘     └──────┘
Understand      Design       Execute      Deliver
```

## Commands

### `/explore [source]`
Explore requirements and codebase with systematic analysis before planning.

**Purpose**: Understand problem space, gather context, identify constraints

**Sources**:
- `@file`: Explore from requirements document
- `#issue`: Explore from GitHub issue
- `description`: Explore from natural language description
- `empty`: Interactive exploration through questions

**Usage**:
```bash
/explore @requirements.md                    # From document
/explore #123                                # From issue
/explore "Add user authentication system"    # From description
/explore                                     # Interactive mode
```

**Outputs**:
- `exploration.md`: Comprehensive analysis
- Domain understanding
- Technical constraints
- Risk assessment
- Initial approach options

**MCP Enhancements**:
- **Sequential Thinking**: Structured multi-step analysis
- **Serena**: Semantic code understanding for codebase exploration
- **Firecrawl**: Web research for external context

---

### `/plan [options]`
Create detailed implementation plan with ordered tasks and dependencies.

**Purpose**: Break down work into manageable, ordered tasks with clear success criteria

**Options**:
- `--from-requirements`: Plan from requirements document
- `--from-issue #123`: Plan from GitHub issue
- `description`: Plan from description

**Usage**:
```bash
/plan                                        # From exploration
/plan --from-requirements @requirements.md   # Skip exploration
/plan --from-issue #456                      # From GitHub issue
/plan "Refactor authentication module"       # Direct planning
```

**Outputs**:
- `implementation-plan.md`: Detailed task breakdown
- `state.json`: Task tracking state
- Ordered tasks with dependencies
- Estimated effort per task
- Validation gates between phases

**MCP Enhancements**:
- **Sequential Thinking**: Complex planning with dependencies
- **Serena**: Code analysis for technical planning

---

### `/next [options]`
Execute next available task from implementation plan.

**Purpose**: Systematic task execution with progress tracking

**Options**:
- `--task TASK-ID`: Execute specific task
- `--batch BATCH-ID`: Execute batch of parallel tasks
- `--preview`: Preview next task without executing
- `--status`: Show current progress

**Usage**:
```bash
/next                                        # Execute next task
/next --task TASK-105                        # Specific task
/next --preview                              # Preview only
/next --status                               # Show progress
```

**Behavior**:
- Loads active work unit state
- Identifies next available task
- Executes task with progress tracking
- Updates state.json automatically
- Creates task completion summary
- Prompts for validation at phase boundaries

**MCP Enhancements**:
- **Sequential Thinking**: Complex task reasoning
- **Serena**: Semantic code operations (70-90% token reduction)

---

### `/ship [options]`
Deliver completed work with validation and comprehensive documentation.

**Purpose**: Validate, document, and deliver completed work professionally

**Options**:
- `--preview`: Preview delivery without executing
- `--pr`: Create pull request
- `--commit`: Create commit only (no PR)
- `--deploy`: Deploy after delivery

**Usage**:
```bash
/ship                                        # Full delivery workflow
/ship --preview                              # Preview without delivery
/ship --pr                                   # Create pull request
/ship --commit                               # Commit only
```

**Delivery Phases**:

1. **Work Completion Verification**: Ensure all tasks complete
2. **Quality Validation**: Run tests, lint, type checking
3. **Documentation Generation**: Create comprehensive docs
4. **Git Operations**: Commit with proper attribution
5. **Memory Reflection**: Capture learnings (NEW in v1.0.0)
6. **Pull Request Creation**: Generate PR with detailed description
7. **Work Unit Archival**: Clean up and archive
8. **Success Communication**: Report delivery status

**Memory Reflection**: Automated analysis of work unit to extract:
- **Decisions**: Architectural choices and rationale
- **Lessons Learned**: What worked, what didn't
- **Conventions**: Standards established
- **Dependencies**: Tools and versions
- **Project State**: Architecture updates

**MCP Enhancements**:
- **Sequential Thinking**: Comprehensive validation reasoning
- **Serena**: Code analysis for quality checks

## Workflow Integration

### Memory System Integration

The workflow plugin automatically loads memory context:

**Auto-loaded Memory Files**:
- `decisions.md`: Architectural decisions
- `lessons_learned.md`: Project learnings
- `project_state.md`: Current system state
- `conventions.md`: Code standards
- `dependencies.md`: External dependencies

**Memory Updates**: `/ship` prompts to update memory with new learnings captured during work unit.

### Work Unit Management

**Work Unit Structure**:
```
.claude/work/current/[work-unit-id]/
├── metadata.json              # Work unit metadata
├── state.json                 # Task tracking state
├── exploration.md             # From /explore
├── implementation-plan.md     # From /plan
├── [task_summaries]/          # From /next
└── COMPLETION_SUMMARY.md      # From /ship
```

**State Tracking**: All workflow commands update `state.json` automatically for progress tracking.

## Best Practices

### Exploration Phase
- ✅ Always run `/explore` for non-trivial tasks
- ✅ Review exploration before planning
- ✅ Ask clarifying questions when uncertain
- ✅ Document constraints discovered
- ❌ Don't skip exploration for complex work
- ❌ Don't assume you understand requirements

### Planning Phase
- ✅ Break work into small, testable tasks
- ✅ Identify dependencies explicitly
- ✅ Set clear success criteria
- ✅ Include validation gates
- ❌ Don't create monolithic tasks
- ❌ Don't plan implementation details upfront

### Execution Phase
- ✅ Execute one task at a time (unless parallel)
- ✅ Create completion summaries per task
- ✅ Run validation at phase boundaries
- ✅ Adapt plan based on discoveries
- ❌ Don't skip tasks without updating plan
- ❌ Don't accumulate many changes without commits

### Delivery Phase
- ✅ Run full validation before delivery
- ✅ Create comprehensive documentation
- ✅ Update memory with learnings
- ✅ Write clear commit messages
- ❌ Don't skip quality checks
- ❌ Don't forget to capture learnings

## Configuration

### Plugin Settings

```json
{
  "settings": {
    "defaultEnabled": true,
    "category": "workflow"
  }
}
```

### Dependencies

```json
{
  "dependencies": {
    "claude-code-core": "^1.0.0",
    "claude-code-memory": "^1.0.0"
  }
}
```

**Required Plugins**:
- `core`: Work management, status, handoff
- `memory`: Context persistence and reflection

### MCP Tools

**Optional** (with graceful degradation):
- `sequential-thinking`: Enhanced reasoning for exploration and planning
- `serena`: Semantic code understanding for implementation
- `firecrawl`: Web research for external context

## Workflow Examples

### Example 1: Feature Development

```bash
# Phase 1: Explore
/explore "Add OAuth2 authentication support"
# Review exploration.md, ask questions

# Phase 2: Plan
/plan
# Review implementation-plan.md, adjust if needed

# Phase 3: Execute
/next                    # Task 1: Research OAuth2 libraries
/next                    # Task 2: Design auth flow
/next                    # Task 3: Implement authentication
/next                    # Task 4: Add tests
# Validation gate: Test coverage >80%

/next                    # Task 5: Integration testing
/next                    # Task 6: Documentation

# Phase 4: Deliver
/ship --pr              # Create pull request with full docs
```

### Example 2: Bug Fix

```bash
# Phase 1: Explore
/explore #789           # From GitHub issue
# Understand bug, identify root cause

# Phase 2: Plan
/plan --from-issue #789
# Break down fix into tasks

# Phase 3: Execute
/next                   # Task 1: Add failing test
/next                   # Task 2: Fix bug
/next                   # Task 3: Verify fix

# Phase 4: Deliver
/ship --commit          # Commit fix (no PR needed)
```

### Example 3: Refactoring

```bash
# Phase 1: Explore
/explore @refactoring-proposal.md
# Understand scope and risks

# Phase 2: Plan
/plan
# Identify safe refactoring steps

# Phase 3: Execute (with parallel tasks)
/next --task TASK-101   # Refactor module A
/next --task TASK-102   # Refactor module B (parallel)
/next                   # Integration after parallel work
/next                   # Update tests

# Phase 4: Deliver
/ship --preview         # Preview first
/ship --pr              # Create PR after preview
```

## Advanced Features

### Parallel Task Execution

When tasks are independent, `/next` can execute them in parallel:

```bash
# Plan creates parallel tasks
# Batch 1.1: TASK-101, TASK-102 (parallel)
# Batch 1.2: TASK-103 (depends on 1.1)

/next --task TASK-101 /next --task TASK-102   # Execute in parallel
/next                                          # Execute TASK-103 after
```

### Adaptive Planning

Plans can be adapted during execution:

```bash
/next                   # Discover new constraint during task
# Update implementation-plan.md
/next                   # Continue with updated plan
```

### Validation Gates

Validation gates ensure quality between phases:

```bash
/next                   # Complete batch
# Validation gate: Run tests
# If validation fails, fix issues before continuing
/next                   # Continue after validation passes
```

### Work Unit Switching

Support for parallel work streams:

```bash
/work switch 002        # Switch to different work unit
/next                   # Execute task in unit 002
/work switch 001        # Switch back to unit 001
/next                   # Continue unit 001
```

## Troubleshooting

### Exploration Not Found

**Symptom**: `/plan` shows "No exploration found"

**Solution**: Run `/explore` first or use `--from-requirements`:
```bash
/explore                                     # Create exploration
/plan                                        # Now works
# OR
/plan --from-requirements @requirements.md   # Skip exploration
```

### Task State Corruption

**Symptom**: `/next` shows incorrect next task

**Solution**: Review `state.json` and fix manually:
```bash
cat .claude/work/current/*/state.json       # Review state
# Edit state.json to fix
/next --status                              # Verify fix
```

### Memory Not Loading

**Symptom**: `/ship` doesn't show memory integration

**Solution**: Verify memory plugin enabled:
```bash
/config plugin status claude-code-memory
/config plugin enable claude-code-memory    # If disabled
```

### Ship Validation Fails

**Symptom**: `/ship` stops at validation phase

**Solution**: Fix validation issues first:
```bash
/ship --preview                             # See what will be validated
# Fix issues (tests, lint, etc.)
/ship                                       # Retry after fixes
```

## Performance

### Token Efficiency

- **With Serena**: 70-90% token reduction for code operations
- **With Sequential Thinking**: +15-30% tokens, +20-30% quality
- **Without MCP**: Standard performance, all features work

### Recommended Limits

- **Tasks per phase**: 5-10 tasks (break into smaller phases if more)
- **Task size**: 1-4 hours each (split larger tasks)
- **Work unit duration**: 1-2 weeks (create new unit for longer work)

## Version History

### 1.0.0 (2025-10-11)
- Initial plugin release
- Four-phase workflow (explore, plan, next, ship)
- Memory system integration
- Work unit management
- Memory reflection in ship command
- Parallel task execution
- Validation gates

## License

MIT License - See project LICENSE file

## Related Plugins

- **core**: Required dependency for work and status
- **memory**: Required dependency for context persistence
- **development**: Integrates with /test, /fix, /review
- **git**: Integrates with /ship for commits and PRs

---

**Note**: This plugin implements the recommended development workflow. For ad-hoc tasks, individual commands from other plugins can be used directly.
