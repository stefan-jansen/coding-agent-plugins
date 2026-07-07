---
name: ml-cv-pipeline
description: This skill should be used when the user asks about "time-series CV", "cross-validation setup", "walk-forward validation", "out-of-sample predictions", or when setting up ML cross-validation pipelines, computing labels/thresholds, or generating OOS predictions without look-ahead bias.
compatibility: Requires scikit-learn, pandas
allowed-tools: Read,Write,Edit,Bash(python:*),Grep
version: 1.0.0
---

# ML Time-Series Cross-Validation Pipeline

This skill covers the complete pre-backtest ML workflow:
1. Time-series cross-validation setup
2. Label definition and thresholding
3. Out-of-sample prediction generation

All procedures must avoid look-ahead bias.

## 1. Time-Series Cross-Validation Fundamentals

### Core Principle: No Shuffling, Ever

Time-series CV differs fundamentally from standard CV:

```python
# WRONG - standard sklearn CV shuffles
from sklearn.model_selection import KFold
kf = KFold(n_splits=5, shuffle=True)  # NEVER for time series

# CORRECT - time-aware splitting
# Validation folds are consecutive, not random
```

### Walk-Forward Validation Structure

```
Training Window     | Validation
[================] -> [====]     Fold 1
  [================] -> [====]   Fold 2
    [================] -> [====] Fold 3
```

**Key parameters:**
- Training: 52-104 weeks of data
- Validation: 4 consecutive weeks
- Folds: Non-overlapping validation periods

### Fold Definition Requirements

Each fold must specify:
```python
fold = {
    'fold_id': 1,
    'train_start': pd.Timestamp('2023-01-08 17:00:00', tz='America/Chicago'),
    'train_end': pd.Timestamp('2024-01-05 16:00:00', tz='America/Chicago'),
    'val_start': pd.Timestamp('2024-01-07 17:00:00', tz='America/Chicago'),
    'val_end': pd.Timestamp('2024-02-02 16:00:00', tz='America/Chicago'),
}
```

**Critical**: Store as timestamps with timezone, not dates or week numbers.

### CME Session Alignment

Fold boundaries must align to CME session boundaries:
- Start: Sunday 5:00 PM CT (session start)
- End: Friday 4:00 PM CT (before weekend break)

See `cme-futures-data` skill for session date handling.

## 2. Label Definition

### Continuous Labels (Regression)

Forward returns over horizon H:
```python
# Future return as label
labels = prices.pct_change(H).shift(-H)
```

### Event-Based Labels (Classification)

Threshold-based labeling for tail prediction:

```python
# Long model: predict upper tail (large positive returns)
# Short model: predict lower tail (large negative returns)
```

### Common Confusion: Long vs Short Labeling

**Long model** targets the **upper tail**:
- Label = 1 when future return >= 95th percentile
- Predicting "price will go UP significantly"

**Short model** targets the **lower tail**:
- Label = 1 when future return <= 5th percentile
- Predicting "price will go DOWN significantly"

```python
# CORRECT labeling
def create_labels(returns, percentile, model_type):
    """
    Create binary labels for tail prediction.

    Parameters
    ----------
    returns : pd.Series
        Forward returns
    percentile : float
        Threshold percentile (e.g., 95 for long, 5 for short)
    model_type : str
        'long' or 'short'
    """
    if model_type == 'long':
        # Upper tail - returns >= threshold
        threshold = returns.quantile(percentile / 100)
        labels = (returns >= threshold).astype(int)
    elif model_type == 'short':
        # Lower tail - returns <= threshold
        threshold = returns.quantile(percentile / 100)
        labels = (returns <= threshold).astype(int)
    else:
        raise ValueError("model_type must be 'long' or 'short'")

    return labels, threshold
```

## 3. Percentile Computation: Training Data Only

### The Look-Ahead Trap

```python
# WRONG - percentiles computed on all data including validation
threshold = all_returns.quantile(0.95)
labels = (all_returns >= threshold).astype(int)

# This leaks validation information into label definition!
```

