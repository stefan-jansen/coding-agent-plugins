# Claude Code Plugins

**Production-tested plugins for structured AI-assisted development**

> Open-source plugin framework built over 6 months of production use on real projects: technical books, content production, and framework development.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## What This Is

A collection of Claude Code plugins that enforce systematic workflows, prevent common pitfalls, and enable productive AI-assisted development. These aren't theoretical best practices—they're patterns we built solving real problems in production.

**Core plugins** (5):
- **setup** - Project initialization and configuration
- **system** - System health and maintenance
- **workflow** - Structured task execution (explore → plan → next → ship)
- **memory** - Context management and session handoffs
- **development** - Code analysis, review, and testing tools

**Domain plugins** (7):
- **quant** - Quantitative finance workflows with validators
- **ml3t-researcher** - ML research with paper search (v2.0: RAG with Qdrant)
- **ml3t-coauthor** - Book production workflow (v1.1: writing-skills integration)
- **reports** - Professional report generation
- **content-marketing** - Technical B2B content production (v1.3: website copy generation)
- **web-development** - Full-stack web development (Django + Tailwind)
- **diagrams** - D2 diagram generation with visual design expertise

**Utility plugins** (1):
- **writing-skills** - Shared writing methodology library (10 skills)

**Total**: 13 active plugins (5 core + 7 domain + 1 utility)

---

## Why We Built This

Claude Code is powerful but has constraints that break productivity if you don't work systematically:

**Context perception error**: Claude reports ~30% lower usage than actual (shows "64%" when actual is 92%)
**Hallucination risks**: Agents fabricate plausible details without systematic verification
**Execution constraints**: Commands run in project directory, not `~/.claude/`, preventing utility sharing

Our plugin framework provides guardrails that work productively within these constraints.

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/claude-code-plugins.git
cd claude-code-plugins

# Copy plugins to your project
cp -r system workflow memory development ~/.claude/plugins/
```

### Enable Plugins

Create or edit `.claude/settings.json` in your project:

```json
{
  "extraKnownMarketplaces": {
    "local": {
      "source": {
        "source": "directory",
        "path": "/path/to/claude-code-plugins"
      }
    }
  },
  "enabledPlugins": {
    "system@local": true,
    "workflow@local": true,
    "memory@local": true,
    "development@local": true
  }
}
```

### Try It

```bash
# Navigate to your project
cd ~/my-project/

# Start with exploration
/explore "add user authentication"

# Create implementation plan
/plan

# Execute tasks systematically
/next

# When approaching context limits
/handoff
```

---

## Core Commands

### Workflow Commands (4 commands)

**`/explore`** - Systematic requirements and codebase analysis
```bash
/explore "add payment processing"
# Analyzes: requirements, current implementation, integration points, recommendations
```

**`/plan`** - Create structured implementation plan with task breakdown
```bash
/plan --from-requirements
# Creates: Ordered tasks with dependencies, state tracking, progress monitoring
```

**`/next`** - Execute next task from plan with focused context
```bash
/next
# Executes: One task at a time, updates state, tracks progress
```

**`/ship`** - Deliver completed work with validation
```bash
/ship --pr
# Validates: All tasks complete, tests passing, documentation current
# Creates: Pull request with comprehensive summary
```

### Memory Commands (3 commands)

**`/handoff`** - Create session handoff before context limits
```bash
/handoff
# Context check: Shows perceived vs actual usage
# Creates: Transition document in .claude/transitions/YYYY-MM-DD/HHMMSS.md
# Preserves: Active work, decisions, next steps
```

**`/index`** - Create persistent project knowledge base
```bash
/index
# Analyzes: Project structure, patterns, conventions
# Generates: Memory files loaded via @import in future sessions
```

**`/continue`** - Resume from most recent handoff (after /clear)
```bash
# After running /clear:
continue
# Loads: Most recent transition document
# Resumes: Exactly where you left off
```

### Development Commands (6 commands)

**`/analyze`** - Deep codebase analysis
**`/review`** - Code review with quality checks
**`/test`** - Test-driven development workflow
**`/fix`** - Debug and apply fixes
**`/run`** - Execute scripts with monitoring
**`/docs`** - Documentation operations

### System Commands (4 commands)

**`/audit`** - Framework compliance validation
**`/cleanup`** - Remove clutter and consolidate docs
**`/setup`** - Project initialization
**`/status`** - Current project and task status

---

## Screenshots

### Context Management: /handoff → /continue

Managing context across sessions to prevent quality degradation:

![Handoff and Continue Workflow](screenshots/01_handoff_continue.png)

**Key features**:
- Context analysis at 70% perceived usage (~85% actual)
- Active work state preservation
- Recent decisions and outstanding items
- Clean continuation after `/clear`

---

### Complete Workflow: /explore → /plan → /next

Systematic task execution from requirements to implementation:

![Workflow Sequence](screenshots/02_workflow_sequence.png)

**Key features**:
- Requirements analysis with `/explore`
- Task breakdown with `/plan`
- Incremental execution with `/next`
- Progress tracking and state management

---

### Code Analysis: /analyze and /review

Deep codebase understanding and quality checks:

![Code Analysis and Review](screenshots/03_analyze_review.png)

**Key features**:
- Structural analysis with pattern identification
- Test coverage metrics
- Code quality review with actionable recommendations
- Security and performance assessment

---

## Command Examples

### Workflow: /explore → /plan → /next → /ship

#### /explore - Analyze Requirements

```bash
$ /explore "add payment processing to checkout flow"

