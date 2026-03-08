module.exports = function buildS7toS10(pres, C, h) {

  // ============================================================
  // SECTION 7 — EXTENDED CONCEPTS
  // ============================================================

  // ----------------------------------------------------------
  // Slide 30: Section Divider — Extended Concepts
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    // Top accent bar
    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });

    // Section number
    s.addText("07", {
      x: 0.6, y: 1.2, w: 2, h: 0.8,
      fontFace: "Trebuchet MS",
      fontSize: 48,
      bold: true,
      color: C.teal,
      align: "left",
      valign: "middle",
    });

    // Section title
    s.addText("Extended Concepts", {
      x: 0.6, y: 2.1, w: 8.8, h: 0.65,
      fontFace: "Trebuchet MS",
      fontSize: 32,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    // Section subtitle
    s.addText("Claude Code, agentic AI, MCP, tool calling, agent skills, and what\u2019s next", {
      x: 0.6, y: 2.8, w: 8.8, h: 0.45,
      fontFace: "Calibri",
      fontSize: 14,
      color: C.textLight,
      align: "left",
      valign: "middle",
    });
  }

  // ----------------------------------------------------------
  // Slide 31: Claude Code — When the IDE Isn't Enough
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "CLAUDE CODE|OVERVIEW", "Claude Code: a CLI agent that works at the repository level, not the file level", C.teal);

    // Left card
    h.addCard(s, 0.3, 1.45, 4.55, 3.35, C.white);

    // Left card top accent
    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 1.45, w: 4.55, h: 0.05,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });

    // Left card header
    s.addText("What it is", {
      x: 0.45, y: 1.58, w: 4.25, h: 0.28,
      fontFace: "Trebuchet MS",
      fontSize: 11,
      bold: true,
      color: C.textDark,
      align: "left",
      valign: "top",
    });

    // Left card body paragraph 1
    s.addText(
      "A terminal-based AI agent. You run it in your project directory and it reads, writes, and executes across your entire codebase autonomously.\n\nNot a plugin \u2014 a separate process that can run for minutes or hours on a single instruction.",
      {
        x: 0.45, y: 1.92, w: 4.25, h: 1.3,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    // Left card body paragraph 2
    s.addText(
      "Key difference from GitHub Copilot/Cursor: it operates at project level, not file level. Give it a goal, it figures out the plan.",
      {
        x: 0.45, y: 3.3, w: 4.25, h: 0.8,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    // Right card
    h.addCard(s, 5.1, 1.45, 4.55, 3.35, C.white);

    // Right card top accent
    s.addShape(pres.ShapeType.rect, {
      x: 5.1, y: 1.45, w: 4.55, h: 0.05,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });

    // Right card header
    s.addText("Claude Code vs IDE tools", {
      x: 5.25, y: 1.58, w: 4.25, h: 0.28,
      fontFace: "Trebuchet MS",
      fontSize: 11,
      bold: true,
      color: C.textDark,
      align: "left",
      valign: "top",
    });

    // Table header row
    s.addShape(pres.ShapeType.rect, {
      x: 5.1, y: 1.92, w: 4.55, h: 0.28,
      fill: { color: C.navy },
      line: { color: C.navy, width: 0 },
    });

    s.addText("Feature", {
      x: 5.18, y: 1.92, w: 1.6, h: 0.28,
      fontFace: "Calibri",
      fontSize: 8,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    s.addText("Claude Code vs Copilot/Cursor", {
      x: 6.85, y: 1.92, w: 2.65, h: 0.28,
      fontFace: "Calibri",
      fontSize: 8,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    // Table rows
    const tableRows = [
      { feature: "Scope",    detail: "Full repo vs current file" },
      { feature: "Autonomy", detail: "Goal-based vs suggestion-based" },
      { feature: "Best for", detail: "Complex multi-file builds vs inline assistance" },
      { feature: "Running",  detail: "Terminal / background vs IDE panel" },
      { feature: "Cowork",   detail: "Team collaboration + session sharing" },
    ];

    tableRows.forEach(function(row, i) {
      const rowY = 1.92 + 0.28 + i * 0.42;
      const rowFill = i % 2 === 0 ? C.offWhite : C.white;

      s.addShape(pres.ShapeType.rect, {
        x: 5.1, y: rowY, w: 4.55, h: 0.42,
        fill: { color: rowFill },
        line: { color: C.divider, width: 0.5 },
      });

      s.addText(row.feature, {
        x: 5.18, y: rowY + 0.04, w: 1.6, h: 0.34,
        fontFace: "Calibri",
        fontSize: 8,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "middle",
        wrap: true,
      });

      s.addText(row.detail, {
        x: 6.85, y: rowY + 0.04, w: 2.65, h: 0.34,
        fontFace: "Calibri",
        fontSize: 8,
        color: C.textMed,
        align: "left",
        valign: "middle",
        wrap: true,
      });
    });

    h.bottomBar(s, "Claude Code unlocks workflows that take 10 minutes to describe and 2 hours to build autonomously \u2014 while you do something else");
  }

  // ----------------------------------------------------------
  // Slide 32: [LIVE DEMO] See It In Action — Claude Code
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "CLAUDE CODE|SEE IT IN ACTION", "[LIVE DEMO] Full pipeline audit \u2014 autonomous, 12 minutes", C.teal);

    // Dark header bar
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
      "Audit our Brent futures fundamental model: find all hardcoded magic numbers, write docstrings for undocumented functions, and generate a test suite for the ELT pipeline.",
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
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
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
      "1. Claude reads every file in the repository\n2. Identifies 23 magic numbers across 8 files\n3. Writes docstrings for 47 undocumented functions\n4. Generates 156 unit tests for the ELT pipeline\n5. Creates a markdown audit report with recommendations",
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

    // Right panel card
    h.addCard(s, 6.25, 2.45, 3.45, 2.35, C.white);

    // Big number
    s.addText("12 min", {
      x: 6.35, y: 2.55, w: 3.25, h: 0.7,
      fontFace: "Trebuchet MS",
      fontSize: 36,
      bold: true,
      color: C.teal,
      align: "center",
      valign: "middle",
    });

    // Label under big number
    s.addText("full codebase audit + test suite generated", {
      x: 6.35, y: 3.3, w: 3.25, h: 0.35,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.textMed,
      align: "center",
      valign: "middle",
      wrap: true,
    });

    // Manual comparison
    s.addText("Manual: 2\u20133 days", {
      x: 6.35, y: 3.72, w: 3.25, h: 0.3,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.red,
      align: "center",
      valign: "middle",
    });

    h.bottomBar(s, "[PRESENTER: open terminal and run \u2018claude\u2019 in the demo repo] \u2014 every model team has a codebase that needs this audit");
  }

  // ----------------------------------------------------------
  // Slide 33: Agentic AI — The Shift From Answering to Doing
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "AGENTIC AI|OVERVIEW", "The shift that happened in 2025: from answering questions to completing tasks", C.teal);

    // Left column stacked cards with left accent
    const agentItems = [
      {
        title: "What changed",
        body: "In 2024, AI tools answered questions. In 2025, they started completing multi-step tasks: reading files, running code, calling APIs, fixing errors, and reporting back.",
      },
      {
        title: "Why it matters for FM\u0026I",
        body: "An agent can: check Dataiku scenario status every morning, flag failed jobs, generate a diagnostic report, and message the team \u2014 without human intervention.",
      },
      {
        title: "What works reliably",
        body: "Deterministic tasks: code generation, file operations, API calls, report formatting. Agents are reliable when the steps are well-defined.",
      },
      {
        title: "What is still unreliable",
        body: "Open-ended reasoning chains > 10 steps. Tasks requiring real-world judgment. Anything where an error compounds silently.",
      },
    ];

    const leftX = 0.3;
    const leftW = 4.5;
    const itemH = 0.82;
    const itemGap = 0.1;
    let itemY = 1.45;

    agentItems.forEach(function(item) {
      h.addCard(s, leftX, itemY, leftW, itemH, C.white);

      // Left accent
      s.addShape(pres.ShapeType.rect, {
        x: leftX, y: itemY, w: 0.05, h: itemH,
        fill: { color: C.teal },
        line: { color: C.teal, width: 0 },
      });

      // Title
      s.addText(item.title, {
        x: leftX + 0.15, y: itemY + 0.06, w: leftW - 0.2, h: 0.22,
        fontFace: "Trebuchet MS",
        fontSize: 10,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      // Body
      s.addText(item.body, {
        x: leftX + 0.15, y: itemY + 0.3, w: leftW - 0.2, h: itemH - 0.35,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });

      itemY += itemH + itemGap;
    });

    // Right card — dark terminal style
    h.addCard(s, 5.1, 1.45, 4.6, 3.3, "1A1A2E");

    // Header row inside dark card
    s.addShape(pres.ShapeType.rect, {
      x: 5.1, y: 1.45, w: 4.6, h: 0.3,
      fill: { color: "2D3748" },
      line: { color: "2D3748", width: 0 },
    });

    s.addText("FM\u0026I agent example \u2014 morning pipeline monitor", {
      x: 5.2, y: 1.45, w: 4.4, h: 0.3,
      fontFace: "Trebuchet MS",
      fontSize: 9,
      bold: true,
      color: C.textLight,
      align: "left",
      valign: "middle",
    });

    // Terminal body
    s.addText(
      "TRIGGER: Daily at 06:00\n\n1. Pull Dataiku scenario run logs\n2. Identify any failures or warnings\n3. Cross-reference with expected schedule\n4. Generate diagnostic summary\n5. Post to Teams channel #fmi-ops",
      {
        x: 5.2, y: 1.82, w: 4.35, h: 2.8,
        fontFace: "Courier New",
        fontSize: 8.5,
        color: C.teal,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    h.bottomBar(s, "Reliable agentic workflows start with well-defined, deterministic tasks \u2014 the FM\u0026I pipeline monitor is a perfect first agent project");
  }

  // ----------------------------------------------------------
  // Slide 34: Tool Calling + MCP — How AI Connects to Your Systems
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "MCP|TOOL CALLING", "Tool calling and MCP: how AI agents connect to your data and systems", C.teal);

    // Left explanation card — Tool Calling
    h.addCard(s, 0.3, 1.45, 4.55, 1.1, C.white);

    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 1.45, w: 4.55, h: 0.05,
      fill: { color: C.cyan },
      line: { color: C.cyan, width: 0 },
    });

    s.addText("Tool Calling", {
      x: 0.45, y: 1.55, w: 4.25, h: 0.25,
      fontFace: "Trebuchet MS",
      fontSize: 10,
      bold: true,
      color: C.textDark,
      align: "left",
      valign: "top",
    });

    s.addText(
      "LLMs can invoke external functions, APIs, and services as part of generating a response. Instead of just answering, the model acts.",
      {
        x: 0.45, y: 1.82, w: 4.25, h: 0.65,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    // Right explanation card — MCP
    h.addCard(s, 5.1, 1.45, 4.55, 1.1, C.white);

    s.addShape(pres.ShapeType.rect, {
      x: 5.1, y: 1.45, w: 4.55, h: 0.05,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });

    s.addText("MCP (Model Context Protocol)", {
      x: 5.25, y: 1.55, w: 4.25, h: 0.25,
      fontFace: "Trebuchet MS",
      fontSize: 10,
      bold: true,
      color: C.textDark,
      align: "left",
      valign: "top",
    });

    s.addText(
      "An open standard for connecting LLMs to tools, databases, and services. One MCP server can give any compatible AI tool access to Dataiku, Bloomberg, internal APIs.",
      {
        x: 5.25, y: 1.82, w: 4.25, h: 0.65,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    // Demo section header bar
    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 2.65, w: 9.4, h: 0.3,
      fill: { color: "1E293B" },
      line: { color: "1E293B", width: 0 },
    });

    s.addText("MCP for Dataiku \u2014 what becomes possible:", {
      x: 0.4, y: 2.65, w: 9.2, h: 0.3,
      fontFace: "Calibri",
      fontSize: 9,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    // Terminal panel
    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 2.98, w: 9.4, h: 0.5,
      fill: { color: "1A1A2E" },
      line: { color: "1A1A2E", width: 0 },
    });

    s.addText(
      "Check all running Dataiku scenarios, identify any that failed in the last 24h, generate a diagnostic report with the last error log.",
      {
        x: 0.45, y: 3.0, w: 9.1, h: 0.46,
        fontFace: "Courier New",
        fontSize: 9,
        color: C.teal,
        align: "left",
        valign: "middle",
        wrap: true,
      }
    );

    // Bottom row: 3 FM&I-relevant MCP example cards
    const mcpCards = [
      {
        x: 0.3,
        title: "MCP for Dataiku",
        body: "Read/write pipelines, trigger scenarios, query logs",
      },
      {
        x: 3.6,
        title: "MCP for internal DB",
        body: "Query production data without copy-paste",
      },
      {
        x: 6.6,
        title: "MCP for Bloomberg",
        body: "Pull market data directly into AI context",
      },
    ];

    mcpCards.forEach(function(card) {
      h.addCard(s, card.x, 3.6, 3.0, 1.2, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: card.x, y: 3.6, w: 3.0, h: 0.05,
        fill: { color: C.teal },
        line: { color: C.teal, width: 0 },
      });

      s.addText(card.title, {
        x: card.x + 0.12, y: 3.7, w: 2.76, h: 0.25,
        fontFace: "Trebuchet MS",
        fontSize: 10,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      s.addText(card.body, {
        x: card.x + 0.12, y: 3.97, w: 2.76, h: 0.7,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });
    });

    h.bottomBar(s, "MCP turns isolated AI tools into connected agents \u2014 a Cursor session with Dataiku MCP can read pipeline status and suggest fixes without leaving the IDE");
  }

  // ----------------------------------------------------------
  // Slide 35: Agent Skills, Context & Tokens, Hooks
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "CONCEPTS|ADVANCED", "Agent skills, context management, and hooks \u2014 the power user layer", C.teal);

    const conceptCards = [
      {
        x: 0.3,
        accentColor: C.blue,
        title: "Agent Skills",
        body: "Reusable, packaged workflows you can invoke with a single slash command.\n\nExample: /data-quality-report generates a structured Dataiku pipeline output report automatically.\n\nHow to make one: write a markdown file defining the skill\u2019s trigger, steps, and output format.",
      },
      {
        x: 3.4,
        accentColor: C.orange,
        title: "Context & Tokens",
        body: "Quality degrades as context fills. Rules:\n\u2022 Use .cursorignore to exclude irrelevant files\n\u2022 Start new conversations for unrelated tasks\n\u2022 Large models cost ~$15/1M tokens \u2014 a 500-file repo in context = expensive\n\u2022 Compress long conversations manually before complex tasks",
      },
      {
        x: 6.5,
        accentColor: C.teal,
        title: "Hooks & Codex",
        body: "Claude Code hooks: shell commands that fire before/after tool calls. Use for: auto-formatting, git commits, Slack notifications on task completion.\n\nChatGPT Codex: OpenAI\u2019s cloud coding agent. Similar to Claude Code but runs in OpenAI\u2019s cloud environment.",
      },
    ];

    conceptCards.forEach(function(card) {
      h.addCard(s, card.x, 1.55, 2.9, 2.75, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: card.x, y: 1.55, w: 2.9, h: 0.05,
        fill: { color: card.accentColor },
        line: { color: card.accentColor, width: 0 },
      });

      s.addText(card.title, {
        x: card.x + 0.15, y: 1.65, w: 2.6, h: 0.28,
        fontFace: "Trebuchet MS",
        fontSize: 11,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      s.addText(card.body, {
        x: card.x + 0.15, y: 2.0, w: 2.6, h: 2.2,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });
    });

    h.bottomBar(s, "Agent skills + hooks = repeatable, automated workflows \u2014 the difference between a tool you use and a tool that works for you");
  }

  // ============================================================
  // SECTION 8 — PERSONAL USE CASES
  // ============================================================

  // ----------------------------------------------------------
  // Slide 36: Section Divider — Personal Use Cases
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    // Top accent bar
    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.blue },
      line: { color: C.blue, width: 0 },
    });

    // Section number
    s.addText("08", {
      x: 0.6, y: 1.2, w: 2, h: 0.8,
      fontFace: "Trebuchet MS",
      fontSize: 48,
      bold: true,
      color: C.blue,
      align: "left",
      valign: "middle",
    });

    // Section title
    s.addText("Personal Use Cases", {
      x: 0.6, y: 2.1, w: 8.8, h: 0.65,
      fontFace: "Trebuchet MS",
      fontSize: 32,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    // Section subtitle
    s.addText("Six real projects \u2014 what was built, how, and what it demonstrates", {
      x: 0.6, y: 2.8, w: 8.8, h: 0.45,
      fontFace: "Calibri",
      fontSize: 14,
      color: C.textLight,
      align: "left",
      valign: "middle",
    });
  }

  // ----------------------------------------------------------
  // Slide 37: Six Things Built With These Tools
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "PERSONAL|USE CASES", "Six real projects \u2014 what each one demonstrates about the tools", C.blue);

    const gridCards = [
      {
        x: 0.3, y: 1.45,
        accentColor: C.teal,
        title: "Claude Code + Remotion",
        body: "Used Claude Code to build programmatic video presentations \u2014 AI writes React code, Remotion renders it as video. Demo: automated video from a data summary.",
      },
      {
        x: 3.4, y: 1.45,
        accentColor: C.blue,
        title: "OpenClaw",
        body: "AI-powered chess analysis tool. Demonstrates: connecting LLM reasoning to a domain-specific knowledge base and structured game state.",
      },
      {
        x: 6.5, y: 1.45,
        accentColor: C.purple,
        title: "Claude Remote",
        body: "SSH + Claude Code for remote server workflows. Run autonomous AI agents on cloud VMs without an IDE \u2014 pure terminal productivity.",
      },
      {
        x: 0.3, y: 3.1,
        accentColor: C.cyan,
        title: "Claude Chrome Ext.",
        body: "Browser-native AI: summarise pages, extract structured data, run prompts on any web content. No copy-paste required.",
      },
      {
        x: 3.4, y: 3.1,
        accentColor: C.orange,
        title: "Weather Alerts",
        body: "Python project using Claude API: automated weather data pull \u2192 AI analysis \u2192 alert trigger \u2192 notification. Template for any API-to-alert workflow.",
      },
      {
        x: 6.5, y: 3.1,
        accentColor: C.green,
        title: "Claude Template Project",
        body: "This repo: CLAUDE.md + agents + skills + prompts = consistent AI output on every project. The _p-presentation-creator is a live demo.",
      },
    ];

    const cW = 2.9;
    const cH = 1.55;

    gridCards.forEach(function(card) {
      h.addCard(s, card.x, card.y, cW, cH, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: card.x, y: card.y, w: cW, h: 0.05,
        fill: { color: card.accentColor },
        line: { color: card.accentColor, width: 0 },
      });

      s.addText(card.title, {
        x: card.x + 0.15, y: card.y + 0.13, w: cW - 0.3, h: 0.28,
        fontFace: "Trebuchet MS",
        fontSize: 10,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      s.addText(card.body, {
        x: card.x + 0.15, y: card.y + 0.46, w: cW - 0.3, h: cH - 0.58,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });
    });

    h.bottomBar(s, "Every one of these was built in hours not days \u2014 the template project pattern is directly applicable to FM\u0026I Dataiku projects");
  }

  // ----------------------------------------------------------
  // Slide 38: The Template Project Pattern — Deep Dive
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "PERSONAL|TEMPLATE PROJECT", "The template project: make AI consistent across your whole team", C.blue);

    // Left: file tree card — dark terminal style
    h.addCard(s, 0.3, 1.45, 4.5, 3.35, "1A1A2E");

    // File tree header
    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 1.45, w: 4.5, h: 0.3,
      fill: { color: "2D3748" },
      line: { color: "2D3748", width: 0 },
    });

    s.addText("Project structure", {
      x: 0.45, y: 1.45, w: 4.2, h: 0.3,
      fontFace: "Trebuchet MS",
      fontSize: 9,
      bold: true,
      color: C.textLight,
      align: "left",
      valign: "middle",
    });

    // File tree body
    s.addText(
      "your-project/\n\u251C\u2500\u2500 CLAUDE.md          \u2190 project context & rules\n\u251C\u2500\u2500 .claude/\n\u2502   \u251C\u2500\u2500 agents/        \u2190 specialist sub-agents\n\u2502   \u251C\u2500\u2500 commands/      \u2190 slash commands\n\u2502   \u2514\u2500\u2500 skills/        \u2190 reusable workflows\n\u251C\u2500\u2500 .cursorrules       \u2190 Cursor equivalent\n\u2514\u2500\u2500 .github/\n    \u2514\u2500\u2500 copilot-instructions.md",
      {
        x: 0.45, y: 1.82, w: 4.2, h: 2.85,
        fontFace: "Courier New",
        fontSize: 8.5,
        color: C.teal,
        align: "left",
        valign: "top",
        wrap: false,
      }
    );

    // Right: stacked cards with left blue accent
    const templateItems = [
      {
        title: "CLAUDE.md / .cursorrules",
        body: "Tells the AI your architecture, conventions, forbidden patterns. Every session starts with the same context \u2014 no re-explaining.",
      },
      {
        title: "Agents directory",
        body: "Specialist sub-agents: a \u2018debugger\u2019 agent, a \u2018test-writer\u2019 agent, a \u2018docs\u2019 agent. Invoke with /agent debugger.",
      },
      {
        title: "Skills directory",
        body: "Reusable workflows packaged as slash commands. /data-quality-report runs the same 10-step process every time.",
      },
      {
        title: "For FM\u0026I",
        body: "A Dataiku project template with CLAUDE.md describing your pipeline patterns \u2014 every new recipe gets consistent AI assistance.",
      },
    ];

    const rightX = 5.1;
    const rightW = 4.6;
    const tItemH = 0.9;
    const tItemGap = 0.1;
    let tItemY = 1.45;

    templateItems.forEach(function(item) {
      h.addCard(s, rightX, tItemY, rightW, tItemH, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: rightX, y: tItemY, w: 0.05, h: tItemH,
        fill: { color: C.blue },
        line: { color: C.blue, width: 0 },
      });

      s.addText(item.title, {
        x: rightX + 0.15, y: tItemY + 0.06, w: rightW - 0.2, h: 0.24,
        fontFace: "Trebuchet MS",
        fontSize: 10,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      s.addText(item.body, {
        x: rightX + 0.15, y: tItemY + 0.32, w: rightW - 0.2, h: tItemH - 0.37,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });

      tItemY += tItemH + tItemGap;
    });

    h.bottomBar(s, "Set this up once for your FM\u0026I projects and every AI tool \u2014 Cursor, GitHub Copilot, Claude Code \u2014 becomes immediately useful to anyone on the team");
  }

  // ============================================================
  // SECTION 9 — BUSINESS USE CASES
  // ============================================================

  // ----------------------------------------------------------
  // Slide 39: Section Divider — Business Use Cases
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
    s.addText("09", {
      x: 0.6, y: 1.2, w: 2, h: 0.8,
      fontFace: "Trebuchet MS",
      fontSize: 48,
      bold: true,
      color: C.green,
      align: "left",
      valign: "middle",
    });

    // Section title
    s.addText("Business Use Cases", {
      x: 0.6, y: 2.1, w: 8.8, h: 0.65,
      fontFace: "Trebuchet MS",
      fontSize: 32,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    // Section subtitle
    s.addText("Commercial opportunities for FM\u0026I \u2014 and how to prepare for Innovation Day", {
      x: 0.6, y: 2.8, w: 8.8, h: 0.45,
      fontFace: "Calibri",
      fontSize: 14,
      color: C.textLight,
      align: "left",
      valign: "middle",
    });
  }

  // ----------------------------------------------------------
  // Slide 40: Four Platform Opportunities Ready to Explore
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "BUSINESS|PLATFORMS", "Four AI-enhanced platforms directly relevant to FM\u0026I workflows", C.green);

    const platformCards = [
      {
        x: 0.3, y: 1.45,
        accentColor: C.blue,
        title: "Copilot for Power BI",
        body: "Natural language queries over your dashboards. Ask: \u2018Show me crack spread volatility vs same period last year\u2019 \u2014 no SQL required. Available now in Power BI Premium.",
      },
      {
        x: 5.1, y: 1.45,
        accentColor: C.purple,
        title: "Plotly Studio",
        body: "AI-assisted interactive visualisation builder. Describe the chart, Plotly Studio writes the Dash code. Directly relevant to FM\u0026I\u2019s ad hoc analysis output.",
      },
      {
        x: 0.3, y: 3.15,
        accentColor: C.teal,
        title: "Dataiku LLM Mesh",
        body: "Dataiku\u2019s built-in LLM integration: code generation in recipes, AI-assisted pipeline debugging, natural language to SQL in dataset views. Currently in limited preview.",
      },
      {
        x: 5.1, y: 3.15,
        accentColor: C.orange,
        title: "MCP for Dataiku",
        body: "Connect Cursor or Claude Code directly to your Dataiku instance via MCP: read scenario status, trigger runs, query job logs \u2014 all from your AI tool. Community server available.",
      },
    ];

    const cW = 4.55;
    const cH = 1.6;

    platformCards.forEach(function(card) {
      h.addCard(s, card.x, card.y, cW, cH, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: card.x, y: card.y, w: cW, h: 0.05,
        fill: { color: card.accentColor },
        line: { color: card.accentColor, width: 0 },
      });

      s.addText(card.title, {
        x: card.x + 0.15, y: card.y + 0.13, w: cW - 0.3, h: 0.28,
        fontFace: "Trebuchet MS",
        fontSize: 11,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      s.addText(card.body, {
        x: card.x + 0.15, y: card.y + 0.47, w: cW - 0.3, h: cH - 0.6,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });
    });

    h.bottomBar(s, "All four are available or in preview today \u2014 the MCP for Dataiku integration is the highest-leverage near-term experiment for FM\u0026I");
  }

  // ----------------------------------------------------------
  // Slide 41: FM&I Commercial Use Case Ideas — Innovation Day Starter
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "BUSINESS|IDEAS", "20 commercial ideas for the Innovation Day board \u2014 your starting point", C.green);

    // Outer card
    h.addCard(s, 0.3, 1.45, 9.4, 3.35, C.white);

    // Left column header 1 — Data & Modelling
    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 1.45, w: 4.5, h: 0.28,
      fill: { color: C.green },
      line: { color: C.green, width: 0 },
    });

    s.addText("Data & Modelling", {
      x: 0.45, y: 1.45, w: 4.2, h: 0.28,
      fontFace: "Trebuchet MS",
      fontSize: 10,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    s.addText(
      "\u2022 Automated model documentation from code\n\u2022 AI-assisted half-life estimator calibration\n\u2022 Anomaly detection agent for ELT pipeline outputs\n\u2022 Automated test generation for fundamental models\n\u2022 Natural language interface for model scenario queries",
      {
        x: 0.45, y: 1.78, w: 4.2, h: 1.1,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    // Left column header 2 — Trading Desk Support
    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 2.98, w: 4.5, h: 0.26,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });

    s.addText("Trading Desk Support", {
      x: 0.45, y: 2.98, w: 4.2, h: 0.26,
      fontFace: "Trebuchet MS",
      fontSize: 10,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    s.addText(
      "\u2022 Morning briefing agent: overnight data summary + alerts\n\u2022 Ad hoc chart generator from desk requests\n\u2022 Automated spread analysis commentary",
      {
        x: 0.45, y: 3.28, w: 4.2, h: 0.9,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    // Vertical divider
    s.addShape(pres.ShapeType.rect, {
      x: 4.78, y: 1.45, w: 0.04, h: 3.35,
      fill: { color: C.divider },
      line: { color: C.divider, width: 0 },
    });

    // Right column header 1 — Platform & Integration
    s.addShape(pres.ShapeType.rect, {
      x: 4.82, y: 1.45, w: 4.88, h: 0.28,
      fill: { color: C.blue },
      line: { color: C.blue, width: 0 },
    });

    s.addText("Platform & Integration", {
      x: 4.97, y: 1.45, w: 4.58, h: 0.28,
      fontFace: "Trebuchet MS",
      fontSize: 10,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    s.addText(
      "\u2022 MCP server for Dataiku scenario monitoring\n\u2022 Power BI Copilot for FM\u0026I dashboard queries\n\u2022 Plotly Studio for rapid visualisation prototyping\n\u2022 AI-assisted Dataiku recipe optimisation",
      {
        x: 4.97, y: 1.78, w: 4.58, h: 1.1,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    // Right column header 2 — Process & Workflow
    s.addShape(pres.ShapeType.rect, {
      x: 4.82, y: 2.98, w: 4.88, h: 0.26,
      fill: { color: C.orange },
      line: { color: C.orange, width: 0 },
    });

    s.addText("Process & Workflow", {
      x: 4.97, y: 2.98, w: 4.58, h: 0.26,
      fontFace: "Trebuchet MS",
      fontSize: 10,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    s.addText(
      "\u2022 Meeting action item extractor (Copilot)\n\u2022 Automated model review report generation\n\u2022 Research synthesis agent for market reports\n\u2022 Data quality monitoring agent with Slack alerts",
      {
        x: 4.97, y: 3.28, w: 4.58, h: 0.9,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    h.bottomBar(s, "Pick your highest-impact idea from this list \u2014 bring it to Innovation Day with: what it does, what data it needs, who benefits");
  }

  // ============================================================
  // SECTION 10 — PHILOSOPHY & CLOSE
  // ============================================================

  // ----------------------------------------------------------
  // Slide 42: Section Divider — Closing Thoughts
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    // Top accent bar
    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: "475569" },
      line: { color: "475569", width: 0 },
    });

    // Section number
    s.addText("10", {
      x: 0.6, y: 1.2, w: 2, h: 0.8,
      fontFace: "Trebuchet MS",
      fontSize: 48,
      bold: true,
      color: "475569",
      align: "left",
      valign: "middle",
    });

    // Section title
    s.addText("Closing Thoughts", {
      x: 0.6, y: 2.1, w: 8.8, h: 0.65,
      fontFace: "Trebuchet MS",
      fontSize: 32,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    // Section subtitle
    s.addText("Three uncomfortable truths about where this is all going", {
      x: 0.6, y: 2.8, w: 8.8, h: 0.45,
      fontFace: "Calibri",
      fontSize: 14,
      color: C.textLight,
      align: "left",
      valign: "middle",
    });
  }

  // ----------------------------------------------------------
  // Slide 43: Statement Slide 1
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.deepNavy };

    // Top accent bar full-width
    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });

    // Large statement text
    s.addText(
      "AI isn\u2019t making data scientists obsolete.\nIt\u2019s making the ones who don\u2019t use it obsolete.",
      {
        x: 0.6, y: 0.9, w: 8.8, h: 1.4,
        fontFace: "Trebuchet MS",
        fontSize: 30,
        bold: true,
        color: C.white,
        align: "left",
        valign: "middle",
        lineSpacingMultiple: 1.3,
        wrap: true,
      }
    );

    // Horizontal rule
    s.addShape(pres.ShapeType.rect, {
      x: 0.6, y: 2.5, w: 2.0, h: 0.04,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });

    // Supporting text
    s.addText(
      "The productivity gap between AI-adopters and non-adopters in technical fields is measurable and growing. Teams that build AI into their workflows are shipping 2-3\u00d7 more models per sprint. The skill that matters now is judgment \u2014 knowing when the AI output is wrong, and how to fix it.",
      {
        x: 0.6, y: 2.7, w: 8.8, h: 1.4,
        fontFace: "Calibri",
        fontSize: 14,
        color: C.textLight,
        align: "left",
        valign: "top",
        lineSpacingMultiple: 1.4,
        wrap: true,
      }
    );
  }

  // ----------------------------------------------------------
  // Slide 44: Statement Slide 2
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.deepNavy };

    // Top accent bar
    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.orange },
      line: { color: C.orange, width: 0 },
    });

    // Statement
    s.addText(
      "The next decade won\u2019t kill technology jobs.\nIt will kill the comfortable middle.",
      {
        x: 0.6, y: 0.9, w: 8.8, h: 1.6,
        fontFace: "Trebuchet MS",
        fontSize: 30,
        bold: true,
        color: C.white,
        align: "left",
        valign: "middle",
        lineSpacingMultiple: 1.3,
        wrap: true,
      }
    );

    // Horizontal rule
    s.addShape(pres.ShapeType.rect, {
      x: 0.6, y: 2.7, w: 2.0, h: 0.04,
      fill: { color: C.orange },
      line: { color: C.orange, width: 0 },
    });

    // Supporting text
    s.addText(
      "People who confused shipping software with owning outcomes. The IT middle layer that never understood the subject domain well enough to be irreplaceable. Medicine, law, accounting, energy trading analytics \u2014 AI is replacing the translator layer, not the domain expert. The people who deeply understand fundamentals modelling and can direct AI to solve commercial problems are more valuable, not less.",
      {
        x: 0.6, y: 2.9, w: 8.8, h: 1.6,
        fontFace: "Calibri",
        fontSize: 13,
        color: C.textLight,
        align: "left",
        valign: "top",
        lineSpacingMultiple: 1.4,
        wrap: true,
      }
    );
  }

  // ----------------------------------------------------------
  // Slide 45: Statement Slide 3
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.deepNavy };

    // Top accent bar
    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.red },
      line: { color: C.red, width: 0 },
    });

    // Statement
    s.addText(
      "The question isn\u2019t whether\nthe AI wrote the code.\nThe question is: who owns the risk?",
      {
        x: 0.6, y: 0.9, w: 8.8, h: 1.6,
        fontFace: "Trebuchet MS",
        fontSize: 28,
        bold: true,
        color: C.white,
        align: "left",
        valign: "middle",
        lineSpacingMultiple: 1.3,
        wrap: true,
      }
    );

    // Horizontal rule
    s.addShape(pres.ShapeType.rect, {
      x: 0.6, y: 2.8, w: 2.0, h: 0.04,
      fill: { color: C.red },
      line: { color: C.red, width: 0 },
    });

    // Supporting text
    s.addText(
      "That\u2019s still you. The performance art around coding \u2014 requirements ceremonies, architecture slideware, digital transformation slogans, AI wrappers \u2014 doesn\u2019t answer the hard question. When the fundamental model gives a bad signal and the trading desk acts on it, someone owns that. Build AI into your workflow. But own the output.",
      {
        x: 0.6, y: 3.0, w: 8.8, h: 1.5,
        fontFace: "Calibri",
        fontSize: 13,
        color: C.textLight,
        align: "left",
        valign: "top",
        lineSpacingMultiple: 1.4,
        wrap: true,
      }
    );
  }

  // ----------------------------------------------------------
  // Slide 46: Closing CTA
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    // Top accent bar
    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });

    // Title
    s.addText("Three things to do before Innovation Day", {
      x: 0.6, y: 0.3, w: 8.8, h: 0.6,
      fontFace: "Trebuchet MS",
      fontSize: 28,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    // CTA cards
    const ctaCards = [
      {
        x: 0.3,
        accentColor: C.teal,
        num: "01",
        numColor: C.teal,
        title: "Request your licence",
        body: "GitHub Copilot via IT portal. Cursor via expense or IT. Takes 10 minutes.",
        sub: "Already have M365? Copilot is already on.",
      },
      {
        x: 3.6,
        accentColor: C.blue,
        num: "02",
        numColor: C.blue,
        title: "Run one real task",
        body: "Pick a task you\u2019re doing this week. Use an AI tool for it. Time how long it takes. Compare.",
        sub: "Start with something you\u2019d normally spend 30+ minutes on.",
      },
      {
        x: 6.6,
        accentColor: C.green,
        num: "03",
        numColor: C.green,
        title: "Bring your best idea",
        body: "Pick one commercial use case from today\u2019s session. Bring it to Innovation Day with: what it does, what data it needs, who benefits.",
        sub: "The evaluation matrix is in the innovation_day_board.md",
      },
    ];

    ctaCards.forEach(function(card) {
      // Card background
      h.addCard(s, card.x, 1.1, 2.9, 3.2, "1E293B");

      // Top accent bar
      s.addShape(pres.ShapeType.rect, {
        x: card.x, y: 1.1, w: 2.9, h: 0.05,
        fill: { color: card.accentColor },
        line: { color: card.accentColor, width: 0 },
      });

      // Number
      s.addText(card.num, {
        x: card.x + 0.15, y: 1.22, w: 2.6, h: 0.55,
        fontFace: "Trebuchet MS",
        fontSize: 24,
        bold: true,
        color: card.numColor,
        align: "left",
        valign: "top",
      });

      // Title
      s.addText(card.title, {
        x: card.x + 0.15, y: 1.82, w: 2.6, h: 0.32,
        fontFace: "Trebuchet MS",
        fontSize: 12,
        bold: true,
        color: C.white,
        align: "left",
        valign: "top",
      });

      // Body
      s.addText(card.body, {
        x: card.x + 0.15, y: 2.2, w: 2.6, h: 1.45,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textLight,
        align: "left",
        valign: "top",
        wrap: true,
      });

      // Sub note
      s.addText(card.sub, {
        x: card.x + 0.15, y: 3.75, w: 2.6, h: 0.4,
        fontFace: "Calibri",
        fontSize: 8,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });
    });

    // Bottom closing statement
    s.addText(
      "You already have the tools. The only thing between you and 10\u00d7 productivity is knowing which one to reach for and when.",
      {
        x: 0.6, y: 4.7, w: 8.8, h: 0.35,
        fontFace: "Calibri",
        fontSize: 10,
        color: C.textLight,
        align: "center",
        valign: "middle",
        wrap: true,
      }
    );
  }

};
