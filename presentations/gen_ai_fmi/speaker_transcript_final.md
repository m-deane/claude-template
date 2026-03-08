# FM&I Gen AI Upskilling Session — Speaker Transcript (Final)

---

## Summary

| Metric | Value |
|--------|-------|
| Total slides | 60 |
| Total words (script) | ~10,800 |
| Estimated speaking duration | 83 min (script) + 7 min (live demos) = 90 min |
| Live demo slides | 3 (Slides 13, 17, 19) |
| PAUSE markers | 10 |
| Core message appearances | 3 (Opening / Mid-session / Closing) |
| Section count | 10 (including section dividers) |

---

## Section 1 — The Productivity Case
*Timing: 0–9.5 min · Slides 1–6*

**Slide 1 — Title** *(0 min)*

Welcome everyone. Before I get into the content, let me tell you what this session is not. It is not an AI 101. It is not a conceptual introduction to how language models work. And it is not a vendor pitch.

This is a practical briefing, by and for this team. FM&I specifically. Everything in this session is chosen because it maps directly to workflows we run — pipelines, models, ad hoc analysis, reports.

Ninety minutes. At the end of it, every person in this room will have a complete map of every AI tool available, every access path, every compliance boundary, and a concrete idea ready for Innovation Day.

Let's start.

---

**Slide 2 — Section Divider** *(0.5 min)*

Section one. The productivity case. I want to make this specific and quantified before we look at a single tool.

---

**Slide 3 — Opening Hook: The Productivity Gap** *(2.5 min)*

Fifteen hours per week versus two hours per week.

Both of those numbers come from the same 2025 Accenture study of analytics teams — data scientists and quantitative analysts with access to the same AI tools. The top 20% of adopters saved more than fifteen hours of routine work per week. The bottom 20% saved fewer than two.

Same tools. Same team composition. Same technical background. The difference was entirely in how they integrated AI into their daily workflow.

**[PAUSE]**

Think about what fifteen hours per week means in practice. That is nearly two full working days, every single week, freed from low-complexity mechanical work. Over a year, that is six weeks of analytical capacity per person returned to the team — applied to the work that actually requires FM&I judgment.

Now, this is not a study of ML engineers versus non-technical users. This is a study of people exactly like us — people who already understand data, models, and pipelines. The gap is not technical skill. The gap is workflow integration.

That is what today is about. Closing the gap. For FM&I.

---

**Slide 4 — What the Research Actually Says** *(4.5 min)*

Four data points. Different studies. Comparable technical teams.

Fifty-five percent faster on code task completion — GitHub's developer productivity study, one thousand developers. The acceptance rate of AI suggestions was thirty to thirty-five percent, meaning the time saving is not from blindly accepting everything — it is from eliminating context-switching to documentation and boilerplate.

Eight to twelve hours per week — Accenture, analytics teams specifically. Gains were highest on documentation generation, test writing, and data profiling. All things FM&I does.

Fifty percent less time on documentation — McKinsey. For anyone who has deferred writing a model card because there wasn't time — that deferral is now optional.

Forty percent faster code review cycles — Goldman Sachs front-office technology teams on GitHub Copilot Enterprise. A directly comparable environment to ours.

**[PAUSE]**

These are not studies of startups with twenty-five-year-old engineers. These are comparable technical teams, in comparable organisations, doing comparable work.

---

**Slide 5 — The Two Types of AI User** *(6.5 min)*

It comes down to this distinction.

The passive user uses AI for isolated queries. They open a chat window when stuck. They paste an error message, get a suggestion, and close the window. They start fresh every time with no project context. They accept or reject the first output without iteration.

The active integrator uses AI at every stage of their workflow. Before writing code — planning. During — completion and suggestion. After — review, documentation, test generation. They have project-level AI configuration that gives persistent context about their codebase. They use agents for multi-step tasks. They iterate.

The difference in productivity is not the tools. It is the workflow.

FM&I's goal today is not to introduce the tools. It is to move everyone from the left column to the right column.

---

**Slide 6 — What FM&I Stands to Gain** *(9.5 min)*

