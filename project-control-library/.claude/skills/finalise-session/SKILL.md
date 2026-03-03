---
name: finalise-session
description: End-of-session housekeeping automation. Updates CLAUDE.md, consolidates plans, updates docs, commits to git, sorts project directories, generates status reports, and cleans root directories. Run this at the end of every work session.
---

# Finalise Session — End-of-Session Housekeeping

## Overview

Comprehensive end-of-session automation that ensures every managed project is left in a clean, documented, committed state. Consolidates plans, updates documentation, cleans directories, and generates status reports.

---

# Process

## Phase 1: Housekeeping

### 1.1 Consolidate Plans

Merge all `.claude_plans/*.md` files into a single unified plan:

```bash
# List all plan files in the target project
ls -la ~/projects/{target}/.claude_plans/*.md
```

**Consolidation rules:**
- Create/update `.claude_plans/UNIFIED_PLAN.md`
- Organize by implementation date (most recent first)
- Mark each item as: `[IMPLEMENTED]`, `[IN PROGRESS]`, or `[PLANNED]`
- Include timestamps for when each item was implemented
- Sync with CLAUDE.md — ensure CLAUDE.md references match actual implementation state

**Unified plan format:**
```markdown
# Unified Project Plan — {Project Name}
*Last updated: {date}*

## Implemented Features
| Feature | Implemented | Plan File | Notes |
|---------|-------------|-----------|-------|
| Task CRUD | 2026-01-15 | task-implementation.md | Core feature |
| Habit Tracker | 2026-02-01 | habit-plan.md | With streaks |

## In Progress
| Feature | Started | Plan File | Remaining Work |
|---------|---------|-----------|----------------|
| Collaboration | 2026-02-28 | collaboration-plan.md | Invitations UI |

## Planned
| Feature | Priority | Plan File | Dependencies |
|---------|----------|-----------|--------------|
| AI Suggestions | P2 | ai-plan.md | None |
```

### 1.2 Update Init / CLAUDE.md

Check if the project's CLAUDE.md needs updating:

- **Scale numbers** — update page count, test count, router count, model count if changed
- **Router list** — add any new routers registered in `root.ts`
- **Architecture** — update if new directories or patterns were added
- **Commands** — update if new scripts were added to package.json
- **Known trade-offs** — document any new intentional limitations

### 1.3 Update Documentation

For each managed project, update:

- **README.md** — ensure it reflects current project state
- **API documentation** — if routers/endpoints changed
- **Type documentation** — if types/schemas changed
- **Plan files** — mark completed items

---

## Phase 2: Directory Cleanup

### 2.1 Clean Root Directory

The project root should only contain standard files. Move everything else:

**Allowed in root:**
```
CLAUDE.md, README.md, STATUS.md, package.json, tsconfig.json,
next.config.ts, vitest.config.ts, tailwind.config.ts, postcss.config.mjs,
.gitignore, .eslintrc.json, .env.example, .env.local,
prisma/, src/, tests/, docs/, public/, .claude/, .claude_plans/,
.claude_prompts/, .claude_research/, node_modules/, .next/, .git/
```

**Files to relocate:**
| File Pattern | Destination |
|-------------|-------------|
| `*.md` (not README/CLAUDE/STATUS) | `docs/` |
| `*.py` | `scripts/` |
| `*.sh` | `scripts/` |
| `*.ipynb` | `notebooks/` |
| `*.json` (not package/tsconfig/config) | `config/` or `data/` |
| `*.log` | Delete or move to `.logs/` |
| `*.tmp`, `*.bak` | Delete |
| Misc research files | `.claude_research/` |

### 2.2 Sort Project Folders

Ensure consistent directory structure:

```bash
# Create standard directories if they don't exist
mkdir -p docs scripts notebooks

# Move misplaced files
# (Only move files that are clearly in the wrong location)
```

### 2.3 Remove Stale Files

Clean up temporary and generated artifacts:

```bash
# Remove common stale files (confirm with user first for anything uncertain)
find ~/projects/{target} -name "*.log" -mtime +7 -delete
find ~/projects/{target} -name "*.tmp" -delete
find ~/projects/{target} -name ".DS_Store" -delete
```

---

## Phase 3: Status Report

### 3.1 Generate STATUS.md

Create/update `STATUS.md` in the project root:

```markdown
# Project Status — {Project Name}
*Generated: {date}*

## Overview
- **Project**: {name from CLAUDE.md}
- **Stack**: {stack from CLAUDE.md}
- **Health**: {passing/failing} (lint: {ok/fail}, build: {ok/fail}, tests: {pass}/{total})

## Completed Items
- [x] {Feature 1} — {date completed}
- [x] {Feature 2} — {date completed}
- [x] {Feature 3} — {date completed}

## In Progress
- [ ] {Feature 4} — started {date}, {description of remaining work}

## Incomplete / Planned
- [ ] {Feature 5} — {priority}, {dependencies}
- [ ] {Feature 6} — {priority}, {dependencies}

## Recent Changes (Last Session)
- {Change 1}
- {Change 2}

## Known Issues
- {Issue 1}
- {Issue 2}

## Metrics
- **Pages**: {count}
- **Routers**: {count}
- **Models**: {count}
- **Tests**: {count} ({pass_rate}% passing)
- **Test Coverage**: {percentage}
```

---

## Phase 4: Git Commit

### 4.1 Review Changes

```bash
# Check what's changed
cd ~/projects/{target}
git status
git diff --stat
```

### 4.2 Commit with Descriptive Message

```bash
# Stage housekeeping changes (exclude secrets and env files)
# Verify .gitignore covers .env files before staging
git add -A ':!.env' ':!.env.local' ':!.env.production' ':!*.pem' ':!*.key'

# Commit with session summary
git commit -m "session: [summary of what was done this session]

Changes:
- [list of key changes]

Housekeeping:
- Consolidated plans into UNIFIED_PLAN.md
- Updated CLAUDE.md with current metrics
- Cleaned root directory
- Generated STATUS.md

[session-id]"
```

### 4.3 Push if Configured

Only push if the project has auto-push enabled in config:

```bash
# Check if auto-push is enabled
# If yes: git push origin {branch}
# If no: report that changes are committed but not pushed
```

---

## Phase 5: Final Report

### 5.1 Session Summary

```markdown
## Session Finalised — {Project Name}

### Housekeeping
- [x] Plans consolidated into UNIFIED_PLAN.md
- [x] CLAUDE.md updated (metrics, routers, architecture)
- [x] Documentation updated
- [x] Root directory cleaned ({n} files relocated)
- [x] STATUS.md generated
- [x] Git commit: {hash}

### Project Health
- Lint: {pass/fail}
- Build: {pass/fail}
- Tests: {pass}/{total}

### Files Modified This Session
{count} files across {directories}

### Next Session Recommendations
- {Recommendation 1 based on incomplete items}
- {Recommendation 2 based on discovered issues}
```

---

## Safety Rules

1. **Never delete files without confirming** they're truly stale/temporary
2. **Never modify .env files** — they may contain secrets
3. **Never force-push** — always regular push or report unpushed
4. **Always run tests before committing** — never commit broken code
5. **Preserve user's git branch** — don't switch branches during cleanup
6. **Back up before bulk moves** — if relocating many files, commit current state first
