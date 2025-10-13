---
allowed-tools: [Read, Write, Grep, Bash, LS, Task, mcp__sequential-thinking__sequentialthinking, mcp__serena__find_symbol, mcp__serena__search_for_pattern, mcp__serena__get_symbols_overview, mcp__serena__find_referencing_symbols]
argument-hint: "[focus_area] or [requirements_doc] [--with-thinking] [--semantic]"
description: Analyze ANY project to understand its structure and architecture with semantic code intelligence and structured reasoning
---

# Analyze Project

Deep analysis of any codebase to understand architecture, patterns, and improvement opportunities.

**Input**: $ARGUMENTS

**Related commands:**
- `/setup` - Add Claude infrastructure to projects without it
- `/index` - Create persistent project mapping for ongoing work

## Performance Monitoring Setup

I'll initialize comprehensive performance tracking for analysis operations:

```bash
# Initialize analysis performance tracking
ANALYZE_START_TIME=$(date +%s)
ANALYZE_SESSION_ID="analyze_$(date +%s)_$$"

# Setup performance monitoring (optional)
if command -v npx >/dev/null 2>&1 && command -v jq >/dev/null 2>&1; then
    echo "📊 Performance monitoring available"

    # Optional: Capture baseline token usage
    BASELINE_TOKENS=$(npx ccusage@latest session --since $(date -d "-1 hour" +%Y%m%dT%H) --json 2>/dev/null | jq '.sessions[-1].total_tokens // 0' 2>/dev/null || echo "0")

    if [ "$BASELINE_TOKENS" != "0" ]; then
        echo "📈 Session baseline: $BASELINE_TOKENS tokens"
    fi
else
    echo "📝 Running without performance monitoring (tools not available)"
fi
```

## Phase 1: Analysis Scope Determination

Based on the provided arguments: $ARGUMENTS

I'll determine the analysis approach and focus:

- **General Analysis**: No specific focus - comprehensive codebase review
- **Focused Analysis**: Specific area or feature mentioned - targeted examination
- **Requirements-Based**: Document provided - analysis for implementation planning
- **Enhanced Reasoning**: `--with-thinking` flag - structured step-by-step analysis
- **Semantic Analysis**: `--semantic` flag - symbol-aware code understanding

### Analysis Method Selection

**Standard Analysis**: Direct examination of codebase structure, patterns, and organization

**Enhanced Reasoning**: For complex analysis involving architectural decisions, integration challenges, or system design considerations

**Semantic Analysis**: For large codebases requiring efficient symbol-level understanding and dependency mapping

## Phase 2: Project Understanding and Confirmation

### Initial Assessment

I'll scan the project to understand:

#### Project Characteristics
- **Language and Framework**: Primary technologies and patterns used
- **Architecture Style**: Monolith, microservices, layered, modular, etc.
- **Development Stage**: Prototype, active development, mature, legacy
- **Code Organization**: Directory structure, naming conventions, patterns

#### Quality Indicators
- **Testing Approach**: Test framework, coverage, testing patterns
- **Documentation State**: README, API docs, code comments, guides
- **Development Practices**: Git workflow, CI/CD, code standards
- **Technical Debt**: Code smells, outdated dependencies, maintenance issues

### Understanding Confirmation

Before proceeding with deep analysis, I'll confirm my initial understanding:

**Project Assessment Summary**:
- **Type**: [Detected technology stack and architecture]
- **Maturity**: [Development stage and stability]
- **Quality**: [Testing, documentation, maintenance status]
- **Focus Area**: [Specific analysis target from arguments]

**Analysis Scope Clarification**: [What aspects need detailed examination and why]

## Phase 3: Comprehensive Analysis Execution

### Architecture Assessment

I'll systematically analyze the codebase structure:

#### Component Mapping
- **Core Components**: Primary modules, services, and their responsibilities
- **Dependency Relationships**: How components interact and depend on each other
- **Design Patterns**: Architectural patterns and frameworks in use
- **Data Flow**: How information moves through the system

#### Quality Evaluation
- **Code Organization**: Structure, naming, and organizational patterns
- **Separation of Concerns**: How well responsibilities are divided
- **Extensibility**: How easily new features can be added
- **Maintainability**: Code clarity, documentation, and testing support

### Integration Analysis

For new functionality planning:

#### Current System Capabilities
- **Existing Features**: What the system currently does well
- **Extension Points**: Where new features can integrate naturally
- **Constraints**: Limitations that affect new development
- **Opportunities**: Areas where improvements would have high impact

