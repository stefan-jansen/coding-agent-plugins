# Diátaxis Template: How-To

**Mode**: Problem-Oriented
**Purpose**: Solve specific problems efficiently
**User Need**: "I need to accomplish X"

## Template Structure

### 1. Problem Statement: What This Solves
- **Pattern**: State problem clearly, establish context
- **Tone**: Direct, acknowledges user's pain point
- **Length**: 2-3 sentences

```markdown
{PROBLEM_DESCRIPTION} occurs when {CONTEXT}. This guide shows you how to {SOLUTION} in {TIMEFRAME}, preventing {NEGATIVE_OUTCOME}.
```

### 2. Prerequisites: What You Need
- **Pattern**: Minimal requirements only
- **Tone**: Assumes competence, no hand-holding
- **Format**: Brief bulleted list

```markdown
## Prerequisites

- {TOOL} configured
- {PERMISSION} access
- {KNOWLEDGE} of {CONCEPT}
```

### 3. Solution Overview: The Approach
- **Pattern**: High-level strategy before tactical steps
- **Tone**: Expert-to-expert
- **Length**: 1 paragraph

```markdown
## Approach

The solution involves {HIGH_LEVEL_STEPS}. We'll {ACTION_1}, then {ACTION_2}, and finally {ACTION_3}. This approach {WHY_THIS_APPROACH_WORKS}.
```

### 4. Step-by-Step Solution
- **Pattern**: Direct instructions, minimal explanation
- **Tone**: Imperative, efficient
- **Structure**: Numbered steps, sub-bullets for options

```markdown
## Solution

**Step 1**: {ACTION_VERB} {OBJECT}

```bash
{COMMAND}
```

**Step 2**: {ACTION_VERB} {OBJECT}

{BRIEF_INSTRUCTION}. For example:

```{LANGUAGE}
{CODE_EXAMPLE}
```

**Step 3**: Verify {OUTCOME}

```bash
{VERIFICATION_COMMAND}
```

Expected output: `{SUCCESS_INDICATOR}`
```

### 5. Troubleshooting: Common Issues
- **Pattern**: Problem → Cause → Fix
- **Tone**: Diagnostic, systematic
- **Format**: Subsections per issue

```markdown
## Troubleshooting

### Issue: {ERROR_MESSAGE}

**Cause**: {WHY_THIS_HAPPENS}

**Fix**: {SOLUTION_STEP}

```bash
{FIX_COMMAND}
```

### Issue: {ANOTHER_ERROR}

**Cause**: {ROOT_CAUSE}

**Fix**: {REMEDIATION}
```

### 6. Variations: Alternative Approaches
- **Pattern**: When to use alternatives
- **Tone**: Pragmatic, trade-off aware
- **Format**: Subsections with "When to use"

```markdown
## Alternatives

### Approach A: {METHOD_NAME}

**When to use**: {USE_CASE}

**Trade-offs**: Faster but {LIMITATION}

```bash
{ALTERNATIVE_COMMAND}
```

### Approach B: {ANOTHER_METHOD}

**When to use**: {ANOTHER_USE_CASE}

**Trade-offs**: More robust but {COST}
```

## Key Principles

### DO: How-To Best Practices
✅ **Start with outcome**: State what will be accomplished upfront
✅ **Assume competence**: Don't explain basic concepts
✅ **Minimize steps**: Combine steps where possible
✅ **Provide context**: Brief "why" helps users adapt solution
✅ **Include troubleshooting**: Address common failure modes
✅ **Show alternatives**: Present trade-offs for different approaches
✅ **Use real examples**: Concrete scenarios, not toy examples

### DON'T: How-To Anti-Patterns
❌ **Explain everything**: Don't teach concepts (use Explanation mode)
❌ **One-size-fits-all**: Don't ignore variations in user context
❌ **Hide trade-offs**: Don't present solution as always optimal
❌ **Skip error handling**: Don't assume happy path only
❌ **Over-abstract**: Don't use generic placeholders without examples
❌ **Assume environment**: Don't skip environment-specific steps

## Topic Sentence Patterns

**Primary Pattern**: Problem + Solution
- "{PROBLEM} occurs when {CONTEXT}. {SOLUTION} resolves this by {MECHANISM}."
- "To {GOAL}, {ACTION} using {TOOL}."

**Secondary Pattern**: Action + Result
- "{ACTION_VERB} {OBJECT} to {ACHIEVE_GOAL}."
- "Configure {SETTING} to prevent {PROBLEM}."