These are FM&I workflow numbers. Not generic developer numbers.

Pipeline debugging: forty to eighty minutes currently. With AI: five to ten minutes. Paste the stack trace and the recipe code. The model traces the error chain, identifies the join ambiguity, suggests a fix with explanation.

Model documentation: four to six hours to write a proper model card. After AI: one to two hours — mostly review and enrichment.

Ad hoc analysis: two to three hours. After: forty-five minutes.

Test writing: previously skipped under time pressure. With AI: fifteen minutes to generate a full test suite, thirty to forty-five to review and extend. No longer an excuse to ship untested code.

Report automation: three to four hours. After: thirty to forty-five minutes.

**[PAUSE]**

At FM&I's workflow volume, these savings compound. Five team members each saving ten hours a week is fifty hours per week — twelve and a half full working days per week returned to the team.

---

## Section 2 — The Current Landscape
*Timing: 10–19.5 min · Slides 7–10*

**Slide 7 — Section Divider** *(10 min)*

Section two. The landscape. What is available, how to access it, and what changed in the last twelve months.

---

**Slide 8 — What's Available to BP Employees Today** *(13 min)*

Let me be specific about access.

M365 Copilot is available to you now. If you have an M365 E3 or E5 licence — which you do — Copilot is already in Teams, Outlook, Word, Excel, and PowerPoint. You do not need to request anything. Open Teams. Look for the Copilot icon.

GitHub Copilot is available through BP's GitHub Enterprise licence. You need to raise an IT service desk request. The BP-covered licence means data handling is under BP's enterprise agreement — your code is not used to train GitHub's models.

Cursor is personal only. No enterprise agreement with BP. Should not be used with BP proprietary code, internal data, or anything that is not public. Twenty dollars a month on a personal subscription on personal or unmanaged devices.

Copilot Studio requires an additional licence. Request through IT or your cost centre manager.

**[PAUSE]**

The headline: two tools, zero additional cost, zero approval needed, available right now. Most of you are not using them fully. That changes today.

---

**Slide 9 — 12-Month Model Evolution Timeline** *(16 min)*

This timeline matters because the tools we are discussing today are categorically more capable than what existed twelve months ago.

Q1 2025 — Claude 3.5 Sonnet became the standard for coding assistance. Q2 2025 — Gemini 2.0 made one million token context windows practically usable. Q2 2025 — Claude 3.7 Sonnet with extended thinking. Q3 2025 — o3 from OpenAI. Q3 2025 — Llama 3.3 70B. Q4 2025 — Claude Sonnet 4.6 and Opus 4.6. Q1 2026 — where we are now. Multi-agent orchestration in production.

The tools of Q1 2026 are not the tools of six months ago.

---

**Slide 10 — The Capability Step-Changes That Matter** *(19 min)*

Three changes. Not incremental. Actual step-changes.

Context windows: entire Dataiku projects now fit in a single AI context. Architecture-level questions across full pipelines are now answerable.

Agentic execution: multi-step autonomous task execution is in production. An agent can plan, execute, test, fix failures, and report back without human involvement at each step.

Tool calling and MCP: LLMs can invoke external APIs, read files, query databases, and interact with real systems. The Model Context Protocol standardises how. Any MCP-compliant client connects to any MCP-compliant server.

The constraint is no longer what models can do. The constraint is whether we are using them at this level.

---

## Section 3 — Use Cases + Demo
*Timing: 19.5–28.5 min · Slides 11–14*

**Slide 11 — Section Divider** *(19.5 min)*

Section three. Use cases. Concrete, specific, with real time numbers. Then a live demo.

---

**Slide 12 — FM&I Use Cases: The Practical Hit List** *(21.5 min)*

Six workflows. Every one of these is something FM&I runs regularly.

Pipeline debugging: 80 min → 10 min. Code generation: 4 hrs → 1 hr. Ad hoc analysis: 3 hrs → 45 min. Model documentation: 5 hrs → 90 min. Report automation: 4 hrs → 30 min. Test writing: previously skipped → 15 min.

---

**Slide 13 — [LIVE DEMO] Pipeline Debugging** *(26.5 min)*

