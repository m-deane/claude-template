# OpenBB Platform - Quick Reference Guide

**Version:** 4.5.0 | **Date:** 2025-12-17

## Installation

```bash
pip install openbb                    # Basic
pip install openbb[all]              # All extensions
pip install openbb-technical         # Technical analysis
pip install openbb-cli               # Command-line interface
```

## Setup

```python
from openbb import obb

# Configure API keys (one-time)
obb.user.credentials.fred_api_key = "YOUR_KEY"
obb.user.credentials.fmp_api_key = "YOUR_KEY"
obb.account.save()
```

## Common Patterns

### Get Stock Price Data

```python
# Historical prices
data = obb.equity.price.historical('AAPL', start_date='2023-01-01')
df = data.to_dataframe()

# Latest quote
quote = obb.equity.price.quote('AAPL', provider='fmp')

# Performance metrics
perf = obb.equity.price.performance('AAPL')
```

### Fundamental Analysis

```python
# Financial statements
balance = obb.equity.fundamental.balance('AAPL', period='quarter', limit=4)
income = obb.equity.fundamental.income('AAPL', period='annual')
cash = obb.equity.fundamental.cash('AAPL')

# Key metrics & ratios
metrics = obb.equity.fundamental.metrics('AAPL')
ratios = obb.equity.fundamental.ratios('AAPL')

# Dividends
divs = obb.equity.fundamental.dividends('AAPL')

# Company profile
profile = obb.equity.profile('AAPL', provider='fmp')
```

### Options Data

```python
# Full options chain with Greeks
options = obb.derivatives.options.chains('AAPL')
df = options.to_dataframe()

# Unusual activity
unusual = obb.derivatives.options.unusual()
```

### Economic Data

```python
# GDP
gdp = obb.economy.gdp.real(country='united_states')

# CPI (inflation)
cpi = obb.economy.cpi(country='united_states', transform='yoy')

# Search FRED database
search = obb.economy.fred_search('unemployment')

# Get FRED series
data = obb.economy.fred_series('DGS10')  # 10-year Treasury
```

### Technical Analysis

```python
# Get price data first
prices = obb.equity.price.historical('AAPL')

# Calculate indicators
rsi = obb.technical.rsi(prices.results, length=14)
macd = obb.technical.macd(prices.results, fast=12, slow=26, signal=9)
sma = obb.technical.sma(prices.results, length=50)
ema = obb.technical.ema(prices.results, length=20)
bbands = obb.technical.bbands(prices.results, length=20, std=2)
```

### Crypto

```python
# Historical crypto prices
btc = obb.crypto.price.historical('BTC')

# Discovery
top_gainers = obb.crypto.discovery.top_gainers()
trending = obb.crypto.discovery.trending()
market_cap = obb.crypto.discovery.top_by_market_cap()
```

### Forex

```python
# Search currency pairs
pairs = obb.currency.search()

# Historical forex data
eurusd = obb.currency.price.historical('EURUSD')
```

### ETFs

```python
# Search ETFs
tech_etfs = obb.etf.search('technology')

# ETF prices
spy = obb.etf.price.historical('SPY')

# Holdings
holdings = obb.etf.holdings('SPY')

# Sector weights
sectors = obb.etf.sectors('SPY')
```

### Fixed Income

```python
# Treasury rates
treasury = obb.fixedincome.government.treasury_rates()

# Corporate bonds
corp_bonds = obb.fixedincome.corporate.bonds()

# Spreads
spreads = obb.fixedincome.spreads()
```

## OBBject Methods

```python
output = obb.equity.price.historical('AAPL')

# Data conversion
df = output.to_dataframe()         # Convert to DataFrame
data = output.results              # Access raw data
dict_data = output.to_dict()       # Convert to dict
json_data = output.to_json()       # Convert to JSON

# Metadata
provider = output.provider         # Which provider was used
warnings = output.warnings         # Any warnings

# Visualization (requires openbb-charting)
output.chart()                     # Display interactive chart
```

## Module Structure

```
obb.equity                    # Stocks
  ├── price                   # Prices & quotes
  ├── fundamental             # Financial statements, metrics, ratios
  ├── profile                 # Company information
  ├── compare                 # Compare companies
  └── screener                # Stock screening

obb.crypto                    # Cryptocurrency
  ├── price                   # Crypto prices
  └── discovery               # Top gainers, losers, trending

obb.currency                  # Forex
  └── price                   # Currency pair prices

obb.derivatives               # Options & futures
  ├── options                 # Options chains, unusual activity
  └── futures                 # Futures data

obb.economy                   # Economic indicators
  ├── gdp                     # GDP data
  ├── cpi                     # Inflation data
  ├── indicators              # Various indicators
  ├── fred_search             # Search FRED database
  └── fred_series             # FRED time series

obb.etf                       # ETFs
  └── price                   # ETF prices

obb.fixedincome               # Bonds
  ├── government              # Government bonds
  ├── corporate               # Corporate bonds
  └── spreads                 # Credit spreads

obb.index                     # Market indices

obb.technical                 # Technical indicators (requires extension)
```

