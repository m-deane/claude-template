---
allowed-tools: Bash, Read, Glob, Grep
argument-hint: [--all | project-name]
description: Run project review across all managed repositories
---

# Batch Review

Run project review across repositories: $ARGUMENTS

## Process

1. **For each managed project**:
   a. **Code quality**: Run lint, check for TypeScript errors
   b. **Test health**: Run test suite, report pass/fail/coverage
   c. **Build status**: Attempt production build
   d. **Documentation sync**: Compare CLAUDE.md claims vs. actual state
   e. **Dependency health**: Check for outdated or vulnerable packages
   f. **Git hygiene**: Check for uncommitted changes, stale branches
   g. **Directory cleanliness**: Check for orphaned files in root

2. **Generate review report**:

```markdown
## Project Review Summary — {date}

| Project | Lint | Tests | Build | Docs Sync | Deps | Git Clean | Score |
|---------|------|-------|-------|-----------|------|-----------|-------|
| project-a | pass | 320/320 | pass | synced | 2 outdated | clean | A |
| project-b | 3 errors | 45/50 | fail | drifted | 5 vulnerable | dirty | D |
```

3. **Prioritized action items**: List issues ranked by severity
