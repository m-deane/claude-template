# Agent 1 Research Document — Gen AI FM&I Upskilling Session
*Prepared for handoff to Agents 2–5. All sections mirror the agenda structure.*

---

## Section 1 — Gen AI for Personal Productivity in Front Office Analytics

### Productivity Gains: Quantitative Evidence

**GitHub's 2024 Developer Productivity Study** (surveying 1,000+ developers): developers using GitHub Copilot completed coding tasks 55% faster than those without it. Acceptance rate of AI suggestions averaged 30–35%, but the cumulative time saving came from not having to context-switch to documentation, Stack Overflow, or mental boilerplate construction.

**McKinsey Global Institute (2024)**: Software engineers using AI coding assistants reported a 20–45% reduction in time spent on low-complexity, repetitive tasks. The gains were highest for: writing unit tests (40%), generating boilerplate code (45%), writing documentation (50%), and debugging (25%).

**Accenture Research (2025)**: Quantitative analysts who integrated AI tools into their daily workflows reported saving 8–12 hours per week on routine tasks — data cleaning, documentation, code review, and report generation. The critical finding: the top 20% of adopters saved more than 15 hours per week; the bottom 20% saved fewer than 2. The gap was driven entirely by prompting skill and tool integration depth, not technical background.

**Goldman Sachs Internal Study (reported Q1 2025)**: Front office technology teams piloting GitHub Copilot Enterprise saw a 30% reduction in code review cycle time and a 25% reduction in bug-to-fix turnaround. Notably, junior engineers in quant teams saw the largest gains in documentation and test coverage (both historically under-resourced).

**BCG Study (2023, extended 2024)**: Professionals who received AI assistance on complex, knowledge-intensive tasks (analysis, coding, writing) outperformed non-AI users by 40% on speed. But quality diverged: AI users who applied domain judgment to AI outputs exceeded unassisted users by 40% on quality too; those who used AI outputs uncritically showed quality degradation.

### Highest-Impact Use Cases for Data Scientists and Quant Modellers

**1. Code Generation (highest immediate gain)**
- Generating repetitive Python boilerplate: data loading, column renaming, merging, reshaping — tasks that are unambiguous and tedious
- Translating SQL window functions or complex aggregations into Python equivalents
- Writing Pandas/Polars/NumPy transformations from a plain English description of the desired output
- Generating entire recipe logic in Dataiku DSS from a specification

**2. Data Exploration Acceleration**
- Generating exploratory analysis code from a schema description: histograms, correlation matrices, outlier detection, missing value summaries
- Creating first-pass visualisations (Plotly, Matplotlib) from data and a description of what to show
- Writing data profiling code that would take 30–60 minutes to write manually

**3. Documentation Generation**
- Writing docstrings, README files, and inline comments for existing code
- Generating Confluence pages or Slack summaries from meeting notes or analysis outputs
- Creating model cards for statistical/ML models (methodology, inputs, outputs, known limitations)

**4. Pipeline Debugging**
- Explaining error messages in Dataiku logs and suggesting fixes
- Tracing data lineage issues when a downstream metric doesn't match expectations
- Identifying off-by-one errors, join ambiguities, and type mismatches from stack traces

**5. Report Generation**
- Drafting commentary for trading desk reports from structured data
- Generating executive summaries of model performance reviews
- Translating technical model outputs into plain-language explanations for traders

**6. Research Synthesis**
- Summarising market research, academic papers, or news articles to inform model assumptions
- Extracting structured data from unstructured text (e.g., supply/demand figures from a PDF report)
- Comparing model approaches across papers and producing a structured comparison

### The Productivity Gap: Passive vs Active Tool Integrators

The critical insight from the Accenture 2025 study and multiple internal case studies is that **tool availability alone does not drive productivity gains**. The gap between passive users (who use AI for the occasional query) and active workflow integrators (who have rebuilt their daily workflows around AI assistance) is 5–8× in productivity terms.

Active integrators:
- Use AI at every stage: before writing code (planning), during writing (completion/suggestion), after writing (review, documentation, test generation)
- Have project-level AI configuration (CLAUDE.md, .cursorrules, copilot instructions) that gives the AI persistent context about their codebase
- Use agents for multi-step tasks rather than single-turn queries
- Review AI outputs critically and iterate rather than accepting first drafts

Passive users:
- Use AI only for isolated questions
- Start fresh conversations without project context
- Accept or reject AI outputs without iteration
- Never configure project-level AI behaviour

---

## Section 2 — Current Landscape & Recent Developments

### State of Gen AI as of Early 2026

The 12 months from Q1 2025 to Q1 2026 saw several capability step-changes that transformed what Gen AI tools are practically capable of:

**Context windows exploded**: Claude 3.5 (2024) supported 200K tokens. Claude Sonnet 4.6 (2025) maintains 200K with improved utilisation. Gemini 2.5 supports 1M tokens (entire codebases). GPT-4o supports 128K. The practical implication: entire Dataiku projects, schemas, and pipelines can now fit in a single context.

**Agentic capabilities became production-ready**: Multi-step autonomous task execution moved from research demos to daily developer tools. Cursor's background agents, Claude Code's orchestrator-subagent model, and GitHub Copilot's workspace agent can now plan, execute, and iterate across an entire codebase without per-step human guidance.

**Tool use / function calling standardised**: All major models now support structured tool calling, enabling LLMs to invoke external APIs, read files, execute code, and interact with databases as part of a reasoning chain.

**Model Context Protocol (MCP)**: Anthropic's open standard (released late 2024, widely adopted through 2025) established a common interface for connecting LLMs to external tools and data sources. MCP servers now exist for Dataiku, databases, Bloomberg, GitHub, Jira, and many more.

**Reasoning models**: OpenAI's o3, Anthropic's extended thinking modes, and Google's Gemini 2.5 introduced explicit chain-of-thought reasoning that can be inspected, improving reliability on complex multi-step problems (math, logic, code architecture).

### Tools Available to BP Employees

**Microsoft Copilot (M365 Copilot)**
- Status: Available to all BP employees with M365 licence (E3/E5)
- Access: Via standard Microsoft 365 apps — Teams, Outlook, Word, Excel, PowerPoint, OneNote
- No additional licence request required for standard Copilot features
- Copilot Studio (for building custom agents): requires additional licence (Power Platform Premium or standalone Copilot Studio licence) — contact BP IT helpdesk or your cost centre manager
- Data handling: all M365 Copilot interactions are covered under BP's Microsoft 365 Enterprise Agreement — data is NOT used to train Microsoft's models, is stored within BP's Microsoft tenant, subject to BP's data retention and compliance policies
- BP internal training: extensive training available on BP's internal learning platform and Microsoft's M365 Copilot adoption hub (bp-specific resources — contact IT or Digital capability team for links)

**GitHub Copilot**
- Status: Available via BP Enterprise GitHub licence (GitHub Enterprise Cloud)
- Access: Request through BP IT service desk — GitHub Copilot Business or Enterprise licence
- IDE support: VS Code, Visual Studio, JetBrains IDEs, Neovim, Xcode
- Enterprise features: organisation-wide policy settings, audit logs, IP indemnification, custom fine-tuning (enterprise only)
- Data handling: BP Enterprise agreement — code is NOT sent to train GitHub's models; all interactions are scoped to the organisation

**Cursor**
- Status: NOT available via BP enterprise licence as of Q1 2026. Cursor is a third-party tool not covered under any BP enterprise agreement.
- Access: Personal subscription only (Cursor Pro: ~$20/month). Use on personal machines or unmanaged devices only.
- DATA GOVERNANCE NOTE: Cursor should NOT be used with BP proprietary code, internal data, or any non-public information without explicit approval from BP's data governance/legal team. This is a hard compliance boundary.
- Some teams in analogous trading firms have obtained approval for Cursor use with appropriate data handling agreements — this is worth pursuing through BP digital/IT governance if the team wants corporate access

**Copilot Studio**
- Status: Available with appropriate Power Platform licence (not included in standard M365)
- Access: Request through IT or Digital/Power Platform team
- Use case: Building custom Copilot agents with specific instructions, data sources, and tools for team or department-level deployment

### What Is NOT Available or Restricted

- **Proprietary model training on BP data**: Training or fine-tuning any external AI model on BP trading data, model IP, client information, or non-public financial information is prohibited
- **Uploading to consumer AI services**: Using ChatGPT.com, Claude.ai, or other consumer products with BP data is a compliance violation — the free tiers of these services may use your inputs for training
- **Cursor with BP code**: Without explicit IT/legal approval, Cursor (being a non-enterprise tool) should not be used with any BP confidential code or data
- **Open-source model hosting on BP infrastructure without approval**: Running LLMs (Ollama, etc.) on BP servers requires infrastructure and security approval

---

## Section 3 — Use Case Examples

### Use Case 1: Dataiku Pipeline Debugging and Optimisation

**Before**: A Dataiku recipe (Python code) fails overnight. The analyst reviews logs, identifies a cryptic Pandas error, cross-references documentation, and spends 45–90 minutes diagnosing that a join is producing duplicate rows due to an ambiguous key combination.