#### Implementation Considerations
- **Technical Requirements**: Infrastructure, dependencies, configuration needs
- **Risk Assessment**: Potential challenges and mitigation strategies
- **Development Approach**: Recommended implementation strategy
- **Testing Strategy**: How to validate new functionality

### Enhanced Integration Analysis (with Serena MCP)
When planning new feature integration using Serena:

**Semantic Integration Planning**:
1. **API Surface Analysis**: Use `find_symbol` to understand existing interfaces
2. **Impact Assessment**: Use `find_referencing_symbols` to identify affected code
3. **Extension Point Discovery**: Find natural places to add new functionality
4. **Consistency Validation**: Ensure new features follow established patterns

**Smart Architecture Integration**:
- **Pattern Adherence**: Verify new features match existing architectural patterns
- **Dependency Management**: Understand real dependency relationships for integration
- **Testing Integration**: Identify existing test patterns for new feature testing
- **Documentation Integration**: Find documentation patterns to follow

## Phase 4: Enhanced Analysis with Agent Support

### Architectural Deep Dive

For complex architectural analysis, I'll invoke the architect agent:

**Agent Delegation**:
- **Purpose**: Comprehensive architectural assessment and recommendations
- **Scope**: System design, component relationships, scalability, maintainability
- **Deliverables**: Architectural insights, improvement recommendations, design guidance

### Structured Reasoning Enhancement

For complex analysis requiring systematic thinking, I'll use Sequential Thinking MCP to ensure comprehensive coverage:

**When to use Sequential Thinking**:
- Multi-layered architectural analysis with interconnected components
- Legacy system assessment requiring careful risk evaluation
- Complex integration analysis involving multiple systems or domains
- Large-scale refactoring planning with significant impact assessment
- Performance optimization analysis across multiple system layers

**Sequential Thinking Benefits**:
- **Systematic Architecture Review**: Step-by-step analysis preventing oversight of critical components
- **Comprehensive Risk Assessment**: Methodical identification of potential issues and edge cases
- **Clear Decision Documentation**: Transparent reasoning trail for architectural and technical decisions
- **Multi-dimensional Analysis**: Consideration of technical, business, and operational factors
- **Quality Assurance**: More thorough and reliable analysis outcomes through structured approach

If the analysis involves significant complexity (architectural decisions, system integration challenges, or multi-domain considerations), I'll engage Sequential Thinking to work through the analysis systematically, ensuring all critical aspects are properly evaluated and documented.

**Graceful Degradation**: When Sequential Thinking MCP is unavailable, I'll use standard analytical approaches while maintaining comprehensive analysis quality. The tool enhances systematic reasoning but isn't required for effective codebase analysis.

## Phase 5: Analysis Documentation and Recommendations

### Comprehensive Analysis Report

I'll generate detailed documentation including:

#### System Overview
- **Architecture Summary**: High-level system design and component overview
- **Technology Stack**: Languages, frameworks, tools, and their integration
- **Quality Assessment**: Testing, documentation, and code quality evaluation
- **Development Workflow**: Current practices and improvement opportunities

#### Integration Analysis (for new features)
- **Implementation Strategy**: Phased approach for adding new functionality
- **Technical Requirements**: Dependencies, infrastructure, configuration changes
- **Risk Mitigation**: Potential challenges and recommended solutions
- **Testing Approach**: Quality assurance strategy for new development

#### Improvement Recommendations
- **Immediate Actions**: High-impact improvements with low effort
- **Strategic Initiatives**: Long-term improvements for system evolution
- **Technical Debt**: Areas requiring cleanup or modernization
- **Development Process**: Workflow and tooling enhancements

### Actionable Next Steps

Based on analysis results:

#### For Feature Implementation
1. **Architecture Preparation**: Infrastructure changes needed before development
2. **Development Planning**: Task breakdown and implementation sequence
3. **Quality Setup**: Testing and validation infrastructure
4. **Documentation Updates**: Required documentation changes

#### For System Improvement
1. **Priority Assessment**: Ranking improvements by impact and effort
2. **Implementation Planning**: Phased approach to system enhancement
3. **Risk Management**: Mitigation strategies for change implementation
4. **Success Metrics**: How to measure improvement effectiveness

## Phase 6: Analysis Method Optimization

### MCP Integration Benefits

**Sequential Thinking Integration**:
- **Complex Decision Making**: Systematic reasoning for architectural choices
- **Risk Analysis**: Comprehensive identification and assessment of challenges
- **Solution Evaluation**: Structured comparison of implementation approaches
- **Quality Assurance**: More thorough and reliable analysis outcomes

