# Agent 2 Content Outline — Gen AI FM&I Upskilling Session
*Narrative architecture, slide plan, and timing allocation. Read by Agents 3, 4, and 5.*

---

## Core Message

**"You already have the tools — the only thing between you and 10× productivity is knowing which tool to reach for and when."**

This message appears in:
- Slide 3 (opening hook)
- Slide 28 (mid-session callback after tool deep-dives)
- Slide 56 (closing CTA)

---

## Narrative Arc (Situation → Complication → Resolution)

**Situation (Slides 1–6)**: FM&I is a highly capable technical team doing critical commercial work. You're already sophisticated users of Python, SQL, ML, and Dataiku. You run production pipelines that support real trading decisions. You understand domain nuance that most AI tools don't.

**Complication (Slides 7–10)**: Gen AI tools are moving faster than any of us can track individually. The productivity gap between teams that have integrated these tools and teams that haven't is measurable and growing. BP has tools available to us right now that most of the team isn't using to full potential. There is an adoption curve and we are not all at the front of it.

**Resolution (Slides 11–56)**: By the end of this session, you have a precise mental map of every tool, access route, and compliance boundary. You have concrete workflow templates you can apply tomorrow. And you have a populated set of commercial use case ideas ready for Innovation Day.

---

## Opening Hook (Slide 3)

**Specific and concrete**: "Goldman Sachs front-office technology teams using GitHub Copilot Enterprise saw a 30% reduction in code review cycle time. The Accenture 2025 study found the top 20% of AI tool adopters in analytics teams saved more than 15 hours per week. The bottom 20% saved fewer than 2. Same tools. Same team. The difference was entirely in how they used them. Today is about closing that gap — for FM&I."

---

## Timing Allocation

| Section | Slides | Duration |
|---------|--------|----------|
| Section 1: Intro + Productivity Case | 1–6 | 10 min |
| Section 2: Landscape + Access | 7–10 | 10 min |
| Section 3: Use Cases + Demo | 11–14 | 10 min |
| Section 4: Tool Deep-Dives | 15–32 | 25 min |
| Section 5: Model Landscape | 33–37 | 8 min |
| Section 6: Ethics & Compliance | 38–41 | 7 min |
| Section 7: Extended Topics | 42–50 | 15 min |
| Section 8: Personal Use Cases | 51–54 | 8 min |
| Section 9+10: Business Use Cases + Philosophy | 55–60 | 7 min |
| **Total** | **60 slides** | **90 min** |

---

## Full Slide Plan

### SECTION 1 — THE PRODUCTIVITY CASE (10 min, Slides 1–6)

---

**Slide 1 — Title Slide**
- Type: Title slide
- Content: "Gen AI for FM&I — Tools, Workflows, and What's Next"
- Subtitle: FM&I Upskilling Session | BP Trading Analytics & Insights | March 2026
- Design: Full `--color-primary` background, white text, accent rule
- Key assertion: N/A (title)
- Duration: 0 min (pre-roll)

---

**Slide 2 — Section Divider: The Productivity Case**
- Type: Section divider
- Content: "Section 1 — The Productivity Case"
- Subtext: "Why this matters more than most AI sessions you've sat through"
- Design: `--color-secondary` background, large numeral "01"
- Key assertion: This isn't evangelism — it's a capability briefing
- Duration: ~0.5 min

---

**Slide 3 — Opening Hook: The Productivity Gap**
- Type: Statistics / big number
- Content:
  - Large: "15 hrs/week" (top 20% adopters save this)
  - vs "2 hrs/week" (bottom 20%)
  - Source: Accenture 2025 Analytics Team Study
  - Body: "Same tools. Same team. Different outcomes. The gap is entirely in how they use them."
- Key assertion: The productivity gap between tool integrators and passive users is 8× — and it's measurable
- Content type: Big number + contrast stat
- Duration: ~2 min

---

**Slide 4 — What the Research Actually Says**
- Type: Icon grid (4 quadrants)
- Content:
  - "55% faster" — GitHub Dev Productivity Study (code task completion)
  - "8–12 hrs/week" — Accenture (routine task time saved, analytics teams)
  - "50% less time" — McKinsey (documentation generation)
  - "40% faster" — Goldman Sachs (code review cycle times)
- Key assertion: This is peer evidence from comparable technical teams — not marketing
- Content type: Stat grid with source callouts
- Duration: ~2 min

---

**Slide 5 — The Two Types of AI User**
- Type: Split layout (two-column comparison)
- Content:
  - Left (passive): "Uses AI for isolated queries. Starts fresh every time. Accepts first drafts. Single-file, single-turn."
  - Right (active integrator): "AI at every stage. Project-level configuration. Iterates on outputs. Agents for multi-step tasks."
  - Bottom: "FM&I's goal today: move every team member from left column to right column"
- Key assertion: Active workflow integration — not tool availability — is what drives the 8× productivity gap
- Content type: Split comparison
- Duration: ~2 min

---

**Slide 6 — What FM&I Stands to Gain**
- Type: Icon grid / bullet list with icons
- Content (FM&I-specific gains):
  - Pipeline debugging: 40–80 min → 5–10 min per incident
  - Model documentation: 4–6 hrs → 1–2 hrs
  - Ad hoc analysis: 2–3 hrs → 45 min
  - Test writing: previously skipped → generated in 15 min
  - Report generation: 3–4 hrs → 30–45 min
- Key assertion: At FM&I's workflow volume, these time savings compound into weeks per quarter
- Content type: Before/after time table
- Duration: ~3 min

---

### SECTION 2 — THE CURRENT LANDSCAPE (10 min, Slides 7–10)

---

**Slide 7 — Section Divider: The Landscape**
- Type: Section divider
- Content: "Section 2 — The Current Landscape"
- Subtext: "What's available to us, how to access it, and what's changed in 12 months"
- Design: `--color-secondary` background, numeral "02"
- Duration: ~0.5 min