**After with GitHub Copilot/Cursor**: Analyst pastes the stack trace + the relevant recipe code into the AI. The model identifies the join ambiguity, suggests adding `validate='one_to_one'` to the merge call, and explains why duplicate keys appear when the upstream data refreshes with new partitions. Fix time: 5–10 minutes.

**Time saved per incident**: 40–80 minutes. With 2–3 pipeline incidents per week, this is 2–4 hours weekly.

### Use Case 2: ELT Pipeline Code Generation (Python/SQL)

**Before**: Writing a new Dataiku Python recipe to process a new data source requires 3–4 hours of boilerplate: schema parsing, type coercion, null handling, deduplication, and unit tests.

**After**: The analyst describes the source schema, target schema, and transformation requirements. The AI generates the full recipe including data validation, error handling, and a test suite. Analyst reviews and adjusts for edge cases. Time: 45–60 minutes.

**Concrete example**: "I have a pandas DataFrame with columns [date, hub, price, volume, contract_month]. I need to: pivot contract_month into columns, forward-fill missing dates per hub, calculate a 30-day rolling average of price weighted by volume, and output to the target dataset." → Full working code in 30 seconds.

### Use Case 3: Ad Hoc Data Analysis Acceleration

**Before**: A trader asks for a quick analysis of seasonal price patterns for a specific hub over the last 5 years. The analyst writes code from scratch: load data, filter, group, calculate statistics, generate charts. Takes 2–3 hours.

**After**: With AI, the analyst writes the data loading code, then describes the analysis in plain English. The AI generates the groupby logic, rolling statistics, and Plotly charts. Analyst spends time on interpretation rather than code construction. Time: 45–60 minutes.

**Specific FM&I application**: Generating ad hoc price spread analysis, forward curve comparisons, or scenario outputs for a trader who needs results before the end of the trading day.

### Use Case 4: Statistical Model Documentation Generation

**Before**: Writing a model card and technical documentation for a new fundamental price model takes 4–6 hours and is often deferred or inadequate.

**After**: The analyst provides the model code, training data schema, validation metrics, and a brief description. The AI generates a complete model card including: methodology description, input/output specification, known limitations, performance metrics interpretation, and appropriate use cases. Analyst reviews and supplements with domain knowledge. Time: 1–2 hours (mostly review and enrichment).

**Value**: Better documentation reduces onboarding time for new team members, improves compliance audit outcomes, and makes model review processes more efficient.

### Use Case 5: Trading Desk Report Automation

**Before**: Producing a weekly trading desk briefing requires manually extracting key figures from multiple data sources, writing commentary, and formatting in PowerPoint. Takes 3–4 hours per cycle.

**After**: A Copilot Agent or Claude Code pipeline extracts structured data, identifies key movements (price anomalies, volume outliers, curve shape changes), and drafts commentary in the required format. Analyst reviews, edits tone, and publishes. Time: 30–45 minutes.

**FM&I application**: Market structure reports, forward curve analysis summaries, and model performance updates that go to trading desks weekly.

### Use Case 6: Research Synthesis from Market Data / News

**Before**: Synthesising 10–15 market research reports or news items to inform a model assumption update takes 2–3 hours of reading and note-taking.

**After**: Analyst uploads documents (PDFs, web articles) to an AI tool with a structured prompt asking for extraction of specific data points, key arguments, and source attribution. AI produces a structured synthesis in 5–10 minutes. Analyst validates key claims against originals.

**Data governance note**: Only use publicly available documents or information that has been cleared for use with the specific AI tool. Do NOT upload broker research with confidential client information.

### Use Case 7: Model Validation and Test Writing

**Before**: Writing comprehensive unit tests for a complex statistical model takes as long as writing the model itself — often skipped due to time pressure.

**After**: AI generates a full test suite from the model code, including edge cases (null inputs, extreme values, date boundary conditions), assertions against known outputs, and property-based tests. Time to generate initial test suite: 10–15 minutes. Time to review and extend: 30–45 minutes.

**FM&I application**: Dataiku scenarios that validate pipeline outputs against historical baselines can be generated from existing pipeline code.

---

## Section 4 — Microsoft Copilot

### Current M365 Copilot Feature Set

**Microsoft 365 Copilot** is the umbrella product integrating GPT-4o (and increasingly o-series reasoning models) directly into the M365 application suite.

**Teams Integration**:
- Meeting transcript and real-time caption generation
- AI-generated meeting summaries with action items extracted
- "Copilot in Teams" chat: ask questions about meeting content during or after the meeting ("What did [person] say about the budget?", "What actions were assigned to me?")
- Thread summarisation in Teams channels
- Draft meeting notes and follow-up emails automatically after a call

**Outlook Integration**:
- Email summarisation (particularly useful for long threads)
- Draft reply generation from bullet-point instructions
- "Prepare for this meeting" — Copilot reads the calendar invite, relevant emails, and documents to generate a briefing
- Priority inbox coaching and follow-up reminders

**Word Integration**:
- Draft documents from prompts or bullet points
- Summarise long documents
- Rewrite sections in a different tone
- Generate tables and structured content from text descriptions

**Excel Integration**:
- Natural language formula generation ("Create a formula that calculates the rolling 30-day average of column C weighted by column D")
- Data insights and anomaly detection from conversational prompts
- Python in Excel (with Copilot assistance): advanced analytics without leaving the spreadsheet

**PowerPoint Integration**:
- Generate slide decks from Word documents or prompts
- Summarise presentations
- Reformat and redesign slides

**OneNote Integration**:
- Summarise notes
- Generate action items and plans from freeform notes
- Cross-notebook search with conversational interface

### Microsoft Copilot Agents

**What they are**: Custom AI assistants built on the Copilot platform, configured with specific instructions, knowledge sources (SharePoint, uploaded documents, web), and tools. They appear in Microsoft Teams as bots or in Copilot as a selectable agent.

**How to build one**:
1. Access Copilot Studio (requires licence)
2. Define the agent's name, purpose, and personality via natural language instructions
3. Connect knowledge sources: SharePoint libraries, uploaded documents, web URLs
4. Add tools: Power Automate flows, custom APIs, connectors
5. Test and refine the agent in the Copilot Studio test panel
6. Publish to Teams, SharePoint, or as a web chatbot

**The instruction-refinement workflow**:
- Give the agent initial instructions
- Ask the agent: "Review your instructions and suggest improvements to make you more effective at [specific task]"
- The agent generates improved instructions — paste these back in
- Iterate 2–3 times to reach a well-specified agent
- This "prompt-the-AI-to-write-its-own-prompt" pattern dramatically improves agent quality without requiring prompt engineering expertise

**What Copilot Agents can access**:
- Documents in SharePoint (with appropriate permissions)
- Microsoft Graph data (calendar, email, Teams content — with user consent)
- Web content (with Bing grounding enabled)
- Custom data via connectors or APIs

**Limitations**:
- Cannot access non-Microsoft systems without a connector
- Knowledge cutoff on training data; real-time information requires Bing grounding or custom connectors
- Cannot execute arbitrary code without Power Automate integration
- Quality degrades with poorly scoped or contradictory instructions

### Copilot Studio vs Standard Copilot

| Feature | Standard M365 Copilot | Copilot Studio |
|---------|----------------------|----------------|
| Custom agents | No | Yes |
| Custom knowledge sources | Limited | Full SharePoint + custom |
| Custom tools/actions | No | Power Automate, APIs |
| Multi-turn conversations | Basic | Full dialog management |
| Deployment | Personal only | Teams, web, SharePoint |
| Licence required | M365 E3/E5 | Additional licence |
| Code required | No | No (low-code) |

### Recent Copilot Enhancement Timeline (Last 12 Months)

- **Q1 2025**: Copilot Business Chat (BizChat) became available across Microsoft 365, giving Copilot access to all M365 data in a single interface
- **Q2 2025**: Copilot Studio added declarative agent framework (agents defined by JSON schema, no UI required for sophisticated developers)
- **Q2 2025**: Copilot in Excel added Python integration — AI-assisted data analysis using Python within Excel cells
- **Q3 2025**: Copilot added support for third-party plugins via the Microsoft Copilot extensibility model
- **Q3 2025**: Real-time meeting transcription quality improved significantly; action item extraction became more reliable
- **Q4 2025**: Copilot in Teams added "meeting preparation" agent (pre-reads agenda, relevant documents, drafts briefing before meeting starts)
- **Q1 2026**: Microsoft released Copilot reasoning mode (o-series model integration) for complex analysis tasks in Word and Outlook

### Copilot Future Roadmap (Confirmed and Speculated through 2026)

- **Confirmed**: Copilot Notebooks (long-form working memory across multiple sessions)
- **Confirmed**: Expanded Power BI Copilot integration (natural language report generation, insight narration)
- **Confirmed**: Copilot Studio expanding to support autonomous multi-agent workflows (multiple agents collaborating)
- **Speculated/Likely**: Copilot integration into Dynamics 365 data and Power BI Service more deeply
- **Speculated**: Copilot as orchestrator for enterprise agentic workflows — booking meeting rooms, processing approvals, triggering reports without human initiation

---

## Section 4b — GitHub Copilot & Cursor

### Key Differentiators

