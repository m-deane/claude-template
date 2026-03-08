# Speaker Scripts: The AI-Augmented Team

**Total presentation time**: 15 minutes
**Audience**: Software engineering teams and tech leadership
**Tone**: Peer sharing findings, not vendor pitch

---

[SLIDE 1: Title Slide]
Duration: 30 seconds

SPEAKER NOTES:
Good morning. I'm [NAME], and for the next fifteen minutes I'm going to walk you through what the research **actually** says about AI tools in software development. Not the hype. Not the vendor marketing. The controlled studies, the industry surveys, the data from millions of lines of code. [PAUSE] I'll cover three things: where the productivity gains are real, where the risks are real, and what the teams that are doing this well have in common. We'll close with three concrete actions you can take starting this week.

KEY POINTS TO HIT:
- Set the frame: this is data-driven, not cheerleading
- Signal honesty about trade-offs upfront to earn credibility with a skeptical audience
- Promise concrete actions so they stay engaged through the data sections

TRANSITION TO NEXT SLIDE:
"Let me start with a number that reframes this entire conversation."

---

[SLIDE 2: 46% of Code Written by Active GitHub Copilot Users Is Now AI-Generated]
Duration: 75 seconds

SPEAKER NOTES:
Forty-six percent. [PAUSE] That is the share of accepted code that GitHub Copilot now generates for its active users. In 2022, when Copilot launched, that number was twenty-seven percent. In under three years, it nearly **doubled**. And this is not a fringe tool. Twenty million developers are using Copilot today. Ninety percent of Fortune 100 companies have adopted it. [PAUSE]

So here is the question I want you to sit with for the rest of this talk: does your team have a **deliberate policy** for this? Not "are people using AI tools" -- of course they are. The question is whether you have a shared standard for how AI-generated code gets reviewed, tested, and merged. Because if you don't, you are absorbing this shift informally. And as we'll see in a few minutes, informal adoption is where the problems concentrate.

Now, some of you might be thinking: "Forty-six percent sounds high. That can't all be production-critical code." You're right to be skeptical. A lot of that is boilerplate, test scaffolding, documentation. But that is exactly the point. The repetitive work that used to eat your afternoons? That is what's being automated first. The question is whether your team is capturing that benefit **with** guardrails, or without them.

KEY POINTS TO HIT:
- Let the 46% number land with a pause before explaining it
- The trajectory matters: 27% to 46% in under three years
- Scale: 20M users, 90% Fortune 100
- Reframe from "are you using AI" to "do you have a policy for AI"

TRANSITION TO NEXT SLIDE:
"To understand why this matters so much right now, let's look at the environment these tools landed in."

---

[SLIDE 3: The Compounding Pressures on Engineering Teams]
Duration: 45 seconds

SPEAKER NOTES:
None of this is happening in a vacuum. Every engineering team I talk to is living the same tension. On one side, you have codebases getting more complex year over year. You have a talent market that is still competitive for senior engineers. You have business stakeholders who want faster releases, higher quality, and lower cost -- all at the same time. [PAUSE]

On the other side, what do you actually have? The same sprint cadence you had three years ago. Rising burnout risk. Technical debt that keeps compounding because there is never time to address it.

AI tools did not arrive because Silicon Valley thought it would be fun. They arrived because there is **genuine demand** for ways to do more with the same engineering headcount. That context matters for how we evaluate them.

KEY POINTS TO HIT:
- Validate the audience's lived experience -- they feel this pressure daily
- Position AI tools as a response to real constraints, not a novelty
- Keep this brief -- it's context-setting, not the core argument

TRANSITION TO NEXT SLIDE:
"So the tools arrived. Teams adopted them. And here's where it gets complicated."

---

[SLIDE 4: The Gap Between Adoption and Impact]
Duration: 60 seconds

SPEAKER NOTES:
Look at this gap. Seventy-six percent of developers say they are using or plan to use AI tools. Adoption is not the problem. [PAUSE] But only forty-seven percent of IT leaders say their AI projects were actually profitable last year. McKinsey found that only **six percent** of organizations qualify as AI high performers -- meaning they see more than five percent impact on their bottom line. The DORA team -- the same group that brought us the Accelerate metrics -- found something even more specific. A twenty-five percent increase in AI adoption correlates with a **seven point two percent decrease** in delivery stability.

Let that sink in. More AI, less stability. [PAUSE]