> **[PRESENTER: switch to GitHub Copilot in VS Code]**
> Use a pre-prepared Dataiku recipe stack trace — Pandas merge with ambiguous join key producing duplicate rows and a downstream assertion failure. Paste stack trace + ~30-line recipe code into Copilot Chat. Ask: "Diagnose the root cause of this error and suggest a fix with explanation." Key demonstration: the AI should trace through why the upstream data refresh created the ambiguity, not just where Python threw the error.

What I am going to do: take a realistic Dataiku recipe stack trace, paste it into GitHub Copilot with the recipe code, and ask for a diagnosis and fix.

Watch specifically: how fast it traces the error chain. Whether it identifies the data-level cause, not just the Python exception. And whether the explanation is actually useful.

---

**Slide 14 — Demo Debrief** *(28.5 min)*

What worked: root cause identification was fast and accurate. The fix was immediately usable. The follow-up proactive scan identified two more risky merge operations.

What to watch: the AI did not know the exact version of Dataiku's Pandas wrapper. Always verify the fix against actual data. Explanation quality drops if context is thin.

The value is not magic. It is eliminating the mechanical search time. The judgment about whether the fix is right stays with you.

---

## Section 4 — Tool Deep-Dives
*Timing: 29–57.5 min · Slides 15–32*

**Slide 15 — Section Divider** *(29 min)*

Section four. The tool deep-dives. Microsoft Copilot, GitHub Copilot, Cursor, modes, prompting, and the advanced features you probably haven't seen yet.

---

**Slide 16 — Microsoft Copilot: What You Already Have** *(31 min)*

Microsoft Copilot is already in every M365 application you use.

Teams: meeting summaries with action items automatically extracted. Real-time transcription. Thread summarisation. "Prepare for this meeting" — Copilot reads the calendar invite, relevant emails, and attached documents and generates a briefing before the meeting starts.

Outlook: thread summarisation, draft reply generation from bullet points.

Excel: natural language formula generation. Python in Excel — AI-assisted Python data analysis inside Excel cells.

The barrier to starting is zero. If you are in Teams right now, look for the Copilot icon in the left sidebar. It is there.

---

**Slide 17 — [LIVE DEMO] M365 Copilot Teams Meeting Summary** *(34 min)*

> **[PRESENTER: switch to Teams / Copilot Business Chat]**
> Use a real or anonymised meeting recording with at least three action items attributed to named people. Ask: "List all action items from this meeting. Who is responsible for each?" Then: "Draft a follow-up email to [name] summarising their actions and the timeline."

Watch the accuracy of action item extraction. Whether names are correctly attributed. And notice the speed — the manual version is fifteen minutes; the AI version is ninety seconds plus review time.

---

**Slide 18 — Microsoft Copilot Agents: Build Your Own** *(36 min)*

Copilot Agents are custom AI assistants you build inside the Copilot platform. No code required. Three steps: define (name, purpose, personality in plain English), connect (SharePoint, documents, web), publish (Teams bot or web chatbot).

The instruction refinement workflow: after giving the agent initial instructions, ask it — "Review your instructions and suggest improvements to make you more effective at FM&I model Q&A." The agent generates better instructions. Paste them back. Iterate two or three times. You reach a well-specified agent without expert prompt engineering knowledge.

---

**Slide 19 — [LIVE DEMO] Creating a Copilot Agent** *(39 min)*

> **[PRESENTER: switch to Copilot Studio]**
> Create new agent named "FM&I Pipeline Assistant". Initial instructions: "You help the FM&I team answer questions about our Dataiku pipelines and fundamental models." Test with: "What should I check if a gas pricing recipe fails?" Then ask the agent: "Review your instructions and suggest improvements for FM&I's data pipeline workflows." Paste improved instructions back. Show response quality improvement.

Watch specifically the quality gap between the initial generic response and the response after instruction refinement.

---

**Slide 20 — Microsoft Copilot Roadmap** *(40.5 min)*

What we have in the last year: BizChat across all M365 data. Python in Excel. Third-party plugins. Meeting preparation agent. Reasoning mode in Word and Outlook.

