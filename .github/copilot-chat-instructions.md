# Copilot Chat Instructions

## Response Style
- Be direct and concise - lead with the answer, not reasoning
- No social validation ("Great question!") or hedging ("might", "could potentially")
- Skip filler words and unnecessary preamble
- Include code examples when explaining patterns

## Verification Requirements
- Before suggesting imports, verify the file and export actually exist in the project
- Before using a function or method, verify its actual signature - do not guess parameters
- Before referencing a package, verify it exists in package.json
- Before writing database queries, verify models and fields match prisma/schema.prisma
- Do not invent CLI flags, configuration options, or API parameters

## When Generating Code
- Always generate complete, working code
- Never use mock data, stubs, or TODOs
- Match existing code style and patterns in this project
- Use tRPC + React Query for all server state
- Scope all database queries by userId
- Handle loading, error, and empty states in components
- Copy patterns from existing working code rather than inventing new ones

## When Reviewing Code
- Check for user-scoping in database queries
- Verify cache invalidation on mutations
- Look for TypeScript `any` types that should be specific
- Ensure no console.log statements remain
- Verify proper error handling at system boundaries
- Check that all imports reference files that actually exist

## Project-Specific Knowledge
- This uses Next.js 15 App Router (not Pages Router)
- tRPC routers are in `src/server/api/routers/`
- UI uses shadcn/ui components from `src/components/ui/`
- Path alias `@/` maps to `src/`
- Authentication via NextAuth with `protectedProcedure`
