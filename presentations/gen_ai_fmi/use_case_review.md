# Use Case Alignment Review
*Agent 1: Use Case Alignment Reviewer*
*Reviewing: slides_s1_s3_v3.cjs (Slides 1–15), slides_s4_s6_v3.cjs (Slides 16–30), slides_s7_s10_v3.cjs (Slides 31–47)*

---

## Goal 1: Upskill — Score: 7/10

### What works

**Tool map is clear and actionable.** Slide 10 (right tool for the task) and Slide 8 (four tools available now) together give a team member a complete decision rule in under 3 seconds. The "task → tool → why" table format is the right structure.

**Access paths are specific.** Slide 9 gives step-by-step access instructions per tool: IT self-service portal name, approval timescales (2–3 days for Copilot), cost (£20/month for Cursor), and the fallback (T&E expense). A team member could act on this immediately.

**Compliance rules are clear enough to apply.** Slides 28–30 give the SAFE / NEVER boundary with real FM&I examples (calibration parameters, live positions, anonymised hub names). Rule 3 ("code does not equal data — but check") addresses the most common edge case correctly.

**Prompting technique is taught with reasonable specificity.** Slide 21 (Better Prompts formula) gives four named techniques with FM&I examples. The FM&I prompt template (Context / Task / Constraints / Verification) is the right structure and is shown in code font so it looks usable.

**Template project concept is explained adequately.** Slide 39 shows the file structure (.claude/, .cursorrules, CLAUDE.md) with concrete FM&I applications. The "For FM&I projects" item explicitly explains what to put in CLAUDE.md.

### Gaps

**The "how to use it in Dataiku specifically" is underdeveloped.** Dataiku is the team's primary platform. Slides explain that Copilot can work with Dataiku recipes, but there is no slide showing the specific IDE configuration for Dataiku (Python recipe editing in VS Code with Dataiku remote kernel, or the Dataiku embedded editor setup). A team member would leave knowing they should use Copilot in VS Code, but not knowing the Dataiku-specific steps to make that work.

**Prompting specificity drops off after the template slide.** Slide 21 teaches the framework but only one worked example is shown in the right-side terminal card. The template card is good; the worked application is thin. There are no "before prompt / after prompt" examples showing the improvement concretely.

**Access instructions for Copilot Studio are vague.** Slide 9 says "IT approval and a manager-signed business justification" and references the intranet guide path. This is adequate but the justification template (what to write) is missing.

**Evidence of total score:**
- Specific access paths: 4/4 tools covered ✓
- Specific workflow steps per tool: 3/4 tools (Dataiku integration missing) ✓/✗
- Prompting technique with FM&I examples: present but one worked example only ✓/✗
- Template project concept explained: adequate ✓
- Compliance boundaries: clear and specific ✓

---

## Goal 2: Inspire — Score: 6/10

### Genuine "wow" moments identified

**Slide 19 — Cursor crack spread app, 12 minutes.** The strongest demo slide. The prompt is specific FM&I language ("crack_spreads.csv", "30-day rolling average", "commodity selector"), the big number (12 min vs 2–3 days) is visible, and the five-step breakdown of what happens makes the result feel real rather than claimed. A data analyst would think "I want to try that this week."

**Slide 33 — Claude Code full pipeline audit.** The prompt is excellent ("Audit our Brent futures fundamental model... replace with named constants... write NumPy docstrings... generate pytest test suite... create MODEL.md"). The output specifics (23 magic numbers across 8 files, 47 undocumented functions, 156 unit tests) are precise enough to feel credible. "12 minutes" vs "2–3 days" lands hard. A modeller or data engineer with documentation debt would immediately recognise this as their problem.

**Slide 2 — 15 hrs vs 2 hrs gap.** The left-side big number panel is the right structure. "Fifteen hours versus two hours" is arresting and specific. This is a genuine wow moment for anyone who currently spends significant time on repetitive tasks.

### Slides that are close but not landing

**Slide 18 — Copilot recipe timeout debug, 20 minutes.** The prompt is specific ("iterrows() anti-pattern", "500k rows", "gas_hub_prices"). The big number (20 min vs 3–4 hours) should be the first thing the eye goes to but it is inside the right panel rather than being displayed prominently. Stronger demo slides make the big number the visual centrepiece.

**Slide 13 — Meeting summary 3 minutes.** The 45-60 min → 3 min comparison is good but "meeting summary" is the most overused AI demo in existence. FM&I team members will have seen this in 10 other sessions. The prompt doesn't use FM&I-specific language — "trading strategy call" is FM&I but "extract action items" is generic. The FM&I-specific version (cross-referencing with model delivery commitments, trading desk follow-ups) would be stronger.

