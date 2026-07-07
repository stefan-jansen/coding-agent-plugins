# Time-Series Fold Generation

## Complete Fold Generator

```python
import pandas as pd
import pytz
from typing import List, Dict

def generate_ts_folds(
    data_start: pd.Timestamp,
    data_end: pd.Timestamp,
    train_weeks: int = 52,
    val_weeks: int = 4,
    step_weeks: int = 4,
) -> List[Dict]:
    """
    Generate time-series CV folds aligned to CME sessions.

    Parameters
    ----------
    data_start : pd.Timestamp
        Start of available data (must be timezone-aware)
    data_end : pd.Timestamp
        End of available data
    train_weeks : int
        Training window size in weeks (default 52)
    val_weeks : int
        Validation window size in weeks (default 4)
    step_weeks : int
        Step size between folds in weeks (default 4)

    Returns
    -------
    list
        List of fold dictionaries with timestamps
    """
    ct = pytz.timezone('America/Chicago')

    # Ensure timestamps are in CT
    if data_start.tz is None:
        raise ValueError("data_start must be timezone-aware")
    data_start = data_start.tz_convert(ct)
    data_end = data_end.tz_convert(ct)

    # Find first Sunday 5 PM after data_start
    def next_sunday_5pm(ts):
        """Find next Sunday 5 PM CT."""
        days_until_sunday = (6 - ts.weekday()) % 7
        if days_until_sunday == 0 and ts.hour >= 17:
            days_until_sunday = 7
        sunday = ts + pd.Timedelta(days=days_until_sunday)
        return sunday.replace(hour=17, minute=0, second=0, microsecond=0)

    # Find Friday 4 PM before a given timestamp
    def prev_friday_4pm(ts):
        """Find previous Friday 4 PM CT."""
        days_since_friday = (ts.weekday() - 4) % 7
        if days_since_friday == 0 and ts.hour < 16:
            days_since_friday = 7
        friday = ts - pd.Timedelta(days=days_since_friday)
        return friday.replace(hour=16, minute=0, second=0, microsecond=0)

    folds = []
    fold_id = 1

    # Start first validation at earliest possible point
    # Need train_weeks of data before first validation
    first_val_start = next_sunday_5pm(
        data_start + pd.Timedelta(weeks=train_weeks)
    )

    val_start = first_val_start

    while True:
        # Calculate all boundaries
        val_end = prev_friday_4pm(
            val_start + pd.Timedelta(weeks=val_weeks)
        )

        # Check if validation period exceeds data
        if val_end > data_end:
            break

        train_start = next_sunday_5pm(
            val_start - pd.Timedelta(weeks=train_weeks)
        )
        train_end = prev_friday_4pm(val_start)

        # Verify train_start has data
        if train_start < data_start:
            # Skip this fold, not enough training data
            val_start = next_sunday_5pm(
                val_start + pd.Timedelta(weeks=step_weeks)
            )
            continue

        fold = {
            'fold_id': fold_id,
            'train_start': train_start,
            'train_end': train_end,
            'val_start': val_start,
            'val_end': val_end,
            'train_weeks': train_weeks,
            'val_weeks': val_weeks,
        }

        folds.append(fold)
        fold_id += 1

        # Move to next fold
        val_start = next_sunday_5pm(
            val_start + pd.Timedelta(weeks=step_weeks)
        )

    return folds
```

## Usage Example

```python
import pandas as pd
import pytz

ct = pytz.timezone('America/Chicago')

# Define data range
data_start = pd.Timestamp('2022-01-02 17:00:00', tz=ct)
data_end = pd.Timestamp('2024-06-28 16:00:00', tz=ct)

# Generate folds
folds = generate_ts_folds(
    data_start=data_start,
    data_end=data_end,
    train_weeks=52,
    val_weeks=4,
    step_weeks=4,
)

# Print fold summary
for fold in folds:
    print(f"Fold {fold['fold_id']}:")
    print(f"  Train: {fold['train_start']} to {fold['train_end']}")
    print(f"  Val:   {fold['val_start']} to {fold['val_end']}")
    print()
```

