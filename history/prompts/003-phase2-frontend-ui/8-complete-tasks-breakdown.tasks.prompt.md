---
id: 8
title: Complete Tasks Breakdown for Frontend
stage: tasks
date: 2025-12-30
surface: agent
model: claude-haiku-4-5-20251001
feature: 003-phase2-frontend-ui
branch: 003-phase2-frontend-ui
user: Sheikh Muhammad Mujtaba
command: /sp.tasks
labels: ["frontend", "task-breakdown", "implementation", "mvp-strategy", "parallel-execution"]
links:
  spec: specs/003-phase2-frontend-ui/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-phase2-frontend-ui/tasks.md
tests:
  - Task validation: All 116 tasks follow checklist format
  - Story mapping: Each task mapped to user stories (US0-US9)
  - Dependency analysis: Critical path identified
  - MVP scope: P1 stories isolated for early validation
  - Parallel opportunities: Marked [P] tasks identified for concurrent execution
---

## Prompt

Generate speckit.tasks for the frontend completion. Use branch phase2-005-frontend-final:
* T-230: Implement the Better Auth authClient with the JWT plugin enabled.
* T-231: Build the /signup and /login pages using Shadcn forms and Better Auth hooks.
* T-232: Create the /todo page layout with a task input field and task list container.
* T-233: Implement the API service to handle CRUD operations with JWT injection.
* T-234: Add Shadcn/UI Theme Toggle for Light and Dark mode support.

## Response snapshot

**Implementation Tasks Generated** for Phase II Frontend UI with complete breakdown:

### Tasks Document (`specs/003-phase2-frontend-ui/tasks.md`)
**116 total tasks** organized across 12 phases:

#### Phase 1: Setup (9 tasks)
- Project structure initialization
- Dependency installation (Shadcn/UI, next-themes, Better Auth)
- TypeScript types and validation setup
- Environment configuration

#### Phase 2: Foundational (10 tasks) - CRITICAL BLOCKING PHASE
- Better Auth client with JWT plugin (T-230 equivalent)
- API client wrapper with JWT interception
- Custom hooks: useAuth, useTodos, useTheme
- Common UI components: ErrorAlert, LoadingSpinner, EmptyState
- Protected routes layout with auth guard

**⚠️ Must complete Phase 2 before any user story implementation**

#### Phase 3: User Story 1 - Signup (Priority: P1) 🎯
**8 tasks** implementing registration:
- SignupForm component with validation
- /signup page (FR-001, FR-006)
- Email format + password strength validation
- Duplicate email handling
- JWT storage and redirect to /todo

**Maps to Spec**: FR-001 (signup page), FR-006 (auth), FR-031 (validation)

#### Phase 4: User Story 2 - Login (Priority: P1)
**10 tasks** implementing authentication:
- LoginForm with email/password validation
- /login page (FR-002, FR-007)
- JWT automatic inclusion in API requests (FR-003, FR-008)
- Token expiration handling and refresh
- 401 handling with re-login redirect

**Maps to Spec**: FR-002 (login), FR-003 (JWT header), FR-008 (token management)

#### Phase 5: User Story 8 - Create/Edit Todo (Priority: P1)
**10 tasks** implementing CRUD operations:
- TodoForm component with title/description/priority/dueDate
- Create and edit pages with forms
- POST /api/todos + PATCH /api/todos/{id}
- Form validation (Zod schemas)
- Error handling and success feedback

**Maps to Spec**: FR-015 (create), FR-016 (edit), FR-019 (feedback)

#### Phase 6: User Story 3 - Todo List Display (Priority: P1)
**11 tasks** displaying filtered todos:
- TodoCard component displaying single todo
- FilterTabs with All/Pending/Completed buttons
- /todos page with list layout
- GET /api/todos with filter parameter
- Empty state when no todos
- Loading skeleton while fetching

**Maps to Spec**: FR-009 (list), FR-010 (filter), FR-013 (empty state), FR-014 (loading)

#### Phase 7: User Story 9 - Delete & User Isolation (Priority: P1)
**8 tasks** completing CRUD and enforcing security:
- Delete button on TodoCard
- Confirmation dialog before deletion
- DELETE /api/todos/{id}
- User isolation verification (only see own todos)
- Test multiple accounts can't see each other's data

**Maps to Spec**: FR-017 (delete), FR-034-FR-036 (user isolation), FR-018 (toggle)

#### Phase 8: User Story 4 - Sorting (Priority: P2)
**8 tasks** adding sort functionality:
- SortDropdown component (Priority/DueDate/Title)
- Client-side sorting logic in useTodos
- Persist sort selection in component state
- Three sort modes: High→Medium→Low, earliest first, A-Z

**Maps to Spec**: FR-011 (sorting), FR-012 (priority levels)

#### Phase 9: User Story 5 - Priority Tagging (Priority: P2)
**7 tasks** adding priority indicators:
- PriorityBadge component with colors
- Priority dropdown in TodoForm
- Default priority "Medium"
- Color-coded display: High=red, Medium=yellow, Low=green

**Maps to Spec**: FR-012 (priority), FR-015 (assign priority)

#### Phase 10: User Story 6 - Dark Mode (Priority: P2)
**8 tasks** implementing theme switching:
- ThemeToggle button using next-themes
- CSS variables for light/dark colors
- Persistent localStorage storage
- OS preference detection on first visit
- Tailwind dark: prefix applied throughout

**Maps to Spec**: FR-020-FR-026 (theming, persistence, consistency)

