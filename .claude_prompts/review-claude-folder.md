# Review .claude/ Folder Configuration

You are an expert in AI-assisted development tooling configuration. Your task is to audit a project's `.claude/` folder (and related AI assistant configuration) against established best practices, then generate corrected configurations and equivalent files for other AI coding tools.

## Instructions

Perform a comprehensive audit of the project's `.claude/` folder and related configuration files. Work through each section below sequentially. For every issue found, provide the exact fix -- do not just describe problems without solutions.

---

## Section 1: Audit the .claude/ Folder Structure

Check that the following structure exists and is properly organized:

```
.claude/
  CLAUDE.md          # Project-level instructions (checked into repo)
  CLAUDE.local.md    # Personal overrides (gitignored)
  settings.json      # Shared tool permissions (checked into repo)
  settings.local.json # Personal tool permissions (gitignored)
  rules/             # Modular, path-scoped instruction files
  commands/          # Slash command definitions
  skills/            # Skill definitions for complex workflows
  agents/            # Agent definitions with tool restrictions
```

Also check for the root-level `CLAUDE.md` file, which serves as the primary entry point.

Report:
- Which files and directories exist
- Which are missing and whether they are required or optional
- Any files present that do not belong

---

## Section 2: Audit CLAUDE.md Quality

Read every `CLAUDE.md` file in the project (root-level and `.claude/CLAUDE.md`). Evaluate each against these criteria:

### Length
- Must be under 200 lines. If over 200 lines, identify content that should be extracted into `rules/` files with path-scoped triggers.
- Aim for concise, high-signal content. Every line should change LLM behavior.

### Content Quality Checklist
- [ ] Contains a clear project overview (stack, architecture, purpose) in under 10 lines
- [ ] Lists essential development commands (dev, build, lint, test, database)
- [ ] Describes the data flow and key directories briefly
- [ ] Documents code conventions and naming standards
- [ ] Includes workflow guidelines that are actionable, not aspirational
- [ ] Avoids tutorial-style explanations of obvious concepts
- [ ] Avoids duplicating information that exists in README.md or package.json
- [ ] Uses concrete examples for patterns the LLM should follow (tRPC routers, component structure)
- [ ] Does not contain environment-specific paths, secrets, or personal preferences (those belong in CLAUDE.local.md)

### Duplication Check
- Compare root `CLAUDE.md` with `.claude/CLAUDE.md`. Flag any duplicated sections.
- Compare with `README.md`. Flag any content that is simply restated from the README without adding LLM-specific guidance.
- Each piece of information should live in exactly one place.

### Anti-Patterns to Flag
- Walls of text without structure
- Generic advice that applies to all projects ("write clean code")
- Excessive code examples that bloat the file beyond 200 lines
- Instructions that contradict each other between files
- Placeholder or TODO items

---

## Section 3: Verify settings.json

Check `.claude/settings.json` for proper allow/deny rules:

```json
{
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run build)",
      "Bash(npm run dev)",
      "Bash(npm run test)",
      "Bash(npx prisma *)",
      "Read(*)",
      "Write(src/**)",
      "Edit(src/**)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Write(.env*)",
      "Edit(.env*)",
      "Write(node_modules/**)",
      "Edit(node_modules/**)"
    ]
  }
}
```

Evaluate:
- Are common safe commands pre-approved to reduce permission prompts?
- Are destructive operations explicitly denied?
- Are sensitive files (.env, credentials) protected from writes?
- Are build artifacts and dependencies protected?
- Is the scope appropriately narrow (not blanket `Bash(*)` approval)?

If `settings.json` does not exist, generate one appropriate for the project's stack.

---

## Section 4: Check rules/ Folder

The `rules/` folder should contain modular, path-scoped rule files that activate only when relevant files are being edited. Check for:

### Structure
```
.claude/rules/
  frontend.md        # Triggers when editing src/app/** or src/components/**
  backend.md         # Triggers when editing src/server/**
  database.md        # Triggers when editing prisma/**
  testing.md         # Triggers when editing tests/**
  styling.md         # Triggers when editing *.css or tailwind config
```

### Each Rule File Should
- Start with a YAML frontmatter block specifying the path glob trigger (if supported)
- Contain focused, domain-specific instructions
- Not repeat content from the main CLAUDE.md
- Be under 50 lines each

### Evaluate
- Are rules properly scoped to relevant file paths?
- Is there content in CLAUDE.md that would be better as a scoped rule?
- Are there missing rule files for major areas of the codebase?

---

## Section 5: Verify .gitignore Entries

Check that the project's `.gitignore` includes:

```
CLAUDE.local.md
.claude/settings.local.json
```

These files contain personal preferences and local tool permissions that must not be committed. Flag if either is missing from `.gitignore`.

