# Claude Code Core Plugin

**Version**: 1.0.0
**Category**: Core (Required)
**Author**: Claude Code Framework

## Overview

The Core Plugin provides essential system functionality for Claude Code. This plugin is **required** and cannot be disabled. It includes fundamental commands for project management, configuration, monitoring, and system operations.

## Commands

### Project Management

#### `/status [verbose]`
Display current project and task status.

**Usage**:
```bash
/status           # Quick status overview
/status verbose   # Detailed status with metrics
```

**Shows**:
- Current work unit and phase
- Active tasks and completion status
- Git branch and changes
- Recent activity

#### `/work [subcommand] [args]`
Manage work units and parallel work streams.

**Subcommands**:
- `list [filter]`: List work units (active/paused/completed/all)
- `continue [unit-id]`: Resume work on specific unit
- `checkpoint`: Save current work state
- `switch [unit-id]`: Switch to different work unit

**Usage**:
```bash
/work list                    # List active work units
/work list all                # List all work units
/work continue 001            # Continue work unit 001
/work checkpoint              # Save current state
/work switch 002              # Switch to work unit 002
```

#### `/config [subcommand] [key] [value]`
Manage framework settings and project preferences.

**Subcommands**:
- `get [key]`: Get configuration value
- `set [key] [value]`: Set configuration value
- `list`: List all configuration values

**Usage**:
```bash
/config list                          # List all settings
/config get memory.max_size           # Get specific setting
/config set git.auto_commit true      # Set configuration
```

### System Operations

#### `/cleanup [options]`
Clean up Claude-generated clutter and consolidate documentation.

**Options**:
- `--dry-run`: Preview what would be cleaned
- `--auto`: Auto-approve all cleanups
- `root`: Clean project root duplicates
- `tests`: Clean test output files
- `reports`: Clean old reports
- `work`: Clean completed work units
- `all`: Clean everything

**Usage**:
```bash
/cleanup --dry-run            # Preview cleanup
/cleanup root                 # Clean project root
/cleanup all                  # Clean everything
```

#### `/index [options]`
Create and maintain persistent project understanding.

**Options**:
- `--update`: Update existing index
- `--refresh`: Rebuild index from scratch
- `[focus_area]`: Index specific area

**Usage**:
```bash
/index                        # Create initial index
/index --update               # Update existing index
/index src/                   # Index specific directory
```

#### `/performance`
View token usage and performance metrics.

**Shows**:
- Session token usage
- Command execution times
- MCP tool performance
- Memory efficiency metrics

### Development Support

#### `/agent <agent-name> "<task>"`
Direct invocation of specialized agents.

**Available Agents**:
- `architect`: System design and architectural decisions
- `test-engineer`: Test creation and coverage analysis
- `code-reviewer`: Code review and quality assurance
- `auditor`: Compliance and framework validation
- `data-scientist`: ML experiments and data analysis

**Usage**:
```bash
/agent architect "Design authentication system"
/agent test-engineer "Create tests for UserService"
/agent code-reviewer "Review changes in src/auth/"
```

#### `/docs [subcommand] [args]`
Unified documentation operations.

**Subcommands**:
- `fetch [url]`: Fetch external documentation
- `search [query]`: Search all documentation
- `generate [scope]`: Generate project documentation

**Usage**:
```bash
/docs search "authentication"         # Search docs
/docs fetch https://api-docs.com      # Fetch external docs
/docs generate api                    # Generate API docs
```

#### `/add-command [name] [description]`
Create new custom slash commands.

**Usage**:
```bash
/add-command deploy "Deploy application to production"
```

Creates command template at `.claude/commands/deploy.md` ready for customization.

### Quality & Maintenance

#### `/audit [options]`
Framework setup and infrastructure compliance audit.

**Options**:
- `--framework`: Audit framework setup
- `--tools`: Audit tool installations
- `--fix`: Auto-fix issues found

**Usage**:
```bash
/audit                        # Full audit
/audit --framework            # Framework only
/audit --tools --fix          # Audit and fix tools
```

#### `/serena [options]`
Activate and manage Serena semantic code understanding.

**Options**:
- `activate`: Enable Serena for project
- `status`: Check Serena status
- `reindex`: Rebuild semantic index

**Usage**:
```bash
/serena activate              # Enable Serena
/serena status                # Check status
/serena reindex               # Rebuild index
```

### Session Management

#### `/handoff [message]`
Create transition documents with context analysis.

**Usage**:
```bash
/handoff "Completed auth refactor, ready for testing"
```

Creates handoff document in `.claude/transitions/` with:
- Current context and state
- Work completed
- Next steps
- Token usage analysis

#### `/spike [topic] [duration]`
Time-boxed exploration in isolated branch.

**Usage**:
```bash
/spike "graphql-integration" 2h
```

Creates isolated branch for exploration with time limit.

### Project Setup

#### `/setup [type] [name] [options]`
Initialize new projects with Claude framework integration.

