---
allowed-tools: [Task, Bash, Read, Write, MultiEdit, Grep, Glob]
argument-hint: "[--preview | --checklist | --validate]"
description: "Validate quant strategy deployment readiness with comprehensive safety checks"
---

# Quant Strategy Deployment Validation

I'll perform comprehensive deployment readiness validation for the quantitative strategy, ensuring all safety controls and quality gates pass before production trading.

**Options**: $ARGUMENTS

## Deployment Readiness Philosophy

**Production trading is unforgiving. A single mistake can wipe out months of gains in minutes.**

This command runs all three validators and generates a deployment checklist verifying:
- ✅ No data leakage in pipeline
- ✅ Realistic backtest (not fantasy profits)
- ✅ Hard risk controls in place
- ✅ Kill switches operational
- ✅ Results reproducible
- ✅ Monitoring and alerts configured

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

MODE="validate"

if [[ "$ARGUMENTS" == *"--preview"* ]]; then
    MODE="preview"
elif [[ "$ARGUMENTS" == *"--checklist"* ]]; then
    MODE="checklist"
fi

echo "🚀 Quant Strategy Deployment Validation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Check for active work unit
if [ ! -f "${WORK_DIR}/ACTIVE_WORK" ]; then
    error_exit "No active work unit. Run /quant-explore first."
fi

ACTIVE_WORK=$(cat "${WORK_DIR}/ACTIVE_WORK")
WORK_UNIT_DIR="${WORK_CURRENT}/${ACTIVE_WORK}"

if [ ! -d "$WORK_UNIT_DIR" ]; then
    error_exit "Work unit not found: $WORK_UNIT_DIR"
fi

echo "📁 Strategy: $ACTIVE_WORK"

# Check for state.json
STATE_FILE="${WORK_UNIT_DIR}/state.json"
if [ ! -f "$STATE_FILE" ]; then
    error_exit "No state.json. Run /quant-plan first."
fi

# Verify all tasks completed
if command -v jq >/dev/null 2>&1; then
    TOTAL=$(jq '.tasks | length' "$STATE_FILE")
    COMPLETED=$(jq '[.tasks[] | select(.status == "completed")] | length' "$STATE_FILE")

    echo "📊 Implementation Progress: $COMPLETED/$TOTAL tasks"

    if [ $COMPLETED -lt $TOTAL ]; then
        warn "Not all tasks completed. Some validation may be incomplete."
    fi
fi

echo ""
echo "Running comprehensive deployment validation..."
```

## Phase 1: Three-Validator Audit

All three validators must pass for production deployment:

### 1. ML/Data Integrity Validation

```
/agent quant-ml-validator "Comprehensive audit of data pipeline, features, and model training"
```

**Critical Checks**:
- [ ] Point-in-time universe (no survivorship bias)
- [ ] UTC timestamps throughout pipeline
- [ ] Corporate actions properly adjusted
- [ ] Preprocessing fit only on training folds
- [ ] Rolling windows backward-looking only
- [ ] Purged and embargoed time-series CV
- [ ] Multiple testing correction applied
- [ ] No center-aligned calculations

**Severity Threshold**: ZERO Critical issues for production

### 2. Backtesting Integrity Validation

```
/agent quant-backtest-validator "Comprehensive audit of backtest execution realism"
```

**Critical Checks**:
- [ ] Transaction costs modeled (commission + spread + slippage)
- [ ] Realistic execution lag (not same-bar fills)
- [ ] Market impact for order sizes
- [ ] Futures roll costs (if applicable)
- [ ] Position/cash accounting reconciled
- [ ] No unlimited liquidity assumptions
- [ ] Bid-ask spread paid on every trade

**Performance Reality Check**:
- If Sharpe > 3.0 after costs → Likely backtest error
- If turnover > 500%/year and high Sharpe → Check execution lag
- If drawdown < 5% over 10 years → Suspicious (too good)

### 3. Risk & Governance Validation

```
/agent quant-risk-validator "Comprehensive audit of risk controls and production safety"
```

**Critical Checks**:
- [ ] Volatility-scaled position sizing (not fixed)
- [ ] Max drawdown circuit breaker (e.g., 20%)
- [ ] Daily loss limit (e.g., 2%)
- [ ] Position size limits (e.g., 5% max)
- [ ] Kill switch / emergency halt
- [ ] All random seeds set
- [ ] Config and hyperparameters logged
- [ ] Data lineage tracked
- [ ] Order execution logged

**Production Safety Requirements**:
- ALL risk controls must be tested
- Kill switch must be manually testable
- Monitoring/alerting must be operational

## Phase 2: Deployment Checklist Generation

Create comprehensive deployment checklist documenting all validations:

### Checklist Structure

```markdown
# Quant Strategy Deployment Checklist