**Enhanced Semantic Analysis (with Serena MCP)**:
When Serena MCP is available, perform intelligent code-aware analysis:

**When to use Serena for analysis**:
- Large codebases where reading entire files would be token-inefficient
- Complex architectures requiring understanding of symbol relationships
- Legacy systems needing dependency and usage pattern analysis
- Code-heavy projects requiring deep structural understanding
- Performance analysis requiring actual code flow understanding

**Serena-Enhanced Analysis Capabilities**:

1. **Efficient Codebase Exploration**:
   - **70-90% token reduction**: Use `get_symbols_overview` instead of reading entire files
   - **Targeted analysis**: Use `find_symbol` to examine specific classes/functions
   - **Dependency mapping**: Use `find_referencing_symbols` to understand usage patterns
   - **Architecture discovery**: Build component relationships through symbol analysis

2. **Semantic Code Intelligence**:
   - **Real symbol relationships**: Understand actual imports and dependencies
   - **Type-aware analysis**: Follow actual type information and contracts
   - **API surface analysis**: Identify public interfaces through symbol inspection
   - **Cross-module understanding**: Trace functionality across files efficiently

3. **Pattern Recognition**:
   - **Architectural patterns**: Identify MVC, MVP, microservices patterns through code structure
   - **Design patterns**: Detect singleton, factory, observer patterns in actual implementation
   - **Anti-patterns**: Find code smells through symbol usage analysis
   - **Consistency analysis**: Check naming and organizational patterns across codebase

**Example Serena Analysis Workflow**:
```bash
# Analyze a large Python codebase efficiently
# 1. Get high-level overview without reading files
/serena get_symbols_overview src/

# 2. Focus on specific components
/serena find_symbol UserService

# 3. Understand usage patterns
/serena find_referencing_symbols UserService

# 4. Analyze cross-cutting concerns
/serena search_for_pattern "def authenticate"
```

**Graceful Degradation**: When Serena unavailable, falls back to traditional file-reading and grep-based analysis while maintaining comprehensive analysis quality.

### Graceful Degradation

When enhanced tools are unavailable:
- **Standard Analysis**: Full functionality using direct codebase examination
- **Clear Communication**: Indication of analysis method being used
- **Quality Maintenance**: Consistent analysis quality regardless of available tools
- **Workflow Continuity**: No disruption to development process

## Success Indicators

Analysis is complete when:
- ✅ Comprehensive understanding of existing codebase documented
- ✅ Clear integration strategy for new functionality defined
- ✅ Implementation risks identified with mitigation strategies
- ✅ Actionable next steps provided with priority guidance
- ✅ Quality improvement opportunities identified
- ✅ Development approach recommendations provided

## Serena MCP Usage Patterns for Different Analysis Types

### Codebase Discovery Analysis
**Use Case**: Understanding a new or unfamiliar codebase
**Serena Approach**:
```bash
# 1. High-level overview without reading files
/serena get_symbols_overview ./

# 2. Identify main entry points
/serena find_symbol "main\|__main__\|app"

# 3. Understand key classes and modules
/serena find_symbol "User\|Service\|Controller"

# 4. Map dependencies and relationships
/serena find_referencing_symbols ClassName
```

### Legacy System Analysis
**Use Case**: Understanding legacy code for modernization
**Serena Approach**:
```bash
# 1. Find deprecated patterns
/serena search_for_pattern "deprecated\|TODO\|FIXME"

# 2. Identify tightly coupled components
/serena find_referencing_symbols ComponentName

# 3. Locate configuration and setup code
/serena find_symbol "config\|setup\|init"

# 4. Map external dependencies
/serena search_for_pattern "import\|require"
```

### Performance Analysis
**Use Case**: Identifying performance bottlenecks
**Serena Approach**:
```bash
# 1. Find database access patterns
/serena search_for_pattern "query\|execute\|connection"

# 2. Locate expensive operations
/serena search_for_pattern "loop\|recursive\|cache"

# 3. Analyze API endpoints
/serena find_symbol "route\|endpoint\|handler"

# 4. Check usage patterns of expensive functions
/serena find_referencing_symbols ExpensiveFunctionName
```

### Security Analysis
**Use Case**: Identifying potential security vulnerabilities
**Serena Approach**:
```bash
# 1. Find authentication/authorization code
/serena find_symbol "auth\|login\|permission"

# 2. Locate input validation
/serena search_for_pattern "validate\|sanitize\|escape"

# 3. Check for hardcoded secrets
/serena search_for_pattern "password\|key\|secret\|token"

# 4. Analyze authentication usage
/serena find_referencing_symbols AuthenticationClass
```

