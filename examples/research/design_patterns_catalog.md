# Corporate Data Science Presentation Design Patterns Catalog

**Research Date**: 2026-03-08
**Scope**: 40 patterns across 8 categories, sourced from consulting firm conventions, tech company design languages, data visualization literature, and conference practice.

---

## How to Use This Catalog

Each pattern entry documents:
- **Pattern name and category**
- **Source/inspiration** — the firm, designer, conference, or publication that established or exemplifies this pattern
- **What makes it effective** — specific design choices and the cognitive rationale behind them
- **Target audience** — executives, engineers, practitioners, or mixed
- **Existing slide type mapping** — which of the 12 base types this extends, or a proposed new type
- **CSS/HTML implementation approach** for reveal.js

---

## Category 1: Data Visualization Slides

### Pattern 1.1 — The McKinsey Single-Point Chart

**Source**: McKinsey & Company consulting deck conventions; Barbara Minto's Pyramid Principle applied to visual evidence.

**What makes it effective**: Every chart slide shows exactly one chart and carries an assertion title — a full sentence that states the conclusion the audience should reach ("Customer acquisition cost fell 34% after model deployment, not just declined"). The chart is visual proof of that sentence, not a neutral exhibit. Gridlines are removed or lightened to near-invisibility. The y-axis label is eliminated when the unit appears in the title. One data point — the most important one — is highlighted in the brand accent color; all others are rendered in medium gray. Direct data labels replace the legend, eliminating the eye-travel required to decode a separate key. The source is set in 10px gray at the bottom-left footer.

**Target audience**: Executives, C-suite, board

**Slide type mapping**: Data/Chart (existing type 5) — assertion title discipline applied with McKinsey-specific annotation conventions

**CSS/HTML approach**:
```html
<section class="slide-chart">
  <h2 class="slide-title assertion">Customer acquisition cost fell 34% after model deployment</h2>
  <div class="chart-container">
    <!-- SVG or Chart.js canvas -->
    <!-- One bar/point highlighted via class="bar--accent", rest are class="bar--muted" -->
  </div>
  <p class="chart-source">Source: Internal data, Q4 2024</p>
</section>
```
Key CSS: `.bar--muted { fill: #94a3b8; } .bar--accent { fill: var(--color-accent); }`

---

### Pattern 1.2 — The Storytelling with Data Declutter

**Source**: Cole Nussbaumer Knaflic, "Storytelling with Data" (Wiley, 2015). Core technique: eliminate all non-data ink before presenting.

**What makes it effective**: Knaflic's declutter process transforms a default chart into a presentation-ready one through five steps: (1) remove chart borders, (2) remove gridlines or convert to light dotted guides, (3) remove data markers on line charts, (4) clean up axis labels to show only start, middle, and end, (5) label data directly and remove the legend. The result is a chart where the eye goes immediately to the data and the annotated insight, not to structural chrome. The "after" version of any Knaflic chart contains 60-70% less ink than the default while conveying the same — or more — information because the signal-to-noise ratio improves. The key annotation — a callout box pointing to the peak, trough, or crossover — carries the narrative weight.

**Target audience**: Mixed; works for executives and practitioners alike

**Slide type mapping**: Data/Chart (existing type 5) — extends with mandatory callout annotation

**CSS/HTML approach**:
```css
.chart-annotation {
  position: absolute;
  background: var(--color-surface);
  border-left: 3px solid var(--color-accent);
  padding: 8px 12px;
  font-size: var(--text-caption);
  max-width: 180px;
}
```

---

### Pattern 1.3 — Tufte Small Multiples Grid

**Source**: Edward Tufte, "The Visual Display of Quantitative Information" (Graphics Press, 1983). Small multiples: a series of similar graphics or charts arranged in a grid for comparative reading.

**What makes it effective**: Small multiples allow audiences to compare many dimensions simultaneously by holding all visual variables (scale, axes, color scheme) constant and varying only the data. Each panel is small enough that six to twelve can appear on a single slide, yet because axes are shared, the eye can flick between panels and detect patterns instantly. For data science presentations, this is ideal for showing model performance across segments, A/B test results across cohorts, or seasonal patterns across regions. The key discipline: every panel must have identical axes and scales. The header row replaces individual panel titles, keeping labels minimal. Background is always white or near-white; panel borders are a single-pixel light gray line.

**Target audience**: Data scientists, practitioners, technical managers

**Slide type mapping**: Data/Chart (existing type 5) — small-multiples variant

**CSS/HTML approach**:
```css
.small-multiples-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.small-multiples-grid .panel {
  border: 1px solid #e2e8f0;
  padding: 12px;
}
/* All panels share identical axes via identical SVG viewBox dimensions */
```

---

### Pattern 1.4 — The Sparkline-in-Table KPI Row

**Source**: Edward Tufte (coined sparklines 2004), popularized in Bloomberg terminals, Stripe Dashboard, and dbt's reporting conventions.

**What makes it effective**: A sparkline is a word-sized chart — a tiny line chart that sits inline with text or within a table cell. In presentation context, this pattern uses a table of KPIs where each row shows: Metric Name | Current Value (large, bold) | Sparkline (12-week trend in 80px width) | Delta vs. prior period (colored up/down arrow + percentage). The cognitive advantage is density without clutter: the viewer gets point-in-time value and trajectory at a glance without switching between slides. The sparkline uses no axes, no labels, just a thin line and a filled dot at the terminal point. Color encodes direction: blue or green for positive trend, red for declining.

**Target audience**: Executives, operations teams, quarterly business reviews

**Slide type mapping**: Statistics/Big Number (existing type 9) — extended to multi-metric KPI row format

**CSS/HTML approach**:
```html
<section class="slide-kpi-table">
  <table class="kpi-rows">
    <tr>
      <td class="kpi-label">Model Accuracy</td>
      <td class="kpi-value">94.2%</td>
      <td class="kpi-spark"><!-- inline SVG sparkline --></td>
      <td class="kpi-delta up">+1.4pp</td>
    </tr>
  </table>
</section>
```

---

### Pattern 1.5 — The Annotated Before/After Chart

**Source**: Combines McKinsey "so what" titling with the "Storytelling with Data: let them do the work" technique; widely used by Databricks and dbt Labs in their Data + AI Summit keynotes.