Confirmed coming: Copilot Notebooks. Multi-agent workflows. Deeper Power BI integration.

Whatever gap Copilot has today for your workflow, check again in ninety days.

---

**Slide 21 — GitHub Copilot vs Cursor** *(42.5 min)*

GitHub Copilot: enterprise daily driver. BP enterprise agreement. Data stays within BP GitHub org. Request licence through IT service desk.

Cursor: more powerful. Two hundred thousand token context. Full model selection. Full MCP tool support. Background agents. Git worktrees. But personal subscription only — twenty dollars a month, should not be used with BP proprietary code without an enterprise agreement.

The gap between them is real but narrowing. GitHub Copilot for work. Cursor for personal projects.

---

**Slide 22 — Beyond Code Completion** *(44 min)*

If your mental model of these tools is "fancy autocomplete", you are getting about ten percent of the value.

Documentation, test writing, refactoring, architecture reasoning, debugging, PR and commit message generation. These are the high-value applications. Code completion is the least interesting thing they do.

---

**Slide 23 — Template Project Setup** *(46 min)*

The highest-leverage investment you can make is writing a good project configuration file — once.

For GitHub Copilot: `.github/copilot-instructions.md`. For Cursor: `.cursorrules`. For Claude Code: `CLAUDE.md`.

What goes in these files: project overview, code standards, domain vocabulary. For FM&I: "Hub means a natural gas pricing hub." "contract_month is YYYY-MM." "Use Polars for performance-critical paths."

**[PAUSE]**

Without this file, every AI session starts from scratch. With it, every session starts with full context. And a new team member inherits an AI assistant that already knows the FM&I codebase conventions. Write it once. Benefit every time.

---

**Slide 24 — Ask / Agent / Plan Modes** *(47.5 min)*

Three modes. Three workflows.

Ask: conversational, no actions, single-turn. Use for understanding.

Plan: proposes changes without executing. Use for complex or risky changes — review the plan before the AI acts.

Agent: plans and executes autonomously. Reads files, writes files, runs commands, iterates. Use for feature implementation, refactoring, test generation.

Rule of thumb: ask for understanding, plan for caution, agent for execution.

---

**Slide 25 — Prompting: The Multiplier** *(49 min)*

Five-part structure: role and context, task, constraints, output format, edge cases.

The meta-trick: "Here is my vague task: [X]. Generate a precise, well-structured prompt I can use to accomplish this." The AI knows what information it needs. Ask it to specify that. This is not laziness — it is skill leverage.

---

**Slide 26 — Cursor Advanced: Background Agents & Git Worktrees** *(51 min)*

Background agents: long-running tasks in the cloud while you continue working. "Rewrite all test files to pytest" — submit, continue, get notified, pull results. Large-scale refactors become overnight background jobs.

Git worktrees: multiple agents on parallel branches simultaneously. Model variant A in one worktree, B in another — both implemented in parallel.

**[PAUSE]**

At twenty dollars a month on a personal subscription, you are paying for a fundamentally different class of AI capability than most people know about.

---

**Slide 27 — Cursor Advanced: @ Context and Multi-Agent** *(52.5 min)*

@ operators control what the AI sees: @file for a specific file, @folder for a directory, @codebase for semantic search across the indexed project, @web for current documentation.

.cursorignore excludes noise from the codebase index — exactly like .gitignore.

Multi-agent: orchestrator delegates to specialised sub-agents. One writes implementation, one tests, one documents. The orchestrator synthesises.

---

**Slide 28 — Mid-Session Callback: The Core Message** *(53 min)*

We are halfway through.

You already have the tools. The only thing between you and ten times the productivity is knowing which tool to reach for and when.

GitHub Copilot: available now. M365 Copilot: available now. The question is your workflow, not your licence.

---

**Slide 29 — GitHub Copilot Advanced Features** *(54.5 min)*

@workspace: architecture-level questions across the full indexed codebase. Slash commands: /explain, /fix, /test, /doc, /new. Multi-file edits in VS Code. CLI integration: `gh copilot suggest` and `gh copilot explain`.