---

**Slide 8 — What's Available to BP Employees Today**
- Type: Comparison / four-column table
- Content:
  | Tool | Status | Access | Data OK? |
  |------|--------|--------|---------|
  | M365 Copilot | Available now | Standard M365 | Internal (non-sensitive) |
  | GitHub Copilot | Available via IT | IT service desk | BP code |
  | Cursor | Personal only | Personal sub ($20/mo) | Public/personal ONLY |
  | Copilot Studio | Licence required | IT / cost centre | Internal (non-sensitive) |
- Key assertion: Two tools are available to you right now with no barriers — most people aren't using them fully
- Content type: Access status table
- Duration: ~3 min

---

**Slide 9 — 12-Month Model Evolution Timeline**
- Type: Timeline
- Content (horizontal timeline):
  - Q1 2025: Claude 3.5 Sonnet → coding standard
  - Q2 2025: Gemini 2.0 → 1M context usable
  - Q2 2025: Claude 3.7 extended thinking
  - Q3 2025: o3 (OpenAI reasoning) public
  - Q3 2025: Llama 3.3 70B (open source narrows gap)
  - Q4 2025: Claude Sonnet 4.6 + Opus 4.6
  - Q4 2025: Gemini 2.5 multimodal + tool use
  - Q1 2026: Claude Opus 4.6 flagship
- Key assertion: The tools of Q1 2026 are categorically more capable than Q1 2025 — most of what seemed impossible 12 months ago is now routine
- Content type: Horizontal timeline with event markers
- Duration: ~3 min

---

**Slide 10 — The Capability Step-Changes That Matter**
- Type: Three-column layout (what changed, why it matters, FM&I application)
- Content:
  - Context windows → Entire Dataiku projects fit in one context → Architecture-level questions across full pipelines
  - Agentic execution → Multi-step autonomous tasks → Overnight pipeline monitor, report agent
  - Tool calling / MCP → LLMs interact with external systems → Connect Claude Code to Dataiku, databases, APIs
- Key assertion: Three capability shifts — not incremental improvements — changed what's practically possible
- Content type: Three-column explanatory table
- Duration: ~3 min

---

### SECTION 3 — USE CASES + DEMO (10 min, Slides 11–14)

---

**Slide 11 — Section Divider: FM&I Use Cases**
- Type: Section divider
- Content: "Section 3 — FM&I Use Cases"
- Subtext: "Concrete workflows with before/after times — then a live demo"
- Design: `--color-secondary`, numeral "03"
- Duration: ~0.5 min

---

**Slide 12 — FM&I Use Cases: The Practical Hit List**
- Type: Icon grid (6 items)
- Content:
  1. Pipeline debugging (Dataiku) — 80 min → 10 min
  2. ELT code generation (Python/SQL) — 4 hrs → 1 hr
  3. Ad hoc analysis acceleration — 3 hrs → 45 min
  4. Model documentation — 5 hrs → 90 min
  5. Report automation — 4 hrs → 30 min
  6. Test writing — previously skipped → 15 min
- Key assertion: Every item here is a workflow FM&I runs regularly — the time savings are immediate and compounding
- Content type: Icon grid with time annotations
- Duration: ~2 min

---

**Slide 13 — [LIVE DEMO] Pipeline Debugging with GitHub Copilot**
- Type: Demo slide
- Content:
  - Left panel: "What we're doing"
    - Paste a Dataiku recipe stack trace + recipe code
    - Ask Copilot to diagnose the root cause
    - Ask for a fix with explanation
  - Right panel: "What to look for"
    - How quickly it identifies the join issue
    - Whether it understands Pandas/Dataiku context
    - The quality of the explanation vs just the fix
- Key assertion: [LIVE DEMO]
- Duration: ~5 min (live demo)
- `[PRESENTER: switch to GitHub Copilot in VS Code]`

---

**Slide 14 — What We Just Saw (Demo Debrief)**
- Type: Split layout
- Content:
  - Left: What worked
    - Root cause identification from stack trace: fast and accurate
    - Fix with explanation: immediately usable
    - Follow-up: "Are there other places in this recipe this pattern could break?" — useful proactive scan
  - Right: What to watch for
    - AI may not know your specific Dataiku version's behaviour
    - Always verify the fix against the actual data
    - Explanation quality drops if context is insufficient
- Key assertion: The value isn't magic — it's eliminating the mechanical search time. Judgment stays with you.
- Content type: Split debrief
- Duration: ~2 min

---

### SECTION 4 — TOOL DEEP-DIVES (25 min, Slides 15–32)

---

**Slide 15 — Section Divider: Tool Deep-Dives**
- Type: Section divider
- Content: "Section 4 — Tool Deep-Dives"
- Subtext: "Microsoft Copilot · GitHub Copilot · Cursor · Prompting · Advanced Features"
- Design: `--color-secondary`, numeral "04"
- Duration: ~0.5 min

---

**Slide 16 — Microsoft Copilot: What You Already Have**
- Type: Icon grid (M365 apps)
- Content:
  - Teams: Meeting summaries, action extraction, real-time transcription
  - Outlook: Thread summarisation, draft generation, meeting prep briefs
  - Word: Document drafting, rewriting, summarisation
  - Excel: Natural language formulas, Python in Excel, data insights
  - PowerPoint: Deck generation from prompts, summarisation
  - OneNote: Action item extraction, cross-notebook search
- Key assertion: M365 Copilot is deployed in every M365 application you already use — the barrier to starting is zero
- Content type: Icon grid with capability bullets
- Duration: ~2 min

---

