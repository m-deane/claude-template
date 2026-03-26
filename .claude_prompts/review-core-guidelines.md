# Review Core Guidelines for Anti-Hallucination Effectiveness

You are an expert in LLM behavior, prompt engineering, and AI-assisted development workflows. Your task is to audit a project's core workflow guidelines and evaluate whether they are specific enough to prevent LLM hallucinations, achieve consistent results, and produce valid code across sessions.

## Context

LLMs in coding contexts have predictable failure modes. The most impactful ones are:

1. **Phantom Imports** - Importing from files or modules that do not exist in the project
2. **Invented APIs** - Calling functions, methods, or properties with wrong signatures or that do not exist
3. **Fabricated Packages** - Using npm packages, CLI tools, or flags that do not exist or are deprecated
4. **Schema Drift** - Referencing database columns, relations, or models that do not match the actual schema
5. **Version Confusion** - Mixing API patterns from different major versions of a framework
6. **Plausible-But-Wrong Logic** - Code that looks correct syntactically but has subtle logical errors
7. **Scope Creep** - Solving problems that were not asked for, refactoring adjacent code, adding "improvements"
8. **Silent Assumptions** - Making decisions based on assumed context without verifying
9. **Pattern Invention** - Creating new architectural patterns instead of following existing project conventions
10. **Confidence Without Verification** - Proceeding confidently on uncertain ground instead of flagging uncertainty

## Audit Instructions

### Step 1: Read All Guideline Files

Read every file that contains instructions for the LLM:
- Root `CLAUDE.md`
- `.claude/CLAUDE.md`
- `.claude/rules/*.md`
- `.cursorrules`
- `.github/copilot-instructions.md`
- `.github/copilot-chat-instructions.md`

### Step 2: Map Guidelines to Failure Modes

For each of the 10 failure modes listed above, check whether the guidelines contain a **specific, actionable rule** that directly mitigates it. Rate each:

| Failure Mode | Rule Exists? | Rule is Specific Enough? | Rule is Actionable? | Score (0-3) |
|---|---|---|---|---|
| Phantom Imports | Y/N | Y/N | Y/N | |
| Invented APIs | Y/N | Y/N | Y/N | |
| ... | | | | |

**Scoring:**
- 0 = No rule exists
- 1 = Rule exists but is too vague to change behavior (e.g., "be careful with imports")
- 2 = Rule exists and is specific but lacks a clear action (e.g., "don't use wrong imports")
- 3 = Rule exists, is specific, and tells the LLM exactly what to do (e.g., "verify files exist before importing from them - do not invent import paths")

### Step 3: Evaluate Rule Specificity

For each rule in the guidelines, evaluate:

**Is it behavioral?** Does it describe a specific action the LLM should take or avoid?
- BAD: "Write good code" (aspirational, not behavioral)
- GOOD: "Verify functions exist and check their actual signatures before calling them" (specific action)

**Is it verifiable?** Can you objectively determine if the rule was followed?
- BAD: "Be careful with dependencies" (subjective)
- GOOD: "Verify package dependencies are installed in package.json before using them" (checkable)

**Is it scoped?** Does it apply to a clear context, or is it so broad it becomes noise?
- BAD: "Always double-check everything" (too broad, becomes background noise)
- GOOD: "Run build/lint after each logical change, not just at the end" (specific checkpoint)

### Step 4: Check for Missing Categories

The guidelines should cover these four categories. Flag any that are missing or underdeveloped:

**1. Verification Rules** (Anti-hallucination)
- File existence verification before imports
- Function/method signature verification before calls
- Package dependency verification before usage
- Schema verification before database queries
- CLI flag/option verification before command construction
- Incremental build verification (after each change, not just at end)
- New dependency verification (do not recommend packages without verifying they exist in the registry - 19.7% of LLM-recommended packages are fabricated)
- Version currency awareness (prefer codebase patterns over training knowledge for fast-moving libraries)