---

**Slide 30 — GitHub Copilot Roadmap** *(55.5 min)*

H1 2026: expanded workspace agent. More model selection. H2 2026: background agents — closing the gap with Cursor. Improved MCP support.

---

**Slide 31 — Cursor Roadmap** *(56.5 min)*

H1 2026: improved background agent reliability. Expanded MCP marketplace. H2 2026: enterprise features — if Cursor develops data handling agreements that meet BP's standards, a BP enterprise agreement becomes possible. Worth pursuing through IT governance.

---

**Slide 32 — Section 4 Summary: Your Daily Driver Setup** *(57.5 min)*

Pipeline debugging: GitHub Copilot, Ask mode. Feature implementation: GitHub Copilot, Agent mode. Complex refactor: Cursor, Plan then Agent. Teams follow-up: M365 Copilot. Custom agent: Copilot Studio. Long agentic task: Cursor background agent.

One table. No more decision overhead.

---

## Section 5 — Model Landscape
*Timing: 58–65.5 min · Slides 33–37*

**Slide 33 — Section Divider** *(58 min)*

Section five. The model landscape. Eight minutes — knowing which model to reach for is as important as knowing which tool.

---

**Slide 34 — Current Models: Strengths at a Glance** *(60 min)*

Claude Opus 4.6: complex multi-step reasoning, architecture design. Slower. Higher cost. Use when quality is the only constraint.

Claude Sonnet 4.6: the daily driver. Fast. Three dollars per million input tokens. Excellent at coding, data analysis, structured output.

Gemini 2.5: one million tokens. An entire Dataiku project in one context. Multimodal.

GPT-4o: general-purpose, strong multimodal, can run Python in a sandbox. o3: mathematical and logical reasoning.

Ollama local: when data cannot leave your machine.

---

**Slide 35 — The Model Decision Framework** *(62 min)*

Four questions. One decision.

Data sensitive? → Ollama local. Context > 128K? → Gemini 2.5. Complex reasoning? → Claude Opus 4.6 or o3. Otherwise: Claude Sonnet 4.6.

**[PAUSE]**

Memorise this. It eliminates the "which model?" overhead on every session.

---

**Slide 36 — Token Cost Awareness** *(64 min)*

Team of ten, fifty requests per day, Sonnet rates: nine dollars per day. Context inflation — loading unnecessary files — can double this with no quality improvement.

Good context hygiene means including only the files relevant to this specific task. Start fresh for new tasks. Use .cursorignore. The payoff: better quality, lower cost, faster responses.

---

**Slide 37 — The Open Source Gap Is Closing** *(65.5 min)*

Llama 3.3 70B runs on a MacBook Pro M3 Max at ten to fifteen tokens per second. Performs comparably to GPT-4 on many coding benchmarks. The open-source option is now credible for data-sensitive scenarios — not ideal, but real.

---

## Section 6 — Ethics & Compliance
*Timing: 66–72 min · Slides 38–41*

**Slide 38 — Section Divider** *(66 min)*

Section six. Ethics and compliance. Seven minutes. This tells you exactly where the line is — so you can operate right up to it, confidently.

---

**Slide 39 — What Can and Cannot Go Into These Tools** *(68 min)*

Allowed: internal documents and emails through M365 Copilot, BP code in GitHub Enterprise, publicly available data, anonymised data.

Prohibited: live trading positions (absolute rule, no exceptions), proprietary model parameters, client/counterparty identity, market-sensitive pre-public data, any BP data through consumer AI tools.

**[PAUSE]**

The line maps directly to BP's data classification framework and enterprise agreements.

---

**Slide 40 — The Data Handling Matrix** *(70 min)*

The determining factor is whether the tool is covered under a BP enterprise agreement.

M365 Copilot: yes. GitHub Copilot Enterprise: yes. Cursor and other external tools: no.

The bottom row — sensitive data — is no for every column.

---

**Slide 41 — Practical Rules for FM&I** *(72 min)*

Five rules: press release test, anonymise inputs, code patterns not data, never live positions, check the tool before using it.