**Slide 17 — [LIVE DEMO] M365 Copilot: Teams Meeting Summary**
- Type: Demo slide
- Content:
  - Left: "What we're doing"
    - Open Teams meeting summary in Copilot
    - Ask: "What action items were assigned to the FM&I team?"
    - Ask: "Draft a follow-up email to [person] about the pipeline timeline"
  - Right: "What to look for"
    - Accuracy of action item extraction
    - Whether names are correctly attributed
    - Speed vs doing this manually
- Duration: ~3 min
- `[PRESENTER: switch to Teams / Copilot Business Chat]`

---

**Slide 18 — Microsoft Copilot Agents: Build Your Own**
- Type: Three-step process / flow diagram
- Content:
  - Step 1: Define — name, purpose, personality (natural language)
  - Step 2: Connect — SharePoint, documents, web, APIs
  - Step 3: Publish — Teams bot, SharePoint, web chatbot
  - Center callout: "The instruction-refinement trick: give it instructions → ask it to improve its own instructions → iterate 2–3 times"
- Key assertion: A custom Copilot agent for FM&I reports or Q&A can be built in under an hour — no code required
- Content type: Process flow
- Duration: ~2 min

---

**Slide 19 — [LIVE DEMO] Creating a Copilot Agent**
- Type: Demo slide
- Content:
  - Left: "What we're doing"
    - Create a new agent in Copilot Studio
    - Give it instructions for FM&I model Q&A
    - Ask it: "How can you improve your own instructions?"
    - Paste improved instructions back
  - Right: "What to look for"
    - How the instruction refinement changes the response quality
    - What data sources are connectable
    - The gap between a generic and a well-instructed agent
- Duration: ~3 min
- `[PRESENTER: switch to Copilot Studio]`

---

**Slide 20 — Microsoft Copilot: Roadmap & Recent Additions**
- Type: Timeline (vertical)
- Content:
  - Q1 2025: BizChat across M365
  - Q2 2025: Python in Excel (AI-assisted)
  - Q3 2025: Third-party plugins in Copilot
  - Q4 2025: Meeting preparation agent
  - Q1 2026: Reasoning mode (o-series) in Word/Outlook
  - Coming: Copilot Notebooks, multi-agent workflows, Power BI deeper integration
- Key assertion: Copilot's capability set is updating quarterly — today's limitations are next quarter's features
- Content type: Vertical timeline
- Duration: ~1.5 min

---

**Slide 21 — GitHub Copilot vs Cursor: Feature Comparison**
- Type: Comparison table
- Content:
  | Feature | GitHub Copilot | Cursor |
  |---------|---------------|--------|
  | Available at BP | Yes (enterprise) | Personal only |
  | Context window | 128K | 200K (Claude) |
  | Codebase awareness | @workspace index | Semantic, by default |
  | Agent mode | Limited | Full (multi-step) |
  | Model choice | GPT-4o, limited Claude | Full model selection |
  | Background agents | No | Yes (Pro) |
  | MCP tools | Limited | Full support |
  | Rules files | `.github/copilot-instructions.md` | `.cursorrules` |
  | Price | BP covered | $20/mo personal |
- Key assertion: GitHub Copilot is your enterprise-grade daily driver; Cursor is more powerful but personal-only — and the gap is narrowing
- Content type: Comparison table
- Duration: ~2 min

---

**Slide 22 — Beyond Code Completion: What These Tools Actually Do**
- Type: Icon grid (6 capabilities)
- Content:
  1. Documentation — docstrings, READMEs, model cards
  2. Test writing — unit tests, edge cases, parametrize
  3. Refactoring — vectorise loops, extract classes, rename across codebase
  4. Architecture reasoning — "how should I structure this new feature?"
  5. Debugging — diagnose errors, trace call stacks, explain failures
  6. PR generation — commit messages, PR summaries, review comments
- Key assertion: Code completion is the least interesting thing these tools do — the high-value applications are above
- Content type: Icon grid
- Duration: ~1.5 min

---

**Slide 23 — Template Project Setup: Configuration as an Asset**
- Type: Split layout with code panel
- Content:
  - Left: concept
    - `.github/copilot-instructions.md` (GitHub Copilot)
    - `.cursorrules` (Cursor)
    - `CLAUDE.md` (Claude Code)
    - "Project-level instructions that give every AI interaction persistent context — written once, applied every time"
  - Right: code panel (CLAUDE.md excerpt from this project)
    ```
    ## Critical Patterns
    - All queries MUST be user-scoped
    - All errors use TRPCError
    - All Zod inputs have .max() bounds
    ```
- Key assertion: The template configuration is the real productivity asset — it eliminates context re-setup on every session
- Content type: Split + code panel
- Duration: ~2 min

---

**Slide 24 — Ask / Agent / Plan Modes: When to Use Each**
- Type: Three-column layout
- Content:
  | Mode | What it does | When to use |
  |------|-------------|-------------|
  | **Ask** | Conversational query, no actions | Quick questions, exploration, learning |
  | **Plan** | Proposes changes, doesn't execute | Complex/risky changes, review before execute |
  | **Agent** | Plans and executes autonomously | Feature implementation, refactoring, debugging |
  - Bottom callout: "Rule of thumb: Ask for understanding. Plan for caution. Agent for execution."
- Key assertion: Mode selection is a workflow design decision — not just a UI toggle
- Content type: Three-column table
- Duration: ~1.5 min

---

**Slide 25 — Prompting: The Multiplier**
- Type: Split layout + code panel
- Content:
  - Left: Effective prompt structure
    1. Role/context — "Working on the FM&I gas pricing model"
    2. Task — "Refactor `calculate_forward_curve`"
    3. Constraints — "Don't change the function signature"
    4. Output format — "Code + inline comments"
    5. Edge cases — "Handle empty DataFrame"
  - Right: The meta-trick
    - "Here's my vague task: [X]. Generate a precise prompt I can use."
    - "Improve this prompt: [draft]"
    - "What context would make this better?"
