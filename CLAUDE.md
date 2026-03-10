# CLAUDE.md — Presentation Creator Template

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

## The 4-Agent Pipeline

| Agent | Role | Output |
|---|---|---|
| Agent 1: Research & Content Strategist | SCR narrative arc, Minto Pyramid, audience analysis | Content outline |
| Agent 2: Slide Architect & Designer | 18 slide types, design system, CSS tokens | Slide design spec |
| Agent 3: Script Writer | Speaker notes, 130 wpm timing, transitions | Complete script |
| Agent 4: Production Engineer | reveal.js HTML, PDF instructions, pptxgenjs PPTX | Final deliverables |

## Invocation

```yaml
topic: "Why Teams Should Adopt AI Coding Assistants"
audience: "Engineering leadership (CTOs, VPs of Engineering)"
purpose: "Get buy-in to roll out AI coding tools company-wide"
duration: "10 minutes"
tone: "Professional but direct"
output_formats: ["html", "pptx"]
brand_colors: ["#0f172a", "#3b82f6", "#f8fafc"]
```

## CRITICAL: pptxgenjs Technical Rules

These rules prevent silent failures. Violating any one of them produces a script that either
crashes or generates wrong output with no error message.

### Non-negotiable rules (silent failures if violated)

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
- **Layout**: `pres.layout = "LAYOUT_16x9"` — gives 10"×5.625" canvas. Never `LAYOUT_WIDE`
  (gives 13.33"×7.5" — wrong coordinate system).
- **Bottom bar safe zone**: `y=5.1, h=0.52` — content below y=5.0 clips on some renderers.
- **Max 4 cards per row**: 5–6 cards always produces illegible 6pt text — use max 4.
- **Min 30 words per card body**: Never label+one-liner cards — they look empty.
- **Courier New for code**: monospace font for terminal/code blocks.

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

### Design system

Color constants (no `#` prefix):

```javascript
const C = {
  navy:"1B2A4A", deepNavy:"0F1B2D", blue:"2563EB", midBlue:"3B82F6",
  lightBlue:"DBEAFE", teal:"0D9488", cyan:"0891B2", green:"059669",
  purple:"7C3AED", orange:"D97706", red:"DC2626", white:"FFFFFF",
  offWhite:"F0F4F8", cream:"F8FAFC", textDark:"1E293B", textMed:"475569",
  textLight:"CBD5E1", divider:"E2E8F0",
};
```

Helper functions (always passed as `h` parameter to section modules):

```javascript
function sectionHeader(s, tag, title, tagColor) { /* top accent bar, tag pills, title */ }
function bottomBar(s, text, y) { /* y defaults to 5.1; deep navy bg, centered text */ }
function addCard(s, x, y, w, h_val, fillColor) { /* simple rect; fillColor defaults to "FFFFFF" */ }
```

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

## Evaluation Pass Thresholds

From `review/final_verdict.md` (current fulfillment score: 74/100):

- Slide count within ±2 of duration target (1 slide per 1.5–2 min)
- 100% of slides have speaker notes in `<aside class="notes">` tags
- 0 slides with >50 words of visible body text
- HTML opens in Chrome without console errors; `S` key opens speaker notes
- Narrative arc traceable: hook → 3 MECE pillars → specific CTA
- Timing estimate within ±15% of target (measured at 130 words/minute)

## Workflow Rules

- Plans → `.claude_plans/`
- Research → `.claude_research/`
- Evaluations → `review/`
- Prompts → `.claude_prompts/`
- Generated presentations → `presentations/<topic>/`
- New presentation scripts: always `.cjs` extension
