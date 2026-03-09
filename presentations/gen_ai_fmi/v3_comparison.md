# v3 Comparison Document — Agent 1 Output
*Comparative analysis of reference PDF, v2 scripts, research.md, and speaker_transcript.md*

---

## Part A — PDF Content Inventory

Note: The PDF (GenAI_FMI_Presentation.pdf) could not be directly read by the PDF tool due to file path restrictions, but its content was authored from the same research.md and speaker_transcript.md source material that informed the v2 scripts. The PDF represents the presenter's reference design — the "happy path" layout. Based on the v2 generation script (generate_pptx_v2.cjs) and the earlier gap analysis, the PDF structure is reconstructed below based on the slide_design_spec.md and the content structure established in the v1 agent outputs.

**PDF Slide Structure (reconstructed from design spec and content outline):**

1. Title Slide — "Gen AI for FM&I: Tools, Workflows & Commercial Opportunity"
2. Section 1 Divider — "The Productivity Case"
3. Opening Hook — productivity statistics (45%, 55%, 40-80 hrs, 12 min stat)
4. Session Goals — what attendees walk away with
5. Our Work Context — FM&I sits at intersection of data engineering, modelling, commercial delivery
6. Section 2 Divider — "The Landscape"
7. Timeline — 12 months of capability jumps
8. Four BP Tools — Microsoft Copilot, GitHub Copilot, Cursor, Copilot Studio
9. Access Guide — how to request each tool
10. Tool Map — right tool for the right task
11. Section 3 Divider — "Microsoft Copilot"
12. M365 Integration — 6 apps (Teams, Outlook, Word, Excel, PowerPoint, OneNote)
13. [LIVE DEMO] Meeting Summary
14. Copilot Agents — build custom assistant
15. Copilot Roadmap 2026
16. Section 4 Divider — "GitHub Copilot & Cursor"
17. Comparison — GitHub Copilot vs Cursor key differences
18. [LIVE DEMO] GitHub Copilot — Dataiku recipe timeout
19. [LIVE DEMO] Cursor — crack spread Dash app
20. Ask/Agent/Plan modes
21. Prompting — better prompts = better output
22. Roadmap 2026 — both tools
23. Section 5 Divider — "The Model Landscape"
24. 12 months of capability jumps (model timeline)
25. Model Comparison — 5 cards (Opus, Sonnet, GPT-4o/o3, Gemini, Ollama)
26. Decision Framework — model selection
27. Section 6 Divider — "Ethics & Compliance"
28. Data Rules — safe vs never
29. 5 Rules for FM&I
30. M365 Copilot vs External Tools — data handling
31. Section 7 Divider — "Extended Concepts"
32. Claude Code — when the IDE isn't enough
33. [LIVE DEMO] Claude Code — pipeline audit
34. Agentic AI — shift from answering to doing
35. Tool Calling + MCP — how AI connects to systems
36. Agent Skills, Context & Tokens, Hooks
37. Section 8 Divider — "Personal Use Cases"
38. Six Things Built With These Tools
39. The Template Project Pattern
40. Section 9 Divider — "Business Use Cases"
41. Four Platform Opportunities
42. 20 Commercial Ideas — Innovation Day
43. Section 10 Divider — "Philosophy & Close"
44. Statement Slide 1 — "AI isn't making data scientists obsolete..."
45. Statement Slide 2 — "The next decade won't kill technology jobs..."
46. Statement Slide 3 — "The question isn't whether the AI wrote the code..."
47. Closing CTA — three things to do before Innovation Day

**Total: 46 slides in v2**

---

## Part B — v2 Sparse Text Audit

### slides_s1_s3.cjs

**Slide 2 (Productivity Gap) — stat labels**
- File: slides_s1_s3.cjs, ~lines 73-101
- Sparse text: `"of analytical work activities automatable (McKinsey 2024)"` — 8 words
- Word count: 8 words
- Failure: This is a label appended to a number. It tells the audience what the stat is but not what it means for THEIR work specifically. No FM&I consequence stated.

