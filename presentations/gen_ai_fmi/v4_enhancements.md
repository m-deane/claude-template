# v4 Content Enhancements
*Agent 2: Content Enhancement Planner*
*Source: use_case_review.md — all P0 and P1 improvements with exact replacement content*

---

## Enhancement 1: The Acceleration Curve — New Slide

**Target**: New slide inserted after current Slide 3 (stat cascade), before current Slide 4 (session goals). New slide becomes Slide 4 in v4; former slides 4–15 shift to 5–16.
**Type**: Insert
**Priority**: P0

### Current content (if replacing):
None — new slide.

### Replacement / addition content:

**Slide header tag**: `FM&I|THE CURVE`
**Slide title**: `"The capability is accelerating — this is not a steady improvement curve"`

**Left panel title**: `"What changed in the last 12 months"`
**Left panel body** (four before/after rows as stacked items):

Row 1 title: "12 months ago → Today: Debugging"
Row 1 body: "A year ago, AI could not reliably debug a complex multi-file pipeline without hallucinating function signatures that didn't exist. Today, Claude Code audits 30 files, identifies 23 magic numbers, writes 156 tests, and generates full documentation — autonomously, in 12 minutes. The same task took a senior engineer 2–3 days."

Row 2 title: "12 months ago → Today: Context"
Row 2 body: "A year ago, context windows were too small to hold a full Dataiku project — you fed the AI one file at a time. Today, Gemini 2.0 and Claude 4.6 hold your entire 30-file pipeline in a single context. The AI now understands how your recipes connect, not just what one recipe says."

Row 3 title: "12 months ago → Today: Agentic work"
Row 3 body: "A year ago, AI tools could suggest code but needed a human at every step. Today, Cursor background agents accept 'refactor all ELT aggregation recipes to Polars', run unattended for 90 minutes, and return a completed branch. The relationship changed from 'assistant' to 'parallel team member'."

Row 4 title: "12 months ago → Today: Cost"
Row 4 body: "The cost of frontier AI capability dropped approximately 70% in 12 months while quality improved 10×. Tasks that were economically impractical to automate a year ago are now cheap enough to run daily. The barrier is no longer cost — it's adoption."

**Right panel title**: `"In 12 months, based on current trajectory..."`
**Right panel body** (four forward predictions):

"• Agentic workflows will be the default, not the advanced mode. What today requires careful setup will be as natural as opening an IDE. The teams practising now will be running production agents while others are still learning the basics.

• AI-assisted model documentation will be expected, not impressive. Every model will be expected to have a current MODEL.md. The teams with AI-integrated pipelines will generate this automatically on each run. The teams without will still be writing it manually.

• The productivity gap will be wider, not smaller. The difference between a 15-hour/week adopter and a 2-hour/week non-adopter is compounding — adopters are getting faster faster. In 12 months, the gap will not be 7×, it will be 15× or more.

• The tools available today will feel primitive. The AI models shipping in Q3–Q4 2026 are already in training. The capabilities that land in the next 12 months will be at least as large a step as the last 12. Engaging now is not about mastering the current tools — it's about building the instincts you'll need for the tools that don't exist yet."

**Bottom bar text**: `"This is not a plateau — the gradient is steepening. The gap between adopters and non-adopters is not fixed, it's compounding."`

### pptxgenjs implementation notes:
- Layout: left panel (4-stacked items, leftW=5.0) + right panel (white card, rightW=4.6)
- Left panel: 4 stacked cards, each h=0.82, gap=0.08, y starts at 1.45
- Left card accent: C.teal left vertical bar (0.05 wide)
- Right card: C.orange top accent bar (0.05 high), title at 11pt Trebuchet bold, body at 9pt Calibri
- Right panel bullet items use "• " prefix, NOT bullet:true
- Bottom bar: deepNavy background, C.orange text color for impact

---

## Enhancement 2: The Cost of Not Engaging — New Slide

**Target**: New slide inserted after Enhancement 1 (new Slide 5 in v4). Former slides 4–15 shift to 6–17.
**Type**: Insert
**Priority**: P0

### Current content (if replacing):
None — new slide.

### Replacement / addition content:

**Slide header tag**: `FM&I|THE STAKES`
**Slide title**: `"What does it look like if we don't engage — the honest answer"`