Why? Not because the tools are bad. Because AI makes it easy to write **more** code, which means larger changesets, which means more risk per deployment. The tools work. But unstructured adoption produces a pattern where teams ship more code and accumulate more risk **simultaneously**. That gap you see on this slide? That is not a tools problem. It is a process problem.

KEY POINTS TO HIT:
- The adoption-impact gap is the central tension of this talk
- DORA's stability finding is the most important data point for this audience
- Root cause: larger changesets, not bad tools
- Frame it as a solvable process problem, not an indictment of AI

TRANSITION TO NEXT SLIDE:
"So let's get into the evidence. Starting with what the tools actually deliver when used well."

---

[SLIDE 5: Section Divider -- Pillar 1: The Productivity Gains Are Real]
Duration: 15 seconds

SPEAKER NOTES:
Pillar one. The productivity evidence. I want to be specific here about methodology -- not just headline numbers, but where those numbers come from and what they measure.

KEY POINTS TO HIT:
- Brief orientation only -- do not linger on section dividers
- Signal that rigor is coming to maintain credibility

TRANSITION TO NEXT SLIDE:
"Here's what the controlled studies show."

---

[SLIDE 6: Controlled Research -- What AI Tools Do to Development Speed]
Duration: 100 seconds

SPEAKER NOTES:
This is the slide I want you to look at carefully, because these are not blog posts or tweets. These are controlled studies with comparison groups.

Start at the top. GitHub partnered with Accenture and ran a study across **forty-eight hundred developers**. Same JavaScript task. Half used Copilot, half didn't. The Copilot group finished fifty-five percent faster. One hour eleven minutes versus two hours forty-one minutes. That is not a marginal gain. [PAUSE]

Move down. A separate study of nearly five thousand developers found twenty-six percent more weekly tasks completed with AI assistance. McKinsey found that code documentation takes **half the time**. Refactoring tasks take about two-thirds the time.

And the one that should get the attention of anyone who has ever waited on a PR review: pull request cycle time dropped from **nine point six days to two point four days**. A seventy-five percent reduction. That is not just developer productivity. That is organizational throughput.

But here is the nuance you need to know. [PAUSE] These gains are **not uniform**. The biggest improvements are in boilerplate generation, documentation, and test scaffolding. When it comes to system design, architecture decisions, complex debugging -- the gains are much smaller. AI tools are not replacing your senior engineers' judgment. They are eliminating the low-cognition work that was burying it.

One more thing. Research shows it takes about **eleven weeks** for a developer to fully internalize the workflow shift. So if your team tried Copilot for two weeks and said "it's not that useful" -- they stopped too early.

KEY POINTS TO HIT:
- Emphasize methodology: controlled studies, not anecdotes
- Walk through the chart systematically -- give the audience time to absorb each bar
- The PR cycle time stat resonates most with leadership
- Non-uniform gains: boilerplate yes, architecture no
- Eleven-week adoption curve -- set realistic expectations

TRANSITION TO NEXT SLIDE:
"Beyond raw speed, there's another metric that matters more than most leaders realize."

---

[SLIDE 7: AI Tools Are Changing How Developers Feel About Their Work]
Duration: 50 seconds

SPEAKER NOTES:
Ninety-five percent of Copilot users report enjoying coding more. Developers using AI tools are **twice as likely** to report being in a flow state. Seventy-three percent say AI helps them stay in flow. Eighty-seven percent say it preserves mental effort during repetitive tasks. [PAUSE]

Now, I know what some of you are thinking. "Developer happiness is a nice-to-have." But here is why it is a business metric. Burnout from repetitive, low-cognition work is one of the top documented causes of senior engineer attrition. And replacing a senior engineer costs you -- what, six months of ramp time for their replacement? More?

If AI tools reduce the toil that drives your best people out, the compounding benefit is **retention**. And retention in senior engineers is worth more than any productivity percentage point on this slide.

KEY POINTS TO HIT:
- Lead with the numbers -- they are striking
- Reframe "happiness" as a retention and quality metric for the leadership audience
- Connect to the financial cost of attrition

TRANSITION TO NEXT SLIDE:
"So the gains are real. But they do not arrive for free. Let's talk about where the risks concentrate."

---

[SLIDE 8: Section Divider -- Pillar 2: The Risks Are Specific and Manageable]
Duration: 15 seconds

