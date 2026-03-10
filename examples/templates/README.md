# Slide Type Templates

18 slide type templates, each with 3 design variants across multiple color palettes. Every template is a self-contained reveal.js HTML file that opens directly in Chrome.

## Template Index

| File | Slide Type | Variants | Palettes | Best Audience |
|------|-----------|----------|----------|---------------|
| `slide_type_01_title.html` | Title | A: Corporate gradient, B: Technical dark, C: Split design | Corporate, Technical | Any |
| `slide_type_02_section_divider.html` | Section Divider | A: Bold color + number, B: Minimal accent line, C: Dark gradient accent | Corporate | Any |
| `slide_type_03_split_layout.html` | Content + Image (Split) | A: Text + gradient panel, B: Data viz + explanation, C: Geometric pattern | Corporate, Technical | Any |
| `slide_type_04_full_bleed.html` | Full-Bleed Image | A: Gradient + statistic, B: Dark gradient + quote, C: Gradient mesh + heading | Corporate | Any |
| `slide_type_05_data_chart.html` | Data/Chart | A: Horizontal bar chart, B: Donut chart, C: Comparison metric bars | Corporate, Technical, Sales | Executives, analysts |
| `slide_type_06_quote.html` | Quote | A: Centered large marks, B: Side-accent dark, C: Split color + white | Corporate | Any |
| `slide_type_07_comparison.html` | Comparison | A: Side-by-side ML approaches, B: Before/after pipeline, C: Pros/cons | Corporate, Technical | Decision-makers |
| `slide_type_08_timeline.html` | Timeline/Process | A: Horizontal 5-step pipeline, B: Vertical timeline, C: Circular/cyclical | Corporate | Any |
| `slide_type_09_statistics.html` | Statistics/Big Number | A: Single massive number, B: Three in a row, C: Number with comparison | Corporate | Executives, investors |
| `slide_type_10_team_bio.html` | Team/Bio | A: 2x2 grid, B: Single featured leader, C: Horizontal row of 4 | Corporate, Creative | Any |
| `slide_type_11_icon_grid.html` | Icon Grid | A: 2x3 DS capabilities, B: 3x1 horizontal pillars, C: 4-icon ML features | Corporate, Technical, Creative | Any |
| `slide_type_12_cta.html` | Closing/CTA | A: Corporate next steps, B: Bold dark gradient, C: Summary + CTA split | Corporate | Any |
| `slide_type_13_dashboard.html` | Dashboard/Multi-KPI | A: 2x2 KPI grid + sparklines, B: 3-across horizontal strip, C: 4 donuts | Corporate, Technical | Executives, managers |
| `slide_type_14_before_after.html` | Before/After Metrics | A: Two-column split, B: Timeline arrow + delta, C: Stacked cards + badges | Corporate, Technical | Decision-makers |
| `slide_type_15_code_explain.html` | Code + Explanation | A: Side-by-side code + text, B: Top code + annotated callouts, C: 3-step progression | Technical | Engineers, data scientists |
| `slide_type_16_model_perf.html` | Model Performance | A: 2x2 metrics grid, B: Confusion matrix + metrics, C: Model comparison table | Technical | Data scientists, ML engineers |
| `slide_type_17_architecture.html` | Architecture/Pipeline | A: Horizontal data pipeline, B: Vertical ML stack, C: Hub-and-spoke | Technical | Engineers, architects |
| `slide_type_18_funnel.html` | Funnel/Conversion | A: Vertical funnel + drop-offs, B: Horizontal pipeline, C: Side-by-side comparison | Corporate, Sales | Sales, marketing, product |

## How to Use

### Opening templates

Open any `.html` file directly in Chrome. Each file is a reveal.js presentation containing 3 slides (one per variant). Navigate between variants with arrow keys.

### Copying a variant into your presentation

1. Open the template HTML in a text editor
2. Find the variant you want -- each is marked with a comment like `<!-- Variant B: Timeline arrow with before/after metrics -->`
3. Copy the entire `<section>...</section>` block
4. Paste it into your presentation's `<div class="slides">` container
5. Copy the corresponding CSS styles from the `<style>` block (each variant's CSS is clearly labeled with `/* ===== Variant B: ... ===== */`)
6. Replace placeholder content where you see `<!-- CUSTOMIZATION: ... -->` comments

### Adapting to your palette

All templates use CSS custom properties defined in `:root`. To switch palettes:

```css
/* Override in your presentation's <style> block */
:root {
  --corp-navy: #your-primary;
  --corp-blue: #your-accent;
  --corp-light: #your-background;
  --corp-white: #ffffff;
  --corp-emerald: #your-positive;
  --corp-rose: #your-negative;
}
```

Or use the Technical (`--tech-*`) or Sales (`--sales-*`) token prefixes if those palettes are closer to your needs.

## Design Rules

Every template in this library follows these rules:

1. **Assertion-evidence model** -- Slide titles are full sentences stating the takeaway, not topic labels. The body provides visual evidence.
2. **CSS custom properties** -- All colors, fonts, sizes, and spacing use the design tokens defined in `:root`. No hardcoded values in component CSS.
3. **No bullet points** -- Body content uses visual evidence: charts, grids, diagrams, large numbers, or structured layouts. Never raw bullet lists.
4. **One idea per slide** -- Each variant demonstrates exactly one content pattern. Complex information is split across multiple slides.
5. **WCAG AA contrast** -- All text/background combinations meet minimum 4.5:1 contrast ratio.
6. **Minimum 18px text** -- No text element goes below `--text-caption` (18px). Most body text is 24px+.
7. **30%+ whitespace** -- Every slide maintains at least 30% whitespace through `--slide-padding` and `--element-gap`.
8. **Image-free by design** -- All templates use CSS gradients, shapes, and typography instead of external images. `<!-- IMAGE_PLACEHOLDER: ... -->` comments mark where real images would improve the slide.
9. **Speaker notes included** -- Each variant contains `<aside class="notes">` with example speaker notes demonstrating the script format.
10. **Three variants per type** -- Variant A, B, and C provide different layouts and palette treatments so designers can pick the best fit without starting from scratch.
