---
name: lightgbm-training
description: Use when training LightGBM models with time-series cross-validation. Covers lightgbm.cv usage, hyperparameter relationships (depth vs leaves), regularization patterns, and iteration exploration without look-ahead bias from early stopping.
allowed-tools: Read,Write,Edit,Bash(python:*),Grep
version: 1.0.0
---

# LightGBM Training for Time-Series ML

This skill covers LightGBM-specific training patterns for financial ML:
1. Using `lightgbm.cv` correctly with time-series folds
2. Hyperparameter relationships and regularization
3. Iteration count exploration without look-ahead bias

## 1. Core Principles

### No Early Stopping on Validation

**THE CRITICAL MISTAKE:**
```python
# WRONG - creates look-ahead bias
model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    callbacks=[lgb.early_stopping(stopping_rounds=50)]
)
# At training time, you don't know which iteration optimizes future performance!
```

**CORRECT APPROACH:**
```python
# Train to max iterations, explore multiple stopping points
boosters = lightgbm.cv(
    params, train_set,
    num_boost_round=500,
    folds=time_series_splitter,
    return_cvbooster=True
)
# Then generate predictions at iterations [50, 100, 150, ..., 500]
# Compare in backtest to find best iteration WITHOUT look-ahead
```

### Tree Complexity Must Be Constrained

Unconstrained trees memorize training data. Financial data is noisy - regularization is essential.

### Validation Metrics ≠ Backtest Results

Information Coefficient (IC) or AUC on validation don't directly predict trading profitability. Generate predictions at multiple iteration counts and compare backtest results.

## 2. Depth vs Leaves Relationship

### The Mathematical Constraint

A binary tree of depth D has at most 2^D leaves:

```python
max_depth = 5  → max 32 leaves
max_depth = 6  → max 64 leaves
max_depth = 7  → max 128 leaves
max_depth = 8  → max 256 leaves
```

### Common Configuration Mistakes

```python
# WRONG - leaves exceed 2^depth
params = {
    'max_depth': 5,
    'num_leaves': 64,  # Impossible! 2^5 = 32
}

# WRONG - very deep tree with no leaf constraint
params = {
    'max_depth': 12,  # 2^12 = 4096 possible leaves!
    'num_leaves': 4096,
}
```

### Correct Patterns

**Pattern A: Depth-Constrained**
```python
params = {
    'max_depth': 5,
    'num_leaves': 31,  # ≤ 2^5
    # Additional regularization
    'min_child_weight': 10,
    'lambda_l2': 1.0,
}
```

**Pattern B: Leaf-Wise with Strong Constraints**
```python
params = {
    # No max_depth specified
    'num_leaves': 31,
    # Strong regularization required
    'min_child_weight': 20,
    'min_gain_to_split': 0.01,
    'lambda_l1': 0.5,
    'lambda_l2': 2.0,
    'feature_fraction': 0.7,
    'bagging_fraction': 0.8,
    'bagging_freq': 1,
}
```

## 3. Essential Regularization Parameters

### Feature Subsampling

```python
'feature_fraction': 0.5 - 0.9
```

Column subsampling per tree. Prevents over-reliance on correlated features.

**Recommended**: Start with 0.7

### Bagging (Row Subsampling)

```python
'bagging_fraction': 0.7 - 0.9
'bagging_freq': 1
```

Row subsampling per iteration. Reduces variance.

**Recommended**: `bagging_fraction=0.8, bagging_freq=1`

### Minimum Child Weight

```python
'min_child_weight': 5 - 20
```

Minimum sum of instance weights (hessian) in a child. Prevents tiny leaves.

**Recommended**: 10-15 for minute data

### Minimum Data in Leaf

```python
'min_data_in_leaf': 50 - 500
```

Alternative to min_child_weight. Minimum number of samples in a leaf.

**Recommended**: 100-200 for large datasets

### L1/L2 Regularization

```python
'lambda_l1': 0.0 - 1.0  # L1 on leaf scores
'lambda_l2': 0.0 - 5.0  # L2 on leaf scores
```