---

## Section 6: Check commands/ Structure

If a `commands/` directory exists, verify:

```
.claude/commands/
  fix-lint.md        # Example: run lint and fix all issues
  deploy.md          # Example: deployment workflow
  review.md          # Example: code review checklist
```

Each command file should:
- Have a clear, descriptive filename
- Contain a single coherent workflow
- Use `$ARGUMENTS` placeholder for dynamic input if needed
- Not duplicate functionality available through standard CLI commands

If no `commands/` directory exists, suggest 2-3 useful project-specific commands based on the codebase.

---

## Section 7: Check skills/ Structure

If a `skills/` directory exists, verify each skill file:
- Describes a complex, multi-step workflow
- Includes context about when to use it
- References specific project files and patterns

---

## Section 8: Check agents/ Configuration

If an `agents/` directory exists, verify each agent definition:

### Required Fields
- `name` - Clear identifier for the agent's purpose
- `model` - Specified model (do not default to most expensive)
- `tools` - Restricted to only the tools the agent needs

### Tool Restriction Principle
Agents should follow the principle of least privilege. A code review agent does not need file write permissions. A documentation agent does not need bash access.

### Flag These Issues
- Agents with unrestricted tool access
- Agents without a specified model field
- Agents whose purpose overlaps significantly with another agent
- Agent names that do not clearly describe their function

---

## Section 9: Generate Cross-Tool Equivalent Configurations

Based on the audited `.claude/` configuration, generate equivalent configuration files for other AI coding tools.

### 9a: Cursor Configuration

Generate `.cursorrules` (root-level) with the core project instructions, adapted for Cursor's format:

```
# Project: [Name]
# Stack: [Technologies]

[Consolidated project instructions from CLAUDE.md, optimized for Cursor]
```

Generate `.cursor/rules/` directory files mirroring the `.claude/rules/` structure, using Cursor's MDC format with frontmatter:

```markdown
---
description: [When this rule applies]
globs: ["src/app/**", "src/components/**"]
alwaysApply: false
---

[Rule content]
```

### 9b: GitHub Copilot Configuration

Generate `.github/copilot-instructions.md` with consolidated project instructions:

```markdown
# Copilot Instructions

[Project context and conventions adapted for GitHub Copilot's instruction format]
```

Note: GitHub Copilot's instruction file is a single flat file. Consolidate the most important rules from CLAUDE.md and the rules/ folder into this one file, prioritizing the instructions that most impact code generation quality.

### 9c: Adaptation Notes
For each generated file, note:
- What was included vs excluded (and why)
- Format differences between tools
- Limitations of the target tool's configuration system

---

## Section 10: Verify Core Workflow Guidelines

The CLAUDE.md (or equivalent configuration) must include comprehensive workflow guidelines. Check that the following are present, and add any that are missing:

### Required Workflow Guidelines

```
WORKFLOW - Core Guidelines:
- Never use mock data, results or workarounds
- Implement tests after every checkpoint and verify all tests pass
- Only update progress and create planning documents in the designated plans folder
- Write all tests to the tests/ folder
- Do not leave files in the root directory - sort into appropriate folders
- Always run lint and build commands to verify changes before completing
- Read and understand existing code before modifying it
- Match the style and patterns of surrounding code
- Make atomic, focused changes - one logical change per unit of work
- Never commit secrets, credentials, API keys, or .env files
- Handle all UI states: loading, error, empty, and success
- Validate at system boundaries; trust internal code and framework guarantees
- Prefer editing existing files over creating new ones
- Verify changes compile and pass linting before marking complete
- Write self-documenting code with clear naming over excessive comments
- Delete dead code completely - no commented-out blocks or unused imports
```

For each guideline:
- Is it present in the configuration? (yes/no)
- If present, is it clearly stated or buried in surrounding text?
- If missing, where should it be added?

Flag any workflow guidelines that contradict each other or conflict with project-specific patterns.

---

## Output Format

Structure your response as follows:

### Audit Summary
A table listing each section (1-10) with a status of PASS, WARN, or FAIL and a one-line summary.

### Critical Issues
List any FAIL items with the exact fix required. Show the file path, the current content (if any), and the corrected content.

### Recommendations
List WARN items ranked by impact. For each, explain why it matters and provide the fix.

### Generated Files
Output the complete contents of each generated file:
1. Corrected `.claude/CLAUDE.md` (if changes needed)
2. Corrected `.claude/settings.json` (if changes needed)
3. Any new `.claude/rules/*.md` files
4. `.cursorrules`
5. `.cursor/rules/*.mdc` files
6. `.github/copilot-instructions.md`

For each generated file, wrap the content in a code block with the file path as a header so it can be directly copied into place.
