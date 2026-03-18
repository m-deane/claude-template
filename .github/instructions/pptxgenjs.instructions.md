---
applyTo: "**/*.cjs"
description: "pptxgenjs technical rules for PowerPoint generation scripts"
---

# pptxgenjs Technical Rules

These rules prevent silent failures. Violating any one of them produces a script that either
crashes or generates wrong output with no error message.

## Non-Negotiable Rules

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

## Design System Color Constants

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

## Helper Functions

Always passed as `h` parameter to section modules:

```javascript
function sectionHeader(s, tag, title, tagColor) { /* top accent bar, tag pills, title */ }
function bottomBar(s, text, y) { /* y defaults to 5.1; deep navy bg, centered text */ }
function addCard(s, x, y, w, h_val, fillColor) { /* simple rect; fillColor defaults to "FFFFFF" */ }
```

## Modular Architecture (Required for Decks > ~20 Slides)

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

## Quick Checklist

Before writing or modifying any `.cjs` script, verify:

- [ ] `.cjs` extension (not `.js`)
- [ ] No `#` on hex colors
- [ ] No `shadow` property anywhere
- [ ] No `bullet: true` anywhere
- [ ] Fresh option objects per `addShape`/`addText` call
- [ ] `pres.ShapeType.rect` (not string `"rect"` or `pres.shapes.RECTANGLE`)
- [ ] `pres.layout = "LAYOUT_16x9"`
- [ ] Bottom bar at `y=5.1, h=0.52`
- [ ] Max 4 cards per row
- [ ] Min 30 words per card body
- [ ] Courier New for code/terminal blocks

## Prohibited Patterns

- `console.log` left in production scripts
- `bullet: true` in any pptxgenjs call
- `shadow` in any pptxgenjs call
- `#` prefix on any hex color value
- Reused option objects across `addShape`/`addText` calls
- Grids with more than 4 cards
- Cards with fewer than 30 words of body content

## Reference

See `presentations/gen_ai_fmi/generate_pptx_v5.cjs` for the canonical working implementation.