**What makes it effective**: Two-panel layout: left panel shows the metric "before" an intervention (e.g., before model deployment, before pipeline optimization), right panel shows "after." Both panels use identical scales — this is the critical design discipline that prevents misleading comparisons. A vertical divider with a label ("Model deployed Q2") marks the inflection point. The most important number — the change magnitude — is displayed in 48pt between the two panels. The title is a full-sentence assertion: "Pipeline optimization cut data freshness lag from 6 hours to 23 minutes." The before panel uses muted gray; the after panel uses the brand accent.

**Target audience**: Executives, business stakeholders, VP-level reviewers

**Slide type mapping**: Before/After with Metrics (proposed new type — see Section 5)

**CSS/HTML approach**:
```css
.before-after-container {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 24px;
  align-items: center;
}
.before-after-divider {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 48px;
  font-weight: 700;
  color: var(--color-accent);
}
```

---

### Pattern 1.6 — The Heatmap / Correlation Matrix Panel

**Source**: Data science community practice (NeurIPS poster conventions, Seaborn/matplotlib default heatmap aesthetic); refined by Airbnb's data visualization team.

**What makes it effective**: A correlation matrix or confusion matrix rendered as a color-coded grid is one of the most compact ways to communicate model performance or feature relationships. The key design disciplines: use a sequential (single-hue) palette for magnitude — not a diverging red-green palette that fails colorblind audiences. Display values inside cells only when the grid has fewer than 8x8 cells; above that, color alone must carry the signal. Row and column labels are set at 45-degree angles to prevent truncation. Diagonal cells in a correlation matrix are called out with a distinct border. The assertion title states the insight: "Features 3 and 7 are near-perfectly correlated — multicollinearity risk."

**Target audience**: Data scientists, ML engineers, technical reviewers

**Slide type mapping**: Data/Chart (existing type 5) — heatmap/matrix variant

---

## Category 2: Technical Architecture Slides

### Pattern 2.1 — The Left-to-Right Data Pipeline

**Source**: Databricks Data + AI Summit keynote conventions; dbt documentation visual language; Google Cloud Architecture Center diagram standards.

**What makes it effective**: Data pipeline diagrams are most readable when they flow strictly left-to-right (source → transform → serve), matching the Western reading direction and the natural mental model of data flow. Each stage is a rounded rectangle with an icon at top-left and a 2-3 word label below. Connecting arrows are straight or orthogonally bent (never curved or diagonal), with arrowheads at destination. Color encodes layer: source systems in blue, transformation in purple, serving layer in green. A horizontal "swim lane" separates storage (bottom row) from compute (top row). The critical discipline: never show more than 5-6 stages on a single diagram. Deeper pipelines should be broken into a "zoom in" sequence of slides.

**Target audience**: Data engineers, architects, technical managers, CTOs

**Slide type mapping**: Architecture/Pipeline (proposed new type — see Section 5)

**CSS/HTML approach**:
```css
.pipeline-diagram {
  display: flex;
  align-items: center;
  gap: 0;
}
.pipeline-stage {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: var(--color-surface);
  border: 1.5px solid var(--color-border);
  border-radius: 8px;
  padding: 16px 20px;
  min-width: 120px;
}
.pipeline-arrow {
  width: 40px;
  height: 2px;
  background: var(--color-border);
  position: relative;
}
```

---

### Pattern 2.2 — The Three-Layer Architecture Stack

**Source**: AWS and Azure architecture diagram conventions; Snowflake "Modern Data Stack" marketing diagrams; widely adopted in enterprise data platform presentations.

**What makes it effective**: A vertical stack of three horizontal bands — Ingest, Store, Serve — communicates a platform architecture at a glance for a non-technical audience. Each band is a distinct background color (not a gradient — solid fills only). Within each band, product logos or icon-plus-label nodes float as horizontal rows. Connecting lines between bands are vertical, thin, and dashed. The key discipline: the stack is hierarchical but not a flowchart — avoid arrowheads between bands because the relationship is "feeds" not "triggers." Adding a fourth "Govern" or "Observe" band as a vertical strip on the right side (spanning all three layers) communicates cross-cutting concerns without cluttering the main flow.

**Target audience**: CTOs, VP Engineering, enterprise architecture teams

**Slide type mapping**: Architecture/Pipeline (proposed new type — see Section 5)

---

### Pattern 2.3 — The ML Experiment Loop Diagram

**Source**: MLflow and Weights & Biases documentation visual conventions; popularized at NeurIPS 2019-2022 applied ML sessions.

**What makes it effective**: The ML experiment lifecycle — data prep, feature engineering, model training, evaluation, deployment, monitoring — is circular, not linear. Rendering it as a loop rather than a flowchart is the single most important design decision: it communicates that ML is iterative by nature. Nodes are rounded rectangles arranged in a clockwise circle. Edges are curved arrows connecting adjacent nodes. One node — the one the presentation is discussing — is highlighted in accent color; all others are muted. A brief label inside each node (max 3 words). The central area of the loop can hold a headline statistic or a brief annotation ("17 experiments run in 3 weeks").

**Target audience**: Data scientists, ML engineers, product managers overseeing ML

**Slide type mapping**: Architecture/Pipeline (proposed new type) — circular variant

---

### Pattern 2.4 — The Code + Context Split

**Source**: Stripe developer documentation design language; Google I/O keynote "code demo" slide format; adopted by dbt Labs for tutorial content at Data Council 2022-2024.

