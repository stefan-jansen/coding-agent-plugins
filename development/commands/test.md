---
allowed-tools: [Read, Write, Edit, Bash, Task]
argument-hint: "[tdd] or [pattern]"
description: Test-driven development workflow using test-engineer agent
---

# Test Workflow

Comprehensive testing workflow using the specialized test-engineer agent. Supports TDD, test running, and coverage analysis.

**Input**: $ARGUMENTS

## Phase 1: Determine Test Strategy

Based on the provided arguments: $ARGUMENTS

I'll analyze the request to determine the appropriate testing approach:

- **TDD Mode**: Arguments contain "tdd" - full test-driven development workflow
- **Pattern Testing**: Specific test pattern provided - run matching tests only
- **Full Test Suite**: No specific arguments - run all tests with coverage
- **Test Creation**: Request to create new tests for specific functionality

### Test Mode Selection

**Test-Driven Development (TDD)**:
When "tdd" is specified, I'll execute the complete RED-GREEN-REFACTOR cycle:
1. **RED**: Write failing tests that define desired behavior
2. **GREEN**: Implement minimal code to make tests pass
3. **REFACTOR**: Improve code quality while keeping tests green

**Targeted Testing**:
When a pattern is provided, I'll focus on specific test execution with detailed reporting.

**Comprehensive Testing**:
When no specific mode is requested, I'll run the full test suite with coverage analysis.

## Phase 2: Project Context Analysis

### Test Framework Detection

I'll identify the testing setup by examining:
- **Python Projects**: pytest, unittest, nose configuration
- **JavaScript Projects**: Jest, Mocha, Jasmine setup
- **Go Projects**: Built-in testing framework
- **Other Languages**: Framework-specific test configurations

### Current Test State Assessment

I'll evaluate the existing test environment:
- **Test Directory Structure**: Organization and conventions
- **Configuration Files**: Test runner settings and coverage config
- **Test Coverage**: Current coverage levels and gaps
- **Test Quality**: Naming conventions, organization, maintainability

## Phase 3: Execute Test-Driven Development Workflow

### TDD Mode Execution

When in TDD mode, I'll use the Task tool to invoke the test-engineer agent:

**Agent Delegation**:
- **subagent_type**: test-engineer
- **description**: Execute comprehensive TDD workflow
- **prompt**: Implement strict Test-Driven Development process:

  **Phase 1 - RED (Failing Tests)**:
  - Verify APIs first using Serena before writing test code
  - Write comprehensive test cases that define expected behavior
  - Include edge cases, error conditions, and boundary values
  - Ensure all tests fail initially (no implementation exists)
  - Verify test failure messages are meaningful and informative

  **Phase 2 - GREEN (Minimal Implementation)**:
  - Write the simplest code possible to make tests pass
  - Focus on correctness, not optimization or elegance
  - Implement only what's needed for current test requirements
  - Verify all tests pass before proceeding

  **Phase 3 - REFACTOR (Code Improvement)**:
  - Improve code structure, readability, and performance
  - Apply design patterns and best practices
  - Add comprehensive documentation and type hints
  - Ensure tests continue to pass throughout refactoring

  **Phase 4 - VALIDATION (Quality Assurance)**:
  - Run complete test suite to check for regressions
  - Verify test coverage meets or exceeds 80% threshold
  - Validate test quality and maintainability
  - Confirm adherence to project coding standards

### Test Execution and Analysis

For non-TDD modes, I'll execute tests and provide comprehensive analysis:

#### Test Execution Strategy
1. **Framework Detection**: Automatically identify test framework and configuration
2. **Test Selection**: Run all tests or filter by provided pattern
3. **Coverage Collection**: Generate coverage data during test execution
4. **Result Analysis**: Parse test results for failures, skips, and performance

#### Quality Metrics Assessment
1. **Coverage Analysis**: Line, branch, and function coverage reporting
2. **Test Distribution**: Count and categorization of test types
3. **Performance Metrics**: Test execution time and resource usage
4. **Quality Indicators**: Test organization, naming, and maintainability

## Phase 4: Specialized Test Creation

### Test Strategy Development

For new functionality requiring tests, I'll invoke the test-engineer agent:

**Agent Delegation**:
- **Purpose**: Create comprehensive test strategy for specific functionality
- **Scope**: Unit tests, integration tests, edge case coverage
- **Deliverables**: Complete test suite with high coverage and quality

### Test Enhancement

For improving existing test suites:
- **Coverage Gap Analysis**: Identify untested code paths
- **Test Quality Review**: Improve test organization and maintainability
- **Performance Optimization**: Reduce test execution time
- **Framework Modernization**: Update to latest testing practices

## Phase 5: Test Results Analysis and Reporting

### Coverage Reporting

I'll provide detailed coverage analysis including:
- **Overall Coverage**: Total percentage across project
- **Module Breakdown**: Coverage by file and function
- **Missing Coverage**: Specific lines and branches not covered
- **Trend Analysis**: Coverage changes over time

### Test Quality Assessment

I'll evaluate test suite quality by examining:
- **Test Organization**: Structure, naming conventions, grouping
- **Test Completeness**: Edge cases, error conditions, integration points
- **Test Maintainability**: Clear assertions, proper fixtures, minimal duplication
- **Test Performance**: Execution speed, resource usage, parallelization

### Actionable Recommendations

Based on analysis, I'll provide specific guidance:
- **Immediate Actions**: Critical test failures or coverage gaps
- **Quality Improvements**: Test organization and maintainability enhancements
- **Strategic Initiatives**: Long-term test infrastructure improvements
- **Best Practices**: Adherence to testing standards and conventions

## Phase 6: Documentation and Context Updates

### Test Documentation

I'll ensure comprehensive test documentation:
- **Test Strategy**: Overall approach and coverage goals
- **Test Organization**: Directory structure and naming conventions
- **Running Tests**: Commands, configuration, and environment setup
- **Coverage Goals**: Targets and measurement methodology

### Session Memory Updates

I'll record test session outcomes:
- **Test Results**: Pass/fail status and coverage achieved
- **Quality Metrics**: Coverage percentages and improvement areas
- **Action Items**: Follow-up tasks for test improvement
- **Configuration Changes**: Updates to test setup or framework

## Success Indicators

Testing workflow is successful when:
- ✅ All tests execute successfully in clean environment
- ✅ Coverage meets or exceeds project standards (typically 80%+)
- ✅ Test failure messages are clear and actionable
- ✅ Test execution time is reasonable for development workflow
- ✅ Tests are well-organized and maintainable
- ✅ Edge cases and error conditions are properly covered

## Testing Best Practices

### TDD Compliance
- Always write tests before implementation
- Ensure tests fail meaningfully before implementation
- Implement minimal code to satisfy tests
- Refactor continuously while maintaining test coverage

### Quality Standards
- Test names clearly describe expected behavior
- Each test focuses on single behavior or outcome
- Tests are independent and can run in any order
- Test setup and teardown properly managed

### Coverage Goals
- Aim for >80% line coverage as minimum
- Prioritize critical path and edge case coverage
- Balance coverage quantity with test quality
- Monitor coverage trends over time

---

*Comprehensive testing workflow emphasizing test-driven development, quality metrics, and continuous improvement through specialized agent support.*