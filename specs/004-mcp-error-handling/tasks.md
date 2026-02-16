# Tasks: MCP Server Error Handling & Validation Fix

**Input**: Design documents from `/specs/004-mcp-error-handling/`
**Prerequisites**: plan.md (✓), spec.md (✓), research.md (✓), data-model.md (✓), contracts/ (✓)

**Tests**: Unit tests requested in plan.md Phase 6 - included as Phase 7

**Organization**: Tasks organized by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US5)
- Include exact file paths in descriptions

## Path Conventions

- **Project Type**: Web application (backend focus)
- **Primary File**: `backend/mcp_server/server.py`
- **Test File**: `backend/tests/test_mcp_server.py`

---

## Phase 1: Setup (Verify Environment)

**Purpose**: Ensure development environment is ready

- [ ] T001 Verify MCP server can start without errors: `cd backend && python -m mcp_server.server`
- [ ] T002 Verify current error by calling add_task tool via curl to `/mcp` endpoint
- [ ] T003 [P] Create backup of `backend/mcp_server/server.py` before modifications

**Checkpoint**: Environment verified, baseline error confirmed

---

## Phase 2: Foundational (Critical Fix - TextContent Type Parameter)

**Purpose**: Fix the root cause that BLOCKS all user stories - adding `type="text"` to all TextContent instances

**⚠️ CRITICAL**: This phase fixes the Pydantic ValidationError. All user stories are blocked until complete.

### FR-001 Implementation (10 TextContent Fixes)

- [x] T004 Fix TextContent at line 112 (`get_user_stats`): add `type="text"` in `backend/mcp_server/server.py`
- [x] T005 [P] Fix TextContent at line 123 (`add_task` success): add `type="text"` in `backend/mcp_server/server.py`
- [x] T006 [P] Fix TextContent at line 128 (`list_tasks` empty): add `type="text"` in `backend/mcp_server/server.py`
- [x] T007 [P] Fix TextContent at line 130 (`list_tasks` with tasks): add `type="text"` in `backend/mcp_server/server.py`
- [x] T008 [P] Fix TextContent at line 147 (`update_task` success): add `type="text"` in `backend/mcp_server/server.py`
- [x] T009 [P] Fix TextContent at line 148 (`update_task` not found): add `type="text"` in `backend/mcp_server/server.py`
- [x] T010 [P] Fix TextContent at line 158 (`delete_task` success): add `type="text"` in `backend/mcp_server/server.py`
- [x] T011 [P] Fix TextContent at line 159 (`delete_task` not found): add `type="text"` in `backend/mcp_server/server.py`
- [x] T012 [P] Fix TextContent at line 171 (`complete_task` success): add `type="text"` in `backend/mcp_server/server.py`
- [x] T013 [P] Fix TextContent at line 172 (`complete_task` not found): add `type="text"` in `backend/mcp_server/server.py`

### Verification

- [x] T014 Restart MCP server and verify no Pydantic ValidationError in logs
- [x] T015 Test `tools/call` endpoint with add_task - verify successful response

**Checkpoint**: Root cause fixed - MCP tools now return valid responses (SC-002, SC-006, SC-007 met)

---

## Phase 3: User Story 1 - Task Creation via Chat (Priority: P1) 🎯 MVP

**Goal**: Users can create tasks via chat without 500 errors or timeouts

**Independent Test**: Send "Add a task called test" via chat API and verify response + database entry

**Acceptance Criteria (from spec.md)**:
- Confirmation message returned within 10 seconds
- Task appears in database with correct title and user_id
- Both title and description are saved correctly

### Implementation for User Story 1

- [x] T016 [US1] Add `create_text_response()` helper function after imports in `backend/mcp_server/server.py`
- [x] T017 [US1] Refactor `add_task` tool to use `create_text_response()` helper in `backend/mcp_server/server.py`
- [x] T018 [US1] Add `validate_required_args()` helper function in `backend/mcp_server/server.py`
- [x] T019 [US1] Update `add_task` to use `validate_required_args(["title"], "add_task")` in `backend/mcp_server/server.py`
- [ ] T020 [US1] Verify add_task works via chat API: POST to `/api/chat` with task creation message

**Checkpoint**: Task creation via chat now works - MVP complete (SC-001 met)

---

## Phase 4: User Story 2 - Graceful Error Handling (Priority: P1)

**Goal**: Errors return user-friendly messages instead of 500 errors

**Independent Test**: Send invalid request (missing user_id) and verify structured error response

**Acceptance Criteria (from spec.md)**:
- Invalid arguments return structured error with clear message
- Database errors are logged with context
- Users never see stack traces

