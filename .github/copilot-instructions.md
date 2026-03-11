# Project Instructions

## Project Purpose

A Claude Code template for creating professional presentations from a brief.
Primary outputs: speaker transcript, reveal.js HTML/PDF, Microsoft PowerPoint (pptxgenjs).
Primary artifact: `.claude_prompts/presentation-creator-prompt.md` — a 4-agent pipeline.

## Repository Structure

```
.claude_prompts/
  presentation-creator-prompt.md  # Main 4-agent presentation system (PRIMARY ARTIFACT)
  claude.md                        # Standard implementation workflow
  iterative-testing-prompt.md      # Iterative browser-based testing workflow
  personal-org-app-prompt.md       # Personal org app build prompt

.claude/
  CLAUDE.md                        # Behavioral directives
  TEMPLATE_GUIDE.md                # How to use this template for new projects
  agents/                          # Specialized sub-agent definitions
  commands/                        # Slash command definitions
  skills/                          # MCP skill definitions
  example_prompt.md                # Prompt template starting point

.claude_plans/                     # Planning and research documents
.claude_research/                  # Background research
review/                            # Evaluation outputs (use case analysis, audit, test HTML files, verdict)
examples/                          # Slide template library, showcases, CSS patterns, design system reference
docs/                              # API reference
presentations/<topic>/             # Generated presentations (one directory per presentation)
```

## Behavioral Directives

### Production Rules

- Direct production output only — complete, working deliverables on first attempt
- No stub slides — never produce a slide with only a title and empty body
- Never write "See speaker notes for full content" as slide body text
- Every slide must have speaker notes (full sentences, not bullet points)
- Every pptxgenjs script must run without errors on first attempt

### Content Standards

- Max 40 words visible on any slide body
- One key assertion per slide — not a list of facts
- Narrative arc must be traceable: hook → 3 MECE pillars → specific CTA
- Speaker notes: 130 words per minute model — verify timing before finalizing
- Demo slides: the big number (time saved, ROI, improvement) must be the visual centerpiece, not a supporting element

## pptxgenjs Technical Rules (Non-Negotiable)

These rules prevent silent failures. Violating any one of them produces a script that either
crashes or generates wrong output with no error message.

### Silent failure rules

- **File extension**: `.cjs` not `.js` — repo has `"type":"module"` in package.json causing ESM
  conflict with `require()`. A `.js` file will throw `require is not defined`.
- **Hex colors**: Never prefix with `#` — write `"2563EB"` not `"#2563EB"`. The `#` causes silent
  wrong color or no render.
- **No shadow**: No `shadow` property on any shape or text object — causes script to fail silently
  on some pptxgenjs versions.
- **No bullet:true**: Use `"• "` prefix in text strings — `bullet: true` renders incorrectly.
- **Fresh option objects**: Create a new object literal for every `addShape`/`addText` call —
  reusing objects causes all shapes to inherit the last call's properties.
- **Shape type**: `pres.ShapeType.rect` — never string `"rect"` or `pres.shapes.RECTANGLE`.
- **Layout**: `pres.layout = "LAYOUT_16x9"` — gives 10"x5.625" canvas. Never `LAYOUT_WIDE`
  (gives 13.33"x7.5" — wrong coordinate system).
- **Bottom bar safe zone**: `y=5.1, h=0.52` — content below y=5.0 clips on some renderers.
- **Max 4 cards per row**: 5-6 cards always produces illegible 6pt text — use max 4.
- **Min 30 words per card body**: Never label+one-liner cards — they look empty.
- **Courier New for code**: monospace font for terminal/code blocks.

### Design system color constants

No `#` prefix on any value:

```javascript
const C = {
  navy:"1B2A4A", deepNavy:"0F1B2D", blue:"2563EB", midBlue:"3B82F6",
  lightBlue:"DBEAFE", teal:"0D9488", cyan:"0891B2", green:"059669",
  purple:"7C3AED", orange:"D97706", red:"DC2626", white:"FFFFFF",
  offWhite:"F0F4F8", cream:"F8FAFC", textDark:"1E293B", textMed:"475569",
  textLight:"CBD5E1", divider:"E2E8F0",
};
```

