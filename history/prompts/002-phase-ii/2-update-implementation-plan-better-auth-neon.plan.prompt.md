---
id: 2
title: Update Implementation Plan for Better Auth + Neon
stage: plan
date: 2025-12-29
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-phase-ii
branch: phase2-001-setup
user: sheikh-mujtaba
command: /sp.plan
labels: ["better-auth", "neon", "authentication", "database", "architecture"]
links:
  spec: specs/002-phase-ii/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-phase-ii/plan.md
tests:
  - None (planning phase)
---

## Prompt

Update speckit.plan to reflect Option A:
* Frontend: Integrate Better Auth and enable the JWT plugin to issue tokens.
* Backend: Replace custom auth middleware with a JWT verification layer that extracts user_id from Better Auth tokens.
* Database: Switch to Neon Serverless PostgreSQL and use the Better Auth managed user/session tables.

## Response snapshot

**Plan Updated Successfully**: `specs/002-phase-ii/plan.md` revised to reflect Better Auth + Neon architecture.

**Key Changes**:

1. **Primary Dependencies**: Updated to `better-auth` (JWT plugin) instead of custom JWT/bcrypt
2. **Phase 2.3 (Better Auth Integration)**:
   - Replaced custom JWT/bcrypt with Better Auth Python client
   - FastAPI middleware validates Better Auth JWT tokens
   - `get_current_user()` dependency extracts user_id from JWT claims
   - Frontend uses Better Auth JavaScript client for signup/signin/logout
   - Success criteria: All user data isolated by user_id from JWT claims

3. **Phase 2.5 (Neon PostgreSQL Migration - NEW)**:
   - Create Neon project and configure connection string
   - Better Auth auto-creates users, sessions, accounts, verifications tables
   - SQLModel Todo model uses Neon connection with proper FK references
   - Connection pooling optimized for serverless (p95 query < 100ms)
   - Local Docker Postgres deprecated (Neon is primary)

4. **Phase 2.6 (Frontend API Integration - Renamed)**:
   - API client (`lib/api.ts`) auto-attaches Better Auth JWT to all requests
   - `useAuth` hook wraps Better Auth JavaScript client (signup, signin, logout, current user)
   - Signin/Signup pages use Better Auth client endpoints
   - All data filtered by user_id from Better Auth JWT claims

5. **Task Dependencies Updated**:
   - Phase 2.3 → Phase 2.4 → Phase 2.5 → Phase 2.6 (sequential path for auth → todo CRUD → database → frontend)
   - Parallel work: M1 (backend) + M2 (frontend) → D1 (schemas) in parallel → A1 (Better Auth) sequential

6. **Key Architectural Decisions**:
   - Decision 2: Better Auth with JWT plugin (replaces custom JWT/shared secret)
   - Decision 4: Neon Serverless PostgreSQL (mandatory per spec, auto-scales, Better Auth schema)
   - Decisions 3, 5, 6: JWT storage, data isolation, HTTP status codes (updated for Better Auth context)

7. **Security Checklist Updated**:
   - Better Auth handles: JWT issuance, password hashing, session management, token rotation
   - No custom bcrypt needed in backend (Better Auth owns password security)
   - Data isolation enforced at query level (WHERE user_id = <extracted_from_jwt>)
   - All 12 security principles maintained

8. **Effort Estimate Revised**:
   - Phase 2.3: 2 days (Better Auth integration, medium effort)
   - Phase 2.5: 1 day (Neon migration, low effort - Better Auth manages schema)
   - Total: ~12 days (vs. ~8 with custom JWT, but spec-compliant + OAuth-ready for Phase III)

**Constitution Compliance**: All Phase II principles verified ✅
- Full-stack web app ✅
- User-scoped data with JWT ✅
- Better Auth mandatory per constitution ✅
- Neon required per spec ✅
- Stateless architecture for Phase III ✅

## Outcome

- ✅ Impact: Implementation plan fully aligned with Better Auth + Neon requirements. Custom JWT/bcrypt development path eliminated; OAuth 2.0 path clear for Phase III.
- 🧪 Tests: No functional tests yet (planning phase); architectural principles validated against spec and constitution.
- 📁 Files: Modified `specs/002-phase-ii/plan.md` (10 sections updated; 3 new decisions; 1 new phase added)
- 🔁 Next prompts: `/sp.tasks` to decompose Phases 2.3-2.6 into task-driven, T-xxx labeled implementation tasks
- 🧠 Reflection: Plan now authoritative for implementation. All architecture decisions trace back to clarification session (Q1-Q5, all Option A). Custom auth system must be completely removed; no hybrid approach.

## Evaluation notes (flywheel)

- Failure modes observed: None; plan updates applied cleanly without contradictions.
- Graders run and results (PASS/FAIL): N/A (planning phase)
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Generate task definitions (`/sp.tasks`) for Phase 2.3 (Better Auth integration); validate task decomposition aligns with constitution requirement for task-driven development.