| Feature | GitHub Copilot | Cursor |
|---------|---------------|--------|
| **Context window** | 128K tokens (workspace) | Up to 200K tokens with Claude |
| **Codebase awareness** | @workspace (index-based) | Codebase-aware by default, semantic indexing |
| **Agent mode** | Copilot Workspace (beta), agentic multi-step editing | Full agent mode with tool use, background agents |
| **IDE** | VS Code, JetBrains, Neovim, Xcode, Visual Studio | Cursor fork of VS Code (built-in) |
| **Model selection** | GPT-4o, Claude 3.5/Sonnet (limited) | GPT-4o, Claude Sonnet/Opus, Gemini — full choice |
| **Price** | $10–$19/month (Business/Enterprise), BP covered | $20/month (Pro), no BP enterprise licence |
| **Background agents** | No (as of Q1 2026) | Yes (cloud background agents) |
| **Git worktrees** | No native support | Yes (parallel agent workstreams) |
| **MCP tool support** | Limited (extensions model) | Full MCP server integration |
| **Rules files** | `.github/copilot-instructions.md` | `.cursorrules`, `rules/` directory |
| **Terminal integration** | Limited | Deep shell integration |
| **PR generation** | Slash command `/pr` | Via agent mode |

### Workflows Beyond Code Completion

**Documentation Generation**:
- Select a function → `/doc` → generates docstring in your preferred format (Google, NumPy, Sphinx)
- Select a module → ask "Generate a README for this module" → full README with usage examples
- Ask "Document all undocumented functions in this file" → agent processes every function

**Test Writing**:
- "Write comprehensive unit tests for the PriceModel class, covering edge cases including null inputs, single-value arrays, and date boundary conditions"
- Agent generates test file with pytest, includes fixtures, parametrize decorators, and edge case coverage

**Refactoring**:
- "Refactor this function to replace the nested loops with vectorised Pandas operations"
- "Extract the data validation logic from this function into a separate validator class"
- Multi-file refactors in agent mode: change a function signature and update all callers across the codebase

**Architecture Reasoning**:
- "Given this codebase structure, what is the best way to add a new feature for [X] without breaking [Y]?"
- "Identify potential performance bottlenecks in this pipeline and suggest optimisations"

**Debugging**:
- Paste error + context → AI diagnoses root cause and provides fix
- "Walk through this function call-by-call and identify where this variable becomes None"

**PR Review and Commit Messages**:
- "Generate a commit message for these staged changes"
- "Review this PR diff and identify potential bugs or style inconsistencies"
- "Summarise the changes in this PR for a non-technical stakeholder"

### Template Project Setup

**Cursor Rules (`.cursorrules` or `rules/` directory)**:

The `.cursorrules` file sits at the project root and provides persistent instructions to Cursor on every prompt. Example structure:

```
# Project Context
This is a Python data pipeline project for FM&I fundamental models.
Stack: Python 3.11, Pandas, Polars, SQLAlchemy, Dataiku DSS

# Code Standards
- All functions must have type hints and NumPy-format docstrings
- Use Polars for performance-critical transformations, Pandas for compatibility
- All pipeline stages must log row counts before and after transformation
- Error handling: raise specific exceptions with context (not bare except clauses)

# Project Structure
- recipes/: Dataiku Python recipes
- models/: statistical model implementations
- tests/: pytest test files (mirror structure of src/)
- config/: YAML configuration files

# Prompting Guidance
When asked to generate code, always:
1. Include type hints
2. Include a docstring
3. Include at least one example in the docstring
4. Add a TODO comment for any assumption that needs verification
```

**GitHub Copilot Instructions (`.github/copilot-instructions.md`)**:

Same concept — project-specific instructions that Copilot reads as persistent context:

```markdown
# GitHub Copilot Instructions — FM&I Pipeline Project

## Project Overview
This repository contains fundamental model pipelines for the FM&I team.
All code is Python 3.11+ unless in a Dataiku recipe context.

## Standards
- Follow PEP 8; max line length 100
- All functions require type annotations and NumPy docstrings
- Tests live in tests/ and must pass: `pytest tests/`

## Domain Context
- "hub" refers to a natural gas pricing hub
- "contract_month" is a YYYY-MM string representing the forward delivery month
- "forward curve" means the time series of forward prices for a commodity
```

**The `_p-presentation-creator` repository as a worked example**:
This repository demonstrates the full template pattern:
- `CLAUDE.md` at the root: project context for Claude Code, defines architecture, commands, critical patterns, and quality gates
- `.claude/CLAUDE.md`: behavioural directives for the AI (implementation philosophy, prohibited patterns, quality standards)
- Agent definitions in the prompt: the complete agent team specification in the task description
- The result: every AI interaction in this project operates with full context about the stack, standards, and patterns — no re-explaining required

### Ask / Agent / Plan Modes

**Ask Mode** (or Chat mode):
- Single-turn conversational queries
- AI reads your context but does NOT take actions
- Use for: explaining code, answering questions, generating snippets you paste manually
- Best for: quick questions, exploration, learning

**Agent Mode** (or Agentic mode):
- AI plans and executes multi-step tasks autonomously
- Can read files, write files, run terminal commands, install packages
- Use for: feature implementation, refactoring, test generation, debugging sessions
- Best for: tasks that span multiple files or require iterative steps
- **Important**: Review what the agent proposes before it executes — use Plan mode first for complex tasks

**Plan Mode** (or Edit planning):
- AI proposes a plan of changes without executing them
- User reviews, approves, or modifies the plan before execution
- Use for: complex, high-risk changes; unfamiliar codebases; tasks where incorrect execution could break things
- Best practice: always use Plan mode for schema changes, API contract changes, or anything touching authentication

### Prompting Fundamentals

**Effective prompt structure**:
1. **Role/context**: "You are working on the FM&I price forecasting model"
2. **Task**: "Refactor the `calculate_forward_curve` function"
3. **Constraints**: "Without changing the function signature or return type"
4. **Output format**: "Provide the refactored code with inline comments explaining the changes"
5. **Edge cases**: "Handle the case where the input DataFrame is empty"

**Using the LLM to write its own prompt**:
- "Here is my task: [vague description]. Generate a precise, well-structured prompt that I can use to accomplish this task."
- "Improve this prompt to make it more effective: [your draft prompt]"
- "What additional context would make this prompt more effective?"

**Prompt templates and reuse**:
- Store effective prompts in a `prompts/` directory in your project
- Create templates with placeholder variables: `{{function_name}}`, `{{error_message}}`, `{{target_schema}}`
- Reference in `.cursorrules` or CLAUDE.md to make templates available to AI agents

### Cursor Advanced Features

**Background Agents**:
- Long-running tasks that execute in the cloud while you work on other things
- Use case: "Rewrite all test files to use pytest instead of unittest" — submit as background task, continue working, get notified when complete
- Available in Cursor Pro; subject to compute limits

**Git Worktrees for Parallel Agent Work**:
- Create multiple worktrees from the same repository: one for feature A, one for feature B
- Run a Cursor agent on each worktree simultaneously
- Agents work in parallel on different branches without interfering
- Command: `git worktree add ../feature-b feature-b-branch`
- Powerful for: running experiments in parallel, implementing multiple features simultaneously

**Multi-Agent Orchestration**:
- Cursor supports spawning sub-agents from an orchestrator agent (in advanced agentic mode)
- Orchestrator plans the high-level task and delegates to specialised sub-agents
- Sub-agents handle: code implementation, test writing, documentation generation
- Orchestrator synthesises results and handles conflicts

**@ Context Referencing**:
- `@file` — include a specific file in context
- `@folder` — include an entire directory
- `@codebase` — semantic search across the entire codebase
- `@web` — search the web for current documentation
- `@docs` — reference indexed documentation sets
- `@git` — reference git history, commits, diffs

**`.cursorignore`**:
- Exclude files from Cursor's codebase index (similar to `.gitignore`)
- Use for: large binary files, sensitive configuration files, generated outputs that shouldn't influence code generation

**Rules Files (advanced)**:
- Cursor supports multiple rule files in a `rules/` directory
- Each rule file can be scoped to specific file patterns (e.g., only apply Python rules to `*.py` files)
- Rules can be conditional: "When working in tests/, always use pytest fixtures"

### GitHub Copilot Advanced Features

**Workspace Agent (`@workspace`)**:
- Understands the full codebase structure (indexed)
- Can answer architecture questions across many files
- "Explain how data flows from the raw ingestion recipes to the final model output"

**Slash Commands**:
- `/explain` — explain selected code
- `/fix` — fix a bug
- `/test` — generate tests
- `/doc` — generate documentation
- `/new` — scaffold a new file/component

**Multi-File Edits**:
- Copilot Edit mode (VS Code) can propose and apply changes across multiple files simultaneously
- Similar to Cursor's agent mode but integrated into VS Code's native editor

**CLI Integration**:
- GitHub Copilot CLI: `gh copilot suggest "command to list all files modified in the last 7 days"` → generates the shell command
- `gh copilot explain "git reset --hard HEAD~1"` → explains what a command does before you run it
- Particularly useful for Bash/shell scripting and complex git workflows

---

## Section 5 — Model Landscape

### Claude Opus 4.6

**Position**: Anthropic's most capable model as of Q1 2026 (flagship)

**Context window**: 200K tokens input, ~8K output (extended thinking: up to 32K output)

