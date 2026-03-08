# Presentation Design Specification
## "The AI-Augmented Team: How Artificial Intelligence Is Transforming Software Development"

**For**: Software engineering teams and tech leadership
**Format**: 16:9 widescreen (1920x1080px reference), 15 slides
**Design philosophy**: Assertion-Evidence Model, Signal-to-Noise Ratio, One Idea Per Slide
**Implementer note**: Every measurement below assumes a 1920x1080 canvas. All padding, font sizes, and positioning are in pixels unless noted as percentages.

---

## CSS Design Token System

```css
:root {
  /* === COLOR TOKENS === */

  /* Backgrounds */
  --color-bg-primary:     #0f172a;   /* Main slide background — navy near-black */
  --color-bg-secondary:   #1e293b;   /* Section panels, card backgrounds */
  --color-bg-surface:     #334155;   /* Cards, chips, table rows */
  --color-bg-overlay:     rgba(15, 23, 42, 0.85); /* Scrim over visuals */

  /* Accents */
  --color-accent:         #06b6d4;   /* Cyan/teal — primary accent, charts, highlights */
  --color-accent-dim:     rgba(6, 182, 212, 0.15); /* Accent fill for bars, backgrounds */
  --color-accent-border:  rgba(6, 182, 212, 0.35); /* Subtle borders with accent hue */

  /* Semantic */
  --color-positive:       #10b981;   /* Emerald — gains, improvements, positive outcomes */
  --color-positive-dim:   rgba(16, 185, 129, 0.15);
  --color-warning:        #f59e0b;   /* Amber — risks, cautions, decline data */
  --color-warning-dim:    rgba(245, 158, 11, 0.15);
  --color-negative:       #ef4444;   /* Red — only for failure/loss data if needed */

  /* Text */
  --color-text-primary:   #f8fafc;   /* Off-white — headings, primary body */
  --color-text-secondary: #94a3b8;   /* Slate — captions, labels, sources */
  --color-text-muted:     #475569;   /* Dimmer slate — de-emphasized content */
  --color-text-accent:    #06b6d4;   /* Accent color for inline emphasis */
  --color-text-warning:   #f59e0b;   /* Amber for risk data inline */
  --color-text-positive:  #10b981;   /* Emerald for gain data inline */

  /* Borders and dividers */
  --color-border-subtle:  rgba(148, 163, 184, 0.12);
  --color-border-accent:  rgba(6, 182, 212, 0.4);

  /* === TYPOGRAPHY TOKENS === */
  --font-family:          'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

  /* Scale */
  --font-hero:            96px;     /* Stat slides — the dominant number */
  --font-hero-weight:     800;
  --font-title:           44px;     /* Primary slide titles */
  --font-title-weight:    700;
  --font-title-sm:        36px;     /* Titles on content-dense slides */
  --font-subtitle:        28px;     /* Subtitles, section subheadings */
  --font-subtitle-weight: 400;
  --font-body:            24px;     /* Body text, bullet items */
  --font-body-weight:     400;
  --font-body-sm:         20px;     /* Secondary body, tight lists */
  --font-label:           16px;     /* Chart labels, card labels */
  --font-caption:         14px;     /* Source citations, footnotes */
  --font-caption-weight:  400;
  --font-section-num:     160px;    /* Oversized section numerals (01, 02, 03) */
  --font-section-num-weight: 800;

  /* Line heights */
  --lh-heading:           1.1;
  --lh-body:              1.5;
  --lh-caption:           1.4;

  /* Letter spacing */
  --ls-heading:           -0.02em;
  --ls-label:             0.04em;   /* Uppercase labels */
  --ls-section-num:       -0.04em;

  /* === SPACING TOKENS === */
  --pad-slide:            60px;     /* Universal slide padding — all four sides */
  --pad-content:          48px;     /* Inner content padding */
  --gap-columns:          48px;     /* Column gutters */
  --gap-items:            32px;     /* Between list/card items */
  --gap-items-sm:         20px;     /* Tight item spacing */
  --gap-section:          56px;     /* Between major content blocks */

  /* === GRID TOKENS === */
  --grid-columns:         12;
  --grid-gutter:          24px;

  /* === COMPONENT TOKENS === */
  --card-radius:          12px;
  --chip-radius:          6px;
  --bar-radius:           4px;
  --divider-weight:       1px;

  /* === MOTION TOKENS (for implementation reference) === */
  --transition-fast:      150ms ease;
  --transition-std:       250ms ease;
}
```

---

## Slide Specifications

---

### Slide 1 — Title Slide

**CSS class**: `.slide--title`
**Type**: Title
**Content**: Main title, subtitle, presenter context line, date

#### Layout

Full-bleed background: `--color-bg-primary`. No split. Single centered column.

- Canvas: 1920 x 1080px
- Content area: horizontally centered, max-width 1100px, vertically centered at 50% minus 20px to account for optical center
- A single 2px horizontal rule (color: `--color-accent`, width: 64px) sits above the title as a visual anchor, centered
- Bottom-left corner: presenter name + role in `--font-caption`, color `--color-text-secondary`
- Bottom-right corner: date ("March 2026") in `--font-caption`, color `--color-text-muted`
- All bottom-anchored text sits at `--pad-slide` (60px) from the bottom edge

#### Typography

| Element | Size | Weight | Color | Notes |
|---|---|---|---|---|
| Accent rule above title | 2px tall, 64px wide | — | `--color-accent` | 32px below rule, then title starts |
| Primary title | `--font-title` (44px) | 700 | `--color-text-primary` | Line height `--lh-heading` |
| Subtitle | `--font-subtitle` (28px) | 400 | `--color-text-secondary` | 24px gap below title; max 2 lines |
| Presenter / date captions | `--font-caption` (14px) | 400 | `--color-text-secondary` | Bottom anchored |

#### Color usage

- Background: `--color-bg-primary`
- Accent rule: `--color-accent`
- No other color elements — maximum restraint on this slide

#### Visual elements

None beyond typography and the accent rule. No imagery, no illustration. The restraint signals data-driven seriousness from slide 1.

Optional subtle texture: a radial gradient centered behind the title block using `rgba(6, 182, 212, 0.04)` spreading to transparent over a 600px radius — adds depth without distraction.

#### Whitespace

- 180px of vertical space above the accent rule (optical center pull-up)
- 32px gap: rule to title
- 24px gap: title to subtitle
- 80px gap: subtitle to bottom attribution area

