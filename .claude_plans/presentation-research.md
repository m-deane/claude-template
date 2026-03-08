# Presentation Research: How AI Tools Are Transforming Software Development

**Audience**: Software engineering teams and tech leadership (engineering managers, tech leads, senior developers)
**Purpose**: Educate and inspire strategic adoption of AI tools in development workflows
**Duration**: 15 minutes (~12-15 slides)
**Tone**: Professional, data-driven, honest about trade-offs

---

## 1. Core Message

> AI coding tools are not optional upgrades — they are a structural shift in how software gets built, and the teams that learn to use them with discipline will outpace those that do not.

---

## 2. Audience Profile

**Knowledge level**: High. This audience writes and reviews code daily. They will not be impressed by vague claims or vendor marketing language. They have tried at least one AI coding tool, formed opinions, and have specific objections.

**Concerns**:
- Code quality regression and accumulation of technical debt
- Security vulnerabilities in AI-generated code (48% of AI-generated code contains potential vulnerabilities per industry research)
- Loss of deep domain understanding if junior developers over-rely on AI
- Trust gaps: only 3% of developers highly trust AI-generated code without review
- Job security, though 70% of professional developers say AI is not a threat to their job (Stack Overflow 2024)

**Motivations**:
- Stay competitive — they see peers and competing teams shipping faster
- Reduce toil and reclaim time for higher-order design and architecture problems
- Demonstrate measurable productivity gains to leadership
- Build a defensible strategy rather than reacting ad hoc to new tools

**What will resonate**: Honest data, acknowledged nuance, concrete workflows, and peer-validated patterns. This audience will reject cheerleading. They respond to specificity, rigor, and admission of failure cases.

---

## 3. Narrative Arc (Minto Pyramid — Situation / Complication / Resolution)

**Situation**: Software engineering teams are under sustained pressure to ship more, faster, with smaller margins for error. The talent market is tight, codebases are growing in complexity, and business expectations have not softened.

**Complication**: A new class of AI tools has arrived that can materially accelerate development — but adoption without strategy is producing mixed and sometimes negative results. Teams report productivity gains AND increased bug rates AND rising technical debt. The tools are real; the discipline to use them well is not yet standard practice.

**Resolution**: Teams that treat AI adoption as a craft — with deliberate workflow integration, clear human oversight patterns, and honest measurement — are seeing durable, compounding gains. The question is not whether to adopt AI tools; it is how to do it in a way that improves quality and velocity together.

---

## 4. Opening Hook

**Option A — Provocative statistic**:
> "In 2022, GitHub Copilot wrote 27% of accepted code for active users. By early 2025, that number was 46%. In the time it takes to run a sprint retrospective, nearly half your team's new code may already be AI-generated — the only question is whether your team has a policy for it."

**Option B — Scenario**:
> "Picture two teams given the same feature request on Monday morning. Team A opens their IDE and starts typing. Team B opens their IDE and does the same — except every developer has an AI assistant that writes boilerplate, suggests test cases, flags security patterns, and summarizes PR diffs. By Friday, Team B has closed 26% more tasks. Six months later, Team A is hiring faster just to keep pace. This is not a thought experiment. It is what the data now shows."

**Recommended**: Option A as an opener (jarring, data-grounded), pivot into Option B as a story to make it concrete.

---

## 5. Three Core Pillars (Rule of Three)

---

### Pillar 1: The Productivity Shift Is Real — and Larger Than Most Teams Realize

**Assertion**: AI coding tools have moved past hype into measurable, reproducible productivity gains that are reshaping how fast software can be shipped.

