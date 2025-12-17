# Glossary of Quantitative Finance Terms

---

## A

**Alpha**
Excess return of a strategy compared to a benchmark. Positive alpha indicates outperformance. Typically annualized.

**Annual Return (CAGR)**
Compound Annual Growth Rate. The geometric mean return per year over a period.

**Annual Volatility**
Annualized standard deviation of returns. Measures dispersion of returns. Typically √252 × daily_std for daily data.

**ATR (Average True Range)**
Volatility indicator measuring the average range of price movement over N periods.

---

## B

**Backtest**
Historical simulation of a trading strategy using past data to estimate future performance.

**Benchmark**
Reference portfolio (e.g., S&P 500) used to compare strategy performance.

**Beta**
Measure of a portfolio's sensitivity to market movements. Beta = 1 means moves with market; Beta > 1 means more volatile.

**Bollinger Bands**
Technical indicator with a moving average and bands at ±N standard deviations above/below.

---

## C

**Calmar Ratio**
Annual return divided by maximum drawdown. Higher is better.

**CAGR**
Compound Annual Growth Rate. See Annual Return.

**CVaR (Conditional VaR)**
Expected loss beyond VaR threshold. Also called Expected Shortfall.

---

## D

**Drawdown**
Decline from a peak value to a subsequent trough. Often expressed as percentage.

**Demeaned Returns**
Returns with the mean subtracted. Used to isolate relative performance.

---

## E

**EMA (Exponential Moving Average)**
Weighted moving average giving more weight to recent prices.

**Expected Shortfall**
See CVaR.

---

## F

**Factor**
Quantitative signal hypothesized to predict future returns (e.g., momentum, value).

**Forward Returns**
Returns measured from current date to N periods in the future.

---

## G

**Greeks**
Sensitivities of option prices to various factors:
- **Delta**: Sensitivity to underlying price
- **Gamma**: Rate of change of delta
- **Theta**: Time decay
- **Vega**: Sensitivity to volatility
- **Rho**: Sensitivity to interest rates

**Gross Leverage**
Sum of absolute values of long and short positions divided by portfolio value.

---

## I

**IC (Information Coefficient)**
Spearman rank correlation between factor values and subsequent returns. Measures predictive power.

**IR (Information Ratio)**
Mean IC divided by IC standard deviation. Measures consistency of predictive power.

**Implied Volatility**
Market's expectation of future volatility, derived from option prices.

---

## L

**Long-Short**
Strategy that buys (longs) top-ranked assets and sells (shorts) bottom-ranked assets.

**Lookback Period**
Historical window used to calculate indicators or factors.

---

## M

**Max Drawdown**
Largest peak-to-trough decline during a period. Key risk metric.

**Monotonicity**
Property where quantile returns consistently increase (or decrease) from lowest to highest quantile.

---

## N

**Numba**
Python library for JIT compilation, providing near-C performance for numerical code.

---

## O

**OBBject**
OpenBB's return type wrapper containing data and metadata.

**Out-of-Sample (OOS)**
Data not used for model fitting. Used to validate model performance.

---

## P

**PnL (Profit and Loss)**
Net gain or loss from a trade or strategy.

**Profit Factor**
Gross profits divided by gross losses. > 1 means profitable.

---

## Q

**Quantile**
Division of ranked values into equal-sized groups. Fifth quantile (Q5) is top 20%.

---

## R

**Returns**
Percentage change in value. Simple returns: (P1 - P0) / P0.

**Round Trip**
Complete trade cycle from opening to closing a position.

**RSI (Relative Strength Index)**
Momentum oscillator measuring speed and change of price movements. Range: 0-100.

---

## S

**Sharpe Ratio**
(Return - Risk-Free Rate) / Volatility. Risk-adjusted return measure.

**SMA (Simple Moving Average)**
Arithmetic mean of prices over N periods.

**Sortino Ratio**
Like Sharpe but only penalizes downside volatility.

**Spread**
Difference between returns of top and bottom quantiles. Long-short profitability.

---

## T

**Tear Sheet**
Comprehensive visual report combining plots and statistics.

**Turnover**
Rate of position changes. Higher turnover = higher transaction costs.

---

## V

**VaR (Value at Risk)**
Maximum expected loss at a given confidence level (e.g., 95% VaR).

**Vectorized**
Operations performed on entire arrays at once, not element-by-element.

**Volatility**
Standard deviation of returns. Measures risk/uncertainty.

---

## W

**Walk-Forward Analysis**
Validation technique repeatedly training on past data and testing on future data.

**Win Rate**
Percentage of trades that are profitable.

---

## Z

**Z-Score**
Number of standard deviations from the mean. Used for normalization.
