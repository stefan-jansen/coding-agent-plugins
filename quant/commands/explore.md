---
allowed-tools: [Task, Bash, Read, Write, Grep, MultiEdit, mcp__firecrawl__firecrawl_search, mcp__firecrawl__firecrawl_scrape, mcp__sequential-thinking__sequentialthinking]
argument-hint: "[quant strategy description or @spec-file]"
description: "Explore quantitative finance ML requirements with domain-specific validation"
---

# Quant Finance Requirements Exploration

I'll explore the quantitative finance strategy requirements with domain-specific analysis, asking critical questions about data integrity, feature engineering, and backtesting realism before planning.

**Input**: $ARGUMENTS

## Quant-Specific Analysis

This exploration focuses on critical aspects unique to quantitative finance ML:

### Data Integrity Questions
1. **Universe Definition**: How will we avoid survivorship bias?
   - Point-in-time constituent data?
   - Delisting/bankruptcy tracking?

2. **Time Handling**: Are all timestamps in UTC?
   - Data source timezone handling?
   - DST boundary handling?

3. **Corporate Actions**: How are splits/dividends adjusted?
   - Back-adjustment methodology?
   - Dividend reinvestment assumption?

### Feature Engineering Questions
4. **Labeling Method**: How do we label training examples?
   - Triple-barrier method (profit/loss/time limits)?
   - Fixed-time horizon?
   - Volatility-adjusted barriers?

5. **Feature Timing**: Are all features strictly causal?
   - Rolling windows backward-looking only?
   - No center-aligned calculations?
   - Proper lag between feature and label?

6. **Cross-Validation**: What CV method prevents leakage?
   - Purged and embargoed CV?
   - Time-series split with gap?
   - Walk-forward validation?

### Backtesting Realism Questions
7. **Transaction Costs**: What costs are modeled?
   - Commission per trade?
   - Bid-ask spread?
   - Market impact/slippage?

8. **Execution Timing**: What's the signal-to-execution lag?
   - Same-bar execution (impossible)?
   - Next-bar open execution?
   - Realistic latency for strategy frequency?

9. **Trading Frequency**: What's the target holding period?
   - Intraday (tick/minute)?
   - Daily/weekly?
   - Monthly+?

### Risk & Governance Questions
10. **Position Sizing**: How are positions sized?
    - Fixed dollar amounts (bad)?
    - Volatility-scaled (good)?
    - Kelly criterion?

11. **Risk Limits**: What hard stops exist?
    - Max drawdown circuit breaker?
    - Daily loss limit?
    - Position size limits?

12. **Reproducibility**: Can we reproduce results exactly?
    - All random seeds set?
    - Config logging in place?
    - Data versioning strategy?

## Implementation

```bash
#!/bin/bash

# Standard constants (must be copied to each command)
readonly CLAUDE_DIR=".claude"
readonly WORK_DIR="${CLAUDE_DIR}/work"
readonly WORK_CURRENT="${WORK_DIR}/current"

# Error handling functions
error_exit() {
    echo "ERROR: $1" >&2
    exit 1
}

warn() {
    echo "WARNING: $1" >&2
}

# Parse arguments
ARGUMENTS="$ARGUMENTS"
REQUIREMENT_SOURCE="$ARGUMENTS"
REQUIREMENT_TYPE="quant_strategy"

if [[ "$ARGUMENTS" =~ ^@(.+)$ ]]; then
    REQUIREMENT_SOURCE="${BASH_REMATCH[1]}"
    REQUIREMENT_TYPE="quant_spec_document"
fi

echo "💹 Exploring Quant Finance Strategy Requirements"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Source Type: $REQUIREMENT_TYPE"
if [ -n "$REQUIREMENT_SOURCE" ]; then
    echo "Strategy: $REQUIREMENT_SOURCE"
fi
echo ""

# Generate work unit ID
WORK_COUNTER_FILE="${WORK_DIR}/.counter"
mkdir -p "$WORK_DIR" "$WORK_CURRENT"

# Read and increment counter
if [ -f "$WORK_COUNTER_FILE" ]; then
    COUNTER=$(cat "$WORK_COUNTER_FILE" 2>/dev/null || echo "0")
else
    COUNTER=0
fi
COUNTER=$((COUNTER + 1))
echo "$COUNTER" > "$WORK_COUNTER_FILE"

# Create work unit ID and name
WORK_ID=$(printf "%03d" $COUNTER)
WORK_NAME="${WORK_ID}_quant_strategy"
if [ -n "$REQUIREMENT_SOURCE" ] && [ "$REQUIREMENT_TYPE" = "quant_strategy" ]; then
    SLUG=$(echo "$REQUIREMENT_SOURCE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/_/g' | sed 's/__*/_/g' | sed 's/^_//;s/_$//' | cut -c1-30)
    WORK_NAME="${WORK_ID}_${SLUG}"
fi

WORK_UNIT_DIR="${WORK_CURRENT}/${WORK_NAME}"

# Create work unit
echo "📁 Creating quant work unit: $WORK_NAME"
mkdir -p "$WORK_UNIT_DIR"

# Initialize metadata
cat > "${WORK_UNIT_DIR}/metadata.json" << EOF
{
    "id": "$WORK_ID",
    "name": "$WORK_NAME",
    "created_at": "$(date -Iseconds)",
    "requirement_type": "$REQUIREMENT_TYPE",
    "requirement_source": "$REQUIREMENT_SOURCE",
    "phase": "exploring",
    "status": "active",
    "domain": "quantitative_finance"
}
EOF

# Create quant-specific requirements template
cat > "${WORK_UNIT_DIR}/requirements.md" << EOF
# Quant Strategy Requirements

## Strategy Description
$REQUIREMENT_SOURCE

## Data Integrity
- [ ] Universe: Point-in-time constituents (avoid survivorship bias)
- [ ] Timestamps: UTC storage (avoid DST issues)
- [ ] Corporate Actions: Adjustment methodology defined
- [ ] Data Sources: Provenance and version tracking

## Feature Engineering
- [ ] Labeling: Triple-barrier method or volatility-adjusted
- [ ] Features: Strictly causal (no look-ahead)
- [ ] Rolling Windows: Backward-looking only
- [ ] Cross-Validation: Purged and embargoed time-series CV

## Backtesting Integrity
- [ ] Transaction Costs: Commission + spread + slippage
- [ ] Execution Lag: Realistic signal-to-fill timing
- [ ] Trading Frequency: [Specify: intraday/daily/weekly]
- [ ] Market Impact: Modeled for order sizes

## Risk & Governance
- [ ] Position Sizing: Volatility-scaled (not fixed)
- [ ] Risk Limits: Max drawdown, daily loss, position limits
- [ ] Kill Switch: Emergency halt capability
- [ ] Reproducibility: Seeds, config logging, data versioning

## Acceptance Criteria
- [ ] All data leakage sources eliminated
- [ ] Backtest costs realistic (not zero)
- [ ] Risk controls implemented
- [ ] Results reproducible

EOF

# Create exploration file
cat > "${WORK_UNIT_DIR}/exploration.md" << EOF
# Quant Strategy Exploration

## Domain Analysis
[Quant-specific analysis to be completed]

## Data Leakage Risks
[Identified look-ahead and survivorship risks]

## Execution Realism Assessment
[Transaction cost and timing analysis]

## Risk Control Requirements
[Hard limits and safeguards needed]

## Next Steps
[Path to implementation]

EOF

# Set as active work
echo "$WORK_NAME" > "${WORK_DIR}/ACTIVE_WORK"

echo ""
echo "✅ Quant work unit created: $WORK_NAME"
echo "📁 Location: $WORK_UNIT_DIR"
echo ""
echo "Next: Analyzing quant-specific requirements..."
```

