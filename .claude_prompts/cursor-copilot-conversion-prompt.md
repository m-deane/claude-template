# Convert Claude Code Template → Cursor + GitHub Copilot Compatible Project

## Objective

Convert this Claude Code presentation-creator template into a project that works natively in **Cursor IDE** and **GitHub Copilot** (VS Code / Copilot Coding Agent). The result should be a single repository that supports all three tools simultaneously — Claude Code, Cursor, and Copilot — with each reading its own configuration format.

## Input: Current Claude Code Structure

```
CLAUDE.md                          # Project-wide instructions (always loaded)
.claude/
  CLAUDE.md                        # Behavioral directives (always loaded)
  agents/                          # 18 specialized sub-agents (YAML frontmatter + markdown)
    pptxgenjs-engineer.md
    reveal-js-engineer.md
    prompt-engineer.md
    context-manager.md
    code-reviewer.md
    ...
  commands/                        # 14 slash commands (YAML frontmatter + markdown)
    code-review.md
    generate-tests.md
    create-pr.md
    ultra-think.md
    ...
  skills/                          # MCP skill definitions
    mcp-builder/SKILL.md
    webapp-testing/SKILL.md
```

### Claude Code Format Reference

**Agent format** (`.claude/agents/*.md`):
```yaml
---
name: pptxgenjs-engineer
description: Specialist agent for generating PowerPoint presentations using pptxgenjs...
tools: Read, Write, Edit, Bash
model: sonnet
---

You are a specialist in pptxgenjs PowerPoint generation...
```

**Command format** (`.claude/commands/*.md`):
```yaml
---
allowed-tools: Read, Bash, Grep, Glob
argument-hint: [file-path] | [commit-hash] | --full
description: Comprehensive code quality review with security, performance, and architecture analysis
---

# Code Quality Review

Perform comprehensive code quality review: $ARGUMENTS
...
```

**Skill format** (`.claude/skills/*/SKILL.md`):
```markdown
# Skill Name

## When to use
...

## Process
...
```

---

## Output: Target Structure

Create all of the following files. The existing `.claude/` directory stays untouched — these new directories coexist alongside it.

### Part 1: Cursor IDE (`.cursor/`)

```
.cursor/
  rules/
    # Always-on rules (loaded every session)
    project-instructions.mdc       ← Root CLAUDE.md content
    behavior.mdc                  ← .claude/CLAUDE.md content

    # Auto-attached rules (loaded when matching files are open)
    pptxgenjs-engineer.mdc        ← .claude/agents/pptxgenjs-engineer.md
    reveal-js-engineer.mdc        ← .claude/agents/reveal-js-engineer.md
    presentation-pipeline.mdc     ← .claude_prompts/presentation-creator-prompt.md (summarized)

    # Agent-requested rules (AI decides when relevant based on description)
    prompt-engineer.mdc           ← .claude/agents/prompt-engineer.md
    context-manager.mdc           ← .claude/agents/context-manager.md
    code-reviewer.mdc             ← .claude/agents/code-reviewer.md
    task-decomposition.mdc        ← .claude/agents/task-decomposition-expert.md
    ui-ux-designer.mdc            ← .claude/agents/ui-ux-designer.md
    technical-researcher.mdc      ← .claude/agents/technical-researcher.md
    debugger.mdc                  ← .claude/agents/debugger.md
    test-engineer.mdc             ← .claude/agents/test-engineer.md
    typescript-pro.mdc            ← .claude/agents/typescript-pro.md
    python-pro.mdc                ← .claude/agents/python-pro.md
    sql-expert.mdc                ← .claude/agents/sql-expert.md
    ml-engineer.mdc               ← .claude/agents/ml-engineer.md

  commands/
    code-review.md                ← .claude/commands/code-review.md
    generate-tests.md             ← .claude/commands/generate-tests.md
    create-pr.md                  ← .claude/commands/create-pr.md
    refactor-code.md              ← .claude/commands/refactor-code.md
    explain-code.md               ← .claude/commands/explain-code.md
    security-scan.md              ← .claude/commands/security-scan.md
    architecture-review.md        ← .claude/commands/architecture-review.md
    ultra-think.md                ← .claude/commands/ultra-think.md
    dependency-update.md          ← .claude/commands/dependency-update.md
    update-docs.md                ← .claude/commands/update-docs.md
    todo.md                       ← .claude/commands/todo.md
    workflow-orchestrator.md      ← .claude/commands/workflow-orchestrator.md
    create-architecture-documentation.md
    generate-api-documentation.md

  mcp.json                        ← MCP server config (if any external servers used)
```

### Part 2: GitHub Copilot (`.github/`)