**Slide 38 — Four personal use cases.** These are credible and specific but described at summary level. "Claude Code + Remotion: AI-generated video presentations" is interesting but the FM&I parallel ("the same pattern applies to any FM&I output that currently involves manual formatting") is written in small body text rather than demonstrated. The FM&I connection is asserted rather than shown.

### Missing "wow" moments

- No demo where an analyst asks a natural language question about a real commodity forward curve and gets a specific market analysis answer
- No before/after showing actual output quality difference: "Here is what ChatGPT 2024 produced for this FM&I prompt. Here is what Claude Opus 4.6 produces for the same prompt today."
- No FM&I "see it in action" for Microsoft Copilot that uses actual trading-desk language

### Visual design issue on demo slides

The big number (12 min, 20 min, 3 min) is positioned in the right-side panel at ~36pt. It should be the first thing the eye goes to on arrival — currently the prompt header competes with it because the eye moves left-to-right and reads the prompt first. A stronger layout would put the big number and the before/after comparison at the top of the slide, with the "what happens" detail below.

---

## Goal 3: Warn About Pace — Score: 4/10

This is the most significant weakness in the presentation. The warning angle is almost entirely absent from the slide content, and where it exists (slides 44–46, the philosophical statement slides), it is abstract rather than viscerally specific.

### What works

**Slides 44–46 (statement slides) have the right instinct.** "AI isn't making data scientists obsolete — it's making the ones who don't use it obsolete" is a strong headline. "The next decade won't kill technology jobs. It will kill the comfortable middle." is honest and correct. These are the right ideas.

**Slide 7 (capability timeline) exists.** Five milestones across 12 months (Mar 2025 → Jan 2026) show the pace of change is real. The milestones are specific (Claude 4.6, Copilot Workspace GA, Cursor background agents).

**Slide 3 (stat cascade)** has "40-80 hrs per month saved" and "12 minutes from prompt to working Dash app" — both contribute to the urgency argument.

### What is missing (specific gaps)

**No dedicated "acceleration" slide.** The capability timeline (Slide 7) is too brief and too positive to communicate alarm. It reads as "here's what changed" rather than "here's how fast this is accelerating and what it means if you're not on the curve." A slide that viscerally communicates compounding acceleration is needed: side-by-side capability jumps showing the before/after of what was possible 12 months ago vs today, with a forward-looking "in 12 months" section.

**No "cost of not engaging" framing anywhere in the slide content.** The statement slides (44–46) address the consequences abstractly ("the comfortable middle will be automated"). But there is no slide that directly quantifies what the gap looks like in practical terms: what does a team at a quant fund with 12 months of AI adoption have over a team with 3 months? How many models per quarter? What is the response time advantage to trading desk requests? This is the argument that converts philosophical agreement into genuine urgency.

**The 12-month trajectory is framed as informational, not alarming.** Slide 24 ("The models you knew a year ago are not the models available today") lists five milestones with neutral descriptions. There is no framing of the gradient: each milestone was not a similar-sized step, it was an accelerating step. The fact that GPT-4o, Claude 3.7, o3, and Claude 4.6 all shipped in 12 months is extraordinary — the slide reads like a neutral changelog rather than a document of extraordinary velocity.

**No "what was impossible 12 months ago that is routine today" framing.** The most powerful version of the warning gives specific before/after examples of capability:
- 12 months ago: AI could not reliably debug a complex multi-file pipeline without hallucinating. Today: Claude Code audits 30 files and writes 156 tests autonomously.
- 12 months ago: context windows were too small to hold a full Dataiku project. Today: Gemini 2.0 holds 1M tokens.
- None of this is framed this way in the current slides.

**The philosophical slides are too abstract for this audience.** Slides 44–46 are well-written but they are philosophical essays in small body text. A quant analyst processes numbers, not essays. The warning needs to be in the same register as the rest of the presentation: specific, quantified, FM&I-specific.

**No competitor / peer framing.** There is no mention of what peer organisations are doing with these tools. "Teams at quant funds with mature AI adoption are shipping 3x more models per quarter at the same headcount" appears in one right-side card on Slide 3 but is buried. It needs a dedicated slide or at minimum a prominent position in the opening section.

---

## Narrative Arc Assessment

### Structure
The session runs: Title → Section 1 (Why Now) → Section 2 (Landscape) → Sections 3-6 (per-tool deep dives) → Sections 7-8 (advanced concepts + personal use cases) → Section 9 (business use cases) → Section 10 (philosophy + close).

### What works
The opening (Slides 2–5) creates urgency correctly. The "15 hrs vs 2 hrs" opening statistic is the right hook. The stat cascade (Slide 3) reinforces the urgency with four data points. The "our work is exactly where Gen AI creates the most leverage" slide (Slide 5) does the important job of connecting general AI claims to specific FM&I workflows.

The tool sections (3–6) are well-structured and follow a consistent pattern: comparison → demo → modes/technique → roadmap. The demos are the emotional high points of each section.

