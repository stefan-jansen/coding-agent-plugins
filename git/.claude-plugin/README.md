# Claude Code Git Plugin

**Version**: 1.0.0
**Category**: Tools
**Author**: Claude Code Framework

## Overview

The Git Plugin provides unified git operations including commits, pull requests, and issue management. It ensures safe, validated git operations with proper attribution and comprehensive documentation.

## Command

### `/git [operation] [arguments]`
Unified git operations - commits, pull requests, and issue management.

**Operations**:
- `commit`: Create safe git commit with validation
- `pr`: Create pull request with documentation
- `issue`: Manage GitHub issues

## Operations

### Git Commit

Create safe git commits with validation and proper attribution.

**Usage**:
```bash
/git commit -m "feat: Add user authentication"
/git commit -m "fix: Resolve login timeout issue"
/git commit -m "docs: Update API documentation"
```

**Features**:
- **Safe Commits**: Uses `git safe-commit` to prevent common mistakes
- **Validation**: Checks for uncommitted changes, conflicts, and issues
- **Attribution**: Automatic co-authorship with Claude
- **Conventional Commits**: Supports conventional commit format
- **Pre-commit Hooks**: Respects repository hooks

**Commit Message Format**:
```
<type>: <description>

[optional body]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Common Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, missing semicolons, etc
- `refactor`: Code change that neither fixes bug nor adds feature
- `perf`: Performance improvement
- `test`: Adding missing tests
- `chore`: Changes to build process or auxiliary tools

**Safety Features**:
1. **Pre-commit Validation**: Runs checks before commit
2. **Conflict Detection**: Identifies merge conflicts
3. **Hook Execution**: Respects pre-commit hooks
4. **Amend Safety**: Only amends own commits, never others
5. **Attribution Check**: Verifies authorship before amend

**Integration with Ship**:
- `/ship` command uses safe commit automatically
- No need to run `/git commit` manually during delivery
- Safe commit is integrated into workflow

---

### Pull Request Creation

Create pull requests with comprehensive documentation.

**Usage**:
```bash
/git pr                                      # Create PR from current branch
/git pr --draft                              # Create draft PR
/git pr --title "Add OAuth2 support"         # Custom title
```

**PR Generation Process**:

1. **Branch Analysis**: Review current branch changes
2. **Commit History**: Analyze all commits since divergence
3. **Change Summary**: Generate comprehensive summary
4. **Documentation**: Create detailed PR description
5. **Test Plan**: Include testing checklist
6. **Attribution**: Add Claude co-authorship note

**PR Description Format**:
```markdown
## Summary
- [Bullet point summary of changes]
- [Key features added]
- [Issues resolved]

## Changes
### [Category 1]
- [Specific change 1]
- [Specific change 2]

### [Category 2]
- [Specific change 3]

## Test Plan
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Documentation updated

## Breaking Changes
[None or description of breaking changes]

## Related Issues
Closes #123
Fixes #456

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Requirements**:
- GitHub CLI (`gh`) must be installed
- Repository must have GitHub remote
- User must be authenticated with `gh auth login`

**Options**:
- `--draft`: Create draft PR (not ready for review)
- `--title "Title"`: Custom PR title
- `--body "Description"`: Custom PR body
- `--base main`: Target branch (default: main/master)

**Integration with Ship**:
- `/ship --pr` creates PR automatically
- Recommended for delivery workflow
- Includes full validation before PR creation

---

### Issue Management

Create and manage GitHub issues.

**Usage**:
```bash
/git issue create --title "Bug: Login fails"
/git issue create --title "Feature: Add OAuth" --label enhancement
/git issue list                              # List open issues
/git issue view 123                          # View issue #123
/git issue close 123                         # Close issue #123
```

**Issue Creation**:
```bash
/git issue create \
  --title "Bug: Login timeout after 30 seconds" \
  --body "Description of issue..." \
  --label bug \
  --assignee username
```

**Issue Labels**:
- `bug`: Bug report
- `enhancement`: Feature request
- `documentation`: Documentation improvement
- `question`: Question or discussion
- `help wanted`: Community help needed
- `good first issue`: Good for newcomers

**Requirements**:
- GitHub CLI (`gh`) must be installed
- Repository must have GitHub remote
- User must be authenticated

