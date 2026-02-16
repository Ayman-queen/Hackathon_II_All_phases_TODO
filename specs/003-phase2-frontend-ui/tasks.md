---
description: "Implementation tasks for Phase II Frontend UI - Next.js, Better Auth, Shadcn/UI, and Todo Management"
---

# Tasks: Phase II Frontend UI

**Feature**: Phase II Frontend UI (Branch: `003-phase2-frontend-ui`)
**Input**: Design documents from `/specs/003-phase2-frontend-ui/` (spec.md, plan.md)
**Tests**: OPTIONAL - Include component/E2E tests only if explicitly requested

**Organization**: Tasks are grouped by phase and user story to enable independent implementation and testing.

---

## Format: `- [ ] [ID] [P?] [Story?] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., [US1], [US2], [US3])
  - Setup & Foundational phases: NO story label
  - User story phases: REQUIRED story label
- Include exact file paths in descriptions

---

## Phase 0: Pre-Implementation Validation (API Contract & Architecture)

**Purpose**: Verify backend API contract and frontend architecture decisions before implementation

**Critical**: These validation tasks must pass before proceeding to Phase 1

- [x] T-230 [P] Verify backend todo API contract - confirm endpoints are `/api/todos` with `/{todo_id}` routes (NOT `/api/{user_id}/tasks` pattern)
  - Inspect `/backend/app/api/todos.py` to confirm endpoint paths
  - Document the exact API contract URL patterns
  - Create `frontend/docs/API_CONTRACT.md` with endpoint specifications
  - Reference: Better Auth JWT tokens solution requires frontend to use `user_id` from JWT claims, backend ensures ownership via JWT validation in `get_current_user` dependency

- [x] T-231 [P] Verify JWT token extraction from Better Auth - confirm frontend can decode `user_id` from JWT token
  - Test Better Auth client can access JWT payload without verification
  - Confirm token structure includes `user_id` or `sub` claim for user identification
  - Document JWT claim structure in `frontend/docs/JWT_STRUCTURE.md`

- [x] T-232 [P] Confirm API client bearer token injection - verify all API requests will include `Authorization: Bearer <token>` header
  - Review plan.md architecture for `api-client.ts` centralized JWT attachment pattern
  - Confirm this matches backend expectation in FastAPI dependency injection
  - Document the JWT attachment pattern in `frontend/docs/JWT_ATTACHMENT.md`

- [x] T-233 [P] Validate Shadcn/UI compatibility with Next.js 16+ and Tailwind CSS in existing setup
  - Check `frontend/package.json` for current Shadcn/UI version
  - Verify Tailwind CSS configuration in `frontend/tailwind.config.ts`
  - Document any version constraints in `frontend/docs/DEPENDENCIES.md`

- [x] T-234 Confirm no manual code writing approach - review available CLI tools and code generation methods
  - Shadcn/UI CLI for component generation
  - Next.js scaffolding for routes and layouts
  - TypeScript interfaces via generation vs. manual creation
  - Document code generation strategy in `frontend/docs/CODE_GENERATION_STRATEGY.md`

**Checkpoint**: API contract verified, JWT strategy confirmed, code generation approach documented. Ready to proceed to Phase 1.

---

## Phase 1: Setup (Project Initialization & Dependencies)

**Purpose**: Frontend project structure and core dependencies

**Depends on**: Phase 0 validation completion

- [x] T-235 [P] Install and configure Shadcn/UI via CLI in frontend/ with default component library
  - Run: `cd frontend && npx shadcn-ui@latest init`
  - Configure for Next.js App Router (default)
  - Select TypeScript (yes), Tailwind CSS (yes), CSS variables (yes)
  - Update `frontend/package.json` and `frontend/components.json` after CLI execution

- [x] T-236 [P] Initialize next-themes provider in frontend/app/layout.tsx for dark/light mode support
  - Install next-themes: `npm install next-themes`
  - Add ThemeProvider to root layout
  - Configure `attribute="class"`, `defaultTheme="system"`, `enableSystem={true}`
  - Reference Task T-236 in layout.tsx comments

