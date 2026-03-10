# Examples Library Builder — Agent Team Prompt

## Mission

You are an **Examples Library Agent Team** — a coordinated system of specialized agents that researches best-in-class corporate data science presentations, analyzes elite slide design patterns, and produces a structured library of example slides and reusable templates. The output populates an `examples/` folder that serves as a reference library and design enhancement resource for the Presentation Creator system defined in `.claude_prompts/presentation-creator-prompt.md`.

---

## Context

Read `.claude_prompts/presentation-creator-prompt.md` and `review/final_verdict.md` before starting. The Presentation Creator defines 12 slide types, a CSS design token system, and 4 color palettes. The evaluation identified these design gaps:

- **Design System score: 72/100** — strongest on CSS tokens, weakest on image fallbacks and data-dense content
- **Gap 8**: No dashboard/multi-metric slide type for data-heavy presentations
- **Gap 3**: Image-dependent slide types need stronger CSS-only fallback patterns
- **Audit finding**: Bullet-heavy output tendency — need more visual-first examples
- **P2-2**: Need a 13th+ slide type for data-dense content (dashboard, multi-KPI)
- **Over-specification**: Whitespace and layout rules need concrete visual examples, not just numeric rules

The examples library directly addresses these gaps by providing concrete, production-quality reference implementations.

---

## Agent Architecture

### Agent 1: Research & Curation Specialist

**Role**: Research and catalog best-in-class corporate data science presentations, identifying elite design patterns, visual techniques, and structural approaches.

**Process**:

1. **Research best-in-class data science presentations** — Search for and analyze:
   - Top-rated data science conference talks (NeurIPS, ICML, Strata, PyData, Data Council)
   - Corporate data science team presentations from FAANG/MAANG companies, consulting firms (McKinsey, BCG, Bain data analytics practices), and data-native companies (Palantir, Databricks, Snowflake, dbt Labs)
   - Award-winning presentation designs from Slideshare, Speaker Deck, Canva design awards
   - Edward Tufte's principles applied to data storytelling slides
   - Storytelling with Data (Cole Nussbaumer Knaflic) visual patterns
   - McKinsey/BCG slide design conventions (the "consulting slide" format)
   - Google, Apple, and Stripe presentation design language

2. **Catalog design patterns by category**:
   - **Data visualization slides**: How elite presenters show charts, dashboards, KPIs, and metrics
   - **Technical architecture slides**: System diagrams, ML pipeline flows, data flow diagrams
   - **Before/after transformation slides**: Showing impact of data science initiatives
   - **ROI and business case slides**: Quantifying value for executive audiences
   - **Process and methodology slides**: Explaining DS/ML workflows to mixed audiences
   - **Team and capability slides**: Showcasing data science team structure and skills
   - **Timeline and roadmap slides**: Presenting project phases and milestones
   - **Comparison and evaluation slides**: Model comparison, tool evaluation, vendor selection

3. **For each pattern, document**:
   - Source/inspiration (company, conference, designer if known)
   - What makes it effective (specific design choices, not vague praise)
   - Target audience it works best for (executives, engineers, mixed)
   - Which of the 12 existing slide types it maps to (or if it requires a new type)
   - CSS/HTML implementation approach for reveal.js

4. **Identify gaps in the current 12 slide types** that data science presentations specifically need:
   - Dashboard/multi-KPI slide (already identified in audit)
   - Before/After comparison with metrics
   - Code snippet + explanation (for technical audiences)
   - Model performance summary (confusion matrix, ROC, metrics grid)
   - Data pipeline/architecture diagram
   - Any others discovered during research

**Output**: `examples/research/design_patterns_catalog.md` — A comprehensive catalog of 30-50 design patterns organized by category, each with source, rationale, audience fit, and implementation notes.

---

### Agent 2: Slide Template Engineer

**Role**: Transform the research catalog into production-quality HTML/CSS slide templates using reveal.js, the existing design token system, and all 4 color palettes.

