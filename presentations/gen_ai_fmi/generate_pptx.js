/**
 * FM&I Gen AI Upskilling Session — PowerPoint Generator
 * ======================================================
 * Agent 5: Production Engineer
 *
 * Usage:
 *   npm install pptxgenjs
 *   node generate_pptx.js
 *
 * Output: gen_ai_fmi_presentation.pptx
 */

const PptxGenJS = require("pptxgenjs");

const pptx = new PptxGenJS();

// ─── Design System ───────────────────────────────────────────────────────────

const C = {
  primary:     "0A1628",   // deep navy — dark slide backgrounds
  secondary:   "1E3A5F",   // mid navy — section dividers
  accent:      "00A3E0",   // cyan — highlights, key data points
  accentWarm:  "F5A623",   // amber — warnings, key stats
  surface:     "F0F4F8",   // off-white — content slide backgrounds
  textPrimary: "0A1628",
  textLight:   "FFFFFF",
  textMuted:   "64748B",
  green:       "22C55E",
  red:         "EF4444",
};

const FONT = {
  heading: "Calibri",
  body:    "Calibri",
  mono:    "Courier New",
};

// Slide dimensions
pptx.layout = "LAYOUT_WIDE"; // 13.33 × 7.5 inches

// ─── Helpers ─────────────────────────────────────────────────────────────────

function titleSlide(prs, title, subtitle, caption) {
  const slide = prs.addSlide();
  slide.background = { color: C.primary };

  // Accent rule
  slide.addShape(prs.ShapeType.rect, {
    x: 2.5, y: 3.15, w: 2, h: 0.05,
    fill: { color: C.accent }, line: { color: C.accent },
  });

  slide.addText(title, {
    x: 0.5, y: 2.2, w: 12.3, h: 0.9,
    fontSize: 40, bold: true, color: C.textLight,
    fontFace: FONT.heading, align: "center",
  });
  slide.addText(subtitle, {
    x: 0.5, y: 3.4, w: 12.3, h: 0.5,
    fontSize: 22, color: C.accent,
    fontFace: FONT.body, align: "center",
  });
  slide.addText(caption, {
    x: 0.5, y: 4.1, w: 12.3, h: 0.4,
    fontSize: 16, color: C.textMuted,
    fontFace: FONT.body, align: "center",
  });
  return slide;
}

function sectionDivider(prs, number, sectionTitle, subtext) {
  const slide = prs.addSlide();
  slide.background = { color: C.secondary };

  // Large background numeral
  slide.addText(number, {
    x: 9.5, y: 3.5, w: 3.8, h: 3.5,
    fontSize: 180, color: C.accent, transparency: 80,
    fontFace: FONT.heading, bold: true, align: "right",
  });

  // Accent bar
  slide.addShape(prs.ShapeType.rect, {
    x: 0.6, y: 2.4, w: 0.08, h: 1.6,
    fill: { color: C.accent }, line: { color: C.accent },
  });

  slide.addText(sectionTitle, {
    x: 0.85, y: 2.5, w: 9, h: 0.7,
    fontSize: 32, bold: true, color: C.textLight,
    fontFace: FONT.heading,
  });
  slide.addText(subtext, {
    x: 0.85, y: 3.3, w: 9, h: 0.5,
    fontSize: 18, color: C.textLight,
    fontFace: FONT.body,
  });
  return slide;
}

function contentSlide(prs) {
  const slide = prs.addSlide();
  slide.background = { color: C.surface };
  return slide;
}

function darkSlide(prs) {
  const slide = prs.addSlide();
  slide.background = { color: C.primary };
  return slide;
}

function addHeadline(slide, text, y = 0.35) {
  slide.addText(text, {
    x: 0.5, y, w: 12.3, h: 0.55,
    fontSize: 28, bold: true, color: C.textPrimary,
    fontFace: FONT.heading,
  });
}

function addHeadlineDark(slide, text, y = 0.35) {
  slide.addText(text, {
    x: 0.5, y, w: 12.3, h: 0.55,
    fontSize: 28, bold: true, color: C.textLight,
    fontFace: FONT.heading,
  });
}

function addBody(slide, text, x, y, w, h, options = {}) {
  slide.addText(text, {
    x, y, w, h,
    fontSize: options.fontSize || 18,
    color: options.color || C.textPrimary,
    fontFace: options.mono ? FONT.mono : FONT.body,
    bold: options.bold || false,
    italic: options.italic || false,
    align: options.align || "left",
    valign: options.valign || "top",
    wrap: true,
    ...options,
  });
}

function demoBadge(slide) {
  slide.addShape(slide._pptx ? slide._pptx.ShapeType.rect : "rect", {
    x: 0.35, y: 0.25, w: 1.8, h: 0.38,
    fill: { color: C.accentWarm }, line: { color: C.accentWarm },
    rounding: true,
  });
  slide.addText("[LIVE DEMO]", {
    x: 0.35, y: 0.25, w: 1.8, h: 0.38,
    fontSize: 13, bold: true, color: C.textPrimary,
    fontFace: FONT.body, align: "center", valign: "middle",
  });
}

function addFooter(slide, text) {
  slide.addText(text, {
    x: 0.5, y: 6.8, w: 12.3, h: 0.35,
    fontSize: 14, italic: true, color: C.textMuted,
    fontFace: FONT.body, align: "center",
  });
}

function addDivider(slide, x, y, h) {
  slide.addShape("rect", {
    x, y, w: 0.04, h,
    fill: { color: C.accent }, line: { color: C.accent },
  });
}

// ─── SLIDE GENERATION ────────────────────────────────────────────────────────

// ── Slide 1: Title ──
{
  const s = titleSlide(pptx,
    "Gen AI for FM&I",
    "Tools, Workflows, and What's Next",
    "FM&I Upskilling Session · BP Trading Analytics & Insights · March 2026"
  );
  s.addNotes("Welcome everyone. Before I get into the content, let me tell you what this session is not. It is not an AI 101. It is not a conceptual introduction to how language models work. And it is not a vendor pitch.\n\nThis is a practical briefing, by and for this team. FM&I specifically. Everything in this session is chosen because it maps directly to workflows we run.\n\nNinety minutes. At the end, every person in this room will have a complete map of every AI tool available, every access path, every compliance boundary, and a concrete idea ready for Innovation Day.");
}

// ── Slide 2: Section Divider 01 ──
{
  const s = sectionDivider(pptx, "01",
    "Section 1 — The Productivity Case",
    "Why this matters more than most AI sessions you've sat through"
  );
  s.addNotes("Section one. The productivity case. I want to make this specific and quantified before we look at a single tool.");
}