**Types**:
- `explore`: Explore project before setup
- `existing`: Setup in existing project
- `python`: New Python project
- `javascript`: New JavaScript project

**Options**:
- `--minimal`: Minimal setup
- `--standard`: Standard setup (default)
- `--full`: Full setup with all features
- `--init-user`: Initialize user configuration
- `--statusline`: Setup status line

**Usage**:
```bash
/setup explore                        # Explore before setup
/setup existing my-project            # Setup existing project
/setup python new-app --standard      # New Python project
/setup --init-user                    # Initialize user config
```

## Capabilities

The core plugin provides 14 essential capabilities:

1. **Status Monitoring**: Project and task status tracking
2. **Work Management**: Parallel work stream management
3. **Configuration Management**: Settings and preferences
4. **Agent Invocation**: Direct agent access
5. **Project Cleanup**: Clutter removal and consolidation
6. **Project Indexing**: Persistent understanding
7. **Performance Monitoring**: Token and efficiency metrics
8. **Session Handoff**: Context preservation
9. **Documentation Operations**: Unified doc management
10. **Project Setup**: New project initialization
11. **Command Creation**: Custom command scaffolding
12. **Framework Audit**: Compliance checking
13. **Serena Setup**: Semantic code understanding
14. **Spike Exploration**: Time-boxed investigations

## Configuration

### Plugin Settings

```json
{
  "settings": {
    "defaultEnabled": true,
    "category": "core",
    "required": true
  }
}
```

**Note**: This plugin is **required** and always enabled.

### MCP Integration

**Optional MCP Tools**:
- `sequential-thinking`: Enhanced structured reasoning
- `serena`: Semantic code understanding

**Graceful Degradation**: All features work without MCP tools, with fallback behavior.

## Dependencies

**None** - Core plugin has no dependencies as it provides foundation for all other plugins.

## File Organization

```
plugins/core/
└── .claude-plugin/
    ├── plugin.json           # Plugin manifest
    ├── README.md             # This file
    └── commands/             # Command implementations
        ├── status.md
        ├── work.md
        ├── config.md
        ├── agent.md
        ├── cleanup.md
        ├── index.md
        ├── performance.md
        ├── handoff.md
        ├── docs.md
        ├── setup.md
        ├── add-command.md
        ├── audit.md
        ├── serena.md
        └── spike.md
```

## Integration Points

### With Workflow Plugin
- Work management integrates with `/next` and `/ship`
- Handoff supports workflow transitions
- Status displays workflow state

### With Development Plugin
- Agent invocation used by development commands
- Audit checks development tool setup
- Performance monitors development operations

### With Memory Plugin
- Configuration includes memory settings
- Status shows memory usage
- Cleanup consolidates memory files

### With Git Plugin
- Status shows git state
- Handoff creates git-friendly transitions
- Cleanup respects gitignore

## Best Practices

### Status Monitoring
- Run `/status` at session start
- Use `/status verbose` when context >80%
- Check status before handoffs

### Work Management
- Use `/work checkpoint` regularly
- Switch work units to maintain focus
- List completed work for accountability

### Configuration
- Review `/config list` periodically
- Set project-specific preferences in `.claude/settings.json`
- Use global settings in `~/.claude/settings.json`

### Cleanup
- Run `/cleanup --dry-run` weekly
- Clean completed work quarterly
- Use `--auto` for trusted cleanups

### Performance
- Monitor `/performance` every 10-15 interactions
- Optimize at 80% token threshold
- Use handoff when approaching limits

## Troubleshooting

### Command Not Found

**Symptom**: `/status` shows "Command not found"

**Solution**: Core plugin is required and should always be enabled. If missing:
```bash
/config plugin enable claude-code-core
```

### Configuration Not Persisting

**Symptom**: Settings reset after restart

**Solution**: Check settings file permissions:
```bash
ls -la ~/.claude/settings.json
ls -la .claude/settings.json
```

### Work Unit Corruption

**Symptom**: `/work list` shows corrupted state

**Solution**: Rebuild work unit state:
```bash
# Backup current state
cp .claude/work/current/*/state.json ~/state-backup.json

# Reset work directory
/cleanup work

# Restore from backup
```

### Performance Degradation

**Symptom**: Commands running slowly

**Solutions**:
1. Check token usage: `/performance`
2. Run cleanup: `/cleanup all`
3. Create handoff: `/handoff`
4. Clear conversation after handoff

## Version History

### 1.0.0 (2025-10-11)
- Initial plugin release
- 14 core commands
- MCP integration support
- Work unit management
- Session handoff capabilities

## License

MIT License - See project LICENSE file

## Related Plugins

- **workflow**: Development workflow (depends on core)
- **development**: Development tools (depends on core)
- **git**: Version control (depends on core)
- **memory**: Context management (standalone, integrates with core)

---

**Note**: This is a required plugin and provides foundation for all Claude Code functionality. Do not disable.
