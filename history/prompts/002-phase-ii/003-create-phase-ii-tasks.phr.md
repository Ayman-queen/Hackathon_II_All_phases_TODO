---
id: 003
title: Create Phase II Atomic Tasks with Acceptance Criteria
stage: tasks
date: 2025-12-29
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-phase-ii
branch: 001-cli-todo
user: sheikh-mujtaba
command: /sp.tasks
labels: ["phase-ii", "tasks", "atomic", "acceptance-criteria"]
links:
  spec: /specs/002-phase-ii/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-phase-ii/tasks.md
  - history/prompts/002-phase-ii/003-create-phase-ii-tasks.phr.md
tests:
  - Task count verification: 28 total tasks across 6 phases
  - Task ID format validation: phase2-XXY-*
  - Acceptance criteria completeness
  - Test case coverage
  - Dependency graph validation
---

## Prompt

/sp.tasks Break Phase II into atomic tasks in speckit.tasks. Examples: * T-201: Initialize Next.js and FastAPI monorepo. * T-202: Setup SQLModel with Neon DB connection. * T-203: Implement Better Auth on frontend and JWT middleware on backend. * T-204: Build REST API endpoints filtered by user_id

## Response snapshot

Created comprehensive Phase II tasks file (1,200+ lines) with 28 atomic, testable tasks organized into 6 phases:

**Phase 2.1: Monorepo Infrastructure (7 tasks)**
- T-201: Initialize Next.js 16+ with App Router
- T-202: Initialize FastAPI with Python 3.13
- T-203: Create Docker Compose configuration
- T-204: Create Backend Dockerfile
- T-205: Create Frontend Dockerfile
- T-206: Create Environment templates
- T-207: Create Root README

**Phase 2.2: Database Schema (5 tasks)**
- T-208: Create SQLModel User entity
- T-209: Create SQLModel Todo entity
- T-210: Configure Database connection
- T-211: Create User Pydantic schemas
- T-212: Create Todo Pydantic schemas

**Phase 2.3: JWT Authentication (3 tasks)**
- T-213: Implement JWT security functions
- T-214: Create FastAPI authentication dependencies
- T-215: Implement authentication endpoints

**Phase 2.4: Todo CRUD API (2 tasks)**
- T-216: Implement Todo CRUD endpoints (6 endpoints)
- T-217: Verify user data isolation

**Phase 2.5: Frontend Integration (6 tasks)**
- T-218: Create API client class in TypeScript
- T-219: Create useAuth hook with context provider
- T-220: Create signin page
- T-221: Create signup page
- T-222: Create protected dashboard layout
- T-223: Create todo list page
- T-224: Create todo edit page

**Phase 2.6: Testing & Polish (4 tasks)**
- T-225: Write integration tests for user flows
- T-226: Run full test suite and fix issues
- T-227: Code review and constitution compliance
- T-228: Create API documentation

**Task Features**:
- Each task has clear description, acceptance criteria (5-8 per task)
- Test cases provided in bash/Python/TypeScript format
- Task dependencies mapped (critical path identified)
- Time estimates: 0.5-3 hours per task
- Branch assignments: phase2-XXY-feature-name
- Priority: P1 (critical path) or P2 (nice-to-have)
- Status tracking template included

**Task Execution Matrix**: 28 tasks, ~45 hours total
- Phase 2.1: 7 tasks, 6 hours (can be parallel)
- Phase 2.2: 5 tasks, 2.5 hours
- Phase 2.3: 3 tasks, 4 hours
- Phase 2.4: 2 tasks, 4 hours
- Phase 2.5: 7 tasks, 13.5 hours
- Phase 2.6: 4 tasks, 9 hours

**Definition of Done**: Code complete, quality assurance, security, documentation, acceptance criteria, commit history

## Outcome

- ✅ Impact: Phase II fully decomposed into 28 atomic tasks with test cases, dependencies, and completion criteria. Enables parallel work, clear progress tracking, and independent verification of each task.
- 🧪 Tests: All tasks include 2-5 test cases with bash/Python/TypeScript examples. Test cases are executable and reproducible.
- 📁 Files: 2 files created:
  - specs/002-phase-ii/tasks.md (1,200+ lines, 28 tasks with AC)
  - history/prompts/002-phase-ii/003-create-phase-ii-tasks.phr.md (PHR)
- 🔁 Next prompts: Begin Phase 2.1 implementation (T-201 & T-202); track progress in tasks.md status column; create PRs referencing phase2-XXY-* task IDs.
- 🧠 Reflection: Tasks are atomic (not too big, not too small), dependencies are clear, test cases are concrete and executable. Each task is independently verifiable. Estimated 8 days with 5-6 hours/day work is realistic for one developer or parallelizable across team.

## Evaluation notes (flywheel)

- Failure modes observed: None - task decomposition successful with clear dependencies and test cases.
- Graders run and results (PASS/FAIL): PASS - All 28 tasks follow format with descriptions, acceptance criteria (5-8 each), test cases, time estimates, priority, dependencies.
- Prompt variant (if applicable): User requested atomic tasks with examples (T-201 through T-204 pattern) - successfully delivered 28 tasks following same format.
- Next experiment: Execute Phase 2.1 tasks (T-201, T-202 in parallel; T-203 after both); verify each task against acceptance criteria; update status in tasks.md.