- [x] T-237 [P] Configure Better Auth JavaScript client in frontend/lib/auth-client.ts with JWT plugin
  - Import `createAuthClient` from `better-auth/react`
  - Import `jwtClient` plugin from `better-auth/client/plugins`
  - Initialize client with jwtClient() plugin enabled
  - Export `useSession()` hook and `getToken()` function
  - Reference Task T-237 and Context 7 JWT documentation in comments

- [x] T-238 [P] Create centralized API fetch wrapper in frontend/lib/api-client.ts with automatic JWT bearer token injection
  - Implement `apiRequest<T>()` function that:
    - Retrieves JWT token from Better Auth via `authClient.token()`
    - Attaches to all requests as `Authorization: Bearer <token>` header
    - Handles 401 responses (token expired) by redirecting to /login
    - Implements retry logic for network failures
  - Export convenience methods: `api.getTodos()`, `api.createTodo()`, `api.updateTodo()`, `api.deleteTodo()`
  - Reference Task T-238, plan.md API layer design, and Context 7 JWT patterns in comments

- [x] T-239 [P] Setup TypeScript interfaces for auth and todo entities in frontend/lib/types/
  - Create `frontend/lib/types/auth.ts` with User, Session, AuthError types
  - Create `frontend/lib/types/todo.ts` with Todo, TodoStatus, Priority types matching backend schema
  - Create `frontend/lib/types/api.ts` with ApiResponse, ErrorResponse types
  - Use Zod schemas where appropriate for runtime validation
  - Reference Task T-239 and plan.md data model in comments

- [x] T-240 [P] Configure environment variables in frontend/.env.example
  - Add NEXT_PUBLIC_API_URL (points to backend FastAPI)
  - Add NEXT_PUBLIC_AUTH_URL (points to Better Auth instance)
  - Add comments explaining each variable
  - Create `frontend/.env.local` with actual values for local development
  - Reference Task T-240 in comments

- [x] T-241 Create root layout component in frontend/app/layout.tsx with Providers (Better Auth, next-themes)
  - Wrap app with ThemeProvider from next-themes
  - Add metadata (title, description)
  - Import and apply globals.css
  - Reference Task T-241 in comments

- [x] T-242 Configure Next.js App Router structure per plan.md (create route groups, protected routes directories)
  - Create `frontend/app/(auth)/` directory for login/signup routes
  - Create `frontend/app/(protected)/` directory for authenticated routes
  - Create `frontend/app/(protected)/todo/` for todo management
  - Reference Task T-242 and plan.md project structure in comments

- [x] T-243 Setup Tailwind CSS custom theme in frontend/tailwind.config.ts with light/dark mode CSS variables
  - Configure dark mode strategy: class-based (for next-themes compatibility)
  - Define CSS variables for colors in light/dark modes
  - Set up Shadcn/UI color overrides
  - Reference Task T-243 and plan.md theming architecture in comments

**Checkpoint**: Frontend project structure ready, dependencies installed via CLI, core utilities initialized. All code generated via tools (Shadcn CLI, Next.js), no manual code writing.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core components and hooks that MUST be complete before any user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**Depends on**: Phase 1 completion (T-235–T-243)

- [x] T-244 [P] Create custom useAuth hook in frontend/lib/hooks/useAuth.ts for authentication state management
  - Integrate with Better Auth client (T-237)
  - Manage session state, JWT token, sign-out functionality
  - Reference Task T-244 and plan.md hooks architecture in comments

- [x] T-245 [P] Create custom useTodos hook in frontend/lib/hooks/useTodos.ts for todo CRUD operations
  - Implement CRUD methods: getTodos, createTodo, updateTodo, deleteTodo
  - Integrate with api-client.ts (T-238) for JWT-authenticated requests
  - Reference Task T-245 and plan.md state management in comments

- [x] T-246 [P] Create custom useTheme hook in frontend/lib/hooks/useTheme.ts for theme persistence
  - Integrate with next-themes ThemeProvider (T-236)
  - Persist theme preference to localStorage
  - Reference Task T-246 in comments

- [ ] T-247 [P] Create ErrorAlert component in frontend/components/common/ErrorAlert.tsx via Shadcn CLI
  - Generate using: `npx shadcn@latest add alert`
  - Wrap for error display use case
  - Reference Task T-247 in comments

