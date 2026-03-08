# FM&I Innovation Day — Gen AI Ideas Board

**Session**: Gen AI Upskilling · March 2026
**Team**: Fundamentals Modelling & Innovation · Trading Analytics & Insights · BP Trading

---

## Current Uses — Seed from the Team

*Add your current AI tool uses here. No idea is too small. The point is to map where we are starting.*

1. What Gen AI tools are you currently using in your day-to-day work — even occasionally?
2. What is the single task where AI has saved you the most time so far?
3. Have you used AI for Dataiku recipe development or debugging? What happened?
4. Have you used M365 Copilot in Teams or Outlook? What did you use it for?
5. Have you tried GitHub Copilot for any FM&I pipeline or model code? What worked?
6. What is the most repetitive task in your current workflow that you have NOT yet tried AI on?
7. Have you used AI for documentation — model cards, code comments, README files?
8. Have you used AI for data analysis or chart generation? Where did it land?
9. What is the prompt or workflow pattern you have found most reliable?
10. What tool or use case would you most want to explore at Innovation Day?

---

## Confirmed Productivity Wins

*Pre-populated from session research. Add your own with time estimates.*

| Tool | FM&I Workflow | Time Saved (estimate) |
|------|---------------|----------------------|
| GitHub Copilot | Dataiku recipe debugging — paste stack trace + recipe, get diagnosis and fix | 40–70 min per incident |
| GitHub Copilot | New ELT recipe generation from schema + transformation description | 2–3 hrs per recipe |
| GitHub Copilot | Unit test suite generation for pipeline functions | 1.5–2 hrs per module |
| GitHub Copilot | Docstring and model card generation from existing code | 2–4 hrs per model |
| M365 Copilot (Teams) | Meeting summary with action item extraction | 10–15 min per meeting |
| M365 Copilot (Outlook) | Email thread summarisation after time away | 5–10 min per thread |
| M365 Copilot (Outlook) | Draft reply generation from bullet-point instructions | 10–15 min per email |
| M365 Copilot (Word) | Model documentation first draft from model code description | 3–4 hrs per document |
| GitHub Copilot | Ad hoc price analysis code generation (groupby, rolling stats, Plotly) | 1.5–2 hrs per analysis |
| GitHub Copilot | Refactoring — vectorise nested loops, extract classes | 1–2 hrs per refactor |
| GitHub Copilot | PR commit message and summary generation | 5–10 min per PR |
| Cursor (personal) | Multi-file refactor across entire pipeline project | 3–5 hrs per session |
| Cursor (personal) | Background agent: large-scale test file conversion (unittest → pytest) | Full day → overnight job |
| Claude Code (personal) | Agent team for complex multi-file deliverable generation | Varies — 10× time compression |
| Cursor (personal) | Architecture reasoning: "how should I add X without breaking Y?" | 1–2 hrs scoping time |

---

## Commercial Use Case Ideas

### Data & Modelling

1. **AI Model Validator Agent**
   - *What*: Agent that automatically tests a new model version against holdout data, compares against incumbent, and generates a structured model comparison report
   - *Tool*: Claude Code + Python testing framework + Dataiku API
   - *Trigger*: On model code commit to Git
   - *Output*: Structured report: performance delta, statistical significance, recommended action (promote/reject)

2. **Automatic Model Card Generator**
   - *What*: On every model code commit, an agent reads the model code, training data schema, and validation metrics, and generates or updates the model card
   - *Tool*: Claude Code hooks (post-commit) or GitHub Actions
   - *Output*: Standardised model card with methodology, inputs, outputs, known limitations, and performance summary

3. **Hyperparameter Reasoning Agent**
   - *What*: Instead of grid search, an agent reasons about which hyperparameter regions to explore based on observed model behaviour and domain knowledge
   - *Tool*: Claude API integrated with model training framework (Python, Dataiku)
   - *Value*: More efficient exploration than brute-force grid search; AI explains the reasoning behind each proposed configuration

4. **AI Code Reviewer for Pipeline Changes**
   - *What*: Before merging a Dataiku recipe change, an agent reviews for: data type assumptions, null handling edge cases, join key uniqueness, performance implications, missing test coverage
   - *Tool*: GitHub Actions + Claude API
   - *Trigger*: Pull request creation
   - *Output*: Code review comment with specific issues flagged and suggested fixes

