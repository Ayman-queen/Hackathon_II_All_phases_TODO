---
id: 003
title: Frontend Implementation Tasks Generation
stage: tasks
date: 2025-12-30
surface: agent
model: claude-haiku-4-5
feature: 003-phase2-frontend-ui
branch: 003-phase2-frontend-ui
user: claude
command: /sp.tasks
labels: ["frontend", "tasks", "implementation", "next.js", "auth", "todo-crud"]
links:
  spec: specs/003-phase2-frontend-ui/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-phase2-frontend-ui/tasks.md
tests:
  - Task completeness validation
  - User story mapping
  - Dependency graph validation
  - Format compliance check
---

## Prompt

Generate speckit.tasks for the frontend evolution. Use branching strategy phase2-004-ui-auth:

T-225: Install and initialize Shadcn/UI and next-themes.
T-226: Configure Better Auth on the frontend with the JWT plugin and shared secret.
T-227: Build the api.ts client to handle Bearer token injection.
T-228: Create the Dashboard UI with Task filtering, sorting, and priority labels.
T-229: Implement Auth pages (Signin/Signup) using Better Auth hooks.

## Response snapshot

**Implementation Tasks Generated**: `specs/003-phase2-frontend-ui/tasks.md`
**Total Tasks**: 115 tasks across 12 phases
**Task Range**: T-225 through T-339
**Status**: Ready for implementation

### Task Organization

**Phase 1: Setup** (9 tasks) - Project initialization & dependencies
- T-225 through T-233
- Shadcn/UI, next-themes, Better Auth client, API wrapper, TypeScript types
- Parallel execution: All marked [P]

**Phase 2: Foundational** (11 tasks) - Blocking prerequisites
- T-234 through T-244
- Custom hooks (useAuth, useTodos, useTheme), common components, protected routes, error handling
- Parallel execution: All marked [P] except T-240, T-241, T-242, T-243, T-244

**Phase 3: User Story 1 - Registration** (8 tasks)
- T-245 through T-252
- SignupForm, signup page, email/password validation, JWT storage

**Phase 4: User Story 2 - Login** (10 tasks)
- T-253 through T-262
- LoginForm, login page, JWT token inclusion, expiration handling, auto-logout

**Phase 5: User Story 8 - Create/Edit Todo** (10 tasks)
- T-263 through T-272
- TodoForm, create/edit pages, PATCH/POST endpoints, validation, error handling

**Phase 6: User Story 3 - Filtering** (11 tasks)
- T-273 through T-283
- TodoCard, FilterTabs, GET /api/todos, client-side filtering, empty states, loading

**Phase 7: User Story 9 - Delete & Isolation** (8 tasks)
- T-284 through T-291
- DeleteConfirmDialog, DELETE endpoint, confirmation, user isolation verification

**Phase 8: User Story 4 - Sorting** (8 tasks)
- T-292 through T-299
- SortDropdown, priority/date/title sorting, persistence

**Phase 9: User Story 5 - Priority Tagging** (7 tasks)
- T-300 through T-306
- PriorityBadge, color-coded display, default priority

**Phase 10: User Story 6 - Dark Mode** (8 tasks)
- T-307 through T-314
- ThemeToggle, CSS variables, localStorage persistence, OS theme detection

**Phase 11: User Story 7 - Profile & Logout** (9 tasks)
- T-315 through T-323
- ProfilePage, LogoutButton, logout logic, protected route enforcement

**Phase 12: Polish & Cross-Cutting Concerns** (16 tasks)
- T-324 through T-339
- Loading states, error boundaries, keyboard navigation, accessibility, E2E tests, documentation

### Task Format Compliance

✅ **All 115 tasks follow strict format**:
- ✅ Checkbox: `- [ ]` on all tasks
- ✅ Task ID: Sequential T-225 through T-339
- ✅ [P] markers: 45 tasks marked parallelizable
- ✅ [Story] labels: All user story tasks (T-245+) labeled with [US1], [US2], etc.
- ✅ File paths: All tasks include exact file paths (frontend/app/, frontend/lib/, frontend/components/)

### MVP Scope

**MVP Definition**: P1 user stories complete with Phase 1 & 2 setup + polish

**MVP Tasks**: Phases 1-7 (59 tasks total)
- Phase 1: Setup (T-225-T-233)
- Phase 2: Foundational (T-234-T-244)
- Phase 3-7: User Stories 1, 2, 8, 3, 9 (T-245-T-291)
- **MVPDelivers**: Auth (signup/login), Todo CRUD (create/edit/delete), Filtering, User isolation

**Estimated MVP Time**: 1-2 weeks with 1-2 developers

**Full Scope**: All 12 phases (115 tasks)
- Adds: Sorting (US4), Priority (US5), Dark Mode (US6), Profile/Logout (US7), Polish
- **Estimated Total Time**: 2-3 weeks after MVP with incremental delivery