**Process**:

1. **Read the design token system** from the presentation creator prompt (CSS custom properties, typography scale, color palettes)

2. **Build template slides for each of the 12 existing slide types**, implementing 2-3 variants per type:
   - **Variant A**: Corporate/Professional palette — data science topic
   - **Variant B**: Technical/Developer palette — data science topic
   - **Variant C** (where applicable): A data-dense or advanced variant

3. **Build NEW slide type templates** for data science-specific patterns not covered by the 12 existing types:
   - **Dashboard/Multi-KPI**: 2x2 or 3x1 grid with large numbers, trend indicators, sparkline-style CSS elements, and context labels
   - **Before/After Metrics**: Side-by-side with highlighted deltas and percentage changes
   - **Code + Explanation**: Split layout with styled code block (left) and plain-language explanation (right)
   - **Model Performance**: Metrics grid with color-coded performance indicators
   - **Architecture/Pipeline**: CSS-only flow diagram with labeled nodes and directional arrows
   - **Funnel/Conversion**: Narrowing visual showing pipeline stages with drop-off metrics

4. **For each template slide, produce**:
   - Complete, self-contained HTML that works inside a reveal.js `<section>` tag
   - All CSS scoped with a unique class (e.g., `.example-dashboard-1`)
   - Realistic data science content (not lorem ipsum — use plausible metrics, model names, KPIs)
   - Speaker notes demonstrating how to present the slide
   - `<!-- CUSTOMIZATION: ... -->` comments showing which values to change for reuse

5. **Image fallback patterns**: For every slide type that would ideally use photography or illustrations, create a compelling CSS-only alternative:
   - Gradient backgrounds with geometric overlays
   - CSS-drawn charts and data visualizations (bar charts, line trends, donut charts using conic-gradient)
   - Icon-based compositions using Unicode or SVG inline icons
   - Typographic treatments (large pull quotes, oversized statistics)

6. **Ensure every template**:
   - Uses CSS custom properties from the design token system (never hard-coded values)
   - Meets WCAG AA contrast (4.5:1 minimum)
   - Has minimum 18px font size for all visible text
   - Follows the assertion-evidence model (full-sentence title, visual body)
   - Contains `<aside class="notes">` with realistic speaker notes
   - Is responsive within reveal.js's scaling system

**Output**:
- `examples/templates/` — Individual HTML files per slide type, each containing 2-3 variants
- `examples/templates/README.md` — Index of all templates with descriptions and screenshots (described, not actual images)

---

### Agent 3: Showcase Presentation Builder

**Role**: Assemble the best template slides into 3 complete showcase presentations that demonstrate the system at its best for data science use cases.

**Process**:

1. **Showcase 1: "Building a Data Science Practice — Executive Briefing"** (8-10 slides, 10 minutes)
   - Audience: C-suite / VP-level executives
   - Purpose: Secure investment for a new data science team
   - Tone: Professional, corporate
   - Palette: Corporate/Professional
   - Must demonstrate: Title, Section Divider, Statistics/Big Number, Dashboard/Multi-KPI, Comparison, Timeline, Icon Grid, CTA
   - Include full speaker notes and timing

2. **Showcase 2: "ML Model Performance Review — Technical Deep Dive"** (10-12 slides, 15 minutes)
   - Audience: Data science team leads, ML engineers
   - Purpose: Present quarterly model performance and improvement roadmap
   - Tone: Technical
   - Palette: Technical/Developer
   - Must demonstrate: Title, Data/Chart, Model Performance, Before/After, Code + Explanation, Architecture/Pipeline, Quote, CTA
   - Include full speaker notes and timing

3. **Showcase 3: "Data-Driven Transformation — Board Presentation"** (6-8 slides, 8 minutes)
   - Audience: Board of directors, investors
   - Purpose: Report on ROI of data science investments
   - Tone: Professional but direct
   - Palette: Sales/Marketing (high energy for board confidence)
   - Must demonstrate: Title, Full-Bleed (CSS gradient), Statistics, Funnel/Conversion, Comparison, CTA
   - Include full speaker notes and timing

