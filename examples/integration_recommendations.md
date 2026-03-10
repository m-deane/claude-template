# Integration Recommendations

Specific, actionable changes to integrate the examples library back into the main presentation creator prompt (`.claude_prompts/presentation-creator-prompt.md`).

---

## 1. Add 6 New Slide Types to Agent 2

**Section to modify**: `Agent 2: Slide Architect & Designer` > `Slide Type Templates` (lines 69-84)

**Why**: The core prompt defines 12 slide types. The examples library adds 6 data-science-oriented types (13-18) that fill gaps for dashboard summaries, before/after impact measurement, code walkthroughs, model evaluation, system architecture, and conversion funnels. These are the most commonly needed slide types for technical and executive data science presentations that the original 12 do not cover well.

**Current text (line 71)**:
```markdown
Design these **12 essential slide types**:
```

**Replace with**:
```markdown
Design these **18 essential slide types**:
```

**Current text ends at line 84 with**:
```markdown
12. **Closing/CTA Slide** — Clear call-to-action. Contact info. Memorable closing statement. Clean and actionable
```

**Add after line 84**:
```markdown
13. **Dashboard/Multi-KPI** — 2x2 or 3-across grid of KPI cards with trend indicators (sparklines, arrows, delta values). Assertion title states the overall status. Each card: metric name, large number, trend indicator, period comparison. For executive status updates and quarterly reviews. See `examples/templates/slide_type_13_dashboard.html` for 3 variants
14. **Before/After Metrics** — Split layout showing measurable change: left column shows "before" state, right column shows "after" state, with delta indicators (percentage improvement, absolute change) highlighted between them. Assertion title states the impact. For ROI demonstrations and impact measurement. See `examples/templates/slide_type_14_before_after.html` for 3 variants
15. **Code + Explanation** — Side-by-side or top/bottom layout: one panel contains syntax-highlighted code (use monospace font, dark background, colored tokens for keywords/strings/comments), the other panel contains 2-3 annotated callouts explaining what the code does and why it matters. For technical deep-dives and API walkthroughs. See `examples/templates/slide_type_15_code_explain.html` for 3 variants
16. **Model Performance** — Metrics grid showing ML evaluation results: accuracy, precision, recall, F1, AUC — presented as large numbers with color-coded thresholds (green/amber/red). Can include a CSS confusion matrix or model comparison table. Assertion title states whether the model meets production criteria. See `examples/templates/slide_type_16_model_perf.html` for 3 variants
17. **Architecture/Pipeline** — CSS-drawn diagram showing system components and data flow: horizontal pipeline (left-to-right stages with arrows), vertical stack (layered architecture), or hub-and-spoke (central service with connected components). 3-6 nodes max, labeled with short names. For system design and data pipeline presentations. See `examples/templates/slide_type_17_architecture.html` for 3 variants
18. **Funnel/Conversion** — Vertical or horizontal funnel visualization showing progressive narrowing with counts and drop-off percentages at each stage. Stages are rendered as CSS trapezoids or progressively narrower bars. For sales pipelines, user conversion flows, and process attrition analysis. See `examples/templates/slide_type_18_funnel.html` for 3 variants
```

**Also update the HTML Slide Patterns list** in Agent 4 (lines 202-214). After `.slide-cta`, add:

```markdown
- `.slide-dashboard` — Multi-KPI grid with trend indicators
- `.slide-before-after` — Before/after metrics with delta highlights
- `.slide-code` — Code + explanation split layout
- `.slide-model-perf` — Model performance metrics grid
- `.slide-architecture` — Architecture/pipeline diagram
- `.slide-funnel` — Funnel/conversion visualization
```

---

## 2. Update Agent 2 Image Fallback Section

**Section to modify**: `Agent 2: Slide Architect & Designer` > `Image & Visual Guidelines` > `LLM Execution Context` (lines 90-94)

**Why**: The current fallback guidance is generic ("bold CSS gradient," "geometric shapes"). The examples library provides concrete, tested CSS patterns that produce professional results. Pointing agents to these reference files eliminates guesswork and improves visual quality of LLM-generated presentations.

**Current text (lines 90-94)**:
```markdown
**LLM Execution Context**: When generating HTML without access to an image library, use the following fallbacks:
- Full-Bleed Image slides → Replace with a bold CSS gradient using the brand palette + large typographic treatment (stat, quote, or section heading)
- Content + Image slides → Replace with a split-layout slide using a CSS-illustrated panel (gradient, geometric shapes, or large icon) on the right side
- Add `<!-- IMAGE_PLACEHOLDER: [description] -->` HTML comments at each point where a real image would improve the slide, so a human can substitute images post-generation
- NEVER leave `[IMAGE: ...]` text visible in the output — always provide a designed fallback
```

**Replace with**:
```markdown
**LLM Execution Context**: When generating HTML without access to an image library, use the following fallbacks:
- Full-Bleed Image slides → Replace with a bold CSS gradient using the brand palette + large typographic treatment (stat, quote, or section heading). Reference: `examples/css_patterns/gradients.html` contains tested gradient patterns across all 4 palettes
- Content + Image slides → Replace with a split-layout slide using a CSS-illustrated panel (gradient, geometric shapes, or large icon) on the right side. Reference: `examples/css_patterns/layout_grids.html` contains grid patterns for split layouts
- Data visualization slides → Use pure CSS charts (horizontal bars via width percentages, donut charts via conic-gradient, sparklines via inline SVG). Reference: `examples/css_patterns/data_viz_css.html` contains copy-ready chart patterns
- Statistics/Big Number slides → Use large typographic treatments with trend indicators and comparison context. Reference: `examples/css_patterns/typography_treatments.html` contains number display patterns
- Add `<!-- IMAGE_PLACEHOLDER: [description] -->` HTML comments at each point where a real image would improve the slide, so a human can substitute images post-generation
- NEVER leave `[IMAGE: ...]` text visible in the output — always provide a designed fallback
```