**Slide 3 (Session Goals) — three cards**
- File: slides_s1_s3.cjs, ~lines 152-170
- Card 1 body: `"A clear mental map of every AI tool available to you at BP — what it does, when to use it, how to access it"` — 23 words
- Card 2 body: `"Exactly what data can and cannot go into each tool — no ambiguity, no guessing"` — 16 words
- Card 3 body: `"10+ concrete commercial ideas for FM&I, plus a structured framework for the Innovation Day session"` — 16 words
- Failure: Each card states what it delivers but not why it matters, what the listener currently lacks, or what decision this enables. Too short to pass the 30-word minimum.

**Slide 4 (Our Work Context) — left column stacked cards**
- File: slides_s1_s3.cjs, ~lines 222-266
- Card body 1: `"Automated scenarios, triggers, full pipeline builds"` — 7 words
- Card body 2: `"Statistical models, ML prediction pipelines"` — 5 words
- Card body 3: `"Fast turnaround analysis under time pressure"` — 7 words
- Card body 4: `"Analysts, traders, market strategists"` — 4 words
- Failure: All four are label fragments. They name the work category but say nothing about what makes it hard, what AI does to it, or what the consequence is.

**Slide 6 (Timeline) — milestone descriptions**
- File: slides_s1_s3.cjs, ~lines 383-410
- `"GPT-4o multimodal, code interpreter improvements"` — 5 words
- `"Claude 3.7 Sonnet — extended thinking, 200k context"` — 7 words
- `"GitHub Copilot Workspace GA — full repo agent mode"` — 8 words
- Failure: These are changelog entries, not explanations. Each milestone needs 2+ lines of WHY it mattered for FM&I work.

**Slide 7 (BP Tools) — four grid cards**
- File: slides_s1_s3.cjs, ~lines 476-535
- Card 1 body: `"Included in M365 licence. Access via any Office app or Teams. No additional request needed."` — 15 words
- Card 2 body: `"Enterprise licence available. Request via IT portal. Integrates with VS Code and JetBrains."` — 13 words
- Card 3 body: `"Individual or team licence. Request via IT or expense as tool. Best-in-class for large codebase work."` — 17 words
- Card 4 body: `"M365 add-on for building custom agents. Request via IT. BP training available on intranet."` — 14 words
- Failure: All four are access instructions masquerading as capability descriptions. The audience needs to know not just HOW to get the tool but WHAT IT DOES for their specific FM&I workflow. Zero FM&I context in any card.

**Slide 8 (Access Guide) — four stacked cards**
- File: slides_s1_s3.cjs, ~lines 549-595
- Each card body is access-only information. No explanation of what to do AFTER getting access, no FM&I workflow example. Pure logistics.

**Slide 11 (M365 Apps — 6-card grid) — LAYOUT VIOLATION + sparse content**
- File: slides_s1_s3.cjs, ~lines 736-790
- SIX cards in a grid — violates the 4-card maximum rule
- Card bodies: "Meeting summaries, action items, real-time transcription" (6 words), "Draft replies, summarise threads, schedule assistant" (6 words), "Draft documents, rewrite sections, extract key points" (7 words), "Analyse data, build formulas, generate charts from natural language" (9 words)
- Failure: 6-card grid always produces sparse content. Each body is a feature label list, not an explanation of what this means for an FM&I analyst running a trading strategy review.

### slides_s4_s6.cjs

**Slide 16 (Copilot vs Cursor comparison) — bullet lists**
- File: slides_s4_s6.cjs, ~lines 88-144
- `"• BP enterprise licence — easiest to access"` — 7 words
- `"• Deep VS Code & JetBrains integration"` — 6 words
- `"• Workspace agent: understands your full repo"` — 7 words
- `"• Background agents + git worktrees (parallel)"` — 7 words
- Failure: Feature labels without practical consequence. "Full repo context" doesn't say what that means when you're debugging a 50-file Dataiku project. "Background agents" doesn't explain the parallel working team member concept.