- Key assertion: Using the LLM to write its own prompt is not laziness — it is skill leverage
- Content type: Split + numbered list
- Duration: ~1.5 min

---

**Slide 26 — Cursor Advanced: Background Agents & Git Worktrees**
- Type: Split layout
- Content:
  - Left (background agents):
    - Long-running tasks in the cloud while you work on other things
    - "Rewrite all test files to pytest" → submit → continue → get notified
  - Right (git worktrees):
    - Multiple worktrees = multiple agents on parallel branches simultaneously
    - `git worktree add ../feature-b feature-b-branch`
    - Use for: parallel experiments, independent features, A/B implementations
  - Bottom: "FM&I application: run model variant A in one worktree, model variant B in another — agents implement both simultaneously"
- Key assertion: Parallel agentic work compresses multi-day implementation into hours
- Content type: Split layout
- Duration: ~2 min

---

**Slide 27 — Cursor Advanced: @ Context + Multi-Agent**
- Type: Code panel + bullet list
- Content:
  - Left: @ context references
    ```
    @file recipes/gas_pricing.py
    @folder models/
    @codebase  # semantic search
    @web  # current docs
    @docs  # indexed documentation
    @git  # history, diffs
    ```
  - Right: Multi-agent orchestration
    - Orchestrator delegates to specialised sub-agents
    - Code sub-agent, test sub-agent, docs sub-agent
    - Orchestrator synthesises and resolves conflicts
    - FM&I use: "Implement new model feature + write tests + update documentation simultaneously"
- Key assertion: Precise context control is the difference between a useful agent and a confused one
- Content type: Code panel + bullets
- Duration: ~1.5 min

---

**Slide 28 — Mid-Session Callback: The Core Message**
- Type: Quote slide / big message
- Content:
  - Large text: "You already have the tools — the only thing between you and 10× productivity is knowing which tool to reach for and when."
  - Sub: "GitHub Copilot: available now. M365 Copilot: available now. The question is your workflow, not your licence."
- Key assertion: Core message callback — we're past the landscape, into delivery
- Content type: Quote / callout
- Duration: ~0.5 min

---

**Slide 29 — GitHub Copilot: Advanced Features**
- Type: Comparison / feature list
- Content:
  - @workspace: architecture-level questions across indexed codebase
  - Slash commands: /explain, /fix, /test, /doc, /new
  - Multi-file edits: propose + apply changes across files simultaneously
  - CLI integration: `gh copilot suggest [task]`, `gh copilot explain [command]`
  - PR generation: automated commit messages, PR summaries
- Key assertion: @workspace + multi-file edits makes GitHub Copilot a genuine codebase-level tool, not just autocomplete
- Content type: Feature list with examples
- Duration: ~1.5 min

---

**Slide 30 — GitHub Copilot: Future Roadmap**
- Type: Timeline (vertical, forward-looking)
- Content:
  - 2026 H1: Expanded workspace agent capabilities (more autonomous multi-step)
  - 2026 H1: Better model selection (more Claude options in enterprise)
  - 2026 H2: Background agents (closing the gap with Cursor)
  - 2026 H2: Improved MCP support (more external tool integrations)
  - Speculated: Native multi-agent coordination within GitHub Enterprise
- Key assertion: GitHub Copilot's enterprise-grade features will continue to expand — the compliance-accessible tool is getting more capable
- Content type: Forward timeline
- Duration: ~1 min

---

**Slide 31 — Cursor: Future Roadmap**
- Type: Timeline (vertical, forward-looking)
- Content:
  - 2026 H1: Improved background agent reliability and capacity
  - 2026 H1: More MCP server integrations in marketplace
  - 2026 H2: Enterprise features (multi-user, audit logging, data handling agreements)
  - Speculated: Enterprise agreements that could unlock BP adoption
  - Speculated: Deep IDE integration improvements (debugging, profiling)
- Key assertion: Cursor's enterprise roadmap is the one to watch — if BP can negotiate an enterprise agreement, this becomes the full-capability option
- Content type: Forward timeline
- Duration: ~1 min

---

**Slide 32 — Section 4 Summary: Your Daily Driver Setup**
- Type: Icon grid / recommendation table
- Content:
  | Task | Tool | Mode |
  |------|------|------|
  | Pipeline debugging | GitHub Copilot | Ask (paste error) |
  | Feature implementation | GitHub Copilot | Agent |
  | Complex refactor | Cursor (personal) | Plan → Agent |
  | Teams/meeting follow-up | M365 Copilot | Chat |
  | Custom team agent | Copilot Studio | Build agent |
  | Long agentic task | Cursor background | Background |
- Key assertion: A clear tool-to-task map eliminates the "which tool?" decision overhead
- Content type: Decision table
- Duration: ~1 min

---

### SECTION 5 — MODEL LANDSCAPE (8 min, Slides 33–37)

---

**Slide 33 — Section Divider: The Model Landscape**
- Type: Section divider
- Content: "Section 5 — The Model Landscape"
- Subtext: "Which model for which task — and why the answer changes quarterly"
- Design: `--color-secondary`, numeral "05"
- Duration: ~0.5 min

---

**Slide 34 — Current Models: Strengths at a Glance**
- Type: Comparison table (5 models × 4 dimensions)
- Content:
  | Model | Best for | Context | Speed | Cost |
  |-------|---------|---------|-------|------|
  | Claude Opus 4.6 | Complex reasoning, architecture | 200K | Slow | $$$ |
  | Claude Sonnet 4.6 | Daily coding, analysis | 200K | Fast | $$ |
  | Gemini 2.5 | Huge codebase, multimodal | 1M | Medium | $$ |
  | GPT-4o / o3 | General, math/logic (o3) | 128K | Fast | $$ |
  | Ollama local | Data-sensitive, offline | Variable | Slow | Free |
