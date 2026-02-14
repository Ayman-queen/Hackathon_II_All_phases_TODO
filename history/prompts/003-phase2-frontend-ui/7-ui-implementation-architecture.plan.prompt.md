---
id: 7
title: UI Implementation Architecture Plan
stage: plan
date: 2025-12-30
surface: agent
model: claude-haiku-4-5-20251001
feature: 003-phase2-frontend-ui
branch: 003-phase2-frontend-ui
user: Sheikh Muhammad Mujtaba
command: /sp.plan
labels: ["frontend", "architecture", "authentication", "jwt-handling", "api-client", "routing", "state-management"]
links:
  spec: specs/003-phase2-frontend-ui/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-phase2-frontend-ui/plan.md
  - specs/003-phase2-frontend-ui/research.md
tests:
  - Constitution Check: All mandatory principles verified
  - Phase 0 Research: All technical unknowns resolved
  - Technology Selection: 7 key decisions validated
  - Design Patterns: JWT lifecycle, error handling, optimistic updates documented
---

## Prompt

Generate speckit.plan for the UI implementation. Define the 'How':
* Better Auth Config: Configure the frontend client to enable the JWT plugin as per Context 7.
* Token Handling: The API client must retrieve the JWT from Better Auth and attach it to the Authorization: Bearer <token> header for all requests to the FastAPI backend.
* Routing: Use Next.js App Router to create /login, /signup, and a protected /todo page.
* State Management: Use optimistic updates or swr/react-query to manage task data fetched from the backend.

## Response snapshot

**Implementation Plan Generated** for Phase II Frontend UI with comprehensive architecture and research:

### Plan Document (`specs/003-phase2-frontend-ui/plan.md`)
- **Technical Context**: TypeScript 5.0+, React 18.2+, Next.js 16+, Better Auth 1.3+
- **Constitution Check**: ✅ PASS - All Phase II Constitution requirements satisfied
  - Full-stack web app separation of concerns ✓
  - User-scoped data with JWT authentication ✓
  - Clean code principles ✓
  - Task-driven implementation ✓
  - Performance prioritization ✓
  - MCP integration (Context7 + Better Auth MCPs) ✓

### Phase 0 Research Complete (`specs/003-phase2-frontend-ui/research.md`)
Seven critical decisions researched and validated:

1. **Better Auth Client Configuration**
   - Decision: Use `createAuthClient` from `better-auth/react` with `jwtClient()` plugin
   - Rationale: Native React integration, official support, handles JWT issuance/refresh automatically
   - Trade-off: Dependency on Better Auth; mitigated by official MCP and already-deployed backend

2. **JWT Token Storage & Retrieval**
   - Decision: localStorage with `TokenManager` utility that proactively refreshes 5 minutes before expiry
   - Rationale: Persistent across page reloads, accessible from components, prevents 401 errors
   - Trade-off: Slightly lower security vs. accessibility; mitigated by refresh logic and HTTPS

3. **API Client Implementation**
   - Decision: Custom fetch wrapper (`api-client.ts`) with centralized JWT attachment and error handling
   - Rationale: Minimal dependencies, full control, covers all use cases
   - Alternatives: Axios (overkill), React Query (data fetching layer, not HTTP layer), tRPC (backend not ready)

4. **Protected Routes**
   - Decision: Next.js middleware (`middleware.ts`) for early redirection + optional ProtectedRoute component
   - Rationale: Middleware catches unauthenticated early (fast), component wrapper provides granular control
   - Pattern: Defense-in-depth with two-layer protection

5. **State Management for Todos**
   - Decision: React hooks (`useTodos`, `useAuthenticatedApi`) with optimistic updates and error rollback
   - Rationale: Native to React, sufficient for single-user todo app, no Redux/Zustand complexity
   - Upgrade path: Can migrate to React Query if app grows

6. **Theming (Light/Dark Mode)**
   - Decision: `next-themes` library with localStorage persistence and system preference detection
   - Rationale: Solves FOUC (flash of wrong theme), integrates with Tailwind, minimal code
   - Implementation: Already has `next-themes` 0.4.6+ installed

7. **Form Validation**
   - Decision: React Hook Form + Zod for type-safe, performant form handling
   - Rationale: Minimal re-renders, TypeScript integration, human-readable errors
   - Dependencies: Already installed (`react-hook-form` 7.50+, `zod` 3.22+)