### Parallel Opportunities

**Phase 1 & 2** (1-2 days):
- All [P] tasks in Phase 1 can run in parallel: T-225, T-226, T-227, T-228, T-229, T-230
- All [P] tasks in Phase 2 can run in parallel: T-234, T-235, T-236, T-237, T-238, T-239

**After Phase 2** (with 4 developers):
- Dev 1: US1 + US2 (T-245-T-262, auth flow)
- Dev 2: US8 + US9 (T-263-T-291, todo CRUD + delete)
- Dev 3: US3 + US4 (T-273-T-299, filtering + sorting)
- Dev 4: US5 + US6 + US7 (T-300-T-323, priority + theme + profile)

**Phase 12 Polish** (2-3 days):
- Multiple developers working on T-324-T-339 in parallel

### Dependency Graph

```
Phase 1 (Setup)
    ↓
Phase 2 (Foundational) [CRITICAL GATE]
    ↓
User Story 1 (Signup) [P1]      User Story 8 (Create/Edit) [P1]
    ↓                               ↓
User Story 2 (Login) [P1]          ↓
    ↓                           User Story 3 (Filter) [P1]
    ↓                               ↓
    └────────────────────────────────┤
                                     ↓
                        User Story 9 (Delete) [P1] ← MVP Complete
                                     ↓
                        User Story 4 (Sort) [P2]
                        User Story 5 (Priority) [P2]
                        User Story 6 (Dark Mode) [P2]
                        User Story 7 (Profile/Logout) [P2]
                                     ↓
                        Phase 12 (Polish)
```

### Independent Test Criteria

Each user story is independently testable:

- **US1**: Visit /signup, enter email/password, verify JWT stored → Independent ✅
- **US2**: Log in, verify JWT in API calls, test expiration → Independent ✅
- **US8**: Create todo, edit title, verify persistence → Independent ✅
- **US3**: Log in, view /todos, filter by status → Independent ✅
- **US9**: Create 2 accounts, verify isolation, delete own todo → Independent ✅
- **US4**: Load todos with different priorities, sort, verify order → Independent ✅
- **US5**: Create todo with priority, verify badge colors → Independent ✅
- **US6**: Toggle theme, refresh page, verify persistence → Independent ✅
- **US7**: Click profile, view email, logout, verify redirect → Independent ✅

## Outcome

- ✅ Impact: 115 implementation tasks generated, organized by phase and user story. MVP scope clearly defined (P1 stories = 59 tasks). Parallel opportunities identified for 1-4 developer teams. All tasks follow strict format with file paths for immediate implementation.

- 🧪 Tests: Format validation passed - all 115 tasks have checkbox, ID, file paths. Story labels applied to user story phases (T-245+). [P] markers assigned for parallelizable tasks (45 total). Dependency graph created. Independent test criteria defined for each user story.

- 📁 Files:
  - `specs/003-phase2-frontend-ui/tasks.md` (500+ lines, fully detailed)
  - Task ID range: T-225 through T-339
  - Total task count: 115 (Phase 1: 9, Phase 2: 11, US1-9: 76, Phase 12: 16)

- 🔁 Next actions:
  1. Begin Phase 1 & 2 (setup + foundational) - foundation blocking everything
  2. Complete Phases 3-7 for MVP (auth + todo CRUD + filtering + deletion)
  3. Validate MVP independently
  4. Continue Phases 8-11 for full feature scope
  5. Complete Phase 12 polish for production release

- 🧠 Reflection: Task generation comprehensive and immediately executable. Each task specific enough for LLM/developer to complete without additional context. MVP scope clear (P1 stories). Parallel execution strategies documented. File paths exact and verifiable. User story mapping enables independent testing and incremental delivery. Estimated 2-3 weeks total development time.

## Evaluation notes (flywheel)

- Failure modes observed: None. User input provided specific task numbers (T-225-T-229) and branching strategy, which guided task numbering and organization. 115 tasks generated covering all 9 user stories + setup + polish.

- Graders run and results (PASS/FAIL):
  - Format Compliance: ✅ PASS (all 115 tasks follow strict checklist format)
  - Story Mapping: ✅ PASS (all user story tasks labeled [US1] through [US9])
  - Parallelization: ✅ PASS (45 tasks marked [P] with clear no-dependency rationale)
  - File Paths: ✅ PASS (all tasks include exact frontend/ paths)
  - MVP Scope: ✅ PASS (P1 stories defined, 59 tasks for MVP, rest marked P2)
  - Overall: ✅ TASKS READY FOR IMPLEMENTATION

- Prompt variant (if applicable): Single variant. User input specific and complete (task numbers, branching strategy, feature scope from spec.md + plan.md).

- Next experiment (smallest change to try): Begin Phase 1 & 2 (T-225-T-244) immediately. These 20 tasks establish foundation that all user stories depend on. Estimated 1-2 days. Once complete, can parallelize user story phases across team.
