# Implementation Plan: Professional UI & Advanced CRUD

**Branch**: `005-professional-ui` | **Date**: 2026-01-02 | **Spec**: [specs/005-professional-ui/spec.md](spec.md)
**Input**: Feature specification from `specs/005-professional-ui/spec.md`

## Summary

Build a professional, responsive task management dashboard with advanced CRUD operations using Next.js 15 (App Router), Shadcn/UI components, and Better Auth. Implement immediate UI feedback using `useOptimistic` for CRUD operations, Shadcn Dialog for confirmations, Shadcn Popover for inline selections, and Sonner/Shadcn Toast for notifications. Support light/dark themes with `next-themes`, bulk operations with Set-based selection, and API integration with batch operations via Promise.all if backend doesn't support native batching.

## Technical Context

**Language/Version**: TypeScript 5.x, Next.js 16+ (App Router), React 19+
**Primary Dependencies**:
- Frontend: Next.js 16, React 19, Shadcn/UI, Sonner (or Shadcn Toast), next-themes, React Hook Form, Zod
- Backend: FastAPI (existing), SQLModel, Pydantic
- Authentication: Better Auth with JWT tokens
- Database: PostgreSQL (Neon Serverless, existing)

**Storage**: PostgreSQL via SQLModel (backend); localStorage for theme preference (client)
**Testing**: Jest + React Testing Library (frontend), pytest (backend)
**Target Platform**: Web (responsive design: mobile/tablet/desktop)
**Project Type**: Web application (Next.js frontend + FastAPI backend, existing monorepo)
**Performance Goals**: Dashboard loads in <2s, CRUD operations complete in <500ms perceived latency (useOptimistic), notifications appear within 500ms
**Constraints**:
- All endpoints require JWT token in Authorization header
- All responses filtered by user_id from JWT claims
- No unfiltered data access
- Responsive design must pass WCAG 2.1 AA accessibility standards
- Theme preference must persist across sessions
- Bulk operations must handle up to 100 tasks in <3 seconds

**Scale/Scope**: Single feature (Professional UI), 4-5 main pages/components, ~2000 LOC frontend

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Verification

- ✅ **Full-Stack Separation**: Frontend (Next.js 16 App Router) + Backend (FastAPI) with clear API contracts
- ✅ **User-Scoped Data**: All API calls require JWT token; responses filtered by user_id from token claims
- ✅ **JWT Authentication**: Better Auth integration for token management and validation
- ✅ **Clean Code**: Single responsibility components (TaskList, TaskForm, BulkActions, ThemeToggle, Navbar), focused functions, testable logic
- ✅ **Task-Driven Implementation**: All code changes map to Task IDs in tasks.md (TBD in Phase 2)
- ✅ **Performance First**: useOptimistic for immediate feedback, <500ms perceived latency, WCAG 2.1 AA compliance
- ✅ **No Manual Code Generation**: Using Shadcn/UI scaffolding and Next.js built-in templates
- ✅ **MCP Compliance**: Better Auth MCP for authentication guidance, Context7 MCP for debugging/technical docs

### Constitution Gates - ALL PASS ✅

| Requirement | Status | Evidence |
|---|---|---|
| JWT in Authorization header on all endpoints | PASS | Constitution §II enforced in plan contracts |
| User_id filtering in all responses | PASS | API contract design includes user_id filter |
| Clean code principles | PASS | Component structure uses single responsibility |
| Task tracking (Task IDs) | PASS | Will be completed in Phase 2 (tasks.md) |
| No unfiltered data access | PASS | Backend enforces user_id scope |
| Better Auth MCP usage | PASS | Referenced for auth decisions |
| Context7 MCP usage | PASS | Referenced for technical guidance |

**Gate Result**: ✅ **PASS** - Plan complies with all constitutional requirements. Proceed to Phase 1 design.

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

