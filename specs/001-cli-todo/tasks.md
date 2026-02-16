# Tasks: CLI Todo Application

**Feature Branch**: `001-cli-todo`
**Created**: 2025-12-27
**Last Updated**: 2025-12-27

**Input**: Design documents from `/specs/001-cli-todo/`
**Prerequisites**: plan.md, spec.md, data-model.md, quickstart.md

## Task Organization

Tasks are grouped by user story to enable independent implementation and testing of each story. Each story phase represents a complete, testable increment toward the MVP.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- **ID**: Sequential task identifier (T001, T002, T003...)
- **File paths**: Exact locations for code and tests

---

## Phase 1: Setup & Project Initialization

**Purpose**: Project initialization and basic structure for CLI application

**Prerequisite**: Must complete before any user story work begins

- [ ] T001 Create project directory structure (src/todo_app/, tests/)
- [ ] T002 Initialize Python project with uv: create pyproject.toml with Python 3.13+ requirement and pytest dependency
- [ ] T003 Create __init__.py files for all packages (src/todo_app/, src/todo_app/models/, src/todo_app/services/, src/todo_app/ui/, tests/, tests/unit/, tests/integration/, tests/contract/)
- [ ] T004 [P] Setup pyproject.toml configuration with CLI entry point and test configuration

**Checkpoint**: Project structure ready and dependencies configured

---

## Phase 2: Foundation (Blocking Prerequisites)

**Purpose**: Core components that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 [P] Create Task model class in src/todo_app/models/task.py with fields (id, title, description, is_complete) and validation
- [ ] T006 [P] Create TodoManager service class in src/todo_app/services/todo_manager.py with CRUD methods (create_task, get_all_tasks, get_task, update_task, mark_complete, delete_task)
- [ ] T007 [P] Create CLI Handler utility functions in src/todo_app/ui/cli_handler.py (format_task, format_task_list, prompt_user_input, display_message)
- [ ] T008 Create main application entry point in src/todo_app/main.py with menu loop and session initialization

**Implementation Details**:
- T005: Task class with @property decorators for immutability; constructor validation for title non-empty
- T006: TodoManager with _tasks: List[Task], _next_id counter; raise ValueError on invalid operations
- T007: Pure functions for formatting; use input() for prompts; support Unicode checkbox symbols (☐, ☑)
- T008: Infinite menu loop using input(); route to operations; handle KeyboardInterrupt gracefully

**Checkpoint**: Foundation complete - all 5 user stories can now be implemented in parallel

---

## Phase 3: User Story 1 - View Todo List (Priority: P1) 🎯 MVP

**Goal**: Users can launch the application and see all todos in an organized, readable format with status indicators (☐/☑)

**Independent Test**: Launch app → verify list displays correctly with empty state message, then add a todo and verify it appears with correct status and formatting

**Acceptance Criteria** (from spec.md):
1. Empty list shows "No todos yet. Add one to get started!"
2. Todos display with ID, title, description, and status (☐ or ☑)
3. Todos appear in insertion order

### Implementation for User Story 1

- [ ] T009 [P] [US1] Create unit test file tests/unit/test_cli_handler.py with tests for format_task() and format_task_list()
- [ ] T010 [P] [US1] Create unit test file tests/unit/test_cli_handler_edge_cases.py testing long title truncation (60 char) and empty description handling
- [ ] T011 [US1] Implement menu option 1 (View Todos) in src/todo_app/main.py: call cli_handler.format_task_list() and display result
- [ ] T012 [US1] Add integration test tests/integration/test_view_todos.py: launch app, verify empty state message, add todo, verify display

**Checkpoint**: User Story 1 complete and independently testable

**MVP Release**: This story alone provides a functional, minimal viable product

---

## Phase 4: User Story 2 - Add New Todo (Priority: P1)

**Goal**: Users can create new todos with required title and optional description; confirmation shows new todo with unique auto-generated ID

**Independent Test**: Execute "Add Todo" → provide title/description → verify new todo appears in list with correct ID, title, description, and incomplete status (☐)

**Acceptance Criteria** (from spec.md):
1. Prompts for title (required) and description (optional)
2. New todo appears with unique auto-incrementing ID starting at 1
3. New todo defaults to incomplete status (☐)
4. Empty title input re-prompts user

### Implementation for User Story 2

- [ ] T013 [P] [US2] Create unit test file tests/unit/test_todo_manager_create.py with tests for TodoManager.create_task() success cases and empty title validation
- [ ] T014 [P] [US2] Create unit test file tests/unit/test_todo_manager_id_generation.py testing auto-increment starting at 1 with multiple sequential creates
- [ ] T015 [US2] Implement menu option 2 (Add Todo) in src/todo_app/main.py: prompt for title/description, validate title non-empty (re-prompt if empty), call manager.create_task(), display success message with ID
- [ ] T016 [US2] Add integration test tests/integration/test_add_todos.py: add single todo, verify in list; add multiple todos, verify IDs increment correctly

**Checkpoint**: User Stories 1 AND 2 complete and both independently testable

**MVP Enhancement**: Story 1 + 2 = Users can view empty list and add todos

---