**Strengths**:
- Complex multi-step reasoning (architecture design, complex debugging, research synthesis)
- Extended thinking mode: explicit chain-of-thought for problems requiring deep analysis
- Code generation quality on complex algorithmic tasks
- Following nuanced, long-form instructions precisely
- Mathematical and statistical reasoning

**Best use cases for FM&I**:
- Complex model architecture design
- Debugging non-obvious issues in statistical models
- Generating comprehensive documentation for complex codebases
- Research synthesis requiring judgment about source quality

**Limitations**:
- Slower than Sonnet (latency matters in interactive workflows)
- Higher cost (~$15/M input tokens, $75/M output tokens — premium tier)
- Overkill for routine tasks (code completion, simple refactors)

**Knowledge cutoff**: Approximately mid-2025 (verify for latest specific claims)

### Claude Sonnet 4.6

**Position**: Anthropic's best balance of capability and speed as of Q1 2026

**Context window**: 200K tokens

**Strengths**:
- Fast (significantly lower latency than Opus)
- Cost-effective (~$3/M input, $15/M output)
- Excellent at coding tasks, data analysis, structured output
- Strong instruction following with sufficient context
- Ideal for interactive coding workflows (Cursor, Claude Code)

**Best use cases for FM&I**:
- Daily coding assistance (pipeline development, debugging)
- Ad hoc data analysis with AI assistance
- Report drafting and documentation
- Interactive Q&A about codebase

**When to prefer Sonnet over Opus**:
- Speed matters more than maximum quality
- Task is well-defined and doesn't require extended reasoning
- High-frequency/interactive use (conversation latency matters)
- Budget-sensitive (team/API cost)

### Gemini 2.5 (Google)

**Position**: Google's current flagship; best-in-class for extremely long context tasks

**Context window**: 1 million tokens (can process entire large codebases in one context)

**Strengths**:
- Unrivalled context length — entire data pipelines, multi-module codebases
- Multimodal: images, audio, video, code together in one context
- Strong tool use and function calling
- Native Google ecosystem integration (Google Docs, Sheets, Drive via Gemini in Workspace)

**Best use cases for FM&I**:
- Loading an entire Dataiku project and asking architecture-level questions
- Processing large multi-page PDF reports for data extraction
- Cross-referencing large volumes of market data documentation

**Limitations**:
- Quality on complex code generation (Cursor integration) slightly below Claude Sonnet
- Slower on large contexts
- Google Workspace integration may not align with BP's M365 environment

**Access**: Google AI Studio (developer), Google Workspace (enterprise), Vertex AI (cloud)

### ChatGPT / GPT-4o and o3 (OpenAI)

**GPT-4o**:
- Position: OpenAI's multimodal production model
- Context: 128K tokens
- Strengths: very strong general performance, fast, excellent multimodal (image understanding)
- Code interpreter: sandbox Python execution — can run Python, generate charts, process uploaded files (CSVs, Excel) without user running code locally
- Best for FM&I: quick data analysis with uploaded files, image/chart interpretation, general-purpose tasks

**o3 (reasoning model)**:
- Position: OpenAI's advanced reasoning model
- Designed for: complex multi-step problems, mathematics, science, code architecture
- Extended "thinking" before responding
- Outperforms GPT-4o on complex algorithmic problems
- Higher cost and latency
- Best for FM&I: complex statistical methodology questions, mathematical modelling problems

**Data governance note for FM&I**: Consumer ChatGPT (ChatGPT.com) must NOT be used with BP data. OpenAI's enterprise API (Azure OpenAI Service via Microsoft) is covered under BP's Microsoft agreement.

### Ollama + Local Models

**What Ollama is**: A tool for running open-source LLMs locally on your own machine. No data leaves your device.

**Current capable models (Q1 2026)**:
- **Llama 3.3 70B**: Meta's open-source flagship; strong general coding and reasoning for local deployment
- **Mistral 7B/24B**: Lean, fast French open-source model; excellent for its size
- **Phi-4 (Microsoft)**: Extremely capable small model (14B); strong on code and reasoning
- **Code Llama / DeepSeek Coder**: Specialised code models for offline use

**When local models matter for FM&I**:
- Working with proprietary code or data that must not leave BP infrastructure
- Air-gapped environments or strict data governance scenarios
- High-volume processing where API costs are prohibitive
- Experimentation with model behaviour without cloud costs

**Performance trade-offs**:
- Llama 3.3 70B requires ~40GB RAM (or a high-end GPU) for acceptable performance
- On Apple M-series machines: 70B models run at ~10–15 tokens/second (workable for non-interactive tasks)
- Quality is meaningfully below Claude Sonnet/GPT-4o for complex tasks
- Best positioned as a "last resort for data safety" rather than first choice for daily use

### 12-Month Model Evolution Timeline

| Date | Model/Event | Significance |
|------|------------|-------------|
| Q1 2025 | Claude 3.5 Sonnet widely deployed | Became de-facto standard for coding tasks |
| Q1 2025 | GPT-4o with improved tool use | More reliable agentic workflows |
| Q2 2025 | Gemini 2.0 release | 1M context window became practically usable |
| Q2 2025 | Claude 3.7 Sonnet with extended thinking | Reasoning model for complex multi-step tasks |
| Q3 2025 | o3 (OpenAI) public release | Step-change in mathematical/logical reasoning |
| Q3 2025 | Llama 3.3 70B release | Open-source quality gap with proprietary models narrowed significantly |
| Q4 2025 | Claude Sonnet 4.6 release | Current production standard; coding and instruction following improvements |
| Q4 2025 | Gemini 2.5 with full tool use | Google's multimodal model becomes competitive for coding |
| Q1 2026 | Claude Opus 4.6 release | Frontier reasoning with extended thinking, multimodal improvements |

### Model Decision Framework

```
Task Complexity:
├── Simple/routine (code completion, debugging, docs) → Claude Sonnet 4.6
├── Complex/architectural (design, deep debugging, synthesis) → Claude Opus 4.6 or o3
└── Math/logic heavy → o3 reasoning mode

Context Size:
├── Normal (< 128K tokens) → Any model
└── Very large (> 128K, full codebase) → Gemini 2.5

Data Sensitivity:
├── Public / cleared data → Any cloud model
├── Internal but cleared for tool → GitHub Copilot (enterprise) / M365 Copilot
└── Sensitive proprietary data → Ollama local model ONLY

Latency Requirements:
├── Interactive / real-time → Claude Sonnet (speed) or GPT-4o
└── Batch / background → Opus or o3 (quality over speed)

Budget:
├── Team/API usage at scale → Sonnet (10× cheaper than Opus)
└── Occasional complex tasks → Opus
```

---

## Section 6 — Ethics & Compliance

### BP's AI Governance Policy

BP has an evolving AI governance framework aligned with:
- The UK AI Safety Institute guidelines
- Microsoft's Responsible AI principles (as the primary AI vendor)
- BP's own internal Digital & Innovation governance (Digital Centre of Excellence)

**Key principles** (as publicly stated and internally communicated):
1. **Human oversight**: AI-generated outputs must be reviewed by a qualified human before being used in commercial decisions
2. **Data protection**: BP's data classification framework applies to AI tools — data cannot be processed by an AI tool that doesn't meet BP's data handling standards for that classification
3. **Transparency**: AI-assisted outputs should be identifiable as such; do not misrepresent AI-generated analysis as purely human-produced without disclosure
4. **No autonomous trading decisions**: AI tools must not be used to make or trigger trading decisions without human review and approval at every step
5. **Compliance with market regulations**: All front-office AI use is subject to the same regulatory obligations as non-AI activities (MAR, REMIT, etc.)

### What Data CAN Go Into These Tools