```
.github/
  copilot-instructions.md         ← Merged root CLAUDE.md + .claude/CLAUDE.md
  instructions/
    pptxgenjs.instructions.md     ← pptxgenjs rules (applyTo: **/*.cjs)
    revealjs.instructions.md      ← reveal.js rules (applyTo: **/*.html)
    presentation.instructions.md  ← presentation pipeline summary
  agents/
    pptxgenjs-engineer.agent.md
    reveal-js-engineer.agent.md
    prompt-engineer.agent.md
    code-reviewer.agent.md
    test-engineer.agent.md
    debugger.agent.md
    context-manager.agent.md
    technical-researcher.agent.md
    ui-ux-designer.agent.md
    task-decomposition.agent.md
    typescript-pro.agent.md
    python-pro.agent.md
    sql-expert.agent.md
    ml-engineer.agent.md
  prompts/
    code-review.prompt.md
    generate-tests.prompt.md
    create-pr.prompt.md
    refactor-code.prompt.md
    explain-code.prompt.md
    security-scan.prompt.md
    architecture-review.prompt.md
    ultra-think.prompt.md
  skills/
    mcp-builder/SKILL.md          ← Direct copy
    webapp-testing/SKILL.md       ← Direct copy

AGENTS.md                         ← Root-level behavioral directives (read by Copilot + others)
```

---

## Conversion Rules

### Rule 1: `.cursor/rules/*.mdc` Format

Every `.mdc` file has this structure:

```
---
description: <1-2 sentence description — Cursor uses this to decide when to auto-include>
globs: <optional file pattern, e.g., "**/*.cjs" — auto-attaches when matching files are open>
alwaysApply: <true|false — true means loaded in every session>
---

<markdown body — the actual instructions/rules>
```