Very effective for noisy financial data.

**Recommended**: Start with `lambda_l2=1.0`

### Minimum Gain to Split

```python
'min_gain_to_split': 0.01 - 0.1
```

Minimum loss reduction required to make further partition. Good for noisy data.

**Recommended**: 0.01 for financial data

## 4. Recommended Parameter Sets

### Conservative (Shallow Trees)

```python
params = {
    'objective': 'binary',  # or 'regression'
    'metric': 'auc',  # or 'rmse'
    'boosting_type': 'gbdt',
    'learning_rate': 0.01,
    'max_depth': 5,
    'num_leaves': 31,
    'min_child_weight': 15,
    'lambda_l2': 2.0,
    'feature_fraction': 0.7,
    'bagging_fraction': 0.8,
    'bagging_freq': 1,
    'verbosity': -1,
}
```

**Use when**: Small feature set (<50 features), concerned about overfitting

### Moderate (Balanced)

```python
params = {
    'objective': 'regression',
    'metric': 'rmse',
    'boosting_type': 'gbdt',
    'learning_rate': 0.01,
    'max_depth': 6,
    'num_leaves': 63,
    'min_child_weight': 10,
    'lambda_l1': 0.5,
    'lambda_l2': 1.0,
    'feature_fraction': 0.8,
    'bagging_fraction': 0.8,
    'bagging_freq': 1,
    'min_gain_to_split': 0.01,
    'verbosity': -1,
}
```

**Use when**: Medium feature set (50-200 features), typical use case

### Aggressive (Leaf-Wise)

```python
params = {
    'objective': 'regression',
    'metric': 'rmse',
    'boosting_type': 'gbdt',
    'learning_rate': 0.01,
    # No max_depth
    'num_leaves': 63,
    'min_child_weight': 20,
    'lambda_l1': 1.0,
    'lambda_l2': 2.0,
    'feature_fraction': 0.6,
    'bagging_fraction': 0.7,
    'bagging_freq': 1,
    'min_gain_to_split': 0.05,
    'verbosity': -1,
}
```

**Use when**: Large feature set (>200 features), need expressive trees

## 5. lightgbm.cv Workflow

### Basic Usage with Custom Folds

```python
import lightgbm as lgb
from ml_cv_pipeline import CMETimeSeriesSplit  # From ml-cv-pipeline skill

# Create dataset
train_data = lgb.Dataset(
    features,
    label=labels,
    free_raw_data=False,  # Keep raw data for reuse
)

# Define folds
ts_splitter = CMETimeSeriesSplit(folds)

# Run CV
cv_results = lgb.cv(
    params,
    train_data,
    num_boost_round=500,
    folds=ts_splitter,
    return_cvbooster=True,  # Return trained boosters
    eval_train_metric=True,  # Track train metrics
)
```

### Custom Metric (Spearman IC)

```python
from scipy.stats import spearmanr

def spearman_ic(y_pred, train_data):
    """
    Custom LightGBM eval metric: Spearman rank correlation (IC).
    """
    y_true = train_data.get_label()

    # Handle edge cases
    if len(y_true) < 2 or y_pred.std() == 0:
        return 'ic', 0.0, True

    ic, _ = spearmanr(y_true, y_pred)
    return 'ic', ic, True  # (name, value, is_higher_better)

# Use in cv
cv_results = lgb.cv(
    params,
    train_data,
    num_boost_round=500,
    folds=ts_splitter,
    feval=spearman_ic,
    return_cvbooster=True,
)
```

### Extracting Boosters

```python
# cv_results is a dict with 'cvbooster' key
cvbooster = cv_results['cvbooster']

# Get booster for specific fold
fold_booster = cvbooster.boosters[fold_idx]

# Generate predictions at specific iteration
predictions = fold_booster.predict(
    features,
    num_iteration=150  # Use only first 150 trees
)
```

## 6. Iteration Exploration Strategy

### Generate Predictions for Multiple Iterations