- [ ] T-248 [P] Create LoadingSpinner component in frontend/components/common/LoadingSpinner.tsx via Shadcn
  - Generate Shadcn skeleton or spinner variant
  - Create reusable loading indicator
  - Reference Task T-248 in comments

- [ ] T-249 [P] Create EmptyState component in frontend/components/common/EmptyState.tsx via Shadcn
  - Create reusable component for empty lists/states
  - Reference Task T-249 in comments

- [ ] T-250 Create protected routes layout in frontend/app/(protected)/layout.tsx with auth guard
  - Check authentication before rendering children
  - Redirect unauthenticated users to /login
  - Reference Task T-250 and plan.md protected routes in comments

- [ ] T-251 Create auth routes layout in frontend/app/(auth)/layout.tsx
  - Styling and layout for login/signup pages
  - Reference Task T-251 in comments

- [x] T-252 Setup error handling and logging in frontend/lib/api-client.ts (handle 401, 403, 500 responses)
  - HTTP error status code handling
  - User-friendly error messages
  - Reference Task T-252 and plan.md error handling in comments

- [x] T-253 Create Navigation component in frontend/components/layout/Navigation.tsx with user menu (profile, logout)
  - Display current user email
  - Profile and logout options
  - Reference Task T-253 in comments

- [ ] T-254 Create ThemeToggle button component in frontend/components/layout/ThemeToggle.tsx (light/dark)
  - Use next-themes useTheme() hook
  - Toggle between light and dark modes
  - Reference Task T-254 in comments

**Checkpoint**: Foundation ready - authentication, API client, hooks, and common components complete. User story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - New User Registration (Priority: P1) 🎯 MVP

**Goal**: Users can create new accounts via Better Auth with email/password validation and JWT token issuance

**Independent Test**: Visit /signup, enter valid email/password, verify account creation and JWT token storage in browser

### Implementation for User Story 1

- [ ] T-245 [P] [US1] Create SignupForm component in frontend/components/auth/SignupForm.tsx with form validation (Shadcn Form)
- [ ] T-246 [P] [US1] Create signup page in frontend/app/(auth)/signup/page.tsx
- [ ] T-247 [US1] Implement signup logic using Better Auth client in useAuth hook - handle email/password registration
- [ ] T-248 [US1] Add email validation (format check) in SignupForm component
- [ ] T-249 [US1] Add password validation feedback (length, complexity requirements) in SignupForm component
- [ ] T-250 [US1] Handle duplicate email error - display "Email already exists" message
- [ ] T-251 [US1] Redirect user to /todos dashboard after successful signup
- [ ] T-252 [US1] Verify JWT token stored in browser (via Better Auth) and available for API calls

**Acceptance Criteria**:
1. ✅ Valid email/password → account created, redirected to /todos with JWT available
2. ✅ Invalid email format → error message, account not created
3. ✅ Weak password → validation feedback, account not created
4. ✅ Existing email → "Email already exists" error

**Checkpoint**: User Story 1 fully functional - signup works end-to-end with JWT issuance

---

## Phase 4: User Story 2 - User Login & JWT Token Management (Priority: P1)

**Goal**: Users can log in with email/password and receive JWT tokens that are automatically included in all subsequent API requests

**Independent Test**: Log in with valid credentials, verify /todos page loads and API calls include JWT header

### Implementation for User Story 2

- [ ] T-253 [P] [US2] Create LoginForm component in frontend/components/auth/LoginForm.tsx (Shadcn Form)
- [ ] T-254 [P] [US2] Create login page in frontend/app/(auth)/login/page.tsx
- [ ] T-255 [US2] Implement login logic in useAuth hook using Better Auth client
- [ ] T-256 [US2] Add password validation and error handling in LoginForm (email required, password required)
- [ ] T-257 [US2] Display "Invalid credentials" error on failed login attempt
- [ ] T-258 [US2] Redirect to /todos after successful login
- [ ] T-259 [US2] Verify JWT token automatically included in Authorization: Bearer <token> header for all API calls
- [ ] T-260 [US2] Implement JWT expiration handling - check token validity before API calls
- [ ] T-261 [US2] Implement auto-logout on 401 Unauthorized response (token expired)
- [ ] T-262 [US2] Redirect to /login when JWT expires or is invalid

