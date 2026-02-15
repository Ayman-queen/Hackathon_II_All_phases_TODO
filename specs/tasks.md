# Tasks: Chatbot Enhancements

**Input**: Design documents from `/specs/001-chatbot-enhancements/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify project initialization and basic structure.

- [X] T001 Verify project structure per implementation plan in `specs/001-chatbot-enhancements/plan.md`.
- [X] T002 Verify language and framework dependencies are installed for both `backend` and `frontend`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

- [X] T003 [P] Implement rate limiting middleware in `backend/app/core/security.py`.
- [X] T004 [P] Configure structured logging in `backend/app/core/config.py`.
- [X] T005 [P] Add basic API metrics for request/response rates and latencies.

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Robust Task Creation (Priority: P1) 🎯 MVP

**Goal**: The chatbot should check for similar tasks before creating a new one to prevent duplicates.

**Independent Test**: Attempt to create a task with a title similar to an existing task. The system should provide feedback instead of creating a new task.

### Implementation for User Story 1

- [X] T006 [US1] Update the `create_task` endpoint in `backend/app/api/endpoints/tasks.py` to include duplicate validation logic.
- [X] T007 [US1] Modify the `chat_agent` in `backend/app/agents/chat_agent.py` to handle the feedback from the duplicate validation.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Correct Welcome Message (Priority: P1)

**Goal**: The chatbot should display the correct task values in the welcome message.

**Independent Test**: Create/delete tasks and then reload the page to check if the welcome message reflects the changes.

### Implementation for User Story 2

- [X] T008 [US2] Implement the `get_user_stats` endpoint in `backend/app/api/endpoints/users.py`.
- [X] T009 [US2] Update the frontend dashboard page in `frontend/app/dashboard/page.tsx` to call the `get_user_stats` endpoint and display the correct task count in the welcome message.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: User Story 3 - Proper Session Handling (Priority: P2)

**Goal**: The application should correctly handle user sessions, so users don't have to log in repeatedly.

**Independent Test**: Log in, close the browser tab, reopen it, and check if the user is still logged in.

### Implementation for User Story 3

- [ ] T010 [US3] Implement session persistence logic in `frontend/lib/auth-client.ts`.
- [ ] T011 [US3] Update the backend authentication logic in `backend/app/core/security.py` to handle session expiration and re-authentication.

**Checkpoint**: All user stories should now be independently functional.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories.

- [ ] T012 [P] Create a documented recovery plan for the service.
- [ ] T013 [P] Review and update all relevant documentation.
- [ ] T014 Run quickstart.md validation from `specs/001-chatbot-enhancements/quickstart.md`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Foundational phase completion.
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2).
- **User Story 2 (P1)**: Can start after Foundational (Phase 2).
- **User Story 3 (P2)**: Can start after Foundational (Phase 2).

### Parallel Opportunities

- All Foundational tasks marked [P] can run in parallel.
- Once Foundational phase completes, all user stories can start in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 & 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Complete Phase 4: User Story 2
5. **STOP and VALIDATE**: Test User Stories 1 & 2 independently.

### Incremental Delivery

1. Complete Setup + Foundational.
2. Add User Story 1 & 2 → Test independently → Deploy/Demo (MVP!).
3. Add User Story 3 → Test independently → Deploy/Demo.