## Strategy Overview
- **Name**: [Strategy Name]
- **Universe**: [Asset universe and size]
- **Frequency**: [Intraday/Daily/Weekly]
- **Target Capacity**: [Estimated AUM capacity]
- **Deployment Date**: [YYYY-MM-DD]

## Data Integrity ✅/❌
- [ ] Point-in-time universe (no survivorship)
- [ ] UTC timestamps (DST-safe)
- [ ] Corporate actions adjusted
- [ ] Data sources documented
- [ ] Data lineage tracked

## Feature Engineering ✅/❌
- [ ] All features strictly causal
- [ ] No look-ahead leakage
- [ ] Rolling windows backward only
- [ ] Preprocessing scoped to training folds
- [ ] Cross-validation properly purged/embargoed

## Backtesting Integrity ✅/❌
- [ ] Transaction costs: ____% per trade
- [ ] Bid-ask spread: ____bps
- [ ] Slippage model: [description]
- [ ] Execution lag: ____ [bars/seconds]
- [ ] Market impact for large orders
- [ ] Position accounting reconciled

## Performance Metrics (Post-Cost)
- **Sharpe Ratio**: ____ (deflated if grid search)
- **Max Drawdown**: ____%
- **Annual Return**: ____%
- **Annual Turnover**: ____%
- **Capacity Estimate**: $____M

## Risk Controls ✅/❌
- [ ] Position sizing: Volatility-scaled
- [ ] Max drawdown stop: ____%
- [ ] Daily loss limit: ____%
- [ ] Max position size: ____%
- [ ] Kill switch tested: YES/NO
- [ ] Circuit breaker tested: YES/NO

## Reproducibility ✅/❌
- [ ] All random seeds set
- [ ] Config logged for every run
- [ ] Code version tracked (git commit)
- [ ] Data version tracked
- [ ] Model checkpoints saved with metadata

## Monitoring & Alerts ✅/❌
- [ ] Real-time P&L tracking
- [ ] Drawdown monitoring
- [ ] Position size monitoring
- [ ] Order fill quality tracking
- [ ] Data staleness alerts
- [ ] Execution lag monitoring

## Production Infrastructure ✅/❌
- [ ] Order execution system tested
- [ ] Fill logging operational
- [ ] Risk limit enforcement tested
- [ ] Emergency halt procedure documented
- [ ] Rollback plan exists
- [ ] Incident response plan

## Validation Results
- **ML Validator**: PASS/FAIL (__ Critical, __ Warnings)
- **Backtest Validator**: PASS/FAIL (__ Critical, __ Warnings)
- **Risk Validator**: PASS/FAIL (__ Critical, __ Warnings)

## Deployment Approval
- [ ] All Critical issues resolved
- [ ] All risk controls tested
- [ ] Performance expectations realistic
- [ ] Capacity appropriate for AUM
- [ ] Team review completed

**GO/NO-GO**: _______