**Evidence**:
- GitHub's controlled study with Accenture across 4,800 developers: tasks completed **55% faster** with Copilot (1h 11m vs. 2h 41m for the same JavaScript task).
- Pull request cycle time dropped from **9.6 days to 2.4 days** — a 75% reduction — in teams that integrated AI throughout the review process.
- Developers complete **26% more weekly tasks** with AI assistance (study of 4,867 software developers).
- GitHub Copilot grew from 3.8M to **20M users** in under three years. **Fortune 100 companies show a 90% adoption rate**, indicating Copilot has moved from pilot to standard infrastructure.
- Gartner forecasts **90% of enterprise software engineers** will use AI coding assistants by 2028, up from less than 14% in early 2024.
- McKinsey: documenting code takes **half the time**; code optimization and refactoring takes **two-thirds the time**.
- Developer happiness is a real metric: **95% of Copilot users report enjoying coding more**; developers using AI are **more than twice as likely** to report being in a flow state (McKinsey).

**Nuance to acknowledge**: Productivity gains are not instant. Research shows it takes approximately **11 weeks** before developers fully internalize the workflow shift. Organizations must account for an adjustment period.

**Transition**: The gains are real, but they do not arrive for free. The second thing any team adopting AI must understand is where the risks concentrate — and what to do about them.

---

### Pillar 2: The Risks Are Specific and Manageable — If You Plan for Them

**Assertion**: AI coding tools introduce a predictable set of risks that, if left unmanaged, erode the productivity gains they create. The teams winning with AI are the ones who built explicit countermeasures.

**Evidence**:
- **48% of AI-generated code** contains potential security vulnerabilities (industry research). Enterprises using AI coding assistants report **10,000+ new security findings per month** attributable to AI-generated code.
- GitClear analyzed **211 million changed lines of code** from 2020–2024 and found that copy-pasted code rose from **8.3% to 12.3%**, while refactoring activity sank from **25% to less than 10%** — a clear signal of accumulating technical debt.
- The 2024 DORA report (3,000 respondents) found that a 25% increase in AI adoption correlates with a **1.5% decrease in throughput** and a **7.2% decrease in delivery stability** — because AI makes it easier to ship larger changesets, and larger changesets introduce more risk.
- **40% of developers** say AI has increased technical debt by creating unnecessary or duplicative code.
- Trust collapse: AI trust among developers fell from 42% in 2024 to **33% in 2025** (Stack Overflow), with senior engineers most skeptical. Only **3% of developers** highly trust AI-generated code without manual review.
- **67% of developers spend more time debugging AI-generated code** due to fast but shallow code generation.

**The countermeasures that work**:
1. Treat AI-generated code as a draft, not a delivery. 71% of developers already refuse to merge without manual review — make that policy explicit.
2. Shrink batch sizes deliberately when using AI tools, directly countering the stability risk the DORA data identifies.
3. Mandate security scanning for AI-generated code as a CI/CD gate, not an afterthought.
4. Track technical debt metrics alongside velocity metrics — do not measure AI adoption by lines generated.

**Transition**: The teams that manage these risks do not abandon AI — they double down, because they have built the governance to extract compounding value. That brings us to the third and most important pillar: what it looks like when teams do this well.

---

### Pillar 3: The Strategic Edge Goes to Teams That Integrate AI Across the Entire SDLC

**Assertion**: The biggest competitive advantage does not come from adding AI to a single task (code completion). It comes from embedding AI across planning, code generation, testing, review, and deployment — and from preparing now for the agentic AI wave arriving in 2025-2026.

**Evidence**:
- McKinsey: top-performing AI teams are **six to seven times more likely** to scale to four or more AI use cases simultaneously. Organizations using AI in four or more SDLC phases see software quality improvements of **31–45%** and time-to-market improvements of **16–30%**.
- Current top use cases (2025 survey data): code generation (72.2%), documentation generation (67.1%), code review/optimization (67.1%), automated testing and debugging (55.7%).
- **21% of Google's code** is now AI-assisted — one of the largest documented enterprise-scale deployments.
- Platform engineering amplifier: teams using internal developer platforms see a **10% increase in team performance** and 8% productivity boost (2024 DORA report).
- The agentic AI frontier: IBM and Morning Consult surveyed 1,000 developers building AI applications — **99% are exploring or actively developing AI agents** for their workflows. Anthropic's 2026 Agentic Coding Trends Report confirms multi-agent architectures are moving from research into production engineering workflows.
- Market signal: Enterprise AI spending surged from **$11.5B in 2024 to $37B in 2025** — a 3.2x jump in a single year. The AI coding assistant market alone is projected to reach **$97.9B by 2030** at a 24.8% CAGR.
- ROI for structured adopters: companies with well-developed AI initiatives grow revenue **2.5x faster** and productivity **2.4x higher** than non-adopters (IDC). Top performers report **$10.30 return per dollar invested** in AI.