5. **Statistical Assumption Checker**
   - *What*: Agent that tests a proposed statistical model against its own declared assumptions — stationarity, homoscedasticity, normality of residuals, multicollinearity — and generates a structured violation report
   - *Tool*: Claude API + Python statistical testing libraries (statsmodels, scipy)
   - *Output*: Pass/fail per assumption, severity rating, recommended remediation

---

### Trading Desk Support

6. **Automated Market Structure Briefing Agent**
   - *What*: Daily agent that runs on market data refresh, identifies 3–5 notable market structure changes (curve shape changes, spread anomalies, volume outliers, significant price movements), and drafts a briefing for the trading desk
   - *Tool*: Claude Code or Copilot Agent with Dataiku data access
   - *Trigger*: Morning data refresh completion
   - *Output*: Structured briefing in standard format, ready for review and distribution

7. **Request Triage Agent**
   - *What*: FM&I receives ad hoc requests from traders. An agent reads the request, identifies what data and analysis is needed, generates the initial code structure, and estimates completion time
   - *Tool*: Teams Copilot Agent or Claude API with Teams integration
   - *Input*: Teams message from trader
   - *Output*: Structured response: data required, analysis approach, initial code scaffold, time estimate

8. **Curve Comparison Narrative Generator**
   - *What*: When a new forward curve is released, the agent compares it to the previous version across key metrics (level shift, slope change, curvature, seasonal pattern) and generates a narrative explanation of the changes
   - *Tool*: Claude API + Dataiku pipeline integration
   - *Trigger*: New curve publication event
   - *Output*: Plain-language narrative suitable for trading desk distribution

9. **Scenario Analysis Automation**
   - *What*: Trader or analyst inputs a set of scenario assumptions in plain English. The agent interprets the assumptions, generates code to run the scenarios through existing models, executes via Dataiku, and formats output in standard reporting format
   - *Tool*: Claude API + Dataiku API + output templates
   - *Output*: Scenario results in standard template with methodology footnotes

10. **News-to-Model-Impact Mapper**
    - *What*: Agent reads a significant news event (major supply disruption, regulatory change, demand shock), identifies which FM&I models are most exposed, and drafts a preliminary impact assessment
    - *Tool*: Claude API + model inventory/documentation index
    - *Output*: Impact assessment: affected models, exposure magnitude estimate, recommended model review actions

---

### Dataiku & Platform Integration

11. **Pipeline Health Dashboard Agent**
    - *What*: Weekly automated report of all Dataiku pipeline health — scenario run times vs baseline, error rates, data freshness, row count anomalies — generated automatically and posted to Teams channel
    - *Tool*: Claude Code + Dataiku API + Teams webhook
    - *Trigger*: Weekly schedule (Monday morning)
    - *Output*: Teams post with structured health summary, flagged anomalies, recommended actions

12. **Natural Language Data Lineage Query Interface**
    - *What*: "Which models downstream are affected if the TTF spot price feed goes down?" — an agent traces the Dataiku lineage graph and returns a human-readable impact assessment
    - *Tool*: Dataiku MCP server + Claude Code or Cursor
    - *Input*: Natural language question about data dependencies
    - *Output*: Dependency chain, impact assessment, affected models/recipes

13. **Recipe Optimisation Agent**
    - *What*: Agent reviews Python recipes for performance bottlenecks — nested loops that could be vectorised, inefficient groupby operations, redundant joins, opportunities for parallelisation — and generates a prioritised optimisation list with code suggestions
    - *Tool*: GitHub Copilot agent mode or Claude Code
    - *Output*: Prioritised list of optimisations with estimated performance improvement and code changes

14. **Schema Drift Detector**
    - *What*: Agent monitors upstream data schemas on every pipeline run. When a column is added, removed, or changes type, it raises an alert, identifies downstream recipes that could be affected, and drafts a remediation plan
    - *Tool*: Dataiku scenario checks + Claude API for impact analysis
    - *Trigger*: Schema comparison at pipeline start
    - *Output*: Teams alert with change summary, affected downstream components, suggested fixes