---

### Slide 2 — Opening Provocation (Stat)

**CSS class**: `.slide--stat`
**Type**: Stat (full-bleed hero number)
**Assertion title**: "46% of Code Written by Active GitHub Copilot Users Is Now AI-Generated"

#### Layout

Three horizontal bands stacked vertically within the slide padding:

1. **Title band** — top, full width
2. **Hero stat band** — vertically dominant center mass
3. **Supporting data band** — bottom strip, max 2 lines, source attribution inline

Content area: `--pad-slide` (60px) on all sides. No columns.

- Title: top-aligned, full width, first element inside the padding box
- Hero number "46%" — centered horizontally, positioned so its vertical midpoint sits at approximately 48% of canvas height (slightly above geometric center — reads as anchored)
- Below the hero number: a small inline timeline "27% in 2022 → 46% in 2025" displayed as a horizontal sequence of nodes
- Supporting stats strip: 80px from bottom edge, left-aligned, two short lines of text

#### Typography

| Element | Size | Weight | Color | Notes |
|---|---|---|---|---|
| Slide title | `--font-title` (44px) | 700 | `--color-text-primary` | Single line, top of slide |
| Hero number "46%" | `--font-hero` (96px) | 800 | `--color-accent` | The dominant element; letter-spacing -0.04em |
| "of code" label | 32px | 400 | `--color-text-secondary` | Sits directly below the hero number, centered; 8px gap |
| Timeline nodes (27% → 46%) | `--font-label` (16px) | 600 | `--color-text-secondary` | Arrow between: `→` in `--color-accent` |
| Supporting data lines | `--font-body-sm` (20px) | 400 | `--color-text-secondary` | Bottom strip |
| Source citation | `--font-caption` (14px) | 400 | `--color-text-muted` | Inline after data |

#### Color usage

- Background: `--color-bg-primary`
- "46%" numeral: `--color-accent` — the only bright color, ensuring it receives 100% of attention
- Timeline arrows: `--color-accent`
- Supporting text: `--color-text-secondary`
- Source: `--color-text-muted`

#### Visual elements

**Inline timeline — "27% → 46%"**: Two circular nodes (24px diameter, filled `--color-bg-surface`, stroked `--color-accent-border`) connected by a horizontal line (1px, `--color-border-subtle`). Left node labeled "2022 / 27%" above; right node labeled "2025 / 46%" above — with the right node stroke in `--color-accent` at full opacity to show the endpoint. Arrow pointer between nodes in `--color-accent`. Total width: approximately 320px. Centered below the hero number with 40px gap.

No bar charts, no illustrations. The number earns its impact through isolation.

#### Whitespace

- 60px padding all edges
- 40px gap: title to hero number block
- 24px gap: hero number to "of code" label
- 32px gap: label to timeline
- Remaining space before bottom strip is empty — intentionally

---

### Slide 3 — Situation: The Pressure Engineering Teams Are Under (Split)

**CSS class**: `.slide--split`
**Type**: Split, two columns
**Assertion title**: "Engineering Teams Are Being Asked for More — With the Same Resources"

#### Layout

- Header row: full-width title, top-anchored, spans both columns
- Content area below title: two columns at 50% / 50% split with `--gap-columns` (48px) gutter between
- Left column: "The Pressures" — 3 items with icons
- Right column: "Current Reality" — 3 items with icons
- Column headers: small uppercase label in `--font-label` with `--ls-label`
- A single 1px vertical divider in `--color-border-subtle` runs between the columns from 16px below the column header baseline to 16px above the bottom of the content area

Padding: `--pad-slide` (60px) on all four sides. Content starts 32px below title baseline.

#### Typography

| Element | Size | Weight | Color | Notes |
|---|---|---|---|---|
| Slide title | `--font-title` (44px) | 700 | `--color-text-primary` | Full width, top |
| Column label (e.g. "HEADWINDS") | `--font-label` (16px) | 600 | `--color-text-secondary` | All-caps, `--ls-label`, 32px below title |
| Item text | `--font-body` (24px) | 400 | `--color-text-primary` | Each item ~1.5 lines max |
| Source | `--font-caption` (14px) | 400 | `--color-text-muted` | Bottom of slide |

#### Color usage

- Left column header "PRESSURES": `--color-warning` (amber) — signals strain
- Right column header "CURRENT STATE": `--color-text-secondary` (neutral)
- Left column icons: `--color-warning`
- Right column icons: `--color-text-secondary`
- Divider: `--color-border-subtle`
- Background: `--color-bg-primary`

#### Visual elements

Each item is presented as a row: a 28px square geometric icon on the left (16px padding) + text to the right. Icons are outline-style (2px stroke, no fill) — pure geometric, not illustrative.

Left column icons (amber):
- Increasing complexity: three nested rectangles, each slightly larger
- Labor market: person silhouette with upward arrow (unfilled)
- Business expectations: three stacked horizontal bars of different lengths (like a demand chart)

Right column icons (slate):
- Sprint cadence: a simple calendar grid square with a checkmark
- Burnout risk: flame icon, simplified — two curved lines
- Tech debt: a block with a crack/fracture line through it

Icon size: 28 x 28px. Gap between icon and text: 16px. Gap between items: `--gap-items` (32px).

#### Whitespace

- 60px padding all edges
- 32px gap: title to column headers
- 20px gap: column header to first item
- 32px between items
- Column vertical divider has 24px clearance top and bottom from content edges

---

### Slide 4 — Complication: The Strategy Gap (Comparison)

**CSS class**: `.slide--chart`
**Type**: Chart (divergence visualization)
**Assertion title**: "Teams Are Adopting AI Rapidly — But Realized Impact Is Lagging Behind"

#### Layout

- Title: top-anchored, full width
- Subtitle / framing statement: one line, 20px below title
- Chart area: occupies 65% of slide height below the subtitle, horizontally centered with 10% margin left and right (total chart width: 80% of canvas = ~1536px)
- Legend: 24px below chart, left-aligned to chart left edge
- Source strip: bottom of slide, right-aligned

#### Typography

