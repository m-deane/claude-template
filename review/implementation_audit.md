# Implementation Audit — Presentation Creator Agent Team

**Auditor**: Agent 2 (Implementation Auditor)
**Date**: 2026-03-08
**Source**: `.claude_prompts/presentation-creator-prompt.md`
**Reference frameworks**: Minto Pyramid Principle, Garr Reynolds (Presentation Zen), Nancy Duarte (Resonate), Edward Tufte (Visual Display of Quantitative Information), reveal.js v5 documentation

---

## 1. Cross-Reference Against Authoritative Frameworks

### 1.1 Barbara Minto Pyramid Principle

**What the prompt says**: Agent 1 uses "Situation → Complication → Resolution" narrative arc and "Rule of Three" for major sections.

**Assessment**:
- The SCR arc is correctly named and placed at the right stage (content strategy, not design or production). **PASS.**
- The Rule of Three is applied correctly as an organising principle for major sections. **PASS.**
- However, the Pyramid Principle's deeper mechanism — **MECE grouping** (Mutually Exclusive, Collectively Exhaustive) — is not specified. Agent 1 is told to create 3 pillars but not given criteria for how to verify they are truly non-overlapping and comprehensive. This is a meaningful omission — it is the most common failure mode when applying Minto.
- The per-section structure (assertion → evidence → transition) is an accurate simplification of Minto's hierarchical message architecture. **PASS with minor gap.**
- The prompt does not specify that the pyramid structure should flow **top-down in delivery** (start with the governing thought, then support), which is Minto's most actionable instruction for presentations. A bottom-up structure (evidence first, conclusion last) is a common mistake that the prompt could prevent but does not.

**Gap identified**: No MECE guidance; no explicit instruction to lead with the conclusion (governing thought) rather than build to it.

---

### 1.2 Garr Reynolds / Nancy Duarte Principles

**What the prompt says**: Assertion-Evidence model, Signal-to-Noise, Picture Superiority Effect, 10/20/30 Rule attribution (Guy Kawasaki), progressive disclosure, no bullet points beyond 3 items.

**Assessment**:
- Assertion-Evidence model (slide titles as full-sentence assertions, body as visual evidence) is correctly specified and is the single most impactful Duarte/Reynolds principle. **PASS.**
- "No bullet points" instruction is partially contradicted. The prompt says "No bullet points exceeding 3 items per slide (prefer visuals)" — this permits bullet lists up to 3 items, which is counter to Reynolds' "no bullets at all" ideal. The prompt creates a middle-ground rule that will produce bullet-heavy outputs in practice because the agent defaults to text when visual specification is ambiguous.
- The 10/20/30 Rule is cited but immediately qualified ("adapt as needed but respect the spirit"). This is pragmatically correct — the rule is a heuristic not a law — but the guidance to adapt without specifics leaves Agent 2 without a clear fallback.
- Nancy Duarte's "Sparkline" structure (moving between what-is and what-could-be) is not mentioned. This is particularly relevant for persuasion/sales use cases.
- The "Picture Superiority Effect" claim (60,000x faster) is a widely-cited but methodologically disputed figure. Citing it as fact is a minor credibility risk if a technically literate audience reads the prompt. This does not affect output quality but matters if the prompt is shared externally.

**Gap identified**: Bullet list rule creates a permissive floor that encourages bullet-heavy outputs. Duarte Sparkline not addressed.

---

### 1.3 Edward Tufte Principles

**What the prompt says**: Signal-to-Noise Ratio, remove chartjunk, data visualization guidelines (sequential/categorical palettes, colorblind-safe, direct labels over legends).

**Assessment**:
- Signal-to-Noise is the correct Tufte framing and is applied correctly to slide design. **PASS.**
- The chart guidance (one chart per slide, annotate the key insight, avoid rainbow charts) correctly operationalises Tufte. **PASS.**
- Tufte's specific objections to PowerPoint as a medium (cognitive style differences, low data density relative to print) are not acknowledged. For a presentation creator, acknowledging this tension would sharpen the guidance.
- The prohibition on "complex tables" (convert to charts or highlight key numbers) is correct Tufte practice. **PASS.**
- Tufte's "sparklines" (inline small charts) are not covered — a gap for data-heavy technical presentations.

