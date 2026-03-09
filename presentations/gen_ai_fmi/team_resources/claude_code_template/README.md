# Claude Code Template — FM&I

Claude Code is Anthropic's official CLI that runs an AI coding agent directly in your terminal, with full read/write access to your project files.

## What this template gives you

- **CLAUDE.md** — drop this into any FM&I Dataiku project root; Claude reads it automatically and instantly knows your platform (Dataiku DSS), language standards (polars, not pandas), domain context (crack spreads, forward curves, VaR), and compliance rules
- **.claude/agents/fmi-dataiku-expert.md** — a specialist sub-agent pre-configured for FM&I recipe work: Dataiku API patterns, polars refactoring, ELT pipeline review, and test generation

## How to install

1. Download the Claude Code CLI: `npm install -g @anthropic/claude-code`
2. Copy `CLAUDE.md` and `.claude/` into your Dataiku project root
3. Open a terminal in that project root and run `claude`
4. Claude reads CLAUDE.md automatically — no setup needed

## Three tasks to try immediately

**1. Debug a recipe timeout**
```
I have a recipe called compute_crack_spread.py that times out on the crack_spreads dataset.
Here is the code: [paste recipe]
What is causing the timeout and how do I fix it?
```

**2. Refactor iterrows() to polars**
```
Refactor this function to use polars vectorised operations instead of iterrows().
Keep the same output schema. Add a pytest test that covers the edge case of empty input.
[paste function]
```

**3. Generate MODEL.md documentation**
```
Read all the recipes in the recipes/ folder and generate a MODEL.md file that documents:
the inputs, outputs, transformation logic, and any assumptions for each recipe.
```

## Using the FM&I Dataiku expert agent

For recipe-specific work, invoke the specialist agent by typing `@fmi-dataiku-expert` at the start of your message, or select it from the agent panel. The agent is pre-loaded with Dataiku API patterns, FM&I domain knowledge, and the polars/pytest standards — you get more precise output without repeating context every time.

Example:
```
@fmi-dataiku-expert Review this ELT pipeline for N+1 dataset read patterns and rewrite
any repeated reads to materialise once. [paste pipeline]
```

## More resources

- Internal docs and training videos: **BP Digital Tools > AI Tools** (intranet)
- Claude Code official docs: https://docs.anthropic.com/en/docs/claude-code
- Questions or issues: post in the FM&I team channel
