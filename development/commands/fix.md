---
allowed-tools: [Task, Read, Edit, MultiEdit, Write, Bash, Grep, mcp__serena__find_symbol, mcp__serena__search_for_pattern, mcp__serena__get_symbols_overview, mcp__serena__find_referencing_symbols, mcp__serena__replace_symbol_body]
argument-hint: "[error|review|audit|all] [file/pattern]"
description: Universal debugging and fix application with semantic code analysis - debug errors or apply review fixes automatically
---

# Universal Fix & Debug Command

Consolidated command for debugging errors and applying fixes from various sources. Automatically detects whether to debug an error or apply fixes based on input.

**Input**: $ARGUMENTS

## Usage

### Debug Error Mode
```bash
/fix "TypeError: 'NoneType' object has no attribute 'get'"
/fix src/auth.py
/fix "Failed tests in test_user.py"
```

### Apply Review Fixes Mode
```bash
/fix review                    # Apply fixes from most recent review
/fix audit                     # Apply fixes from audit results
/fix all                       # Apply all available fixes
```

## Phase 1: Determine Fix Mode

Based on the arguments provided: $ARGUMENTS

I'll automatically determine the appropriate mode:

### Debug Mode (for errors and issues)
- When arguments contain error messages, stack traces, or exceptions
- When pointing to specific files with problems
- When describing symptoms or failing behavior

### Fix Application Mode (for structured fixes)
- When arguments mention "review", "audit", or "all"
- When referencing existing analysis results
- When applying pre-identified improvements

## Phase 2: Execute Debug Mode

When debugging errors or issues:

### Error Analysis
1. **Understand the Error**: Parse error messages, stack traces, and symptoms
2. **Locate Source**: Identify files and lines causing the issue
3. **Gather Context**: Read relevant code sections and dependencies
4. **Identify Root Cause**: Determine the underlying problem

### Investigation Process
1. **Reproduce the Issue**: Create test cases or reproduction steps
2. **Trace Execution**: Follow code paths to identify failure points
3. **Check Dependencies**: Verify imports, configurations, and environment
4. **Validate Assumptions**: Test expected vs actual behavior

### Solution Implementation
1. **Verify APIs First**: Use Serena to check exact method signatures BEFORE writing fixes
2. **Design Fix**: Plan the minimal change to resolve the issue
3. **Apply Changes**: Implement the fix with proper error handling
4. **Test Validation**: Verify the fix resolves the problem
5. **Regression Check**: Ensure no new issues are introduced

### Enhanced Semantic Debugging (with Serena MCP)
When Serena MCP is available, leverage semantic code understanding for more efficient and accurate debugging:

**When to use Serena for debugging**:
- Complex codebases requiring understanding of symbol relationships
- Debugging issues involving method calls, class hierarchies, or inheritance
- Tracing errors through multiple files and modules
- Understanding impact of changes across the codebase
- Large codebases where reading entire files would be token-inefficient

**Serena-Enhanced Debugging Process**:

1. **Semantic Error Analysis**:
   - Use `find_symbol` to locate exact functions/classes mentioned in errors
   - Use `find_referencing_symbols` to understand usage patterns
   - Use `get_symbols_overview` to understand module structure without reading entire files
   - Trace actual symbol relationships rather than text-based searching

2. **Efficient Context Gathering**:
   - **70-90% token reduction**: Only load relevant symbols instead of entire files
   - **Precise targeting**: Find exact methods/classes causing issues
   - **Dependency intelligence**: Understand real import relationships
   - **Type-aware analysis**: Follow actual type information and contracts

3. **Smart Fix Application**:
   - Use `replace_symbol_body` for surgical fixes to specific methods/classes
   - Understand impact using `find_referencing_symbols` before making changes
   - Ensure changes maintain API compatibility across the codebase

**Example Serena Debugging Workflow**:
```bash
# Error: "AttributeError: 'User' object has no attribute 'email'"
# 1. Find the User class definition
/serena find_symbol User

# 2. Check all references to understand expected attributes
/serena find_referencing_symbols User

# 3. Examine specific method causing issue
/serena find_symbol User/get_email

# 4. Apply surgical fix to specific method
/serena replace_symbol_body User/get_email "fixed implementation"
```

**Graceful Degradation**: When Serena unavailable, falls back to traditional file-reading and grep-based analysis while maintaining full debugging functionality.

## Phase 3: Execute Fix Application Mode

When applying structured fixes from reviews or audits:

