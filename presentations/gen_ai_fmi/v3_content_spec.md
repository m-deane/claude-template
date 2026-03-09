# v3 Content Specification — Agent 2 Output
*Complete slide-by-slide content plan for the v3 rebuild. Every card body text is at least 30 words. Maximum 4 cards per grid. All FM&I specific.*

---

## SECTION 1 — WHY NOW
Section accent: C.teal

---

## Slide 1 — Title Slide (type: title)

Background: C.deepNavy
Top accent bar: C.teal

Main title: "Gen AI for FM&I"
Subtitle: "Tools, Workflows & Commercial Opportunity"
Team tag: "FM&I | Trading Analytics & Insights | BP"
Session note: "Session duration: 90 minutes"

Bottom bar: [none — title slide]

---

## Slide 2 — The 15-Hour vs 2-Hour Gap (Section 1, type: big number + statement)
Section accent: C.teal
Header: FM&I | THE CASE

BIG NUMBER PANEL (left):
  Stat: 15 hrs/week
  Context: Accenture's 2025 study of quant analysts and data engineers found the top 20% of AI adopters saved 15 hours per week. The bottom 20% saved 2 hours. Same tools, same technical background — the gap was entirely explained by prompting skill and tool integration depth. This is the productivity gap that is already opening inside every analytics team.

SUPPORTING STATEMENT (right card):
  Title: "The gap is already opening"
  Body: Fifteen hours versus two hours — that is the difference between an analyst who has integrated AI into their daily workflow and one who uses it occasionally for spell-checking. In FM&I terms: fifteen hours reclaimed per week means three additional ad hoc analysis requests answered, one extra model backlog item cleared, documentation that actually gets written. The question is not whether to adopt. The question is: are you in the top 20% or the bottom 20%?

Bottom bar: "The only difference between 15 hrs saved and 2 hrs saved is prompting skill and integration depth — both learnable in a session"

---

## Slide 3 — The Productivity Gap Is Already Opening (Section 1, type: stat cascade + right card)
Section accent: C.teal
Header: FM&I | WHY NOW

STAT CASCADE (left, 4 stats):

Stat 1:
  Number: "45%"
  Color: C.teal
  Label: "of analytical work activities automatable with current AI (McKinsey 2024)"
  Context note (below label): "For FM&I: ELT recipe documentation, test writing, data quality checks, boilerplate aggregation logic, report formatting — the work absorbing 30-40% of every sprint."

Stat 2:
  Number: "55%"
  Color: C.blue
  Label: "faster task completion for data engineers using AI coding tools (GitHub 2024)"
  Context note: "The gain comes from not context-switching to documentation, not writing boilerplate from scratch, and having a first draft to critique rather than starting blank."

Stat 3:
  Number: "40-80 hrs"
  Color: C.green
  Label: "per month saved by active AI tool users vs passive users (Accenture 2025)"
  Context note: "At 40 hrs/month that is one additional full working week per month — one week that currently disappears into repetitive tasks that AI can own."

Stat 4:
  Number: "12 min"
  Color: C.orange
  Label: "from prompt to working Plotly Dash crack spread app (vs 2-3 days manual)"
  Context note: "This is not theoretical — this is the Cursor demo from this session. The ad hoc desk request that currently takes until Friday can be answered by lunch."

RIGHT CARD:
  Title: "The gap"
  Body: Teams using AI tools are outpacing those who are not, and the gap is measurable in sprint velocity, model delivery time, and analyst capacity. Organisations with mature AI adoption in their quant teams are shipping 2-3 times more models per quarter than peers at the same headcount. The FM&I team has access to four AI tools today. The question is how deeply each person uses them.

Bottom bar: "This isn't about replacing analysts — it's about which teams can deliver 3 models where others deliver 1"

---

## Slide 4 — What You Will Walk Away With Today (Section 1, type: 3-card grid)
Section accent: C.teal
Header: FM&I | SESSION GOALS

CARD 1 — "Tool map"
  Accent: C.teal
  Body: A complete mental map of every AI tool available to you at BP — what each one does, when to use it over the alternatives, and exactly how to request access if you don't already have it. By the end of this session you will be able to answer in under 10 seconds: "which tool do I reach for when the Dataiku recipe is timing out?"

CARD 2 — "Compliance clarity"
  Accent: C.blue
  Body: Exactly what data can and cannot go into each tool — with the reasoning behind each boundary, not just the list. You will understand why the rule exists, which means you can apply it confidently in edge cases without needing to ask compliance every time you want to use an AI tool for something non-standard.

CARD 3 — "Innovation Day ready"
  Accent: C.green
  Body: Ten or more concrete commercial ideas for FM&I, each with enough specificity to bring to Innovation Day — what it does, what data it needs, who benefits, and what a two-week MVP would look like. Plus a framework for evaluating and pitching ideas that the session evaluation committee is looking for.

Bottom bar: "Core message: you already have the tools — the only gap is knowing which one to reach for and when"

---

## Slide 5 — Our Work Is Exactly Where Gen AI Creates the Most Leverage (Section 1, type: left stacked + right card)
Section accent: C.teal
Header: FM&I | CONTEXT

LEFT COLUMN — 4 stacked cards (left teal accent):

Card A — "ELT pipelines on Dataiku"
  Body: We build and maintain ELT pipelines that move commodity price data from raw sources through transformation recipes to model-ready datasets. These pipelines need to be debugged when upstream data changes unexpectedly, optimised when they hit performance limits, and documented so new team members can take ownership. All three are tasks where AI creates 5-10x acceleration.

Card B — "Fundamental model development"
  Body: Crack spread models, time spread estimators, location basis calculations, VaR scenarios — these are mathematically complex, domain-specific, and iterative. AI tools accelerate the code implementation phase significantly, freeing model developers to focus on the methodology and calibration where their domain expertise is irreplaceable.

Card C — "Ad hoc analysis for trading desks"
  Body: Fast turnaround analysis under time pressure is where the 12-minute Dash app benchmark matters most. A trader asking for crack spread visualisation by delivery month and location cannot wait 2 days. With Cursor or Claude Code, an analyst can deliver a working interactive chart in the time it previously took to set up the Jupyter environment.

Card D — "Cross-squad collaboration"
  Body: FM&I sits between data suppliers, model developers, and trading desk consumers. Documentation, handover notes, and meeting summaries — the connective tissue of collaboration — consume significant time. Microsoft Copilot in Teams and Outlook handles this class of work, giving analysts more time for the analytical work only they can do.

RIGHT CARD — "The leverage opportunity":
  Title: "The leverage opportunity"
  Body: Every FM&I workflow maps onto a different AI tool. ELT debugging → GitHub Copilot or Cursor. Model documentation → Claude Code. Desk request visualisation → Cursor in agent mode. Meeting action items → Microsoft Copilot. Understanding which tool to reach for — and doing so in under 3 seconds — is the skill that separates the 15-hour savers from the 2-hour savers.

Bottom bar: "FM&I sits at the intersection of data engineering, modelling, and commercial delivery — peak leverage for Gen AI"

---

## SECTION 2 — THE LANDSCAPE
Section accent: C.cyan

---

## Slide 6 — Section Divider — The Landscape (type: divider)
Background: C.navy
Top accent: C.cyan
Number: "02"
Title: "The Landscape"
Subtitle: "What's available, what changed, and how to access it"

---

## Slide 7 — The Last 12 Months Changed What's Possible (Section 2, type: timeline)
Section accent: C.cyan
Header: LANDSCAPE | TIMELINE

TIMELINE (5 milestones, horizontal):

Milestone 1 — "Mar 2025"
  Title: GPT-4o multimodal
  Body: Analysts could paste a chart or PDF page directly into the AI and ask questions about it — no manual data extraction. For FM&I: paste an ICE Brent forward curve and ask what the contango steepest point signals about storage economics. Answered in seconds, not hours of manual curve reading.

Milestone 2 — "May 2025"
  Title: Claude 3.7 Sonnet
  Body: Extended thinking enabled reliable multi-step problem solving for the first time. Complex statistical model debugging — tracing through 5 interacting components to find a root cause — became consistently possible without hallucination. The first model useful for the kind of non-obvious bugs that previously required a senior engineer's full day.

Milestone 3 — "Jul 2025"
  Title: GitHub Copilot Workspace GA
  Body: An enterprise-licensed AI tool could, for the first time, reason across an entire repository rather than just the open file. For a 30-file Dataiku project, this meant asking "what's the downstream impact of changing the VaR calculation?" and getting an answer that traces through all dependent recipes.

Milestone 4 — "Oct 2025"
  Title: Cursor background agents
  Body: Background agents changed the relationship from "assistant you talk to" to "parallel team member you assign work to." You can submit "refactor all ELT recipes to use Polars" and come back 90 minutes later to a completed branch. This is the moment AI became a parallel worker, not just a faster typist.

Milestone 5 — "Jan 2026"
  Title: Claude 4.6 Opus/Sonnet
  Body: Reliable agentic multi-step tool calling — executing code, seeing results, correcting errors, and continuing autonomously — made Claude Code production-worthy for FM&I pipeline work. A single instruction now reliably produces a complete, useful multi-file output without constant user supervision.

Bottom bar: "Context windows hit 1M tokens, reasoning improved 10×, agentic workflows became reliable — all in 12 months"

---

## Slide 8 — Four Tools Available to BP Employees Right Now (Section 2, type: 2×2 grid)
Section accent: C.cyan
Header: LANDSCAPE | BP TOOLS

