// slides_s4_s6_v5.cjs
// v5 changes: 3 new slides after Slide 21 — Dataiku Copilot setup, Dataiku Cursor setup, Before/After prompts

module.exports = function buildS4toS6(pres, C, h) {

  // ============================================================
  // SECTION 4 — GITHUB COPILOT & CURSOR
  // ============================================================

  // ----------------------------------------------------------
  // Slide 16: Section Divider — GitHub Copilot & Cursor
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.green },
      line: { color: C.green, width: 0 },
    });

    s.addText("04", {
      x: 0.6, y: 1.2, w: 2, h: 0.8,
      fontFace: "Trebuchet MS",
      fontSize: 48,
      bold: true,
      color: C.green,
      align: "left",
      valign: "middle",
    });

    s.addText("GitHub Copilot \u0026 Cursor", {
      x: 0.6, y: 2.1, w: 8.8, h: 0.65,
      fontFace: "Trebuchet MS",
      fontSize: 32,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

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
  // Slide 17: Same Category, Very Different Strengths
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "TOOLS|COMPARISON", "GitHub Copilot vs Cursor: same category, very different strengths", C.green);

    const cardW = 4.55;
    const cardH = 3.35;
    const cardY = 1.45;

    // Left card — GitHub Copilot
    h.addCard(s, 0.3, cardY, cardW, cardH, C.white);

    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: cardY, w: cardW, h: 0.32,
      fill: { color: C.blue },
      line: { color: C.blue, width: 0 },
    });
    s.addText("GitHub Copilot", {
      x: 0.45, y: cardY, w: cardW - 0.3, h: 0.32,
      fontFace: "Trebuchet MS",
      fontSize: 12,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    s.addText(
      "BP enterprise licence makes this the zero-friction choice \u2014 request it, get it in 2 days, use it in the IDE you already have. The @workspace agent indexes your entire Dataiku project and can answer architecture questions across files. Slash commands (/fix, /explain, /test, /doc) cover 80% of daily coding tasks.\n\nWhat \u2018full repo awareness\u2019 means in practice: when debugging a timeout in your gas_hub_prices recipe, Copilot @workspace reads all related recipes, models, and configs. Ask \u201cwhat upstream changes could be causing this timeout?\u201d and it traces dependencies across 20+ files without being told to look there.\n\nBest for: daily inline work, debugging in your existing IDE, documentation generation, PR review, and any task where BP enterprise licence is the access route.",
      {
        x: 0.45, y: cardY + 0.4, w: cardW - 0.3, h: cardH - 0.55,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    // Right card — Cursor
    h.addCard(s, 5.1, cardY, cardW, cardH, C.white);

    s.addShape(pres.ShapeType.rect, {
      x: 5.1, y: cardY, w: cardW, h: 0.32,
      fill: { color: C.green },
      line: { color: C.green, width: 0 },
    });
    s.addText("Cursor", {
      x: 5.25, y: cardY, w: cardW - 0.3, h: 0.32,
      fontFace: "Trebuchet MS",
      fontSize: 12,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    s.addText(
      "A full VS Code fork \u2014 AI is not an add-on but the core architecture. Semantic codebase indexing means Cursor has not just read the file names but understands how your Dataiku project\u2019s recipes, models, and outputs connect. Full model choice: Claude Sonnet for speed, Opus for deep debugging, Gemini for very large context tasks.\n\nWhat background agents mean in practice: type \u201crefactor all ELT aggregation recipes to use Polars for the heavy transforms.\u201d Cursor submits this to a background agent and returns control immediately. Ninety minutes later: the refactor is complete, tests are updated, and a branch is created. This is AI as a parallel team member, not AI as a faster keyboard.\n\nBest for: large multi-file projects, complex builds from scratch, tasks requiring sustained autonomy, and when you want to choose your model per task.",
      {
        x: 5.25, y: cardY + 0.4, w: cardW - 0.3, h: cardH - 0.55,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    h.bottomBar(s, "Use GitHub Copilot for daily inline work in your existing IDE; use Cursor when the task spans multiple files or requires autonomous execution");
  }

  // ----------------------------------------------------------
  // Slide 18: [LIVE DEMO] GitHub Copilot — Dataiku Recipe Timeout
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "GITHUB COPILOT|SEE IT IN ACTION", "[LIVE DEMO] Dataiku recipe timeout \u2014 debugged in 20 minutes", C.green);

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

    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 1.78, w: 9.4, h: 0.55,
      fill: { color: "1A1A2E" },
      line: { color: "1A1A2E", width: 0 },
    });
    s.addText(
      "This Dataiku recipe is timing out on 500k rows. It runs fine on 10k rows in isolation. Identify the bottleneck and rewrite the aggregation logic using vectorised operations.",
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

    // Left panel
    h.addCard(s, 0.3, 2.45, 5.8, 2.35, C.white);

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

    s.addText(
      "1. Copilot @workspace reads the full recipe and all upstream data sources\n2. Identifies the iterrows() anti-pattern on line 47 \u2014 O(n) loop over 500k rows\n3. Rewrites using pandas vectorised groupby \u2014 reduces from O(n) to O(n log n)\n4. Adds a docstring explaining the original problem and the optimisation choice\n5. Suggests unit tests for the refactored function with edge cases for empty input and single-row data",
      {
        x: 0.45, y: 2.8, w: 5.5, h: 1.85,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    // Right panel
    h.addCard(s, 6.25, 2.45, 3.45, 2.35, C.white);

    s.addText("20 min", {
      x: 6.35, y: 2.55, w: 3.25, h: 0.6,
      fontFace: "Trebuchet MS",
      fontSize: 36,
      bold: true,
      color: C.green,
      align: "center",
      valign: "middle",
    });

    s.addText("from timeout to optimised, tested, documented recipe", {
      x: 6.35, y: 3.2, w: 3.25, h: 0.35,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.textMed,
      align: "center",
      valign: "middle",
      wrap: true,
    });

    s.addText("Manual: 3\u20134 hours", {
      x: 6.35, y: 3.62, w: 3.25, h: 0.3,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.red,
      align: "center",
      valign: "middle",
    });

    h.bottomBar(s, "[PRESENTER: open VS Code with the demo recipe] \u2014 the 3-4 hour debug cycle just became a 20-minute review cycle");
  }

  // ----------------------------------------------------------
  // Slide 19: [LIVE DEMO] Cursor — Prompt to Working Dash App in 12 Minutes
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "CURSOR|SEE IT IN ACTION", "[LIVE DEMO] Prompt to working Dash app \u2014 12 minutes", C.green);

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

    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 1.78, w: 9.4, h: 0.55,
      fill: { color: "1A1A2E" },
      line: { color: "1A1A2E", width: 0 },
    });
    s.addText(
      "Build a Plotly Dash app showing crack spread evolution for Q1 2025. Read from crack_spreads.csv, add a 30-day rolling average, include a date range picker and commodity selector. Deploy locally on port 8050.",
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

    // Left panel
    h.addCard(s, 0.3, 2.45, 5.8, 2.35, C.white);

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

    s.addText(
      "1. Cursor reads crack_spreads.csv and understands the column schema and date range\n2. Writes the complete Dash app layout with Plotly chart callbacks\n3. Implements the rolling average with correct NaN handling at the start of the series\n4. Adds date range picker and commodity selector dropdown with proper callback wiring\n5. Runs the app locally \u2014 browser opens automatically to localhost:8050",
      {
        x: 0.45, y: 2.8, w: 5.5, h: 1.85,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    // Right panel — v4: big number as visual centrepiece (Enhancement 4)
    h.addCard(s, 6.25, 2.45, 3.45, 2.35, C.white);

    s.addText("12 min", {
      x: 6.35, y: 2.45, w: 3.25, h: 0.72,
      fontFace: "Trebuchet MS",
      fontSize: 48,
      bold: true,
      color: C.green,
      align: "center",
      valign: "middle",
    });

    s.addText("from first prompt to app running in browser", {
      x: 6.35, y: 3.2, w: 3.25, h: 0.35,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.textMed,
      align: "center",
      valign: "middle",
      wrap: true,
    });

    s.addShape(pres.ShapeType.rect, {
      x: 6.45, y: 3.57, w: 3.05, h: 0.03,
      fill: { color: C.divider },
      line: { color: C.divider, width: 0 },
    });

    s.addText("Manual equivalent", {
      x: 6.35, y: 3.63, w: 3.25, h: 0.22,
      fontFace: "Calibri",
      fontSize: 8,
      italic: true,
      color: C.textMed,
      align: "center",
      valign: "middle",
    });

    s.addText("2\u20133 days", {
      x: 6.35, y: 3.86, w: 3.25, h: 0.45,
      fontFace: "Trebuchet MS",
      fontSize: 22,
      bold: true,
      color: C.red,
      align: "center",
      valign: "middle",
    });

    s.addText("That is not a typo.", {
      x: 6.35, y: 4.33, w: 3.25, h: 0.22,
      fontFace: "Calibri",
      fontSize: 8,
      italic: true,
      color: C.textMed,
      align: "center",
      valign: "middle",
    });

    h.bottomBar(s, "[PRESENTER: run this live now] \u2014 this is the \u2018hours to minutes\u2019 shift that changes how FM\u0026I responds to desk requests");
  }

  // ----------------------------------------------------------
  // Slide 20: Three Modes — Match the Mode to the Task
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
        body: "Single-turn question and answer. The AI reads your context but takes no actions. Use Ask mode for: explaining what an unfamiliar function does, getting a second opinion on a data model design, understanding why a Pandas merge is dropping rows, or learning the correct Dataiku API call for triggering a scenario. The mental model: Ask is the colleague you interrupt with a quick question \u2014 no need to pick up where you left off, because there is no state.",
      },
      {
        x: 3.4,
        accentColor: C.blue,
        badgeColor: C.blue,
        badgeText: "COMPLEX",
        title: "Agent",
        body: "Multi-step autonomous execution. Give a goal, the agent plans and executes across your codebase. Use Agent mode for: implementing a feature that touches 5+ files, debugging a production issue by reading logs and tracing the call stack, writing a comprehensive test suite, or adding docstrings to every function in a recipe. FM\u0026I use case: \u201cadd data quality validation to the gas pricing ELT pipeline\u201d \u2014 Agent plans the changes across all affected recipes, implements them, runs existing tests.",
      },
      {
        x: 6.5,
        accentColor: C.purple,
        badgeColor: C.purple,
        badgeText: "SAFE",
        title: "Plan",
        body: "The AI proposes a complete plan of changes and waits for approval before executing anything. Use Plan mode when: touching a production pipeline, working in an unfamiliar codebase and wanting to understand scope before changes are made, or when a wrong first step could compound into a large rollback. FM\u0026I use case: \u201cmigrate the VaR calculation from the legacy module to the new risk framework\u201d \u2014 Plan shows every file that changes before writing a single line.",
      },
    ];

    const cardW = 2.9;
    const cardH = 2.85;
    const cardY = 1.55;

    modes.forEach(function(mode) {
      h.addCard(s, mode.x, cardY, cardW, cardH, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: mode.x, y: cardY, w: cardW, h: 0.05,
        fill: { color: mode.accentColor },
        line: { color: mode.accentColor, width: 0 },
      });

      s.addShape(pres.ShapeType.rect, {
        x: mode.x + cardW - 0.68, y: cardY + 0.1, w: 0.6, h: 0.22,
        fill: { color: mode.badgeColor },
        line: { color: mode.badgeColor, width: 0 },
      });
      s.addText(mode.badgeText, {
        x: mode.x + cardW - 0.68, y: cardY + 0.1, w: 0.6, h: 0.22,
        fontFace: "Trebuchet MS",
        fontSize: 7,
        bold: true,
        color: C.white,
        align: "center",
        valign: "middle",
      });

      s.addText(mode.title, {
        x: mode.x + 0.15, y: cardY + 0.13, w: cardW - 0.88, h: 0.3,
        fontFace: "Trebuchet MS",
        fontSize: 14,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      s.addText(mode.body, {
        x: mode.x + 0.15, y: cardY + 0.52, w: cardW - 0.3, h: cardH - 0.68,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });
    });

    h.bottomBar(s, "Default to Ask for questions, Agent for tasks, Plan when the stakes are high \u2014 this single habit change 3\u00d7 the value of either tool");
  }

  // ----------------------------------------------------------
  // Slide 21: Better Prompts = Better Output — The Formula
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "TOOLS|PROMPTING", "Better prompts = better output \u2014 here\u2019s the formula", C.green);

    const promptCards = [
      {
        title: "Be specific about context",
        body: "Include the specific framework, data shape, and expected output format in every prompt. \u201cOptimise this function\u201d produces generic output. \u201cOptimise this Pandas aggregation for a 500k-row gas pricing dataset, targeting a 5\u00d7 speedup, without changing the output schema\u201d produces a solution you can use. Context specificity is the single highest-leverage prompt improvement.",
      },
      {
        title: "State constraints explicitly",
        body: "Enumerate what you cannot change: \u201cuse pandas not polars \u2014 this runs in a Dataiku Python 3.8 environment,\u201d \u201coutput must be a dictionary keyed by hub name not a DataFrame,\u201d \u201cdo not modify the function signature \u2014 it is called by 12 downstream recipes.\u201d Constraints prevent the AI from producing a technically correct but practically useless solution.",
      },
      {
        title: "Use the LLM to improve your prompt",
        body: "Type your rough prompt, then ask: \u201cRewrite this prompt to be clearer and more likely to produce the output I need, without changing the core task.\u201d The improved prompt consistently outperforms your original. This takes 30 seconds and routinely saves 15 minutes of iteration \u2014 it is not laziness but using the tool\u2019s strength to improve your tool use.",
      },
      {
        title: "Template your common prompts",
        body: "Store your best prompts in .cursorrules or .github/copilot-instructions.md so they are available as project context on every session. The FM\u0026I template: \u201cContext: [what the pipeline/model does]. Task: [specific action]. Constraints: [language, framework, output format, what cannot change]. Verification: [how to check correctness].\u201d",
      },
    ];

    const leftX = 0.3;
    const leftW = 4.5;
    const pCardH = 0.76;
    const pCardGap = 0.07;
    let pCardY = 1.45;

    promptCards.forEach(function(card) {
      h.addCard(s, leftX, pCardY, leftW, pCardH, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: leftX, y: pCardY, w: 0.05, h: pCardH,
        fill: { color: C.green },
        line: { color: C.green, width: 0 },
      });

      s.addText(card.title, {
        x: leftX + 0.15, y: pCardY + 0.05, w: leftW - 0.2, h: 0.23,
        fontFace: "Trebuchet MS",
        fontSize: 9.5,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      s.addText(card.body, {
        x: leftX + 0.15, y: pCardY + 0.29, w: leftW - 0.2, h: 0.4,
        fontFace: "Calibri",
        fontSize: 8,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });

      pCardY += pCardH + pCardGap;
    });

    // Right terminal card
    const rightX = 5.1;
    const rightW = 4.6;
    const rightH = 3.35;

    s.addShape(pres.ShapeType.rect, {
      x: rightX, y: 1.45, w: rightW, h: rightH,
      fill: { color: "1A1A2E" },
      line: { color: "1A1A2E", width: 0 },
    });

    s.addShape(pres.ShapeType.rect, {
      x: rightX, y: 1.45, w: rightW, h: 0.32,
      fill: { color: "2D3748" },
      line: { color: "2D3748", width: 0 },
    });
    s.addText("FM\u0026I prompt template", {
      x: rightX + 0.15, y: 1.45, w: rightW - 0.3, h: 0.32,
      fontFace: "Trebuchet MS",
      fontSize: 9,
      bold: true,
      color: C.textLight,
      align: "left",
      valign: "middle",
    });

    const templateLines = [
      "Context:",
      "  [what the pipeline/model does and",
      "   what the data looks like]",
      "",
      "Task:",
      "  [specific action to perform]",
      "",
      "Constraints:",
      "  - Python 3.8 / Dataiku DSS env",
      "  - Output format: [schema / type]",
      "  - Must not change: [function sig]",
      "",
      "Verification:",
      "  [how to check the output is correct]",
    ];
    s.addText(templateLines.join("\n"), {
      x: rightX + 0.2, y: 1.85, w: rightW - 0.4, h: rightH - 0.5,
      fontFace: "Courier New",
      fontSize: 8,
      color: C.teal,
      align: "left",
      valign: "top",
      wrap: false,
    });

    h.bottomBar(s, "The _p-presentation-creator repo is a live example: CLAUDE.md + agents + skills = consistent AI output on every run");
  }

  // ----------------------------------------------------------
  // Slide 22 (v5 NEW): Connecting GitHub Copilot to Your Dataiku Workflow
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "TOOLS|DATAIKU SETUP", "Connecting GitHub Copilot to your Dataiku workflow", C.blue);

    // Left card: copilot-instructions.md template
    s.addShape(pres.ShapeType.rect, {x: 0.3, y: 1.45, w: 4.55, h: 3.35, fill: {color: "1A1A2E"}, line: {color: "1A1A2E", width: 0}});
    s.addShape(pres.ShapeType.rect, {x: 0.3, y: 1.45, w: 4.55, h: 0.28, fill: {color: C.blue}, line: {color: C.blue, width: 0}});
    s.addText("copilot-instructions.md  (save in project root)", {x: 0.45, y: 1.45, w: 4.25, h: 0.28, fontFace: "Courier New", fontSize: 7.5, bold: true, color: C.white, valign: "middle"});
    s.addText(
      "# FM&I Dataiku Project \u2014 Copilot Instructions\n\n## Context\nThis is a Dataiku DSS project for the FM&I team at BP Trading.\nPrimary language: Python. Recipes run as Dataiku Python recipes.\nPipelines read from and write to Dataiku managed datasets.\n\n## Code style\n- Use polars for dataframe operations, not pandas\n- All functions must have NumPy-style docstrings\n- Wrap Dataiku dataset reads: dataiku.Dataset('name').get_dataframe()\n- Never use iterrows() \u2014 use vectorised operations\n\n## Domain context\n- Commodity: energy (crude, refined products, natural gas)\n- Key datasets: crack_spreads, gas_hub_prices, brent_forward_curve\n- Calibration parameters are NEVER to be logged or written to output\n\n## When suggesting fixes\nAlways explain why the current approach is wrong before suggesting the fix.",
      {x: 0.45, y: 1.8, w: 4.25, h: 2.85, fontFace: "Courier New", fontSize: 7, color: "A8B8D8", valign: "top", wrap: true}
    );

    // Right card: step-by-step setup
    s.addShape(pres.ShapeType.rect, {x: 5.1, y: 1.45, w: 4.55, h: 3.35, fill: {color: C.white}, line: {color: C.divider, width: 1}});
    s.addShape(pres.ShapeType.rect, {x: 5.1, y: 1.45, w: 4.55, h: 0.28, fill: {color: C.blue}, line: {color: C.blue, width: 0}});
    s.addText("How to set this up (5 minutes)", {x: 5.25, y: 1.45, w: 4.25, h: 0.28, fontFace: "Trebuchet MS", fontSize: 9, bold: true, color: C.white, valign: "middle"});

    const setupSteps = [
      {n: "1", title: "Create the file", body: "Save the template above as .github/copilot-instructions.md in your Dataiku project root. If you work in VS Code connected to a Dataiku remote kernel, this is the VS Code workspace root."},
      {n: "2", title: "Open VS Code with Dataiku extension", body: "Install the Dataiku VS Code extension. Connect to your DSS instance using your API key. Open a Python recipe \u2014 Copilot now has access to your project context AND your custom instructions simultaneously."},
      {n: "3", title: "Test it", body: "Type a comment: # read the crack_spreads dataset and calculate rolling 30-day average. Copilot should suggest code that uses dataiku.Dataset() correctly and polars syntax \u2014 not generic pandas code."},
      {n: "4", title: "Refine the instructions", body: "After your first real use, ask Copilot: \u2018Review my copilot-instructions.md and suggest what\u2019s missing given what you know about my codebase.\u2019 Paste the file, let it improve itself."},
    ];

    setupSteps.forEach(function(step, i) {
      const stepY = 1.82 + i * 0.72;
      s.addShape(pres.ShapeType.rect, {x: 5.2, y: stepY, w: 0.28, h: 0.28, fill: {color: C.blue}, line: {color: C.blue, width: 0}});
      s.addText(step.n, {x: 5.2, y: stepY, w: 0.28, h: 0.28, fontFace: "Trebuchet MS", fontSize: 8, bold: true, color: C.white, align: "center", valign: "middle"});
      s.addText(step.title, {x: 5.55, y: stepY, w: 3.95, h: 0.2, fontFace: "Trebuchet MS", fontSize: 8.5, bold: true, color: C.textDark, valign: "middle"});
      s.addText(step.body, {x: 5.55, y: stepY + 0.22, w: 3.95, h: 0.42, fontFace: "Calibri", fontSize: 7.5, color: C.textMed, valign: "top", wrap: true});
    });

    h.bottomBar(s, "The copilot-instructions.md file is the difference between generic AI suggestions and FM&I-specific code \u2014 takes 5 minutes to set up, saves hours every week");
  }

  // ----------------------------------------------------------
  // Slide 23 (v5 NEW): Connecting Cursor to Your Dataiku Project
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "TOOLS|DATAIKU SETUP", "Connecting Cursor to your Dataiku project", C.green);

    // Left card: .cursorrules template
    s.addShape(pres.ShapeType.rect, {x: 0.3, y: 1.45, w: 4.55, h: 3.35, fill: {color: "1A1A2E"}, line: {color: "1A1A2E", width: 0}});
    s.addShape(pres.ShapeType.rect, {x: 0.3, y: 1.45, w: 4.55, h: 0.28, fill: {color: C.green}, line: {color: C.green, width: 0}});
    s.addText(".cursorrules  (save in project root)", {x: 0.45, y: 1.45, w: 4.25, h: 0.28, fontFace: "Courier New", fontSize: 7.5, bold: true, color: C.white, valign: "middle"});
    s.addText(
      "# Cursor Rules \u2014 FM&I Dataiku Project\n\n## Project type\nDataiku DSS Python project. BP Trading, FM&I team.\n\n## Always do\n- Use polars not pandas\n- Use dataiku.Dataset('name').get_dataframe() for reads\n- Add NumPy docstrings to every function\n- Write pytest tests for every new function\n- Use pathlib not os.path\n\n## Never do\n- Use iterrows() or apply() on large dataframes\n- Log or print calibration parameters\n- Use f-strings for SQL queries (use parameterised queries)\n- Hardcode dataset names \u2014 read from config\n\n## FM&I domain terms\ncrack spread, forward curve, VaR, half-life estimator,\nELT pipeline, Dataiku scenario, trigger, recipe\n\n## Code review checklist\nBefore suggesting any change, check:\n1. Does this work with Dataiku\u2019s managed dataset API?\n2. Is this vectorised (no loops over rows)?\n3. Does this function have a test?",
      {x: 0.45, y: 1.8, w: 4.25, h: 2.85, fontFace: "Courier New", fontSize: 6.8, color: "A8B8D8", valign: "top", wrap: true}
    );

    // Right card: Cursor-specific advantages
    s.addShape(pres.ShapeType.rect, {x: 5.1, y: 1.45, w: 4.55, h: 3.35, fill: {color: C.white}, line: {color: C.divider, width: 1}});
    s.addShape(pres.ShapeType.rect, {x: 5.1, y: 1.45, w: 4.55, h: 0.28, fill: {color: C.green}, line: {color: C.green, width: 0}});
    s.addText("Why Cursor + Dataiku is especially powerful", {x: 5.25, y: 1.45, w: 4.25, h: 0.28, fontFace: "Trebuchet MS", fontSize: 9, bold: true, color: C.white, valign: "middle"});

    const cursorPoints = [
      {title: "@Codebase understands your whole project", body: "Open Cursor with your Dataiku project folder as the root. Type @Codebase in the chat. Cursor indexes every recipe, config file, and model spec \u2014 then answers architecture questions across the full pipeline. Ask: \u2018which recipes depend on the crack_spreads dataset?\u2019 and get an accurate answer without searching manually."},
      {title: "Composer mode for multi-recipe refactors", body: "Use Ctrl+I (Composer) to apply a change across multiple recipes at once. Example: \u2018Update all ELT aggregation recipes to use polars.read_csv() instead of pandas \u2014 maintain existing output schema\u2019. Cursor creates a branch with all changes, you review the diff."},
      {title: "Background agent for long tasks", body: "Use Cursor background agents to run unattended: \u2018Add NumPy docstrings to all undocumented functions in the /recipes folder, write pytest tests for each, update requirements.txt\u2019. Returns 45 minutes later with a complete branch. Same cost as doing it yourself \u2014 fraction of the time."},
      {title: "First setup: open project, run /Rules", body: "Save .cursorrules in your project root. Open Cursor, open the project folder. In chat, type /rules to confirm the rules are loaded. Test: ask Cursor to fix an iterrows() call \u2014 it should suggest a polars equivalent without being told."},
    ];

    cursorPoints.forEach(function(pt, i) {
      const ptY = 1.82 + i * 0.72;
      s.addShape(pres.ShapeType.rect, {x: 5.15, y: ptY, w: 0.04, h: 0.55, fill: {color: C.green}, line: {color: C.green, width: 0}});
      s.addText(pt.title, {x: 5.28, y: ptY, w: 4.25, h: 0.22, fontFace: "Trebuchet MS", fontSize: 8.5, bold: true, color: C.textDark, valign: "middle"});
      s.addText(pt.body, {x: 5.28, y: ptY + 0.24, w: 4.25, h: 0.38, fontFace: "Calibri", fontSize: 7.5, color: C.textMed, valign: "top", wrap: true});
    });

    h.bottomBar(s, "The .cursorrules file means every Cursor conversation in your project already knows the FM&I context \u2014 you stop repeating yourself and it stops suggesting pandas");
  }

  // ----------------------------------------------------------
  // Slide 24 (v5 NEW): Before and After — What a Better Prompt Looks Like
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "PROMPTING|FM\u0026I EXAMPLES", "Before and after: what a better prompt looks like in practice", C.purple);

    // Three before/after pairs
    const pairs = [
      {
        before: "debug this recipe",
        after: "I have a Dataiku Python recipe that reads gas_hub_prices (500k rows, daily frequency, 10-year history) and aggregates by hub and month. It\u2019s timing out at 45 seconds on the Dataiku dev node. Use polars not pandas. Identify the bottleneck, explain why it\u2019s causing the timeout, and rewrite the aggregation to run in under 5 seconds.",
        result: "Identifies iterrows() loop as bottleneck, rewrites with polars groupby, adds timing assertion to the test"
      },
      {
        before: "write a model summary doc",
        after: "Read the crack spread half-life estimator model in /recipes/crack_spread_halflife.py and the config in /config/model_params.json. Generate a MODEL.md file with: (1) purpose and commercial application, (2) data inputs and their sources, (3) methodology with the key equations in LaTeX, (4) known limitations, (5) calibration parameters that must not be shared externally. Format for the FM\u0026I model registry.",
        result: "Produces a complete MODEL.md using actual variable names, flags the 3 calibration parameters, formats equations correctly"
      },
      {
        before: "summarise this meeting",
        after: "Summarise this FM\u0026I model review call recording. Extract: all actions assigned to the analytics team with owner name and due date, any model calibration decisions made or deferred, open questions about the crack spread ELT pipeline raised by the trading desk. Format as a structured brief ready to post to the FM\u0026I Teams channel.",
        result: "Returns structured brief with 4 named actions, 2 deferred calibration decisions, 3 pipeline questions \u2014 ready to post in 90 seconds"
      }
    ];

    pairs.forEach(function(pair, i) {
      const rowY = 1.45 + i * 1.22;
      const rowH = 1.1;

      // Before label
      s.addShape(pres.ShapeType.rect, {x: 0.3, y: rowY, w: 0.55, h: 0.22, fill: {color: C.red}, line: {color: C.red, width: 0}});
      s.addText("BEFORE", {x: 0.3, y: rowY, w: 0.55, h: 0.22, fontFace: "Trebuchet MS", fontSize: 6, bold: true, color: C.white, align: "center", valign: "middle"});
      s.addShape(pres.ShapeType.rect, {x: 0.3, y: rowY + 0.22, w: 2.8, h: rowH - 0.22, fill: {color: "FEF2F2"}, line: {color: "FECACA", width: 1}});
      s.addText(pair.before, {x: 0.42, y: rowY + 0.28, w: 2.6, h: rowH - 0.38, fontFace: "Courier New", fontSize: 8, color: C.red, valign: "middle", italic: true, wrap: true});

      // Arrow
      s.addText("\u2192", {x: 3.18, y: rowY + 0.22, w: 0.35, h: rowH - 0.22, fontFace: "Calibri", fontSize: 16, bold: true, color: C.textMed, align: "center", valign: "middle"});

      // After label
      s.addShape(pres.ShapeType.rect, {x: 3.6, y: rowY, w: 0.55, h: 0.22, fill: {color: C.green}, line: {color: C.green, width: 0}});
      s.addText("AFTER", {x: 3.6, y: rowY, w: 0.55, h: 0.22, fontFace: "Trebuchet MS", fontSize: 6, bold: true, color: C.white, align: "center", valign: "middle"});
      s.addShape(pres.ShapeType.rect, {x: 3.6, y: rowY + 0.22, w: 4.3, h: rowH - 0.22, fill: {color: "F0FDF4"}, line: {color: "BBF7D0", width: 1}});
      s.addText(pair.after, {x: 3.72, y: rowY + 0.28, w: 4.1, h: rowH - 0.38, fontFace: "Courier New", fontSize: 7, color: C.textDark, valign: "top", wrap: true});

      // Result tag
      s.addShape(pres.ShapeType.rect, {x: 8.0, y: rowY + 0.22, w: 1.8, h: rowH - 0.22, fill: {color: C.lightBlue}, line: {color: C.blue, width: 1}});
      s.addText("Result: " + pair.result, {x: 8.08, y: rowY + 0.28, w: 1.64, h: rowH - 0.38, fontFace: "Calibri", fontSize: 7, color: C.blue, valign: "top", wrap: true});
    });

    h.bottomBar(s, "The formula: Context (what system/data) + Task (specific output) + Constraints (format, limits) + Verification (how to check it\u2019s right) \u2014 10 seconds to type, 10x better output");
  }

  // ----------------------------------------------------------
  // Slide 25 (v4: Slide 22): Both Tools Are Shipping Major Upgrades in 2026
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "TOOLS|ROADMAP", "Both tools are shipping major capability upgrades in 2026", C.green);

    const cardW = 4.55;
    const cardH = 3.35;
    const cardY = 1.45;

    // Left card — GitHub Copilot 2026
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
      {
        q: "Q1",
        desc: "Copilot Extensions: tool calling that connects to external services. For FM\u0026I: Copilot chat can query your Dataiku scenario status without leaving VS Code, using MCP-style integration.",
      },
      {
        q: "Q2",
        desc: "Copilot CLI GA: natural language terminal commands. Type what you want in English, Copilot CLI writes the shell command. Useful for Dataiku CLI operations and complex git workflows.",
      },
      {
        q: "Q3",
        desc: "Multi-file autonomous edits without per-step approval. Currently, Copilot Edit mode requires review of each change. Q3 enables \u2018apply all\u2019 for trusted agent sessions \u2014 closer to Cursor\u2019s agent mode.",
      },
      {
        q: "Q4",
        desc: "Integrated pre-PR review agent \u2014 flags issues in your code before you raise the pull request, reducing review cycle time and catching regressions that would otherwise reach code review.",
      },
    ];

    let rmYL = cardY + 0.42;
    copilotRoadmap.forEach(function(item) {
      s.addText(item.q + ":", {
        x: 0.45, y: rmYL, w: 0.38, h: 0.56,
        fontFace: "Trebuchet MS",
        fontSize: 9,
        bold: true,
        color: C.blue,
        align: "left",
        valign: "top",
      });
      s.addText(item.desc, {
        x: 0.86, y: rmYL, w: cardW - 0.62, h: 0.56,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });
      rmYL += 0.64;
    });

    // Right card — Cursor 2026
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
      {
        q: "Q1",
        desc: "Cursor Teams: shared .cursorrules and agent coordination across the whole team. Every FM\u0026I engineer starts each session with the same project context, conventions, and shared prompt templates \u2014 no individual setup required.",
      },
      {
        q: "Q2",
        desc: "Background agents on cloud: submit long-running tasks and they run even when your laptop is closed. Submit a large-scale ELT refactor overnight and review the completed result in the morning.",
      },
      {
        q: "Q3",
        desc: "Integrated test runner: the agent writes code, immediately runs tests, sees failures, fixes them, and iterates \u2014 all in a single autonomous loop. Closes the manual \u2018trigger the test run\u2019 step that currently requires human involvement.",
      },
      {
        q: "Q4",
        desc: "Cursor for notebooks: full Jupyter notebook support with agent mode. For FM\u0026I analysts working primarily in Jupyter for model development, this brings the full Cursor agent workflow to notebook-based work.",
      },
    ];

    let rmYR = cardY + 0.42;
    cursorRoadmap.forEach(function(item) {
      s.addText(item.q + ":", {
        x: 5.25, y: rmYR, w: 0.38, h: 0.56,
        fontFace: "Trebuchet MS",
        fontSize: 9,
        bold: true,
        color: C.green,
        align: "left",
        valign: "top",
      });
      s.addText(item.desc, {
        x: 5.66, y: rmYR, w: cardW - 0.62, h: 0.56,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });
      rmYR += 0.64;
    });

    h.bottomBar(s, "Cursor\u2019s cloud background agents (Q2) + GitHub Copilot\u2019s extension ecosystem (Q1) are the two most relevant near-term features for FM\u0026I");
  }

  // ============================================================
  // SECTION 5 — THE MODEL LANDSCAPE
  // ============================================================

  // ----------------------------------------------------------
  // Slide 26 (v4: Slide 23): Section Divider — The Model Landscape
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.purple },
      line: { color: C.purple, width: 0 },
    });

    s.addText("05", {
      x: 0.6, y: 1.2, w: 2, h: 0.8,
      fontFace: "Trebuchet MS",
      fontSize: 48,
      bold: true,
      color: C.purple,
      align: "left",
      valign: "middle",
    });

    s.addText("The Model Landscape", {
      x: 0.6, y: 2.1, w: 8.8, h: 0.65,
      fontFace: "Trebuchet MS",
      fontSize: 32,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

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
  // Slide 27 (v4: Slide 24): The Models You Knew a Year Ago Are Not the Models Available Today
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "MODELS|TIMELINE", "The models you knew a year ago are not the models available today", C.purple);

    const milestones = [
      {
        date: "Q1 2025",
        title: "Claude 3.5 + GPT-4o",
        desc: "Claude 3.5 Sonnet became the de-facto coding standard \u2014 the first model where test generation, documentation, and refactoring reached production quality. GPT-4o\u2019s improved tool use made agentic workflows reliable for professional use. The inflection point for FM\u0026I engineering.",
        color: C.blue,
      },
      {
        date: "Q2 2025",
        title: "Gemini 2.0 + Claude 3.7",
        desc: "Gemini 2.0 made 1M context windows practically usable \u2014 entire large Dataiku projects in one context. Claude 3.7 added extended thinking: visible reasoning chains for complex multi-step problems. Both moved the frontier for what was possible in a single AI session.",
        color: C.teal,
      },
      {
        date: "Q3 2025",
        title: "o3 + Llama 3.3",
        desc: "OpenAI\u2019s o3 reasoning model achieved step-change performance on mathematical problems \u2014 relevant for statistical methodology questions. Llama 3.3 70B narrowed the open-source quality gap, making local-model workflows genuinely viable for data-sensitive use cases.",
        color: C.green,
      },
      {
        date: "Q4 2025",
        title: "Claude Sonnet 4.6",
        desc: "Current production standard. Coding and instruction-following improvements made it the best daily-driver for FM\u0026I pipeline development \u2014 fast enough for interactive sessions, accurate enough for complex transformations, cost-effective for high-frequency use.",
        color: C.orange,
      },
      {
        date: "Q1 2026",
        title: "Claude Opus 4.6",
        desc: "Frontier reasoning with extended thinking and multimodal improvements. Extended thinking mode enables complex statistical model debugging \u2014 the kind where you trace through 5 interacting components \u2014 with visible reasoning steps. The first model for architecture-level FM\u0026I problems.",
        color: C.purple,
      },
    ];

    const timelineY = 1.75;
    const totalW = 9.4;
    const startX = 0.3;
    const slotW = totalW / milestones.length;
    const dotSize = 0.16;

    s.addShape(pres.ShapeType.rect, {
      x: startX, y: timelineY + 0.07, w: totalW, h: 0.03,
      fill: { color: C.divider },
      line: { color: C.divider, width: 0 },
    });

    milestones.forEach(function(m, i) {
      const cx = startX + i * slotW + slotW / 2;

      s.addShape(pres.ShapeType.rect, {
        x: cx - dotSize / 2, y: timelineY,
        w: dotSize, h: dotSize,
        fill: { color: m.color },
        line: { color: m.color, width: 0 },
      });

      s.addText(m.date, {
        x: cx - slotW / 2 + 0.05, y: timelineY + 0.22,
        w: slotW - 0.1, h: 0.2,
        fontFace: "Calibri",
        fontSize: 8,
        bold: true,
        color: m.color,
        align: "center",
        valign: "top",
      });

      s.addText(m.title, {
        x: cx - slotW / 2 + 0.05, y: timelineY + 0.44,
        w: slotW - 0.1, h: 0.2,
        fontFace: "Trebuchet MS",
        fontSize: 8,
        bold: true,
        color: C.textDark,
        align: "center",
        valign: "top",
      });

      s.addText(m.desc, {
        x: cx - slotW / 2 + 0.05, y: timelineY + 0.66,
        w: slotW - 0.1, h: 2.1,
        fontFace: "Calibri",
        fontSize: 7.5,
        color: C.textMed,
        align: "center",
        valign: "top",
        wrap: true,
      });
    });

    h.bottomBar(s, "Quality improved 10\u00d7 in 12 months \u2014 the model you tried 12 months ago is not the one you should evaluate today");
  }

  // ----------------------------------------------------------
  // Slide 28 (v4: Slide 25): Different Models Excel at Different Tasks
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "MODELS|COMPARISON", "Different models excel at different tasks \u2014 here is the map", C.purple);

    const modelCards = [
      {
        x: 0.3, y: 1.45,
        accentColor: C.teal,
        title: "Claude Sonnet 4.6",
        body: "The daily driver for 80% of FM\u0026I coding work. Fast enough for interactive sessions, accurate enough for complex pandas/polars transformations, and at ~$3/M tokens \u2014 cost-effective for high-frequency use. Use Sonnet when: building or debugging Dataiku recipes, writing documentation and docstrings, generating test suites, interactive Q\u0026A about your codebase. The sensible default \u2014 upgrade only when Sonnet\u2019s output isn\u2019t good enough.",
      },
      {
        x: 5.1, y: 1.45,
        accentColor: C.purple,
        title: "Claude Opus 4.6",
        body: "Best for problems requiring sustained multi-step reasoning \u2014 debugging non-obvious model bugs that require tracing through 5 interacting components, designing a new pipeline architecture from scratch, or synthesising a large body of research to inform a modelling decision. Use Opus when: Sonnet has tried and failed, the problem is genuinely complex, or the stakes are high enough that maximum quality matters more than speed or cost.",
      },
      {
        x: 0.3, y: 3.3,
        accentColor: C.blue,
        title: "GPT-4o / o3",
        body: "GPT-4o is strong for multimodal tasks \u2014 understanding charts, processing uploaded CSV files via Code Interpreter, and image-based analysis. o3 is purpose-built for mathematical and logical reasoning: use it for complex statistical methodology questions, calibration problems, or anything requiring rigorous numerical reasoning. For FM\u0026I: o3 for half-life estimator methodology questions; GPT-4o for processing uploaded market data files in ChatGPT\u2019s analysis sandbox.",
      },
      {
        x: 5.1, y: 3.3,
        accentColor: C.green,
        title: "Ollama (local models)",
        body: "The only safe option for any input containing proprietary data. Ollama runs Llama 3.3, Mistral, or Phi-4 on your local machine \u2014 zero data leaves BP infrastructure. Use Ollama when: the code contains actual model parameters, calibrated coefficients, or position-adjacent data in comments or variable names. Quality is meaningfully below Claude Sonnet but infinitely better than not using AI for data-sensitive work.",
      },
    ];

    const cardW = 4.4;
    const cardH = 1.72;

    modelCards.forEach(function(card) {
      h.addCard(s, card.x, card.y, cardW, cardH, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: card.x, y: card.y, w: cardW, h: 0.05,
        fill: { color: card.accentColor },
        line: { color: card.accentColor, width: 0 },
      });

      s.addText(card.title, {
        x: card.x + 0.15, y: card.y + 0.1, w: cardW - 0.3, h: 0.28,
        fontFace: "Trebuchet MS",
        fontSize: 10,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      s.addText(card.body, {
        x: card.x + 0.15, y: card.y + 0.43, w: cardW - 0.3, h: cardH - 0.55,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });
    });

    h.bottomBar(s, "Default to Claude Sonnet for 80% of FM\u0026I tasks \u2014 use Opus for complexity, o3 for maths, Ollama for data-sensitive work");
  }

  // ----------------------------------------------------------
  // Slide 29 (v4: Slide 26): A Simple Decision Framework for Model Selection
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "MODELS|DECISION", "A simple decision framework for model selection", C.purple);

    const decisionCards = [
      {
        question: "Q1: Does the task involve sensitive or proprietary data (positions, model parameters, live prices)?",
        yesLabel: "Yes \u2192",
        yesAnswer: "Ollama local model. Non-negotiable. No cloud model should receive proprietary FM\u0026I data.",
        yesBadgeColor: C.orange,
        noLabel: "No \u2192",
        noAnswer: "Proceed to Q2",
      },
      {
        question: "Q2: Is this an interactive coding task or a batch/agentic workflow running unattended?",
        yesLabel: "Interactive \u2192",
        yesAnswer: "Claude Sonnet 4.6. Speed matters; Sonnet is 3-5\u00d7 faster than Opus for interactive sessions.",
        yesBadgeColor: C.cyan,
        noLabel: "Batch \u2192",
        noAnswer: "Claude Opus or o3. Running while you sleep: optimise for quality over latency.",
      },
      {
        question: "Q3: Does the task require deep mathematical or statistical reasoning (calibration, complex methodology)?",
        yesLabel: "Yes \u2192",
        yesAnswer: "o3 (OpenAI reasoning model). Outperforms all other models on complex mathematical problems.",
        yesBadgeColor: C.teal,
        noLabel: "No \u2192",
        noAnswer: "Claude Sonnet 4.6. Default and correct for most FM\u0026I coding and analysis tasks.",
      },
    ];

    const leftX = 0.3;
    const leftW = 6.3;
    const dCardH = 0.92;
    const dCardGap = 0.1;
    let dCardY = 1.45;

    decisionCards.forEach(function(card) {
      h.addCard(s, leftX, dCardY, leftW, dCardH, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: leftX, y: dCardY, w: 0.05, h: dCardH,
        fill: { color: C.purple },
        line: { color: C.purple, width: 0 },
      });

      s.addText(card.question, {
        x: leftX + 0.15, y: dCardY + 0.05, w: leftW - 0.25, h: 0.3,
        fontFace: "Trebuchet MS",
        fontSize: 8.5,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
        wrap: true,
      });

      const halfW = (leftW - 0.25) / 2;

      s.addText(card.yesLabel, {
        x: leftX + 0.15, y: dCardY + 0.44, w: 0.75, h: 0.36,
        fontFace: "Calibri",
        fontSize: 8.5,
        bold: true,
        color: card.yesBadgeColor,
        align: "left",
        valign: "top",
      });

      s.addText(card.yesAnswer, {
        x: leftX + 0.9, y: dCardY + 0.44, w: halfW - 0.5, h: 0.36,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textDark,
        align: "left",
        valign: "top",
        wrap: true,
      });

      s.addText(card.noLabel, {
        x: leftX + 0.15 + halfW, y: dCardY + 0.44, w: 0.75, h: 0.36,
        fontFace: "Calibri",
        fontSize: 8.5,
        bold: true,
        color: C.textMed,
        align: "left",
        valign: "top",
      });
      s.addText(card.noAnswer, {
        x: leftX + 0.9 + halfW, y: dCardY + 0.44, w: halfW - 0.7, h: 0.36,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });

      dCardY += dCardH + dCardGap;
    });

    // Cost reference card
    const costX = 6.8;
    const costW = 2.9;
    const costH = 3.3;
    h.addCard(s, costX, 1.45, costW, costH, C.lightBlue);

    s.addText("Approximate cost per 1M tokens (Q1 2026)", {
      x: costX + 0.15, y: 1.55, w: costW - 0.3, h: 0.35,
      fontFace: "Trebuchet MS",
      fontSize: 8.5,
      bold: true,
      color: C.textDark,
      align: "left",
      valign: "top",
      wrap: true,
    });

    const costLines = [
      "Opus 4.6:     $15 / $75",
      "Sonnet 4.6:    $3 / $15",
      "GPT-4o:        $5 / $15",
      "o3:           $10 / $40",
      "Gemini 2.5:  $3.50 / $10.50",
      "Ollama local:  $0 / $0",
    ];
    s.addText(costLines.join("\n"), {
      x: costX + 0.15, y: 2.0, w: costW - 0.3, h: 2.5,
      fontFace: "Courier New",
      fontSize: 9,
      color: C.textDark,
      align: "left",
      valign: "top",
      wrap: false,
    });

    h.bottomBar(s, "Default to Sonnet for daily FM\u0026I work \u2014 only upgrade to Opus when the task genuinely demands multi-step reasoning over large context");
  }

  // ============================================================
  // SECTION 6 — ETHICS & COMPLIANCE
  // ============================================================

  // ----------------------------------------------------------
  // Slide 30 (v4: Slide 27): Section Divider — Ethics & Compliance
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.orange },
      line: { color: C.orange, width: 0 },
    });

    s.addText("06", {
      x: 0.6, y: 1.2, w: 2, h: 0.8,
      fontFace: "Trebuchet MS",
      fontSize: 48,
      bold: true,
      color: C.orange,
      align: "left",
      valign: "middle",
    });

    s.addText("Ethics \u0026 Compliance", {
      x: 0.6, y: 2.1, w: 8.8, h: 0.65,
      fontFace: "Trebuchet MS",
      fontSize: 32,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

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
  // Slide 31 (v4: Slide 28): The Data Boundary Is the Most Important Thing in This Session
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "COMPLIANCE|DATA RULES", "The data boundary is the most important thing in this session", C.orange);

    const cardW = 4.55;
    const cardH = 3.35;
    const cardY = 1.45;

    // Left card — SAFE
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
      "\u2022 Open-source code and generic scripts \u2014 code structure and patterns are not proprietary. Asking \u201chow do I optimise this type of loop?\u201d is safe because the technique is separable from the data.",
      "\u2022 Anonymised sample data \u2014 replace specific hub names, volumes, and prices with generic placeholders before pasting. Structure is safe; real values may not be.",
      "\u2022 Public research and academic papers \u2014 already public. Summarise, extract, and synthesise freely.",
      "\u2022 Internal documentation (non-sensitive) \u2014 meeting notes, process documents, architecture diagrams that do not contain market-sensitive information or proprietary model details.",
      "\u2022 Code logic without real values \u2014 the structure of your half-life estimator is safer than a version containing calibrated coefficients for a live book.",
    ];
    s.addText(safeLines.join("\n"), {
      x: 0.45, y: cardY + 0.5, w: cardW - 0.3, h: cardH - 0.65,
      fontFace: "Calibri",
      fontSize: 8.5,
      color: C.textDark,
      align: "left",
      valign: "top",
      wrap: true,
    });

    // Right card — NEVER
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
      "\u2022 Live trading positions \u2014 MIFID II / REMIT territory. Positions submitted to an external AI tool constitute a data security event and potentially a regulatory breach.",
      "\u2022 Counterparty names or deal terms \u2014 commercially sensitive under NDA and potentially market-sensitive. Even anonymised, patterns in deal terms can be reverse-engineered.",
      "\u2022 Proprietary model parameters \u2014 calibrated coefficients represent years of analytical work and competitive advantage. They must not leave BP\u2019s infrastructure under any circumstances.",
      "\u2022 Unpublished price forecasts \u2014 qualify as inside information under MAR if they reflect material non-public analysis. External submission is a regulatory risk.",
      "\u2022 Anything marked CONFIDENTIAL or RESTRICTED \u2014 BP\u2019s data classification applies when pasting content into AI tools, exactly as it does when sharing via email.",
    ];
    s.addText(neverLines.join("\n"), {
      x: 5.25, y: cardY + 0.5, w: cardW - 0.3, h: cardH - 0.65,
      fontFace: "Calibri",
      fontSize: 8.5,
      color: C.textDark,
      align: "left",
      valign: "top",
      wrap: true,
    });

    h.bottomBar(s, "Rule of thumb: if you wouldn\u2019t paste it into a public Slack channel, do not paste it into an AI tool you don\u2019t control");
  }

  // ----------------------------------------------------------
  // Slide 32 (v4: Slide 29): Five Rules Cover 95% of Situations — Memorise These
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "COMPLIANCE|FM\u0026I RULES", "Five rules cover 95% of situations \u2014 memorise these", C.orange);

    const rules = [
      {
        num: "Rule 1",
        body: "Anonymise before you paste \u2014 Replace position sizes, counterparty names, and model outputs with generic placeholders before sharing with any AI tool outside the Microsoft tenant. \u201cHub_A: [volume] TWh at [price]\u201d is always safer than the real values. The anonymisation habit protects you from accidental disclosure even when you\u2019re moving fast.",
      },
      {
        num: "Rule 2",
        body: "M365 Copilot is safer for internal content \u2014 Microsoft\u2019s enterprise agreement covers BP data. When Copilot processes your internal Teams messages or SharePoint documents, data stays within BP\u2019s Microsoft tenant and is not used to train Microsoft\u2019s models. External tools (Cursor, Claude.ai, ChatGPT) are governed by individual terms of service that do not carry the same contractual protection.",
      },
      {
        num: "Rule 3",
        body: "Code does not equal data \u2014 but check \u2014 Pasting code logic is generally safe. Pasting the data the code runs on may not be. The distinction matters when code contains embedded real values: a function that hardcodes actual calibration parameters as defaults is sending proprietary data when you paste it. Extract the logic without the values before submitting to external tools.",
      },
      {
        num: "Rule 4",
        body: "Check before you use, not after \u2014 If you are unsure whether a specific use case is compliant \u2014 a new type of data, a new tool, a non-standard workflow \u2014 contact the Digital Centre of Excellence before using the tool, not after. The after-the-fact disclosure conversation is significantly harder than a 10-minute pre-approval check.",
      },
      {
        num: "Rule 5",
        body: "You own the output \u2014 always \u2014 AI-generated code or analysis must be reviewed and validated by you before it is used in any commercial decision or shared with the trading desk. The AI is not self-validating. When a fundamental model gives a bad signal and the desk acts on it, the analyst who produced that model owns that outcome \u2014 regardless of whether AI wrote the code.",
      },
    ];

    const ruleW = 9.4;
    const ruleH = 0.62;
    const ruleGap = 0.08;
    let ruleY = 1.45;

    rules.forEach(function(rule) {
      h.addCard(s, 0.3, ruleY, ruleW, ruleH, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: 0.3, y: ruleY, w: 0.05, h: ruleH,
        fill: { color: C.orange },
        line: { color: C.orange, width: 0 },
      });

      s.addText(rule.num, {
        x: 0.45, y: ruleY + 0.06, w: 0.78, h: ruleH - 0.12,
        fontFace: "Trebuchet MS",
        fontSize: 9,
        bold: true,
        color: C.orange,
        align: "left",
        valign: "middle",
      });

      s.addText(rule.body, {
        x: 1.25, y: ruleY + 0.06, w: ruleW - 1.05, h: ruleH - 0.12,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textDark,
        align: "left",
        valign: "middle",
        wrap: true,
      });

      ruleY += ruleH + ruleGap;
    });

    h.bottomBar(s, "BP AI guidance: intranet \u2192 \u2018Digital Tools\u2019 \u2192 \u2018AI Governance\u2019 \u2014 Digital Centre of Excellence for front-office questions");
  }

  // ----------------------------------------------------------
  // Slide 33 (v4: Slide 30): Not All AI Tools Handle Your Data the Same Way
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "COMPLIANCE|DATA HANDLING", "Not all AI tools handle your data the same way", C.orange);

    const cardW = 4.55;
    const cardH = 3.35;
    const cardY = 1.45;

    // Left — Microsoft M365 Copilot
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

    s.addText(
      "Data stays within BP\u2019s Microsoft tenant. Microsoft\u2019s enterprise data processing agreement means your inputs are not used to train Microsoft\u2019s models, IT administrators can access audit logs, and BP\u2019s data classification framework applies. The tool to use most freely for FM\u0026I operational content \u2014 meeting notes, internal reports, process documentation.",
      {
        x: 0.45, y: cardY + 0.42, w: cardW - 0.3, h: 0.9,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    const m365Lines = [
      "\u2022 Data stays within BP\u2019s Microsoft tenant",
      "\u2022 Covered by enterprise data processing agreement",
      "\u2022 Not used to train Microsoft\u2019s models",
      "\u2022 Audit logs available to IT administrators",
      "\u2022 Appropriate for internal BP content (non-market-sensitive)",
    ];
    s.addText(m365Lines.join("\n"), {
      x: 0.45, y: cardY + 1.42, w: cardW - 0.3, h: cardH - 1.55,
      fontFace: "Calibri",
      fontSize: 8.5,
      color: C.textDark,
      align: "left",
      valign: "top",
      wrap: true,
    });

    // Right — External Tools
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

    s.addText(
      "Data is sent to third-party servers governed by individual terms of service \u2014 not BP\u2019s enterprise agreements. Training data opt-out varies by tool and subscription plan. For FM\u0026I: use external tools only for code logic, generic patterns, and publicly available information. Any internal data carries a compliance risk with these tools.",
      {
        x: 5.25, y: cardY + 0.42, w: cardW - 0.3, h: 0.9,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    const externalLines = [
      "\u2022 Data sent to third-party servers",
      "\u2022 Covered by individual terms of service only",
      "\u2022 Training data opt-out varies by tool and plan",
      "\u2022 No BP enterprise data processing agreement by default",
      "\u2022 Use for code logic and public information only",
    ];
    s.addText(externalLines.join("\n"), {
      x: 5.25, y: cardY + 1.42, w: cardW - 0.3, h: cardH - 2.25,
      fontFace: "Calibri",
      fontSize: 8.5,
      color: C.textDark,
      align: "left",
      valign: "top",
      wrap: true,
    });

    s.addText(
      "Note: API-based access (e.g. via Claude API key) has stronger data handling terms \u2014 check current BP guidance for API use status before building API-based workflows.",
      {
        x: 5.25, y: cardY + 2.6, w: cardW - 0.3, h: 0.6,
        fontFace: "Calibri",
        fontSize: 8,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
        italic: true,
      }
    );

    h.bottomBar(s, "Default to M365 Copilot for anything involving internal BP content; external tools for code logic and public information only");
  }

};