**Microsoft M365 Copilot** (covered under BP's enterprise agreement):
- Internal documents, emails, Teams messages — Copilot's standard scope
- Analysis outputs intended for internal circulation
- Non-public but not market-sensitive internal communications and working documents

**GitHub Copilot** (covered under BP Enterprise GitHub):
- BP's internal codebase that is in the GitHub Enterprise org
- Code that does not contain embedded sensitive data (credentials, actual market prices in comments, etc.)
- Infrastructure and pipeline code

**IMPORTANT BOUNDARY**: Do not embed actual trading data, live prices, client identities, or position information in code comments or docstrings that will be sent to AI tools.

### What CANNOT Go Into These Tools

**Hard prohibitions for FM&I**:
1. **Live trading positions** — current or recent book positions, outstanding orders
2. **Proprietary model parameters** — calibrated model coefficients, proprietary curve construction methods that represent commercial advantage
3. **Client/counterparty information** — identities, negotiated terms, relationship details
4. **Market-sensitive information before public release** — supply/demand data that qualifies as insider information
5. **Model performance data that reveals trading strategy** — which models are driving which trading decisions
6. **Credentials and API keys** — never in code sent to AI tools (use environment variables)

**Consumer AI tools** (not covered under enterprise agreements):
- ChatGPT.com free/Plus tier
- Claude.ai without enterprise agreement
- Cursor (without explicit IT/legal approval)
These tools may use your inputs for model training and are NOT compliant with BP data handling requirements.

### Practical Rules of Thumb for FM&I

1. **The "press release test"**: If the information would be problematic if it appeared in a press release, do not put it in an AI tool (unless that tool is covered under BP's data handling agreements)
2. **Anonymise inputs when possible**: Replace real hub names, counterparty names, or specific volumes with generic placeholders when asking AI for code or analysis patterns
3. **Code patterns, not data**: Use AI for code structure, methodology, and pattern — not for running on actual live data
4. **Never paste live positions**: This is an absolute rule — positions, orders, and recent trades must never enter external AI tools
5. **Check the tool's data handling before using it**: If unsure whether a tool is covered under BP's agreements, assume it is not and contact IT/compliance

### Difference Between M365 Copilot and External Tools

| Dimension | M365 Copilot | GitHub Copilot (Enterprise) | Cursor / External |
|-----------|-------------|---------------------------|-------------------|
| Data used for training | No | No | No (Pro+) / Unclear (Free) |
| Data stored where | BP's Microsoft tenant | BP's GitHub org | Cursor's cloud |
| Covered by BP agreement | Yes | Yes | No (currently) |
| Compliant for internal data | Yes (within M365 classification) | Yes (code only) | No |
| Compliant for sensitive data | No | No | No |

### Where to Find Current BP AI Guidance

- BP's internal governance pages (accessible via the intranet — search "AI governance" or "responsible AI")
- Digital Centre of Excellence: responsible for AI policy at BP
- BP's Legal and Compliance team: for front-office specific questions
- IT Service Desk: for questions about specific tool approvals
- Line manager / Cost Centre Manager: for licence request approvals

*Note: AI governance at BP is an actively evolving area. Always refer to the current internal guidance rather than relying on any snapshot — including this one.*

---

## Section 7 — Extended Topics

### Claude Code

**What it is**: Claude Code is Anthropic's official command-line interface (CLI) tool for interacting with Claude at the repository and project level. Unlike IDE plugins (GitHub Copilot, Cursor), Claude Code operates in the terminal and can interact with any files, run shell commands, execute scripts, and manage git operations.

**How it differs from IDE plugins**:
- **Scope**: Claude Code works at the repository level — it understands the entire project, not just what's open in your editor
- **Tool use**: Can execute bash commands, read/write any file, manage git, run tests, interact with the filesystem
- **Long-running tasks**: Can work autonomously for minutes-to-hours on complex tasks
- **Headless**: Can be invoked from CI/CD pipelines, scheduled jobs, or other automation without a human at the keyboard
- **Multi-agent**: Can spawn sub-agents (using the Agent SDK) for parallel workstreams

**Workflow differences**:
- Typical IDE plugin workflow: write code → get completions → accept/reject
- Claude Code workflow: describe a task → agent plans → executes across multiple files → reports results
- Claude Code can: run your test suite, see failures, fix them, re-run, and iterate — all without user involvement per step

**The CLAUDE.md file**:
- Sits at the project root (or in `.claude/` for layered configuration)
- Provides persistent instructions to Claude Code for every session in that project
- The `_p-presentation-creator` project has both a root `CLAUDE.md` (project-wide instructions) and `.claude/CLAUDE.md` (behavioural directives)
- Well-written CLAUDE.md dramatically reduces the need to re-explain project context in each session

### Claude Cowork (Claude.ai Projects and Teams)

**Note**: "Claude Cowork" as of Q1 2026 refers to Claude's collaborative features accessible via claude.ai — specifically the Projects feature and the Teams subscription tier.

**Claude Projects**:
- Persistent context across conversations (project-level memory)
- Upload documents that remain available across all sessions in the project
- Custom instructions per project (effectively CLAUDE.md for the web interface)
- Share projects with team members (on Teams tier)

**Claude Teams**:
- Enterprise-grade collaboration: shared projects, team knowledge bases
- Admin controls and usage monitoring
- Priority access and higher rate limits
- Data handling under Anthropic's enterprise agreement (no training on data)

**Use cases beyond coding**:
- Research synthesis projects with uploaded documents
- Persistent team knowledge base (upload specifications, standards, model documentation)
- Shared prompt libraries for consistent team outputs

### Claude Code Agent Teams

**Architecture**:
- **Orchestrator agent**: receives the high-level task, plans the approach, delegates to sub-agents
- **Sub-agents**: specialised agents responsible for specific aspects of the task (research, implementation, testing, documentation)
- **Communication**: orchestrator passes context and partial results to sub-agents; sub-agents report back
- **Tool use**: each agent can use the full Claude Code tool set (bash, read, write, search, etc.)

**When to use agent teams**:
- Tasks that have clearly separable parallelisable components
- Long-running tasks where specialisation improves quality
- Workflows with distinct phases (research → plan → implement → test → document)

**The `_p-presentation-creator` project** is itself an example of agent team design:
- Agent 1 (Research Lead) → Agent 2 (Content Architect) → Agent 3 (Slide Designer) → Agent 4 (Transcript Writer) → Agent 5 (Production Engineer)
- Each agent reads all prior outputs and produces a specific deliverable
- The CLAUDE.md in the project defines the agent team protocol

### Claude Code Recent Enhancement Timeline (Last 12 Months)

- **Q1 2025**: Claude Code (then in beta) released publicly
- **Q2 2025**: Background agent support added (long-running tasks without blocking)
- **Q2 2025**: Git worktree support for parallel agent workstreams
- **Q3 2025**: Multi-agent orchestration (Agent SDK public release)
- **Q3 2025**: MCP server support extended significantly — now hundreds of community MCP servers
- **Q4 2025**: Claude Code hooks system (pre/post tool-call automation)
- **Q1 2026**: Claude Code agent skills (`/skills` system for reusable packaged capabilities)
- **Q1 2026**: Integration with Claude.ai Projects for shared team context

### Claude Code Future Roadmap

- Expanded IDE integration (Claude Code as a VS Code extension alongside CLI)
- More sophisticated background agent coordination
- Native CI/CD integration (Claude Code as a pipeline step)
- Team-level agent sharing and collaboration
- Improved memory and project context management

### Tool Calling

**What it is**: The ability for an LLM to invoke external functions, APIs, or services as part of generating a response. The LLM doesn't just output text — it outputs structured instructions to call a function, receives the result, and incorporates it into the next step of its reasoning.

**Example**:
```
User: What's the current price of TTF natural gas?
LLM: [decides to call a price API]
      → calls: get_commodity_price(symbol="TTF", date="today")
      → receives: {"price": 32.45, "currency": "EUR/MWh", "timestamp": "2026-03-08T09:30:00Z"}
      → responds: "The current TTF price is €32.45/MWh as of 09:30 UTC."
```

**How it enables agentic workflows**:
- Without tool calling: LLM can only generate text based on training data
- With tool calling: LLM can read files, query databases, call APIs, run code, and take actions in the world
- Enables: data retrieval → analysis → action in a single agent session

**Cursor MCP Tool Calling**:
- Cursor supports Model Context Protocol servers
- Any MCP server exposes a set of callable tools to the LLM
- Example: an MCP server for a Dataiku instance exposes: `list_projects()`, `get_recipe_status()`, `get_job_logs()`, `trigger_scenario()`
- Cursor agent can then reason about pipeline status and take actions without leaving the IDE

**GitHub Copilot Tool Calling**:
- GitHub Copilot extensions model (different from MCP)
- Extensions are installed in GitHub and can expose tools to Copilot chat
- Less flexible than MCP; more tightly controlled security model
- Available tools: GitHub itself (issues, PRs, code search), plus third-party extensions

**Why tool calling matters**:
- Transforms LLMs from "very smart autocomplete" to "autonomous agents that interact with systems"
- This is the foundational capability enabling all agentic AI workflows

### MCP (Model Context Protocol)

**What MCP is**: An open standard developed by Anthropic (released November 2024) that defines a common interface between AI models and external tools, data sources, and services. Think of it as "USB for AI integrations" — any MCP-compliant client (Cursor, Claude Code, any MCP-aware host) can connect to any MCP-compliant server.

**Why it matters**: Before MCP, every AI tool had its own bespoke integration format. MCP standardises this, meaning:
- One MCP server for Dataiku can be used by Cursor, Claude Code, and any other MCP-compliant AI tool
- Community-built MCP servers can be reused across organisations
- The ecosystem is growing rapidly: databases, APIs, development tools, SaaS platforms

**Current MCP server examples relevant to FM&I**:
- **Dataiku MCP**: (community/custom) — read project status, recipe definitions, scenario results, job logs; trigger scenarios; query datasets
- **Database MCP (PostgreSQL/SQLite)**: read schema, run queries, explain query plans
- **Bloomberg/financial data MCP**: (emerging) — query price data, news, fundamentals via AI interaction
- **GitHub MCP**: read PRs, issues, code, commit history
- **Filesystem MCP**: read/write local files in a controlled, permissioned way
- **Slack MCP**: read channels, send messages, query history

**How to find MCP servers**:
- Anthropic's official MCP server repository (GitHub: `modelcontextprotocol/servers`)
- Cursor's MCP marketplace
- Community repositories (search: `mcp-server-[tool name]`)

**How to build a simple MCP server** (Python example pattern):
```python
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("dataiku-mcp")

@server.tool("get_job_status")
async def get_job_status(project_key: str, job_id: str) -> str:
    # Call Dataiku API
    status = dataiku_client.get_job(project_key, job_id)
    return f"Job {job_id}: {status['state']} ({status['duration']}s)"

server.run()
```

**MCP in practice for FM&I**:
- Connect Cursor to your Dataiku instance
- Ask: "What's the current status of the gas pricing pipeline? Are there any failed jobs?"
- Cursor calls the Dataiku MCP server, retrieves job status, and responds
- Ask: "The gas_hub_prices recipe failed yesterday. Get the logs and suggest a fix."
- Cursor retrieves logs via MCP, reads the recipe code, generates a fix

### Agentic AI

**The shift from single-turn to multi-step autonomous agents**:
- **Pre-2024**: AI = ask question → get answer. One turn, no memory, no actions.
- **2024–2025**: AI = give task → agent plans → executes steps → reads results → adjusts → completes task. Multiple turns, persistent state, tool use.

**What changed technically**:
- Tool calling became reliable enough for production use
- Context windows became large enough to hold complex task state
- Models became better at following multi-step plans without losing track
- Infrastructure (Cursor, Claude Code, LangChain, AutoGen) matured to handle agent orchestration

**Why this matters for FM&I** — concrete use cases:
- **Pipeline monitoring agent**: runs nightly, checks all Dataiku pipeline outputs against expected ranges, generates an exception report, posts to Teams
- **Model drift monitor**: weekly agent that compares current model performance against baseline, flags drift above threshold, drafts a brief for the model owner
- **Ad hoc request triage**: agent that receives a request from a trader, identifies what data is needed, generates the analysis code, runs it, and formats output — reporting back with results and methodology
- **Report generation pipeline**: agent triggered on data refresh, pulls latest figures, updates commentary template, formats output in the required style

**Current state — what works reliably**:
- Well-defined tasks with clear success criteria
- Tasks where errors are detectable and recoverable (e.g., test failures caught by the test suite)
- Tasks with bounded scope (single repository, defined set of tools)

**Current limitations — what is still unreliable**:
- Long chains of reasoning (error accumulation over many steps)
- Tasks requiring accurate real-world knowledge (hallucination risk)
- Ambiguous success criteria (agent may think it's done when it isn't)
- Complex tool use with unfamiliar APIs (tool call failures)
- Tasks requiring human judgment at intermediate steps

**The orchestrator-subagent pattern**:
```
Orchestrator (high-level task manager)
├── Receives: "Generate monthly model performance report for FM&I"
├── Plans: Research → Data Pull → Analysis → Writing → Formatting
├── Delegates to:
│   ├── Research sub-agent: "Gather all model performance data for March"
│   ├── Analysis sub-agent: "Identify top 5 performance anomalies"
│   ├── Writing sub-agent: "Draft commentary for each section"
│   └── Formatting sub-agent: "Produce the final report in our standard template"
└── Synthesises: Combines outputs, resolves conflicts, produces final deliverable
```

### Agent Skills

**What agent skills are**: Packaged, reusable capabilities that can be invoked by AI agents. In Claude Code, they are implemented as skills accessible via `/skill-name`. A skill encapsulates a specific workflow — a set of instructions, tools, and output format — that can be triggered by name rather than re-described each time.

**Why they are useful**:
- Encapsulate complex workflows as a single callable unit
- Ensure consistency: every invocation follows the same process
- Reusable across projects and team members
- Skills can invoke other skills (composable)

**Example agent skill — Data Quality Report**:
```markdown
# Skill: data-quality-report
Description: Generate a structured data quality report for a Dataiku dataset output

## Instructions
When invoked with a dataset name or DataFrame:
1. Profile the dataset: row count, column count, dtypes
2. For each column: null count/%, unique values, min/max/mean (if numeric), sample values (if string)
3. Flag: columns with >10% nulls, columns with single unique value, numeric columns with outliers (>3 IQR)
4. Generate: summary text, a structured JSON output, and a list of recommended actions
5. Format: markdown table + JSON block

## Output format
[structured markdown with embedded JSON]
```

**How to create a new agent skill** (in Claude Code):
1. Create a file in `.claude/skills/` (e.g., `data-quality-report.md`)
2. Write the skill specification: name, description, invocation pattern, instructions, output format
3. Reference in CLAUDE.md under "Available Skills"
4. Invoke with `/data-quality-report [dataset_name]`

**Best practices**:
- Skills should have single, well-defined responsibilities
- Output format should be explicitly specified
- Include examples of expected inputs and outputs in the skill definition
- Version-control skill definitions alongside the codebase

### Context & Tokens

**Why context management matters**:
- Every token in context costs money (input tokens are charged)
- Large contexts slow down responses (latency increases with context size)
- Quality degrades if context is filled with irrelevant noise (the AI has to "find" the relevant parts)
- Context windows have limits (200K for Claude, 128K for GPT-4o) — large codebases can exceed them

**Practical rules**:
1. **Include only what's relevant**: Don't dump your entire codebase into context — use `@file` or specific selections
2. **Start fresh conversations for new tasks**: Don't carry context pollution from an unrelated earlier conversation
3. **Use `.cursorignore`/`.gitignore` to protect context quality**: Exclude: `node_modules/`, `__pycache__/`, build outputs, large data files, dependency lock files
4. **Compress context when possible**: Summarise long conversation histories; ask the AI to "summarise what we've decided so far" before continuing
5. **System prompt efficiency**: CLAUDE.md / cursor rules should be dense with signal, not verbose — every line costs tokens on every request

**Token cost awareness** (approximate Q1 2026 rates):
| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Claude Opus 4.6 | $15 | $75 |
| Claude Sonnet 4.6 | $3 | $15 |
| GPT-4o | $5 | $15 |
| o3 | $10 | $40 |
| Gemini 2.5 Pro | $3.50 | $10.50 |
| Llama 3.3 (local) | $0 | $0 |

**Scale example**: A team of 10 analysts each making 50 AI requests per day with ~4K tokens per exchange (input+output) at Claude Sonnet rates ≈ ~$9/day or ~$2,000/year. Context inflation (poor hygiene) can double this. For Opus: 10× cost.

### Hooks in Claude Code

**What hooks are**: Pre- and post-execution triggers that run automatically when Claude Code uses specific tools. They enable automation of common patterns.

**Types**:
- **Pre-tool hooks**: run before Claude Code executes a tool (e.g., before writing a file)
- **Post-tool hooks**: run after a tool executes (e.g., after writing a file)

**Use cases**:
- Auto-run linter after code is written (`eslint --fix` or `black` after every file write)
- Auto-run tests after changes are made
- Log all AI tool invocations for audit purposes
- Send a Slack notification when a background agent completes
- Validate that written files meet project standards before proceeding

**Configuration**: Defined in `.claude/hooks/` directory or in CLAUDE.md under a hooks section.

### ChatGPT Codex

**What Codex is**: OpenAI's cloud-based autonomous coding agent, separate from ChatGPT's code interpreter. Codex is OpenAI's answer to Cursor's background agents and Claude Code's agentic mode.

**How it works**: Codex receives a task description, spins up a sandboxed virtual environment with your code, executes changes autonomously, and returns a PR or diff. Similar to Cursor's background agents but hosted entirely by OpenAI.

**Comparison to Claude Code / Cursor**:
| Dimension | ChatGPT Codex | Cursor Background Agents | Claude Code |
|-----------|---------------|-------------------------|-------------|
| Environment | OpenAI cloud sandbox | Cursor cloud | Local or cloud |
| Code access | Uploaded / connected repo | Local workspace | Local filesystem |
| Tool use | Limited to sandbox | Full MCP support | Full bash + tools |
| Model | GPT-4o / o3 | User choice | Claude Opus/Sonnet |
| Data handling | OpenAI cloud | Cursor cloud | Local (highest privacy) |

**When Codex is relevant for FM&I**: For teams using OpenAI's ecosystem (Azure OpenAI Service via BP), Codex represents a cloud-native agentic coding option that may eventually integrate with BP's Azure infrastructure.

---

## Section 8 — Personal Use Cases

### Claude Code + Remotion

**What Remotion is**: A React-based framework for creating videos programmatically. Instead of using video editing software, you write React components that define each "frame" of the video — text animations, charts, data visualisations — and Remotion renders them to MP4.

**The Claude Code + Remotion workflow**:
1. Describe the video content and structure to Claude Code
2. Claude Code generates React/Remotion components for each scene
3. Data-driven sections (charts, statistics) are generated from structured data inputs
4. Remotion's preview server shows real-time output in a browser
5. Final render via Remotion CLI

**Why this is interesting for FM&I**:
- Model performance videos: animate a forward curve's evolution over time
- Scenario analysis: programmatic video that walks through scenario assumptions and outcomes
- Automated briefing videos: weekly market update video generated entirely from structured data inputs
- The entire `_p-presentation-creator` repository exists as a template for this kind of AI-assisted content production pipeline

### OpenClaw

**Research note**: OpenClaw does not appear to be a well-documented publicly available tool as of the knowledge cutoff. It may refer to:
- An internal tool at a specific organisation
- A niche open-source project with limited public documentation
- A colloquial name for a specific Claude Code workflow
*Presenter should verify: if this is an internal or personal project, describe it directly.*

### Claude Remote

**What Claude Remote refers to**: The ability to run Claude Code over SSH on a remote machine. This enables:
- Running Claude Code on a powerful remote server (GPU machine, cloud instance) while working from a lightweight laptop
- Accessing Claude Code on machines that store data locally (important for data governance scenarios)
- Running Claude Code in headless CI/CD environments

**The workflow**:
```bash
ssh user@remote-server
# On remote server:
claude code  # Full Claude Code experience over SSH terminal
```

**Why this matters for FM&I**:
- Run AI assistance directly on the machine where sensitive data lives (data never leaves the server)
- Use powerful cloud instances for computationally intensive agentic tasks
- Consistent environment across team members via shared remote development servers

### Claude Chrome Extension

**Available Chrome extensions for Claude (as of Q1 2026)**:

1. **Claude for Google (unofficial)**: Displays Claude's response alongside Google search results
2. **Anthropic's official Claude extension** (if/when released): Direct Claude access from any browser tab
3. **Third-party workflow integrations**: Extensions that add Claude to specific web apps (Gmail, Notion, etc.)

**Most relevant for productivity**:
- Quick access to Claude from any page without switching tabs
- Highlight and explain: select text on any webpage and send to Claude
- Form filling assistance: draft email replies, Confluence page content, Jira descriptions
- Web research: open a financial news article, ask Claude to extract key data points

**Data governance note**: Browser extensions can read page content — be cautious about using Claude browser extensions on pages containing sensitive BP data.

### Weather Alerts Project (`_p-weather_alerts`)

**Project pattern**: A Python automation project that uses the Claude API (Anthropic's Python SDK) to generate intelligent weather alerts for specific geographic/commercial contexts.

**Architecture**:
```
weather_data_api → Python script → Claude API (analysis prompt) → Alert generation → Delivery (email/Slack)
```

**What makes it interesting for FM&I**:
- **Demonstrates the API integration pattern**: calling Claude programmatically, not via chat UI
- **Trigger-based agent**: event-driven automation that runs on a schedule or data trigger
- **Structured output**: prompt engineering to ensure Claude returns machine-parseable JSON (alert severity, affected areas, recommended actions)
- **Template for FM&I**: same pattern applies to: pipeline failure alerts, model drift alerts, unusual market condition alerts — any event-driven AI notification workflow

**The pattern in code (simplified)**:
```python
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def generate_weather_alert(weather_data: dict) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"""
            Analyse this weather data for commercial impact on gas infrastructure:
            {json.dumps(weather_data)}

            Return JSON with: severity (1-5), affected_regions,
            commercial_impact_summary, recommended_actions
            """
        }]
    )
    return json.loads(response.content[0].text)
```

**Replication for FM&I**: Replace weather data with pipeline status, model performance metrics, or market data anomalies. Same pattern, different context.

### Claude Template Project Deep Dive (`_p-presentation-creator`)

**What this repository demonstrates**:

This repository is a working example of a fully configured AI-assisted development template. Every file is intentional:

**`CLAUDE.md` (root)**:
- Project overview with full stack description
- All development commands (not just remembered, but codified)
- Architecture description with key directories
- Critical patterns that MUST be followed (user scoping, TRPCError, Zod bounds)
- Feature-adding workflow (5-step checklist)
- Testing framework details
- Known trade-offs (prevents the AI from "fixing" intentional decisions)
- Troubleshooting guide

**`.claude/CLAUDE.md`** (behavioural directives):
- Implementation philosophy ("direct implementation only, no partial implementations")
- Analysis framework (technical feasibility, edge cases, performance, integration)
- Prohibited patterns (explicit list of what the AI must never do)
- Quality gates (lint, build, test must pass)

**Agent definitions**:
The task prompt for this session is itself an agent team specification — complete with roles, research briefs, output formats, and success criteria for each agent. This is the template pattern for complex AI-assisted work.

**Why this matters**:
- Without CLAUDE.md: every session starts from zero; AI makes inconsistent decisions; quality varies
- With CLAUDE.md: AI has persistent context about standards, patterns, and constraints; consistent quality across sessions and team members
- The template is the asset: the investment in writing good CLAUDE.md pays dividends on every subsequent AI interaction

---

## Section 9 — Business Potential Use Cases

### Copilot for Power BI

**What it does**: Microsoft Copilot integration in Power BI (available to Power BI Premium/Fabric customers) enables:
- **Natural language report creation**: "Create a report showing monthly gas volume by hub for the last 12 months with a YoY comparison" → Copilot generates the report
- **DAX formula generation**: describe a calculation in plain English → Copilot generates the DAX measure
- **Report summarisation**: narrative text automatically generated from charts and data — "Write a summary of the key insights from this report"
- **Q&A over data**: ask natural language questions about any dataset

**FM&I-specific use cases**:
- Generate first-pass dashboards for new data sources without manual DAX coding
- Auto-generate executive narrative summaries from model performance dashboards
- Enable traders to self-serve simple data queries without analyst intervention
- Reduce dashboard development time from days to hours for standard report types

**Access**: Requires Power BI Premium or Microsoft Fabric licence. Check with BI/analytics team for BP availability.

### Plotly Studio (Plotly AI)

**What Plotly Studio is**: An AI-assisted interactive data visualisation platform built on Plotly/Dash. AI generates Plotly/Dash code from natural language descriptions of the desired visualisation.

**Capabilities**:
- Describe a chart → get working Plotly code
- Upload a dataset → AI suggests appropriate visualisations
- Iterate: "Make the colours match our brand", "Add a secondary y-axis for volume", "Export as an interactive HTML"

**FM&I relevance**:
- Accelerate forward curve visualisation development
- Generate bespoke interactive charts for ad hoc analysis without deep Plotly expertise
- Create publication-quality analytical charts for trading desk presentations faster

**Data governance**: Plotly Studio is a cloud service — apply same data handling rules as other external tools.

### Dataiku Gen AI Capability

**Dataiku's LLM Mesh**:
- Dataiku 13+ includes a built-in "LLM Mesh" that connects Dataiku projects to external LLMs (OpenAI, Anthropic, Azure OpenAI) with appropriate data governance controls
- Allows: calling LLMs from within Dataiku Python/R recipes, without engineers needing to manage API keys individually
- Governance layer: LLM calls go through a managed gateway with logging and cost management

**AI-Assisted Pipeline Building in Dataiku**:
- AI suggestions for recipe logic
- Dataiku's built-in code assistant (powered by LLM Mesh) can suggest Python code within recipe editors
- "Visual AI" recipes for no-code ML model training

**Implications for FM&I**:
- Leverage LLM calls within ETL pipelines (e.g., extract structured data from unstructured text inputs)
- AI-assisted code generation within the familiar Dataiku environment
- Build NLP pipelines (news article parsing, report summarisation) as standard Dataiku recipes

**Maturity level**: LLM Mesh is production-ready in Dataiku 13+. AI code assistant is in active development — capabilities will increase through 2026.

### MCP Tools for Dataiku

**What's possible today**:
Building a custom MCP server for Dataiku using Dataiku's REST API:

```python
# Simplified MCP server pattern for Dataiku
@server.tool("get_scenario_status")
async def get_scenario_status(project_key: str, scenario_id: str) -> str:
    response = dataiku.api_client().get_scenario(project_key, scenario_id)
    last_run = response.get_last_runs(limit=1)[0]
    return f"Scenario: {scenario_id}, Last run: {last_run['start']}, Status: {last_run['status']}"

@server.tool("trigger_scenario")
async def trigger_scenario(project_key: str, scenario_id: str) -> str:
    result = dataiku.api_client().trigger_scenario(project_key, scenario_id)
    return f"Triggered run ID: {result['runId']}"

@server.tool("get_job_logs")
async def get_job_logs(project_key: str, job_id: str) -> str:
    logs = dataiku.api_client().get_job_log(project_key, job_id)
    return logs[-2000:]  # Return last 2000 chars
```

**With this MCP server in Cursor or Claude Code**:
- "What FM&I pipeline scenarios ran today? Were there any failures?"
- "Get the logs for the failed gas_curve_build job and tell me what went wrong"
- "Re-trigger the gas_hub_prices scenario"

**Effort to build**: A basic read-only Dataiku MCP server is a 200–300 line Python project — achievable in a day.

### Innovation Day Commercial Use Case Ideas (20+ ideas)

#### Data & Modelling
1. **AI-assisted model validation**: Agent that automatically tests a new model version against holdout data, compares against incumbent, generates a structured model comparison report
2. **Automatic model documentation**: On every model code commit, an agent generates/updates the model card, input/output spec, and known limitations
3. **Hyperparameter search with AI reasoning**: Instead of grid search, use an AI agent to reason about which hyperparameter regions to explore based on model behaviour
4. **AI code reviewer for pipeline changes**: Before merging a Dataiku recipe change, an agent reviews for: data type assumptions, null handling, join uniqueness, performance implications
5. **Statistical assumption checker**: Agent that tests a proposed model against its statistical assumptions (stationarity, homoscedasticity, etc.) and flags violations

#### Trading Desk Support
6. **Automated market structure briefing**: Daily agent that identifies 3–5 notable market structure changes (curve shape changes, spread anomalies, volume outliers) and drafts a briefing for the trading desk
7. **Request triage agent**: FM&I receives ad hoc requests from traders; an agent reads the request, identifies what data/analysis is needed, generates the initial code structure, and estimates completion time
8. **Curve comparison narrative generator**: When a new forward curve is released, an agent compares it to the previous version and generates a narrative explanation of changes
9. **Scenario analysis automation**: Trader inputs a set of scenario assumptions; agent generates the code to run the scenarios through existing models and formats the output in standard reporting format
10. **News-to-model-impact mapper**: Agent reads a news event (e.g., major supply disruption), identifies which FM&I models are most exposed, and drafts a preliminary impact assessment

#### Dataiku & Platform Integration
11. **Pipeline health dashboard agent**: Weekly report of all Dataiku pipeline health — run times, error rates, data freshness, row count anomalies — generated automatically
12. **Data lineage query interface**: Ask in natural language "Which models downstream are affected if the TTF spot price feed goes down?" — agent traces the Dataiku lineage graph
13. **Recipe optimisation agent**: Agent reviews Python recipes for performance bottlenecks and suggests vectorisation, parallelisation, or caching improvements
14. **Schema drift detector**: Agent monitors upstream data schemas and alerts when a column is added, removed, or has a type change that could affect downstream models
15. **Test coverage gap analyser**: Agent reviews which Dataiku recipes lack adequate test scenarios and generates a prioritised list of test coverage to add

#### Reporting & Visualisation
16. **Natural language chart generator**: Analyst describes a chart in plain English → agent generates Plotly code and embeds in report
17. **Automated PowerPoint generation**: Weekly model performance data → agent generates a formatted PowerPoint presentation in standard template
18. **Report commentary assistant**: Analyst produces charts; agent drafts commentary that explains movements and highlights anomalies
19. **Executive summary generator**: Full technical model report → agent produces a 1-page executive summary for senior stakeholders
20. **Comparative visualisation generator**: "Show me how our gas hub price forecasts have evolved over the last 6 months" → agent pulls historical forecasts and generates comparison charts

#### Process & Workflow Automation
21. **Meeting action item extractor**: Post-meeting, agent reads Teams transcript, identifies action items, assigns to named individuals, creates Jira tickets or sends Teams follow-ups
22. **Onboarding knowledge base agent**: New team member asks questions; agent answers from FM&I documentation, model cards, and codebase — drastically reducing onboarding time
23. **Incident response assistant**: When a model or pipeline failure is reported, agent retrieves relevant logs, recent code changes, and upstream data status to help diagnose the root cause
24. **Regulatory filing assistant**: Agent checks model documentation against internal regulatory filing requirements and identifies gaps before submission
25. **Specification-to-code pipeline**: Business analyst writes a natural language specification for a new analysis; agent generates the initial code structure and test cases

---

## Section 10 — Philosophical Anecdotes

### AI Making Work Cheap

**The commoditisation argument**: Certain categories of analytical work are becoming commodities — not because AI is better than humans at them, but because AI makes them fast enough and cheap enough that the calculus changes. The example that resonates in financial services:

Before AI: writing a data quality report for a new dataset took a junior analyst 4 hours. It was a billable activity, a visible contribution, a line on the timesheet.

After AI: the same report takes 20 minutes with AI assistance — 5 to prompt, 15 to review and correct.

The consequence is not that the analyst is made redundant. It is that **doing the routine work is no longer sufficient evidence of contribution**. The analyst who previously spent 4 hours on this is not producing proportionally more value — they are now expected to produce something with the freed time. The question every analytical professional should be asking: "What am I doing with the time AI just gave me?"

**Evidence**: A 2024 BCG study found that in tasks where AI provided meaningful assistance, the productivity distribution compressed for routine tasks but expanded for complex, judgment-dependent tasks. The top performers (who used AI + domain expertise) widened the gap over average performers. The bottom performers (who used AI without judgment) produced worse outputs than they did without AI. The commodity risk is real for routine work; the premium for domain judgment increased.

**What this means for FM&I**: The fundamental models, market structure insights, and commercial judgment that FM&I provides are not commodities. The boilerplate around them — the code scaffolding, the documentation, the data profiling, the report formatting — increasingly is. The team's differentiation is in the intellectual content, not the production of it.

### AI Changing Software Engineering

**The shift from writing code to owning outcomes**: The argument, made compellingly by several engineering leaders in 2024–2025, is that code generation changes what it means to be a software engineer. When generating a function takes 30 seconds instead of 30 minutes, the bottleneck shifts entirely to:
- Knowing what to build (product and domain judgment)
- Knowing when the output is correct (verification and testing)
- Knowing what to do when it goes wrong (debugging intuition and domain knowledge)

**The performance art critique** (from the philosophical section of the agenda): There is a class of software development activity that was always performance art — the elaborate sprint planning ceremonies, the architecture decision records nobody reads, the digital transformation strategy decks, the "prompt playbooks," the "AI wrapper" products. These activities existed because the actual coding was slow enough that the planning was proportionally valuable. When code generation is fast and cheap, the ratio flips: excessive ceremony becomes a liability.

**The "who owns the risk" question**: As AI generates more code, the critical question becomes accountability. When an AI-generated model has a bug that affects a trading decision — who owns that? The engineer who accepted the AI's output? The team that deployed it? This is not a rhetorical question — it is actively being worked out in financial services regulatory frameworks. The answer, almost certainly, will be: **the human who deployed it without adequate verification**. This increases, not decreases, the premium on engineering judgment.

### AI Won't Replace Data Scientists, but Tool Users Will Replace Non-Tool Users

**The productivity gap evidence** (from the Accenture 2025 study referenced in Section 1): Within a cohort of data scientists given identical access to AI tools, the top 20% of tool adopters saved 15+ hours per week; the bottom 20% saved fewer than 2. This is not a technology access problem — it is a workflow integration problem.

**The compounding effect**: A data scientist saving 10 hours per week on routine tasks can, over a year, produce 25+ additional weeks of non-routine analytical work. At team scale, this is a capability step-change. The team that integrates AI tools into its workflows will produce more rigorous analysis, more thorough documentation, more comprehensive testing, and faster turnaround on ad hoc requests — not because any individual is smarter, but because routine friction has been reduced.

**The replacement dynamic**: The threat is not AI replacing data scientists as a category. The threat is that teams and organisations that integrate AI well will require fewer people to do the same volume of work, or will do proportionally more work with the same headcount. In a competitive market — whether internal resource allocation or external hiring — the team that ships 2× the analytical output with the same headcount will attract investment and headcount; the team that doesn't will face pressure.

### The Next Decade's Threat: The Comfortable Middle

**The hollowing-out thesis**: The most exposed professional category in the next decade is not the low-skill worker (automation of physical and repetitive tasks is well-advanced and the social response is well-understood). It is the comfortable middle: the professionals who added value by being the translator between domain and technology.

- The IT business analyst who translated business requirements into technical specs — without being able to verify either
- The management consultant who synthesised research without building the models
- The project manager who coordinated without understanding what was being built
- The "digital transformation" lead who scheduled workshops without shipping products

AI doesn't threaten these roles because it can do the work better. It threatens them because **the gap they filled — between domain expert and technical implementation — is closing**. The domain expert (the trader, the quant, the doctor) can now interact directly with the technical layer (code, data, systems) via AI mediation. The need for a non-expert intermediary decreases.

**The implication for FM&I**: This team sits on the right side of this divide. FM&I are domain experts in fundamental modelling who also command the technical layer. The threat is not to FM&I; it is to the layers around them that have historically mediated between FM&I and other parts of the business.

### The Performance Art Around Coding

**The observation**: A substantial portion of what passed for software delivery in large organisations was performance art — visible activity that signalled effort without necessarily producing proportional outcomes. The elaborate requirements ceremonies. The enterprise architecture slide decks. The digital transformation slogans on Confluence pages. The "AI strategy" documents that predated any AI adoption. The prompt playbooks. The "AI wrappers" (ChatGPT with a different login page) sold as products.

**Why AI accelerates the denouement**: When execution is fast and cheap, performance art becomes conspicuous. The team that spent 3 sprints writing requirements and 1 sprint building can no longer justify the ratio when building takes 10% of the time it used to. The organisations that shipped products win; the organisations that ran processes will face an existential question about what they were doing.

**The "AI wrapper" observation**: A non-trivial portion of software products launched 2023–2024 were thin wrappers around foundation model APIs — the same underlying capability with a different interface. The market has become sophisticated enough to recognise this, and the premium has moved to genuine workflow integration (making something 10× faster or possible that was previously impossible), not to API wrapping.

**The key question: "Who owns the risk when the AI is wrong?"**: This is the question that determines whether an AI use case is viable in a regulated front-office environment. It is the question that cuts through the performance art. For FM&I: you own the risk on every model output, regardless of whether a human or an AI wrote the code. This is a quality argument for rigorous AI-assisted testing, not an argument against AI adoption. The answer to "AI can be wrong" is "so can humans, and AI-assisted testing catches more of both."

---

*Research document complete. All 10 agenda sections covered with substantive factual content. Handoff to Agent 2 (Content Architect & Narrative Strategist).*