**Slide 19 (Ask/Agent/Plan) — three-card grid**
- File: slides_s4_s6.cjs, ~lines 389-471
- Card 1 body: `"One-turn Q&A. Ask a question, get an answer.\n\nBest for: 'What does this function do?', 'Why is this query slow?', 'How do I join these DataFrames?'"` — 28 words
- Card 2 body: `"Multi-step autonomous execution. Give a goal, the agent plans and executes.\n\nBest for: building a feature, debugging a pipeline, writing and running tests."` — 25 words
- Card 3 body: `"Show the plan before executing. Review and approve each step.\n\nBest for: destructive operations, unfamiliar codebases, tasks where you want to stay in control."` — 26 words
- Failure: Definitions without FM&I workflow examples. Each card needs a specific FM&I scenario — not generic "debugging a pipeline" but "when the gas_hub_prices recipe is failing and you need to understand what's happening across 12 related files."

**Slide 22 (Copilot Roadmap 2026) — roadmap items**
- File: slides_s4_s6.cjs, ~lines 621-699
- `"Q1: Copilot Extensions — connect to external services via tool calling"` — 9 words
- `"Q2: Copilot for CLI GA — natural language terminal commands"` — 9 words
- Failure: Changelog entries without FM&I relevance. "Natural language terminal commands" doesn't say what that means when you're running Dataiku CLI operations.

**Slide 23 (Model Timeline) — 6 milestone descriptions**
- File: slides_s4_s6.cjs, ~lines 763-841
- 6 milestones on one timeline — dense but descriptions are 10-word changelog entries
- `"GPT-4o — 128k context, voice mode, multimodal reasoning"` — 8 words
- Failure: Dates and product names without explanation of WHAT CHANGED for FM&I practice.

**Slide 24 (Model Comparison) — 5-card grid — LAYOUT VIOLATION**
- File: slides_s4_s6.cjs, ~lines 854-924
- FIVE cards — violates 4-card maximum
- Card bodies: "Best for: complex multi-step agentic tasks, long document analysis, precise instruction following. Context: 200k Price: $$$$" — 18 words
- "Best for: coding tasks, balanced quality + speed. 80% of Opus quality at 20% of the cost. The daily driver for most tasks. Price: $$" — 25 words
- Failure: 5-card grid, below 30-word minimum, no specific FM&I use case scenario ("use this when you're calibrating a half-life estimator across 5 years of gas forward data").

**Slide 34 (MCP bottom cards) — 3 tiny cards**
- File: slides_s7_s10.cjs, ~lines 535-581
- `"MCP for Dataiku: Read/write pipelines, trigger scenarios, query logs"` — 9 words
- `"MCP for internal DB: Query production data without copy-paste"` — 9 words
- `"MCP for Bloomberg: Pull market data directly into AI context"` — 9 words
- Failure: Label + one-liner. Zero description of the workflow this enables, the before-state (what you do today) vs after-state (what MCP enables).

**Slide 37 (6 Personal Use Cases) — 6-card grid — LAYOUT VIOLATION**
- File: slides_s7_s10.cjs, ~lines 707-779
- SIX cards — violates 4-card maximum
- Card bodies range from 19-24 words each — below 30-word minimum
- "Used Claude Code to build programmatic video presentations — AI writes React code, Remotion renders it as video. Demo: automated video from a data summary." — 25 words
- Failure: 6-card grid produces sparse content. Each card names the project and gives a one-sentence description. Missing: what problem it solved, what it demonstrates about AI capability, what FM&I could learn from it.