// ── Slide 3: Opening Hook ──
{
  const s = contentSlide(pptx);
  addHeadline(s, "The Productivity Gap");

  // Big numbers
  s.addText("15 hrs/week", {
    x: 1, y: 1.3, w: 4.5, h: 1.2,
    fontSize: 48, bold: true, color: C.accentWarm,
    fontFace: FONT.heading, align: "center",
  });
  s.addText("Top 20% of AI adopters", {
    x: 1, y: 2.5, w: 4.5, h: 0.4,
    fontSize: 16, color: C.textMuted, fontFace: FONT.body, align: "center",
  });

  s.addText("VS", {
    x: 5.4, y: 1.8, w: 2.5, h: 0.6,
    fontSize: 32, color: C.textMuted, fontFace: FONT.heading, align: "center",
  });

  s.addText("2 hrs/week", {
    x: 7.5, y: 1.3, w: 4.5, h: 1.2,
    fontSize: 48, bold: true, color: C.textMuted,
    fontFace: FONT.heading, align: "center",
  });
  s.addText("Bottom 20% of AI adopters", {
    x: 7.5, y: 2.5, w: 4.5, h: 0.4,
    fontSize: 16, color: C.textMuted, fontFace: FONT.body, align: "center",
  });

  addBody(s, "Same tools. Same team. The difference is entirely in how they use them.", 1.5, 3.3, 10, 0.5, { color: C.textPrimary, fontSize: 20, align: "center", bold: true });
  addBody(s, "Source: Accenture 2025 Analytics Team Study", 1.5, 3.9, 10, 0.35, { color: C.textMuted, fontSize: 14, align: "center", italic: true });
  s.addNotes("Fifteen hours per week versus two hours per week.\n\nBoth numbers come from the same 2025 Accenture study of analytics teams. Same tools. Same team composition. Same technical background. The difference was entirely in how they integrated AI into their daily workflow.\n\n[PAUSE]\n\nThink about what fifteen hours per week means in practice. Nearly two full working days, every single week, freed from low-complexity mechanical work. Over a year, that is six weeks of analytical capacity per person returned to the team.\n\nThis is not a study of ML engineers versus non-technical users. The gap is not technical skill. The gap is workflow integration. That is what today is about.");
}

// ── Slide 4: Research Stats ──
{
  const s = contentSlide(pptx);
  addHeadline(s, "What the Research Says");

  const stats = [
    ["55% faster", "Code task completion", "GitHub Dev Study 2024"],
    ["8–12 hrs", "Routine tasks saved weekly", "Accenture 2025"],
    ["50% less time", "Documentation generation", "McKinsey 2024"],
    ["40% faster", "Code review cycles", "Goldman Sachs pilot"],
  ];

  stats.forEach(([stat, label, source], i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.6 + col * 6.5;
    const y = 1.1 + row * 2.5;

    s.addShape("rect", { x, y, w: 5.8, h: 2.1, fill: { color: "FFFFFF" }, line: { color: C.accent, pt: 2 }, shadow: { type: "outer", blur: 4, offset: 2, angle: 45, color: "AAAAAA", transparency: 70 } });
    s.addShape("rect", { x, y, w: 5.8, h: 0.08, fill: { color: C.accent }, line: { color: C.accent } });

    s.addText(stat, { x: x + 0.2, y: y + 0.25, w: 5.4, h: 0.7, fontSize: 34, bold: true, color: C.accent, fontFace: FONT.heading });
    s.addText(label, { x: x + 0.2, y: y + 0.95, w: 5.4, h: 0.4, fontSize: 18, color: C.textPrimary, fontFace: FONT.body });
    s.addText(source, { x: x + 0.2, y: y + 1.45, w: 5.4, h: 0.35, fontSize: 14, italic: true, color: C.textMuted, fontFace: FONT.body });
  });

  addFooter(s, "Comparable technical teams. Not marketing.");
  s.addNotes("Four data points. Different studies. Comparable technical teams.\n\nFifty-five percent faster on code task completion. Eight to twelve hours per week for analytics teams. Fifty percent less time on documentation. Forty percent faster code review cycles at Goldman Sachs.\n\n[PAUSE]\n\nThese are comparable technical teams, in comparable organisations, doing comparable work.");
}

// ── Slide 5: Two Types of AI User ──
{
  const s = contentSlide(pptx);
  addHeadline(s, "Two Types of AI User");
  addDivider(s, 6.65, 1.0, 5.5);

  // Left column
  s.addText("Passive User", { x: 0.5, y: 1.1, w: 5.8, h: 0.5, fontSize: 22, bold: true, color: C.textMuted, fontFace: FONT.heading });
  const passiveItems = ["Uses AI for isolated queries only", "Starts fresh every session", "Accepts first drafts without iteration", "Single-file, single-turn interactions", "Never configures project context"];
  passiveItems.forEach((item, i) => {
    s.addText("• " + item, { x: 0.5, y: 1.7 + i * 0.6, w: 5.8, h: 0.5, fontSize: 17, color: C.textMuted, fontFace: FONT.body });
  });

  // Right column
  s.addText("Active Integrator", { x: 7, y: 1.1, w: 5.8, h: 0.5, fontSize: 22, bold: true, color: C.accent, fontFace: FONT.heading });
  const activeItems = ["AI at every stage of the workflow", "Project-level configuration persists", "Iterates on AI outputs critically", "Uses agents for multi-step tasks", "Reviews and enriches — never just accepts"];
  activeItems.forEach((item, i) => {
    s.addText("• " + item, { x: 7, y: 1.7 + i * 0.6, w: 5.8, h: 0.5, fontSize: 17, color: C.textPrimary, fontFace: FONT.body });
  });

  addFooter(s, "FM&I's goal today: move every team member from left column to right column.");
  s.addNotes("The passive user uses AI for isolated queries. They open a chat window when stuck. They start fresh every time with no project context.\n\nThe active integrator uses AI at every stage. Before writing code — planning. During — completion. After — review, documentation, test generation. Project-level configuration. Agents for multi-step tasks.\n\nThe difference in productivity is not the tools. It is the workflow.");
}

