# Cursor — FM&I Setup Guide

Cursor is an AI-native code editor built on VS Code that uses your project files as context to answer questions, generate code, and explain pipelines across your whole codebase.

---

## Setup (5 minutes)

1. Download Cursor from [cursor.com](https://cursor.com) and install it
2. Copy `.cursorrules` into the **root folder of your Dataiku project**
3. Open that folder in Cursor: `File > Open Folder`
4. Verify setup (see below)

That is it. Cursor reads `.cursorrules` automatically — no plugin or extension required.

---

## Verify setup worked

Open Cursor chat (`Cmd+L`) and type:

```
@Codebase — what recipes exist in this project and what does each one do?
```

If Cursor describes your actual recipes by name, the workspace index is working correctly.

---

## 5 workflows to use from day one

### 1. Explain an unfamiliar recipe
Paste any recipe script into chat and ask:
```
Explain what this recipe does, what datasets it reads from and writes to,
and flag any polars anti-patterns or security issues.
```

### 2. Rewrite a pandas recipe to polars
```
@Codebase — find any recipe that imports pandas and rewrite it using polars.
Keep the Dataiku dataset read/write API exactly as-is.
```

### 3. Generate tests for a new function
After writing a function:
```
Write pytest tests for the function I just wrote. Cover the happy path,
an empty DataFrame input, and a DataFrame with nulls in the price column.
```

### 4. Investigate upstream/downstream impact
```
@Codebase — if I change the date column in gas_hub_prices from string to Date type,
which recipes would break and what would I need to update?
```

### 5. Generate a MODEL.md for a recipe
```
@Codebase — generate a MODEL.md for the crack_spread_calculator recipe.
Include: purpose, inputs, outputs, key assumptions, and calibration parameters
(but do not include any actual parameter values).
```

---

## Cost and access

Cursor costs approximately £20/month (Pro plan). Claim via T&E as a business tool subscription.
Use the category: *Software / Developer Tools*.

The free tier (Hobby) works but has a limit of 2,000 completions per month — sufficient for evaluation but not daily use.
