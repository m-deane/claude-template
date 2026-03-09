# v5 Upskill Enhancements — Content Specification

## Summary of Changes

Four new slides (A, B, C, D) added to Section 4. One existing slide modified (Slide 11 — Access instructions for Copilot Studio). The prompting slide (Slide 21) is retained as-is; Slide C replaces no existing slide but is inserted directly after Slide 21 as an additional worked-example slide.

---

## Slide A — "Connecting GitHub Copilot to Your Dataiku Workflow"

**Target file**: `slides_s4_s6_v5.cjs`
**Insert position**: After Slide 18 (GitHub Copilot live demo), before Slide 19 (Cursor live demo)
**Layout**: Two-column — left step-by-step card (accent `C.green`), right terminal card (dark background `1A1A2E`, `C.teal` text)
**Bottom bar**: "This one file gives Copilot permanent FM&I Dataiku context — every recipe you open inherits it without re-explaining the setup"

### Left card — "The VS Code + Dataiku setup" (header `C.green`)

Numbered setup sequence:
1. Install VS Code + GitHub Copilot extension from the BP IT self-service portal under 'Developer Tools'. The extension appears in VS Code's Extensions sidebar — search 'GitHub Copilot' and install both the main extension and GitHub Copilot Chat.
2. Install the Dataiku VS Code extension (DSS remote kernel). Search 'Dataiku' in the VS Code Extensions sidebar. This extension connects VS Code directly to your DSS instance.
3. Configure the remote kernel: open VS Code settings (Cmd/Ctrl+comma), search 'Dataiku', set the DSS URL to your instance (e.g. https://dss.bp.com) and your API key from DSS > Profile > API Keys.
4. Open any Python recipe in VS Code via File > Open Folder, pointing at your Dataiku project directory. Copilot now sees the full recipe context and all lib/ Python files.
5. Create `.github/copilot-instructions.md` in the project root with FM&I Dataiku context (see right panel). This file gives Copilot permanent project awareness on every session.

### Right card — terminal showing `copilot-instructions.md` template

Title: "copilot-instructions.md for a Dataiku project"
Background: `1A1A2E`, text: `C.teal`, font: Courier New

Content:
```
# Project: FM&I Fundamental Models
# Platform: Dataiku DSS 12.x
# Stack: Python 3.9, pandas, numpy, scikit-learn

## Recipe patterns
- Always use managed datasets via dataiku.Dataset()
- Use dku.get_variables() for project variables
- Recipes must be idempotent (safe to re-run)

## Code style
- Docstrings required on all functions
- No hardcoded paths — use project variables
- Log to dku.get_custom_variables() for run tracking

## Testing
- Test with a 1000-row sample before full run
- Use dataiku.default_project_key() in test code
```

---

## Slide B — "Connecting Cursor to Your Dataiku Project"

**Target file**: `slides_s4_s6_v5.cjs`
**Insert position**: After Slide A (new), before Slide 19 (Cursor live demo)
**Layout**: Left column with 3 stacked cards (accent `C.green`), right terminal card (dark background `1A1A2E`, `C.teal` text)
**Bottom bar**: "A .cursorrules file turns Cursor from a generic coding assistant into an FM&I Dataiku specialist that already knows your data schemas"

### Left stacked cards

Card 1 — "Point Cursor at your DSS project directory"
Open Cursor at the root of your Dataiku project folder (the directory synced from DSS or checked out from Git). Cursor then has full context over all recipes, lib/ Python files, and tests in one session. It can reason across all of them simultaneously — a timeout in one recipe caused by a schema change in another becomes visible immediately.

Card 2 — "Write a .cursorrules file for your project"
Create `.cursorrules` in the project root. This file tells Cursor about your Dataiku conventions, data schemas, and code patterns once — it applies to every session automatically. Without it, you re-explain context every conversation and get generic answers instead of FM&I-specific ones.

Card 3 — "Use Agent mode for cross-recipe tasks"
Switch to Agent mode when the task spans multiple recipes or requires reading the lib/ directory alongside the recipe. Agent mode reads the full project structure before responding, so it understands how your ELT pipeline connects end-to-end. Ask mode only reads what you paste in.

### Right card — `.cursorrules` template

Background: `1A1A2E`, text: `C.teal`, font: Courier New

Content:
```
# Dataiku DSS project — FM&I Fundamental Models

## Platform context
- Dataiku DSS 12.x, Python recipes
- Datasets accessed via dataiku.Dataset()
- Project variables via dku.get_variables()
- All recipes must be idempotent

## This project's data
- crack_spreads: daily ICE Brent crack spread data,
  cols: [date, spread_type, value, currency]
- eia_storage: weekly EIA storage data,
  cols: [date, region, volume_mb, change_mb]
- model_outputs: fundamental model predictions,
  cols: [date, commodity, forecast, confidence]

## Conventions
- Functions: snake_case, docstrings required
- No hardcoded values — use project variables
- Log exceptions, never silently fail
- Sample before full run (use nrows=1000 for dev)
```

---

## Slide C — "Before and After: What a Better Prompt Looks Like"

**Target file**: `slides_s4_s6_v5.cjs`
**Insert position**: After Slide 21 (Better Prompts formula), before Slide 22 (Both tools roadmap)
**Layout**: Two-column left/right (before/after), plus a full-width bottom panel
**Bottom bar**: "The before versions get generic code. The after versions get production-ready Dataiku recipes. The framework is the only difference."

### Left card — "Before: the prompt most people write" (header `C.red`)

Dark terminal background (`1A1A2E`), Courier New text showing three weak prompts:
```
"Write me a Python function to process data"
→ Too vague: no data shape, no output spec, no context

"Help me with this Dataiku recipe, it's slow"
→ No diagnosis path: Copilot cannot identify the cause
  without data size, operations, or error message

"Document this code"
→ No output spec: docstring? README? inline comments?
  For whom? What level of detail?
```

### Right card — "After: the same prompt with the framework" (header `C.green`)

Dark terminal background (`1A1A2E`), Courier New text showing improved versions:
```
"Context: Dataiku recipe processing 500k rows of
daily crack spread data (date, spread_type, value).
Task: Rewrite the aggregation to remove iterrows()
and use vectorised pandas operations.
Constraints: Must stay under 4GB memory, output
same schema, must be idempotent.
Verify: Add a row-count assertion before and after."

"Context: Dataiku recipe reading EIA storage data,
timing out on join with 2M-row positions table.
Task: Identify the bottleneck and fix it.
Constraints: pandas only, no Spark, DSS 12.x."

"Context: This function calculates the half-life
of a calendar spread mean reversion signal.
Task: Write a NumPy docstring with params,
returns, raises, and a worked example."
```

### Bottom panel

Full-width bar, dark `C.navy` background, white Trebuchet MS 11pt bold:
"The LLM already has the answer. The prompt is just the quality filter."

---

## Slide D — "Your First 30 Minutes — Start Here, Not There"

**Target file**: `slides_s4_s6_v5.cjs`
**Insert position**: After Slide C (new), before Slide 22 (Both tools roadmap)
**Layout**: 3-card horizontal row (x: 0.3, 3.6, 6.6; y: 1.45; w: 2.9; h: 3.3), dark navy backgrounds, with a full-width note bar below
**Bottom bar**: "Don't optimise the process before you've used it once — pick one real FM&I task this week and run the loop"

### Card 1 — "Minute 0–10: Request access" (fill `C.navy`, top accent `C.teal`)

Title: "Minute 0–10: Request access" (white, 11pt Trebuchet MS bold)
Body (Calibri 8.5pt `C.textLight`):
If you have M365: open Word or Teams now and click the Copilot button. It is already on. If you want GitHub Copilot: go to the BP IT self-service portal, search 'GitHub Copilot', submit the request. Approval: 2–3 days. That is it. Do not spend this time reading documentation — spend it submitting the request.

### Card 2 — "Minute 10–20: Your first real task" (fill `C.navy`, top accent `C.blue`)

Title: "Minute 10–20: Your first real task" (white, 11pt Trebuchet MS bold)
Body (Calibri 8.5pt `C.textLight`):
Do not start with a new project. Find a Dataiku recipe you wrote in the last 30 days. Open it in VS Code with Copilot active. Type: 'Write pytest tests for the main transformation function in this recipe. Use a 100-row sample. Test the edge case where input data is empty.' Review what comes back.

### Card 3 — "Minute 20–30: Learn from the output" (fill `C.navy`, top accent `C.green`)

Title: "Minute 20–30: Learn from the output" (white, 11pt Trebuchet MS bold)
Body (Calibri 8.5pt `C.textLight`):
If the tests are wrong: tell Copilot exactly what is wrong and ask it to fix them. If they are right: run them. If they pass: you just saved 45 minutes of test-writing. That is the productivity loop. Do it again tomorrow with a different recipe. The data point from this one task is worth more than any general advice.

### Note bar below cards

Full-width rect (`C.deepNavy`, y: 4.8, h: 0.2), Calibri 9pt `C.textLight`:
"One task. One tool. Time it. That data point is more valuable than anything in this presentation."

---

## Modified Slide — Copilot Studio Access (Slide 11 in `slides_s1_s3_v5.cjs`)

**Target file**: `slides_s1_s3_v5.cjs`
**Slide**: Slide 11 — "Requesting access takes less than 10 minutes"
**Change**: The layout is restructured. The four access cards are kept at reduced height, and a new terminal-style card is added at the bottom showing the Copilot Studio business justification template.

The Copilot Studio access card body text is updated to add: "Use the template below when writing your business justification — it includes FM&I-specific language that addresses the standard approval questions."

### Justification template card

Dark terminal background (`1A1A2E`), Courier New 7.5pt, `C.teal` text, placed below the four access cards:

```
Subject: Copilot Studio licence request — FM&I/TA&I

Business justification:
The FM&I team runs [X] Dataiku pipelines producing
fundamental models for BP Trading desks. We require
Copilot Studio to build automated agents that:

1. Monitor pipeline scenario run status and alert
   the team to failures via Teams
2. Summarise daily fundamental model outputs and
   post structured briefings to our Teams channel
3. Process ad hoc analysis requests from trading
   desks without manual triage

Estimated time saving: 3-5 hours/week per analyst.
Tool: Microsoft Copilot Studio (M365 add-on).
Data classification: Internal only — no position
data or trading signals will be processed.

Requesting for: [your name], FM&I, TA&I
Manager approval: [manager name]
```

---

## Slide Sequence in v5 (Section 4 summary)

- Slide 16: Section Divider — GitHub Copilot & Cursor (unchanged)
- Slide 17: Same Category, Very Different Strengths (unchanged)
- Slide 18: [LIVE DEMO] GitHub Copilot — Dataiku Recipe Timeout (unchanged)
- **Slide 18A (NEW): Connecting GitHub Copilot to Your Dataiku Workflow**
- **Slide 18B (NEW): Connecting Cursor to Your Dataiku Project**
- Slide 19: [LIVE DEMO] Cursor — Prompt to Working Dash App (unchanged)
- Slide 20: Three Modes — Match the Mode to the Task (unchanged)
- Slide 21: Better Prompts = Better Output — The Formula (unchanged)
- **Slide 21C (NEW): Before and After — What a Better Prompt Looks Like**
- **Slide 21D (NEW): Your First 30 Minutes — Start Here, Not There**
- Slide 22: Both Tools Are Shipping Major Upgrades (unchanged)