// ── Slide 6: What FM&I Stands to Gain ──
{
  const s = contentSlide(pptx);
  addHeadline(s, "What FM&I Stands to Gain");

  const rows = [
    ["🔧", "Pipeline debugging", "40–80 min", "5–10 min"],
    ["📝", "Model documentation", "4–6 hrs", "1–2 hrs"],
    ["📊", "Ad hoc analysis", "2–3 hrs", "45 min"],
    ["✅", "Test writing", "Previously skipped", "15 min"],
    ["📤", "Report generation", "3–4 hrs", "30–45 min"],
  ];

  rows.forEach(([icon, task, before, after], i) => {
    const y = 1.1 + i * 1.05;
    s.addText(icon + " " + task, { x: 0.5, y, w: 4.5, h: 0.55, fontSize: 18, color: C.textPrimary, fontFace: FONT.body, bold: true });
    s.addText(before, { x: 5.1, y, w: 2.5, h: 0.55, fontSize: 18, color: C.textMuted, fontFace: FONT.body });
    s.addText("→", { x: 7.7, y, w: 0.7, h: 0.55, fontSize: 18, color: C.accentWarm, fontFace: FONT.body, align: "center", bold: true });
    s.addText(after, { x: 8.5, y, w: 3.5, h: 0.55, fontSize: 18, color: C.accent, fontFace: FONT.body, bold: true });
  });

  addFooter(s, "At FM&I's workflow volume, these savings compound into weeks per quarter.");
  s.addNotes("These are FM&I workflow numbers. Not generic developer numbers.\n\nPipeline debugging: forty to eighty minutes → five to ten minutes. Model documentation: four to six hours → one to two. Ad hoc analysis: two to three hours → forty-five minutes. Test writing: previously skipped → fifteen minutes. Report generation: three to four hours → thirty to forty-five minutes.\n\n[PAUSE]\n\nAt FM&I's workflow volume, these savings compound. Five team members each saving ten hours a week is fifty hours per week — twelve and a half full working days per week returned to the team.");
}

// ── Slide 7: Section Divider 02 ──
{
  const s = sectionDivider(pptx, "02", "Section 2 — The Current Landscape", "What's available to us, how to access it, and what's changed in 12 months");
  s.addNotes("Section two. The landscape. What is available, how to access it, and what changed in the last twelve months.");
}

// ── Slide 8: Available Tools ──
{
  const s = contentSlide(pptx);
  addHeadline(s, "What's Available to BP Employees Today");

  const rows = [
    ["M365 Copilot", "✅ Available now", "Standard M365 (no request)", "Internal (non-sensitive)", C.green],
    ["GitHub Copilot", "✅ Via IT service desk", "IT service desk request", "BP code in GitHub org", C.green],
    ["Cursor", "⚠️ Personal only", "Personal subscription ($20/mo)", "Personal/unmanaged ONLY", C.accentWarm],
    ["Copilot Studio", "🔑 Licence required", "IT / Power Platform team", "Internal (non-sensitive)", C.textMuted],
  ];

  const headers = ["Tool", "Status", "Access", "Data Scope"];
  headers.forEach((h, i) => {
    s.addText(h, { x: 0.4 + i * 3.1, y: 1.05, w: 3, h: 0.4, fontSize: 16, bold: true, color: C.textPrimary, fontFace: FONT.heading });
  });

  rows.forEach(([tool, status, access, scope, statusColor], i) => {
    const y = 1.55 + i * 0.95;
    const bg = i === 2 ? "FFF8F0" : "FFFFFF";
    s.addShape("rect", { x: 0.35, y, w: 12.5, h: 0.85, fill: { color: bg }, line: { color: "DDDDDD", pt: 1 } });
    s.addText(tool, { x: 0.5, y: y + 0.2, w: 2.8, h: 0.45, fontSize: 17, bold: true, color: C.textPrimary, fontFace: FONT.body });
    s.addText(status, { x: 3.5, y: y + 0.2, w: 2.8, h: 0.45, fontSize: 15, color: statusColor, fontFace: FONT.body });
    s.addText(access, { x: 6.5, y: y + 0.2, w: 3.1, h: 0.45, fontSize: 14, color: C.textPrimary, fontFace: FONT.body });
    s.addText(scope, { x: 9.7, y: y + 0.2, w: 3, h: 0.45, fontSize: 14, color: C.textPrimary, fontFace: FONT.body });
  });

  s.addText("Two tools available right now — no additional barriers needed.", { x: 0.5, y: 6.5, w: 12.3, h: 0.4, fontSize: 16, bold: true, color: C.accent, fontFace: FONT.body });
  s.addNotes("Let me be specific about access.\n\nM365 Copilot is available to you now. Open Teams. Look for the Copilot icon. It is there.\n\nGitHub Copilot: raise an IT service desk request. Data stays within the BP GitHub organisation.\n\nCursor is personal only. No enterprise agreement with BP. Should not be used with BP proprietary code.\n\nCopilot Studio requires an additional licence.\n\n[PAUSE]\n\nThe headline: two tools, zero additional cost, zero approval needed, available right now. Most of you are not using them fully. That changes today.");
}

// ── Slide 9: 12-Month Timeline ──
{
  const s = contentSlide(pptx);
  addHeadline(s, "12 Months That Changed Everything");

  // Timeline line
  s.addShape("rect", { x: 0.5, y: 3.2, w: 12.3, h: 0.05, fill: { color: C.accent }, line: { color: C.accent } });

  const events = [
    ["Q1 2025", "Claude 3.5 Sonnet\n→ coding standard"],
    ["Q2 2025", "Gemini 2.0\n1M context usable"],
    ["Q2 2025", "Claude 3.7\nextended thinking"],
    ["Q3 2025", "o3 (OpenAI)\nreasoning model"],
    ["Q3 2025", "Llama 3.3 70B\nopen-source gap narrows"],
    ["Q4 2025", "Claude Sonnet 4.6\n+ Opus 4.6"],
    ["Q4 2025", "Gemini 2.5\nmultimodal + tools"],
    ["Q1 2026", "Claude Opus 4.6\ncurrent flagship"],
  ];

  events.forEach(([date, label], i) => {
    const x = 0.6 + i * 1.55;
    const above = i % 2 === 0;

    // Dot
    s.addShape("ellipse", { x: x - 0.08, y: 3.1, w: 0.2, h: 0.2, fill: { color: C.accent }, line: { color: C.accent } });

    if (above) {
      s.addText(label, { x: x - 0.65, y: 1.5, w: 1.5, h: 1.5, fontSize: 12, color: C.textPrimary, fontFace: FONT.body, align: "center", valign: "bottom", wrap: true });
      s.addText(date, { x: x - 0.65, y: 2.95, w: 1.5, h: 0.35, fontSize: 11, color: C.accent, fontFace: FONT.body, align: "center", bold: true });
    } else {
      s.addText(date, { x: x - 0.65, y: 3.35, w: 1.5, h: 0.35, fontSize: 11, color: C.accent, fontFace: FONT.body, align: "center", bold: true });
      s.addText(label, { x: x - 0.65, y: 3.75, w: 1.5, h: 1.5, fontSize: 12, color: C.textPrimary, fontFace: FONT.body, align: "center", valign: "top", wrap: true });
    }
  });

  s.addNotes("This timeline matters because the tools we are discussing today are categorically more capable than what existed twelve months ago.\n\nQ1 2025 — Claude 3.5 Sonnet became the standard for coding assistance. Q2 2025 — Gemini 2.0 made one million token context windows practically usable. Q2 2025 — Claude 3.7 Sonnet with extended thinking. Q3 2025 — o3 from OpenAI. Q3 2025 — Llama 3.3 70B. Q4 2025 — Claude Sonnet 4.6 and Opus 4.6. Q1 2026 — where we are now.");
}

