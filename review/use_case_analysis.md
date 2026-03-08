# Use Case Analysis — Presentation Creator Agent Team

**Analyst**: Agent 1 (Use Case Analyst)
**Date**: 2026-03-08
**Source**: `.claude_prompts/presentation-creator-prompt.md`

---

## 1. Stated Purpose & Value Proposition

The system is a **multi-agent prompt framework** that coordinates four specialised roles to produce professional presentations from a minimal topic brief. The stated value proposition is:

> "You take a topic, audience, and purpose as input and deliver complete, polished slide decks with speaker scripts in HTML, PDF, and/or PowerPoint formats."

The framework positions itself as a **one-prompt replacement** for the multi-hour workflow of: independent research → slide design → script writing → technical production. It targets output quality comparable to professional presentation consultants, grounded in named methodologies (Barbara Minto, Garr Reynolds, Nancy Duarte, Edward Tufte).

---

## 2. Target User

The prompt does not explicitly define a target user persona, but the design choices reveal the intended audience:

- **Primary**: Knowledge workers who create presentations regularly (product managers, consultants, engineers, sales professionals) but lack dedicated design/communications support.
- **Secondary**: AI practitioners who want a reusable prompt template for delegating presentation creation to an LLM agent.
- **Not targeted**: Professional designers or presentation specialists who would find the prescriptive rules constraining.

The system assumes the user can supply a meaningful topic brief (8 input fields) and can open an HTML file in a browser. No coding knowledge is required for HTML output; PPTX output requires Node.js/PptxGenJS.

---

## 3. Inputs Required vs Outputs Promised

### Inputs (from the YAML input schema)
| Field | Required? | Notes |
|---|---|---|
| `topic` | Required | The subject matter |
| `audience` | Required | Who will watch |
| `purpose` | Required | Desired audience outcome |
| `duration` | Required | Target length in minutes |
| `tone` | Required | Style register |
| `output_formats` | Required | html / pdf / pptx |
| `brand_colors` | Optional | Hex codes |
| `additional_context` | Optional | Specifics, data, requirements |

### Outputs Promised
1. **HTML**: Complete, self-contained reveal.js presentation. Single file. Speaker notes via `S` key. Print-to-PDF support. Works in any browser.
2. **PDF**: Via reveal.js `?print-pdf` URL parameter + Chrome print. Optional: Puppeteer/Playwright automation. At minimum: printed instructions.
3. **PPTX**: PptxGenJS structure or Node.js generation script. Speaker notes included.
4. **Speaker Script**: Embedded in HTML notes and/or provided as separate document with timing, transitions, engagement cues.

---

## 4. The Agent Pipeline

### Agent 1: Research & Content Strategist
- Deep-researches the topic (facts, stats, case studies, quotes)
- Identifies a single core message
- Builds audience profile (knowledge, concerns, motivations)
- Structures using Situation → Complication → Resolution (Minto Pyramid)
- Applies Rule of Three (3 main pillars)
- Per section: assertion + evidence + transition
- Creates full content outline: hook → 3 sections → CTA
- **Output**: Structured content document

### Agent 2: Slide Architect & Designer
- Selects design theme based on tone/audience
- Maps content to one of 12 slide type templates
- Defines visual hierarchy per slide
- Selects color palette from 4 named palettes or brand input
- Specifies typography, layout, whitespace, animation rules
- **Output**: Slide Design Specification

### Agent 3: Presentation Script Writer
- Writes speaker notes per slide in conversational voice
- Adds timing markers (pace targets: ~2 min/content slide)
- Includes transitions, pause markers, rhetorical questions
- Reviews for natural speaking rhythm
- Total timing validated against target duration
- **Output**: Complete Speaker Script

### Agent 4: Production Engineer
- Generates HTML with reveal.js, embedded CSS, full design system
- Generates PDF conversion instructions (or automates via Puppeteer)
- Generates PptxGenJS structure or Node.js script (if PPTX requested)
- Quality-checks all outputs
- **Output**: Final deliverable files

---

## 5. Quality Checklist Items (as specified)

### Content Quality (8 items)
1. Core message clear and repeated 3+ times
2. Every slide makes exactly one point
3. Data is accurate and sourced
4. No more than 6 words in topic-label slide titles (assertion titles are full sentences — exception acknowledged)
5. No bullet list exceeding 3 items
6. Opening hook is compelling (first 10 seconds)
7. Closing has clear, actionable CTA
8. Total slide count matches duration guidelines

### Design Quality (9 items)
1. Consistent color palette (max 3-4 colors)
2. Font sizes never below 18pt
3. Maximum 2 typefaces
4. All elements aligned to grid
5. 30%+ whitespace per slide
6. Images are high-quality and relevant
7. Charts labeled and annotated with key takeaway
8. Contrast ratios meet WCAG AA (4.5:1)
9. Consistent visual language (icons, images, colors)

