---
allowed-tools: [Read, Write, Edit, Bash, Task]
argument-hint: "[tdd] or [pattern]"
description: Test-driven development workflow using test-engineer agent
---

# Test Workflow

**Input**: $ARGUMENTS

## Usage

```bash
/test             # Run full test suite with coverage
/test tdd         # TDD workflow: RED-GREEN-REFACTOR
/test auth        # Run tests matching pattern
/test coverage    # Coverage analysis only
```

## Process

### 1. Determine Mode
- **tdd**: Full Test-Driven Development cycle
- **pattern**: Run matching tests only
- **No args**: Full suite with coverage analysis

### 2. Detect Framework
- Python: pytest, unittest
- JavaScript: Jest, Mocha
- Go: built-in testing
- Check config files for settings

### 3. TDD Mode (via test-engineer agent)

**RED**: Write failing tests defining expected behavior
- Include edge cases, error conditions, boundary values
- Verify meaningful failure messages

**GREEN**: Minimal implementation to pass tests
- Simplest code possible
- Only what's needed for current tests

**REFACTOR**: Improve while keeping green
- Structure, readability, performance
- Documentation and type hints

**VALIDATE**: Quality assurance
- Full suite regression check
- Coverage ≥80% threshold

### 4. Standard Test Execution
1. Run tests (all or filtered by pattern)
2. Collect coverage data
3. Parse results for failures/skips
4. Report coverage by module

### 5. Results Analysis
- Coverage: line, branch, function percentages
- Gaps: uncovered code paths
- Quality: organization, naming, maintainability
- Performance: execution time

## Success Criteria
- ✅ All tests pass
- ✅ Coverage ≥80%
- ✅ Clear failure messages
- ✅ Reasonable execution time
- ✅ Tests are maintainable
