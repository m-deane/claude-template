# CLAUDE.md — FM&I Dataiku Project

This file gives Claude Code context about this project. Claude reads this automatically.

## Project Context

**Team**: FM&I (Fundamentals Modelling & Innovation), Trading Analytics & Insights, BP
**Platform**: Dataiku DSS — Python recipes, managed datasets, scenarios, triggers
**Domain**: Energy commodities — crude oil, refined products, natural gas

## Project Structure

```
project-root/
├── recipes/           # Dataiku Python recipes
├── config/            # Model parameters and dataset configs
├── lib/               # Shared utility functions
├── tests/             # pytest test suite
├── notebooks/         # Exploratory analysis (not production)
├── MODEL.md           # Model documentation (keep updated)
├── CLAUDE.md          # This file
└── .cursorrules       # Cursor AI rules (if using Cursor)
```

## Code Standards

### Python
- **Dataframes**: polars only — never pandas
- **Dataset reads**: `dataiku.Dataset('name').get_dataframe()` — never direct file reads
- **Dataset writes**: `dataiku.Dataset('name').write_with_schema(df)` — always with schema
- **Loops**: No iterrows(), no apply() on large frames — use vectorised polars operations
- **Docstrings**: NumPy format on every function
- **Tests**: pytest — every new function must have at least one test
- **Paths**: pathlib.Path only — never os.path or string concatenation
- **SQL**: parameterised queries only — never f-strings or string concatenation

### Naming
- Recipe files: `verb_noun.py` (e.g. `compute_crack_spread.py`, `aggregate_hub_prices.py`)
- Dataset names: `snake_case` — match Dataiku dataset name exactly
- Config keys: `UPPER_CASE` for constants, `snake_case` for parameters

## Domain Context

### Key datasets
- `crack_spreads`: Refinery margin data, daily frequency, multiple products and hubs
- `gas_hub_prices`: Natural gas spot and forward prices by hub
- `brent_forward_curve`: Brent crude forward curve, multiple tenors

### Domain terms (use these in prompts and code comments)
- **Crack spread**: Refinery margin = product price - crude input cost
- **Forward curve**: Time-series of futures prices at different delivery dates
- **VaR**: Value at Risk — statistical measure of potential losses
- **Half-life estimator**: Mean reversion speed parameter in models
- **ELT**: Extract, Load, Transform — Dataiku pipeline pattern
- **Contango/backwardation**: Forward curve shape (contango = far > near, backwardation = near > far)

## Security and Compliance

### NEVER include in code, logs, or outputs
- Live position data (current trading positions, P&L)
- Calibration parameters (model parameters used in live pricing)
- Counterparty names or trade details
- Internal system credentials or API keys

### Safe to use with AI tools
- Historical price data that is publicly available
- Anonymised hub names in research context
- Model structure and code logic
- Aggregated performance statistics

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run a specific recipe test
pytest tests/test_compute_crack_spread.py -v
```

## When to use Claude Code

**Best tasks for Claude Code in this project:**
1. Debugging Dataiku recipe timeouts — paste the recipe and describe the timeout
2. Adding docstrings and tests to existing functions
3. Refactoring iterrows() loops to polars vectorised operations
4. Generating MODEL.md documentation from recipe code
5. Reviewing ELT pipeline for N+1 dataset read patterns
6. Writing parameterised pytest fixtures for Dataiku dataset mocking

**How to start a session:**
Open Claude Code in the project root. The first time, type:
"Read CLAUDE.md and summarise the project context for me."
Then describe your task specifically — include the recipe name, dataset name, and the specific problem.