SPEAKER NOTES:
Pillar two. The risks. This is the section I would most want you to take notes on, because it is the part that most teams skip when they read the productivity headlines.

KEY POINTS TO HIT:
- Create urgency around this section
- Signal that this is the highest-value content for practitioners

TRANSITION TO NEXT SLIDE:
"There are three distinct risk categories. Each one is well-documented, and each one has a direct countermeasure."

---

[SLIDE 9: Where AI-Generated Code Introduces Risk]
Duration: 110 seconds

SPEAKER NOTES:
Three columns on this slide. Three risk categories. Let me walk through each one.

**First: security.** Forty-eight percent of AI-generated code contains potential security vulnerabilities. That is not my number -- that is from industry-wide security research. Enterprises using AI coding assistants are reporting over ten thousand new security findings **per month** attributable to AI-generated code. The countermeasure is straightforward: security scanning has to be a CI/CD gate, not an afterthought. If AI-generated code does not pass the same automated security checks as human-written code, you are creating a bypass in your own security model.

**Second: technical debt.** GitClear analyzed two hundred and eleven million changed lines of code from 2020 to 2024. Copy-pasted code rose from eight point three percent to twelve point three percent. Refactoring activity -- which is how you **pay down** technical debt -- sank from twenty-five percent to under ten percent. [PAUSE] Forty percent of developers say AI has increased technical debt by creating unnecessary or duplicative code. The countermeasure: you have to track debt metrics alongside velocity metrics. If you only measure how fast code ships, you will miss that your codebase is degrading.

**Third: delivery stability.** This is the DORA finding I mentioned earlier. AI makes it easy to write more code per PR. Larger PRs fail more often. The countermeasure is almost comically simple: enforce smaller PRs as a team norm when using AI tools. The tool makes it easy to write a lot of code fast. Your process needs to make it hard to **ship** a lot of code at once.

Here is the important framing. [PAUSE] These risks are **specific and well-characterized**. Each one has a known engineering response. This is very different from risks that are unknown or unpredictable. You know what to watch for. The question is whether you build the countermeasures before or after the problems show up in production.

KEY POINTS TO HIT:
- Walk through all three columns systematically
- The GitClear data is the most novel finding for most audiences
- Each risk has a concrete, actionable countermeasure
- End on the framing: specific and manageable, not existential

TRANSITION TO NEXT SLIDE:
"There's one more risk signal worth examining -- and it's actually good news in disguise."

---

[SLIDE 10: Developer Trust in AI Is Falling -- That Is Actually a Good Sign]
Duration: 60 seconds

SPEAKER NOTES:
Developer trust in AI-generated code dropped from forty-two percent in 2024 to thirty-three percent in 2025. Only three percent of developers say they highly trust AI-generated code. Seventy-one percent refuse to merge AI-generated code without manual review. [PAUSE]

You might look at those numbers and think: "That's a problem." I want to reframe it. Declining trust reflects **maturity**, not failure. Think about it this way. A junior team that blindly trusts AI output? That is the team accumulating the security debt and the technical debt we just talked about. A senior team that reflexively rejects AI output? They are leaving fifty-five percent productivity gains on the table.

The winning posture is somewhere specific: use the tools, **distrust the output by default**, and verify systematically. That is not cynicism. That is engineering discipline applied to a new kind of tool. The seventy-one percent who refuse to merge without review? They are doing it right.

KEY POINTS TO HIT:
- Reframe declining trust as a sign of maturity
- The spectrum: blind trust is dangerous, reflexive rejection is wasteful
- The correct stance: structured skepticism with systematic verification
- 71% refusing to merge without review is the right behavior

TRANSITION TO NEXT SLIDE:
"The teams that manage these risks don't abandon AI. They double down, because they've built the governance to extract compounding value. That brings us to the forward-looking question."

---

[SLIDE 11: Section Divider -- Pillar 3: The Strategic Edge Comes From Full-SDLC Integration]
Duration: 15 seconds

SPEAKER NOTES:
Pillar three. This section looks forward. The first two pillars are about the current state. This pillar is about the twelve to twenty-four month horizon -- where the real competitive differentiation is going to emerge.

KEY POINTS TO HIT:
- Signal a shift from present evidence to future strategy
- Create anticipation for the forward-looking content

TRANSITION TO NEXT SLIDE:
"Most teams are using AI for exactly one thing. That's a mistake."