**The emerging model — the developer as orchestrator**: McKinsey now predicts that in the near term, individual contributors will spend part of their time as "engineering managers directing a junior team of asynchronous agents." The skill set is shifting from pure implementation toward specification, architecture, and quality oversight.

---

## 6. Closing with Call to Action

**Bridge statement**: "We are not at the end of this shift. We are at the beginning of it. The teams that will look back on 2025–2026 as a turning point are the ones that started building structured, disciplined AI-augmented workflows now — not the ones that waited for the tools to mature further."

**CTA — Three actions, each with an owner and a time horizon**:

1. **This week (Individual)**: Instrument your workflow. Pick one task category — boilerplate generation, test case writing, or PR summaries — and run a deliberate two-week experiment with an AI tool. Measure before and after.

2. **This sprint (Team)**: Establish your team's AI policy. Document three things: which AI tools are approved, what the mandatory human review standard is, and how security scanning is applied to AI-generated code. This takes one hour and prevents six months of inconsistency.

3. **This quarter (Leadership)**: Commission a measurement baseline. You cannot manage what you do not measure. Track deployment frequency, change failure rate, and code review cycle time before and after structured AI adoption. Make the data visible to the team.

---

## 7. Slide-by-Slide Content Outline

---

### Slide 1 — Title Slide
**Type**: Title
**Title**: "The AI-Augmented Team: How Artificial Intelligence Is Transforming Software Development"
**Subtitle**: What the data actually shows — and what your team should do about it
**Visual**: Minimal. Dark background, clean typography. Optional: a subtle visualization of a code diff with AI suggestions highlighted.
**Speaker notes**: Introduce yourself and the framing: this will be data-driven, honest about trade-offs, and will close with three concrete actions. Tell the audience upfront that you will not be selling them on AI hype — you are going to show them the actual research.

---

### Slide 2 — The Opening Provocation
**Type**: Stat (full-bleed number)
**Title**: "46% of Code Written by Active GitHub Copilot Users Is Now AI-Generated"
**Key message**: The shift is already happening at scale — in your codebase and every codebase around you.
**Supporting data**:
- 2022: 27% of accepted code was AI-generated (Copilot launch)
- 2025: 46% of accepted code is AI-generated
- 20 million Copilot users as of mid-2025; 90% Fortune 100 adoption rate
**Visual**: Large typographic treatment of "46%" anchoring the slide. Small timeline showing 27% (2022) → 46% (2025).
**Speaker notes**: Let the number land. Then ask the audience: "Does your team have a deliberate policy for this, or are you absorbing it informally?" This is not a rhetorical trick — it is a genuine diagnosis question. Most teams have no formal policy.

---

### Slide 3 — Situation: The Pressure Engineering Teams Are Under
**Type**: Split (two columns)
**Title**: "The Compounding Pressures on Engineering Teams"
**Key message**: Teams are being asked to do more with the same or fewer resources. This is the context in which AI tools land.
**Left column — headwinds**:
- Codebase complexity increasing year over year
- Tight developer labor market
- Business expectations: faster releases, higher quality, lower cost
**Right column — what teams actually have**:
- Same sprint cadence
- Burnout risk rising
- Tech debt accumulating
**Visual**: Simple two-column layout with icons. No clip art — use minimal geometric icons.
**Speaker notes**: This is not doom and gloom — it is honest context. AI tools did not arrive in a vacuum. They arrived because there is genuine demand for ways to do more with the same engineering headcount. That matters for how we evaluate them.