**Conversion from Claude agent format:**
- DROP the `tools:` field (Cursor manages its own tool access)
- DROP the `model:` field (Cursor uses its configured model)
- KEEP the `description:` value — rewrite if needed to help Cursor decide when to include
- ADD `globs:` if the agent maps to specific file types
- ADD `alwaysApply: true` ONLY for project-wide behavioral rules (max 2-3 files)
- KEEP the full markdown body (the agent's instructions/expertise)

**Glob mappings for auto-attach:**
| Agent/Source | Glob |
|---|---|
| pptxgenjs-engineer | `**/*.cjs` |
| reveal-js-engineer | `presentations/**/*.html` |
| presentation-pipeline | `presentations/**` |
| typescript-pro | `**/*.ts, **/*.tsx` |
| python-pro | `**/*.py` |
| sql-expert | `**/*.sql` |

**Rules that should be `alwaysApply: true`:**
- `project-instructions.mdc` (root CLAUDE.md)
- `behavior.mdc` (.claude/CLAUDE.md)

All others should be `alwaysApply: false`.

### Rule 2: `.cursor/commands/*.md` Format

Cursor commands are **plain Markdown** — no YAML frontmatter.

```markdown
# Command Title

<instructions for what the command does>

Reference @project-instructions for project standards.
```

**Conversion from Claude command format:**
- DROP the `---` YAML frontmatter entirely (no `allowed-tools:`, no `argument-hint:`, no `description:`)
- REPLACE `$ARGUMENTS` with natural language like "the specified file or scope"
- REPLACE inline bash `!`command`` with instructions like "Check git status" (Cursor runs tools itself)
- KEEP the structured task steps
- ADD `@rulename` references where the command should pull in a specific rule for context

### Rule 3: `.github/copilot-instructions.md` Format

Single Markdown file, no frontmatter required. Merge both CLAUDE.md files:

```markdown
# Project Instructions

## Project Purpose
<from root CLAUDE.md>

## Behavioral Directives
<from .claude/CLAUDE.md>

## Technical Rules
<pptxgenjs rules, reveal.js rules — the critical stuff>

## Prohibited Patterns
<from .claude/CLAUDE.md>
```

Keep it under 500 lines. Prioritize the non-negotiable technical rules and prohibited patterns. Drop lengthy code examples — those belong in path-scoped instruction files.

### Rule 4: `.github/instructions/*.instructions.md` Format

```yaml
---
applyTo: "**/*.cjs"
description: "pptxgenjs technical rules for PowerPoint generation scripts"
---

<markdown body — rules specific to this file type>
```

- `applyTo:` is a glob pattern — equivalent to Cursor's `globs:`
- These are additive — they layer on top of `copilot-instructions.md`

### Rule 5: `.github/agents/*.agent.md` Format

```yaml
---
name: pptxgenjs-engineer
description: "Specialist in generating PowerPoint presentations using pptxgenjs"
tools: ["read", "edit", "execute", "search"]
model: claude-opus-4-6
---

<markdown body — the agent's expertise and rules>
```

**Conversion from Claude agent format:**
- KEEP `name:` and `description:`
- REPLACE `tools: Read, Write, Edit, Bash` with Copilot tool names: `["read", "edit", "execute", "search"]`
  - `Read` → `"read"`
  - `Write` / `Edit` → `"edit"`
  - `Bash` → `"execute"`
  - `Grep` / `Glob` → `"search"`
- REPLACE `model: sonnet` → `model: claude-sonnet-4-6` or `model: claude-opus-4-6`
- KEEP the full markdown body

### Rule 6: `.github/prompts/*.prompt.md` Format

```yaml
---
mode: agent
description: "What this slash command does"
tools: ["read", "edit", "execute", "search"]
---

<markdown body — the command instructions>
```

**Conversion from Claude command format:**
- ADD `mode: agent` (allows multi-step execution)
- MOVE `description:` from Claude frontmatter
- REPLACE `allowed-tools:` with Copilot `tools:` array (same mapping as agents)
- REPLACE `$ARGUMENTS` with `${input:description}` (Copilot's variable syntax)
- REPLACE `!`command`` with plain instructions
- KEEP the structured task steps

### Rule 7: `AGENTS.md` (Root Level)

Create a root-level `AGENTS.md` that serves as the universal agent instruction file. This is read by Copilot Coding Agent, and increasingly by other tools.

Structure it as a concise version of the behavioral directives + key technical rules. Keep it under 200 lines. Focus on:
- What this project produces (presentations)
- The 4-agent pipeline concept
- Non-negotiable pptxgenjs rules (the 11 silent-failure rules)
- Reveal.js rules
- Quality gates
- Prohibited patterns
- File organization (where things go)

### Rule 8: MCP Configuration

**Cursor** (`.cursor/mcp.json`):
```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "package-name"],
      "env": {}
    }
  }
}
```

**Copilot** (`.vscode/mcp.json`):
```json
{
  "servers": {
    "server-name": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "package-name"]
    }
  }
}
```

Only create these if the project actually uses MCP servers. The current skills (mcp-builder, webapp-testing) are instructional guides, not running servers — so MCP config files may not be needed unless you set up Playwright or other tool servers.

---

## What CANNOT Be Directly Converted

These Claude Code features have no equivalent and require workarounds:

| Feature | Workaround |
|---|---|
| **4-agent pipeline orchestration** | Document as a reference workflow in `presentation-pipeline.mdc` / `presentation.instructions.md`. The user manually invokes each step. |
| **Quality gates between agents** | Add checklist sections at the end of each agent's instructions: "Before proceeding, verify: ..." |
| **`TodoWrite` progress tracking** | Use a `todos.md` file convention or VS Code's built-in task tracking |
| **Per-agent model selection** | Cursor: not supported. Copilot: `model:` field in `.agent.md` works in IDE only. |
| **Inline bash in commands** (`!`cmd``) | Replace with natural-language instructions; the AI will run commands itself |
| **`$ARGUMENTS` variable substitution** | Cursor: describe expected input in prose. Copilot: use `${input:name}` syntax. |

---

## Execution Plan

1. **Read every file** in `.claude/agents/`, `.claude/commands/`, `.claude/skills/`, and `.claude_prompts/`
2. **Create `.cursor/rules/`** — convert each agent → `.mdc` with correct frontmatter
3. **Create `.cursor/commands/`** — convert each command → plain `.md`
4. **Create `.github/copilot-instructions.md`** — merge both CLAUDE.md files
5. **Create `.github/instructions/`** — path-scoped technical rules
6. **Create `.github/agents/`** — convert each agent → `.agent.md`
7. **Create `.github/prompts/`** — convert each command → `.prompt.md`
8. **Copy `.claude/skills/`** → `.github/skills/`
9. **Create `AGENTS.md`** at project root
10. **Verify** no existing files were modified — all changes are additive

## Quality Checks

After conversion, verify:
- [ ] `.claude/` directory is completely untouched
- [ ] Every `.mdc` file has valid YAML frontmatter with `description`, `globs` (if applicable), `alwaysApply`
- [ ] Only 2-3 `.mdc` files have `alwaysApply: true`
- [ ] Every `.agent.md` file has `name`, `description`, `tools` in frontmatter
- [ ] Every `.prompt.md` file has `mode`, `description` in frontmatter
- [ ] `copilot-instructions.md` is under 500 lines
- [ ] `AGENTS.md` is under 200 lines
- [ ] No `$ARGUMENTS` remains in any Cursor command file
- [ ] No `!`backtick`` inline bash remains in any Cursor command file
- [ ] No Claude-specific YAML keys (`allowed-tools:`, `model: sonnet`) remain in Cursor/Copilot files
- [ ] All pptxgenjs non-negotiable rules appear in at least one file for each tool (Cursor + Copilot)