The closing CTAs (Slide 47) are clear, specific, and actionable. "Request your licence", "run one real task this week", and "bring your best idea" are the right three calls to action.

### Where it loses momentum

**The arc goes: urgency → tools → more tools → more tools → philosophy.** By the time the audience reaches slides 44–46, they have been in "tool information" mode for 40+ slides and the philosophical warning is an abrupt gear change. The warning feels like an ending rather than a thread woven through the session.

**The warning should come earlier and be reinforced.** The ideal structure would have an acceleration narrative in Section 1 (after the productivity statistics), another reference in the capability timeline slide (framed as alarming not informational), and then the philosophical slides at the end serve as a synthesis rather than an introduction of the warning theme.

**The opening does not create urgency about the pace of change.** It creates urgency about the productivity gap (which is good), but the "this is moving faster than you realise" thread is absent until the capability timeline slide 7, and even there it is framed informally.

**Slide 4 ("What you will walk away with today") dissipates urgency.** Coming immediately after the strong productivity gap slide, the session-goals slide is procedural and polite. A stronger session opening would delay the agenda until after the opening hook has fully landed, or would frame the session goals in terms of the warning: "Here are the three things that will make the difference between being in the 15-hour group and the 2-hour group."

---

## Priority Improvements (ordered by impact)

### P0: Must Fix

**P0-1: Add a dedicated acceleration / "the curve" slide in Section 1 (after Slide 3 or as new Slide 3a)**
The presentation needs one slide that makes the pace of change viscerally clear, with specific before/after capability examples (not just milestone names), and a forward-looking "in 12 months, based on current trajectory..." section. This is the single most important missing piece against Goal 3.
- Target: new slide inserted after Slide 3 (before "What you will walk away with today")
- Content: specific capability jumps with before/after framing + 3-4 forward predictions
- Tone: "I'm not trying to alarm you, but here's what I'm seeing — and here's why the next 12 months matter more than the last 12 did"

**P0-2: Add a "cost of not engaging" slide in Section 1**
A dedicated slide that directly answers "what does it look like in 12 months if we don't adopt these tools?" Not fear-mongering but honest quantification: competitor velocity, output gap, response time advantage. This converts philosophical agreement into genuine urgency.
- Target: new slide inserted after the acceleration slide, before Slide 4
- Content: quantified gap between adopters and non-adopters at 6-month and 12-month horizons, with FM&I-specific framing

**P0-3: Reframe Slide 7 (capability timeline) as alarming, not informational**
The current timeline lists five milestones neutrally. It needs to be reframed to communicate the gradient: "Each of these milestones landed within a few months of the last. This is not one step change — it is an accelerating curve."
- Target: replace bottom bar text and add explicit "the gradient" framing to the slide header
- Additional: add a note that quality improved 10× in capability terms while cost per token dropped ~70%

### P1: Should Fix

**P1-1: Strengthen the Slide 19 Cursor demo visual layout**
The 12-minute big number should be the first thing the eye goes to. Currently the prompt header occupies the visual prime position. The big number should move up or be made larger.
- Target: Slide 19 right panel — increase "12 min" font size to 48-52pt and reduce surrounding text size

**P1-2: Replace the Slide 13 Microsoft Copilot demo prompt with FM&I-specific language**
"Summarise this 45-minute trading strategy call" is generic. Replace with a prompt that uses actual FM&I domain language and a more specific output that a team member would recognise as theirs.
- Target: Slide 13 prompt text — make the FM&I context unmistakably specific

**P1-3: Add quantified "adopter vs non-adopter" data to Slide 3 right-side card**
The current right card says "organisations with mature AI adoption are shipping 2-3 times more models per quarter." This line is doing enormous work but is buried in body text at 9pt. It needs to be a headline, not a buried statistic.
- Target: Slide 3 right card — elevate the 2-3x model delivery stat to a much more prominent position

**P1-4: Sharpen the closing statement slides (44–46) with more specific numbers**
The statement slides are philosophically right but too abstract for a quantitative audience. Each should include at least one specific, quantified data point that gives the abstract claim teeth.
- Target: Slides 44–46 — add one specific numerical proof point to each body text section

### P2: Nice to Have

**P2-1: Add a "before/after output quality" comparison slide in Section 5 (Model Landscape)**
Show the same FM&I prompt given to a 2024-era model vs Claude Sonnet 4.6 today — to make the quality improvement visceral rather than described.

**P2-2: Slide 4 session goals — reframe in terms of urgency, not agenda**
"What you will walk away with today" is procedural. An alternative framing: "By the end of this session, you will have no excuse not to be in the 15-hour group."

**P2-3: Slide 18 Copilot demo — make the big number (20 min) the visual centrepiece**
Same issue as Slide 19: the time saving should be the first visual element, not a supporting element.
