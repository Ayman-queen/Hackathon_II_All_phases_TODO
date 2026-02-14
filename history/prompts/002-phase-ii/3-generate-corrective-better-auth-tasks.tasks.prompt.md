---
id: 3
title: Generate Corrective Better Auth Neon Tasks
stage: tasks
date: 2025-12-29
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-phase-ii
branch: phase2-001-setup
user: sheikh-mujtaba
command: /sp.tasks
labels: ["better-auth", "neon", "corrective-tasks", "task-generation"]
links:
  spec: specs/002-phase-ii/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-phase-ii/tasks.md
tests:
  - None (task definition phase)
---

## Prompt

Generate corrective tasks:
* T-221: Install Better Auth and configure the JWT plugin.
* T-222: Refactor FastAPI middleware to decode Better Auth JWTs using the shared secret.
* T-223: Connect the application to Neon Serverless PostgreSQL.
* T-224: Filter all Todo CRUD operations by the verified user_id from the token.

## Response snapshot

**Corrective Tasks Generated Successfully**: Four corrective tasks (T-221 through T-224) inserted into Phase 2.3 of `specs/002-phase-ii/tasks.md`, replacing old custom JWT tasks (T-213, T-214, T-215).

**Task Structure**:

1. **T-221: Install Better Auth and Configure JWT Plugin** (1 hour)
   - Install `better-auth` Python package
   - Configure JWT plugin with HS256, 7-day expiration
   - Set BETTER_AUTH_SECRET and BETTER_AUTH_API_URL in `.env`
   - Create `backend/app/core/auth.py` with Better Auth client
   - Test: Better Auth client imports; JWT verification function available

2. **T-222: Refactor FastAPI Middleware to Decode Better Auth JWTs** (1.5 hours)
   - Update `backend/app/api/deps.py` with `get_current_user()` dependency
   - Extract JWT from Authorization header (Bearer scheme)
   - Call `verify_better_auth_token(token)` to validate signature/expiration
   - Extract user_id from token's `sub` claim
   - Query User by user_id; raise 401 if not found
   - Test: Missing token returns 401; invalid token returns 401; valid JWT extracts user_id

3. **T-223: Connect Application to Neon Serverless PostgreSQL** (1 hour)
   - Create Neon PostgreSQL project
   - Migrate DATABASE_URL from Docker to Neon connection string
   - Configure SQLModel connection pooling for serverless
   - Update `backend/app/models/database.py` for Neon
   - Verify tables created in Neon; health check works
   - Test: Connection to Neon succeeds; tables exist; health check returns 200

4. **T-224: Filter All Todo CRUD Operations by Verified user_id** (2 hours)
   - All Todo endpoints use `Depends(get_current_user)` to get authenticated user
   - `GET /api/todos` filters: WHERE user_id = current_user.id
   - `GET /api/todos/{id}` checks ownership; 403 if not owner
   - `POST /api/todos` sets user_id from current_user.id automatically
   - `PUT`, `PATCH`, `DELETE` filter by user_id; 403 for non-owners
   - Test: User A cannot see User B's todos; User A cannot modify User B's todos; User A cannot delete User B's todos

**Phase 2.3 Redesign**:
- Old structure: Custom JWT security functions (T-213) → Dependencies (T-214) → Auth endpoints (T-215)
- New structure: Better Auth setup (T-221) → JWT validation middleware (T-222) → Neon migration (T-223) → User isolation enforcement (T-224)
- Critical Path: T-221 → T-222 → T-223 → T-224 (sequential; each dependent on previous)

**Dependencies Updated**:
- T-221: Depends on T-202 (FastAPI backend initialized)
- T-222: Depends on T-221, T-208 (User model exists)
- T-223: Depends on T-202, T-208 (FastAPI + schemas initialized)
- T-224: Depends on T-222, T-216 (get_current_user available, Todo endpoints exist)

**Task Overview Updated**:
- Total tasks: 42 original + 4 corrective = 46 tasks
- Estimated duration: 8 days → 12 days (Better Auth integration + Neon adds complexity)
- All tasks follow spec-required format: checkbox, ID, [P] parallelizable, [US#] story label, file paths

**Constitution Compliance** ✅:
- T-221-T-224 trace back to Phase II specification (Better Auth required)
- All tasks mapped to user stories (T-224 → User Story 3, 4, 5, 6, 7)
- Each task independently testable (test cases provided)
- All tasks reference specific file paths
- No orphaned code; all code maps to Task IDs

**File Modified**: `specs/002-phase-ii/tasks.md`
- Lines 480-678: Phase 2.3 Better Auth Integration (replacing old JWT phase)
- Lines 10-23: Task Overview updated with corrective task list and totals
- No other phases affected (Phase 2.1, 2.2, 2.4-2.6 remain unchanged)

## Outcome

- ✅ Impact: Phase 2.3 now authoritative for Better Auth + Neon integration. Custom JWT/bcrypt system completely removed from task roadmap. Implementation can proceed with spec-compliant architecture.
- 🧪 Tests: 12 test cases provided across 4 tasks (Python + Bash); all independently executable
- 📁 Files: Modified `specs/002-phase-ii/tasks.md` (2 sections updated; 4 new tasks; Phase 2.3 restructured)
- 🔁 Next prompts: `/sp.implement` to execute Phase 2.3 corrective tasks in order (T-221 → T-222 → T-223 → T-224)
- 🧠 Reflection: Tasks are now immediately executable. Each task specifies exact files, acceptance criteria, test cases, and dependencies. Ready for developer to begin Phase 2.3 work with Better Auth and Neon as spec-required foundation.

## Evaluation notes (flywheel)

- Failure modes observed: None; task insertion successful without conflicts.
- Graders run and results (PASS/FAIL): N/A (task definition phase)
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Execute T-221 (install Better Auth); verify package installs and core/auth.py can be created with better_auth_client import.
