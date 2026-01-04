---
allowed-tools: [Read, Write, Task, Bash, Grep, Glob, mcp__sequential-thinking__sequentialthinking]
argument-hint: "[file/directory] [--spec requirements.md] [--systematic] [--semantic]"
description: "Code review: bugs, design flaws, dead code, with prioritized action plan"
---

# Code Review

Practical code review focused on bugs, design issues, and maintainability.

**Input**: $ARGUMENTS

## Usage

```bash
/review                        # Review entire project
/review src/auth.py            # Review specific file
/review --spec design.md       # Validate against requirements
/review --systematic           # Structured reasoning for complex code
/review --semantic             # Use Serena (70-90% token reduction)
```

## Focus Areas

1. **Bugs**: Logic errors, edge cases, error handling, null checks
2. **Design**: Organization, coupling, SOLID violations, patterns
3. **Dead Code**: Unused functions, imports, variables, commented code
4. **Quality**: Readability, complexity, naming, documentation gaps
5. **Performance**: Obvious inefficiencies, N+1 queries, memory leaks

## NOT Included (By Design)

- Security scanning → use specialized tools
- Infrastructure audits → use `/audit`

## Output Format

```markdown
# Code Review Results

## Summary
Brief overview of findings.

## Critical Issues (Fix Immediately)
- **Issue**: [description]
  - **Location**: file:line
  - **Impact**: [why it matters]
  - **Fix**: [specific steps]

## Important Issues (Fix Soon)
[same format]

## Minor Issues (Fix When Convenient)
[same format]

## Positive Observations
- Well-implemented patterns
- Good practices found

## Action Plan
1. Immediate: [critical fixes]
2. This Sprint: [important improvements]
3. Backlog: [minor cleanups]

## Estimated Effort
- Critical: X hours
- Important: Y hours
- Minor: Z hours
```

## Integration

After review: `/fix review` to apply recommended fixes
