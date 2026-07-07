---
allowed-tools: [Task, Read, Edit, MultiEdit, Write, Bash, Grep, mcp__serena__find_symbol, mcp__serena__search_for_pattern, mcp__serena__get_symbols_overview, mcp__serena__find_referencing_symbols, mcp__serena__replace_symbol_body]
argument-hint: "[error|review|audit|all] [file/pattern]"
description: Universal debugging and fix application with semantic code analysis
---

# Universal Fix & Debug

**Input**: $ARGUMENTS

## Usage

```bash
# Debug Mode
/fix "TypeError: 'NoneType' has no attribute 'get'"
/fix src/auth.py
/fix "Failed tests in test_user.py"

# Apply Fixes Mode
/fix review   # Apply fixes from recent review
/fix audit    # Apply fixes from audit results
/fix all      # Apply all available fixes
```

## Process

### 1. Determine Mode
- **Debug**: Error messages, stack traces, file references → investigate and fix
- **Apply**: "review", "audit", "all" → apply structured fixes from analysis files

### 2. Debug Mode
1. Parse error message/stack trace
2. Locate source files and lines
3. Gather context (dependencies, related code)
4. Identify root cause
5. **Verify APIs with Serena before writing fix**
6. Apply minimal targeted fix
7. Test and verify resolution

### 3. Apply Fixes Mode
1. Load fix recommendations from review/audit files
2. Categorize: code quality, bugs, performance, security
3. Apply fixes systematically (critical first)
4. Validate each change
5. Document results

### 4. Verification
- Run relevant tests
- Check linting
- Verify functionality preserved
- Update documentation if needed

## Serena Enhancement

**When available** (70-90% token reduction):
- `find_symbol` → locate exact functions/classes in errors
- `find_referencing_symbols` → understand usage patterns
- `get_symbols_overview` → module structure without reading files
- `replace_symbol_body` → surgical fixes to specific methods

**Example workflow**:
```bash
# Error: "AttributeError: 'User' object has no attribute 'email'"
find_symbol User                    # Find class definition
find_referencing_symbols User       # Check usage
replace_symbol_body User/get_email  # Apply targeted fix
```

**Fallback**: File reading + grep-based analysis
