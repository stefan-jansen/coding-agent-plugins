# Threshold Calibration Patterns

## Core Principle

**All thresholds must be computed from training data only.**

This applies to:
1. Label thresholds (return percentiles)
2. Prediction thresholds (signal generation)
3. Any other cutoffs used in the pipeline

## Pattern 1: Per-Fold Label Thresholds

```python
class FoldLabelGenerator:
    """Generate labels with per-fold training thresholds."""

    def __init__(self, model_type: str, percentile: float):
        """
        Parameters
        ----------
        model_type : str
            'long' (upper tail) or 'short' (lower tail)
        percentile : float
            Threshold percentile (e.g., 95 for long, 5 for short)
        """
        self.model_type = model_type
        self.percentile = percentile
        self.fold_thresholds = {}

    def fit_fold(self, fold_id: int, train_returns: pd.Series):
        """Compute threshold from training returns."""
        threshold = train_returns.quantile(self.percentile / 100)
        self.fold_thresholds[fold_id] = threshold
        return threshold

    def transform(self, returns: pd.Series, fold_id: int) -> pd.Series:
        """Apply stored threshold to generate labels."""
        threshold = self.fold_thresholds[fold_id]

        if self.model_type == 'long':
            labels = (returns >= threshold).astype(int)
        else:  # short
            labels = (returns <= threshold).astype(int)

        return labels

    def fit_transform_fold(
        self,
        fold_id: int,
        train_returns: pd.Series,
        val_returns: pd.Series
    ):
        """Fit on training, transform both train and val."""
        self.fit_fold(fold_id, train_returns)

        train_labels = self.transform(train_returns, fold_id)
        val_labels = self.transform(val_returns, fold_id)

        return train_labels, val_labels
```

## Pattern 2: Prediction Signal Calibration

```python
class SignalCalibrator:
    """Calibrate prediction thresholds on training predictions."""

    def __init__(self, model_type: str, percentile: float):
        self.model_type = model_type
        self.percentile = percentile
        self.fold_thresholds = {}

    def fit_fold(self, fold_id: int, train_predictions: pd.Series):
        """Compute signal threshold from training predictions."""
        threshold = train_predictions.quantile(self.percentile / 100)
        self.fold_thresholds[fold_id] = threshold
        return threshold

    def transform(self, predictions: pd.Series, fold_id: int) -> pd.Series:
        """Apply stored threshold to generate signals."""
        threshold = self.fold_thresholds[fold_id]

        if self.model_type == 'long':
            signals = (predictions >= threshold).astype(int)
        else:
            signals = (predictions <= threshold).astype(int)

        return signals

    def fit_transform_fold(
        self,
        fold_id: int,
        train_preds: pd.Series,
        val_preds: pd.Series
    ):
        """Fit on training predictions, transform both."""
        self.fit_fold(fold_id, train_preds)

        train_signals = self.transform(train_preds, fold_id)
        val_signals = self.transform(val_preds, fold_id)

        return train_signals, val_signals
```

## Pattern 3: Rolling Window Thresholds

Sometimes you want thresholds from a recent window rather than all training data:

```python
def compute_rolling_threshold(
    train_predictions: pd.Series,
    window_weeks: int = 12,
    percentile: float = 95.0,
) -> float:
    """
    Compute threshold from recent training window only.

    Useful when market regime changes and older data
    is less relevant.
    """
    # Use last N weeks of training data
    cutoff = train_predictions.index.max() - pd.Timedelta(weeks=window_weeks)
    recent_preds = train_predictions[train_predictions.index >= cutoff]

    return recent_preds.quantile(percentile / 100)
```

## Pattern 4: Multiple Thresholds for Entry/Exit