## Phase 5: User Story 3 - Mark Todo Complete (Priority: P2)

**Goal**: Users can toggle todo status (complete ↔ incomplete) using todo ID; status changes immediately reflected in list display

**Independent Test**: Add todo → mark complete (verify ☑) → mark incomplete (verify ☐) → view list and confirm status persisted

**Acceptance Criteria** (from spec.md):
1. Prompt for todo ID
2. Toggle status: incomplete → complete (☑), complete → incomplete (☐)
3. Status change immediately visible in list
4. Error message if ID not found

### Implementation for User Story 3

- [ ] T017 [P] [US3] Create unit test file tests/unit/test_todo_manager_mark_complete.py testing mark_complete() success, toggle behavior, and invalid ID error
- [ ] T018 [US3] Implement menu option 4 (Mark Complete/Incomplete) in src/todo_app/main.py: prompt for ID, validate numeric, call manager.mark_complete(), display success or error message
- [ ] T019 [US3] Add integration test tests/integration/test_mark_complete.py: add todo, mark complete, view list verify ☑, mark incomplete, view list verify ☐

**Checkpoint**: User Stories 1, 2, AND 3 complete

---

## Phase 6: User Story 4 - Update Todo (Priority: P2)

**Goal**: Users can modify existing todo's title and/or description independently; changes persist immediately in list

**Independent Test**: Add todo → update only title → verify title changed, description unchanged → update only description → verify both correct

**Acceptance Criteria** (from spec.md):
1. Prompt for todo ID
2. Prompt for new title (blank = keep current)
3. Prompt for new description (blank = keep current)
4. At least one field must be non-empty
5. Error if ID not found

### Implementation for User Story 4

- [ ] T020 [P] [US4] Create unit test file tests/unit/test_todo_manager_update.py testing update_task() with partial updates (title only, description only, both), field independence, and invalid ID error
- [ ] T021 [US4] Implement menu option 3 (Update Todo) in src/todo_app/main.py: prompt for ID, prompt for new title (accept blank = no change), prompt for new description (accept blank = no change), validate at least one change requested, call manager.update_task(), display success or error
- [ ] T022 [US4] Add integration test tests/integration/test_update_todos.py: add todo, update title only verify description unchanged, update description only verify title unchanged, update both

**Checkpoint**: User Stories 1, 2, 3, AND 4 complete

---

## Phase 7: User Story 5 - Delete Todo (Priority: P3)

**Goal**: Users can permanently remove todos with confirmation prompt to prevent accidental deletion

**Independent Test**: Add todo → delete → confirm → verify removed from list; repeat with cancellation → verify todo persists

**Acceptance Criteria** (from spec.md):
1. Prompt for todo ID
2. Display confirmation prompt "Are you sure? (yes/no)"
3. Delete only on "yes" or "y" (case-insensitive)
4. Cancel on "no" or "n"
5. Error if ID not found

### Implementation for User Story 5

- [ ] T023 [P] [US5] Create unit test file tests/unit/test_todo_manager_delete.py testing delete_task() success, return values, invalid ID error
- [ ] T024 [US5] Implement menu option 5 (Delete Todo) in src/todo_app/main.py: prompt for ID, display confirmation "Are you sure? (yes/no):", accept "yes"/"y" for confirm (case-insensitive) or "no"/"n" for cancel, call manager.delete_task() on confirm, display success or error, display cancel message
- [ ] T025 [US5] Add integration test tests/integration/test_delete_todos.py: add todo, delete with confirm, verify removed; add todo, delete and cancel, verify persists

**Checkpoint**: All 5 user stories complete and independently testable

---

## Phase 8: Menu & Navigation

**Purpose**: Complete main menu and user interaction loop

- [ ] T026 [US1] Add menu display logic to main loop showing all 6 options ([1] View, [2] Add, [3] Update, [4] Mark, [5] Delete, [6] Exit)
- [ ] T027 Implement menu selection routing: map 1-6 to appropriate operations
- [ ] T028 Implement menu option 6 (Exit): display "Goodbye!" and exit gracefully
- [ ] T029 Add invalid menu selection handling: display "Invalid choice. Please try again" and re-prompt
- [ ] T030 Add error handling for non-numeric menu input with user-friendly message

**Checkpoint**: Complete menu system functional

---

## Phase 9: Edge Cases & Error Handling

**Purpose**: Handle boundary conditions and user errors gracefully

- [ ] T031 [P] Handle non-numeric ID input: display "Invalid ID format. Please enter a number." and re-prompt
- [ ] T032 [P] Handle non-existent todo ID (update/delete/mark): display "Todo not found. Please try again." and re-prompt
- [ ] T033 Handle very long titles: accept input up to 500 chars, truncate display to 60 chars with ellipsis
- [ ] T034 Handle empty title input during add: display "Title cannot be empty. Please try again." and re-prompt for title
- [ ] T035 Handle special characters and Unicode in titles/descriptions: accept and display as-is (no filtering)
- [ ] T036 Handle KeyboardInterrupt (Ctrl+C) gracefully: display "Goodbye!" and exit cleanly

**Checkpoint**: All edge cases handled with user-friendly error messages

---