## Phase 1: Quant-Specific Requirement Analysis

I'll analyze the strategy requirements through a quantitative finance lens, asking the 12 critical questions above to ensure we avoid the common pitfalls that cause 90% of quant strategies to fail in production.

### Sequential Thinking for Complex Strategies

For multi-asset strategies, complex labeling schemes, or high-frequency approaches, I'll use Sequential Thinking to systematically work through:
1. Data integrity risks across all assets
2. Feature leakage paths in complex transformations
3. Execution realism for the target frequency
4. Risk control architecture

### Document-Based Strategy Specs

When analyzing specification documents (@syntax):
1. **Extract Strategy Logic**: Core alpha generation methodology
2. **Identify Data Requirements**: Assets, frequency, history needed
3. **Map Leakage Risks**: Where could future data leak into features?
4. **Assess Cost Sensitivity**: How much do costs matter at this frequency?
5. **Design Risk Framework**: What limits prevent disaster?

## Phase 2: ML/Data Validator Invocation

After capturing requirements, I'll invoke the **quant-ml-validator** agent to perform static analysis:

```
/agent quant-ml-validator "Review requirements for data leakage and preprocessing risks"
```

This catches:
- Survivorship bias in universe definition
- Look-ahead leakage in feature specs
- Time-series CV violations in validation plan
- Unadjusted price data in requirements
- Missing UTC timezone specification

## Phase 3: Exploration Documentation

I'll create comprehensive documentation in the work unit:

### requirements.md
- Strategy description and objectives
- Data integrity checklist (12 items)
- Feature engineering requirements
- Backtesting realism requirements
- Risk & governance requirements
- Acceptance criteria

### exploration.md
- Domain-specific analysis findings
- Identified data leakage risks
- Execution realism assessment
- Risk control requirements
- Recommended implementation approach

## Phase 4: Next Step Recommendation

Based on exploration findings, I'll recommend:

### ✅ Ready for Planning
```
Requirements clear, data leakage risks identified
→ Run `/quant-plan` to create detailed implementation plan with validation gates
```

### ⚠️ Needs Clarification
```
Critical questions unanswered:
- Universe definition unclear (survivorship risk)
- Labeling methodology not specified
- Transaction cost assumptions missing
→ Clarify these, then run `/quant-plan`
```

## Success Indicators

- ✅ Quant work unit created with domain template
- ✅ 12 critical questions asked and answered
- ✅ Data leakage risks identified
- ✅ Execution realism requirements captured
- ✅ Risk controls specified
- ✅ ML validator invoked for early detection
- ✅ Clear path to `/quant-plan` established

## Enhanced Capabilities

### With Sequential Thinking MCP
- Systematic analysis of multi-asset strategies
- Structured risk assessment for complex alpha logic
- Step-by-step evaluation of feature engineering pipelines

### With Serena MCP
- Semantic code analysis of existing strategies
- Symbol-level understanding of data pipelines
- Impact analysis for strategy modifications

## Example Usage

```bash
# New momentum strategy
/quant-explore "daily momentum strategy on S&P 500 stocks"

# From specification document
/quant-explore @strategy-spec.md

# Mean reversion strategy
/quant-explore "intraday mean reversion on futures"
```

---

*Quant-specific exploration ensuring data integrity, execution realism, and risk controls from the start*
