---
paths:
  - "presentations/**"
  - "**/*.cjs"
---

# pptxgenjs Technical Rules

These rules prevent silent failures. Violating any one produces a script that either
crashes or generates wrong output with no error message.

## Non-negotiable rules

- **File extension**: `.cjs` not `.js` — repo has `"type":"module"` in package.json.
- **Hex colors**: Never prefix with `#` — write `"2563EB"` not `"#2563EB"`.
- **No shadow**: No `shadow` property on any shape or text object.
- **No bullet:true**: Use `"• "` prefix in text strings instead.
- **Fresh option objects**: New `{}` literal for every `addShape`/`addText` call.
- **Shape type**: `pres.ShapeType.rect` — never string `"rect"` or `pres.shapes.RECTANGLE`.
- **Layout**: `pres.layout = "LAYOUT_16x9"` (10"×5.625"). Never `LAYOUT_WIDE`.
- **Bottom bar safe zone**: `y=5.1, h=0.52`.
- **Max 4 cards per row**: 5–6 produces illegible text.
- **Min 30 words per card body**: Label+one-liner looks empty.
- **Courier New for code**: monospace font for terminal/code blocks.

## Modular architecture (required for decks > ~20 slides)

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

## Design system

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