**Approved By**: ___________ Date: __________
```

## Phase 3: Performance Reality Assessment

Validate that backtest metrics are realistic:

### Red Flags (Likely Backtest Errors)
- **Sharpe > 3.5** after costs → Check for data leakage or unrealistic fills
- **Drawdown < 5%** over 10 years → Too good, missing costs or risk
- **Win rate > 70%** with high turnover → Likely look-ahead bias
- **Returns spike around** corporate actions → Unadjusted prices
- **Performance degrades** out-of-sample → Overfit to training period

### Capacity Estimation
```
Estimated Capacity = (Daily Volume * Price * % Participation) / Strategy Weight
                   × Impact Tolerance / Turnover
```

**Example**:
- Universe: S&P 500 (avg $500M daily volume)
- Participation: 10% (conservative)
- Impact tolerance: 10bps
- Turnover: 200%/year
- **Capacity**: ~$50M-100M

### Performance Expectations
Set realistic expectations for live trading:
- **Sharpe decay**: 20-40% from backtest to live (typical)
- **Higher costs**: Live slippage often 2-3x backtest estimates
- **Execution challenges**: Partial fills, queue position, adverse selection
- **First 3 months**: Expect underperformance during calibration

## Phase 4: Production Deployment Guidance

### Pre-Deployment Steps
1. **Paper Trading** (1-3 months):
   - Simulate orders without real execution
   - Validate fill assumptions
   - Calibrate cost models
   - Test kill switches and limits

2. **Small-Scale Live** (1-2 months):
   - 5-10% of target size
   - Validate execution quality
   - Refine slippage estimates
   - Monitor risk controls

3. **Gradual Ramp**:
   - Increase 25% per month if performance in line
   - Halt ramp if significant deviation
   - Re-validate capacity assumptions

### Post-Deployment Monitoring
- **Daily**: P&L, drawdown, position limits
- **Weekly**: Execution quality, turnover, correlations
- **Monthly**: Sharpe, capacity utilization, drift detection
- **Quarterly**: Full re-validation of all assumptions

### When to Kill the Strategy
- Drawdown exceeds limit (automated)
- Sharpe degrades > 50% for 3 months (review)
- Capacity constraints binding (reduce size or retire)
- Market regime change invalidates assumptions

## Phase 5: Delivery Documentation

Generate final deployment package:

### Documentation Artifacts
1. **deployment-checklist.md**: Comprehensive validation checklist
2. **performance-report.md**: Backtest metrics and capacity analysis
3. **risk-controls.md**: All limits, circuit breakers, procedures
4. **monitoring-plan.md**: Metrics, alerts, dashboards
5. **runbook.md**: Deployment, operations, incident response

### Code Deliverables
- Clean, production-ready codebase
- All tests passing
- Configuration externalized
- Logging comprehensive
- Error handling robust

## Success Indicators

- ✅ All three validators passed (or only minor warnings)
- ✅ ZERO Critical data leakage issues
- ✅ Transaction costs realistically modeled
- ✅ All risk controls tested and operational
- ✅ Kill switch manually verified
- ✅ Reproducibility confirmed (results match)
- ✅ Performance expectations realistic
- ✅ Capacity appropriate for target AUM
- ✅ Deployment checklist complete
- ✅ Paper trading plan ready

## Deployment Decision

Based on validation results:

### ✅ APPROVED FOR DEPLOYMENT
```
All validation gates passed
Risk controls operational
Performance expectations realistic
→ Proceed to paper trading phase
```

### ⚠️ CONDITIONAL APPROVAL
```
Minor warnings found, no Critical issues
Risk controls operational
Performance needs calibration
→ Address warnings, then paper trade
```

### ❌ NOT READY FOR DEPLOYMENT
```
Critical issues found:
- [List Critical issues from validators]
→ Fix all Critical issues before deployment
→ Re-run /quant-ship after fixes
```

## Critical Reminder

**Never deploy a quant strategy to production without**:
1. All three validators passing
2. Kill switch manually tested
3. Risk limits proven to work
4. Realistic cost/slippage assumptions
5. Paper trading validation

**One uncaught data leakage or missing risk control can cause catastrophic losses.**

---

*Comprehensive deployment validation ensuring production safety for quantitative trading strategies*
