---
allowed-tools: [Read, Bash, Task, Write, MultiEdit]
argument-hint: "commit|pr|issue [arguments]"
description: Unified git operations - commits, pull requests, and issue management
---

# Git Operations Hub

Consolidated command for all git-related operations. Combines commit, PR, and issue workflows into a single interface.

**Input**: $ARGUMENTS

## Usage

### Commit Operations
```bash
/git commit "feat: Add user authentication"
/git commit                               # Interactive commit message
```

### Pull Request Operations
```bash
/git pr                                   # Create PR from current branch
/git pr --draft                          # Create draft PR
```

### Issue Operations
```bash
/git issue "#123"                         # Start work on GitHub issue
/git issue "Fix login bug"               # Work on issue by title
```

## Phase 1: Parse Operation Type

Based on the arguments provided: $ARGUMENTS

I'll determine which git operation to perform:

- If arguments start with "commit": Handle git commit workflow
- If arguments start with "pr": Handle pull request creation
- If arguments start with "issue": Handle GitHub issue workflow
- If no arguments: Show usage help

## Phase 2: Execute Git Commit Workflow

When handling commit operations:

### Pre-Commit Validation
1. Check git status to see what files are staged/modified
2. Ensure we're in a git repository
3. Validate that there are changes to commit

### Quality Gates
1. Run available tests (if any exist)
2. Check for linting issues (if tools available)
3. Verify no secrets or sensitive data being committed

### Commit Creation
1. Stage appropriate files if needed
2. Generate conventional commit message if not provided
3. Execute git commit with proper formatting
4. Include Claude Code attribution

## Phase 3: Execute Pull Request Workflow

When handling PR operations:

### Pre-PR Validation
1. Ensure we're on a feature branch (not main/master)
2. Check that commits exist beyond main branch
3. Verify branch is pushed to remote

### PR Creation
1. Use GitHub CLI (gh) if available
2. Generate meaningful PR title and description
3. Include summary of changes made
4. Link to relevant issues if applicable
5. Set appropriate labels and reviewers

### Quality Information
1. Include test status in PR description
2. Note any breaking changes
3. Highlight areas needing special review attention

## Phase 4: Execute Issue Workflow

When handling issue operations:

### Issue Resolution
1. Parse issue number or search by title
2. Create feature branch named appropriately
3. Update local context with issue details
4. Set up work unit tracking if needed

### Issue Context
1. Extract issue requirements and acceptance criteria
2. Identify related files and components
3. Plan implementation approach
4. Document work started in commit messages

## Phase 5: Quality Verification

For all git operations:

### Verification Steps
1. Confirm operation completed successfully
2. Show current git status
3. Display next recommended steps
4. Update any tracking systems

### Error Handling
1. Provide clear error messages for failures
2. Suggest remediation steps
3. Preserve work in progress when possible
4. Guide user to resolution

## Success Indicators

- ✅ Git operation completed without errors
- ✅ Proper conventional commit format used
- ✅ Quality gates passed (tests, linting)
- ✅ No sensitive data committed
- ✅ Clear audit trail in git history
- ✅ Appropriate branch management
- ✅ PR/Issue properly linked and documented

## Examples

### Smart Commit
```bash
/git commit "feat: Add JWT authentication middleware"
# → Runs tests, checks linting, creates conventional commit
```

### Draft PR Creation
```bash
/git pr --draft
# → Creates draft PR with auto-generated description
```

### Issue Workflow
```bash
/git issue "#42"
# → Creates feature branch, updates context, starts work tracking
```

---

*Consolidated git operations command with quality gates and proper workflow automation.*