### Implementation for User Story 2

- [x] T021 [US2] Add `create_error_response()` helper function in `backend/mcp_server/server.py`
- [x] T022 [US2] Update `tools/call` handler to wrap execution in try-except in `backend/mcp_server/server.py`
- [x] T023 [US2] Add ValueError catch for validation errors returning -32602 in `backend/mcp_server/server.py`
- [x] T024 [US2] Add generic Exception catch returning -32603 "Internal server error" in `backend/mcp_server/server.py`
- [x] T025 [US2] Add tool name validation - return error if missing in `backend/mcp_server/server.py`
- [ ] T026 [US2] Verify error handling: send request with missing user_id, verify JSON-RPC error response

**Checkpoint**: All errors return structured responses (SC-003, SC-004 met)

---

## Phase 5: User Story 3 - Task Listing and Stats (Priority: P2)

**Goal**: Users can view task stats and list via chat

**Independent Test**: Request task stats and verify formatted response

**Acceptance Criteria (from spec.md)**:
- Stats show "Pending tasks: X, Completed tasks: Y"
- Empty list shows "No tasks found."
- Task list shows title, ID, completion status

### Implementation for User Story 3

- [x] T027 [US3] Refactor `get_user_stats` tool to use `create_text_response()` in `backend/mcp_server/server.py`
- [x] T028 [US3] Refactor `list_tasks` tool (empty case) to use `create_text_response()` in `backend/mcp_server/server.py`
- [x] T029 [US3] Refactor `list_tasks` tool (with tasks) to use `create_text_response()` in `backend/mcp_server/server.py`
- [ ] T030 [US3] Verify stats via curl: call get_user_stats tool

**Checkpoint**: Stats and list tools work correctly

---

## Phase 6: User Story 4 - Task Operations (Priority: P2)

**Goal**: Users can update, delete, and complete tasks via chat

**Independent Test**: Create task, mark complete, verify is_complete=True in database

**Acceptance Criteria (from spec.md)**:
- Complete sets is_complete to True
- Delete removes task from database
- Update changes title successfully
- Non-existent ID returns "Task with ID 'xxx' not found."

### Implementation for User Story 4

- [x] T031 [US4] Add `parse_uuid_safe()` helper function in `backend/mcp_server/server.py`
- [x] T032 [US4] Refactor `update_task` tool: use helpers + validate args in `backend/mcp_server/server.py`
- [x] T033 [US4] Refactor `delete_task` tool: use helpers + validate args in `backend/mcp_server/server.py`
- [x] T034 [US4] Refactor `complete_task` tool: use helpers + validate args in `backend/mcp_server/server.py`
- [x] T035 [US4] Handle invalid UUID format with user-friendly error message in `backend/mcp_server/server.py`
- [ ] T036 [US4] Verify update/delete/complete via curl: test each operation

**Checkpoint**: All task operations work with proper validation

---

## Phase 7: User Story 5 - Error Logging and Diagnostics (Priority: P3)

**Goal**: Admins can diagnose issues from logs

**Independent Test**: Trigger error, check logs contain timestamp, tool name, error type

**Acceptance Criteria (from spec.md)**:
- Logs contain timestamp, method name, error type, message
- Tool failures log tool name and sanitized arguments
- No sensitive data in logs (user_id logged as boolean presence)

### Implementation for User Story 5

- [x] T037 [US5] Add structured request logging at start of `handle_mcp_request()` in `backend/mcp_server/server.py`
- [x] T038 [US5] Add success logging after tool execution in `backend/mcp_server/server.py`
- [x] T039 [US5] Ensure error logging includes tool name and error type in `backend/mcp_server/server.py`
- [x] T040 [US5] Sanitize logs: log `has_user_id: bool` not actual user_id in `backend/mcp_server/server.py`
- [ ] T041 [US5] Verify logging: trigger error and check log output format

**Checkpoint**: Logs provide sufficient diagnostic information (SC-005 met)

---

## Phase 8: Unit Tests

**Purpose**: Automated verification of all fixes

**New File**: `backend/tests/test_mcp_server.py`

### Test Implementation