🔍 Analyzing requirements and codebase...

Current Implementation:
├── checkout_service.py (lines 45-280)
│   └── Order creation and validation logic
├── payment_gateway.py (stub implementation)
│   └── TODO: Stripe integration needed
└── order_model.py
    └── Database schema ready for payment fields

Integration Requirements:
• PCI-DSS compliance for payment data handling
• Idempotency keys for retry safety
• Webhook handling for async payment confirmations
• Error handling for declined payments

Security Considerations:
⚠️  Store payment tokens only, never raw card data
⚠️  Implement rate limiting on payment endpoints
⚠️  Add audit logging for all payment operations

Recommendations:
✓ Start with Stripe SDK (most mature, best docs)
✓ Implement idempotency layer before payment calls
✓ Test with Stripe test mode first
✓ Add comprehensive error handling

Next Steps:
Run /plan to create structured implementation tasks
```

#### /plan - Create Implementation Plan

```bash
$ /plan --from-requirements

📋 Creating implementation plan...

Work Unit: WU-042_payment_processing
Location: .claude/work/current/042_payment_processing/

Implementation Plan (8 tasks):

TASK-001: Design PaymentService interface [PENDING]
├── Dependencies: None
├── Estimate: 1-2 hours
└── Deliverable: payment_service.py with abstract class

TASK-002: Integrate Stripe SDK [PENDING]
├── Dependencies: TASK-001
├── Estimate: 2-3 hours
└── Deliverable: stripe_processor.py implementation

TASK-003: Implement idempotency layer [PENDING]
├── Dependencies: TASK-002
├── Estimate: 2-3 hours
└── Deliverable: idempotency middleware

TASK-004: Add payment validation logic [PENDING]
├── Dependencies: TASK-002
├── Estimate: 1-2 hours
└── Deliverable: validation rules in validators.py

TASK-005: Create webhook handler [PENDING]
├── Dependencies: TASK-002
├── Estimate: 2-3 hours
└── Deliverable: webhook endpoint + signature verification

TASK-006: Write integration tests [PENDING]
├── Dependencies: TASK-002, TASK-003, TASK-004
├── Estimate: 3-4 hours
└── Deliverable: test_payment_integration.py

TASK-007: Add error handling and retry logic [PENDING]
├── Dependencies: TASK-002
├── Estimate: 2-3 hours
└── Deliverable: Exponential backoff + error mapping

TASK-008: Update checkout flow integration [PENDING]
├── Dependencies: ALL ABOVE
├── Estimate: 2-3 hours
└── Deliverable: Checkout service integration complete

Total Estimate: 15-23 hours
State tracking: .claude/work/current/042_payment_processing/state.json

Ready to execute: /next
```

#### /next - Execute Next Task

```bash
$ /next