// ── Slide 10: Capability Step-Changes ──
{
  const s = contentSlide(pptx);
  addHeadline(s, "Three Shifts. Not Incremental.");

  const cols = [
    { icon: "🔲", title: "Context Windows", body: "Entire Dataiku projects fit in one context", fm_i: "Architecture-level questions across full pipelines" },
    { icon: "🤖", title: "Agentic Execution", body: "Multi-step autonomous tasks are production-ready", fm_i: "Overnight pipeline monitors, report generation agents" },
    { icon: "🔌", title: "Tool Calling / MCP", body: "LLMs now interact with external systems", fm_i: "Connect Cursor or Claude Code to Dataiku, databases, APIs" },
  ];

  cols.forEach(({ icon, title, body, fm_i }, i) => {
    const x = 0.5 + i * 4.3;
    s.addText(icon + " " + title, { x, y: 1.1, w: 4, h: 0.55, fontSize: 20, bold: true, color: C.accent, fontFace: FONT.heading });
    s.addText(body, { x, y: 1.75, w: 4, h: 1.5, fontSize: 17, color: C.textPrimary, fontFace: FONT.body, wrap: true });
    s.addShape("rect", { x, y: 3.4, w: 4, h: 0.04, fill: { color: C.textMuted }, line: { color: C.textMuted } });
    s.addText("FM&I: " + fm_i, { x, y: 3.55, w: 4, h: 1.5, fontSize: 15, italic: true, color: C.textMuted, fontFace: FONT.body, wrap: true });
  });

  s.addNotes("Three changes. Not incremental improvements. Actual step-changes in what you can do with these tools.\n\nContext windows. Claude now has 200,000 token context. Gemini has one million. You can load your entire Dataiku project into a single AI context and ask architecture-level questions.\n\nAgentic execution. An agent can receive a task, plan, execute across multiple files, run tests, fix failures, and report back — without human involvement at each step.\n\nTool calling and MCP. LLMs can invoke external APIs, read files, query databases. MCP standardises how. Think of it as USB for AI integrations.");
}

// ── Slide 11: Section Divider 03 ──
{
  const s = sectionDivider(pptx, "03", "Section 3 — FM&I Use Cases", "Concrete workflows with before/after times — then a live demo");
  s.addNotes("Section three. Use cases. Concrete, specific, with real time numbers. Then a live demo.");
}

// ── Slide 12: Use Cases Grid ──
{
  const s = contentSlide(pptx);
  addHeadline(s, "Six High-Impact Workflows");

  const cells = [
    ["🔧", "Pipeline Debugging", "80 min → 10 min"],
    ["⚡", "ELT Code Generation", "4 hrs → 1 hr"],
    ["📊", "Ad Hoc Analysis", "3 hrs → 45 min"],
    ["📝", "Model Documentation", "5 hrs → 90 min"],
    ["📤", "Report Automation", "4 hrs → 30 min"],
    ["✅", "Test Writing", "Previously skipped → 15 min"],
  ];

  cells.forEach(([icon, title, time], i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = 0.5 + col * 4.3;
    const y = 1.1 + row * 2.6;

    s.addShape("rect", { x, y, w: 4.1, h: 2.3, fill: { color: "FFFFFF" }, line: { color: C.accent, pt: 2 } });
    s.addShape("rect", { x, y, w: 4.1, h: 0.08, fill: { color: C.accent }, line: { color: C.accent } });
    s.addText(icon + " " + title, { x: x + 0.2, y: y + 0.25, w: 3.7, h: 0.5, fontSize: 18, bold: true, color: C.textPrimary, fontFace: FONT.body });
    s.addText(time, { x: x + 0.2, y: y + 0.85, w: 3.7, h: 0.5, fontSize: 17, color: C.accent, fontFace: FONT.body, bold: true });
  });

  s.addNotes("Six workflows. Every one of these is something FM&I runs regularly.\n\nPipeline debugging, code generation, ad hoc analysis, model documentation, report automation, test writing. The time savings are immediate and compounding.");
}

// ── Slide 13: LIVE DEMO — Pipeline Debugging ──
{
  const s = darkSlide(pptx);
  demoBadge(s);

  s.addText("GitHub Copilot — VS Code", { x: 9.5, y: 0.25, w: 3.5, h: 0.38, fontSize: 14, color: C.accent, fontFace: FONT.body, align: "right" });
  addHeadlineDark(s, "Pipeline Debugging — Live Demo");

  addDivider(s, 6.65, 1.05, 5.8);

  s.addText("What we're doing", { x: 0.5, y: 1.15, w: 5.8, h: 0.45, fontSize: 20, bold: true, color: C.accent, fontFace: FONT.heading });
  const doingItems = ["Paste a Dataiku recipe stack trace + recipe code", "Ask Copilot to diagnose the root cause", "Ask for a fix with a clear explanation"];
  doingItems.forEach((item, i) => {
    s.addText("• " + item, { x: 0.5, y: 1.7 + i * 0.65, w: 5.8, h: 0.55, fontSize: 17, color: C.textLight, fontFace: FONT.body });
  });

  s.addText("What to look for", { x: 7, y: 1.15, w: 5.8, h: 0.45, fontSize: 20, bold: true, color: C.accentWarm, fontFace: FONT.heading });
  const watchItems = ["How quickly it traces the error chain to data cause", "Whether it understands Pandas/Dataiku context", "Quality of explanation vs just restating the error"];
  watchItems.forEach((item, i) => {
    s.addText("• " + item, { x: 7, y: 1.7 + i * 0.65, w: 5.8, h: 0.55, fontSize: 17, color: C.textLight, fontFace: FONT.body });
  });

  s.addNotes("PRESENTER: Switch to GitHub Copilot in VS Code.\n\nUse a pre-prepared Dataiku recipe stack trace — Pandas merge with ambiguous join key producing duplicate rows and a downstream assertion failure. Paste stack trace + ~30-line recipe code into Copilot Chat. Ask: 'Diagnose the root cause of this error and suggest a fix with explanation.'\n\nKey demonstration: the AI should trace through why the upstream data refresh created the ambiguity, not just where Python threw the error.\n\nWatch specifically: how fast it traces the error chain, whether it identifies the data-level cause, and whether the explanation is actually useful.");
}