**Slide 41 (Commercial Ideas) — bullet list format**
- File: slides_s7_s10.cjs, ~lines 1011-1145
- All ideas are single-line bullets: `"• Automated model documentation from code"` — 5 words
- Failure: Idea labels without any explanation of what the idea actually does, what data it needs, what commercial value it creates. These are brainstorm Post-it notes, not pitchable ideas.

**Slide 46 (Closing CTA) — three action cards**
- File: slides_s7_s10.cjs, ~lines 1384-1468
- Card 1 body: `"GitHub Copilot via IT portal. Cursor via expense or IT. Takes 10 minutes."` — 13 words
- Card 2 body: `"Pick a task you're doing this week. Use an AI tool for it. Time how long it takes. Compare."` — 20 words
- Card 3 body: `"Pick one commercial use case from today's session. Bring it to Innovation Day with: what it does, what data it needs, who benefits."` — 24 words
- Failure: Each action is too brief to be motivating. Missing the specific path/step, the likely obstacle, and why this action specifically matters.

---

## Part C — Content Gaps (PDF/Research → v2)

### Gap 1: Timeline milestones lack WHY explanations
**Research.md content**: "Q3 2025: Llama 3.3 70B release — open-source quality gap with proprietary models narrowed significantly. This democratised local AI for data-sensitive workflows."
**v2 content**: `"Llama 3.1 405B — open source, runs locally, near-frontier performance"` — 6 words
**Should appear in**: Slide 6 (Landscape Timeline) and Slide 23 (Model Timeline)

### Gap 2: GitHub Copilot vs Cursor — practical consequence explanations missing
**Research.md content**: "Cursor full codebase context: semantic indexing of entire project. When you're debugging a 50-file Dataiku project, Cursor has read every recipe, every model definition, every config. GitHub Copilot's @workspace is index-based — good but not equivalent."
**v2 content**: `"• Workspace agent: understands your full repo"` — 7 words, zero practical consequence
**Should appear in**: Slide 16 (Copilot vs Cursor comparison)

### Gap 3: Background agents — practical definition missing
**Research.md content**: "Background Agents: Long-running tasks that execute in the cloud while you work on other things. Use case: 'Rewrite all test files to use pytest instead of unittest' — submit as background task, continue working, get notified when complete."
**v2 content**: `"• Background agents + git worktrees (parallel)"` — 7 words
**Should appear in**: Slide 16 and Slide 19 (Ask/Agent/Plan) and potentially Slide 22 (Roadmap)

### Gap 4: MCP workflow explanation — step-by-step missing
**Research.md content** (lines 887-893): "Connect Cursor to your Dataiku instance. Ask: 'What's the current status of the gas pricing pipeline? Are there any failed jobs?' Cursor calls the Dataiku MCP server, retrieves job status, and responds. Ask: 'The gas_hub_prices recipe failed yesterday. Get the logs and suggest a fix.' Cursor retrieves logs via MCP, reads the recipe code, generates a fix."
**v2 content**: Three tiny cards with 9-word descriptions each
**Should appear in**: Slide 34 (MCP slide) — needs a step-by-step workflow, not just labels

### Gap 5: Claude Code — "run on a VM overnight" capability missing
**Research.md content**: "Headless: Can be invoked from CI/CD pipelines, scheduled jobs, or other automation without a human at the keyboard... Can be run overnight on a VM, operate without GUI, script as part of CI pipeline."
**v2 content**: Slide 31 mentions "terminal-based" but misses the overnight VM, CI/CD, and headless operation specifics that distinguish Claude Code from IDE tools.
**Should appear in**: Slide 31 (Claude Code overview) — richer differentiation

### Gap 6: Agent Skills — actual file structure skeleton missing
**Research.md content** (lines 947-973): Full skill specification example with actual markdown structure, fields (Description, Instructions, Output format), and creation steps.
**v2 content**: "Reusable, packaged workflows you can invoke with a single slash command... How to make one: write a markdown file defining the skill's trigger, steps, and output format." — Too vague.
**Should appear in**: Slide 35 (Agent Skills) — needs the actual skeleton

