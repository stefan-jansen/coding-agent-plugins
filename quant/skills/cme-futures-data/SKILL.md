---
name: cme-futures-data
description: Use when working with CME futures minute data - session dates vs calendar dates, Sunday 5pm CT boundaries, forward returns with break handling, and invalid timestamp filtering. Essential for any CME data preparation.
allowed-tools: Read,Write,Edit,Bash(python:*),Grep
version: 1.0.0
---

# CME Futures Data Handling

This skill covers two critical aspects of CME futures data that cause subtle but serious bugs:
1. Session date handling (vs calendar dates)
2. Forward return calculation with break filtering

## 1. CME Session Structure

### The Sunday 5pm Rule

CME futures trade 23 hours/day, 5 days/week. The weekly session starts **Sunday 5:00 PM CT**.

**Critical implication**: Sunday evening minutes belong to the **Monday session date**, not Sunday.

```
Calendar time          | Session date
-----------------------|-------------
Sunday 5:00 PM CT      | Monday
Sunday 11:59 PM CT     | Monday
Monday 12:00 AM CT     | Monday
Monday 4:00 PM CT      | Monday (until maintenance break)
```

### Why This Matters

If you group data by calendar date:
- Sunday evening becomes its own "day" with ~7 hours of data
- Monday appears to start at midnight with missing overnight data
- Daily returns are distorted
- Sharpe ratios and other metrics are biased

**Always use session dates, never calendar dates.**

### Daily Maintenance Breaks

CME has daily maintenance breaks (typically 4:00-5:00 PM CT for equity futures). During breaks:
- No trading occurs
- Prices don't change
- Data may be forward-filled but is not tradable

### Weekend Break

Friday 4:00 PM CT to Sunday 5:00 PM CT - no trading.

## 2. Fold Boundaries Must Align to Sessions

When defining cross-validation folds:

**WRONG**: Use calendar week (Monday-Sunday by calendar date)
- Cuts Sunday evening session in half
- Training data bleeds into validation

**CORRECT**: Use CME trading week
- Week starts Sunday 5:00 PM CT
- Week ends Friday 4:00 PM CT (before weekend break)
- Fold boundaries align to session boundaries

### Handling Holidays

- Some weeks have fewer than 5 trading days (holidays)
- **Do NOT shift fold boundaries to compensate**
- Accept shorter weeks; maintain session alignment
- A 4-day trading week is still one complete week

### Store Fold Definitions

Always store folds as explicit timestamps:
```python
folds = [
    {
        'train_start': '2023-01-08 17:00:00-06:00',  # Sunday 5pm CT
        'train_end': '2024-01-05 16:00:00-06:00',    # Friday 4pm CT
        'val_start': '2024-01-07 17:00:00-06:00',    # Sunday 5pm CT
        'val_end': '2024-02-02 16:00:00-06:00',      # Friday 4pm CT
    },
    # ... more folds
]
```

This ensures exact reproducibility.

## 3. Forward Return Calculation

### The Problem

Forward returns over horizon H minutes:
```
r(t) = (P(t+H) - P(t)) / P(t)
```

But `t+H` may fall inside a break where:
- Price is forward-filled (unchanged)
- No actual trading can occur
- The return is numerically valid but **conceptually invalid**

### Step A: Create Continuous Price Series

Forward-fill prices through all breaks:
```python
# Ensure continuous series
prices = prices.ffill()
```

This makes `P(t+H)` defined for all timestamps.

### Step B: Compute Raw Forward Returns

```python
# Compute returns and align to start time
forward_returns = prices.pct_change(periods=H).shift(-H)
```

The shift aligns each return to its **start timestamp**.

### Step C: Mark Invalid Timestamps

A return starting at `t` is **invalid** if `t+H` falls inside a break AND does not exit within H minutes.

**Examples with H=15 minutes:**

| Start time (t) | End time (t+H) | Valid? | Reason |
|----------------|----------------|--------|--------|
| 3:45 PM | 4:00 PM | Yes | Ends before break |
| 4:00 PM | 4:15 PM | No | Ends inside break |
| 4:45 PM | 5:00 PM | No | Ends inside break |
| 4:50 PM | 5:05 PM | Yes | Ends after break reopens |

**Weekend example with H=120 minutes:**

| Start time | End time | Valid? |
|------------|----------|--------|
| Fri 3:00 PM | Fri 5:00 PM | No | Ends in weekend |
| Sun 4:30 PM | Sun 6:30 PM | No | Ends before reopen |
| Sun 4:30 PM (H=180) | Sun 8:30 PM | Yes | Ends after Sunday 5pm reopen |

### Implementation Pattern

```python
def is_valid_return_timestamp(t, horizon_minutes, break_schedule):
    """
    Return True if forward return starting at t is valid.

    Valid means: end_time is in a tradable period OR
    horizon spans a break and exits into tradable period.
    """
    end_time = t + pd.Timedelta(minutes=horizon_minutes)

    for break_start, break_end in break_schedule:
        if break_start <= end_time < break_end:
            # End falls in break - invalid
            return False

    return True

# Filter returns
valid_mask = returns.index.map(
    lambda t: is_valid_return_timestamp(t, H, breaks)
)
clean_returns = returns[valid_mask]
```

### Break Schedule Definition

Define breaks explicitly:
```python
# Daily maintenance (example for ES futures)
daily_breaks = [
    (time(16, 0), time(17, 0)),  # 4-5 PM CT
]

# Weekend break
weekend_break = (
    (4, time(16, 0)),   # Friday 4 PM
    (6, time(17, 0)),   # Sunday 5 PM
)
```

## 4. Common Mistakes

### Mistake 1: Using Calendar Dates
```python
# WRONG
df['date'] = df.index.date
daily_returns = df.groupby('date')['price'].last().pct_change()

# CORRECT
df['session_date'] = compute_session_date(df.index)
daily_returns = df.groupby('session_date')['price'].last().pct_change()
```

### Mistake 2: Not Filtering Invalid Returns
```python
# WRONG - includes returns ending in breaks
returns = prices.pct_change(H).shift(-H)

# CORRECT - filter invalid timestamps
returns = prices.pct_change(H).shift(-H)
returns = returns[valid_return_mask]
```

### Mistake 3: Shifting Folds for Holidays
```python
# WRONG - shifting to get "full" weeks
if holiday_in_week:
    fold_end += timedelta(days=1)  # DON'T DO THIS

# CORRECT - accept shorter weeks
# Fold boundaries stay on session boundaries regardless of holidays
```

### Mistake 4: Mixing Timezones
```python
# WRONG - naive datetime or wrong timezone
fold_start = datetime(2024, 1, 7, 17, 0)  # What timezone?

# CORRECT - explicit CT timezone
import pytz
ct = pytz.timezone('America/Chicago')
fold_start = ct.localize(datetime(2024, 1, 7, 17, 0))
```

## 5. Checklist

Before proceeding with any CME futures analysis:

- [ ] Data indexed by session date, not calendar date
- [ ] Sunday evening minutes assigned to Monday session
- [ ] Fold boundaries align to session starts/ends
- [ ] Fold definitions stored as explicit timestamps with timezone
- [ ] Forward returns filtered for break invalidity
- [ ] Break schedule defined for the specific contract
- [ ] Timezone handling explicit (America/Chicago for CT)

## References

For detailed implementation patterns, see:
- `{baseDir}/references/session-date-calculation.md`
- `{baseDir}/references/break-schedules.md`
