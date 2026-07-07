---
title: "experiment"
aliases: ["exp", "ml-exp"]
---

# Run ML Experiment

Executes a machine learning experiment with comprehensive tracking and reproducibility.

## Usage

```bash
/experiment "objective" [--model algorithm] [--data path] [--validation strategy]
```

## Arguments

- **objective**: Clear description of what this experiment aims to achieve
- **--model**: ML algorithm to use (xgboost, randomforest, neural_net, etc.)
- **--data**: Path to dataset (default: looks for common patterns)
- **--validation**: Validation strategy (kfold, temporal, holdout, etc.)

## Process

The command orchestrates an ML experiment through these phases:

### 1. Setup Phase
- Creates experiment tracking JSON
- Generates unique experiment ID
- Validates data availability
- Sets random seeds for reproducibility

### 2. Data Preparation
- Loads and validates data
- Documents data shape and statistics
- Applies preprocessing pipeline
- Creates train/validation splits

### 3. Model Training
- Trains model with specified algorithm
- Tracks all hyperparameters
- Logs training metrics
- Saves model artifacts

### 4. Evaluation
- Runs comprehensive evaluation
- Generates visualizations
- Computes multiple metrics
- Creates confusion matrices

### 5. Documentation
- Updates experiment JSON with results
- Saves all artifacts
- Generates experiment report
- Links to related experiments

## Implementation

```bash
#!/bin/bash

OBJECTIVE="$ARGUMENTS"
EXPERIMENTS_DIR=".claude/experiments"
COUNTER_FILE="$EXPERIMENTS_DIR/.counter"

# Initialize experiments directory
mkdir -p "$EXPERIMENTS_DIR"
mkdir -p "$EXPERIMENTS_DIR/artifacts"
mkdir -p "$EXPERIMENTS_DIR/models"
mkdir -p "$EXPERIMENTS_DIR/plots"

# Generate experiment ID with atomic counter
get_experiment_id() {
    if [ ! -f "$COUNTER_FILE" ]; then
        echo "1" > "$COUNTER_FILE"
    fi

    # Atomic read and increment
    exec 200>"$COUNTER_FILE.lock"
    flock -x 200

    COUNTER=$(cat "$COUNTER_FILE")
    NEXT=$((COUNTER + 1))
    echo "$NEXT" > "$COUNTER_FILE"

    flock -u 200
    exec 200>&-

    printf "EXP-%03d" "$COUNTER"
}

EXP_ID=$(get_experiment_id)
EXP_FILE="$EXPERIMENTS_DIR/${EXP_ID}.json"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Create initial experiment JSON
cat > "$EXP_FILE" <<EOF
{
  "experiment_id": "$EXP_ID",
  "timestamp": "$TIMESTAMP",
  "objective": "$OBJECTIVE",
  "status": "started"
}
EOF

echo "🧪 Starting experiment $EXP_ID: $OBJECTIVE"
echo ""
echo "📊 Experiment tracking at: $EXP_FILE"
echo ""

# Invoke data-scientist agent with specific instructions
cat <<'EOF'
I need you to run an ML experiment with the following objective:

**Objective**: $ARGUMENTS

**Experiment ID**: $EXP_ID
**Tracking File**: $EXP_FILE

Please follow these steps:

1. **Data Analysis** (@data-scientist)
   - Load and validate the dataset
   - Perform EDA to understand distributions
   - Document data quality issues
   - Update the experiment JSON with data metadata

2. **Feature Engineering** (@data-scientist)
   - Create appropriate features
   - Handle missing values explicitly
   - Apply proper encoding strategies
   - Document transformations in experiment JSON

3. **Model Training** (@data-scientist)
   - Select appropriate algorithm based on problem type
   - Use proper validation strategy (TimeSeriesSplit for temporal data)
   - Set random seed to 42 for reproducibility
   - Track all hyperparameters in experiment JSON

4. **Evaluation** (@data-scientist)
   - Compute comprehensive metrics
   - Generate visualizations (ROC curves, feature importance)
   - Create confusion matrix if classification
   - Save all artifacts to experiments/artifacts/

5. **Documentation** (@data-scientist)
   - Update experiment JSON with complete results
   - Include model performance metrics
   - List all generated artifacts
   - Add notes about findings and next steps

**Experiment JSON Schema**:
```json
{
  "experiment_id": "EXP-XXX",
  "timestamp": "ISO-8601",
  "objective": "string",
  "data": {
    "source": "path",
    "version_hash": "hash",
    "shape": [rows, cols],
    "split_strategy": "string"
  },
  "preprocessing": {
    "steps": ["step1", "step2"],
    "feature_count": number
  },
  "model": {
    "algorithm": "string",
    "hyperparameters": {},
    "random_seed": 42
  },
  "validation": {
    "strategy": "string",
    "n_splits": number
  },
  "results": {
    "validation_metric": "string",
    "score": number,
    "std": number,
    "confusion_matrix": [],
    "feature_importance": {}
  },
  "artifacts": {
    "model_file": "path",
    "plots": ["path1", "path2"],
    "notebook": "path"
  },
  "status": "completed",
  "notes": "string"
}
```

**Important**:
- Use @data-scientist agent for all ML operations
- Ensure reproducibility with fixed random seeds
- Document everything in the experiment JSON
- Save all artifacts for later analysis
- Report findings honestly, including failures

Start by analyzing available data and determining the best approach for: $ARGUMENTS
EOF

# After execution, show summary
echo ""
echo "📈 Experiment $EXP_ID tracking updated"
echo ""
echo "To compare with other experiments, run:"
echo "  /evaluate --experiment $EXP_ID"
echo ""
echo "To view experiment details:"
echo "  cat $EXP_FILE | jq ."
```

## Features

### Automatic Tracking
- Unique experiment IDs with atomic counter
- JSON-based tracking for easy analysis
- Artifact management and organization
- Linkage to previous experiments

### Reproducibility
- Fixed random seeds throughout
- Environment capture (libraries, versions)
- Data versioning via hash
- Complete parameter logging

### Quality Assurance
- Automatic data validation
- Proper train/test separation
- No data leakage prevention
- Statistical significance testing

### Integration
- Works with data-scientist agent
- Compatible with /evaluate command
- Generates artifacts for /ship
- Updates project memory

## Examples

### Basic Classification Experiment
```bash
/experiment "Predict customer churn using transaction data"
```

### Regression with Specific Model
```bash
/experiment "Forecast sales next quarter" --model xgboost --validation temporal
```

### A/B Test Comparison
```bash
/experiment "Compare new feature extraction vs baseline" --data data/features_v2.csv
```

### Hyperparameter Tuning
```bash
/experiment "Optimize model hyperparameters for accuracy" --model randomforest
```

## Best Practices

1. **Clear Objectives**: State exactly what you're trying to achieve
2. **Version Control**: Commit before experiments for rollback capability
3. **Incremental Improvement**: Build on previous experiments
4. **Document Failures**: Failed experiments provide valuable insights
5. **Review Results**: Always validate results make business sense

## Error Handling

- **Missing Data**: Provides helpful error about data location
- **Invalid Model**: Lists available algorithms
- **Memory Issues**: Suggests data sampling strategies
- **Convergence Failure**: Adjusts hyperparameters automatically

## See Also

- `/evaluate` - Compare multiple experiments
- `/analyze` - Understand codebase before experiments
- `@data-scientist` - ML expertise and best practices
- `.claude/experiments/` - Experiment storage location

---

*Track ML experiments with comprehensive logging and reproducibility. Part of Claude Code Framework v3.1.*