### Script Quality (6 items)
1. Natural conversational tone (passes read-aloud test)
2. Speaker adds value beyond slide content
3. Timing totals match target duration
4. At least 2 stories or concrete examples
5. Transitions feel natural
6. Pause markers at key moments

### Technical Quality (6 items)
1. HTML opens in Chrome, Firefox, Safari
2. Speaker notes accessible via `S` key
3. Print-to-PDF produces one slide per page
4. PPTX opens in PowerPoint and Google Slides
5. All files self-contained
6. Responsive on different screen sizes

---

## 6. Five Canonical Use Cases

### Use Case A: Technical Pitch to Engineering Leadership (15 min)

**Scenario**: A senior engineer or engineering manager presents to a CTO, VP Engineering, or Staff Engineer audience to gain approval for a technical initiative (e.g., adopting a new framework, changing CI/CD pipeline, migrating to a new architecture).

**Input profile**:
- Audience: High technical literacy, skeptical of hype, time-constrained
- Purpose: Approval or buy-in
- Duration: 15 minutes
- Tone: Professional but direct
- Complexity: High — data, benchmarks, risk analysis expected

**Why this is a stress test**: The audience will reject vague claims. The content must include specific benchmarks, migration paths, risk mitigations, and a clear ask. Design must be restrained; script must sound like an engineer, not a salesperson.

---

### Use Case B: Sales Deck for Non-Technical Executives (10 min)

**Scenario**: A sales or business development professional presents a product or service to C-suite buyers who lack technical background. The goal is to generate interest and move to next steps.

**Input profile**:
- Audience: Low technical literacy, motivated by ROI, risk, and competitive positioning
- Purpose: Generate interest, move to next meeting or demo
- Duration: 10 minutes
- Tone: Professional, sales-oriented
- Complexity: Medium — business value, case studies, clear CTA

**Why this is a stress test**: Requires translating technical capabilities into business outcomes. The script must avoid jargon. The design must feel premium and confident. The CTA must be specific and low-friction.

---

### Use Case C: Educational Overview for Students/Beginners (20 min)

**Scenario**: An educator, developer advocate, or team lead introduces a complex topic (ML, distributed systems, security) to an audience with little prior knowledge.

**Input profile**:
- Audience: Low domain knowledge, curious, motivated to learn
- Purpose: Build foundational literacy; inspire further exploration
- Duration: 20 minutes
- Tone: Accessible and inspirational
- Complexity: Medium — must simplify without dumbing down; analogies critical

**Why this is a stress test**: The Rule of Three and Pyramid Principle must be adapted for pedagogical pacing rather than persuasion. The script needs more teaching moments, more analogies, and checkpoints for understanding.

---

### Use Case D: Startup Investor Pitch (5 min)

**Scenario**: A founder pitches to early-stage investors in a lightning format — a demo day, accelerator event, or first meeting.

**Input profile**:
- Audience: Experienced investors, high-value/low-attention audience
- Purpose: Generate enough interest for a follow-up meeting; not to close the deal
- Duration: 5 minutes
- Tone: Inspirational, confident, urgent
- Complexity: High in compression — every slide must do maximum work in minimum time

**Why this is a stress test**: The 5-7 slide count for a 5-minute presentation puts extreme pressure on slide efficiency. The narrative must cover problem, solution, market, traction, team, and ask in very few slides. The opening hook has zero margin for error.

---

### Use Case E: Internal Tool Adoption Proposal (10 min)

**Scenario**: A product manager or tech lead proposes adopting a new internal tool (e.g., a new project management system, observability platform, or AI coding assistant) to a mixed audience of managers and engineers.

**Input profile**:
- Audience: Mixed — technical and non-technical, moderate to high skepticism
- Purpose: Gain approval and voluntary adoption commitment
- Duration: 10 minutes
- Tone: Professional but collaborative ("we" language, not top-down)
- Complexity: Medium — requires current-state pain, proposed solution, adoption plan

**Why this is a stress test**: The mixed audience creates tension — technical depth vs. business framing. The script must navigate both registers. The narrative must include change management cues (addressing the "what's in it for me?" for both audiences).

---

## 7. Success Criteria per Use Case

### Measurement Framework

All use cases are assessed across 5 dimensions:

| Dimension | Weight | Description |
|---|---|---|
| Content Completeness | 25% | Required narrative sections present and logically structured |
| Design System Adherence | 25% | Checklist items from the prompt met |
| Script Quality | 20% | Timing, tone, conversational quality, examples present |
| Technical Deliverable | 20% | HTML/PPTX renders, notes accessible, no structural errors |
| End-to-End Coherence | 10% | Traceable narrative arc from hook to CTA |

---

### Use Case A — Technical Pitch (15 min) Success Criteria

**PASS thresholds**:
- Slide count: 10-14 slides (15 min / ~1.5 min per slide)
- Content completeness: Present — hook, problem definition, 3 technical pillars, risk analysis, migration plan, CTA
- Audience calibration: Script uses domain language (no jargon simplification that would condescend to engineers)
- Data slides: Minimum 2 data/chart slides with benchmarks or metrics
- Script quality: 2+ concrete technical examples or case studies; timing within ±15% of 15 min
- Design: Technical/Developer palette appropriate; code-style elements acceptable
- Technical: HTML renders, speaker notes present on every slide, no broken structure
- Coherence: SCR arc traceable (current pain → technical gap → proposed solution)