## Saving and Loading Folds

```python
import json

def save_folds(folds: List[Dict], filepath: str):
    """Save folds to JSON with ISO timestamps."""
    serializable = []
    for fold in folds:
        f = fold.copy()
        for key in ['train_start', 'train_end', 'val_start', 'val_end']:
            f[key] = f[key].isoformat()
        serializable.append(f)

    with open(filepath, 'w') as f:
        json.dump(serializable, f, indent=2)


def load_folds(filepath: str) -> List[Dict]:
    """Load folds from JSON."""
    with open(filepath, 'r') as f:
        data = json.load(f)

    folds = []
    for fold in data:
        f = fold.copy()
        for key in ['train_start', 'train_end', 'val_start', 'val_end']:
            f[key] = pd.Timestamp(f[key])
        folds.append(f)

    return folds
```

## Sklearn-Compatible Splitter

```python
from sklearn.model_selection import BaseCrossValidator
import numpy as np

class CMETimeSeriesSplit(BaseCrossValidator):
    """
    Time-series CV splitter aligned to CME sessions.

    Compatible with sklearn's cross_val_score and similar functions.
    """

    def __init__(self, folds: List[Dict]):
        """
        Parameters
        ----------
        folds : list
            Fold definitions from generate_ts_folds()
        """
        self.folds = folds

    def get_n_splits(self, X=None, y=None, groups=None):
        return len(self.folds)

    def split(self, X, y=None, groups=None):
        """
        Generate train/test indices for each fold.

        Parameters
        ----------
        X : pd.DataFrame
            Feature matrix with DatetimeIndex

        Yields
        ------
        tuple
            (train_indices, test_indices) as numpy arrays
        """
        for fold in self.folds:
            train_mask = (
                (X.index >= fold['train_start']) &
                (X.index < fold['train_end'])
            )
            test_mask = (
                (X.index >= fold['val_start']) &
                (X.index < fold['val_end'])
            )

            train_idx = np.where(train_mask)[0]
            test_idx = np.where(test_mask)[0]

            yield train_idx, test_idx
```

## Expanding Window Variant

```python
def generate_expanding_folds(
    data_start: pd.Timestamp,
    data_end: pd.Timestamp,
    min_train_weeks: int = 52,
    val_weeks: int = 4,
    step_weeks: int = 4,
) -> List[Dict]:
    """
    Generate expanding window folds (training grows over time).

    Unlike fixed-window folds, each fold uses all available
    historical data for training.
    """
    ct = pytz.timezone('America/Chicago')
    data_start = data_start.tz_convert(ct)
    data_end = data_end.tz_convert(ct)

    # ... similar logic but train_start is always data_start
    # and train_end grows with each fold
    pass
```

## Validation

```python
def validate_folds(folds: List[Dict], data_index: pd.DatetimeIndex):
    """
    Validate fold definitions against actual data.

    Checks:
    - All boundaries are within data range
    - No validation overlap
    - Sufficient training data per fold
    """
    errors = []

    for i, fold in enumerate(folds):
        # Check boundaries within data
        if fold['train_start'] < data_index.min():
            errors.append(f"Fold {fold['fold_id']}: train_start before data")
        if fold['val_end'] > data_index.max():
            errors.append(f"Fold {fold['fold_id']}: val_end after data")

        # Check train before val
        if fold['train_end'] >= fold['val_start']:
            errors.append(f"Fold {fold['fold_id']}: train overlaps validation")

    # Check no validation overlap
    for i in range(len(folds) - 1):
        if folds[i]['val_end'] > folds[i+1]['val_start']:
            errors.append(
                f"Folds {folds[i]['fold_id']} and {folds[i+1]['fold_id']}: "
                "validation periods overlap"
            )

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        raise ValueError(f"Found {len(errors)} fold validation errors")

    print(f"Validated {len(folds)} folds successfully")
```