### Helper functions

Always passed as `h` parameter to section modules:

```javascript
function sectionHeader(s, tag, title, tagColor) { /* top accent bar, tag pills, title */ }
function bottomBar(s, text, y) { /* y defaults to 5.1; deep navy bg, centered text */ }
function addCard(s, x, y, w, h_val, fillColor) { /* simple rect; fillColor defaults to "FFFFFF" */ }
```

### Modular architecture (required for decks > ~20 slides)

Split into section modules to avoid the 32K output token limit:

```javascript
// Section module: slides_s1_s5.cjs
module.exports = function buildS1toS5(pres, C, h) {
  { const s = pres.addSlide(); /* slide 1 */ }
  { const s = pres.addSlide(); /* slide 2 */ }
};

// Master script: generate_pptx.cjs
const PptxGenJS = require("pptxgenjs");
const path = require("path");
const pres = new PptxGenJS();
pres.layout = "LAYOUT_16x9";
const C = { /* color constants */ };
const h = { sectionHeader, bottomBar, addCard };
const buildS1 = require(path.join(__dirname, "slides_s1_s5.cjs"));
buildS1(pres, C, h);
pres.writeFile({ fileName: "output.pptx" })
  .then(() => console.log("Done"))
  .catch(err => { console.error(err); process.exit(1); });
```

Run with: `node generate_pptx.cjs`

See `presentations/gen_ai_fmi/generate_pptx_v5.cjs` for the canonical working implementation.

## Reveal.js Rules

- RevealNotes plugin: import `notes.esm.js` and include `plugins: [RevealNotes]` in `Reveal.initialize()`
- Speaker notes: `<aside class="notes">full script here</aside>` inside each `<section>`
- Print-to-PDF: append `?print-pdf` to the URL, print in Chrome with background graphics on
- Self-contained: CDN links only, no local file dependencies
- Images: use `<!-- IMAGE_PLACEHOLDER: description -->` comment + CSS gradient fallback — never broken img tags

```html
<script type="module">
import Reveal from 'https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.esm.js';
import RevealNotes from 'https://cdn.jsdelivr.net/npm/reveal.js@5/plugin/notes/notes.esm.js';
Reveal.initialize({ hash: true, plugins: [ RevealNotes ] });
</script>
```

## Quality Gates

Before delivering any output:

- pptxgenjs script runs: `node generate_pptx.cjs` exits 0
- HTML opens in Chrome without console errors; `S` key opens speaker notes
- Slide count within +/-2 of duration target (8 slides per 10 min)
- 100% of slides have speaker notes
- Narrative arc reviewable in slide titles alone

## Evaluation Thresholds

- Slide count within +/-2 of duration target (1 slide per 1.5-2 min)
- 100% of slides have speaker notes in `<aside class="notes">` tags
- 0 slides with >50 words of visible body text
- HTML opens in Chrome without console errors; `S` key opens speaker notes
- Narrative arc traceable: hook → 3 MECE pillars → specific CTA
- Timing estimate within +/-15% of target (measured at 130 words/minute)

## Prohibited Patterns

- `console.log` left in production scripts
- Slides with >50 words of body text
- Grids with more than 4 cards
- Cards with fewer than 30 words of body content
- `bullet: true` in any pptxgenjs call
- `shadow` in any pptxgenjs call
- `#` prefix on any hex color value
- Reused option objects across `addShape`/`addText` calls
- Social validation ("Great question!"), hedging language ("might", "could potentially")
- Stub slides with only a title and empty body
- "See speaker notes for full content" as slide body text

## Workflow Rules

- Plans go in `.claude_plans/`
- Research goes in `.claude_research/`
- Evaluations go in `review/`
- Prompts go in `.claude_prompts/`
- Generated presentations go in `presentations/<topic>/`
- New presentation scripts: always use `.cjs` extension
