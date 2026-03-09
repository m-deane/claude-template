// slides_s7_s10_v5.cjs
// v5 change: New Slide 40 "Your First 30 Minutes" action guide inserted after Template Project slide

module.exports = function buildS7toS10(pres, C, h) {

  // ============================================================
  // SECTION 7 — EXTENDED CONCEPTS
  // ============================================================

  // ----------------------------------------------------------
  // Slide 31: Section Divider — Extended Concepts
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });

    s.addText("07", {
      x: 0.6, y: 1.2, w: 2, h: 0.8,
      fontFace: "Trebuchet MS",
      fontSize: 48,
      bold: true,
      color: C.teal,
      align: "left",
      valign: "middle",
    });

    s.addText("Extended Concepts", {
      x: 0.6, y: 2.1, w: 8.8, h: 0.65,
      fontFace: "Trebuchet MS",
      fontSize: 32,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

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
  // Slide 32: Claude Code — Repository-Level, Not File-Level
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "CLAUDE CODE|OVERVIEW", "Claude Code: a CLI agent that works at the repository level, not the file level", C.teal);

    const cardW = 4.55;
    const cardH = 3.35;
    const cardY = 1.45;

    // Left card
    h.addCard(s, 0.3, cardY, cardW, cardH, C.white);

    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: cardY, w: cardW, h: 0.05,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });

    s.addText("What it is and why it\u2019s different", {
      x: 0.45, y: cardY + 0.1, w: cardW - 0.3, h: 0.28,
      fontFace: "Trebuchet MS",
      fontSize: 10,
      bold: true,
      color: C.textDark,
      align: "left",
      valign: "top",
    });

    s.addText(
      "Claude Code is a terminal-based AI agent \u2014 not a plugin, not a chat window, but a separate process that runs in your project directory and can read, write, and execute across your entire codebase autonomously.\n\nThe key differentiator from GitHub Copilot and Cursor: it operates at repository level, not file level. When you give it a goal, it figures out which files to touch, in what order, and how to verify the result.\n\nThree things you can do with Claude Code that you literally cannot do in IDE tools:\n\u2022 Run it overnight on a cloud VM \u2014 no GUI required, no user at the keyboard\n\u2022 Invoke it from a CI/CD pipeline as an automated step\n\u2022 Script it via the Claude SDK as one agent in a larger orchestration system",
      {
        x: 0.45, y: cardY + 0.45, w: cardW - 0.3, h: cardH - 0.6,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    // Right card — comparison table
    h.addCard(s, 5.1, cardY, cardW, cardH, C.white);

    s.addShape(pres.ShapeType.rect, {
      x: 5.1, y: cardY, w: cardW, h: 0.05,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });

    s.addText("Claude Code vs IDE tools \u2014 practical comparison", {
      x: 5.25, y: cardY + 0.1, w: cardW - 0.3, h: 0.28,
      fontFace: "Trebuchet MS",
      fontSize: 10,
      bold: true,
      color: C.textDark,
      align: "left",
      valign: "top",
    });

    s.addShape(pres.ShapeType.rect, {
      x: 5.1, y: cardY + 0.44, w: cardW, h: 0.28,
      fill: { color: C.navy },
      line: { color: C.navy, width: 0 },
    });
    s.addText("Feature", {
      x: 5.18, y: cardY + 0.44, w: 1.5, h: 0.28,
      fontFace: "Calibri",
      fontSize: 8,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });
    s.addText("Copilot/Cursor", {
      x: 6.72, y: cardY + 0.44, w: 1.3, h: 0.28,
      fontFace: "Calibri",
      fontSize: 8,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });
    s.addText("Claude Code", {
      x: 8.08, y: cardY + 0.44, w: 1.5, h: 0.28,
      fontFace: "Calibri",
      fontSize: 8,
      bold: true,
      color: C.teal,
      align: "left",
      valign: "middle",
    });

    const tableRows = [
      { feature: "Scope",    left: "Current or open files",      right: "Entire repository" },
      { feature: "Autonomy", left: "Suggestion-based",           right: "Goal-based, verifies" },
      { feature: "Runtime",  left: "IDE open, user watching",    right: "Headless, runs alone" },
      { feature: "Overnight",left: "Not possible",               right: "Yes \u2014 run on VM" },
      { feature: "CI/CD",    left: "Not applicable",             right: "Yes \u2014 scriptable" },
    ];

    tableRows.forEach(function(row, i) {
      const rowY = cardY + 0.44 + 0.28 + i * 0.44;
      const rowFill = i % 2 === 0 ? C.offWhite : C.white;

      s.addShape(pres.ShapeType.rect, {
        x: 5.1, y: rowY, w: cardW, h: 0.44,
        fill: { color: rowFill },
        line: { color: C.divider, width: 0.5 },
      });

      s.addText(row.feature, {
        x: 5.18, y: rowY + 0.04, w: 1.46, h: 0.36,
        fontFace: "Calibri",
        fontSize: 8,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "middle",
        wrap: true,
      });
      s.addText(row.left, {
        x: 6.72, y: rowY + 0.04, w: 1.3, h: 0.36,
        fontFace: "Calibri",
        fontSize: 8,
        color: C.textMed,
        align: "left",
        valign: "middle",
        wrap: true,
      });
      s.addText(row.right, {
        x: 8.08, y: rowY + 0.04, w: 1.48, h: 0.36,
        fontFace: "Calibri",
        fontSize: 8,
        color: C.teal,
        bold: true,
        align: "left",
        valign: "middle",
        wrap: true,
      });
    });

    h.bottomBar(s, "Claude Code unlocks workflows that take 10 minutes to describe and 2 hours to build autonomously \u2014 while you do something else");
  }

  // ----------------------------------------------------------
  // Slide 33: [LIVE DEMO] Full Pipeline Audit — 12 Minutes
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "CLAUDE CODE|SEE IT IN ACTION", "[LIVE DEMO] Full pipeline audit \u2014 autonomous, 12 minutes", C.teal);

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
      "Audit our Brent futures fundamental model: find all hardcoded magic numbers and replace with named constants, write NumPy docstrings for every undocumented function, generate a pytest test suite for the ELT pipeline, and create a MODEL.md covering inputs, outputs, calibration approach, and known limitations.",
      {
        x: 0.45, y: 1.8, w: 9.1, h: 0.51,
        fontFace: "Courier New",
        fontSize: 8.5,
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
      "1. Claude reads every file in the repository \u2014 recipes, models, tests, configs\n2. Identifies 23 magic numbers across 8 files, extracts them to a constants.py module\n3. Writes NumPy-format docstrings for 47 undocumented functions\n4. Generates 156 unit tests for the ELT pipeline covering normal cases and edge cases\n5. Creates MODEL.md with sections: Overview, Data Sources, Calibration Approach, Known Limitations, Changelog",
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

    s.addText("12 min", {
      x: 6.35, y: 2.55, w: 3.25, h: 0.6,
      fontFace: "Trebuchet MS",
      fontSize: 36,
      bold: true,
      color: C.teal,
      align: "center",
      valign: "middle",
    });

    s.addText("full codebase audit + test suite + documentation generated", {
      x: 6.35, y: 3.2, w: 3.25, h: 0.38,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.textMed,
      align: "center",
      valign: "middle",
      wrap: true,
    });

    s.addText("Manual: 2\u20133 days", {
      x: 6.35, y: 3.65, w: 3.25, h: 0.3,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.red,
      align: "center",
      valign: "middle",
    });

    h.bottomBar(s, "[PRESENTER: open terminal and run \u2018claude\u2019 in the demo repo] \u2014 every model team has a codebase that needs exactly this audit");
  }

  // ----------------------------------------------------------
  // Slide 34: Agentic AI — The Shift from Answering to Doing
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "AGENTIC AI|OVERVIEW", "The shift that happened in 2025: from answering questions to completing tasks", C.teal);

    const agentItems = [
      {
        title: "What changed",
        body: "In 2024, AI tools answered questions. In 2025, they started completing multi-step tasks \u2014 reading files, running code, calling APIs, fixing errors, and reporting back \u2014 without human intervention at each step. Enabled by three simultaneous advances: reliable tool calling, context windows large enough to hold task state, and infrastructure mature enough to manage agent orchestration.",
      },
      {
        title: "Why it matters for FM\u0026I",
        body: "An agent can check Dataiku scenario status every morning, flag failed jobs, generate a diagnostic report comparing actual vs expected outputs, and post the results to the FM\u0026I Teams channel \u2014 all triggered by a scheduled cron job with no human in the execution loop. The analyst sets the rules and reviews the output. The agent does the daily monitoring.",
      },
      {
        title: "What works reliably today",
        body: "Well-defined, deterministic tasks where the steps are clear and success criteria are checkable: code generation, file operations, test running, report formatting, API calls. Agents are reliable when errors are detectable and recoverable \u2014 a failing test gives the agent clear feedback to correct on. Start with these tasks before moving to open-ended reasoning chains.",
      },
      {
        title: "What is still unreliable",
        body: "Reasoning chains longer than 10-15 steps accumulate errors \u2014 each step has a small failure probability that compounds. Tasks requiring accurate real-world knowledge are risky because hallucination grows with knowledge specificity. Tasks with ambiguous success criteria are unreliable because the agent may believe it has finished when it has not. Design in clear success criteria.",
      },
    ];

    const leftX = 0.3;
    const leftW = 4.5;
    const itemH = 0.82;
    const itemGap = 0.08;
    let itemY = 1.45;

    agentItems.forEach(function(item) {
      h.addCard(s, leftX, itemY, leftW, itemH, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: leftX, y: itemY, w: 0.05, h: itemH,
        fill: { color: C.teal },
        line: { color: C.teal, width: 0 },
      });

      s.addText(item.title, {
        x: leftX + 0.15, y: itemY + 0.06, w: leftW - 0.2, h: 0.22,
        fontFace: "Trebuchet MS",
        fontSize: 9.5,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

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

    // Right dark terminal card
    h.addCard(s, 5.1, 1.45, 4.6, 3.35, "1A1A2E");

    s.addShape(pres.ShapeType.rect, {
      x: 5.1, y: 1.45, w: 4.6, h: 0.3,
      fill: { color: "2D3748" },
      line: { color: "2D3748", width: 0 },
    });
    s.addText("FM\u0026I agent \u2014 morning pipeline monitor", {
      x: 5.2, y: 1.45, w: 4.4, h: 0.3,
      fontFace: "Trebuchet MS",
      fontSize: 9,
      bold: true,
      color: C.textLight,
      align: "left",
      valign: "middle",
    });

    s.addText(
      "TRIGGER: Daily cron at 06:00 UTC\n\nStep 1: Pull Dataiku scenario run logs\n        for all FM\u0026I projects\nStep 2: Compare actual run times vs\n        expected schedule\nStep 3: Flag any failures or >2hr delays\nStep 4: Cross-reference with expected\n        data volumes (anomaly check)\nStep 5: Generate diagnostic summary\n        with error logs for failures\nStep 6: Post to Teams #fmi-ops channel\n\nOUTPUT: Morning brief ready by 06:15",
      {
        x: 5.2, y: 1.82, w: 4.35, h: 2.85,
        fontFace: "Courier New",
        fontSize: 8.5,
        color: C.teal,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    h.bottomBar(s, "Reliable agentic workflows start with well-defined, deterministic tasks \u2014 the FM\u0026I pipeline monitor is the perfect first agent project");
  }

  // ----------------------------------------------------------
  // Slide 35: Tool Calling and MCP — How AI Agents Connect to Your Systems
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "MCP|TOOL CALLING", "Tool calling and MCP: how AI agents connect to your data and systems", C.teal);

    // Top row — 2 explanation cards
    const topCardW = 4.55;
    const topCardH = 1.1;

    h.addCard(s, 0.3, 1.45, topCardW, topCardH, C.white);
    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 1.45, w: topCardW, h: 0.05,
      fill: { color: C.cyan },
      line: { color: C.cyan, width: 0 },
    });
    s.addText("Tool Calling", {
      x: 0.45, y: 1.55, w: topCardW - 0.3, h: 0.25,
      fontFace: "Trebuchet MS",
      fontSize: 10,
      bold: true,
      color: C.textDark,
      align: "left",
      valign: "top",
    });
    s.addText(
      "The ability for an LLM to invoke external functions, APIs, and services as part of generating a response. Instead of just outputting text, the model outputs structured instructions to call a function, receives the result, and incorporates it into the next reasoning step. This is what makes agentic workflows possible: the AI can take actions, not just describe them.",
      {
        x: 0.45, y: 1.82, w: topCardW - 0.3, h: 0.68,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    h.addCard(s, 5.1, 1.45, topCardW, topCardH, C.white);
    s.addShape(pres.ShapeType.rect, {
      x: 5.1, y: 1.45, w: topCardW, h: 0.05,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });
    s.addText("MCP (Model Context Protocol)", {
      x: 5.25, y: 1.55, w: topCardW - 0.3, h: 0.25,
      fontFace: "Trebuchet MS",
      fontSize: 10,
      bold: true,
      color: C.textDark,
      align: "left",
      valign: "top",
    });
    s.addText(
      "An open standard developed by Anthropic (November 2024) that defines a common interface between AI models and external tools. Think of it as USB for AI integrations \u2014 any MCP-compliant client (Cursor, Claude Code) can connect to any MCP-compliant server. One MCP server built for Dataiku can be used by every AI tool your team uses, with no bespoke integration work per tool.",
      {
        x: 5.25, y: 1.82, w: topCardW - 0.3, h: 0.68,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    // Demo section
    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 2.65, w: 9.4, h: 0.28,
      fill: { color: "1E293B" },
      line: { color: "1E293B", width: 0 },
    });
    s.addText("MCP for Dataiku \u2014 a step-by-step workflow:", {
      x: 0.4, y: 2.65, w: 9.2, h: 0.28,
      fontFace: "Calibri",
      fontSize: 9,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 2.96, w: 9.4, h: 0.38,
      fill: { color: "1A1A2E" },
      line: { color: "1A1A2E", width: 0 },
    });
    s.addText(
      "\"The gas_hub_prices recipe failed overnight. Get the last error log, read the recipe code, and propose a fix.\"",
      {
        x: 0.45, y: 2.98, w: 9.1, h: 0.34,
        fontFace: "Courier New",
        fontSize: 8.5,
        color: C.teal,
        align: "left",
        valign: "middle",
        wrap: true,
      }
    );

    // 3 bottom MCP cards
    const mcpCards = [
      {
        x: 0.3,
        title: "MCP for Dataiku",
        body: "Read pipeline status, trigger scenarios, query job logs, and write recipe fixes \u2014 all from within Cursor or Claude Code. A Cursor session with Dataiku MCP can diagnose a failed overnight run and propose a fix without the engineer opening the Dataiku UI. Community server already exists on GitHub: search mcp-server-dataiku.",
      },
      {
        x: 3.6,
        title: "MCP for databases",
        body: "Query your production database schema, run read-only analytical queries, and get schema documentation \u2014 all from your AI tool. The MCP enforces read-only access and you review every query before it runs. No copy-paste of query results into AI context required, eliminating the manual data extraction step.",
      },
      {
        x: 6.9,
        title: "MCP for market data",
        body: "Emerging MCP servers for financial data APIs allow AI tools to pull market data directly into their context. Ask \u201cwhat does the ICE Brent forward curve look like this morning?\u201d and Claude retrieves the data via MCP and responds with analysis \u2014 no manual download, no copy-paste into a chat window.",
      },
    ];

    mcpCards.forEach(function(card) {
      h.addCard(s, card.x, 3.44, 3.0, 1.35, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: card.x, y: 3.44, w: 3.0, h: 0.05,
        fill: { color: C.teal },
        line: { color: C.teal, width: 0 },
      });

      s.addText(card.title, {
        x: card.x + 0.12, y: 3.54, w: 2.76, h: 0.24,
        fontFace: "Trebuchet MS",
        fontSize: 9.5,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      s.addText(card.body, {
        x: card.x + 0.12, y: 3.8, w: 2.76, h: 0.92,
        fontFace: "Calibri",
        fontSize: 8,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });
    });

    h.bottomBar(s, "MCP turns isolated AI tools into connected agents \u2014 Cursor + Dataiku MCP can diagnose a failed pipeline without leaving the IDE");
  }

  // ----------------------------------------------------------
  // Slide 36: Agent Skills, Context Management, and Hooks
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
        body: "Reusable, packaged workflows invoked by a single slash command. Store in .claude/skills/ as markdown files. The FM\u0026I use case: /data-quality-report triggers a 10-step profiling process that produces the same structured output every time \u2014 row count, column profiles, null analysis, outlier detection, recommended actions \u2014 regardless of which analyst runs it. Build once, use consistently across the team.\n\nSkill file skeleton:\n# Skill: data-quality-report\nTrigger: /data-quality-report [dataset]\n\n## Instructions\n1. Profile: row count, column dtypes\n2. Per column: null %, unique vals, min/max\n3. Flag: >10% nulls, single unique val\n4. Output: markdown table + JSON + actions",
      },
      {
        x: 3.4,
        accentColor: C.orange,
        title: "Context \u0026 Tokens",
        body: "Quality degrades as context fills with irrelevant noise. Every token costs money \u2014 Claude Opus at $15/M input tokens means a 500-file codebase in context is expensive. Practical rules: use .cursorignore to exclude node_modules, __pycache__, and build outputs; start fresh conversations for unrelated tasks; compress long conversation histories before complex tasks by asking the AI to summarise what has been decided. Context discipline is as important as prompt quality.",
      },
      {
        x: 6.5,
        accentColor: C.teal,
        title: "Hooks \u0026 Automation",
        body: "Claude Code hooks fire shell commands before or after tool calls, enabling automated workflows without manual triggering. Examples: a post-write hook that runs black formatting after every file edit; a post-session hook that commits all changes to git with an AI-generated commit message and posts a summary to the team Slack channel; a pre-tool hook that validates the proposed edit against your .cursorrules before applying it. Hooks transform Claude Code from a tool you use to a tool that works for you.",
      },
    ];

    const cW = 2.9;
    const cH = 2.9;

    conceptCards.forEach(function(card) {
      h.addCard(s, card.x, 1.55, cW, cH, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: card.x, y: 1.55, w: cW, h: 0.05,
        fill: { color: card.accentColor },
        line: { color: card.accentColor, width: 0 },
      });

      s.addText(card.title, {
        x: card.x + 0.15, y: 1.65, w: cW - 0.3, h: 0.28,
        fontFace: "Trebuchet MS",
        fontSize: 11,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      s.addText(card.body, {
        x: card.x + 0.15, y: 2.0, w: cW - 0.3, h: cH - 0.52,
        fontFace: "Calibri",
        fontSize: 8,
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
  // Slide 37: Section Divider — Personal Use Cases
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.blue },
      line: { color: C.blue, width: 0 },
    });

    s.addText("08", {
      x: 0.6, y: 1.2, w: 2, h: 0.8,
      fontFace: "Trebuchet MS",
      fontSize: 48,
      bold: true,
      color: C.blue,
      align: "left",
      valign: "middle",
    });

    s.addText("Personal Use Cases", {
      x: 0.6, y: 2.1, w: 8.8, h: 0.65,
      fontFace: "Trebuchet MS",
      fontSize: 32,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    s.addText("Four real projects \u2014 what was built, how, and what it demonstrates", {
      x: 0.6, y: 2.8, w: 8.8, h: 0.45,
      fontFace: "Calibri",
      fontSize: 14,
      color: C.textLight,
      align: "left",
      valign: "middle",
    });
  }

  // ----------------------------------------------------------
  // Slide 38: Four Real Projects Built With These Tools
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "PERSONAL|USE CASES", "Four real projects \u2014 what each one demonstrates about the tools", C.blue);

    const gridCards = [
      {
        x: 0.3, y: 1.45,
        accentColor: C.teal,
        title: "Claude Code + Remotion: AI-generated video presentations",
        body: "Problem: converting weekly model performance numbers into a stakeholder briefing consumed 2+ hours of formatting and design work. Solution: Claude Code generates a React component for each slide, Remotion renders them as video frames, and the entire briefing is produced programmatically from a structured data source in a single command. What it demonstrates: AI can own the full creative and production workflow, not just assist with it. The same pattern applies to any FM\u0026I output that currently involves manual formatting.",
      },
      {
        x: 5.1, y: 1.45,
        accentColor: C.blue,
        title: "OpenClaw: domain-specific AI expertise",
        body: "An AI-powered chess analysis tool that connects an LLM to a structured position database and gives it tools to query positions, evaluate moves, and explain reasoning chains. The chess application is incidental \u2014 what OpenClaw demonstrates is the pattern: connect an LLM to a domain-specific knowledge base with well-defined tool access, and the model becomes a domain expert. The identical pattern applies to connecting a model to a commodity pricing database or a Dataiku recipe catalogue.",
      },
      {
        x: 0.3, y: 3.15,
        accentColor: C.purple,
        title: "Claude Remote: overnight VM workflows",
        body: "SSH-based workflow for running Claude Code autonomously on a remote cloud VM. Write the instruction, start the session over SSH, close the connection, and return the next morning to completed work. A full codebase refactor now runs autonomously overnight at a cost of approximately \u00a35-15 in API tokens. What it demonstrates: the \u201cAI as parallel team member\u201d concept at its fullest. The engineer\u2019s job shifts from executing to directing and reviewing.",
      },
      {
        x: 5.1, y: 3.15,
        accentColor: C.green,
        title: "Template Project: this presentation as a live example",
        body: "This presentation was built using the template project pattern. CLAUDE.md defines the project. .claude/agents/ contains 5 specialist agents \u2014 Research Lead, Content Architect, and three Section Builders. Each reads all prior outputs. The entire content and all code was generated in one agent-team session from a high-level brief. What it demonstrates: team-scale agentic workflows where each \u201cteam member\u201d is a specialised AI agent. Apply to FM\u0026I Dataiku projects for consistent AI assistance across every recipe.",
      },
    ];

    const cW = 4.4;
    const cH = 1.58;

    gridCards.forEach(function(card) {
      h.addCard(s, card.x, card.y, cW, cH, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: card.x, y: card.y, w: cW, h: 0.05,
        fill: { color: card.accentColor },
        line: { color: card.accentColor, width: 0 },
      });

      s.addText(card.title, {
        x: card.x + 0.15, y: card.y + 0.12, w: cW - 0.3, h: 0.28,
        fontFace: "Trebuchet MS",
        fontSize: 9.5,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      s.addText(card.body, {
        x: card.x + 0.15, y: card.y + 0.45, w: cW - 0.3, h: cH - 0.57,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });
    });

    h.bottomBar(s, "Every one of these was built in hours, not days \u2014 the template project pattern is directly applicable to FM\u0026I Dataiku projects");
  }

  // ----------------------------------------------------------
  // Slide 39: The Template Project — Make AI Consistent Across Your Whole Team
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "PERSONAL|TEMPLATE PROJECT", "The template project: make AI consistent across your whole team", C.blue);

    // Left — dark terminal file tree
    h.addCard(s, 0.3, 1.45, 4.5, 3.35, "1A1A2E");

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

    // Right — 4 stacked cards
    const templateItems = [
      {
        title: "CLAUDE.md / .cursorrules",
        body: "Persistent instructions to the AI about your project\u2019s architecture, conventions, and forbidden patterns. Every session starts with the same full context \u2014 no re-explaining your stack, no AI forgetting that your Dataiku environment requires Python 3.8. This single file eliminates 20-30% of the correction overhead in typical AI-assisted development.",
      },
      {
        title: "Agents directory",
        body: "Specialist sub-agents defined as markdown files \u2014 a \u2018debugger\u2019 agent, a \u2018test-writer\u2019 agent, a \u2018documentation\u2019 agent. Each has a specific scope, instructions, and output format. Invoked with /agent debugger. Rather than one general-purpose AI doing everything, you get focused specialists doing one thing very well.",
      },
      {
        title: "Skills directory",
        body: "Reusable workflows packaged as slash commands. /data-quality-report runs the same 10-step profiling process every time, in the same format, regardless of which team member runs it or what dataset they point it at. Build once, use consistently across the team. Quality becomes predictable, not dependent on who wrote the prompt.",
      },
      {
        title: "For FM\u0026I projects",
        body: "A Dataiku project template with CLAUDE.md describing your pipeline patterns, recipe conventions, data schema standards, and quality gates. Every new recipe \u2014 by any team member using GitHub Copilot, Cursor, or Claude Code \u2014 starts with the same complete project context. AI assistance becomes useful on day one rather than requiring weeks of customisation per engineer.",
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
        x: rightX + 0.15, y: tItemY + 0.06, w: rightW - 0.2, h: 0.23,
        fontFace: "Trebuchet MS",
        fontSize: 9.5,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      s.addText(item.body, {
        x: rightX + 0.15, y: tItemY + 0.31, w: rightW - 0.2, h: tItemH - 0.37,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });

      tItemY += tItemH + tItemGap;
    });

    h.bottomBar(s, "Set this up once and every AI tool \u2014 Cursor, GitHub Copilot, Claude Code \u2014 becomes immediately useful to any team member");
  }

  // ----------------------------------------------------------
  // Slide 40 (v5): Your First 30 Minutes — Start Here, Not There
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.deepNavy };

    // Top accent bar
    s.addShape(pres.ShapeType.rect, {x: 0, y: 0, w: 10, h: 0.06, fill: {color: C.orange}, line: {color: C.orange, width: 0}});

    // Tag pill
    s.addShape(pres.ShapeType.rect, {x: 0.4, y: 0.25, w: 1.4, h: 0.32, fill: {color: C.orange}, line: {color: C.orange, width: 0}});
    s.addText("ACTION GUIDE", {x: 0.4, y: 0.25, w: 1.4, h: 0.32, fontFace: "Trebuchet MS", fontSize: 8.5, bold: true, color: C.white, align: "center", valign: "middle", charSpacing: 1.5});

    // Slide title
    s.addText("Your first 30 minutes — start here, not there", {
      x: 0.4, y: 0.65, w: 9.2, h: 0.65,
      fontFace: "Trebuchet MS", fontSize: 28, bold: true, color: C.white,
      valign: "middle"
    });

    // Sub-title
    s.addText("Three actions, in order. Don't skip to step 3.", {
      x: 0.4, y: 1.3, w: 9.2, h: 0.3,
      fontFace: "Calibri", fontSize: 12, color: C.textLight,
      valign: "middle"
    });

    const actions = [
      {
        num: "01",
        time: "5 min",
        title: "Request your licence",
        body: "Microsoft Copilot: open Word or Teams right now — if the Copilot button is there, you already have it. If not, raise a standard IT ticket referencing 'M365 Copilot activation'. GitHub Copilot: IT self-service portal, search 'GitHub Copilot', submit — approval in 2-3 days, no manager sign-off required. Cursor: request via T&E as a business subscription (£20/month). Copilot Studio: use the justification template from Slide 11.",
        numColor: C.teal,
        accentColor: C.teal,
      },
      {
        num: "02",
        time: "15 min",
        title: "Run one real task — not a tutorial, not a demo",
        body: "Take an actual piece of work sitting in your backlog right now. If you have GitHub Copilot: open a Dataiku recipe that has an iterrows() loop, open VS Code, ask Copilot to rewrite it with polars. If you have Microsoft Copilot: paste the notes from your last model review meeting and ask for a structured brief with actions, decisions, and open questions. Do not follow a tutorial. Do the real thing. Bad first attempts are more valuable than perfect tutorials.",
        numColor: C.orange,
        accentColor: C.orange,
      },
      {
        num: "03",
        time: "10 min",
        title: "Learn from the output — then bring your best idea",
        body: "Read what it produced. Notice where it was right immediately, where it needed correction, where it surprised you. That calibration is worth more than any training module. Now write down one FM&I-specific use case you want to build or automate before the Innovation Day. Bring that idea to the mural board — not a generic 'use AI for data analysis' idea, but a specific: 'I want to build an agent that monitors our ELT pipeline scenarios and posts a health summary to Teams every morning at 07:30.'",
        numColor: C.green,
        accentColor: C.green,
      }
    ];

    const cardW = 2.95;
    const cardH = 2.95;
    const cardY = 1.72;

    actions.forEach(function(action, i) {
      const cardX = 0.3 + i * (cardW + 0.2);

      // Card background
      s.addShape(pres.ShapeType.rect, {x: cardX, y: cardY, w: cardW, h: cardH, fill: {color: "0D1B2E"}, line: {color: "1E3A5F", width: 1}});

      // Top accent bar
      s.addShape(pres.ShapeType.rect, {x: cardX, y: cardY, w: cardW, h: 0.05, fill: {color: action.accentColor}, line: {color: action.accentColor, width: 0}});

      // Number circle
      s.addShape(pres.ShapeType.rect, {x: cardX + 0.12, y: cardY + 0.12, w: 0.52, h: 0.52, fill: {color: action.numColor}, line: {color: action.numColor, width: 0}});
      s.addText(action.num, {x: cardX + 0.12, y: cardY + 0.12, w: 0.52, h: 0.52, fontFace: "Trebuchet MS", fontSize: 16, bold: true, color: C.white, align: "center", valign: "middle"});

      // Time badge
      s.addShape(pres.ShapeType.rect, {x: cardX + cardW - 0.75, y: cardY + 0.15, w: 0.65, h: 0.22, fill: {color: "1E3A5F"}, line: {color: "1E3A5F", width: 0}});
      s.addText(action.time, {x: cardX + cardW - 0.75, y: cardY + 0.15, w: 0.65, h: 0.22, fontFace: "Calibri", fontSize: 8, bold: true, color: action.accentColor, align: "center", valign: "middle"});

      // Title
      s.addText(action.title, {x: cardX + 0.12, y: cardY + 0.72, w: cardW - 0.24, h: 0.4, fontFace: "Trebuchet MS", fontSize: 10, bold: true, color: C.white, valign: "middle", wrap: true});

      // Divider
      s.addShape(pres.ShapeType.rect, {x: cardX + 0.12, y: cardY + 1.14, w: cardW - 0.24, h: 0.02, fill: {color: "1E3A5F"}, line: {color: "1E3A5F", width: 0}});

      // Body
      s.addText(action.body, {x: cardX + 0.12, y: cardY + 1.22, w: cardW - 0.24, h: 1.6, fontFace: "Calibri", fontSize: 7.5, color: C.textLight, valign: "top", wrap: true});
    });

    h.bottomBar(s, "The first 30 minutes matters more than the next 30 hours of watching demos — do the real thing, today, with a real task");
  }

  // ============================================================
  // SECTION 9 — BUSINESS USE CASES
  // ============================================================

  // ----------------------------------------------------------
  // Slide 41: Section Divider — Business Use Cases
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.green },
      line: { color: C.green, width: 0 },
    });

    s.addText("09", {
      x: 0.6, y: 1.2, w: 2, h: 0.8,
      fontFace: "Trebuchet MS",
      fontSize: 48,
      bold: true,
      color: C.green,
      align: "left",
      valign: "middle",
    });

    s.addText("Business Use Cases", {
      x: 0.6, y: 2.1, w: 8.8, h: 0.65,
      fontFace: "Trebuchet MS",
      fontSize: 32,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

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
  // Slide 42: Four AI-Enhanced Platforms Directly Relevant to FM&I
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
        body: "Natural language queries over your existing FM\u0026I dashboards \u2014 no SQL required. Ask \u201cshow me crack spread volatility versus the same period last year, filtered to ICE Brent\u201d and the report builds itself. For FM\u0026I, this transforms the trading desk interaction model: traders query the data directly rather than submitting a request to the analytics team. Available now in Power BI Premium, which BP already has access to.",
      },
      {
        x: 5.1, y: 1.45,
        accentColor: C.purple,
        title: "Plotly Studio",
        body: "AI-assisted interactive visualisation builder where you describe the chart you need and Plotly Studio generates the Dash code. For FM\u0026I\u2019s ad hoc analysis output, this compresses the visual delivery step from \u201cwrite the Dash code\u201d (30-90 minutes) to \u201cdescribe what I want and review the output\u201d (5 minutes). Particularly relevant for the crack spread and time spread visualisations that the trading desk requests frequently.",
      },
      {
        x: 0.3, y: 3.15,
        accentColor: C.teal,
        title: "Dataiku LLM Mesh",
        body: "Dataiku\u2019s native LLM integration, currently in limited preview for enterprise accounts. AI-assisted code generation directly in recipe editors, natural language to SQL in dataset views, and AI-powered pipeline debugging that reads the full recipe chain before suggesting fixes. When it reaches GA, it will be the most integrated AI tool for FM\u0026I Dataiku work \u2014 the AI understands the full Dataiku data model, not just the Python code.",
      },
      {
        x: 5.1, y: 3.15,
        accentColor: C.orange,
        title: "MCP for Dataiku",
        body: "Connect Cursor or Claude Code to your live Dataiku instance via an MCP server. Read scenario status, trigger runs, query job logs, and push recipe fixes \u2014 all from your AI tool without opening the Dataiku UI. The community MCP server already exists (search: mcp-server-dataiku on GitHub). The FM\u0026I team could deploy and test this in a half-day. This is the highest-leverage near-term experiment available.",
      },
    ];

    const cW = 4.4;
    const cH = 1.58;

    platformCards.forEach(function(card) {
      h.addCard(s, card.x, card.y, cW, cH, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: card.x, y: card.y, w: cW, h: 0.05,
        fill: { color: card.accentColor },
        line: { color: card.accentColor, width: 0 },
      });

      s.addText(card.title, {
        x: card.x + 0.15, y: card.y + 0.12, w: cW - 0.3, h: 0.28,
        fontFace: "Trebuchet MS",
        fontSize: 11,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      s.addText(card.body, {
        x: card.x + 0.15, y: card.y + 0.46, w: cW - 0.3, h: cH - 0.58,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });
    });

    h.bottomBar(s, "All four are available or in preview today \u2014 Dataiku MCP integration is the highest-leverage near-term experiment for FM\u0026I");
  }

  // ----------------------------------------------------------
  // Slide 43: 16 Commercial Ideas for the Innovation Day Board
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "BUSINESS|IDEAS", "16 commercial ideas for the Innovation Day board \u2014 your starting point", C.green);

    // Outer containing card
    h.addCard(s, 0.3, 1.45, 9.4, 3.35, C.white);

    // Vertical divider
    s.addShape(pres.ShapeType.rect, {
      x: 5.02, y: 1.45, w: 0.04, h: 3.35,
      fill: { color: C.divider },
      line: { color: C.divider, width: 0 },
    });

    // Horizontal divider
    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 2.66, w: 9.4, h: 0.03,
      fill: { color: C.divider },
      line: { color: C.divider, width: 0 },
    });

    // Top-left: Data & Modelling
    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 1.45, w: 4.7, h: 0.28,
      fill: { color: C.green },
      line: { color: C.green, width: 0 },
    });
    s.addText("Data \u0026 Modelling", {
      x: 0.45, y: 1.45, w: 4.4, h: 0.28,
      fontFace: "Trebuchet MS",
      fontSize: 9.5,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });
    s.addText(
      "\u2022 Automated model documentation: Claude Code reads your fundamental model codebase and generates a complete model card \u2014 inputs, outputs, calibration approach, and known limitations. Eliminates the documentation backlog every model team has.\n\u2022 AI-assisted half-life estimator calibration: an agent monitors new price data, compares against current estimates, flags drift above a threshold, and drafts a calibration recommendation for the model owner to review.\n\u2022 Anomaly detection on ELT pipeline outputs: after each scheduled run, an agent compares row counts and value distributions against baselines and posts a Teams health check when any metric exceeds 2 standard deviations.",
      {
        x: 0.45, y: 1.78, w: 4.4, h: 0.83,
        fontFace: "Calibri",
        fontSize: 7.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    // Top-right: Trading Desk Support
    s.addShape(pres.ShapeType.rect, {
      x: 5.08, y: 1.45, w: 4.62, h: 0.28,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });
    s.addText("Trading Desk Support", {
      x: 5.23, y: 1.45, w: 4.3, h: 0.28,
      fontFace: "Trebuchet MS",
      fontSize: 9.5,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });
    s.addText(
      "\u2022 Morning briefing agent: runs at 05:45 UTC, pulls overnight market moves, cross-references FM\u0026I model positions, and generates a structured 1-page brief for the trading desk \u2014 replacing a 45-minute manual process.\n\u2022 Ad hoc chart generator: a Teams bot that accepts a request from the trading desk, builds the Plotly Dash app, and returns a link \u2014 from request to interactive chart in under 15 minutes.\n\u2022 Automated spread analysis commentary: after each model run, an agent generates 2-paragraph commentary on key spread movements, likely drivers, and anomalies \u2014 ready to review and send to the desk.",
      {
        x: 5.23, y: 1.78, w: 4.3, h: 0.83,
        fontFace: "Calibri",
        fontSize: 7.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    // Bottom-left: Platform & Integration
    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 2.69, w: 4.7, h: 0.28,
      fill: { color: C.blue },
      line: { color: C.blue, width: 0 },
    });
    s.addText("Platform \u0026 Integration", {
      x: 0.45, y: 2.69, w: 4.4, h: 0.28,
      fontFace: "Trebuchet MS",
      fontSize: 9.5,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });
    s.addText(
      "\u2022 MCP server for Dataiku monitoring: a Cursor/Claude Code integration that reads FM\u0026I pipeline status, error logs, and scenario results directly \u2014 enabling AI-assisted debugging without opening the Dataiku UI. Highest-leverage near-term experiment.\n\u2022 Power BI Copilot for FM\u0026I dashboards: natural language queries on existing reports \u2014 traders query their own data in plain English rather than submitting analytical requests to the team.\n\u2022 AI-assisted recipe optimisation: Claude Code audits all ELT recipes for performance anti-patterns and generates optimised versions \u2014 months of technical debt resolved in a single overnight run.",
      {
        x: 0.45, y: 3.02, w: 4.4, h: 0.73,
        fontFace: "Calibri",
        fontSize: 7.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    // Bottom-right: Process & Workflow
    s.addShape(pres.ShapeType.rect, {
      x: 5.08, y: 2.69, w: 4.62, h: 0.28,
      fill: { color: C.orange },
      line: { color: C.orange, width: 0 },
    });
    s.addText("Process \u0026 Workflow", {
      x: 5.23, y: 2.69, w: 4.3, h: 0.28,
      fontFace: "Trebuchet MS",
      fontSize: 9.5,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });
    s.addText(
      "\u2022 Research synthesis agent: monitors a SharePoint folder for new market research PDFs, extracts the commodity, price outlook, and FM\u0026I-relevant data points, and posts structured summaries to Teams \u2014 2-3 hours of weekly reading compressed to a 5-minute review.\n\u2022 Model review report generation: after each quarterly review, an agent drafts the review report using a standard template, filling in performance metrics, calibration history, and compliance checklists.\n\u2022 Data quality monitoring with alerts: a daily agent runs checks on FM\u0026I datasets and sends a Teams alert when data quality drops below configurable thresholds \u2014 catching issues before they reach model outputs.",
      {
        x: 5.23, y: 3.02, w: 4.3, h: 0.73,
        fontFace: "Calibri",
        fontSize: 7.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    h.bottomBar(s, "Pick your highest-impact idea \u2014 bring it to Innovation Day with: what it does, what data it needs, who benefits, what the MVP looks like");
  }

  // ============================================================
  // SECTION 10 — PHILOSOPHY & CLOSE
  // ============================================================

  // ----------------------------------------------------------
  // Slide 44: Section Divider — Closing Thoughts
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: "475569" },
      line: { color: "475569", width: 0 },
    });

    s.addText("10", {
      x: 0.6, y: 1.2, w: 2, h: 0.8,
      fontFace: "Trebuchet MS",
      fontSize: 48,
      bold: true,
      color: "475569",
      align: "left",
      valign: "middle",
    });

    s.addText("Closing Thoughts", {
      x: 0.6, y: 2.1, w: 8.8, h: 0.65,
      fontFace: "Trebuchet MS",
      fontSize: 32,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

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
  // Slide 45: Statement Slide 1
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.deepNavy };

    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });

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

    s.addShape(pres.ShapeType.rect, {
      x: 0.6, y: 2.5, w: 2.0, h: 0.04,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });

    s.addText(
      "The productivity gap between AI adopters and non-adopters in technical fields is now measurable in sprint velocity, model delivery time, and analyst capacity utilisation. Teams with mature AI adoption are shipping 2\u20133 times more models per quarter at the same headcount \u2014 not because their engineers are smarter, but because each engineer is directing AI tools rather than executing every step manually.\n\nIn front-office analytics specifically: Accenture\u2019s 2025 study found the top 20% of AI adopters saved 15 hours per week. The bottom 20% saved 2 hours. Same tools. Same technical background. The entire gap was explained by one thing: how deeply they had integrated AI into their daily workflow.\n\nThe FM\u0026I domain expertise you have built \u2014 crack spreads, forward curves, calibration methodology, the commercial context that makes a number meaningful \u2014 is exactly the judgment layer that makes AI-assisted work valuable rather than just fast. The threat is not to people who deeply understand the fundamentals. The threat is to people who can be replaced by someone who deeply understands the fundamentals and also uses AI. That person exists. They are being hired right now.",
      {
        x: 0.6, y: 2.7, w: 8.8, h: 2.1,
        fontFace: "Calibri",
        fontSize: 12,
        color: C.textLight,
        align: "left",
        valign: "top",
        lineSpacingMultiple: 1.4,
        wrap: true,
      }
    );
  }

  // ----------------------------------------------------------
  // Slide 46: Statement Slide 2
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.deepNavy };

    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.orange },
      line: { color: C.orange, width: 0 },
    });

    s.addText(
      "The next decade won\u2019t kill technology jobs.\nIt will kill the comfortable middle.",
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

    s.addShape(pres.ShapeType.rect, {
      x: 0.6, y: 2.5, w: 2.0, h: 0.04,
      fill: { color: C.orange },
      line: { color: C.orange, width: 0 },
    });

    s.addText(
      "The comfortable middle is the layer of work that sits between deep domain expertise and pure execution \u2014 the translator function between subject matter experts and systems. In energy trading analytics, this is the role of someone who writes queries and formats reports but does not deeply own the models or the commercial decisions those models inform.\n\nAI is replacing that translation layer faster than most people inside it realise. A 2025 Goldman Sachs internal study found a 30% reduction in code review cycle time in teams using AI coding tools \u2014 not because fewer people reviewed code, but because the code arriving at review was better. The work being compressed is exactly the mid-layer work.\n\nThe people in the comfortable middle who never built irreplaceable domain knowledge are finding their role automated at the rate of one capability jump per quarter. The response is not to panic about AI, but to invest in the domain expertise that sits above the translation layer. The analytical depth that makes you irreplaceable is not threatened by AI \u2014 it is amplified by it. The only risk is doing neither: not building domain depth, and not using AI.",
      {
        x: 0.6, y: 2.7, w: 8.8, h: 2.1,
        fontFace: "Calibri",
        fontSize: 12,
        color: C.textLight,
        align: "left",
        valign: "top",
        lineSpacingMultiple: 1.4,
        wrap: true,
      }
    );
  }

  // ----------------------------------------------------------
  // Slide 47: Statement Slide 3
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.deepNavy };

    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.red },
      line: { color: C.red, width: 0 },
    });

    s.addText(
      "The question isn\u2019t whether\nthe AI wrote the code.\nThe question is: who owns the risk?",
      {
        x: 0.6, y: 0.9, w: 8.8, h: 1.55,
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

    s.addShape(pres.ShapeType.rect, {
      x: 0.6, y: 2.65, w: 2.0, h: 0.04,
      fill: { color: C.red },
      line: { color: C.red, width: 0 },
    });

    s.addText(
      "That is still you. The performance art around coding \u2014 requirements ceremonies, architecture slideware, AI wrappers that make no one accountable \u2014 does not answer the hard question. When the fundamental model gives a bad signal because the ELT pipeline had a bug and the trading desk acts on it, someone owns that outcome. The fact that an AI tool wrote the code that contained the bug does not change the ownership.\n\nThis matters because the current generation of AI tools are right 85\u201395% of the time on well-defined tasks. That means 5\u201315% of AI-generated outputs have an error \u2014 sometimes a subtle one that looks correct. In FM\u0026I, where model outputs inform commercial decisions, a plausible-but-wrong output that reaches the trading desk is a real risk.\n\nBuild AI into your workflow enthusiastically. But own the output with the same rigour you would apply to code you wrote by hand. Review it. Test it. Validate it against your domain knowledge. The AI is fast and often right. You are the one who knows when the output is plausible but wrong in the specific context of this commodity, this market structure, this week\u2019s supply dynamic. That judgment is not replaceable \u2014 and it is exactly what the tools depend on you to provide.",
      {
        x: 0.6, y: 2.85, w: 8.8, h: 2.0,
        fontFace: "Calibri",
        fontSize: 12,
        color: C.textLight,
        align: "left",
        valign: "top",
        lineSpacingMultiple: 1.4,
        wrap: true,
      }
    );
  }

  // ----------------------------------------------------------
  // Slide 48: Closing CTA — Three Things to Do Before Innovation Day
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });

    s.addText("Three things to do before Innovation Day", {
      x: 0.5, y: 0.15, w: 9, h: 0.6,
      fontFace: "Trebuchet MS",
      fontSize: 26,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    const ctaCards = [
      {
        x: 0.25,
        accentColor: C.teal,
        num: "01",
        numColor: C.teal,
        title: "Request your licence",
        body: "GitHub Copilot: IT self-service portal \u2192 \u2018Developer Tools\u2019 \u2192 submit request. Approval in 2-3 business days. Already have M365? Open Teams or Word \u2014 Copilot is already active. Cursor: expense via T\u0026E with manager approval (\u00a320/month Pro) or raise an IT request with an FM\u0026I business justification. The entire process takes under 10 minutes to initiate.",
        sub: "If you leave today without initiating a request, the probability of doing it tomorrow drops to near zero.",
      },
      {
        x: 3.58,
        accentColor: C.blue,
        num: "02",
        numColor: C.blue,
        title: "Run one real task this week",
        body: "Pick a task you are doing this week that would normally take 30+ minutes \u2014 a recipe debug, a documentation update, a data quality check, a meeting follow-up. Use an AI tool for it. Time how long it takes. The time comparison, experienced personally rather than read on a slide, is what converts a sceptic into a regular user.",
        sub: "First task recommendation: use Copilot in Teams to summarise your next meeting and draft the follow-up actions.",
      },
      {
        x: 6.92,
        accentColor: C.green,
        num: "03",
        numColor: C.green,
        title: "Bring your best idea",
        body: "Pick one commercial use case from today\u2019s session that maps to a problem you actually face. Prepare four things: what is the specific problem (time it takes, how often it occurs), what data does the solution need and is it safe, who benefits and by how much, and what would a 2-week MVP demonstration look like.",
        sub: "The innovation_day_board.md in the FM\u0026I shared drive has the full evaluation rubric and submission template.",
      },
    ];

    ctaCards.forEach(function(card) {
      h.addCard(s, card.x, 0.88, 3.1, 3.85, "1E293B");

      s.addShape(pres.ShapeType.rect, {
        x: card.x, y: 0.88, w: 3.1, h: 0.05,
        fill: { color: card.accentColor },
        line: { color: card.accentColor, width: 0 },
      });

      s.addText(card.num, {
        x: card.x + 0.15, y: 1.0, w: 2.8, h: 0.52,
        fontFace: "Trebuchet MS",
        fontSize: 22,
        bold: true,
        color: card.numColor,
        align: "left",
        valign: "top",
      });

      s.addText(card.title, {
        x: card.x + 0.15, y: 1.58, w: 2.8, h: 0.32,
        fontFace: "Trebuchet MS",
        fontSize: 11,
        bold: true,
        color: C.white,
        align: "left",
        valign: "top",
      });

      s.addText(card.body, {
        x: card.x + 0.15, y: 1.96, w: 2.8, h: 1.8,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textLight,
        align: "left",
        valign: "top",
        wrap: true,
      });

      s.addText(card.sub, {
        x: card.x + 0.15, y: 3.85, w: 2.8, h: 0.78,
        fontFace: "Calibri",
        fontSize: 7.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
        italic: true,
      });
    });

    s.addText(
      "You already have the tools. The only thing between you and 10\u00d7 productivity is knowing which one to reach for \u2014 and when.",
      {
        x: 0.5, y: 4.8, w: 9, h: 0.32,
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
