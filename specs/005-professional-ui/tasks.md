# Tasks: Professional UI & Advanced CRUD

**Feature**: 005-professional-ui
**Branch**: `005-professional-ui`
**Created**: 2026-01-02
**Input**: Design documents from `specs/005-professional-ui/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

---

## Implementation Strategy

This feature is organized into **5 independently testable user stories** plus foundational and polish phases:

- **Phase 1: Setup** - Project initialization and dependencies
- **Phase 2: Foundational** - Auth, theme provider, API client setup
- **Phase 3: User Story 1** - Professional dashboard with theme (P1) 🎯 MVP
- **Phase 4: User Story 2** - Task CRUD operations (P1)
- **Phase 5: User Story 3** - Bulk operations (P2)
- **Phase 6: User Story 4** - Interactive feedback/notifications (P1)
- **Phase 7: User Story 5** - Navbar & logout (P1)
- **Phase 8: Polish** - Accessibility, performance, refinement

**MVP Scope**: Complete Phase 3 (US1 - Professional Dashboard) for a functioning UI foundation.

**Parallel Execution**: Multiple user stories can be implemented in parallel after Phase 2 (all are independent).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency setup

- [ ] T001 Create frontend project structure per plan.md in `frontend/src/app`, `frontend/src/components`, `frontend/src/services`, `frontend/src/hooks`, `frontend/src/types`
- [x] T002 Install dependencies: Next.js 16, React 19, TypeScript 5.x in `frontend/package.json` <!-- NOTE: React is v18, not v19 as planned. Deferring upgrade to avoid breaking changes. -->
- [x] T003 [P] Install Shadcn/UI, next-themes, react-hook-form, Zod, Sonner in `frontend/package.json`
- [x] T004 [P] Install testing dependencies: Jest, React Testing Library, @testing-library/user-event in `frontend/package.json`
- [x] T005 [P] Configure TypeScript strict mode and path aliases in `frontend/tsconfig.json` <!-- NOTE: Strict mode is enabled. Path alias '@/*' points to './*' to match existing structure, not './src/*'. -->
- [x] T006 [P] Setup ESLint and Prettier configuration in `frontend/.eslintrc.json`, `frontend/.prettierrc` <!-- NOTE: Files exist and are configured. -->
- [x] T007 Initialize Next.js App Router structure with `frontend/src/app/layout.tsx` and `frontend/src/app/page.tsx` <!-- NOTE: Files exist at `frontend/app/`, not `frontend/src/app/`. Adapting to existing structure. -->

**Checkpoint**: All dependencies installed, project structure ready, TypeScript configured. Proceed to Phase 2.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Setup Better Auth session middleware in `frontend/src/middleware.ts` to check authentication before route access
- [ ] T009 Create root layout with `useSession()` hook + theme provider in `frontend/src/app/layout.tsx` to prevent unauthenticated content flash
- [ ] T010 [P] Configure next-themes in root layout: `frontend/src/app/theme-provider.tsx` with light/dark modes, localStorage persistence
- [ ] T011 Create API fetch client with JWT headers in `frontend/src/services/api.ts` - all requests include Authorization header with bearer token
- [ ] T012 [P] Create auth service module in `frontend/src/services/auth.ts` with Better Auth hooks (useSession, useLogout)
- [ ] T013 Create task API service in `frontend/src/services/tasks.ts` with methods: listTasks, createTask, updateTask, deleteTask, bulkDeleteTasks, bulkCompleteTasks
- [ ] T014 [P] Create TypeScript types/interfaces in `frontend/src/types/tasks.ts` for Task, TaskInput, OptimisticTask, priority enum
- [ ] T015 Setup Sonner toast provider in root layout `frontend/src/app/layout.tsx` for notifications
- [ ] T016 [P] Create reusable useOptimistic hook in `frontend/src/hooks/useTaskActions.ts` for task CRUD with immediate feedback
- [ ] T017 Create bulk selection hook in `frontend/src/hooks/useBulkSelection.ts` using Set<string> for efficient ID tracking
- [ ] T018 [P] Create environment configuration in `frontend/.env.local` with API base URL for backend
- [ ] T019 Setup jest.config.js and @testing-library configuration in `frontend/jest.config.js`

**Checkpoint**: Authentication, theme provider, API client, hooks, and services all functional. User story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - View Professional Dashboard with Theme Support (Priority: P1) 🎯 MVP

**Goal**: Users can see a responsive, professional dashboard with persistent light/dark theme toggle.

**Independent Test**: Login → Dashboard displays with sidebar & navbar → Toggle theme (light ↔ dark) persists on refresh

### Implementation for User Story 1

- [ ] T020 [P] Create responsive dashboard layout component in `frontend/src/components/dashboard/DashboardLayout.tsx` with navbar, sidebar, and main content area
- [ ] T021 Create Navbar component in `frontend/src/components/dashboard/Navbar.tsx` showing:
  - [ ] User profile info (name/email from Better Auth session)
  - [ ] Theme toggle button that calls `useTheme().setTheme()`
  - [ ] Logout button that calls logout from auth service and redirects to `/login`
- [ ] T022 [P] Create Sidebar component in `frontend/src/components/dashboard/Sidebar.tsx` with responsive hamburger menu on mobile (<640px)
- [ ] T023 Create ThemeToggle reusable component in `frontend/src/components/common/ThemeToggle.tsx` with sun/moon icons
- [ ] T024 [P] Create responsive CSS/Tailwind for mobile (< 640px), tablet (640-1024px), and desktop (> 1024px) layouts in component files
- [ ] T025 Create main dashboard page in `frontend/src/app/dashboard/page.tsx` that renders DashboardLayout
- [ ] T026 Create dashboard layout wrapper in `frontend/src/app/dashboard/layout.tsx` with auth check and route protection
- [ ] T027 [P] Write component tests for Navbar.tsx in `frontend/tests/components/Navbar.test.tsx` (profile display, logout functionality)
- [ ] T028 Write component tests for ThemeToggle.tsx in `frontend/tests/components/ThemeToggle.test.tsx` (theme switching, persistence)
- [ ] T029 [P] Write responsive design tests in `frontend/tests/components/DashboardLayout.test.tsx` (mobile, tablet, desktop layouts)
- [ ] T030 [P] Write integration test for theme persistence in `frontend/tests/integration/theme-persistence.test.tsx`
- [ ] T031 Create Loading and Error fallback components in `frontend/src/components/common/` for suspense boundaries

**Checkpoint**: Dashboard displays correctly on all device sizes. Theme toggle works and persists. Navbar shows user info and logout button. US1 is fully functional and independently testable. ✅

---

## Phase 4: User Story 2 - Manage Tasks with Advanced CRUD Operations (Priority: P1)

**Goal**: Users can add, edit, and delete individual tasks with title, description, and priority.

**Independent Test**: Create task → Edit task → Delete task with confirmation → All changes persist in database

### Implementation for User Story 2

- [ ] T032 [P] Create TaskList component in `frontend/src/components/tasks/TaskList.tsx` that:
  - [ ] Displays all user's tasks in a list format
  - [ ] Shows title, description preview, priority badge, completion status
  - [ ] Uses useOptimistic hook for immediate UI updates
  - [ ] Has loading and empty states
- [ ] T033 Create TaskItem component in `frontend/src/components/tasks/TaskItem.tsx` for single task row with:
  - [ ] Edit button (opens form modal)
  - [ ] Delete button (opens confirmation dialog)
  - [ ] Completion toggle
  - [ ] Priority display badge
- [ ] T034 Create TaskForm component in `frontend/src/components/tasks/TaskForm.tsx` with:
  - [ ] React Hook Form integration
  - [ ] Zod validation schema (title: 1-500 chars required, description: 0-2000 chars optional, priority enum)
  - [ ] Inline error messages above fields
  - [ ] Submit handler calls useTaskActions for optimistic update
  - [ ] Modal wrapper using Shadcn Dialog
- [ ] T035 [P] Create Zod validation schema in `frontend/src/services/validations.ts` with taskCreateSchema and taskUpdateSchema
- [ ] T036 Create DeleteConfirmDialog in `frontend/src/components/tasks/DeleteConfirmDialog.tsx` using Shadcn Dialog for single task deletion
- [ ] T037 [P] Create PriorityPopover in `frontend/src/components/tasks/PriorityPopover.tsx` using Shadcn Popover for inline priority selection
- [ ] T038 Implement POST /api/tasks integration in task service and handle 201 response in `frontend/src/services/tasks.ts`
- [ ] T039 Implement PUT /api/tasks/{id} integration for task updates in `frontend/src/services/tasks.ts`
- [ ] T040 [P] Implement DELETE /api/tasks/{id} integration for single task deletion in `frontend/src/services/tasks.ts`
- [ ] T041 Create main tasks page in `frontend/src/app/dashboard/tasks/page.tsx` that renders TaskList
- [ ] T042 [P] Write component tests for TaskForm.tsx in `frontend/tests/components/TaskForm.test.tsx` (validation, form submission)
- [ ] T043 Write component tests for TaskList.tsx in `frontend/tests/components/TaskList.test.tsx` (display, optimistic updates, add/edit/delete flows)
- [ ] T044 [P] Write integration test for complete CRUD flow in `frontend/tests/integration/task-crud.test.tsx`
- [ ] T045 [P] Write API contract tests in `frontend/tests/contract/tasks.test.ts` (POST, PUT, DELETE endpoints with JWT)
- [ ] T046 Write error handling tests for validation, network errors, 403 Forbidden scenarios in `frontend/tests/components/TaskForm.test.tsx`

**Checkpoint**: All CRUD operations (create, read, update, delete) work with optimistic feedback. Forms validate with Zod. Confirmations prevent accidental deletion. US2 is fully functional and independently testable. ✅

---

## Phase 5: User Story 3 - Perform Bulk Operations on Multiple Tasks (Priority: P2)

**Goal**: Users can select multiple tasks and bulk delete or mark complete.

**Independent Test**: Select 5 tasks via checkboxes → Bulk delete with confirmation showing count → All tasks removed

### Implementation for User Story 3

- [ ] T047 Create checkbox column in TaskItem component (`frontend/src/components/tasks/TaskItem.tsx`) with:
  - [ ] Checkbox input for each task
  - [ ] onChange handler calls useBulkSelection.toggleSelection(id)
- [ ] T048 Create "Select All" checkbox in TaskList component header that calls useBulkSelection.selectAll(allTaskIds)
- [ ] T049 Create BulkActions component in `frontend/src/components/tasks/BulkActions.tsx` with:
  - [ ] Shows selection count: "{n} tasks selected"
  - [ ] "Bulk Delete" button (disabled if no selection)
  - [ ] "Bulk Mark Complete" button (disabled if no selection)
  - [ ] "Clear Selection" button
- [ ] T050 Create BulkDeleteDialog in `frontend/src/components/tasks/BulkDeleteDialog.tsx` using Shadcn Dialog with:
  - [ ] Confirmation message: "Delete {n} tasks?"
  - [ ] Confirm/Cancel buttons
  - [ ] Calls bulkDeleteTasks from task service
- [ ] T051 [P] Implement bulk delete via Promise.all in `frontend/src/services/tasks.ts`:
  - [ ] Takes array of task IDs
  - [ ] Parallelizes DELETE /api/tasks/{id} requests (5 concurrent)
  - [ ] Counts successes/failures
  - [ ] Returns { deleted_count, failed_count }
- [ ] T052 Implement bulk mark-complete via Promise.all in `frontend/src/services/tasks.ts`:
  - [ ] Takes array of task IDs
  - [ ] Parallelizes PUT /api/tasks/{id} with { completed: true }
  - [ ] Returns { updated_count, failed_count }
- [ ] T053 [P] Integrate BulkActions and bulk operations into TaskList component
- [ ] T054 [P] Add optimistic updates for bulk operations in useTaskActions hook
- [ ] T055 [P] Write component tests for BulkActions in `frontend/tests/components/BulkActions.test.tsx` (selection state, button states)
- [ ] T056 Write integration test for bulk delete flow in `frontend/tests/integration/bulk-delete.test.tsx`
- [ ] T057 [P] Write integration test for bulk complete in `frontend/tests/integration/bulk-complete.test.tsx`
- [ ] T058 Write performance test: bulk operations on 100 tasks complete within 3 seconds in `frontend/tests/performance/bulk-operations.test.tsx`

**Checkpoint**: Checkbox selection works, bulk operations execute via Promise.all parallelization in <3 seconds, confirmations prevent accidents. US3 is fully functional and independently testable. ✅

---

## Phase 6: User Story 4 - Receive Interactive Feedback on All Actions (Priority: P1)

**Goal**: Toast notifications appear for all task operations with success/error messages.

**Independent Test**: Create task → Success toast appears → Delete task → Error handling shows error toast

### Implementation for User Story 4

- [ ] T059 Create TaskNotification utility in `frontend/src/services/notifications.ts` with helper functions:
  - [ ] showSuccessToast(message) - uses sonner.toast.success()
  - [ ] showErrorToast(message) - uses sonner.toast.error()
  - [ ] showLoadingToast(message) - uses sonner.loading()
- [ ] T060 Create notification messages helper in `frontend/src/constants/messages.ts` with:
  - [ ] Task created successfully
  - [ ] Task updated successfully
  - [ ] Task deleted successfully
  - [ ] {n} tasks deleted successfully
  - [ ] {n} tasks marked complete
  - [ ] Error messages for validation, network, 403, 500 errors
- [ ] T061 Integrate toast notifications into TaskForm submit handler - show success after create/update, error on failure
- [ ] T062 [P] Integrate toast notifications into delete operations - show success after single delete
- [ ] T063 Integrate toast notifications into bulk operations - show "{n} tasks deleted" or "{n} tasks marked complete"
- [ ] T064 [P] Add error handling for failed requests: catch 401/403/422/500 and show appropriate error toast
- [ ] T065 Implement retry logic with toast: "Request failed. Retrying..." for network errors
- [ ] T066 [P] Write component tests for notification display in `frontend/tests/components/TaskForm.test.tsx`
- [ ] T067 Write integration tests for notification flow in `frontend/tests/integration/notifications.test.tsx`
- [ ] T068 [P] Verify toast stacking and auto-dismiss (5 seconds) in `frontend/tests/integration/toast-behavior.test.tsx`
- [ ] T069 Test notification appearance timing: all toasts appear within 500ms of action

**Checkpoint**: All operations show clear feedback. Errors are user-friendly. Notifications auto-dismiss and stack correctly. US4 is fully functional. ✅

---

## Phase 7: User Story 5 - View User Profile and Logout (Priority: P1)

**Goal**: Navbar displays user profile info and logout button. Logout terminates session and prevents access to protected pages.

**Independent Test**: Login → Navbar shows user email → Click logout → Redirect to login page → Back button doesn't restore access

### Implementation for User Story 5

- [ ] T070 Update Navbar component to fetch and display user profile via Better Auth session:
  - [ ] Display user.name or user.email from useSession()
  - [ ] User avatar/initial (if Better Auth provides)
  - [ ] User menu/dropdown (optional)
- [ ] T071 Implement logout button in Navbar that:
  - [ ] Calls logout() from auth service
  - [ ] Clears JWT token from cookies/storage
  - [ ] Redirects to /login page
  - [ ] Clears session state
- [ ] T072 [P] Verify middleware redirects unauthenticated users to /login on protected routes in `frontend/src/middleware.ts`
- [ ] T073 Test that browser back button after logout doesn't restore access to protected pages (no cache replay)
- [ ] T074 [P] Add session expiration handling: detect expired JWT in API responses (401) and redirect to login
- [ ] T075 Create UserMenu component in `frontend/src/components/dashboard/UserMenu.tsx` (optional dropdown with profile options)
- [ ] T076 [P] Write component tests for Navbar logout in `frontend/tests/components/Navbar.test.tsx`
- [ ] T077 Write integration test for logout flow in `frontend/tests/integration/logout.test.tsx`
- [ ] T078 [P] Write integration test for session expiration handling in `frontend/tests/integration/session-expiration.test.tsx`
- [ ] T079 Write security test: verify JWT is never exposed in localStorage/sessionStorage, only in httpOnly cookies

**Checkpoint**: User profile displays, logout works, session is terminated, protected pages are inaccessible after logout. US5 is fully functional. ✅

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Finalization, optimization, accessibility, and quality assurance

- [ ] T080 [P] Accessibility audit: keyboard navigation (Tab, Escape) in all modals and forms
- [ ] T081 Accessibility: verify color contrast meets WCAG 2.1 AA (use Shadcn components, built on Radix UI)
- [ ] T082 [P] Accessibility: verify touch targets are >= 44x44px on mobile
- [ ] T083 [P] Accessibility: test with screen reader (NVDA/JAWS) - all interactive elements announced correctly
- [ ] T084 Performance: measure dashboard load time on 4G network - must be < 2 seconds
- [ ] T085 Performance: measure CRUD operation latency with useOptimistic - must show <50ms perceived delay
- [ ] T086 [P] Performance: measure bulk operation latency - 100 tasks must delete in <3 seconds via Promise.all
- [ ] T087 [P] Responsive design testing: verify layouts on mobile (320px), tablet (768px), desktop (1024px) using Chrome DevTools
- [ ] T088 Error boundary implementation in `frontend/src/components/common/ErrorBoundary.tsx` for graceful error handling
- [ ] T089 [P] Add loading skeletons for TaskList in `frontend/src/components/common/TaskSkeleton.tsx` during data fetch
- [ ] T090 Implement error recovery: "Retry" button on failed task operations
- [ ] T091 [P] Setup Sentry or similar error tracking for production monitoring in `frontend/src/lib/sentry.ts`
- [ ] T092 Add analytics: track user actions (task created, deleted, bulk ops) using event tracking
- [ ] T093 [P] Code review checklist: all tasks follow clean code principles, single responsibility, testable functions
- [ ] T094 Final end-to-end test: complete user journey (login → create/edit/delete/bulk tasks → logout) in `frontend/tests/e2e/user-journey.test.tsx`
- [ ] T095 [P] Documentation: update README.md with setup instructions, env vars, testing guide
- [ ] T096 Documentation: update API documentation with task-api.openapi.yaml integration
- [ ] T097 [P] Git workflow: ensure all commits reference Task ID (T001, T002, etc.) per constitution
- [ ] T098 Security review: verify JWT handling, no secrets in code, CORS configured, input validation

**Checkpoint**: All user stories complete, accessible, performant, tested, documented. Feature ready for production. ✅

---

## Dependency Graph & Parallel Execution

### Phase 2 is BLOCKING (must complete first)
After Phase 2, the following can run in PARALLEL:

```
Phase 3 (US1: Dashboard)    ──┐
Phase 4 (US2: CRUD)         ──┼──> Final integration
Phase 5 (US3: Bulk)         ──┤
Phase 6 (US4: Notifications)─┤
Phase 7 (US5: Profile)      ──┘