---

### Slide 4 — Complication: Adoption Without Strategy Is Producing Mixed Results
**Type**: Stat or comparison
**Title**: "The Gap Between Adoption and Impact"
**Key message**: 76% of developers use or plan to use AI tools — but only 47% of IT leaders say their AI projects were profitable in 2024.
**Supporting data**:
- Stack Overflow 2024: 76% using or planning to use AI tools; 62% actively using
- IDC/McKinsey: only 6% of organizations qualify as AI "high performers" (5%+ EBIT impact)
- 70–85% of AI initiatives fail to meet expected outcomes
- DORA 2024: 25% increase in AI adoption correlates with 7.2% decrease in delivery stability
**Visual**: A simple divergence chart — adoption curve trending up steeply, "realized impact" curve trending up gradually, with a visible gap between them labeled "the strategy gap."
**Speaker notes**: This is the complication. The tools work — the research is consistent on that. But unstructured adoption is producing a pattern where teams ship more code and accumulate more risk simultaneously. The gap is not a tools problem. It is a process problem.

---

### Slide 5 — Section Divider: Pillar 1
**Type**: Section divider
**Title**: "Pillar 1: The Productivity Gains Are Real"
**Subtitle**: What controlled research actually shows
**Visual**: Clean section divider. Large "01" numeral. Minimal text.
**Speaker notes**: Brief orientation — tell the audience this section covers the productivity evidence, and you will be specific about the methodology behind the numbers, not just the headline figures.

---

### Slide 6 — The Productivity Evidence
**Type**: Chart / data-dense
**Title**: "Controlled Research: What AI Tools Do to Development Speed"
**Key message**: Multiple independent studies converge on a consistent range of productivity gains across different task types.
**Supporting data (cite sources explicitly on slide)**:
- GitHub + Accenture (4,800 developers): **55% faster** task completion with Copilot
- McKinsey: Code documentation **2x faster**; refactoring tasks completed in **~65% of previous time**
- 4,867-developer study: **26% more weekly tasks** completed
- PR cycle time: **9.6 days → 2.4 days** (75% reduction) with AI-assisted review
- McKinsey top performers: software quality improvements **31–45%**, time-to-market improvements **16–30%**
**Visual**: Horizontal bar chart comparing "without AI" vs. "with AI" across 4–5 task categories (task completion, PR cycle time, documentation time, code optimization). Use a consistent color pair.
**Speaker notes**: Walk through each bar. Emphasize that these are controlled studies with comparison groups — not vendor marketing. Point out that the gains are not uniform: the biggest gains are in boilerplate, documentation, and test generation. Design and architecture work shows much smaller gains.

---

### Slide 7 — Developer Experience Is a Business Metric
**Type**: Icons / stat grid
**Title**: "AI Tools Are Changing How Developers Feel About Their Work"
**Key message**: Developer satisfaction and flow state are not soft metrics — they predict retention, quality, and long-term velocity.
**Supporting data**:
- 95% of Copilot users report enjoying coding more
- Developers using AI tools are **2x more likely** to report flow state (McKinsey)
- 60% of developers report increased job satisfaction
- 87% say AI helps preserve mental effort during repetitive tasks
- 73% say AI helps them stay in flow
**Visual**: 3x2 grid of large percentages with single-line labels. Clean, minimal.
**Speaker notes**: This matters to engineering leaders for a specific reason: burnout from repetitive low-cognition work is a documented cause of attrition. If AI tools reduce that toil, the compounding benefit is retention — and retention in senior engineers is worth more than any productivity percentage point.

---

### Slide 8 — Section Divider: Pillar 2
**Type**: Section divider
**Title**: "Pillar 2: The Risks Are Specific and Manageable"
**Subtitle**: What to watch for — and what to do about it
**Visual**: Clean section divider. Large "02" numeral.
**Speaker notes**: Tell the audience this is the section you would most want them to take notes on, because it is the part that most teams skip when they read the productivity headlines.

