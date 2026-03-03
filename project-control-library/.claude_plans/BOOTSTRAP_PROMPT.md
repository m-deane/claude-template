# Bootstrap Prompt: Project Control Library

> **This is the master prompt to initialize and develop the project-control library.**
> Copy this into a new Claude Code session opened at `~/projects/project-control-library/`.

---

## Prompt

You are initializing a **Project Control Library** — a meta-orchestration system that sits in `~/projects/` with access to all sibling project repositories. It uses `claude-template` as its base and provides skills, commands, agents, and batch operations to manage multiple Claude Code sessions across a developer's entire project portfolio.

### Problem Statement

Managing multiple software projects with Claude Code requires constant manual context-switching, repetitive housekeeping, inconsistent documentation, and fragmented orchestration. This library solves that by providing:

1. **Prompt generation** (`give-me-a-prompt` skill) — reads a target project's CLAUDE.md, diagnoses the problem, creates implementation plans with testable success criteria
2. **Demo notebooks** (`create-demo-notebooks` skill) — auto-generates Jupyter notebooks showcasing project features from CLAUDE.md and source analysis
3. **Agent teams** (`create-an-agent-team` skill) — designs and deploys multi-agent teams using Opus 4.6 for planning/review and Sonnet 4.6 for implementation, with token tracking
4. **Service launching** (`launch` skill) — starts services on unused ports only, never kills other projects' processes, maintains a central port registry
5. **Session cleanup** (`finalise-session` skill) — consolidates plans, updates docs, commits to git, sorts directories, generates status reports
6. **Batch operations** — cross-project commits, doc updates, reviews, production readiness checks, housekeeping, rule propagation
7. **Catalog system** — registry of all skills, hooks, plugins, and agents across all managed projects

### Architecture

```
~/projects/
├── project-control-library/     ← THIS PROJECT (control plane)
│   ├── CLAUDE.md                ← Project instructions (provided)
│   ├── .claude/                 ← Skills, commands, agents (provided)
│   ├── scripts/                 ← Python/bash utilities (provided)
│   ├── catalog/                 ← JSON registry of all items (provided)
│   ├── config.json              ← Global configuration (provided)
│   └── status/                  ← Per-project status files (generated)
├── claude-template/             ← Base template (reference)
├── project-a/                   ← Managed project
└── project-b/                   ← Managed project
```

### What Has Been Created (Foundation)

The following files are already in place and should be treated as the foundation:

**Core Configuration:**
- `CLAUDE.md` — Full project instructions with problem statement, architecture, model strategy, quality gates
- `.claude/CLAUDE.md` — Behavioral directives: model selection rules, prohibited patterns, post-task protocol
- `config.json` — Global settings: port registry, token budget, model assignments, housekeeping rules

**5 Skills (in `.claude/skills/`):**
- `give-me-a-prompt/SKILL.md` — 4-phase prompt generation (context → diagnosis → plan → generate)
- `create-demo-notebooks/SKILL.md` — 3-phase notebook creation (discovery → generation → output)
- `create-an-agent-team/SKILL.md` — 4-phase agent orchestration (plan → review → implement → post-task)
- `launch/SKILL.md` — 3-phase safe launch (port discovery → launch → verification)
- `finalise-session/SKILL.md` — 5-phase session cleanup (housekeeping → cleanup → status → commit → report)

**8 Batch Commands (in `.claude/commands/`):**
- `batch-commit.md`, `batch-update-docs.md`, `batch-init.md`, `batch-review.md`
- `batch-production-readiness.md`, `batch-housekeeping.md`, `batch-update-rules.md`, `catalog.md`

**4 Utility Scripts (in `scripts/`):**
- `port-manager.py` — Safe port allocation with registry
- `project-scanner.py` — Discover and index all repos
- `token-tracker.py` — Token usage monitoring and budget
- `housekeeping.sh` — Directory cleanup automation

**Catalog (in `catalog/`):**
- `skills.json`, `agents.json`, `commands.json` — Registry of all items

### Your Task

Using the foundation above, implement the following in order:

#### Phase 1: Validate and Harden (Opus 4.6)
1. Read every file in this project and verify internal consistency
2. Ensure all cross-references between CLAUDE.md, skills, commands, and config are accurate
3. Add any missing edge case handling to the utility scripts
4. Create `catalog/plugins.json` and `catalog/hooks.json` (empty initial catalogs)

#### Phase 2: Project Scanner Integration (Sonnet 4.6)
1. Run `python scripts/project-scanner.py` to discover all projects in `~/projects/`
2. Register discovered projects in `config.json`
3. Generate initial `status/{project-name}.status.md` files for each discovered project
4. Verify the port manager works: `python scripts/port-manager.py --scan`

#### Phase 3: Template Linking (Sonnet 4.6)
1. Create a symlink or reference from `templates/claude-template/` to `~/projects/claude-template/`
2. Verify the `batch-init` command can read the template's `.claude/` directory
3. Test `batch-update-rules` in dry-run mode against one project

#### Phase 4: Skill Testing (Sonnet 4.6)
1. Test `give-me-a-prompt` by generating a prompt for one of the discovered projects
2. Test `launch` by starting a documentation server for this project on an available port
3. Test `finalise-session` on this project (it should consolidate plans, clean root, generate STATUS.md)

#### Phase 5: Documentation (Sonnet 4.6)
1. Generate `STATUS.md` for this project
2. Ensure CLAUDE.md metrics are accurate
3. Commit everything with a descriptive message

### Model Strategy (MANDATORY)

| Task Type | Model | Examples |
|-----------|-------|---------|
| Planning, architecture, review | Opus 4.6 | Phase 1, agent team planning, problem diagnosis |
| Implementation, code generation | Sonnet 4.6 | Phases 2-5, writing code, editing files |
| Quick lookups, status checks | Haiku 4.5 | Port checks, file existence, simple queries |

### Success Criteria

#### Must Have (P0)
- [ ] All 5 skills have complete, consistent SKILL.md files
- [ ] All 8 batch commands are functional
- [ ] Port manager correctly identifies used/available ports
- [ ] Project scanner discovers and registers all projects
- [ ] Token tracker can log and report usage
- [ ] Housekeeping script cleans directories without data loss
- [ ] `config.json` accurately reflects discovered projects and port state
- [ ] No orphaned files in project root after finalise-session

#### Should Have (P1)
- [ ] Catalog system shows all skills/commands/agents across all projects
- [ ] STATUS.md generated for every managed project
- [ ] `batch-review` produces a meaningful health scorecard
- [ ] Template linking works for `batch-init` and `batch-update-rules`

#### Nice to Have (P2)
- [ ] Demo notebook generated for at least one project
- [ ] Agent team tested end-to-end on a small task
- [ ] Token budget alerts working when threshold exceeded

### Constraints
- Never modify files in managed projects unless explicitly invoked via a skill or command
- Never kill processes on ports owned by other projects
- Always run a project's own test suite before committing changes to it
- All Zod/Pydantic inputs validated with bounds
- No `console.log` or `print()` in production paths (scripts are fine)
- Use the cheapest model that can handle each subtask
- Follow all patterns defined in CLAUDE.md (this project's and each target project's)

### Post-Implementation Protocol
After completing all phases:
1. Run `bash scripts/housekeeping.sh .` to clean this project
2. Generate `STATUS.md` with completed/incomplete items
3. Update `CLAUDE.md` if any metrics changed
4. Commit with message: `feat: initialize project-control-library with 5 skills, 8 commands, 4 scripts, and catalog system`
5. Push to designated branch

---

*This prompt was generated by the project-control-library bootstrap process. Date: 2026-03-03.*
