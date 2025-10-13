---
allowed-tools: [Read, Write, Task, Bash, Grep, Glob, mcp__sequential-thinking__sequentialthinking]
argument-hint: "[file/directory] [--spec requirements.md] [--systematic] [--semantic]"
description: Standard code review focused on bugs, design flaws, dead code, and code quality with prioritized action plan
---

# Code Review

Standard code review focused on practical code quality issues: bugs, design flaws, dead code, and maintainability. Always provides a prioritized action plan for improvements.

**Input**: $ARGUMENTS

## Usage

### Standard Code Review (Default)
```bash
/review                    # Review entire project for code quality issues
/review src/auth.py        # Review specific file
/review src/components/    # Review specific directory
```

### Requirements Validation
```bash
/review --spec design.md   # Validate code against requirements document
/review --spec @requirements.md  # Validate against specific requirements
```

### Systematic Review (Complex Projects)
```bash
/review --systematic       # Use structured reasoning for complex codebases
/review src/ --systematic  # Systematic review of specific area
```

### Semantic Review (With Serena)
```bash
/review --semantic         # Use Serena for semantic analysis (70-90% token reduction)
/review src/ --semantic    # Semantic review of specific directory
/review --semantic --spec design.md  # Combine semantic analysis with requirements
```

## What This Review Covers

### ✅ Standard Code Review Focus
1. **Bug Detection**: Logic errors, edge cases, error handling issues
2. **Design Flaws**: Code organization, coupling, cohesion problems
3. **Dead Code**: Unused functions, imports, variables, commented code
4. **Code Quality**: Readability, maintainability, consistency
5. **Performance Issues**: Obvious inefficiencies and bottlenecks
6. **Best Practices**: Language-specific patterns and conventions

### ⚠️ What's NOT Included (By Design)
- **Security Scanning**: No longer the default focus - use specialized security tools if needed
- **Infrastructure Audits**: Use `/audit` command for framework and infrastructure validation
- **Documentation Validation**: Handled by specialized documentation commands

## Phase 1: Determine Review Scope

Parse the arguments to determine what to review and which mode to use:

- **Target**: `$ARGUMENTS` (file or directory to review)
- **--spec [file]**: Validate against requirements document
- **--systematic**: Use structured reasoning for complex analysis

If reviewing a large codebase (>30 files), consider using semantic analysis tools if available (like Serena MCP) for more efficient symbol analysis and dependency tracking.

## Phase 2: Requirements Validation (If Specified)

```bash
if [ -n "$REQUIREMENTS_FILE" ]; then
    echo "📖 Loading requirements specification..."

    # Handle @file syntax
    SPEC_FILE="$REQUIREMENTS_FILE"
    if [[ "$REQUIREMENTS_FILE" == @* ]]; then
        SPEC_FILE="${REQUIREMENTS_FILE#@}"
    fi

    if [ ! -f "$SPEC_FILE" ]; then
        echo "❌ Requirements file not found: $SPEC_FILE"
        echo "Please ensure the specification file exists."
        exit 1
    fi

    echo "✅ Requirements loaded from: $SPEC_FILE"
    echo ""
fi
```

## Phase 3: Execute Code Review

Perform the code review using appropriate methods:

**If semantic analysis tools are available** (e.g., Serena MCP):
- Use symbol-aware analysis for dead code detection
- Trace function dependencies and call graphs
- Identify circular dependencies and design patterns
- This can reduce token usage by 70-90% for large codebases

**Task Parameters for Code-Reviewer Agent**:
- **subagent_type**: code-reviewer
- **description**: Standard code review focused on practical issues
- **prompt**: Perform a code review of `$REVIEW_TARGET` focusing on:

  **Primary Focus Areas**:
  1. **Bug Detection and Logic Issues**:
     - Logic errors and edge cases
     - Error handling gaps and exception safety
     - Null pointer issues and bounds checking
     - Race conditions and concurrency issues
     - Input validation problems

  2. **Design and Architecture Issues**:
     - Code organization and structure problems
     - Tight coupling and low cohesion
     - Violation of SOLID principles
     - Missing abstractions or over-engineering
     - Inconsistent patterns and conventions

  3. **Dead Code and Cleanup**:
     - Unused functions, classes, and variables
     - Unreachable code paths
     - Commented-out code blocks
     - Unused imports and dependencies
     - Obsolete TODOs and FIXME comments

  4. **Code Quality and Maintainability**:
     - Readability and clarity issues
     - Complex functions that need refactoring
     - Magic numbers and hardcoded values
     - Naming conventions and clarity
     - Documentation gaps for complex logic

  5. **Performance Observations**:
     - Obvious inefficiencies (N+1 queries, unnecessary loops)
     - Memory usage issues
     - Algorithmic improvements
     - Resource leak potential