## Key Providers

| Provider | Free | API Key | Best For |
|----------|------|---------|----------|
| yfinance | Yes | No | Quick prototyping, stock prices |
| FMP | Tier | Yes | Comprehensive fundamentals |
| Polygon | Tier | Yes | High-quality market data |
| FRED | Yes | Yes | Economic data |
| SEC | Yes | No | Official filings |
| Intrinio | No | Yes | Professional-grade data |
| Alpha Vantage | Tier | Yes | Beginners, basic data |

## API Key Configuration

### Option 1: Configuration File

Edit `~/.openbb_platform/user_settings.json`:

```json
{
  "credentials": {
    "fmp_api_key": "YOUR_KEY",
    "polygon_api_key": "YOUR_KEY",
    "fred_api_key": "YOUR_KEY",
    "intrinio_api_key": "YOUR_KEY",
    "alpha_vantage_api_key": "YOUR_KEY"
  }
}
```

### Option 2: Python Code

```python
from openbb import obb

# Set and save
obb.user.credentials.fred_api_key = "YOUR_KEY"
obb.user.credentials.fmp_api_key = "YOUR_KEY"
obb.account.save()
```

### Option 3: OpenBB Hub

```python
# Login with Personal Access Token
obb.account.login(pat="YOUR_PAT_TOKEN")
```

## Common Patterns

### Multiple Stocks

```python
symbols = ['AAPL', 'MSFT', 'GOOGL']
data = {s: obb.equity.price.historical(s).to_dataframe() for s in symbols}
```

### Error Handling

```python
try:
    output = obb.equity.price.historical('AAPL', provider='fmp')
    if output.warnings:
        print("Warnings:", output.warnings)
    df = output.to_dataframe()
except Exception as e:
    print(f"Error: {e}")
    # Fallback to different provider
    output = obb.equity.price.historical('AAPL', provider='yfinance')
```

### Chaining Operations

```python
# Get data, calculate indicator
prices = obb.equity.price.historical('AAPL')
rsi = obb.technical.rsi(prices.results, length=14)
```

## Provider Selection

```python
# Explicit provider
obb.equity.price.historical('AAPL', provider='yfinance')

# Auto-select from priority list (configured in settings)
obb.equity.price.historical('AAPL')
```

## REST API

```bash
# Start API server
openbb-api

# Or manually
uvicorn openbb_core.api.rest_api:app --port 8000

# Access at: http://127.0.0.1:6900
# Documentation: http://127.0.0.1:6900/docs
```

## Useful Commands

```bash
# Update OpenBB
pip install --upgrade openbb

# Install specific extension
pip install openbb-technical
pip install openbb-charting

# Install CLI
pip install openbb-cli
```

## Tips

1. Always convert OBBject to DataFrame: `df = output.to_dataframe()`
2. Check warnings: `output.warnings`
3. Specify provider explicitly for production
4. Cache frequently accessed data
5. Use `help(function)` or `function?` to see documentation
6. Check provider-specific fields in documentation
7. Use paid tiers for critical applications

## Common Issues

| Issue | Solution |
|-------|----------|
| Function not found | Install extension: `pip install openbb-{extension}` |
| API key error | Configure in `user_settings.json` or via `obb.user.credentials` |
| Rate limit | Use paid tier or throttle requests |
| Symbol not found | Use search functions to find correct symbol |
| Missing data fields | Try different provider |

## Resources

- Docs: https://docs.openbb.co/
- GitHub: https://github.com/OpenBB-finance/OpenBB
- Examples: https://github.com/OpenBB-finance/examples
- PyPI: https://pypi.org/project/openbb/

## Complete Example: Stock Analysis

```python
from openbb import obb

# 1. Get price data
prices = obb.equity.price.historical('AAPL', start_date='2023-01-01')
df_prices = prices.to_dataframe()

# 2. Get fundamentals
metrics = obb.equity.fundamental.metrics('AAPL')
ratios = obb.equity.fundamental.ratios('AAPL')
income = obb.equity.fundamental.income('AAPL', period='annual', limit=5)

# 3. Calculate technical indicators
rsi = obb.technical.rsi(prices.results, length=14)
macd = obb.technical.macd(prices.results)
sma_50 = obb.technical.sma(prices.results, length=50)
sma_200 = obb.technical.sma(prices.results, length=200)

# 4. Get options data
options = obb.derivatives.options.chains('AAPL')
df_options = options.to_dataframe()

# 5. Company profile
profile = obb.equity.profile('AAPL', provider='fmp')

# 6. Recent news
# news = obb.equity.news('AAPL')

print("Analysis complete!")
```

---

**Quick Reference v1.0** | Research Date: 2025-12-17