| Element | Size | Weight | Color | Notes |
|---|---|---|---|---|
| Slide title | `--font-title-sm` (36px) | 700 | `--color-text-primary` | Single line |
| Framing statement | `--font-body-sm` (20px) | 400 | `--color-text-secondary` | "76% of developers use or plan to use AI tools — only 6% of orgs qualify as high performers" |
| Chart axis labels | `--font-caption` (14px) | 400 | `--color-text-secondary` | X-axis: years; Y-axis: percentage |
| Data labels on curves | `--font-label` (16px) | 600 | Curve color | At end of each line |
| "THE STRATEGY GAP" annotation | `--font-label` (16px) | 700 | `--color-warning` | Centered in the gap zone with a bracket |
| Legend labels | `--font-label` (16px) | 400 | `--color-text-secondary` | Dot + label |
| Source citation | `--font-caption` (14px) | 400 | `--color-text-muted` | Bottom right |

#### Color usage

- Adoption curve line: `--color-accent` (cyan), 3px stroke
- Impact curve line: `--color-positive` (emerald), 3px stroke, but dotted/dashed to signal uncertainty in measurement
- Gap zone fill: `rgba(245, 158, 11, 0.08)` — very subtle amber wash between the curves
- "THE STRATEGY GAP" label and bracket: `--color-warning`
- Grid lines: `--color-border-subtle`
- Axes: `--color-border-subtle`

#### Visual elements

**Divergence line chart** — described precisely for developer implementation:

- X-axis: 2022 / 2023 / 2024 / 2025 (four points)
- Y-axis: 0% to 100%, labeled at 0, 25, 50, 75, 100
- Curve A (Adoption): starts at ~45% in 2022, climbs steeply to ~76% in 2025. Use `--color-accent`.
- Curve B (High Performer Rate): starts at ~5% in 2022, rises only to ~6% in 2025. Essentially flat. Use `--color-positive` dashed.
- The area between the two curves is filled with the amber wash defined above.
- A double-headed vertical bracket arrow rendered between the two curves at the 2025 x-position, labeled "THE STRATEGY GAP" with the `--color-warning` text.
- Both curves terminate with a labeled dot: "76% adoption" and "6% high performers" respectively, rendered in their curve color.
- Chart background: `--color-bg-secondary` (#1e293b), `--card-radius` (12px) corner radius. No chart border.

#### Whitespace

- 60px slide padding
- 16px gap: title to framing statement
- 28px gap: framing statement to chart top
- 24px gap: chart bottom to legend
- 48px bottom margin before source

---

### Slide 5 — Section Divider: Pillar 1

**CSS class**: `.slide--section-divider`
**Type**: Section divider
**Content**: "Pillar 1: The Productivity Gains Are Real"

#### Layout

Full-bleed background: `--color-bg-secondary` (slightly lighter than primary — signals a mode shift). No columns.

Two-zone vertical layout:
- Left zone (60% width): text content — section number, title, subtitle, a short horizontal rule
- Right zone (40% width): purely decorative — the oversized section numeral "01" rendered as a watermark

The oversized numeral "01" is right-aligned within the right zone, vertically centered, at `--font-section-num` (160px), weight 800, color `rgba(6, 182, 212, 0.08)` — barely visible, serves as structural texture only.

Left zone text stack is vertically centered in the full slide height.

#### Typography

| Element | Size | Weight | Color | Notes |
|---|---|---|---|---|
| Pillar label ("PILLAR 01") | `--font-label` (16px) | 700 | `--color-accent` | All-caps, `--ls-label`; topmost element in stack |
| Section title | `--font-title` (44px) | 700 | `--color-text-primary` | 16px below pillar label; line height `--lh-heading` |
| Section subtitle | `--font-subtitle` (28px) | 400 | `--color-text-secondary` | 20px below title |
| Horizontal rule (decorative) | 2px height, 48px width | — | `--color-accent` | 24px above the pillar label |
| Watermark numeral "01" | 160px | 800 | `rgba(6, 182, 212, 0.08)` | Right zone, decorative only |

#### Color usage

- Background: `--color-bg-secondary`
- Accent rule + pillar label + watermark: `--color-accent` / `--color-accent-dim`
- Title: `--color-text-primary`
- Subtitle: `--color-text-secondary`

#### Visual elements

No charts, no icons. The large muted numeral is the only non-text visual — it provides compositional balance without adding information load.

A 1px top border in `--color-accent` spans the full width of the slide — a thin cyan line at the very top edge.

#### Whitespace

- 60px padding left/right; 0 padding top (the accent border runs edge to edge)
- Left text stack: vertically centered (transform: translateY(-10%) for optical correction)
- Right zone: 40% width, numeral optically centered

---

### Slide 6 — The Productivity Evidence (Chart / Data-Dense)

**CSS class**: `.slide--chart .slide--chart--dense`
**Type**: Chart
**Assertion title**: "Five Independent Studies Converge: AI Tools Deliver 26–75% Gains Across Task Types"

#### Layout

- Title: top-anchored, full width — `--font-title-sm` (36px) to preserve chart space
- Subtitle/framing: one short line below title in `--font-body-sm`, `--color-text-secondary`
- Chart area: occupies approximately 68% of slide height, starting 80px below title, full horizontal width minus `--pad-slide` on each side
- Source strip: two lines, bottom of slide, left-aligned
- This is the slide that earns 90–120 seconds; dense information is appropriate here

#### Typography

| Element | Size | Weight | Color | Notes |
|---|---|---|---|---|
| Slide title | `--font-title-sm` (36px) | 700 | `--color-text-primary` | |
| Chart category labels (Y-axis) | `--font-body-sm` (20px) | 500 | `--color-text-primary` | Left of bars |
| Bar value labels | `--font-label` (16px) | 700 | Bar color | Right-end of each bar, outside |
| X-axis labels | `--font-caption` (14px) | 400 | `--color-text-secondary` | |
| Source inline citations | `--font-caption` (14px) | 400 | `--color-text-muted` | Below chart |
| Legend labels | `--font-label` (16px) | 400 | `--color-text-secondary` | |

#### Color usage

- "Without AI" bars: `--color-bg-surface` (#334155) — dark neutral
- "With AI" bars: `--color-accent` (#06b6d4) — cyan
- Bar value labels: white on the "With AI" bar; `--color-text-secondary` on "Without" bar
- Bar background track: `--color-bg-secondary`
- Delta annotation (improvement %) placed between the two bars per category: `--color-positive` (emerald) text

#### Visual elements

**Horizontal paired bar chart** — 5 categories, each with two bars (before/after):

Categories (Y-axis, top to bottom):
1. Task Completion Speed — Without AI: 100% (baseline); With AI: 45% of original time (55% faster). Source: GitHub + Accenture
2. PR Cycle Time — Without AI: 9.6 days; With AI: 2.4 days (75% reduction). Source: Multiple studies
3. Code Documentation Speed — Without AI: 100%; With AI: ~50% (2x faster). Source: McKinsey
4. Weekly Tasks Completed — Without AI: baseline; With AI: +26%. Source: 4,867-dev study
5. Code Optimization Time — Without AI: 100%; With AI: ~65% (35% faster). Source: McKinsey

Implementation note: normalize all metrics to a common scale (0 to 100%, where 100% = baseline "without AI" time or task count). For "faster" metrics, show the "with AI" bar as shorter (less time). For "more tasks," show the "with AI" bar as longer. Label each bar end with its actual value (e.g. "2.4 days", "55% faster") rather than a normalized percentage.

Bar height: 32px each. Gap between paired bars: 8px. Gap between categories: 24px. Bar left-edge aligns with category labels (which are left of the chart). Bars fill rightward. Maximum bar width: 70% of chart area.

A thin vertical reference line at the "100% baseline" position in `--color-border-subtle`.

Delta badge — between the two bars per row: a small pill (background `--color-positive-dim`, border `--color-border-subtle`, border-radius `--chip-radius`) containing the improvement figure in `--color-positive`, `--font-label`, bold. Example: "+55%" or "75% faster".

Chart background: `--color-bg-secondary`, `--card-radius`.

#### Whitespace

- 60px slide padding
- Title to chart: 28px
- Between chart and sources: 20px
- Sources occupy the bottom 40px of the content area

---

### Slide 7 — Developer Experience Is a Business Metric (Icons / Stat Grid)

**CSS class**: `.slide--stat-grid`
**Type**: Icons / stat grid
**Assertion title**: "Developer Satisfaction Metrics Predict Retention — Not Just Morale"

#### Layout

- Title: top-anchored, full width
- Framing sentence: one line below title
- Stat grid: 3 columns x 2 rows of stat cards, centered horizontally
- Grid starts 60px below the framing sentence
- No bottom content below grid — generous breathing room

Grid dimensions:
- Card width: ~560px
- Card height: ~180px
- Column gap: 40px
- Row gap: 28px
- Total grid: 3 x 560px + 2 x 40px = 1760px wide — fits at 1920px canvas with 80px margins (intentionally slightly tight — the stat grid commands the slide)

Adjust to: card width 520px, gap 40px = 1600px grid, centered in 1920px canvas with 160px left/right margin.

#### Typography

| Element | Size | Weight | Color | Notes |
|---|---|---|---|---|
| Slide title | `--font-title-sm` (36px) | 700 | `--color-text-primary` | |
| Framing sentence | `--font-body-sm` (20px) | 400 | `--color-text-secondary` | One line max |
| Stat number per card | 64px | 800 | `--color-accent` | The anchor of each card |
| Stat label (one line) | `--font-body-sm` (20px) | 400 | `--color-text-primary` | Directly below number |
| Source (per card, optional) | `--font-caption` (14px) | 400 | `--color-text-muted` | Bottom of card |

#### Color usage

- Card background: `--color-bg-surface` (#334155)
- Card border: `--color-border-subtle`
- Card border-radius: `--card-radius` (12px)
- Stat number: `--color-accent`
- For the single negative-trend stat ("trust declining"): number in `--color-warning` to signal caution — do not include a declining stat here; this slide is pure positive. Save trust data for Slide 10.

#### Visual elements

Six stat cards, left-to-right, top-to-bottom:

Row 1:
- Card 1: "95%" / "Report enjoying coding more" / Source: GitHub, 2023
- Card 2: "2x" / "More likely to report flow state" / Source: McKinsey
- Card 3: "73%" / "Say AI helps them stay in flow" / Source: GitHub

Row 2:
- Card 4: "60%" / "Report increased job satisfaction" / Source: Multiple studies
- Card 5: "87%" / "Say AI preserves mental effort on repetitive tasks" / Source: GitHub
- Card 6: "26%" / "More tasks completed per week" / Source: 4,867-developer study

No icons in these cards — the number is the icon. Keeping the card layout purely typographic maximizes legibility at presentation scale.

Each card has 28px internal padding on all sides. The stat number is top-aligned within the card's content area.

#### Whitespace

- 60px slide padding
- 20px gap: title to framing sentence
- 60px gap: framing sentence to grid top
- 28px between rows; 40px between columns
- Generous empty space at bottom of slide (approximately 80px from grid bottom to slide edge) — this is intentional; slides 5-6 were dense, this slide breathes

---

### Slide 8 — Section Divider: Pillar 2

**CSS class**: `.slide--section-divider`
**Type**: Section divider
**Content**: "Pillar 2: The Risks Are Specific and Manageable"

#### Layout

Same template as Slide 5. Watermark numeral: "02". Left zone text stack vertically centered.

#### Typography

Same token assignments as Slide 5.

| Element | Content | Color override |
|---|---|---|
| Pillar label | "PILLAR 02" | `--color-warning` (amber) — signals risk section |
| Section title | "Pillar 2: The Risks Are Specific and Manageable" | `--color-text-primary` |
| Section subtitle | "What to watch for — and what to do about it" | `--color-text-secondary` |
| Accent rule above label | 2px x 48px | `--color-warning` |
| Watermark numeral "02" | right zone | `rgba(245, 158, 11, 0.08)` (amber wash) |

#### Color usage

Using amber instead of cyan for this section divider signals a tonal shift. The 1px top border is `--color-warning`. The pillar label is amber. The watermark is amber. This is the only slide where the accent changes — it returns to cyan for Pillar 3 and the CTA.

#### Whitespace

Identical to Slide 5.

---

### Slide 9 — The Risk Map (Three-Column Comparison)

**CSS class**: `.slide--comparison`
**Type**: Comparison — three columns
**Assertion title**: "Three Distinct Risk Categories, Each With a Direct Countermeasure"

#### Layout

- Title: top-anchored, full width, `--font-title-sm` (36px)
- Three equal-width columns below title: Security / Technical Debt / Delivery Stability
- Column width: (1920 - 120px padding - 2 x 40px gutter) / 3 = approximately 573px each
- Column gap: 40px
- Content starts 48px below title baseline
- Each column has internal structure: risk header → risk data points → divider → countermeasure

Column internal structure (top to bottom, within 40px internal padding):
1. Category label (uppercase, `--font-label`)
2. Key data point — large, bold
3. Supporting stat — smaller
4. A 1px horizontal divider in `--color-border-subtle` spanning column width
5. Countermeasure label ("COUNTERMEASURE" in uppercase `--font-caption`)
6. Countermeasure description text

Each column is a card with `--color-bg-surface` background, `--card-radius` (12px) radius.

#### Typography

| Element | Size | Weight | Color |
|---|---|---|---|
| Slide title | 36px | 700 | `--color-text-primary` |
| Column category label | `--font-label` (16px) | 700 | `--color-warning` | All-caps |
| Key data point (hero number) | 56px | 800 | `--color-warning` | e.g. "48%" |
| Key data description | `--font-body-sm` (20px) | 400 | `--color-text-primary` | Below hero number |
| Supporting stat | `--font-caption` (14px) | 400 | `--color-text-secondary` | |
| "COUNTERMEASURE" label | `--font-caption` (14px) | 700 | `--color-positive` | All-caps |
| Countermeasure text | `--font-body-sm` (20px) | 400 | `--color-text-primary` | |
| Source | `--font-caption` (14px) | 400 | `--color-text-muted` | |

#### Color usage

- Risk data points (hero numbers, category labels): `--color-warning` (amber) — consistent with risk theme
- Countermeasure labels: `--color-positive` (emerald) — signals resolution
- Column background: `--color-bg-surface`
- A 2px left border on each card: `--color-warning` (top half of card, the risk zone) transitioning to `--color-positive` at the divider — implement as two separate 2px border elements stacked, each covering half the card height.

#### Visual elements

Column 1 — Security:
- Category: "SECURITY RISK"
- Hero number: "48%"
- Description: "of AI-generated code contains potential vulnerabilities"
- Supporting: "10,000+ new security findings/month at enterprises"
- Countermeasure: "Mandatory security scanning as a CI/CD gate — not an afterthought"
- Source: Industry research; Qodo 2025

Column 2 — Technical Debt:
- Category: "TECH DEBT RISK"
- Hero number: "12.3%"
- Description: "of code is copy-pasted (up from 8.3% in 2020)"
- Supporting: "Refactoring activity dropped from 25% to under 10%"
- Countermeasure: "Track debt metrics alongside velocity; mandate refactoring sprints"
- Source: GitClear, 211M lines analyzed

Column 3 — Delivery Stability:
- Category: "STABILITY RISK"
- Hero number: "7.2%"
- Description: "decrease in delivery stability with 25% more AI adoption"
- Supporting: "Root cause: AI encourages larger changesets"
- Countermeasure: "Enforce smaller PRs as a team norm when using AI tools"
- Source: DORA 2024

#### Whitespace

- 60px slide padding
- 48px gap: title to card row
- 40px internal card padding all sides
- 24px gap at divider (12px above, 12px below)

---

### Slide 10 — The Trust Gap (Timeline / Trend)

**CSS class**: `.slide--chart .slide--chart--trend`
**Type**: Timeline / trend line
**Assertion title**: "Declining Developer Trust in AI Is a Sign of Maturity, Not Failure"

#### Layout

- Title: top, full width, `--font-title-sm` (36px)
- Framing statement: one line below title
- Main visual: trend chart occupying 55% of slide height, left-aligned, 60% of slide width
- Right panel (40% width): three key stats in a vertical list, vertically centered alongside the chart
- A vertical 1px divider separates chart zone and stat list

#### Typography

| Element | Size | Weight | Color |
|---|---|---|---|
| Slide title | 36px | 700 | `--color-text-primary` |
| Framing statement | 20px | 400 | `--color-text-secondary` |
| Chart axis labels | 14px | 400 | `--color-text-secondary` |
| Trust percentage line values | 16px | 700 | Curve color |
| Annotation text ("structured review") | 16px | 500 | `--color-text-primary` |
| Right panel stat numbers | 40px | 800 | varies |
| Right panel stat labels | 20px | 400 | `--color-text-secondary` |

#### Color usage

- Trust decline line: `--color-warning` (amber, 3px) — this is a negative trend
- "High performer" annotation box: `--color-positive-dim` background, `--color-positive` border, `--color-positive` label text
- Right panel: "71%" in `--color-positive`; "3%" in `--color-warning`; "67%" in `--color-warning`

#### Visual elements

**Left zone — Trust trend line chart:**

- X-axis: 2023 / 2024 / 2025
- Y-axis: 0% to 60% (trust level)
- Single amber line: 2023: ~52%, 2024: 42%, 2025: 33% — declining slope
- Data points: filled circles, 10px diameter, amber fill
- Value labels at each point: "52%", "42%", "33%"
- Annotation: a callout box (background `--color-positive-dim`, border `--color-positive`, 1px, `--chip-radius`) placed in the lower-right of the chart area. Arrow line from box pointing to the 2025 data point. Box text: "High performers maintain structured review — the workflow is the protection, not the trust level." Font: 14px, `--color-positive`.
- Chart background: `--color-bg-secondary`, `--card-radius`.

**Right zone — three key stats:**

Vertical stack, 32px between items:
- "71%" in 40px/800, `--color-positive` — "of developers refuse to merge without manual review"
- "3%" in 40px/800, `--color-warning` — "highly trust AI code without review"
- "67%" in 40px/800, `--color-warning` — "spend more time debugging AI-generated code"

Each stat is: number on first line, label on second line in `--font-body-sm` / `--color-text-secondary`.

#### Whitespace

- 60px slide padding
- Left zone: 60% width; right zone: 36%; 4% for the divider margin
- 28px gap: title to framing statement
- 32px gap: framing statement to chart/stat panel
- Right stat list: vertically centered within the panel height

---

### Slide 11 — Section Divider: Pillar 3

**CSS class**: `.slide--section-divider`
**Type**: Section divider
**Content**: "Pillar 3: The Strategic Edge Comes From Full-SDLC Integration"

#### Layout

Same template as Slides 5 and 8. Watermark numeral: "03".

| Element | Content | Color |
|---|---|---|
| Accent rule | 2px x 48px | `--color-accent` (returns to cyan) |
| Pillar label | "PILLAR 03" | `--color-accent` |
| Section title | "Pillar 3: The Strategic Edge Comes From Full-SDLC Integration" | `--color-text-primary` |
| Section subtitle | "From code completion to agentic workflows" | `--color-text-secondary` |
| Watermark numeral "03" | right zone | `rgba(6, 182, 212, 0.08)` |
| Top border | 1px full width | `--color-accent` |

Return to cyan palette signals the shift from risk acknowledgment back to forward-looking opportunity.

---

### Slide 12 — The SDLC Integration Opportunity (Horizontal Flow)

**CSS class**: `.slide--flow`
**Type**: Timeline / horizontal flow diagram
**Assertion title**: "Teams Using AI Across Four or More SDLC Phases See 31–45% Quality Improvements"

#### Layout

- Title: top, full width, `--font-title-sm` (36px)
- Subtitle stat: one line below title
- SDLC pipeline diagram: occupies 60% of slide height, vertically centered in remaining space, full horizontal width minus `--pad-slide`
- Below pipeline: a 3-column stat row with the supporting evidence

Pipeline zone: six stage nodes connected by arrows. Horizontal flow, left to right.

Stat row: three inline stats separated by vertical `--color-border-subtle` rules.

#### Typography

| Element | Size | Weight | Color |
|---|---|---|---|
| Slide title | 36px | 700 | `--color-text-primary` |
| Subtitle stat | 20px | 400 | `--color-text-secondary` |
| Stage node label | 16px | 700 | `--color-text-primary` |
| Stage AI use case (below label) | 14px | 400 | `--color-text-secondary` |
| Stage data callout | 20px | 700 | `--color-accent` or `--color-positive` |
| Arrow glyphs | 20px | — | `--color-accent-border` |
| Stat row number | 40px | 800 | `--color-accent` |
| Stat row label | 16px | 400 | `--color-text-secondary` |
| Source | 14px | 400 | `--color-text-muted` |

#### Color usage

- "Current high adoption" stages (Code Generation, Testing, Documentation): node border `--color-accent`, node background `--color-accent-dim`
- "Emerging adoption" stages (Planning, Review, Deployment): node border `--color-border-accent` at 50% opacity, node background `--color-bg-surface` — slightly dimmer to show opportunity headroom
- Arrow connectors: `--color-accent-border`
- Stage callout badge: `--color-accent` text on `--color-accent-dim` background

#### Visual elements

**SDLC pipeline — six nodes connected by arrows:**

Each node is a rounded rectangle (160px wide x 100px tall, `--card-radius`):

Node 1 — Planning (emerging):
- Label: "PLANNING"
- AI use: "Requirements analysis, dependency mapping"
- Dimmer styling

Node 2 — Code Generation (active):
- Label: "CODE GEN"
- AI use: "Completion, boilerplate, scaffolding"
- Callout badge: "72%" (adoption rate)
- Full accent styling

Node 3 — Code Review (active):
- Label: "REVIEW"
- AI use: "PR summaries, security flagging"
- Callout badge: "67%"
- Full accent styling

Node 4 — Testing (active):
- Label: "TESTING"
- AI use: "Test generation, regression, coverage"
- Callout badge: "56%"
- Full accent styling

Node 5 — Documentation (active):
- Label: "DOCS"
- AI use: "Inline docs, changelogs, arch summaries"
- Callout badge: "67%"
- Full accent styling

Node 6 — Deployment (emerging):
- Label: "DEPLOYMENT"
- AI use: "Anomaly detection, rollback automation"
- Dimmer styling

Arrows: right-pointing chevron glyphs (">") or SVG path connecting node right-edge to next node left-edge. Color: `--color-accent-border`. Width: 32px between nodes.

**Below pipeline — stat row (3 columns):**

- "6-7x" / "More likely to scale to 4+ use cases" / McKinsey
- "31-45%" / "Software quality improvement" / McKinsey
- "21%" / "of Google's code is AI-assisted" / Google

Separated by 1px vertical rules in `--color-border-subtle`.

#### Whitespace

- 60px slide padding
- 16px gap: title to subtitle
- 40px gap: subtitle to pipeline
- 36px gap: pipeline to stat row
- Pipeline nodes: equal horizontal spacing across full content width

---

### Slide 13 — The Agentic Horizon (Quote / Forward-Looking)

**CSS class**: `.slide--quote`
**Type**: Quote / comparison
**Assertion title**: "The Next Shift: Developers Will Function as Orchestrators of AI Agent Teams"

#### Layout

Split layout — two panels side by side, each 50% width with a 48px gap.

- Title: top, full width, `--font-title-sm` (36px)
- Below title: two cards — "TODAY: AI Assistant" (left) and "NEXT: AI Agent" (right)
- Card height: approximately 480px
- Below cards: a single McKinsey quote rendered as a blockquote strip

Each card:
- Header bar at top (48px tall) in `--color-bg-surface` with category label centered
- Content area: 28px padding, describes the mode

Blockquote strip: full width, `--color-bg-secondary` background, 4px left border in `--color-accent`, 32px vertical padding.

#### Typography

| Element | Size | Weight | Color |
|---|---|---|---|
| Slide title | 36px | 700 | `--color-text-primary` |
| Card category label | 14px | 700 | varies | All-caps |
| Card mode label | 28px | 700 | `--color-text-primary` | |
| Card description lines | 20px | 400 | `--color-text-secondary` | |
| Flow step labels | 16px | 500 | `--color-text-primary` | |
| Blockquote text | 24px | 400 | `--color-text-primary` | Italic style |
| Quote attribution | 16px | 400 | `--color-text-secondary` | |
| Market stat below quote | 28px | 700 | `--color-accent` | |

#### Color usage

- Left card "TODAY" header: `--color-bg-surface`; label: `--color-text-secondary`
- Right card "NEXT" header: `--color-accent-dim`; label: `--color-accent`
- Right card border: 2px solid `--color-accent`
- Left card border: 1px solid `--color-border-subtle`
- Blockquote left border: `--color-accent`

#### Visual elements

**Left card — "AI Assistant" mode:**

Flow description as a 4-step vertical sequence with connector arrows:
1. Developer writes prompt
2. AI generates code
3. Developer reviews and edits
4. Developer commits

Each step: small circle node (16px, `--color-bg-surface` fill, `--color-border-subtle` stroke) + step label at 16px. Connector: dashed vertical line, 1px, `--color-text-muted`.

**Right card — "AI Agent" mode:**

Same 4-step structure but different steps:
1. Developer specifies intent
2. Agent plans approach
3. Agent executes, tests, iterates
4. Developer reviews outcome + deploys

Right card step nodes: `--color-accent-dim` fill, `--color-accent-border` stroke — visually distinct from left card.

"Human role" badge at bottom of right card: pill shape, `--color-positive-dim` background, `--color-positive` text — "HUMAN ROLE: Specification + Oversight"

**Blockquote strip:**

> "Individual contributors will spend part of their time as engineering managers directing a junior team of asynchronous agents."

Attribution: "— McKinsey & Company, 2025"

Below the quote, right-aligned: "$37B enterprise AI spend in 2025 — up from $11.5B in 2024" in `--color-accent` / 24px / bold.

#### Whitespace

- 60px slide padding
- 24px gap: title to cards
- 40px gap: cards to blockquote strip
- Blockquote strip: 32px vertical padding inside

---

### Slide 14 — What the Best Teams Do Differently (Icons / Grid)

**CSS class**: `.slide--icons`
**Type**: Icons / best practices
**Assertion title**: "The Differentiator Is Discipline Around the Tools, Not the Tools Themselves"

#### Layout

- Title: top, full width, `--font-title-sm` (36px)
- One-line framing: "How many of these six does your team have in place today?"
- Six-item grid: 3 columns x 2 rows of practice cards
- Card dimensions: ~580px wide x 156px tall
- Grid gap: 28px (columns and rows)
- Grid centered with 80px side margins (inside the 60px slide padding = 140px effective left/right margin; adjust to 60px padding + fit grid)

Actual grid calc: 3 cards x 560px + 2 x 28px = 1736px. At 1920 wide with 60px padding each side = 1800px content area. Adjust card to 580px: 3 x 580 + 2 x 28 = 1796px — fits with 2px to spare. Use 580px cards.

Each card: icon on left (48 x 48px), text content (title + description) on right. Card has 24px internal padding.

#### Typography

| Element | Size | Weight | Color |
|---|---|---|---|
| Slide title | 36px | 700 | `--color-text-primary` |
| Framing question | 20px | 400 | `--color-text-secondary` |
| Practice number (e.g., "01") | 14px | 700 | `--color-text-muted` | Inside card, top-left |
| Practice title | 20px | 700 | `--color-text-primary` | |
| Practice description | 16px | 400 | `--color-text-secondary` | Max 2 lines |

#### Color usage

- Card background: `--color-bg-surface`
- Card left accent border: 3px solid `--color-accent`
- Card hover state (if interactive): background `--color-bg-secondary` — for presenter animation use
- Icons: `--color-accent` (all six use the same accent color — these are all positive signals)
- Practice number: `--color-text-muted`

#### Visual elements

Six practice cards, 3 x 2 grid:

Row 1:
- Card 1: Number "01" | Icon: document with shield | Title: "Written AI Tool Policy" | Description: "Approved tools, review standards, security gates — documented and shared"
- Card 2: Number "02" | Icon: chart with up-arrow | Title: "Measurement Before and After" | Description: "Deployment frequency, change failure rate, PR cycle time — tracked as baselines"
- Card 3: Number "03" | Icon: compact stack of cards | Title: "Small PRs Enforced" | Description: "Counter the DORA-identified batch-size risk that AI tools amplify"

Row 2:
- Card 4: Number "04" | Icon: lock with checkmark | Title: "Security Scanning as CI/CD Gate" | Description: "Not optional, not manual — automated for every AI-generated code path"
- Card 5: Number "05" | Icon: horizontal flow nodes | Title: "Whole-SDLC Adoption" | Description: "Documentation, testing, review — not just code completion"
- Card 6: Number "06" | Icon: person with guardrail | Title: "Developer Autonomy Within Guardrails" | Description: "Trust engineers to calibrate; give them the policy, not the workflow prescription"

Icons: 48 x 48px, drawn as outline vectors (2px stroke, no fill), `--color-accent`. Use a geometric, minimal style — no illustrative details.

#### Whitespace

- 60px slide padding
- 16px gap: title to framing question
- 40px gap: framing question to grid
- 24px internal card padding
- 28px grid gaps

---

### Slide 15 — Call to Action

**CSS class**: `.slide--cta`
**Type**: CTA
**Assertion title**: "Three Actions. Three Time Horizons. Start This Week."

#### Layout

This slide intentionally carries less information density than slides 6, 9, and 12. White space is strategic here — it gives the audience room to breathe and absorb the action items.

- Title: top, full width, `--font-title` (44px) — returns to the larger title size used on slides 1 and 2
- Subtitle: one line below title
- Three-column action card layout: equal thirds
- Each card has a prominent time horizon label at top, followed by the action text
- Source strip: none needed — this slide is forward-looking

Card dimensions:
- Content area width: 1920 - 120px padding = 1800px
- Three columns: (1800 - 2 x 48px gap) / 3 = 568px each
- Card height: 320px

A subtle bottom strip (full width, 64px tall) in `--color-bg-secondary` anchors the slide — contains a single short closing line.

#### Typography

| Element | Size | Weight | Color |
|---|---|---|---|
| Slide title | 44px | 700 | `--color-text-primary` | |
| Subtitle | 24px | 400 | `--color-text-secondary` | "Strategic AI adoption starts with small, deliberate steps" |
| Time horizon label (e.g. "THIS WEEK") | 14px | 700 | Card accent color | All-caps, `--ls-label` |
| Owner label (e.g. "Individual") | 20px | 600 | `--color-text-secondary` | |
| Action text | 22px | 400 | `--color-text-primary` | 3-4 lines; line-height 1.5 |
| Closing line in bottom strip | 18px | 400 | `--color-text-secondary` | Centered |

#### Color usage

Each column has its own accent color to help the time horizon concept register visually:

- Column 1 "THIS WEEK": accent `--color-accent` (cyan) — immediate, actionable
- Column 2 "THIS SPRINT": accent `--color-positive` (emerald) — team-scale action
- Column 3 "THIS QUARTER": accent `--color-warning` (amber) — strategic, leadership
- Card backgrounds: `--color-bg-surface` for all three — same surface, differentiated by top accent strip
- Top accent strip on each card: 4px tall, full card width, in the card's accent color

#### Visual elements

**Three action cards** — each card structure:

Top: 4px accent color bar (full card width, top-flush)
Padding: 28px all sides

Card 1 — THIS WEEK (Cyan):
- Time horizon: "THIS WEEK"
- Owner: "Individual Action"
- Action: "Pick one task category. Run a two-week experiment with an AI tool. Measure before and after. Document what you learn."

Card 2 — THIS SPRINT (Emerald):
- Time horizon: "THIS SPRINT"
- Owner: "Team Action"
- Action: "Write your AI tool policy. Approved tools, mandatory review standard, security scanning requirement. One hour. Prevents six months of drift."

Card 3 — THIS QUARTER (Amber):
- Time horizon: "THIS QUARTER"
- Owner: "Leadership Action"
- Action: "Establish a measurement baseline. Deployment frequency, change failure rate, PR cycle time. Make the data visible to the team."

**Bottom strip (64px, `--color-bg-secondary`):**
Centered text: "The teams that will look back on 2025–2026 as a turning point are the ones that started building structured, disciplined workflows now."
Font: 18px / 400 / `--color-text-secondary`. Italic.

No icons. No charts. The card structure and the three action statements are the entire visual content of this slide. The deliberate reduction in density signals the close.

#### Whitespace

- 60px slide padding (except bottom where the full-width strip touches edge)
- 16px gap: title to subtitle
- 48px gap: subtitle to cards
- 48px gap between columns (same as `--gap-columns`)
- 48px gap: cards to bottom strip
- 28px internal card padding

---

## Slide Type Summary Reference

| Slide | CSS Class | Type | Primary Color Role |
|---|---|---|---|
| 1 | `.slide--title` | Title | Accent rule only |
| 2 | `.slide--stat` | Stat hero | Accent for hero number |
| 3 | `.slide--split` | Two-column split | Warning (left), neutral (right) |
| 4 | `.slide--chart` | Divergence chart | Accent + positive + warning gap |
| 5 | `.slide--section-divider` | Section divider | Accent (Pillar 1) |
| 6 | `.slide--chart .slide--chart--dense` | Paired bar chart | Accent bars vs surface bars |
| 7 | `.slide--stat-grid` | Stat card grid | Accent for all numbers |
| 8 | `.slide--section-divider` | Section divider | Warning (Pillar 2) |
| 9 | `.slide--comparison` | Three-column comparison | Warning (risk), positive (countermeasure) |
| 10 | `.slide--chart .slide--chart--trend` | Trend + stat panel | Warning trend, positive annotation |
| 11 | `.slide--section-divider` | Section divider | Accent (Pillar 3) |
| 12 | `.slide--flow` | SDLC pipeline + stat row | Accent active, dim for emerging |
| 13 | `.slide--quote` | Before/after + blockquote | Accent (agent card), neutral (assistant card) |
| 14 | `.slide--icons` | Six-card best practices | Accent icons, surface cards |
| 15 | `.slide--cta` | Three-column CTA | Cyan / Emerald / Amber per column |

---

## Accessibility Annotations

**Color contrast**: All text combinations must meet WCAG 2.1 AA (4.5:1 for body text, 3:1 for large text).

Verified pairings:
- `--color-text-primary` (#f8fafc) on `--color-bg-primary` (#0f172a): contrast ratio ~15.6:1 — passes AAA
- `--color-text-secondary` (#94a3b8) on `--color-bg-primary` (#0f172a): contrast ratio ~6.4:1 — passes AA
- `--color-accent` (#06b6d4) on `--color-bg-primary` (#0f172a): contrast ratio ~6.9:1 — passes AA for large text; verify at `--font-label` size (16px)
- `--color-warning` (#f59e0b) on `--color-bg-primary` (#0f172a): contrast ratio ~8.2:1 — passes AA
- `--color-positive` (#10b981) on `--color-bg-primary` (#0f172a): contrast ratio ~5.8:1 — passes AA

**Do not rely on color alone**: All risk data on Slide 9 is labeled "SECURITY RISK", "TECH DEBT RISK", "STABILITY RISK" — not just differentiated by color. All positive/negative chart data is labeled numerically.

**Font minimums**: No text rendered below 14px (`--font-caption`). At 14px on dark backgrounds, use `--color-text-secondary` minimum (not `--color-text-muted`) unless the text is purely supplementary and its absence does not change comprehension.

**Slide structure**: Each slide must have exactly one H1-equivalent element (the title). Section dividers may omit this — the section label ("PILLAR 01") serves the heading role in those cases.

---

## Implementation Notes for Developers

1. **Slide canvas size**: Design at 1920 x 1080px. If implementing in CSS, set the slide container to `aspect-ratio: 16/9` and `width: 100%` — font sizes will need to scale proportionally using `vw` units or CSS `clamp()`. Provided pixel values are for 1920px reference.

2. **Font loading**: Load Inter from Google Fonts or bundle via `@fontsource/inter`. Weights required: 400, 500, 600, 700, 800.

3. **Chart implementation**: Bar charts and line charts should be implemented in SVG or a library such as Recharts or D3. Do not use canvas — SVG preserves accessibility and vector quality for projection.

4. **Section divider watermark numerals**: Implement as `::before` or `::after` pseudo-elements with `position: absolute`, `pointer-events: none`, `user-select: none`, `aria-hidden: true` on the parent.

5. **Slide padding consistency**: Apply `--pad-slide` (60px) to all slides via a shared `.slide` base class. Individual slide types add their own internal layout on top of this base.

6. **Icon set**: Use Heroicons (outline style) or Phosphor Icons (regular weight) — both are available as SVG sets and match the geometric, minimal aesthetic required. Do not use filled icons.

7. **Print / export**: If PDF export is required, test at 1920x1080 → 297x167mm (A4 landscape). Font sizes may need a +2px adjustment at print resolution.

8. **Base slide class structure**:

```css
.slide {
  position: relative;
  width: 1920px;
  height: 1080px;
  background: var(--color-bg-primary);
  padding: var(--pad-slide);
  font-family: var(--font-family);
  color: var(--color-text-primary);
  overflow: hidden;
  box-sizing: border-box;
}

.slide--section-divider {
  background: var(--color-bg-secondary);
}

.slide__title {
  font-size: var(--font-title);
  font-weight: var(--font-title-weight);
  line-height: var(--lh-heading);
  letter-spacing: var(--ls-heading);
  color: var(--color-text-primary);
  margin: 0 0 28px 0;
}

.slide__title--sm {
  font-size: var(--font-title-sm);
}

.slide__source {
  font-size: var(--font-caption);
  color: var(--color-text-muted);
  line-height: var(--lh-caption);
}

.slide__label {
  font-size: var(--font-label);
  font-weight: 700;
  letter-spacing: var(--ls-label);
  text-transform: uppercase;
}
```