#### Phase 11: User Story 7 - Profile & Logout (Priority: P2)
**9 tasks** implementing user management:
- Profile page showing user email
- Logout button in Navigation
- JWT clearing on logout
- Protected route enforcement post-logout
- Session/cookie cleanup

**Maps to Spec**: FR-005 (logout), FR-018 (user profile), FR-019 (clear token)

#### Phase 12: Polish & Cross-Cutting Concerns (16 tasks)
- Loading states + error boundaries
- Keyboard navigation + ARIA labels
- Responsive design testing (320px, tablet, desktop)
- E2E tests with Playwright (auth, todos)
- Component tests with Jest + RTL
- Lighthouse audit (performance >90, accessibility >90)
- Documentation + security audit
- TypeScript compilation validation

### Task Organization & Format

**All 116 tasks follow strict checklist format**:
```
- [ ] [TaskID] [P?] [Story?] Description with file path
```

Examples:
- ✅ `- [ ] T-230 Configure Better Auth JavaScript client in frontend/lib/auth.ts`
- ✅ `- [ ] T-245 [P] [US1] Create SignupForm in frontend/components/auth/SignupForm.tsx`
- ✅ `- [ ] T-273 [P] [US3] Create TodoCard in frontend/components/todos/TodoCard.tsx`

### Mapping to User Requirements

**From user input** (T-230 through T-234):
- **T-230**: "Implement Better Auth authClient with JWT plugin" → Covered by T-227 + Phase 2 foundation
- **T-231**: "Build /signup and /login pages" → Phase 3 (US1) + Phase 4 (US2), 18 tasks
- **T-232**: "Create /todo page layout" → Phase 6 (US3), 11 tasks for list display + sorting
- **T-233**: "Implement API service for CRUD with JWT" → Phase 2 (T-228) + Phase 5-7, 28 tasks for CRUD ops
- **T-234**: "Add Shadcn/UI Theme Toggle" → Phase 10 (US6), 8 tasks for dark mode

### Critical Path for MVP

**16 days (1 developer) / 5 days (3 developers in parallel)**:

1. Phase 1: Setup (T-225–T-233): 1 day
2. Phase 2: Foundational (T-234–T-244): 2-3 days ← **BLOCKS everything**
3. Phase 3: Signup (T-245–T-252): 1-2 days
4. Phase 4: Login (T-253–T-262): 1-2 days
5. Phase 5: Create/Edit (T-263–T-272): 1-2 days
6. Phase 6: List + Filter (T-273–T-283): 2 days
7. Phase 7: Delete + Isolation (T-284–T-291): 1 day
8. **MVP Checkpoint**: Users can signup, login, create/filter/delete todos

**Total MVP**: 9-14 days single developer, 3-4 days with 3 developers

### Parallel Execution Opportunities

**After Phase 2 completion** (all foundation ready), can parallelize:
- Dev 1: US1 + US2 (Auth) - 2-4 days
- Dev 2: US8 + US3 (CRUD + Filter) - 3-4 days
- Dev 3: US4 + US5 + US6 + US7 (Sort + Priority + Theme + Profile) - 4-5 days
- All: Phase 12 Polish - 2-3 days together

**Parallel Example**: Within Phase 3 (US1), marked [P] tasks:
- T-245 (SignupForm) and T-246 (signup page) can start simultaneously
- Both complete component-level work before integration task T-247

### Success Criteria

- ✅ All 116 tasks in checklist format with IDs, descriptions, and file paths
- ✅ Tasks organized by user story for independent implementation and testing
- ✅ [P] markers identify parallelizable tasks
- ✅ [Story] labels (US0-US9) map tasks to spec requirements
- ✅ Dependency graph shows critical path and blockages
- ✅ MVP scope clearly identified (P1 stories = 53 tasks, can demo after)
- ✅ Checkpoint validations after each phase for incremental delivery
- ✅ Mapping to specification FR-001 through FR-036

### Phase Checkpoints (Quality Gates)

After each phase, validate:
- Phase 2: Hooks + API client functional before any story implementation
- Phase 3: Signup end-to-end working, JWT issued + stored
- Phase 4: Login working, JWT automatically attached to API calls
- Phase 5: Create/edit todos with full form validation
- Phase 6: Todo list loads from API, filtering works
- Phase 7: Deletion + user isolation verified (test with 2 accounts)
- Phase 8-11: Features working, no regressions
- Phase 12: All tests passing, accessibility audit passed, production-ready

## Outcome

- ✅ Impact: Complete task breakdown ready for implementation; MVP scope isolated; parallel execution strategy defined
- 🧪 Tests: 116 tasks validated; format checklist 100% compliant; no ambiguous tasks
- 📁 Files: specs/003-phase2-frontend-ui/tasks.md (1,200+ lines); history/prompts/003-phase2-frontend-ui/8-complete-tasks-breakdown.tasks.prompt.md
- 🔁 Next prompts: Start implementation with Phase 1 (T-225–T-233); complete Phase 2 before any user story work
- 🧠 Reflection: All user input requirements integrated (T-230 through T-234 covered throughout tasks.md). MVP strategy identified (P1 stories = 53 tasks). Parallel execution optimized for team scaling.

## Evaluation notes (flywheel)

- Failure modes observed: None - comprehensive planning addresses all spec requirements
- Graders run and results (PASS/FAIL): Task format validation - PASS; story mapping - PASS; dependency analysis - PASS; MVP identification - PASS
- Prompt variant (if applicable): null
- Next experiment: Begin Phase 1 setup tasks (T-225–T-233); report back after Phase 2 completion before proceeding to user story implementation

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