```python
def explore_iterations(
    cvbooster,
    features: pd.DataFrame,
    folds: list,
    iteration_counts: list = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
):
    """
    Generate OOS predictions for multiple iteration counts.

    Parameters
    ----------
    cvbooster : lgb.CVBooster
        Trained CV booster from lgb.cv
    features : pd.DataFrame
        Full feature matrix
    folds : list
        Fold definitions
    iteration_counts : list
        Iterations to evaluate

    Returns
    -------
    dict
        {iteration_count: oos_predictions}
    """
    results = {}

    for n_iter in iteration_counts:
        fold_predictions = []

        for fold_idx, fold in enumerate(folds):
            # Get validation mask
            val_mask = (
                (features.index >= fold['val_start']) &
                (features.index < fold['val_end'])
            )
            X_val = features[val_mask]

            # Predict with this fold's booster at n_iter trees
            booster = cvbooster.boosters[fold_idx]
            preds = booster.predict(X_val, num_iteration=n_iter)

            fold_predictions.append(
                pd.Series(preds, index=X_val.index)
            )

        # Concatenate OOS predictions
        oos = pd.concat(fold_predictions).sort_index()
        results[n_iter] = oos

    return results
```

### Compare in Backtest

```python
# Generate signals for each iteration candidate
iteration_results = explore_iterations(cvbooster, features, folds)

# For each iteration count, run backtest
backtest_results = {}
for n_iter, oos_preds in iteration_results.items():
    # Generate signals (see ml-cv-pipeline skill)
    signals = calibrate_signals(oos_preds, folds)

    # Run backtest
    bt_result = backtest(signals, prices)  # Your backtest function

    backtest_results[n_iter] = {
        'sharpe': bt_result.sharpe,
        'returns': bt_result.cumulative_returns,
        'trades': bt_result.num_trades,
    }

# Select best iteration based on backtest
best_iter = max(backtest_results.items(), key=lambda x: x[1]['sharpe'])[0]
```

## 7. Learning Curves

```python
def plot_learning_curves(cv_results):
    """Plot train/val metrics over iterations."""
    import matplotlib.pyplot as plt

    # cv_results contains 'metric_name-mean', 'metric_name-stdv'
    train_metric = cv_results['train-rmse-mean']  # Adjust metric name
    val_metric = cv_results['valid-rmse-mean']

    plt.figure(figsize=(10, 6))
    plt.plot(train_metric, label='Train')
    plt.plot(val_metric, label='Validation')
    plt.xlabel('Iteration')
    plt.ylabel('RMSE')
    plt.legend()
    plt.title('Learning Curves')
    plt.show()
```

## 8. Common Mistakes

### Mistake 1: Early Stopping on Validation
```python
# WRONG
model.fit(X, y, eval_set=[(X_val, y_val)], callbacks=[lgb.early_stopping(50)])
```

### Mistake 2: Incompatible Depth/Leaves
```python
# WRONG
params = {'max_depth': 5, 'num_leaves': 100}  # 100 > 2^5
```

### Mistake 3: No Regularization
```python
# WRONG - will overfit on financial data
params = {'max_depth': 10, 'num_leaves': 1024}  # No constraints!
```

### Mistake 4: Forgetting free_raw_data
```python
# WRONG - can't reuse dataset for multiple CV runs
train_data = lgb.Dataset(X, y, free_raw_data=True)
```

## 9. Checklist

Before training:

- [ ] Parameters respect depth/leaves relationship
- [ ] Regularization parameters set (feature_fraction, bagging, min_child_weight)
- [ ] Custom folds defined with explicit timestamps
- [ ] Dataset created with `free_raw_data=False`
- [ ] No early stopping on validation folds
- [ ] Plan to explore multiple iteration counts
- [ ] Custom metrics defined if needed (IC for regression)

## References

For detailed patterns, see:
- `{baseDir}/references/lgbm-cv-examples.md`
- `{baseDir}/references/hyperparameter-tuning.md`
