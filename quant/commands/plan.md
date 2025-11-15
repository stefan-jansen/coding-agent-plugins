---
allowed-tools: [Task, Bash, Read, Write, Grep, MultiEdit, mcp__sequential-thinking__sequentialthinking]
argument-hint: "[additional planning guidance]"
description: "Create quant strategy implementation plan with validation gates and cost modeling"
---

# Quant Strategy Implementation Planning

I'll create a detailed implementation plan for the quantitative strategy with built-in validation gates and execution realism requirements.

**Input**: $ARGUMENTS

## Quant-Specific Planning Enhancements

This planning phase adds critical quant finance considerations that prevent the 90% of strategies that fail in production:

### Data Pipeline Planning
- **Point-in-Time Universe**: Plan for PIT database integration
- **Corporate Actions**: Schedule adjustment pipeline implementation
- **UTC Enforcement**: Plan timezone handling from day 1
- **Data Lineage**: Design provenance tracking system

### Feature Engineering Architecture
- **Labeling Infrastructure**: Triple-barrier method implementation
- **Rolling Window Safety**: Ensure all windows are backward-looking
- **Cross-Validation Setup**: Purged and embargoed time-series CV
- **Preprocessing Pipeline**: Fit-transform within CV folds only

### Backtesting Infrastructure
- **Cost Modeling**: Commission + spread + slippage framework
- **Execution Simulator**: Realistic signal-to-fill lag
- **Market Impact**: Square-root model for order sizing
- **Position Accounting**: Full cash/position reconciliation

### Risk Management Framework
- **Position Sizing**: Volatility-scaled allocation system
- **Hard Limits**: Drawdown circuit breaker, daily loss cap
- **Kill Switch**: Emergency halt mechanism
- **Monitoring Dashboard**: Real-time risk metrics

## Implementation

```bash
#!/bin/bash

# Standard constants
readonly CLAUDE_DIR=".claude"
readonly WORK_DIR="${CLAUDE_DIR}/work"
readonly WORK_CURRENT="${WORK_DIR}/current"

error_exit() {
    echo "ERROR: $1" >&2
    exit 1
}

echo "📊 Creating Quant Strategy Implementation Plan"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Find active work unit
ACTIVE_WORK=$(cat "${WORK_DIR}/ACTIVE_WORK" 2>/dev/null || echo "")
if [ -z "$ACTIVE_WORK" ]; then
    error_exit "No active work unit. Run /quant-explore first."
fi

WORK_UNIT_DIR="${WORK_CURRENT}/${ACTIVE_WORK}"
if [ ! -d "$WORK_UNIT_DIR" ]; then
    error_exit "Work unit not found: $WORK_UNIT_DIR"
fi

# Check if quant work unit
DOMAIN=$(grep '"domain"' "${WORK_UNIT_DIR}/metadata.json" 2>/dev/null | grep -o 'quantitative_finance' || echo "")
if [ -z "$DOMAIN" ]; then
    warn "Not a quant work unit. Consider using standard /plan instead."
fi

echo "📁 Work Unit: $ACTIVE_WORK"
echo ""

# Check for requirements
if [ ! -f "${WORK_UNIT_DIR}/requirements.md" ]; then
    error_exit "requirements.md not found. Run /quant-explore first to capture requirements."
fi

echo "✅ Requirements found"
echo ""
echo "Creating quant-specific implementation plan with validation gates..."
```

## Phase 1: Quant Requirements Validation

Before planning, I'll validate that critical quant requirements are captured:

### Data Integrity Checklist
- [ ] Universe definition avoids survivorship bias
- [ ] Timestamps in UTC (DST-safe)
- [ ] Corporate actions adjustment method defined
- [ ] Data provenance tracking planned

### Feature Engineering Checklist
- [ ] Labeling methodology specified (triple-barrier recommended)
- [ ] All features strictly causal (no look-ahead)
- [ ] Rolling windows backward-looking only
- [ ] Cross-validation method prevents leakage

### Backtesting Realism Checklist
- [ ] Transaction costs modeled (commission + spread + slippage)
- [ ] Execution lag realistic for strategy frequency
- [ ] Market impact for large orders
- [ ] Position accounting with cash reconciliation

### Risk Framework Checklist
- [ ] Position sizing volatility-scaled (not fixed)
- [ ] Hard risk limits defined (drawdown, daily loss)
- [ ] Kill switch/circuit breaker planned
- [ ] Reproducibility (seeds, logging, versioning)

## Phase 2: Sequential Planning with Validation Gates

I'll create a phased plan with validation checkpoints:

### Phase 1: Data Infrastructure (Foundation)
**Tasks**:
1. Setup point-in-time universe database
2. Implement corporate actions adjustment pipeline
3. Create UTC timezone handling layer
4. Build data lineage tracking system

**Validation Gate**: `/agent quant-ml-validator "Review data pipeline for leakage risks"`

### Phase 2: Feature Engineering Pipeline
**Tasks**:
5. Implement triple-barrier labeling method
6. Create backward-only rolling window library
7. Setup purged/embargoed time-series CV
8. Build preprocessing pipeline with proper scoping

**Validation Gate**: `/agent quant-ml-validator "Review feature pipeline for temporal violations"`

### Phase 3: Backtesting Infrastructure
**Tasks**:
9. Implement transaction cost model (commission + spread + slippage)
10. Create execution simulator with realistic lag
11. Add market impact for order sizing
12. Build position/cash accounting with reconciliation

**Validation Gate**: `/agent quant-backtest-validator "Review backtest for execution realism"`

### Phase 4: Model Training & Validation
**Tasks**:
13. Implement model training with purged CV
14. Add multiple testing correction (deflated Sharpe)
15. Create walk-forward out-of-sample validation
16. Build performance attribution system

