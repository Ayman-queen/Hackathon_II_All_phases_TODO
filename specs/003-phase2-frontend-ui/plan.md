# Implementation Plan: Phase II Frontend UI

**Branch**: `003-phase2-frontend-ui` | **Date**: 2025-12-30 | **Spec**: [Phase II Frontend UI Specification](spec.md)
**Input**: Feature specification from `specs/003-phase2-frontend-ui/spec.md` with user requirements for complete frontend implementation

## Summary

Build a complete Next.js 16+ frontend for Evo-TODO that integrates Better Auth for authentication, provides protected routes for todo management, and delivers a polished UI with Shadcn/UI components and light/dark theme support. The implementation requires:
1. Better Auth client configuration with JWT plugin for secure token management
2. Custom API client that automatically attaches JWT tokens to all FastAPI backend requests
3. Protected routes using Next.js App Router with middleware-based auth redirection
4. State management via optimistic updates and SWR/React Query for todo operations
5. Complete CRUD interface with filtering, sorting, and theme persistence

## Technical Context

**Language/Version**: TypeScript 5.0+ with React 18.2+ / Next.js 16.0+
**Primary Dependencies**:
  - Frontend: better-auth (1.3.0+), next-themes (0.4.6+), shadcn-ui (0.9.5+), react-hook-form (7.50+), zod (3.22+), lucide-react (0.562+)
  - API: Custom fetch wrapper with JWT interception and error handling
**Storage**: localStorage (JWT token), browser sessionStorage (UI state), backend PostgreSQL via FastAPI REST API
**Testing**: jest, @testing-library/react for unit and integration tests
**Target Platform**: Web browser (modern ES2020+), mobile-responsive (320px+)
**Project Type**: Full-stack web application (frontend focused, backend API dependency)
**Performance Goals**:
  - Landing page: < 2 seconds load time
  - Todo list: < 2 seconds fetch from API
  - Filter/sort operations: < 500ms UI update
  - Theme toggle: < 1 second CSS transition
  - JWT token refresh: < 5 minutes before expiry
