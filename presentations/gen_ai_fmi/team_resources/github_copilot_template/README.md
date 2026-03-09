# GitHub Copilot — FM&I Setup Guide

GitHub Copilot is an AI coding assistant embedded in VS Code (and JetBrains) that suggests code completions and answers questions about your codebase. The `copilot-instructions.md` file is how you tell Copilot about your project — without it, Copilot gives generic Python suggestions that ignore Dataiku, polars, and FM&I conventions.

---

## Setup (5 minutes)

1. Copy the `.github/` folder into the **root of your Dataiku project**
   — the file must live at `.github/copilot-instructions.md`
2. Open the project folder in VS Code
3. Install the **Dataiku** extension from the VS Code marketplace
4. Connect VS Code to your DSS instance:
   - Open the Dataiku extension panel
   - Enter your DSS URL and an API key (generate one from your Dataiku profile settings)
5. Open any Python recipe — Copilot now has full project context

---

## Verify setup worked

Open Copilot Chat (`Ctrl+Shift+I` / `Cmd+Shift+I`) and type:

```
@workspace — summarise this project: what platform is it on, what dataframe library does it use, and what are the key datasets?
```

If the response mentions Dataiku, polars, and your actual dataset names, the instructions file is being read correctly.

---

## 5 workflows to use from day one

### 1. Audit a recipe for anti-patterns
```
@workspace — does any recipe in this project use pandas or iterrows()?
Flag each one and show the polars equivalent.
```

### 2. Explain a recipe end-to-end
Open the recipe file, then in Copilot Chat:
```
/explain — what does this recipe do, what are its inputs and outputs,
and are there any performance or security issues I should know about?
```

### 3. Generate pytest tests
Select a function in the editor, then:
```
/test — generate pytest tests covering: happy path, empty DataFrame input,
and a DataFrame where the price column contains nulls.
```

### 4. Add docstrings to undocumented functions
Select one or more functions, then:
```
/doc — add NumPy-style docstrings to each selected function.
Use FM&I domain terms where relevant (crack_spread, forward_curve, half_life).
```

### 5. Trace downstream impact of a schema change
```
@workspace — if I rename the 'settlement_date' column to 'delivery_date'
in brent_forward_curve, which recipes would break?
```

---

## Access and cost

GitHub Copilot is included in the **BP enterprise licence** — there is no personal cost.

If Copilot is not active in your VS Code, raise an IT ticket:

- Ticket type: *Software Access Request*
- Description: "Request access to GitHub Copilot under BP enterprise licence"
- Typical turnaround: **2–3 business days**, no manager approval required

Once access is granted, sign into GitHub in VS Code (`Accounts` icon, bottom-left) and Copilot activates automatically.