**Validation Gate**: `/agent quant-ml-validator "Review training for overfitting risks"`

### Phase 5: Risk Management
**Tasks**:
17. Implement volatility-scaled position sizing
18. Add hard risk limits (drawdown, daily loss)
19. Create kill switch and circuit breakers
20. Build risk monitoring dashboard

**Validation Gate**: `/agent quant-risk-validator "Review risk controls for production readiness"`

### Phase 6: Production Deployment
**Tasks**:
21. Setup reproducibility (seeds, config logging, versioning)
22. Create data lineage audit system
23. Implement order execution and fill logging
24. Deploy monitoring and alerting

**Validation Gate**: `/agent quant-risk-validator "Final production safety audit"`

## Phase 3: Create Detailed Task Breakdown

For each phase, I'll create detailed tasks with:

### Task Structure
```json
{
  "id": "TASK-001",
  "title": "Setup Point-in-Time Universe Database",
  "description": "Create database for historical index constituents to avoid survivorship bias",
  "type": "foundation",
  "phase": "data_infrastructure",
  "status": "pending",
  "dependencies": [],
  "quant_principle": "DAT-SURVIVORSHIP-002",
  "acceptance_criteria": [
    "Database contains historical S&P 500 constituents from 2000",
    "Query function get_universe_at_date(date, index='SP500') works",
    "Includes delisting dates and reasons",
    "Test: Universe size changes over time (not constant 500)"
  ],
  "validation_agent": "quant-ml-validator",
  "estimated_hours": 4,
  "priority": "critical"
}
```

### Cost/Slippage Modeling Tasks
Special attention to backtesting realism:
- **Commission Model**: Per-trade and per-share commission structures
- **Bid-Ask Spread**: Time-of-day and liquidity-dependent spreads
- **Market Impact**: Square-root model `impact = k * sqrt(order_size / ADV)`
- **Execution Lag**: Signal generation timestamp → order transmission → fill

### Time-Series CV Tasks
Proper validation to prevent leakage:
- **Purged K-Fold**: Remove overlapping labels between train/test
- **Embargo Period**: Gap between train and test sets (≥ label horizon)
- **Walk-Forward**: Expanding or sliding window validation
- **Multiple Testing**: Deflated Sharpe ratio for parameter searches

## Phase 4: Backtest Validator Invocation

After creating the plan, I'll invoke the **quant-backtest-validator** to review:

```
/agent quant-backtest-validator "Review implementation plan for backtesting integrity"
```

This validates:
- Transaction cost modeling is included in infrastructure
- Execution lag is enforced in backtest design
- Market impact modeling for realistic fills
- Position accounting reconciliation planned

## Phase 5: State File Creation

I'll create `state.json` with quant-specific metadata:

```json
{
  "project": {
    "name": "Quant Strategy: [name]",
    "type": "quantitative_finance_ml",
    "trading_frequency": "[intraday/daily/weekly]",
    "created_at": "2025-01-24T10:00:00Z"
  },
  "status": "planning_complete",
  "quant_metadata": {
    "universe": "[description]",
    "labeling_method": "triple_barrier",
    "cv_method": "purged_embargoed_kfold",
    "cost_model": "commission_spread_impact",
    "risk_limits": {
      "max_drawdown": 0.20,
      "max_daily_loss": 0.02,
      "max_position_size": 0.05
    }
  },
  "validation_gates": [
    {"phase": "data_infrastructure", "agent": "quant-ml-validator"},
    {"phase": "feature_engineering", "agent": "quant-ml-validator"},
    {"phase": "backtesting", "agent": "quant-backtest-validator"},
    {"phase": "model_training", "agent": "quant-ml-validator"},
    {"phase": "risk_management", "agent": "quant-risk-validator"},
    {"phase": "deployment", "agent": "quant-risk-validator"}
  ],
  "tasks": [...],
  "next_available": ["TASK-001"]
}
```

## Phase 6: Implementation Plan Document

I'll create `plan.md` with comprehensive quant strategy plan:

### Sections
1. **Strategy Overview**: Objective, universe, frequency, expected capacity
2. **Architecture**: Data → Features → Model → Backtest → Risk → Deploy
3. **Task Breakdown**: Phased tasks with validation gates
4. **Quality Metrics**: Sharpe (deflated), max drawdown, turnover, capacity
5. **Risk Controls**: Hard limits, kill switches, monitoring
6. **Timeline**: Effort estimates with critical path

### Quant-Specific Considerations
- **Data Quality First**: Can't backtest without clean data
- **Validation Before Training**: Prevent garbage-in, garbage-out
- **Cost Modeling Early**: Know if strategy is viable before optimization
- **Risk Framework Upfront**: Production safety is not an afterthought

## Success Indicators

- ✅ Phased plan with validation gates
- ✅ Data integrity tasks prioritized
- ✅ Cost modeling in backtest infrastructure
- ✅ Time-series CV properly designed
- ✅ Risk controls planned from start
- ✅ Backtesting validator reviewed plan
- ✅ State file ready for `/quant-next`
- ✅ Clear path to production-ready strategy

## Next Steps

After planning:
```bash
/quant-next  # Execute first task with phase-appropriate validation
```

The `/quant-next` command will:
1. Execute current task
2. Run relevant validator at phase checkpoints
3. Update state and progress to next task

## Enhanced Capabilities

### With Sequential Thinking MCP
- Systematic planning of complex multi-asset strategies
- Structured analysis of execution realism requirements
- Step-by-step risk framework design

### With Serena MCP (if existing codebase)
- Semantic analysis of existing strategy code
- Impact assessment for modifications
- Integration planning with existing infrastructure

---

*Quant-specific planning with built-in validation gates preventing the common mistakes that cause production failures*