---

### Slide 9 — The Risk Map
**Type**: Comparison or four-quadrant layout
**Title**: "Where AI-Generated Code Introduces Risk"
**Key message**: Three distinct risk categories — security, technical debt, and delivery stability — each has documented evidence and a direct countermeasure.
**Supporting data**:

Security risk:
- 48% of AI-generated code contains potential security vulnerabilities
- Enterprises report 10,000+ new security findings/month from AI-generated code
- Countermeasure: mandatory security scanning as a CI/CD gate

Technical debt risk:
- GitClear (211M lines of code, 2020–2024): copy-paste code up from 8.3% to 12.3%; refactoring activity down from 25% to under 10%
- 40% of developers say AI has increased technical debt
- Countermeasure: track debt metrics alongside velocity; mandate refactoring cycles

Delivery stability risk:
- DORA 2024: 25% AI adoption increase → 7.2% delivery stability decrease
- Root cause: AI makes it easy to write larger changesets; larger changesets fail more
- Countermeasure: enforce smaller PRs as a team norm when using AI tools

**Visual**: Three-column layout. Each column: risk category name, key data point, countermeasure. Use amber/orange for the risk data points to signal caution without alarm.
**Speaker notes**: Do not let this slide generate fatalism. The point is that these risks are well-characterized and each has a known engineering response. This is very different from risks that are unknown or unpredictable.

---

### Slide 10 — The Trust Gap and What It Tells Us
**Type**: Timeline or trend line
**Title**: "Developer Trust in AI Is Falling — That Is Actually a Good Sign"
**Key message**: Declining trust reflects maturity, not failure. The teams performing best are the ones with structured skepticism — not naive adoption or total rejection.
**Supporting data**:
- AI trust among developers: 42% (2024) → 33% (2025) (Stack Overflow)
- 71% of developers refuse to merge AI-generated code without manual review
- Only 3% of developers highly trust AI-generated code
- 67% spend more time debugging AI-generated code
- 39% report little to no trust (DORA 2024)
**Visual**: Simple trend line showing trust declining 2023→2025. Then a secondary annotation: "High performers maintain structured review regardless of trust level — the workflow is the protection."
**Speaker notes**: Reframe this data. A junior team that blindly trusts AI output is the team accumulating security debt. A senior team that reflexively rejects AI output is leaving 55% productivity gains on the table. The winning posture is: use the tools, distrust the output by default, verify systematically.

---

### Slide 11 — Section Divider: Pillar 3
**Type**: Section divider
**Title**: "Pillar 3: The Strategic Edge Comes From Full-SDLC Integration"
**Subtitle**: From code completion to agentic workflows
**Visual**: Clean section divider. Large "03" numeral.
**Speaker notes**: This section looks forward. The first two pillars are about the present state of AI tools. This pillar is about the 12–24 month horizon — where the real competitive differentiation will emerge.

---

### Slide 12 — The SDLC Integration Opportunity
**Type**: Timeline or horizontal flow diagram
**Title**: "AI Across the Full Software Development Lifecycle"
**Key message**: Teams limiting AI to code completion are capturing only a fraction of the available productivity gain.
**Supporting data**:
- Top 2025 use cases: code generation (72%), documentation (67%), code review (67%), testing/debugging (56%)
- McKinsey: top performers are 6-7x more likely to scale to 4+ AI use cases
- Organizations using AI across 4+ SDLC phases: software quality +31–45%, time-to-market +16–30%
- 21% of Google's code is now AI-assisted (full pipeline integration)
- Internal developer platforms + AI: +10% team performance, +8% individual productivity (DORA 2024)

**SDLC stages with AI opportunity**:
1. Planning: requirements analysis, dependency mapping, timeline forecasting
2. Code generation: completion, boilerplate, test scaffolding
3. Code review: automated PR summaries, security flagging, style enforcement
4. Testing: test case generation, regression detection, coverage analysis
5. Documentation: inline docs, changelog generation, architecture summaries
6. Deployment: anomaly detection, rollback triggers, SRE automation

