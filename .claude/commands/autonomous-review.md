---
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task
argument-hint: [scope: full | security | performance | quality] [--branch main]
description: Autonomous codebase review pipeline with parallel audit, prioritized fixes, and validation
---

# Autonomous Codebase Review Pipeline

Run a full autonomous review and improvement pipeline: $ARGUMENTS

## Current Project State

- Main branch: !`git branch --show-current`
- Test command: !`cat package.json 2>/dev/null | grep '"test"' | head -1 || echo "pytest tests/ -v"`
- Build command: !`cat package.json 2>/dev/null | grep '"build"' | head -1 || echo "No build command"`
- File count: !`find . -type f -not -path './.git/*' -not -path './node_modules/*' -not -path './.venv/*' | wc -l`
- Languages: !`find . -type f -name '*.py' -o -name '*.ts' -o -name '*.js' -o -name '*.go' | head -20 | sed 's/.*\.//' | sort | uniq -c | sort -rn`

## Task

Execute a multi-phase autonomous codebase review. Each phase builds on the previous one.

## Phase 1: Parallel Audit

Spawn 6 parallel Task agents, one per audit dimension:

### Agent 1: Security Vulnerabilities
- Scan for OWASP Top 10 vulnerabilities
- Check for hardcoded secrets, credentials, API keys
- Review authentication and authorization patterns
- Check dependency vulnerabilities
- Review input validation and sanitization

### Agent 2: Performance Bottlenecks
- Identify N+1 query patterns
- Find unnecessary re-renders or recomputations
- Check for missing indexes in database queries
- Review memory allocation patterns
- Identify blocking operations in async code

### Agent 3: Dead Code & Duplication
- Find unused imports, variables, functions, classes
- Identify duplicated logic across modules
- Check for unreachable code paths
- Find TODO/FIXME/HACK comments that indicate incomplete work

### Agent 4: Type Safety & Error Handling
- Check for untyped function signatures
- Find uncaught exceptions or missing error handlers
- Review null/undefined safety
- Check for type assertion abuse
- Verify error messages are actionable

### Agent 5: Test Coverage Gaps
- Identify untested business logic functions
- Find untested error paths and edge cases
- Check for missing integration tests
- Review test quality (assertions, not just execution)

### Agent 6: Dependency & Config Issues
- Check for outdated dependencies with known vulnerabilities
- Review configuration files for inconsistencies
- Check for environment-specific hardcoded values
- Review build and deployment configuration

### Audit Output Format (per agent)
```
## [Dimension] Audit Results

### P0 (Critical)
- [finding]: [file:line] — [description]

### P1 (High)
- [finding]: [file:line] — [description]

### P2 (Medium)
- [finding]: [file:line] — [description]

### P3 (Low)
- [finding]: [file:line] — [description]
```

## Phase 2: Consolidation & Planning

After all audit agents complete:
1. Merge all findings into a single prioritized list
2. Group related fixes (changes that affect the same files)
3. Create an implementation plan sorted by priority (P0 first)
4. Estimate blast radius for each fix group
5. Write the plan to `.claude_plans/review-findings.md`

## Phase 3: Parallel Implementation

For each fix group, spawn a Task agent that:
1. Creates a working branch: `fix/<group-name>`
2. Implements all fixes in that group
3. Runs the full test suite and fixes any regressions
4. Writes a CHANGELOG entry describing what changed and why
5. Commits with conventional commit messages (`fix:`, `perf:`, `refactor:`)
6. Reports files changed, tests passed/failed, summary of changes

## Phase 4: Integration Validation

After all implementation agents complete:
1. Merge all fix branches into a single integration branch
2. Run the complete test suite
3. Run the build
4. Produce a final report

### Final Report Format
```
## Codebase Review Summary

### Audit Statistics
- Total findings: X
- P0 (Critical): X
- P1 (High): X
- P2 (Medium): X
- P3 (Low): X

### Implementation Results
| Fix Group | Branch | Files Changed | Tests | Status |
|-----------|--------|---------------|-------|--------|
| [name] | fix/[name] | X files | PASS/FAIL | ✅/⚠️ |

### Validation
- Integration build: PASS/FAIL
- Full test suite: X passed, Y failed, Z skipped
- Regressions introduced: X

### Remaining Items
- [any P2/P3 items deferred for future work]
```

Save the full report to `.claude_plans/review-report.md`.