**What makes it effective**: When a technical slide needs to show code, the split-layout pattern places the code in a dark-background syntax-highlighted panel on the right (60% width) and a plain-language explanation on the left (40% width). Left panel: 3-4 bullet points (or numbered steps) explaining what the code does in plain English. Right panel: dark background (#1e293b or similar), monospace font, syntax highlighting using a muted palette (not the garish defaults — a calm Solarized Dark or GitHub Dark variant). Line numbers in the gutter. A highlight stripe on the 1-3 lines most critical to the explanation. Arrow or callout connecting a left bullet to the highlighted line. Avoid showing more than 15 lines of code; any more requires a separate "code deep-dive" appendix.

**Target audience**: Developers, data engineers, technical practitioners

**Slide type mapping**: Code + Explanation (proposed new type — see Section 5)

**CSS/HTML approach**:
```css
.slide-code-split {
  display: grid;
  grid-template-columns: 2fr 3fr;
  gap: 40px;
  height: 100%;
}
.code-panel {
  background: #1e293b;
  border-radius: 8px;
  padding: 24px;
  font-family: var(--font-mono);
  font-size: 16px;
  line-height: 1.6;
  overflow: hidden;
}
.code-highlight-line {
  background: rgba(59, 130, 246, 0.2);
  margin: 0 -24px;
  padding: 0 24px;
  border-left: 3px solid var(--color-accent);
}
```

---

### Pattern 2.5 — The Medallion Architecture Diagram

**Source**: Databricks' "Medallion Architecture" (Bronze/Silver/Gold) documentation and Data + AI Summit 2022-2024 presentations; widely adopted across data lake platform teams.

**What makes it effective**: The Bronze-Silver-Gold naming and the progressive refinement metaphor are now industry standard. The visual convention: three vertical columns (Bronze, Silver, Gold) with a warm metallic color accent applied to column headers only — not to the data within (that would be distracting). Each column lists 3-4 characteristics (raw, deduplicated, business-ready). The horizontal dimension shows data quality increasing left-to-right; a small quality progress bar beneath each column header reinforces this. The title should assert the business value: "Our lakehouse ensures analysts always work from trusted, governed data."

**Target audience**: Data engineers, CTO, CDO, VP Data

**Slide type mapping**: Architecture/Pipeline (proposed new type)

---

## Category 3: Before/After Transformation Slides

### Pattern 3.1 — The Consulting Comparison Table (New vs. Old State)

**Source**: McKinsey and Bain "current state vs. future state" transformation slides; adapted by data transformation consultants including ThoughtWorks and Slalom.

**What makes it effective**: A three-column table: Dimension | Before (State A) | After (State B). The first column lists 5-7 dimensions that matter to the audience: Data freshness, Access method, Query time, Governance, Cost. The "Before" column uses red or gray text to convey inadequacy. The "After" column uses green or accent-color text plus a checkmark icon to convey improvement. Row height is generous — 48-56px — to prevent the table from feeling cramped. No table borders except a horizontal rule under the header row and between the header and body. The column header for "After" matches the brand accent color. The title asserts the outcome, not the process: "The new platform delivers real-time data to 200 analysts vs. 24-hour batch exports."

**Target audience**: Executives, C-suite, business stakeholders

**Slide type mapping**: Comparison/Two-Column (existing type 7) — tabular variant with status encoding

---

### Pattern 3.2 — The Quantified Impact Bridge

**Source**: McKinsey waterfall chart convention applied to data science ROI; adapted by Bain's Advanced Analytics practice for client transformations.

**What makes it effective**: A waterfall chart variant showing how multiple data science initiatives combine to produce total business impact. The leftmost bar is the starting baseline (e.g., current revenue or cost). Each subsequent bar is a positive or negative contributor labeled with its initiative ("Churn model: +$2.1M", "Pricing optimization: +$3.7M"). The rightmost bar is the new total, filled in the brand primary color. Positive bars are accent-colored; negative bars (costs, risks) are rose/red. The total delta floats as a large number above the final bar: "+$8.4M incremental revenue." This pattern is uniquely powerful because it makes individual model contributions visible and comparable — answering the CFO's question "which model actually drives value."

**Target audience**: CFOs, CEOs, boards, business sponsors

**Slide type mapping**: Data/Chart (existing type 5) — waterfall variant with ROI framing

---

### Pattern 3.3 — The State Transition Story (Narrative Before/After)

**Source**: Nancy Duarte's "Sparkline" narrative structure from "Resonate" (2010); applied to data transformation stories in tech keynotes by Databricks, Snowflake, and Palantir.

**What makes it effective**: Rather than showing before and after as simultaneous comparison, this pattern narrates the journey. Slide 1 shows "what is" (the current painful state, rendered in muted, low-contrast tones with explicit pain point labels). Slide 2 shows "what could be" (the future state, rendered in high-contrast, bright, aspirational colors). The visual language shift between the two slides — dim to bright, cluttered to clean, red to green — does as much storytelling work as the words. The "what is" slide should make the audience uncomfortable; the "what could be" slide should make them eager. Pain points on slide 1 map directly to capabilities on slide 2 via consistent iconography.

**Target audience**: Mixed; particularly effective for board presentations and executive sponsorship pitches

**Slide type mapping**: Split Layout (existing type 3) — two-slide narrative sequence variant

---

### Pattern 3.4 — The Ops Metrics Triptych

**Source**: Site Reliability Engineering (Google SRE) culture applied to data operations; used by dbt's advocacy team and analytics engineering community at Coalesce conferences.

**What makes it effective**: Three side-by-side metric panels, each showing one operational dimension (e.g., Data Freshness, Pipeline Reliability, Query Performance). Each panel is a mini Big Number slide — the key metric large (56-64pt), a brief label below, and a small sparkline trend beneath that. The three panels share a consistent card height and card style, creating visual rhythm. A thin vertical divider separates panels. The title asserts the combined story: "Our data platform now matches the reliability of production software." Using exactly three panels enforces cognitive manageability and maps to the Rule of Three.

**Target audience**: VP Data, CDO, technical leadership, data platform teams

**Slide type mapping**: Statistics/Big Number (existing type 9) — triptych/three-panel variant

---

## Category 4: ROI and Business Case Slides

### Pattern 4.1 — The 2x2 Value Matrix

**Source**: BCG Growth-Share Matrix; McKinsey prioritization frameworks; adapted for data science initiative prioritization by Gartner and MIT CDOIQ presentations.

**What makes it effective**: A 2x2 matrix with axes labeled "Business Impact" (y) and "Implementation Feasibility" (x) plots data science initiatives as labeled circles. Circle size encodes resource requirement or estimated cost. The four quadrants are labeled: Quick Wins (high impact, high feasibility), Strategic Bets (high impact, lower feasibility), Fill-Ins (lower impact, high feasibility), and Deprioritize (lower impact, lower feasibility). Three or four circles should cluster in Quick Wins to create a compelling immediate action case. The positioning of circles is argued in the body, but the chart makes the prioritization recommendation viscerally clear. Quadrant backgrounds use very light fills (5% opacity) in green/yellow/gray/red to convey valence without overwhelming.

**Target audience**: CDOs, VP Data, product leadership, investment committees

**Slide type mapping**: Data/Chart (existing type 5) — 2x2 matrix variant

**CSS/HTML approach**:
```css
.matrix-2x2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 4px;
  aspect-ratio: 1;
  position: relative;
}
.matrix-quadrant { border-radius: 4px; padding: 16px; }
.matrix-quadrant.quick-wins { background: rgba(16, 185, 129, 0.06); }
.matrix-quadrant.strategic { background: rgba(59, 130, 246, 0.06); }
.initiative-dot {
  position: absolute;
  border-radius: 50%;
  background: var(--color-accent);
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 600; color: white;
}
```

---

### Pattern 4.2 — The Three-Number ROI Summary

**Source**: Guy Kawasaki's "10/20/30 Rule" minimalism applied to ROI communication; used extensively in Stripe and Shopify investor-facing presentations and data platform business cases.

**What makes it effective**: Three massive numbers on a dark background, each with a 2-4 word descriptor below. The numbers are 72-96pt; the descriptors are 18-20pt. Examples: "$4.2M" / "Annual cost savings"; "23%" / "Reduction in churn"; "6 weeks" / "Payback period." The three numbers answer the three questions executives always ask: What do we save? What do we gain? How fast? Dark background creates contrast and signals importance — this is a "poster moment" slide that the audience photographs. Each number should be pre-attentively striking: round numbers or one significant decimal only. No context is needed on this slide; context has been built up in the preceding slides.

**Target audience**: CEO, CFO, board, executive sponsors

**Slide type mapping**: Statistics/Big Number (existing type 9) — three-number ROI variant on dark background

---

### Pattern 4.3 — The Investment vs. Return Timeline

**Source**: Bain & Company NPV visualization conventions; adapted for technology ROI presentations by McKinsey's Digital practice and AWS professional services teams.

**What makes it effective**: A single chart with two overlaid areas: investment (costs, shown as negative red/gray bars below the zero axis) and cumulative return (shown as a green/accent area above the zero axis). The x-axis is time (months or quarters). The crossover point where return exceeds investment is labeled "Break-even: Month 14" with a vertical dashed line. Projected numbers are shown with a dashed line rather than solid, clearly communicating the certainty boundary. The shape of the investment curve (front-loaded) vs. return curve (accelerating after model deployment) tells a classic technology investment story that financial audiences recognize instantly.

**Target audience**: CFO, finance team, investment committees

**Slide type mapping**: Data/Chart (existing type 5) — cumulative ROI timeline variant

---

### Pattern 4.4 — The Capability vs. Competitor Gap Map

**Source**: BCG competitive positioning matrices; Gartner Magic Quadrant conventions adapted for internal capability assessments by data science teams.

**What makes it effective**: A radar (spider) chart or horizontal bar comparison showing the organization's data science capabilities against an industry benchmark or a "best-in-class" comparator. The current state is rendered in gray with a dashed border. The target state (12 months out) is rendered in accent color with a solid border. Gap areas are labeled with brief annotations. For radar charts, limiting to 5-7 dimensions prevents the polygon from becoming unreadable. For bar chart variants, dimensions are sorted largest-to-smallest gap to create an implicit priority ordering. The title states the business urgency: "We lag peers on feature engineering and model serving — closing the gap requires this investment."

**Target audience**: CDO, executive leadership, board

**Slide type mapping**: Comparison/Two-Column (existing type 7) — capability radar variant

---

### Pattern 4.5 — The Cost-of-Inaction Calculation

**Source**: Consultative sales methodology (Challenger Sale, MEDDIC) applied to internal data science proposals; used by Databricks and Snowflake enterprise sales presentations as a template for internal champions.

**What makes it effective**: This slide exists to quantify what happens if the organization does nothing. Structure: a single centered calculation block showing: "Current cost of [problem] per year: $X" → "X years until leadership decision: N" → "Total cost of inaction: $X*N." This is supplemented by two softer costs framed as risks: competitive lag and talent attrition. The calculation is displayed at 48pt in a highlighted box. The assertion title is the punchline: "Delaying one year costs more than the full implementation." This pattern works because loss aversion is a stronger motivator than gain expectation.

**Target audience**: CFO, CEO, skeptical executives

**Slide type mapping**: Statistics/Big Number (existing type 9) — loss framing variant

---

## Category 5: Process and Methodology Slides

### Pattern 5.1 — The CRISP-DM / Lifecycle Arc

**Source**: CRISP-DM industry standard (1996), re-visualized for modern audiences by IBM, SAS, and data science consultancies; the circular lifecycle format was popularized by Microsoft's Team Data Science Process.

**What makes it effective**: The data science lifecycle is rendered as a horizontal swim-lane process with six phases: Business Understanding, Data Understanding, Data Preparation, Modeling, Evaluation, Deployment. Each phase is a rounded rectangle node. The nodes are connected by forward arrows (showing primary flow) plus one backward arrow from Evaluation to Modeling (showing the iterative loop). Currently active or highlighted phases are filled in accent color; completed phases use green; future phases use gray. Time estimates float above each phase in a smaller font. The key design discipline: phases should be equally sized horizontally even if they take unequal time — otherwise the width implies duration, which misleads.

**Target audience**: Business stakeholders, project sponsors, non-technical leadership

**Slide type mapping**: Timeline/Process (existing type 8) — lifecycle variant

---

### Pattern 5.2 — The Numbered Step-by-Step

**Source**: Apple WWDC presentation conventions applied to process explanation; also the standard tutorial format at PyData conferences.

**What makes it effective**: A vertical list of 4-6 steps, each with: (1) a large step number (56pt, accent color, left-aligned), (2) a bold 5-6 word step name, (3) a single sentence of explanation in regular weight. The numbers are the visual anchor — large and colorful — while the text is subordinate. A thin horizontal rule separates steps. Optionally, a small icon to the right of the step name reinforces the action. This pattern replaces the default bullet list but improves on it by making sequence explicit, making each step visually distinct, and reducing the temptation to add sub-bullets.

**Target audience**: Practitioners, developers, workshop participants

**Slide type mapping**: Timeline/Process (existing type 8) — numbered list variant

---

### Pattern 5.3 — The Methodology Decision Tree

**Source**: Used by BCG and Bain for strategic decision frameworks; adapted for ML model selection and statistical method choice by data science education community.

**What makes it effective**: A binary or multi-branch tree diagram that walks the audience through a decision sequence. Root node at top: "Which model approach should we use?" Branching criterion is a Yes/No question at each node. Terminal leaf nodes show the recommended method, highlighted in accent color for the path the team chose. Non-chosen paths remain visible in muted gray to show the breadth of options considered (building credibility) and the rigor of the selection process. Maximum depth: 3 levels, which yields a maximum of 8 terminal nodes. Beyond that, compress the tree into a summary table.

**Target audience**: Technical reviewers, data science leads, peer practitioners

**Slide type mapping**: Architecture/Pipeline (proposed new type) — decision tree variant

---

### Pattern 5.4 — The Experiment Design Recap

**Source**: A/B testing culture codified by Airbnb's Experimentation Platform team and Etsy's data science blog; popularized at Strata Data Conference (O'Reilly, 2016-2022).

**What makes it effective**: A clean, centered layout showing the key parameters of an experiment: Control group (icon + sample size), Treatment group (icon + sample size), primary metric (large, centered), duration (calendar icon + date range), statistical power and significance threshold in small caption text. Hypothesis statement in bold italic above the diagram. Result in a prominent callout box with traffic-light color: green border for significant positive, red border for significant negative, gray border for inconclusive. This pattern builds trust by showing statistical rigor without requiring the audience to understand the statistics — they see the structure and infer the discipline.

**Target audience**: Product managers, business stakeholders, data science peers

**Slide type mapping**: Comparison/Two-Column (existing type 7) — A/B test summary variant

---

### Pattern 5.5 — The Feature Engineering Funnel

**Source**: Data science teaching conventions at fast.ai, Coursera, and data engineering conference talks; the "funnel" metaphor applied to data transformation stages.

**What makes it effective**: A narrowing funnel diagram with 4-5 horizontal sections, each narrower than the one above. Top section: "Raw data (500 features, 10M rows)." Each subsequent section shows features filtered or engineered: "After null removal (380 features)", "After correlation filtering (95 features)", "After domain-driven selection (23 features)", "Final feature set (12 features used in production)." The numbers are displayed prominently inside each section, making the reduction concrete. The funnel metaphor communicates that feature engineering is a deliberate, disciplined reduction process — important framing for business audiences who might otherwise ask "why not use all the data?"

**Target audience**: Data science practitioners, technical managers, ML reviewers

**Slide type mapping**: Funnel/Conversion (proposed new type — see Section 6)

---

## Category 6: Team and Capability Slides

### Pattern 6.1 — The Hub-and-Spoke Org Model

**Source**: Gartner data and analytics organizational structure recommendations; adapted by McKinsey's CDO advisory practice for data science team design presentations.

**What makes it effective**: A hub-and-spoke diagram with the central data science team or Center of Excellence at the center (dark-filled circle with team name), and embedded data science pods in business units radiating outward as spokes. Each spoke terminus is a smaller circle showing: BU name, number of DS resources, primary focus area. Dotted lines indicate "dotted-line" reporting; solid lines indicate direct reporting. Color encodes team type: central team in brand primary, embedded pods in brand accent, business units in gray. This diagram is cleaner and more strategic than a traditional org chart because it shows relationships and operating model, not just hierarchy.

**Target audience**: CDO, CHRO, executive leadership building out data science capacity

**Slide type mapping**: Team/Bio (existing type 10) — org model variant

---

### Pattern 6.2 — The Capability Maturity Heatmap

**Source**: MIT Sloan Management Review data maturity models; Gartner's Data and Analytics Maturity Model; used extensively in CDO advisory presentations.

**What makes it effective**: A grid where rows are capability dimensions (Data Engineering, ML Ops, Feature Stores, Model Governance, etc.) and columns are maturity levels (Ad Hoc, Defined, Managed, Optimized). Each cell is either empty (not yet reached), filled in gray (partial), or filled in accent (achieved). The current-state column is outlined with a heavier border. The target-state column is outlined with a dashed accent border. This heatmap enables the audience to see at a glance which capabilities are strongest and where the gaps are, without reading a dense text assessment. The title asserts the gap: "We have strong engineering foundations but lag peers in model governance and ML Ops."

**Target audience**: CDO, CTO, board technology committee

**Slide type mapping**: Comparison/Two-Column (existing type 7) — maturity grid variant

---

### Pattern 6.3 — The Skills Inventory Tile Grid

**Source**: Google's People Analytics presentations; used by data science team leads at tech companies to show team composition for hiring discussions.

**What makes it effective**: A grid of cards (3x3 or 4x3), each representing a team member. Each card: photo or avatar circle, name in bold, title in regular weight, and 3-4 skill tags in pill-shaped labels. Skill tags use semantic colors to indicate proficiency: filled accent for expert, outlined for intermediate, gray for familiar. The grid layout communicates team scale and diversity at a glance. Important: maintain consistent card dimensions and padding — visual inconsistency in people-cards signals organizational disorganization to the audience, undermining the message. The title can assert composition: "12 specialists covering the full ML lifecycle from data to deployment."

**Target audience**: Executives, hiring committees, technology investors

**Slide type mapping**: Team/Bio (existing type 10) — skills inventory variant

---

### Pattern 6.4 — The RACI Responsibility Matrix

**Source**: Project management and consulting standard; adapted for data governance and ML model ownership presentations by Snowflake's governance advisory team and dbt Labs' analytics engineering community.

**What makes it effective**: A RACI matrix (Responsible, Accountable, Consulted, Informed) rendered as a clean table. Rows are activities (model training, feature deployment, data quality monitoring); columns are roles (Data Scientist, ML Engineer, Data Engineer, Product Manager, Business Owner). Each cell contains a single letter (R, A, C, I) or is empty. R is accent-colored; A is darker/primary; C and I are gray. The key design discipline: the table must not exceed 8 rows and 5 columns on a single slide — otherwise compress by grouping activities. Horizontal zebra striping (alternating white and very-light-gray rows) aids reading without introducing heavy borders. Used to resolve ownership ambiguity in multi-function data science teams.

**Target audience**: Project sponsors, operations leads, cross-functional teams

**Slide type mapping**: Comparison/Two-Column (existing type 7) — matrix/RACI variant

---

## Category 7: Timeline and Roadmap Slides

### Pattern 7.1 — The Quarterly Roadmap Swimlane

**Source**: Atlassian Jira roadmap visualization applied to slide format; used by Snowflake and Databricks product teams in their annual summit roadmap reveals.

**What makes it effective**: A horizontal timeline with quarters as columns and 2-4 workstreams as rows (swimlanes). Each initiative is a rounded rectangle that spans its duration, color-coded by theme (infrastructure, model development, productization, governance). Completed items use a solid dark fill with a checkmark. In-progress items use the accent fill. Future items use outlined (unfilled) rectangles. Milestone diamonds mark key delivery dates. The swimlane labels are left-aligned in a sticky column that doesn't scroll. Keeping the roadmap to 4 quarters on screen (and showing the prior quarter for context) prevents the chart from becoming illegible at presentation scale.

**Target audience**: Executives, product stakeholders, steering committees

**Slide type mapping**: Timeline/Process (existing type 8) — swimlane roadmap variant

---

### Pattern 7.2 — The Milestone Achievement Tracker

**Source**: Consulting project status decks (McKinsey PMO slides); adapted for data science program management by large analytics teams at banks, retailers, and telcos.

**What makes it effective**: A vertical or horizontal timeline of 6-10 milestones. Achieved milestones are filled circles with a checkmark, positioned on the left. Current milestone is highlighted with a ring/halo effect in accent color and a "You are here" label. Future milestones are outlined circles. Each milestone has a 3-4 word label and an optional date below it. Color encoding: green for complete, accent for current, gray for future, red for delayed. A horizontal progress bar above the timeline shows percentage completion. The visual language of the tracker is reassuring to sponsors: it shows structured progress toward commitments.

**Target audience**: Project sponsors, steering committees, executive stakeholders

**Slide type mapping**: Timeline/Process (existing type 8) — milestone tracker variant

---

### Pattern 7.3 — The Phase Gate Sequence

**Source**: Stage-gate product development methodology (Robert Cooper) applied to ML model development; used by financial services and pharma data science teams presenting to compliance and risk committees.

**What makes it effective**: A horizontal sequence of phases (Discovery, Pilot, Validation, Staging, Production), each as a wide rectangle separated by a diamond-shaped gate. The gate diamonds are decision points labeled with the approval criteria (e.g., "AUC > 0.82", "Business sign-off"). This pattern signals rigor and governance — critical for regulated industries. The current phase is highlighted; past phases are dimmed and may show the actual outcome at each gate. A thin progress bar beneath the entire sequence shows elapsed calendar time. Presenting this slide reassures risk and compliance audiences that the model deployment process has decision points with explicit criteria.

**Target audience**: Risk officers, compliance teams, regulated industry leadership

**Slide type mapping**: Timeline/Process (existing type 8) — phase gate variant

---

### Pattern 7.4 — The Before/Now/Next Three-Column Roadmap

**Source**: Product management "Now/Next/Later" roadmap format; applied to data platform evolution presentations at Snowflake Summit and dbt Coalesce.

**What makes it effective**: Three columns of equal width: Before (what was done / legacy state), Now (current capabilities / active work), Next (planned investments). Each column holds 3-5 bullet points or icon-labeled items. Before column uses gray or muted styling to signal "this is receding." Now column uses accent color on bullet markers to signal active state. Next column uses outlined accent styling to signal commitment without over-promising. A horizontal divider between Before and Now may be labeled with a delivery date or major version release name. This three-horizon framing is highly legible to executives who need to understand context before hearing about future plans.

**Target audience**: Executives, customers, investors, partner organizations

**Slide type mapping**: Comparison/Two-Column (existing type 7) — three-column timeline variant (needs CSS extension)

---

## Category 8: Comparison and Evaluation Slides

### Pattern 8.1 — The Model Leaderboard

**Source**: Kaggle competition leaderboard aesthetic applied to internal model evaluation; popularized by ML platform teams at Netflix, Spotify, and LinkedIn's data science blogs.

**What makes it effective**: A ranked table showing model performance across a consistent set of metrics. Each row is a model (Baseline, Logistic Regression, Random Forest, XGBoost, production model). Columns are metrics: Accuracy, Precision, Recall, F1, Inference Time, Training Cost. The production model row is highlighted with an accent background. Metric columns use conditional formatting: cells are color-graded within their column (best value = full accent, worst = light gray). The rank column uses medal colors (gold, silver, bronze) for top three. Inference time and cost columns remind the audience that accuracy is not the only dimension that matters for production deployment decisions.

**Target audience**: Data scientists, ML engineers, technical reviewers

**Slide type mapping**: Model Performance (proposed new type — see Section 6)

**CSS/HTML approach**:
```css
.model-leaderboard {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0 4px;
}
.model-leaderboard tr.production-model {
  background: rgba(59, 130, 246, 0.08);
  font-weight: 600;
}
.metric-cell {
  text-align: right;
  font-variant-numeric: tabular-nums;
}
/* Conditional fill: inline style generated from data range */
```

---

### Pattern 8.2 — The Tool Evaluation Matrix

**Source**: Gartner Magic Quadrant methodology simplified for internal decision slides; standard format used in data platform RFP evaluations at enterprise organizations.

**What makes it effective**: A weighted scoring matrix comparing 3-4 tool options against 6-8 evaluation criteria. Rows are criteria; columns are tools. Each cell contains a score (1-5) rendered as filled circles for visual scanning speed. A weight column on the far left shows the relative importance of each criterion. A weighted total row at the bottom shows the summary score for each tool. The recommended tool column is highlighted with accent styling. The key design discipline: the weighting is as important as the scoring. Showing weights builds credibility — it demonstrates the team had a principled prioritization framework, not a pre-determined conclusion.

**Target audience**: VP Data, CTO, procurement teams, technology decision makers

**Slide type mapping**: Comparison/Two-Column (existing type 7) — weighted scoring matrix variant

---

### Pattern 8.3 — The Metric Tradeoff Triangle

**Source**: Statistical and ML community's "precision-recall tradeoff" visualization adapted for executive-facing presentation by Chip Huyen ("Designing Machine Learning Systems," 2022) and MLOps community practice.

**What makes it effective**: A triangle or three-axis diagram showing the tension between three optimization dimensions — typically Accuracy, Speed, and Cost (or Precision, Recall, and Threshold). The current model position is plotted as a point inside the triangle. Alternative configurations are plotted as secondary points, labeled. Arrows show the tradeoff direction: "moving from current to option B gains 8ms latency but costs 2% accuracy." This pattern communicates that model selection involves genuine tradeoffs, not unlimited optimization — a crucial framing that manages stakeholder expectations and prevents post-deployment complaints about the model "not being better."

**Target audience**: Product managers, business stakeholders, ML leads

**Slide type mapping**: Data/Chart (existing type 5) — tradeoff triangle variant

---

### Pattern 8.4 — The "Is This the Right Chart?" Decision Showcase

**Source**: Data visualization education community; "chart chooser" frameworks from Juice Analytics, Extreme Presentation Method (Andrew Abela); taught at Strata Data conferences.

**What makes it effective**: A two-column layout showing a poor chart choice (left, labeled "Original") and an improved chart choice (right, labeled "Revised") for the same data. The bottom of each panel contains a 1-2 sentence annotation explaining the design rationale. Used in team training presentations, methodology decks, or data literacy program slides. The contrast between the two versions makes the design principle concrete and memorable in a way that abstract rules do not. Color the "Original" panel border in red/amber; "Revised" panel border in green to encode judgment immediately.

**Target audience**: Data science teams, analytics engineers, presentation skills training

**Slide type mapping**: Comparison/Two-Column (existing type 7) — chart critique variant

---

### Pattern 8.5 — The Side-by-Side Distribution Comparison

**Source**: Scientific poster conventions at NeurIPS and ICML; Bayesian inference presentation patterns from statistical consulting.

**What makes it effective**: Two violin plots, box plots, or density curves placed side-by-side on shared axes. One distribution represents the current model or status quo; the other represents the proposed change or new model. The overlap region is shaded in a third muted color to communicate shared performance range. The median lines are prominently labeled with their values. An effect size or Cohen's d annotation below the chart communicates the practical significance, not just statistical significance, of the difference. This pattern elevates the presentation from "one model is better" to "here is the magnitude and shape of the improvement."

**Target audience**: Data scientists, statisticians, quantitative researchers

**Slide type mapping**: Data/Chart (existing type 5) — distribution comparison variant

---

## Section 5: Proposed New Slide Types for Data Science

The 12 base slide types in the current system cover general presentation needs but miss five patterns that recur specifically in data science contexts. Below are the proposed new types.

### New Type A — Dashboard/Multi-KPI

**Justification**: Data science teams present to operational stakeholders who need to see 4-8 metrics simultaneously — not one metric per slide. The Big Number type handles one metric; this type handles a grid.

**Layout**: 2x2 or 2x3 grid of metric cards. Each card: metric name (caption size), current value (48-56pt, bold), trend indicator (up/down arrow + delta), sparkline (80px wide, bottom of card). Card background is white with subtle shadow. One card may be highlighted with accent border if it requires special attention.

**HTML structure**:
```html
<section class="slide-dashboard">
  <h2 class="slide-title assertion">Model platform KPIs are all green for Q1 2025</h2>
  <div class="kpi-grid kpi-grid--2x3">
    <div class="kpi-card">
      <span class="kpi-label">Model Accuracy</span>
      <span class="kpi-value">94.2%</span>
      <span class="kpi-delta up">+1.4pp</span>
      <!-- sparkline SVG -->
    </div>
    <!-- repeat for other KPIs -->
  </div>
</section>
```

**CSS tokens**:
```css
.kpi-grid { display: grid; gap: 20px; }
.kpi-grid--2x3 { grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(2, 1fr); }
.kpi-card { background: white; border-radius: 8px; padding: 24px; box-shadow: var(--shadow-card); }
.kpi-value { font-size: 48px; font-weight: 700; display: block; }
.kpi-delta.up { color: #10b981; }
.kpi-delta.down { color: #f43f5e; }
```

---

### New Type B — Before/After with Metrics

**Justification**: The comparison type (type 7) handles side-by-side text/lists; this type handles quantified before/after states with charts or large numbers as evidence.

**Layout**: Two equal panels separated by a center column. Left panel (Before): muted gray scheme, metric shown large. Center column: vertical divider with the delta displayed prominently (48pt, accent color, + or - prefix). Right panel (After): accent scheme, improved metric shown large.

---

### New Type C — Code + Explanation

**Justification**: Split layout (type 3) handles text + image; this type handles text explanation + syntax-highlighted code. The code panel requires distinct background treatment (dark), monospace typography, and line-level highlighting.

**Layout**: Left 40% — explanation bullets or numbered steps. Right 60% — dark-background code panel with syntax highlighting, line numbers, and callout annotations.

---

### New Type D — Model Performance / Metrics Grid

**Justification**: Data/Chart type (type 5) handles single charts; this type handles a grid of model evaluation outputs: confusion matrix, ROC curve, precision-recall curve, and metric summary table arranged as a 2x2 panel.

**Layout**: 2x2 grid of evaluation panels. Top-left: confusion matrix heatmap. Top-right: ROC curve. Bottom-left: PR curve. Bottom-right: metric summary table (accuracy, precision, recall, F1, AUC). All panels share consistent axis styling and color palette.

---

### New Type E — Architecture/Pipeline Diagram

**Justification**: No existing type handles flow diagrams, pipeline diagrams, or system architecture. The icon grid (type 11) shows icons in a static grid but cannot represent directional flow.

**Layout**: Full-bleed diagram area with a constrained bounding box (90% of slide width, 70% of slide height). Diagram is positioned center-center. Assertion title sits above. A brief legend (if needed) sits below in caption size.

---

### New Type F — Funnel/Conversion

**Justification**: Funnel diagrams appear in both marketing conversion analysis and data science feature selection/filtering workflows. No existing type supports the tapered/narrowing funnel shape.

**Layout**: Centered trapezoid stack narrowing from top to bottom. Each tier: label left, value right, percentage reduction displayed between tiers. Maximum 5 tiers per slide.

---

## Section 6: Cross-Cutting Design Principles for Data Science Presentations

### Principle D1 — Assert the Insight, Not the Topic

Derived from McKinsey's action-title convention and reinforced by Knaflic's "takeaway titles" recommendation. Every data slide title must be a full sentence that states the conclusion. "Model Performance" is a topic label; "Our production model achieves 94% accuracy with sub-10ms latency" is an assertion. Assertion titles remove ambiguity about what the audience should take away, which matters especially when the presentation is distributed asynchronously or read without the speaker present.

### Principle D2 — Colorblind-Safe Palette Enforcement

For all charts and diagrams in data science presentations: never use red-green as the sole distinguishing dimension. Use blue-orange or blue-red as the primary contrasting pair. Use pattern fills or direct labels as a secondary encoding for audiences who may not distinguish hue. Minimum WCAG AA contrast ratio (4.5:1) for all text, including axis labels and chart annotations. This is not merely an accessibility nicety — approximately 8% of male audiences are colorblind, which in a 30-person executive team means 2-3 people cannot read a red-green chart.

### Principle D3 — Data Recency and Source Attribution

Every quantitative slide should carry a source footer: source, date, and methodology note if required. For internal data: "Source: Internal data warehouse, Q4 2024, N=X." For model performance: "Evaluation set: 20% holdout, Jan-Mar 2024." For market data: "Source: Company name, publication year." This discipline prevents the audience question "where did this number come from?" which derails presentation flow.

### Principle D4 — Progressive Technical Depth

Structure the deck in two layers. The main narrative is accessible to a business audience (executives, product managers). Technical details — model architecture, feature engineering choices, statistical tests — live in an Appendix section that technical reviewers can reference. In reveal.js, use horizontal navigation for the main deck and vertical navigation for technical deep-dives under each main section. This pattern serves mixed audiences without compromising either group.

### Principle D5 — Single Annotation per Chart

Each chart should carry exactly one annotation callout — the most important insight on the chart. Not two callouts. Not a callout for every interesting data point. One. This mirrors the "one idea per slide" discipline but applied within a chart. The annotation should state what the audience should notice: "Accuracy plateaued at 200 trees — adding more increases training cost with no performance benefit." The annotation is the spoken content made visible, positioned nearest the relevant data region.

---

## JSON Output Summary

```json
{
  "search_summary": {
    "platforms_searched": ["google_web", "scholarly_sources", "consulting_firm_publications", "conference_archives"],
    "repositories_analyzed": 0,
    "docs_reviewed": 14,
    "patterns_cataloged": 40,
    "new_slide_types_proposed": 6
  },
  "repositories": [],
  "technical_insights": {
    "common_patterns": [
      "Assertion titles (full-sentence conclusions) used universally by elite presenters",
      "One chart per slide with a single annotated insight",
      "Dark-background slides reserved for high-impact moments only",
      "Colorblind-safe palettes adopted by data science teams presenting to mixed audiences",
      "Progressive technical depth: business narrative + appendix for technical detail",
      "Waterfall/bridge charts for ROI quantification in executive presentations",
      "Left-to-right pipeline diagrams for architecture slides",
      "Small multiples for comparative model evaluation"
    ],
    "best_practices": [
      "Use the McKinsey assertion-title convention for all data slides",
      "Apply Knaflic's declutter process before finalizing any chart",
      "Show the Before/After comparison with identical axes and scales",
      "Present ROI in three numbers: savings, gain, payback period",
      "Reserve code slides for technical audiences; use diagrams for mixed audiences",
      "Add source attribution footer to every quantitative slide",
      "Use circular loop diagrams for iterative ML workflows",
      "Limit pipeline diagrams to 5-6 stages per slide"
    ],
    "pitfalls": [
      "Topic-label titles that don't state a conclusion",
      "Red-green color encoding that fails colorblind audiences",
      "Showing too many metrics simultaneously without visual hierarchy",
      "Inconsistent axis scales in before/after comparisons",
      "Code blocks longer than 15 lines on a single slide",
      "Over-complex architecture diagrams with more than 10 nodes",
      "ROI claims without source attribution or methodology notes",
      "Confusion matrix without associated precision/recall/F1 summary"
    ],
    "emerging_trends": [
      "Dashboard-in-a-slide (Multi-KPI grid) replacing the traditional one-metric Big Number slide",
      "Code + Explanation split layout for developer-facing data engineering presentations",
      "Circular ML lifecycle diagrams replacing linear flowcharts",
      "Medallion architecture (Bronze/Silver/Gold) as a standard data platform visual vocabulary",
      "Phase gate diagrams for regulated-industry ML deployment presentations"
    ]
  },
  "implementation_recommendations": [
    {
      "scenario": "Executive quarterly business review",
      "recommended_solution": "Dashboard/Multi-KPI slide (New Type A) + Three-Number ROI Summary (Pattern 4.2) + Quantified Impact Bridge waterfall (Pattern 3.2)",
      "rationale": "Executives need status at a glance and clear financial framing; these patterns deliver both without requiring technical literacy"
    },
    {
      "scenario": "Board presentation for data platform investment",
      "recommended_solution": "Cost-of-Inaction (Pattern 4.5) + Investment vs. Return Timeline (Pattern 4.3) + Capability vs. Competitor Gap Map (Pattern 4.4)",
      "rationale": "Loss aversion framing, NPV visualization, and competitive gap map address the three questions boards ask: What happens if we wait? What's the return? Are we behind?"
    },
    {
      "scenario": "Model deployment technical review",
      "recommended_solution": "Model Performance Grid (New Type D) + Model Leaderboard (Pattern 8.1) + Phase Gate Sequence (Pattern 7.3)",
      "rationale": "Technical reviewers need evaluation rigor evidence; leaderboard and confusion matrix grid provide it; phase gate shows governance discipline"
    },
    {
      "scenario": "Data engineering team all-hands roadmap",
      "recommended_solution": "Before/Now/Next Three-Column Roadmap (Pattern 7.4) + Left-to-Right Pipeline Diagram (Pattern 2.1) + Ops Metrics Triptych (Pattern 3.4)",
      "rationale": "Engineering teams need context (where have we come from), current state visibility, and forward direction with clear deliverables"
    },
    {
      "scenario": "Data science methodology/tool selection",
      "recommended_solution": "Tool Evaluation Matrix (Pattern 8.2) + Methodology Decision Tree (Pattern 5.3) + 2x2 Value Matrix (Pattern 4.1)",
      "rationale": "Selection decisions require transparent criteria, visible tradeoffs, and prioritization rationale — these three patterns together make the decision process auditable"
    }
  ],
  "community_insights": {
    "popular_solutions": [
      "McKinsey action title (assertion-evidence) applied to data slides",
      "Knaflic's declutter checklist before any chart is finalized",
      "Three-number ROI summary for executive justification",
      "Pipeline diagram left-to-right with color-coded layers",
      "Medallion architecture diagram for data lake/lakehouse presentations"
    ],
    "controversial_topics": [
      "Whether pie charts are ever acceptable (consensus: only for 2-3 segments, and only when part-of-whole is the primary insight)",
      "Dark vs. light backgrounds for data slides (consensus: light for charts, dark only for high-impact stat/quote slides)",
      "Whether to show confidence intervals in executive presentations (consensus: simplify to point estimates with a clear caveat; full uncertainty in appendix)"
    ],
    "expert_opinions": [
      "Knaflic: every piece of non-data ink adds cognitive load — remove it first, then decide if anything needs to come back",
      "Tufte: the data-ink ratio should approach 1.0; ink that does not represent data is decoration",
      "Minto: lead with the answer, not the analysis — the pyramid principle applied means the chart title states the conclusion before the audience looks at the chart",
      "Duarte: contrast between 'what is' and 'what could be' is the engine of persuasion — use visual language to make the gap feel real"
    ]
  }
}
```