Phase 8 (Polish) ──> Production ready
```

### Suggested Parallel Groups
- **Developer 1**: US1 (Dashboard) + US4 (Notifications)
- **Developer 2**: US2 (CRUD) + US5 (Profile)
- **Developer 3**: US3 (Bulk Operations)
- **QA/DevOps**: Run Phase 8 (Polish) after all user stories complete

### MVP Scope
To deliver MVP with core functionality:
1. Complete Phase 1 & 2 (foundational)
2. Complete Phase 3 (US1: Dashboard - responsive layout with theme)
3. Complete Phase 4 (US2: Task CRUD operations)

**MVP Checklist**:
- [ ] Dashboard displays correctly
- [ ] Users can create, edit, delete individual tasks
- [ ] Theme toggle works and persists
- [ ] User profile shows in navbar
- [ ] Logout works

**Post-MVP Enhancements**:
- Bulk operations (US3)
- Toast notifications (US4)
- Accessibility & performance (Phase 8)

---

## Task Assignment & Tracking

Each task follows format: `[ID] [P?] [Story?] Description`

Use task ID in commit messages:
```
git commit -m "T045: Add API contract tests for task CRUD endpoints"
```

Update task status:
```
- [ ] T001 ... (pending)
- [x] T001 ... (completed)
- [-] T001 ... (in progress)
```

---

## Success Metrics

By completing all tasks, you will achieve:

✅ **Functional Completeness**
- All 5 user stories independently testable
- 100% task CRUD operations functional
- Bulk operations handle 100 tasks in <3 seconds
- All user journeys end-to-end testable

✅ **Quality**
- WCAG 2.1 AA accessibility compliance
- <2 second dashboard load time
- <500ms perceived CRUD latency (useOptimistic)
- >95% test coverage for critical paths

✅ **Production Readiness**
- Authentication enforced on all routes
- JWT validation on all API calls
- Error handling for all failure modes
- Logging and monitoring configured
- Code follows clean code principles
- All commits linked to Task IDs

---

## Notes & Assumptions

- All file paths assume `frontend/` for Next.js app (monorepo structure from plan.md)
- Backend endpoints (`DELETE /api/todos/{todo_id}`, etc.) already exist from Phase 1
- Bulk operations use Promise.all since backend has no native batch endpoints (per clarifications)
- Form validation uses Zod with React Hook Form (1-500 char title, 0-2000 char description)
- Session check via Better Auth `useSession()` hook + Next.js middleware prevents FOUC
- All tasks are independent and parallelizable except where noted by sequential dependencies
