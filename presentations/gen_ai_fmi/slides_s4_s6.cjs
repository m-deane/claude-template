module.exports = function buildS4toS6(pres, C, h) {

  // ============================================================
  // SECTION 4 — GITHUB COPILOT & CURSOR
  // ============================================================

  // ----------------------------------------------------------
  // Slide 15: Section Divider — GitHub Copilot & Cursor
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    // Top accent bar
    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.green },
      line: { color: C.green, width: 0 },
    });

    // Section number
    s.addText("04", {
      x: 0.6, y: 1.2, w: 2, h: 0.8,
      fontFace: "Trebuchet MS",
      fontSize: 48,
      bold: true,
      color: C.green,
      align: "left",
      valign: "middle",
    });

    // Section title
    s.addText("GitHub Copilot \u0026 Cursor", {
      x: 0.6, y: 2.1, w: 8.8, h: 0.65,
      fontFace: "Trebuchet MS",
      fontSize: 32,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    // Section subtitle
    s.addText("Two tools, different strengths \u2014 and workflows that go beyond coding", {
      x: 0.6, y: 2.8, w: 8.8, h: 0.45,
      fontFace: "Calibri",
      fontSize: 14,
      color: C.textLight,
      align: "left",
      valign: "middle",
    });
  }

  // ----------------------------------------------------------
  // Slide 16: GitHub Copilot vs Cursor — The Key Differences
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "TOOLS|COMPARISON", "GitHub Copilot vs Cursor: same category, very different strengths", C.green);

    const cardW = 4.55;
    const cardH = 3.35;
    const cardY = 1.45;

    // --- Left card: GitHub Copilot ---
    h.addCard(s, 0.3, cardY, cardW, cardH, C.white);

    // Top accent bar
    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: cardY, w: cardW, h: 0.05,
      fill: { color: C.blue },
      line: { color: C.blue, width: 0 },
    });

    // Header label
    s.addText("GitHub Copilot", {
      x: 0.45, y: cardY + 0.1, w: cardW - 0.3, h: 0.3,
      fontFace: "Trebuchet MS",
      fontSize: 12,
      bold: true,
      color: C.textDark,
      align: "left",
      valign: "top",
    });

    // Body bullets
    const copilotLines = [
      "\u2022 BP enterprise licence \u2014 easiest to access",
      "\u2022 Deep VS Code \u0026 JetBrains integration",
      "\u2022 Workspace agent: understands your full repo",
      "\u2022 Slash commands: /fix, /explain, /test, /doc",
      "\u2022 CLI integration for terminal workflows",
      "\u2022 Best for: inline suggestions + existing BP stack",
    ];
    s.addText(copilotLines.join("\n"), {
      x: 0.45, y: cardY + 0.5, w: cardW - 0.3, h: cardH - 0.65,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.textMed,
      align: "left",
      valign: "top",
      wrap: true,
    });

    // --- Right card: Cursor ---
    h.addCard(s, 5.1, cardY, cardW, cardH, C.white);

    // Top accent bar
    s.addShape(pres.ShapeType.rect, {
      x: 5.1, y: cardY, w: cardW, h: 0.05,
      fill: { color: C.green },
      line: { color: C.green, width: 0 },
    });

    // Header label
    s.addText("Cursor", {
      x: 5.25, y: cardY + 0.1, w: cardW - 0.3, h: 0.3,
      fontFace: "Trebuchet MS",
      fontSize: 12,
      bold: true,
      color: C.textDark,
      align: "left",
      valign: "top",
    });

    // Body bullets
    const cursorLines = [
      "\u2022 Standalone IDE (fork of VS Code)",
      "\u2022 Full codebase context in every conversation",
      "\u2022 Background agents + git worktrees (parallel)",
      "\u2022 Multi-agent orchestration for complex tasks",
      "\u2022 .cursorrules for project-level AI instructions",
      "\u2022 Best for: large codebase work + complex builds",
    ];
    s.addText(cursorLines.join("\n"), {
      x: 5.25, y: cardY + 0.5, w: cardW - 0.3, h: cardH - 0.65,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.textMed,
      align: "left",
      valign: "top",
      wrap: true,
    });

    h.bottomBar(s, "Use GitHub Copilot for day-to-day inline work in your existing IDE; use Cursor when the task spans multiple files or requires autonomous execution");
  }

  // ----------------------------------------------------------
  // Slide 17: [LIVE DEMO] See It In Action — GitHub Copilot
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "GITHUB COPILOT|SEE IT IN ACTION", "[LIVE DEMO] Dataiku recipe timeout \u2014 debugged in 20 minutes", C.green);

    // Dark header bar — "The prompt you type:"
    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 1.45, w: 9.4, h: 0.3,
      fill: { color: "1E293B" },
      line: { color: "1E293B", width: 0 },
    });
    s.addText("The prompt you type:", {
      x: 0.4, y: 1.45, w: 9.2, h: 0.3,
      fontFace: "Calibri",
      fontSize: 9,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    // Terminal panel
    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 1.78, w: 9.4, h: 0.55,
      fill: { color: "1A1A2E" },
      line: { color: "1A1A2E", width: 0 },
    });
    s.addText(
      "This Dataiku recipe is timing out on 500k rows. Identify the bottleneck and rewrite the aggregation logic using vectorised operations.",
      {
        x: 0.45, y: 1.8, w: 9.1, h: 0.51,
        fontFace: "Courier New",
        fontSize: 9,
        color: C.teal,
        align: "left",
        valign: "middle",
        wrap: true,
      }
    );

    // Left panel card
    h.addCard(s, 0.3, 2.45, 5.8, 2.35, C.white);

    // Left panel header bar
    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 2.45, w: 5.8, h: 0.28,
      fill: { color: C.green },
      line: { color: C.green, width: 0 },
    });
    s.addText("What happens:", {
      x: 0.4, y: 2.45, w: 5.6, h: 0.28,
      fontFace: "Trebuchet MS",
      fontSize: 10,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    const copilotSteps = [
      "1. Copilot reads the full recipe and diagnoses the slow loop",
      "2. Identifies the iterrows() anti-pattern on line 47",
      "3. Rewrites using pandas vectorised operations",
      "4. Adds a docstring explaining the optimisation",
      "5. Suggests unit tests for the refactored function",
    ];
    s.addText(copilotSteps.join("\n"), {
      x: 0.45, y: 2.8, w: 5.5, h: 1.85,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.textMed,
      align: "left",
      valign: "top",
      wrap: true,
    });

    // Right panel card
    h.addCard(s, 6.25, 2.45, 3.45, 2.35, C.white);

    // Big number
    s.addText("20 min", {
      x: 6.35, y: 2.55, w: 3.25, h: 0.6,
      fontFace: "Trebuchet MS",
      fontSize: 36,
      bold: true,
      color: C.green,
      align: "center",
      valign: "middle",
    });

    // Label under big number
    s.addText("from timeout to optimised, tested recipe", {
      x: 6.35, y: 3.2, w: 3.25, h: 0.3,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.textMed,
      align: "center",
      valign: "middle",
    });

    // Manual comparison
    s.addText("Manual: 3\u20134 hours", {
      x: 6.35, y: 3.6, w: 3.25, h: 0.3,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.red,
      align: "center",
      valign: "middle",
    });

    h.bottomBar(s, "[PRESENTER: open VS Code with the demo recipe now] \u2014 the 3-4 hour debug cycle just became a 20-minute review cycle");
  }

  // ----------------------------------------------------------
  // Slide 18: [LIVE DEMO] See It In Action — Cursor
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "CURSOR|SEE IT IN ACTION", "[LIVE DEMO] Prompt to working Dash app \u2014 12 minutes", C.green);

    // Dark header bar — "The prompt you type:"
    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 1.45, w: 9.4, h: 0.3,
      fill: { color: "1E293B" },
      line: { color: "1E293B", width: 0 },
    });
    s.addText("The prompt you type:", {
      x: 0.4, y: 1.45, w: 9.2, h: 0.3,
      fontFace: "Calibri",
      fontSize: 9,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    // Terminal panel
    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 1.78, w: 9.4, h: 0.55,
      fill: { color: "1A1A2E" },
      line: { color: "1A1A2E", width: 0 },
    });
    s.addText(
      "Build a Plotly Dash app showing crack spread evolution for Q1 2025. Read from crack_spreads.csv, add a 30-day rolling average, and deploy locally on port 8050.",
      {
        x: 0.45, y: 1.8, w: 9.1, h: 0.51,
        fontFace: "Courier New",
        fontSize: 9,
        color: C.teal,
        align: "left",
        valign: "middle",
        wrap: true,
      }
    );

    // Left panel card
    h.addCard(s, 0.3, 2.45, 5.8, 2.35, C.white);

    // Left panel header bar
    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 2.45, w: 5.8, h: 0.28,
      fill: { color: C.green },
      line: { color: C.green, width: 0 },
    });
    s.addText("What happens:", {
      x: 0.4, y: 2.45, w: 5.6, h: 0.28,
      fontFace: "Trebuchet MS",
      fontSize: 10,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    const cursorSteps = [
      "1. Cursor reads crack_spreads.csv and understands the schema",
      "2. Writes the full Dash layout with Plotly charts",
      "3. Implements rolling average calculation",
      "4. Adds date range picker and commodity selector",
      "5. Runs app locally \u2014 browser opens automatically",
    ];
    s.addText(cursorSteps.join("\n"), {
      x: 0.45, y: 2.8, w: 5.5, h: 1.85,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.textMed,
      align: "left",
      valign: "top",
      wrap: true,
    });

    // Right panel card
    h.addCard(s, 6.25, 2.45, 3.45, 2.35, C.white);

    // Big number
    s.addText("12 min", {
      x: 6.35, y: 2.55, w: 3.25, h: 0.6,
      fontFace: "Trebuchet MS",
      fontSize: 36,
      bold: true,
      color: C.green,
      align: "center",
      valign: "middle",
    });

    // Label under big number
    s.addText("from prompt to interactive app running in browser", {
      x: 6.35, y: 3.2, w: 3.25, h: 0.3,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.textMed,
      align: "center",
      valign: "middle",
    });

    // Manual comparison
    s.addText("Manual: 2\u20133 days", {
      x: 6.35, y: 3.6, w: 3.25, h: 0.3,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.red,
      align: "center",
      valign: "middle",
    });

    h.bottomBar(s, "[PRESENTER: run this live now] \u2014 this is the \u2018hours to minutes\u2019 shift that changes how quickly FM\u0026I can respond to desk requests");
  }

  // ----------------------------------------------------------
  // Slide 19: Ask, Agent, Plan — Three Modes, Three Use Cases
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "TOOLS|MODES", "Three modes: match the mode to the task complexity", C.green);

    const modes = [
      {
        x: 0.3,
        accentColor: C.cyan,
        badgeColor: C.cyan,
        badgeText: "QUICK",
        title: "Ask",
        body: "One-turn Q\u0026A. Ask a question, get an answer.\n\nBest for: \u2018What does this function do?\u2019, \u2018Why is this query slow?\u2019, \u2018How do I join these DataFrames?\u2019",
      },
      {
        x: 3.4,
        accentColor: C.blue,
        badgeColor: C.blue,
        badgeText: "COMPLEX",
        title: "Agent",
        body: "Multi-step autonomous execution. Give a goal, the agent plans and executes.\n\nBest for: building a feature, debugging a pipeline, writing and running tests.",
      },
      {
        x: 6.5,
        accentColor: C.purple,
        badgeColor: C.purple,
        badgeText: "SAFE",
        title: "Plan",
        body: "Show the plan before executing. Review and approve each step.\n\nBest for: destructive operations, unfamiliar codebases, tasks where you want to stay in control.",
      },
    ];

    const cardW = 2.9;
    const cardH = 2.65;
    const cardY = 1.55;

    modes.forEach(function(mode) {
      // Card background
      h.addCard(s, mode.x, cardY, cardW, cardH, C.white);

      // Top accent bar
      s.addShape(pres.ShapeType.rect, {
        x: mode.x, y: cardY, w: cardW, h: 0.05,
        fill: { color: mode.accentColor },
        line: { color: mode.accentColor, width: 0 },
      });

      // Badge (top-right of card)
      s.addShape(pres.ShapeType.rect, {
        x: mode.x + cardW - 0.65, y: cardY + 0.1, w: 0.58, h: 0.22,
        fill: { color: mode.badgeColor },
        line: { color: mode.badgeColor, width: 0 },
      });
      s.addText(mode.badgeText, {
        x: mode.x + cardW - 0.65, y: cardY + 0.1, w: 0.58, h: 0.22,
        fontFace: "Trebuchet MS",
        fontSize: 7,
        bold: true,
        color: C.white,
        align: "center",
        valign: "middle",
      });

      // Card title
      s.addText(mode.title, {
        x: mode.x + 0.15, y: cardY + 0.13, w: cardW - 0.85, h: 0.3,
        fontFace: "Trebuchet MS",
        fontSize: 13,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      // Card body
      s.addText(mode.body, {
        x: mode.x + 0.15, y: cardY + 0.52, w: cardW - 0.3, h: cardH - 0.68,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });
    });

    h.bottomBar(s, "Default to Ask for questions, Agent for tasks, Plan when the stakes are high \u2014 this single habit change 3\u00d7 the value of either tool");
  }

  // ----------------------------------------------------------
  // Slide 20: Prompting — How to Get Consistent, High-Quality Output
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "TOOLS|PROMPTING", "Better prompts = better output \u2014 here\u2019s the formula", C.green);

    const promptCards = [
      {
        title: "Be specific about context",
        body: "Include: what language/framework, what the data looks like, what the expected output is. Generic prompts produce generic code.",
      },
      {
        title: "State constraints explicitly",
        body: "e.g. \u2018use pandas not polars\u2019, \u2018must run in Dataiku\u2019, \u2018output must be a dictionary not a DataFrame\u2019",
      },
      {
        title: "Use the LLM to improve your prompt",
        body: "Type your rough prompt, then: \u2018Rewrite this prompt to be clearer and more likely to produce the output I need.\u2019",
      },
      {
        title: "Template your common prompts",
        body: "Store your best prompts in .cursorrules or .github/copilot-instructions.md \u2014 they become project-level context",
      },
    ];

    const leftX = 0.3;
    const leftW = 4.5;
    const pCardH = 0.75;
    const pCardGap = 0.08;
    let pCardY = 1.45;

    promptCards.forEach(function(card) {
      h.addCard(s, leftX, pCardY, leftW, pCardH, C.white);

      // Left accent bar
      s.addShape(pres.ShapeType.rect, {
        x: leftX, y: pCardY, w: 0.05, h: pCardH,
        fill: { color: C.green },
        line: { color: C.green, width: 0 },
      });

      // Title
      s.addText(card.title, {
        x: leftX + 0.15, y: pCardY + 0.05, w: leftW - 0.2, h: 0.24,
        fontFace: "Trebuchet MS",
        fontSize: 9.5,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      // Body
      s.addText(card.body, {
        x: leftX + 0.15, y: pCardY + 0.3, w: leftW - 0.2, h: 0.38,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });

      pCardY += pCardH + pCardGap;
    });

    // Right side — terminal card
    const rightX = 5.1;
    const rightW = 4.6;
    const rightH = 3.3;

    s.addShape(pres.ShapeType.rect, {
      x: rightX, y: 1.45, w: rightW, h: rightH,
      fill: { color: "1A1A2E" },
      line: { color: "1A1A2E", width: 0 },
    });

    // Header row within terminal card
    s.addShape(pres.ShapeType.rect, {
      x: rightX, y: 1.45, w: rightW, h: 0.32,
      fill: { color: "2D3748" },
      line: { color: "2D3748", width: 0 },
    });
    s.addText("Template: FM\u0026I prompt structure", {
      x: rightX + 0.15, y: 1.45, w: rightW - 0.3, h: 0.32,
      fontFace: "Trebuchet MS",
      fontSize: 9,
      bold: true,
      color: C.textLight,
      align: "left",
      valign: "middle",
    });

    // Template body
    const templateLines = [
      "Context: [what the code does / data looks like]",
      "",
      "Task: [specific action to perform]",
      "",
      "Constraints: [language, framework, output format]",
      "",
      "Example: [if helpful]",
    ];
    s.addText(templateLines.join("\n"), {
      x: rightX + 0.2, y: 1.85, w: rightW - 0.4, h: rightH - 0.5,
      fontFace: "Courier New",
      fontSize: 8.5,
      color: C.teal,
      align: "left",
      valign: "top",
      wrap: true,
    });

    h.bottomBar(s, "The _p-presentation-creator repo is a live example of this: CLAUDE.md + agents + skills = consistent AI output on every run");
  }

  // ----------------------------------------------------------
  // Slide 21: GitHub Copilot & Cursor Roadmap — 2026
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "TOOLS|ROADMAP", "Both tools are shipping major capability upgrades in 2026", C.green);

    const cardW = 4.55;
    const cardH = 3.35;
    const cardY = 1.45;

    // --- Left card: GitHub Copilot 2026 ---
    h.addCard(s, 0.3, cardY, cardW, cardH, C.white);

    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: cardY, w: cardW, h: 0.32,
      fill: { color: C.blue },
      line: { color: C.blue, width: 0 },
    });
    s.addText("GitHub Copilot 2026", {
      x: 0.45, y: cardY, w: cardW - 0.3, h: 0.32,
      fontFace: "Trebuchet MS",
      fontSize: 11,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    const copilotRoadmap = [
      { q: "Q1:", desc: "Copilot Extensions \u2014 connect to external services via tool calling" },
      { q: "Q2:", desc: "Copilot for CLI GA \u2014 natural language terminal commands" },
      { q: "Q3:", desc: "Multi-file autonomous edits without manual approval" },
      { q: "Q4:", desc: "Integrated code review agent \u2014 flags issues before PR" },
    ];

    let rmY = cardY + 0.42;
    copilotRoadmap.forEach(function(item) {
      s.addText(item.q, {
        x: 0.45, y: rmY, w: 0.4, h: 0.52,
        fontFace: "Trebuchet MS",
        fontSize: 9,
        bold: true,
        color: C.blue,
        align: "left",
        valign: "top",
      });
      s.addText(item.desc, {
        x: 0.88, y: rmY, w: cardW - 0.65, h: 0.52,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });
      rmY += 0.62;
    });

    // --- Right card: Cursor 2026 ---
    h.addCard(s, 5.1, cardY, cardW, cardH, C.white);

    s.addShape(pres.ShapeType.rect, {
      x: 5.1, y: cardY, w: cardW, h: 0.32,
      fill: { color: C.green },
      line: { color: C.green, width: 0 },
    });
    s.addText("Cursor 2026", {
      x: 5.25, y: cardY, w: cardW - 0.3, h: 0.32,
      fontFace: "Trebuchet MS",
      fontSize: 11,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    const cursorRoadmap = [
      { q: "Q1:", desc: "Cursor Teams \u2014 shared .cursorrules and agent coordination" },
      { q: "Q2:", desc: "Background agents on cloud \u2014 run overnight tasks without keeping IDE open" },
      { q: "Q3:", desc: "Integrated test runner \u2014 agent writes and validates tests in one loop" },
      { q: "Q4:", desc: "Cursor for notebooks \u2014 full Jupyter support with agent mode" },
    ];

    let crY = cardY + 0.42;
    cursorRoadmap.forEach(function(item) {
      s.addText(item.q, {
        x: 5.25, y: crY, w: 0.4, h: 0.52,
        fontFace: "Trebuchet MS",
        fontSize: 9,
        bold: true,
        color: C.green,
        align: "left",
        valign: "top",
      });
      s.addText(item.desc, {
        x: 5.68, y: crY, w: cardW - 0.65, h: 0.52,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });
      crY += 0.62;
    });

    h.bottomBar(s, "Cursor\u2019s cloud background agents (Q2) + GitHub Copilot\u2019s extension ecosystem (Q1) are the two near-term features most relevant to FM\u0026I workflows");
  }

  // ============================================================
  // SECTION 5 — MODEL LANDSCAPE
  // ============================================================

  // ----------------------------------------------------------
  // Slide 22: Section Divider — The Model Landscape
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    // Top accent bar
    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.purple },
      line: { color: C.purple, width: 0 },
    });

    // Section number
    s.addText("05", {
      x: 0.6, y: 1.2, w: 2, h: 0.8,
      fontFace: "Trebuchet MS",
      fontSize: 48,
      bold: true,
      color: C.purple,
      align: "left",
      valign: "middle",
    });

    // Section title
    s.addText("The Model Landscape", {
      x: 0.6, y: 2.1, w: 8.8, h: 0.65,
      fontFace: "Trebuchet MS",
      fontSize: 32,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    // Section subtitle
    s.addText("12 months of capability jumps \u2014 and how to choose the right model", {
      x: 0.6, y: 2.8, w: 8.8, h: 0.45,
      fontFace: "Calibri",
      fontSize: 14,
      color: C.textLight,
      align: "left",
      valign: "middle",
    });
  }

  // ----------------------------------------------------------
  // Slide 23: 12 Months of Capability Jumps
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "MODELS|TIMELINE", "The models you knew a year ago are not the models available today", C.purple);

    const milestones = [
      {
        date: "Mar 2025",
        desc: "GPT-4o \u2014 128k context, voice mode, multimodal reasoning",
        color: C.blue,
      },
      {
        date: "May 2025",
        desc: "Claude 3.7 \u2014 extended thinking, 200k context, best coding benchmark",
        color: C.teal,
      },
      {
        date: "Jul 2025",
        desc: "Gemini 1.5 Pro \u2014 1M context window, multimodal, YouTube/Drive native",
        color: C.green,
      },
      {
        date: "Sep 2025",
        desc: "Llama 3.1 405B \u2014 open source, runs locally, near-frontier performance",
        color: C.orange,
      },
      {
        date: "Nov 2025",
        desc: "o3-mini \u2014 OpenAI reasoning model, 3\u00d7 cheaper than GPT-4o for code",
        color: C.red,
      },
      {
        date: "Jan 2026",
        desc: "Claude 4.6 Opus/Sonnet \u2014 agentic multi-step, tool calling, extended context",
        color: C.purple,
      },
    ];

    const timelineY = 2.1;
    const totalW = 9.4;
    const startX = 0.3;
    const slotW = totalW / milestones.length;
    const dotSize = 0.16;

    // Horizontal connecting line
    s.addShape(pres.ShapeType.rect, {
      x: startX, y: timelineY + 0.05, w: totalW, h: 0.03,
      fill: { color: C.divider },
      line: { color: C.divider, width: 0 },
    });

    milestones.forEach(function(m, i) {
      const cx = startX + i * slotW + slotW / 2;

      // Milestone dot
      s.addShape(pres.ShapeType.rect, {
        x: cx - dotSize / 2, y: timelineY,
        w: dotSize, h: dotSize,
        fill: { color: m.color },
        line: { color: m.color, width: 0 },
      });

      // Date label
      s.addText(m.date, {
        x: cx - slotW / 2 + 0.05, y: timelineY + 0.22,
        w: slotW - 0.1, h: 0.22,
        fontFace: "Calibri",
        fontSize: 8,
        bold: true,
        color: m.color,
        align: "center",
        valign: "top",
      });

      // Description
      s.addText(m.desc, {
        x: cx - slotW / 2 + 0.05, y: timelineY + 0.46,
        w: slotW - 0.1, h: 0.75,
        fontFace: "Calibri",
        fontSize: 7.5,
        color: C.textMed,
        align: "center",
        valign: "top",
        wrap: true,
      });
    });

    h.bottomBar(s, "Context windows grew 10\u00d7, reasoning improved dramatically, and local models hit near-frontier quality \u2014 the landscape shifted faster than most teams noticed");
  }

  // ----------------------------------------------------------
  // Slide 24: Model Comparison — Strengths and Best Use Cases
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "MODELS|COMPARISON", "Different models excel at different tasks \u2014 here is the map", C.purple);

    const modelCards = [
      {
        x: 0.3, y: 1.45,
        accentColor: C.teal,
        title: "Claude 4.6 Opus",
        body: "Best for: complex multi-step agentic tasks, long document analysis, precise instruction following.\nContext: 200k\nPrice: $$$$",
      },
      {
        x: 3.4, y: 1.45,
        accentColor: C.cyan,
        title: "Claude 4.6 Sonnet",
        body: "Best for: coding tasks, balanced quality + speed. 80% of Opus quality at 20% of the cost. The daily driver for most tasks.\nPrice: $$",
      },
      {
        x: 6.5, y: 1.45,
        accentColor: C.blue,
        title: "GPT-4o / o3",
        body: "Best for: data analysis with Code Interpreter, multimodal tasks, OpenAI ecosystem. o3 excels at math and reasoning.\nPrice: $$$",
      },
      {
        x: 0.3, y: 3.35,
        accentColor: C.green,
        title: "Gemini 2.0 Pro",
        body: "Best for: 1M token context, Google Workspace integration, YouTube and video analysis. Fast and cheap for long-context tasks.\nPrice: $$",
      },
      {
        x: 3.4, y: 3.35,
        accentColor: C.orange,
        title: "Ollama (local)",
        body: "Best for: sensitive data (stays on your machine), offline use, high-volume low-stakes tasks. Llama 3.1, Mistral, Phi.\nPrice: FREE",
      },
    ];

    const cardW = 2.9;
    const cardH = 1.75;

    modelCards.forEach(function(card) {
      h.addCard(s, card.x, card.y, cardW, cardH, C.white);

      // Top accent bar
      s.addShape(pres.ShapeType.rect, {
        x: card.x, y: card.y, w: cardW, h: 0.05,
        fill: { color: card.accentColor },
        line: { color: card.accentColor, width: 0 },
      });

      // Title
      s.addText(card.title, {
        x: card.x + 0.15, y: card.y + 0.1, w: cardW - 0.3, h: 0.28,
        fontFace: "Trebuchet MS",
        fontSize: 10,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      // Body
      s.addText(card.body, {
        x: card.x + 0.15, y: card.y + 0.42, w: cardW - 0.3, h: cardH - 0.55,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });
    });

    h.bottomBar(s, "For FM\u0026I: Claude Sonnet for most coding tasks, Ollama for anything involving position data or proprietary model IP that cannot leave the machine");
  }

  // ----------------------------------------------------------
  // Slide 25: Which Model for Which Task — Decision Framework
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "MODELS|DECISION", "A simple decision framework for model selection", C.purple);

    const decisionCards = [
      {
        question: "Q1: Does the task involve sensitive/proprietary data (positions, live trades, model IP)?",
        yesLabel: "Yes \u2192",
        yesAnswer: "Use Ollama locally",
        yesBadgeColor: C.orange,
        noLabel: "No \u2192",
        noAnswer: "proceed to next question",
      },
      {
        question: "Q2: Is this a one-off task or part of an automated pipeline?",
        yesLabel: "Pipeline \u2192",
        yesAnswer: "Use Claude Sonnet (API) \u2014 predictable, fast, cost-effective",
        yesBadgeColor: C.cyan,
        noLabel: "One-off \u2192",
        noAnswer: "proceed to next question",
      },
      {
        question: "Q3: Does it require reasoning over a very long document (>50 pages) or multi-step planning?",
        yesLabel: "Yes \u2192",
        yesAnswer: "Use Claude Opus or Gemini 2.0 Pro",
        yesBadgeColor: C.teal,
        noLabel: "No \u2192",
        noAnswer: "Claude Sonnet or GPT-4o \u2014 both excellent",
      },
    ];

    const leftX = 0.3;
    const leftW = 6.2;
    const dCardH = 0.9;
    const dCardGap = 0.1;
    let dCardY = 1.45;

    decisionCards.forEach(function(card) {
      h.addCard(s, leftX, dCardY, leftW, dCardH, C.white);

      // Left accent bar
      s.addShape(pres.ShapeType.rect, {
        x: leftX, y: dCardY, w: 0.05, h: dCardH,
        fill: { color: C.purple },
        line: { color: C.purple, width: 0 },
      });

      // Question text
      s.addText(card.question, {
        x: leftX + 0.15, y: dCardY + 0.05, w: leftW - 0.25, h: 0.3,
        fontFace: "Trebuchet MS",
        fontSize: 9,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
        wrap: true,
      });

      // Yes path
      s.addText(card.yesLabel, {
        x: leftX + 0.15, y: dCardY + 0.42, w: 0.8, h: 0.25,
        fontFace: "Calibri",
        fontSize: 8.5,
        bold: true,
        color: card.yesBadgeColor,
        align: "left",
        valign: "top",
      });
      s.addText(card.yesAnswer, {
        x: leftX + 0.95, y: dCardY + 0.42, w: (leftW - 1.1) / 2, h: 0.25,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textDark,
        align: "left",
        valign: "top",
        wrap: true,
      });

      // No path
      s.addText(card.noLabel, {
        x: leftX + 0.15 + (leftW - 0.25) / 2, y: dCardY + 0.42, w: 0.8, h: 0.25,
        fontFace: "Calibri",
        fontSize: 8.5,
        bold: true,
        color: C.textMed,
        align: "left",
        valign: "top",
      });
      s.addText(card.noAnswer, {
        x: leftX + 0.15 + (leftW - 0.25) / 2 + 0.8, y: dCardY + 0.42, w: (leftW - 1.1) / 2 - 0.15, h: 0.25,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });

      dCardY += dCardH + dCardGap;
    });

    // Cost reference box
    const costX = 6.8;
    const costW = 2.9;
    const costH = 3.3;
    h.addCard(s, costX, 1.45, costW, costH, C.lightBlue);

    s.addText("Rough cost per 1M tokens", {
      x: costX + 0.15, y: 1.55, w: costW - 0.3, h: 0.3,
      fontFace: "Trebuchet MS",
      fontSize: 9,
      bold: true,
      color: C.textDark,
      align: "left",
      valign: "top",
    });

    const costLines = [
      "Opus:         ~$15",
      "Sonnet:       ~$3",
      "GPT-4o:       ~$5",
      "Gemini Pro:   ~$1.25",
      "Ollama:       $0",
    ];
    s.addText(costLines.join("\n"), {
      x: costX + 0.15, y: 1.95, w: costW - 0.3, h: 2.6,
      fontFace: "Courier New",
      fontSize: 9,
      color: C.textDark,
      align: "left",
      valign: "top",
      wrap: false,
    });

    h.bottomBar(s, "Default to Claude Sonnet for 80% of FM\u0026I tasks \u2014 only upgrade to Opus when the task genuinely demands multi-step reasoning over large context");
  }

  // ============================================================
  // SECTION 6 — ETHICS & COMPLIANCE
  // ============================================================

  // ----------------------------------------------------------
  // Slide 26: Section Divider — Ethics & Compliance
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    // Top accent bar
    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.orange },
      line: { color: C.orange, width: 0 },
    });

    // Section number
    s.addText("06", {
      x: 0.6, y: 1.2, w: 2, h: 0.8,
      fontFace: "Trebuchet MS",
      fontSize: 48,
      bold: true,
      color: C.orange,
      align: "left",
      valign: "middle",
    });

    // Section title
    s.addText("Ethics \u0026 Compliance", {
      x: 0.6, y: 2.1, w: 8.8, h: 0.65,
      fontFace: "Trebuchet MS",
      fontSize: 32,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    // Section subtitle
    s.addText("What data can go in, what can\u2019t, and the 5 rules for safe use in FM\u0026I", {
      x: 0.6, y: 2.8, w: 8.8, h: 0.45,
      fontFace: "Calibri",
      fontSize: 14,
      color: C.textLight,
      align: "left",
      valign: "middle",
    });
  }

  // ----------------------------------------------------------
  // Slide 27: What Data Can and Cannot Go Into These Tools
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "COMPLIANCE|DATA RULES", "The data boundary is the most important thing in this session", C.orange);

    const cardW = 4.55;
    const cardH = 3.35;
    const cardY = 1.45;

    // --- Left card: SAFE TO USE ---
    h.addCard(s, 0.3, cardY, cardW, cardH, C.white);

    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: cardY, w: cardW, h: 0.05,
      fill: { color: C.green },
      line: { color: C.green, width: 0 },
    });

    s.addText("\u2713 SAFE TO USE", {
      x: 0.45, y: cardY + 0.1, w: cardW - 0.3, h: 0.3,
      fontFace: "Trebuchet MS",
      fontSize: 11,
      bold: true,
      color: C.green,
      align: "left",
      valign: "top",
    });

    const safeLines = [
      "\u2022 Open-source code and generic scripts",
      "\u2022 Anonymised sample data (no positions, no counterparty names)",
      "\u2022 Public research, academic papers",
      "\u2022 Internal documentation (non-sensitive)",
      "\u2022 Aggregated market data (already public)",
      "\u2022 Code logic questions without real values",
    ];
    s.addText(safeLines.join("\n"), {
      x: 0.45, y: cardY + 0.5, w: cardW - 0.3, h: cardH - 0.65,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.textDark,
      align: "left",
      valign: "top",
      wrap: true,
    });

    // --- Right card: NEVER INPUT ---
    h.addCard(s, 5.1, cardY, cardW, cardH, C.white);

    s.addShape(pres.ShapeType.rect, {
      x: 5.1, y: cardY, w: cardW, h: 0.05,
      fill: { color: C.red },
      line: { color: C.red, width: 0 },
    });

    s.addText("\u2717 NEVER INPUT", {
      x: 5.25, y: cardY + 0.1, w: cardW - 0.3, h: 0.3,
      fontFace: "Trebuchet MS",
      fontSize: 11,
      bold: true,
      color: C.red,
      align: "left",
      valign: "top",
    });

    const neverLines = [
      "\u2022 Live positions or trading exposures",
      "\u2022 Counterparty names or deal terms",
      "\u2022 Proprietary fundamental model logic or IP",
      "\u2022 Unpublished price forecasts",
      "\u2022 Personal data of any kind",
      "\u2022 Anything marked CONFIDENTIAL or RESTRICTED",
    ];
    s.addText(neverLines.join("\n"), {
      x: 5.25, y: cardY + 0.5, w: cardW - 0.3, h: cardH - 0.65,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.textDark,
      align: "left",
      valign: "top",
      wrap: true,
    });

    h.bottomBar(s, "Rule of thumb: if you would not paste it into a public Slack channel, do not paste it into an AI tool you do not control");
  }

  // ----------------------------------------------------------
  // Slide 28: 5 Rules for Safe Gen AI Use in FM&I
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "COMPLIANCE|FM\u0026I RULES", "Five rules cover 95% of situations \u2014 memorise these", C.orange);

    const rules = [
      {
        num: "Rule 1",
        body: "Anonymise before you paste \u2014 replace position sizes, counterparty names, and model outputs with placeholders before sharing with any AI tool",
      },
      {
        num: "Rule 2",
        body: "M365 Copilot = safer for internal content \u2014 Microsoft\u2019s enterprise agreement covers BP data; external tools (Cursor, Claude.ai) do not have the same contractual protection",
      },
      {
        num: "Rule 3",
        body: "Code \u2260 data \u2014 pasting code logic is generally safe; pasting the actual data the code runs on may not be",
      },
      {
        num: "Rule 4",
        body: "Check before you use \u2014 if you\u2019re unsure whether a specific use case is allowed, ask the Digital Centre of Excellence before using the tool, not after",
      },
      {
        num: "Rule 5",
        body: "You own the output \u2014 AI-generated code or analysis must be reviewed and validated by you. It is not self-validating.",
      },
    ];

    const ruleW = 9.4;
    const ruleH = 0.62;
    const ruleGap = 0.08;
    let ruleY = 1.45;

    rules.forEach(function(rule) {
      h.addCard(s, 0.3, ruleY, ruleW, ruleH, C.white);

      // Left accent bar
      s.addShape(pres.ShapeType.rect, {
        x: 0.3, y: ruleY, w: 0.05, h: ruleH,
        fill: { color: C.orange },
        line: { color: C.orange, width: 0 },
      });

      // Rule number label
      s.addText(rule.num, {
        x: 0.45, y: ruleY + 0.06, w: 0.75, h: ruleH - 0.12,
        fontFace: "Trebuchet MS",
        fontSize: 9,
        bold: true,
        color: C.orange,
        align: "left",
        valign: "middle",
      });

      // Rule body
      s.addText(rule.body, {
        x: 1.22, y: ruleY + 0.06, w: ruleW - 1.0, h: ruleH - 0.12,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textDark,
        align: "left",
        valign: "middle",
        wrap: true,
      });

      ruleY += ruleH + ruleGap;
    });

    h.bottomBar(s, "Current BP AI guidance: intranet \u2192 \u2018Digital Tools\u2019 \u2192 \u2018AI Governance\u2019 \u2014 the Digital Centre of Excellence is the point of contact for questions");
  }

  // ----------------------------------------------------------
  // Slide 29: M365 Copilot vs External Tools — Data Handling
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "COMPLIANCE|DATA HANDLING", "Not all AI tools handle your data the same way", C.orange);

    const cardW = 4.55;
    const cardH = 3.35;
    const cardY = 1.45;

    // --- Left card: Microsoft Copilot (M365) ---
    h.addCard(s, 0.3, cardY, cardW, cardH, C.white);

    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: cardY, w: cardW, h: 0.32,
      fill: { color: C.blue },
      line: { color: C.blue, width: 0 },
    });
    s.addText("Microsoft Copilot (M365)", {
      x: 0.45, y: cardY, w: cardW - 0.3, h: 0.32,
      fontFace: "Trebuchet MS",
      fontSize: 11,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    const m365Lines = [
      "\u2022 Data stays within BP\u2019s Microsoft tenant",
      "\u2022 Covered by enterprise data processing agreement",
      "\u2022 Not used to train Microsoft\u2019s models",
      "\u2022 Audit logs available to IT administrators",
      "\u2022 Appropriate for internal BP content",
    ];
    s.addText(m365Lines.join("\n"), {
      x: 0.45, y: cardY + 0.42, w: cardW - 0.3, h: cardH - 0.55,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.textDark,
      align: "left",
      valign: "top",
      wrap: true,
    });

    // --- Right card: External Tools ---
    h.addCard(s, 5.1, cardY, cardW, cardH, C.white);

    s.addShape(pres.ShapeType.rect, {
      x: 5.1, y: cardY, w: cardW, h: 0.32,
      fill: { color: C.orange },
      line: { color: C.orange, width: 0 },
    });
    s.addText("External Tools (Cursor, Claude.ai, ChatGPT)", {
      x: 5.25, y: cardY, w: cardW - 0.3, h: 0.32,
      fontFace: "Trebuchet MS",
      fontSize: 10,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    const externalLines = [
      "\u2022 Data sent to third-party servers",
      "\u2022 Covered by individual terms of service only",
      "\u2022 Training data opt-out varies by tool and plan",
      "\u2022 No BP enterprise data processing agreement by default",
      "\u2022 Use for code logic and public information only",
    ];
    s.addText(externalLines.join("\n"), {
      x: 5.25, y: cardY + 0.42, w: cardW - 0.3, h: cardH - 1.05,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.textDark,
      align: "left",
      valign: "top",
      wrap: true,
    });

    // Note at bottom of right card
    s.addText(
      "Note: API-based access (e.g. via Claude API key) has stronger data handling terms \u2014 check current BP guidance for API use status",
      {
        x: 5.25, y: cardY + 2.5, w: cardW - 0.3, h: 0.7,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
        italic: true,
      }
    );

    h.bottomBar(s, "Default to M365 Copilot for anything involving internal BP content; use external tools only for code logic and publicly available information");
  }

};
