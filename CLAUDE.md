# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Personal Organization App** - A web-based personal organization system (digital Filofax) for managing tasks, habits, calendar events, memos, and ideas.

**Stack**: Next.js 15 (App Router) + TypeScript + tRPC + Prisma + NextAuth + Tailwind/shadcn + PostgreSQL (Supabase)

## Development Commands

```bash
npm run dev          # Start dev server (localhost:3000)
npm run build        # Production build
npm run lint         # ESLint check
npm run db:generate  # Generate Prisma client after schema changes
npm run db:push      # Push schema to database (use for development)
npm run db:studio    # Open Prisma Studio GUI
npm run db:seed      # Seed database (tsx prisma/seed.ts)
```

## Architecture

### Data Flow
```
React Components → tRPC hooks → tRPC routers → Prisma → PostgreSQL
```

### Key Directories
- `src/app/` - Next.js App Router pages and API routes
- `src/app/dashboard/` - Protected dashboard routes (tasks, habits, memos, ideas, planner)
- `src/components/ui/` - shadcn/ui components
- `src/components/layout/` - Sidebar and Header components
- `src/server/api/routers/` - tRPC routers (tasks, habits, memos, ideas, calendar, categories, tags)
- `src/server/auth.ts` - NextAuth config (GitHub, Google OAuth + dev bypass)
- `src/server/db.ts` - Prisma client singleton
- `src/lib/trpc.ts` - tRPC React hooks (`api` object)
- `src/types/` - Shared TypeScript types and Zod input schemas
- `prisma/schema.prisma` - Database schema

### Database Models
Core models: `User`, `Task`, `Subtask`, `Category`, `Habit`, `HabitLog`, `Memo`, `Tag`, `Idea`, `CalendarEvent`, `GitHubRepo`, `UserPreferences`

### Key Patterns
```typescript
// tRPC query in components
const { data, isLoading } = api.tasks.getAll.useQuery({ status: "TODO" });

// Mutation with cache invalidation
const utils = api.useUtils();
const create = api.tasks.create.useMutation({
  onSuccess: () => utils.tasks.getAll.invalidate(),
});
```

### Adding a New Feature
1. Define/update Prisma schema → `npm run db:generate` → `npm run db:push`
2. Create/update tRPC router in `src/server/api/routers/`
3. Add router to `src/server/api/root.ts`
4. Build UI components in `src/app/dashboard/[feature]/`
5. Wire up with `api.[router].[procedure].useQuery()` or `useMutation()`

### Authentication
- All data user-scoped via `ctx.session.user.id` in protected procedures
- Dev bypass: Set `DEV_AUTH_BYPASS=true` in `.env`

### Path Alias
Use `@/` to import from `src/`: `import { api } from "@/lib/trpc";`

## Project Conventions

- Planning documents go in `.claude_plans/`
- Tests go in `tests/`
- No mocks/stubs/TODOs - implement complete working code
- Run `npm run lint` and `npm run build` to verify changes
- See `.claude/rules/` for detailed guidelines by concern