**Gap identified**: No guidance for data-dense slides where a single chart is insufficient; no sparkline pattern specified.

---

### 1.4 reveal.js v5 Technical Accuracy

**What the prompt says**: CDN URL `https://cdn.jsdelivr.net/npm/reveal.js@5/`, speaker notes via `S` key, `?print-pdf` for PDF, `<aside class="notes">` for speaker notes, config options `hash`, `slideNumber`, `showNotes`, `pdfMaxPagesPerSlide`, `pdfSeparateFragments`.

**Assessment**:
- CDN path `https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.css` is correct. **PASS.**
- `<aside class="notes">` is the correct reveal.js speaker notes mechanism. **PASS.**
- `Reveal.initialize({ hash: true, slideNumber: true, showNotes: false, pdfMaxPagesPerSlide: 1, pdfSeparateFragments: false })` — all valid v5 config keys. **PASS.**
- **Critical gap**: The `?print-pdf` mode in reveal.js v5 requires the Notes plugin to be loaded if speaker notes should print. The template does not include the Notes plugin:
  ```javascript
  plugins: [ RevealNotes ]
  ```
  Without this, pressing `S` for speaker notes does NOT work. The speaker notes feature is broken in the provided template.
- **Critical gap**: The template links `theme/white.css` but if the custom CSS overrides the theme substantially, leaving the base theme link is redundant and may cause specificity conflicts. Guidance on when to drop the base theme is absent.
- The HTML template uses `<link rel="stylesheet" href="...reveal.css">` and `<link rel="stylesheet" href="...theme/white.css">` — both are correct paths for CDN v5. **PASS.**
- `pdfMaxPagesPerSlide` and `pdfSeparateFragments` are valid but the more critical `pdf-page-height-offset` is not mentioned (needed when slides have unusual aspect ratios).
- The template does not load the `RevealHighlight` or `RevealMarkdown` plugins — acceptable for this use case since the content is HTML-generated, not Markdown.

**Gap identified (CRITICAL)**: Missing `plugins: [ RevealNotes ]` in `Reveal.initialize()` — speaker notes via `S` key will not function without this.

---

## 2. Implementation Gaps

### Gap 1: Missing RevealNotes Plugin (CRITICAL)
**Location**: Agent 4, Output Format 1 (HTML template)
**Problem**: `Reveal.initialize()` does not include the Notes plugin. Speaker notes via `S` key is broken.
**Impact**: Fails the "Speaker notes accessible via `S` key" technical quality checklist item. Every generated presentation fails this criterion.

### Gap 2: No Agent Handoff Failure Protocol
**Location**: Workflow section, Execution Sequence
**Problem**: The workflow lists a clean sequential pipeline with no error handling. What happens if Agent 1's research is thin (e.g., the topic is highly specialised, niche, or recent)? What if Agent 1 produces 2 pillars instead of 3? What if Agent 2 cannot find an appropriate image for a required full-bleed slide?
**Impact**: In practice, the pipeline will silently degrade — Agent 2 will proceed with insufficient content and Agent 4 will produce a structurally incomplete output with no flag to the user.

### Gap 3: Vague Visual Content Specification
**Location**: Agent 2, Image & Visual Guidelines
**Problem**: "Use high-quality images only (minimum 1920x1080 for full-bleed)" — but the agent is an LLM, not an image retrieval system. It cannot fetch images. The prompt never addresses this fundamental constraint. The result is either: (a) placeholder text like `[IMAGE: team working together]` that breaks the output, or (b) the agent generates inline SVG/CSS art as a workaround, which is inconsistent.
**Impact**: The "Full-Bleed Image" and "Content + Image" slide types (2 of 12) are effectively unsupported in a pure LLM execution context. The quality checklist item "Images are high-quality and relevant" is structurally unachievable.

### Gap 4: Bullet List Contradiction
**Location**: Agent 2 design principles vs Agent 3 Script Structure
**Problem**: Agent 2 says "Assertion-Evidence Model: body is visual evidence — not bullet points." But the Script Structure template shows:
```
KEY POINTS TO HIT:
- {Point 1}
- {Point 2}
```
This bullet structure in the script creates a gravitational pull toward bullet-based slides in the HTML output, because Agent 4 will naturally mirror the script structure when generating slides.
**Impact**: Produces bullet-heavy slides that contradict the design philosophy.

