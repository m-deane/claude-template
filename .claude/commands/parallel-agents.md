---
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task
argument-hint: Feature 1: [desc], Feature 2: [desc], Feature 3: [desc]
description: Self-healing parallel agent implementation with build verification gates
---

# Self-Healing Parallel Agents

Implement features using parallel agents with automatic build verification: $ARGUMENTS

## Current Project State

- Build command: !`cat package.json 2>/dev/null | grep -A5 '"scripts"' | head -6 || cat Makefile 2>/dev/null | head -5 || echo "No build config found"`
- Test command: !`cat package.json 2>/dev/null | grep '"test"' || cat pyproject.toml 2>/dev/null | grep 'test' | head -3 || echo "No test config found"`
- Lint command: !`cat package.json 2>/dev/null | grep '"lint"' || echo "No lint config found"`

## Task

Implement the requested features using parallel Task agents. Each agent MUST follow the self-healing workflow below.

## Self-Healing Agent Protocol

### Per-Agent Workflow (MANDATORY)
Each spawned agent must execute this sequence:

1. **IMPLEMENT**: Write the complete feature code
2. **BUILD CHECK**: Run the project's build/compile command
3. **LINT CHECK**: Run the project's linter
4. **SELF-HEAL LOOP**: If ANY errors exist from steps 2-3:
   - Analyze the error output
   - Fix the issues
   - Re-run build + lint
   - Repeat up to 3 times
5. **TEST**: Run tests for affected modules
6. **REPORT**: Only report completion when build + lint + tests all pass with zero errors
7. **ESCALATE**: If unable to resolve after 3 attempts, report the specific blocker with full error output

### Agent Instruction Template
When spawning each Task agent, include these instructions:
```
After implementing your changes:
1. Run: [BUILD_COMMAND]
2. Run: [LINT_COMMAND]
3. If errors, fix and re-run. Max 3 attempts.
4. Run: [TEST_COMMAND] for affected files
5. Only report success if all pass with zero errors.
6. If blocked after 3 attempts, report the exact errors.
```

## Post-Agent Integration Phase

After ALL agents complete:

1. **Integration Build**: Run full project build
2. **Conflict Resolution**: Fix any cross-agent conflicts:
   - Import collisions
   - Type mismatches
   - Duplicate declarations
   - Shared state conflicts
3. **Full Test Suite**: Run the complete test suite
4. **Final Report**: Summarize all changes, files modified, and test results

## Output Format

### Per-Feature Summary
```
Feature: [name]
Status: ✅ Complete | ⚠️ Blocked
Files Modified: [list]
Build: PASS/FAIL
Lint: PASS/FAIL
Tests: X passed, Y failed
Blockers: [if any]
```

### Integration Summary
```
Integration Build: PASS/FAIL
Cross-Agent Conflicts Found: [count]
Conflicts Resolved: [count]
Full Test Suite: X passed, Y failed, Z skipped
```