✅ TASK-001 COMPLETE: PaymentService interface designed

Files Created:
├── app/services/payment_service.py (145 lines)
│   ├── PaymentProcessor (abstract base class)
│   ├── PaymentResult (dataclass)
│   ├── PaymentError (exception hierarchy)
│   └── Type hints and comprehensive docstrings
└── app/services/__init__.py (updated)

Key Design Decisions:
• Abstract base class allows multiple payment providers
• PaymentResult encapsulates success/failure states
• Error hierarchy enables granular exception handling
• Async-first design for non-blocking operations

Tests Added:
└── tests/services/test_payment_service.py (85 lines)
    └── 12 tests covering interface contract

Next Task: TASK-002 (Integrate Stripe SDK)
Ready to continue: /next
```

#### /ship - Deliver with Validation

```bash
$ /ship --pr

🎉 Validating payment processing feature...

Task Completion:
✅ 8/8 tasks completed
✅ All dependencies satisfied
✅ No pending work items

Quality Checks:
✅ Tests passing: 47 new tests, 100% pass rate
✅ Code coverage: 92% (meets 90% threshold)
✅ Type checking: No mypy errors
✅ Linting: All ruff checks passed
✅ Security scan: No vulnerabilities detected

Documentation:
✅ API documentation updated
✅ Integration guide created
✅ README updated with payment setup
✅ Changelog entry added

Files Changed:
 12 files changed
  3 files created
  9 files modified

 +847 lines added
 -123 lines removed

Creating Pull Request...

────────────────────────────────────────
Pull Request #247 Created
────────────────────────────────────────

Title: Add Stripe payment processing to checkout flow

Summary:
Implements complete payment processing system with:
• Stripe SDK integration with idempotency
• Webhook handling for async confirmations
• Comprehensive error handling and retry logic
• PCI-DSS compliant (tokens only, no raw card data)
• 47 new integration tests (100% passing)

Breaking Changes: None
Migration Required: No
Feature Flag: payments.stripe.enabled (default: false)

Ready for Review: ✓
CI Status: Building...

View PR: https://github.com/your-org/project/pull/247
────────────────────────────────────────
```

### Context Management: /handoff → /continue

#### /handoff - Create Session Handoff

```bash
$ /handoff

Creating transition document...