4. **Each showcase must**:
   - Be a complete, self-contained HTML file using reveal.js
   - Include the RevealNotes plugin (the P0 bug fix)
   - Pass all Production-Quality Pass Thresholds from `review/final_verdict.md`
   - Use realistic, plausible data science content (not generic business content)
   - Demonstrate the assertion-evidence model throughout
   - Have zero bullet-heavy slides (every body is visual, not text lists)
   - Include `<!-- IMAGE_PLACEHOLDER: ... -->` comments where real images would enhance

**Output**:
- `examples/showcases/executive_briefing.html`
- `examples/showcases/technical_review.html`
- `examples/showcases/board_presentation.html`

---

### Agent 4: Documentation & Integration Architect

**Role**: Create the documentation, organization, and integration guidance that makes the examples library usable and connects it back to the main presentation creator system.

**Process**:

1. **Create the examples folder structure**:
   ```
   examples/
   ├── README.md                    # Library overview, how to use, quick-start
   ├── research/
   │   ├── design_patterns_catalog.md   # Agent 1's research output
   │   └── sources.md                   # Bibliography of all sources researched
   ├── templates/
   │   ├── README.md                    # Template index with descriptions
   │   ├── slide_type_01_title.html
   │   ├── slide_type_02_section_divider.html
   │   ├── slide_type_03_split_layout.html
   │   ├── slide_type_04_full_bleed.html
   │   ├── slide_type_05_data_chart.html
   │   ├── slide_type_06_quote.html
   │   ├── slide_type_07_comparison.html
   │   ├── slide_type_08_timeline.html
   │   ├── slide_type_09_statistics.html
   │   ├── slide_type_10_team_bio.html
   │   ├── slide_type_11_icon_grid.html
   │   ├── slide_type_12_cta.html
   │   ├── slide_type_13_dashboard.html      # NEW
   │   ├── slide_type_14_before_after.html   # NEW
   │   ├── slide_type_15_code_explain.html   # NEW
   │   ├── slide_type_16_model_perf.html     # NEW
   │   ├── slide_type_17_architecture.html   # NEW
   │   └── slide_type_18_funnel.html         # NEW
   ├── showcases/
   │   ├── executive_briefing.html
   │   ├── technical_review.html
   │   └── board_presentation.html
   ├── css_patterns/
   │   ├── gradients.html           # Reusable gradient background patterns
   │   ├── data_viz_css.html        # CSS-only chart patterns (bars, donuts, sparklines)
   │   ├── layout_grids.html        # Grid layout examples (2-col, 3-col, 2x2, asymmetric)
   │   └── typography_treatments.html  # Large stat, pull quote, headline treatments
   └── design_system/
       ├── color_palettes.html       # All 4 palettes rendered with swatches and usage examples
       ├── typography_scale.html     # Type scale rendered at all sizes with pairing examples
       └── component_library.html   # Reusable micro-components (cards, badges, trend indicators, progress bars)
   ```

2. **Write `examples/README.md`** with:
   - Purpose of the library (enhancement resource for the presentation creator)
   - How to use: browse templates → pick slide types → customize content
   - Quick-start: open any showcase HTML in Chrome to see the system at its best
   - Folder structure explanation
   - How to contribute new patterns

3. **Write integration recommendations** — specific, actionable changes to `.claude_prompts/presentation-creator-prompt.md` that reference the examples library:
   - Add new slide types (13-18) to Agent 2's Slide Type Templates section
   - Add CSS pattern references for image fallback section
   - Add data science-specific content patterns to Agent 1's research guidance
   - Reference showcase presentations as quality benchmarks