**Constraints**:
  - All API requests must include `Authorization: Bearer <token>` header
  - User isolation enforced (only user's own todos displayed)
  - WCAG 2.1 Level A accessibility compliance
  - Mobile-first responsive design (no horizontal scrolling at 320px)
**Scale/Scope**:
  - 6 main pages (landing, login, signup, todos, profile, settings)
  - ~15-20 React components (form, card, dialog, navbar, sidebar, etc.)
  - Complete CRUD operations (Create, Read, Update, Delete) for todos

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Mandatory Requirements (Phase II Constitution)

✅ **Full-Stack Web Application with Separation of Concerns**
- Frontend: Next.js 16+ (App Router) ✓
- Backend: FastAPI (dependency, already implemented) ✓
- Database: PostgreSQL via Neon (backend responsibility) ✓
- Authentication: Better Auth with JWT ✓

✅ **User-Scoped Data and JWT Authentication (Mandatory)**
- All API requests include JWT in Authorization header ✓ (FR-003, FR-008)
- Every response filtered by user_id from JWT claims ✓ (enforced on backend, Frontend respects boundaries)
- No endpoint returns unfiltered data ✓ (backend enforced, verified via FR-034, FR-035, FR-036)

✅ **Clean Code Principles**
- Functions small and focused (single responsibility) ✓ (design includes isolated hooks, components)
- Clear, self-documenting variable names ✓ (TypeScript with strict types)
- Minimal nesting, testable logic ✓ (component-based architecture with hooks)

✅ **Task-Driven Implementation**
- All code maps to Task IDs ✓ (tasks.md will be generated with explicit task references)
- No orphaned code ✓ (every feature maps to spec requirement → task → code)

✅ **Performance Over Brevity**
- Design prioritizes measurable performance ✓ (SC-001 through SC-011 define specific metrics)
- Profiling and optimization expected for critical paths ✓ (API calls, theme switching, list rendering)
- Trade-offs documented ✓ (plan includes rationale for each decision)

✅ **No Manual Code Writing**
- Code generation/scaffolding preferred ✓ (Shadcn/UI components generated, form hooks from react-hook-form)
- Manual coding justified post-exploration ✓ (custom API client and hooks necessary for JWT handling)

✅ **MCP Integration**
- Context7 MCP for technical documentation ✓ (used for API patterns, Next.js best practices)
- Better Auth MCP for authentication ✓ (used for JWT configuration, token management)

**GATE STATUS**: ✅ **PASS** - All constitutional mandates satisfied. Proceeding to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

**Selected Structure**: Web application frontend (Option 2) - Full-stack with separate frontend and backend

```text
frontend/                        # Next.js 16+ application
├── app/                        # App Router directory structure
│   ├── layout.tsx              # Root layout with ThemeProvider
│   ├── page.tsx                # Landing page (public)
│   ├── globals.css             # Global styles + Tailwind
│   ├── (auth)/                 # Auth group layout
│   │   ├── layout.tsx          # Auth pages layout
│   │   ├── login/
│   │   │   └── page.tsx        # Login page (FR-002)
│   │   └── signup/
│   │       └── page.tsx        # Signup page (FR-001)
│   └── (protected)/            # Protected group with auth middleware
│       ├── layout.tsx          # Protected layout with auth check
│       ├── todo/               # Todo dashboard
│       │   └── page.tsx        # Todo list with CRUD (FR-009 to FR-020)
│       ├── profile/
│       │   └── page.tsx        # User profile (FR-006, FR-018)
│       └── settings/
│           └── page.tsx        # Settings (theme, logout, FR-023)
│
├── lib/                        # Utility functions and configuration
│   ├── auth-client.ts          # Better Auth client setup with JWT plugin
│   ├── api-client.ts           # Custom fetch wrapper with JWT interception
│   ├── token-manager.ts        # JWT token refresh and expiration handling
│   └── constants.ts            # API endpoints, themes, etc.
│
├── hooks/                      # React hooks for auth and API
│   ├── useAuth.ts              # Auth state hook (session, JWT, signOut)
│   ├── useAuthenticatedApi.ts  # API request hook with error handling
│   ├── useTokenRefresh.ts      # Proactive token refresh hook
│   └── useTodos.ts             # Todo CRUD operations hook
│
├── components/                 # Reusable React components
│   ├── AuthProvider.tsx        # Auth context provider
│   ├── ProtectedRoute.tsx       # Route protection HOC (FR-004, FR-025)
│   ├── ThemeToggle.tsx          # Dark/light mode toggle (FR-020, FR-023)
│   ├── TodoForm.tsx            # Create/edit todo form (FR-015, FR-016)
│   ├── TodoList.tsx            # Display todos with filters/sorting (FR-010, FR-011, FR-012)
│   ├── TodoItem.tsx            # Individual todo card (FR-013)
│   ├── Navbar.tsx              # Top navigation with profile menu
│   ├── Sidebar.tsx             # Navigation sidebar (optional)
│   └── LoadingSpinner.tsx       # Loading states (FR-014)
│
├── types/                      # TypeScript types and interfaces
│   ├── auth.ts                 # Auth types (User, Session)
│   ├── todo.ts                 # Todo types (Todo, TodoStatus, Priority)
│   └── api.ts                  # API response types
│
├── styles/                     # CSS modules if needed (optional with Tailwind)
│   └── theme.css               # Theme-specific overrides
│
├── public/                     # Static assets (icons, logos, etc.)
│   └── ...
│
├── __tests__/                  # Test files (unit, integration)
│   ├── components/
│   ├── hooks/
│   └── lib/
│
├── middleware.ts               # Next.js middleware for auth redirection (FR-004)
├── next.config.js              # Next.js configuration
├── tsconfig.json               # TypeScript configuration
├── tailwind.config.js          # Tailwind CSS configuration
├── package.json                # Dependencies (already has: better-auth, next-themes, shadcn-ui)
└── README.md                   # Frontend documentation

backend/                         # FastAPI application (existing, for reference)
├── app/
│   ├── api/
│   │   └── todos.py            # Todo endpoints (already implemented T-216+)
│   ├── models/
│   ├── core/
│   └── main.py
└── ...

specs/003-phase2-frontend-ui/   # This feature's specification and planning
├── spec.md                     # Feature specification ✓
├── plan.md                     # Implementation plan (this file)
├── research.md                 # Phase 0 output (to be created)
├── data-model.md               # Phase 1 output (to be created)
├── contracts/                  # Phase 1 output (to be created)
├── quickstart.md               # Phase 1 output (to be created)
├── tasks.md                    # Phase 2 output (to be created via /sp.tasks)
└── checklists/
    └── requirements.md         # Specification validation checklist ✓
```

**Structure Decision**:
- **Frontend**: Next.js App Router with grouped routes for auth and protected pages. Hooks and utilities organized by domain (auth, API, state). Components follow atomic design principles.
- **Auth Isolation**: `(auth)` route group for public auth pages, `(protected)` group for user-scoped content. Middleware enforces redirection to login for unauthenticated access.
- **API Layer**: Custom `api-client.ts` wrapper provides centralized JWT attachment and error handling. All API calls route through this client.
- **Token Management**: Separate `token-manager.ts` handles refresh logic and expiration detection. `useTokenRefresh` hook ensures proactive token refresh.
- **State Management**: React hooks for auth state (`useAuth`) and API calls (`useAuthenticatedApi`, `useTodos`). Optimistic updates and error recovery at component level.

## Phase 0: Research & Architecture Decisions

### Key Design Decisions

**1. Better Auth Integration Pattern (JWT Plugin)**
- **Decision**: Use Better Auth's official `createAuthClient` from `better-auth/react` with `jwtClient()` plugin
- **Rationale**: Provides native JWT support, automatic token issuance on login/signup, built-in session management
- **Alternatives Rejected**: Custom OAuth2 implementation (too complex), Auth.js/NextAuth (different framework)
- **Trade-off**: Dependency on Better Auth API; mitigated by using official MCP for support

**2. JWT Token Storage & Retrieval**
- **Decision**: Store JWT in localStorage with `getValidToken()` utility for proactive refresh
- **Rationale**: Persistent across page reloads, accessible from components, enables refresh before expiration
- **Alternatives**: httpOnly cookies (more secure but no JS access), sessionStorage (lost on tab close), memory-only (lost on refresh)
- **Trade-off**: Slightly reduced security vs. accessibility; mitigated by refresh logic checking expiration (5-min buffer)

**3. API Client Implementation**
- **Decision**: Custom fetch wrapper (`api-client.ts`) with JWT interception and centralized error handling
- **Rationale**: Centralizes JWT attachment logic, enables consistent error handling, avoids request duplication
- **Alternatives**: Axios (extra dependency), tRPC (backend integration not ready), SWR/React Query (data fetching, not HTTP layer)
- **Trade-off**: Manual fetch wrapper vs. external library; justified by minimal overhead and full control

**4. State Management for Todos**
- **Decision**: React hooks (`useTodos`, `useAuthenticatedApi`) with optimistic updates and error recovery
- **Rationale**: Simple for single-user TODO app, native to React, no Redux/Zustand complexity
- **Alternatives**: React Query (powerful but overkill), Redux (boilerplate-heavy), Context API (prop drilling)
- **Trade-off**: Manual cache management vs. library features; mitigated by simple todo domain

**5. Protected Routes Implementation**
- **Decision**: Use Next.js middleware (`middleware.ts`) for auth redirection + ProtectedRoute component wrapper
- **Rationale**: Middleware catches redirects early (faster), component wrapper provides granular control per route
- **Alternatives**: Route guards only (loose in components), API-only checks (late failure), HOC only (less flexibility)
- **Trade-off**: Two-layer protection adds slight complexity; justified by defense-in-depth and performance

**6. Theming Architecture**
- **Decision**: Use `next-themes` library with localStorage persistence + CSS class-based switching
- **Rationale**: Zero-FOUC (no flash of wrong theme), system preference detection, easy Tailwind integration
- **Alternatives**: Context API (manual), CSS variables only (no persistence), localStorage (manual hydration)
- **Trade-off**: Additional dependency (`next-themes`); justified by solving FOUC and system detection

**7. Form Handling**
- **Decision**: React Hook Form + Zod validation for type-safe, performant forms
- **Rationale**: Minimal re-renders, built-in validation, TypeScript integration
- **Alternatives**: Formik (more boilerplate), native HTML (no validation), Unform (unmaintained)
- **Trade-off**: Two dependencies; justified by significant DX improvement and validation

### Technology Selection Summary

| Layer | Technology | Why | Dependency |
|-------|-----------|-----|----------|
| Framework | Next.js 16+ | Modern React, built-in routing, SSR ready | Required |
| Auth | Better Auth | Secure, JWT-native, official MCP support | Required |
| Token Mgmt | Custom wrapper | Centralized JWT logic, no external overhead | Custom |
| API Calls | Fetch API | Native, no extra deps, sufficient for REST | Native |
| Styling | Tailwind CSS | Utility-first, small bundle, dark mode support | Installed |
| Components | Shadcn/UI | Headless, accessible, Tailwind-based | Installed |
| Forms | React Hook Form + Zod | Performant, type-safe, minimal boilerplate | Installed |
| Theme | next-themes | Zero-FOUC, system detection, localStorage | Installed |
| Type Safety | TypeScript | Full type coverage, better DX and safety | Installed |

## Phase 1: Detailed Design (Data Model & API Contracts)

### Data Model

**User Entity** (from Better Auth)
```typescript
interface User {
  id: string;              // UUID from Better Auth
  email: string;           // Unique email
  name?: string;           // Optional full name
  emailVerified: boolean;  // Email verification status
  createdAt: Date;         // Account creation timestamp
  updatedAt: Date;         // Last update timestamp
}
```

**Todo Entity** (from FastAPI Backend)
```typescript
interface Todo {
  id: string;              // UUID
  userId: string;          // User ID (from JWT claims)
  title: string;           // Required, 1-255 chars
  description?: string;    // Optional, 0-2000 chars
  priority: 'HIGH' | 'MEDIUM' | 'LOW';  // Default: 'MEDIUM'
  completed: boolean;      // Default: false
  dueDate?: Date;          // Optional due date
  createdAt: Date;         // Timestamp
  updatedAt: Date;         // Timestamp
}
```

**Auth Session State** (Frontend)
```typescript
interface AuthSession {
  session: User | null;          // Current user or null
  token: string | null;          // JWT token
  isLoading: boolean;            // Auth state loading
  error: Error | null;           // Auth error
  signOut: () => Promise<void>;  // Sign out function
}
```

**Todo List State** (Frontend)
```typescript
interface TodoListState {
  todos: Todo[];
  filter: 'ALL' | 'PENDING' | 'COMPLETED';  // Current filter
  sort: 'PRIORITY' | 'DUE_DATE' | 'TITLE';  // Current sort
  isLoading: boolean;
  error: string | null;
}
```

### API Contracts (Frontend → FastAPI Backend)

**Authentication Endpoints** (Managed by Better Auth)
```
POST /api/auth/sign-up
  Request: { email, password, name? }
  Response: { user: User, token: JWT }
  Status: 201 | 400 (email exists) | 422 (invalid input)

POST /api/auth/sign-in
  Request: { email, password }
  Response: { user: User, token: JWT }
  Status: 200 | 401 (invalid credentials) | 404 (user not found)

POST /api/auth/sign-out
  Headers: Authorization: Bearer <token>
  Response: { success: true }
  Status: 200 | 401 (unauthorized)

GET /api/auth/session
  Headers: Authorization: Bearer <token>
  Response: { user: User, token: JWT }
  Status: 200 | 401 (expired/invalid token)
```

**Todo Endpoints** (Implemented in FastAPI)
```
GET /api/todos
  Headers: Authorization: Bearer <token>
  Query: ?filter=ALL|PENDING|COMPLETED&sort=PRIORITY|DUE_DATE|TITLE
  Response: { todos: Todo[], count: number }
  Status: 200 | 401 (unauthorized) | 400 (invalid filter)

POST /api/todos
  Headers: Authorization: Bearer <token>
  Body: { title, description?, priority, dueDate? }
  Response: { todo: Todo }
  Status: 201 | 400 (validation error) | 401 (unauthorized)

PATCH /api/todos/{id}
  Headers: Authorization: Bearer <token>
  Body: { title?, description?, priority?, completed?, dueDate? }
  Response: { todo: Todo }
  Status: 200 | 404 (not found) | 401 (unauthorized) | 403 (not owner)

DELETE /api/todos/{id}
  Headers: Authorization: Bearer <token>
  Response: { success: true }
  Status: 200 | 404 (not found) | 401 (unauthorized) | 403 (not owner)

PATCH /api/todos/{id}/toggle
  Headers: Authorization: Bearer <token>
  Body: { completed: boolean }
  Response: { todo: Todo }
  Status: 200 | 404 (not found) | 401 (unauthorized) | 403 (not owner)
```

**Error Response Format** (Consistent)
```typescript
interface ErrorResponse {
  error: string;           // Error code: INVALID_INPUT, UNAUTHORIZED, NOT_FOUND, etc.
  message: string;         // Human-readable message
  status: number;          // HTTP status code
  details?: Record<string, string>;  // Field-level errors for validation
}
```

### Key Design Patterns

**1. JWT Token Lifecycle**
```
Login/Signup
  ↓
Better Auth issues JWT + stores in localStorage
  ↓
Request to /api/todos
  ↓
API Client retrieves JWT from localStorage
  ↓
Attach `Authorization: Bearer <token>` header
  ↓
FastAPI validates JWT and returns todos
  ↓
5 minutes before expiry
  ↓
Token Manager calls refresh endpoint
  ↓
New JWT stored in localStorage
  ↓
Automatic attachment continues
```

**2. Error Handling Flow**
```
API Request Fails
  ↓
Check status code
  ↓
401 (Unauthorized)
  ↓
Clear JWT + redirect to /login
  ↓
Other errors (4xx, 5xx)
  ↓
Display error message to user
  ↓
Offer retry option
```

**3. Optimistic Update Pattern**
```
User clicks "Create Todo"
  ↓
Immediately add todo to local state (optimistic)
  ↓
Send POST /api/todos in background
  ↓
If success
  ↓
Update local state with server response (ID, timestamps)
  ↓
If failure
  ↓
Rollback to previous state
  ↓
Show error message
  ↓
Offer retry
```

## Complexity Tracking

**No constitutional violations** - No complexity justification needed. All design decisions follow best practices and are well-justified above.