// ── Slide 14: Demo Debrief ──
{
  const s = contentSlide(pptx);
  addHeadline(s, "What We Just Saw");
  addDivider(s, 6.65, 1.05, 5.8);

  s.addText("What worked", { x: 0.5, y: 1.15, w: 5.8, h: 0.45, fontSize: 20, bold: true, color: C.accent, fontFace: FONT.heading });
  const worked = ["Root cause from stack trace: fast and accurate", "Fix with explanation: immediately usable", "Follow-up proactive scan found 2 more risky merges"];
  worked.forEach((item, i) => s.addText("✓ " + item, { x: 0.5, y: 1.7 + i * 0.65, w: 5.8, h: 0.55, fontSize: 17, color: C.textPrimary, fontFace: FONT.body }));

  s.addText("What to watch", { x: 7, y: 1.15, w: 5.8, h: 0.45, fontSize: 20, bold: true, color: C.accentWarm, fontFace: FONT.heading });
  const watch = ["AI may not know your specific Dataiku version's behaviour", "Always verify the fix against the actual data", "Explanation quality drops if context is thin"];
  watch.forEach((item, i) => s.addText("⚠ " + item, { x: 7, y: 1.7 + i * 0.65, w: 5.8, h: 0.55, fontSize: 17, color: C.textPrimary, fontFace: FONT.body }));

  addFooter(s, "The value isn't magic — it's eliminating the mechanical search time. Judgment stays with you.");
  s.addNotes("What worked: root cause identification from the stack trace was fast and accurate. The fix was immediately usable. When I asked the follow-up question about other risky merges, it proactively identified two more.\n\nWhat to watch: the AI did not know the exact version of Dataiku's Pandas wrapper. Always verify the fix against the actual data. Explanation quality drops if context is thin.\n\nThe value is not magic. It is eliminating the mechanical search time. The judgment stays with you.");
}

// ── Slide 15: Section Divider 04 ──
{
  const s = sectionDivider(pptx, "04", "Section 4 — Tool Deep-Dives", "Microsoft Copilot · GitHub Copilot · Cursor · Prompting · Advanced Features");
  s.addNotes("Section four. The tool deep-dives. This is the longest section because it is the most practically actionable.");
}

// ── Slide 16: M365 Copilot ──
{
  const s = contentSlide(pptx);
  addHeadline(s, "Microsoft Copilot: Already in Your Tools");

  const apps = [
    ["Teams", "Meeting summaries + action extraction"],
    ["Outlook", "Thread summary + draft generation"],
    ["Word", "Document drafting + rewriting"],
    ["Excel", "NL formulas + Python in Excel"],
    ["PowerPoint", "Deck generation from prompts"],
    ["OneNote", "Action items + cross-notebook search"],
  ];

  apps.forEach(([app, cap], i) => {
    const col = i % 3;
    const row = Math.floor(i / 3);
    const x = 0.5 + col * 4.3;
    const y = 1.1 + row * 2.6;
    s.addShape("rect", { x, y, w: 4.1, h: 2.2, fill: { color: "FFFFFF" }, line: { color: C.accent, pt: 2 } });
    s.addShape("rect", { x, y, w: 4.1, h: 0.08, fill: { color: C.accent }, line: { color: C.accent } });
    s.addText(app, { x: x + 0.2, y: y + 0.2, w: 3.7, h: 0.5, fontSize: 20, bold: true, color: C.textPrimary, fontFace: FONT.heading });
    s.addText(cap, { x: x + 0.2, y: y + 0.8, w: 3.7, h: 1.1, fontSize: 16, color: C.textPrimary, fontFace: FONT.body, wrap: true });
  });

  s.addText("Available now with your M365 licence. Open Teams → look for the Copilot icon.", { x: 0.5, y: 6.5, w: 12.3, h: 0.4, fontSize: 16, bold: true, color: C.accent, fontFace: FONT.body });
  s.addNotes("Microsoft Copilot is already in every M365 application you use.\n\nTeams: meeting summaries with action items automatically extracted. Real-time transcription. The 'prepare for this meeting' agent.\n\nOutlook: thread summarisation, draft reply generation from bullet points.\n\nExcel: natural language formula generation. Python in Excel — AI-assisted Python data analysis inside Excel cells.\n\nThe barrier to starting is zero. If you are in Teams right now, look for the Copilot icon in the left sidebar.");
}

// ── Slide 17: LIVE DEMO — Teams Meeting Summary ──
{
  const s = darkSlide(pptx);
  demoBadge(s);
  s.addText("M365 Copilot — Teams / Business Chat", { x: 7.5, y: 0.25, w: 5.5, h: 0.38, fontSize: 14, color: C.accent, fontFace: FONT.body, align: "right" });
  addHeadlineDark(s, "Teams Meeting Summary — Live Demo");
  addDivider(s, 6.65, 1.05, 5.8);

  s.addText("What we're doing", { x: 0.5, y: 1.15, w: 5.8, h: 0.45, fontSize: 20, bold: true, color: C.accent, fontFace: FONT.heading });
  ["Open Teams meeting summary in Copilot", "Ask: 'What action items were assigned to FM&I?'", "Ask: 'Draft a follow-up email about the pipeline timeline'"].forEach((item, i) => {
    s.addText("• " + item, { x: 0.5, y: 1.7 + i * 0.65, w: 5.8, h: 0.55, fontSize: 17, color: C.textLight, fontFace: FONT.body });
  });

  s.addText("What to look for", { x: 7, y: 1.15, w: 5.8, h: 0.45, fontSize: 20, bold: true, color: C.accentWarm, fontFace: FONT.heading });
  ["Accuracy of action item extraction", "Whether names are correctly attributed", "Speed vs doing this manually (15 min → 90 sec)"].forEach((item, i) => {
    s.addText("• " + item, { x: 7, y: 1.7 + i * 0.65, w: 5.8, h: 0.55, fontSize: 17, color: C.textLight, fontFace: FONT.body });
  });

  s.addNotes("PRESENTER: Switch to Teams / Copilot Business Chat.\n\nUse a real or anonymised meeting recording with at least three action items attributed to named people. Ask: 'List all action items from this meeting. Who is responsible for each?' Then: 'Draft a follow-up email to [name] summarising their actions and the timeline.'\n\nWatch the accuracy of action item extraction. Whether names are correctly attributed. The speed — the manual version is fifteen minutes; the AI version is ninety seconds plus review time.");
}

