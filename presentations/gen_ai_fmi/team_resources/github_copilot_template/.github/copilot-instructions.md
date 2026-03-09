# FM&I Dataiku Project — GitHub Copilot Instructions
# BP Trading Analytics & Insights
# Save this file as .github/copilot-instructions.md in your project root
# GitHub Copilot reads this automatically when you have @workspace enabled

## Project context
This is a Dataiku DSS project for the FM&I team at BP Trading Analytics & Insights.
Primary language: Python. Recipes are Dataiku Python recipe scripts.
Pipelines read from and write to Dataiku managed datasets.
Domain: energy commodities — crude oil, refined products, natural gas.

## Code style requirements

### Dataframes
- Use polars exclusively — never pandas or numpy for tabular operations
- Imports: `import polars as pl`
- Dataset reads: `dataiku.Dataset('name').get_dataframe()` — returns polars DataFrame
- Dataset writes: `dataiku.Dataset('name').write_with_schema(df)`

### Performance
- Never use iterrows(), apply(), or Python for loops over dataframe rows
- Use polars lazy evaluation for datasets > 100k rows: `df.lazy()...collect()`
- For rolling calculations: `df.with_columns(pl.col('price').rolling_mean(window_size=30))`
- For aggregations: `df.groupby('hub').agg(pl.col('price').mean())`

### Code quality
- Every function must have a NumPy-style docstring
- Every new function must have at least one pytest test
- Use pathlib.Path for all file operations — never os.path
- Parameterised SQL queries only — never f-string construction

## Domain vocabulary
When writing code or comments, use these exact terms:
- crack_spread (not crack spread or crackspread)
- forward_curve (not forward curve)
- half_life_estimator (not halflife or half life)
- elt_pipeline (not ETL — we use ELT on Dataiku)
- gas_hub (not hub alone when context is gas)

## Security rules — CRITICAL
NEVER suggest code that:
- Logs, prints, or writes calibration parameters to any output dataset
- Includes live position data in any logging statement
- Writes counterparty names to any non-permissioned dataset
- Uses API keys or credentials inline in code

If you see any of the above in existing code, flag it immediately.

## Copilot-specific setup notes

### VS Code with Dataiku extension
1. Install "Dataiku" extension from VS Code marketplace
2. Connect to your DSS instance (API key from your Dataiku profile)
3. Open a Python recipe — Copilot now has recipe context + these instructions
4. Use @workspace to ask architecture questions across the full project

### Useful @workspace prompts for FM&I
- "@workspace which recipes depend on the crack_spreads dataset?"
- "@workspace does any recipe use iterrows() — flag it and suggest the polars equivalent"
- "@workspace generate a MODEL.md for the [recipe name] recipe"
- "@workspace what is the downstream impact of changing the date column type in gas_hub_prices?"

### Slash commands to use daily
- `/explain` — paste any recipe, get a plain-English explanation with FM&I context
- `/fix` — paste an error, get a fix that uses the correct Dataiku API
- `/test` — generate pytest tests for a function or recipe section
- `/doc` — generate NumPy docstrings for undocumented functions
