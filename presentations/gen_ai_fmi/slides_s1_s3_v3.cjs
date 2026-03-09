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

    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });

    s.addText("Gen AI for FM\u0026I", {
      x: 0.5, y: 1.4, w: 9, h: 0.9,
      fontFace: "Trebuchet MS",
      fontSize: 44,
      bold: true,
      color: C.white,
      align: "center",
      valign: "middle",
    });

    s.addText("Tools, Workflows \u0026 Commercial Opportunity", {
      x: 0.5, y: 2.4, w: 9, h: 0.4,
      fontFace: "Calibri",
      fontSize: 18,
      color: C.textLight,
      align: "center",
      valign: "middle",
    });

    s.addText("FM\u0026I | Trading Analytics \u0026 Insights | BP", {
      x: 0.5, y: 3.0, w: 9, h: 0.3,
      fontFace: "Calibri",
      fontSize: 11,
      color: C.textMed,
      align: "center",
      valign: "middle",
    });

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
  // Slide 2: The 15-Hour vs 2-Hour Gap
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "FM\u0026I|THE CASE", "The productivity gap: 15 hours saved per week vs 2 hours", C.teal);

    // Left big number panel
    h.addCard(s, 0.3, 1.45, 4.5, 3.3, C.white);

    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 1.45, w: 4.5, h: 0.05,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });

    s.addText("15 hrs", {
      x: 0.4, y: 1.58, w: 4.3, h: 0.75,
      fontFace: "Trebuchet MS",
      fontSize: 52,
      bold: true,
      color: C.teal,
      align: "center",
      valign: "middle",
    });

    s.addText("saved per week — top 20% of AI adopters", {
      x: 0.4, y: 2.38, w: 4.3, h: 0.35,
      fontFace: "Calibri",
      fontSize: 10,
      color: C.textMed,
      align: "center",
      valign: "middle",
    });

    s.addShape(pres.ShapeType.rect, {
      x: 0.9, y: 2.82, w: 3.3, h: 0.02,
      fill: { color: C.divider },
      line: { color: C.divider, width: 0 },
    });

    s.addText("vs 2 hrs/week — bottom 20%", {
      x: 0.4, y: 2.92, w: 4.3, h: 0.3,
      fontFace: "Calibri",
      fontSize: 10,
      bold: true,
      color: C.red,
      align: "center",
      valign: "middle",
    });

    s.addText("Source: Accenture 2025 quant analyst study. Same tools. Same technical background. Gap explained entirely by prompting skill and integration depth.", {
      x: 0.45, y: 3.32, w: 4.15, h: 1.25,
      fontFace: "Calibri",
      fontSize: 8.5,
      color: C.textMed,
      align: "left",
      valign: "top",
      wrap: true,
    });

    // Right statement card
    h.addCard(s, 5.1, 1.45, 4.55, 3.3, C.white);

    s.addShape(pres.ShapeType.rect, {
      x: 5.1, y: 1.45, w: 4.55, h: 0.05,
      fill: { color: C.orange },
      line: { color: C.orange, width: 0 },
    });

    s.addText("The gap is already opening", {
      x: 5.25, y: 1.58, w: 4.2, h: 0.3,
      fontFace: "Trebuchet MS",
      fontSize: 11,
      bold: true,
      color: C.textDark,
      align: "left",
      valign: "top",
    });

    s.addText(
      "Fifteen hours versus two hours \u2014 that is the difference between an analyst who has integrated AI into their daily workflow and one who uses it occasionally for spell-checking.\n\nIn FM\u0026I terms: fifteen hours reclaimed per week means three additional ad hoc analysis requests answered, one extra model backlog item cleared, documentation that actually gets written.\n\nThe question is not whether to adopt. The question is: are you in the top 20% or the bottom 20%? This session is about what separates them.",
      {
        x: 5.25, y: 1.98, w: 4.2, h: 2.65,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    h.bottomBar(s, "The only difference between 15 hrs saved and 2 hrs saved is prompting skill and integration depth \u2014 both learnable today");
  }

  // ----------------------------------------------------------
  // Slide 3: The Productivity Gap — Stat Cascade
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "FM\u0026I|WHY NOW", "The productivity gap is already opening \u2014 and it is measurable", C.teal);

    const stats = [
      {
        num: "45%",
        numColor: C.teal,
        label: "of analytical work activities automatable with current AI (McKinsey 2024)",
        context: "For FM\u0026I: ELT recipe documentation, test writing, data quality checks, boilerplate aggregation logic, report formatting \u2014 the work absorbing 30\u201340% of every sprint.",
      },
      {
        num: "55%",
        numColor: C.blue,
        label: "faster task completion for data engineers using AI coding tools (GitHub 2024)",
        context: "The gain comes from not context-switching to documentation, not writing boilerplate from scratch, and having a first draft to critique rather than starting blank.",
      },
      {
        num: "40-80 hrs",
        numColor: C.green,
        label: "per month saved by active AI tool users vs passive users (Accenture 2025)",
        context: "At 40 hrs/month that is one additional full working week per month \u2014 one week that currently disappears into repetitive tasks that AI can own.",
      },
      {
        num: "12 min",
        numColor: C.orange,
        label: "from prompt to working Plotly Dash crack spread app (vs 2-3 days manual)",
        context: "This is not theoretical \u2014 this is the Cursor demo from this session. The ad hoc desk request that currently takes until Friday can be answered by lunch.",
      },
    ];

    const leftW = 5.5;

    stats.forEach(function(stat, i) {
      const yBase = 1.48 + i * 0.845;

      s.addText(stat.num, {
        x: 0.3, y: yBase, w: 2.0, h: 0.4,
        fontFace: "Trebuchet MS",
        fontSize: 28,
        bold: true,
        color: stat.numColor,
        align: "left",
        valign: "middle",
      });

      s.addText(stat.label, {
        x: 2.45, y: yBase, w: leftW - 2.2, h: 0.25,
        fontFace: "Calibri",
        fontSize: 9,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "middle",
        wrap: true,
      });

      s.addText(stat.context, {
        x: 2.45, y: yBase + 0.25, w: leftW - 2.2, h: 0.56,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });

      if (i < 3) {
        s.addShape(pres.ShapeType.rect, {
          x: 0.3, y: yBase + 0.8, w: leftW, h: 0.015,
          fill: { color: C.divider },
          line: { color: C.divider, width: 0 },
        });
      }
    });

    // Right card
    h.addCard(s, 6.0, 1.45, 3.7, 3.3, C.white);

    s.addShape(pres.ShapeType.rect, {
      x: 6.0, y: 1.45, w: 3.7, h: 0.05,
      fill: { color: C.teal },
      line: { color: C.teal, width: 0 },
    });

    s.addText("The gap", {
      x: 6.15, y: 1.58, w: 3.4, h: 0.28,
      fontFace: "Trebuchet MS",
      fontSize: 11,
      bold: true,
      color: C.textDark,
      align: "left",
      valign: "top",
    });

    s.addText(
      "Teams using AI tools are outpacing those who are not, and the gap is measurable in sprint velocity, model delivery time, and analyst capacity utilisation.\n\nOrganisations with mature AI adoption in their quant teams are shipping 2-3 times more models per quarter than peers at the same headcount.\n\nThe FM\u0026I team has access to four AI tools today. The question is how deeply each person uses them.",
      {
        x: 6.15, y: 1.95, w: 3.4, h: 2.7,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    h.bottomBar(s, "This isn\u2019t about replacing analysts \u2014 it\u2019s about which teams can deliver 3 models where others deliver 1");
  }

  // ----------------------------------------------------------
  // Slide 4: What You Will Walk Away With Today
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
        body: "A complete mental map of every AI tool available to you at BP \u2014 what each one does, when to use it over the alternatives, and exactly how to request access if you don\u2019t already have it. By the end of this session you will be able to answer in under 10 seconds: \u201cwhich tool do I reach for when the Dataiku recipe is timing out?\u201d",
      },
      {
        x: 3.4,
        accentColor: C.blue,
        title: "Compliance clarity",
        body: "Exactly what data can and cannot go into each tool \u2014 with the reasoning behind each boundary, not just the list. You will understand why the rule exists, which means you can apply it confidently in edge cases without needing to ask compliance every time you want to use an AI tool for something non-standard.",
      },
      {
        x: 6.5,
        accentColor: C.green,
        title: "Innovation Day ready",
        body: "Ten or more concrete commercial ideas for FM\u0026I, each with enough specificity to bring to Innovation Day \u2014 what it does, what data it needs, who benefits, and what a two-week MVP would look like. Plus the evaluation framework the committee is looking for when scoring submissions.",
      },
    ];

    const cardW = 2.9;
    const cardH = 2.9;
    const cardY = 1.55;

    cards.forEach(function(card) {
      h.addCard(s, card.x, cardY, cardW, cardH, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: card.x, y: cardY, w: cardW, h: 0.05,
        fill: { color: card.accentColor },
        line: { color: card.accentColor, width: 0 },
      });

      s.addText(card.title, {
        x: card.x + 0.15, y: cardY + 0.15, w: cardW - 0.3, h: 0.3,
        fontFace: "Trebuchet MS",
        fontSize: 11,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      s.addText(card.body, {
        x: card.x + 0.15, y: cardY + 0.55, w: cardW - 0.3, h: cardH - 0.72,
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
  // Slide 5: Our Work Is Exactly Where Gen AI Creates the Most Leverage
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "FM\u0026I|CONTEXT", "Our work is exactly where Gen AI creates the most leverage", C.teal);

    const leftItems = [
      {
        title: "ELT pipelines on Dataiku",
        body: "We build pipelines that move commodity price data from raw sources through transformation recipes to model-ready datasets. Debugging when upstream data changes, optimising at performance limits, and documenting for team ownership: all tasks where AI creates 5-10\u00d7 acceleration.",
      },
      {
        title: "Fundamental model development",
        body: "Crack spread models, time spread estimators, location basis calculations, VaR scenarios \u2014 mathematically complex, domain-specific, and iterative. AI accelerates the code implementation phase, freeing developers to focus on methodology and calibration where domain expertise is irreplaceable.",
      },
      {
        title: "Ad hoc analysis for trading desks",
        body: "The 12-minute Dash app benchmark matters most here. A trader asking for crack spread visualisation by delivery month cannot wait 2 days. With Cursor in agent mode, an analyst can deliver a working interactive chart in the time it previously took to set up the Jupyter environment.",
      },
      {
        title: "Cross-squad collaboration",
        body: "FM\u0026I sits between data suppliers, model developers, and trading desk consumers. Documentation, handover notes, and meeting summaries consume significant time. Microsoft Copilot handles this class of work \u2014 giving analysts more time for analytical work only they can do.",
      },
    ];

    const leftX = 0.3;
    const leftW = 4.5;
    const itemH = 0.82;
    const itemGap = 0.08;
    let yOff = 1.45;

    leftItems.forEach(function(item) {
      h.addCard(s, leftX, yOff, leftW, itemH, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: leftX, y: yOff, w: 0.05, h: itemH,
        fill: { color: C.teal },
        line: { color: C.teal, width: 0 },
      });

      s.addText(item.title, {
        x: leftX + 0.15, y: yOff + 0.06, w: leftW - 0.2, h: 0.23,
        fontFace: "Trebuchet MS",
        fontSize: 9.5,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      s.addText(item.body, {
        x: leftX + 0.15, y: yOff + 0.3, w: leftW - 0.2, h: itemH - 0.35,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });

      yOff += itemH + itemGap;
    });

    // Right card
    const rightX = 5.1;
    const rightW = 4.6;
    const rightH = 3.35;
    h.addCard(s, rightX, 1.45, rightW, rightH, C.white);

    s.addShape(pres.ShapeType.rect, {
      x: rightX, y: 1.45, w: rightW, h: 0.05,
      fill: { color: C.orange },
      line: { color: C.orange, width: 0 },
    });

    s.addText("The leverage opportunity", {
      x: rightX + 0.2, y: 1.58, w: rightW - 0.4, h: 0.3,
      fontFace: "Trebuchet MS",
      fontSize: 11,
      bold: true,
      color: C.textDark,
      align: "left",
      valign: "top",
    });

    s.addText(
      "Every FM\u0026I workflow maps onto a different AI tool. ELT debugging \u2192 GitHub Copilot or Cursor. Model documentation \u2192 Claude Code. Desk request visualisation \u2192 Cursor in agent mode. Meeting action items \u2192 Microsoft Copilot.\n\nUnderstanding which tool to reach for \u2014 and doing so in under 3 seconds \u2014 is the skill that separates the 15-hour savers from the 2-hour savers.\n\nThe FM\u0026I team sits at the intersection of data engineering, quantitative modelling, and commercial delivery. That is exactly the combination of workflows where Gen AI creates the most leverage across the most task types.",
      {
        x: rightX + 0.2, y: 2.0, w: rightW - 0.4, h: 2.68,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    h.bottomBar(s, "FM\u0026I sits at the intersection of data engineering, modelling, and commercial delivery \u2014 peak leverage for Gen AI");
  }

  // ============================================================
  // SECTION 2 — THE LANDSCAPE
  // ============================================================

  // ----------------------------------------------------------
  // Slide 6: Section Divider — The Landscape
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.cyan },
      line: { color: C.cyan, width: 0 },
    });

    s.addText("02", {
      x: 0.6, y: 1.2, w: 2, h: 0.8,
      fontFace: "Trebuchet MS",
      fontSize: 48,
      bold: true,
      color: C.cyan,
      align: "left",
      valign: "middle",
    });

    s.addText("The Landscape", {
      x: 0.6, y: 2.1, w: 8.8, h: 0.65,
      fontFace: "Trebuchet MS",
      fontSize: 32,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    s.addText("What\u2019s available, what changed, and how to access it", {
      x: 0.6, y: 2.8, w: 8.8, h: 0.45,
      fontFace: "Calibri",
      fontSize: 14,
      color: C.textLight,
      align: "left",
      valign: "middle",
    });
  }

  // ----------------------------------------------------------
  // Slide 7: The Last 12 Months Changed What's Possible
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "LANDSCAPE|TIMELINE", "The last 12 months changed what\u2019s possible", C.cyan);

    const milestones = [
      {
        date: "Mar 2025",
        title: "GPT-4o multimodal",
        desc: "Analysts could paste a chart or PDF page directly into AI and ask questions. For FM\u0026I: paste an ICE Brent forward curve and ask what the contango steepest point signals about storage economics. Answered in seconds, not hours of manual curve reading.",
        color: C.blue,
      },
      {
        date: "May 2025",
        title: "Claude 3.7 Sonnet",
        desc: "Extended thinking enabled reliable multi-step problem solving. Complex statistical model debugging \u2014 tracing through 5 interacting components \u2014 became consistently possible. The first model useful for the non-obvious bugs that previously required a senior engineer\u2019s full day.",
        color: C.teal,
      },
      {
        date: "Jul 2025",
        title: "Copilot Workspace GA",
        desc: "For the first time, an enterprise-licensed AI tool could reason across an entire repository. For a 30-file Dataiku project: ask \u201cwhat\u2019s the downstream impact of changing the VaR calculation?\u201d and get an answer tracing through all dependent recipes.",
        color: C.green,
      },
      {
        date: "Oct 2025",
        title: "Cursor background agents",
        desc: "Background agents changed the relationship from \u201cassistant you talk to\u201d to \u201cparallel team member you assign work to.\u201d Submit \u201crefactor all ELT recipes to use Polars\u201d and come back 90 minutes later to a completed branch. AI as a parallel worker, not just a faster typist.",
        color: C.purple,
      },
      {
        date: "Jan 2026",
        title: "Claude 4.6 Opus/Sonnet",
        desc: "Reliable agentic multi-step tool calling \u2014 executing code, seeing results, correcting errors, and continuing \u2014 made Claude Code production-worthy for FM\u0026I work. A single instruction now reliably produces a complete, useful multi-file output without constant supervision.",
        color: C.orange,
      },
    ];

    const timelineY = 1.75;
    const totalW = 9.4;
    const startX = 0.3;
    const slotW = totalW / milestones.length;

    s.addShape(pres.ShapeType.rect, {
      x: startX, y: timelineY + 0.07, w: totalW, h: 0.03,
      fill: { color: C.divider },
      line: { color: C.divider, width: 0 },
    });

    milestones.forEach(function(m, i) {
      const cx = startX + i * slotW + slotW / 2;
      const dotSize = 0.16;

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

    h.bottomBar(s, "Context windows hit 1M tokens, reasoning improved 10\u00d7, agentic workflows became reliable \u2014 all in 12 months");
  }

  // ----------------------------------------------------------
  // Slide 8: Four Tools Available to BP Employees Right Now
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
        body: "Embedded in your M365 licence \u2014 if you have access to Teams, Outlook, Word, or Excel, Copilot is already available. No IT request required in most cases. The entry point for AI-assisted meeting summaries, document drafting, and data analysis in Excel. The lowest-friction tool to start using today.",
      },
      {
        x: 5.1, y: 1.45,
        accentColor: C.green,
        title: "GitHub Copilot",
        body: "BP holds an enterprise licence, making this the most straightforward coding AI to request. Integrates directly into VS Code and JetBrains \u2014 the IDEs already in use for Dataiku recipe development. Best for inline code completion, debugging, and documentation generation within your existing IDE environment.",
      },
      {
        x: 0.3, y: 3.15,
        accentColor: C.teal,
        title: "Cursor",
        body: "A full VS Code fork with AI deeply integrated at every level \u2014 not an add-on but the core of the product. Best-in-class for large, multi-file projects where you need the AI to understand the entire Dataiku project structure, not just the file you have open. Requires individual licence request or T\u0026E expense.",
      },
      {
        x: 5.1, y: 3.15,
        accentColor: C.purple,
        title: "Copilot Studio",
        body: "The no-code agent builder in the Microsoft ecosystem. If you can write a paragraph describing what an automated assistant should do, you can build it in Copilot Studio without writing a line of code. FM\u0026I use case: a research monitoring agent that reads new reports from SharePoint and posts summaries to Teams.",
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

    h.bottomBar(s, "All four are either included in existing BP licences or accessible via IT request \u2014 no technical barrier to starting today");
  }

  // ----------------------------------------------------------
  // Slide 9: Requesting Access Takes Less Than 10 Minutes
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "LANDSCAPE|ACCESS", "Requesting access takes less than 10 minutes", C.cyan);

    const accessCards = [
      {
        accentColor: C.blue,
        body: "Microsoft Copilot \u2014 Already active if you have M365 E3 or E5. Open Word, Excel, or Teams and look for the Copilot button. If not visible, raise a standard IT ticket referencing \u2018M365 Copilot activation\u2019. No additional licence cost, no manager approval required for the base tier. Most FM\u0026I team members can start today.",
      },
      {
        accentColor: C.green,
        body: "GitHub Copilot \u2014 Request via the BP IT self-service portal under \u2018Developer Tools\u2019. Approval typically takes 2-3 business days. Once approved, install the GitHub Copilot extension in VS Code, sign in with your GitHub Enterprise account, and it is immediately active in your existing IDE. Works in VS Code, JetBrains, and GitHub Copilot CLI.",
      },
      {
        accentColor: C.teal,
        body: "Cursor \u2014 Not in the standard IT catalogue as of Q1 2026. Two options: (1) raise an IT request with an FM\u0026I pipeline development business justification, or (2) expense as a professional tool via T\u0026E with manager approval \u2014 approximately \u00a320/month Pro tier. Once installed, import your VS Code settings and sign in with a Cursor account.",
      },
      {
        accentColor: C.purple,
        body: "Copilot Studio \u2014 An M365 add-on requiring IT approval and a manager-signed business justification. BP\u2019s intranet has a step-by-step setup guide under \u2018Digital Tools \u003e AI \u003e Copilot Studio\u2019. Once provisioned, access via the Copilot Studio portal \u2014 no local installation required. Provisioning typically takes 3-5 business days.",
      },
    ];

    const cardW = 9.4;
    const cardH = 0.72;
    const cardGap = 0.1;
    let cardY = 1.45;

    accessCards.forEach(function(card) {
      h.addCard(s, 0.3, cardY, cardW, cardH, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: 0.3, y: cardY, w: 0.05, h: cardH,
        fill: { color: card.accentColor },
        line: { color: card.accentColor, width: 0 },
      });

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
  // Slide 10: The Right Tool Depends on the Task
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "LANDSCAPE|TOOL MAP", "The right tool depends on the task \u2014 here is the map", C.cyan);

    const tableData = [
      {
        task: "Writing, summarising, emails",
        tool: "Microsoft Copilot",
        why: "M365-native, zero context switching. Data stays inside BP\u2019s Microsoft tenant \u2014 safest option for internal content.",
      },
      {
        task: "Debugging Python or SQL in your IDE",
        tool: "GitHub Copilot",
        why: "Inline and context-aware in your existing IDE. BP enterprise licence means IT and legal coverage without extra approval.",
      },
      {
        task: "Building a new model or full app",
        tool: "Cursor",
        why: "Full-repository context understands how your 30-file Dataiku project connects. Agent mode handles multi-step builds autonomously.",
      },
      {
        task: "Automating a document workflow",
        tool: "Copilot Studio",
        why: "No-code agent builder connected to M365 data. Build a research summariser without writing Python. Best for non-developer workflows.",
      },
      {
        task: "Long agentic coding task or overnight audit",
        tool: "Claude Code (CLI)",
        why: "Headless operation \u2014 runs on a VM overnight without a GUI. Best for full codebase audits, multi-file refactors, CI/CD integration.",
      },
    ];

    const tableX = 0.3;
    const tableW = 9.4;
    const headerH = 0.35;
    const rowH = 0.55;
    const tableY = 1.45;
    const colWidths = [3.1, 2.4, 3.9];

    s.addShape(pres.ShapeType.rect, {
      x: tableX, y: tableY, w: tableW, h: headerH,
      fill: { color: C.navy },
      line: { color: C.navy, width: 0 },
    });

    const headers = ["Task", "Best Tool", "Why It Wins"];
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

    tableData.forEach(function(row, i) {
      const rowY = tableY + headerH + i * rowH;
      const rowFill = i % 2 === 0 ? C.offWhite : C.white;

      s.addShape(pres.ShapeType.rect, {
        x: tableX, y: rowY, w: tableW, h: rowH,
        fill: { color: rowFill },
        line: { color: C.divider, width: 0.5 },
      });

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
  // Slide 11: Section Divider — Microsoft Copilot
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.navy };

    s.addShape(pres.ShapeType.rect, {
      x: 0, y: 0, w: "100%", h: 0.06,
      fill: { color: C.blue },
      line: { color: C.blue, width: 0 },
    });

    s.addText("03", {
      x: 0.6, y: 1.2, w: 2, h: 0.8,
      fontFace: "Trebuchet MS",
      fontSize: 48,
      bold: true,
      color: C.blue,
      align: "left",
      valign: "middle",
    });

    s.addText("Microsoft Copilot", {
      x: 0.6, y: 2.1, w: 8.8, h: 0.65,
      fontFace: "Trebuchet MS",
      fontSize: 32,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

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
  // Slide 12: Copilot Is Embedded in Every M365 App
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "MICROSOFT|COPILOT M365", "Copilot is embedded in every M365 app you already use", C.blue);

    const m365Cards = [
      {
        x: 0.3, y: 1.45,
        accentColor: C.blue,
        title: "Teams + Outlook",
        body: "Teams Copilot transcribes meetings in real time, extracts action items by person and team, and generates a structured follow-up summary within 30 seconds of the call ending. Outlook Copilot drafts replies matching your tone and summarises long email threads. For FM\u0026I: trading strategy calls become structured action logs automatically.",
      },
      {
        x: 5.1, y: 1.45,
        accentColor: C.midBlue,
        title: "Word + PowerPoint",
        body: "Word Copilot drafts documents from bullet points, rewrites sections in a different tone, and generates tables from plain text descriptions. PowerPoint Copilot generates entire decks from a Word document or prompt and reformats existing slides. For FM\u0026I: model documentation and management reporting drafted in minutes rather than hours.",
      },
      {
        x: 0.3, y: 3.15,
        accentColor: C.cyan,
        title: "Excel \u2014 the FM\u0026I-relevant capabilities",
        body: "Natural language formula generation: describe what you want and Excel writes it. Python in Excel: Copilot-assisted Python runs inside Excel cells for statistical analysis without leaving the spreadsheet. Natural language data insights: ask \u201cwhat are the three most unusual patterns?\u201d and Copilot detects anomalies and narrates findings. For FM\u0026I: crack spread analysis and scenario outputs interrogated without writing code.",
      },
      {
        x: 5.1, y: 3.15,
        accentColor: C.teal,
        title: "OneNote + Loop",
        body: "OneNote Copilot summarises freeform notes, generates action plans from meeting capture, and enables cross-notebook search via conversational queries. Microsoft Loop adds AI-assisted shared workspaces for collaborative document updates. For FM\u0026I: morning operational briefs auto-drafted from a structured prompt, and cross-team research notes synthesised across notebooks automatically.",
      },
    ];

    const cW = 4.4;
    const cH = 1.58;

    m365Cards.forEach(function(card) {
      h.addCard(s, card.x, card.y, cW, cH, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: card.x, y: card.y, w: cW, h: 0.05,
        fill: { color: card.accentColor },
        line: { color: card.accentColor, width: 0 },
      });

      s.addText(card.title, {
        x: card.x + 0.15, y: card.y + 0.12, w: cW - 0.3, h: 0.28,
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

    h.bottomBar(s, "If you use any M365 app, you already have a Copilot \u2014 most people just haven\u2019t turned it on yet");
  }

  // ----------------------------------------------------------
  // Slide 13: [LIVE DEMO] Meeting Summary in 3 Minutes
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "MICROSOFT|SEE IT IN ACTION", "[LIVE DEMO] Meeting summary in 3 minutes", C.blue);

    // Prompt header
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

    // Terminal
    s.addShape(pres.ShapeType.rect, {
      x: 0.3, y: 1.78, w: 9.4, h: 0.55,
      fill: { color: "1A1A2E" },
      line: { color: "1A1A2E", width: 0 },
    });
    s.addText(
      "Summarise this 45-minute trading strategy call, extract all action items assigned to FM\u0026I with owner and due date, and draft follow-up emails for each action item owner.",
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

    s.addText(
      "1. Copilot transcribes and summarises the full meeting in real time\n2. Identifies action items, assigns each to a named individual with due date\n3. Drafts structured follow-up emails for each action item owner\n4. Links each action back to the meeting recording timestamp\n5. Formats summary in your preferred style (bullet points or prose)",
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

    s.addText("3 min", {
      x: 6.35, y: 2.55, w: 3.25, h: 0.6,
      fontFace: "Trebuchet MS",
      fontSize: 36,
      bold: true,
      color: C.blue,
      align: "center",
      valign: "middle",
    });

    s.addText("from recording to structured follow-ups with emails drafted", {
      x: 6.35, y: 3.2, w: 3.25, h: 0.35,
      fontFace: "Calibri",
      fontSize: 9,
      color: C.textMed,
      align: "center",
      valign: "middle",
      wrap: true,
    });

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
  // Slide 14: Copilot Agents — Build a Custom Automated Assistant
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "MICROSOFT|COPILOT AGENTS", "Copilot Agents: build a custom automated assistant in minutes", C.blue);

    const agentItems = [
      {
        title: "What it is",
        body: "A custom AI assistant you define with natural language instructions, data sources, and actions. It lives in Microsoft Teams or Copilot and retains its configuration across all conversations. You describe what it should do and what it should know \u2014 no coding required. It can be shared across your team once built.",
      },
      {
        title: "What it can access",
        body: "Microsoft Graph data (your calendar, emails, Teams messages, with consent), SharePoint document libraries you specify, web content via Bing grounding, and external systems via Power Automate connectors. For FM\u0026I: an agent can read new research reports from a SharePoint library, summarise them, and act on their contents without manual input.",
      },
      {
        title: "How to build one",
        body: "Open Copilot Studio. Define the agent\u2019s name and purpose in plain language. Connect knowledge sources \u2014 a SharePoint folder of market reports, a web URL, or uploaded documents. Add Power Automate flows for actions. Test in the Studio test panel and iterate. Publish to Teams. Build time for a useful first version: 30-60 minutes.",
      },
      {
        title: "The self-improvement trick",
        body: "After giving the agent its initial instructions, type: \u201cReview your instructions and suggest improvements to make you more effective at this task.\u201d Paste the improved instructions back in. Run this loop 2-3 times. The resulting agent is consistently better than one refined manually and requires no prompt engineering expertise to improve.",
      },
    ];

    const leftX = 0.3;
    const leftW = 4.5;
    const agentCardH = 0.82;
    const agentGap = 0.08;
    let agentY = 1.45;

    agentItems.forEach(function(item) {
      h.addCard(s, leftX, agentY, leftW, agentCardH, C.white);

      s.addShape(pres.ShapeType.rect, {
        x: leftX, y: agentY, w: 0.05, h: agentCardH,
        fill: { color: C.blue },
        line: { color: C.blue, width: 0 },
      });

      s.addText(item.title, {
        x: leftX + 0.15, y: agentY + 0.06, w: leftW - 0.2, h: 0.22,
        fontFace: "Trebuchet MS",
        fontSize: 9.5,
        bold: true,
        color: C.textDark,
        align: "left",
        valign: "top",
      });

      s.addText(item.body, {
        x: leftX + 0.15, y: agentY + 0.3, w: leftW - 0.2, h: agentCardH - 0.35,
        fontFace: "Calibri",
        fontSize: 8.5,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      });

      agentY += agentCardH + agentGap;
    });

    // Right card — FM&I example
    const rightX = 5.1;
    const rightW = 4.6;
    const rightH = 3.45;
    h.addCard(s, rightX, 1.45, rightW, rightH, C.white);

    s.addShape(pres.ShapeType.rect, {
      x: rightX, y: 1.45, w: rightW, h: 0.32,
      fill: { color: C.midBlue },
      line: { color: C.midBlue, width: 0 },
    });
    s.addText("FM\u0026I example: research monitor", {
      x: rightX + 0.15, y: 1.45, w: rightW - 0.3, h: 0.32,
      fontFace: "Trebuchet MS",
      fontSize: 10,
      bold: true,
      color: C.white,
      align: "left",
      valign: "middle",
    });

    s.addText(
      "An agent configured to monitor a SharePoint folder where market research reports are filed. Every time a new PDF is added, the agent reads it and extracts: the commodity covered, key price outlook (bullish/bearish), top 3 risks, and any FM\u0026I-relevant data points.\n\nIt posts a structured summary to the FM\u0026I Teams channel within 2 minutes of the file arriving.\n\nBuild time: 45 minutes.\nTime saved per week: 2-3 hours of manual report reading compressed to a 5-minute review of AI summaries.",
      {
        x: rightX + 0.15, y: 1.85, w: rightW - 0.3, h: 2.9,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textMed,
        align: "left",
        valign: "top",
        wrap: true,
      }
    );

    h.bottomBar(s, "Copilot Studio requires no coding \u2014 if you can write a paragraph describing what the agent should do, you can build it");
  }

  // ----------------------------------------------------------
  // Slide 15: Copilot in 2026 — More Autonomy, Deeper Integration
  // ----------------------------------------------------------
  {
    const s = pres.addSlide();
    s.background = { color: C.offWhite };
    h.sectionHeader(s, "MICROSOFT|ROADMAP", "Copilot in 2026: more autonomy, deeper integration", C.blue);

    const roadmapItems = [
      {
        quarter: "Q1 2026",
        title: "Reasoning mode",
        desc: "Microsoft integrated OpenAI\u2019s o-series reasoning model into Word and Outlook Copilot. For complex multi-step document tasks \u2014 \u201canalyse this model review report and identify all actions requiring compliance sign-off\u201d \u2014 reasoning mode produces structurally better outputs than standard Copilot.",
        color: C.blue,
      },
      {
        quarter: "Q2 2026",
        title: "Power BI Copilot expansion",
        desc: "Natural language report generation directly in Power BI Service \u2014 describe the analysis you want, Copilot builds the report. For FM\u0026I: trading desk requests for spread analysis become a conversation rather than a development sprint. The highest-value near-term integration for this team.",
        color: C.teal,
      },
      {
        quarter: "Q3 2026",
        title: "1,000+ connector ecosystem",
        desc: "Third-party connectors expand Copilot Studio\u2019s reach to 1,000+ external services. For FM\u0026I, this means Copilot agents that can query Bloomberg, pull Dataiku scenario status, or read from commodity pricing APIs \u2014 all without custom MCP development.",
        color: C.green,
      },
      {
        quarter: "Q4 2026",
        title: "Multi-agent orchestration",
        desc: "Copilot agents can spawn and coordinate sub-agents. An orchestrator receives \u201cprepare the monthly model performance pack\u201d and delegates to sub-agents: data collector, analyst, writer, formatter. The orchestrator synthesises results and delivers the finished pack.",
        color: C.purple,
      },
    ];

    const rmTimelineY = 1.8;
    const rmTotalW = 9.4;
    const rmStartX = 0.3;
    const rmSlotW = rmTotalW / roadmapItems.length;
    const rmDotSize = 0.16;

    s.addShape(pres.ShapeType.rect, {
      x: rmStartX, y: rmTimelineY + 0.07, w: rmTotalW, h: 0.03,
      fill: { color: C.divider },
      line: { color: C.divider, width: 0 },
    });

    roadmapItems.forEach(function(item, i) {
      const cx = rmStartX + i * rmSlotW + rmSlotW / 2;

      s.addShape(pres.ShapeType.rect, {
        x: cx - rmDotSize / 2, y: rmTimelineY,
        w: rmDotSize, h: rmDotSize,
        fill: { color: item.color },
        line: { color: item.color, width: 0 },
      });

      s.addText(item.quarter, {
        x: cx - rmSlotW / 2 + 0.05, y: rmTimelineY + 0.22,
        w: rmSlotW - 0.1, h: 0.2,
        fontFace: "Calibri",
        fontSize: 8,
        bold: true,
        color: item.color,
        align: "center",
        valign: "top",
      });

      s.addText(item.title, {
        x: cx - rmSlotW / 2 + 0.05, y: rmTimelineY + 0.44,
        w: rmSlotW - 0.1, h: 0.2,
        fontFace: "Trebuchet MS",
        fontSize: 8,
        bold: true,
        color: C.textDark,
        align: "center",
        valign: "top",
      });

      s.addText(item.desc, {
        x: cx - rmSlotW / 2 + 0.05, y: rmTimelineY + 0.66,
        w: rmSlotW - 0.1, h: 1.8,
        fontFace: "Calibri",
        fontSize: 7.5,
        color: C.textMed,
        align: "center",
        valign: "top",
        wrap: true,
      });
    });

    // Note card
    h.addCard(s, 0.3, 3.65, 9.4, 0.85, C.lightBlue);
    s.addText(
      "BP internal training on the intranet under \u2018Digital Tools \u003e AI\u2019 covers M365 Copilot setup, data governance, and Copilot Studio basics in 3 self-paced modules. Estimated 90 minutes total for all three modules.",
      {
        x: 0.5, y: 3.72, w: 9.0, h: 0.72,
        fontFace: "Calibri",
        fontSize: 9,
        color: C.textDark,
        align: "left",
        valign: "middle",
        wrap: true,
      }
    );

    h.bottomBar(s, "The Power BI Copilot integration (Q2 2026) is the highest-leverage near-term opportunity for FM\u0026I reporting workflows");
  }

};