**FAIL conditions**:
- Fewer than 8 or more than 18 slides
- No specific technical data (pure narrative without numbers)
- Script that simplifies content to the point of condescension
- Missing CTA or vague CTA ("let's discuss" without specific next step)

---

### Use Case B — Sales Deck for Non-Technical Executives (10 min) Success Criteria

**PASS thresholds**:
- Slide count: 8-12 slides
- Content completeness: Hook, business problem, value proposition, 3 key benefits, social proof (customer/case study), CTA
- Audience calibration: Zero technical jargon; ROI/outcome framing throughout
- Business metrics: At least 1 quantified outcome (e.g., "X% cost reduction", "Y weeks saved")
- Script quality: Conversational, benefit-led, not feature-led; 2+ examples or stories
- Design: Sales/Marketing palette; premium feel; no cluttered slides
- Technical: HTML renders; notes present on every slide
- CTA: Specific and low-friction (book a demo, schedule a call — not "contact us")

**FAIL conditions**:
- Technical jargon unexplained
- No social proof or customer reference
- Generic CTA
- More than 50 words on any single slide

---

### Use Case C — Educational Overview for Students/Beginners (20 min) Success Criteria

**PASS thresholds**:
- Slide count: 14-20 slides
- Content completeness: Hook (why this matters), concept foundations (3 pillars), worked examples, common misconceptions addressed, further reading/CTA
- Audience calibration: Analogies present (minimum 2); no unexplained jargon; progressive complexity
- Teaching moments: At least 1 rhetorical question per pillar section; 1 summary/recap slide
- Script quality: Accessible tone; 3+ concrete examples; timing within ±15% of 20 min
- Design: Inspirational/Creative or Corporate palette; icon grids and visual metaphors preferred
- Technical: HTML renders; notes present on every slide

**FAIL conditions**:
- Unexplained jargon used as if audience knows it
- No analogies or concrete examples
- Linear list of facts with no narrative arc
- No engagement prompts in script

---

### Use Case D — Startup Investor Pitch (5 min) Success Criteria

**PASS thresholds**:
- Slide count: 5-8 slides
- Content completeness: Problem (visceral, personal), solution, market size, traction/proof, team, ask
- Hook: Opening hook established within first 60 seconds; memorable
- Compression: Every slide makes one point only; no slide with >30 words of body text
- Script quality: Confident, urgent tone; story-driven; timing within ±15% of 5 min
- Design: High visual impact; Statistics/Big Number slides used for traction data
- Technical: HTML renders; notes present on every slide
- Coherence: The ask is specific (amount, terms, use of funds) — not vague

**FAIL conditions**:
- Fewer than 5 slides or more than 8 slides
- Missing any of: problem, solution, market, team, ask
- Vague or missing ask
- Script sounds read, not spoken

---

### Use Case E — Internal Tool Adoption Proposal (10 min) Success Criteria

**PASS thresholds**:
- Slide count: 8-12 slides
- Content completeness: Current pain (quantified), proposed tool overview, 3 adoption benefits, implementation plan, cost/risk, CTA (approval/pilot)
- Audience calibration: Addresses both technical and non-technical concerns; includes "what changes for you" framing
- Change management: Adoption plan present (rollout phases, training, support); objection handling evident in script
- Script quality: Collaborative "we" tone; 2+ examples; timing within ±15% of 10 min
- Design: Corporate/Professional palette; timeline/process slides present for rollout
- Technical: HTML renders; notes present on every slide

**FAIL conditions**:
- No quantified current-state pain
- Missing adoption/rollout plan
- Script that sounds like a top-down decree rather than collaborative proposal
- No risk/cost acknowledgment

---

## 8. Universal Pass/Fail Thresholds (All Use Cases)

These thresholds apply regardless of use case:

```
UNIVERSAL PASS thresholds:
- Slide count within ±2 of the duration-implied target
- 100% of slides have speaker notes in <aside class="notes"> tags
- 0 slides with >50 words of body text (body = non-title, non-notes content)
- HTML opens without console errors in Chrome
- Narrative arc traceable: opening hook → 3-pillar structure → clear CTA
- Design token consistency: ≥90% of slides use defined CSS variables (not hard-coded inline values)
- Speaker script timing estimate accurate within ±15% of target duration
- No slide titles that are pure topic labels (minimum: noun phrase with implication; ideal: full-sentence assertion)
```

```
UNIVERSAL FAIL conditions:
- HTML file has syntax errors or does not display in Chrome
- Any slide missing speaker notes
- More than 25% of slides have >50 words of body text
- No discernible CTA in closing
- Core message not repeated (appears only once)
- Slide count off by more than 3 from target
```