**2. Grounding Rules** (Anchoring to reality)
- Read actual source before modifying
- Use existing patterns as templates
- Search codebase for usage examples before writing new code
- State assumptions explicitly
- Ask for clarification rather than guessing
- Surface interpretation of ambiguous requirements before implementing (28% intent misuse rate without this)
- Reference concrete code (file paths, function names) not abstractions

**3. Scope Control Rules** (Preventing drift)
- Restate task before starting
- Change only what is necessary
- No unsolicited refactoring or improvements
- Flag downstream impact of shared interface changes
- No added abstractions or configurability beyond request

**4. Process Rules** (Consistency)
- No mock data or workarounds
- Complete code only - no stubs/TODOs
- Tests after every checkpoint
- Lint/build verification
- File organization standards

**5. Security Rules** (Input validation)
- All procedures accepting user input must validate with complete schemas
- No `.passthrough()` or open-ended input acceptance
- Null/undefined/empty handling required in both UI and server logic (not just UI layer)

### Step 5: Check Cross-Tool Consistency

Compare the guidelines across all tool configurations (Claude, Cursor, Copilot). Flag:
- Rules present in one config but missing from others
- Rules worded differently that could cause inconsistent behavior
- Rules that are tool-specific and should not be in other configs

### Step 6: Test with Adversarial Scenarios

For each guideline, construct a scenario where an LLM would typically hallucinate and check if the rule would prevent it:

**Scenario 1: New feature request**
"Add a notifications system." Would the rules prevent the LLM from inventing a `@/lib/notifications` module that doesn't exist?

**Scenario 2: Bug fix in unfamiliar code**
"Fix the calculation in the analytics module." Would the rules force the LLM to read the actual module before making assumptions about the data model?

**Scenario 3: Package integration**
"Add email sending with Resend." Would the rules prevent the LLM from using a made-up API method like `resend.emails.sendBatch()` without verifying it exists?

**Scenario 4: Database query**
"Show all records with their child count." Would the rules prevent the LLM from referencing a relation or column that may not exist in the actual schema?

**Scenario 5: Scope creep**
"Fix the date formatting on the dashboard." Would the rules prevent the LLM from also refactoring the component's state management?

**Scenario 6: New dependency recommendation (Slopsquatting)**
"Add CSV export for tasks." Would the rules prevent the LLM from recommending `npm install csv-export-helper` (a fabricated package name)? Research shows 19.7% of LLM-recommended packages are non-existent, and 58% of fabricated names repeat consistently, making them supply-chain attack vectors.

**Scenario 7: Version confusion**
"Add a server action for form submission." Would the rules prevent the LLM from using patterns from an older version of the framework instead of the version actually installed?

**Scenario 8: Ambiguous requirement**
"Make the dashboard faster." Would the rules force the LLM to state its interpretation (e.g., "I interpret this as: optimize the dashboard page's initial load time by reducing database queries") before implementing?

## Output Format

### Scorecard
A table showing each failure mode, its score (0-3), and the exact rule text that addresses it (or "MISSING" if none).

### Gap Analysis
For each score below 3, provide:
- The specific gap
- Why it matters (what goes wrong without it)
- The exact rule text to add
- Which files need updating

### Redundancy Check
List any rules that appear in multiple files unnecessarily, and recommend where each should live (single source of truth).

### Adversarial Test Results
For each scenario, state whether the current guidelines would prevent the hallucination (PASS/FAIL) and explain why.

### Updated Guidelines
Provide the complete, updated core guidelines section that addresses all gaps. Structure it as:

```
## WORKFLOW - Core Guidelines

### Implementation Standards
[rules]

### Verification (Anti-Hallucination)
[rules]

### Grounding (Stay Anchored to Reality)
[rules]

### Scope Control
[rules]

### Change Management
[rules]

### Security
[rules]

### Code Quality
[rules]
```

### Recommended Updates
For each tool configuration file that needs changes, provide the exact diff or replacement content.