$([ -n "$REQUIREMENTS_FILE" ] && echo "
  6. **Requirements Compliance**:
     - Validate implementation against requirements in $SPEC_FILE
     - Check for missing functionality
     - Verify acceptance criteria are met
     - Identify gaps between spec and implementation")

  **Output Requirements**:
  - **Focus on practical issues**: Bugs, design flaws, maintainability
  - **No security emphasis**: Skip security scanning unless critical
  - **Prioritized action plan**: High/Medium/Low priority issues
  - **Specific recommendations**: Concrete steps to fix each issue
  - **Code examples**: Show specific problematic code when possible

### Systematic Review (Complex Projects)

When systematic review is requested, use structured reasoning:

```bash
if [ "$USE_SYSTEMATIC" = "true" ]; then
    echo "🧠 Performing systematic code review with structured reasoning..."
    echo ""
fi
```

Use Sequential Thinking MCP for comprehensive analysis:

**Sequential Thinking Parameters**:
- **Initial thoughts**: 15-20 for comprehensive systematic review
- **Focus**: Step-by-step code quality analysis across multiple dimensions
- **Process**: Systematic evaluation of bugs, design, maintainability

**Systematic Review Process**:
1. **Codebase Overview**: Understand project structure and patterns
2. **Bug Analysis**: Systematic search for logic errors and edge cases
3. **Design Evaluation**: Assess architecture and organization
4. **Quality Assessment**: Evaluate readability and maintainability
5. **Performance Review**: Identify obvious inefficiencies
6. **Best Practices Check**: Verify adherence to conventions
7. **Prioritization**: Rank issues by impact and effort to fix
8. **Action Plan Generation**: Create specific, actionable recommendations

## Phase 4: Generate Prioritized Action Plan

All reviews must include a structured action plan:

```bash
echo ""
echo "📋 Generating prioritized action plan..."
echo ""
```

The code-reviewer agent will provide output in this format:

```markdown
# Code Review Results

## Summary
Brief overview of findings and overall code quality assessment.

## Critical Issues (Fix Immediately)
- **Issue**: Specific problem description
  - **Location**: File:line or component
  - **Impact**: Why this matters
  - **Fix**: Specific steps to resolve

## Important Issues (Fix Soon)
- **Issue**: Specific problem description
  - **Location**: File:line or component
  - **Impact**: Why this matters
  - **Fix**: Specific steps to resolve

## Minor Issues (Fix When Convenient)
- **Issue**: Specific problem description
  - **Location**: File:line or component
  - **Impact**: Why this matters
  - **Fix**: Specific steps to resolve

## Positive Observations
- Things that are well-implemented
- Good patterns and practices found
- Areas of quality code

## Action Plan Priority
1. **Immediate** (Critical): [List of critical fixes]
2. **This Sprint** (Important): [List of important improvements]
3. **Backlog** (Minor): [List of minor cleanups]

## Estimated Effort
- Critical fixes: X hours
- Important improvements: Y hours
- Minor cleanups: Z hours
- **Total estimated effort**: N hours
```

## Phase 5: Save Review Results

```bash
# Save review results for tracking and follow-up
echo "💾 Saving review results..."

# Determine save location
REVIEW_FILE=""
if [ -n "$WORK_UNIT_DIR" ] && [ -d "$WORK_UNIT_DIR" ]; then
    # Save in work unit if available
    REVIEW_FILE="$WORK_UNIT_DIR/review_$(date +%Y%m%d_%H%M%S).md"
    echo "📂 Saving in active work unit: $(basename "$WORK_UNIT_DIR")"
else
    # Save in .claude directory
    mkdir -p .claude/reviews
    REVIEW_FILE=".claude/reviews/review_$(date +%Y%m%d_%H%M%S).md"
    echo "📂 Saving in .claude/reviews/"
fi

echo "✅ Review saved: $REVIEW_FILE"
echo ""
echo "💡 Next steps:"
echo "   - Review the prioritized action plan"
echo "   - Use /fix to apply recommended fixes"
echo "   - Run /review again after fixes to verify improvements"
```

## Success Indicators

A successful code review includes:

- ✅ **Practical Focus**: Bugs, design issues, dead code identified
- ✅ **No Security Emphasis**: Focus on code quality, not security scanning
- ✅ **Prioritized Action Plan**: Critical/Important/Minor classification
- ✅ **Specific Recommendations**: Concrete steps to fix each issue
- ✅ **Effort Estimates**: Time required for fixes
- ✅ **Clear Output**: Easy to understand and act upon

## Integration with Fix Command

After review, apply fixes with:

```bash
/fix review                    # Apply fixes from most recent review
/fix .claude/reviews/review_*.md  # Apply fixes from specific review
```

The `/fix` command can automatically apply many of the recommended improvements.

## Examples

### Basic Code Review
```bash
/review
# → Standard review of entire project
# → Identifies bugs, design issues, dead code
# → Provides prioritized action plan
```

### Targeted Review
```bash
/review src/auth.py
# → Reviews authentication module specifically
# → Focuses on logic errors and design issues
# → Provides specific recommendations for auth code
```

### Requirements Validation
```bash
/review --spec requirements.md
# → Reviews code against requirements
# → Identifies missing functionality
# → Validates implementation completeness
```

### Complex Project Review
```bash
/review --systematic
# → Uses structured reasoning for comprehensive analysis
# → Systematic evaluation across multiple quality dimensions
# → Detailed step-by-step analysis process
```

### Semantic Code Review (With Serena)
```bash
/review --semantic
# → Uses Serena semantic analysis for efficient review
# → 70-90% token reduction compared to traditional grep
# → Symbol-aware analysis finds dead code, dependencies
# → Auto-enables for large codebases (>30 files)
```

### Combined Semantic and Requirements Review
```bash
/review --semantic --spec requirements.md
# → Semantic analysis of code structure
# → Validates implementation against requirements
# → Most efficient review mode available
```

---

*This simplified review command focuses on practical code quality issues that developers encounter daily, providing actionable recommendations without the overhead of security scanning. When Serena is connected, it automatically leverages semantic analysis for massive token savings.*