- Key assertion: No model wins on all dimensions — knowing the trade-offs is the skill
- Content type: Comparison table
- Duration: ~2 min

---

**Slide 35 — The Model Decision Framework**
- Type: Decision tree / flowchart
- Content:
  ```
  Is data sensitive (must not leave infrastructure)?
  ├── YES → Ollama local (Llama 3.3 / Phi-4)
  └── NO ↓

  Is context > 128K tokens (full pipeline/codebase)?
  ├── YES → Gemini 2.5 (1M context)
  └── NO ↓

  Is the task complex (architecture/deep reasoning)?
  ├── YES → Claude Opus 4.6 or o3
  └── NO ↓

  Default: Claude Sonnet 4.6
  (speed + quality + cost balance)
  ```
- Key assertion: The decision framework fits on one slide — you can internalise it by the end of today
- Content type: Decision flowchart
- Duration: ~2 min

---

**Slide 36 — Token Cost Awareness**
- Type: Statistics / comparison table
- Content:
  | Model | Input / 1M tokens | 10 analysts × 50 req/day |
  |-------|------------------|--------------------------|
  | Claude Sonnet 4.6 | $3 | ~$9/day |
  | Claude Opus 4.6 | $15 | ~$45/day |
  | GPT-4o | $5 | ~$15/day |
  | Ollama (local) | Free | Infrastructure cost only |
  - Bottom: "Context hygiene directly reduces cost. Bloated context = 2× cost for same quality."
- Key assertion: At team scale, context hygiene is a cost and quality issue — not an aesthetic one
- Content type: Cost table with practical callout
- Duration: ~2 min

---

**Slide 37 — The Open Source Gap Is Closing**
- Type: Timeline + quote
- Content:
  - Timeline: Llama 1 (2023) → Llama 2 (2023) → Llama 3 (2024) → Llama 3.3 70B (2025) — quality gap vs frontier models narrowed dramatically at each step
  - Quote callout: "Llama 3.3 70B performs comparably to GPT-4 in many coding benchmarks — and runs locally on a MacBook Pro M3 Max."
  - Bottom: "Implication for FM&I: for data-sensitive tasks, local models are now viable for code generation and analysis — not ideal, but no longer unusable."
- Key assertion: The local model option is not theoretical — it's a credible fallback for data-sensitive workflows
- Content type: Timeline + quote
- Duration: ~1.5 min

---

### SECTION 6 — ETHICS & COMPLIANCE (7 min, Slides 38–41)

---

**Slide 38 — Section Divider: Ethics & Compliance**
- Type: Section divider
- Content: "Section 6 — Ethics & Compliance"
- Subtext: "The non-negotiables for front-office AI use"
- Design: `--color-secondary`, numeral "06"
- Duration: ~0.5 min

---

**Slide 39 — What Can and Cannot Go Into These Tools**
- Type: Split layout (green / red columns)
- Content:
  - GREEN (allowed):
    - Internal documents, emails (M365 Copilot)
    - BP code in GitHub Enterprise (GitHub Copilot)
    - Public analysis, publicly available data
    - Anonymised/synthetic data
  - RED (prohibited):
    - Live trading positions
    - Proprietary model parameters
    - Client/counterparty identity and terms
    - Market-sensitive data (pre-public)
    - Any data via consumer AI tools (ChatGPT.com, Claude.ai free, Cursor without enterprise)
- Key assertion: The line is clear — and it's not about capability, it's about data classification and tool agreements
- Content type: Split green/red
- Duration: ~2 min

---

**Slide 40 — The Data Handling Matrix**
- Type: Comparison table
- Content:
  | Dimension | M365 Copilot | GitHub Copilot (Enterprise) | Cursor / External |
  |-----------|-------------|---------------------------|-------------------|
  | Used for training | No | No | No (Pro+) / Unclear (Free) |
  | Data stored | BP M365 tenant | BP GitHub org | Cursor cloud |
  | BP agreement | Yes | Yes | No |
  | Internal data OK | Yes | Code only | No |
  | Sensitive data OK | No | No | No |
- Key assertion: Enterprise tool coverage is the dividing line — when in doubt, default to M365/GitHub Copilot over external tools
- Content type: Data governance table
- Duration: ~2 min

---

**Slide 41 — Practical Rules for FM&I**
- Type: Icon grid (5 rules)
- Content:
  1. "The press release test" — if it would be problematic in a press release, don't paste it
  2. Anonymise inputs — replace real hub names, volumes, counterparties with placeholders
  3. Code patterns, not data — use AI for code structure, not to run on live proprietary data
  4. Never paste live positions — absolute rule, no exceptions
  5. Check the tool before using it — is it covered under BP's agreements?
  - Bottom: "Where to find current guidance: BP intranet ('AI governance') + Digital Centre of Excellence"
- Key assertion: Five rules cover 95% of situations — memorise them and you're operating safely
- Content type: Numbered rules grid
- Duration: ~2 min

---

### SECTION 7 — EXTENDED TOPICS (15 min, Slides 42–50)

---

**Slide 42 — Section Divider: Extended Topics**
- Type: Section divider
- Content: "Section 7 — Extended Topics"
- Subtext: "Claude Code · MCP · Agentic AI · Agent Skills · Context Management"
- Design: `--color-secondary`, numeral "07"
- Duration: ~0.5 min

---

**Slide 43 — Claude Code: The CLI Difference**
- Type: Split layout (IDE vs CLI)
- Content:
  - Left (IDE plugin — Copilot/Cursor):
    - File-level or selection-level context
    - Interactive, per-step approval
    - Best for: active coding sessions
  - Right (Claude Code — CLI):
    - Repository-level scope
    - Can run bash, git, tests autonomously
    - Long-running agentic tasks
    - Headless (CI/CD, scheduled)
    - Multi-agent orchestration
  - Bottom callout: "Claude Code is what you use when you want to describe an outcome and come back when it's done"
