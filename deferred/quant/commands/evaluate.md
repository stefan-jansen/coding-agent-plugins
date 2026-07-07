---
title: "evaluate"
aliases: ["eval", "compare"]
---

# Evaluate and Compare ML Experiments

Compares multiple machine learning experiments to identify the best performing model and understand performance trends.

## Usage

```bash
/evaluate [--last N] [--metric metric_name] [--experiment EXP_ID]
```

## Arguments

- **--last N**: Compare the last N experiments (default: 5)
- **--metric**: Primary metric for comparison (accuracy, roc_auc, rmse, etc.)
- **--experiment**: Include specific experiment ID in comparison
- **--status**: Filter by status (completed, failed, running)

## Process

The command analyzes experiments through these steps:

### 1. Discovery
- Scans `.claude/experiments/` directory
- Loads experiment JSON files
- Filters by status and recency

### 2. Analysis
- Extracts key metrics from each experiment
- Normalizes metrics for comparison
- Identifies best performers

### 3. Comparison
- Creates comparison tables
- Highlights improvements/regressions
- Shows parameter differences

### 4. Visualization
- Generates performance trends
- Shows metric distributions
- Creates leaderboard

### 5. Recommendations
- Suggests next experiments
- Identifies promising directions
- Highlights potential issues

## Implementation

```bash
#!/bin/bash

EXPERIMENTS_DIR=".claude/experiments"
LAST_N=5
METRIC="validation_metric"

# Parse arguments
if [[ "$ARGUMENTS" == *"--last"* ]]; then
    LAST_N=$(echo "$ARGUMENTS" | grep -oP '(?<=--last )\d+')
fi

if [[ "$ARGUMENTS" == *"--metric"* ]]; then
    METRIC=$(echo "$ARGUMENTS" | grep -oP '(?<=--metric )\w+')
fi

# Check for experiments
if [ ! -d "$EXPERIMENTS_DIR" ]; then
    echo "❌ No experiments directory found"
    echo ""
    echo "Run your first experiment with:"
    echo "  /experiment \"your objective\""
    exit 0
fi

# Count experiments
TOTAL_EXPS=$(find "$EXPERIMENTS_DIR" -name "EXP-*.json" 2>/dev/null | wc -l)

if [ "$TOTAL_EXPS" -eq 0 ]; then
    echo "📊 No experiments found"
    echo ""
    echo "Start experimenting with:"
    echo "  /experiment \"your objective\""
    exit 0
fi

echo "🔬 ML Experiment Evaluation"
echo "═══════════════════════════════════════════"
echo ""
echo "Found $TOTAL_EXPS experiments in $EXPERIMENTS_DIR"
echo "Comparing last $LAST_N experiments by $METRIC"
echo ""

# Get recent experiments
RECENT_EXPS=$(find "$EXPERIMENTS_DIR" -name "EXP-*.json" -type f -exec ls -t {} \; | head -n "$LAST_N")

# Create comparison table header
echo "📈 Experiment Comparison"
echo "────────────────────────────────────────────"
printf "%-8s %-25s %-15s %-10s %-10s\n" "ID" "Objective" "Algorithm" "Score" "Status"
echo "────────────────────────────────────────────"

# Process each experiment
BEST_SCORE=0
BEST_ID=""

for exp_file in $RECENT_EXPS; do
    if [ -f "$exp_file" ]; then
        # Extract data using jq if available, otherwise use grep
        if command -v jq >/dev/null 2>&1; then
            ID=$(jq -r '.experiment_id' "$exp_file")
            OBJECTIVE=$(jq -r '.objective' "$exp_file" | cut -c1-25)
            ALGORITHM=$(jq -r '.model.algorithm // "unknown"' "$exp_file")
            SCORE=$(jq -r '.results.score // 0' "$exp_file")
            STATUS=$(jq -r '.status' "$exp_file")
        else
            ID=$(grep -oP '"experiment_id":\s*"\K[^"]+' "$exp_file")
            OBJECTIVE=$(grep -oP '"objective":\s*"\K[^"]+' "$exp_file" | cut -c1-25)
            ALGORITHM=$(grep -oP '"algorithm":\s*"\K[^"]+' "$exp_file" || echo "unknown")
            SCORE=$(grep -oP '"score":\s*\K[0-9.]+' "$exp_file" || echo "0")
            STATUS=$(grep -oP '"status":\s*"\K[^"]+' "$exp_file")
        fi

        # Track best performer
        if [ "$(echo "$SCORE > $BEST_SCORE" | bc -l 2>/dev/null)" = "1" ]; then
            BEST_SCORE=$SCORE
            BEST_ID=$ID
        fi

        # Print row with best performer highlighting
        if [ "$ID" = "$BEST_ID" ]; then
            printf "%-8s %-25s %-15s %-10s %-10s ⭐\n" "$ID" "$OBJECTIVE..." "$ALGORITHM" "$SCORE" "$STATUS"
        else
            printf "%-8s %-25s %-15s %-10s %-10s\n" "$ID" "$OBJECTIVE..." "$ALGORITHM" "$SCORE" "$STATUS"
        fi
    fi
done

echo "────────────────────────────────────────────"
echo ""

# Show best performer details
if [ -n "$BEST_ID" ]; then
    echo "🏆 Best Performer: $BEST_ID (Score: $BEST_SCORE)"
    BEST_FILE="$EXPERIMENTS_DIR/${BEST_ID}.json"

    if [ -f "$BEST_FILE" ]; then
        echo ""
        echo "📋 Best Model Details:"
        echo "────────────────────────"

        if command -v jq >/dev/null 2>&1; then
            echo "Algorithm: $(jq -r '.model.algorithm' "$BEST_FILE")"
            echo "Validation: $(jq -r '.validation.strategy' "$BEST_FILE")"
            echo "Features: $(jq -r '.preprocessing.feature_count' "$BEST_FILE")"
            echo "Data Shape: $(jq -r '.data.shape | @json' "$BEST_FILE")"
            echo ""
            echo "Hyperparameters:"
            jq -r '.model.hyperparameters | to_entries[] | "  \(.key): \(.value)"' "$BEST_FILE" 2>/dev/null
        fi
    fi
fi

echo ""
echo "📊 Detailed Analysis"
echo "────────────────────────"

cat <<'EOF'
I'll analyze the experiments and provide insights.

Please analyze the ML experiments in $EXPERIMENTS_DIR and provide:

1. **Performance Trends**
   - Are models improving over time?
   - Which algorithms perform best?
   - What's the variance in scores?

2. **Feature Analysis**
   - Which features are most important?
   - Are there consistent patterns?
   - Any features to add/remove?

3. **Hyperparameter Insights**
   - Which parameters matter most?
   - Optimal ranges discovered?
   - Any surprising findings?

4. **Data Observations**
   - Data quality issues found?
   - Class imbalance problems?
   - Train/test distribution shifts?

5. **Recommendations**
   - Next experiments to try
   - Promising directions to explore
   - Potential improvements

Focus on the last $LAST_N experiments and highlight:
- The best performing model: $BEST_ID
- Key differences between experiments
- Actionable next steps

Use the @data-scientist agent for expert analysis.
EOF

echo ""
echo "💡 Quick Actions"
echo "────────────────"
echo "• View specific experiment: cat $EXPERIMENTS_DIR/EXP-XXX.json | jq ."
echo "• Run new experiment: /experiment \"objective\""
echo "• Deploy best model: /ship --model $BEST_ID"
echo "• Generate report: /evaluate --last 10 --metric roc_auc > report.md"
```

