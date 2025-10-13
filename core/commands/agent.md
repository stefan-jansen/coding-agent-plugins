---
allowed-tools: [Task, Read, Write]
argument-hint: "<agent-name> \"<task>\""
description: Direct invocation of specialized agents with explicit context
---

# Agent Invocation

Direct invocation of specialized agents for complex tasks. Provides explicit control over which agent handles specific work.

**Input**: $ARGUMENTS

## Phase 1: Agent Selection and Task Analysis

Based on the provided arguments: $ARGUMENTS

I'll parse the request to identify the target agent and task:

### Available Agents

- **architect**: System design, technology decisions, architectural patterns
- **test-engineer**: Test creation, TDD workflows, coverage analysis
- **code-reviewer**: Code quality, security analysis, best practices review
- **doc-reviewer**: Documentation quality, completeness, clarity assessment
- **auditor**: Infrastructure verification, compliance, system health

### Task Preparation

I'll analyze the request to:
1. **Identify target agent**: Which specialist is most appropriate
2. **Extract task details**: Clear description of work to be performed
3. **Gather context**: Relevant project information and constraints
4. **Prepare delegation**: Formatted request for agent execution

## Phase 2: Context Assembly

### Project Context Collection

I'll gather relevant context for the agent including:

#### Environmental Information
- **Project type**: Language, framework, architecture
- **Current state**: Git branch, recent changes, active work
- **Development setup**: Tools, configuration, dependencies
- **Quality standards**: Testing, linting, documentation requirements

#### Task-Specific Context
- **Related files**: Code, documentation, configuration relevant to task
- **Previous decisions**: Architectural choices, patterns established
- **Constraints**: Performance, security, compatibility requirements
- **Success criteria**: How to measure task completion

## Phase 3: Agent Invocation

### Specialized Agent Delegation

I'll use the Task tool to invoke the appropriate agent:

**Agent Parameters**:
- **subagent_type**: [Selected agent name from arguments]
- **description**: [Task summary for specialized execution]
- **prompt**: Execute specialized task with full agent expertise:

  **Task Request**: [Complete task description from arguments]

  **Your Role**: Apply your specialized knowledge and protocols as defined in your agent specification.

  **Context Application**: Use the project environment and constraints to inform your approach.

  **Deliverable Requirements**:
  - Clear analysis addressing the specific task
  - Actionable recommendations or implementations
  - Detailed reasoning behind decisions and approaches
  - Specific next steps for continued progress

  **Quality Standards**:
  - Challenge assumptions and validate approaches
  - Provide genuine insights, not just compliance responses
  - Document thought process and decision rationale
  - Follow anti-sycophancy protocols and quality standards

  **Project Integration**: Ensure recommendations fit project constraints, standards, and architectural decisions.

## Phase 4: Agent-Specific Execution Patterns

### Architect Agent Tasks
For system design and architectural decisions:
- **Technology evaluation**: Framework and tool selection
- **System design**: Component architecture and interaction patterns
- **Scalability planning**: Performance and growth considerations
- **Integration planning**: External system and API design

### Test-Engineer Agent Tasks
For testing and quality assurance:
- **Test strategy development**: Comprehensive testing approach
- **TDD implementation**: Red-Green-Refactor cycle execution
- **Coverage analysis**: Gap identification and improvement
- **Quality metrics**: Testing standards and measurement

### Code-Reviewer Agent Tasks
For code quality and security:
- **Security analysis**: Vulnerability assessment and mitigation
- **Code quality review**: Standards compliance and best practices
- **Performance evaluation**: Optimization opportunities
- **Maintainability assessment**: Long-term code health

### Documentation Reviewer Tasks
For documentation quality:
- **Completeness assessment**: Coverage of all features and APIs
- **Clarity evaluation**: User comprehension and usability
- **Accuracy verification**: Documentation matches implementation
- **Organization review**: Structure and navigation optimization

### Auditor Agent Tasks
For infrastructure and compliance:
- **System validation**: Configuration and setup verification
- **Compliance checking**: Standards and requirement adherence
- **Security auditing**: Infrastructure security assessment
- **Performance monitoring**: System health and optimization

## Phase 5: Result Integration and Follow-up

### Output Processing

After agent completion, I'll:

#### Result Documentation
- **Capture recommendations**: Record agent findings and suggestions
- **Document rationale**: Preserve reasoning and decision factors
- **Identify actions**: Extract specific next steps and priorities
- **Update context**: Add insights to project knowledge base

#### Session Integration
- **Memory updates**: Record agent insights in session context
- **Decision tracking**: Log important architectural or technical decisions
- **Action planning**: Schedule follow-up work based on recommendations
- **Quality tracking**: Monitor implementation of quality improvements

### Follow-up Guidance

Based on agent type and recommendations:

#### Architecture Follow-up
- **Design validation**: Review architectural decisions with stakeholders
- **Implementation planning**: Break down design into development tasks
- **Technology setup**: Configure tools and frameworks as recommended
- **Documentation updates**: Capture architectural decisions and rationale

#### Testing Follow-up
- **Test implementation**: Execute TDD workflow as designed
- **Coverage improvement**: Address identified gaps in test coverage
- **Quality automation**: Set up continuous testing and quality checks
- **Performance validation**: Implement and monitor performance tests

#### Code Review Follow-up
- **Issue resolution**: Address identified security and quality issues
- **Standard adoption**: Implement recommended coding standards
- **Refactoring tasks**: Schedule code improvement and cleanup work
- **Knowledge sharing**: Document insights for team learning

#### Documentation Follow-up
- **Content updates**: Improve documentation based on feedback
- **Structure optimization**: Reorganize documentation for better usability
- **Accuracy verification**: Ensure documentation matches current implementation
- **User testing**: Validate documentation with actual users

## Success Indicators

Agent invocation is successful when:
- ✅ Appropriate specialist selected for task type
- ✅ Complete context provided to agent
- ✅ Agent applies specialized expertise effectively
- ✅ Actionable recommendations provided
- ✅ Next steps clearly defined
- ✅ Results integrated into project workflow

## Best Practices

### Agent Selection
- **Match expertise to need**: Choose agent with relevant specialization
- **Clear task definition**: Provide specific, actionable task description
- **Context richness**: Include all relevant project information
- **Success criteria**: Define clear expectations for agent output

### Result Utilization
- **Immediate review**: Assess recommendations for validity and feasibility
- **Integration planning**: Schedule implementation of agent suggestions
- **Knowledge capture**: Document insights for future reference
- **Feedback loop**: Use results to improve future agent interactions

---

*Direct agent invocation providing specialized expertise for complex technical tasks with proper context and result integration.*