```python
class DualThresholdCalibrator:
    """Separate thresholds for entry and exit signals."""

    def __init__(
        self,
        model_type: str,
        entry_percentile: float,
        exit_percentile: float
    ):
        """
        Parameters
        ----------
        entry_percentile : float
            Percentile for entry signals (more aggressive)
        exit_percentile : float
            Percentile for exit signals (more conservative)
        """
        self.model_type = model_type
        self.entry_percentile = entry_percentile
        self.exit_percentile = exit_percentile
        self.fold_thresholds = {}

    def fit_fold(self, fold_id: int, train_preds: pd.Series):
        """Compute both thresholds from training."""
        self.fold_thresholds[fold_id] = {
            'entry': train_preds.quantile(self.entry_percentile / 100),
            'exit': train_preds.quantile(self.exit_percentile / 100),
        }

    def generate_signals(
        self,
        predictions: pd.Series,
        fold_id: int
    ) -> pd.DataFrame:
        """Generate entry and exit signals."""
        thresholds = self.fold_thresholds[fold_id]

        if self.model_type == 'long':
            entry = (predictions >= thresholds['entry']).astype(int)
            exit_ = (predictions < thresholds['exit']).astype(int)
        else:
            entry = (predictions <= thresholds['entry']).astype(int)
            exit_ = (predictions > thresholds['exit']).astype(int)

        return pd.DataFrame({
            'entry_signal': entry,
            'exit_signal': exit_,
        }, index=predictions.index)
```

## Anti-Pattern: Global Thresholds

```python
# WRONG - computed on all data
def bad_labeling(returns):
    global_threshold = returns.quantile(0.95)  # Includes future data!
    return (returns >= global_threshold).astype(int)

# WRONG - computed on validation data
def bad_signal_calibration(train_preds, val_preds):
    # Using validation to set threshold = look-ahead
    threshold = val_preds.quantile(0.95)
    return (val_preds >= threshold).astype(int)
```

## Threshold Storage for Reproducibility

```python
def save_thresholds(calibrator, filepath: str):
    """Save calibrated thresholds for reproducibility."""
    data = {
        'model_type': calibrator.model_type,
        'percentile': calibrator.percentile,
        'fold_thresholds': calibrator.fold_thresholds,
    }

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def load_thresholds(filepath: str) -> dict:
    """Load saved thresholds."""
    with open(filepath, 'r') as f:
        return json.load(f)
```

## Complete Workflow Example

```python
def generate_signals_pipeline(
    features: pd.DataFrame,
    returns: pd.Series,
    folds: list,
    model_type: str = 'long',
    label_percentile: float = 95.0,
    signal_percentile: float = 95.0,
):
    """
    Complete signal generation with proper threshold handling.
    """
    # Initialize calibrators
    label_gen = FoldLabelGenerator(model_type, label_percentile)
    signal_cal = SignalCalibrator(model_type, signal_percentile)

    all_val_signals = []

    for fold in folds:
        fold_id = fold['fold_id']

        # Split data
        train_mask = (features.index >= fold['train_start']) & \
                     (features.index < fold['train_end'])
        val_mask = (features.index >= fold['val_start']) & \
                   (features.index < fold['val_end'])

        X_train = features[train_mask]
        X_val = features[val_mask]
        train_returns = returns[train_mask]
        val_returns = returns[val_mask]

        # Generate labels (training threshold only)
        train_labels, val_labels = label_gen.fit_transform_fold(
            fold_id, train_returns, val_returns
        )

        # Train model
        model = train_model(X_train, train_labels)  # Your training function

        # Generate predictions
        train_preds = pd.Series(model.predict(X_train), index=X_train.index)
        val_preds = pd.Series(model.predict(X_val), index=X_val.index)

        # Calibrate signals (training predictions only)
        train_signals, val_signals = signal_cal.fit_transform_fold(
            fold_id, train_preds, val_preds
        )

        all_val_signals.append(val_signals)

    # Concatenate OOS signals
    oos_signals = pd.concat(all_val_signals).sort_index()

    return oos_signals, label_gen, signal_cal
```