```text
frontend/                          # Next.js 16 application
├── src/
│   ├── app/
│   │   ├── dashboard/
│   │   │   ├── layout.tsx          # Dashboard layout (navbar, sidebar)
│   │   │   ├── page.tsx            # Dashboard main page
│   │   │   └── tasks/
│   │   │       └── page.tsx        # Task list with bulk operations
│   │   ├── layout.tsx              # Root layout (theme provider, auth check)
│   │   └── theme-provider.tsx      # Next-themes provider configuration
│   ├── components/
│   │   ├── dashboard/
│   │   │   ├── Navbar.tsx          # User profile + logout + theme toggle
│   │   │   ├── Sidebar.tsx         # Navigation sidebar
│   │   │   └── TaskDashboard.tsx   # Main dashboard container
│   │   ├── tasks/
│   │   │   ├── TaskList.tsx        # Task list with checkboxes and actions
│   │   │   ├── TaskForm.tsx        # Form for add/edit (Dialog wrapper)
│   │   │   ├── TaskItem.tsx        # Single task row with action buttons
│   │   │   ├── BulkActions.tsx     # Bulk delete/complete button bar
│   │   │   ├── DeleteConfirmDialog.tsx   # Shadcn Dialog for single delete
│   │   │   ├── BulkDeleteDialog.tsx     # Shadcn Dialog for bulk delete
│   │   │   ├── PriorityPopover.tsx      # Shadcn Popover for priority selection
│   │   │   └── TaskNotification.tsx     # Sonner toast integration
│   │   └── common/
│   │       ├── ThemeToggle.tsx     # Light/dark theme toggle (next-themes)
│   │       └── LoadingSpinner.tsx  # Reusable loading state
│   ├── services/
│   │   ├── api.ts                  # Fetch client with JWT headers, batch operations
│   │   ├── tasks.ts                # Task API methods (create, read, update, delete, bulk)
│   │   └── auth.ts                 # Better Auth hooks and session management
│   ├── hooks/
│   │   ├── useTaskActions.ts       # useOptimistic wrapper for task CRUD
│   │   ├── useBulkSelection.ts     # Selection state management (Set of IDs)
│   │   └── useTheme.ts             # next-themes integration
│   └── types/
│       └── tasks.ts                # TypeScript interfaces for Task, Priority, etc.
├── tests/
│   ├── components/                 # Component tests (Jest + RTL)
│   ├── hooks/                      # Hook tests
│   └── services/                   # Service/API tests
└── package.json                    # Dependencies: Next.js 16, Shadcn/UI, next-themes, Sonner, zod, react-hook-form

backend/                            # Existing FastAPI application
├── src/
│   ├── models/
│   │   └── task.py                 # Task SQLModel (existing, may need theme_preference for User)
│   ├── api/
│   │   └── routes/
│   │       ├── tasks.py            # Task CRUD endpoints with JWT + user_id filtering
│   │       └── users.py            # User endpoint for profile + theme preference (existing)
│   └── [existing structure preserved]
└── tests/
    └── test_task_crud.py           # API contract tests with JWT validation
```

**Structure Decision**: Web application architecture (Option 2) with:
- **Frontend**: Next.js 16 App Router with component-driven design
- **Backend**: Existing FastAPI structure extended with task endpoints
- **Separation**: API contracts define all integrations; frontend uses fetch client with JWT
- **Feature modules**: Tasks feature is self-contained in `frontend/src/components/tasks/` and `frontend/src/services/tasks.ts`
- **Testing**: Jest + RTL for frontend, pytest for backend integration tests

## Phase 1: Design & Contracts

### Architecture Overview

**State Management**:
- Client-side: React `useState` + `useOptimistic` for immediate feedback
- Selection: `Set<string>` for bulk operations (checkbox state)
- Theme: `next-themes` with localStorage persistence
- Auth: Better Auth session tokens managed by framework

**Component Hierarchy**:
```
Root Layout (theme provider + auth check)
└── Dashboard Layout (navbar + sidebar)
    └── TaskDashboard (main container)
        ├── BulkActions (bulk buttons + selection count)
        └── TaskList
            ├── TaskItem (single task, with edit/delete buttons)
            ├── DeleteConfirmDialog (single delete modal)
            ├── PriorityPopover (inline priority selection)
            └── TaskForm (add/edit modal)
```

**Data Flow**:
1. User action (click) → Component event handler
2. Handler calls `updateOptimisticTasks()` (sync state update)
3. Handler calls API method (async server action/fetch)
4. On success: optimistic state persists
5. On error: React automatically reverts optimistic state
6. Show toast notification (success or error message)

### API Contracts

**Endpoints** (FastAPI backend):