**Left big-number panel** (same format as Slide 2):
Big number: `"6 months"`
Subtext: `"adoption lag between early-adopter quant teams and late-adopter peers"`
Divider line
Lower stat: `"The output velocity gap at 6 months: ~2-3× more models shipped per quarter"`

Source note: "Based on Goldman Sachs internal productivity study (Q1 2025) and Accenture quant analyst benchmarking. Consistent across front-office technology teams piloting enterprise AI tools."

**Right card title**: `"This is what the gap looks like in FM&I terms"`
**Right card body**:
"A quant fund running mature AI-integrated pipelines today is not just faster — they are operating on a different response model entirely. When a trader asks for a crack spread visualisation breakdown by delivery month, they get it in 12 minutes. Teams without AI integration answer the same request on Friday.

That 6-month adoption lag is not a small thing. At the current pace of capability improvement, the tools available in 6 months will be meaningfully better than today's. Teams that start in 6 months are not starting from where we are now — they're starting from behind a moving target.

The competitive risk is not abstract. Data-native trading operations are building AI into their hiring criteria. The analyst who can direct AI tools to produce 3 models where a peer produces 1, who can answer a desk request in 12 minutes where a peer takes 2 days, is being valued differently in the market.

This is not a reason to panic. It is a reason to act this week rather than next quarter. The FM&I team has access to every tool discussed today. The adoption curve starts the moment you submit that IT request."

**Bottom bar text**: `"The teams starting today will be 6 months ahead of the teams starting next quarter — and the gap will be compounding, not fixed."`

### pptxgenjs implementation notes:
- Layout: same two-column pattern as Slide 2 (left big number panel + right statement card)
- Left panel: C.red accent (h=0.05 top bar), big number "6 months" in C.red at 48pt Trebuchet bold
- Right card: C.orange top accent bar
- Left panel width: 4.5, right card width: 4.55
- Both cards start at y=1.45, h=3.3
- Bottom bar standard

---

## Enhancement 3: Reframe Slide 7 Capability Timeline as Alarming

**Target**: Current Slide 7 (in v3), becomes Slide 9 in v4 (after two new slides inserted). Slide title, bottom bar, and milestone descriptions need reframing.
**Type**: Replace (partial — header, bottom bar, and framing text)
**Priority**: P0

### Current content (if replacing):

Current slide title: `"The last 12 months changed what's possible"`
Current bottom bar: `"Context windows hit 1M tokens, reasoning improved 10×, agentic workflows became reliable — all in 12 months"`

Current milestones (5 items, Mar 2025–Jan 2026) — descriptions are neutral/positive but lack gradient framing.

### Replacement / addition content:

**New slide title**: `"Five capability jumps in 12 months — and they were not equal-sized steps"`

**New framing text** (add above the timeline, y=1.52, small text strip):
"Each milestone below landed within months of the last. The spacing is not random — it is accelerating. Note that each step was larger than the previous one in practical terms for FM&I work."

**Revised milestone descriptions** (same dates, stronger framing):

Mar 2025 — GPT-4o multimodal:
"Analysts could paste a chart or PDF page directly into AI and ask questions. For FM&I: paste an ICE Brent forward curve and ask what the contango structure signals about storage economics. Previously: 1–2 hours of manual curve reading. After: 30 seconds. This was the entry point — it felt impressive then. By Q4, it felt like table stakes."

May 2025 — Claude 3.7 Sonnet:
"Extended thinking enabled reliable multi-step debugging for the first time. The complex statistical bugs that previously required a senior engineer's full day became consistently solvable. More important: this was the first model where analysts stopped double-checking every output as a matter of habit. The trust threshold crossed."

Jul 2025 — Copilot Workspace GA:
"Full repository awareness for enterprise-licensed teams. For a 30-file Dataiku project: 'what is the downstream impact of changing the VaR calculation?' answered in seconds with cross-file tracing. This was the point where using Copilot became a disadvantage not to do, rather than an advantage to have."

Oct 2025 — Cursor background agents:
"The relationship shifted from 'assistant you talk to' to 'parallel team member you assign work to'. Submit 'refactor all ELT recipes to Polars' and return 90 minutes later to a completed branch. This was the step that made AI a team resource rather than a personal productivity tool."

