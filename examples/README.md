# Examples Library

Enhancement resources for the Presentation Creator system (`.claude_prompts/presentation-creator-prompt.md`). This library provides reusable slide templates, CSS pattern references, design system documentation, and research-backed design patterns that extend the core 12-slide-type system to 18 types.

## Quick Start

1. Open any template HTML file in Chrome to see it rendered as a reveal.js presentation
2. Press `S` to view speaker notes on template slides
3. Browse the slide types, pick what fits your content, and copy the `<section>` block into your own presentation

## Folder Structure

```
examples/
├── README.md                  # This file
├── integration_recommendations.md  # How to integrate this library into the main prompt
├── research/
│   ├── design_patterns_catalog.md  # 40 patterns across 8 categories with sources
│   └── sources.md                  # 43 citations (books, papers, consulting frameworks)
├── templates/
│   ├── README.md                   # Template index with usage instructions
│   ├── slide_type_01_title.html    # ... through slide_type_18_funnel.html
│   └── (18 template files total)
├── showcases/                      # Full example presentations (planned)
│   ├── executive_briefing.html     # 10 slides, 10 min, C-suite
│   ├── technical_review.html       # 12 slides, 15 min, ML engineers
│   └── board_presentation.html     # 8 slides, 8 min, Board/investors
├── css_patterns/
│   ├── gradients.html              # Gradient patterns for image-free backgrounds
│   ├── data_viz_css.html           # Pure CSS chart and visualization patterns
│   ├── layout_grids.html           # Grid layout systems for complex slides
│   └── typography_treatments.html  # Typographic styles for emphasis and hierarchy
└── design_system/
    ├── color_palettes.html         # All 4 palettes with swatches and usage rules
    ├── typography_scale.html       # Type scale, pairings, and responsive sizing
    └── component_library.html      # Reusable micro-components (planned)
```

## How to Use Templates

### Step 1: Browse templates

Open any `templates/slide_type_*.html` file in Chrome. Each file contains 3 variants of that slide type, rendered across different color palettes (Corporate, Technical, Sales).

### Step 2: Pick a slide type

Use the reference table below to find the right slide type for your content. Each template file contains 3 design variants (A, B, C) so you can pick the layout that fits your tone and audience.

### Step 3: Copy the `<section>` HTML

Open the template source and find the variant you want. Each variant is wrapped in a `<section>` tag with a clear comment header:

```html
<!-- Variant A: Corporate palette — clean text on gradient background -->
<section class="slide-title-gradient">
  <!-- CUSTOMIZATION: Change title, subtitle, presenter info -->
  ...
</section>
```

Copy the entire `<section>` block into your presentation's `<div class="slides">` container.

### Step 4: Customize content

Look for `<!-- CUSTOMIZATION: ... -->` comments inside each variant. These mark the content you should replace: titles, data values, labels, colors, and descriptions. The CSS classes and structure should remain intact.

### Step 5: Adjust palette

Each template uses CSS custom properties (`--corp-navy`, `--tech-charcoal`, `--sales-blue`, etc.). To switch palettes, either swap the class prefix in your CSS or redefine the custom property values in your presentation's `:root` block.

## Slide Type Reference

| # | Type | File | Description | Best For |
|---|------|------|-------------|----------|
| 1 | Title | `slide_type_01_title.html` | Presentation title with full-bleed background or gradient | Opening slide for any presentation |
| 2 | Section Divider | `slide_type_02_section_divider.html` | Bold color background with section number and title | Transitions between major sections |
| 3 | Content + Image (Split) | `slide_type_03_split_layout.html` | Two-column layout: text + visual panel | Explaining concepts with supporting visuals |
| 4 | Full-Bleed Image | `slide_type_04_full_bleed.html` | Edge-to-edge gradient with overlaid text | Emotional impact, storytelling moments |
| 5 | Data/Chart | `slide_type_05_data_chart.html` | Single chart with assertion title | Presenting data-driven evidence |
| 6 | Quote | `slide_type_06_quote.html` | Large quotation with attribution | Expert endorsement, thought leadership |
| 7 | Comparison | `slide_type_07_comparison.html` | Side-by-side comparison layout | Before/after, pros/cons, option A vs B |
| 8 | Timeline/Process | `slide_type_08_timeline.html` | Horizontal/vertical/circular flow | Showing steps, pipelines, workflows |
| 9 | Statistics/Big Number | `slide_type_09_statistics.html` | Massive numbers with descriptors | Shock value, emphasis on key metrics |
| 10 | Team/Bio | `slide_type_10_team_bio.html` | Photo grid with name, title, bio | Team introductions, leadership slides |
| 11 | Icon Grid | `slide_type_11_icon_grid.html` | 3-6 icons with labels in grid | Features, pillars, capabilities |
| 12 | Closing/CTA | `slide_type_12_cta.html` | Call-to-action with contact info | Final slide, next steps |
| 13 | Dashboard/Multi-KPI | `slide_type_13_dashboard.html` | 2x2 or 3-across KPI grid with sparklines | Executive status updates, quarterly reviews |
| 14 | Before/After Metrics | `slide_type_14_before_after.html` | Split or timeline layout showing change | Impact measurement, ROI demonstrations |
| 15 | Code + Explanation | `slide_type_15_code_explain.html` | Syntax-highlighted code with annotations | Technical deep-dives, API walkthroughs |
| 16 | Model Performance | `slide_type_16_model_perf.html` | Metrics grid, confusion matrix, model comparison | ML model evaluation, data science reviews |
| 17 | Architecture/Pipeline | `slide_type_17_architecture.html` | Horizontal, vertical, or hub-spoke diagrams | System design, data pipelines, infrastructure |
| 18 | Funnel/Conversion | `slide_type_18_funnel.html` | Vertical or horizontal funnel with drop-offs | Sales pipelines, user conversion, process attrition |

