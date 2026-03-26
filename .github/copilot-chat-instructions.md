# Copilot Chat Instructions

## Response Style
- Be direct and concise - lead with the answer, not reasoning
- No social validation ("Great question!") or hedging ("might", "could potentially")
- Skip filler words and unnecessary preamble
- Include code examples when explaining patterns

## When Generating Code
- Always generate complete, working code
- Never use mock data, stubs, or TODOs
- Match existing code style and patterns in this project
- Use tRPC + React Query for all server state
- Scope all database queries by userId
- Handle loading, error, and empty states in components

## When Reviewing Code
- Check for user-scoping in database queries
- Verify cache invalidation on mutations
- Look for TypeScript `any` types that should be specific
- Ensure no console.log statements remain
- Verify proper error handling at system boundaries

## Project-Specific Knowledge
- This uses Next.js 15 App Router (not Pages Router)
- tRPC routers are in `src/server/api/routers/`
- UI uses shadcn/ui components from `src/components/ui/`
- Path alias `@/` maps to `src/`
- Authentication via NextAuth with `protectedProcedure`