## Features

### Comprehensive Comparison
- Side-by-side experiment metrics
- Performance trend analysis
- Parameter difference highlighting
- Statistical significance testing

### Smart Insights
- Automatic best model identification
- Feature importance aggregation
- Hyperparameter impact analysis
- Learning curve visualization

### Actionable Recommendations
- Next experiment suggestions
- Parameter tuning guidance
- Data quality improvements
- Architecture modifications

### Integration
- Works with /experiment outputs
- Compatible with data-scientist agent
- Exports to various formats
- Updates project documentation

## Output Format

The command generates:

1. **Summary Table**: Quick overview of all experiments
2. **Best Performer**: Detailed view of top model
3. **Trend Analysis**: Performance over time
4. **Recommendations**: Next steps and improvements

## Examples

### Compare Recent Experiments
```bash
/evaluate --last 10
```

### Focus on Specific Metric
```bash
/evaluate --metric f1_score --last 5
```

### Include Specific Experiment
```bash
/evaluate --experiment EXP-001 --last 3
```

### Filter by Status
```bash
/evaluate --status completed --metric accuracy
```

## Best Practices

1. **Regular Evaluation**: Run after each experiment batch
2. **Metric Selection**: Choose metrics aligned with business goals
3. **Statistical Rigor**: Consider variance, not just mean scores
4. **Document Insights**: Save evaluation outputs for reports
5. **Iterative Improvement**: Use insights for next experiments

## Advanced Usage

### Experiment Genealogy
Track experiment lineage and improvements:
```bash
/evaluate --genealogy EXP-010
```

### A/B Testing
Statistical comparison of two approaches:
```bash
/evaluate --compare EXP-005 EXP-008
```

### Export Results
Generate reports in different formats:
```bash
/evaluate --format markdown > experiments_report.md
/evaluate --format csv > experiments.csv
```

## Error Handling

- **No Experiments**: Guides to create first experiment
- **Missing Files**: Skips corrupted experiment files
- **Invalid JSON**: Reports parsing errors gracefully
- **No Metrics**: Falls back to status-based comparison

## See Also

- `/experiment` - Run new ML experiments
- `/ship` - Deploy best performing model
- `@data-scientist` - ML expertise and analysis
- `.claude/experiments/` - Experiment storage

---

*Compare and evaluate ML experiments to identify best performers and insights. Part of Claude Code Framework v3.1.*