### Gap 5: PowerPoint Spec is Incomplete for Autonomous Execution
**Location**: Agent 4, Output Format 3 (PPTX)
**Problem**: The PptxGenJS specification shows a single slide's JSON structure but does not specify: (a) the complete list of all 12 slide types in PptxGenJS syntax, (b) how image placement works without actual image files, (c) the complete Node.js script structure. An agent given this spec would produce valid JSON fragments but could not generate a runnable script without significant inference.
**Impact**: PPTX output is not autonomously executable from the prompt alone. It requires the agent to infer PptxGenJS API from the partial spec — introducing inconsistency.

### Gap 6: Duration-to-Slide Mapping Inconsistency
**Location**: Agent 3 Timing Guide vs Agent 2 design philosophy
**Problem**: Agent 3's timing guide:
- 10-minute = 8-12 slides
- 20-minute = 15-20 slides
This implies ~1-1.5 min per slide on average. But Agent 3 also says "~2 minutes per content slide. 30 seconds for dividers." For a 10-minute presentation with 10 slides — if 3 are section dividers (30 sec each) and 7 are content slides (2 min each), total = 1.5 + 14 = 15.5 minutes. The timing arithmetic does not add up at the boundaries specified.
**Impact**: Presentations will systematically run over time if the timing guidance is followed strictly.

### Gap 7: No Specification for Multi-Speaker or Panel Scenarios
**Location**: Entire prompt
**Problem**: The prompt assumes a single presenter throughout. There is no guidance for: (a) panels with multiple speakers, (b) interactive Q&A slides, (c) modular presentations (e.g., each team member presents one pillar).
**Impact**: Use cases that naturally involve multiple presenters (board updates, team reviews, conference panels) will produce speaker notes formatted for one voice and be awkward to split.

### Gap 8: No Data-Heavy Content Pattern
**Location**: Agent 2 slide types
**Problem**: The 12 slide types do not include a "Dashboard" or "Multi-metric" slide for presentations where the audience expects a data-rich overview (e.g., quarterly business reviews, engineering metrics reviews). The closest is "Data/Chart Slide" (one chart only) — but many engineering and business contexts require 2-4 KPIs on a single slide.
**Impact**: Technical and business review presentations will be awkward — either splitting naturally cohesive data across multiple slides or violating the one-chart rule.

### Gap 9: No Fallback for Missing Brand Colors
**Location**: Input schema, Design System Reference
**Problem**: When `brand_colors` is empty (`[]`), the prompt provides 4 named palettes to choose from (Corporate, Creative, Technical, Sales) but does not specify: (a) which palette maps to which `tone` value, or (b) how to choose between them systematically.
**Impact**: The agent must guess, producing inconsistent palette selection across runs for the same input.

### Gap 10: No Content Quality Gate Between Agents
**Location**: Workflow section
**Problem**: The workflow defines 4 phases but has no checkpoint mechanism. A real professional workflow would review Agent 1's outline before spending time on design. Without a review gate, errors in the research phase (wrong audience reading, incorrect core message) propagate through all subsequent agents and into the final output.
**Impact**: Structural content errors cannot be caught before production.

---

## 3. Over-Specifications and Anti-Patterns

### Over-Specification 1: "No more than 6 words in any slide title"
The prompt simultaneously says: (a) titles should be ≤6 words, and (b) assertion titles are full sentences (exception). In practice, an assertion-evidence title like "AI Coding Tools Reduce Developer Context-Switching by 40%, Freeing Creative Capacity" is correct per the Assertion-Evidence model but clearly violates the 6-word rule. The exception clause is necessary but underspecified — it creates a loophole that agents will handle inconsistently.

### Over-Specification 2: "Minimum 5% padding on all sides" + "60px slide-padding"
These two specifications may conflict depending on screen resolution and slide dimensions. 5% of a 1920px wide slide is 96px, not 60px. An agent implementing both literally will get confused.

### Over-Specification 3: "Minimum 30-40% whitespace per slide"
Measuring whitespace percentage in an HTML/CSS slide is practically unmeasurable without visual analysis. Agents will interpret this qualitatively, not quantitatively, making this checklist item unverifiable.