**Acceptance Criteria**:
1. ✅ Valid credentials → authenticated, redirected to /todos
2. ✅ Invalid credentials → error message, remain on login page
3. ✅ All API requests include JWT in Authorization header
4. ✅ JWT expiration → prompt to re-login, redirect to /login page

**Checkpoint**: User Stories 1 & 2 complete - full auth flow working (signup, login, JWT token management)

---

## Phase 5: User Story 8 - Create & Edit Todo (Priority: P1)

**Goal**: Users can create new todos and edit existing ones with title, description, priority, and optional due date

**Independent Test**: Create new todo with title, verify it appears in list; edit title, verify update persists

### Implementation for User Story 8

- [ ] T-263 [P] [US8] Create TodoForm component in frontend/components/todos/TodoForm.tsx (create/edit mode) (Shadcn Form)
- [ ] T-264 [P] [US8] Create create todo page in frontend/app/(protected)/todos/new/page.tsx
- [ ] T-265 [P] [US8] Create edit todo page in frontend/app/(protected)/todos/[id]/page.tsx
- [ ] T-266 [US8] Implement useTodos hook logic for POST /api/todos (create with title, description) - backend auto-assigns user_id from JWT
- [ ] T-267 [US8] Implement useTodos hook logic for PUT /api/todos/{id} (update title/description fields)
- [ ] T-268 [US8] Add form validation in TodoForm (title required, priority dropdown with High/Medium/Low)
- [ ] T-269 [US8] Add optional due date picker in TodoForm (Shadcn DatePicker)
- [ ] T-270 [US8] Handle API errors (network failure, validation errors) - display ErrorAlert component
- [ ] T-271 [US8] Redirect to /todos after successful create or edit
- [ ] T-272 [US8] Pre-populate TodoForm with existing todo data when editing

**Acceptance Criteria**:
1. ✅ Title + priority → todo created, appears in list
2. ✅ Empty title → validation error shown
3. ✅ Edit todo → form pre-populated, changes persist after save
4. ✅ API errors → ErrorAlert displayed with retry option

**Checkpoint**: User Stories 1, 2, & 8 complete - full CRUD create/edit working for todos

---

## Phase 6: User Story 3 - Todo List Display with Filtering (Priority: P1)

**Goal**: Users view their todo list filtered by status (All, Pending, Completed) with clean, organized display

**Independent Test**: Log in, view /todos page, use filter buttons, verify task list updates by status

### Implementation for User Story 3

- [ ] T-273 [P] [US3] Create TodoCard component in frontend/components/todos/TodoCard.tsx (displays single todo with priority badge) (Shadcn Card)
- [ ] T-274 [P] [US3] Create FilterTabs component in frontend/components/todos/FilterTabs.tsx (All/Pending/Completed buttons) (Shadcn Tabs)
- [ ] T-275 [US3] Create todos list page in frontend/app/(protected)/todos/page.tsx
- [ ] T-276 [US3] Implement GET /api/todos with filter param in useTodos hook (filter=all|pending|completed)
- [ ] T-277 [US3] Implement client-side filtering in useTodos hook or component state
- [ ] T-278 [US3] Display all todos in TodoList component with TodoCard for each
- [ ] T-279 [US3] Implement "Pending" filter (status === "pending")
- [ ] T-280 [US3] Implement "Completed" filter (status === "completed")
- [ ] T-281 [US3] Display EmptyState when no todos exist - "No todos yet. Create your first todo!"
- [ ] T-282 [US3] Display LoadingSpinner while fetching todos from API
- [ ] T-283 [US3] Handle API errors - display ErrorAlert with retry button

**Acceptance Criteria**:
1. ✅ Logged-in user with todos → all todos displayed
2. ✅ "Pending" filter → only incomplete todos shown
3. ✅ "Completed" filter → only completed todos shown
4. ✅ No todos → EmptyState message with create CTA
5. ✅ "All" filter → all todos regardless of status shown