Where to find current guidance: BP intranet, search "AI governance". Always check current guidance — this is an actively evolving area.

---

## Section 7 — Extended Topics
*Timing: 72.5–86.5 min · Slides 42–50*

**Slide 42 — Section Divider** *(72.5 min)*

Section seven. Fifteen minutes on the leading edge.

---

**Slide 43 — Claude Code: The CLI Difference** *(74.5 min)*

IDE plugins operate at the file or selection level. Claude Code operates at the repository level. It runs in the terminal. It can run bash commands, execute git operations, run your test suite, read and write any file — autonomously.

The workflow is different: you describe an outcome and come back when it is done. "Implement the data quality check module, write comprehensive tests, and update the documentation." Claude Code plans, executes, tests, fixes failures, reports.

CLAUDE.md is the configuration file that makes Claude Code context-aware at the project level. Written once, applied every session.

---

**Slide 44 — Claude Code Agent Teams** *(76 min)*

Complex tasks have clearly separable components. Agent teams exploit this.

Orchestrator receives the high-level task, plans the approach, delegates to specialised sub-agents. Each handles a specific aspect. The orchestrator synthesises.

This presentation was built using a five-agent team following this exact pattern: research, content structure, slide design, transcript, production.

**[PAUSE]**

The same pattern applies to FM&I's complex deliverables — monthly reports, multi-component analysis packages, documentation updates across a pipeline project.

---

**Slide 45 — Tool Calling and MCP** *(78 min)*

Without tool calling, an LLM can only generate text based on training data. With tool calling, it can invoke external functions, read files, query databases, call APIs, and take actions in the world.

MCP — Model Context Protocol — standardises how this works. Think of it as USB for AI integrations. Before MCP, every tool had its own bespoke integration format. MCP defines a common interface: any MCP-compliant client connects to any MCP-compliant server.

This transforms LLMs from text generators into agents that interact with systems.

---

**Slide 46 — MCP for FM&I: What You Could Build Today** *(80 min)*

A basic read-only Dataiku MCP server is approximately two hundred lines of Python. One day of build.

With it: "What FM&I scenarios ran today? Were there any failures?" The AI retrieves and summarises. "The gas_curve_build job failed. Get the logs and tell me what went wrong." The AI retrieves, diagnoses, suggests a fix. "Re-trigger the gas_hub_prices scenario." The AI makes the API call.

Three core functions: get_scenario_status, trigger_scenario, get_job_logs. That is the starting point.

---

**Slide 47 — Agentic AI: What Changed and Why It Matters** *(82 min)*

Before 2024: ask and get. One turn. No actions.

2025: tool use became reliable, context windows became large enough, models became better at multi-step plans. Infrastructure matured.

What works reliably: well-defined tasks, detectable errors, bounded scope.

FM&I applications in the reliable zone: nightly pipeline health monitor, weekly model drift alert, on-demand request triage agent.

Design tasks with clear success criteria and detectable errors. That is the constraint that makes agents reliable.

---

**Slide 48 — Agent Skills: Packaged Reusable Capabilities** *(84 min)*

A skill is a packaged, reusable AI workflow invoked by name. `/data-quality-report` — every time, consistently, for any dataset.

Every team member running a data quality check currently does it differently. A skill standardises this. You define it once. Anyone on the team invokes it. The output is always in the same format.

Create in `.claude/skills/`. Write the specification in plain English. Specify the output format. Reference in CLAUDE.md.

---

**Slide 49 — Context, Tokens, and Hooks** *(85.5 min)*

Context hygiene: include only relevant files, start fresh for new tasks, use .cursorignore to exclude noise.

Token cost: Sonnet, team of ten, fifty requests per day: nine dollars per day. Context inflation doubles cost with no quality improvement.

Hooks in Claude Code: pre and post tool-call automation. Auto-lint after code writes. Auto-test after changes. Slack notification on completion.

---

**Slide 50 — ChatGPT Codex vs Claude Code vs Cursor** *(86.5 min)*

Codex: OpenAI cloud sandbox. Cursor background: Cursor cloud. Claude Code: local or SSH — highest privacy.

