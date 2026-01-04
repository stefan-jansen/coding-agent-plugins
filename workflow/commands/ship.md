---
allowed-tools: [Task, Bash, Read, Write, MultiEdit, Grep, Glob]
argument-hint: "[--preview | --pr | --commit | --deploy]"
description: "Deliver completed work with validation and documentation"
---

# Work Delivery

Validate, document, and deliver completed work.

**Options**: $ARGUMENTS

## Modes

- `--preview`: Show what would be delivered (no changes)
- `--pr`: Create pull request with documentation
- `--commit`: Commit to current branch
- `--deploy`: Prepare for production deployment

## Process

1. **Readiness Check**
   - Find active work unit
   - Verify all tasks completed
   - Check git status (clean/dirty)

2. **Quality Validation**
   - Run test suite (>80% coverage required)
   - Execute linting/type checking
   - Security scan
   - Build verification

3. **Generate Documentation**
   - DELIVERY.md: What was built, architecture, metrics
   - CHANGELOG.md: Added/changed/fixed
   - DEPLOYMENT.md: Prerequisites, steps, rollback

4. **Execute Delivery**
   - PR: Generate description, include metrics, link issues
   - Commit: Stage changes, create conventional commit
   - Deploy: Final validation, env config, monitoring setup

5. **Memory Reflection**
   - Analyze work unit for learnings
   - Prompt for `/memory-update` to capture:
     - Decisions made
     - Lessons learned
     - New conventions
     - Dependencies added

6. **Archive Work Unit**
   - Update status to completed
   - Record delivery method
   - Move to archives

## Quality Gates

All must pass:
- ✅ Tests pass with >80% coverage
- ✅ No critical lint/security issues
- ✅ Documentation complete
- ✅ Build successful

## Commit Format

```
feat|fix|docs: Brief description

Detailed explanation of changes.

🤖 Generated with [Claude Code](https://claude.ai/code)
Co-Authored-By: Claude <noreply@anthropic.com>
```