**Checkpoint**: User Stories 1, 2, 3, & 8 complete - Auth + Todo CRUD + Filtering working (MVP scope complete!)

---

## Phase 7: User Story 9 - Delete Todo & User Isolation (Priority: P1)

**Goal**: Users can delete their own todos with confirmation; strict user isolation enforced (users only see their own todos)

**Independent Test**: Create two accounts, verify User A cannot see User B's todos; User A can delete their todo

### Implementation for User Story 9

- [ ] T-284 [P] [US9] Add delete button to TodoCard component in frontend/components/todos/TodoCard.tsx
- [ ] T-285 [P] [US9] Create DeleteConfirmDialog component in frontend/components/todos/DeleteConfirmDialog.tsx (Shadcn Dialog)
- [ ] T-286 [US9] Implement DELETE /api/todos/{id} in useTodos hook
- [ ] T-287 [US9] Show confirmation dialog before deletion in TodoCard
- [ ] T-288 [US9] Remove todo from list after successful deletion (update state)
- [ ] T-289 [US9] Handle deletion errors - display ErrorAlert with retry
- [ ] T-290 [US9] Verify user isolation - useTodos hook filters todos by current user's JWT (backend enforces, frontend respects)
- [ ] T-291 [US9] Test that User B cannot access User A's todo ID via direct API call (backend returns 401/403)

**Acceptance Criteria**:
1. ✅ User can delete their own todo with confirmation
2. ✅ Todo removed from list after deletion
3. ✅ User A cannot see User B's todos
4. ✅ User A cannot delete User B's todo via API

**Checkpoint**: User Stories 1, 2, 3, 8, & 9 complete - Full P1 scope (MVP) working with security isolation

---

## Phase 8: User Story 4 - Todo Sorting (Priority: P2)

**Goal**: Users can sort todos by Priority, Due Date, or Title to manage workload effectively

**Independent Test**: Load todo list, use sort menu, verify list reorders by selected criteria

### Implementation for User Story 4

- [ ] T-292 [P] [US4] Create SortDropdown component in frontend/components/todos/SortDropdown.tsx (Priority/DueDate/Title options) (Shadcn Select)
- [ ] T-293 [US4] Add SortDropdown to todos list page in frontend/app/(protected)/todos/page.tsx
- [ ] T-294 [US4] Implement client-side sorting in useTodos hook (sort=[priority|dueDate|title])
- [ ] T-295 [US4] Implement "Sort by Priority" - High → Medium → Low
- [ ] T-296 [US4] Implement "Sort by Due Date" - earliest first
- [ ] T-297 [US4] Implement "Sort by Title" - alphabetical (A-Z)
- [ ] T-298 [US4] Persist sort selection in component state (reset on page reload is acceptable)
- [ ] T-299 [US4] Display current sort selection in UI

**Acceptance Criteria**:
1. ✅ "Sort by Priority" → High → Medium → Low order
2. ✅ "Sort by Due Date" → soonest first
3. ✅ "Sort by Title" → alphabetical order
4. ✅ Sort persists until user selects different option

**Checkpoint**: User Stories 1-4, 8-9 complete - Filtering + Sorting working for todo management

---

## Phase 9: User Story 5 - Priority Tagging (Priority: P2)

**Goal**: Users assign priority levels (High/Medium/Low) to todos with visually distinct indicators

**Independent Test**: Create todo with priority, view it in list with visible priority badge; edit priority, verify update

### Implementation for User Story 5

- [ ] T-300 [P] [US5] Create PriorityBadge component in frontend/components/todos/PriorityBadge.tsx (color-coded High/Medium/Low) (Shadcn Badge)
- [ ] T-301 [US5] Update TodoCard to display PriorityBadge for each todo
- [ ] T-302 [US5] Add priority field to TodoForm component (dropdown: High/Medium/Low)
- [ ] T-303 [US5] Set default priority to "Medium" when creating new todo (T-266 updates)
- [ ] T-304 [US5] Implement priority colors - High=red, Medium=yellow, Low=green (Tailwind classes)
- [ ] T-305 [US5] Allow editing priority in TodoForm (T-267 updates)
- [ ] T-306 [US5] Update useTodos hook POST/PATCH to include priority field