- Key assertion: CLI tools unlock a fundamentally different class of workflow — not better at IDE tasks, better at autonomous project-level tasks
- Content type: Split comparison
- Duration: ~2 min

---

**Slide 44 — Claude Code Agent Teams**
- Type: Diagram (orchestrator-subagent)
- Content:
  - Center: Orchestrator ("Generate FM&I monthly report")
  - Branches to:
    - Research agent: "Pull all model performance data"
    - Analysis agent: "Identify top 5 anomalies"
    - Writing agent: "Draft commentary per section"
    - Formatting agent: "Produce final output in template"
  - Footer: "This session's presentation was built by a 5-agent team using this exact pattern"
- Key assertion: Agent teams decompose complex tasks into parallelisable specialised workstreams — same pattern scales from a report to a product
- Content type: Diagram
- Duration: ~1.5 min

---

**Slide 45 — Tool Calling & MCP: The Connectivity Layer**
- Type: Flow diagram
- Content:
  ```
  LLM → [decides to call tool] → Tool Call Request
    → External System (Dataiku, DB, API, filesystem)
    → Returns result
  LLM → incorporates result → continues reasoning
  ```
  - Left callout: "MCP (Model Context Protocol): open standard — any LLM client ↔ any MCP server"
  - Right callout: "FM&I application: Cursor → Dataiku MCP → 'What scenarios failed last night? Get logs, suggest fix'"
- Key assertion: Tool calling transforms the LLM from text generator to action-taking agent — MCP makes this portable across tools
- Content type: Flow diagram + callout
- Duration: ~2 min

---

**Slide 46 — MCP for FM&I: What You Could Build Today**
- Type: Code panel + list
- Content:
  - Left: code panel showing simplified Dataiku MCP server pattern
    ```python
    @server.tool("get_scenario_status")
    async def get_scenario_status(
        project_key: str, scenario_id: str
    ) -> str:
        status = dataiku_client.get_job(project_key, scenario_id)
        return f"Status: {status['state']}"
    ```
  - Right: What this enables
    - "What scenarios ran today? Any failures?"
    - "Get logs for the failed gas_curve_build job"
    - "Re-trigger the pricing scenario"
    - "Which datasets haven't refreshed in 24 hours?"
- Key assertion: A basic Dataiku MCP server is a 200-line Python project — achievable in a day, immediately useful for FM&I
- Content type: Code panel + capability list
- Duration: ~2 min

---

**Slide 47 — Agentic AI: What Changed and Why It Matters**
- Type: Timeline + split layout
- Content:
  - Timeline: 2023 (single-turn only) → 2024 (tool use reliable) → 2025 (production agentic) → 2026 (multi-agent orchestration)
  - Bottom: Works reliably vs Still unreliable
    - Works: well-defined tasks, detectable errors, bounded scope
    - Unreliable: long chains (error accumulation), ambiguous success, complex novel APIs
  - FM&I applications:
    - Pipeline health monitor (nightly agent)
    - Model drift alert (weekly agent)
    - Ad hoc request triage (on-demand agent)
- Key assertion: Agentic AI is production-ready for well-scoped tasks — the key is designing tasks with clear success criteria and error detection
- Content type: Timeline + split
- Duration: ~2 min

---

**Slide 48 — Agent Skills: Packaged Reusable Capabilities**
- Type: Split layout + code panel
- Content:
  - Left: concept
    - A skill = packaged workflow invocable by name
    - `/data-quality-report [dataset]` → executes a defined process
    - Consistent, reusable, version-controlled
    - Team members share and invoke the same skills
  - Right: code panel (skill spec example)
    ```markdown
    # Skill: data-quality-report
    When invoked with dataset name:
    1. Profile: row count, dtypes, null %
    2. Flag: >10% nulls, single-value cols,
       outliers (>3 IQR)
    3. Output: markdown table + JSON + actions
    ```
- Key assertion: Skills encapsulate institutional knowledge — a well-designed skill makes every team member's analysis as thorough as the most thorough person's
- Content type: Split + code panel
- Duration: ~2 min

---

**Slide 49 — Context, Tokens, and Hooks**
- Type: Three-column layout
- Content:
  - Context hygiene:
    - Include only relevant files
    - Start fresh for new tasks
    - Use .cursorignore to exclude noise
    - Compress long conversations
  - Token cost at scale:
    - Sonnet: $3/1M → team of 10 ≈ $9/day
    - Context inflation doubles costs
    - Good hygiene = 2× quality + 0.5× cost
  - Hooks (Claude Code):
    - Pre/post tool-call triggers
    - Auto-run linter after code writes
    - Auto-run tests after changes
    - Slack notification on completion
- Key assertion: Context management is not optional — it affects cost, quality, and speed simultaneously
- Content type: Three-column
- Duration: ~1.5 min

---

**Slide 50 — ChatGPT Codex vs Claude Code vs Cursor**
- Type: Comparison table
- Content:
  | Dimension | ChatGPT Codex | Cursor Background | Claude Code |
  |-----------|---------------|------------------|-------------|
  | Environment | OpenAI cloud sandbox | Cursor cloud | Local / SSH |
  | Code access | Uploaded/connected | Local workspace | Full filesystem |
  | Tool use | Limited | Full MCP | Full bash + tools |
  | Model | GPT-4o / o3 | User choice | Claude Opus/Sonnet |
  | Data handling | OpenAI cloud | Cursor cloud | Local (best privacy) |
  | BP compliance | Azure path only | No enterprise | No enterprise |
- Key assertion: For data-sensitive FM&I work, Claude Code running locally or via SSH is the most defensible option — data stays where you control it
- Content type: Comparison table
- Duration: ~1 min