**Occasional**: Question + Answer (for decision points)
- "Should you use {APPROACH_A} or {APPROACH_B}? Use {APPROACH_A} when {CONDITION}."

**Avoid**: Concept + Analogy (too abstract), Definition + Importance (not solution-focused)

## Example Paragraph

**Good How-To Paragraph**:
```markdown
Debugging slow API responses requires identifying the bottleneck: database queries, external service calls, or application logic. Add timing instrumentation around each component using a profiler:

```python
import time

def timed_operation(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = (time.time() - start) * 1000
        print(f"{func.__name__}: {elapsed:.2f}ms")
        return result
    return wrapper

@timed_operation
def fetch_user_data(user_id):
    return db.query("SELECT * FROM users WHERE id = ?", user_id)
```

Run your endpoint and examine output. In our analysis of 500 production requests, 80% of slowdowns traced to unoptimized database queries. If queries exceed 100ms, add indexes or reduce fetched columns.
```

**Analysis**:
- ✅ Problem stated clearly (slow API responses)
- ✅ Solution provided directly (profiling)
- ✅ Concrete code example (complete, runnable)
- ✅ Real-world data (80% of slowdowns)
- ✅ Next action (if queries slow, optimize)
- ✅ Minimal explanation (straight to solution)

## Diátaxis Mode Integration

### When to Use How-To Mode
- **User Intent**: Problem-solving, needs solution now
- **User State**: Competent, stuck on specific issue
- **Content Goal**: Enable user to solve problem and move on
- **Success Metric**: Problem solved efficiently

### Relationship to Other Modes
- **How-To ← Tutorial**: User learned basics, now applying to real problems
- **How-To ↔ Reference**: User looks up specifics while following How-To
- **How-To → Explanation**: After solving problem, user seeks deeper understanding

### Evidence Integration in How-Tos
- **Use for validation**: Cite to establish solution effectiveness
- **Example**: "This approach reduced P95 latency from 2.3s to 400ms in our benchmark of 500 production requests"
- **Keep brief**: Focus on outcome, not methodology details

## Variable Placeholders

Replace these during content generation:

- `{PROBLEM_DESCRIPTION}`: The problem (e.g., "Slow database queries")
- `{CONTEXT}`: When it happens (e.g., "joining multiple tables without indexes")
- `{SOLUTION}`: What will fix it (e.g., "add composite indexes")
- `{TIMEFRAME}`: How long solution takes (e.g., "under 5 minutes")
- `{NEGATIVE_OUTCOME}`: What's prevented (e.g., "request timeouts")
- `{TOOL}`: Required software (e.g., "PostgreSQL 14+")
- `{PERMISSION}`: Access needed (e.g., "database admin")
- `{KNOWLEDGE}`: Assumed knowledge (e.g., "SQL basics")
- `{HIGH_LEVEL_STEPS}`: Strategy summary (e.g., "profiling, indexing, verifying")
- `{ACTION_VERB}`: Imperative (e.g., "Profile", "Index", "Verify")
- `{COMMAND}`: Code/command to run
- `{ERROR_MESSAGE}`: Common error (e.g., "Timeout Error")
- `{ROOT_CAUSE}`: Why error occurs
- `{FIX_COMMAND}`: How to fix
- `{METHOD_NAME}`: Alternative approach name
- `{USE_CASE}`: When to use alternative
- `{LIMITATION}`: Downside of alternative

## Usage by section-drafter Agent

1. **Load this template** when `diataxis_mode === "howto"`
2. **Start with problem** statement in opening
3. **Provide solution overview** before tactical steps
4. **Use Problem + Solution** topic sentence pattern
5. **Keep explanations minimal** - focus on actions
6. **Include troubleshooting** section for failure modes
7. **Present alternatives** when multiple valid approaches exist
8. **Use imperative mood** throughout

## Quality Checklist

Before finalizing How-To content, verify:

- [ ] Problem clearly stated upfront
- [ ] Solution outcome specified
- [ ] Steps are actionable and complete
- [ ] Commands are copy-pasteable
- [ ] Expected output provided for verification
- [ ] Common errors addressed in troubleshooting
- [ ] Alternatives presented with trade-offs
- [ ] Assumptions about user environment stated
- [ ] Real-world examples used (not toy data)
- [ ] Evidence cited for solution effectiveness

---

**Template Version**: 1.0.0 (SIF Plugin)
**Last Updated**: 2025-10-27
**References**: Diátaxis Framework (Procida 2017), SIF skills/diataxis-framework/SKILL.md
