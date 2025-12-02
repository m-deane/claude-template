# Sample Output: Module 2, Section 2.2 - Data Vintage Concepts

*This is an example of what the AI should generate when using the main prompt - showing the level of detail and practical focus expected*

## 2.2 Data Vintage Concepts (60 minutes)

### Understanding the Temporal Trinity

In commodities trading, every piece of fundamental data exists in three temporal dimensions that must be carefully tracked to avoid look-ahead bias:

1. **Observation Date**: When the economic event actually occurred
2. **Publication Date**: When the data was first released to the market
3. **As-of Date**: The point in time from which we're viewing the data

Consider this critical example from crude oil markets:

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

@dataclass
class PointInTimeRecord:
    """
    Fundamental unit of temporal data storage for commodities.

    This class ensures we never accidentally use future information
    in historical analysis or model training.
    """
    series_id: str              # e.g., "EIA.CRUDE.STOCKS"
    observation_date: datetime  # Date data refers to (Friday for EIA)
    publication_date: datetime  # When released (Wednesday 10:30 ET)
    as_of_date: datetime       # Our temporal viewpoint
    value: float               # The actual data point
    revision: int              # 0=first release, 1=first revision, etc.
    is_final: bool            # Is this the final, non-revised value?

    def was_known_on(self, query_date: datetime) -> bool:
        """
        Critical method: Could a trader have known this data point
        on the query_date?

        Args:
            query_date: The date we're checking data availability

        Returns:
            bool: True if data was published by query_date
        """
        return self.publication_date <= query_date

    def days_lag(self) -> int:
        """
        Calculate the reporting lag for this data point.

        Returns:
            int: Days between observation and publication
        """
        return (self.publication_date - self.observation_date).days
```

### Real-World Example: EIA Crude Oil Inventories

The EIA releases crude oil inventory data every Wednesday at 10:30 AM ET, reporting data for the week ending the previous Friday. This creates a consistent 5-day lag that must be properly modeled:

```python
class EIACrudeVintageTracker:
    """
    Manages crude oil inventory data with proper vintage tracking.

    The EIA revises data occasionally due to:
    - Late respondent submissions
    - Error corrections
    - Methodology updates
    """

    def __init__(self):
        self.data_store = []
        self.revision_history = {}

    def add_release(self,
                    observation_week_ending: datetime,
                    value: float,
                    release_datetime: datetime = None,
                    is_revision: bool = False):
        """
        Store a new data release or revision with proper timestamps.

        Args:
            observation_week_ending: Friday date the data refers to
            value: Inventory level in thousands of barrels
            release_datetime: When published (default: next Wed 10:30 ET)
            is_revision: Whether this updates a previous release
        """
        if release_datetime is None:
            # Standard release pattern: Wednesday after observation Friday
            days_until_wednesday = (2 - observation_week_ending.weekday()) % 7
            if days_until_wednesday == 0:
                days_until_wednesday = 7
            release_datetime = observation_week_ending + timedelta(days=days_until_wednesday + 5)
            release_datetime = release_datetime.replace(hour=10, minute=30)

        # Determine revision number
        revision_num = 0
        if is_revision:
            existing = [r for r in self.data_store
                       if r.observation_date == observation_week_ending]
            revision_num = len(existing)

        record = PointInTimeRecord(
            series_id="EIA.CRUDE.STOCKS",
            observation_date=observation_week_ending,
            publication_date=release_datetime,
            as_of_date=release_datetime,  # We know it as of publication
            value=value,
            revision=revision_num,
            is_final=False  # EIA can revise for months
        )

        self.data_store.append(record)

        # Track revision magnitude if applicable
        if is_revision and revision_num > 0:
            original = existing[0].value
            self.revision_history[observation_week_ending] = {
                'original': original,
                'revised': value,
                'revision_magnitude': value - original,
                'revision_percentage': (value - original) / original * 100
            }

    def get_data_as_of(self, as_of_date: datetime) -> pd.DataFrame:
        """
        Retrieve data as it would have been known on a specific date.

        This is the critical method for backtesting - it ensures we only
        use information that was actually available historically.

        Args:
            as_of_date: The point in time to retrieve data for

        Returns:
            DataFrame with the most recent known values as of as_of_date
        """
        # Filter to data published by as_of_date
        known_data = [r for r in self.data_store
                     if r.was_known_on(as_of_date)]

        if not known_data:
            return pd.DataFrame()

        # For each observation date, get the most recent revision
        latest_by_date = {}
        for record in known_data:
            obs_date = record.observation_date
            if obs_date not in latest_by_date:
                latest_by_date[obs_date] = record
            elif record.revision > latest_by_date[obs_date].revision:
                latest_by_date[obs_date] = record

        # Convert to DataFrame
        df_data = []
        for obs_date, record in sorted(latest_by_date.items()):
            df_data.append({
                'observation_date': obs_date,
                'crude_stocks': record.value,
                'publication_lag_days': record.days_lag(),
                'revision_number': record.revision,
                'known_as_of': as_of_date
            })

        return pd.DataFrame(df_data).set_index('observation_date')
