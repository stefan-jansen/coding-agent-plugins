---
allowed-tools: [Bash, Read, Write, Grep, Glob, MultiEdit]
argument-hint: "[--framework | --tools | --fix]"
description: "Framework setup and infrastructure compliance audit"
---

# Framework Infrastructure Audit

Validates Claude Code framework setup, tool installation, and infrastructure compliance.

**Input**: $ARGUMENTS

## Usage

```bash
/audit                    # Full infrastructure audit
/audit --framework        # Focus on framework setup only
/audit --tools           # Focus on tool installation
/audit --fix             # Apply fixes for detected issues
```

## Phase 1: Framework Setup Validation

### Directory Structure Audit
1. Verify `.claude/` directory exists and has proper structure
2. Check for required subdirectories: `work/`, `memory/`, `reference/`
3. Validate permissions on framework directories
4. Ensure proper gitignore entries for sensitive files

### Configuration Validation
1. Check `settings.json` exists and has valid syntax
2. Validate hook configurations if present
3. Verify tool permissions are properly configured
4. Ensure CLAUDE.md hierarchy is properly structured

### Memory System Health
1. Verify memory files are not corrupted
2. Check import links are valid (no broken @references)
3. Validate memory file sizes are within limits
4. Ensure session memory is properly rotated

## Phase 2: Tool Installation Audit

### Core Dependencies
1. **Git**: Version check, configuration validation
2. **Python Tools**: ruff, black, mypy, pytest availability
3. **JavaScript Tools**: eslint, prettier, jest (if applicable)
4. **System Tools**: jq, flock, timeout, mktemp

### Git Configuration
1. Verify `git safe-commit` alias is configured
2. Check user name and email are set
3. Validate pre-commit hooks are installed
4. Ensure conventional commit format is enforced

### Language-Specific Tools
1. **Python Projects**: Check pyproject.toml, requirements.txt
2. **JavaScript Projects**: Validate package.json, node_modules
3. **Go Projects**: Verify go.mod, tool installations
4. **Rust Projects**: Check Cargo.toml, rust toolchain

## Phase 3: Quality Infrastructure Audit

### Code Quality Tools
1. Verify linting tools are properly configured
2. Check formatting tools work correctly
3. Validate type checking is enabled where appropriate
4. Ensure test runners are properly set up

### Git Workflow Validation
1. Check branch protection rules (if applicable)
2. Validate commit message format enforcement
3. Verify pre-commit hooks are functioning
4. Ensure proper gitignore configurations

### Security Compliance
1. Check for exposed secrets in git history
2. Validate file permissions are secure
3. Ensure sensitive files are properly ignored
4. Verify hook scripts have appropriate permissions

## Phase 4: Work Unit System Audit

### Work Unit Health Check
1. Verify work unit directory structure is correct
2. Check state.json files have valid syntax
3. Validate work unit metadata is consistent
4. Ensure proper archival of completed work

### State Management Validation
1. Check JSON schema compliance for state files
2. Verify task state transitions are logical
3. Validate work unit tracking is accurate
4. Ensure proper cleanup of temporary files

## Phase 5: Performance and Maintenance

### Performance Audit
1. Check for oversized memory files that need compression
2. Identify slow or inefficient command configurations
3. Validate context window usage is optimal
4. Ensure proper cleanup of temporary artifacts

### Maintenance Recommendations
1. Identify outdated dependencies needing updates
2. Suggest optimizations for frequently used workflows
3. Recommend cleanup for accumulated artifacts
4. Propose improvements for identified bottlenecks

## Phase 6: Fix Recommendations

### Automatic Fixes (if --fix specified)
1. Install missing dependencies where possible
2. Configure git safe-commit alias if missing
3. Create missing directory structures
4. Fix common configuration issues

### Manual Fix Guidance
1. Provide specific commands for complex fixes
2. Recommend tool-specific configuration changes
3. Suggest workflow improvements
4. Document required manual interventions

## Success Indicators

- ✅ All framework directories exist with proper permissions
- ✅ Git is properly configured with safe-commit alias
- ✅ Required development tools are installed and working
- ✅ Code quality tools are configured correctly
- ✅ Work unit system is functioning properly
- ✅ Memory system is healthy and optimized
- ✅ Security compliance is maintained
- ✅ No critical infrastructure issues detected

## Common Issues and Solutions

### Missing Dependencies
- **Problem**: Tool not found in PATH
- **Solution**: Install via package manager or update PATH

### Git Configuration Issues
- **Problem**: safe-commit alias missing
- **Solution**: `git config --global alias.safe-commit '!f() { git add -A && git commit "$@"; }; f'`

### Permission Problems
- **Problem**: Cannot write to framework directories
- **Solution**: Check ownership and permissions with `ls -la`

### Corrupted Work Units
- **Problem**: Invalid JSON in state files
- **Solution**: Restore from backup or recreate work unit

## Examples

### Full Audit
```bash
/audit
# → Comprehensive check of all infrastructure components
```

### Tool-Focused Audit
```bash
/audit --tools
# → Focus only on development tool installation and configuration
```

### Auto-Fix Mode
```bash
/audit --fix
# → Detect issues and apply automatic fixes where possible
```

---

*Infrastructure validation command ensuring Claude Code framework is properly configured and maintained.*