### Anti-Pattern 1: Contradictory Bullet Rules (documented above in Gap 4)

### Anti-Pattern 2: Guy Kawasaki's 10/20/30 Rule
The Rule is cited as a guideline then immediately qualified. The 30pt minimum font rule from Kawasaki is absorbed into the prompt's own "never below 18pt" rule — creating a conflict (18pt < 30pt). The prompt's 18pt minimum is correct for general use; the 30pt Kawasaki rule is for his specific investor pitch context. Citing Kawasaki while using a different standard is confusing.

### Anti-Pattern 3: "No Questions? slide" + "End with CTA"
This is correct practice but the anti-patterns section frames it as "end with CTA or a memorable closing statement. Questions happen naturally." In a 5-minute investor pitch, there is no natural Q&A opportunity — this guidance implies Q&A is optional/informal when in practice the audience may expect a structured Q&A. The guidance is incomplete for formal presentation contexts.

---

## 4. Scores Across 10 Dimensions (1-10 Scale)

| # | Dimension | Score | Rationale |
|---|---|---|---|
| 1 | Clarity of instructions | 7 | Instructions are generally clear and well-written. Key ambiguities exist in visual content (images), palette selection without brand colors, and the bullet contradiction. |
| 2 | Completeness of agent definitions | 6 | Each agent has a role and process. Missing: handoff failure protocols, content review gates, data-heavy content patterns. |
| 3 | Feasibility of outputs (can a real agent execute this?) | 6 | HTML output is feasible. PDF is instruction-only (acceptable). PPTX is underspecified. The image specification is structurally unachievable for LLM execution. Critical Notes plugin bug prevents speaker notes from working. |
| 4 | Design system quality | 8 | The design system is well-grounded in authoritative sources. Color palettes, typography scale, layout rules, and 12 slide types are comprehensive and professional. The quantitative whitespace rule is unverifiable but directionally correct. |
| 5 | Script guidance quality | 7 | Script structure is well-defined. Conversational tone guidance is actionable. Timing arithmetic has edge-case inconsistencies. Multi-speaker scenarios unaddressed. |
| 6 | Technical accuracy (reveal.js, PDF, PPTX specs) | 5 | reveal.js CDN and config keys are correct, but the missing Notes plugin is a critical technical bug that breaks the headline speaker notes feature. PPTX spec is a skeleton, not an executable spec. |
| 7 | Error handling / edge cases | 3 | Essentially no error handling. No handoff failure protocols, no quality gates between phases, no handling of thin research, ambiguous topics, or incompatible constraints (e.g., 5-minute presentation covering 10 topics). |
| 8 | Inter-agent coordination | 5 | The sequential pipeline is defined. Output documents are named (Content Outline, Slide Design Specification, Speaker Script, Final Files). But there is no specification of what each handoff document must contain, no verification that downstream agents have sufficient input. |
| 9 | Scalability (10-min vs 45-min presentations) | 6 | The timing guide covers 5 min to 45 min. The 45-min keynote guidance ("30-50 slides with faster pacing") is underdeveloped — 45-minute keynotes have fundamentally different structure than 10-minute pitches (intermissions, demos, audience participation). |
| 10 | Real-world applicability | 7 | For the core use case (10-15 min professional presentation, HTML output), the system would produce a solid result. The image constraint, Notes plugin bug, and PPTX gaps reduce applicability for production use without workarounds. |

**Average Score: 6.0 / 10**

---

## 5. Summary of Critical vs. Significant vs. Minor Gaps

### Critical (blocks expected functionality)
1. Missing `RevealNotes` plugin — speaker notes via `S` key broken
2. Image specification unachievable in LLM execution context

### Significant (produces mediocre instead of excellent output)
3. No agent handoff failure protocol — errors propagate silently
4. Bullet list contradiction between design principles and script template
5. PPTX spec insufficient for autonomous execution
6. Duration-to-slide timing arithmetic inconsistency
7. No palette mapping when brand_colors is empty

### Minor (edge cases or nice-to-haves)
8. No multi-speaker / panel guidance
9. No data-dense / multi-metric slide type
10. Slide title length rule contradiction (6-word rule vs assertion titles)
11. Competing padding specifications (5% vs 60px)
12. Whitespace percentage unverifiable as a quality criterion