4. **Create `examples/design_system/` files**:
   - Render all 4 color palettes as visual swatches in HTML
   - Show the typography scale at every size
   - Build a component library of reusable micro-elements:
     - Trend indicators (up/down arrows with color)
     - KPI cards (number + label + trend)
     - Progress bars (with percentage labels)
     - Status badges (green/yellow/red)
     - Sparkline-style CSS patterns
     - Data table styling (minimal, Tufte-inspired)

**Output**: All files in the structure above, fully populated with production-quality content.

---

## Workflow

### Execution Sequence

```
Phase 1: RESEARCH (Agent 1)
├── Search for best-in-class data science presentations
├── Analyze design patterns from top sources
├── Catalog 30-50 patterns by category
├── Identify gaps requiring new slide types
└── Output: examples/research/design_patterns_catalog.md

Quality Gate 1: Verify catalog contains:
- [ ] Minimum 30 documented patterns
- [ ] At least 5 sources from tier-1 companies or conferences
- [ ] Clear mapping to existing 12 slide types + identified new types
- [ ] Specific CSS/HTML implementation notes per pattern
- [ ] Data science-specific patterns (not generic business)

Phase 2: TEMPLATES (Agent 2)
├── Build 2-3 variants per existing slide type (12 × 2-3 = 24-36 slides)
├── Build new slide type templates (6 new types × 2-3 = 12-18 slides)
├── Create CSS-only image fallback patterns
├── Ensure design token consistency
└── Output: examples/templates/ (36-54 template slides total)

Quality Gate 2: Verify templates:
- [ ] All 12 existing types have at least 2 variants
- [ ] All new types have at least 2 variants
- [ ] 100% use CSS custom properties (no hard-coded colors/sizes)
- [ ] 100% include speaker notes
- [ ] 100% use assertion-evidence titles
- [ ] 0 templates with bullet-heavy bodies

Phase 3: SHOWCASES (Agent 3)
├── Build 3 complete presentations from template library
├── Apply realistic data science content
├── Verify against production-quality pass thresholds
├── Test HTML validity
└── Output: examples/showcases/ (3 HTML files)

Quality Gate 3: Each showcase passes:
- [ ] RevealNotes plugin loaded; S key works
- [ ] Slide count within timing guidelines
- [ ] 100% of slides have speaker notes
- [ ] 0 slides with >50 words of body text
- [ ] Narrative arc: hook → 3 MECE pillars → specific CTA
- [ ] Total timing within ±15% of target (at 130 wpm)

Phase 4: DOCUMENTATION (Agent 4)
├── Create folder structure
├── Write README and index files
├── Build design system reference files
├── Write integration recommendations
└── Output: All documentation and design system files
```

---

## Quality Standards

### Every HTML file must:
- Be self-contained (reveal.js CDN, embedded CSS)
- Open without errors in Chrome
- Include the RevealNotes plugin
- Use the design token CSS custom properties
- Meet WCAG AA contrast ratios
- Have no text below 18px

### Content must be:
- Realistic data science content (plausible metrics, real tool/framework names, actual ML concepts)
- NOT lorem ipsum, NOT generic business platitudes
- Specific enough to be immediately useful as a starting point for real presentations

### Design must:
- Follow assertion-evidence model (sentence titles, visual bodies)
- Prioritize visual communication over text
- Demonstrate proper whitespace and layout grid usage
- Show color palette usage correctly (60-30-10 rule)

---

## Example Invocation

```
Execute the Examples Library Builder agent team:

Focus areas:
1. Corporate data science presentations for executive and technical audiences
2. Best-in-class slide design from McKinsey, Google, Stripe, and top DS conferences
3. CSS-only data visualization patterns (charts, dashboards, KPIs without JavaScript libraries)
4. New slide types for data-dense content (dashboards, model performance, architecture diagrams)

Output: Populate the examples/ folder with the complete library structure defined above.
Additional context: The presentation creator system uses reveal.js for HTML output.
All templates must work within reveal.js's section-based slide structure.
The system currently scores 72/100 on design — the examples library should demonstrate 90+ quality.
```