## Phase 10: Integration & End-to-End Testing

**Purpose**: Validate complete user workflows across all features

- [ ] T037 Create comprehensive integration test tests/integration/test_full_workflow.py: add 3 todos, view list, update one, mark one complete, delete one, view final list, verify all changes
- [ ] T038 Create contract test tests/contract/test_cli_interface.py validating exact menu format, prompt format, and output format against spec
- [ ] T039 Add performance test tests/integration/test_performance.py: add 100 todos, verify operations complete in <100ms each

**Checkpoint**: Full integration validated

---

## Phase 11: Polish & Final Verification

**Purpose**: Code quality, documentation, and final testing

- [ ] T040 [P] Add docstrings to all functions (Task, TodoManager, CLI Handler, main)
- [ ] T041 [P] Add inline comments for complex logic (ID generation, list search, status toggle)
- [ ] T042 Run full test suite: `uv run pytest` - verify all tests pass
- [ ] T043 Code review checklist: verify clean code principles (single responsibility, no nesting, clear naming)
- [ ] T044 Manual acceptance testing: execute all 5 user stories manually, verify against spec acceptance criteria
- [ ] T045 Verify no data persistence (confirm todos lost on app exit per in-memory design)

**Checkpoint**: Code ready for production

---

## Implementation Strategy

### MVP Scope (Phase 1-3)

**Deliver First**: User Stories 1 & 2 (View & Add)
- Minimum viable product: users can add todos and see them
- Represents ~40% of implementation effort
- Validates architecture and user interaction model

### Incremental Delivery (Phase 4-7)

**Deliver Second**: User Stories 3, 4, 5 (Mark, Update, Delete)
- Full CRUD functionality
- Represents ~60% of implementation effort
- Each story independently testable and deployable

### Parallel Execution Opportunities

**Can Run in Parallel**:
- T005 Task model + T006 TodoManager (different files, no dependencies)
- T009-T010 Tests + T011-T012 Implementation (tests first, then implementation)
- US3, US4, US5 stories can all be implemented in parallel after Foundation complete (T005-T008)
- T031-T036 Edge case handling can be implemented in parallel

**Sequential Requirements**:
- T001-T004 (Setup) must complete before anything else
- T005-T008 (Foundation) must complete before any user story
- Within each story: tests should be written before implementation
- T026-T030 (Menu) coordinates all user story routes

---

## Dependency Graph

```
T001-T004 (Setup)
    ↓
T005-T008 (Foundation)
    ↓
┌─────────────────────────────────────┐
│ User Story 1-5 Parallel             │
├─────────────────────────────────────┤
│ T009-T012 (US1: View & Add tests)  │ ← Blocks T026-T030 (Menu)
│ T013-T016 (US2: Add CRUD logic)     │
│ T017-T019 (US3: Mark Complete)      │
│ T020-T022 (US4: Update)             │
│ T023-T025 (US5: Delete)             │
└─────────────────────────────────────┘
    ↓
T026-T030 (Menu & Navigation)
    ↓
T031-T036 (Edge Cases)
    ↓
T037-T039 (Integration & Performance)
    ↓
T040-T045 (Polish & Final)
```

---

## Success Metrics

**All tasks complete** ✅ when:
1. All 45 tasks marked `[x]` complete
2. All unit tests pass: `uv run pytest tests/unit/`
3. All integration tests pass: `uv run pytest tests/integration/`
4. All contract tests pass: `uv run pytest tests/contract/`
5. All 5 user stories work independently (can demo any story alone)
6. Code review checklist: all items verified
7. Manual acceptance testing: all spec scenarios verified
8. Performance: all operations <100ms (verified in T039)

---

## Estimated Effort

| Phase | Tasks | Effort | Notes |
|-------|-------|--------|-------|
| 1. Setup | T001-T004 | 30 min | Project initialization |
| 2. Foundation | T005-T008 | 90 min | Core models and services |
| 3. US1 | T009-T012 | 60 min | MVP: View functionality |
| 4. US2 | T013-T016 | 60 min | MVP: Add functionality |
| 5. US3 | T017-T019 | 45 min | Mark Complete |
| 6. US4 | T020-T022 | 45 min | Update functionality |
| 7. US5 | T023-T025 | 45 min | Delete functionality |
| 8. Menu | T026-T030 | 30 min | Menu system |
| 9. Edge Cases | T031-T036 | 60 min | Error handling |
| 10. Integration | T037-T039 | 45 min | End-to-end testing |
| 11. Polish | T040-T045 | 45 min | Documentation & final |
| **TOTAL** | **45 tasks** | **~550 min** | **~9-10 hours** |

---

## Task Tracking

Use this checklist to track progress. Each task ID maps to:
- Specification requirement: See spec.md user story
- Plan component: See plan.md architecture and quickstart.md
- Code location: Exact file path in description
- Tests: Related unit/integration/contract tests

All tasks follow constitutional requirements:
- ✅ Python 3.13+ with uv
- ✅ In-memory storage only
- ✅ Clean code (functions, single responsibility)
- ✅ Task-ID tracing (each task maps back to this document)
- ✅ Performance measured (sub-100ms targets)
