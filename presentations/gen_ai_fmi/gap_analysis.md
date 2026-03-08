# Gap Analysis — generate_pptx.js vs Reference Design Standard

## Agent 1 Output

---

## Summary

The current script (`generate_pptx.js`) is a functional first-generation prototype. It generates a PPTX using pptxgenjs correctly but deviates significantly from the authoritative reference design standard on layout, typography, color palette, component library, content depth, and technical anti-patterns.

**Critical finding**: Slides 20–32 and 33–60 are placeholder stubs — they contain only a headline and "See speaker notes for full content." This means approximately 40 of the ~60 slides are empty shells.

---

## Design System Gaps

### Color Palette

| Status | Issue |
|--------|-------|
| ❌ | Different color palette — uses `primary: "0A1628"`, `secondary: "1E3A5F"`, `accent: "00A3E0"` vs reference `navy: "1B2A4A"`, `blue: "2563EB"`, `teal: "0D9488"` etc. |
| ❌ | No section-specific accent colors (S1 teal, S2 cyan, S3 blue, etc.) — single cyan accent used throughout |
| ❌ | No `offWhite: "F0F4F8"` (uses `surface: "F0F4F8"` — same value, different naming convention) |
| ❌ | Missing: `deepNavy: "0F1B2D"`, `midBlue: "3B82F6"`, `lightBlue: "DBEAFE"`, `cream: "F8FAFC"`, `divider: "E2E8F0"` |
| ❌ | Missing: `textDark: "1E293B"`, `textMed: "475569"`, `textLight: "CBD5E1"` |
| ⚠️ | `green: "22C55E"` vs reference `green: "059669"` — different shade |
| ⚠️ | `red: "EF4444"` vs reference `red: "DC2626"` — different shade |

### Typography

| Status | Issue |
|--------|-------|
| ❌ | Header font is `Calibri` — reference requires `Trebuchet MS` |
| ❌ | Body font size 16–18pt — reference requires 9–11pt (script uses 13.33×7.5" layout not 10×5.625") |
| ❌ | Wrong slide layout — `pptx.layout = "LAYOUT_WIDE"` gives 13.33×7.5"; reference requires 10×5.625" (16:9 standard) |
| ⚠️ | Mono font `Courier New` — correct |

### Slide Dimensions

