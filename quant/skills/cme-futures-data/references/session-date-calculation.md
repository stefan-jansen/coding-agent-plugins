# CME Session Date Calculation

## Core Function

```python
import pandas as pd
import pytz

def compute_session_date(timestamps: pd.DatetimeIndex) -> pd.Series:
    """
    Convert timestamps to CME session dates.

    CME session starts Sunday 5:00 PM CT.
    All times before Sunday 5 PM belong to Friday's session (weekend).
    All times Sunday 5 PM onwards belong to Monday's session.

    Parameters
    ----------
    timestamps : pd.DatetimeIndex
        Timestamps in any timezone (will be converted to CT)

    Returns
    -------
    pd.Series
        Session dates as datetime.date objects
    """
    ct = pytz.timezone('America/Chicago')

    # Convert to CT
    if timestamps.tz is None:
        raise ValueError("Timestamps must be timezone-aware")

    ct_times = timestamps.tz_convert(ct)

    session_dates = []
    for ts in ct_times:
        weekday = ts.weekday()  # Monday=0, Sunday=6
        hour = ts.hour

        if weekday == 6:  # Sunday
            if hour >= 17:  # 5 PM or later
                # Belongs to Monday session
                session_date = (ts + pd.Timedelta(days=1)).date()
            else:
                # Before Sunday 5 PM - weekend, belongs to Friday
                session_date = (ts - pd.Timedelta(days=2)).date()
        elif weekday == 5:  # Saturday
            # Weekend - belongs to Friday
            session_date = (ts - pd.Timedelta(days=1)).date()
        else:  # Monday-Friday
            if hour < 17:
                # Before 5 PM - same day session
                session_date = ts.date()
            else:
                # 5 PM or later - next day session (or Monday if Friday)
                if weekday == 4:  # Friday after 5 PM
                    # Actually closed, but if data exists, next session is Monday
                    session_date = (ts + pd.Timedelta(days=3)).date()
                else:
                    session_date = (ts + pd.Timedelta(days=1)).date()

        session_dates.append(session_date)

    return pd.Series(session_dates, index=timestamps)
```

## Usage Example

```python
import pandas as pd
import pytz

# Sample minute data
ct = pytz.timezone('America/Chicago')
timestamps = pd.DatetimeIndex([
    '2024-01-07 17:00:00',  # Sunday 5 PM -> Monday session
    '2024-01-07 23:00:00',  # Sunday 11 PM -> Monday session
    '2024-01-08 09:00:00',  # Monday 9 AM -> Monday session
    '2024-01-08 16:30:00',  # Monday 4:30 PM -> Monday session (in break)
    '2024-01-08 17:30:00',  # Monday 5:30 PM -> Tuesday session
]).tz_localize(ct)

session_dates = compute_session_date(timestamps)
print(session_dates)
# 2024-01-07 17:00:00-06:00    2024-01-08  (Monday)
# 2024-01-07 23:00:00-06:00    2024-01-08  (Monday)
# 2024-01-08 09:00:00-06:00    2024-01-08  (Monday)
# 2024-01-08 16:30:00-06:00    2024-01-08  (Monday)
# 2024-01-08 17:30:00-06:00    2024-01-09  (Tuesday)
```

## Adding Session Date Column

```python
def add_session_date(df: pd.DataFrame) -> pd.DataFrame:
    """Add session_date column to dataframe with datetime index."""
    df = df.copy()
    df['session_date'] = compute_session_date(df.index)
    return df
```

## Aggregating by Session

```python
def daily_ohlcv_by_session(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate minute data to daily OHLCV by session date.

    Parameters
    ----------
    df : pd.DataFrame
        Minute data with columns: open, high, low, close, volume
        Index must be timezone-aware DatetimeIndex

    Returns
    -------
    pd.DataFrame
        Daily OHLCV indexed by session date
    """
    df = add_session_date(df)

    daily = df.groupby('session_date').agg({
        'open': 'first',
        'high': 'max',
        'low': 'min',
        'close': 'last',
        'volume': 'sum'
    })

    return daily
```