**Acceptance Criteria**:
1. ✅ Create todo with priority → priority displays with visual indicator
2. ✅ Edit todo → can change priority, update reflects immediately
3. ✅ Priority badges visually distinct (High=red, Medium=yellow, Low=green)
4. ✅ Default priority "Medium" assigned if not explicitly set

**Checkpoint**: User Stories 1-5, 8-9 complete - Priority management + visual tagging working

---

## Phase 10: User Story 6 - Dark Mode & Light Mode Toggle (Priority: P2)

**Goal**: Users toggle between light and dark themes with persistent preference across sessions

**Independent Test**: Click theme toggle, verify UI switches theme; refresh page, verify theme persists

### Implementation for User Story 6

- [ ] T-307 [P] [US6] Implement ThemeToggle button in frontend/components/layout/ThemeToggle.tsx using next-themes
- [ ] T-308 [P] [US6] Add ThemeToggle to Navigation component in frontend/components/layout/Navigation.tsx
- [ ] T-309 [US6] Configure dark mode class in frontend/tailwind.config.ts (class strategy)
- [ ] T-310 [US6] Define CSS variables in frontend/styles/globals.css for light/dark mode colors
- [ ] T-311 [US6] Implement useTheme hook (T-236) to persist theme in localStorage
- [ ] T-312 [US6] Ensure theme persists across page reloads and browser restarts
- [ ] T-313 [US6] Respect OS-level theme preference on first visit (prefers-color-scheme)
- [ ] T-314 [US6] Apply theme consistently to all pages (Shadcn components inherit theme automatically)

**Acceptance Criteria**:
1. ✅ Light mode → Dark mode toggle switches UI instantly
2. ✅ Dark mode preference persists after refresh
3. ✅ New user on first visit → respects OS theme preference
4. ✅ Theme applies consistently across all pages/components

**Checkpoint**: User Stories 1-6, 8-9 complete - Full theme switching with persistence working

---

## Phase 11: User Story 7 - User Profile & Logout (Priority: P2)

**Goal**: Users view profile information (email) and securely log out with JWT cleared

**Independent Test**: Click profile menu → view email; click logout → redirected to login, cannot access /todos

### Implementation for User Story 7

- [ ] T-315 [P] [US7] Create ProfilePage component in frontend/app/(protected)/profile/page.tsx
- [ ] T-316 [P] [US7] Create LogoutButton component in frontend/components/auth/LogoutButton.tsx
- [ ] T-317 [US7] Add profile menu to Navigation component (user email → Profile/Logout options)
- [ ] T-318 [US7] Display user email on Profile page fetched from useAuth hook
- [ ] T-319 [US7] Implement logout in useAuth hook - clear JWT token via Better Auth client
- [ ] T-320 [US7] Redirect to /login after logout
- [ ] T-321 [US7] Clear all auth state in useAuth hook on logout
- [ ] T-322 [US7] Prevent access to protected routes after logout - redirect to /login if attempting direct access
- [ ] T-323 [US7] Clear cookies/sessionStorage holding JWT token

**Acceptance Criteria**:
1. ✅ Logged-in user → profile menu shows email
2. ✅ Click logout → redirected to /login
3. ✅ After logout → cannot access /todos (redirected to /login)
4. ✅ Browser history back button → still cannot access protected pages without re-login

**Checkpoint**: All user stories 1-7, 8-9 complete - Full frontend feature set working!

---

## Phase 12: Polish & Cross-Cutting Concerns

**Purpose**: Improvements affecting multiple user stories