### Fix Source Identification
1. **Review Fixes**: Apply recommendations from recent code reviews
2. **Audit Fixes**: Address issues found in infrastructure audits
3. **All Fixes**: Comprehensively apply all identified improvements
4. **Prioritization**: Address critical issues first, then improvements

### Fix Categories
1. **Code Quality**: Formatting, linting, style consistency
2. **Bug Fixes**: Logic errors, edge cases, error handling
3. **Performance**: Inefficiencies, optimization opportunities
4. **Security**: Vulnerabilities, exposure risks, best practices
5. **Maintainability**: Refactoring, documentation, clarity

### Application Process
1. **Read Fix Sources**: Load recommendations from review/audit files
2. **Categorize Fixes**: Group by type, priority, and complexity
3. **Apply Systematically**: Implement fixes in logical order
4. **Validate Changes**: Test each fix as it's applied
5. **Document Results**: Record what was changed and why

### Enhanced Fix Application (with Serena MCP)
When Serena is available, apply fixes more efficiently:

**Semantic Fix Application**:
- **Symbol-level changes**: Use `replace_symbol_body` for precise function/method fixes
- **Impact analysis**: Check `find_referencing_symbols` before applying changes
- **Efficient targeting**: Use `find_symbol` to locate exact code to fix
- **Token efficiency**: Apply fixes without reading entire files

**Smart Refactoring Support**:
- **Cross-file consistency**: Ensure symbol changes are applied consistently
- **API compatibility**: Check references before changing method signatures
- **Dependency awareness**: Understand real import relationships when refactoring

## Phase 4: Quality Verification

For all fix operations:

### Testing and Validation
1. **Run Tests**: Execute relevant test suites to verify fixes
2. **Check Linting**: Ensure code quality standards are maintained
3. **Verify Functionality**: Confirm original behavior is preserved
4. **Performance Check**: Ensure fixes don't degrade performance

### Documentation Updates
1. **Code Comments**: Add explanations for complex fixes
2. **Commit Messages**: Document what was fixed and why
3. **Review Updates**: Mark fixes as applied in tracking systems
4. **Learning Notes**: Record insights for future reference

## Phase 5: Error Prevention

### Proactive Improvements
1. **Add Error Handling**: Implement proper exception management
2. **Input Validation**: Add checks for edge cases and bad input
3. **Type Annotations**: Improve type safety where applicable
4. **Test Coverage**: Add tests for previously uncovered scenarios

### Future Prevention
1. **Pattern Recognition**: Identify common error patterns
2. **Tool Configuration**: Adjust linting/checking tools to catch similar issues
3. **Process Improvements**: Suggest workflow changes to prevent recurrence
4. **Documentation**: Update guides and standards based on learnings

## Success Indicators

### Debug Mode Success
- ✅ Root cause identified and understood
- ✅ Minimal, targeted fix applied
- ✅ Issue no longer reproduces
- ✅ No regression issues introduced
- ✅ Tests pass and functionality verified

### Fix Application Success
- ✅ All applicable fixes identified and applied
- ✅ Code quality metrics improved
- ✅ Security issues addressed
- ✅ Performance maintained or improved
- ✅ Documentation updated appropriately

## Common Fix Patterns

### Error Handling Improvements
- Add try/catch blocks for risky operations
- Validate inputs before processing
- Provide meaningful error messages
- Implement graceful degradation

### Code Quality Fixes
- Fix linting violations (formatting, imports, unused variables)
- Improve variable and function naming
- Extract complex logic into helper functions
- Add type annotations for clarity

### Performance Optimizations
- Cache expensive computations
- Optimize database queries
- Reduce memory usage
- Eliminate unnecessary operations

### Security Hardening
- Sanitize user inputs
- Fix SQL injection vulnerabilities
- Remove hardcoded credentials
- Implement proper authentication checks

## Examples

### Debug a Specific Error
```bash
/fix "AttributeError: 'User' object has no attribute 'email' in auth.py:42"
# → Analyzes the attribute error and fixes the User class
```

### Apply Review Recommendations
```bash
/fix review
# → Reads recent review file and applies all recommendations
```

### Comprehensive Fix Application
```bash
/fix all
# → Applies fixes from reviews, audits, and code analysis
```

### File-Specific Debugging
```bash
/fix src/models/user.py
# → Analyzes and fixes issues specific to the user model file
```

---

*Universal fix command that intelligently debugs errors or applies structured improvements based on context.*