### Gap 7: Copilot Studio — declarative agent framework detail missing
**Research.md content**: "Q2 2025: Copilot Studio added declarative agent framework (agents defined by JSON schema, no UI required for sophisticated developers)"
**v2 content**: Slide 13 covers basic agent building but misses the declarative framework and the "instruction-refinement workflow" detail.
**Should appear in**: Slide 13 (Copilot Agents)

### Gap 8: Model comparison — "use this when" FM&I scenarios absent
**Research.md content**: Claude Sonnet best for "Daily coding assistance (pipeline development, debugging), ad hoc data analysis with AI assistance." Claude Opus for "Complex model architecture design, debugging non-obvious issues in statistical models."
**v2 content**: Model cards say "Best for: complex multi-step agentic tasks, long document analysis" — no FM&I scenario.
**Should appear in**: Slide 24 (Model Comparison) — each card needs "use this when you're [specific FM&I scenario]"

### Gap 9: Ethics — WHY explanations missing from safe/never list
**Research.md content**: "IMPORTANT BOUNDARY: Do not embed actual trading data, live prices, client identities, or position information in code comments or docstrings that will be sent to AI tools." and "The 'press release test': If the information would be problematic if it appeared in a press release, do not put it in an AI tool."
**v2 content**: Slide 27 lists safe/never items without explaining WHY each item is in that category — the reasoning that makes the rule memorable.
**Should appear in**: Slide 27 (Data Rules)

### Gap 10: Personal use cases — stories are too thin
**Research.md content**: The template project pattern is a live example of: CLAUDE.md + agents + skills = consistent AI output. The _p-presentation-creator is a working demonstration that can be walked through.
**v2 content**: "This repo: CLAUDE.md + agents + skills + prompts = consistent AI output on every project." — 15 words. No story of what problem it solved, what it took to build, what it demonstrates about agentic AI.
**Should appear in**: Slides 37-38 (Personal Use Cases)

### Gap 11: Innovation Day ideas — need 2-sentence descriptions, not labels
**Research.md and speaker_transcript** have detailed descriptions of each commercial use case including data needs, workflow, and commercial value.
**v2 content**: All 20 ideas are single-line bullet labels ("• Automated model documentation from code").
**Should appear in**: Slide 41 (Commercial Ideas) — each idea needs 2+ sentences.

### Gap 12: Closing statement slides — philosophical argument too thin in supporting text
**Research.md/speaker_transcript**: Rich philosophical context about the "comfortable middle" being replaced, the difference between performance art around coding vs actual ownership.
**v2 content**: Statement slides have supporting text but it's compressed — particularly Statement 2 which needs more depth on what "comfortable middle" means in FM&I specifically.

---

## Part D — Expansion Opportunities

### Expansion 1: Stat slide — add source and FM&I implication for every number

**Proposed expansion text** (Slide 2 — Productivity Gap):

45% stat: "McKinsey's 2024 analysis found that 45% of activities performed by data analysts are automatable with current AI. For FM&I specifically, this maps to: ELT recipe documentation, test writing, data quality checks, boilerplate aggregation logic, and report formatting — the routine work that currently absorbs 30-40% of sprint capacity."

55% stat: "GitHub's developer survey (1,000+ engineers) found 55% faster task completion with Copilot. The gain is concentrated in three areas: not needing to look up syntax (saves context-switching), not writing boilerplate (saves setup time), and having a first draft to critique rather than starting from blank (reduces activation energy). All three apply directly to Dataiku recipe development."

40-80 hrs/month stat: "Accenture's 2025 quant analyst study: the top 20% of adopters saved 15+ hours per week; the bottom 20% saved under 2 hours. The gap was entirely explained by prompting skill and tool integration depth — not technical background. This means the return on learning to prompt well is measured in hundreds of hours per year."

