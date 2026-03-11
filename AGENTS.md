# AGENTS.md — Presentation Creator Template

## Project Purpose

A template for creating professional presentations from a brief.
Primary outputs: speaker transcript, reveal.js HTML/PDF, PowerPoint (pptxgenjs).
Primary artifact: `.claude_prompts/presentation-creator-prompt.md` — a 4-agent pipeline.

## Repository Structure

```
.claude_prompts/          # Main prompts including the 4-agent presentation pipeline
.claude/                  # Behavioral directives, agents, commands, skills
.claude_plans/            # Planning and research documents
.claude_research/         # Background research
.github/agents/           # GitHub Copilot agent definitions
.github/prompts/          # GitHub Copilot prompt definitions
.github/skills/           # GitHub Copilot skill definitions
review/                   # Evaluation outputs (audit, test files, verdict)
examples/                 # Slide template library, CSS patterns, design system
docs/                     # API reference
presentations/<topic>/    # Generated presentations (one directory per topic)
```

## The 4-Agent Pipeline

| Agent | Role | Output |
|---|---|---|
| Agent 1: Research & Content Strategist | SCR narrative arc, Minto Pyramid, audience analysis | Content outline |
| Agent 2: Slide Architect & Designer | 18 slide types, design system, CSS tokens | Slide design spec |
| Agent 3: Script Writer | Speaker notes, 130 wpm timing, transitions | Complete script |
| Agent 4: Production Engineer | reveal.js HTML, PDF instructions, pptxgenjs PPTX | Final deliverables |

## pptxgenjs Non-Negotiable Rules

These rules prevent silent failures. Violating any one produces a script that crashes or generates wrong output with no error message.

1. **File extension**: `.cjs` not `.js` — repo has `"type":"module"` in package.json.
2. **Hex colors**: Never prefix with `#` — write `"2563EB"` not `"#2563EB"`.
3. **No shadow**: No `shadow` property on any shape or text object.
4. **No bullet:true**: Use `"• "` prefix in text strings instead.
5. **Fresh option objects**: Create a new `{}` literal for every `addShape`/`addText` call.
6. **Shape type**: `pres.ShapeType.rect` — never string `"rect"` or `pres.shapes.RECTANGLE`.
7. **Layout**: `pres.layout = "LAYOUT_16x9"` — gives 10"x5.625" canvas.
8. **Bottom bar safe zone**: `y=5.1, h=0.52` — content below y=5.0 clips.
9. **Max 4 cards per row**: 5-6 cards produces illegible text.
10. **Min 30 words per card body**: Label+one-liner cards look empty.
11. **Courier New for code**: Monospace font for terminal/code blocks.

## Reveal.js Rules

- **CDN only**: `https://cdn.jsdelivr.net/npm/reveal.js@5/dist/reveal.esm.js`
- **RevealNotes plugin**: Import `notes.esm.js`, include `plugins: [RevealNotes]` in `Reveal.initialize()`
- **Speaker notes**: `<aside class="notes">full script here</aside>` inside each `<section>`
- **Print-to-PDF**: Append `?print-pdf` to the URL, print in Chrome with background graphics on
- **Self-contained**: CDN links only, no local file dependencies
- **Images**: Use `<!-- IMAGE_PLACEHOLDER: description -->` comment + CSS gradient fallback

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
- Speaker notes timing: word count / 130 = target duration +/-15%

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
- No stub slides — never produce a slide with only a title and empty body
- Never write "See speaker notes for full content" as slide body text

## File Organization

- Plans -> `.claude_plans/`
- Research -> `.claude_research/`
- Evaluations -> `review/`
- Prompts -> `.claude_prompts/`
- Generated presentations -> `presentations/<topic>/`
- New presentation scripts: always `.cjs` extension

## Design System Colors

```javascript
const C = {
  navy:"1B2A4A", deepNavy:"0F1B2D", blue:"2563EB", midBlue:"3B82F6",
  lightBlue:"DBEAFE", teal:"0D9488", cyan:"0891B2", green:"059669",
  purple:"7C3AED", orange:"D97706", red:"DC2626", white:"FFFFFF",
  offWhite:"F0F4F8", cream:"F8FAFC", textDark:"1E293B", textMed:"475569",
  textLight:"CBD5E1", divider:"E2E8F0",
};
```

## Modular Architecture

For decks > 20 slides, split into section modules:

```javascript
// Section module: slides_s1_s5.cjs
module.exports = function buildS1toS5(pres, C, h) {
  { const s = pres.addSlide(); /* slide 1 */ }
  { const s = pres.addSlide(); /* slide 2 */ }
};

// Master script: generate_pptx.cjs
const buildS1 = require(path.join(__dirname, "slides_s1_s5.cjs"));
buildS1(pres, C, h);
```

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