## Capabilities

### Safe Commits

**Integrated With**: `/ship`, `/next` commands

**Safety Checks**:
1. **Staged Changes**: Verifies files staged for commit
2. **Conflicts**: Checks for merge conflicts
3. **Hooks**: Respects pre-commit hooks
4. **Attribution**: Validates authorship
5. **Message Format**: Validates commit message

**Auto-Amend Logic**:
```
If pre-commit hook modifies files:
  1. Check authorship (git log -1 --format='%an %ae')
  2. Check not pushed (git status shows "ahead")
  3. If both true: Amend commit
  4. Else: Create new commit
```

**Never Amend When**:
- Commit authored by someone else
- Commit already pushed to remote
- User explicitly requests no amend

---

### Pull Request Creation

**Integrated With**: `/ship --pr` command

**PR Workflow**:
1. **Validate State**: Ensure branch up-to-date, no uncommitted changes
2. **Analyze Changes**: Review full diff from base branch
3. **Generate Description**: Create comprehensive PR summary
4. **Create PR**: Use `gh pr create` with generated content
5. **Return URL**: Provide PR link to user

**PR Quality**:
- **Comprehensive Summary**: Covers all changes
- **Categorized Changes**: Organized by type
- **Test Plan**: Checklist for reviewers
- **Issue References**: Links to related issues
- **Attribution**: Claude co-authorship noted

---

### Issue Management

**Commands**:
- `create`: Create new issue
- `list`: List issues (open, closed, all)
- `view`: View issue details
- `close`: Close issue
- `reopen`: Reopen closed issue
- `comment`: Add comment to issue

**Use Cases**:
- Bug reporting during development
- Feature request tracking
- Discussion and questions
- Community engagement

## Configuration

### Plugin Settings

```json
{
  "settings": {
    "defaultEnabled": true,
    "category": "tools"
  }
}
```

### Dependencies

```json
{
  "dependencies": {
    "claude-code-core": "^1.0.0"
  }
}
```

### System Requirements

```json
{
  "systemRequirements": {
    "git": {
      "required": true,
      "minVersion": "2.0.0"
    },
    "gh": {
      "required": false,
      "description": "GitHub CLI for pull request and issue management"
    }
  }
}
```

**Git**: Required for all operations
**GitHub CLI**: Required only for PR and issue operations

### MCP Tools

**None** - Git plugin operates independently of MCP tools.

**Graceful Degradation**: All features work in standard environments.

## Best Practices

### Commits

✅ **Do**:
- Use conventional commit format
- Write clear, descriptive messages
- Commit related changes together
- Include "why" in commit body for complex changes
- Let `/ship` handle commits during delivery

❌ **Don't**:
- Use `git commit` directly (use `git safe-commit` or `/git commit`)
- Commit without running tests first
- Make commits too large (split into logical chunks)
- Skip commit messages or use vague messages like "fixes"
- Amend commits authored by others

### Pull Requests

✅ **Do**:
- Create PR from feature branch
- Include comprehensive test plan
- Reference related issues
- Request review from appropriate team members
- Use `/ship --pr` for automatic PR creation

❌ **Don't**:
- Create PR with failing tests
- Submit PR without description
- Include unrelated changes
- Push to PR after review without notification
- Create PR from main/master branch

### Issues

✅ **Do**:
- Use clear, specific titles
- Include reproduction steps for bugs
- Add appropriate labels
- Link related PRs and issues
- Respond to comments promptly

❌ **Don't**:
- Create duplicate issues (search first)
- Use vague titles like "it doesn't work"
- Skip issue template sections
- Close issues without resolution
- Leave issues open indefinitely without updates

## Integration with Workflow

### With `/explore`
- Create issues for discovered requirements
- Reference issues in exploration notes

### With `/plan`
- Link plan tasks to GitHub issues
- Create issues for identified work items

### With `/next`
- Commit after each task completion
- Use safe commit automatically

### With `/ship`
- Create final commit with all changes
- Generate PR with comprehensive docs
- Link PR to related issues
- Mark issues as resolved

## Workflow Examples

### Example 1: Feature Development with PR