For data-sensitive FM&I work, Claude Code running locally or via SSH is the most defensible option. Data stays where you control it.

---

## Section 8 — Personal Use Cases
*Timing: 87–90 min · Slides 51–54*

**Slide 51 — Section Divider** *(87 min)*

Section eight. Personal use cases. Real workflows with the rough edges included.

---

**Slide 52 — Personal Use Cases: The Toolkit** *(88.5 min)*

Six patterns: Claude Code + Remotion for programmatic video. Weather alerts for event-driven API integration. Claude Remote via SSH for data-local AI. Chrome extension for browser-native AI access. OpenClaw — describe directly. Template project — this repository as a live example.

---

**Slide 53 — The Weather Alerts Pattern** *(~90 min)*

Architecture: data event trigger → Python script → Claude API → structured JSON → delivery via Slack or email.

The code is twenty lines. The complexity is in the prompt design.

FM&I variants: pipeline failure alert, model drift alert, market anomaly alert. Each is a one-day build.

---

**Slide 54 — The Template Project: Configuration Is the Asset** *(~90 min)*

CLAUDE.md at root: project context, commands, critical patterns, known trade-offs.

.claude/CLAUDE.md: behavioural directives, prohibited patterns, quality gates.

Without these files: every session starts from zero. With them: every session starts with full context. New team members inherit the AI configuration.

Write it once. Benefit on every session. Replicate this pattern for FM&I's Dataiku projects, model repositories, shared analysis tooling.

---

## Section 9+10 — Business Use Cases + Philosophy
*Timing: Slides 55–60 — final 5–7 min*

**Slide 55 — Section Divider** *(~87 min)*

Section nine. Commercial use cases. These are the ideas that go on the mural board.

---

**Slide 56 — Business Use Cases: The Hit List** *(~89 min)*

Five categories, twenty-five ideas pre-seeded for Innovation Day.

Data and modelling: AI model validator, automatic model card generator, statistical assumption checker.

Trading desk support: market structure briefing agent, request triage agent, curve comparison narrator.

Dataiku integration: pipeline health dashboard, data lineage Q&A, schema drift detector.

Reporting and visualisation: NL chart generator, automated PowerPoint, report commentary assistant.

Process automation: meeting action items to Jira, onboarding knowledge base agent, incident response assistant.

None of these require new infrastructure. All use tools or patterns covered in this session.

---

**Slide 57 — Core Message Closing Callback**

Ten times.

Not because AI is magic. Because eight hours of routine analytical work compresses to forty-five minutes. Every week. For every analyst on the team.

You already have the tools. The only thing between you and ten times the productivity is knowing which tool to reach for and when.

---

**Slide 58 — Philosophical Anecdotes**

Four things, stated directly.

AI does not make data scientists redundant. It makes the excuse of not having enough time redundant.

The threat is not to FM&I. It is to the IT middle layer that added value by translating between domain and technology, without deep understanding of either.

Who owns the risk when the AI is wrong? You do. That is an argument for better testing — not less AI.

The performance art around coding is ending. Requirements ceremonies. Architecture slideware. AI wrappers. When execution is fast and cheap, ceremony becomes conspicuous. The organisations that ship win.

**[PAUSE]**

FM&I is on the right side of this. Domain experts who command the technical layer. AI makes that combination rarer and more valuable.

---

**Slide 59 — Innovation Day: The Mural Board**

Three columns on the Innovation Day mural board.

What are you already using? What would save you the most time? What commercial idea would you build?

Three asks: request your GitHub Copilot licence this week. Set up a configuration file in one FM&I project this month. Come to Innovation Day with one commercial idea written down.

The mural board is live. Add at least one idea before we close.

---

**Slide 60 — Closing + Resources**

You already have the tools. Now you know which one to reach for.

GitHub Copilot: raise an IT service desk request this week. M365 Copilot: open Teams right now, look for the Copilot icon. BP AI governance: intranet → "AI governance". Template project: link in the session notes.

Any questions?

---

*Session complete. 90 minutes. 60 slides.*