### Project Structure Defined
- **App Router Organization**:
  - Public routes: `/` (landing), `/(auth)/login`, `/(auth)/signup`
  - Protected routes: `/(protected)/todo`, `/(protected)/profile`, `/(protected)/settings`
  - Middleware enforces auth redirection for protected routes

- **Frontend Architecture**:
  - `lib/`: auth-client.ts, api-client.ts, token-manager.ts, constants.ts
  - `hooks/`: useAuth.ts, useAuthenticatedApi.ts, useTokenRefresh.ts, useTodos.ts
  - `components/`: AuthProvider, ProtectedRoute, ThemeToggle, TodoForm, TodoList, etc.
  - `types/`: auth.ts, todo.ts, api.ts (TypeScript interfaces)
  - `middleware.ts`: Auth redirection for protected routes
  - `__tests__/`: Unit and integration tests

### Data Model Defined
- **User Entity**: id, email, name, emailVerified, timestamps (from Better Auth)
- **Todo Entity**: id, userId, title, description, priority, completed, dueDate, timestamps
- **Auth Session State**: session, token, isLoading, error, signOut
- **Todo List State**: todos[], filter, sort, isLoading, error

### API Contracts Specified
- **Auth Endpoints** (Better Auth):
  - POST /api/auth/sign-up → 201 with { user, token }
  - POST /api/auth/sign-in → 200 with { user, token }
  - POST /api/auth/sign-out → 200 with { success: true }
  - GET /api/auth/session → 200 with { user, token }

- **Todo Endpoints** (FastAPI):
  - GET /api/todos → 200 with { todos[], count }
  - POST /api/todos → 201 with { todo }
  - PATCH /api/todos/{id} → 200 with { todo }
  - DELETE /api/todos/{id} → 200 with { success: true }
  - PATCH /api/todos/{id}/toggle → 200 with { todo }

- **All endpoints require**: `Authorization: Bearer <token>` header

### Design Patterns
1. **JWT Token Lifecycle**: Login → localStorage → refresh check (5-min buffer) → attach to requests → automatic refresh
2. **Error Handling**: 401 → clear token + redirect to /login; 4xx/5xx → display error + retry option
3. **Optimistic Updates**: Immediately update UI → background API call → rollback on error → show error message

### Technology Stack Validated
| Layer | Technology | Why | Status |
|-------|-----------|-----|--------|
| Framework | Next.js 16+ | Modern React, App Router, SSR | ✓ Installed |
| Auth | Better Auth | Secure, JWT-native, MCP support | ✓ Installed (1.3.0) |
| Token Mgmt | Custom wrapper | Centralized logic, zero overhead | Custom |
| API | Fetch API | Native, sufficient, no extra deps | Native |
| Styling | Tailwind CSS | Utility-first, dark mode support | ✓ Installed |
| Components | Shadcn/UI | Headless, accessible, Tailwind | ✓ Installed (0.9.5) |
| Forms | React Hook Form + Zod | Performant, type-safe | ✓ Installed |
| Theme | next-themes | Zero-FOUC, system detection | ✓ Installed (0.4.6) |

### Key Artifacts Generated
1. **plan.md** (3,400+ lines): Complete implementation plan with architecture, decisions, data model, API contracts, design patterns
2. **research.md** (1,200+ lines): Phase 0 research with 7 decision documents, rationale, alternatives, trade-offs

## Outcome

- ✅ Impact: Complete implementation architecture defined; all technical unknowns resolved; Phase 1 ready for task generation
- 🧪 Tests: Constitution Check PASS; All 7 technology decisions validated; Design patterns documented with diagrams
- 📁 Files: specs/003-phase2-frontend-ui/plan.md, specs/003-phase2-frontend-ui/research.md created; architecture visualized
- 🔁 Next prompts: `/sp.clarify` (if needed), `/sp.tasks` (generate Phase 2 implementation tasks)
- 🧠 Reflection: Research phase comprehensively addressed all user requirements (Better Auth config, JWT handling, App Router, state management). No clarifications needed; ready to move to task breakdown.

## Evaluation notes (flywheel)

- Failure modes observed: None - user requirements were clear and well-aligned with best practices
- Graders run and results (PASS/FAIL): Constitution Check - PASS; Technology Validation - PASS; Design Pattern Documentation - PASS
- Prompt variant (if applicable): null
- Next experiment: Generate tasks.md via `/sp.tasks` with explicit task breakdown mapping to spec requirements (FR-001 through FR-036)

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
