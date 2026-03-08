/**
 * FM&I Gen AI Upskilling Session — PowerPoint Generator v2
 * =========================================================
 * Usage:  node generate_pptx_v2.cjs
 * Output: gen_ai_fmi_presentation_v2.pptx
 * Prereq: npm install pptxgenjs (already installed)
 */

const PptxGenJS = require("pptxgenjs");

const pres = new PptxGenJS();
pres.layout = "LAYOUT_16x9";

// ─── Design System ────────────────────────────────────────────────────────────

const C = {
  navy:      "1B2A4A",
  deepNavy:  "0F1B2D",
  blue:      "2563EB",
  midBlue:   "3B82F6",
  lightBlue: "DBEAFE",
  teal:      "0D9488",
  cyan:      "0891B2",
  green:     "059669",
  purple:    "7C3AED",
  orange:    "D97706",
  red:       "DC2626",
  white:     "FFFFFF",
  offWhite:  "F0F4F8",
  cream:     "F8FAFC",
  textDark:  "1E293B",
  textMed:   "475569",
  textLight: "CBD5E1",
  divider:   "E2E8F0",
};

// ─── Helper Functions ─────────────────────────────────────────────────────────

function sectionHeader(s, tag, title, tagColor) {
  // Top accent bar
  s.addShape(pres.ShapeType.rect, {x: 0, y: 0, w: 10, h: 0.06, fill: {color: tagColor}});

  // Primary tag pill
  const parts = tag.split("|");
  s.addShape(pres.ShapeType.rect, {x: 0.4, y: 0.25, w: 1.4, h: 0.32, fill: {color: "94A3B8"}});
  s.addText(parts[0], {x: 0.4, y: 0.25, w: 1.4, h: 0.32,
    fontSize: 8.5, fontFace: "Trebuchet MS", color: "FFFFFF", bold: true,
    align: "center", valign: "middle", margin: 0, charSpacing: 1.5});

  // Secondary tag pill (if present)
  if (parts[1]) {
    s.addShape(pres.ShapeType.rect, {x: 1.92, y: 0.25, w: 1.6, h: 0.32, fill: {color: tagColor}});
    s.addText(parts[1], {x: 1.92, y: 0.25, w: 1.6, h: 0.32,
      fontSize: 8.5, fontFace: "Trebuchet MS", color: "FFFFFF", bold: true,
      align: "center", valign: "middle", margin: 0, charSpacing: 1.5});
  }

  // Slide title
  s.addText(title, {x: 0.4, y: 0.65, w: 9.2, h: 0.65,
    fontSize: 30, fontFace: "Trebuchet MS", color: "1E293B", bold: true,
    margin: 0, valign: "middle"});
}

function bottomBar(s, text, y) {
  const barY = (y !== undefined) ? y : 5.1;
  s.addShape(pres.ShapeType.rect, {x: 0, y: barY, w: 10, h: 0.52, fill: {color: "0F1B2D"}});
  s.addText(text, {x: 0.5, y: barY, w: 9, h: 0.52,
    fontSize: 10, fontFace: "Calibri", color: "CBD5E1", bold: true,
    align: "center", valign: "middle", margin: 0});
}

function addCard(s, x, y, w, h_val, fillColor) {
  const fc = fillColor || "FFFFFF";
  s.addShape(pres.ShapeType.rect, {x: x, y: y, w: w, h: h_val, fill: {color: fc}});
}

const h = { sectionHeader, bottomBar, addCard };

// ─── Section Modules ──────────────────────────────────────────────────────────

const buildS1toS3 = require("./slides_s1_s3.cjs");
const buildS4toS6 = require("./slides_s4_s6.cjs");
const buildS7toS10 = require("./slides_s7_s10.cjs");

buildS1toS3(pres, C, h);
buildS4toS6(pres, C, h);
buildS7toS10(pres, C, h);

// ─── Write Output ─────────────────────────────────────────────────────────────

pres.writeFile({fileName: "gen_ai_fmi_presentation_v2.pptx"})
  .then(() => {
    console.log("✅ gen_ai_fmi_presentation_v2.pptx generated successfully.");
  })
  .catch((err) => {
    console.error("❌ Error generating PPTX:", err);
    process.exit(1);
  });