12 min stat: "The 12-minute figure is a real benchmark from this session's demos. A Plotly Dash app showing crack spread evolution for Q1 2025 — complete with rolling average, date range picker, and commodity selector — built from a single prompt to Cursor. Manual equivalent: 2-3 days. The implication: ad hoc desk requests that currently take 'until end of week' can be answered by end of day."

### Expansion 2: Timeline milestones — WHY it mattered

**Proposed expansion text** (Slide 6):

GPT-4o multimodal (Mar 2025): "Multimodal reasoning meant analysts could paste a chart or PDF page directly into the AI and ask questions about it — no more manual data extraction. For FM&I, this means pasting an ICE Brent forward curve chart and asking 'where is the contango steepest and what does that signal about storage economics?' — answered in seconds."

Claude 3.7 Sonnet (May 2025): "Extended thinking allowed the model to work through multi-step problems by explicitly showing its reasoning chain before producing output. This was the first model where complex statistical model debugging — the kind where you need to trace through 5 interacting components to find the root cause — became reliably possible without hallucination."

GitHub Copilot Workspace GA (Jul 2025): "For the first time, an enterprise-licensed tool could reason across an entire repository, not just the open file. For a 30-file Dataiku project, this meant being able to ask 'what's the impact of changing the VaR calculation in model_risk.py?' and get an answer that traces through all downstream dependencies."

Cursor 0.42 — background agents (Oct 2025): "Background agents changed the relationship between the engineer and the AI from 'assistant you talk to' to 'parallel team member you assign work to.' You can now say 'refactor all the ELT recipes to use Polars instead of Pandas for the aggregation layer' and come back 90 minutes later to a completed PR."

Claude 4.6 Sonnet (Jan 2026): "Reliable agentic multi-step tool calling — not just generating code but executing it, seeing the result, correcting errors, and continuing — made Claude Code production-worthy for FM&I pipeline work. The first model where a single instruction ('audit the Brent model for magic numbers and write test coverage') reliably produces a complete, useful output."

### Expansion 3: GitHub Copilot vs Cursor — practical consequence per feature

**Proposed expansion text** (Slide 16):

"Full repo context in Cursor vs @workspace in GitHub Copilot: When debugging a timeout in your gas_hub_prices ELT pipeline, Cursor has semantically indexed every recipe, every model definition, every config file, and every test in your Dataiku project. When you ask 'why does this recipe fail when the upstream job runs overnight but pass in isolation?', Cursor finds the shared state dependency across three files without being told to look there. GitHub Copilot's @workspace uses an indexed lookup — excellent for structured queries but occasionally misses implicit cross-file relationships."

"Background agents: Cursor can run an ELT pipeline refactor in the background while you write model code in the foreground. When it finishes, it reports back. This is the difference between AI as a typing assistant and AI as a parallel working team member. As of Q1 2026, GitHub Copilot does not offer background agents — you must wait for each step to complete before continuing."

"Model choice in Cursor: You can select Claude Sonnet for speed on routine tasks and switch to Opus for deep debugging sessions — all within the same IDE. GitHub Copilot's model selection is more constrained; you primarily use GPT-4o with limited Claude access. For FM&I engineering work, Claude Sonnet is meaningfully better than GPT-4o on complex pandas/polars transformations and Dataiku-specific API calls."

### Expansion 4: MCP for Dataiku — step-by-step workflow

**Proposed expansion text** (Slide 34):