---

[SLIDE 12: AI Across the Full Software Development Lifecycle]
Duration: 100 seconds

SPEAKER NOTES:
Here is where most teams are today. Code generation: seventy-two percent. Documentation: sixty-seven percent. Code review and optimization: sixty-seven percent. Testing and debugging: fifty-six percent. [PAUSE] Notice the pattern? Almost all of that is in **two phases** of the development lifecycle: writing code and testing code.

But look at what happens when teams go broader. McKinsey found that top-performing AI teams are **six to seven times more likely** to have scaled to four or more AI use cases simultaneously. Organizations using AI across four or more SDLC phases see software quality improvements of thirty-one to forty-five percent, and time-to-market improvements of sixteen to thirty percent. Those are not incremental gains. Those are structural advantages.

Take a look at this pipeline on the slide. [PAUSE] Planning -- AI can do requirements analysis, dependency mapping, timeline forecasting. Code generation -- that's where most teams stop. Code review -- automated PR summaries, security flagging, style enforcement. Testing -- test case generation, regression detection, coverage analysis. Documentation -- inline docs, changelogs, architecture summaries. Deployment -- anomaly detection, rollback triggers.

How many of those six stages is your team actively using AI in? [PAUSE] If the answer is one or two, you are capturing maybe a third of the available productivity gain. Google has twenty-one percent of their code AI-assisted across their full pipeline. That is the direction this is heading.

And there is an amplifier here. The 2024 DORA report found that teams using internal developer platforms see a ten percent increase in team performance. When you combine platform engineering with AI tooling, the gains stack.

KEY POINTS TO HIT:
- Most teams are stuck in code generation only
- The 6-7x multiplier for teams with 4+ use cases is the key stat
- Walk through all six SDLC stages with specific AI applications
- Ask the audience to self-assess: how many stages are you covering?
- Platform engineering as a multiplier

TRANSITION TO NEXT SLIDE:
"And this pipeline integration? It's about to get a lot more interesting."

---

[SLIDE 13: The Next Shift -- From AI Assistants to AI Agents]
Duration: 75 seconds

SPEAKER NOTES:
Everything we have talked about so far is AI as an **assistant**. You prompt it. It responds. You integrate the output. That model is already shifting. [PAUSE]

IBM and Morning Consult surveyed a thousand developers building AI applications. Ninety-nine percent are exploring or actively developing AI agents for their workflows. Not assistants. Agents. The difference matters. An assistant responds to your prompt. An agent takes a specification, plans its approach, executes across multiple steps, tests its own output, and reports back. Your role shifts from writing code to **specifying intent and reviewing results**.

McKinsey is now predicting that individual contributors will spend part of their time functioning as -- and this is their phrase -- "engineering managers directing a junior team of asynchronous agents." [PAUSE]

Look at the market signal. Enterprise AI spending went from eleven and a half billion dollars in 2024 to thirty-seven billion in 2025. That is a three point two X jump in a **single year**. The AI coding assistant market alone is projected to hit nearly a hundred billion dollars by 2030.

Here is why this matters for you **today**. The teams that are building governance and review processes for AI assistants right now? They are the teams that will be ready to safely adopt agentic workflows when those tools mature. The teams that have not started? They will be eighteen months behind. And in this market, eighteen months is a long time.

KEY POINTS TO HIT:
- Clear distinction: assistant (reactive) vs. agent (proactive, multi-step)
- 99% exploring agents -- this is not fringe
- McKinsey's "engineering managers directing agents" framing
- Market spending signals conviction, not speculation
- Today's governance work is tomorrow's readiness

TRANSITION TO NEXT SLIDE:
"So what does it actually look like when a team does all of this well?"

---

[SLIDE 14: The Playbook -- What High-Performing AI-Augmented Teams Have in Common]
Duration: 60 seconds

SPEAKER NOTES:
If you are going to photograph one slide from this talk, make it this one. [PAUSE]

Six things that the high-performing teams have in common. **One**: a written AI tool policy. Which tools are approved, what the mandatory review standard is, how security scanning applies. **Two**: measurement before and after. Deployment frequency, change failure rate, PR cycle time. You cannot manage what you do not measure. **Three**: small PRs enforced. This directly counters the batch-size risk that DORA identified. **Four**: security scanning as a CI/CD gate. Not optional. Not manual. Automated and mandatory. **Five**: whole-SDLC adoption. Not just code completion -- documentation, testing, review, deployment. **Six**: developer autonomy within guardrails. Give your engineers the policy, not a workflow prescription. Trust them to calibrate within the boundaries you set.

