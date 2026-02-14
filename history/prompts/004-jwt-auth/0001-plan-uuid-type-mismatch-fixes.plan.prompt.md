---
id: 0001
title: Plan UUID type mismatch fixes
stage: plan
date: 2026-01-02
surface: agent
model: claude-haiku-4-5-20251001
feature: 004-jwt-auth
branch: 004-jwt-auth
user: claude
command: /sp.plan
labels: ["type-system", "better-auth", "uuid-fix", "critical-fix", "spec-driven-development"]
links:
  spec: specs/004-jwt-auth/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/004-jwt-auth/plan.md
  - specs/004-jwt-auth/spec.md
tests:
  - Run Phase 3 integration tests after implementation
  - pytest tests/test_api/test_todos.py -v
  - Manual curl test with JWT token
---

## Prompt

User input: "ok now create a plan for the fixes to apply all the fixes"

Context: User had requested `/sp.analyze` to identify specification gaps related to UUID/string type mismatch error in backend. The analyze command identified 4 critical issues and 4 high-severity issues related to Better Auth user_id type mismatch.

Task: Create comprehensive implementation plan to fix all UUID type mismatches in backend models, schemas, and database, aligning with Constitution requirements and Better Auth integration.

## Response snapshot

Created comprehensive 4-phase implementation plan in specs/004-jwt-auth/plan.md:

**Phase 0: Pre-Implementation (MCP Consultation)**
- Query Better Auth MCP to confirm user_id format is string
- Document findings
- Gate: Cannot proceed without MCP confirmation

**Phase 1: Model & Schema Refactoring**
- Update 6 Python files: user.py, todo.py (models), todo.py (schemas), deps.py (API), todos.py (endpoints)
- Change all `user_id: UUID` → `user_id: str`
- Remove UUID imports where unused

**Phase 2: Database Migration**
- ALTER TABLE todos ALTER COLUMN user_id TYPE VARCHAR(255)
- Verify foreign key constraints remain intact

**Phase 3: Integration Testing**
- Run unit tests for models and schemas
- Run integration tests for API endpoints
- Manual curl testing with actual JWT tokens

**Phase 4: Documentation Update**
- Update spec.md and plan.md with Better Auth user_id format documentation
- Update API contracts

All phases include detailed validation steps and success criteria.

## Outcome

- ✅ Impact: Complete implementation roadmap created; blocks all remaining work until executed. Resolves CRITICAL Constitution violation (type safety principle).
- 🧪 Tests: 3 test phases defined (unit, integration, manual). All endpoints must pass with zero ValidationError.
- 📁 Files: 1 plan file created/updated (plan.md); 6 additional files to be modified during Phase 1-2.
- 🔁 Next prompts: User should execute `/sp.implement` to start Phase 0 (MCP consultation), then proceed through Phases 1-4 in sequence.
- 🧠 Reflection: Plan follows Constitution Principle IV (task-driven). Phase 0 ensures MCP consultation per Constitution Principle VII. Minimal scope (6 files) reduces complexity and risk. Database migration is backward-compatible (string can represent UUID data).

## Evaluation notes (flywheel)

- Failure modes observed: None during planning. Potential failure in Phase 2 if database connection fails or foreign keys break (mitigated by verification queries).
- Graders run and results (PASS/FAIL): Constitution Check: PASS (with MCP prerequisite). Technical Context: COMPLETE. All gates cleared.
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Start with Phase 1.1 (update user.py) as proof-of-concept. If successful, continue with remaining Phase 1 files. Then execute Phase 2 migration.
