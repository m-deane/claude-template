# Prior Art Comparison Table for tidy-signal

## Python Signal/Trading Libraries - Feature Comparison

| Library | Signal Definition | API Style | Strengths | Limitations | Key Lesson for tidy-signal |
|---------|------------------|-----------|-----------|-------------|----------------------------|
| **Zipline** | Pipeline API - factors as transformations | OOP + Functional (Pipeline) | - Modular factor research<br>- Point-in-time data<br>- Production-ready | - No longer maintained<br>- Steep learning curve<br>- Equity-focused | Separate signal computation from execution; Pipeline optimization |
| **VectorBT** | Boolean arrays for entry/exit | Fluent interface (method chaining) | - Extremely fast (Numba)<br>- Pattern recognition<br>- Interactive dashboards | - Pro features paid<br>- Less intuitive for complex strategies | Boolean signal arrays; Factory pattern; Method chaining |
| **Backtrader** | SignalStrategy class with signal types | OOP (inheritance-based) | - Very flexible<br>- Live trading support<br>- Extensive docs | - More verbose<br>- Slower optimization | Signal taxonomy (entry/exit, long/short); Strategy lifecycle |
| **Alphalens** | Factor analysis on quantiles | Functional (utilities) | - Comprehensive validation<br>- IC analysis<br>- Sector decomposition | - Archived<br>- Equity-focused | Information Coefficient as key metric; Quantile-based analysis |
| **Pyfolio** | Portfolio returns analysis | Functional (plotting) | - Comprehensive metrics<br>- Tear sheets<br>- Benchmark comparison | - Archived<br>- Limited to performance analysis | Tear sheet pattern; Rolling metrics; Drawdown analysis |
| **Empyrical** | Pure metric calculations | Pure functional | - Comprehensive metrics<br>- Rolling variants<br>- Backend for others | - No visualization<br>- Limited scope | Separate calculation from analysis; Support multiple periodicities |

## R Tidyverse/Tidymodels - Pattern Extraction

| Component | Pattern | Application to tidy-signal |
|-----------|---------|---------------------------|
| **dplyr** | Grammar of verbs: mutate, filter, select, arrange, summarise | `detect_*`, `filter_*`, `mutate_*`, `validate_*`, `summarize_*` |
| **%>% pipe** | Left-to-right, top-to-bottom reading | Method chaining: `data.detect_cointegration().fit_ou().generate_signals()` |
| **parsnip** | Specification → Engine → Mode → Fit → Predict | `SignalSpec(type, engine, mode) → fit() → predict()` |
| **recipes** | step_* preprocessing pipeline | `add_preprocessing()` with step functions |
| **workflows** | Bundle preprocessing + model + postprocessing | `SignalWorkflow().add_preprocessing().add_signal().add_validation()` |
| **broom** | tidy(), augment(), glance() - three output types | `signal_outputs`, `signal_parameters`, `signal_metrics` DataFrames |
| **tidyquant** | tq_mutate vs tq_transmute (periodicity) | Distinguish operations that change observation count |

## Statistical Methods - Priority Ranking

| Rank | Method | Python Implementation | Use Case | Importance |
|------|--------|----------------------|----------|------------|
| 1 | Cointegration (Johansen, E-G) | `statsmodels.tsa.stattools.coint()`, `coint_johansen()` | Pairs selection | Critical |
| 2 | Stationarity (ADF, KPSS) | `statsmodels.tsa.stattools.adfuller()`, `kpss()` | Mean reversion validation | Critical |
| 3 | Walk-Forward Analysis | Custom implementation | Out-of-sample validation | Critical |
| 4 | Structural Breaks (Zivot-Andrews) | `statsmodels.tsa.stattools.zivot_andrews()` | Regime change detection | High |
| 5 | OU Parameter Estimation | Kalman filtering (statsmodels) | Entry/exit thresholds | High |
| 6 | Information Coefficient | alphalens | Factor validation | High |
| 7 | GARCH Volatility | `arch` library | Risk management | Medium |
| 8 | Half-Life Estimation | AR(1) coefficient analysis | Holding period | Medium |
| 9 | Kalman Filtering | `statsmodels.tsa.statespace` | State estimation | Medium |
| 10 | Seasonality Decomposition | `statsmodels.tsa.seasonal` | Commodity seasonality | Medium (High for agri/energy) |

## Data Structure Recommendations

| Data Type | Structure | Library | Use Case |
|-----------|-----------|---------|----------|
| Multi-dimensional (vintage × date × tenor × contract) | Dataset with named dimensions | xarray | Forward curves, vintage data |
| Signal time series | Long format DataFrame | pandas | Tidy data principles, easy filtering |
| Signal specifications | Frozen dataclass | dataclasses | Immutable, serializable configs |
| Signal outputs | Three DataFrames (outputs, parameters, metrics) | pandas | Standardized analysis interface |

## Commodity-Specific Patterns