15. **Test Coverage Gap Analyser**
    - *What*: Agent reviews which Dataiku recipes and Python modules lack adequate test scenarios and generates a prioritised list of test coverage to add, with initial test scaffolding
    - *Tool*: Claude Code analysis of project structure + Dataiku scenario inventory
    - *Output*: Coverage report with prioritised list, effort estimates, and generated test stubs

---

### Reporting & Visualisation

16. **Natural Language Chart Generator**
    - *What*: Analyst describes a chart in plain English ("show me TTF spot price vs the 12M forward for the last 6 months, with the spread on a secondary axis") → agent generates working Plotly code ready to embed in a report
    - *Tool*: Claude API or GitHub Copilot (chat interface)
    - *Output*: Working Plotly Python code, ready for Dataiku recipe or Jupyter notebook

17. **Automated PowerPoint Generation**
    - *What*: Weekly model performance data → agent generates a fully formatted PowerPoint presentation in FM&I's standard template, including charts, commentary, and methodology notes
    - *Tool*: Claude Code + python-pptx or PptxGenJS
    - *Trigger*: Weekly data refresh completion
    - *Output*: Ready-to-review PPTX in standard template

18. **Report Commentary Assistant**
    - *What*: Analyst produces charts and tables. Agent reads the data underlying those charts and drafts commentary that explains key movements, highlights anomalies, and flags anything requiring management attention
    - *Tool*: M365 Copilot (Word) or Claude API with chart data input
    - *Output*: Draft commentary in the analyst's preferred style, ready for review and editing

19. **Executive Summary Generator**
    - *What*: Full technical model report (20+ pages) → agent produces a 1-page executive summary for senior stakeholders: key findings, performance against benchmark, risk flags, recommended actions
    - *Tool*: M365 Copilot (Word) or Claude API
    - *Output*: Concise, accurate 1-page summary in plain language

20. **Comparative Forward Curve Visualisation Generator**
    - *What*: "Show me how our gas hub price forecasts have evolved over the last 6 months" → agent pulls historical forecast data from Dataiku, generates a comparison chart showing forecast evolution over time against actuals
    - *Tool*: Claude Code + Dataiku API + Plotly
    - *Output*: Interactive Plotly chart ready for distribution or embedding

---

### Process & Workflow Automation

21. **Meeting Action Item Extractor → Jira/Teams**
    - *What*: After every FM&I team meeting, agent reads the Teams transcript, identifies all action items with assigned owners, creates Jira tickets or sends Teams follow-ups automatically
    - *Tool*: M365 Copilot Teams integration + Power Automate
    - *Trigger*: Meeting ends + transcript available
    - *Output*: Jira tickets or Teams follow-up messages, one per action item

22. **FM&I Onboarding Knowledge Base Agent**
    - *What*: New team member asks questions about FM&I pipelines, models, processes. Agent answers from FM&I documentation, model cards, Confluence pages, and the FM&I codebase
    - *Tool*: Copilot Studio agent with SharePoint + Confluence knowledge source
    - *Output*: Accurate, sourced answers to common onboarding questions

23. **Incident Response Assistant**
    - *What*: When a model or pipeline failure is reported in Teams, the agent automatically retrieves: relevant job logs, recent code changes in the affected recipe, upstream data status, and similar historical incidents. Generates a structured incident diagnostic package.
    - *Tool*: Claude Code + Dataiku MCP + GitHub API
    - *Trigger*: Teams alert or manual invocation
    - *Output*: Diagnostic package: logs, code diff, upstream status, suggested root cause, recommended fix

24. **Regulatory Filing Gap Checker**
    - *What*: Agent checks model documentation against a checklist of internal regulatory filing requirements and identifies gaps before submission — missing sections, unclear methodology descriptions, undocumented assumptions
    - *Tool*: Claude API with regulatory requirements template
    - *Input*: Model documentation draft
    - *Output*: Gap report with specific missing items and suggested additions