**Visual**: Horizontal SDLC pipeline diagram with each stage labeled. Stages with current AI tooling highlighted; stages with emerging AI tooling shown in a lighter shade. Data callouts above the highest-impact stages.
**Speaker notes**: Walk through each stage. Point out that most teams are only active in stages 2 and 4. Ask the audience to note which stages their teams are not yet touching — those are the next opportunities.

---

### Slide 13 — The Agentic Horizon
**Type**: Quote or forward-looking visual
**Title**: "The Next Shift: From AI Assistants to AI Agents"
**Key message**: The tools are evolving from reactive (respond to prompts) to agentic (independently plan, execute, verify multi-step tasks). This is the 2025–2026 frontier.
**Supporting data**:
- IBM + Morning Consult: 99% of developers building AI applications are exploring or developing AI agents
- Anthropic 2026 Agentic Coding Trends Report: multi-agent architectures moving from research into production engineering workflows
- McKinsey forecast: individual contributors will increasingly function as "engineering managers directing a junior team of asynchronous agents"
- Enterprise AI spend: $11.5B (2024) → $37B (2025) — 3.2x YoY jump; AI coding assistant market projected at $97.9B by 2030
- Agentic AI capability: up to 60% reduction in manual workloads for repetitive development tasks

**Visual**: A simple before/after comparison. Left: "AI Assistant" — developer prompts, AI responds, developer integrates. Right: "AI Agent" — developer specifies intent, agent plans, executes, tests, and reports back. Human role: specification + oversight.
**Speaker notes**: Emphasize that this is not science fiction — it is already in early production at leading engineering orgs. The teams building governance for AI assistants today are the teams that will be ready to safely adopt agentic workflows when they mature in 2026. The teams that have not started yet will be 18 months behind.

---

### Slide 14 — What the Best Teams Do Differently
**Type**: Icons / best practices list
**Title**: "The Playbook: What High-Performing AI-Augmented Teams Have in Common"
**Key message**: The differentiator is not which AI tools a team uses — it is the discipline and structure around how they use them.
**Points**:
1. Written AI tool policy — approved tools, review standards, security gates
2. Measurement before and after — deployment frequency, change failure rate, PR cycle time
3. Small PRs enforced — to counter the batch-size risk that DORA identified
4. Security scanning as a CI/CD gate — not optional, not manual
5. Whole-SDLC adoption — not just code completion; documentation, testing, review
6. Developer autonomy within guardrails — trust the engineers to calibrate; give them the policy, not the workflow prescription
**Visual**: Six icons in a grid, each with a two-line description. Clean, professional.
**Speaker notes**: This slide is the distillation of everything in the previous slides. If someone photographs one slide from this presentation, this should be it. Ask: "How many of these six does your team have today?"

---

### Slide 15 — Call to Action
**Type**: CTA
**Title**: "Three Actions. Three Time Horizons."
**Key message**: Strategic AI adoption starts with small, deliberate steps — not a platform migration or a budget ask.
**Actions**:

This week — Individual action:
> Pick one task category. Run a two-week experiment with an AI tool. Measure before and after. Document what you learn.

This sprint — Team action:
> Write your AI tool policy. Approved tools, mandatory review standard, security scanning requirement. One hour. Prevents six months of drift.

This quarter — Leadership action:
> Establish a measurement baseline. Deployment frequency, change failure rate, PR cycle time. Make the data visible to the team.

**Visual**: Three-column layout with a clear time-horizon label at the top of each column. Simple, action-oriented. CTA slide should feel calmer than the data slides — less information, more white space.
**Speaker notes**: End on energy, not exhaustion. The point of three horizons is to make adoption feel tractable. The teams that succeed with AI do not do it all at once — they start with one disciplined experiment, build confidence, and scale from there.

---

## Research Sources

[1] GitHub Blog. "Research: quantifying GitHub Copilot's impact on developer productivity and happiness." GitHub, 2023.
https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/

