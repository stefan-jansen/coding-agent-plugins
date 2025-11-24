# CME Break Schedules

## Overview

Different CME products have different maintenance break schedules. This document provides schedules for common products and a framework for defining custom schedules.

## ES/NQ/RTY (Equity Index Futures)

**Daily Maintenance Break**: 4:00 PM - 5:00 PM CT (Mon-Thu)
**Friday Close**: 4:00 PM CT
**Weekend Break**: Friday 4:00 PM CT - Sunday 5:00 PM CT

```python
ES_BREAKS = {
    'daily_maintenance': {
        'start': (16, 0),   # 4:00 PM CT
        'end': (17, 0),     # 5:00 PM CT
        'days': [0, 1, 2, 3],  # Mon-Thu
    },
    'weekend': {
        'start': (4, 16, 0),   # Friday 4:00 PM CT (weekday=4)
        'end': (6, 17, 0),     # Sunday 5:00 PM CT (weekday=6)
    }
}
```

## CL/NG (Energy Futures)

**Daily Maintenance Break**: 4:00 PM - 5:00 PM CT (Mon-Thu)
**Friday Close**: 4:00 PM CT
**Weekend Break**: Friday 4:00 PM CT - Sunday 5:00 PM CT

```python
CL_BREAKS = ES_BREAKS  # Same schedule as equity futures
```

## GC/SI (Metals Futures)

**Daily Maintenance Break**: 4:00 PM - 5:00 PM CT (Mon-Thu)
**Friday Close**: 4:00 PM CT
**Weekend Break**: Friday 4:00 PM CT - Sunday 5:00 PM CT

```python
GC_BREAKS = ES_BREAKS  # Same schedule as equity futures
```

## ZB/ZN/ZF (Treasury Futures)

**Daily Maintenance Break**: 4:00 PM - 5:00 PM CT (Mon-Thu)
**Friday Close**: 4:00 PM CT
**Weekend Break**: Friday 4:00 PM CT - Sunday 5:00 PM CT

```python
ZB_BREAKS = ES_BREAKS  # Same schedule
```

## Break Detection Functions

```python
import pandas as pd
from datetime import time
import pytz

def is_in_daily_break(ts: pd.Timestamp, break_start: tuple, break_end: tuple) -> bool:
    """
    Check if timestamp is in daily maintenance break.

    Parameters
    ----------
    ts : pd.Timestamp
        Timezone-aware timestamp
    break_start : tuple
        (hour, minute) of break start
    break_end : tuple
        (hour, minute) of break end

    Returns
    -------
    bool
    """
    ct = pytz.timezone('America/Chicago')
    ts_ct = ts.tz_convert(ct)

    break_start_time = time(*break_start)
    break_end_time = time(*break_end)

    return break_start_time <= ts_ct.time() < break_end_time


def is_in_weekend_break(ts: pd.Timestamp) -> bool:
    """
    Check if timestamp is in weekend break.

    Weekend break: Friday 4:00 PM CT to Sunday 5:00 PM CT

    Parameters
    ----------
    ts : pd.Timestamp
        Timezone-aware timestamp

    Returns
    -------
    bool
    """
    ct = pytz.timezone('America/Chicago')
    ts_ct = ts.tz_convert(ct)

    weekday = ts_ct.weekday()
    hour = ts_ct.hour

    # Friday after 4 PM
    if weekday == 4 and hour >= 16:
        return True

    # All Saturday
    if weekday == 5:
        return True

    # Sunday before 5 PM
    if weekday == 6 and hour < 17:
        return True

    return False


def is_in_any_break(ts: pd.Timestamp, schedule: dict) -> bool:
    """
    Check if timestamp is in any break period.

    Parameters
    ----------
    ts : pd.Timestamp
        Timezone-aware timestamp
    schedule : dict
        Break schedule (e.g., ES_BREAKS)

    Returns
    -------
    bool
    """
    # Check weekend
    if is_in_weekend_break(ts):
        return True

    # Check daily maintenance
    ct = pytz.timezone('America/Chicago')
    ts_ct = ts.tz_convert(ct)
    weekday = ts_ct.weekday()

    daily = schedule.get('daily_maintenance', {})
    if weekday in daily.get('days', []):
        if is_in_daily_break(ts, daily['start'], daily['end']):
            return True

    return False
```

## Forward Return Validity

```python
def is_valid_forward_return(
    start_ts: pd.Timestamp,
    horizon_minutes: int,
    schedule: dict
) -> bool:
    """
    Check if forward return starting at start_ts is valid.

    A return is invalid if its end time falls inside a break.

    Parameters
    ----------
    start_ts : pd.Timestamp
        Start timestamp of the return period
    horizon_minutes : int
        Return horizon in minutes
    schedule : dict
        Break schedule

    Returns
    -------
    bool
        True if return is valid (end time not in break)
    """
    end_ts = start_ts + pd.Timedelta(minutes=horizon_minutes)
    return not is_in_any_break(end_ts, schedule)


def filter_valid_returns(
    returns: pd.Series,
    horizon_minutes: int,
    schedule: dict
) -> pd.Series:
    """
    Filter returns to keep only those with valid end times.

    Parameters
    ----------
    returns : pd.Series
        Forward returns indexed by start timestamp
    horizon_minutes : int
        Return horizon used to compute these returns
    schedule : dict
        Break schedule

    Returns
    -------
    pd.Series
        Filtered returns
    """
    valid_mask = returns.index.map(
        lambda ts: is_valid_forward_return(ts, horizon_minutes, schedule)
    )
    return returns[valid_mask]
```

## Holiday Schedules

CME observes certain holidays with early closes or full closures. Common holidays:

- New Year's Day
- Martin Luther King Jr. Day
- Presidents Day
- Good Friday
- Memorial Day
- Independence Day
- Labor Day
- Thanksgiving Day
- Christmas Day

**Note**: Holiday schedules vary by year. Check CME Group's holiday calendar for the specific year.

```python
# Example: define holidays for a specific year
HOLIDAYS_2024 = [
    '2024-01-01',  # New Year's Day
    '2024-01-15',  # MLK Day
    '2024-02-19',  # Presidents Day
    '2024-03-29',  # Good Friday
    '2024-05-27',  # Memorial Day
    '2024-07-04',  # Independence Day
    '2024-09-02',  # Labor Day
    '2024-11-28',  # Thanksgiving
    '2024-12-25',  # Christmas
]

def is_holiday(session_date, holidays: list) -> bool:
    """Check if session date is a holiday."""
    return str(session_date) in holidays
```
