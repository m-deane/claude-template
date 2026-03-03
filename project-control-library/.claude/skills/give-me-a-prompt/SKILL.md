---
name: give-me-a-prompt
description: Generate well-structured prompts with success criteria linked to a target project's CLAUDE.md. Diagnoses the problem, identifies solutions, creates implementation plans with defined success criteria. Supports manual review notes for iterative refinement.
---

# Give Me A Prompt — Intelligent Prompt Generator

## Overview

Generate precise, actionable prompts for Claude Code sessions by analyzing a target project's CLAUDE.md, diagnosing the problem being described, and producing a comprehensive prompt with success criteria, constraints, and implementation guidance.

---

# Process

## Phase 1: Context Gathering

### 1.1 Identify Target Project

Determine which project this prompt is for:

```bash
# List all managed projects
ls ~/projects/*/CLAUDE.md 2>/dev/null
```

**Read the target project's CLAUDE.md** to understand:
- Project overview, stack, and scale
- Architecture and key directories
- Critical patterns and conventions
- Existing commands, quality gates, testing approach
- Known trade-offs and troubleshooting notes

### 1.2 Read Existing Plans

Check for existing context in the target project:

```bash
# Check for existing plans and status
ls ~/projects/{target}/.claude_plans/ 2>/dev/null
cat ~/projects/{target}/STATUS.md 2>/dev/null
```

### 1.3 Accept Manual Review Notes (Optional)

If the user provides manual review notes or additional context:
- Incorporate them as constraints in the generated prompt
- Use them to refine the problem diagnosis
- Flag any conflicts with existing CLAUDE.md directives

---

## Phase 2: Problem Diagnosis

### 2.1 Identify the Problem

From the user's description, create a comprehensive problem statement:

**Problem Statement Template:**
```markdown
## Problem Statement

**What**: [One sentence describing the observable issue or desired feature]
**Why**: [Business/user impact — why this matters]
**Where**: [Which files, routes, components, or systems are affected]
**Current State**: [What exists now — reference specific code/patterns from CLAUDE.md]
**Desired State**: [What should exist after implementation]
**Gap Analysis**: [What's missing between current and desired state]
```

### 2.2 Diagnose Root Cause

Analyze the problem against the project's architecture:
- Is this a missing feature, a bug, a performance issue, or a refactoring need?
- Does the project's existing architecture support this, or does it need extension?
- Are there existing patterns in the codebase that should be followed?
- What are the edge cases and failure modes?

### 2.3 Identify Solutions

Propose 1-3 solution approaches ranked by:
- **Alignment with existing patterns** (from CLAUDE.md critical patterns section)
- **Implementation complexity** (prefer simpler solutions)
- **Impact on existing tests** (prefer non-breaking changes)
- **Token efficiency** (prefer approaches that need fewer agent turns)

---

## Phase 3: Plan Implementation

### 3.1 Create Implementation Plan

For the selected solution, create a phased plan:

```markdown
## Implementation Plan

### Phase 1: [Foundation/Setup]
- [ ] Step 1 — [specific, measurable action]
- [ ] Step 2 — [specific, measurable action]

### Phase 2: [Core Implementation]
- [ ] Step 3 — [specific, measurable action]
- [ ] Step 4 — [specific, measurable action]

### Phase 3: [Integration/Testing]
- [ ] Step 5 — [specific, measurable action]
- [ ] Step 6 — [specific, measurable action]
```

### 3.2 Define Success Criteria

Every prompt MUST include explicit, testable success criteria:

```markdown
## Success Criteria

### Must Have (P0)
- [ ] [Criterion 1 — testable assertion]
- [ ] [Criterion 2 — testable assertion]

### Should Have (P1)
- [ ] [Criterion 3 — testable assertion]

### Nice to Have (P2)
- [ ] [Criterion 4 — testable assertion]

### Verification Commands
\`\`\`bash
# How to verify each criterion
npm run lint          # No lint errors
npm run build         # Build succeeds
npm test              # All tests pass
# [project-specific verification commands]
\`\`\`
```

---

## Phase 4: Generate the Prompt

### 4.1 Output Format

Produce the final prompt in this structure:

```markdown
# Task: [Concise title]

## Context
[Link to CLAUDE.md commercial use case / problem statement]
[Reference to project architecture and relevant patterns]

## Problem Statement
[From Phase 2.1]

## Solution Approach
[Selected solution from Phase 2.3]

## Implementation Plan
[From Phase 3.1]

## Success Criteria
[From Phase 3.2]

## Constraints
- Follow all patterns defined in CLAUDE.md
- [Project-specific constraints from CLAUDE.md critical patterns]
- [Manual review notes constraints, if any]
- Use [Opus/Sonnet] for [planning/implementation] phases

## Out of Scope
- [Explicitly list what this prompt does NOT cover]

## Files Likely Affected
- `path/to/file1.ts` — [what changes]
- `path/to/file2.ts` — [what changes]
```

### 4.2 Quality Checks

Before delivering the prompt, verify:
- [ ] Problem statement is specific and references actual project code/patterns
- [ ] Success criteria are testable with concrete verification commands
- [ ] Implementation plan follows the project's established patterns (from CLAUDE.md)
- [ ] Constraints don't conflict with CLAUDE.md directives
- [ ] Out of scope section prevents scope creep
- [ ] Files listed actually exist in the target project
- [ ] Prompt is self-contained — an agent can execute it without additional context

---

## Examples

### Input
> "I need to add email notifications to my task manager when tasks are overdue"

### Output
```markdown
# Task: Add Overdue Task Email Notifications

## Context
Digital Filofax (CLAUDE.md) — personal organization system managing tasks with
urgency calculations already implemented in `src/lib/urgency.ts`.

## Problem Statement
**What**: Tasks that pass their due date have no notification mechanism
**Why**: Users miss deadlines because the app is passive — no proactive alerts
**Where**: `src/server/api/routers/tasks.ts`, new notification service
**Current State**: Tasks have `dueDate` field, urgency scoring exists, no notification system
**Desired State**: Daily check sends email for tasks overdue by 1+ days
**Gap Analysis**: Missing: notification service, email integration, scheduled job

## Solution Approach
Add a tRPC procedure triggered by a cron job that queries overdue tasks
and sends digest emails via Resend API, following existing router patterns.

## Implementation Plan
### Phase 1: Foundation
- [ ] Add Resend SDK dependency
- [ ] Create notification preferences in Prisma schema
- [ ] Run db:generate and db:push

### Phase 2: Core Implementation
- [ ] Create `src/server/api/routers/notifications.ts` router
- [ ] Add `getOverdueTasks` procedure with user scoping
- [ ] Add `sendDigest` procedure that formats and sends email
- [ ] Register router in `root.ts`

### Phase 3: Integration
- [ ] Create API route for cron trigger
- [ ] Add notification preferences to settings page
- [ ] Write tests for notification router

## Success Criteria
### Must Have (P0)
- [ ] Overdue tasks correctly identified (dueDate < now, status != completed)
- [ ] Email sent with task list to user's email
- [ ] All queries user-scoped (userId: ctx.session.user.id)
- [ ] TRPCError used for all error cases

### Should Have (P1)
- [ ] User can disable notifications in preferences
- [ ] Email template is readable and well-formatted

### Verification Commands
npm run lint && npm run build && npm test

## Constraints
- All Zod string inputs must have .max() bounds
- All errors must use TRPCError
- Follow protectedProcedure pattern
- Use Opus 4.6 for planning, Sonnet 4.6 for implementation

## Out of Scope
- Push notifications (email only)
- Real-time notifications (batch digest only)
- SMS notifications
```