```

### Practical Exercise: Detecting Look-Ahead Bias

Here's a common mistake that introduces look-ahead bias, and how to fix it:

```python
def calculate_inventory_change_WRONG(df: pd.DataFrame) -> pd.Series:
    """
    INCORRECT: This function has look-ahead bias!
    It uses Wednesday's inventory to trade on Tuesday.
    """
    # Calculate week-over-week change
    df['inventory_change'] = df['crude_stocks'].diff()

    # Generate signal on Tuesday (day before release!)
    df['signal_date'] = df.index - timedelta(days=1)

    # THIS IS LOOK-AHEAD BIAS - we're using Wednesday's data on Tuesday!
    df['trading_signal'] = df['inventory_change'].apply(
        lambda x: 'BUY' if x < -2000 else 'SELL' if x > 2000 else 'HOLD'
    )

    return df

def calculate_inventory_change_CORRECT(vintage_tracker: EIACrudeVintageTracker,
                                      signal_date: datetime) -> dict:
    """
    CORRECT: Properly respects data availability.
    Only uses data that was known on signal_date.
    """
    # Get data as it was known on signal date
    known_data = vintage_tracker.get_data_as_of(signal_date)

    if len(known_data) < 2:
        return {'signal': 'HOLD', 'reason': 'Insufficient history'}

    # Calculate change using only historical data
    latest_known = known_data.iloc[-1]['crude_stocks']
    previous_known = known_data.iloc[-2]['crude_stocks']
    inventory_change = latest_known - previous_known

    # Note the data vintage we're using
    latest_obs_date = known_data.index[-1]
    days_old = (signal_date - latest_obs_date).days

    # Generate signal with metadata
    signal = {
        'signal': 'BUY' if inventory_change < -2000 else 'SELL' if inventory_change > 2000 else 'HOLD',
        'inventory_change': inventory_change,
        'latest_data_date': latest_obs_date,
        'data_age_days': days_old,
        'signal_generated': signal_date
    }

    return signal