### Correct Approach: Per-Fold Training Percentiles

```python
def compute_fold_labels(returns, folds, percentile, model_type):
    """
    Compute labels using training-only percentiles per fold.

    Parameters
    ----------
    returns : pd.Series
        Forward returns for entire dataset
    folds : list
        List of fold definitions with train/val timestamps
    percentile : float
        Threshold percentile
    model_type : str
        'long' or 'short'

    Returns
    -------
    dict
        Labels and thresholds per fold
    """
    results = {}

    for fold in folds:
        # Extract training returns
        train_mask = (
            (returns.index >= fold['train_start']) &
            (returns.index < fold['train_end'])
        )
        train_returns = returns[train_mask]

        # Compute threshold from training data ONLY
        if model_type == 'long':
            threshold = train_returns.quantile(percentile / 100)
        else:  # short
            threshold = train_returns.quantile(percentile / 100)

        # Apply threshold to both train and val
        val_mask = (
            (returns.index >= fold['val_start']) &
            (returns.index < fold['val_end'])
        )

        if model_type == 'long':
            train_labels = (train_returns >= threshold).astype(int)
            val_labels = (returns[val_mask] >= threshold).astype(int)
        else:
            train_labels = (train_returns <= threshold).astype(int)
            val_labels = (returns[val_mask] <= threshold).astype(int)

        results[fold['fold_id']] = {
            'threshold': threshold,
            'train_labels': train_labels,
            'val_labels': val_labels,
        }

    return results
```

## 4. Prediction Threshold Calibration

After model training, predictions must be converted to signals.

### The Same Rule Applies

Prediction thresholds come from **training predictions only**:

```python
def calibrate_prediction_threshold(
    train_predictions,
    val_predictions,
    percentile,
    model_type
):
    """
    Calibrate prediction threshold on training data,
    apply to validation data.

    Parameters
    ----------
    train_predictions : pd.Series
        Model predictions on training data
    val_predictions : pd.Series
        Model predictions on validation data
    percentile : float
        Threshold percentile for signals
    model_type : str
        'long' or 'short'

    Returns
    -------
    tuple
        (threshold, train_signals, val_signals)
    """
    # Threshold from training predictions ONLY
    threshold = train_predictions.quantile(percentile / 100)

    if model_type == 'long':
        # Signal when prediction >= threshold
        train_signals = (train_predictions >= threshold).astype(int)
        val_signals = (val_predictions >= threshold).astype(int)
    else:
        # Signal when prediction <= threshold
        train_signals = (train_predictions <= threshold).astype(int)
        val_signals = (val_predictions <= threshold).astype(int)

    return threshold, train_signals, val_signals
```

## 5. Out-of-Sample Prediction Assembly

### Concatenate Validation Predictions

After training and predicting on each fold:

```python
def assemble_oos_predictions(fold_predictions):
    """
    Concatenate validation predictions across folds
    to form continuous out-of-sample series.

    Parameters
    ----------
    fold_predictions : dict
        {fold_id: {'val_predictions': pd.Series, ...}}

    Returns
    -------
    pd.Series
        Continuous OOS predictions sorted by time
    """
    oos_parts = []

    for fold_id in sorted(fold_predictions.keys()):
        val_preds = fold_predictions[fold_id]['val_predictions']
        oos_parts.append(val_preds)

    oos_predictions = pd.concat(oos_parts).sort_index()

    # Verify no overlap
    assert oos_predictions.index.is_unique, "Overlapping validation periods!"

    return oos_predictions
```

### Multiple Iteration Candidates

When exploring different boosting iteration counts:

```python
def generate_iteration_candidates(
    fold_boosters,
    features,
    iteration_counts=[50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
):
    """
    Generate OOS predictions for multiple iteration counts.

    Parameters
    ----------
    fold_boosters : dict
        {fold_id: trained_booster}
    features : pd.DataFrame
        Feature matrix for all data
    iteration_counts : list
        Iteration counts to evaluate

    Returns
    -------
    dict
        {iteration_count: oos_predictions}
    """
    candidates = {}

    for n_iter in iteration_counts:
        fold_preds = {}
        for fold_id, booster in fold_boosters.items():
            # Predict using only first n_iter trees
            preds = booster.predict(
                features,
                num_iteration=n_iter
            )
            fold_preds[fold_id] = preds

        candidates[n_iter] = assemble_oos_predictions(fold_preds)

    return candidates
```

## 6. Complete Pipeline Example

```python
def run_cv_pipeline(
    features: pd.DataFrame,
    returns: pd.Series,
    folds: list,
    model_type: str,
    label_percentile: float,
    signal_percentile: float,
):
    """
    Complete pre-backtest ML pipeline.

    Parameters
    ----------
    features : pd.DataFrame
        Feature matrix
    returns : pd.Series
        Forward returns
    folds : list
        Fold definitions
    model_type : str
        'long' or 'short'
    label_percentile : float
        Percentile for label definition (95 for long, 5 for short)
    signal_percentile : float
        Percentile for signal generation

    Returns
    -------
    dict
        OOS predictions, signals, and metadata
    """
    results = {
        'folds': folds,
        'model_type': model_type,
        'label_percentile': label_percentile,
        'signal_percentile': signal_percentile,
        'fold_results': {},
        'oos_predictions': None,
        'oos_signals': None,
    }

    # Step 1: Compute labels per fold (training percentiles only)
    fold_labels = compute_fold_labels(
        returns, folds, label_percentile, model_type
    )

    # Step 2: Train models per fold (see lightgbm-training skill)
    # ... model training code ...

    # Step 3: Generate predictions per fold
    # ... prediction code ...

    # Step 4: Calibrate thresholds (training predictions only)
    # ... threshold calibration ...

    # Step 5: Assemble OOS predictions
    results['oos_predictions'] = assemble_oos_predictions(fold_preds)

    # Step 6: Apply training-calibrated thresholds to OOS
    # ... signal generation ...

    return results
```

## 7. Common Mistakes

### Mistake 1: Global Percentiles
```python
# WRONG
global_threshold = all_returns.quantile(0.95)

# CORRECT
train_threshold = train_returns.quantile(0.95)
```

### Mistake 2: Validation Percentiles for Thresholds
```python
# WRONG
threshold = val_predictions.quantile(0.95)

# CORRECT
threshold = train_predictions.quantile(0.95)
# Then apply to val_predictions
```

### Mistake 3: Confusing Long/Short Labels
```python
# WRONG - inverted logic
long_label = returns <= returns.quantile(0.05)  # This is SHORT!

# CORRECT
long_label = returns >= returns.quantile(0.95)  # Upper tail
short_label = returns <= returns.quantile(0.05)  # Lower tail
```

### Mistake 4: Overlapping Validation Folds
```python
# WRONG - validation periods overlap
fold1_val = data['2024-01':'2024-02']
fold2_val = data['2024-02':'2024-03']  # Feb included twice!

# CORRECT - no overlap
fold1_val = data['2024-01-07':'2024-02-02']  # 4 weeks
fold2_val = data['2024-02-04':'2024-03-01']  # Next 4 weeks, no overlap
```

## 8. Checklist

Before proceeding to backtesting:

- [ ] Folds defined with explicit timestamps (not week numbers)
- [ ] Fold boundaries align to CME sessions
- [ ] No overlap between validation periods
- [ ] Label percentiles computed on training data only
- [ ] Long model targets upper tail, short model targets lower tail
- [ ] Prediction thresholds calibrated on training predictions only
- [ ] OOS predictions concatenated without overlap
- [ ] Fold definitions stored for reproducibility

## References

For detailed patterns, see:
- `{baseDir}/references/fold-generation.md`
- `{baseDir}/references/threshold-patterns.md`
