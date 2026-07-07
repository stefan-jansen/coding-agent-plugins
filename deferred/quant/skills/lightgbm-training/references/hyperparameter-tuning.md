# LightGBM Hyperparameter Tuning

## Systematic Tuning Approach

Tune parameters in stages to manage interactions efficiently.

## Stage 1: Tree Structure

Start with conservative structure, adjust complexity.

### Parameters to Tune
- `max_depth` or `num_leaves`
- `min_child_weight` or `min_data_in_leaf`

### Grid

```python
depth_grid = [
    # Conservative
    {'max_depth': 4, 'num_leaves': 15, 'min_child_weight': 20},
    # Moderate
    {'max_depth': 5, 'num_leaves': 31, 'min_child_weight': 15},
    {'max_depth': 6, 'num_leaves': 63, 'min_child_weight': 10},
    # Aggressive
    {'max_depth': 7, 'num_leaves': 127, 'min_child_weight': 5},
]
```

### Evaluation

Train each configuration, compare validation IC or AUC.

```python
from lightgbm import cv

results = []

for config in depth_grid:
    params = base_params.copy()
    params.update(config)

    cv_result = cv(
        params,
        train_data,
        num_boost_round=500,
        folds=ts_splitter,
    )

    # Extract final metric
    final_metric = cv_result['valid-auc-mean'][-1]

    results.append({
        'config': config,
        'metric': final_metric,
    })

best_config = max(results, key=lambda x: x['metric'])['config']
```

## Stage 2: Regularization

Fix tree structure from Stage 1, tune regularization.

### Parameters to Tune
- `lambda_l1`, `lambda_l2`
- `min_gain_to_split`

### Grid

```python
reg_grid = [
    # Light
    {'lambda_l1': 0.0, 'lambda_l2': 0.5, 'min_gain_to_split': 0.0},
    # Moderate
    {'lambda_l1': 0.5, 'lambda_l2': 1.0, 'min_gain_to_split': 0.01},
    {'lambda_l1': 1.0, 'lambda_l2': 2.0, 'min_gain_to_split': 0.01},
    # Heavy
    {'lambda_l1': 2.0, 'lambda_l2': 5.0, 'min_gain_to_split': 0.05},
]
```

## Stage 3: Subsampling

Fix structure and regularization, tune sampling.

### Parameters to Tune
- `feature_fraction`
- `bagging_fraction`, `bagging_freq`

### Grid

```python
sampling_grid = [
    # Conservative
    {'feature_fraction': 0.6, 'bagging_fraction': 0.7, 'bagging_freq': 1},
    # Moderate
    {'feature_fraction': 0.7, 'bagging_fraction': 0.8, 'bagging_freq': 1},
    {'feature_fraction': 0.8, 'bagging_fraction': 0.8, 'bagging_freq': 1},
    # Aggressive
    {'feature_fraction': 0.9, 'bagging_fraction': 0.9, 'bagging_freq': 1},
]
```

## Stage 4: Learning Rate

Fix all other parameters, adjust learning rate and iterations.

```python
lr_grid = [0.001, 0.005, 0.01, 0.05]

for lr in lr_grid:
    params['learning_rate'] = lr
    # Train with more iterations for lower LR
    num_rounds = 1000 if lr <= 0.01 else 500
    # ... train and evaluate
```

## Complete Tuning Function

