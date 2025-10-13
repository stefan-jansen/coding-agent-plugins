---
allowed-tools: [Task, Bash, Read, Write, MultiEdit, Grep, Glob]
argument-hint: "[--preview | --pr | --commit | --deploy]"
description: "Deliver completed work with validation and comprehensive documentation"
@import .claude/memory/conventions.md
@import .claude/memory/decisions.md
@import .claude/memory/dependencies.md
@import .claude/memory/lessons_learned.md
@import .claude/memory/project_state.md
---

# Work Delivery

I'll validate, document, and deliver your completed work, ensuring everything meets quality standards.

**Options**: $ARGUMENTS

## Phase 1: Delivery Readiness Assessment

I'll validate the work is ready for delivery before proceeding:

1. **Check project setup** - Verify `.claude` directory and work unit structure
2. **Find active work unit** - Identify work unit to be shipped
3. **Validate completion** - Ensure all tasks are completed
4. **Check git status** - Verify changes are committed (if in git repo)

If validation fails, I'll provide specific guidance on what needs to be completed before shipping.

Based on the provided arguments: $ARGUMENTS

I'll determine the delivery approach and validation scope:

- **Preview Mode**: Show what would be delivered without making changes
- **Pull Request**: Create PR with comprehensive documentation
- **Direct Commit**: Commit work to current branch with proper messaging
- **Deployment**: Prepare for production deployment

### Work Completion Validation

Before proceeding with delivery, I'll verify:
1. **All tasks completed**: No pending or blocked tasks remain
2. **Quality gates passed**: Tests, coverage, linting all successful
3. **Documentation complete**: README, API docs, deployment guides current
4. **Integration ready**: Code compiles/builds successfully
5. **Dependencies resolved**: All external requirements satisfied

## Phase 2: Quality Assurance Verification

### Comprehensive Test Validation

I'll execute full quality validation including:

#### Test Suite Execution
- **Unit Tests**: Complete test suite with coverage analysis
- **Integration Tests**: Cross-component interaction validation
- **End-to-End Tests**: Full user journey verification
- **Performance Tests**: Load and stress testing (if applicable)

#### Code Quality Assessment
- **Linting**: Code style and convention adherence
- **Type Safety**: Static type checking validation
- **Security Scanning**: Vulnerability assessment
- **Dependency Audit**: Third-party library security review

#### Documentation Validation
- **Completeness**: All features and APIs documented
- **Accuracy**: Documentation matches implementation
- **Usability**: Clear setup and usage instructions
- **Maintenance**: Troubleshooting and deployment guides

### Quality Gate Requirements

All must pass before delivery:
- ✅ Test suite passes with >80% coverage
- ✅ No critical linting errors or security vulnerabilities
- ✅ Documentation complete and accurate
- ✅ Build/compilation successful
- ✅ Performance requirements met

## Phase 3: Delivery Documentation Generation

### Implementation Summary Creation

I'll generate comprehensive delivery documentation:

#### Project Overview Document
**DELIVERY.md** containing:
- **What was built**: Feature descriptions and capabilities
- **Technical architecture**: System design and component overview
- **Implementation approach**: Key technical decisions and patterns
- **Quality metrics**: Test coverage, performance, security results

#### Change Documentation
**CHANGELOG.md** with structured change tracking:
- **Added features**: New functionality and capabilities
- **Changed behavior**: Modified existing features
- **Fixed issues**: Bug resolutions and improvements
- **Security updates**: Vulnerability fixes and enhancements
- **Performance improvements**: Optimization results

#### Deployment Instructions
**DEPLOYMENT.md** providing:
- **Prerequisites**: Required software, environment setup
- **Installation steps**: Detailed deployment procedure
- **Configuration**: Environment variables, settings, customization
- **Verification**: Health checks and validation procedures
- **Rollback plan**: Emergency recovery procedures

### Technical Handoff Materials

I'll prepare comprehensive handoff documentation:

#### Developer Guide
- **Architecture overview**: System design and data flow
- **Code organization**: Directory structure and conventions
- **Development setup**: Local environment configuration
- **Testing strategy**: How to run and maintain tests
- **Debugging guide**: Common issues and troubleshooting

#### User Documentation
- **Feature guide**: How to use new functionality
- **API documentation**: Endpoints, parameters, examples
- **Configuration options**: Available settings and customization
- **Troubleshooting**: Common problems and solutions

## Phase 4: Delivery Method Execution

### Preview Mode Processing

When in preview mode, I'll:
1. **Show validation results**: Quality checks without making changes
2. **Display delivery plan**: What would be included in delivery
3. **Highlight any issues**: Problems that need resolution
4. **Provide recommendations**: Suggested next steps

### Pull Request Creation

For PR delivery, I'll:
1. **Generate PR description**: Comprehensive change summary
2. **Include test results**: Coverage and quality metrics
3. **Add deployment notes**: Special considerations for deployment
4. **Link related issues**: Connect to original requirements

### Direct Commit Delivery

For commit delivery, I'll:
1. **Stage all changes**: Include all work-related modifications
2. **Create meaningful commit**: Clear, conventional commit message
3. **Include co-authorship**: Proper attribution to Claude Code
4. **Verify commit success**: Ensure changes are properly recorded

### Deployment Preparation

For production deployment, I'll:
1. **Final validation**: Extra security and performance checks
2. **Environment preparation**: Production-specific configuration
3. **Rollback planning**: Detailed recovery procedures
4. **Monitoring setup**: Health checks and alerting configuration

## Phase 5: Memory Reflection and Learning Capture

### Automated Work Unit Analysis

Before finalizing delivery, I'll analyze the work unit to identify valuable learnings:

