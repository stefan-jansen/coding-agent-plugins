# Agents Plugin

**Purpose**: Specialized agent invocation and semantic code understanding
**Category**: Agents
**Version**: 1.0.0

## Overview

The Agents plugin provides meta-tools for invoking specialized agents and activating semantic code understanding. These are orchestration capabilities that invoke other AI capabilities for specific tasks.

## Commands (2)

### /agent
**Purpose**: Direct invocation of specialized agents with explicit context

Invoke specialized agents for focused tasks:
- Architectural design and decisions
- Test creation and coverage analysis
- Code quality and security review
- Compliance and framework validation
- Report generation

**Usage**:
```bash
/agent <agent-name> "<task>"

# Examples
/agent architect "Design authentication system architecture"
/agent test-engineer "Create test suite for payment processing"
/agent code-reviewer "Review security of API endpoints"
/agent auditor "Validate framework compliance"
/agent report-generator "Generate stakeholder report"
```

**Available Agents**:
- **architect** - System design and architectural decisions
- **test-engineer** - Test creation and coverage analysis
- **code-reviewer** - Code quality and security review
- **auditor** - Compliance and framework validation
- **reasoning-specialist** - Complex analysis and structured reasoning
- **report-generator** - Professional stakeholder reports

### /serena
**Purpose**: Activate and manage Serena semantic code understanding for projects

Activate Serena MCP for semantic code operations:
- Find symbols by name (70-90% token reduction vs grep)
- Replace symbol bodies with precision
- Get symbols overview for files
- Activate projects for semantic context

**Usage**:
```bash
/serena                          # Activate for current project
/serena --update                 # Update semantic index
/serena --status                 # Check Serena status
```

**Benefits**:
- **70-90% token reduction** on code-heavy tasks vs text search
- **Precise symbol manipulation** without manual editing
- **Semantic understanding** of code structure
- **Fast navigation** to definitions and implementations

**Requirements**:
- Serena MCP server installed and configured
- Per-project activation (one-time setup)
- Graceful degradation to grep when unavailable

## Integration

### Specialized Agents
The `/agent` command provides unified interface to invoke:
- Core agents (architect, test-engineer, code-reviewer, auditor, reasoning-specialist)
- Report agents (report-generator for stakeholder communications)

### Serena MCP
The `/serena` command activates semantic code understanding:
- Integrates with Serena MCP server
- Provides semantic alternatives to grep/text search
- Enables precise symbol manipulation
- Gracefully degrades when MCP unavailable

### Other Plugins
- **development** plugin uses agents for code review and testing
- **workflow** plugin can invoke agents during task execution
- **system** plugin audit command may use auditor agent

## Use Cases

### Architecture Design
```bash
/agent architect "Design microservices architecture for payment system"
# Returns detailed architectural plan with diagrams and rationale
```

### Test Creation
```bash
/agent test-engineer "Create comprehensive test suite for authentication"
# Returns test plan and implementation
```

### Code Review
```bash
/agent code-reviewer "Review security of user input handling"
# Returns security analysis with specific findings
```

### Framework Validation
```bash
/agent auditor "Validate Claude Code framework compliance"
# Returns compliance report with recommendations
```

### Semantic Code Operations
```bash
/serena                          # Activate semantic understanding
# Now can use Serena MCP for fast symbol operations

# Example: Find and modify symbol
# Uses find_symbol() instead of grep (70-90% fewer tokens)
# Uses replace_symbol_body() for precise edits
```

## Best Practices

### Agent Invocation
- **Be specific** in task descriptions - agents work best with clear context
- **One task per invocation** - don't combine multiple responsibilities
- **Review agent output** - agents provide recommendations, you make decisions
- **Iterate** - invoke multiple times with refinements as needed

### Serena Usage
- **Activate per-project** - Serena requires one-time project activation
- **Use for code operations** - Serena excels at symbol finding/manipulation
- **Fallback gracefully** - Commands work without Serena (just less efficient)
- **Update periodically** - Keep semantic index fresh with `--update`

### When to Use Agents
✅ **Use agents for**:
- Complex architectural decisions requiring expertise
- Comprehensive test suite creation
- Security-focused code review
- Framework compliance validation
- Complex analysis requiring structured reasoning
- Professional report generation

❌ **Don't use agents for**:
- Simple code changes (use direct tools)
- Quick grep searches (use grep or Serena directly)
- Tasks you already know how to do efficiently

## Migration from Core Plugin

These commands moved from the `core` plugin (v0.9.x):
- `agent` - Was `/core/agent`
- `serena` - Was `/core/serena`

Command names and behavior unchanged. Only organizational change.

## MCP Integration

### Serena MCP
**Token Efficiency**: 70-90% reduction on code operations
**Capabilities**:
- `find_symbol(name, file)` - Find symbols by name
- `replace_symbol_body(name, file, new_body)` - Replace symbol implementation
- `get_symbols_overview(file)` - Get file symbol structure
- `activate_project(path)` - Activate semantic indexing

**Setup**:
1. Install Serena MCP server
2. Run `/serena` in project (one-time activation)
3. Use semantic operations in commands

**Graceful Degradation**:
- `find_symbol()` → grep fallback
- `replace_symbol_body()` → manual editing
- `get_symbols_overview()` → file reading

## Dependencies

None - Agents plugin is standalone.

Optional:
- **Serena MCP** - For semantic code understanding (graceful degradation)

## See Also

- **development** plugin - Uses agents for code review and testing
- **workflow** plugin - May invoke agents during task execution
- **system** plugin - Audit command uses auditor agent

---

**Maintained by**: Claude Code Framework Team
**Version**: 1.0.0
**Last Updated**: 2025-10-18
