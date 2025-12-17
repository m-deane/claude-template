# OpenBB Platform - Comprehensive API Reference

**Research Date:** 2025-12-17
**Latest Version:** 4.5.0 (Released October 8, 2025)
**License:** AGPLv3
**GitHub:** https://github.com/OpenBB-finance/OpenBB (55.6k+ stars)

---

## Table of Contents

1. [Overview](#overview)
2. [Installation](#installation)
3. [Complete Module Inventory](#complete-module-inventory)
4. [Key Functions by Module](#key-functions-by-module)
5. [Data Provider Configuration](#data-provider-configuration)
6. [Core Concepts](#core-concepts)
7. [Usage Patterns](#usage-patterns)
8. [Best Practices](#best-practices)

---

## Overview

OpenBB Platform is an open-source financial data platform designed for analysts, quants, and AI agents. It operates on a "connect once, consume everywhere" model, consolidating and exposing data to:

- Python environments (for quants)
- OpenBB Workspace and Excel (for analysts)
- MCP servers (for AI agents)
- REST APIs (for applications)

**Key Features:**
- Integrates with ~100 data sources
- Multi-provider architecture with standardized interface
- Modular extension system
- Free and open source
- Comprehensive coverage: equity, options, crypto, forex, economy, fixed income, and more

---

## Installation

### Python Version Requirements

- **Minimum:** Python 3.9.21
- **Maximum:** Python 3.13
- **Recommended:** Python 3.10-3.13
- **Note:** Python 3.9 triggers deprecation warning (support ends fall 2025)

### Installation Commands

```bash
# Basic installation (core + essential providers)
pip install openbb

# Install with ALL extensions and providers
pip install openbb[all]

# Minimal installation (core only, no providers)
pip install openbb-core && pip install openbb --no-deps

# Install CLI
pip install openbb-cli

# Install from source
git clone https://github.com/OpenBB-finance/OpenBB.git
cd OpenBB
python dev_install.py -e --cli
```

### System Requirements

- **Processor:** Modern processor (5 years or less)
- **RAM:** 4GB minimum
- **OS:** Windows, Linux, macOS
- **Windows:** Microsoft Visual C++ 14.0 or greater
- **Linux:** Rust and Cargo in PATH, libwebkit2gtk-4.0-dev (Debian-based)

---

## Complete Module Inventory

### Core Routers (v4.3.3+)

| Module | Description | Sub-routers |
|--------|-------------|-------------|
| `obb.equity` | Equity/stock market data | price, fundamental, profile, compare, screener, search, news |
| `obb.crypto` | Cryptocurrency data | price, discovery |
| `obb.currency` | Forex/currency pairs | price, search |
| `obb.derivatives` | Derivatives markets | options, futures |
| `obb.economy` | Economic indicators | gdp, cpi, indicators, fred_search, fred_series |
| `obb.etf` | Exchange-traded funds | price, search, holdings, sectors |
| `obb.fixedincome` | Fixed income/bonds | rates, corporate, spreads, government |
| `obb.index` | Market indices | search, constituents, price |
| `obb.news` | Financial news | - |
| `obb.regulators` | Regulatory filings | - |
| `obb.commodity` | Commodity markets | - |
| `obb.technical` | Technical indicators | Requires: `pip install openbb-technical` |

### Utility Routers

- `obb.account` - Account management
- `obb.user` - User settings and credentials
- `obb.system` - System information
- `obb.coverage` - Data coverage information

---

## Key Functions by Module

### 1. Equity Price Functions

#### `obb.equity.price.historical()`
Get historical OHLCV price data for stocks.

```python
obb.equity.price.historical(
    symbol: str,              # Stock ticker (required)
    start_date: str = None,   # YYYY-MM-DD format
    end_date: str = None,     # YYYY-MM-DD format
    provider: str = None      # 'fmp', 'intrinio', 'polygon', 'tiingo', 'yfinance'
)

# Example
data = obb.equity.price.historical(
    symbol='AAPL',
    start_date='2020-01-01',
    provider='yfinance'
)
df = data.to_dataframe()
```

**Returns:** OBBject with DataFrame containing Open, High, Low, Close, Volume, Adj Close

#### `obb.equity.price.quote()`
Get real-time quote data.

```python
obb.equity.price.quote(
    symbol: str,              # Stock ticker (required, multiple allowed)
    provider: str = None      # 'cboe', 'fmp', 'intrinio', 'tmx', 'tradier', 'yfinance'
)

# Example
quote = obb.equity.price.quote(symbol='AAPL', provider='fmp')
```

**Returns:** Quote with open, high, low, close, volume, previous close, change, change %, 52W high/low

#### `obb.equity.price.performance()`
Price performance over different periods.

```python
obb.equity.price.performance(symbol: str, provider: str = None)
```

---

### 2. Equity Fundamental Functions

#### `obb.equity.fundamental.balance()`
Get balance sheet data.

```python
obb.equity.fundamental.balance(
    symbol: str,                        # Stock ticker (required)
    period: str = 'annual',            # 'annual' or 'quarter'
    limit: int = 5,                    # Number of periods
    provider: str = None               # 'fmp', 'intrinio', 'polygon', 'yfinance'
)

# Example
balance = obb.equity.fundamental.balance(
    'AAPL',
    period='quarter',
    provider='fmp',
    limit=4
)
```

**Returns:** Balance sheet with assets, liabilities, equity line items

#### `obb.equity.fundamental.income()`
Get income statement data.

```python
obb.equity.fundamental.income(
    symbol: str,
    period: str = 'annual',
    limit: int = 5,
    provider: str = None
)

# Example
income = obb.equity.fundamental.income('AAPL', period='annual', provider='fmp')
```

**Returns:** Income statement with revenue, expenses, net income

#### `obb.equity.fundamental.cash()`
Get cash flow statement.

```python
obb.equity.fundamental.cash(
    symbol: str,
    period: str = 'annual',
    limit: int = 5,
    provider: str = None
)

# Example
cash = obb.equity.fundamental.cash('AAPL', provider='intrinio')
df = cash.to_df().transpose()
```

**Returns:** Cash flow statement with operating, investing, financing activities

#### `obb.equity.fundamental.metrics()`
Get key financial metrics and ratios.

```python
obb.equity.fundamental.metrics(
    symbol: str,
    period: str = None,        # 'annual', 'quarter', 'ttm'
    limit: int = None,
    provider: str = None
)

# Example
metrics = obb.equity.fundamental.metrics('AAPL', provider='fmp')
```

**Returns comprehensive metrics:**
- Valuation: market_cap, pe_ratio, forward_pe, peg_ratio, price_to_book, price_to_sales
- Profitability: gross_margin, ebit_margin, profit_margin, roe, roa, roic
- Liquidity: quick_ratio, current_ratio, debt_to_equity
- Growth: eps_growth, revenue_growth, ebitda_growth
- Other: dividend_yield, beta, free_cash_flow_yield, altman_z_score

#### `obb.equity.fundamental.ratios()`
Get detailed financial ratios over time.

```python
obb.equity.fundamental.ratios(
    symbol: str,
    period: str = None,
    limit: int = None,
    provider: str = None
)
```

**Returns 30+ ratios including:**
- **Liquidity:** current_ratio, quick_ratio, cash_ratio, cash_conversion_cycle
- **Efficiency:** inventory_turnover, asset_turnover, receivables_turnover
- **Profitability:** gross_profit_margin, operating_profit_margin, net_profit_margin
- **Leverage:** debt_ratio, debt_to_equity, interest_coverage
- **Valuation:** price_to_earnings, price_to_book, enterprise_value_multiple

#### `obb.equity.fundamental.dividends()`
Get historical dividend data.

```python
obb.equity.fundamental.dividends(
    symbol: str,
    provider: str = None       # 'fmp', 'intrinio', 'nasdaq', 'tmx', 'yfinance'
)

# Example
dividends = obb.equity.fundamental.dividends(symbol='AAPL', provider='intrinio')
```

#### Complete List of Fundamental Functions

All available functions under `obb.equity.fundamental.*`:

- `balance` - Balance sheet
- `balance_growth` - Balance sheet growth metrics
- `cash` - Cash flow statement
- `cash_growth` - Cash flow growth metrics
- `dividends` - Historical dividends
- `employee_count` - Employee headcount over time
- `filings` - SEC filings
- `historical_attributes` - Historical fundamental attributes
- `historical_eps` - Historical earnings per share
- `historical_splits` - Stock split history
- `income` - Income statement
- `income_growth` - Income statement growth metrics
- `latest_attributes` - Latest fundamental attributes
- `management` - Management team information
- `management_compensation` - Executive compensation
- `metrics` - Key financial metrics
- `multiples` - Valuation multiples
- `overview` - Company overview
- `ratios` - Financial ratios
- `reported_financials` - As-reported financials
- `revenue_per_geography` - Revenue breakdown by geography
- `revenue_per_segment` - Revenue breakdown by segment
- `search_attributes` - Search fundamental data points
- `trailing_dividend_yield` - Trailing dividend yield
- `transcript` - Earnings call transcripts

---

### 3. Equity Profile & Discovery

#### `obb.equity.profile()`
Get company profile information.

```python
obb.equity.profile(
    symbol: str,
    provider: str = None       # 'finviz', 'fmp', 'intrinio', 'tmx', 'yfinance'
)

# Example
profile = obb.equity.profile(symbol='AAPL', provider='fmp')
```

**Returns:** Company description, sector, industry, executives, website, address, contact info

#### `obb.equity.compare.company_facts()`
Compare fundamental data across companies.

```python
obb.equity.compare.company_facts(
    symbol: str = None,        # Multiple symbols allowed
    fact: str,                 # Fact to compare (required)
    year: int = None,
    provider: str = 'sec'
)

# Example - Compare revenue across tech giants
obb.equity.compare.company_facts(
    symbol='NVDA,AAPL,AMZN,MSFT,GOOG',
    fact='RevenueFromContractWithCustomerExcludingAssessedTax',
    year=2024,
    provider='sec'
)
```

---

### 4. Derivatives - Options Functions

#### `obb.derivatives.options.chains()`
Get options chains with Greeks and implied volatility.

```python
obb.derivatives.options.chains(
    symbol: str,               # Stock ticker (required)
    date: str = None,          # Expiration date filter
    provider: str = None
)

# Example
options = obb.derivatives.options.chains('AAPL')
```

**Returns comprehensive options data:**
- Contract details: contract_symbol, expiration, strike, option_type (call/put)
- Pricing: last_price, bid, ask
- Volume data: volume, open_interest
- Volatility: implied_volatility, orats_final_iv (updated hourly)
- Greeks: delta, gamma, theta, vega, rho, phi, charm, vanna, vomma
- Timestamps: last_trade_timestamp, greeks_timestamp

#### `obb.derivatives.options.unusual()`
Get unusual options activity.

```python
obb.derivatives.options.unusual(symbol: str = None, provider: str = None)
```

---

### 5. Derivatives - Futures Functions

#### `obb.derivatives.futures.instruments()`
Get reference data for futures instruments.

```python
obb.derivatives.futures.instruments(symbol: str = None, provider: str = None)
```

#### `obb.derivatives.futures.historical()`
Get historical futures price data.

```python
obb.derivatives.futures.historical(
    symbol: str,
    start_date: str = None,
    end_date: str = None,
    provider: str = None
)

# Example
futures_data = obb.derivatives.futures.historical('ES')
```

#### `obb.derivatives.futures.curve()`
Get futures curve (term structure).

```python
obb.derivatives.futures.curve(symbol: str, provider: str = None)

# Example - Crude oil futures curve
curve = obb.derivatives.futures.curve('CL')
```

---

### 6. Economy Functions

#### `obb.economy.gdp.real()`
Get real GDP data by country.

```python
obb.economy.gdp.real(
    country: str = None,       # Multiple countries allowed
    start_date: str = None,    # YYYY-MM-DD
    end_date: str = None,
    provider: str = None       # 'oecd', 'econdb', 'fred'
)

# Example
gdp = obb.economy.gdp.real(
    country='united_states,germany,japan',
    provider='econdb'
)
```

**Returns:** Country, date, real GDP value, growth_rate_qoq, growth_rate_yoy

#### `obb.economy.cpi()`
Get Consumer Price Index data.

```python
obb.economy.cpi(
    country: str = None,       # Multiple countries allowed
    transform: str = 'yoy',    # 'period', 'yoy', 'mom'
    start_date: str = None,
    end_date: str = None,
    provider: str = None       # 'fred', 'oecd'
)

# Example
cpi = obb.economy.cpi(
    country='united_states',
    transform='yoy',
    provider='fred'
)
```

**Transform options:**
- `period` - Change since previous period
- `yoy` - Year over year (default)
- `mom` - Month over month

#### `obb.economy.indicators()`
Get economic indicators by country and type.

```python
obb.economy.indicators(
    symbol: str = None,        # Indicator symbol (e.g., 'CPI', 'PCOCO')
    country: str = None,       # Multiple countries allowed
    start_date: str = None,
    end_date: str = None,
    provider: str = 'econdb'
)

# Example
indicators = obb.economy.indicators(
    symbol='CPI',
    country='united_states,jp',
    provider='econdb'
)
```

#### `obb.economy.fred_search()`
Search FRED database for series IDs.

```python
obb.economy.fred_search(
    query: str,                # Search query (required)
    provider: str = 'fred'
)

# Example
search_results = obb.economy.fred_search('treasury yield')
```

#### `obb.economy.fred_series()`
Get data for a specific FRED series.

```python
obb.economy.fred_series(
    series_id: str,            # FRED series ID (required)
    start_date: str = None,
    end_date: str = None,
    provider: str = 'fred'
)

# Example - 10-Year Treasury Rate
treasury = obb.economy.fred_series('DGS10')
```

#### `obb.economy.unemployment()`
Get unemployment rate data.

```python
obb.economy.unemployment(
    country: str = None,
    start_date: str = None,
    end_date: str = None,
    provider: str = None
)
```

---

### 7. Fixed Income Functions

#### `obb.fixedincome.government.treasury_rates()`
Get US Treasury rates.

```python
obb.fixedincome.government.treasury_rates(
    start_date: str = None,
    end_date: str = None,
    provider: str = None
)

# Example
treasury_curve = obb.fixedincome.government.treasury_rates()
```

**Returns:** Yield curve data by maturity (constant maturity or inflation protected)

#### `obb.fixedincome.corporate.bonds()`
Get corporate bond data.

```python
obb.fixedincome.corporate.bonds(provider: str = None)
```

#### `obb.fixedincome.spreads()`
Get bond spread data.

```python
obb.fixedincome.spreads(provider: str = None)
```

**Returns:** Credit spreads and yield differentials

---

### 8. Crypto Functions

#### `obb.crypto.price.historical()`
Get historical cryptocurrency price data.

```python
obb.crypto.price.historical(
    symbol: str,               # 'BTC', 'ETH', etc. (required)
    start_date: str = None,
    end_date: str = None,
    provider: str = None
)

# Example
btc = obb.crypto.price.historical('BTC')
```

#### Crypto Discovery Functions

```python
# Top gaining cryptocurrencies
obb.crypto.discovery.top_gainers(provider=None)

# Top losing cryptocurrencies
obb.crypto.discovery.top_losers(provider=None)

# Trending cryptocurrencies
obb.crypto.discovery.trending(provider=None)

# Top by market capitalization
obb.crypto.discovery.top_by_market_cap(provider=None)
```

---

### 9. Currency (Forex) Functions

#### `obb.currency.search()`
Search for currency pairs.

```python
obb.currency.search(query: str = None, provider: str = None)
```

#### `obb.currency.price.historical()`
Get historical forex price data.

```python
obb.currency.price.historical(
    symbol: str,               # 'EURUSD', etc. (required)
    start_date: str = None,
    end_date: str = None,
    provider: str = None
)

# Example
eurusd = obb.currency.price.historical('EURUSD')
```

---

### 10. ETF Functions

#### `obb.etf.search()`
Search for ETFs.

```python
obb.etf.search(query: str = None, provider: str = None)

# Example
tech_etfs = obb.etf.search('technology')
```

#### `obb.etf.price.historical()`
Get historical ETF price data.

```python
obb.etf.price.historical(
    symbol: str,
    start_date: str = None,
    end_date: str = None,
    provider: str = None
)

# Example
spy = obb.etf.price.historical('SPY')
```

#### `obb.etf.holdings()`
Get ETF holdings/constituents.

```python
obb.etf.holdings(symbol: str, provider: str = None)

# Example
spy_holdings = obb.etf.holdings('SPY')
```

#### `obb.etf.sectors()`
Get ETF sector weights.

```python
obb.etf.sectors(symbol: str, provider: str = None)

# Example
spy_sectors = obb.etf.sectors('SPY')
```

---

### 11. Technical Analysis Functions

**Note:** Requires installation of `openbb-technical` extension:
```bash
pip install openbb-technical
```

#### `obb.technical.rsi()`
Calculate Relative Strength Index.

```python
obb.technical.rsi(
    data,                      # DataFrame or OBBject (required)
    target: str = 'close',     # Column to calculate on
    length: int = 14           # RSI period
)

# Example
historical = obb.equity.price.historical('AAPL', provider='yfinance')
rsi = obb.technical.rsi(data=historical.results, length=14)
```

#### `obb.technical.macd()`
Calculate Moving Average Convergence Divergence.

```python
obb.technical.macd(
    data,
    target: str = 'close',
    fast: int = 12,            # Fast EMA period
    slow: int = 26,            # Slow EMA period
    signal: int = 9            # Signal line period
)

# Example
macd = obb.technical.macd(data=historical.results, fast=12, slow=26, signal=9)
```

#### `obb.technical.sma()`
Calculate Simple Moving Average.

```python
obb.technical.sma(
    data,
    target: str = 'close',
    length: int = 50           # SMA period
)

# Example
sma = obb.technical.sma(data=historical.results, length=50)
```

#### `obb.technical.ema()`
Calculate Exponential Moving Average.

```python
obb.technical.ema(
    data,
    target: str = 'close',
    length: int = 50           # EMA period
)

# Example
ema = obb.technical.ema(data=historical.results, length=20)
```

#### `obb.technical.bbands()`
Calculate Bollinger Bands.

```python
obb.technical.bbands(
    data,
    target: str = 'close',
    length: int = 20,          # Period for moving average
    std: float = 2.0           # Number of standard deviations
)

# Example
bbands = obb.technical.bbands(data=historical.results, length=20, std=2)
```

**Returns:** Upper band, middle band (SMA), lower band

#### Complete Technical Indicators List

All available indicators in `openbb-technical`:

- `ad` - Accumulation/Distribution
- `adosc` - Accumulation/Distribution Oscillator
- `adx` - Average Directional Index
- `aroon` - Aroon Indicator
- `atr` - Average True Range
- `bbands` - Bollinger Bands
- `cci` - Commodity Channel Index
- `cg` - Center of Gravity
- `clenow` - Clenow Volatility
- `cones` - Volatility Cones
- `demark` - Demark Indicators
- `donchian` - Donchian Channels
- `ema` - Exponential Moving Average
- `fib` - Fibonacci Levels
- `fisher` - Fisher Transform
- `hma` - Hull Moving Average
- `ichimoku` - Ichimoku Cloud
- `kc` - Keltner Channel
- `macd` - Moving Average Convergence Divergence
- `obv` - On Balance Volume
- `rsi` - Relative Strength Index
- `sma` - Simple Moving Average
- `stoch` - Stochastic Oscillator
- `vwap` - Volume Weighted Average Price
- `wma` - Weighted Moving Average
- `zlma` - Zero Lag Moving Average

---

## Data Provider Configuration

### Overview

OpenBB uses a multi-provider architecture where each data source is a separate extension. Users configure API keys and set provider priority.

### Configuration Methods

#### 1. Configuration File Method

Location: `~/.openbb_platform/user_settings.json`

```json
{
  "credentials": {
    "fmp_api_key": "YOUR_FMP_KEY",
    "polygon_api_key": "YOUR_POLYGON_KEY",
    "benzinga_api_key": "YOUR_BENZINGA_KEY",
    "fred_api_key": "YOUR_FRED_KEY",
    "nasdaq_api_key": "YOUR_NASDAQ_KEY",
    "intrinio_api_key": "YOUR_INTRINIO_KEY",
    "alpha_vantage_api_key": "YOUR_AV_KEY",
    "biztoc_api_key": "YOUR_BIZTOC_KEY",
    "tradier_api_key": "YOUR_TRADIER_KEY",
    "tradingeconomics_api_key": "YOUR_TE_KEY",
    "tiingo_token": "YOUR_TIINGO_KEY"
  }
}
```

#### 2. Python Session Method (Current Session Only)

```python
from openbb import obb

# Set API key for current session
obb.user.credentials.intrinio_api_key = "my_api_key"
obb.user.credentials.fred_api_key = "my_fred_key"
```

#### 3. Python with Save

```python
from openbb import obb

# Set and save API key permanently
obb.user.credentials.fred_api_key = "YOUR_KEY"
obb.account.save()  # Writes to user_settings.json
```

#### 4. OpenBB Hub (Cloud Sync)

1. Login to OpenBB Hub at https://my.openbb.co
2. Navigate to API Keys section
3. Add your API keys
4. Generate Personal Access Token (PAT)
5. Login from Python:

```python
from openbb import obb
obb.account.login(pat="YOUR_PAT_TOKEN")
```

### Available Data Providers

| Provider | Extension | API Key Required | Cost | Data Types |
|----------|-----------|------------------|------|------------|
| Yahoo Finance | `openbb-yfinance` | No | Free | Equity, ETF, Crypto, Forex |
| FMP | `openbb-fmp` | Yes | Free tier + Paid | Equity, Crypto, Forex, Fundamentals |
| Polygon.io | `openbb-polygon` | Yes | Free tier + Paid | Equity, Options, Crypto, Forex |
| FRED | `openbb-fred` | Yes | Free | Economy, Rates |
| Intrinio | `openbb-intrinio` | Yes | Paid | Equity, Fundamentals, Options |
| SEC | `openbb-sec` | No | Free | Filings, Fundamentals |
| Tiingo | `openbb-tiingo` | Yes | Free tier + Paid | Equity, Crypto, Forex |
| Alpha Vantage | `openbb-alphavantage` | Yes | Free tier + Paid | Equity, Crypto, Forex, Technical |
| OECD | `openbb-oecd` | No | Free | Economy |
| Benzinga | `openbb-benzinga` | Yes | Paid | News, Earnings |
| Tradier | `openbb-tradier` | Yes | Free sandbox + Paid | Equity, Options |
| Trading Economics | `openbb-tradingeconomics` | Yes | Paid | Economy |
| CBOE | `openbb-cboe` | No | Free | Options, Volatility |
| Finviz | `openbb-finviz` | No | Free | Equity, Screener |
| TMX | `openbb-tmx` | No | Free | Canadian Equity |

### Installing Provider Extensions

```bash
# Install individual provider
pip install openbb-fmp
pip install openbb-polygon
pip install openbb-yfinance

# Install all providers at once
pip install openbb[all]
```

### Obtaining API Keys

**FRED (Free):**
- URL: https://fred.stlouisfed.org/docs/api/api_key.html
- Process: Free registration, instant API key

**FMP (Free tier available):**
- URL: https://site.financialmodelingprep.com/developer/docs
- Process: Free tier with registration, paid tiers available

**Polygon (Free tier available):**
- URL: https://polygon.io/
- Process: Free tier with registration, paid tiers for more features

**Alpha Vantage (Free tier available):**
- URL: https://www.alphavantage.co/support/#api-key
- Process: Free registration, instant API key

**Intrinio (Paid):**
- URL: https://intrinio.com/
- Process: Contact sales for pricing

### Provider Priority

When the `provider` parameter is omitted, OpenBB uses a configured priority list.

**Example:**
- For CPI data: FRED (if API key configured) → OECD (fallback)

**Configuration:** Set in `user_settings.json` or via `obb.user.preferences`

---

## Core Concepts

### 1. The OBB Interface

The main entry point for all OpenBB Platform functionality.

```python
# Correct import
from openbb import obb

# DO NOT use (unsupported)
# from openbb.obb.equity import *
```

### 2. OBBject Return Type

OpenBB functions return an `OBBject` - a custom object that wraps data and metadata.

#### OBBject Methods

```python
output = obb.equity.price.historical('AAPL')

# Convert to pandas DataFrame
df = output.to_dataframe()
df = output.to_df()  # Shorthand

# Convert to other formats
dict_data = output.to_dict()
json_data = output.to_json()

# Display chart (requires openbb-charting)
output.chart()

# Display data
output.show()
```

#### OBBject Properties

```python
# Access raw data
data = output.results

# Check which provider was used
provider = output.provider

# Check for warnings
warnings = output.warnings

# Access chart object
chart = output.chart

# Access additional metadata
extra = output.extra
```

### 3. Multi-Provider Architecture

Key characteristics:

- OpenBB does not store data - it aggregates from providers
- Standardized interface across providers
- Automatic fallback to available providers
- Provider-specific fields may vary
- Some providers require API keys, others don't
- Can specify provider explicitly or use priority list

### 4. Extensions System

#### Data Extensions
Add new data sources/providers.
```bash
pip install openbb-fmp
pip install openbb-polygon
```

#### Router Extensions
Add new functionality domains.
```bash
pip install openbb-equity
pip install openbb-crypto
```

#### Toolkit Extensions
Add specialized analysis capabilities.
```bash
pip install openbb-technical
pip install openbb-econometrics
pip install openbb-quantitative
```

#### Charting Extension
Add interactive Plotly charting.
```bash
pip install openbb-charting

# Usage
output = obb.equity.price.historical('AAPL')
output.chart()
```

### 5. REST API

OpenBB Platform includes a FastAPI-based REST API.

```bash
# Start API server
uvicorn openbb_core.api.rest_api:app --host 0.0.0.0 --port 8000 --reload

# Alternative
openbb-api

# Default URLs
# API: http://127.0.0.1:6900
# Docs: http://127.0.0.1:6900/docs
```

**Features:**
- Access all OpenBB functionality via HTTP
- Automatic OpenAPI documentation
- Use from any programming language
- Authentication with PAT tokens

### 6. CLI

Command-line interface for OpenBB Platform.

```bash
# Install
pip install openbb-cli

# Features:
# - Terminal-based interface
# - Interactive commands
# - Script automation support
# - Access to all data providers
```

### 7. Workspace

Enterprise UI for OpenBB Platform.

- **URL:** https://pro.openbb.co
- **Features:** Web-based interface, dashboards, collaborative workspace, Excel integration

---

## Usage Patterns

### Basic Workflow

```python
# Step 1: Import OpenBB
from openbb import obb

# Step 2: Fetch data
output = obb.equity.price.historical('AAPL', start_date='2020-01-01')

# Step 3: Convert to DataFrame
df = output.to_dataframe()

# Step 4: Analyze or visualize
print(df.head())
print(df.describe())
```

### Specifying Providers

```python
# Explicit provider
obb.equity.price.historical('AAPL', provider='yfinance')

# Priority list (set in user_settings.json or via obb.user.preferences)
obb.equity.price.historical('AAPL')  # Uses priority list
```

### Exploring Available Commands

```python
# Method 1: Use IDE IntelliSense
# Type 'obb.equity.' and see suggestions

# Method 2: Use help()
help(obb.equity.price.historical)

# Method 3: Use question mark (in Jupyter/IPython)
obb.equity.price.historical?

# Method 4: Check documentation
# Visit docs.openbb.co
```

### Working with Data

```python
# Convert to DataFrame
df = output.to_dataframe()

# Access raw results
data = output.results

# Transpose for better viewing
df.transpose()

# Filter columns
df[['open', 'high', 'low', 'close']]

# Date filtering
df.loc['2023-01-01':'2023-12-31']

# Calculate returns
df['returns'] = df['close'].pct_change()

# Statistical summary
df.describe()
```

### Chaining Operations

Fetch data then apply technical analysis.

```python
# Get historical data
data = obb.equity.price.historical('AAPL', provider='yfinance')

# Apply technical indicators
rsi = obb.technical.rsi(data.results, length=14)
macd = obb.technical.macd(data.results, fast=12, slow=26, signal=9)
sma_50 = obb.technical.sma(data.results, length=50)
```

### Error Handling

```python
try:
    output = obb.equity.price.historical('AAPL', provider='fmp')

    # Check for warnings
    if output.warnings:
        print("Warnings:", output.warnings)

    df = output.to_dataframe()

except Exception as e:
    print(f"Error: {e}")
    # Fallback to different provider
    output = obb.equity.price.historical('AAPL', provider='yfinance')
```

### Common Patterns

#### Get Multiple Stocks

```python
symbols = ['AAPL', 'GOOGL', 'MSFT']
data = {}

for symbol in symbols:
    data[symbol] = obb.equity.price.historical(symbol).to_dataframe()
```

#### Compare Fundamentals

```python
# Get metrics for multiple companies
companies = ['AAPL', 'MSFT', 'GOOGL']
metrics = {}

for company in companies:
    metrics[company] = obb.equity.fundamental.metrics(company).to_dict()
```

#### Economic Data Dashboard

```python
# Fetch multiple economic indicators
gdp = obb.economy.gdp.real(country='united_states').to_dataframe()
cpi = obb.economy.cpi(country='united_states').to_dataframe()
unemployment = obb.economy.unemployment(country='united_states').to_dataframe()
```

---

## Best Practices

### 1. Configuration

- Always specify provider explicitly for production applications
- Configure multiple providers as fallbacks
- Use paid tiers for critical applications requiring reliability
- Store API keys securely (use environment variables in production)

### 2. Data Fetching

- Cache frequently accessed data to minimize API calls
- Implement error handling and retries
- Check `output.warnings` for potential issues
- Be mindful of provider rate limits

### 3. Development

- Use virtual environments to manage dependencies
- Keep extensions updated: `pip install --upgrade openbb`
- Consult provider documentation for data update frequencies
- Use OBBject methods for data conversion rather than manual parsing

### 4. Performance

- API calls are synchronous by default
- Large historical datasets can be memory-intensive
- Consider pagination for large result sets
- Provider response times vary significantly

### 5. Production Deployment

- Use configuration files for API keys (not hardcoded)
- Implement retry logic for network failures
- Monitor API usage to avoid rate limits
- Log provider usage for debugging
- Consider using OpenBB REST API for multi-language support

### 6. Common Pitfalls to Avoid

| Issue | Symptom | Solution |
|-------|---------|----------|
| API key not configured | Function not available or error | Configure key in user_settings.json |
| Rate limits exceeded | Requests fail after multiple calls | Use paid tier or throttle requests |
| Symbol not found | No data returned or error | Use search functions for correct symbol |
| Missing extension | Module/function not available | Install extension: `pip install openbb-{extension}` |
| Provider-specific fields | Expected fields missing | Check docs for provider-specific fields, try different provider |
| Data quality issues | Inconsistent/missing data | Try alternative providers, paid tiers have better quality |

---

## Implementation Recommendations

### Use Case: Stock Analysis Dashboard

**Solution:** Use `obb.equity.price.historical()` for price data, `obb.equity.fundamental.*` for financials, `obb.technical.*` for indicators

**Rationale:** Comprehensive data coverage with flexible provider options

```python
# Price data
prices = obb.equity.price.historical('AAPL', start_date='2023-01-01')

# Fundamentals
metrics = obb.equity.fundamental.metrics('AAPL')
ratios = obb.equity.fundamental.ratios('AAPL')

# Technical indicators
rsi = obb.technical.rsi(prices.results)
macd = obb.technical.macd(prices.results)
```

### Use Case: Economic Data Analysis

**Solution:** Use `obb.economy.*` functions with FRED provider for US data, OECD for international

**Rationale:** FRED is authoritative source for US economic data with free API

```python
# US economic indicators
gdp = obb.economy.gdp.real(country='united_states', provider='fred')
cpi = obb.economy.cpi(country='united_states', provider='fred')
unemployment = obb.economy.unemployment(country='united_states')
```

### Use Case: Options Trading Analysis

**Solution:** Use `obb.derivatives.options.chains()` with Tradier or paid providers

**Rationale:** Options data requires reliable providers with Greeks calculations

```python
# Get full options chain
options = obb.derivatives.options.chains('AAPL', provider='tradier')
df = options.to_dataframe()

# Filter by expiration
chain = df[df['expiration'] == '2024-12-20']

# Analyze Greeks
high_delta_calls = chain[(chain['option_type'] == 'call') & (chain['delta'] > 0.7)]
```

### Use Case: Cryptocurrency Portfolio Tracking

**Solution:** Use `obb.crypto.price.historical()` and `obb.crypto.discovery.*` functions

**Rationale:** Built-in crypto support with multiple provider options

```python
# Get crypto prices
btc = obb.crypto.price.historical('BTC')
eth = obb.crypto.price.historical('ETH')

# Discovery
top_gainers = obb.crypto.discovery.top_gainers()
trending = obb.crypto.discovery.trending()
```

### Use Case: Fundamental Screening

**Solution:** Use `obb.equity.fundamental.metrics()` and `obb.equity.fundamental.ratios()` with FMP provider

**Rationale:** FMP provides comprehensive fundamental data with good free tier

```python
# Screen multiple stocks
stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
results = []

for stock in stocks:
    metrics = obb.equity.fundamental.metrics(stock, provider='fmp')
    results.append(metrics.to_dict())

# Filter by criteria (e.g., PE < 20, ROE > 15%)
```

### Use Case: Multi-Language Application

**Solution:** Use OpenBB REST API with `openbb-api` command

**Rationale:** Language-agnostic HTTP interface with automatic documentation

```bash
# Start API server
openbb-api

# Access from any language via HTTP
# GET http://127.0.0.1:6900/api/v1/equity/price/historical?symbol=AAPL
```

---

## Community Resources

- **Documentation:** https://docs.openbb.co/
- **GitHub:** https://github.com/OpenBB-finance/OpenBB
- **Discord:** Community server (link on GitHub)
- **Examples:** https://github.com/OpenBB-finance/examples
- **Blog:** https://openbb.co/blog
- **YouTube:** OpenBB tutorials and examples

---

## Alternative Implementations

| Library | Comparison | Use Case |
|---------|------------|----------|
| yfinance | Single provider (Yahoo), simpler but less flexible | Quick prototyping |
| pandas-datareader | Multiple providers but less maintained | Legacy projects |
| alpaca-py | Trading-focused, requires broker account | Algorithmic trading |
| QuantLib | Quantitative finance library, no data fetching | Derivatives pricing |

---

## Future Developments

**Trends:**
- Expanding AI/LLM integrations (MCP servers)
- More data providers being added
- Enhanced charting capabilities
- Improved Excel integration
- Real-time data streaming support

**Deprecation Notices:**
- Python 3.9 support ending fall 2025
- Legacy SDK (OpenBB Terminal SDK) deprecated in favor of OpenBB Platform

---

## Citations

1. OpenBB Documentation. "OpenBB Docs." https://docs.openbb.co/
2. PyPI. "openbb - PyPI." https://pypi.org/project/openbb/
3. OpenBB Documentation. "Introduction | OpenBB Docs." https://docs.openbb.co/python
4. GitHub. "Releases - OpenBB-finance/OpenBB." https://github.com/OpenBB-finance/OpenBB/releases
5. OpenBB Documentation. "Platform | OpenBB." https://openbb.co/products/platform
6. AlgoTrading101. "OpenBB Platform - A Complete Guide." https://algotrading101.com/learn/openbb-platform-guide/
7. OpenBB Documentation. "Installation | OpenBB Docs." https://docs.openbb.co/python/installation
8. OpenBB Documentation. "Authorization and API Keys | OpenBB Docs." https://docs.openbb.co/platform/getting_started/api_keys
9. OpenBB Documentation. "equity/price/quote - Reference." https://docs.openbb.co/platform/reference/equity/price/quote
10. OpenBB Documentation. "equity/fundamental/metrics - Reference." https://docs.openbb.co/platform/reference/equity/fundamental/metrics
11. OpenBB Documentation. "derivatives/options/chains - Reference." https://docs.openbb.co/platform/reference/derivatives/options/chains
12. OpenBB Documentation. "economy/cpi - Reference." https://docs.openbb.co/platform/reference/economy/cpi
13. OpenBB Documentation. "Technical | OpenBB Docs." https://docs.openbb.co/platform/reference/technical
14. GitHub. "examples/newOBB.py - OpenBB-finance/examples." https://github.com/OpenBB-finance/examples/blob/main/newOBB.py
15. OpenBB Documentation. "Data Extensions | OpenBB Docs." https://docs.openbb.co/platform/usage/extensions/data_extensions

---

**Research completed by:** Technical Researcher Agent
**Date:** 2025-12-17
**Document Version:** 1.0