```python
import pandas as pd
from itertools import product

def tune_lightgbm(
    features,
    labels,
    folds,
    base_params: dict,
    param_grid: dict,
    metric_name: str = 'auc',
):
    """
    Grid search with time-series CV.

    Parameters
    ----------
    features : pd.DataFrame
    labels : pd.Series
    folds : list
    base_params : dict
        Fixed parameters
    param_grid : dict
        {param_name: [values]}
    metric_name : str
        Metric to optimize

    Returns
    -------
    pd.DataFrame
        Results sorted by metric
    """
    import lightgbm as lgb

    train_data = lgb.Dataset(
        features.values,
        label=labels.values,
        feature_name=list(features.columns),
        free_raw_data=False,
    )

    def fold_generator():
        for fold in folds:
            train_mask = (
                (features.index >= fold['train_start']) &
                (features.index < fold['train_end'])
            )
            test_mask = (
                (features.index >= fold['val_start']) &
                (features.index < fold['val_end'])
            )

            train_idx = features.index.get_indexer(
                features.index[train_mask]
            )
            test_idx = features.index.get_indexer(
                features.index[test_mask]
            )

            yield train_idx, test_idx

    # Generate all parameter combinations
    param_names = list(param_grid.keys())
    param_values = list(param_grid.values())

    results = []

    for values in product(*param_values):
        config = dict(zip(param_names, values))

        # Merge with base params
        params = base_params.copy()
        params.update(config)

        # Run CV
        cv_result = lgb.cv(
            params,
            train_data,
            num_boost_round=500,
            folds=fold_generator(),
        )

        # Extract final validation metric
        metric_key = f'valid-{metric_name}-mean'
        final_metric = cv_result[metric_key][-1]

        results.append({
            **config,
            f'val_{metric_name}': final_metric,
        })

    # Convert to DataFrame and sort
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(
        f'val_{metric_name}',
        ascending=(metric_name in ['rmse', 'mae'])  # Lower is better
    )

    return results_df
```

## Example Usage

```python
# Stage 1: Tree structure
base_params = {
    'objective': 'binary',
    'metric': 'auc',
    'boosting_type': 'gbdt',
    'learning_rate': 0.01,
    'lambda_l2': 1.0,
    'feature_fraction': 0.8,
    'bagging_fraction': 0.8,
    'bagging_freq': 1,
    'verbosity': -1,
    'seed': 42,
}

structure_grid = {
    'max_depth': [4, 5, 6],
    'num_leaves': [15, 31, 63],
    'min_child_weight': [5, 10, 15, 20],
}

structure_results = tune_lightgbm(
    features, labels, folds,
    base_params, structure_grid, 'auc'
)

print(structure_results.head())

# Use best structure for next stage
best_structure = structure_results.iloc[0]
base_params.update({
    'max_depth': int(best_structure['max_depth']),
    'num_leaves': int(best_structure['num_leaves']),
    'min_child_weight': best_structure['min_child_weight'],
})

# Stage 2: Regularization
reg_grid = {
    'lambda_l1': [0.0, 0.5, 1.0, 2.0],
    'lambda_l2': [0.5, 1.0, 2.0, 5.0],
    'min_gain_to_split': [0.0, 0.01, 0.05],
}

reg_results = tune_lightgbm(
    features, labels, folds,
    base_params, reg_grid, 'auc'
)

# ... and so on
```

## Bayesian Optimization Alternative

For larger search spaces, use Bayesian optimization:

```python
from skopt import BayesSearchCV
from skopt.space import Real, Integer

# Define search space
search_spaces = {
    'max_depth': Integer(4, 8),
    'num_leaves': Integer(15, 127),
    'min_child_weight': Real(5, 25),
    'lambda_l1': Real(0.0, 2.0),
    'lambda_l2': Real(0.5, 5.0),
    'feature_fraction': Real(0.6, 0.9),
    'bagging_fraction': Real(0.7, 0.9),
}

# Note: Need to wrap LightGBM for sklearn compatibility
# or use lightgbm.LGBMClassifier/LGBMRegressor
```

## Quick Presets by Data Size

### Small Dataset (<100K samples)
```python
params = {
    'max_depth': 4,
    'num_leaves': 15,
    'min_child_weight': 20,
    'lambda_l2': 2.0,
    'learning_rate': 0.01,
}
```

### Medium Dataset (100K-1M samples)
```python
params = {
    'max_depth': 5,
    'num_leaves': 31,
    'min_child_weight': 10,
    'lambda_l2': 1.0,
    'learning_rate': 0.01,
}
```

### Large Dataset (>1M samples)
```python
params = {
    'max_depth': 6,
    'num_leaves': 63,
    'min_child_weight': 5,
    'lambda_l2': 0.5,
    'learning_rate': 0.01,
}
```

## Feature Engineering Impact

**More important than hyperparameter tuning** for financial ML:

1. **Feature quality** - Better features > Better tuning
2. **Feature count** - 50-200 good features better than 500 weak ones
3. **Feature correlation** - Reduce multicollinearity before tuning

Only tune after feature engineering is solid.