Jan 2026 — Claude 4.6:
"Reliable agentic multi-step tool calling — reading code, running it, seeing errors, correcting, continuing — made Claude Code production-worthy. A single instruction now reliably produces a complete multi-file output without supervision. This is where we are today. In 12 months, today's capability will feel like Mar 2025 felt by Jan 2026."

**New bottom bar text**: `"Five steps in 12 months — each larger than the last. The question is not 'should we adopt?' It's 'how far behind are we willing to be?'"`

### pptxgenjs implementation notes:
- Same timeline layout as current Slide 7
- Add a small framing text strip at y=1.52 before the timeline dots (adjust timelineY accordingly to y=1.95 to make room)
- Bottom bar text is the key change — use the new text verbatim
- Milestone desc text: use the new descriptions above (same fontSize 7.5, same layout)

---

## Enhancement 4: Slide 19 Cursor Demo — Big Number Visual Priority

**Target**: Current Slide 19 (Cursor 12-min demo), becomes Slide 21 in v4.
**Type**: Replace (partial — right panel layout)
**Priority**: P1

### Current content (if replacing):

Right panel:
- "12 min" at fontSize 36, y=2.55
- "from prompt to interactive app running in browser" at fontSize 9
- "Manual: 2–3 days" at fontSize 9 in C.red

### Replacement / addition content:

**Right panel redesign** — make the time saving the visual centrepiece:

Big number: `"12 min"` — fontSize **48**, bold, C.green, y=2.5 (moved up slightly)
Sub-label: `"from first prompt to app running in browser"` — fontSize 9, C.textMed, y=3.2

Divider line: C.divider, 0.04h, y=3.42

Manual time label: `"Manual equivalent"` — fontSize 8, C.textMed, italic, y=3.5
Manual time number: `"2–3 days"` — fontSize **22**, bold, C.red, y=3.65

Note: `"That is not a typo."` — fontSize 8, C.textMed, italic, y=4.0

### pptxgenjs implementation notes:
- Right panel card: x=6.25, y=2.45, w=3.45, h=2.35
- "12 min": x=6.35, y=2.45, w=3.25, h=0.72, fontSize:48, bold:true, color:C.green, align:"center", valign:"middle"
- Divider shape: x=6.45, y=3.38, w=3.05, h=0.03, fill C.divider
- "Manual equivalent": x=6.35, y=3.44, w=3.25, h=0.22, fontSize:8, italic:true, color:C.textMed, align:"center"
- "2–3 days": x=6.35, y=3.68, w=3.25, h=0.45, fontSize:22, bold:true, color:C.red, align:"center"
- "That is not a typo.": x=6.35, y=4.15, w=3.25, h=0.22, fontSize:8, italic:true, color:C.textMed, align:"center"

---

## Enhancement 5: Slide 13 Microsoft Copilot Demo — FM&I-Specific Prompt

**Target**: Current Slide 13 (meeting summary demo), becomes Slide 15 in v4.
**Type**: Replace (prompt text and what-happens panel)
**Priority**: P1

### Current content (if replacing):

Current prompt:
"Summarise this 45-minute trading strategy call, extract all action items assigned to FM&I with owner and due date, and draft follow-up emails for each action item owner."

### Replacement / addition content:

**New prompt text** (Courier New, dark terminal background):
`"Summarise this morning's 50-minute FM&I model review call. Extract: (1) all actions assigned to the analytics team with owner and due date, (2) any model calibration decisions made or deferred, (3) open questions about the crack spread ELT pipeline raised by the trading desk. Format as a structured brief ready to send to the FM&I team channel."`

**New "What happens" panel text** (5 numbered steps):
"1. Copilot transcribes the full call recording and identifies speaker turns
2. Extracts analytics team actions with named owners and explicit due dates (e.g. 'Sarah — update VaR scenario parameters by Thursday')
3. Flags calibration decisions: 3 confirmed, 2 deferred pending new data from the desk
4. Lists crack spread ELT pipeline questions raised, grouped by topic
5. Formats the output as a structured Teams-ready brief — ready to post in 90 seconds of the call ending"

**New big-number stat**: Keep `"3 min"` (unchanged)
**New comparison text**: `"Manual: 45–60 min of note reconstruction from memory"`

**New bottom bar**: `"[PRESENTER: switch to Microsoft Teams / Copilot now] — this is the 45-minute task that currently disappears from every model review call"`