```

### Handling Data Revisions

Data revisions are common in commodities and must be properly tracked:

```python
def analyze_revision_patterns(vintage_tracker: EIACrudeVintageTracker) -> pd.DataFrame:
    """
    Analyze how data revisions affect trading signals.

    This helps us understand:
    1. How large are typical revisions?
    2. Are revisions biased (always up or down)?
    3. Should we wait for revised data before trading?
    """
    revision_stats = []

    for obs_date, revisions in vintage_tracker.revision_history.items():
        # Calculate time between initial release and revision
        original_records = [r for r in vintage_tracker.data_store
                          if r.observation_date == obs_date]

        if len(original_records) >= 2:
            initial_pub = original_records[0].publication_date
            revision_pub = original_records[1].publication_date
            revision_lag = (revision_pub - initial_pub).days

            revision_stats.append({
                'observation_date': obs_date,
                'original_value': revisions['original'],
                'revised_value': revisions['revised'],
                'revision_magnitude': revisions['revision_magnitude'],
                'revision_pct': revisions['revision_percentage'],
                'revision_lag_days': revision_lag,
                'revision_direction': 'UP' if revisions['revision_magnitude'] > 0 else 'DOWN'
            })

    df_revisions = pd.DataFrame(revision_stats)

    # Calculate summary statistics
    print("Revision Pattern Analysis")
    print("=" * 50)
    print(f"Average revision magnitude: {df_revisions['revision_magnitude'].mean():.1f} kb")
    print(f"Average revision %: {df_revisions['revision_pct'].mean():.2f}%")
    print(f"Revision bias: {df_revisions['revision_magnitude'].sum():.1f} kb total")
    print(f"Upward revisions: {(df_revisions['revision_direction'] == 'UP').sum()}")
    print(f"Downward revisions: {(df_revisions['revision_direction'] == 'DOWN').sum()}")
    print(f"Average days until revision: {df_revisions['revision_lag_days'].mean():.1f}")

    return df_revisions
```

### Common Pitfall: Joining Data Without Temporal Alignment

```python
# WRONG: This creates look-ahead bias by misaligning dates
def merge_data_WRONG(prices: pd.DataFrame, fundamentals: pd.DataFrame):
    """
    DON'T DO THIS: Simple merge ignores publication lags.
    """
    # This assumes fundamental data is available on observation date!
    return prices.merge(fundamentals, left_index=True, right_index=True)

# CORRECT: Properly align based on when data was known
def merge_data_CORRECT(prices: pd.DataFrame,
                       vintage_tracker: EIACrudeVintageTracker):
    """
    Properly merge prices with fundamentals respecting publication dates.
    """
    merged_data = []

    for date in prices.index:
        price = prices.loc[date, 'close']

        # Get fundamentals as known on this date
        known_fundamentals = vintage_tracker.get_data_as_of(date)

        if len(known_fundamentals) > 0:
            latest_inventory = known_fundamentals.iloc[-1]['crude_stocks']
            data_age = (date - known_fundamentals.index[-1]).days
        else:
            latest_inventory = np.nan
            data_age = np.nan

        merged_data.append({
            'date': date,
            'price': price,
            'inventory': latest_inventory,
            'inventory_data_age_days': data_age
        })

    return pd.DataFrame(merged_data).set_index('date')
```

### Quiz Questions

1. **Why is publication date different from observation date?**
   - A) Data errors need correction
   - B) Collection, processing, and quality checks take time ✓
   - C) Markets are closed on observation date
   - D) Regulations require delays

2. **When calculating signals for Wednesday trading, which EIA inventory data can you use?**
   - A) Wednesday's release (published 10:30 AM that day)
   - B) The previous Wednesday's release ✓
   - C) Friday's inventory level
   - D) Next Wednesday's forecast

3. **Debug this code - what's wrong?**
```python
# Trading signal for March 15, 2024
signal_date = datetime(2024, 3, 15)
# Get inventory for March 15
inventory = eia_data.loc['2024-03-15', 'crude_stocks']
signal = 'BUY' if inventory < 430000 else 'SELL'
```

**Answer**: Look-ahead bias! March 15's inventory isn't known on March 15. The EIA reports Friday's data the following Wednesday. Should use `get_data_as_of(signal_date)` to get the most recent known value.

### Key Takeaways

✓ Every data point has three dates: observation, publication, and as-of
✓ Trading systems must respect publication lags to avoid look-ahead bias
✓ Data revisions are common and should be tracked for impact analysis
✓ Always use "as-of" queries when backtesting or training models
✓ Join datasets based on when data was known, not when events occurred

### Next Section Preview

In Section 2.3, we'll build a complete point-in-time database using SQLite that can efficiently handle millions of vintage records across multiple commodities while maintaining query performance for backtesting...