- [ ] T-324 [P] Add loading states (skeleton screens) for todo list in frontend/app/(protected)/todos/page.tsx
- [ ] T-325 [P] Add error boundary component in frontend/components/common/ErrorBoundary.tsx for graceful error handling
- [ ] T-326 [P] Add form submission loading states (disabled buttons) in SignupForm, LoginForm, TodoForm
- [ ] T-327 [P] Implement keyboard navigation (Tab, Enter) for all forms and interactive elements
- [ ] T-328 [P] Add ARIA labels and semantic HTML for accessibility (WCAG 2.1 Level A compliance)
- [ ] T-329 [P] Test responsive design on mobile (320px), tablet, desktop viewports
- [ ] T-330 Implement E2E tests with Playwright in frontend/tests/e2e/auth.spec.ts (signup, login, logout)
- [ ] T-331 Implement E2E tests with Playwright in frontend/tests/e2e/todos.spec.ts (create, filter, sort, delete)
- [ ] T-332 Add component tests with Jest + RTL for TodoCard, FilterTabs, SortDropdown
- [ ] T-333 Run Lighthouse audit - verify performance >90, accessibility >90
- [ ] T-334 Add documentation in frontend/README.md (setup, architecture, component guide)
- [ ] T-335 Validate quickstart.md (install deps, run locally, test signup → create todo flow)
- [ ] T-336 [P] Code cleanup - remove console.log, unused imports, dead code
- [ ] T-337 Validate all TypeScript types compile without errors
- [ ] T-338 Security audit - verify no sensitive data in logs, no XSS vulnerabilities
- [ ] T-339 Performance optimization - lazy load components, image optimization, bundle size check

**Checkpoint**: Complete polish phase - frontend production-ready!

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - can start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 completion - **BLOCKS all user story work**
- **User Story Phases (3+)**: All depend on Phase 2 completion
  - P1 user stories (US1, US2, US8, US9) should complete before P2 stories for MVP validation
  - P2 user stories (US3, US4, US5, US6, US7) can be done after P1 stories
- **Phase 12 (Polish)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (Signup - P1)**: Depends on Phase 2 - No dependencies on other stories
- **US2 (Login - P1)**: Depends on Phase 2, can benefit from US1 completion (shared auth logic)
- **US8 (Create/Edit Todo - P1)**: Depends on Phase 2, can work in parallel with auth stories
- **US9 (Delete & Isolation - P1)**: Depends on US8 (needs todo list to exist)
- **US3 (Filter - P1)**: Depends on US8 (needs todos to filter)
- **US4 (Sort - P2)**: Depends on US3 (builds on filtered list)
- **US5 (Priority - P2)**: Can be independent or enhance US4/US8
- **US6 (Dark Mode - P2)**: Completely independent of other stories
- **US7 (Profile & Logout - P2)**: Depends on US1/US2 (needs auth to logout)

### Suggested Implementation Order (MVP First)

**MVP Scope (P1 Only)** - Recommended for first release:

1. Complete Phase 1: Setup (T-225 through T-233)
2. Complete Phase 2: Foundational (T-234 through T-244)
3. Complete Phase 3: US1 Signup (T-245 through T-252)
4. Complete Phase 4: US2 Login (T-253 through T-262)
5. Complete Phase 5: US8 Create/Edit Todo (T-263 through T-272)
6. Complete Phase 6: US3 Filter Todo List (T-273 through T-283)
7. Complete Phase 7: US9 Delete & Isolation (T-284 through T-291)
8. **STOP and VALIDATE**: MVP complete - Auth + Todo CRUD + Filtering working
9. Optional: Phase 12 Polish (T-324 through T-339) for production release

**Full Feature Scope** (P1 + P2) - After MVP validation:

10. Complete Phase 8: US4 Sorting (T-292 through T-299)
11. Complete Phase 9: US5 Priority Tagging (T-300 through T-306)
12. Complete Phase 10: US6 Dark Mode (T-307 through T-314)
13. Complete Phase 11: US7 Profile & Logout (T-315 through T-323)
14. Complete Phase 12: Polish (T-324 through T-339)

### Parallel Opportunities

- **Phase 1 & 2**: Setup and Foundational phases can be split across team (T-225-T-233 in parallel, then T-234-T-244 in parallel within Phase 2)
- **Once Phase 2 completes**: All user stories can theoretically start in parallel
  - Team member 1: US1 + US2 (auth flow)
  - Team member 2: US8 + US9 (todo CRUD + deletion)
  - Team member 3: US3 + US4 (filtering + sorting)
  - Team member 4: US5 + US6 + US7 (priority, theme, profile)
- **Within each user story**: Marked [P] tasks can run in parallel (different files/components)
  - Example: T-245 (SignupForm) and T-246 (signup page) can run in parallel