## Design System

The `design_system/` directory contains interactive HTML references for the visual foundations used across all templates.

- **`color_palettes.html`** -- All 4 palettes (Corporate, Technical, Creative, Sales) with hex values, contrast ratios, and usage guidelines. Includes the 60-30-10 rule applied to each palette.
- **`typography_scale.html`** -- The type scale from `--text-caption` (18px) through `--text-hero` (72px), font pairings, line-height rules, and responsive sizing guidance.
- **`component_library.html`** (planned) -- Reusable micro-components: cards, badges, progress bars, stat blocks, annotation callouts.

Open these files in Chrome to see every design token rendered with live examples.

## CSS Patterns

The `css_patterns/` directory provides copy-ready CSS solutions for common presentation design challenges -- particularly useful when generating HTML without access to images.

- **`gradients.html`** -- Linear, radial, and conic gradient patterns across all 4 palettes. Use these as LLM-generated image fallbacks for full-bleed and split-layout slides.
- **`data_viz_css.html`** -- Pure CSS charts: horizontal bars, donut charts (conic-gradient), sparklines, progress bars, and gauge indicators. No JavaScript or SVG required.
- **`layout_grids.html`** -- Grid systems for complex layouts: 2-column, 3-column, 2x2, dashboard grids, and asymmetric splits. Each with proper spacing and responsive behavior.
- **`typography_treatments.html`** -- Large-number treatments, pull-quote styling, hierarchical text blocks, and label/value pair layouts for statistics slides.

## Showcases

*Note: Showcase files are planned but not yet generated.*

Three complete example presentations demonstrating the system at its best:

| Showcase | Slides | Duration | Audience | Palette | Slide Types Used |
|----------|--------|----------|----------|---------|-----------------|
| Executive Briefing | 10 | 10 min | C-suite | Corporate | Title, Section Divider, Dashboard, Before/After, Statistics, Data/Chart, CTA |
| Technical Review | 12 | 15 min | ML engineers | Technical | Title, Code+Explain, Model Performance, Architecture, Data/Chart, Timeline, CTA |
| Board Presentation | 8 | 8 min | Board/investors | Sales | Title, Statistics, Funnel, Before/After, Data/Chart, Comparison, CTA |

Each showcase is a self-contained HTML file that opens in Chrome and demonstrates the full pipeline: narrative arc, design system, speaker notes, and timing.

## Research

The `research/` directory contains the evidence base for all design decisions:

- **`design_patterns_catalog.md`** -- 40 patterns across 8 categories (data visualization, narrative structure, layout, typography, color, animation, technical content, executive communication). Each pattern includes source attribution, effectiveness rationale, target audience, and CSS/HTML implementation approach.
- **`sources.md`** -- 43 citations covering foundational texts (Tufte, Minto, Duarte, Reynolds, Knaflic), consulting firm conventions (McKinsey, BCG, Bain), tech company design systems, and data science conference practices.

## How to Contribute

### Adding a new slide type template

1. Create `slide_type_NN_name.html` in `templates/`
2. Include 3 variants (A, B, C) across at least 2 different palettes
3. Use the standard design tokens from `:root` (copy from any existing template)
4. Add `<!-- CUSTOMIZATION: ... -->` comments at every point where content should be swapped
5. Include `<aside class="notes">` with example speaker notes
6. Update the table in `templates/README.md`

### Adding a CSS pattern

1. Add to the appropriate file in `css_patterns/` (or create a new category file)
2. Each pattern needs: a visible rendered example, the CSS source in a `<pre>` block, and a one-line description of when to use it

### Adding a design pattern to the catalog

1. Follow the entry format in `research/design_patterns_catalog.md`
2. Include: pattern name, source, effectiveness rationale, target audience, slide type mapping, and CSS/HTML approach
3. Add the source citation to `research/sources.md`