- [x] T042 [P] Create test file structure with pytest imports in `backend/tests/test_mcp_server.py`
- [x] T043 [P] Add `test_text_content_has_type_field` - verify responses include type="text" in `backend/tests/test_mcp_server.py`
- [x] T044 [P] Add `test_add_task_success` - valid task creation in `backend/tests/test_mcp_server.py`
- [x] T045 [P] Add `test_add_task_missing_title` - returns -32602 error in `backend/tests/test_mcp_server.py`
- [x] T046 [P] Add `test_add_task_missing_user_id` - returns -32602 error in `backend/tests/test_mcp_server.py`
- [x] T047 [P] Add `test_update_task_invalid_uuid` - returns -32602 error in `backend/tests/test_mcp_server.py`
- [x] T048 [P] Add `test_unknown_tool` - returns ValueError in `backend/tests/test_mcp_server.py`
- [x] T049 [P] Add `test_handle_mcp_request_unknown_method` - returns -32601 in `backend/tests/test_mcp_server.py`
- [ ] T050 Run all tests: `cd backend && pytest tests/test_mcp_server.py -v`

**Checkpoint**: All tests pass

---

## Phase 9: Polish & Integration Verification

**Purpose**: Final verification and cleanup

- [ ] T051 Run full integration test: start both servers, test chat API end-to-end
- [x] T052 Verify all 10 TextContent instances have type="text" (grep/audit)
- [ ] T053 Verify no Pydantic ValidationError in logs during integration test
- [x] T054 Update verification checklist in plan.md - mark all items complete
- [ ] T055 Run quickstart.md validation steps
- [ ] T056 Commit all changes with descriptive message referencing feature 004

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Setup) → Phase 2 (Foundational/Critical Fix) → All User Stories
                                     ↓
                    ┌────────────────┴────────────────┐
                    ↓                                  ↓
            Phase 3 (US1: MVP)              Phase 4 (US2: Error Handling)
                    ↓                                  ↓
            Phase 5 (US3: Stats)            Phase 6 (US4: Operations)
                    ↓                                  ↓
                    └────────────────┬────────────────┘
                                     ↓
                            Phase 7 (US5: Logging)
                                     ↓
                            Phase 8 (Unit Tests)
                                     ↓
                            Phase 9 (Polish)
```

### User Story Dependencies

- **US1 (Task Creation)**: Depends on Phase 2 only - MVP, can ship independently
- **US2 (Error Handling)**: Depends on Phase 2 only - enhances all tools
- **US3 (Stats/List)**: Depends on Phase 2 only - independent
- **US4 (Operations)**: Depends on Phase 2 only - independent
- **US5 (Logging)**: Depends on US2 - enhances error handling

### Critical Path (Minimum Viable Fix)

```
T001 → T004-T015 → T020 (verify)
```

This path alone fixes the blocking bug and enables task creation.

### Parallel Opportunities

**Phase 2 (after T004)**:
```bash
# All TextContent fixes can run in parallel:
T005, T006, T007, T008, T009, T010, T011, T012, T013
```

**After Phase 2 Complete**:
```bash
# US1, US2, US3, US4 can proceed in parallel:
US1: T016-T020
US2: T021-T026
US3: T027-T030
US4: T031-T036
```

**Phase 8 (Tests)**:
```bash
# All test tasks can run in parallel:
T042, T043, T044, T045, T046, T047, T048, T049
```

---

## Implementation Strategy

### MVP First (Minimum to Unblock Users)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational Fix (T004-T015) - **CRITICAL**
3. Partial Phase 3: Verify add_task works (T020)
4. **STOP and VALIDATE**: Test chat API - task creation should work
5. Deploy hotfix if critical

### Full Implementation

1. Setup → Foundational Fix → **MVP Validated**
2. Complete US1 (helper functions for add_task)
3. Add US2 (error handling) - makes system robust
4. Add US3 + US4 (remaining tools) - complete functionality
5. Add US5 (logging) - operational excellence
6. Add Tests (Phase 8) - regression prevention
7. Polish + Integration verification

### Task Count Summary

| Phase | Tasks | Parallel |
|-------|-------|----------|
| Phase 1: Setup | 3 | 1 |
| Phase 2: Foundational | 12 | 9 |
| Phase 3: US1 | 5 | 0 |
| Phase 4: US2 | 6 | 0 |
| Phase 5: US3 | 4 | 0 |
| Phase 6: US4 | 6 | 0 |
| Phase 7: US5 | 5 | 0 |
| Phase 8: Tests | 9 | 8 |
| Phase 9: Polish | 6 | 0 |
| **Total** | **56** | **18** |

---

## Notes

- [P] tasks = different files or independent changes, no dependencies
- [US#] label maps task to specific user story for traceability
- Critical path (T001-T015, T020) unblocks users immediately
- Each user story should be independently completable and testable
- Commit after each phase or logical group
- All tasks reference `backend/mcp_server/server.py` as PRIMARY FILE
