---
name: review
description: This skill should be used when the user asks to "review this code", "check for bugs", "code review", "find issues", "review my changes", "look for problems", or when evaluating code quality, finding bugs, or identifying improvements.
allowed-tools: [Read, Write, Task, Bash, Grep, Glob, mcp__sequential-thinking__sequentialthinking, mcp__serena__find_symbol, mcp__serena__search_for_pattern, mcp__serena__get_symbols_overview, mcp__serena__find_referencing_symbols]
---

# Code Review

Practical code review focused on bugs, design issues, and maintainability.

## When This Triggers

- "Review this code" / "review my changes"
- "Check for bugs"
- "Find issues in this code"
- "Look for problems"
- "Code review please"
- Evaluating code quality

## Flags (if explicitly passed)

- `--systematic`: Structured reasoning for complex code
- `--semantic`: Use Serena (70-90% token reduction)
- `--spec requirements.md`: Validate against requirements

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
