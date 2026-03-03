---
name: create-an-agent-team
description: Design and deploy multi-agent teams with Opus 4.6 for planning/review and Sonnet 4.6 for implementation. Orchestrates parallel agent execution, tracks token usage, and ensures post-task documentation and commits.
---

# Create An Agent Team — Multi-Agent Orchestration

## Overview

Design, deploy, and manage teams of specialized Claude agents that work together on complex tasks. Uses a two-tier model strategy: Opus 4.6 for planning and review (deep reasoning), Sonnet 4.6 for implementation (fast execution). Reports token usage and enforces post-task automation.

---

# Process

## Phase 1: Plan (Opus 4.6)

### 1.1 Analyze the Task

The planning agent (Opus) receives the task and:

1. **Reads the target project's CLAUDE.md** — understands architecture, patterns, constraints
2. **Breaks the task into subtasks** — identifies independent vs. dependent work
3. **Maps subtasks to agent roles** — assigns each subtask to the most appropriate agent type
4. **Defines the execution graph** — which tasks can run in parallel, which are sequential
5. **Sets success criteria per subtask** — testable assertions for each piece of work

### 1.2 Agent Role Assignment

Available agent roles for team composition:

| Role | Model | When to Use |
|------|-------|-------------|
| `architect` | Opus 4.6 | System design, API contracts, schema changes |
| `implementer` | Sonnet 4.6 | Writing code, creating files, editing existing code |
| `tester` | Sonnet 4.6 | Writing tests, running test suites, coverage analysis |
| `reviewer` | Opus 4.6 | Code review, security audit, architecture validation |
| `documenter` | Sonnet 4.6 | Updating docs, CLAUDE.md, README files |
| `researcher` | Opus 4.6 | Investigating APIs, analyzing libraries, reading docs |
| `debugger` | Sonnet 4.6 | Investigating errors, fixing test failures |

### 1.3 Execution Plan Format

```markdown
## Agent Team Plan

### Task: [Task title]
### Target Project: [project-name]
### Estimated Agents: [count]
### Estimated Token Budget: [range]

### Execution Graph

\`\`\`
[architect] ──→ [implementer-1] ──→ [tester] ──→ [reviewer]
                [implementer-2] ──↗
                [documenter] ─────────────────────↗
\`\`\`

### Agent Assignments

#### Agent 1: architect (Opus 4.6)
- **Task**: Design the API contract and schema changes
- **Inputs**: CLAUDE.md, existing routers, Prisma schema
- **Outputs**: Schema diff, router interface spec, type definitions
- **Success Criteria**: Types compile, no conflicts with existing schema

#### Agent 2: implementer-1 (Sonnet 4.6)
- **Depends on**: Agent 1
- **Task**: Implement the tRPC router
- **Inputs**: Router interface spec from Agent 1
- **Outputs**: Router file, registered in root.ts
- **Success Criteria**: Router compiles, follows protectedProcedure pattern

#### Agent 3: implementer-2 (Sonnet 4.6)
- **Depends on**: Agent 1
- **Task**: Implement the UI page
- **Inputs**: Type definitions from Agent 1
- **Outputs**: Page component with loading/error states
- **Success Criteria**: Page renders, uses correct tRPC hooks

#### Agent 4: tester (Sonnet 4.6)
- **Depends on**: Agent 2, Agent 3
- **Task**: Write and run tests
- **Inputs**: Implemented router and page
- **Outputs**: Test file, all tests passing
- **Success Criteria**: npm test passes, coverage maintained

#### Agent 5: reviewer (Opus 4.6)
- **Depends on**: Agent 4
- **Task**: Review all changes for quality and security
- **Inputs**: All files modified by the team
- **Outputs**: Review report, requested changes
- **Success Criteria**: No security issues, follows all CLAUDE.md patterns
```

---

## Phase 2: Review Plan (Opus 4.6)

### 2.1 Validate the Plan

Before execution, the planning agent validates:

- [ ] All subtasks have clear, testable success criteria
- [ ] Dependencies are correctly ordered (no circular dependencies)
- [ ] Parallel tasks are truly independent
- [ ] Token budget is reasonable for the task complexity
- [ ] Agent roles match the work (no Opus for simple implementation)
- [ ] Post-task automation is included (docs, tests, commit)

### 2.2 Present Plan for Approval

Present the plan to the user with:
- Execution graph visualization
- Estimated token budget per agent
- Risk assessment (what could go wrong)
- Fallback strategies (what if an agent fails)

Wait for user approval before proceeding to Phase 3.

---

## Phase 3: Implement (Sonnet 4.6 + Opus 4.6)

### 3.1 Execute the Plan

Launch agents according to the execution graph:

```
For each execution tier (respecting dependencies):
  1. Launch all independent agents in parallel
  2. Wait for all agents in current tier to complete
  3. Validate success criteria for each completed agent
  4. If any agent fails:
     a. Attempt self-repair (give the agent its error output)
     b. If self-repair fails, escalate to Opus for diagnosis
     c. If Opus can't resolve, halt and report to user
  5. Pass outputs to next tier's agents as inputs
  6. Proceed to next tier
```

### 3.2 Token Tracking

During execution, track per-agent:
- Input tokens consumed
- Output tokens generated
- Number of tool calls
- Wall clock time
- Success/failure status

### 3.3 Progress Reporting

Report progress as agents complete:

```markdown
## Team Progress

| Agent | Role | Status | Tokens In | Tokens Out | Duration |
|-------|------|--------|-----------|------------|----------|
| architect | Opus | completed | 12,400 | 8,200 | 45s |
| implementer-1 | Sonnet | completed | 8,100 | 15,300 | 32s |
| implementer-2 | Sonnet | in_progress | 6,200 | ... | ... |
| tester | Sonnet | pending | — | — | — |
| reviewer | Opus | pending | — | — | — |

**Total tokens**: 50,200 / 100,000 budget
**Elapsed time**: 1m 17s
```

---

## Phase 4: Post-Task Automation

### 4.1 Mandatory Post-Task Steps

After the agent team completes:

1. **Run project tests**: `npm test` (or project-specific test command)
2. **Run project lint**: `npm run lint` (or project-specific lint command)
3. **Run project build**: `npm run build` (or project-specific build command)
4. **Update CLAUDE.md**: If implementation changed architecture, update docs
5. **Update plans**: Mark completed items in .claude_plans/
6. **Update STATUS.md**: Refresh project status file
7. **Commit to git**: With descriptive message summarizing the team's work
8. **Report token usage**: Final summary of total spend

### 4.2 Final Report

```markdown
## Agent Team Report

### Task: [Title]
### Status: [Completed/Partially Completed/Failed]
### Duration: [Total wall clock time]
### Token Usage: [Total input + output tokens]

### What Was Done
- [Bullet point summary of changes]

### Files Modified
- `path/to/file.ts` — [description of changes]

### Tests
- [X] All tests passing ([count] tests)
- [X] Build succeeds
- [X] Lint clean

### Git Commit
- Branch: [branch-name]
- Commit: [hash] — [message]

### Token Breakdown
| Agent | Input | Output | Total |
|-------|-------|--------|-------|
| architect | 12,400 | 8,200 | 20,600 |
| implementer-1 | 8,100 | 15,300 | 23,400 |
| ... | ... | ... | ... |
| **Total** | **X** | **Y** | **Z** |
```
