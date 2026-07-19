# System Plugin

**Purpose**: System configuration and health monitoring
**Category**: System
**Version**: 1.0.0

## Overview

The System plugin provides essential commands for configuring, monitoring, and maintaining Claude Code installations. These are system-level operations that configure or monitor Claude Code itself.

## Commands (9)

### /system:status
**Purpose**: Unified view of work, system, and memory state

Provides comprehensive status overview including:
- Active work units and progress
- Memory system state
- System configuration health
- Recent activity summary

**Usage**:
```bash
/system:status              # Standard status view
/system:status verbose      # Detailed status with full context
```

### /config
**Purpose**: Manage Claude Code configuration settings

Interactive configuration management:
- View current settings
- Update configuration
- Reset to defaults
- Validate configuration

**Usage**:
```bash
/config              # View current configuration
/config set key=value
/config reset
```

> **Project setup moved to the `setup` plugin.** Use `/setup` (interview-driven
> bootstrap of the current project) and `/setup:user` (global user config). The
> old `/setup:python`, `/setup:javascript`, `/setup:existing`,
> `/setup:statusline` commands and the `system:project-setup` skill were
> consolidated into `/setup`.

### /audit
**Purpose**: Validate framework compliance and configuration

Comprehensive framework validation:
- Configuration compliance checks
- Directory structure validation
- Memory system health
- Work unit integrity
- Best practices verification

**Usage**:
```bash
/audit                   # Full audit
/audit --framework       # Framework structure only
/audit --fix             # Auto-fix issues where possible
```

### /cleanup
**Purpose**: Clean up generated files and temporary data

Intelligent cleanup operations:
- Remove Claude-generated clutter
- Consolidate documentation
- Archive completed work
- Free up disk space

**Options**:
```bash
/cleanup --dry-run       # Preview what would be cleaned
/cleanup --auto          # Auto-cleanup with safe defaults
/cleanup root            # Clean project root only
/cleanup tests           # Clean test artifacts
/cleanup reports         # Clean old reports
/cleanup work            # Archive completed work units
/cleanup all             # Comprehensive cleanup
```

## Integration

### Memory System
- `system:status` command integrates with memory to show context state
- `audit` validates memory structure and health

### Work Units
- `system:status` shows active work unit progress
- `audit` validates work unit integrity
- `cleanup` can archive completed work units

### MCP Tools
- **Sequential Thinking** (optional): Enhanced status analysis and audit reasoning
- Graceful degradation when MCP unavailable

## Use Cases

### Daily Workflow
```bash
/system:status                  # Check what's happening
# ... do work ...
/system:status verbose          # Review progress before handoff
```

### Project Initialization
```bash
/setup                   # Interview-driven bootstrap of the current project (setup plugin)
/audit                   # Verify setup correct
```

### Maintenance
```bash
/audit                   # Check framework health
/cleanup --dry-run       # See what can be cleaned
/cleanup all             # Clean up clutter
```

### Configuration Management
```bash
/config                  # Review current settings
/config set memory.auto_gc=true
/audit                   # Verify configuration valid
```

## Best Practices

### System Health
- Run `/system:status` at session start to understand current state
- Run `/audit` periodically to catch configuration drift
- Use `/cleanup` when projects accumulate clutter

### Configuration
- Use `/config` to view before modifying manually
- Run `/audit` after configuration changes
- Keep configuration in version control

### Setup
- Use `/setup` to bootstrap the current project (empty or existing); it detects
  the language and interviews you for the `AGENTS.md` content
- Use `/setup:user` once to configure global preferences

## Migration Notes

### From Core Plugin (v0.9.x)
These commands moved from the `core` plugin:
- `status` → `/system:status` (renamed to avoid conflict with native /status)
- `config` - Was `/core/config`
- `setup` - Was `/core/setup`
- `audit` - Was `/core/audit`
- `cleanup` - Was `/core/cleanup`

### Name Change (v1.1.0)
- `/status` → `/system:status` to avoid conflict with Claude Code native `/status` command

## Dependencies

None - System plugin is foundational.

## See Also

- **workflow** plugin - Task workflow management
- **memory** plugin - Knowledge and context management
- **development** plugin - Development tools

---

**Maintained by**: Claude Code Framework Team
**Version**: 1.0.0
**Last Updated**: 2025-10-18
