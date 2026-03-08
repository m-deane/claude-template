module.exports = function buildS1toS3(pres, C, h) {

  // ============================================================
  // SECTION 1 — WHY NOW
  // ============================================================

  // ----------------------------------------------------------
  // Slide 1: Title Slide
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.deepNavy };

    // Top accent bar
    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });

    // Main title
    s.addText("Gen AI for FM\u0026I", {
      x: 0.5, y: 1.5, w: 9, h: 0.8,
      fontFace: "Trebuchet MS",
      fontSize: 44,
      bold: true,
      color: C.white,
      align: "center",
      valign: "middle",
    });

    // Subtitle
    s.addText("Tools, Workflows \u0026 Commercial Opportunity", {
      x: 0.5, y: 2.4, w: 9, h: 0.4,
      fontFace: "Calibri",
      fontSize: 18,
      color: C.textLight,
      align: "center",
      valign: "middle",
    });

    // Team tag
    s.addText("FM\u0026I | Trading Analytics \u0026 Insights | BP", {
      x: 0.5, y: 3.1, w: 9, h: 0.3,
      fontFace: "Calibri",
      fontSize: 11,
      color: C.textMed,
      align: "center",
      valign: "middle",
    });

    // Session duration
    s.addText("Session duration: 90 minutes", {
      x: 0.5, y: 4.7, w: 9, h: 0.25,
      fontFace: "Calibri",
      fontSize: 10,
      color: C.textLight,
      align: "center",
      valign: "middle",
    });
  }

  // ----------------------------------------------------------
  // Slide 2: The Productivity Gap Is Already Opening
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "FM\u0026I|WHY NOW", "The productivity gap is already opening", C.teal);

    // Stat cascade — 4 stats, starting y=1.55, spacing 0.75"
    const stats = [
      { num: "45%",      label: "of analytical work activities automatable (McKinsey 2024)",            numColor: C.teal  },
      { num: "55%",      label: "faster code generation for data engineers adopting AI tools",           numColor: C.blue  },
      { num: "40-80 hrs", label: "per month saved by active AI tool users vs passive",                  numColor: C.green },
      { num: "12 min",   label: "to go from prompt to working Plotly Dash app (vs 2-3 days manual)",    numColor: C.orange},
    ];

    stats.forEach(function(stat, i) {
      const yBase = 1.55 + i * 0.75;

      // Big number
      s.addText(stat.num, {
        x: 0.3, y: yBase, w: 2.1, h: 0.42,
        fontFace: "Trebuchet MS",
        fontSize: 32,
        bold: true,
        color: stat.numColor,
        align: "left",
        valign: "middle",
      });

      // Label
      s.addText(stat.label, {
        x: 2.5, y: yBase + 0.02, w: 3.5, h: 0.4,
        fontFace: "Calibri",
        fontSize: 12,
        color: C.textMed,
        align: "left",
        valign: "middle",
      });
    });

    // Right-side card — white background with left teal accent
    h.addCard(s, 6.2, 1.35, 3.5, 3.5, C.white);

    // Left accent bar on right card
    s.addShape(pres.ShapeType.rect, {
      x: 6.2, y: 1.35, w: 0.05, h: 3.5,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });

    // Card header
    s.addText("The gap", {
      x: 6.35, y: 1.45, w: 3.25, h: 0.28,
      fontFace: "Trebuchet MS",
      fontSize: 11,
      bold: true,
      color: C.textDark,
      align: "left",
      valign: "top",
    });

    // Card body
    s.addText(
      "Teams using AI tools are outpacing those who aren't. The gap is measurable, growing, and showing up in sprint velocity, model delivery time, and analyst capacity.",
      {
        x: 6.35, y: 1.8, w: 3.25, h: 2.8,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    h.bottomBar(s, "This isn't about replacing analysts \u2014 it's about which teams can deliver 3 models where others deliver 1");
  }

  // ----------------------------------------------------------
  // Slide 3: What You'll Walk Away With
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "FM\u0026I|SESSION GOALS", "What you will walk away with today", C.teal);

    const cards = [
      {
        x: 0.3,
        accentColor: C.teal,
        title: "Tool map",
        body: "A clear mental map of every AI tool available to you at BP \u2014 what it does, when to use it, how to access it",
      },
      {
        x: 3.4,
        accentColor: C.blue,
        title: "Compliance clarity",
        body: "Exactly what data can and cannot go into each tool \u2014 no ambiguity, no guessing",
      },
      {
        x: 6.5,
        accentColor: C.green,
        title: "Innovation Day ready",
        body: "10+ concrete commercial ideas for FM\u0026I, plus a structured framework for the Innovation Day session",
      },
    ];

    const cardW = 2.9;
    const cardH = 2.8;
    const cardY = 1.55;

    cards.forEach(function(card) {
      // Card background
      h.addCard(s, card.x, cardY, cardW, cardH, C.white);

      // Top accent bar
      s.addShape(pres.ShapeType.rect, {
        x: card.x, y: cardY, w: cardW, h: 0.05,
        fill: { color: card.accentColor },
        line: { color: card.accentColor, width: 0 },
      });

      // Card title
      s.addText(card.title, {
        x: card.x + 0.15, y: cardY + 0.15, w: cardW - 0.3, h: 0.32,
        fontFace: "Trebuchet MS",
        fontSize: 11,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      // Card body
      s.addText(card.body, {
        x: card.x + 0.15, y: cardY + 0.55, w: cardW - 0.3, h: cardH - 0.75,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });
    });

    h.bottomBar(s, "Core message: you already have the tools \u2014 the only gap is knowing which one to reach for and when");
  }

  // ----------------------------------------------------------
  // Slide 4: Who We Are and Why This Matters for Our Work
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "FM\u0026I|CONTEXT", "Our work is exactly where Gen AI creates the most leverage", C.teal);

    // Left column — stacked cards with left teal accent
    const leftItems = [
      { title: "ELT pipelines on Dataiku", body: "Automated scenarios, triggers, full pipeline builds" },
      { title: "Fundamental model development", body: "Statistical models, ML prediction pipelines" },
      { title: "Ad hoc analysis for trading desks", body: "Fast turnaround analysis under time pressure" },
      { title: "Cross-squad collaboration", body: "Analysts, traders, market strategists" },
    ];

    const leftX = 0.3;
    const leftW = 4.5;
    const cardH = 0.7;
    const gap = 0.12;
    let yOffset = 1.45;

    leftItems.forEach(function(item) {
      // Card background
      h.addCard(s, leftX, yOffset, leftW, cardH, C.white);

      // Left accent
      s.addShape(pres.ShapeType.rect, {
        x: leftX, y: yOffset, w: 0.05, h: cardH,
        fill: { color: C.teal },
        line: { color: C.teal, width: 0 },
      });

      // Title
      s.addText(item.title, {
        x: leftX + 0.15, y: yOffset + 0.05, w: leftW - 0.2, h: 0.25,
        fontFace: "Trebuchet MS",
        fontSize: 10,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      // Body
      s.addText(item.body, {
        x: leftX + 0.15, y: yOffset + 0.3, w: leftW - 0.2, h: 0.32,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
      });

      yOffset += cardH + gap;
    });

    // Right column — single large card with top orange accent
    const rightX = 5.1;
    const rightW = 4.6;
    const rightH = 3.3;
    h.addCard(s, rightX, 1.45, rightW, rightH, C.white);

    // Top orange accent
    s.addShape(pres.ShapeType.rect, {
      x: rightX, y: 1.45, w: rightW, h: 0.05,
      fill: { color: C.orange },
      line: { color: C.orange, width: 0 },
    });

    // Right card header
    s.addText("The leverage opportunity", {
      x: rightX + 0.2, y: 1.58, w: rightW - 0.4, h: 0.3,
      fontFace: "Trebuchet MS",
      fontSize: 11,
      bold: true,
      color: C.textDark,
      align: "left",
      valign: "top",
    });

    // Right card body paragraph 1
    s.addText(
      "Every one of these workflows \u2014 pipeline debugging, model documentation, ad hoc chart generation, test writing \u2014 can be accelerated 5-10\u00d7 with the right Gen AI tool.",
      {
        x: rightX + 0.2, y: 2.0, w: rightW - 0.4, h: 1.0,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    // Right card body paragraph 2
    s.addText(
      "The question isn't whether to adopt. It's which tool for which task.",
      {
        x: rightX + 0.2, y: 3.1, w: rightW - 0.4, h: 0.5,
        fontFace: "Calibri",
        fontSize: 9,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    h.bottomBar(s, "FM\u0026I sits at the intersection of data engineering, modelling, and commercial delivery \u2014 peak leverage for Gen AI");
  }

  // ============================================================
  // SECTION 2 — LANDSCAPE
  // ============================================================

  // ----------------------------------------------------------
  // Slide 5: Section Divider — The Landscape
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    // Top accent bar
    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.cyan },
      line: { color: C.cyan, width: 0 },
    });

    // Section number
    s.addText("02", {
      x: 0.6, y: 1.2, w: 2, h: 0.8,
      fontFace: "Trebuchet MS",
      fontSize: 48,
      bold: true,
      color: C.cyan,
      align: "left",
      valign: "middle",
    });

    // Section title
    s.addText("The Landscape", {
      x: 0.6, y: 2.1, w: 8.8, h: 0.65,
      fontFace: "Trebuchet MS",
      fontSize: 32,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    // Section subtitle
    s.addText("What's available, what changed, and how to access it", {
      x: 0.6, y: 2.8, w: 8.8, h: 0.45,
      fontFace: "Calibri",
      fontSize: 14,
      color: C.textLight,
      align: "left",
      valign: "middle",
    });
  }

  // ----------------------------------------------------------
  // Slide 6: The Last 12 Months Changed What's Possible
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "LANDSCAPE|TIMELINE", "The last 12 months changed what's possible", C.cyan);

    const milestones = [
      {
        date: "Mar 2025",
        desc: "GPT-4o multimodal, code interpreter improvements",
        color: C.blue,
      },
      {
        date: "May 2025",
        desc: "Claude 3.7 Sonnet \u2014 extended thinking, 200k context",
        color: C.teal,
      },
      {
        date: "Jul 2025",
        desc: "GitHub Copilot Workspace GA \u2014 full repo agent mode",
        color: C.green,
      },
      {
        date: "Oct 2025",
        desc: "Cursor 0.42 \u2014 background agents, git worktrees",
        color: C.purple,
      },
      {
        date: "Jan 2026",
        desc: "Claude 4.6 Opus/Sonnet \u2014 agentic multi-step, tool calling",
        color: C.orange,
      },
    ];

    const timelineY = 2.1;
    const dotY = timelineY;
    const cardY = 1.6;
    const totalW = 9.4;
    const startX = 0.3;
    const slotW = totalW / milestones.length;

    // Horizontal connecting line
    s.addShape(pres.ShapeType.rect, {
      x: startX, y: timelineY + 0.05, w: totalW, h: 0.03,
      fill: { color: C.divider },
      line: { color: C.divider, width: 0 },
    });

    milestones.forEach(function(m, i) {
      const cx = startX + i * slotW + slotW / 2;
      const dotSize = 0.16;

      // Milestone dot
      s.addShape(pres.ShapeType.rect, {
        x: cx - dotSize / 2,
        y: dotY,
        w: dotSize,
        h: dotSize,
        fill: { color: m.color },
        line: { color: m.color, width: 0 },
      });

      // Date label
      s.addText(m.date, {
        x: cx - slotW / 2 + 0.05, y: dotY + 0.22, w: slotW - 0.1, h: 0.22,
        fontFace: "Calibri",
        fontSize: 8,
        bold: true,
        color: m.color,
        align: "center",
        valign: "top",
      });

      // Description
      s.addText(m.desc, {
        x: cx - slotW / 2 + 0.05, y: dotY + 0.46, w: slotW - 0.1, h: 0.65,
        fontFace: "Calibri",
        fontSize: 8,
        color: C.textMed,
        align: "center",
        valign: "top",
        wrap: true,
      });
    });

    h.bottomBar(s, "Context windows hit 1M tokens, reasoning improved 10\u00d7, and agentic multi-step workflows became reliable \u2014 all in 12 months");
  }

  // ----------------------------------------------------------
  // Slide 7: Tools Available to You at BP Right Now
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "LANDSCAPE|BP TOOLS", "Four tools available to BP employees right now", C.cyan);

    const gridCards = [
      {
        x: 0.3, y: 1.45,
        accentColor: C.blue,
        title: "Microsoft Copilot",
        body: "Included in M365 licence. Access via any Office app or Teams. No additional request needed.",
      },
      {
        x: 5.1, y: 1.45,
        accentColor: C.green,
        title: "GitHub Copilot",
        body: "Enterprise licence available. Request via IT portal. Integrates with VS Code and JetBrains.",
      },
      {
        x: 0.3, y: 3.1,
        accentColor: C.teal,
        title: "Cursor",
        body: "Individual or team licence. Request via IT or expense as tool. Best-in-class for large codebase work.",
      },
      {
        x: 5.1, y: 3.1,
        accentColor: C.purple,
        title: "Copilot Studio",
        body: "M365 add-on for building custom agents. Request via IT. BP training available on intranet.",
      },
    ];

    const cW = 4.4;
    const cH = 1.5;

    gridCards.forEach(function(card) {
      h.addCard(s, card.x, card.y, cW, cH, C.white);

      // Top accent bar
      s.addShape(pres.ShapeType.rect, {
        x: card.x, y: card.y, w: cW, h: 0.05,
        fill: { color: card.accentColor },
        line: { color: card.accentColor, width: 0 },
      });

      // Title
      s.addText(card.title, {
        x: card.x + 0.15, y: card.y + 0.13, w: cW - 0.3, h: 0.28,
        fontFace: "Trebuchet MS",
        fontSize: 11,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      // Body
      s.addText(card.body, {
        x: card.x + 0.15, y: card.y + 0.48, w: cW - 0.3, h: 0.85,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });
    });

    h.bottomBar(s, "All four are either included in existing BP licences or accessible via IT request \u2014 there is no technical barrier to starting today");
  }

  // ----------------------------------------------------------
  // Slide 8: How to Access Each Tool
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "LANDSCAPE|ACCESS", "Requesting access takes less than 10 minutes", C.cyan);

    const accessCards = [
      {
        accentColor: C.blue,
        body: "Microsoft Copilot \u2014 Already active if you have M365 E3/E5. Open Word, Excel, or Teams and look for the Copilot button. If not visible, raise an IT ticket.",
      },
      {
        accentColor: C.green,
        body: "GitHub Copilot \u2014 Request via the BP IT self-service portal under 'Developer Tools'. Approval typically 2-3 business days. Works in VS Code, JetBrains, and CLI.",
      },
      {
        accentColor: C.teal,
        body: "Cursor \u2014 Not in standard catalogue. Options: (1) request via IT with business justification, (2) expense via T\u0026E with manager approval. ~\u00a320/month.",
      },
      {
        accentColor: C.purple,
        body: "Copilot Studio \u2014 Add-on to M365. Request via IT with manager approval. BP intranet has step-by-step setup guide under 'Digital Tools'.",
      },
    ];

    const cardW = 9.4;
    const cardH = 0.72;
    const cardGap = 0.1;
    let cardY = 1.45;

    accessCards.forEach(function(card) {
      h.addCard(s, 0.3, cardY, cardW, cardH, C.white);

      // Left accent bar
      s.addShape(pres.ShapeType.rect, {
        x: 0.3, y: cardY, w: 0.05, h: cardH,
        fill: { color: card.accentColor },
        line: { color: card.accentColor, width: 0 },
      });

      // Body text
      s.addText(card.body, {
        x: 0.5, y: cardY + 0.1, w: cardW - 0.3, h: cardH - 0.2,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "middle",
        wrap: true,
      });

      cardY += cardH + cardGap;
    });

    h.bottomBar(s, "Start with Microsoft Copilot today \u2014 it requires zero additional requests if you have an M365 licence");
  }

  // ----------------------------------------------------------
  // Slide 9: Which Tool for Which Job
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "LANDSCAPE|TOOL MAP", "The right tool depends on the task \u2014 here is the map", C.cyan);

    const tableData = [
      { task: "Writing, summarising, emails",     tool: "Microsoft Copilot",     why: "M365 native, no context switching" },
      { task: "Debugging Python / SQL in IDE",    tool: "GitHub Copilot",        why: "Inline, context-aware, BP standard" },
      { task: "Building a new model or app",      tool: "Cursor",                why: "Full repo context, agent mode, background tasks" },
      { task: "Automating a document workflow",   tool: "Copilot Studio",        why: "No-code agent builder, connects to M365 data" },
      { task: "Long agentic coding task",         tool: "Claude Code (CLI)",     why: "Best-in-class for multi-step autonomous work" },
    ];

    const tableX = 0.3;
    const tableW = 9.4;
    const headerH = 0.35;
    const rowH = 0.55;
    const tableY = 1.45;
    const colWidths = [3.2, 2.5, 3.7];

    // Header row background
    s.addShape(pres.ShapeType.rect, {
      x: tableX, y: tableY, w: tableW, h: headerH,
      fill: { color: C.navy },
      line: { color: C.navy, width: 0 },
    });

    // Header labels
    const headers = ["Task", "Best Tool", "Why"];
    let hx = tableX;
    headers.forEach(function(label, i) {
      s.addText(label, {
        x: hx + 0.1, y: tableY + 0.04, w: colWidths[i] - 0.15, h: headerH - 0.08,
        fontFace: "Calibri",
        fontSize: 9,
        bold: true,
        color: C.white,
        align: "left",
        valign: "middle",
      });
      hx += colWidths[i];
    });

    // Data rows
    tableData.forEach(function(row, i) {
      const rowY = tableY + headerH + i * rowH;
      const rowFill = i % 2 === 0 ? C.offWhite : C.white;

      // Row background
      s.addShape(pres.ShapeType.rect, {
        x: tableX, y: rowY, w: tableW, h: rowH,
        fill: { color: rowFill },
        line: { color: C.divider, width: 0.5 },
      });

      // Row cells
      const cells = [row.task, row.tool, row.why];
      let cx = tableX;
      cells.forEach(function(cell, j) {
        s.addText(cell, {
          x: cx + 0.1, y: rowY + 0.05, w: colWidths[j] - 0.15, h: rowH - 0.1,
          fontFace: "Calibri",
          fontSize: 9,
          color: C.textDark,
          align: "left",
          valign: "middle",
          wrap: true,
        });
        cx += colWidths[j];
      });
    });

    h.bottomBar(s, "No single tool wins every task \u2014 the productivity gain comes from knowing which one to reach for in under 3 seconds");
  }

  // ============================================================
  // SECTION 3 — MICROSOFT COPILOT
  // ============================================================

  // ----------------------------------------------------------
  // Slide 10: Section Divider — Microsoft Copilot
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
    s.addText("03", {
      x: 0.6, y: 1.2, w: 2, h: 0.8,
      fontFace: "Trebuchet MS",
      fontSize: 48,
      bold: true,
      color: C.blue,
      align: "left",
      valign: "middle",
    });

    // Section title
    s.addText("Microsoft Copilot", {
      x: 0.6, y: 2.1, w: 8.8, h: 0.65,
      fontFace: "Trebuchet MS",
      fontSize: 32,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    // Section subtitle
    s.addText("M365 integration, Copilot Agents, and the roadmap ahead", {
      x: 0.6, y: 2.8, w: 8.8, h: 0.45,
      fontFace: "Calibri",
      fontSize: 14,
      color: C.textLight,
      align: "left",
      valign: "middle",
    });
  }

  // ----------------------------------------------------------
  // Slide 11: Copilot Is Embedded in Every M365 App
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "MICROSOFT|COPILOT M365", "Copilot is embedded in every M365 app you already use", C.blue);

    const m365Cards = [
      { title: "Teams",            body: "Meeting summaries, action items, real-time transcription" },
      { title: "Outlook",          body: "Draft replies, summarise threads, schedule assistant" },
      { title: "Word",             body: "Draft documents, rewrite sections, extract key points" },
      { title: "Excel",            body: "Analyse data, build formulas, generate charts from natural language" },
      { title: "PowerPoint",       body: "Generate slides from prompts, reformat layouts, add speaker notes" },
      { title: "OneNote / Loop",   body: "Capture notes, organise meeting outputs, shared workspace AI" },
    ];

    const cW = 2.9;
    const cH = 1.6;
    const row1Y = 1.45;
    const row2Y = 1.45 + cH + 0.15;
    const cols = [0.3, 3.35, 6.4];

    m365Cards.forEach(function(card, i) {
      const colIdx = i % 3;
      const rowIdx = Math.floor(i / 3);
      const cx = cols[colIdx];
      const cy = rowIdx === 0 ? row1Y : row2Y;

      h.addCard(s, cx, cy, cW, cH, C.white);

      // Top accent bar
      s.addShape(pres.ShapeType.rect, {
        x: cx, y: cy, w: cW, h: 0.05,
        fill: { color: C.blue },
        line: { color: C.blue, width: 0 },
      });

      // Title
      s.addText(card.title, {
        x: cx + 0.15, y: cy + 0.13, w: cW - 0.3, h: 0.28,
        fontFace: "Trebuchet MS",
        fontSize: 11,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      // Body
      s.addText(card.body, {
        x: cx + 0.15, y: cy + 0.48, w: cW - 0.3, h: cH - 0.6,
        fontFace: "Calibri",
        fontSize: 8,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });
    });

    h.bottomBar(s, "If you use any M365 app, you already have a Copilot \u2014 most people just haven't turned it on yet");
  }

  // ----------------------------------------------------------
  // Slide 12: [LIVE DEMO] See It In Action — Meeting Summary
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "MICROSOFT|SEE IT IN ACTION", "[LIVE DEMO] Meeting summary in 3 minutes", C.blue);

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
      "Summarise this 45-minute trading strategy call, extract all action items assigned to FM\u0026I, and draft follow-up emails for each.",
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
      fill: { color: C.blue },
      line: { color: C.blue, width: 0 },
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

    const steps = [
      "1. Copilot transcribes and summarises the meeting",
      "2. Identifies action items by person and team",
      "3. Drafts individual follow-up emails",
      "4. Links back to the meeting recording",
    ];
    s.addText(steps.join("\n"), {
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
    s.addText("3 min", {
      x: 6.35, y: 2.55, w: 3.25, h: 0.6,
      fontFace: "Trebuchet MS",
      fontSize: 36,
      bold: true,
      color: C.blue,
      align: "center",
      valign: "middle",
    });

    // Label under big number
    s.addText("from recording to follow-up emails", {
      x: 6.35, y: 3.2, w: 3.25, h: 0.3,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.textMed,
      align: "center",
      valign: "middle",
    });

    // Manual comparison
    s.addText("Manual: 45-60 min", {
      x: 6.35, y: 3.6, w: 3.25, h: 0.3,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.red,
      align: "center",
      valign: "middle",
    });

    h.bottomBar(s, "[PRESENTER: switch to Microsoft Teams / Copilot now to run this live]");
  }

  // ----------------------------------------------------------
  // Slide 13: Copilot Agents — Build Your Own Automated Assistant
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "MICROSOFT|COPILOT AGENTS", "Copilot Agents: build a custom automated assistant in minutes", C.blue);

    // Left column — stacked cards with left blue accent
    const agentItems = [
      {
        title: "What it is",
        body: "An AI agent you define with instructions, data sources, and actions. Lives in Teams or SharePoint.",
      },
      {
        title: "What it can access",
        body: "M365 data (emails, docs, SharePoint), external APIs via connectors, your own data via upload",
      },
      {
        title: "How to build one",
        body: "Copilot Studio: describe what it should do, test it, then refine by asking it to improve its own instructions",
      },
      {
        title: "FM\u0026I example",
        body: "An agent that monitors a SharePoint folder, summarises new research reports, and posts key findings to a Teams channel",
      },
    ];

    const leftX = 0.3;
    const leftW = 4.5;
    const agentCardH = 0.8;
    const agentGap = 0.1;
    let agentY = 1.45;

    agentItems.forEach(function(item) {
      h.addCard(s, leftX, agentY, leftW, agentCardH, C.white);

      // Left accent
      s.addShape(pres.ShapeType.rect, {
        x: leftX, y: agentY, w: 0.05, h: agentCardH,
        fill: { color: C.blue },
        line: { color: C.blue, width: 0 },
      });

      // Title
      s.addText(item.title, {
        x: leftX + 0.15, y: agentY + 0.06, w: leftW - 0.2, h: 0.25,
        fontFace: "Trebuchet MS",
        fontSize: 10,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      // Body
      s.addText(item.body, {
        x: leftX + 0.15, y: agentY + 0.33, w: leftW - 0.2, h: 0.4,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });

      agentY += agentCardH + agentGap;
    });

    // Right column — single large card
    const rightX = 5.1;
    const rightW = 4.6;
    const rightH = 3.35;
    h.addCard(s, rightX, 1.45, rightW, rightH, C.white);

    // Header bar
    s.addShape(pres.ShapeType.rect, {
      x: rightX, y: 1.45, w: rightW, h: 0.32,
      fill: { color: C.midBlue },
      line: { color: C.midBlue, width: 0 },
    });
    s.addText("The refine-yourself trick", {
      x: rightX + 0.15, y: 1.45, w: rightW - 0.3, h: 0.32,
      fontFace: "Trebuchet MS",
      fontSize: 11,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    // Body text paragraph 1
    s.addText(
      "After giving the agent its initial instructions, type: 'What's missing from your instructions to make you more accurate?' Then ask it to rewrite its own system prompt.",
      {
        x: rightX + 0.15, y: 1.85, w: rightW - 0.3, h: 1.3,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    // Body text paragraph 2
    s.addText(
      "This iterative self-improvement loop consistently produces better agents than manual refinement.",
      {
        x: rightX + 0.15, y: 3.3, w: rightW - 0.3, h: 0.4,
        fontFace: "Calibri",
        fontSize: 9,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    h.bottomBar(s, "Copilot Studio requires no coding \u2014 if you can write a paragraph describing what the agent should do, you can build it");
  }

  // ----------------------------------------------------------
  // Slide 14: Copilot Roadmap — What's Coming in 2026
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "MICROSOFT|ROADMAP", "Copilot in 2026: more autonomy, deeper integration", C.blue);

    const roadmapItems = [
      {
        quarter: "Q1 2026",
        desc: "Copilot Actions GA \u2014 autonomous multi-step task execution across M365",
        color: C.blue,
      },
      {
        quarter: "Q2 2026",
        desc: "Copilot in Fabric \u2014 natural language queries over Power BI datasets and dataflows",
        color: C.teal,
      },
      {
        quarter: "Q3 2026",
        desc: "Expanded connector ecosystem \u2014 1000+ third-party integrations",
        color: C.green,
      },
      {
        quarter: "Q4 2026",
        desc: "Multi-agent orchestration \u2014 Copilot agents that spawn and coordinate sub-agents",
        color: C.purple,
      },
    ];

    const rmTimelineY = 2.1;
    const rmTotalW = 9.4;
    const rmStartX = 0.3;
    const rmSlotW = rmTotalW / roadmapItems.length;
    const rmDotSize = 0.16;

    // Horizontal connector line
    s.addShape(pres.ShapeType.rect, {
      x: rmStartX, y: rmTimelineY + 0.05, w: rmTotalW, h: 0.03,
      fill: { color: C.divider },
      line: { color: C.divider, width: 0 },
    });

    roadmapItems.forEach(function(item, i) {
      const cx = rmStartX + i * rmSlotW + rmSlotW / 2;

      // Milestone dot
      s.addShape(pres.ShapeType.rect, {
        x: cx - rmDotSize / 2, y: rmTimelineY,
        w: rmDotSize, h: rmDotSize,
        fill: { color: item.color },
        line: { color: item.color, width: 0 },
      });

      // Quarter label
      s.addText(item.quarter, {
        x: cx - rmSlotW / 2 + 0.05, y: rmTimelineY + 0.22,
        w: rmSlotW - 0.1, h: 0.22,
        fontFace: "Calibri",
        fontSize: 9,
        bold: true,
        color: item.color,
        align: "center",
        valign: "top",
      });

      // Description
      s.addText(item.desc, {
        x: cx - rmSlotW / 2 + 0.05, y: rmTimelineY + 0.46,
        w: rmSlotW - 0.1, h: 0.75,
        fontFace: "Calibri",
        fontSize: 8,
        color: C.textMed,
        align: "center",
        valign: "top",
        wrap: true,
      });
    });

    // Note below timeline
    h.addCard(s, 0.3, 3.55, 9.4, 0.9, C.lightBlue);
    s.addText(
      "BP internal training available on the intranet under 'Digital Tools > AI' \u2014 covers M365 Copilot setup in detail",
      {
        x: 0.5, y: 3.62, w: 9.0, h: 0.75,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textDark,
        align: "left",
        valign: "middle",
        wrap: true,
      }
    );

    h.bottomBar(s, "The Power BI Copilot integration (Q2 2026) is the most significant near-term opportunity for FM\u0026I reporting workflows");
  }

};