| Status | Issue |
|--------|-------|
| ❌ | **CRITICAL**: Uses `LAYOUT_WIDE` (13.33 × 7.5") — reference specifies 10 × 5.625". All coordinates and sizes are therefore mismatched. |

---

## Component Library Gaps

| Component | Status | Notes |
|-----------|--------|-------|
| `sectionHeader(s, tag, title, tagColor)` | ❌ Missing | Reference has dual-tag pill system + 30pt title below |
| `bottomBar(s, text)` | ❌ Missing | Reference requires dark navy bar at y=5.1, h=0.52 |
| `addCard(s, x, y, w, h, fillColor)` | ❌ Missing | Simple rect helper |
| Section Divider | ⚠️ Partial | Present but uses different layout (background numeral, vertical accent bar) vs reference (top accent strip, large colored number at y=1.2, subtitle pattern) |
| Statement Slide | ❌ Missing | deepNavy background, bold statement, horizontal rule, supporting text pattern |
| "See It In Action" Layout | ❌ Missing | Not implemented for any tool |

---

## Anti-Pattern Violations (with line numbers)

| Line | Violation | Rule |
|------|-----------|------|
| 247 | `shadow: { type: "outer", blur: 4, ... }` on shape | ❌ NEVER use shadows on shapes |
| 334 | `shadow: { type: "outer", ... }` on shape | ❌ NEVER use shadows on shapes |
| 166 | `s.addShape("rect", {...})` — string not `pres.ShapeType.rect` | ❌ NEVER use string "rect" — use `pres.ShapeType.rect` |
| 334 | `s.addShape("rect", {...})` — string not `pres.ShapeType.rect` | ❌ NEVER use string "rect" |
| 351 | `s.addShape("rect", {...})` | ❌ NEVER use string "rect" |
| 369 | `s.addShape("ellipse", {...})` | ❌ string shape type |
| 398 | `s.addShape("rect", {...})` | ❌ string shape type |
| 431–432 | `s.addShape("rect", {...})` | ❌ string shape type |
| 508–509 | `s.addShape("rect", {...})` | ❌ string shape type |
| 550–554 | `s.addShape("ellipse", {...})` | ❌ string shape type |
| 558–559 | `s.addShape("rect", {...})` | ❌ string shape type |
| 144–155 | `demoBadge()` uses `rounding: true` — not a valid pptxgenjs option | Potential runtime error |
| 144–145 | `slide._pptx ? slide._pptx.ShapeType.rect : "rect"` — fragile internal API access | Should use passed `pres` reference |
| ~600–611 | Slides 20–32 are stubs: `s.addText("See speaker notes for full content.", ...)` | ❌ No placeholder slides allowed |
| ~615–658 | Slides 33–60 are stubs with no visual content | ❌ No placeholder slides allowed |
| 39 | `pptx.layout = "LAYOUT_WIDE"` — wrong layout | Should be `pres.defineCustomSlideSize` or remove layout for 10×5.625 |

---

## Missing "See It In Action" Slides

| Tool | Status |
|------|--------|
| Microsoft Copilot (meeting summary) | ❌ Has demo slide but NOT the "See It In Action" layout from reference |
| GitHub Copilot (Dataiku recipe debug) | ❌ Has demo slide but NOT the "See It In Action" layout |
| Cursor (Plotly Dash app) | ❌ Missing entirely |
| Claude Code (pipeline audit) | ❌ Missing entirely |
| Agentic AI / MCP (morning pipeline check) | ❌ Missing entirely |

---

## Missing Required Components

| Component | Status |
|-----------|--------|
| 10 Section Dividers (S1–S10) | ⚠️ Only 5 implemented (01–05 partially, via stubs) |
| 3 Philosophical Statement Slides | ❌ Missing (rolled into a single stub slide) |
| Closing CTA slide (3 concrete actions) | ❌ Missing — only a generic "Closing + Resources" stub |
| Bottom bar on every content slide | ❌ Missing entirely from architecture |
| Section-specific accent colors | ❌ All slides use same cyan accent |
| FM&I-specific prompts in terminal panels | ❌ Missing (no terminal panels exist) |
| Big number time savings | ⚠️ Some numbers present but not in reference format |

---

## Content Quality Issues

| Issue | Priority |
|-------|----------|
| Slides 20–32: stubs only — no visual content | P0 |
| Slides 33–60: stubs only — no visual content | P0 |
| Wrong slide dimensions affect all coordinate math | P0 |
| Shadow anti-pattern on 2+ slides | P0 |
| Missing "See It In Action" for all 5 major tools | P1 |
| No bottom bar on any slide | P1 |
| Header font Calibri instead of Trebuchet MS | P1 |
| Section dividers don't follow reference pattern | P1 |
| No statement slides | P1 |
| No closing CTA with 3 concrete actions | P1 |
| No section-specific colors | P2 |
| String shape types instead of pres.ShapeType.rect | P0 (runtime risk) |

---

## Prioritised Fix List

### P0 — Technical / Breaking

1. Fix slide layout to 10×5.625" (remove `LAYOUT_WIDE`)
2. Replace all `"rect"` string shapes with `pres.ShapeType.rect`
3. Remove all `shadow:` properties from shapes
4. Implement all ~40 stub slides with full visual content
5. Save as `.cjs` extension (repo has `"type": "module"`)

### P1 — Missing Components

6. Implement reference `sectionHeader()` component
7. Implement reference `bottomBar()` component with FM&I "so what?" text
8. Add "See It In Action" slides for: Copilot, GitHub Copilot, Cursor, Claude Code, Agentic/MCP
9. Add 3 philosophical statement slides (deepNavy background, bold text)
10. Add proper closing CTA slide with 3 concrete actions
11. Switch header font to Trebuchet MS
12. Implement 10 section dividers following reference pattern

### P2 — Content Quality

13. Apply section-specific accent colors (10 colors)
14. Add FM&I-specific prompts in Courier New terminal panels
15. Format big numbers at 28-36pt Trebuchet MS in reference layout
16. Ensure every bottom bar is FM&I-specific and ≤120 chars
17. Ensure every title ≤40 chars

---

## Slide Count

Current script generates approximately 35 slides total (5 fully implemented + 13 tool slide stubs + ~17 remaining section stubs). Target is 50–70 slides.