25. **Specification-to-Code Pipeline**
    - *What*: Business analyst or trader writes a natural language specification for a new analysis ("I need a weekly report that shows gas hub price spreads vs the 5-year average, with Z-score anomaly flagging"). Agent generates the initial code structure and test cases.
    - *Tool*: Claude Code or GitHub Copilot agent mode
    - *Input*: Natural language specification
    - *Output*: Initial code scaffold, test structure, and a clarifying questions list for any ambiguities

---

## Evaluation Matrix

*Pre-populated for all 25 confirmed ideas. Owner column to be completed by the team at Innovation Day.*

| # | Idea | Effort (1–5) | Impact (1–5) | Data Risk (L/M/H) | Owner |
|---|------|-------------|-------------|------------------|-------|
| 1 | AI Model Validator Agent | 3 | 5 | L | |
| 2 | Automatic Model Card Generator | 2 | 4 | L | |
| 3 | Hyperparameter Reasoning Agent | 4 | 3 | L | |
| 4 | AI Code Reviewer for Pipeline Changes | 2 | 5 | L | |
| 5 | Statistical Assumption Checker | 3 | 4 | L | |
| 6 | Automated Market Structure Briefing | 3 | 5 | M | |
| 7 | Request Triage Agent | 2 | 4 | L | |
| 8 | Curve Comparison Narrative Generator | 2 | 4 | M | |
| 9 | Scenario Analysis Automation | 4 | 5 | M | |
| 10 | News-to-Model-Impact Mapper | 3 | 3 | L | |
| 11 | Pipeline Health Dashboard Agent | 2 | 5 | L | |
| 12 | NL Data Lineage Query Interface | 3 | 4 | L | |
| 13 | Recipe Optimisation Agent | 2 | 4 | L | |
| 14 | Schema Drift Detector | 2 | 5 | L | |
| 15 | Test Coverage Gap Analyser | 2 | 4 | L | |
| 16 | NL Chart Generator | 1 | 4 | L | |
| 17 | Automated PowerPoint Generation | 2 | 4 | M | |
| 18 | Report Commentary Assistant | 1 | 4 | M | |
| 19 | Executive Summary Generator | 1 | 4 | M | |
| 20 | Comparative Forecast Visualisation | 2 | 4 | M | |
| 21 | Meeting Action Item → Jira | 1 | 4 | L | |
| 22 | Onboarding Knowledge Base Agent | 2 | 5 | L | |
| 23 | Incident Response Assistant | 3 | 5 | L | |
| 24 | Regulatory Filing Gap Checker | 2 | 4 | M | |
| 25 | Specification-to-Code Pipeline | 2 | 4 | L | |

**Effort scale**: 1 = hours, 2 = 1–2 days, 3 = 1 week, 4 = 2–4 weeks, 5 = quarter+
**Impact scale**: 1 = marginal improvement, 5 = step-change in team capability
**Data Risk**: L = no sensitive data involved, M = internal data (enterprise tool required), H = requires local/offline solution

---

## Quick Wins (High Impact, Low Effort)

*Effort ≤ 2 AND Impact ≥ 4 — these are the Innovation Day day-one candidates:*

| Idea | Effort | Impact | Recommended first step |
|------|--------|--------|----------------------|
| AI Code Reviewer for Pipeline Changes | 2 | 5 | Set up GitHub Actions with Claude API for one pipeline repo |
| Automatic Model Card Generator | 2 | 4 | Create a Claude Code skill for model card generation |
| Pipeline Health Dashboard Agent | 2 | 5 | Build a Python script + Dataiku API + Teams webhook |
| Schema Drift Detector | 2 | 5 | Add schema validation check at pipeline start with alert |
| NL Chart Generator | 1 | 4 | Add a GitHub Copilot prompt template to the team's prompts/ directory |
| Report Commentary Assistant | 1 | 4 | Configure M365 Copilot in Word with FM&I reporting style instructions |
| Executive Summary Generator | 1 | 4 | Use M365 Copilot Word: "Summarise this document in 1 page for senior stakeholders" |
| Meeting Action Item → Jira | 1 | 4 | Enable Teams Copilot + connect Power Automate to Jira |
| Onboarding Knowledge Base Agent | 2 | 5 | Build Copilot Studio agent on FM&I SharePoint documentation |

---

*Innovation Day board seeded. Team to add current uses and additional commercial ideas during the session.*