Context Analysis:
├── Token Usage: 140K/200K (70% Claude's perception)
├── System Status: ~85% actual usage (context perception gap)
└── Quality Risk: Approaching degradation threshold

Active Work:
├── Work Unit: WU-042_payment_processing
├── Current Phase: Implementation (8 tasks defined)
├── Progress: 3 of 8 tasks complete (38%)
└── Current Focus: TASK-004 (payment validation logic)

Recent Decisions:
• Chose Stripe over PayPal (better API, clearer docs)
• Implemented abstract PaymentProcessor (multi-provider ready)
• Added idempotency middleware (prevents duplicate charges)
• Using webhook secrets for signature verification

Active Challenges:
• Webhook retry logic needs exponential backoff
• Test coverage for error scenarios still at 75%
• Need to handle payment method updates

Next Steps:
1. Complete TASK-004 (validation logic)
2. Implement TASK-005 (webhook handler)
3. Add comprehensive error scenario tests
4. Integration testing with Stripe test mode

Session Context Preserved:
└── .claude/transitions/2025-10-29/034512.md

────────────────────────────────────────
✅ Handoff complete!

To continue:
1. Run /clear (the CLI command)
2. Say: "continue"
────────────────────────────────────────
```

#### /continue - Resume from Handoff

```bash
# After running /clear in new session:
$ continue

Resuming from .claude/transitions/2025-10-29/034512.md

Context Loaded:
├── Active Work: WU-042_payment_processing
├── Current Phase: Implementation (38% complete)
├── Last Task: TASK-003 completed (idempotency layer)
└── Next Task: TASK-004 (payment validation logic)

Recent Context:
• 3 of 8 tasks complete
• Stripe integration working
• Webhook foundation in place
• Need validation logic and error scenarios

Outstanding Items:
⚠️  Webhook retry logic (exponential backoff needed)
⚠️  Test coverage for errors (currently 75%, target 90%)
⚠️  Payment method update handling

Ready to continue with TASK-004
Run /next to proceed
```

### Development: /analyze and /review

#### /analyze - Deep Codebase Analysis

```bash
$ /analyze app/services/ --focus payment

📊 Analyzing codebase: app/services/

Structure Analysis:
app/services/
├── payment_service.py (145 lines)
│   ├── PaymentProcessor (abstract, 45 lines)
│   ├── StripeProcessor (implementation, 87 lines)
│   └── PaymentResult (dataclass, 13 lines)
├── webhook_handler.py (203 lines)
│   ├── WebhookVerifier (signature validation)
│   └── WebhookProcessor (event handling)
└── idempotency.py (156 lines)
    └── IdempotencyMiddleware (request deduplication)

Key Patterns Identified:
✓ Abstract base class for extensibility
✓ Async-first design (all I/O operations)
✓ Comprehensive error handling
✓ Type hints throughout
✓ Docstrings with examples

Potential Issues:
⚠️  StripeProcessor has 3 methods >50 lines (refactor candidates)
⚠️  WebhookProcessor error handling could be more granular
⚠️  Missing rate limiting on webhook endpoint

Dependencies:
├── stripe==7.2.0 (latest stable)
├── pydantic==2.5.0 (data validation)
└── aiohttp==3.9.0 (async HTTP client)

Test Coverage:
├── payment_service.py: 92% ✓
├── webhook_handler.py: 78% ⚠️  (below 90% threshold)
└── idempotency.py: 95% ✓

Recommendations:
1. Refactor long methods in StripeProcessor
2. Improve webhook_handler test coverage
3. Add rate limiting middleware
4. Consider splitting webhook_handler.py

Technical Debt: Low (well-structured, needs minor improvements)
```

#### /review - Code Quality Review

```bash
$ /review app/services/payment_service.py --systematic

🔍 Code Review: app/services/payment_service.py

Quality Metrics:
├── Lines of Code: 145
├── Cyclomatic Complexity: 8 (good, <10 threshold)
├── Test Coverage: 92%
└── Type Coverage: 100%

Code Quality: A-

Strengths:
✓ Clear separation of concerns (interface vs implementation)
✓ Comprehensive error handling with custom exceptions
✓ Type hints throughout (mypy passes)
✓ Docstrings with usage examples
✓ Async-first design
✓ No security vulnerabilities detected

Issues Found (3):

1. [MEDIUM] Long Method (lines 67-112, 45 lines)
   Method: StripeProcessor.process_payment()
   Suggestion: Extract validation logic to separate method
   Impact: Reduces testability and readability

2. [LOW] Missing Error Context (line 89)
   Code: raise PaymentError("Charge failed")
   Suggestion: Include Stripe error details in exception
   Impact: Makes debugging harder

3. [LOW] Hardcoded Retry Count (line 102)
   Code: max_retries = 3
   Suggestion: Make configurable via settings
   Impact: Less flexible for different environments

Best Practices Followed:
✓ No magic numbers (constants defined)
✓ Proper exception hierarchy
✓ Context managers used correctly
✓ No SQL injection vectors (using ORM)
✓ Secrets not hardcoded
✓ Logging at appropriate levels

Security:
✓ No hardcoded credentials
✓ API keys loaded from environment
✓ Input validation before Stripe calls
✓ PCI-DSS compliant (tokens only)

Performance:
✓ Async I/O (non-blocking)
✓ Connection pooling configured
⚠️  Consider caching Stripe customer objects

Action Items:
- [ ] Refactor process_payment() (extract validation)
- [ ] Add error context to PaymentError exceptions
- [ ] Make retry count configurable
- [ ] Consider customer object caching

Overall: Production-ready with minor improvements suggested
```

---

## Production Use Cases

### ML4T Textbook (25 Chapters, 6 Months)

**Challenge**: Write technical book with code examples, academic citations, and consistent learning objectives

**Plugins Used**:
- `workflow` - Systematic chapter development
- `ml3t/researcher` - Literature review (semantic search over 79,957 indexed papers)
- `ml3t/coauthor` - Learning objective validation
- `memory` - Context management across 25 parallel chapters

**Results**:
- Literature review time: 2.5 hours vs 8-12 hours manual (67-75% reduction)
- Citation accuracy: 92% with semantic search
- Handoff discipline prevented cross-contamination between chapters

### Automation Discovery Whitepaper (24,836 Words)

**Challenge**: Produce publication-quality technical content without hallucinations

**Plugins Used**:
- `workflow` - Section-by-section systematic drafting
- `memory` - Handoffs at 70% perceived usage (before quality degradation)
- `reports` - Fact manifest tracking and section checkpoints

**Results**:
- Production time: 40 hours vs 100-120 manual (60-67% reduction)
- **Zero hallucinations in final output** (fact manifest caught issues at checkpoints)
- All metrics exact (76.4% not "~75%", maintained precision throughout)

### Plugin Framework Development (This Repo, 6 Months)

**Challenge**: Build production-ready plugin system for Claude Code

**Plugins Used**:
- `workflow` - Feature development
- `development` - Code review and testing
- `memory` - Context management during rapid iteration

**Results**:
- 11 plugins shipped
- Testing infrastructure complete
- Used daily in production across multiple projects

---

## Key Lessons Learned

### 1. Handoff at 70% Perceived Usage

**Problem**: Context perception is ~30% off. Claude shows "64%" when actual is 92%.

**Solution**: Create `/handoff` at 70% perceived usage (roughly 85% actual). Quality degrades before Claude realizes—by the time you notice issues, hallucinations have already entered output.

**Impact**: Maintained quality across 24,836-word technical report with zero hallucinations.

### 2. Clean Background Processes Before Handoff

**Problem**: `/continue` loses focus when 11+ background processes create system reminders.

**Solution**: Kill all background processes before creating handoff. Clean environment enables reliable continuation.

```bash
# Before /handoff
ps aux | grep -E "(docker|python|npm)" | grep -v grep | awk '{print $2}' | xargs -r kill -9
```

### 3. Embrace Duplication When Execution Context Requires It

**Problem**: Commands execute in project directory, not `~/.claude/`. Cannot source external utilities.

**Solution**: Copy utilities inline to each command. Duplication is not a bug—it's the price of functionality.

**Rationale**: We spent 8-12 hours building sophisticated shared utilities. Usage: **zero**. Working duplicated code beats elegant broken abstractions.

### 4. Fact Manifests Prevent Hallucinations

**Problem**: Agents fabricate plausible details (names, dates, metrics) without verification.

**Solution**: Track every quantitative claim to source file and line number. Run section checkpoints every 1,500-2,000 words.

**Impact**: Caught 1 hallucination during checkpoints before it contaminated 24,836-word final output.

### 5. Schema Validation Matters

**Problem**: Invalid `plugin.json` breaks command loading silently. No error messages.

**Solution**: Validate schema before shipping. Read official docs first.

```bash
# Validate plugin.json
jq empty .claude-plugin/plugin.json && echo "✅ Valid" || echo "❌ Invalid"
```

**Lesson**: We broke 13 projects simultaneously with invalid schema. Spent 3+ hours trial-and-error before reading docs.

---

## Plugin Architecture

### Official Claude Code Structure

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Manifest (name, version, author, commands)
├── commands/                # Slash commands at ROOT
│   └── command-name.md
├── agents/                  # Specialized agents at ROOT
│   └── agent-name.md
├── hooks/                   # Event handlers (optional)
│   └── hook-name.sh
└── .mcp.json               # MCP servers (optional)
```

**Critical**: Commands, agents, and hooks live at plugin **root**, not inside `.claude-plugin/`.

### Per-Project Activation

Different projects enable different plugin combinations:

**Book project**:
```json
{
  "enabledPlugins": {
    "system@local": true,
    "workflow@local": true,
    "ml3t-researcher@local": true,
    "ml3t-coauthor@local": true,
    "memory@local": true
  }
}
```

**Quant project**:
```json
{
  "enabledPlugins": {
    "system@local": true,
    "workflow@local": true,
    "development@local": true,
    "quant@local": true
  }
}
```

**Outcome**: Same tool adapts to different workflows without bloat.

---

## Testing

The repository includes comprehensive testing infrastructure:

```bash
# Run tests (check individual plugin directories for test scripts)
cd system && ./test.sh
cd workflow && ./test.sh
cd memory && ./test.sh
```

Testing validates:
- Command execution in project context
- State management and transitions
- File creation and organization
- Error handling and edge cases

---

## Contributing

We welcome contributions! This framework emerged from real production use, and we want to learn from your experiences too.

### How to Contribute

1. **Use the plugins** on real projects
2. **Document what breaks** (failure modes we haven't seen)
3. **Share what works** (patterns you discovered)
4. **Submit PRs** with fixes or enhancements

### Guidelines

- **Evidence-based**: Contributions should solve observed problems (not theoretical ones)
- **Keep it minimal**: Add commands when patterns emerge from actual use (3+ occurrences)
- **Test thoroughly**: Include tests for new functionality
- **Document honestly**: Include what works AND what doesn't

### What We Need

- More domain plugins (your specialized workflows)
- Additional use cases (what projects benefit most?)
- Performance optimization (where are the bottlenecks?)
- Better documentation (what's confusing?)

---

## Writing Frameworks Architecture

**Last Updated**: November 2025 (v1.2 consolidation)

### The 2+1 Model

After 6 months of production use, we consolidated three writing frameworks into a cleaner architecture:

**2 Domain Frameworks** (workflows for specific use cases):
- **content-marketing** v1.2 - Technical B2B content production
- **ml3t-coauthor** v1.1 - Academic book authoring (ML4T 3rd edition)

**1 Shared Library** (writing methodologies):
- **writing-skills** v1.0 - 7 writing techniques usable across frameworks

### Why We Consolidated

**Before consolidation**:
- 3 frameworks with unclear differentiation
- Skill duplication (pyramid-principle, SCQA in 2 places)
- One framework (structured-intelligence) built speculatively without clear use case

**After consolidation**:
- Clear answer to "which framework?" (marketing vs book content)
- Zero skill duplication (shared writing-skills library)
- Honest assessment: deprecated framework with no use case

### Content-Marketing Framework (v1.2)

**Purpose**: Professional content production with positioning-first process

**Use cases**:
- White papers (3500-5000 words)
- Blog posts (2500 words)
- Landing pages (800 words)
- Social media content (400 words)

**Key innovation**: Positioning-first approach where strategic decisions (7 questions) precede execution

**v1.2 Enhancements** (requires writing-skills plugin):
- **Architect agent**: Optional Diátaxis framework mode for documentation content
- **Author agent**: Optional topic-sentence method and information-mapping techniques
- All enhancements are **optional** and **backward compatible**

**Commands**: /position, /research, /outline, /draft, /review

**When to use**: Marketing content, technical documentation, website copy

### ML3T Coauthor Framework (v1.1)

**Purpose**: Academic book production for Machine Learning for Trading (ML4T) 3rd edition

**Use cases**:
- Chapter writing with research integration
- Code example generation and testing
- Jupyter notebook management
- Citation tracking with Zotero

**v1.1 Enhancement** (optional writing-skills):
- Optional access to writing methodologies (pyramid-principle, SCQA, etc.)
- Fully backward compatible

**Integration**: Works with ml3t-researcher plugin (paper search, Qdrant vector DB)

**When to use**: Academic book authoring, research-heavy technical writing

### Writing-Skills Library (v1.0)

**Purpose**: Shared writing methodologies reusable across frameworks

**7 Skills**:
1. **pyramid-principle** - Hierarchical structure (answer first, then supporting points)
2. **scqa-framework** - Narrative structure (Situation-Complication-Question-Answer)
3. **excellent-writing** - 15 principles for clarity, precision, engagement
4. **diataxis-framework** - Documentation structure (tutorials, how-tos, reference, explanation)
5. **topic-sentence-method** - Clear paragraph focus and scannability
6. **information-mapping** - DITA-inspired information organization
7. **plain-language** - Accessible writing principles

**When to use**: Enable as optional dependency for content-marketing or ml3t-coauthor

### Deprecated: Structured-Intelligence

**Status**: ⚠️ DEPRECATED (November 2025)

**Why deprecated**:
- No distinct use case identified after testing
- Built speculatively based on theory, not observed need
- Violated Factory's "build for observed needs" philosophy

**Value preserved**:
- All 7 skills extracted to writing-skills library
- No methodology lost

**Migration paths**:
- **Marketing content** → Use content-marketing v1.2
- **Book content** → Use ml3t-coauthor v1.1
- **Future technical docs** → Wait for observed need, then build domain-specific framework

### Enabling Writing Frameworks

**For marketing/website content**:
```json
{
  "enabledPlugins": {
    "content-marketing@local": true,
    "writing-skills@local": true  // Optional, enables enhanced techniques
  }
}
```

**For academic book authoring**:
```json
{
  "enabledPlugins": {
    "ml3t-researcher@local": true,
    "ml3t-coauthor@local": true,
    "writing-skills@local": true  // Optional, provides writing methodologies
  }
}
```

**Standalone writing skills** (for custom workflows):
```json
{
  "enabledPlugins": {
    "writing-skills@local": true  // Access skills directly without domain framework
  }
}
```

### Lessons Learned

**What worked**:
1. **Positioning-first process** (content-marketing) - Strategic constraints before execution prevents scope creep
2. **Shared skills library** - Eliminates duplication, enables reuse
3. **Evidence-based deprecation** - Honest assessment when frameworks don't have use case
4. **Optional enhancements** - Backward compatibility while adding value

**What didn't work**:
1. **Speculative framework building** (structured-intelligence) - Theory ≠ observed need
2. **Skill duplication** - Pyramid-principle in 2 places was maintenance burden
3. **Unclear differentiation** - "Which framework?" shouldn't require analysis

**Going forward**:
- Build domain frameworks only for observed needs (3+ occurrences, >30 min each)
- Extract methodologies to writing-skills library
- Deprecate without guilt when use case doesn't emerge

---

## When Claude Code Excels

✅ Multi-file coordinated refactoring
✅ Systematic workflow automation (explore → plan → next → ship)
✅ Content production with verification (fact manifests + checkpoints)
✅ Domain-specific work with specialized plugins
✅ Long-form technical writing (with handoff discipline)

**Real gains**: 30-40% feature development reduction, 60-67% content production reduction, 67-75% literature review reduction with researcher plugin.

---

## When Claude Code Struggles

❌ Real-time systems (no persistent connections)
❌ Background monitoring (stateless execution model)
❌ One-off simple tasks (overhead not worth it)
❌ GUI applications (terminal-only)

**Work within constraints**: Context limits require handoffs. Hallucination risks require systematic verification. Execution context requires duplication. Don't fight the framework—build guardrails that work within it.

---

## ROI Reality

**Investment**:
- Learning curve: 2-4 weeks to productivity
- Setup per project: 30-60 minutes (plugin activation, memory files)
- Ongoing discipline: 10-15% overhead (handoffs, checkpoints, verification)

**Returns**:
- 30-40% feature development reduction
- 60-67% content production reduction
- 67-75% literature review reduction with researcher plugin
- Overall: 2-5x productivity gain for systematic users when discipline maintained

**The framework doesn't eliminate effort—it channels effort into systematic verification that prevents expensive mistakes.**

---

## About

Built by the Applied AI team over 6 months of production use on:
- 25-chapter ML textbook
- Technical whitepapers (20K+ words)
- Framework and plugin development
- Web applications and content production

**Website**: [Applied AI](https://appliedai.com)
**License**: MIT
**Repository**: https://github.com/your-org/claude-code-plugins

---

## Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/your-org/claude-code-plugins/issues)
- **Discussions**: Share experiences and ask questions in [GitHub Discussions](https://github.com/your-org/claude-code-plugins/discussions)
- **Consulting**: Need help implementing Claude Code in your organization? [Contact Applied AI](https://appliedai.com/contact)

---

**Use this framework. Build on our lessons. Avoid our mistakes.**

*Last updated: November 2025 | Writing Frameworks v1.2 Consolidation | Claude Code 6 months since release*
