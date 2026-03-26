---
description: Testing standards and practices
---

# Testing Standards

## Test Organization
- All tests go in the `tests/` directory
- Mirror the source directory structure in tests
- Name test files clearly: `[feature].test.ts` or `test_[feature].py`

## Test Quality
- Test real behavior, not implementation details
- Cover happy path, error cases, and edge cases
- No mock data that masks real integration issues
- Tests must be deterministic and repeatable

## Test Workflow
- Run tests after every significant change
- All tests must pass before marking work complete
- Fix broken tests immediately - do not skip or disable them