How many of these six does your team have today? [PAUSE] If the answer is fewer than three, you have a clear roadmap for the next quarter.

KEY POINTS TO HIT:
- Frame this as the "screenshot slide" -- the distillation of the whole talk
- Read through all six concisely -- this is a summary, not new information
- Each point maps back to evidence from earlier slides
- Close with the self-assessment question

TRANSITION TO NEXT SLIDE:
"Let me leave you with three things you can do, starting this week."

---

[SLIDE 15: Three Actions. Three Time Horizons.]
Duration: 60 seconds

SPEAKER NOTES:
Three actions. Three time horizons. Each one has a clear owner.

**This week. Individual action.** Pick one task category -- boilerplate generation, test case writing, or PR summaries. Run a deliberate two-week experiment with an AI tool. Measure your output before and after. Document what you learn. This costs you nothing but attention.

**This sprint. Team action.** Write your AI tool policy. It's one document with three things in it: which AI tools are approved, what the mandatory human review standard is, and how security scanning applies to AI-generated code. This takes one hour. It prevents six months of inconsistency and drift. [PAUSE]

**This quarter. Leadership action.** Establish a measurement baseline. Deployment frequency. Change failure rate. PR cycle time. Measure these before and after structured AI adoption. Make the data visible to the team. You cannot improve what you are not tracking.

Remember where we started. Forty-six percent. [PAUSE] That number is not going down. The shift is here. The teams that will look back on this period as a turning point are the ones that started building structured, disciplined AI-augmented workflows **now** -- not the ones that waited for the tools to get better.

The tools are already good enough. The question is whether your process is ready for them. [PAUSE]

Thank you.

KEY POINTS TO HIT:
- Three actions, escalating in scope: individual, team, leadership
- Each action is concrete, time-bound, and low-cost to start
- Callback to the opening 46% statistic for narrative closure
- End with energy and conviction, not exhaustion
- Final line lands on process readiness, not tool quality

TRANSITION TO NEXT SLIDE:
N/A -- end of presentation. Open for questions.

---

## Timing Summary

| Slide | Title | Duration |
|-------|-------|----------|
| 1 | Title Slide | 0:30 |
| 2 | 46% Statistic | 1:15 |
| 3 | Compounding Pressures | 0:45 |
| 4 | Adoption vs. Impact Gap | 1:00 |
| 5 | Pillar 1 Divider | 0:15 |
| 6 | Productivity Evidence | 1:40 |
| 7 | Developer Experience | 0:50 |
| 8 | Pillar 2 Divider | 0:15 |
| 9 | Risk Map | 1:50 |
| 10 | Trust Gap | 1:00 |
| 11 | Pillar 3 Divider | 0:15 |
| 12 | Full-SDLC Integration | 1:40 |
| 13 | Agentic Horizon | 1:15 |
| 14 | The Playbook | 1:00 |
| 15 | Call to Action | 1:00 |
| **Total** | | **14:30** |

*30-second buffer for natural pacing variation and audience reactions.*

---

## Presenter Preparation Notes

**Rehearsal targets**: Read through twice silently, then deliver aloud twice. The scripts are written in speaking cadence -- short sentences, active voice -- so they should feel natural when spoken.

**Emphasis technique**: Words marked in **bold** should receive vocal stress. [PAUSE] markers indicate a full beat of silence -- roughly one second. Use these to let data points land before explaining them.

**Data confidence**: Every statistic in this script traces back to a cited source in the research document. If an audience member asks "where does that number come from," the source is documented. The most common challenge points will be the DORA stability finding (Slide 4/9) and the 48% security vulnerability figure (Slide 9).

**Audience read**: Watch for nods during the risk section (Slides 8-10). That is where credibility is earned with this audience. If you see skepticism during the productivity section, lean harder into methodology ("controlled study, forty-eight hundred developers, comparison group").

**Energy arc**: Start calm and data-grounded (Slides 1-4). Build energy through the productivity evidence (Slides 5-7). Drop to serious and direct for the risk section (Slides 8-10). Build again for the forward-looking section (Slides 11-13). Land the playbook with authority (Slide 14). Close with warmth and conviction (Slide 15).
