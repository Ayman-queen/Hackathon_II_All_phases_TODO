---
description: "Task list template for feature implementation"
---

# Tasks: Phase III Chat Interface

**Input**: Design documents from `/specs/phase3-chat/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/
**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Install MCP Python SDK and OpenAI Agents SDK in backend/pyproject.toml
- [ ] T002 [P] Create backend/mcp directory structure per plan.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T003 Implement Neon DB migrations for conversations and messages tables in backend/migrate_db.py
- [ ] T004 Create MCP Server service in backend/mcp/__init__.py with basic setup

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Access Chat and Receive Greeting (Priority: P1) 🎯 MVP

**Goal**: Personalized greeting with stats on dashboard load

**Independent Test**: Load dashboard; greeting shows accurate stats scoped to user

### Implementation for User Story 1

- [ ] T005 [P] [US1] Add get_user_stats tool in backend/mcp/tools/stats.py
- [ ] T006 [US1] Implement proactive greet logic in frontend/app/dashboard/chat/page.tsx using session context
- [ ] T007 [US1] Wire greeting to trigger on dashboard load in frontend/app/dashboard/layout.tsx

**Checkpoint**: User Story 1 fully functional independently

---

## Phase 4: User Story 2 - Perform Natural Language CRUD Operations (Priority: P2)

**Goal**: Natural language todo CRUD via agent

**Independent Test**: Send CRUD phrases; agent processes, updates DB, responds correctly

### Implementation for User Story 2

- [ ] T008 [P] [US2] Create CRUD tools (add/list/update/delete/complete) in backend/mcp/tools/todo_tools.py
- [ ] T009 [US2] Implement Backend Chat logic: windowed memory, summarization trigger, JWT verification in backend/app/api/chat.py
- [ ] T010 [US2] Setup OpenAI Agents Runner with MCP tools and 5-msg trigger in backend/app/agents/chat_agent.py

**Checkpoint**: User Stories 1 AND 2 work independently

---

## Phase 5: User Story 3 - Experience Responsive Chat UI (Priority: P3)

**Goal**: Smooth formatted chat interface

**Independent Test**: Send messages; auto-scrolls, bubbles distinct, responsive on mobile

### Implementation for User Story 3

- [ ] T011 [P] [US3] Build Chat UI with Shadcn ScrollArea in frontend/app/dashboard/chat/page.tsx
- [ ] T012 [US3] Add fetch wrapper sending Better Auth JWT in frontend/lib/hooks/useChat.ts
- [ ] T013 [US3] Ensure Light/Dark mode and responsiveness in frontend/app/dashboard/chat/page.tsx

**Checkpoint**: All user stories independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements affecting multiple stories

- [ ] T014 [P] Add error handling and loading states across chat UI files
- [ ] T015 Documentation updates in specs/phase3-chat/quickstart.md
- [ ] T016 Run quickstart.md validation for end-to-end chat flow

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phase 3+)**: Depend on Foundational
- **Polish (Final)**: Depends on all stories

### User Story Dependencies

- **US1 (P1)**: After Foundational
- **US2 (P2)**: After Foundational (uses stats tool)
- **US3 (P3)**: After US1 (chat page)

### Parallel Opportunities

- T001-T002 [P]
- T005 [P], T006-T007 sequential
- T008 [P], T009-T010 sequential
- T011 [P], T012-T013 sequential

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1-2
2. Complete Phase 3 (US1)
3. **VALIDATE**: Greeting works
4. Deploy/demo MVP

### Incremental Delivery

1. Phase 1-2 → Foundation
2. +US1 → MVP greeting
3. +US2 → Full CRUD agent
4. +US3 → Polished UI
5. Polish → Production ready

**Total tasks**: 16 | **US1**: 3 | **US2**: 3 | **US3**: 3 | **Parallel**: 4
