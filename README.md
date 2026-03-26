# AI-Assisted Development Template

A project template with pre-configured rules for Claude Code, Cursor, and GitHub Copilot. Designed to reduce LLM hallucinations and produce consistent, working code.

## Features

- **Claude Code** - `.claude/` folder with rules, agents, commands, skills, and settings
- **Cursor** - `.cursorrules` and `.cursor/rules/` with glob-scoped rules
- **GitHub Copilot** - `.github/copilot-instructions.md` and chat instructions
- **Anti-hallucination rules** - Verification, grounding, and scope control guidelines
- **Specialized agents** for Python, TypeScript, SQL, ML, debugging, and more
- **14 slash commands** for code review, testing, architecture, security scanning

## Quick Start

### 1. Clone This Template

```bash
git clone https://github.com/your-username/claude-template.git my-project
cd my-project
rm -rf .git
git init
```

### 2. Customize for Your Project

1. **Edit `CLAUDE.md`** - Replace placeholders with your project overview, stack, and commands
2. **Edit `.cursorrules`** - Same content adapted for Cursor
3. **Edit `.github/copilot-instructions.md`** - Same content adapted for Copilot
4. **Edit `.claude/settings.json`** - Adjust allow/deny rules for your stack
5. **Copy `.claude/example_prompt.md`** - Use as a starting point for project requirements

### 3. Start Building

```bash
claude    # Open with Claude Code CLI
```

## Template Structure

```
your-project/
├── CLAUDE.md                          # Project context (CUSTOMIZE THIS)
├── .cursorrules                       # Cursor rules (CUSTOMIZE THIS)
├── .claude/
│   ├── CLAUDE.md                      # Core workflow directives
│   ├── settings.json                  # Tool permissions (allow/deny)
│   ├── rules/                         # Modular, path-scoped rules
│   │   ├── workflow.md                # Core workflow guidelines
│   │   ├── code-style.md             # Naming and style conventions
│   │   ├── testing.md                # Testing standards
│   │   └── api-conventions.md        # API conventions (path-scoped)
│   ├── agents/                        # 16 specialized agents
│   ├── commands/                      # 14 slash commands
│   ├── skills/                        # MCP skills
│   ├── TEMPLATE_GUIDE.md             # Customization guide
│   └── example_prompt.md             # Project prompt template
├── .cursor/
│   └── rules/                         # Cursor glob-scoped rules
│       ├── api-conventions.mdc
│       ├── ui-components.mdc
│       └── testing.mdc
├── .github/
│   ├── copilot-instructions.md        # GitHub Copilot instructions
│   └── copilot-chat-instructions.md   # Copilot Chat instructions
├── .claude_plans/                     # Planning documents
├── .claude_prompts/                   # Workflow prompts
├── .claude_research/                  # Research documents
├── src/                               # Source code
└── tests/                             # Test files
```

## Core Workflow Guidelines

These rules are enforced across all three AI tools:

**Implementation** - No mock data, no stubs, no TODOs. Complete working code only.

**Verification** - Verify files exist before importing. Check function signatures before calling. Confirm packages exist before installing. Validate schema before querying.

**Grounding** - Read actual source before modifying. Copy existing patterns. State assumptions explicitly. Ask rather than guess.

**Scope Control** - Restate the task first. Change only what's necessary. No unsolicited refactoring.

## Available Commands

| Command | Description |
|---------|-------------|
| `/ultra-think [problem]` | Deep multi-dimensional analysis |
| `/code-review [file]` | Comprehensive code review |
| `/generate-tests [component]` | Generate test suite |
| `/architecture-review` | Review architecture patterns |
| `/create-architecture-documentation` | Generate architecture docs |
| `/update-docs` | Update documentation |
| `/todo [action]` | Manage project todos |
| `/security-scan [scope]` | Security audit |
| `/explain-code [file]` | Detailed code explanation |
| `/create-pr [branch]` | Create PR with auto-generated description |
| `/dependency-update` | Check and update dependencies |

## Available Agents

| Agent | Use For |
|-------|---------|
| `python-pro` | Python optimization, best practices |
| `typescript-pro` | TypeScript type system, strict mode |
| `sql-expert` | Database design, query optimization |
| `ml-engineer` | ML pipelines, model training, MLOps |
| `test-engineer` | Test strategy, automation |
| `code-reviewer` | Code quality, security |
| `debugger` | Error investigation |
| `technical-researcher` | Technical research |
| `prompt-engineer` | AI prompt optimization |
| `ui-ux-designer` | UI/UX design |

## Customization

See [`.claude/TEMPLATE_GUIDE.md`](.claude/TEMPLATE_GUIDE.md) for detailed instructions.

## License

[Your License Here]