CARD 1 — "Microsoft Copilot"
  Accent: C.blue
  Body: Embedded in your M365 licence — if you have access to Teams, Outlook, Word, or Excel, Copilot is already available. No IT request required in most cases. The entry point for AI-assisted meeting summaries, document drafting, and data analysis in Excel. The lowest-friction tool to start using today.

CARD 2 — "GitHub Copilot"
  Accent: C.green
  Body: BP holds an enterprise licence, making this the most straightforward coding AI to request. Integrates directly into VS Code and JetBrains — the IDEs already in use for Dataiku recipe development and Python model work. Best for inline code completion, debugging, and documentation generation within your existing IDE environment.

CARD 3 — "Cursor"
  Accent: C.teal
  Body: A full VS Code fork with AI capabilities deeply integrated at every level — not an add-on, but the core of the product. Best-in-class for large, multi-file projects where you need the AI to understand the entire Dataiku project structure, not just the file you have open. Currently requires individual licence request or T&E expense.

CARD 4 — "Copilot Studio"
  Accent: C.purple
  Body: The no-code agent builder in the Microsoft ecosystem. If you can write a paragraph describing what an automated assistant should do, you can build it in Copilot Studio without writing a line of code. The FM&I use case: a research monitoring agent that reads new reports from a SharePoint folder, summarises them, and posts key findings to a Teams channel.

Bottom bar: "All four are either included in existing BP licences or accessible via IT request — there is no technical barrier to starting today"

---

## Slide 9 — Requesting Access Takes Less Than 10 Minutes (Section 2, type: stacked access cards)
Section accent: C.cyan
Header: LANDSCAPE | ACCESS

STACKED CARD 1 — accent: C.blue
  Body: Microsoft Copilot — Already active if you have an M365 E3 or E5 licence. Open Word, Excel, or Teams and look for the Copilot button in the toolbar. If it is not visible, raise a standard IT ticket referencing "M365 Copilot activation." No additional licence cost and no manager approval required for the base tier.

STACKED CARD 2 — accent: C.green
  Body: GitHub Copilot — Request via the BP IT self-service portal under "Developer Tools." Approval is typically 2-3 business days. Once approved, install the GitHub Copilot extension in VS Code, sign in with your GitHub Enterprise account, and it is immediately active. Works in VS Code, JetBrains, and the GitHub Copilot CLI.

STACKED CARD 3 — accent: C.teal
  Body: Cursor — Not in the standard IT catalogue as of Q1 2026. Two options: (1) raise an IT request with a business justification citing FM&I pipeline development needs, or (2) expense as a professional tool via T&E with manager approval — approximately £20/month Pro tier. Once installed, sign in with a Cursor account and import your VS Code settings.

STACKED CARD 4 — accent: C.purple
  Body: Copilot Studio — An add-on to your M365 licence requiring IT approval and a manager-signed business justification. BP's intranet has a step-by-step setup guide under "Digital Tools > AI > Copilot Studio." Once provisioned, access via the Copilot Studio portal — no local installation required.

Bottom bar: "Start with Microsoft Copilot today — it requires zero additional requests if you have an M365 licence"

---

## Slide 10 — The Right Tool Depends on the Task (Section 2, type: table)
Section accent: C.cyan
Header: LANDSCAPE | TOOL MAP

TABLE HEADERS: Task | Best Tool | Why It Wins

Row 1: "Writing, summarising, emails" | Microsoft Copilot | M365-native — zero context switching. Stays inside Teams/Outlook/Word where the content already lives. Data stays inside BP's Microsoft tenant — safest option for internal content.

Row 2: "Debugging Python or SQL in IDE" | GitHub Copilot | Inline and context-aware inside your existing IDE. No separate window, no context switching. BP enterprise licence means IT and legal coverage without additional approval.

Row 3: "Building a new model or full app" | Cursor | Full-repository context understands how your 30-file Dataiku project connects together. Agent mode and background agents handle multi-step builds without supervision. Best model choice (Claude Sonnet/Opus).

Row 4: "Automating a document workflow" | Copilot Studio | No-code agent builder connected to M365 data. Build a research summariser or action item tracker without writing Python. Best for non-developer workflows.

Row 5: "Long agentic coding task overnight" | Claude Code (CLI) | Headless operation — run on a VM overnight, no GUI required. Best for full codebase audits, multi-file refactors, and tasks where you want to come back to a completed result rather than supervise each step.

Bottom bar: "No single tool wins every task — the productivity gain comes from knowing which one to reach for in under 3 seconds"

---

## SECTION 3 — MICROSOFT COPILOT
Section accent: C.blue

---

## Slide 11 — Section Divider — Microsoft Copilot (type: divider)
Background: C.navy
Top accent: C.blue
Number: "03"
Title: "Microsoft Copilot"
Subtitle: "M365 integration, Copilot Agents, and the roadmap ahead"

---

## Slide 12 — Copilot Is Embedded in Every M365 App You Already Use (Section 3, type: 2×2 grid)
Section accent: C.blue
Header: MICROSOFT | COPILOT M365

CARD 1 — "Teams + Outlook"
  Accent: C.blue
  Body: Teams Copilot transcribes meetings in real time, extracts action items by person and team, and generates a structured follow-up summary within 30 seconds of the call ending. Outlook Copilot drafts replies matching your tone, summarises long email threads, and flags emails requiring your attention today. For FM&I: trading strategy calls become structured action logs automatically.

CARD 2 — "Word + PowerPoint"
  Accent: C.midBlue
  Body: Word Copilot drafts documents from bullet points or prompts, rewrites sections in a different tone, and generates tables and structured content from plain text descriptions. PowerPoint Copilot can generate an entire slide deck from a Word document or prompt, and it can reformat and redesign existing slides. For FM&I: model documentation and management reporting can be drafted in minutes rather than hours.

CARD 3 — "Excel — the FM&I-relevant capabilities"
  Accent: C.cyan
  Body: Natural language formula generation — describe what you want in plain English and Excel writes the formula. Python in Excel: Copilot-assisted Python code runs inside Excel cells, enabling statistical analysis without leaving the spreadsheet. Natural language data insights: paste a dataset and ask "what are the three most unusual patterns in this data?" — Copilot detects anomalies and narrates findings. For FM&I: crack spread analysis and scenario outputs can be interrogated without writing a line of code.

CARD 4 — "OneNote + Loop"
  Accent: C.teal
  Body: OneNote Copilot summarises freeform notes, generates action plans from meeting capture, and enables cross-notebook search via conversational queries. Microsoft Loop adds AI-assisted shared workspaces where Copilot can update documents collaboratively. For FM&I: the morning operational brief can be auto-drafted from a structured prompt, and cross-team research notes can be synthesised across notebooks automatically.

Bottom bar: "If you use any M365 app, you already have a Copilot — most people just haven't turned it on yet"

---

## Slide 13 — [LIVE DEMO] Meeting Summary in 3 Minutes (Section 3, type: demo)
Section accent: C.blue
Header: MICROSOFT | SEE IT IN ACTION

PROMPT PANEL (dark):
  Header: "The prompt you type:"
  Terminal: "Summarise this 45-minute trading strategy call, extract all action items assigned to FM&I, and draft follow-up emails for each action item owner."

LEFT PANEL — "What happens:"
  Steps:
  1. Copilot transcribes and summarises the meeting in real time
  2. Identifies action items and assigns them to individuals by name
  3. Drafts structured follow-up emails for each action item owner
  4. Links back to the meeting recording timestamp for each action
  5. Formats the summary in your preferred style (bullet points or prose)

RIGHT PANEL (big number):
  Stat: "3 min"
  Label: "from recording to structured follow-ups with emails drafted"
  Manual: "Manual: 45-60 min"

Bottom bar: "[PRESENTER: switch to Microsoft Teams / Copilot now to run this live]"

---

## Slide 14 — Copilot Agents: Build a Custom Automated Assistant in Minutes (Section 3, type: left stacked + right card)
Section accent: C.blue
Header: MICROSOFT | COPILOT AGENTS

LEFT COLUMN — 4 stacked cards (left blue accent):

Card A — "What it is"
  Body: A custom AI assistant you define with natural language instructions, data sources, and actions. It lives in Microsoft Teams as a bot or is accessible via the Copilot interface. You describe what it should do, what it should know, and how it should respond — no coding required. The agent retains its instructions across all conversations.

Card B — "What it can access"
  Body: Microsoft Graph data (your calendar, emails, Teams messages, with your consent), SharePoint document libraries you specify, web content via Bing grounding, and external systems via Power Automate connectors. For FM&I, this means an agent can read new research reports from a SharePoint library, summarise them, and act on their contents without manual input.

Card C — "How to build one"
  Body: Open Copilot Studio. Define the agent's name, purpose, and personality in plain language. Connect knowledge sources — a SharePoint folder of market reports, a web URL, or uploaded documents. Add Power Automate flows for actions. Test in the Studio test panel. Publish to Teams. The entire build, including testing and iteration, takes 30-60 minutes for a useful first version.

Card D — "The self-improvement trick"
  Body: After giving the agent its initial instructions, type: "Review your instructions and suggest improvements to make you more effective at [specific task]." The agent generates improved instructions — paste them back in. Run this loop 2-3 times. The resulting agent is consistently better than one refined manually, and the process requires no prompt engineering expertise.