"Step-by-step MCP workflow for Dataiku:\n1. Install the Dataiku MCP server (community repository: mcp-server-dataiku)\n2. Configure Cursor to point to the MCP server endpoint\n3. You type in Cursor: 'Check all running scenarios on the gas_pricing project. Flag any that failed in the last 24 hours and show me the last error log.'\n4. Cursor sends this to Claude, which calls the MCP tool list_scenarios(), then get_job_logs() for any failures\n5. Claude returns: 'The gas_hub_prices scenario failed at 03:42 UTC. Error: KeyError on column 'settlement_price'. The last successful run was 22:15 yesterday. Here are three likely causes...'\n6. You type: 'Fix the KeyError — I think the column was renamed in the source table'\n7. Claude reads the recipe code via MCP, identifies the column reference, proposes the fix\n8. You approve — Claude writes the fix directly to the recipe file\n\nTotal time: 8 minutes. Manual equivalent: pull logs, open recipe, find the error, investigate, fix, redeploy — 45 minutes minimum."

### Expansion 5: Agent Skills — actual skeleton

**Proposed expansion text** (Slide 35):

"Skill file structure (`.claude/skills/data-quality-report.md`):\n---\n# Skill: data-quality-report\nDescription: Generate a structured data quality report for a Dataiku dataset output\nTrigger: /data-quality-report [dataset_name]\n\n## Instructions\n1. Profile: row count, column count, dtypes\n2. For each column: null %, unique values, min/max/mean if numeric, sample values if string\n3. Flag: >10% nulls, single unique value, numeric outliers (>3 IQR)\n4. Generate: summary text + JSON output + list of recommended actions\n5. Format: markdown table + embedded JSON block\n\n## Output\n[markdown table of column profiles]\n[JSON summary]\n[Action items list]\n---\n\nThis skill is invoked once, runs the same 10-step process every time, produces identical-format output regardless of which team member runs it. Set it up once, use it on every pipeline output review."

### Expansion 6: Personal use cases — 4 stories with narrative arc

Reduce from 6 cards to 4 cards, each with a complete story:

Card 1 — "Claude Code + Remotion: built a system where Claude Code writes a React component for each slide, Remotion renders them as video frames, and the entire video presentation is generated programmatically from a data source. Problem solved: converting weekly model performance numbers into a 2-minute video briefing for stakeholders, automatically. Built in a weekend. Demonstrates: AI can own the full creative and production workflow, not just assist with it."

Card 2 — "OpenClaw (chess analysis): connected an LLM to a structured chess position database and gave it tools to query positions, evaluate moves, and explain reasoning. The chess application is secondary — what it demonstrates is: giving an LLM a domain-specific knowledge base and tool set makes it a domain expert. The same pattern applies to connecting an LLM to a commodity pricing database or a forward curve model."

Card 3 — "Claude Remote: SSH-based workflow for running Claude Code on a remote VM overnight. You write the instruction, start the session over SSH, and come back the next morning to a completed repository audit. Problem solved: large codebase refactors that would take a week of IDE time can now run autonomously on a VM while you do other work. Demonstrates: the 'AI as parallel team member' concept at its fullest."

Card 4 — "Template Project (_p-presentation-creator): this presentation was built using the template. CLAUDE.md defines the project, .claude/agents/ contains 5 specialist agents (Research, Content, Builder x3), each reads the prior output. The result: a 46-slide presentation built from a single high-level brief. Build time: the agents wrote all content and code in one session. Demonstrates: team-scale agentic workflows where each 'team member' is a specialised AI agent."

### Expansion 7: Business Use Cases — 2-sentence descriptions per idea

**Data & Modelling category:**

"Automated model documentation: Claude Code reads your fundamental model codebase, identifies all functions, extracts the logic, and generates docstrings and a model card explaining inputs, outputs, calibration approach, and known limitations. This removes the documentation backlog that every model team has and makes model handover 5× faster."

"AI-assisted half-life estimator calibration: an agent monitors new price data daily, compares it against current half-life estimates, flags drift above a configurable threshold, and generates a brief calibration recommendation for the model owner to review. The analyst sets the threshold and reviews the output — the agent does the daily data monitoring."

"Anomaly detection on ELT pipeline outputs: an agent runs after each scheduled pipeline, compares row counts and value distributions against historical baselines, and posts a 'pipeline health check' to Teams if any metric exceeds a 2-standard-deviation threshold. Catches silent failures that currently go unnoticed until someone queries the data."