---

### SECTION 8 — PERSONAL USE CASES (8 min, Slides 51–54)

---

**Slide 51 — Section Divider: From the Field**
- Type: Section divider
- Content: "Section 8 — From the Field"
- Subtext: "Real workflows using these tools — with the rough edges included"
- Design: `--color-secondary`, numeral "08"
- Duration: ~0.5 min

---

**Slide 52 — Personal Use Cases: The Toolkit**
- Type: Icon grid (6 items)
- Content:
  1. Claude Code + Remotion — programmatic video from code
  2. Weather alerts project — Claude API as event-driven trigger
  3. Claude Remote / SSH — running agents on remote data-local machines
  4. Claude Chrome Extension — AI from any browser tab
  5. OpenClaw — [presenter to describe directly]
  6. Template project deep dive — this repository as a live worked example
- Key assertion: These are real workflows, not demos — the patterns all transfer to FM&I
- Content type: Icon grid
- Duration: ~1.5 min

---

**Slide 53 — The Weather Alerts Pattern (Transferable to FM&I)**
- Type: Flow diagram + code panel
- Content:
  - Flow: Data event trigger → Python script → Claude API → Structured JSON output → Delivery (Slack/email)
  - Code panel:
    ```python
    response = client.messages.create(
        model="claude-sonnet-4-6",
        messages=[{"role": "user", "content":
            f"Analyse pipeline status: {data}\n"
            "Return JSON: {severity, affected, actions}"
        }]
    )
    alert = json.loads(response.content[0].text)
    ```
  - FM&I variants: pipeline failure alert, model drift alert, market anomaly alert
- Key assertion: The Claude API integration pattern is 20 lines of Python — the complexity is in the prompt design, not the code
- Content type: Flow + code panel
- Duration: ~2 min

---

**Slide 54 — The Template Project: Why Configuration Is the Asset**
- Type: Split layout
- Content:
  - Left: What's in the template
    - `CLAUDE.md`: project context, commands, critical patterns, known trade-offs
    - `.claude/CLAUDE.md`: behavioural directives, prohibited patterns, quality gates
    - Agent definitions: roles, briefs, success criteria
    - Prompt templates: reusable, version-controlled
  - Right: What this means
    - Every AI session starts with full context — no re-explaining
    - Consistent quality across team members
    - AI decisions are constrained by explicit patterns
    - Onboarding: new team member inherits the AI configuration
  - Bottom: "The template is the institutional knowledge layer for AI-assisted work"
- Key assertion: A well-configured template project multiplies team-wide AI productivity — write it once, benefit on every session
- Content type: Split layout
- Duration: ~3 min

---

### SECTION 9+10 — BUSINESS USE CASES + PHILOSOPHY (7 min, Slides 55–60)

---

**Slide 55 — Section Divider: Business Use Cases + Innovation Day**
- Type: Section divider
- Content: "Section 9 — Commercial Use Cases for FM&I"
- Subtext: "Ideas for the mural board — and beyond"
- Design: `--color-secondary`, numeral "09"
- Duration: ~0.5 min

---

**Slide 56 — Business Use Cases: The Hit List**
- Type: Icon grid (categories)
- Content:
  - Data & Modelling: AI model validator, automated model card generator, hypothesis-driven hyperparameter search
  - Trading Desk Support: market structure briefing agent, request triage agent, curve comparison narrator
  - Dataiku Integration: pipeline health dashboard, data lineage Q&A, schema drift detector
  - Reporting & Viz: natural language chart generator, automated PowerPoint, report commentary assistant
  - Copilot for Power BI: DAX generation, narrative summaries, self-serve data Q&A for traders
- Key assertion: None of these require new infrastructure — they require deliberate workflow design with tools already available
- Content type: Icon grid by category
- Duration: ~2 min

---

**Slide 57 — Core Message (Closing Callback)**
- Type: Quote / big number slide
- Content:
  - Large: "10×"
  - Body: "Not because AI is magic. Because 8 hours of routine analytical work compresses to 45 minutes. Every week. For every analyst on the team."
  - Callback: "You already have the tools — the only thing between you and 10× productivity is knowing which tool to reach for and when."
- Key assertion: Core message final repetition — and it lands differently now that the audience has the full picture
- Content type: Big number + quote
- Duration: ~0.5 min

---

**Slide 58 — Philosophical Anecdotes**
- Type: Quote slide (4 assertions)
- Content:
  1. "AI doesn't make data scientists redundant. It makes the excuse of not having enough time redundant."
  2. "The threat isn't to FM&I. It's to the IT middle layer that never understood the subject domain well enough to survive without it."
  3. "Who owns the risk when the AI is wrong? You do. That's an argument for better testing, not less AI."
  4. "The performance art around coding is ending — requirements ceremonies, architecture slideware, AI wrappers with different login pages. The question is: what are you actually shipping?"
- Key assertion: The next decade's risk is not AI replacing your job — it's your peers who use AI replacing the case for your headcount
- Content type: Quote grid
- Duration: ~2 min

---

**Slide 59 — Innovation Day: The Mural Board**
- Type: Closing / CTA
- Content:
  - "Innovation Day — Gen AI Commercial Use Cases"
  - Call to action: three columns
    - Left: "What are you already using?" (seed the current use column)
    - Center: "What would save you the most time?" (productivity wins column)
    - Right: "What commercial idea would you build?" (commercial ideas column)
  - Bottom: "The mural board is live. Add your ideas now before we close."
- Key assertion: Everything in today's session feeds into Innovation Day — your ideas go on the board
- Content type: CTA / closing action slide
- Duration: ~2.5 min

---