| Pattern | Description | Python Tools | Use Case |
|---------|-------------|--------------|----------|
| **Calendar Spreads** | Near-month vs far-month futures | Custom + pandas | Term structure arbitrage |
| **Crack Spreads** | Crude oil vs refined products (3-2-1) | Custom calculation | Energy refining margins |
| **Crush Spreads** | Soybeans vs meal + oil | Custom calculation | Agricultural processing |
| **Seasonality** | Harvest cycle patterns | statsmodels seasonal decomposition | Agricultural commodities |
| **Forward Curves** | Term structure modeling | QuantLib-Python, Kalman filtering | Pricing and hedging |

## Lookahead Bias Prevention Techniques

| Technique | Implementation | Benefit |
|-----------|----------------|---------|
| Signal shifting | `df['Position'] = df['Buy'].shift(1)` | Ensures signal available before execution |
| Event-driven backtesting | Queue-based message passing | Prevents indexing mistakes |
| Point-in-time databases | ALFRED-style vintage tracking | Uses only data available at signal time |
| Walk-forward analysis | Rolling train/test splits | Simulates real-world retraining |
| Train/test temporal separation | No overlap in time periods | Proper out-of-sample validation |

## API Design Patterns for tidy-signal

| Pattern | Purpose | Example | Benefit |
|---------|---------|---------|---------|
| **Fluent Interface** | Method chaining for readability | `spec.set_type().set_engine().set_lookback()` | Concise, readable code |
| **Registry Pattern** | Extensible engine discovery | `@register_signal('mean_rev', 'ou')` | Plugin architecture |
| **Factory Pattern** | Multiple construction methods | `SignalSpec.from_config()`, `.from_dict()` | Flexible instantiation |
| **Dual-Path Architecture** | Standard vs raw data handling | `fit()` vs `fit_raw()` | Handles special data requirements |
| **Three-DataFrame Output** | Standardized results | outputs, parameters, metrics | Consistent downstream analysis |
| **Frozen Dataclass Specs** | Immutable specifications | `@dataclass(frozen=True)` | Reproducibility, no side effects |

## Gap Analysis Summary

| Current State | tidy-signal Innovation | Value Provided |
|---------------|----------------------|----------------|
| Fragmented tools (zipline + alphalens + pyfolio) | Unified grammar for signal workflows | End-to-end pipeline in one package |
| No native vintage data support | First-class `vintage_date` dimension | Proper lookahead bias prevention |
| Limited multi-dimensional support | xarray integration | Natural term structure representation |
| Inconsistent output formats | Three-DataFrame broom pattern | Standardized analysis interface |
| Manual validation workflows | Built-in walk-forward, IC, breaks | Rigorous validation by default |
| Generic financial tools | Commodity-specific features | Domain expertise (spreads, seasonality) |
| Ad-hoc config management | Frozen dataclass specs with serialization | Reproducible research |

## Community Consensus

| Topic | Consensus | Implication for tidy-signal |
|-------|-----------|---------------------------|
| **Best validation method** | Walk-forward analysis (Robert Pardo 1992) | Make walk-forward built-in, not optional |
| **Stationarity testing** | Use ADF + KPSS together (opposite nulls) | Provide combined test function |
| **Commodities trading** | Trend-following > mean reversion (but spreads differ) | Support both paradigms; emphasize spreads for mean reversion |
| **Backtesting approach** | Vectorized (speed) vs event-driven (realism) | Support both via dual-path architecture |
| **Factor validation** | Information Coefficient critical | Integrate IC analysis in validation workflow |
| **Output format** | Tear sheets from pyfolio/alphalens popular | Adopt three-DataFrame tear sheet pattern |

## Key Performance Benchmarks from Literature

| Study | Strategy | Performance | Source |
|-------|----------|-------------|--------|
| Caldeira & Moura | OU-based pairs trading (Brazilian stocks) | 16.38% annual return, 1.34 Sharpe | Academic literature |
| Alphalens guideline | Information Ratio benchmark | IR ≥ 0.05 considered good | Quantopian docs |
| Calendar spread | Margin requirement reduction | 75% credit typical | CME Group |

## Development Priority Roadmap

| Phase | Components | Estimated Effort | Dependencies |
|-------|-----------|------------------|--------------|
| **Phase 1: Core** | Data structures, specs, registry, outputs | High | xarray, dataclasses |
| **Phase 2: Stat Arb** | Cointegration, OU process, pairs selection | Medium | statsmodels, scipy |
| **Phase 3: Validation** | Walk-forward, IC, structural breaks | Medium | Phase 1 + 2 |
| **Phase 4: Commodities** | Spreads, seasonality, term structure | Medium | Phase 1 |
| **Phase 5: Workflows** | Multi-signal composition, pipelines | Low | All previous |

---

**Recommendation:** Start with Phase 1 (Core Infrastructure) to establish architectural patterns, then Phase 2 (Statistical Arbitrage) to deliver immediate value to target users, followed by Phase 3 (Validation Framework) to ensure rigor.