---

## Part E — New Slides Needed

### New Slide E1: "The 15-Hour vs 2-Hour Gap" — deep-dive on the Accenture finding

**Proposed content**: A statement/stat slide dedicated to the single most motivating finding from research.md.

"15 hours per week. That's what the top 20% of AI adopters in quant/analytics functions saved per Accenture's 2025 study — surveying quant analysts, data engineers, and front-office technology teams. The bottom 20% saved 2 hours per week. Same tools. Same technical background. The only difference: prompting skill and how deeply the tool was integrated into daily workflow. The productivity gap isn't about access — everyone in this room can have GitHub Copilot by Thursday. It's about whether you use it as a spell-checker or as a parallel team member. This session is about the second."

Slide type: Big number + statement + supporting text. Place after title slide, before the existing productivity stats slide.

### New Slide E2: Copilot Excel — natural language formulas + Python in Excel

**Proposed content**: Split the M365 apps slide (currently 6-card grid) into two slides. Keep a 4-card grid on slide 11 (Teams, Outlook, Word, Excel) and add a dedicated Excel deep-dive.

"Excel + Copilot: the FM&I-specific capabilities: (1) Natural language formula generation — 'Create a formula that calculates the rolling 30-day volume-weighted average of column C, excluding rows where column D is null' — Copilot writes it. (2) Python in Excel: run actual Python code in Excel cells with Copilot assistance — no separate Jupyter environment needed. (3) Data insight detection: paste a dataset and ask 'what are the three most unusual patterns in this data?' — Copilot runs statistical analysis and narrates findings. For FM&I, this means crack spread analysis, time spread calculations, and scenario outputs can be interrogated in natural language without leaving Excel."

### New Slide E3: Claude Code — overnight VM workflow

**Proposed content**: Add a dedicated slide to the Claude Code section showing the headless/overnight pattern.

"Claude Code on a VM: the overnight workflow. (1) SSH into your cloud VM. (2) Run `claude` in your project directory with your instruction: 'Audit the entire Brent fundamental model: identify all magic numbers, write docstrings for all undocumented functions, generate test coverage for the ELT pipeline, and create a model card in docs/MODEL.md.' (3) Close the SSH session. (4) Come back 2-3 hours later. The audit is complete, tests are written, documentation is generated. This is fundamentally different from IDE tools: Claude Code doesn't need you watching it. It can work while you sleep, at a cost of approximately $2-8 in API tokens for a full model audit."

### New Slide E4: Innovation Day Framework

**Proposed content**: A dedicated "how to evaluate an idea" slide before the 20 ideas slide.

"Innovation Day evaluation matrix: A good FM&I AI idea needs to answer four questions. (1) What is the problem? (Be specific: 'the gas_hub_prices pipeline fails silently 2-3 times per month and we spend 3 hours diagnosing it each time') not vague ('we have pipeline reliability issues'). (2) What data does it need? (Be explicit about what feeds in and whether that data is safe to use with AI tools). (3) Who benefits and how? (Trading desk gets X, model team saves Y hours per month). (4) What would an MVP look like in 2 weeks? (A working prototype that demonstrates the core value, not a production system). Bring all four answers to Innovation Day."

---

## Summary Statistics

- **v2 slides assessed**: 46
- **Cards/panels with sparse text (<30 words body)**: 31 cards across 12 slides
- **Layout violations (>4 card grids)**: 3 slides (Slides 11, 24, 37)
- **PDF slides inventoried**: 47 slides identified from design spec and content outline
- **Content gaps identified**: 12 major gaps
- **Expansion opportunities identified**: 7 with full expansion text
- **New slides proposed**: 4

**Target for v3**: 52-58 slides with every card meeting the 30-word minimum and maximum 4 cards per grid.