---

## 3. Add Data Science Content Patterns to Agent 1

**Section to modify**: `Agent 1: Research & Content Strategist` > `Process` (lines 15-28)

**Why**: Agent 1's research guidance is domain-agnostic. Data science presentations have specific content patterns (metrics, frameworks, evaluation criteria) that the agent should look for when the topic falls in this domain. Adding this guidance helps Agent 1 produce more structured outlines for technical and DS-oriented presentations.

**Current text (lines 15-16)**:
```markdown
**Process**:
1. Research the topic thoroughly — gather facts, statistics, case studies, quotes, and supporting evidence
```

**Replace with**:
```markdown
**Process**:
1. Research the topic thoroughly — gather facts, statistics, case studies, quotes, and supporting evidence. For data science and ML topics, specifically look for:
   - **Model metrics**: accuracy, precision, recall, F1, AUC-ROC, RMSE, MAE — and which metrics matter most for the business context
   - **Before/after comparisons**: baseline vs. improved performance, manual vs. automated process metrics
   - **Pipeline stages**: data collection → preprocessing → feature engineering → training → evaluation → deployment → monitoring
   - **Business impact framing**: translate technical metrics into business outcomes (e.g., "2% accuracy improvement = $1.4M annual savings")
   - **Common DS frameworks**: CRISP-DM, MLOps maturity model, data mesh, feature store architecture — reference these when they fit the narrative
```

---

## 4. Reference Showcases as Quality Benchmarks

**Section to modify**: `Quality Checklist` (lines 311-350)

**Why**: The quality checklist is currently abstract ("consistent color palette," "opening hook is compelling"). Pointing to concrete showcase presentations gives agents a visible benchmark to compare against. This makes the checklist actionable rather than aspirational.

**Current text (lines 311-313)**:
```markdown
## Quality Checklist

Before delivering, verify:
```

**Replace with**:
```markdown
## Quality Checklist

**Quality benchmarks**: Compare your output against the showcase presentations in `examples/showcases/` — these demonstrate the target quality level for executive, technical, and board presentations. Each showcase passes every check below.

Before delivering, verify:
```

**Also add to the Design Quality section, after line 334**:

```markdown
- [ ] Slide types from `examples/templates/` are used correctly — each slide maps to an appropriate type from the 18-type library
```

---

## 5. Add Component Library Reference to Agent 4

**Section to modify**: `Agent 4: Production Engineer` > `Output Format 1: HTML (reveal.js)` (lines 152-162)

**Why**: Agent 4 currently generates all CSS from scratch for every presentation. Pointing to the component library gives the agent tested, reusable micro-components (cards, badges, progress bars, stat blocks) that reduce generation errors and produce more consistent output.

**Current text (lines 152-162)**:
```markdown
#### Output Format 1: HTML (reveal.js)

Generate a complete, self-contained HTML file using reveal.js that:
- Is a single HTML file with embedded CSS and all content
- Uses reveal.js CDN (https://cdn.jsdelivr.net/npm/reveal.js@5/) for framework
- Includes speaker notes view (press `S` to open)
- Has print-to-PDF support (append `?print-pdf` to URL)
- Implements the full design system (colors, typography, layout)
- Is responsive and works on any screen
- Includes all custom CSS for the slide types above
- Can be opened directly in any browser — zero dependencies
```

**Replace with**:
```markdown
#### Output Format 1: HTML (reveal.js)

Generate a complete, self-contained HTML file using reveal.js that:
- Is a single HTML file with embedded CSS and all content
- Uses reveal.js CDN (https://cdn.jsdelivr.net/npm/reveal.js@5/) for framework
- Includes speaker notes view (press `S` to open)
- Has print-to-PDF support (append `?print-pdf` to URL)
- Implements the full design system (colors, typography, layout)
- Is responsive and works on any screen
- Includes all custom CSS for the slide types above
- Can be opened directly in any browser — zero dependencies

**Reference implementations**: Use `examples/templates/` for tested HTML/CSS patterns for each of the 18 slide types. Use `examples/design_system/component_library.html` for reusable micro-components (cards, KPI blocks, badges, progress indicators, annotation callouts). Use `examples/design_system/color_palettes.html` and `examples/design_system/typography_scale.html` for the complete design token reference. Copy CSS patterns directly from these files rather than writing from scratch — the patterns have been tested for cross-browser rendering and WCAG AA compliance.
```

---

## Summary of Changes

| # | Change | Lines Affected | Impact |
|---|--------|---------------|--------|
| 1 | Add 6 slide types (13-18) to Agent 2 + update Agent 4 class list | 71, 84, 202-214 | Expands slide vocabulary from 12 to 18 types |
| 2 | Enhance image fallback section with CSS pattern references | 90-94 | Improves visual quality of LLM-generated fallbacks |
| 3 | Add DS content patterns to Agent 1 research | 15-16 | Better outlines for data science presentations |
| 4 | Reference showcases as quality benchmarks | 311-313, 334 | Makes quality checklist concrete and measurable |
| 5 | Add component library reference to Agent 4 | 152-162 | Reduces CSS errors via tested, reusable patterns |

All changes are additive — no existing functionality is removed. The prompt grows by approximately 60 lines, with the bulk being the 6 new slide type definitions.