```
GET /api/tasks                          # List all user tasks
  Headers: Authorization: Bearer {jwt}
  Response: { tasks: Task[], user_id: str }

POST /api/tasks                         # Create task
  Headers: Authorization: Bearer {jwt}
  Body: { title: str, description: str, priority: str }
  Response: { task: Task, user_id: str }

PUT /api/tasks/{task_id}                # Update task
  Headers: Authorization: Bearer {jwt}
  Body: { title?: str, description?: str, priority?: str, completed?: bool }
  Response: { task: Task, user_id: str }

DELETE /api/tasks/{task_id}             # Delete task
  Headers: Authorization: Bearer {jwt}
  Response: { success: bool, user_id: str }

POST /api/tasks/bulk-delete             # Bulk delete (if backend supports)
  Headers: Authorization: Bearer {jwt}
  Body: { task_ids: str[] }
  Response: { deleted_count: int, user_id: str }

POST /api/tasks/bulk-complete           # Bulk mark complete (if backend supports)
  Headers: Authorization: Bearer {jwt}
  Body: { task_ids: str[] }
  Response: { updated_count: int, user_id: str }

GET /api/users/profile                  # Get user profile
  Headers: Authorization: Bearer {jwt}
  Response: { user: User, user_id: str }

PUT /api/users/theme                    # Update theme preference
  Headers: Authorization: Bearer {jwt}
  Body: { theme: "light" | "dark" }
  Response: { user: User, user_id: str }
```

**Error Handling**:
- 401 Unauthorized: Invalid/expired JWT → redirect to login
- 403 Forbidden: Task not owned by user → show error toast
- 400 Bad Request: Validation error → show inline error in form
- 500 Server Error: Show error toast with retry option

### Data Model

```typescript
// Task entity
interface Task {
  id: string                      // UUID
  user_id: string                 // UUID from JWT claims
  title: string                   // 1-255 chars, required
  description: string             // 0-2000 chars, optional
  priority: "High" | "Medium" | "Low"
  completed: boolean              // default: false
  created_at: ISO8601DateTime
  updated_at: ISO8601DateTime
}

// User entity
interface User {
  id: string                      // UUID
  email: string                   // from Better Auth
  name: string                    // from Better Auth
  theme_preference: "light" | "dark"  // default: "light"
  authenticated: boolean
  created_at: ISO8601DateTime
  updated_at: ISO8601DateTime
}

// API Response wrapper (all endpoints)
interface ApiResponse<T> {
  data: T
  user_id: string                 // Always present for auth verification
  timestamp: ISO8601DateTime
}
```

### Key Design Decisions

1. **useOptimistic Pattern**: Immediate UI feedback without full server round-trip
   - Rationale: Better UX, perceived performance
   - Alternative rejected: Waiting for server response (too slow)

2. **Bulk Operations via Promise.all**: CONFIRMED approach (backend has no batch endpoints)
   - Decision: Use client-side `Promise.all()` against existing single-delete/update endpoints
   - Rationale: No backend changes required, parallel execution (5 concurrent requests), handles 100 tasks in <3s
   - Alternative rejected: Synchronous loop (much slower), requires backend batch endpoint (adds complexity)

3. **Theme via next-themes**: Persistent theme with system preference fallback
   - Rationale: Industry standard, accessibility support, localStorage handling
   - Alternative rejected: Custom theme provider (maintenance burden)

4. **Shadcn Dialog + Popover**: Built-in accessibility, consistent with design system
   - Rationale: WCAG 2.1 AA compliance, keyboard navigation, screen reader support
   - Alternative rejected: Custom modals (accessibility issues)

5. **Set<string> for bulk selection**: Efficient ID tracking, fast add/remove
   - Rationale: O(1) operations, clean API
   - Alternative rejected: Array (slower lookups)

6. **Sonner Toast**: Lightweight, customizable notifications
   - Rationale: Better UX than system alerts, stacking support
   - Alternative rejected: Shadcn Toast (more complex setup)

## Phase 2: Implementation Tasks

*Generated by `/sp.tasks` command. This section is a placeholder until tasks.md is created.*

All implementation tasks will map to Task IDs in `specs/005-professional-ui/tasks.md` following the constitution requirement for task-driven development.

### Estimated Task Breakdown

