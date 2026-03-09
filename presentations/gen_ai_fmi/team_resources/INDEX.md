# FM&I Gen AI Upskilling — Team Resources

These files are reference templates produced during the FM&I Gen AI upskilling session. They are
ready to use: copy a folder into your Dataiku project root, follow the README, and the tool has
context about FM&I conventions from day one.

---

## Start here

Three actions in priority order:

**1. Get access (this week)**
- GitHub Copilot: raise an IT ticket — "Request access to GitHub Copilot under BP enterprise licence". No manager approval needed. Turnaround 2–3 days.
- Claude Code: install via `npm install -g @anthropic/claude-code`. Requires Anthropic API key — request through your line manager or the AI Tools budget holder.
- Cursor: download from cursor.com. Expense £20/month Pro plan under *Software / Developer Tools* via T&E.

**2. Add a context file to your next project (day one)**
Copy `claude_code_template/CLAUDE.md` (or `github_copilot_template/.github/copilot-instructions.md` for Copilot) into your Dataiku project root before you write a single line of code. This one file gives any AI tool immediate knowledge of your platform, dataframe library, domain terms, and compliance rules — so you stop re-explaining the same context in every prompt.

**3. Try one real task this week**
Pick a task from the list below and use whichever tool you have access to. Do not wait for the perfect task — use a real one:
- Paste a recipe that uses iterrows() and ask Claude to rewrite it in polars
- Ask Copilot to explain an unfamiliar pipeline and flag any issues
- Use the pipeline reviewer agent to audit a recipe before your next PR

---

## Template folders

| Folder | What it is | How to use |
|---|---|---|
| `claude_code_template/` | CLAUDE.md project context file + agent definition for the FM&I Dataiku expert | Copy folder into your Dataiku project root. Run `claude` in terminal. |
| `github_copilot_template/` | copilot-instructions.md pre-loaded with FM&I domain context and coding standards | Copy `.github/` into your project root. Works immediately in VS Code with Copilot active. |
| `cursor_template/` | .cursorrules file with FM&I context for the Cursor AI editor | Copy `.cursorrules` into project root. Open folder in Cursor. |
| `agent_examples/` | Reference examples showing agent and skill definitions | Read-only reference. Copy individual definitions into your `.claude/agents/` or `.claude/commands/` folders. |

---

## Agent examples

| File | What it demonstrates |
|---|---|
| `agent_examples/presentation-creator-agent.md` | Full agent definition format — YAML frontmatter, system prompt, tool list, output spec. Shows how to build any custom agent. |
| `agent_examples/dataiku-pipeline-reviewer.md` | A working, ready-to-copy agent for FM&I recipe review. Covers performance, Dataiku API, code quality, compliance, and test generation. Copy to `.claude/agents/dataiku-pipeline-reviewer.md`. |
| `agent_examples/skill-example-model-doc.md` | Explains agent vs skill (slash command). Shows the `/model-doc` skill that auto-generates MODEL.md from recipe code. |

---

## AI tools available at BP — quick reference

| Tool | What it does | Access route | Cost |
|---|---|---|---|
| GitHub Copilot | In-editor code completion and chat across your whole codebase | IT ticket: "Request access to GitHub Copilot under BP enterprise licence" | Free (BP enterprise licence) |
| Microsoft Copilot | General-purpose AI assistant in M365 (Teams, Word, Outlook) | Available now via M365 — open Teams and click the Copilot icon | Free (included in M365) |
| Claude Code | Agentic CLI that reads/writes your project files, runs commands, and works through multi-step tasks | Install: `npm install -g @anthropic/claude-code`. API key via line manager or AI Tools budget | API usage cost — check with line manager |
| Cursor | AI-native code editor (VS Code fork) with codebase-wide context | Download cursor.com | ~£20/month — expense via T&E |
| ChatGPT / Claude.ai | General-purpose AI chat | Personal accounts available; check BP data policy before using with work data | Personal cost; BP accounts available in some teams |

**Data policy reminder**: Only use publicly available or anonymised data with external AI tools. Never paste live positions, calibration parameters, counterparty names, or internal credentials into any AI tool. The templates in this folder include explicit guidance on what is and is not safe to share.

---

## Questions and next steps

- Internal AI tools guidance: BP Digital Tools > AI Tools (intranet)
- Claude Code docs: https://docs.anthropic.com/en/docs/claude-code
- Post questions in the FM&I team channel