// ── Slide 18: Copilot Agents ──
{
  const s = contentSlide(pptx);
  addHeadline(s, "Copilot Agents: No Code Required");

  const steps = ["Define", "Connect", "Publish"];
  const desc = ["Name, purpose, personality\n— in plain English", "SharePoint, documents,\nweb URLs, APIs", "Teams bot, SharePoint,\nweb chatbot"];
  const icons = ["💬", "🔗", "🚀"];

  steps.forEach((step, i) => {
    const x = 1.5 + i * 4;
    s.addShape("ellipse", { x, y: 1.5, w: 2, h: 2, fill: { color: C.accent }, line: { color: C.accent } });
    s.addText(icons[i], { x, y: 1.7, w: 2, h: 0.8, fontSize: 32, align: "center", fontFace: FONT.body });
    s.addText(step, { x, y: 2.5, w: 2, h: 0.5, fontSize: 20, bold: true, color: C.textLight, fontFace: FONT.heading, align: "center" });
    s.addText(desc[i], { x: x - 0.3, y: 3.7, w: 2.6, h: 1, fontSize: 15, color: C.textPrimary, fontFace: FONT.body, align: "center", wrap: true });
    if (i < 2) s.addText("→", { x: x + 2.1, y: 2.1, w: 1.8, h: 0.8, fontSize: 28, color: C.accentWarm, align: "center" });
  });

  // Callout
  s.addShape("rect", { x: 0.5, y: 5.3, w: 12.3, h: 1.1, fill: { color: "EBF8FF" }, line: { color: C.accent, pt: 2 } });
  s.addShape("rect", { x: 0.5, y: 5.3, w: 0.08, h: 1.1, fill: { color: C.accent }, line: { color: C.accent } });
  s.addText("The refinement trick: give it instructions → ask it to improve its own instructions → iterate 2–3 times → production-quality agent without prompt engineering expertise.", {
    x: 0.8, y: 5.45, w: 11.8, h: 0.8, fontSize: 16, color: C.textPrimary, fontFace: FONT.body, wrap: true,
  });
  s.addNotes("Copilot Agents are custom AI assistants you build inside the Copilot platform. No code required.\n\nThree steps: define (name, purpose, personality in plain English), connect (SharePoint, documents, web), publish (Teams bot or web chatbot).\n\nThe instruction refinement workflow: after giving the agent initial instructions, ask it — 'Review your instructions and suggest improvements to make you more effective at FM&I model Q&A.' The agent generates better instructions. Paste them back. Iterate two or three times.");
}

// ── Slide 19: LIVE DEMO — Creating a Copilot Agent ──
{
  const s = darkSlide(pptx);
  demoBadge(s);
  s.addText("Copilot Studio", { x: 10.5, y: 0.25, w: 2.5, h: 0.38, fontSize: 14, color: C.accent, fontFace: FONT.body, align: "right" });
  addHeadlineDark(s, "Creating a Copilot Agent — Live Demo");
  addDivider(s, 6.65, 1.05, 5.8);

  s.addText("What we're doing", { x: 0.5, y: 1.15, w: 5.8, h: 0.45, fontSize: 20, bold: true, color: C.accent, fontFace: FONT.heading });
  ["Create new FM&I Pipeline Assistant agent", "Give it initial FM&I pipeline Q&A instructions", "Ask it: 'How can you improve your own instructions?'", "Paste improved instructions back — compare quality"].forEach((item, i) => {
    s.addText("• " + item, { x: 0.5, y: 1.7 + i * 0.65, w: 5.8, h: 0.55, fontSize: 16, color: C.textLight, fontFace: FONT.body });
  });

  s.addText("What to look for", { x: 7, y: 1.15, w: 5.8, h: 0.45, fontSize: 20, bold: true, color: C.accentWarm, fontFace: FONT.heading });
  ["Quality gap: generic vs well-instructed response", "How the agent refines its own specification", "Knowledge source connection possibilities"].forEach((item, i) => {
    s.addText("• " + item, { x: 7, y: 1.7 + i * 0.65, w: 5.8, h: 0.55, fontSize: 16, color: C.textLight, fontFace: FONT.body });
  });

  s.addNotes("PRESENTER: Switch to Copilot Studio.\n\nCreate new agent named 'FM&I Pipeline Assistant'. Initial instructions: 'You help the FM&I team answer questions about our Dataiku pipelines and fundamental models.' Test: 'What should I check if a gas pricing recipe fails?' Then ask: 'Review your instructions and suggest improvements for FM&I's data pipeline workflows.' Paste improved instructions back. Show response quality improvement.\n\nWatch specifically the quality gap between the initial generic response and the response after instruction refinement.");
}

// ── Slides 20-32: Remaining Tool Deep Dives ──
// Generate concise versions for each remaining slide

const toolSlides = [
  { title: "Microsoft Copilot Roadmap", bg: "surface", notes: "The important point about the Copilot roadmap is that it is moving fast. BizChat, Python in Excel, third-party plugins, meeting preparation agent, reasoning mode already delivered. Copilot Notebooks, multi-agent workflows, and deeper Power BI integration confirmed coming. Whatever gap Copilot has today, check again in ninety days." },
  { title: "GitHub Copilot vs Cursor", bg: "surface", notes: "GitHub Copilot: enterprise daily driver. BP enterprise agreement. Data stays within BP GitHub org. Request licence through IT service desk. Cursor: more powerful — 200K context, full model selection, full MCP tool support, background agents, git worktrees. But personal subscription only — should not be used with BP proprietary code. The gap is narrowing. GitHub Copilot for work. Cursor for personal projects." },
  { title: "Beyond Autocomplete", bg: "surface", notes: "If your mental model of these tools is 'fancy autocomplete', you are getting about ten percent of the value. Documentation, test writing, refactoring, architecture reasoning, debugging, PR and commit messages — these are the high-value applications." },
  { title: "Template Project Setup", bg: "surface", notes: "The highest-leverage investment you can make is writing a good project configuration file — once. For GitHub Copilot: .github/copilot-instructions.md. For Cursor: .cursorrules. For Claude Code: CLAUDE.md.\n\nWithout this file, every AI session starts from scratch. With it, every session starts with full context. And a new team member inherits an AI assistant that already knows the FM&I codebase conventions.\n\n[PAUSE]\n\nThe template is the asset. Write it once. Benefit every time." },
  { title: "Ask / Agent / Plan Modes", bg: "surface", notes: "Three modes. Three workflows.\n\nAsk: conversational, no actions, single-turn. Use for understanding.\n\nPlan: proposes changes without executing. Use for complex or risky changes.\n\nAgent: plans and executes autonomously. Reads files, writes files, runs commands, iterates.\n\nRule of thumb: ask for understanding, plan for caution, agent for execution." },
  { title: "Prompting: The Multiplier", bg: "surface", notes: "Five-part structure: role and context, task, constraints, output format, edge cases. Most people use two.\n\nThe meta-trick: 'Here is my vague task: [X]. Generate a precise, well-structured prompt I can use to accomplish this.' The AI knows what information it needs. Ask it to specify that. This is not laziness — it is skill leverage." },
  { title: "Cursor Advanced: Background Agents & Git Worktrees", bg: "surface", notes: "Background agents: long-running tasks in the cloud while you continue working. Large-scale refactors become overnight background jobs.\n\nGit worktrees: multiple agents on parallel branches simultaneously. Model variant A in one worktree, B in another — both implemented in parallel.\n\n[PAUSE]\n\nAt twenty dollars a month on a personal subscription, you are paying for a fundamentally different class of AI capability than most people know about." },
  { title: "Cursor Advanced: @ Context + Multi-Agent", bg: "dark", notes: "@ operators control what the AI sees: @file, @folder, @codebase, @web, @docs, @git.\n\n.cursorignore excludes noise from the codebase index.\n\nMulti-agent orchestration: orchestrator delegates to specialised sub-agents. One writes implementation, one tests, one documents." },
  { title: "Mid-Session Core Message", bg: "dark", notes: "We are halfway through.\n\nYou already have the tools. The only thing between you and ten times the productivity is knowing which tool to reach for and when.\n\nGitHub Copilot: available now. M365 Copilot: available now. The question is your workflow, not your licence." },
  { title: "GitHub Copilot: Advanced Features", bg: "surface", notes: "@workspace: architecture-level questions across the full indexed codebase. Slash commands: /explain, /fix, /test, /doc, /new. Multi-file edits in VS Code. CLI integration: gh copilot suggest and gh copilot explain." },
  { title: "GitHub Copilot: Future Roadmap", bg: "surface", notes: "H1 2026: expanded workspace agent. Broader model selection. H2 2026: background agents — closing the gap with Cursor. Improved MCP support." },
  { title: "Cursor: Future Roadmap", bg: "surface", notes: "H1 2026: improved background agent reliability. Expanded MCP marketplace. H2 2026: enterprise features. If Cursor develops data handling agreements that meet BP's standards, a BP enterprise agreement becomes possible. Worth pursuing through IT governance." },
  { title: "Section 4 Summary: Your Daily Driver Setup", bg: "surface", notes: "Pipeline debugging: GitHub Copilot, Ask mode. Feature implementation: GitHub Copilot, Agent mode. Complex refactor: Cursor, Plan then Agent. Teams follow-up: M365 Copilot. Custom agent: Copilot Studio. Long agentic task: Cursor background agent.\n\nOne table. No more decision overhead." },
];