#### Work Unit Review
I'll examine all work unit files to extract insights:
- **Read exploration.md**: Understand initial approach and discoveries
- **Read implementation-plan.md**: Review planned vs actual execution
- **Read validation reports**: Identify what worked well and what didn't
- **Read task summaries**: Extract specific learnings from each task
- **Review changed files**: Understand technical decisions made

#### Learning Categorization
I'll categorize findings into memory types:

**Decisions** (`.claude/memory/decisions.md`):
- Architectural choices made during implementation
- Technology selections and their rationale
- Design patterns adopted
- Trade-offs and their justification

**Lessons Learned** (`.claude/memory/lessons_learned.md`):
- What worked well and should be repeated
- What didn't work and should be avoided
- Unexpected challenges encountered
- Successful problem-solving approaches

**Conventions** (`.claude/memory/conventions.md`):
- New coding standards established
- Naming patterns adopted
- File organization decisions
- Documentation standards

**Dependencies** (`.claude/memory/dependencies.md`):
- New tools or libraries added
- Version requirements discovered
- Integration requirements learned

**Project State** (`.claude/memory/project_state.md`):
- Current architecture updates
- New capabilities added
- System state changes

### Memory Update Prompt

After analyzing the work unit, I'll present findings and prompt for memory update:

```
🧠 Memory Reflection Analysis
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Work unit analysis complete. Identified learnings:

📋 DECISIONS (N items identified):
- [Decision 1]: [Brief description]
- [Decision 2]: [Brief description]
...

📚 LESSONS LEARNED (N items identified):
✅ What Worked:
- [Lesson 1]: [Brief description]
- [Lesson 2]: [Brief description]

❌ What NOT to Do:
- [Anti-pattern 1]: [Brief description]
- [Anti-pattern 2]: [Brief description]

🔧 CONVENTIONS (N items identified):
- [Convention 1]: [Brief description]
...

📦 DEPENDENCIES (N items identified):
- [Dependency 1]: [Brief description]
...

🏗️ PROJECT STATE (N updates identified):
- [State update 1]: [Brief description]
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 RECOMMENDATION: Update memory to capture these learnings

Options:
1. Run /memory-update to review and add selected learnings
2. Skip if no memory updates needed (type 'skip')

Choice: _
```

### User Decision Handling

I'll handle the user's response:

**If user runs /memory-update**:
- Present findings in interactive format
- Allow selective addition to memory files
- Update timestamps on modified memory files
- Proceed with delivery

**If user types 'skip'**:
- Note that learnings were not captured
- Warn about potential knowledge loss
- Proceed with delivery anyway

**If no response / uncertainty**:
- Default to prompting for /memory-update
- Emphasize value of capturing learnings
- Offer to proceed without updates if user insists

## Phase 6: Work Unit Management and Archival

### Completion Recording

I'll properly record work completion:

#### State Finalization
- **Update work unit status**: Mark as completed with timestamp
- **Record delivery method**: How work was delivered (PR, commit, deploy)
- **Document final metrics**: Test coverage, performance, quality scores
- **Archive task details**: Complete task execution history

#### Session Memory Updates (if memory-update was run)
- **Project summary**: What was accomplished
- **Key decisions**: Important technical choices made (now in memory)
- **Lessons learned**: Insights for future work (now in memory)
- **Follow-up items**: Potential enhancements or maintenance needs

### Work Unit Archival

For completed work units, I'll:
1. **Create archive entry**: Move completed work to archive with timestamp
2. **Generate summary**: Brief overview of what was accomplished
3. **Preserve context**: Keep important decisions and documentation
4. **Clean active workspace**: Remove completed work from active area

## Phase 7: Quality Assurance with Agent Support

### Code Review Validation

For critical deliveries, I'll invoke the code-reviewer agent:

**Agent Delegation**:
- **Purpose**: Final code quality and security review
- **Scope**: All modified and new code
- **Focus**: Security, performance, maintainability
- **Deliverables**: Review report with recommendations

### Documentation Review

For client-facing deliveries, I'll invoke the doc-reviewer agent:

**Agent Delegation**:
- **Purpose**: Documentation quality and completeness review
- **Scope**: All user-facing documentation
- **Focus**: Clarity, completeness, accuracy
- **Deliverables**: Documentation quality report

## Phase 8: Delivery Confirmation and Handoff

### Delivery Verification

I'll confirm successful delivery by checking:
- **Integration success**: Code merged/committed without conflicts
- **Build success**: Continuous integration passes
- **Deployment readiness**: All prerequisites met
- **Documentation availability**: All docs accessible and current

### Handoff Preparation

For team or client handoff, I'll prepare:

#### Knowledge Transfer Package
- **Technical overview**: Architecture and implementation details
- **Operational guide**: Running, monitoring, maintaining the system
- **Development guide**: How to extend and modify functionality
- **Support information**: Common issues and resolution procedures

#### Success Metrics
- **Functionality delivered**: All requirements met
- **Quality achieved**: Test coverage and performance targets
- **Documentation complete**: All guides and references ready
- **Team prepared**: Handoff materials reviewed and understood

## Success Indicators

Delivery is successful when:
- ✅ All planned functionality implemented and tested
- ✅ Quality gates passed (tests, coverage, security, performance)
- ✅ Documentation complete and accurate
- ✅ Code integrated via chosen method (PR, commit, deploy)
- ✅ Work unit properly archived with context preserved
- ✅ Handoff materials prepared and delivered
- ✅ Team/client ready to take ownership

## Post-Delivery Support

After successful delivery:
1. **Monitor for issues**: Watch for deployment problems or user feedback
2. **Document lessons learned**: Capture insights for future work
3. **Plan maintenance**: Schedule follow-up reviews and updates
4. **Prepare for enhancements**: Document potential future improvements

---

*Professional work delivery ensuring quality, documentation, and smooth handoff for sustained success.*