---
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task
argument-hint: [bug description with file/function reference]
description: Test-driven bug fix with codebase-wide sibling pattern scanning
---

# Test-Driven Bug Fix

Fix bugs using test-first methodology with codebase-wide sibling scanning: $ARGUMENTS

## Current Test Infrastructure

- Test framework: !`cat package.json 2>/dev/null | grep -E '"(jest|mocha|vitest)"' || cat pyproject.toml 2>/dev/null | grep -E '(pytest|unittest)' || echo "Unknown test framework"`
- Test directory: !`ls -d tests/ test/ __tests__/ spec/ 2>/dev/null | head -1 || echo "No test directory found"`
- Test command: !`cat package.json 2>/dev/null | grep '"test"' | head -1 || echo "pytest tests/ -v"`

## Task

Fix the described bug using the strict test-driven protocol below. Do NOT write any fix code until the reproduction test exists and fails.

## Test-Driven Fix Protocol

### Step 1: REPRODUCE
Write a minimal test that **fails** and demonstrates the exact bug described.
- Place in the appropriate test directory
- Name clearly: `test_regression_<bug_name>` or `<bug_name>.regression.test`
- The test must FAIL before the fix is applied — run it to confirm failure

### Step 2: SCAN FOR SIBLINGS
Use Grep to search the **entire codebase** for ALL functions, classes, or modules that use the same pattern as the buggy code.

Look for:
- Functions with similar names (e.g., if `step_sma` is buggy, check `step_ewm`, `step_expanding`, `step_lead`, etc.)
- Copy-pasted logic blocks
- Shared utility function calls with similar parameters
- Related switch/match cases

**List every instance found** — do not skip any.

### Step 3: EXPAND TESTS
For each sibling instance identified in Step 2:
- Determine if it has the same vulnerability
- If yes, write a failing test for it
- Run all new tests to confirm they fail

### Step 4: FIX ALL
Implement fixes for:
- The original reported bug
- Every sibling instance with the same vulnerability

Do NOT fix only the reported instance.

### Step 5: VALIDATE
Run the full test suite (old tests + new regression tests):
- If ANY test fails, investigate and fix
- Iterate until ALL tests pass
- Run the project build to ensure no compilation errors

### Step 6: REPORT
Provide a summary with:

```
## Bug Fix Report

### Original Bug
- Description: [what was broken]
- Root Cause: [why it was broken]
- File/Function: [location]

### Sibling Instances Found
| Location | Same Bug? | Fixed? |
|----------|-----------|--------|
| file:function | Yes/No | Yes/N/A |

### Tests Added
- [test_file]: [test_name] — [what it verifies]

### Fix Details
- [file:line]: Before → After (brief description)

### Validation
- New regression tests: X passed
- Full test suite: X passed, Y failed
- Build: PASS/FAIL
```