[2] Second Talent. "GitHub Copilot Statistics & Adoption Trends [2025]."
https://www.secondtalent.com/resources/github-copilot-statistics/

[3] Stack Overflow. "AI | 2024 Stack Overflow Developer Survey."
https://survey.stackoverflow.co/2024/ai

[4] Stack Overflow. "AI | 2025 Stack Overflow Developer Survey."
https://survey.stackoverflow.co/2025/ai

[5] Stack Overflow Blog. "Developers remain willing but reluctant to use AI: The 2025 Developer Survey results are here." December 29, 2025.
https://stackoverflow.blog/2025/12/29/developers-remain-willing-but-reluctant-to-use-ai-the-2025-developer-survey-results-are-here/

[6] McKinsey & Company. "Unleashing Developer Productivity with Generative AI." June 2023.
https://www.mckinsey.com/capabilities/tech-and-ai/our-insights/unleashing-developer-productivity-with-generative-ai

[7] McKinsey & Company. "Unlocking the Value of AI in Software Development." November 2025.
https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/unlocking-the-value-of-ai-in-software-development

[8] DORA. "Accelerate State of DevOps Report 2024." Google Cloud, 2024.
https://dora.dev/research/2024/dora-report/

[9] DORA. "State of AI-assisted Software Development 2025." Google Cloud, 2025.
https://dora.dev/research/2025/dora-report/

[10] GitClear. "AI Copilot Code Quality: 2025 Data Suggests 4x Growth in Code Clones."
https://www.gitclear.com/ai_assistant_code_quality_2025_research

[11] Qodo. "State of AI Code Quality in 2025."
https://www.qodo.ai/reports/state-of-ai-code-quality/

[12] Menlo Ventures. "2025: The State of Generative AI in the Enterprise."
https://menlovc.com/perspective/2025-the-state-of-generative-ai-in-the-enterprise/

[13] Business Wire / Research and Markets. "Generative AI Coding Assistants Market to Reach $97.9 Billion by 2030." March 2025.
https://www.businesswire.com/news/home/20250319490646/en/

[14] Microsoft / IDC. "Generative AI Delivering Substantial ROI to Businesses." January 2025.
https://news.microsoft.com/en-xm/2025/01/14/generative-ai-delivering-substantial-roi-to-businesses-integrating-the-technology-across-operations-microsoft-sponsored-idc-report/

[15] Anthropic. "2026 Agentic Coding Trends Report."
https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf

[16] Index.dev. "Top 100 Developer Productivity Statistics with AI Tools 2026."
https://www.index.dev/blog/developer-productivity-statistics-with-ai-tools

[17] Techreviewer. "AI in Software Development 2025: From Exploration to Accountability." 2025.
https://techreviewer.co/blog/ai-in-software-development-2025-from-exploration-to-accountability-a-global-survey-analysis

[18] OpsLevel. "TL;DR: Key Takeaways from the 2024 Google Cloud DORA Report."
https://www.opslevel.com/resources/tl-dr-key-takeaways-from-the-2024-google-cloud-dora-report

---

## Notes for Presentation Design

- **Color palette**: Use a dark, professional base (near-black background or dark navy) with a single accent color (teal or blue-green works well for tech audiences). Reserve amber/orange exclusively for risk/caution data points.
- **Typography**: Use a single sans-serif font family. Large numbers for stat slides — 72pt or larger for the headline figure.
- **Data citation**: Every data point shown on a slide should have a visible source attribution, even if small. This audience will ask "where did this come from?" Build the answer into the slide.
- **No stock photos**: Use data visualizations, minimal icons, and typography. Stock photography undercuts the data-driven positioning.
- **Speaker notes**: These outlines are for the presenter to internalize, not to read. The slides should be sparse enough that a presenter does not need to read them.
- **Slide count**: 15 slides at 15 minutes = 60 seconds per slide average. Slides 6, 9, and 12 are data-dense and will take 90–120 seconds. Compensate with faster pacing on the section dividers and the title slide.
