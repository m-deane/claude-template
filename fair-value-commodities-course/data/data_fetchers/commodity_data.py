"""
Commodity Data Fetchers
=======================

This module provides utilities to download and cache commodity market data
from various sources including Yahoo Finance and FRED.

Key Features:
- Automatic caching to avoid redundant API calls
- Point-in-time data simulation for backtesting
- Support for multiple data vintages
- Comprehensive commodity coverage
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any, Union
import numpy as np
import pandas as pd
import warnings

# Try to import optional dependencies
try:
    import yfinance as yf
    HAS_YFINANCE = True
except ImportError:
    HAS_YFINANCE = False

try:
    from pandas_datareader import data as pdr
    from fredapi import Fred
    HAS_FRED = True
except ImportError:
    HAS_FRED = False


# Commodity tickers for Yahoo Finance
COMMODITY_TICKERS = {
    # Energy
    'crude_oil': 'CL=F',        # WTI Crude Oil
    'brent_oil': 'BZ=F',        # Brent Crude
    'natural_gas': 'NG=F',      # Natural Gas
    'gasoline': 'RB=F',         # RBOB Gasoline
    'heating_oil': 'HO=F',      # Heating Oil

    # Precious Metals
    'gold': 'GC=F',             # Gold
    'silver': 'SI=F',           # Silver
    'platinum': 'PL=F',         # Platinum
    'palladium': 'PA=F',        # Palladium

    # Base Metals
    'copper': 'HG=F',           # Copper

    # Agriculture
    'corn': 'ZC=F',             # Corn
    'wheat': 'ZW=F',            # Wheat
    'soybeans': 'ZS=F',         # Soybeans
    'soybean_oil': 'ZL=F',      # Soybean Oil
    'soybean_meal': 'ZM=F',     # Soybean Meal
    'coffee': 'KC=F',           # Coffee
    'sugar': 'SB=F',            # Sugar
    'cotton': 'CT=F',           # Cotton
    'cocoa': 'CC=F',            # Cocoa

    # Livestock
    'live_cattle': 'LE=F',      # Live Cattle
    'lean_hogs': 'HE=F',        # Lean Hogs
}

# FRED series codes for economic data
FRED_SERIES = {
    # Interest rates
    'fed_funds': 'FEDFUNDS',
    'treasury_3m': 'DTB3',
    'treasury_10y': 'DGS10',

    # Dollar index
    'dollar_index': 'DTWEXBGS',

    # Inflation
    'cpi': 'CPIAUCSL',
    'pce': 'PCEPI',

    # Economic indicators
    'industrial_production': 'INDPRO',
    'unemployment': 'UNRATE',

    # Energy specific
    'wti_spot': 'DCOILWTICO',
    'brent_spot': 'DCOILBRENTEU',
    'gas_price': 'GASREGW',

    # Inventories (monthly/weekly)
    'crude_inventory': 'WCESTUS1',
    'natural_gas_inventory': 'NGINSTUS',
}


class CommodityDataFetcher:
    """
    Fetch and cache commodity data from various sources.

    Parameters
    ----------
    cache_dir : str
        Directory for caching downloaded data
    fred_api_key : str, optional
        FRED API key (can also be set via FRED_API_KEY env var)
    """

    def __init__(self,
                 cache_dir: str = './data/cache',
                 fred_api_key: Optional[str] = None):
        self.cache_dir = cache_dir
        self.fred_api_key = fred_api_key or os.environ.get('FRED_API_KEY')

        # Create cache directory
        os.makedirs(cache_dir, exist_ok=True)

        # Initialize FRED client if available
        self._fred = None
        if HAS_FRED and self.fred_api_key:
            try:
                self._fred = Fred(api_key=self.fred_api_key)
            except Exception as e:
                warnings.warn(f"Failed to initialize FRED client: {e}")

    def get_commodity_price(self,
                            commodity: str,
                            start: str = '2010-01-01',
                            end: Optional[str] = None,
                            use_cache: bool = True) -> pd.DataFrame:
        """
        Get price data for a commodity.

        Parameters
        ----------
        commodity : str
            Commodity name (e.g., 'crude_oil', 'gold')
        start : str
            Start date
        end : str, optional
            End date (default: today)
        use_cache : bool
            Whether to use cached data if available

        Returns
        -------
        pd.DataFrame
            OHLCV data with datetime index
        """
        if not HAS_YFINANCE:
            raise ImportError("yfinance is required for commodity data. Install with: pip install yfinance")

        # Get ticker
        ticker = COMMODITY_TICKERS.get(commodity)
        if ticker is None:
            raise ValueError(f"Unknown commodity: {commodity}. Available: {list(COMMODITY_TICKERS.keys())}")

        # Check cache
        cache_file = os.path.join(self.cache_dir, f"{commodity}_prices.parquet")
        if use_cache and os.path.exists(cache_file):
            cached = pd.read_parquet(cache_file)

            # Check if cache covers requested range
            cached_start = cached.index[0]
            cached_end = cached.index[-1]

            requested_start = pd.Timestamp(start)
            requested_end = pd.Timestamp(end) if end else pd.Timestamp.today()

            if cached_start <= requested_start and cached_end >= requested_end - timedelta(days=5):
                return cached.loc[start:end]

        # Download from Yahoo Finance
        data = yf.download(ticker, start=start, end=end, progress=False)

        if data.empty:
            warnings.warn(f"No data returned for {commodity}")
            return pd.DataFrame()

        # Rename columns
        data.columns = ['open', 'high', 'low', 'close', 'adj_close', 'volume']
        data.index.name = 'date'

        # Cache the data
        if use_cache:
            data.to_parquet(cache_file)

        return data

    def get_multiple_commodities(self,
                                 commodities: List[str],
                                 column: str = 'adj_close',
                                 start: str = '2010-01-01',
                                 end: Optional[str] = None) -> pd.DataFrame:
        """
        Get price data for multiple commodities.

        Parameters
        ----------
        commodities : list
            List of commodity names
        column : str
            Column to extract ('close', 'adj_close', 'open', etc.)
        start : str
            Start date
        end : str, optional
            End date

        Returns
        -------
        pd.DataFrame
            DataFrame with commodity prices as columns
        """
        prices = {}

        for commodity in commodities:
            try:
                data = self.get_commodity_price(commodity, start, end)
                if not data.empty and column in data.columns:
                    prices[commodity] = data[column]
            except Exception as e:
                warnings.warn(f"Failed to get {commodity}: {e}")

        if not prices:
            return pd.DataFrame()

        return pd.DataFrame(prices)

    def get_fred_series(self,
                        series_id: str,
                        start: str = '2010-01-01',
                        end: Optional[str] = None,
                        use_cache: bool = True) -> pd.Series:
        """
        Get data from FRED.

        Parameters
        ----------
        series_id : str
            FRED series ID (can use alias from FRED_SERIES)
        start : str
            Start date
        end : str, optional
            End date
        use_cache : bool
            Whether to cache data

        Returns
        -------
        pd.Series
            Time series data
        """
        if not HAS_FRED:
            raise ImportError("fredapi is required. Install with: pip install fredapi")

        if self._fred is None:
            raise ValueError("FRED API key not set. Set FRED_API_KEY env var or pass to constructor.")

        # Resolve alias
        series_id = FRED_SERIES.get(series_id, series_id)

        # Check cache
        cache_file = os.path.join(self.cache_dir, f"fred_{series_id}.parquet")
        if use_cache and os.path.exists(cache_file):
            cached = pd.read_parquet(cache_file)['value']
            return cached.loc[start:end]

        # Download from FRED
        data = self._fred.get_series(series_id, start, end)

        if data.empty:
            warnings.warn(f"No data returned for FRED series {series_id}")
            return pd.Series()

        data.name = series_id
        data.index.name = 'date'

        # Cache
        if use_cache:
            pd.DataFrame({'value': data}).to_parquet(cache_file)

        return data

    def get_commodity_fundamentals(self,
                                   commodity: str,
                                   start: str = '2010-01-01',
                                   end: Optional[str] = None) -> pd.DataFrame:
        """
        Get fundamental data for a commodity (price + related series).

        Parameters
        ----------
        commodity : str
            Commodity name
        start : str
            Start date
        end : str, optional
            End date

        Returns
        -------
        pd.DataFrame
            Combined price and fundamental data
        """
        # Get price data
        prices = self.get_commodity_price(commodity, start, end)

        if prices.empty:
            return pd.DataFrame()

        result = pd.DataFrame({
            'price': prices['adj_close'],
            'volume': prices['volume'],
        })

        # Add related FRED series based on commodity
        fred_additions = {
            'crude_oil': ['crude_inventory', 'wti_spot', 'dollar_index'],
            'natural_gas': ['natural_gas_inventory', 'dollar_index'],
            'gold': ['dollar_index', 'treasury_10y', 'fed_funds'],
            'silver': ['dollar_index', 'treasury_10y'],
            'corn': ['dollar_index'],
            'wheat': ['dollar_index'],
            'soybeans': ['dollar_index'],
        }

        related_series = fred_additions.get(commodity, ['dollar_index'])

        for series in related_series:
            try:
                fred_data = self.get_fred_series(series, start, end)
                if not fred_data.empty:
                    result[series] = fred_data
            except Exception as e:
                warnings.warn(f"Could not get {series}: {e}")

        return result

    def get_inventory_data(self,
                           commodity: str,
                           start: str = '2010-01-01',
                           end: Optional[str] = None) -> pd.Series:
        """
        Get inventory data for a commodity.

        Parameters
        ----------
        commodity : str
            Commodity name
        start : str
            Start date
        end : str, optional
            End date

        Returns
        -------
        pd.Series
            Inventory levels
        """
        inventory_series = {
            'crude_oil': 'crude_inventory',
            'natural_gas': 'natural_gas_inventory',
        }

        series_name = inventory_series.get(commodity)
        if series_name is None:
            warnings.warn(f"No inventory data available for {commodity}")
            return pd.Series()

        return self.get_fred_series(series_name, start, end)


def create_sample_dataset(commodity: str = 'crude_oil',
                          n_years: int = 5,
                          include_fundamentals: bool = True,
                          seed: int = 42) -> pd.DataFrame:
    """
    Create a sample dataset for testing and demonstrations.

    This generates synthetic but realistic-looking commodity data when
    actual data sources are not available.

    Parameters
    ----------
    commodity : str
        Commodity type (affects price level and volatility)
    n_years : int
        Number of years of data to generate
    include_fundamentals : bool
        Whether to include fundamental data columns
    seed : int
        Random seed for reproducibility

    Returns
    -------
    pd.DataFrame
        Sample dataset
    """
    np.random.seed(seed)

    # Parameters by commodity
    params = {
        'crude_oil': {'base_price': 70, 'volatility': 0.25, 'mean_reversion': 0.02},
        'gold': {'base_price': 1800, 'volatility': 0.15, 'mean_reversion': 0.01},
        'natural_gas': {'base_price': 3.5, 'volatility': 0.40, 'mean_reversion': 0.05},
        'corn': {'base_price': 500, 'volatility': 0.20, 'mean_reversion': 0.03},
        'wheat': {'base_price': 600, 'volatility': 0.22, 'mean_reversion': 0.03},
    }

    p = params.get(commodity, params['crude_oil'])

    # Generate dates
    n_days = n_years * 252
    end_date = pd.Timestamp.today()
    start_date = end_date - pd.Timedelta(days=int(n_days * 365 / 252))
    dates = pd.bdate_range(start=start_date, end=end_date)[:n_days]

    # Generate price using mean-reverting process with seasonality
    dt = 1/252
    prices = np.zeros(n_days)
    prices[0] = p['base_price']

    for t in range(1, n_days):
        # Mean reversion component
        mr = p['mean_reversion'] * (p['base_price'] - prices[t-1]) * dt

        # Random component
        shock = np.random.normal(0, p['volatility'] * np.sqrt(dt)) * prices[t-1]

        # Seasonal component (annual cycle)
        day_of_year = dates[t].dayofyear
        seasonal = 0.05 * np.sin(2 * np.pi * day_of_year / 365) * prices[t-1] * dt

        prices[t] = prices[t-1] + mr + shock + seasonal
        prices[t] = max(prices[t], p['base_price'] * 0.3)  # Floor

    # Build DataFrame
    data = pd.DataFrame({
        'price': prices,
        'volume': np.random.lognormal(15, 0.5, n_days).astype(int),
    }, index=dates)

    data.index.name = 'date'

    if include_fundamentals:
        # Add inventory (mean-reverting around 0)
        inventory = np.zeros(n_days)
        inventory[0] = 0
        for t in range(1, n_days):
            inventory[t] = 0.95 * inventory[t-1] + np.random.normal(0, 5)

        # Scale to reasonable levels (in millions of barrels for oil)
        inventory_mean = 400
        data['inventory'] = inventory_mean + inventory

        # Add production and consumption
        data['production'] = 10 + np.cumsum(np.random.normal(0, 0.02, n_days))
        data['consumption'] = 10.5 + np.cumsum(np.random.normal(0, 0.02, n_days))

        # Add interest rate
        data['interest_rate'] = 2 + 3 * np.sin(np.linspace(0, 2*np.pi, n_days)) + np.random.normal(0, 0.1, n_days)
        data['interest_rate'] = data['interest_rate'].clip(0, 10)

        # Add dollar index
        data['dollar_index'] = 100 + np.cumsum(np.random.normal(0, 0.2, n_days))
        data['dollar_index'] = data['dollar_index'].clip(80, 120)

    return data


def prepare_training_data(data: pd.DataFrame,
                          target_column: str = 'price',
                          feature_columns: List[str] = None,
                          test_size: float = 0.2) -> Dict[str, pd.DataFrame]:
    """
    Prepare data for training with temporal train/test split.

    Parameters
    ----------
    data : pd.DataFrame
        Input data
    target_column : str
        Name of target column
    feature_columns : list, optional
        Feature column names (uses all except target if None)
    test_size : float
        Fraction of data for testing

    Returns
    -------
    dict
        Dictionary with 'X_train', 'X_test', 'y_train', 'y_test' keys
    """
    # Sort by date
    data = data.sort_index()

    # Determine split point
    split_idx = int(len(data) * (1 - test_size))

    # Split
    train_data = data.iloc[:split_idx]
    test_data = data.iloc[split_idx:]

    # Separate features and target
    if feature_columns is None:
        feature_columns = [c for c in data.columns if c != target_column]

    return {
        'X_train': train_data[feature_columns],
        'X_test': test_data[feature_columns],
        'y_train': train_data[target_column],
        'y_test': test_data[target_column],
        'train_dates': train_data.index,
        'test_dates': test_data.index,
    }
