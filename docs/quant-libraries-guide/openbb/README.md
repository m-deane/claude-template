# OpenBB Platform - Comprehensive User Reference Guide

**Version:** 4.5.0 (October 2025)
**Status:** Actively Maintained
**Purpose:** Financial Data Acquisition Platform
**License:** AGPLv3

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [Complete API Reference](#complete-api-reference)
5. [Data Provider Configuration](#data-provider-configuration)
6. [Use Cases by Skill Level](#use-cases-by-skill-level)
7. [Core Concepts](#core-concepts)
8. [Best Practices & Common Pitfalls](#best-practices--common-pitfalls)

---

## Overview

OpenBB Platform is an open-source financial data platform consolidating ~100 data sources into a unified interface. It operates on a "connect once, consume everywhere" model.

**Key Capabilities:**
- Equity data (prices, fundamentals, profiles)
- Options and derivatives
- Economic indicators
- Cryptocurrency and forex
- ETFs and fixed income
- Technical analysis
- REST API for multi-language access

---

## Installation

### Python Requirements
- **Minimum:** Python 3.9.21
- **Recommended:** Python 3.10 - 3.13
- **Note:** Python 3.9 deprecated (support ends fall 2025)

### Installation Commands

```bash
# Basic (core + essential providers)
pip install openbb

# All extensions and providers
pip install openbb[all]

# Technical analysis extension
pip install openbb-technical

# CLI interface
pip install openbb-cli

# Charting extension
pip install openbb-charting
```

### System Requirements
- Modern processor (< 5 years old)
- 4GB RAM minimum
- Windows: Microsoft Visual C++ 14.0+
- Linux: Rust/Cargo in PATH

---

## Quick Start

```python
from openbb import obb

# Fetch stock data
data = obb.equity.price.historical('AAPL', start_date='2023-01-01')
df = data.to_dataframe()
print(df.head())

# Get company metrics
metrics = obb.equity.fundamental.metrics('AAPL')
print(metrics.to_df())

# Economic data
gdp = obb.economy.gdp.real(country='united_states')
print(gdp.to_df())
```

---

## Complete API Reference

### Module: obb.equity

#### obb.equity.price.historical()

```python
obb.equity.price.historical(
    symbol,                     # str - Stock ticker (Required)
    start_date=None,            # str - 'YYYY-MM-DD'
    end_date=None,              # str - 'YYYY-MM-DD'
    provider=None               # str - 'fmp', 'polygon', 'yfinance', etc.
)
```

**Returns:** OBBject with OHLCV data

**Example:**
```python
data = obb.equity.price.historical(
    symbol='AAPL',
    start_date='2023-01-01',
    end_date='2023-12-31',
    provider='yfinance'
)
df = data.to_dataframe()
```

#### obb.equity.price.quote()

```python
obb.equity.price.quote(
    symbol,                     # str - Ticker(s), comma-separated
    provider=None               # str - 'cboe', 'fmp', 'yfinance', etc.
)
```

**Returns:** Real-time quote with open, high, low, close, volume, change %

#### obb.equity.profile()

```python
obb.equity.profile(
    symbol,                     # str - Stock ticker
    provider=None               # str - 'finviz', 'fmp', 'yfinance'
)
```

**Returns:** Company description, sector, industry, executives

---

### Fundamental Analysis Functions

#### obb.equity.fundamental.balance()

```python
obb.equity.fundamental.balance(
    symbol,                     # str - Stock ticker
    period='annual',            # str - 'annual' or 'quarter'
    limit=5,                    # int - Number of periods
    provider=None               # str - 'fmp', 'intrinio', 'polygon'
)
```

**Returns:** Balance sheet (assets, liabilities, equity)

#### obb.equity.fundamental.income()

```python
obb.equity.fundamental.income(
    symbol,
    period='annual',
    limit=5,
    provider=None
)
```

**Returns:** Income statement (revenue, expenses, net income)

#### obb.equity.fundamental.cash()

```python
obb.equity.fundamental.cash(
    symbol,
    period='annual',
    limit=5,
    provider=None
)
```

**Returns:** Cash flow statement

#### obb.equity.fundamental.metrics()

```python
obb.equity.fundamental.metrics(
    symbol,
    period=None,                # str - 'annual', 'quarter', 'ttm'
    limit=None,
    provider=None
)
```

**Returns comprehensive metrics:**
- Valuation: PE, PEG, P/B, P/S, EV/EBITDA
- Profitability: ROE, ROA, ROIC, margins
- Liquidity: Current ratio, quick ratio
- Growth: EPS growth, revenue growth
- Other: Dividend yield, beta

#### obb.equity.fundamental.ratios()

```python
obb.equity.fundamental.ratios(
    symbol,
    period=None,
    limit=None,
    provider=None
)
```

**Returns 30+ ratios:**
- Liquidity: current_ratio, quick_ratio, cash_ratio
- Efficiency: inventory_turnover, asset_turnover
- Profitability: gross_margin, operating_margin, net_margin
- Leverage: debt_ratio, debt_to_equity, interest_coverage

#### obb.equity.fundamental.dividends()

```python
obb.equity.fundamental.dividends(
    symbol,
    provider=None               # 'fmp', 'intrinio', 'nasdaq', 'yfinance'
)
```

**Returns:** Historical dividend data

#### Complete Fundamental Function List

```python
obb.equity.fundamental.balance()
obb.equity.fundamental.balance_growth()
obb.equity.fundamental.cash()
obb.equity.fundamental.cash_growth()
obb.equity.fundamental.dividends()
obb.equity.fundamental.employee_count()
obb.equity.fundamental.filings()
obb.equity.fundamental.historical_eps()
obb.equity.fundamental.historical_splits()
obb.equity.fundamental.income()
obb.equity.fundamental.income_growth()
obb.equity.fundamental.management()
obb.equity.fundamental.management_compensation()
obb.equity.fundamental.metrics()
obb.equity.fundamental.multiples()
obb.equity.fundamental.overview()
obb.equity.fundamental.ratios()
obb.equity.fundamental.revenue_per_geography()
obb.equity.fundamental.revenue_per_segment()
obb.equity.fundamental.transcript()
```

---

### Module: obb.derivatives

#### obb.derivatives.options.chains()

```python
obb.derivatives.options.chains(
    symbol,                     # str - Stock ticker
    date=None,                  # str - Expiration filter
    provider=None               # str - 'cboe', 'intrinio', 'tradier'
)
```

**Returns comprehensive options data:**
- Contract: symbol, expiration, strike, type (call/put)
- Pricing: last_price, bid, ask
- Volume: volume, open_interest
- Volatility: implied_volatility
- Greeks: delta, gamma, theta, vega, rho

**Example:**
```python
options = obb.derivatives.options.chains('AAPL')
df = options.to_dataframe()

# Filter calls expiring in 30 days
import datetime
target = datetime.date.today() + datetime.timedelta(days=30)
calls = df[(df['option_type'] == 'call') &
           (df['expiration'] <= str(target))]
```

#### obb.derivatives.options.unusual()

```python
obb.derivatives.options.unusual(
    symbol=None,
    provider=None
)
```

**Returns:** Unusual options activity

#### obb.derivatives.futures.historical()

```python
obb.derivatives.futures.historical(
    symbol,                     # str - Futures symbol
    start_date=None,
    end_date=None,
    provider=None
)
```

#### obb.derivatives.futures.curve()

```python
obb.derivatives.futures.curve(
    symbol,                     # str - Futures symbol
    provider=None
)
```

**Returns:** Term structure / futures curve

---

### Module: obb.economy

#### obb.economy.gdp.real()

```python
obb.economy.gdp.real(
    country=None,               # str - Country or comma-separated list
    start_date=None,
    end_date=None,
    provider=None               # str - 'oecd', 'econdb', 'fred'
)
```

**Returns:** Real GDP with growth rates (QoQ, YoY)

**Example:**
```python
gdp = obb.economy.gdp.real(
    country='united_states,germany,japan',
    provider='econdb'
)
df = gdp.to_dataframe()
```

#### obb.economy.cpi()

```python
obb.economy.cpi(
    country=None,
    transform='yoy',            # str - 'period', 'yoy', 'mom'
    start_date=None,
    end_date=None,
    provider=None               # str - 'fred', 'oecd'
)
```

**Returns:** Consumer Price Index data

**Transform options:**
- `period`: Change since previous period
- `yoy`: Year-over-year (default)
- `mom`: Month-over-month

#### obb.economy.indicators()

```python
obb.economy.indicators(
    symbol=None,                # str - Indicator symbol
    country=None,
    start_date=None,
    end_date=None,
    provider='econdb'
)
```

**Returns:** Various economic indicators

#### obb.economy.fred_search()

```python
obb.economy.fred_search(
    query,                      # str - Search query
    provider='fred'
)
```

**Returns:** FRED series matching query

#### obb.economy.fred_series()

```python
obb.economy.fred_series(
    series_id,                  # str - FRED series ID
    start_date=None,
    end_date=None,
    provider='fred'
)
```

**Example:**
```python
# 10-Year Treasury Rate
treasury = obb.economy.fred_series('DGS10')
df = treasury.to_dataframe()
```

#### obb.economy.unemployment()

```python
obb.economy.unemployment(
    country=None,
    start_date=None,
    end_date=None,
    provider=None
)
```

---

### Module: obb.crypto

```python
# Historical prices
obb.crypto.price.historical(
    symbol,                     # str - 'BTC', 'ETH', etc.
    start_date=None,
    end_date=None,
    provider=None
)

# Discovery
obb.crypto.discovery.top_gainers(provider=None)
obb.crypto.discovery.top_losers(provider=None)
obb.crypto.discovery.trending(provider=None)
obb.crypto.discovery.top_by_market_cap(provider=None)
```

---

### Module: obb.currency

```python
# Search currency pairs
obb.currency.search(query=None, provider=None)

# Historical forex data
obb.currency.price.historical(
    symbol,                     # str - 'EURUSD', etc.
    start_date=None,
    end_date=None,
    provider=None
)
```

---

### Module: obb.etf

```python
# Search ETFs
obb.etf.search(query=None, provider=None)

# Historical ETF prices
obb.etf.price.historical(
    symbol,
    start_date=None,
    end_date=None,
    provider=None
)

# ETF holdings
obb.etf.holdings(symbol, provider=None)

# ETF sector weights
obb.etf.sectors(symbol, provider=None)
```

**Example:**
```python
# Get SPY holdings
holdings = obb.etf.holdings('SPY')
df = holdings.to_dataframe()
print(df.head(10))  # Top 10 holdings
```

---

### Module: obb.fixedincome

```python
# Treasury rates
obb.fixedincome.government.treasury_rates(
    start_date=None,
    end_date=None,
    provider=None
)

# Corporate bonds
obb.fixedincome.corporate.bonds(provider=None)

# Bond spreads
obb.fixedincome.spreads(provider=None)
```

---

### Module: obb.technical

**Requires:** `pip install openbb-technical`

#### Moving Averages

```python
# Simple Moving Average
obb.technical.sma(
    data,                       # DataFrame or OBBject
    target='close',             # str - Column to calculate on
    length=50                   # int - Period
)

# Exponential Moving Average
obb.technical.ema(data, target='close', length=50)

# Weighted Moving Average
obb.technical.wma(data, target='close', length=50)
```

#### Momentum Indicators

```python
# RSI
obb.technical.rsi(
    data,
    target='close',
    length=14
)

# MACD
obb.technical.macd(
    data,
    target='close',
    fast=12,
    slow=26,
    signal=9
)

# Stochastic
obb.technical.stoch(data, fast_k=14, slow_d=3, slow_k=3)
```

#### Volatility Indicators

```python
# Bollinger Bands
obb.technical.bbands(
    data,
    target='close',
    length=20,
    std=2.0
)
# Returns: upper, middle, lower bands

# ATR
obb.technical.atr(data, length=14)

# Keltner Channel
obb.technical.kc(data, length=20, scalar=2)
```

#### Volume Indicators

```python
# On-Balance Volume
obb.technical.obv(data)

# VWAP
obb.technical.vwap(data)

# Accumulation/Distribution
obb.technical.ad(data)
```

#### Complete Technical Indicator List

```python
obb.technical.ad()          # Accumulation/Distribution
obb.technical.adosc()       # A/D Oscillator
obb.technical.adx()         # Average Directional Index
obb.technical.aroon()       # Aroon Indicator
obb.technical.atr()         # Average True Range
obb.technical.bbands()      # Bollinger Bands
obb.technical.cci()         # Commodity Channel Index
obb.technical.donchian()    # Donchian Channels
obb.technical.ema()         # Exponential MA
obb.technical.fib()         # Fibonacci Levels
obb.technical.fisher()      # Fisher Transform
obb.technical.hma()         # Hull MA
obb.technical.ichimoku()    # Ichimoku Cloud
obb.technical.kc()          # Keltner Channel
obb.technical.macd()        # MACD
obb.technical.obv()         # On-Balance Volume
obb.technical.rsi()         # RSI
obb.technical.sma()         # Simple MA
obb.technical.stoch()       # Stochastic
obb.technical.vwap()        # VWAP
obb.technical.wma()         # Weighted MA
obb.technical.zlma()        # Zero Lag MA
```

---

## Data Provider Configuration

### Available Providers

| Provider | API Key | Cost | Data Types |
|----------|---------|------|------------|
| Yahoo Finance | No | Free | Equity, ETF, Crypto, Forex |
| FMP | Yes | Free tier + Paid | Equity, Fundamentals, Crypto |
| Polygon | Yes | Free tier + Paid | Equity, Options, Crypto |
| FRED | Yes | Free | Economy, Rates |
| Intrinio | Yes | Paid | Equity, Fundamentals, Options |
| SEC | No | Free | Filings, Fundamentals |
| Tiingo | Yes | Free tier + Paid | Equity, Crypto |
| Alpha Vantage | Yes | Free tier + Paid | Equity, Technical |
| OECD | No | Free | Economy |
| Tradier | Yes | Free sandbox + Paid | Equity, Options |
| CBOE | No | Free | Options, Volatility |
| Finviz | No | Free | Screener |

### Configuration Methods

#### Method 1: JSON Configuration File

Location: `~/.openbb_platform/user_settings.json`

```json
{
  "credentials": {
    "fmp_api_key": "YOUR_FMP_KEY",
    "polygon_api_key": "YOUR_POLYGON_KEY",
    "fred_api_key": "YOUR_FRED_KEY",
    "intrinio_api_key": "YOUR_INTRINIO_KEY",
    "tiingo_token": "YOUR_TIINGO_KEY"
  }
}
```

#### Method 2: Python Session

```python
from openbb import obb

# Set for current session only
obb.user.credentials.fmp_api_key = "YOUR_KEY"
obb.user.credentials.fred_api_key = "YOUR_KEY"

# Save permanently
obb.account.save()
```

#### Method 3: OpenBB Hub (Cloud Sync)

```python
from openbb import obb

# Login with Personal Access Token
obb.account.login(pat="YOUR_PAT_TOKEN")
```

### Obtaining Free API Keys

**FRED (Free):**
- URL: https://fred.stlouisfed.org/docs/api/api_key.html
- Instant registration

**FMP (Free tier):**
- URL: https://site.financialmodelingprep.com/developer/docs
- Free tier with limits

**Polygon (Free tier):**
- URL: https://polygon.io/
- Free tier available

**Alpha Vantage (Free tier):**
- URL: https://www.alphavantage.co/support/#api-key
- Instant API key

---

## Use Cases by Skill Level

### BEGINNER: Fetch Stock Data

```python
"""
Beginner Example: Basic stock analysis
Goal: Get price data and key metrics for a stock
"""
from openbb import obb
import pandas as pd

# Step 1: Get historical prices
print("=== Historical Prices ===")
data = obb.equity.price.historical(
    symbol='AAPL',
    start_date='2023-01-01',
    provider='yfinance'  # Free, no API key needed
)

df = data.to_dataframe()
print(f"Shape: {df.shape}")
print(df.tail())

# Step 2: Get current quote
print("\n=== Current Quote ===")
quote = obb.equity.price.quote('AAPL', provider='yfinance')
print(quote.to_df())

# Step 3: Get company profile
print("\n=== Company Profile ===")
profile = obb.equity.profile('AAPL', provider='yfinance')
profile_df = profile.to_df()
print(profile_df[['sector', 'industry', 'full_time_employees']])

# Step 4: Get key metrics
print("\n=== Key Metrics ===")
metrics = obb.equity.fundamental.metrics('AAPL', provider='fmp')
metrics_df = metrics.to_df().T  # Transpose for readability
print(metrics_df)

# Step 5: Calculate basic returns
print("\n=== Returns Analysis ===")
df['returns'] = df['close'].pct_change()
print(f"Total Return: {(df['close'].iloc[-1] / df['close'].iloc[0] - 1):.2%}")
print(f"Avg Daily Return: {df['returns'].mean():.4%}")
print(f"Daily Volatility: {df['returns'].std():.4%}")
```

### INTERMEDIATE: Fundamental Screening

```python
"""
Intermediate Example: Multi-stock fundamental screening
Goal: Compare multiple stocks on key metrics
"""
from openbb import obb
import pandas as pd

# Define universe
stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']

# Collect metrics for all stocks
results = []
for symbol in stocks:
    try:
        metrics = obb.equity.fundamental.metrics(symbol, provider='fmp')
        data = metrics.to_dict()
        if data:
            data[0]['symbol'] = symbol
            results.append(data[0])
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")

# Create comparison DataFrame
df = pd.DataFrame(results)
df = df.set_index('symbol')

# Select key metrics
key_metrics = [
    'market_cap', 'pe_ratio', 'forward_pe', 'peg_ratio',
    'price_to_book', 'roe', 'profit_margin', 'revenue_growth'
]
comparison = df[key_metrics]

print("=== Fundamental Comparison ===")
print(comparison.round(2))

# Rank by PEG ratio (lower is better)
print("\n=== Ranked by PEG Ratio ===")
ranked = comparison.sort_values('peg_ratio')
print(ranked)

# Simple scoring
def score_stock(row):
    score = 0
    # Lower PE is better
    if row['pe_ratio'] < 25:
        score += 1
    if row['pe_ratio'] < 15:
        score += 1
    # Higher ROE is better
    if row['roe'] > 0.15:
        score += 1
    if row['roe'] > 0.25:
        score += 1
    # Higher profit margin is better
    if row['profit_margin'] > 0.20:
        score += 1
    return score

comparison['score'] = comparison.apply(score_stock, axis=1)
print("\n=== Scored Comparison ===")
print(comparison.sort_values('score', ascending=False))
```

### ADVANCED: Options Analysis

```python
"""
Advanced Example: Options chain analysis with Greeks
Goal: Analyze options for trading opportunities
"""
from openbb import obb
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Get options chain
print("=== Fetching Options Chain ===")
options = obb.derivatives.options.chains('AAPL')
df = options.to_dataframe()

print(f"Total contracts: {len(df)}")
print(f"Expirations: {df['expiration'].nunique()}")

# Filter for near-term options (30-45 days)
today = datetime.now().date()
target_start = today + timedelta(days=30)
target_end = today + timedelta(days=45)

df['expiration'] = pd.to_datetime(df['expiration']).dt.date
near_term = df[
    (df['expiration'] >= target_start) &
    (df['expiration'] <= target_end)
]

print(f"\nNear-term contracts: {len(near_term)}")

# Separate calls and puts
calls = near_term[near_term['option_type'] == 'call']
puts = near_term[near_term['option_type'] == 'put']

# Find ATM options (delta closest to 0.5 for calls, -0.5 for puts)
if 'delta' in calls.columns:
    atm_call = calls.loc[(calls['delta'] - 0.5).abs().idxmin()]
    atm_put = puts.loc[(puts['delta'] + 0.5).abs().idxmin()]

    print("\n=== ATM Call ===")
    print(f"Strike: ${atm_call['strike']:.2f}")
    print(f"Premium: ${atm_call['last_price']:.2f}")
    print(f"IV: {atm_call['implied_volatility']:.1%}")
    print(f"Delta: {atm_call['delta']:.3f}")
    print(f"Gamma: {atm_call['gamma']:.4f}")
    print(f"Theta: {atm_call['theta']:.3f}")
    print(f"Vega: {atm_call['vega']:.3f}")

    print("\n=== ATM Put ===")
    print(f"Strike: ${atm_put['strike']:.2f}")
    print(f"Premium: ${atm_put['last_price']:.2f}")
    print(f"IV: {atm_put['implied_volatility']:.1%}")
    print(f"Delta: {atm_put['delta']:.3f}")

# Find high IV options (potential premium selling)
print("\n=== Highest IV Options ===")
high_iv = near_term.nlargest(5, 'implied_volatility')[
    ['strike', 'option_type', 'expiration', 'implied_volatility', 'last_price', 'open_interest']
]
print(high_iv)

# Calculate put-call ratio
pc_ratio = puts['open_interest'].sum() / calls['open_interest'].sum()
print(f"\n=== Market Sentiment ===")
print(f"Put-Call OI Ratio: {pc_ratio:.2f}")
if pc_ratio > 1.2:
    print("Interpretation: Bearish sentiment")
elif pc_ratio < 0.8:
    print("Interpretation: Bullish sentiment")
else:
    print("Interpretation: Neutral sentiment")
```

### EXPERT: Economic Dashboard

```python
"""
Expert Example: Multi-source economic dashboard
Goal: Build comprehensive economic overview
"""
from openbb import obb
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class EconomicDashboard:
    """Production-grade economic data dashboard."""

    def __init__(self):
        self.data = {}
        self.errors = []

    def fetch_with_fallback(self, func, name, **kwargs):
        """Fetch data with error handling."""
        try:
            result = func(**kwargs)
            self.data[name] = result.to_dataframe()
            return True
        except Exception as e:
            self.errors.append(f"{name}: {e}")
            return False

    def fetch_us_data(self):
        """Fetch US economic indicators."""
        # GDP
        self.fetch_with_fallback(
            obb.economy.gdp.real,
            'us_gdp',
            country='united_states',
            provider='fred'
        )

        # CPI (Inflation)
        self.fetch_with_fallback(
            obb.economy.cpi,
            'us_cpi',
            country='united_states',
            transform='yoy'
        )

        # Unemployment
        self.fetch_with_fallback(
            obb.economy.unemployment,
            'us_unemployment',
            country='united_states'
        )

        # Treasury yields
        self.fetch_with_fallback(
            obb.fixedincome.government.treasury_rates,
            'treasury_rates'
        )

        # FRED series (specific indicators)
        fred_series = {
            'fed_funds': 'FEDFUNDS',
            'initial_claims': 'ICSA',
            'consumer_sentiment': 'UMCSENT'
        }

        for name, series_id in fred_series.items():
            self.fetch_with_fallback(
                obb.economy.fred_series,
                name,
                series_id=series_id
            )

    def fetch_global_data(self):
        """Fetch global comparison data."""
        countries = 'united_states,germany,japan,china,united_kingdom'

        self.fetch_with_fallback(
            obb.economy.gdp.real,
            'global_gdp',
            country=countries,
            provider='oecd'
        )

        self.fetch_with_fallback(
            obb.economy.cpi,
            'global_cpi',
            country=countries
        )

    def analyze_yield_curve(self):
        """Analyze treasury yield curve for recession signals."""
        if 'treasury_rates' not in self.data:
            return None

        rates = self.data['treasury_rates']

        # Get latest rates
        latest = rates.iloc[-1]

        analysis = {
            '2y_rate': latest.get('month_2', np.nan),
            '10y_rate': latest.get('year_10', np.nan),
            'spread_2y_10y': latest.get('year_10', 0) - latest.get('month_2', 0)
        }

        # Inversion check
        if analysis['spread_2y_10y'] < 0:
            analysis['signal'] = 'INVERTED - Recession Warning'
        elif analysis['spread_2y_10y'] < 0.5:
            analysis['signal'] = 'FLAT - Caution'
        else:
            analysis['signal'] = 'NORMAL'

        return analysis

    def calculate_trends(self):
        """Calculate trend indicators."""
        trends = {}

        for name, df in self.data.items():
            if df is not None and len(df) > 0:
                try:
                    # Find numeric column
                    numeric_cols = df.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        col = numeric_cols[0]
                        latest = df[col].iloc[-1]
                        prev_year = df[col].iloc[-12] if len(df) >= 12 else df[col].iloc[0]

                        trends[name] = {
                            'current': latest,
                            'year_ago': prev_year,
                            'yoy_change': (latest - prev_year) / prev_year if prev_year != 0 else 0
                        }
                except Exception:
                    pass

        return trends

    def generate_report(self):
        """Generate comprehensive dashboard report."""
        print("=" * 70)
        print("ECONOMIC DASHBOARD REPORT")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print("=" * 70)

        # Fetch data
        print("\nFetching data...")
        self.fetch_us_data()
        self.fetch_global_data()

        if self.errors:
            print("\nWarnings:")
            for error in self.errors:
                print(f"  - {error}")

        # Yield Curve Analysis
        print("\n" + "-" * 50)
        print("YIELD CURVE ANALYSIS")
        print("-" * 50)
        curve = self.analyze_yield_curve()
        if curve:
            print(f"2-Year Rate: {curve['2y_rate']:.2%}")
            print(f"10-Year Rate: {curve['10y_rate']:.2%}")
            print(f"2Y-10Y Spread: {curve['spread_2y_10y']:.2%}")
            print(f"Signal: {curve['signal']}")

        # Trend Analysis
        print("\n" + "-" * 50)
        print("TREND ANALYSIS (YoY)")
        print("-" * 50)
        trends = self.calculate_trends()
        for name, data in trends.items():
            print(f"\n{name.upper()}:")
            print(f"  Current: {data['current']:.2f}")
            print(f"  YoY Change: {data['yoy_change']:.1%}")

        # Summary
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Data Sources Used: {len(self.data)}")
        print(f"Errors Encountered: {len(self.errors)}")

        return self.data

# Usage
dashboard = EconomicDashboard()
data = dashboard.generate_report()
```

---

## Core Concepts

### OBBject Return Type

All OpenBB functions return an `OBBject` wrapper:

```python
output = obb.equity.price.historical('AAPL')

# Methods
df = output.to_dataframe()    # Convert to DataFrame
df = output.to_df()           # Shorthand
dict_data = output.to_dict()  # Convert to dict
json_data = output.to_json()  # Convert to JSON
output.chart()                # Display chart (requires openbb-charting)
output.show()                 # Display data

# Properties
data = output.results         # Raw data
provider = output.provider    # Which provider used
warnings = output.warnings    # Any warnings
```

### Multi-Provider Architecture

- OpenBB aggregates data from multiple providers
- Standardized interface across all providers
- Specify provider explicitly or use priority list
- Provider-specific fields may vary

```python
# Explicit provider
obb.equity.price.historical('AAPL', provider='yfinance')

# Using priority (from user_settings.json)
obb.equity.price.historical('AAPL')  # Uses configured priority
```

### Extensions System

```bash
# Data extensions (providers)
pip install openbb-fmp
pip install openbb-polygon

# Toolkit extensions
pip install openbb-technical
pip install openbb-quantitative

# Charting
pip install openbb-charting
```

---

## Best Practices & Common Pitfalls

### Best Practices

1. **Specify provider explicitly** for production applications
2. **Configure multiple providers** as fallbacks
3. **Cache frequently accessed data** to minimize API calls
4. **Check `output.warnings`** for potential issues
5. **Use paid providers** for critical applications
6. **Handle rate limits** with appropriate delays

### Common Pitfalls

| Issue | Symptom | Solution |
|-------|---------|----------|
| API key not configured | Function unavailable | Set key in user_settings.json |
| Rate limit exceeded | Requests fail | Use paid tier or throttle |
| Symbol not found | No data returned | Use search functions first |
| Missing extension | Module not found | Install: `pip install openbb-{ext}` |
| Provider fields vary | Missing expected columns | Try different provider |
| Data quality issues | Inconsistent data | Use paid providers |

### Provider Selection Guide

| Use Case | Recommended Provider |
|----------|---------------------|
| Quick prototyping | Yahoo Finance (free) |
| US equity fundamentals | FMP, Intrinio |
| Options with Greeks | Tradier, CBOE |
| Economic data | FRED |
| Cryptocurrency | Multiple crypto providers |
| High-frequency data | Polygon (paid) |

---

## Resources

- **Documentation:** https://docs.openbb.co/
- **GitHub:** https://github.com/OpenBB-finance/OpenBB
- **PyPI:** https://pypi.org/project/openbb/
- **Discord:** Community support
- **Examples:** https://github.com/OpenBB-finance/examples