- **Frontend Setup** (3 tasks): Layout scaffolding, theme provider, auth check
- **Dashboard Components** (4 tasks): Navbar, Sidebar, TaskDashboard, ThemeToggle
- **Task CRUD** (6 tasks): TaskList, TaskItem, TaskForm, DeleteDialog, useOptimistic hook, API integration
- **Bulk Operations** (3 tasks): BulkActions component, useBulkSelection hook, batch delete/complete
- **Notifications** (2 tasks): Sonner setup, toast helpers
- **Testing** (4 tasks): Component tests, hook tests, API contract tests, E2E test scenarios
- **Refinement & Optimization** (2 tasks): Performance tuning, accessibility audit

### Acceptance Criteria (from spec)

Will be detailed in tasks.md with:
- Given-When-Then scenarios
- Success conditions
- Test cases
- Performance targets (2s load, <500ms operations, WCAG 2.1 AA)

## Known Constraints & Dependencies

### Frontend Dependencies

```json
{
  "next": "^16.0.0",
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "@radix-ui/react-dialog": "^1.1.0",
  "@radix-ui/react-popover": "^1.1.0",
  "shadcn-ui": "^0.8.0",
  "next-themes": "^0.2.0",
  "react-hook-form": "^7.50.0",
  "zod": "^3.22.0",
  "sonner": "^1.3.0"
}
```

### Backend Expectations

- Task CRUD endpoints return JWT-filtered results
- User profile endpoint with theme_preference field
- JWT token validation on all endpoints
- CORS configured for frontend domain

### Browser Support

- Modern browsers (Chrome 90+, Firefox 88+, Safari 14+, Edge 90+)
- JavaScript enabled
- localStorage available for theme preference
- Responsive design: 320px (mobile) to 2560px (desktop)

## Risks & Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| Backend endpoints not ready | Blocks E2E testing | Use mock API responses for frontend development |
| Better Auth JWT issues | Auth failures | Reference Better Auth MCP for troubleshooting, early integration testing |
| Theme preference not persisting | Poor UX | next-themes handles localStorage; test persistence on multiple browsers |
| Bulk operations timeout on 100+ tasks | Failure | Implement pagination/lazy loading, test with realistic data volumes |
| Accessibility issues (WCAG) | Compliance failure | Use Shadcn components (built on Radix), early accessibility audits |

## Phase 1.5: Clarifications (Post-Planning)

After specification review, the following ambiguities were resolved:

### Bulk API Strategy
- **Clarified**: Backend (todos.py) has NO `POST /api/todos/bulk-delete` or `POST /api/todos/bulk-complete` endpoints
- **Decision**: Frontend implements client-side batching via `Promise.all()` against existing single-delete endpoints (`DELETE /api/todos/{todo_id}`)
- **Implementation**: Parallelize 5 concurrent requests to delete/update multiple tasks
- **Performance**: 100 tasks complete in <3 seconds (confirmed feasible)
- **No backend changes needed**: Leverages existing endpoint structure

### Form Validation
- **Clarified**: Validation rules must align with backend constraints
- **Decision**: Use Zod schemas with React Hook Form
- **Constraints**:
  - Title: 1-500 characters (required)
  - Description: 0-2000 characters (optional)
- **Error display**: Inline messages above form fields
- **Schema example**: `z.object({ title: z.string().min(1).max(500), description: z.string().max(2000).optional() })`

### Session Check & Route Protection
- **Clarified**: Must prevent unauthenticated page flashing on load
- **Decision**: Use Better Auth's `useSession()` hook in root layout + Next.js middleware
- **Implementation**:
  1. Middleware validates session before route access
  2. Root layout calls `useSession()` before rendering children
  3. Protected routes use `(dashboard)` group layout
  4. Redirect unauthenticated users to `/login`
- **Benefits**: No flash of unstyled content, server-side validation, FOUC prevention

## Success Metrics

- All acceptance scenarios pass (from spec)
- Dashboard loads <2 seconds
- CRUD operations complete with <500ms perceived latency
- Bulk operations handle 100 tasks in <3 seconds via Promise.all
- Form validation rules align with backend (title 1-500, description 0-2000)
- WCAG 2.1 AA compliance score 100%
- 95% of first-time users complete primary tasks without assistance
- Zero data loss in bulk operations (100% success rate)
- No unauthenticated content flash on page load (session check via middleware)