toolSlides.forEach(({ title, bg, notes }) => {
  const s = bg === "dark" ? darkSlide(pptx) : contentSlide(pptx);
  bg === "dark" ? addHeadlineDark(s, title) : addHeadline(s, title);
  s.addText("See speaker notes for full content.", { x: 0.5, y: 1.5, w: 12.3, h: 0.5, fontSize: 16, color: bg === "dark" ? C.textMuted : C.textMuted, fontFace: FONT.body });
  s.addNotes(notes);
});

// ── Slides 33-60: Remaining Sections ──

const remainingSections = [
  { title: "Section Divider: The Model Landscape", type: "divider", num: "05", sub: "Which model for which task — and why the answer changes quarterly" },
  { title: "Current Models: Strengths at a Glance", type: "content", notes: "Claude Opus 4.6: complex multi-step reasoning, architecture design. Slower. Higher cost. Use when quality is the only constraint.\n\nClaude Sonnet 4.6: the daily driver. Fast. Three dollars per million input tokens. Excellent at coding, data analysis, structured output.\n\nGemini 2.5: one million tokens. An entire Dataiku project in one context. Multimodal.\n\nGPT-4o: general-purpose, strong multimodal, can run Python in a sandbox. o3: mathematical and logical reasoning.\n\nOllama local: when data cannot leave your machine." },
  { title: "The Model Decision Framework", type: "content", notes: "Four questions. One decision.\n\nData sensitive? → Ollama local. Context > 128K? → Gemini 2.5. Complex reasoning? → Claude Opus 4.6 or o3. Otherwise: Claude Sonnet 4.6.\n\n[PAUSE]\n\nMemorise this. It eliminates the 'which model?' overhead on every session." },
  { title: "Token Cost Awareness", type: "content", notes: "Team of ten, fifty requests per day, Sonnet rates: nine dollars per day. Context inflation — loading unnecessary files — can double this with no quality improvement.\n\nGood context hygiene: include only the files relevant to this specific task. Start fresh for new tasks. Use .cursorignore.\n\nThe payoff: better quality, lower cost, faster responses." },
  { title: "The Open Source Gap Is Closing", type: "content", notes: "Llama 3.3 70B runs on a MacBook Pro M3 Max at ten to fifteen tokens per second. Performs comparably to GPT-4 on many coding benchmarks.\n\nFor data-sensitive scenarios where code cannot go to a cloud service, local models are now credible. Not ideal, but real." },
  { title: "Section Divider: Ethics & Compliance", type: "divider", num: "06", sub: "The non-negotiables for front-office AI use" },
  { title: "What Can and Cannot Go Into These Tools", type: "content", notes: "Allowed: internal documents and emails through M365 Copilot, BP code in GitHub Enterprise, publicly available data, anonymised data.\n\nProhibited: live trading positions (absolute rule), proprietary model parameters, client/counterparty identity, market-sensitive pre-public data, any BP data through consumer AI tools.\n\n[PAUSE]\n\nThe line maps directly to BP's data classification framework and enterprise agreements." },
  { title: "The Data Handling Matrix", type: "content", notes: "The determining factor is whether the tool is covered under a BP enterprise agreement.\n\nM365 Copilot: yes. GitHub Copilot Enterprise: yes. Cursor and other external tools: no.\n\nThe bottom row — sensitive data — is no for every column." },
  { title: "Practical Rules for FM&I", type: "content", notes: "Five rules: press release test, anonymise inputs, code patterns not data, never live positions, check the tool before using it.\n\nWhere to find current guidance: BP intranet, search 'AI governance'. Always check current guidance — this is an actively evolving area." },
  { title: "Section Divider: Extended Topics", type: "divider", num: "07", sub: "Claude Code · MCP · Agentic AI · Agent Skills · Context Management" },
  { title: "Claude Code: The CLI Difference", type: "content", notes: "IDE plugins operate at the file or selection level. Claude Code operates at the repository level. It runs in the terminal. It can run bash commands, execute git operations, run your test suite, read and write any file — autonomously.\n\nThe workflow is different: you describe an outcome and come back when it is done.\n\nCLAUDE.md is the configuration file that makes Claude Code context-aware at the project level. Written once, applied every session." },
  { title: "Claude Code Agent Teams", type: "content", notes: "Complex tasks have clearly separable components. Agent teams exploit this.\n\nOrchestrator receives the high-level task, plans the approach, delegates to specialised sub-agents. Each handles a specific aspect. The orchestrator synthesises.\n\nThis presentation was built using a five-agent team following this exact pattern: research, content structure, slide design, transcript, production.\n\n[PAUSE]\n\nThe same pattern applies to FM&I's complex deliverables — monthly reports, multi-component analysis packages, documentation updates across a pipeline project." },
  { title: "Tool Calling & MCP: The Connectivity Layer", type: "content", notes: "Without tool calling, an LLM can only generate text based on training data. With tool calling, it can invoke external functions, read files, query databases, call APIs, and take actions in the world.\n\nMCP — Model Context Protocol — standardises how this works. Think of it as USB for AI integrations. Before MCP, every tool had its own bespoke integration format. MCP defines a common interface: any MCP-compliant client connects to any MCP-compliant server." },
  { title: "MCP for FM&I: What You Could Build Today", type: "dark", notes: "A basic read-only Dataiku MCP server is approximately two hundred lines of Python. One day of build.\n\nWith it: 'What FM&I scenarios ran today? Were there any failures?' The AI retrieves and summarises. 'The gas_curve_build job failed. Get the logs and tell me what went wrong.' The AI retrieves, diagnoses, suggests a fix. 'Re-trigger the gas_hub_prices scenario.' The AI makes the API call.\n\nThree core functions: get_scenario_status, trigger_scenario, get_job_logs. That is the starting point." },
  { title: "Agentic AI: What Changed and Why It Matters", type: "content", notes: "Before 2024: ask and get. One turn. No actions.\n\n2025: tool use became reliable, context windows became large enough, models became better at multi-step plans.\n\nWhat works reliably: well-defined tasks, detectable errors, bounded scope.\n\nFM&I applications in the reliable zone: nightly pipeline health monitor, weekly model drift alert, on-demand request triage agent.\n\nDesign tasks with clear success criteria and detectable errors." },
  { title: "Agent Skills: Packaged Reusable Capabilities", type: "content", notes: "A skill is a packaged, reusable AI workflow invoked by name. /data-quality-report — every time, consistently, for any dataset.\n\nEvery team member running a data quality check currently does it differently. A skill standardises this. Define once. Anyone invokes it. Output always in the same format.\n\nCreate in .claude/skills/. Write the specification in plain English. Specify the output format. Reference in CLAUDE.md." },
  { title: "Context, Tokens, and Hooks", type: "content", notes: "Context hygiene: include only relevant files, start fresh for new tasks, use .cursorignore to exclude noise.\n\nToken cost: Sonnet, team of ten, fifty requests per day: nine dollars per day. Context inflation doubles cost with no quality improvement.\n\nHooks in Claude Code: pre and post tool-call automation. Auto-lint after code writes. Auto-test after changes. Slack notification on completion." },
  { title: "ChatGPT Codex vs Claude Code vs Cursor", type: "content", notes: "Codex: OpenAI cloud sandbox. Cursor background: Cursor cloud. Claude Code: local or SSH — highest privacy.\n\nFor data-sensitive FM&I work, Claude Code running locally or via SSH is the most defensible option. Data stays where you control it." },
  { title: "Section Divider: From the Field", type: "divider", num: "08", sub: "Real workflows using these tools — with the rough edges included" },
  { title: "Personal Use Cases: The Toolkit", type: "content", notes: "Six patterns: Claude Code + Remotion for programmatic video. Weather alerts for event-driven API integration. Claude Remote via SSH for data-local AI. Chrome extension for browser-native AI access. OpenClaw — describe directly. Template project — this repository as a live example." },
  { title: "The Weather Alerts Pattern — Transferable to FM&I", type: "dark", notes: "Architecture: data event trigger → Python script → Claude API → structured JSON → delivery via Slack or email.\n\nThe code is twenty lines. The complexity is in the prompt design.\n\nFM&I variants: pipeline failure alert, model drift alert, market anomaly alert. Each is a one-day build." },
  { title: "The Template Project: Configuration Is the Asset", type: "content", notes: "CLAUDE.md at root: project context, commands, critical patterns, known trade-offs.\n\n.claude/CLAUDE.md: behavioural directives, prohibited patterns, quality gates.\n\nWithout these files: every session starts from zero. With them: every session starts with full context. New team members inherit the AI configuration.\n\nWrite it once. Benefit on every session. Replicate this pattern for FM&I's Dataiku projects, model repositories, shared analysis tooling." },
  { title: "Section Divider: Business Use Cases + Innovation Day", type: "divider", num: "09", sub: "Ideas for the Innovation Day mural board — and beyond" },
  { title: "Business Use Cases: The Hit List", type: "content", notes: "Five categories, twenty-five ideas pre-seeded for Innovation Day.\n\nData and modelling: AI model validator, automatic model card generator, statistical assumption checker.\n\nTrading desk support: market structure briefing agent, request triage agent, curve comparison narrator.\n\nDataiku integration: pipeline health dashboard, data lineage Q&A, schema drift detector.\n\nReporting and visualisation: NL chart generator, automated PowerPoint, report commentary assistant.\n\nProcess automation: meeting action items to Jira, onboarding knowledge base agent, incident response assistant.\n\nNone of these require new infrastructure." },
  { title: "Core Message — Closing Callback", type: "dark", notes: "Ten times.\n\nNot because AI is magic. Because eight hours of routine analytical work compresses to forty-five minutes. Every week. For every analyst on the team.\n\nYou already have the tools. The only thing between you and ten times the productivity is knowing which tool to reach for and when." },
  { title: "Philosophical Anecdotes", type: "dark", notes: "Four things, stated directly.\n\nAI does not make data scientists redundant. It makes the excuse of not having enough time redundant.\n\nThe threat is not to FM&I. It is to the IT middle layer that added value by translating between domain and technology, without deep understanding of either.\n\nWho owns the risk when the AI is wrong? You do. That is an argument for better testing — not less AI.\n\nThe performance art around coding is ending. Requirements ceremonies. Architecture slideware. AI wrappers. When execution is fast and cheap, ceremony becomes conspicuous. The organisations that ship win.\n\n[PAUSE]\n\nFM&I is on the right side of this. Domain experts who command the technical layer. AI makes that combination rarer and more valuable." },
  { title: "Innovation Day: The Mural Board", type: "dark", notes: "Three columns on the Innovation Day mural board.\n\nWhat are you already using? What would save you the most time? What commercial idea would you build?\n\nThree asks: request your GitHub Copilot licence this week. Set up a configuration file in one FM&I project this month. Come to Innovation Day with one commercial idea written down.\n\nThe mural board is live. Add at least one idea before we close." },
  { title: "Closing + Resources", type: "dark", notes: "You already have the tools. Now you know which one to reach for.\n\nGitHub Copilot: raise an IT service desk request this week. M365 Copilot: open Teams right now, look for the Copilot icon. BP AI governance: intranet → 'AI governance'. Template project: link in the session notes.\n\nAny questions?" },
];

remainingSections.forEach(({ title, type, num, sub, notes }) => {
  let s;
  if (type === "divider") {
    s = sectionDivider(pptx, num, title, sub || "");
  } else if (type === "dark") {
    s = darkSlide(pptx);
    addHeadlineDark(s, title);
  } else {
    s = contentSlide(pptx);
    addHeadline(s, title);
  }
  if (notes) s.addNotes(notes);
});

// ─── Export ───────────────────────────────────────────────────────────────────

pptx.writeFile({ fileName: "gen_ai_fmi_presentation.pptx" })
  .then(() => console.log("✅ gen_ai_fmi_presentation.pptx generated successfully."))
  .catch(err => console.error("❌ Error generating PPTX:", err));