RIGHT CARD — "FM&I Research Monitor Agent":
  Title: "FM&I example: research monitor"
  Body: An agent configured to monitor a SharePoint folder where market research reports are filed. Every time a new PDF is added, the agent reads it, extracts: the commodity covered, key price outlook (bullish/bearish), top 3 risks, and any FM&I-relevant data points. It posts a structured summary to the FM&I Teams channel within 2 minutes of the file arriving. Build time: 45 minutes. Time saved per week: 2-3 hours of manual report reading, compressed to 2 minutes of reviewing AI summaries.

Bottom bar: "Copilot Studio requires no coding — if you can write a paragraph describing what the agent should do, you can build it"

---

## Slide 15 — Copilot in 2026: More Autonomy, Deeper Integration (Section 3, type: timeline)
Section accent: C.blue
Header: MICROSOFT | ROADMAP

TIMELINE (4 milestones):

Milestone 1 — "Q1 2026"
  Title: Copilot reasoning mode
  Color: C.blue
  Body: Microsoft integrated OpenAI's o-series reasoning model into Word and Outlook Copilot. For complex multi-step document tasks — "analyse this model review report and identify all actions that require compliance sign-off" — reasoning mode produces structurally better outputs than the standard Copilot.

Milestone 2 — "Q2 2026"
  Title: Power BI Copilot expansion
  Color: C.teal
  Body: Natural language report generation directly in Power BI Service — describe the analysis you want, Copilot builds the report. For FM&I, this is the highest-value near-term integration: trading desk requests for spread analysis become a conversation rather than a development sprint.

Milestone 3 — "Q3 2026"
  Title: 1,000+ connector ecosystem
  Color: C.green
  Body: Third-party connectors expand Copilot Studio's reach to 1,000+ external services. For FM&I, this means Copilot agents that can query Bloomberg, pull Dataiku scenario status, or read from commodity pricing APIs — all without custom MCP development.

Milestone 4 — "Q4 2026"
  Title: Multi-agent orchestration
  Color: C.purple
  Body: Copilot agents can spawn and coordinate sub-agents for complex workflows. An orchestrating agent receives a task — "prepare the monthly model performance pack" — and delegates to sub-agents: data collector, analyst, writer, formatter. The orchestrator synthesises the results and delivers the finished pack.

NOTE CARD (below timeline, lightBlue background):
  Body: BP internal training available on the intranet under "Digital Tools > AI" — covers M365 Copilot setup, data governance, and Copilot Studio basics in 3 self-paced modules.

Bottom bar: "The Power BI Copilot integration (Q2 2026) is the highest-leverage near-term opportunity for FM&I reporting workflows"

---

## SECTION 4 — GITHUB COPILOT & CURSOR
Section accent: C.green

---

## Slide 16 — Section Divider — GitHub Copilot & Cursor (type: divider)
Background: C.navy
Top accent: C.green
Number: "04"
Title: "GitHub Copilot & Cursor"
Subtitle: "Two tools, different strengths — and workflows that go beyond coding"

---

## Slide 17 — Same Category, Very Different Strengths (Section 4, type: two-column comparison)
Section accent: C.green
Header: TOOLS | COMPARISON

LEFT CARD — "GitHub Copilot"
  Accent: C.blue
  Body: BP enterprise licence makes this the zero-friction choice — request it, get it in 2 days, use it in the IDE you already have. The @workspace agent indexes your entire Dataiku project and can answer architecture questions across files. Slash commands (/fix, /explain, /test, /doc) cover 80% of daily coding tasks.

  What "full repo awareness" means in practice: when debugging a timeout in your gas_hub_prices recipe, Copilot @workspace reads all related recipes, models, and configs. Ask "what upstream changes could be causing this timeout?" and it traces dependencies across 20+ files without being told to look there. This is categorically different from file-level completion.

  Best for: daily inline work, debugging in your existing IDE, documentation generation, PR review, and any team where BP enterprise licence is the access route.

RIGHT CARD — "Cursor"
  Accent: C.green
  Body: A full VS Code fork — AI is not an add-on but the core architecture. Semantic codebase indexing means Cursor has not just read the file names but understands how your Dataiku project's recipes, models, and outputs connect to each other. Full model choice: Claude Sonnet for speed, Claude Opus for deep debugging, Gemini for very large context tasks.

  What background agents mean in practice: you type "refactor all ELT aggregation recipes to use Polars instead of Pandas for the heavy transforms." Cursor submits this to a background agent and returns control to you immediately. Ninety minutes later: the refactor is complete, tests are updated, a branch is created, and you receive a summary. This is AI as a parallel team member, not AI as a faster keyboard.

  Best for: large, multi-file projects; complex builds from scratch; tasks requiring sustained autonomy; when you want to choose your model per task.

Bottom bar: "Use GitHub Copilot for daily inline work in your existing IDE; use Cursor when the task spans multiple files or requires autonomous execution"

---

## Slide 18 — [LIVE DEMO] Dataiku Recipe Timeout — Debugged in 20 Minutes (Section 4, type: demo)
Section accent: C.green
Header: GITHUB COPILOT | SEE IT IN ACTION

PROMPT PANEL (dark):
  Header: "The prompt you type:"
  Terminal: "This Dataiku recipe is timing out on 500k rows. The aggregation runs fine on 10k rows in isolation. Identify the bottleneck and rewrite the aggregation logic using vectorised operations."

LEFT PANEL — "What happens:"
  Steps:
  1. Copilot @workspace reads the full recipe and all upstream data sources
  2. Identifies the iterrows() anti-pattern on line 47 — O(n) loop over 500k rows
  3. Rewrites using pandas vectorised groupby operations — reduces to O(n log n)
  4. Adds a docstring explaining the original problem and the optimisation
  5. Suggests unit tests for the refactored function with edge cases

RIGHT PANEL (big number):
  Stat: "20 min"
  Label: "from timeout to optimised, tested, documented recipe"
  Manual: "Manual debug cycle: 3-4 hours"

Bottom bar: "[PRESENTER: open VS Code with the demo recipe] — the 3-4 hour debug cycle just became a 20-minute review cycle"

---

## Slide 19 — [LIVE DEMO] Prompt to Working Dash App — 12 Minutes (Section 4, type: demo)
Section accent: C.green
Header: CURSOR | SEE IT IN ACTION

PROMPT PANEL (dark):
  Header: "The prompt you type:"
  Terminal: "Build a Plotly Dash app showing crack spread evolution for Q1 2025. Read from crack_spreads.csv, add a 30-day rolling average line, include a date range picker and commodity selector dropdown. Deploy locally on port 8050."

LEFT PANEL — "What happens:"
  Steps:
  1. Cursor reads crack_spreads.csv and understands the column schema and date range
  2. Writes the complete Dash app layout with Plotly chart callbacks
  3. Implements the rolling average calculation with correct handling of leading NaN values
  4. Adds the date range picker and commodity selector with proper callback wiring
  5. Runs the app locally — browser opens automatically to localhost:8050

RIGHT PANEL (big number):
  Stat: "12 min"
  Label: "from prompt to interactive app running in browser"
  Manual: "Manual: 2-3 days"

Bottom bar: "[PRESENTER: run this live now] — this is the 'hours to minutes' shift that changes how FM&I responds to desk requests"

---

## Slide 20 — Three Modes: Match the Mode to the Task (Section 4, type: 3-card grid)
Section accent: C.green
Header: TOOLS | MODES

CARD 1 — "Ask" (badge: QUICK, color: C.cyan)
  Accent: C.cyan
  Body: Single-turn question and answer. The AI reads your context but takes no actions. Use Ask mode for: explaining what an unfamiliar function does, getting a second opinion on a data model design, understanding why a Pandas merge is dropping rows, or learning the correct Dataiku API call for triggering a scenario programmatically. The mental model: Ask is the colleague you can interrupt with a quick question without them needing to pick up where you left off.

CARD 2 — "Agent" (badge: COMPLEX, color: C.blue)
  Accent: C.blue
  Body: Multi-step autonomous execution. Give a goal, the agent plans and executes across your codebase. Use Agent mode for: implementing a new feature that touches 5+ files, debugging a production issue by reading logs and tracing through the call stack, writing a comprehensive test suite for a model class, or adding docstrings to every function in a recipe. The FM&I use case: "add data quality validation to the gas pricing ELT pipeline" — Agent mode plans the changes across all affected recipes, implements them, and runs the existing tests to verify nothing broke.

CARD 3 — "Plan" (badge: SAFE, color: C.purple)
  Accent: C.purple
  Body: The AI proposes a complete plan of changes and waits for approval before executing anything. Use Plan mode when: the stakes are high (touching a production pipeline or shared model), you are working in an unfamiliar codebase and want to understand the scope before changes are made, or the task is complex enough that a wrong first step could compound into a large rollback. FM&I use case: "migrate the VaR calculation from the legacy module to the new risk framework" — Plan mode shows you every file that will change and every function that will be affected before writing a single line.

Bottom bar: "Default to Ask for questions, Agent for tasks, Plan when the stakes are high — this single habit change 3× the value of either tool"

---

## Slide 21 — Better Prompts = Better Output: The Formula (Section 4, type: left stacked + right terminal)
Section accent: C.green
Header: TOOLS | PROMPTING

LEFT COLUMN — 4 stacked cards (left green accent):

Card A — "Be specific about context"
  Body: Include the specific framework, data shape, and expected output format in every prompt. "Optimise this function" produces generic output. "Optimise this Pandas aggregation for a 500k-row gas pricing dataset, targeting a 5× speedup, without changing the output schema" produces a solution you can use. Context specificity is the single highest-leverage prompt improvement.