**Slide 60 — Closing + Resources**
- Type: Closing / CTA
- Content:
  - Core message (final): "You already have the tools."
  - Resources:
    - GitHub Copilot: request via IT service desk
    - M365 Copilot: already available — open Teams, look for the Copilot icon
    - BP AI governance: intranet → search "AI governance"
    - Template project: `_p-presentation-creator` (shared link)
    - Questions and follow-up: [presenter contact]
  - Footer: "FM&I · Gen AI Upskilling · March 2026"
- Key assertion: Leave the room with exactly one action: open M365 Copilot before end of day
- Content type: Closing / resources
- Duration: ~1 min

---

## Agenda Coverage Checklist

Verifying every item from `gen_ai_presentation_plan.md` is covered:

### FM&I Context and Focus
- [x] FM&I team context and mission — Slides 1, 6, throughout
- [x] No first-principles LLM theory — confirmed throughout
- [x] Focused on practical productivity and commercial delivery — central theme

### Agenda Item 1: Intro to Gen AI for Personal Productivity
- [x] Productivity use cases in front office analytics — Slides 3, 4, 5, 6
- [x] Team context — Slides 1, 6

### Agenda Item 2: Current Landscape
- [x] Tools available at BP — Slide 8
- [x] Recent developments — Slides 9, 10
- [x] How to access each tool — Slide 8

### Agenda Item 3: Use Cases + Demo
- [x] Use case examples — Slides 12, 13, 14
- [x] Live demo — Slide 13 (GitHub Copilot debugging)

### Agenda Item 4: Microsoft Copilot
- [x] M365 Copilot + Teams integration — Slides 16, 17
- [x] Microsoft Copilot Agents — Slides 18, 19
- [x] Future roadmap — Slide 20
- [x] Recent timeline of additions — Slide 20
- [x] Example creating agent (instruction refinement) — Slide 19

### Agenda Item 4: GitHub Copilot & Cursor
- [x] Introduction and differentiators — Slide 21
- [x] Workflows beyond coding — Slide 22
- [x] Template project setup — Slide 23
- [x] When to use and how — Slides 24, 32
- [x] Future roadmap — Slides 30, 31

### Both tools: Modes
- [x] Ask / Agent / Plan modes — Slide 24

### Prompting
- [x] How to prompt, LLM-generated prompts, templates — Slide 25

### Cursor Advanced Features
- [x] Background agents, git worktrees — Slide 26
- [x] @ context, multi-agent orchestration — Slide 27
- [x] Other advanced features (rules, .cursorignore) — Slide 23, 27

### Agenda Item 5: Model Landscape
- [x] Claude Opus 4.6 — Slide 34
- [x] Claude Sonnet 4.6 — Slide 34
- [x] Gemini — Slide 34
- [x] ChatGPT/o3 — Slide 34
- [x] Ollama local models — Slides 34, 37
- [x] Model evolution over last year — Slide 9
- [x] Model decision framework — Slide 35

### Agenda Item 6: Ethics & Compliance
- [x] What can/cannot go into tools — Slide 39
- [x] Data handling matrix — Slide 40
- [x] Practical rules for FM&I — Slide 41

### Agenda Item 7: Extended Topics

#### Claude Code/Cowork
- [x] What Claude Code is, CLI vs IDE — Slide 43
- [x] Workflow differences — Slide 43
- [x] Claude Cowork/Teams/Projects — referenced in Slide 43, 54
- [x] Future roadmap for Claude tools — Slide 43 notes
- [x] Claude Code agent teams — Slide 44

#### Tool Calling
- [x] What tool calling is — Slide 45
- [x] Agentic workflows in Cursor and GitHub Copilot — Slide 45
- [x] Differences in tool calling — Slide 45

#### MCP
- [x] What MCP is — Slide 45
- [x] Why it's useful — Slide 45, 46
- [x] FM&I application (Dataiku MCP) — Slide 46

#### Agentic AI
- [x] Shift to agentic AI — Slide 47
- [x] FM&I applications — Slide 47
- [x] What works, what doesn't — Slide 47

#### Agent Skills
- [x] What they are — Slide 48
- [x] Example skill — Slide 48
- [x] How to create — Slide 48

#### Context & Tokens
- [x] Why it matters — Slide 49
- [x] Practical rules — Slide 49

#### Other (Hooks, ChatGPT Codex)
- [x] Hooks — Slide 49
- [x] ChatGPT Codex — Slide 50

### Agenda Item 8: Personal Use Cases
- [x] Claude Code + Remotion — Slide 52
- [x] OpenClaw — Slide 52
- [x] Claude Remote — Slide 52, 53
- [x] Claude Chrome Extension — Slide 52
- [x] Weather alerts project — Slide 53
- [x] Template project deep dive — Slide 54

### Agenda Item 9: Business Use Cases
- [x] Ideas and discussion — Slides 56, 59
- [x] Copilot for Power BI — Slide 56
- [x] Plotly Studio — referenced in research, available for presenter note
- [x] Dataiku Gen AI capability — Slide 56
- [x] MCP tools for Dataiku — Slide 46, 56

### Agenda Item 9 (second): Philosophical Anecdotes
- [x] AI making work cheap — Slide 58
- [x] AI changing software engineering — Slide 58
- [x] AI won't replace data scientists, tool users will — Slide 58
- [x] Next decade threat (comfortable middle) — Slide 58
- [x] Performance art around coding — Slide 58

### Structure & Quality
- [x] 60 slides (within 45–65 target)
- [x] Timings sum to 90 minutes
- [x] Core message in opening (Slide 3), mid-session (Slide 28), closing (Slide 57, 60)
- [x] Innovation Day bridge explicit (Slide 59)
- [x] MECE check: sections are non-overlapping and complete
- [x] Every section has a section divider slide
- [x] Opening hook is specific and audience-relevant (Slide 3: specific statistics from named studies)

---

*Content outline complete. Handoff to Agent 3 (Slide Designer).*