```bash
# Development
git checkout -b feature/oauth2
# ... implement feature ...

# Commit during development
/git commit -m "feat: Add OAuth2 authentication"
/git commit -m "test: Add OAuth2 integration tests"
/git commit -m "docs: Update authentication docs"

# Create PR
/git pr --title "Add OAuth2 authentication support"
# Or use ship command
/ship --pr
```

### Example 2: Bug Fix with Issue

```bash
# Create issue
/git issue create \
  --title "Bug: Login timeout after 30 seconds" \
  --label bug

# Fix bug
git checkout -b fix/login-timeout
# ... fix issue ...

# Commit fix
/git commit -m "fix: Resolve login timeout issue

Increased timeout to 60 seconds and added retry logic.

Fixes #123"

# Ship fix
/ship --pr
```

### Example 3: Collaborative Development

```bash
# Check open issues
/git issue list

# Pick issue
/git issue view 456
git checkout -b feature/issue-456

# Implement
# ... development ...

# Commit
/git commit -m "feat: Implement feature from #456"

# Create PR linking issue
/git pr --title "Implement feature XYZ" --body "Closes #456"
```

## Troubleshooting

### GitHub CLI Not Found

**Symptom**: `/git pr` shows "gh command not found"

**Solution**: Install GitHub CLI:
```bash
# macOS
brew install gh

# Linux
sudo apt install gh

# Authenticate
gh auth login
```

### Push Permission Denied

**Symptom**: Cannot push to remote

**Solution**: Set up authentication:
```bash
# SSH
ssh-keygen -t ed25519
gh ssh-key add ~/.ssh/id_ed25519.pub

# HTTPS
gh auth login --web
```

### Pre-commit Hook Fails

**Symptom**: Commit fails with hook error

**Solution**: Fix hook issues or bypass if necessary:
```bash
# Fix the issue (preferred)
# ... fix linting, tests, etc. ...

# Or skip hooks (use sparingly)
git commit --no-verify
```

### PR Creation Fails

**Symptom**: `/git pr` shows error

**Solutions**:
1. Verify branch pushed to remote:
   ```bash
   git push -u origin feature-branch
   ```
2. Check GitHub CLI authenticated:
   ```bash
   gh auth status
   ```
3. Verify repository has GitHub remote:
   ```bash
   git remote -v
   ```

### Wrong Remote Branch

**Symptom**: PR targets wrong branch

**Solution**: Specify base branch explicitly:
```bash
/git pr --base develop
```

## Performance

### Operation Times

- **Commit**: <1 second (excluding pre-commit hooks)
- **PR Creation**: 2-5 seconds (including analysis)
- **Issue Creation**: 1-2 seconds
- **Issue List**: 1-2 seconds

### Pre-commit Hooks

Hook execution time depends on repository configuration:
- **Fast** (<5s): Linting, formatting
- **Medium** (5-30s): Unit tests
- **Slow** (>30s): Integration tests, builds

Consider hook optimization for frequently-committing workflows.

## Security Considerations

### Commit Attribution

All commits include Claude co-authorship:
```
Co-Authored-By: Claude <noreply@anthropic.com>
```

This ensures transparency about AI-assisted development.

### Sensitive Information

**Never commit**:
- API keys, tokens, passwords
- Private keys, certificates
- Personal data
- Proprietary code (in public repos)

Use `.gitignore` and pre-commit hooks to prevent accidental commits.

### Branch Protection

Recommended GitHub branch protection rules:
- Require pull request reviews
- Require status checks to pass
- Enforce linear history
- Require signed commits (optional)

## Version History

### 1.0.0 (2025-10-11)
- Initial plugin release
- Safe commit integration
- PR creation with comprehensive docs
- GitHub issue management
- Integration with workflow plugin

## License

MIT License - See project LICENSE file

## Related Plugins

- **core**: Required dependency
- **workflow**: Integrated with `/ship` for commits and PRs
- **development**: Code review integrates with PRs

## Additional Resources

- Git Documentation: https://git-scm.com/doc
- GitHub CLI Documentation: https://cli.github.com/manual/
- Conventional Commits: https://www.conventionalcommits.org/
- GitHub Flow: https://guides.github.com/introduction/flow/

---

**Note**: This plugin ensures safe, validated git operations with proper attribution. Always use `/git commit` or let workflow commands handle commits automatically.