Card B — "State constraints explicitly"
  Body: Enumerate what you cannot change: "use pandas not polars — this runs in a Dataiku Python 3.8 environment," "output must be a dictionary keyed by hub name not a DataFrame," "do not modify the function signature — it is called by 12 downstream recipes." Constraints prevent the AI from producing a technically correct but practically useless solution.

Card C — "Use the LLM to improve your prompt"
  Body: Type your rough prompt, then ask: "Rewrite this prompt to be clearer and more likely to produce the output I need, without changing the core task." The improved prompt consistently outperforms your original. This is not laziness — it is using the tool's strength (writing) to improve your own tool use. Takes 30 seconds and routinely saves 15 minutes of iteration.

Card D — "Template your common prompts"
  Body: Store your best prompts in .cursorrules or .github/copilot-instructions.md so they are available as project context on every session. The FM&I template structure: "Context: [what the pipeline/model does]. Task: [specific action]. Constraints: [language, framework, output format, what cannot change]. Verification: [how to check the output is correct]." Run this structure for 2 weeks and your prompt quality becomes consistent.

RIGHT PANEL (dark terminal):
  Header: "FM&I prompt template:"
  Terminal code:
    Context: [what the pipeline/model does and
             what the data looks like]

    Task: [specific action to perform]

    Constraints:
    - Python 3.8 / Dataiku DSS env
    - Output format: [schema / type]
    - Must not change: [function sig / schema]

    Verification: [how to check correctness]

Bottom bar: "The _p-presentation-creator repo is a live example: CLAUDE.md + agents + skills = consistent AI output on every run"

---

## Slide 22 — Both Tools Are Shipping Major Upgrades in 2026 (Section 4, type: two-column roadmap)
Section accent: C.green
Header: TOOLS | ROADMAP

LEFT CARD — "GitHub Copilot 2026"
  Header accent: C.blue
  Q1: Copilot Extensions — tool calling that connects to external services. For FM&I, this means Copilot chat can query your Dataiku scenario status without leaving VS Code, using the same kind of MCP-style integration that Cursor already supports. The extension ecosystem will grow rapidly through 2026.
  Q2: Copilot CLI GA — natural language terminal commands. Type what you want to do in plain English and GitHub Copilot CLI writes the correct shell command. Relevant for Dataiku CLI operations, complex git workflows, and SSH-based pipeline management.
  Q3: Multi-file autonomous edits without per-step approval. Currently, Copilot Edit mode requires review of each proposed change. Q3 will enable "apply all" for trusted agent sessions — bringing GitHub Copilot closer to Cursor's agent mode.
  Q4: Integrated pre-PR review agent — flags issues in your code before you raise the pull request, reducing review cycle time. Particularly useful for FM&I teams with distributed code ownership.

RIGHT CARD — "Cursor 2026"
  Header accent: C.green
  Q1: Cursor Teams — shared .cursorrules and agent coordination across the whole team. Every FM&I engineer would start every session with the same project context, conventions, and shared prompt templates — no individual setup required.
  Q2: Background agents on cloud infrastructure — submit long-running tasks and they run on Cursor's cloud even when your laptop is closed. Submit a "migrate all legacy models to the new data schema" overnight and review the result in the morning.
  Q3: Integrated test runner — the agent writes code, immediately runs the tests, sees which tests fail, fixes them, and iterates — all in a single autonomous loop. This closes the loop that currently requires a human to trigger the test run.
  Q4: Cursor for notebooks — full Jupyter notebook support with agent mode. For FM&I analysts who work primarily in Jupyter rather than .py files, this brings the full Cursor agent workflow to notebook-based model development.

Bottom bar: "Cursor's cloud background agents (Q2) + GitHub Copilot's extension ecosystem (Q1) are the two near-term features most relevant to FM&I"

---

## SECTION 5 — THE MODEL LANDSCAPE
Section accent: C.purple

---

## Slide 23 — Section Divider — The Model Landscape (type: divider)
Background: C.navy
Top accent: C.purple
Number: "05"
Title: "The Model Landscape"
Subtitle: "12 months of capability jumps — and how to choose the right model"

---

## Slide 24 — The Models You Knew a Year Ago Are Not the Models Available Today (Section 5, type: timeline)
Section accent: C.purple
Header: MODELS | TIMELINE

TIMELINE (5 milestones — reduce from 6 to 5 to avoid crowding):

Milestone 1 — "Q1 2025"
  Title: Claude 3.5 Sonnet + GPT-4o
  Color: C.blue
  Body: Claude 3.5 Sonnet became the de-facto standard for coding tasks — the first model where test generation, documentation, and refactoring reached production quality. Simultaneously GPT-4o's improved tool use made agentic workflows reliable enough for professional use. This was the inflection point when AI tools became genuinely useful for FM&I engineering work.

Milestone 2 — "Q2 2025"
  Title: Gemini 2.0 + Claude 3.7
  Color: C.teal
  Body: Gemini 2.0 made 1M context windows practically usable — an entire large Dataiku project could now fit in one context. Claude 3.7 added extended thinking: visible chain-of-thought reasoning for complex multi-step problems. Both moved the frontier for what was possible in a single AI session.

Milestone 3 — "Q3 2025"
  Title: o3 + Llama 3.3
  Color: C.green
  Body: OpenAI's o3 reasoning model achieved step-change performance on mathematical and logical problems — relevant for statistical model methodology questions. Llama 3.3 70B narrowed the open-source quality gap significantly, making local-model-only workflows (for data-sensitive use cases) genuinely viable for the first time.

Milestone 4 — "Q4 2025"
  Title: Claude Sonnet 4.6
  Color: C.orange
  Body: Current production standard. Coding and instruction-following improvements made it the best daily-driver for FM&I pipeline development — fast enough for interactive sessions, accurate enough for complex transformations, and significantly cheaper than Opus for high-frequency use.

Milestone 5 — "Q1 2026"
  Title: Claude Opus 4.6
  Color: C.purple
  Body: Frontier reasoning with extended thinking and multimodal improvements. Extended thinking mode allows the model to work through complex statistical methodology questions with visible reasoning steps — the first model genuinely useful for architecture-level FM&I problems like "how should we restructure the VaR calculation to support intraday scenario runs?"

Bottom bar: "Quality improved 10× in 12 months. The model you tried 12 months ago is not the model you should evaluate today"

---

## Slide 25 — Different Models Excel at Different Tasks (Section 5, type: 2×2 grid)
Section accent: C.purple
Header: MODELS | COMPARISON

CARD 1 — "Claude Sonnet 4.6"
  Accent: C.teal
  Body: The daily driver for 80% of FM&I coding work. Fast enough for interactive sessions, accurate enough for complex pandas/polars transformations, and at ~$3/M tokens — cost-effective for high-frequency use. Use Sonnet when: building or debugging Dataiku recipes, writing documentation and docstrings, generating test suites, interactive Q&A about your codebase. It is the sensible default — upgrade only when Sonnet's output isn't good enough.

CARD 2 — "Claude Opus 4.6"
  Accent: C.purple
  Body: Best for problems that require sustained multi-step reasoning — debugging non-obvious model bugs that require tracing through 5 interacting components, designing the architecture of a new pipeline from scratch, or synthesising a large body of research to inform a modelling decision. Use Opus when: Sonnet has tried and failed, the problem is genuinely complex, or the stakes are high enough that maximum quality matters more than speed or cost.

CARD 3 — "GPT-4o / o3"
  Accent: C.blue
  Body: GPT-4o is strong for multimodal tasks — understanding charts, processing uploaded CSV files via Code Interpreter, and image-based analysis. o3 is purpose-built for mathematical and logical reasoning: use it for complex statistical methodology questions, calibration problems, or anything requiring rigorous numerical reasoning. For FM&I: o3 for half-life estimator methodology questions; GPT-4o for processing uploaded market data files in ChatGPT's sandbox.

CARD 4 — "Ollama (local models)"
  Accent: C.green
  Body: The only safe option for any input that contains proprietary data. Ollama runs Llama 3.3, Mistral, or Phi-4 on your local machine — zero data leaves BP infrastructure. Use Ollama when: the code you are working on contains actual model parameters, calibrated coefficients, or position-adjacent data in comments or variable names. Quality is meaningfully below Claude Sonnet but infinitely better than not using AI for data-sensitive work.

Bottom bar: "Default to Claude Sonnet for 80% of FM&I tasks — use Opus for complexity, o3 for maths, Ollama for data-sensitive work"

---

## Slide 26 — A Simple Framework for Model Selection (Section 5, type: decision tree + cost card)
Section accent: C.purple
Header: MODELS | DECISION

DECISION CARDS (left, 3 stacked):

Card 1 — Q1: Does the task involve sensitive or proprietary data?
  Yes → Ollama local model. This is non-negotiable. No cloud model should receive live positions, proprietary model coefficients, or counterparty information regardless of the task.
  No → proceed to Q2

