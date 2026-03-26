# GitHub Copilot Instructions

## Project Overview
Personal Organization App - A web-based personal organization system for managing tasks, habits, calendar events, memos, and ideas.

**Stack**: Next.js 15 (App Router) + TypeScript + tRPC + Prisma + NextAuth + Tailwind/shadcn + PostgreSQL (Supabase)

## Development Commands
```
npm run dev          # Start dev server (localhost:3000)
npm run build        # Production build
npm run lint         # ESLint check
npm run db:generate  # Generate Prisma client after schema changes
npm run db:push      # Push schema to database
npm run db:seed      # Seed database
```

## WORKFLOW - Core Guidelines

### Implementation Standards
- Never use mock data, results, or workarounds
- Generate complete, working code - no stubs, TODOs, or placeholder functions
- Implement tests after every checkpoint and verify all tests pass
- Always run `npm run lint` and `npm run build` to verify changes before completing

### Verification (Anti-Hallucination)
- Verify files exist before importing from them - do not invent import paths
- Verify functions, methods, and properties exist and check their actual signatures before calling them
- Verify package dependencies are installed in package.json before using them
- Verify database models and fields match `prisma/schema.prisma` before writing queries
- Run build/lint after each logical change, not just at the end
- Do not invent CLI flags, configuration options, or API parameters - verify they exist first
- Do not recommend installing new packages without verifying the exact package name exists in the npm registry
- When a library's API has changed across major versions (Next.js, Prisma, tRPC), prefer codebase patterns over training knowledge - the codebase reflects the installed version
- When a library's API is unclear, search the codebase for existing usage before guessing

### Grounding (Stay Anchored to Reality)
- Read the actual source file before modifying or referencing it
- Use existing project patterns as templates - copy and adapt, do not invent new patterns
- When uncertain, search the codebase for existing usage before writing new code
- State assumptions explicitly rather than proceeding silently
- When facing ambiguity, ask for clarification rather than guessing intent
- Before implementing a feature with ambiguous requirements, state your interpretation of the expected behavior in one sentence before writing code

### Scope Control
- Restate the specific task before starting implementation
- Only change what is necessary to fulfill the stated task
- Do not refactor, optimize, or "improve" adjacent code unless asked
- If changes affect shared interfaces, flag the downstream impact first

### File Organization
- Planning documents go in `.claude_plans/`
- Tests go in `tests/`
- Do not leave files in the root directory - sort into appropriate folders
- Prefer editing existing files over creating new ones

### Change Management
- Read and understand existing code before modifying it
- Match the style and patterns of surrounding code
- Make atomic, focused changes - one logical change per unit of work
- Verify changes compile and pass linting before marking complete

### Security
- Never commit secrets, credentials, API keys, or .env files
- Validate at system boundaries; trust internal code and framework guarantees
- All tRPC procedures that accept user input must validate with a complete Zod schema - do not use `.passthrough()`

### Code Quality
- Write self-documenting code with clear naming over excessive comments
- Delete dead code completely - no commented-out blocks or unused imports
- Do not add features, refactoring, or improvements beyond what was asked
- Keep functions focused with single responsibility

## Architecture

### Data Flow
```
React Components → tRPC hooks → tRPC routers → Prisma → PostgreSQL
```

### Key Directories
- `src/app/` - Next.js App Router pages and API routes
- `src/app/dashboard/` - Protected dashboard routes
- `src/components/ui/` - shadcn/ui components
- `src/server/api/routers/` - tRPC routers
- `src/server/auth.ts` - NextAuth configuration
- `src/lib/trpc.ts` - tRPC React hooks
- `src/types/` - Shared TypeScript types and Zod schemas
- `prisma/schema.prisma` - Database schema

### tRPC Patterns
When generating tRPC router code:
- Always scope queries with `userId: ctx.session.user.id`
- Use `protectedProcedure` for authenticated endpoints
- Use Zod for input validation
- Include related data to avoid N+1 queries
- Invalidate caches on mutations

```typescript
// Router pattern
export const exampleRouter = createTRPCRouter({
  getAll: protectedProcedure
    .input(z.object({ /* filters */ }).optional())
    .query(async ({ ctx, input }) => {
      return ctx.db.model.findMany({
        where: { userId: ctx.session.user.id, ...input },
        include: { /* related models */ },
        orderBy: { createdAt: "desc" },
      });
    }),
});

// Component pattern
const { data, isLoading } = api.router.procedure.useQuery();
const utils = api.useUtils();
const mutation = api.router.create.useMutation({
  onSuccess: () => utils.router.getAll.invalidate(),
});
```

## TypeScript Conventions
- Variables/functions: camelCase
- Types/interfaces/classes: PascalCase
- Constants: SCREAMING_SNAKE_CASE
- Files: kebab-case.ts or camelCase.ts
- Use `@/` path alias for imports from `src/`

## Prohibited Patterns
- Mock functions or placeholder data
- Using `any` type when proper types exist
- Queries without user scoping
- Direct database access outside tRPC routers
- Console.log in committed code
- Importing from files that do not exist in the project
- Using API methods without verifying their signatures
- Inventing package names, CLI flags, or configuration options

## UI Components
- Use shadcn/ui from `src/components/ui/`
- Handle all states: loading, error, empty, success
- Use `"use client"` directive for client components
- Use `cn()` utility for conditional Tailwind classes

## Testing
- All tests in `tests/` directory
- Test real behavior, not implementation details
- All tests must pass before completing work

## Authentication
- All data user-scoped via `ctx.session.user.id`
- `protectedProcedure` ensures authentication
- Dev bypass: `DEV_AUTH_BYPASS=true`