### Example Parallel Execution

**After Phase 2 completion with 2 developers**:

```
Developer A: US1 + US2 (Auth)
  T-245: SignupForm component
  T-246: signup page
  T-247: signup logic
  ...
  T-253: LoginForm component
  T-254: login page
  ...

Developer B: US8 + US9 (Todo CRUD)
  T-263: TodoForm component
  T-264: create page
  ...
  T-284: Delete button
  T-285: DeleteConfirmDialog
  ...

Once A finishes US1, can help B
Once B finishes US8, can start US3
```

---

## Implementation Strategy

### MVP First (Minimum Viable Product - P1 Stories Only)

1. **Setup + Foundation** (1-2 days)
   - Complete Phase 1 & 2
   - Core hooks, API client, common components ready

2. **Auth + CRUD** (3-5 days)
   - Complete US1, US2, US8, US9
   - Users can signup, login, create/delete todos
   - MVP ready for testing

3. **Validate & Deploy** (1 day)
   - Comprehensive testing of MVP scope
   - Performance optimization
   - Bug fixes
   - Deploy to staging/production

4. **Get Feedback** (ongoing)
   - Users test auth + todo management
   - Identify bugs/improvements

**Total MVP Time**: ~1-2 weeks with 1-2 developers

### Incremental Delivery

After MVP validation:

5. **Add US3 (Filtering)** - 1-2 days
6. **Add US4 (Sorting)** - 1 day
7. **Add US5 (Priority)** - 1 day
8. **Add US6 (Dark Mode)** - 1 day
9. **Add US7 (Profile/Logout)** - 1 day
10. **Polish** - 2-3 days

**Total Full Feature Time**: ~2-3 weeks after MVP

### Parallel Team Strategy (Recommended)

With 3-4 developers:

1. Team pair: Complete Phase 1 & 2 together (~2 days)
2. Once Phase 2 done:
   - Dev 1: US1 + US2 (Auth)
   - Dev 2: US8 + US9 (CRUD + Delete)
   - Dev 3: US3 + US4 (Filter + Sort)
   - Dev 4: US5 + US6 + US7 (Priority + Theme + Profile)
3. Stories complete in parallel, integrate together
4. Team pair: Phase 12 Polish

**Total Time with 3 devs**: ~1.5 weeks for MVP, ~2 weeks for full scope

---

## Checkpoints & Validation Gates

After each phase completion, validate:

✅ **After Phase 1**: Dependencies installed, core files created, no errors
✅ **After Phase 2**: Hooks working, API wrapper functioning, auth flows ready for implementation
✅ **After Phase 3 (US1)**: Signup works end-to-end, JWT issued and stored
✅ **After Phase 4 (US2)**: Login works, JWT included in API calls, expiration handling
✅ **After Phase 5 (US8)**: Create and edit todos working, changes persist
✅ **After Phase 6 (US3)**: Filtering by status working, empty states display correctly
✅ **After Phase 7 (US9)**: Deletion working with confirmation, user isolation verified
✅ **After Phase 8 (US4)**: Sorting by priority/date/title working correctly
✅ **After Phase 9 (US5)**: Priority tags display with correct colors and styling
✅ **After Phase 10 (US6)**: Dark mode toggle works, preference persists
✅ **After Phase 11 (US7)**: Profile displays email, logout works, protected routes enforced
✅ **After Phase 12**: Code clean, tests passing, accessibility audit passed, ready for production

---

## Notes

- **[P] marker**: Tasks marked [P] are parallelizable (no file conflicts, no dependencies within phase)
- **[Story] label**: Maps task to specific user story for traceability and independent testing
- **Each user story**: Should be independently completable and testable at a checkpoint
- **Tests**: Optional - only included if explicitly requested in feature spec. This tasks.md focuses on implementation.
- **Commits**: Commit after each task or logical group, reference task ID in commit message (e.g., "T-245: Create signup form")
- **Branching**: Use `phase2-004-ui-auth` branch for all feature work, create sub-branches if needed (phase2-004-signup, phase2-004-login, etc.)
- **PR strategy**: One PR per user story or logical component group after checkpoint validation