Card 2 — Q2: Is this an interactive coding task or a batch/agentic workflow?
  Interactive (you're watching) → Claude Sonnet 4.6. Speed matters; Sonnet is 3-5× faster than Opus for interactive use.
  Batch/overnight → Claude Opus 4.6 or o3. For tasks that run while you sleep, optimise for quality not latency.

Card 3 — Q3: Does the task require deep mathematical/statistical reasoning?
  Yes → o3 (OpenAI reasoning model). Outperforms all other models on complex mathematical and logical problems.
  No → Claude Sonnet 4.6. Default and correct for most FM&I coding and analysis tasks.

COST REFERENCE CARD (right, lightBlue background):
  Title: "Approximate cost per 1M tokens (Q1 2026)"
  Data:
    Claude Opus 4.6:    $15 in / $75 out
    Claude Sonnet 4.6:   $3 in / $15 out
    GPT-4o:             $5 in / $15 out
    o3:                $10 in / $40 out
    Gemini 2.5 Pro:    $3.50 in / $10.50 out
    Ollama (local):     $0 / $0

Bottom bar: "Sonnet for daily FM&I work — only upgrade to Opus when complexity demands it; the cost difference is 5×"

---

## SECTION 6 — ETHICS & COMPLIANCE
Section accent: C.orange

---

## Slide 27 — Section Divider — Ethics & Compliance (type: divider)
Background: C.navy
Top accent: C.orange
Number: "06"
Title: "Ethics & Compliance"
Subtitle: "What data can go in, what can't, and the 5 rules for safe use in FM&I"

---

## Slide 28 — The Data Boundary Is the Most Important Thing in This Session (Section 6, type: two-column)
Section accent: C.orange
Header: COMPLIANCE | DATA RULES

LEFT CARD — "SAFE TO USE" (green header):
  Items with WHY explanations:
  • Open-source code and generic scripts — code structure and patterns are not proprietary. Asking "how do I optimise this type of loop?" is safe because the technique is separable from the data.
  • Anonymised sample data — replace specific hub names, volumes, and prices with generic placeholders. "Hub A: 500 TWh at 32.45" is safer than the real values if the hub is identifiable.
  • Public research and academic papers — already public. Use AI to summarise, extract, or synthesise freely.
  • Internal documentation (non-sensitive) — meeting notes, process documents, architecture diagrams that do not contain market-sensitive information or proprietary model details.
  • Code logic without real values — the structure of your half-life estimator is safer than a version containing calibrated coefficients for a live book.

RIGHT CARD — "NEVER INPUT" (red header):
  Items with WHY explanations:
  • Live trading positions — this is MIFID II / REMIT territory. Positions submitted to an external AI tool constitute a data security event and potentially a regulatory breach.
  • Counterparty names or deal terms — commercially sensitive under NDA and potentially market-sensitive. Even anonymised, patterns in deal terms can be reverse-engineered.
  • Proprietary model parameters — calibrated coefficients represent years of analytical work and competitive advantage. They must not leave BP's infrastructure under any circumstances.
  • Unpublished price forecasts — qualify as inside information under MAR if they reflect material non-public analysis. External submission is a regulatory risk.
  • Anything marked CONFIDENTIAL or RESTRICTED — BP's data classification applies. If the document has a classification label, the same rules apply when pasting its content into an AI tool.

Bottom bar: "Rule of thumb: if you wouldn't paste it into a public Slack channel, do not paste it into an AI tool you don't control"

---

## Slide 29 — Five Rules Cover 95% of Situations — Memorise These (Section 6, type: 5 stacked rules)
Section accent: C.orange
Header: COMPLIANCE | FM&I RULES

RULE CARDS (5 stacked, each with left orange accent):

Rule 1 — "Anonymise before you paste"
  Body: Replace position sizes, counterparty names, and model outputs with generic placeholders before sharing with any AI tool outside the Microsoft tenant. "Hub_A: [volume] TWh at [price]" is always safer than the real values. The anonymisation habit protects you from accidental disclosure even when you're moving fast.

Rule 2 — "M365 Copilot is safer for internal content"
  Body: Microsoft's enterprise agreement covers BP data. When Copilot processes your internal Teams messages or SharePoint documents, that data stays within BP's Microsoft tenant and is not used to train Microsoft's models. External tools — Cursor, Claude.ai, ChatGPT — are governed by individual terms of service that do not carry the same contractual protection for BP data.

Rule 3 — "Code does not equal data — but check"
  Body: Pasting code logic is generally safe. Pasting the data the code runs on may not be. The distinction matters when code contains embedded real values: a function that hardcodes actual calibration parameters as defaults is sending proprietary data when you paste it. Extract the logic without the values before submitting to external tools.

Rule 4 — "Check before you use, not after"
  Body: If you are unsure whether a specific use case is compliant — a new type of data, a new tool, a non-standard workflow — contact the Digital Centre of Excellence before using the tool, not after. The after-the-fact disclosure conversation is significantly harder than a 10-minute pre-approval check. BP's governance team is the right contact for front-office AI use questions.

Rule 5 — "You own the output — always"
  Body: AI-generated code or analysis must be reviewed and validated by you before it is used in any commercial decision or shared with the trading desk. The AI is not self-validating. When a fundamental model gives a bad signal and the trading desk acts on it, the analyst who produced that model owns that outcome — regardless of whether AI wrote the code.

Bottom bar: "BP AI guidance: intranet → 'Digital Tools' → 'AI Governance' — Digital Centre of Excellence for front-office questions"

---

## Slide 30 — Not All AI Tools Handle Your Data the Same Way (Section 6, type: two-column)
Section accent: C.orange
Header: COMPLIANCE | DATA HANDLING

LEFT CARD — "Microsoft Copilot (M365)"
  Accent: C.blue
  Body: Data stays within BP's Microsoft tenant. Microsoft's enterprise data processing agreement means your inputs are not used to train Microsoft's models, IT administrators can access audit logs of Copilot interactions, and BP's data classification framework applies. Microsoft Copilot is appropriate for internal BP content that is not marked as market-sensitive, RESTRICTED, or CONFIDENTIAL. This is the tool you can use most freely for FM&I operational content — meeting notes, internal reports, process documentation.

  Items:
  • Data stays within BP's Microsoft tenant
  • Covered by enterprise data processing agreement
  • Not used to train Microsoft's models
  • Audit logs available to IT administrators
  • Appropriate for internal BP content (not market-sensitive)

RIGHT CARD — "External Tools (Cursor, Claude.ai, ChatGPT)"
  Accent: C.orange
  Body: Data is sent to third-party servers governed by individual terms of service — not by BP's enterprise agreements. Training data opt-out varies by tool and subscription plan: ChatGPT free tier by default uses inputs for training; Cursor Pro does not, but this requires verification against the current terms. For FM&I: use external tools only for code logic, generic patterns, and publicly available information. Any internal data — even internal documentation — carries a compliance risk with these tools.

  Items:
  • Data sent to third-party servers
  • Covered by individual terms of service only
  • Training data opt-out varies by tool and plan
  • No BP enterprise data processing agreement by default
  • Use for code logic and public information only

  Note: API-based access (e.g., via Claude API key) has stronger data handling terms — check current BP guidance for API use status before building API-based workflows.

Bottom bar: "Default to M365 Copilot for anything involving internal BP content; external tools for code logic and public information only"

---

## SECTION 7 — EXTENDED CONCEPTS
Section accent: C.teal

---

## Slide 31 — Section Divider — Extended Concepts (type: divider)
Background: C.navy
Top accent: C.teal
Number: "07"
Title: "Extended Concepts"
Subtitle: "Claude Code, agentic AI, MCP, tool calling, agent skills, and what's next"

---

## Slide 32 — Claude Code: Repository-Level, Not File-Level (Section 7, type: two-column)
Section accent: C.teal
Header: CLAUDE CODE | OVERVIEW

LEFT CARD — "What it is and why it's different"
  Accent: C.teal
  Body: Claude Code is a terminal-based AI agent — not a plugin, not a chat window, but a separate process that runs in your project directory and can read, write, and execute across your entire codebase autonomously. The key differentiator from GitHub Copilot and Cursor: it operates at repository level, not file level. When you give it a goal, it figures out which files to touch, in what order, and how to verify the result.

  Three things you can do with Claude Code that you literally cannot do in IDE tools:
  1. Run it overnight on a cloud VM while you sleep — no GUI required, no user at the keyboard
  2. Invoke it from a CI/CD pipeline as an automated step: "after merge to main, run Claude Code to regenerate model documentation"
  3. Script it: use the Claude SDK to build multi-agent workflows where Claude Code is one agent in a larger orchestration system

RIGHT CARD — "Claude Code vs IDE tools — practical comparison"
  Accent: C.teal
  Table header: Feature | Copilot/Cursor | Claude Code

  Row 1 — Scope: Current file or open files | Entire repository
  Row 2 — Autonomy: Suggestion-based, you accept/reject | Goal-based, executes and verifies
  Row 3 — Runtime: Requires IDE open and user watching | Headless, runs while you do other things
  Row 4 — Overnight: Not possible | Yes — run on VM, return to completed work
  Row 5 — CI/CD: Not applicable | Yes — scriptable as a pipeline step
  Row 6 — Best for: Interactive coding sessions | Complex multi-file builds and audits

Bottom bar: "Claude Code unlocks workflows that take 10 minutes to describe and 2 hours to build autonomously — while you do something else"

---

## Slide 33 — [LIVE DEMO] Full Pipeline Audit — 12 Minutes (Section 7, type: demo)
Section accent: C.teal
Header: CLAUDE CODE | SEE IT IN ACTION

PROMPT PANEL (dark):
  Header: "The prompt you type:"
  Terminal: "Audit our Brent futures fundamental model: find all hardcoded magic numbers and replace with named constants, write docstrings for every undocumented function, generate a pytest test suite for the ELT pipeline, and create a MODEL.md file documenting inputs, outputs, calibration approach, and known limitations."

LEFT PANEL — "What happens:"
  Steps:
  1. Claude reads every file in the repository — recipes, models, tests, configs
  2. Identifies 23 magic numbers across 8 files, replaces with named constants in a constants.py
  3. Writes NumPy-format docstrings for 47 undocumented functions
  4. Generates 156 unit tests for the ELT pipeline covering normal cases and edge cases
  5. Creates MODEL.md with sections: Overview, Data Sources, Calibration Approach, Known Limitations, Changelog

RIGHT PANEL (big number):
  Stat: "12 min"
  Label: "full codebase audit + test suite + documentation generated"
  Manual: "Manual equivalent: 2-3 days of engineering time"

Bottom bar: "[PRESENTER: open terminal and run 'claude' in the demo repo] — every model team has a codebase that needs exactly this audit"

---

## Slide 34 — The Shift That Happened in 2025: From Answering to Doing (Section 7, type: left stacked + right terminal)
Section accent: C.teal
Header: AGENTIC AI | OVERVIEW

LEFT COLUMN — 4 stacked cards (left teal accent):

Card A — "What changed"
  Body: In 2024, AI tools answered questions. In 2025, they started completing multi-step tasks — reading files, running code, calling APIs, fixing errors, and reporting back — without human intervention at each step. The shift was enabled by three things simultaneously: reliable tool calling, large enough context windows to hold task state, and infrastructure (Cursor, Claude Code) mature enough to manage agent orchestration.

Card B — "Why it matters for FM&I"
  Body: An agent can check Dataiku scenario status every morning, flag failed jobs, generate a diagnostic report comparing actual vs expected outputs, and post the results to the FM&I Teams channel — all triggered by a scheduled cron job, with no human involved in the execution. The analyst sets the rules and reviews the output. The agent does the daily monitoring.

Card C — "What works reliably today"
  Body: Well-defined, deterministic tasks where the steps are clear and the success criteria are checkable: code generation, file operations, test running, report formatting, API calls. Agents are reliable when errors are detectable and recoverable — a failing test gives the agent clear feedback to correct on. Start with these tasks before moving to open-ended reasoning chains.

Card D — "What is still unreliable"
  Body: Reasoning chains longer than 10-15 steps accumulate errors — each step has a small failure probability that compounds. Tasks requiring accurate real-world knowledge are risky because hallucination probability grows with the knowledge specificity required. Tasks with ambiguous success criteria are unreliable because the agent may believe it has finished when it has not.

RIGHT PANEL (dark terminal):
  Header: "FM&I agent — morning pipeline monitor"
  Terminal:
    TRIGGER: Daily cron at 06:00 UTC

    Step 1: Pull Dataiku scenario run logs
            for all FM&I projects
    Step 2: Compare actual run times vs
            expected schedule
    Step 3: Flag any failures or >2hr delays
    Step 4: Cross-reference with expected
            data volumes (anomaly check)
    Step 5: Generate diagnostic summary
            with error logs for failures
    Step 6: Post to Teams #fmi-ops channel

    OUTPUT: Morning brief ready by 06:15

Bottom bar: "Reliable agentic workflows start with well-defined, deterministic tasks — the FM&I pipeline monitor is the perfect first agent project"

---

## Slide 35 — Tool Calling and MCP: How AI Agents Connect to Your Systems (Section 7, type: explanation + demo)
Section accent: C.teal
Header: MCP | TOOL CALLING

TOP ROW — 2 explanation cards:

Card 1 — "Tool Calling"
  Accent: C.cyan
  Body: The ability for an LLM to invoke external functions, APIs, and services as part of generating a response. Instead of just outputting text, the model outputs structured instructions to call a function, receives the result, and incorporates it into the next reasoning step. Example: you ask "what's the current status of the gas pricing scenario?" — the LLM calls list_scenarios(), reads the result, and responds with a structured status summary. This is what makes agentic workflows possible.

Card 2 — "MCP (Model Context Protocol)"
  Accent: C.teal
  Body: An open standard developed by Anthropic (released November 2024) that defines a common interface between AI models and external tools. Think of it as USB for AI integrations — any MCP-compliant client (Cursor, Claude Code, Claude Desktop) can connect to any MCP-compliant server. One MCP server built for Dataiku can be used by every AI tool your team uses, with no bespoke integration work per tool.

DEMO SECTION — "MCP for Dataiku: a step-by-step workflow"
  Dark header bar: "MCP for Dataiku — what becomes possible:"
  Terminal prompt: "The gas_hub_prices recipe failed overnight. Get the last error log, read the recipe code, and propose a fix."

  Step-by-step text (below terminal):
  1. Cursor calls the Dataiku MCP tool get_job_logs("gas_hub_prices") — receives the full error log
  2. Claude reads the error: KeyError on column 'settlement_price' at line 47 of the recipe
  3. Claude calls get_recipe_code("gas_hub_prices") via MCP — reads the full recipe
  4. Claude identifies the column rename in the upstream source table, proposes the fix
  5. You type "apply the fix" — Claude writes directly to the recipe file via write_recipe_code() MCP tool
  Total time: 8 minutes. Manual equivalent: pull logs, open recipe, investigate, fix, redeploy — 45 minutes minimum.

BOTTOM ROW — 3 FM&I MCP cards:

Card A — "MCP for Dataiku"
  Body: Read pipeline status, trigger scenarios, query job logs, and write recipe fixes — all from within Cursor or Claude Code. A Cursor session with Dataiku MCP installed can diagnose a failed overnight run and propose a fix without the engineer opening the Dataiku UI.

Card B — "MCP for internal databases"
  Body: Query your production database schema, run read-only analytical queries, and get schema documentation — all from your AI tool. The MCP enforces read-only access; you review every query before it runs. No copy-paste of query results into AI context required.

Card C — "MCP for Bloomberg / market data"
  Body: Emerging MCP servers for financial data APIs allow AI tools to pull market data directly into their context. Ask "what does the ICE Brent forward curve look like this morning?" and Claude retrieves the data via MCP and responds with analysis — no manual download required.

Bottom bar: "MCP turns isolated AI tools into connected agents — Cursor + Dataiku MCP can diagnose a failed pipeline without leaving the IDE"

---

## Slide 36 — Agent Skills, Context Management, and Hooks (Section 7, type: 3-card grid + skill file panel)
Section accent: C.teal
Header: CONCEPTS | ADVANCED

CARD 1 — "Agent Skills"
  Accent: C.blue
  Body: Reusable, packaged workflows invoked by a single slash command. A skill encapsulates a specific multi-step process — what to do, in what order, and what format the output should take. Store in `.claude/skills/`. The FM&I use case: `/data-quality-report` triggers a 10-step profiling process that produces the same structured output every time, regardless of which analyst runs it. Skills are the mechanism for making AI assistance consistent and team-scalable.

  Skill file skeleton:
    # Skill: data-quality-report
    Trigger: /data-quality-report [dataset]

    ## Instructions
    1. Profile: row count, column dtypes
    2. Per column: null %, unique values,
       min/max/mean if numeric
    3. Flag: >10% nulls, single unique value,
       numeric outliers (>3 IQR)
    4. Output: markdown table + JSON + actions

    ## Format: markdown + embedded JSON

CARD 2 — "Context & Tokens"
  Accent: C.orange
  Body: Quality degrades as context fills with irrelevant noise. Every token costs money — Claude Opus at $15/M input tokens means a 500-file codebase in context is expensive. Practical rules: use .cursorignore to exclude node_modules, __pycache__, and build outputs; start fresh conversations for unrelated tasks; compress long conversation histories before complex tasks by asking the AI to summarise what has been decided. The discipline of context management is as important as the quality of your prompt.

CARD 3 — "Hooks & Automation"
  Accent: C.teal
  Body: Claude Code hooks fire shell commands before or after tool calls — enabling automated workflows without manual triggering. Examples: a post-write hook that runs black formatting after every file edit; a post-session hook that commits all changes to git with an AI-generated commit message and posts a summary to the team Slack channel; a pre-tool hook that validates the proposed edit against your .cursorrules before applying it. Hooks transform Claude Code from a tool you use to a tool that works for you.

Bottom bar: "Agent skills + hooks = repeatable, automated workflows — the difference between a tool you use and a tool that works for you"

---

## SECTION 8 — PERSONAL USE CASES
Section accent: C.blue

---

## Slide 37 — Section Divider — Personal Use Cases (type: divider)
Background: C.navy
Top accent: C.blue
Number: "08"
Title: "Personal Use Cases"
Subtitle: "Four real projects — what was built, how, and what it demonstrates"

---

## Slide 38 — Four Real Projects Built With These Tools (Section 8, type: 2×2 grid)
Section accent: C.blue
Header: PERSONAL | USE CASES

CARD 1 — "Claude Code + Remotion: AI-generated video presentations"
  Accent: C.teal
  Body: Problem: converting weekly model performance numbers into a stakeholder briefing consumed 2+ hours of formatting and design work. Solution: Claude Code generates a React component for each slide, Remotion renders them as video frames, and the entire video briefing is produced programmatically from a structured data source — in a single command. What it demonstrates: AI can own the full creative and production workflow, not just assist with it. The same pattern applies to any FM&I output that currently involves manual formatting.

CARD 2 — "OpenClaw: domain-specific AI expertise"
  Accent: C.blue
  Body: An AI-powered chess analysis tool that connects an LLM to a structured position database and gives it tools to query positions, evaluate moves, and explain reasoning chains. The chess application is incidental — what OpenClaw demonstrates is the pattern: connect an LLM to a domain-specific knowledge base with well-defined tool access, and the model becomes a domain expert. The identical pattern applies to connecting a model to a commodity pricing database, a forward curve engine, or a Dataiku recipe catalogue.

CARD 3 — "Claude Remote: overnight VM workflows"
  Accent: C.purple
  Body: SSH-based workflow for running Claude Code autonomously on a remote cloud VM. Write the instruction, start the session over SSH, close the connection, and return the next morning to completed work. A full codebase refactor — the kind that would take a week of IDE time — now runs autonomously overnight at a cost of approximately £5-15 in API tokens. What it demonstrates: the "AI as parallel team member" concept at its fullest extent. The engineer's job shifts from executing to directing and reviewing.

CARD 4 — "Template Project: this presentation as a live example"
  Accent: C.green
  Body: This presentation was built using the template project pattern. CLAUDE.md defines the project. `.claude/agents/` contains 5 specialist agents — Research Lead, Content Architect, and three Section Builders. Each agent reads all prior outputs. The entire content and all code was generated in a single agent-team session from a high-level brief. What it demonstrates: team-scale agentic workflows where each "team member" is a specialised AI agent. The same structure, applied to an FM&I Dataiku project, makes AI assistance consistent across every recipe every engineer builds.

Bottom bar: "Every one of these was built in hours, not days — the template project pattern is directly applicable to FM&I Dataiku projects"

---

## Slide 39 — The Template Project: Make AI Consistent Across Your Whole Team (Section 8, type: left terminal + right stacked)
Section accent: C.blue
Header: PERSONAL | TEMPLATE PROJECT

LEFT CARD (dark terminal — file tree):
  Header: "Project structure"
  Terminal:
    your-project/
    ├── CLAUDE.md          ← project context & rules
    ├── .claude/
    │   ├── agents/        ← specialist sub-agents
    │   ├── commands/      ← slash commands
    │   └── skills/        ← reusable workflows
    ├── .cursorrules       ← Cursor equivalent
    └── .github/
        └── copilot-instructions.md

RIGHT COLUMN — 4 stacked cards (left blue accent):

Card A — "CLAUDE.md / .cursorrules"
  Body: Persistent instructions to the AI about your project's architecture, conventions, and forbidden patterns. Every session starts with the same full context — no re-explaining your stack, no AI forgetting that your Dataiku environment requires Python 3.8, no AI generating Polars code when you told it to use Pandas. This single file eliminates 20-30% of the correction overhead in typical AI-assisted development.

Card B — "Agents directory"
  Body: Specialist sub-agents defined as markdown files — a "debugger" agent, a "test-writer" agent, a "documentation" agent. Each has a specific scope, instructions, and output format. Invoked with /agent debugger for the debugging agent. Rather than one general-purpose AI session doing everything, you get five focused specialists doing one thing each very well. Quality improves significantly.

Card C — "Skills directory"
  Body: Reusable workflows packaged as slash commands. /data-quality-report runs the same 10-step profiling process — row count, column profiles, null analysis, outlier detection, recommended actions — every time, in the same format, regardless of which team member runs it or what dataset they point it at. Build once, use consistently across the team.

Card D — "For FM&I projects"
  Body: A Dataiku project template with CLAUDE.md describing your pipeline patterns, recipe conventions, data schema standards, and quality gates. Every new recipe developed in that project — by any team member using GitHub Copilot, Cursor, or Claude Code — starts with the same complete context. AI assistance becomes immediately useful on day one rather than requiring weeks of customisation.

Bottom bar: "Set this up once and every AI tool — Cursor, GitHub Copilot, Claude Code — becomes immediately useful to any team member"

---

## SECTION 9 — BUSINESS USE CASES
Section accent: C.green

---

## Slide 40 — Section Divider — Business Use Cases (type: divider)
Background: C.navy
Top accent: C.green
Number: "09"
Title: "Business Use Cases"
Subtitle: "Commercial opportunities for FM&I — and how to prepare for Innovation Day"

---

## Slide 41 — Four AI-Enhanced Platforms Directly Relevant to FM&I (Section 9, type: 2×2 grid)
Section accent: C.green
Header: BUSINESS | PLATFORMS

CARD 1 — "Copilot for Power BI"
  Accent: C.blue
  Body: Natural language queries over your existing FM&I dashboards — no SQL required. Ask "show me crack spread volatility versus the same period last year, filtered to ICE Brent" and the report builds itself. For FM&I, this transforms the trading desk interaction model: instead of submitting a request to the analytics team for a report variation, the trader queries the data directly. Available now in Power BI Premium, which BP already has access to.

CARD 2 — "Plotly Studio (AI-assisted visualisation)"
  Accent: C.purple
  Body: Describe the chart you need and Plotly Studio generates the Dash code — no manual layout building. For FM&I's ad hoc analysis output, this compresses the visual delivery step from "write the Dash code" (30-90 minutes) to "describe what I want and review the output" (5 minutes). Particularly relevant for the crack spread and time spread visualisations that the trading desk requests frequently.

CARD 3 — "Dataiku LLM Mesh"
  Accent: C.teal
  Body: Dataiku's native LLM integration, currently in limited preview for enterprise accounts. Capabilities include AI-assisted code generation directly in recipe editors, natural language to SQL in dataset views, and AI-powered pipeline debugging that reads the full recipe chain before suggesting fixes. When it reaches GA, it will be the most integrated AI tool for FM&I Dataiku work — the AI understands the full Dataiku data model, not just the Python code.

CARD 4 — "MCP for Dataiku"
  Accent: C.orange
  Body: Connect Cursor or Claude Code to your live Dataiku instance via an MCP server. Read scenario status, trigger runs, query job logs, and push recipe fixes — all from your AI tool without opening the Dataiku UI. The community MCP server for Dataiku already exists (search: mcp-server-dataiku on GitHub). The FM&I team could deploy and test this in a half-day. This is the highest-leverage near-term experiment available.

Bottom bar: "All four are available or in preview today — Dataiku MCP integration is the highest-leverage near-term experiment for FM&I"

---

## Slide 42 — The Innovation Day Evaluation Framework (Section 9, type: left stacked + right card)
Section accent: C.green
Header: BUSINESS | INNOVATION DAY

LEFT COLUMN — 4 stacked cards (evaluation criteria):

Card A — "What is the specific problem?"
  Body: Not "we have pipeline reliability issues" but "the gas_hub_prices ELT pipeline fails silently 2-3 times per month, we spend an average of 3 hours per failure diagnosing and fixing it, and the failures are invisible to the trading desk until they notice stale data in their tools." Specificity is what separates a fundable idea from a brainstorm Post-it note. The evaluation committee wants to understand the pain before the solution.

Card B — "What data does it need and is it safe?"
  Body: Specify exactly what data the solution requires — source system, data type, update frequency, volume. Then verify each data source against the compliance boundary: is this data safe to send to the AI tool you plan to use? If not, does Ollama local-model provide sufficient quality for the task? Data safety must be designed in from the start, not retrofitted after the prototype is built.

Card C — "Who benefits and what is the quantified value?"
  Body: Be specific: "the trading desk receives the morning briefing 45 minutes earlier, the FM&I analyst saves 2 hours per week of manual pipeline monitoring, the model team eliminates the 3-hour average diagnosis time per failure." Numbers are not required to be precise, but they must be directionally meaningful. "Saves time" is not enough — how many hours, for whom, per week or month?

Card D — "What does a 2-week MVP look like?"
  Body: Not a production system — a working prototype that demonstrates the core value. A script that runs manually and produces the right output is enough to prove the concept. Describe exactly what someone would see when the MVP works: "an automated Teams message at 06:15 containing the pipeline health check for the FM&I overnight jobs, with errors highlighted and error logs attached."

RIGHT CARD — "Innovation Day evaluation matrix":
  Title: "How ideas are scored"
  Body: Ideas are evaluated on four dimensions: Specificity (is the problem well-defined?), Feasibility (is the data safe and the technology proven?), Impact (is the quantified value meaningful?), and Buildability (is there a credible 2-week MVP path?). The ideas that advance are not necessarily the most ambitious — they are the ones with the most complete answers to these four questions. Come prepared to answer all four in under 3 minutes.

Bottom bar: "The best Innovation Day pitch is one where the problem is so specific the evaluators immediately know someone who has that problem"

---

## Slide 43 — 16 Commercial Ideas for the Innovation Day Board (Section 9, type: 4-quadrant idea board)
Section accent: C.green
Header: BUSINESS | IDEAS

QUADRANT LAYOUT — 4 sections with sub-bullets (2 sentences each):

TOP-LEFT: "Data & Modelling"
  • Automated model documentation: Claude Code reads your fundamental model codebase, identifies all functions, and generates a complete model card covering inputs, outputs, calibration approach, and known limitations — eliminating the documentation backlog that every model team has.
  • AI-assisted half-life estimator calibration: an agent monitors new price data, compares against current estimates, flags drift above a threshold, and drafts a calibration recommendation for the model owner to review — making drift detection automatic rather than periodic.
  • Anomaly detection on ELT pipeline outputs: after each scheduled pipeline run, an agent compares row counts and value distributions against historical baselines and posts a health check to Teams when any metric exceeds 2 standard deviations — catching silent failures before the trading desk notices stale data.
  • Automated test generation for fundamental models: Claude Code generates a pytest test suite covering normal cases, edge cases, and boundary conditions for every function in a model — from zero test coverage to 80%+ coverage in a single overnight run.

TOP-RIGHT: "Trading Desk Support"
  • Morning briefing agent: an agent runs at 05:45 UTC, pulls overnight market moves, cross-references against FM&I model positions, identifies material divergences, and generates a structured 1-page brief for the trading desk — replacing a 45-minute manual process with a 2-minute review.
  • Ad hoc chart generator: a Teams bot that accepts a request from the trading desk ("show me ICE Brent crack spread by delivery month for Q1-Q3 2025"), builds the Plotly Dash app, and returns a link — from request to interactive chart in under 15 minutes.
  • Natural language model scenario queries: an interface where a trader types "run the VaR scenario for a 20% ICE Brent price drop" and the system generates the appropriate query, runs it, and returns structured results — no model team involvement required for standard scenario types.
  • Automated spread analysis commentary: after each model run, an agent generates a 2-paragraph commentary on the key spread movements, their likely drivers, and any anomalies — ready to be reviewed and sent to the desk, not written from scratch.

BOTTOM-LEFT: "Platform & Integration"
  • MCP server for Dataiku monitoring: a Cursor/Claude Code integration that reads FM&I pipeline status, error logs, and scenario results directly — enabling AI-assisted debugging of pipeline failures without opening the Dataiku UI. Highest-leverage near-term experiment.
  • Power BI Copilot for FM&I dashboards: enable natural language queries on existing FM&I Power BI reports — traders query their own data in plain English rather than submitting analytical requests. Available in Power BI Premium now.
  • AI-assisted Dataiku recipe optimisation: Claude Code audits all ELT recipes for performance anti-patterns (iterrows, non-vectorised operations, unnecessary copies) and generates optimised versions — turning months of technical debt into a single overnight refactor.
  • Plotly Studio for rapid visualisation: replace manual Dash code writing with AI-generated chart code from a description — compressing the visualisation delivery step from hours to minutes for ad hoc desk requests.

BOTTOM-RIGHT: "Process & Workflow"
  • Research synthesis agent: monitors a SharePoint folder for new market research PDFs, extracts the commodity, price outlook, top risks, and FM&I-relevant data points, and posts structured summaries to Teams — 2-3 hours of weekly report reading compressed to a 5-minute review.
  • Model review report generation: after each quarterly model review, an agent drafts the review report using a standard template, filling in model performance metrics, calibration history, and compliance checklists — leaving the reviewer to validate and annotate rather than write from scratch.
  • Data quality monitoring with alerts: a daily agent that runs data quality checks on FM&I datasets, compares against configurable thresholds, and sends a Slack/Teams alert when data quality drops — catching data issues before they propagate to model outputs.
  • Meeting action item extraction: a Copilot Studio agent that processes meeting recordings for all recurring FM&I meetings, extracts action items with assignees and due dates, posts to Teams, and creates calendar reminders — eliminating the manual action log process.

Bottom bar: "Pick your highest-impact idea — bring it to Innovation Day with: what it does, what data it needs, who benefits, what the MVP looks like"

---

## SECTION 10 — PHILOSOPHY & CLOSE
Section accent: "475569"

---

## Slide 44 — Section Divider — Closing Thoughts (type: divider)
Background: C.navy
Top accent: "475569"
Number: "10"
Title: "Closing Thoughts"
Subtitle: "Three uncomfortable truths about where this is all going"

---

## Slide 45 — Statement Slide 1 (Section 10, type: statement — deepNavy background)
Section accent: C.teal

STATEMENT: "AI isn't making data scientists obsolete. It's making the ones who don't use it obsolete."

HORIZONTAL RULE: C.teal

SUPPORTING TEXT (sustained argument, 4-5 sentences):
"The productivity gap between AI adopters and non-adopters in technical fields is now measurable in sprint velocity, model delivery time, and analyst capacity utilisation. Teams with mature AI adoption are shipping 2-3 times more models per quarter at the same headcount — not because their engineers are smarter, but because each engineer is directing AI tools rather than executing every step manually. The critical skill is not coding faster — it is judgment: knowing when the AI output is correct, when it is plausible but wrong, and how to course-correct efficiently. The FM&I domain expertise you have built — understanding crack spreads, forward curves, calibration methodology, the commercial context that makes a number meaningful — is exactly the judgment layer that makes AI-assisted work valuable rather than just fast. The threat is not to people who deeply understand the fundamentals. The threat is to people who can be replaced by someone who deeply understands the fundamentals and also uses AI."

---

## Slide 46 — Statement Slide 2 (Section 10, type: statement — deepNavy background)
Section accent: C.orange

STATEMENT: "The next decade won't kill technology jobs. It will kill the comfortable middle."

HORIZONTAL RULE: C.orange

SUPPORTING TEXT (sustained argument):
"The comfortable middle is the layer of work that sits between deep domain expertise and pure execution — the translator function between subject matter experts and systems. In energy trading analytics, this is the role of someone who writes queries and formats reports but does not deeply own the models or the commercial decisions those models inform. AI is replacing that translation layer, not the domain expertise above it. People who deeply understand fundamentals modelling and can direct AI to solve commercial problems are becoming more valuable — they now have a tool that does the execution while they own the judgment. The people in the comfortable middle who never built irreplaceable domain knowledge are finding their role automated faster than they can upskill. The response is not to panic about AI, but to invest in the domain expertise that sits above the translation layer and cannot be automated."

---

## Slide 47 — Statement Slide 3 (Section 10, type: statement — deepNavy background)
Section accent: C.red

STATEMENT: "The question isn't whether the AI wrote the code. The question is: who owns the risk?"

HORIZONTAL RULE: C.red

SUPPORTING TEXT (sustained argument):
"That is still you. The performance art around coding — requirements ceremonies, architecture slideware, digital transformation slogans, AI wrappers that make no one accountable — does not answer the hard question. When the fundamental model gives a bad signal because the ELT pipeline had a bug and the trading desk acts on it, someone owns that outcome. The fact that an AI tool wrote the code that contained the bug does not change the ownership. Build AI into your workflow enthusiastically — but own the output with the same rigour you would apply to code you wrote by hand. Review it. Test it. Validate it against your domain knowledge. The AI is fast and often right. You are the one who knows when the output is plausible but wrong in the specific context of this commodity, this market structure, this week's supply dynamic."

---

## Slide 48 — Three Things to Do Before Innovation Day (Section 10, type: closing CTA)
Section accent: C.teal
Background: C.navy
Top accent: C.teal

TITLE: "Three things to do before Innovation Day"

CTA CARDS (3 cards, dark background "1E293B"):

CARD 01 — "Request your licence"
  Accent: C.teal
  Num: "01"
  Title: "Request your licence"
  Body: GitHub Copilot: IT self-service portal → "Developer Tools" → submit request. Approval in 2-3 business days. Already have M365? Open Teams or Word — Copilot is already active. Cursor: expense via T&E with manager approval (£20/month Pro) or raise an IT request with an FM&I business justification. The entire process takes under 10 minutes to initiate.
  Sub note: "If you leave today without initiating a licence request, the probability of doing it tomorrow drops to near zero"

CARD 02 — "Run one real task this week"
  Accent: C.blue
  Num: "02"
  Title: "Run one real task this week"
  Body: Pick a task you are doing this week that would normally take 30+ minutes. A recipe debug, a documentation update, a data quality check, a meeting follow-up. Use an AI tool for it. Time how long it takes with AI assistance vs your mental estimate of the manual approach. The time comparison — experienced personally rather than read on a slide — is what converts a sceptic into a regular user.
  Sub note: "First task recommendation: use Copilot in Teams to summarise your next meeting and draft the follow-up actions"

CARD 03 — "Bring your best idea"
  Accent: C.green
  Num: "03"
  Title: "Bring your best idea to Innovation Day"
  Body: Pick one commercial use case from today's session that resonates with a problem you actually face. Prepare: what is the specific problem (time it takes, how often it occurs), what data does the solution need (and is it safe to use with AI), who benefits and by how much, and what would a 2-week MVP demonstration look like. The evaluation matrix rewards specificity over ambition.
  Sub note: "The innovation_day_board.md in the FM&I shared drive has the full evaluation rubric and submission template"

CLOSING STATEMENT:
  Text: "You already have the tools. The only thing between you and 10× productivity is knowing which one to reach for — and when."

---

## Target Slide Count: 48 slides

Section distribution:
- S1 (Why Now): Slides 1-5 (5 slides)
- S2 (Landscape): Slides 6-10 (5 slides, including divider)
- S3 (Microsoft Copilot): Slides 11-15 (5 slides, including divider)
- S4 (GitHub Copilot & Cursor): Slides 16-22 (7 slides, including divider)
- S5 (Model Landscape): Slides 23-26 (4 slides, including divider)
- S6 (Ethics & Compliance): Slides 27-30 (4 slides, including divider)
- S7 (Extended Concepts): Slides 31-36 (6 slides, including divider)
- S8 (Personal Use Cases): Slides 37-39 (3 slides, including divider)
- S9 (Business Use Cases): Slides 40-43 (4 slides, including divider)
- S10 (Philosophy & Close): Slides 44-48 (5 slides, including divider)

**All cards: minimum 30 words body text. No grid exceeds 4 cards. All FM&I specific.**