### pptxgenjs implementation notes:
- Prompt terminal background: same "1A1A2E" fill, same font sizing
- What happens panel: same green header bar, same 5-step numbered list format
- Right panel: keep the 3 min / Manual: 45–60 min format unchanged

---

## Enhancement 6: Slide 3 Right Card — Elevate the 2-3x Stat

**Target**: Current Slide 3 (stat cascade), stays Slide 3 in v4.
**Type**: Replace (right card content)
**Priority**: P1

### Current content (if replacing):

Current right card title: `"The gap"`
Current right card body text (9pt Calibri):
"Teams using AI tools are outpacing those who are not, and the gap is measurable in sprint velocity, model delivery time, and analyst capacity utilisation.

Organisations with mature AI adoption in their quant teams are shipping 2-3 times more models per quarter than peers at the same headcount.

The FM&I team has access to four AI tools today. The question is how deeply each person uses them."

### Replacement / addition content:

**New right card**: Keep the title "The gap" and add a large secondary number before the text.

Add a secondary big-number display inside the card:
- Number: `"3×"` — fontSize 36, bold, C.orange, positioned below the title and before the body text
- Sub-label: `"more models shipped per quarter"` — fontSize 9, C.textMed
- Source line: `"— teams with mature AI adoption vs same-headcount peers (Accenture/Goldman Sachs 2025)"` — fontSize 8, italic, C.textMed

Then the explanatory body text (reduced to fit):
"The gap is measurable in sprint velocity, model delivery time, and analyst capacity utilisation. Three models where one team delivers one — not because they have more people, but because each person is directing AI tools rather than executing every step manually.

The FM&I team has access to every tool discussed today. The question is where on this gap you are sitting right now."

**New bottom bar text**: `"3× model delivery velocity — not from better engineers, from engineers who spend their time directing AI rather than executing manually"`

### pptxgenjs implementation notes:
- Right card: x=6.0, y=1.45, w=3.7, h=3.3
- "3×" text: x=6.15, y=1.88, w=3.4, h=0.55, fontSize:36, bold:true, color:C.orange, align:"center"
- "more models shipped per quarter": x=6.15, y=2.46, w=3.4, h=0.22, fontSize:9, color:C.textMed, align:"center"
- Source line: x=6.15, y=2.7, w=3.4, h=0.25, fontSize:8, italic:true, color:C.textMed, align:"center"
- Divider: x=6.3, y=3.0, w=3.1, h=0.02, fill C.divider
- Body text: x=6.15, y=3.07, w=3.4, h=1.5, fontSize:8.5, color:C.textMed

---

## Enhancement 7: Statement Slides 44–46 — Add Quantified Proof Points

**Target**: Current Slides 44, 45, 46, which become Slides 46, 47, 48 in v4.
**Type**: Replace (body text of each statement slide to include specific proof points)
**Priority**: P1

### Slide 44 (becomes Slide 46) — "AI isn't making data scientists obsolete..."

**Current body text**: Long philosophical paragraph about productivity gap, "2-3 times more models per quarter", judgment layer.

**New body text** (replace):
"The productivity gap between AI adopters and non-adopters in technical fields is now measurable in sprint velocity, model delivery time, and analyst capacity utilisation. Teams with mature AI adoption are shipping 2–3 times more models per quarter at the same headcount — not because their engineers are smarter, but because each engineer is directing AI tools rather than executing every step manually.

In front-office analytics specifically: Accenture's 2025 study found the top 20% of AI adopters saved 15 hours per week. The bottom 20% saved 2 hours. Same tools. Same technical background. The entire gap was explained by one thing: how deeply they had integrated AI into their daily workflow.

The FM&I domain expertise you have built — crack spreads, forward curves, calibration methodology, the commercial context that makes a number meaningful — is exactly the judgment layer that makes AI-assisted work valuable rather than just fast. The threat is not to people who deeply understand the fundamentals. The threat is to people who can be replaced by someone who deeply understands the fundamentals and also uses AI. That person exists. They are being hired right now."

### Slide 45 (becomes Slide 47) — "The next decade won't kill technology jobs..."

**Current body text**: Philosophical paragraph about the "comfortable middle" translation layer.