## Analysis Integration with Framework

### Memory Management
- **Project Mapping**: Create persistent understanding via `/index` command
- **Session Context**: Record analysis insights for future reference
- **Decision Documentation**: Capture architectural and technical decisions

### Workflow Integration
- **Planning Support**: Analysis feeds into `/plan` command for task creation
- **Development Guidance**: Insights support `/next` task execution
- **Quality Assurance**: Recommendations inform `/review` and `/ship` activities

## Performance Analysis and ROI Report

I'll conclude with comprehensive performance metrics and optimization insights:

```bash
# Calculate analysis session performance
ANALYZE_END_TIME=$(date +%s)
ANALYZE_DURATION=$((ANALYZE_END_TIME - ANALYZE_START_TIME))

if command -v npx >/dev/null 2>&1; then
    echo ""
    echo "📈 Analysis Performance Report"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Calculate actual token usage
    CURRENT_TOKENS=$(npx ccusage@latest session --since $(date -d "-1 hour" +%Y%m%dT%H) --json 2>/dev/null | jq '.sessions[-1].total_tokens // 0')
    SESSION_TOKENS=$((CURRENT_TOKENS - BASELINE_TOKENS))

    echo "⏱️ Analysis Duration: ${ANALYZE_DURATION}s"
    echo "🎯 Tokens Used: $SESSION_TOKENS tokens"

    # Dynamic context system efficiency metrics
    if [ -n "$DYNAMIC_CONTEXT_BUDGET" ]; then
        BUDGET_USAGE=$((SESSION_TOKENS * 100 / DYNAMIC_CONTEXT_BUDGET))
        echo "💰 Budget Utilization: ${BUDGET_USAGE}% of ${DYNAMIC_CONTEXT_BUDGET} allocated"

        # Simple ROI calculation
            if [[ "$DYNAMIC_CONTEXT_MCP_TOOLS" == *"serena"* ]]; then
                # Calculate Serena efficiency gains
                EXPECTED_MANUAL_TOKENS=15000  # Baseline for manual code analysis
                if [ $SESSION_TOKENS -lt $EXPECTED_MANUAL_TOKENS ]; then
                    SERENA_EFFICIENCY=$(( (EXPECTED_MANUAL_TOKENS - SESSION_TOKENS) * 100 / EXPECTED_MANUAL_TOKENS ))
                    echo "⚡ Serena Efficiency: ${SERENA_EFFICIENCY}% token reduction (semantic analysis)"
                fi
            fi

            if [[ "$DYNAMIC_CONTEXT_MCP_TOOLS" == *"sequential_thinking"* ]]; then
                echo "🧠 Sequential Thinking: Enhanced analysis depth and coverage"
            fi

            # Overall ROI calculation
            if [ $SESSION_TOKENS -lt $EXPECTED_BASELINE_TOKENS ]; then
                TOTAL_EFFICIENCY=$(( (EXPECTED_BASELINE_TOKENS - SESSION_TOKENS) * 100 / EXPECTED_BASELINE_TOKENS ))
                echo "✅ Total Efficiency Gain: ${TOTAL_EFFICIENCY}% vs baseline analysis"

                # Cost savings calculation
                TOKEN_COST=0.000003  # Approximate cost per token
                SAVINGS=$(echo "$EXPECTED_BASELINE_TOKENS $SESSION_TOKENS $TOKEN_COST" | awk '{printf "%.4f", ($1 - $2) * $3}')
                echo "💵 Estimated Cost Savings: \$${SAVINGS}"
            fi
        fi
    fi

    echo ""
    echo "📊 Analysis Optimization Insights:"
    echo "   • Project Type: $DYNAMIC_CONTEXT_PROJECT_TYPE"
    echo "   • MCP Tools Used: $DYNAMIC_CONTEXT_MCP_TOOLS"
    echo "   • Context Efficiency: Intelligent relevance-based loading"
    echo "   • Token Management: Dynamic budget allocation"

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
fi
```

### Performance Insights for Future Analysis
- **Optimal Budget**: Code analysis typically requires 12k tokens for comprehensive coverage
- **Serena Value**: 70-90% token reduction on code-heavy projects through semantic understanding
- **Sequential Thinking**: Enhances analysis quality for complex architectural patterns
- **Dynamic Context**: Intelligent context loading maximizes relevance within budget constraints

---

*Comprehensive codebase analysis with integrated performance monitoring, MCP optimization, and actionable efficiency insights.*