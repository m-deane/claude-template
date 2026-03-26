# Copilot Chat Instructions

## Response Style
- Be direct and concise - lead with the answer, not reasoning
- No social validation ("Great question!") or hedging ("might", "could potentially")
- Skip filler words and unnecessary preamble
- Include code examples when explaining patterns

## Verification Requirements
- Before suggesting imports, verify the file and export actually exist in the project
- Before using a function or method, verify its actual signature - do not guess parameters
- Before referencing a package, verify it exists in the project's dependency file
- Before writing database queries, verify models and fields match the schema
- Do not invent CLI flags, configuration options, or API parameters

## When Generating Code
- Always generate complete, working code
- Never use mock data, stubs, or TODOs
- Match existing code style and patterns in this project
- Copy patterns from existing working code rather than inventing new ones
- Handle error and edge cases explicitly

## When Reviewing Code
- Check for proper input validation at system boundaries
- Verify error handling covers realistic failure modes
- Look for loosely-typed constructs that should be specific
- Ensure no debug print/log statements remain
- Check that all imports reference files that actually exist
