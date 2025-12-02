"""
Point-in-Time Data Management
=============================

This module provides infrastructure for managing temporal data with proper
handling of observation dates, publication dates, and data revisions.

The key insight is that commodity fundamental data (inventories, production,
demand) is typically:
1. Observed on one date (observation_date)
2. Published/released on a later date (publication_date)
3. Often revised multiple times after initial release

For backtesting and model validation, we must only use data that was
actually available at each point in time - this is the "as-of" concept.

Example:
    # EIA Weekly Petroleum Status Report
    # - Observation: Week ending Friday Jan 12, 2024
    # - Publication: Wednesday Jan 17, 2024 at 10:30am ET
    # - First revision: Following week

    >>> record = PointInTimeRecord(
    ...     series_id='EIA.CRUDE.STOCKS',
    ...     observation_date=datetime(2024, 1, 12),
    ...     publication_date=datetime(2024, 1, 17, 10, 30),
    ...     value=432.5,  # million barrels
    ...     revision=0,
    ...     is_final=False
    ... )
    >>> record.was_known_on(datetime(2024, 1, 18))
    True
    >>> record.was_known_on(datetime(2024, 1, 16))
    False
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, Union, List, Dict, Any, Tuple
import pandas as pd
import numpy as np
import sqlite3
from pathlib import Path
import warnings


@dataclass
class PointInTimeRecord:
    """
    Fundamental unit of temporal data storage.

    A single data point with full temporal metadata including when it
    was observed, when it was published, and revision information.

    Attributes
    ----------
    series_id : str
        Unique identifier for the data series (e.g., "EIA.CRUDE.STOCKS")
    observation_date : datetime
        The date/period the data refers to
    publication_date : datetime
        When the data was released/published
    value : float
        The actual data value
    revision : int
        Revision number (0=initial release, 1=first revision, etc.)
    is_final : bool
        Whether this is the final/definitive value
    source : str, optional
        Data source identifier
    unit : str, optional
        Unit of measurement
    metadata : dict, optional
        Additional metadata

    Examples
    --------
    >>> # EIA crude oil inventory data
    >>> record = PointInTimeRecord(
    ...     series_id='EIA.CRUDE.STOCKS.US',
    ...     observation_date=datetime(2024, 1, 12),
    ...     publication_date=datetime(2024, 1, 17, 10, 30),
    ...     value=432.5,
    ...     revision=0,
    ...     is_final=False,
    ...     source='EIA',
    ...     unit='million_barrels'
    ... )
    """
    series_id: str
    observation_date: datetime
    publication_date: datetime
    value: float
    revision: int = 0
    is_final: bool = False
    source: Optional[str] = None
    unit: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def as_of_date(self) -> datetime:
        """Alias for publication_date - when we knew this value."""
        return self.publication_date

    @property
    def publication_lag(self) -> timedelta:
        """Time between observation and publication."""
        return self.publication_date - self.observation_date

    def was_known_on(self, query_date: datetime) -> bool:
        """
        Check if this data point was available on a specific date.

        Parameters
        ----------
        query_date : datetime
            The date to check availability for

        Returns
        -------
        bool
            True if data was published by query_date
        """
        return self.publication_date <= query_date

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'series_id': self.series_id,
            'observation_date': self.observation_date.isoformat(),
            'publication_date': self.publication_date.isoformat(),
            'value': self.value,
            'revision': self.revision,
            'is_final': self.is_final,
            'source': self.source,
            'unit': self.unit,
            'metadata': self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'PointInTimeRecord':
        """Create from dictionary."""
        data = data.copy()
        data['observation_date'] = datetime.fromisoformat(data['observation_date'])
        data['publication_date'] = datetime.fromisoformat(data['publication_date'])
        return cls(**data)


class PointInTimeDataFrame:
    """
    DataFrame wrapper with point-in-time query capabilities.

    This class wraps a pandas DataFrame and provides methods to query
    data "as of" a specific date, properly handling publication lags
    and data revisions.

    The underlying DataFrame must have columns:
    - observation_date: When the data refers to
    - publication_date: When the data was released
    - value: The data value
    - revision: Revision number (optional, defaults to 0)

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with temporal columns
    series_id : str, optional
        Series identifier

    Examples
    --------
    >>> # Create from DataFrame
    >>> df = pd.DataFrame({
    ...     'observation_date': pd.date_range('2023-01-01', periods=10, freq='W'),
    ...     'publication_date': pd.date_range('2023-01-04', periods=10, freq='W'),
    ...     'value': np.random.randn(10) * 10 + 100,
    ...     'revision': [0] * 10
    ... })
    >>> pit_df = PointInTimeDataFrame(df, series_id='test_series')
    >>>
    >>> # Query data as of a specific date
    >>> known_data = pit_df.as_of(datetime(2023, 2, 1))
    >>> print(f"Known observations: {len(known_data)}")
    """

    def __init__(
        self,
        df: pd.DataFrame,
        series_id: Optional[str] = None,
        observation_col: str = 'observation_date',
        publication_col: str = 'publication_date',
        value_col: str = 'value',
        revision_col: str = 'revision'
    ):
        self.df = df.copy()
        self.series_id = series_id
        self.observation_col = observation_col
        self.publication_col = publication_col
        self.value_col = value_col
        self.revision_col = revision_col

        # Validate required columns
        required = [observation_col, publication_col, value_col]
        missing = [c for c in required if c not in self.df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        # Ensure datetime types
        for col in [observation_col, publication_col]:
            if not pd.api.types.is_datetime64_any_dtype(self.df[col]):
                self.df[col] = pd.to_datetime(self.df[col])

        # Add revision column if missing
        if revision_col not in self.df.columns:
            self.df[revision_col] = 0

        # Sort by observation date and revision
        self.df = self.df.sort_values(
            [observation_col, publication_col, revision_col]
        ).reset_index(drop=True)

    def as_of(self, query_date: Union[datetime, str]) -> pd.DataFrame:
        """
        Get data as it was known on a specific date.

        Returns the most recent revision of each observation that was
        published by the query date.

        Parameters
        ----------
        query_date : datetime or str
            The date to query data for

        Returns
        -------
        pd.DataFrame
            Data available as of query_date, indexed by observation_date

        Examples
        --------
        >>> # Get crude oil inventory data as known on Jan 20, 2024
        >>> known_data = pit_df.as_of('2024-01-20')
        >>> print(known_data.tail())
        """
        if isinstance(query_date, str):
            query_date = pd.to_datetime(query_date)

        # Filter to data published by query_date
        mask = self.df[self.publication_col] <= query_date
        available = self.df[mask].copy()

        if available.empty:
            return pd.DataFrame()

        # For each observation, get the latest revision
        idx = available.groupby(self.observation_col)[self.publication_col].idxmax()
        result = available.loc[idx].set_index(self.observation_col)

        return result.sort_index()

    def get_value_as_of(
        self,
        observation_date: Union[datetime, str],
        as_of_date: Union[datetime, str],
        column: Optional[str] = None
    ) -> Optional[float]:
        """
        Get a specific value as it was known on as_of_date.

        Parameters
        ----------
        observation_date : datetime or str
            The observation period to query
        as_of_date : datetime or str
            When we're "standing" - what was known then
        column : str, optional
            Column to return (defaults to value_col)

        Returns
        -------
        float or None
            The value, or None if not available
        """
        if isinstance(observation_date, str):
            observation_date = pd.to_datetime(observation_date)
        if isinstance(as_of_date, str):
            as_of_date = pd.to_datetime(as_of_date)

        column = column or self.value_col

        # Find matching records
        mask = (
            (self.df[self.observation_col] == observation_date) &
            (self.df[self.publication_col] <= as_of_date)
        )
        matching = self.df[mask]

        if matching.empty:
            return None

        # Return most recent revision
        latest_idx = matching[self.publication_col].idxmax()
        return matching.loc[latest_idx, column]

    def get_revision_history(
        self,
        observation_date: Union[datetime, str]
    ) -> pd.DataFrame:
        """
        Get all revisions for a specific observation date.

        Parameters
        ----------
        observation_date : datetime or str
            The observation date to query

        Returns
        -------
        pd.DataFrame
            All revisions sorted by publication date
        """
        if isinstance(observation_date, str):
            observation_date = pd.to_datetime(observation_date)

        mask = self.df[self.observation_col] == observation_date
        return self.df[mask].sort_values(self.publication_col)

    def revision_statistics(self) -> pd.DataFrame:
        """
        Calculate revision statistics across the dataset.

        Returns
        -------
        pd.DataFrame
            Statistics on revision patterns
        """
        # Group by observation date
        grouped = self.df.groupby(self.observation_col)

        stats = []
        for obs_date, group in grouped:
            if len(group) > 1:
                initial = group.iloc[0][self.value_col]
                final = group.iloc[-1][self.value_col]
                revision_count = len(group) - 1
                revision_magnitude = final - initial
                revision_pct = (final - initial) / abs(initial) * 100 if initial != 0 else 0

                stats.append({
                    'observation_date': obs_date,
                    'initial_value': initial,
                    'final_value': final,
                    'revision_count': revision_count,
                    'revision_magnitude': revision_magnitude,
                    'revision_pct': revision_pct,
                    'days_to_final': (group.iloc[-1][self.publication_col] -
                                     group.iloc[0][self.publication_col]).days
                })

        return pd.DataFrame(stats) if stats else pd.DataFrame()

    def publication_lag_stats(self) -> Dict[str, float]:
        """
        Calculate publication lag statistics.

        Returns
        -------
        dict
            Statistics on publication delays
        """
        lags = (self.df[self.publication_col] -
                self.df[self.observation_col]).dt.days

        return {
            'mean_lag_days': lags.mean(),
            'median_lag_days': lags.median(),
            'min_lag_days': lags.min(),
            'max_lag_days': lags.max(),
            'std_lag_days': lags.std(),
        }

    def create_lagged_features(
        self,
        lags: List[int],
        as_of_date: Union[datetime, str],
        respect_publication: bool = True
    ) -> pd.DataFrame:
        """
        Create lagged features respecting publication dates.

        Parameters
        ----------
        lags : list of int
            Lag periods to create
        as_of_date : datetime or str
            Date we're "standing" at
        respect_publication : bool
            If True, only use data that was published by as_of_date

        Returns
        -------
        pd.DataFrame
            DataFrame with lagged features
        """
        if isinstance(as_of_date, str):
            as_of_date = pd.to_datetime(as_of_date)

        if respect_publication:
            data = self.as_of(as_of_date)
        else:
            data = self.df.set_index(self.observation_col)

        result = pd.DataFrame(index=data.index)
        result['value'] = data[self.value_col]

        for lag in lags:
            result[f'value_lag_{lag}'] = data[self.value_col].shift(lag)

        return result

    @classmethod
    def from_csv(
        cls,
        filepath: Union[str, Path],
        series_id: Optional[str] = None,
        **kwargs
    ) -> 'PointInTimeDataFrame':
        """Load from CSV file."""
        df = pd.read_csv(filepath, **kwargs)
        return cls(df, series_id=series_id)

    def to_csv(self, filepath: Union[str, Path], **kwargs):
        """Save to CSV file."""
        self.df.to_csv(filepath, index=False, **kwargs)

    def __len__(self) -> int:
        return len(self.df)

    def __repr__(self) -> str:
        return (f"PointInTimeDataFrame(series_id={self.series_id}, "
                f"records={len(self.df)}, "
                f"observations={self.df[self.observation_col].nunique()})")


class PointInTimeDatabase:
    """
    SQLite-based point-in-time data store.

    Provides persistent storage for temporal data with efficient
    as-of queries using proper SQL indexing.

    Parameters
    ----------
    db_path : str or Path
        Path to SQLite database file

    Examples
    --------
    >>> db = PointInTimeDatabase('commodities.db')
    >>>
    >>> # Insert data
    >>> record = PointInTimeRecord(
    ...     series_id='EIA.CRUDE.STOCKS',
    ...     observation_date=datetime(2024, 1, 12),
    ...     publication_date=datetime(2024, 1, 17),
    ...     value=432.5,
    ...     revision=0
    ... )
    >>> db.insert(record)
    >>>
    >>> # Query as-of
    >>> data = db.query_as_of('EIA.CRUDE.STOCKS', as_of_date='2024-01-20')
    """

    def __init__(self, db_path: Union[str, Path] = ':memory:'):
        self.db_path = str(db_path)
        self._init_database()

    def _init_database(self):
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS commodity_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    series_id TEXT NOT NULL,
                    observation_date TEXT NOT NULL,
                    publication_date TEXT NOT NULL,
                    value REAL NOT NULL,
                    revision INTEGER DEFAULT 0,
                    is_final INTEGER DEFAULT 0,
                    source TEXT,
                    unit TEXT,
                    metadata TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(series_id, observation_date, publication_date)
                )
            """)

            # Create indexes for efficient queries
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_series_obs
                ON commodity_data(series_id, observation_date)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_series_pub
                ON commodity_data(series_id, publication_date)
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_pub_date
                ON commodity_data(publication_date)
            """)

            conn.commit()

    def insert(self, record: PointInTimeRecord) -> int:
        """
        Insert a single record.

        Parameters
        ----------
        record : PointInTimeRecord
            The record to insert

        Returns
        -------
        int
            Row ID of inserted record
        """
        import json

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT OR REPLACE INTO commodity_data
                (series_id, observation_date, publication_date, value,
                 revision, is_final, source, unit, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                record.series_id,
                record.observation_date.isoformat(),
                record.publication_date.isoformat(),
                record.value,
                record.revision,
                int(record.is_final),
                record.source,
                record.unit,
                json.dumps(record.metadata) if record.metadata else None,
            ))
            conn.commit()
            return cursor.lastrowid

    def insert_many(self, records: List[PointInTimeRecord]) -> int:
        """
        Insert multiple records efficiently.

        Parameters
        ----------
        records : list of PointInTimeRecord
            Records to insert

        Returns
        -------
        int
            Number of records inserted
        """
        import json

        data = [
            (r.series_id, r.observation_date.isoformat(),
             r.publication_date.isoformat(), r.value, r.revision,
             int(r.is_final), r.source, r.unit,
             json.dumps(r.metadata) if r.metadata else None)
            for r in records
        ]

        with sqlite3.connect(self.db_path) as conn:
            conn.executemany("""
                INSERT OR REPLACE INTO commodity_data
                (series_id, observation_date, publication_date, value,
                 revision, is_final, source, unit, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, data)
            conn.commit()
            return len(data)

    def query_as_of(
        self,
        series_id: str,
        as_of_date: Union[datetime, str],
        start_date: Optional[Union[datetime, str]] = None,
        end_date: Optional[Union[datetime, str]] = None
    ) -> pd.DataFrame:
        """
        Query data as it was known on a specific date.

        This is the core as-of query that returns the latest revision
        of each observation that was published by as_of_date.

        Parameters
        ----------
        series_id : str
            Series to query
        as_of_date : datetime or str
            Point in time to query from
        start_date : datetime or str, optional
            Filter observations from this date
        end_date : datetime or str, optional
            Filter observations to this date

        Returns
        -------
        pd.DataFrame
            Data available as of the query date
        """
        if isinstance(as_of_date, str):
            as_of_date = as_of_date
        else:
            as_of_date = as_of_date.isoformat()

        query = """
            SELECT
                series_id,
                observation_date,
                publication_date,
                value,
                revision,
                is_final,
                source,
                unit
            FROM commodity_data
            WHERE series_id = ?
              AND publication_date <= ?
              AND (series_id, observation_date, publication_date) IN (
                  SELECT series_id, observation_date, MAX(publication_date)
                  FROM commodity_data
                  WHERE series_id = ?
                    AND publication_date <= ?
                  GROUP BY series_id, observation_date
              )
        """
        params = [series_id, as_of_date, series_id, as_of_date]

        if start_date:
            if isinstance(start_date, datetime):
                start_date = start_date.isoformat()
            query += " AND observation_date >= ?"
            params.append(start_date)

        if end_date:
            if isinstance(end_date, datetime):
                end_date = end_date.isoformat()
            query += " AND observation_date <= ?"
            params.append(end_date)

        query += " ORDER BY observation_date"

        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(query, conn, params=params)

        # Convert date columns
        for col in ['observation_date', 'publication_date']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])

        return df

    def get_series_list(self) -> List[str]:
        """Get list of all series in database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT DISTINCT series_id FROM commodity_data ORDER BY series_id"
            )
            return [row[0] for row in cursor.fetchall()]

    def get_series_info(self, series_id: str) -> Dict[str, Any]:
        """Get information about a series."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT
                    COUNT(*) as record_count,
                    MIN(observation_date) as first_observation,
                    MAX(observation_date) as last_observation,
                    MIN(publication_date) as first_publication,
                    MAX(publication_date) as last_publication,
                    COUNT(DISTINCT observation_date) as unique_observations,
                    MAX(revision) as max_revision
                FROM commodity_data
                WHERE series_id = ?
            """, (series_id,))
            row = cursor.fetchone()

            return {
                'series_id': series_id,
                'record_count': row[0],
                'first_observation': row[1],
                'last_observation': row[2],
                'first_publication': row[3],
                'last_publication': row[4],
                'unique_observations': row[5],
                'max_revision': row[6],
            }

    def to_point_in_time_dataframe(
        self,
        series_id: str
    ) -> PointInTimeDataFrame:
        """
        Load a series as PointInTimeDataFrame.

        Parameters
        ----------
        series_id : str
            Series to load

        Returns
        -------
        PointInTimeDataFrame
            The series data
        """
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query(
                "SELECT * FROM commodity_data WHERE series_id = ?",
                conn,
                params=(series_id,)
            )

        for col in ['observation_date', 'publication_date']:
            df[col] = pd.to_datetime(df[col])

        return PointInTimeDataFrame(df, series_id=series_id)


def simulate_publication_schedule(
    observation_dates: pd.DatetimeIndex,
    publication_lag_days: int = 4,
    publication_time: str = '10:30:00',
    weekday_only: bool = True
) -> pd.DatetimeIndex:
    """
    Simulate publication dates for observations.

    Parameters
    ----------
    observation_dates : pd.DatetimeIndex
        Observation dates
    publication_lag_days : int
        Days between observation and publication
    publication_time : str
        Time of publication
    weekday_only : bool
        If True, skip weekends for publication

    Returns
    -------
    pd.DatetimeIndex
        Publication dates
    """
    pub_dates = []
    pub_time = pd.to_datetime(publication_time).time()

    for obs_date in observation_dates:
        pub_date = obs_date + timedelta(days=publication_lag_days)

        if weekday_only:
            # Move to next weekday if on weekend
            while pub_date.weekday() >= 5:  # Saturday=5, Sunday=6
                pub_date += timedelta(days=1)

        # Combine date with time
        pub_datetime = datetime.combine(pub_date.date(), pub_time)
        pub_dates.append(pub_datetime)

    return pd.DatetimeIndex(pub_dates)


def create_sample_pit_data(
    series_id: str = 'SAMPLE.SERIES',
    start_date: str = '2020-01-01',
    end_date: str = '2024-01-01',
    frequency: str = 'W-FRI',
    publication_lag_days: int = 4,
    revision_probability: float = 0.3,
    revision_magnitude: float = 0.02
) -> PointInTimeDataFrame:
    """
    Create sample point-in-time data for testing and demonstrations.

    Parameters
    ----------
    series_id : str
        Series identifier
    start_date : str
        Start of observation period
    end_date : str
        End of observation period
    frequency : str
        Observation frequency (e.g., 'W-FRI' for weekly Friday)
    publication_lag_days : int
        Days between observation and publication
    revision_probability : float
        Probability of each observation being revised
    revision_magnitude : float
        Standard deviation of revision as fraction of value

    Returns
    -------
    PointInTimeDataFrame
        Sample data with revisions
    """
    np.random.seed(42)

    # Generate observation dates
    obs_dates = pd.date_range(start=start_date, end=end_date, freq=frequency)

    # Generate initial values (random walk)
    n = len(obs_dates)
    initial_value = 100
    returns = np.random.randn(n) * 0.02
    values = initial_value * np.exp(np.cumsum(returns))

    # Generate publication dates
    pub_dates = simulate_publication_schedule(obs_dates, publication_lag_days)

    # Create records
    records = []

    for i, (obs_date, pub_date, value) in enumerate(zip(obs_dates, pub_dates, values)):
        # Initial release
        records.append({
            'series_id': series_id,
            'observation_date': obs_date,
            'publication_date': pub_date,
            'value': value,
            'revision': 0,
            'is_final': False,
        })

        # Add revision with some probability
        if np.random.random() < revision_probability:
            # Revision comes 7 days after initial publication
            revision_pub_date = pub_date + timedelta(days=7)
            revision_value = value * (1 + np.random.randn() * revision_magnitude)

            records.append({
                'series_id': series_id,
                'observation_date': obs_date,
                'publication_date': revision_pub_date,
                'value': revision_value,
                'revision': 1,
                'is_final': True,
            })

    df = pd.DataFrame(records)
    return PointInTimeDataFrame(df, series_id=series_id)


if __name__ == '__main__':
    # Demo
    print("Point-in-Time Data Infrastructure Demo")
    print("=" * 50)

    # Create sample data
    pit_df = create_sample_pit_data(
        series_id='DEMO.CRUDE.STOCKS',
        start_date='2023-01-01',
        end_date='2024-01-01',
        publication_lag_days=4
    )

    print(f"\nCreated: {pit_df}")
    print(f"\nPublication lag stats: {pit_df.publication_lag_stats()}")

    # Query as of a specific date
    as_of_date = datetime(2023, 6, 15)
    known_data = pit_df.as_of(as_of_date)
    print(f"\nData known as of {as_of_date.date()}:")
    print(known_data.tail())

    # Revision statistics
    rev_stats = pit_df.revision_statistics()
    if not rev_stats.empty:
        print(f"\nRevision statistics:")
        print(f"  Average revision: {rev_stats['revision_pct'].mean():.2f}%")
        print(f"  Max revision: {rev_stats['revision_pct'].abs().max():.2f}%")