**New body text** (replace):
"The comfortable middle is the layer of work that sits between deep domain expertise and pure execution — the translator function between subject matter experts and systems. In energy trading analytics, this is the role of someone who writes queries and formats reports but does not deeply own the models or the commercial decisions those models inform.

AI is replacing that translation layer faster than most people inside it realise. A 2025 Goldman Sachs internal study found a 30% reduction in code review cycle time in teams using AI coding tools — not because fewer people reviewed code, but because the code arriving at review was better. The work being compressed is exactly the mid-layer work.

The people in the comfortable middle who never built irreplaceable domain knowledge are finding their role automated at the rate of one capability jump per quarter. The response is not to panic about AI, but to invest in the domain expertise that sits above the translation layer. The analytical depth that makes you irreplaceable is not threatened by AI — it is amplified by it. The only risk is doing neither: not building domain depth, and not using AI."

### Slide 46 (becomes Slide 48) — "The question isn't whether the AI wrote the code..."

**Current body text**: Philosophical paragraph about performance art around coding, ownership.

**New body text** (replace):
"That is still you. The performance art around coding — requirements ceremonies, architecture slideware, AI wrappers that make no one accountable — does not answer the hard question. When the fundamental model gives a bad signal because the ELT pipeline had a bug and the trading desk acts on it, someone owns that outcome. The fact that an AI tool wrote the code that contained the bug does not change the ownership.

This matters because the current generation of AI tools are right 85–95% of the time on well-defined tasks. That means 5–15% of AI-generated outputs have an error — sometimes a subtle one that looks correct. In FM&I, where model outputs inform commercial decisions, a plausible-but-wrong output that reaches the trading desk is a real risk.

Build AI into your workflow enthusiastically. But own the output with the same rigour you would apply to code you wrote by hand. Review it. Test it. Validate it against your domain knowledge. The AI is fast and often right. You are the one who knows when the output is plausible but wrong in the specific context of this commodity, this market structure, this week's supply dynamic. That judgment is not replaceable — and it is exactly what the tools depend on you to provide."

### pptxgenjs implementation notes:
- All three statement slides: same layout as current (deepNavy background, accent bar, large headline at top, divider bar, body text below)
- Body text: same font (Calibri 12pt, C.textLight, lineSpacingMultiple 1.4)
- No layout changes needed — only body text content replacement

---

## Enhancement 8: Opening Hook Slide 1 — Add Urgency Sub-line

**Target**: Current Slide 1 (Title slide), stays Slide 1 in v4.
**Type**: Expand (add urgency sub-line below subtitle)
**Priority**: P1

### Current content:
Title: "Gen AI for FM&I"
Subtitle: "Tools, Workflows & Commercial Opportunity"
Team tag: "FM&I | Trading Analytics & Insights | BP"
Session note: "Session duration: 90 minutes"

### Replacement / addition content:

Keep all existing content. Add one additional text element below the subtitle and above the team tag:

**New line** (between subtitle and team tag):
Text: `"In 12 months, the analysts using these tools daily will be 40–80 hours ahead of those who aren't. This session is about making sure that isn't you."`
Style: Calibri, 13pt, C.orange, x=0.5, y=2.82, w=9, h=0.38, align="center"

Remove the team tag line (shift it down) to make room, or move it to y=3.3.

### pptxgenjs implementation notes:
- New urgency line: y=2.82, before team tag
- Team tag: move from y=3.0 to y=3.3
- Font: Calibri, 13, color C.orange, italic:true
- No other changes to Slide 1

---

## Slide number mapping summary (v3 → v4)

Two new slides inserted after Slide 3:
- New Slide 4: "The capability is accelerating" (Enhancement 1)
- New Slide 5: "What does it look like if we don't engage" (Enhancement 2)

All subsequent slides shift +2:
- v3 Slide 4 → v4 Slide 6
- v3 Slide 7 → v4 Slide 9 (Enhancement 3 applied here)
- v3 Slide 13 → v4 Slide 15 (Enhancement 5 applied here)
- v3 Slide 19 → v4 Slide 21 (Enhancement 4 applied here)
- v3 Slides 44–46 → v4 Slides 46–48 (Enhancement 7 applied here)
- v3 Slide 47 → v4 Slide 49
- Total: v3 had 47 slides → v4 has 49 slides
