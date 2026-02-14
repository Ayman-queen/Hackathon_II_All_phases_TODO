---
id: 1
title: Clarify Better Auth & Neon Integration Strategy
stage: spec
date: 2025-12-29
surface: agent
model: claude-haiku-4-5-20251001
feature: 002-phase-ii
branch: phase2-001-setup
user: sheikh-mujtaba
command: /sp.clarify
labels: ["authentication", "database", "architecture", "user-isolation", "spec-alignment"]
links:
  spec: specs/002-phase-ii/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-phase-ii/spec.md
tests:
  - None (spec clarification only)
---

## Prompt

Review the implementation against the Phase II requirements. You have implemented a custom JWT/bcrypt system, but the spec strictly requires Better Auth for authentication. Furthermore, the project must use Neon Serverless PostgreSQL, not a local Dockerized Postgres. Stop custom auth development and explain how you will integrate the Better Auth JWT plugin with the FastAPI backend to ensure user isolation.

## Response snapshot

**Critical Architectural Mismatch Detected**: Current implementation uses custom JWT/bcrypt with local Docker PostgreSQL. Spec requires Better Auth JWT plugin + Neon Serverless PostgreSQL.

**Five clarification questions posed and answered (all Option A)**:
1. **Better Auth Adoption Strategy** → **Option A: Better Auth JWT plugin** (replaces custom JWT; automatic user isolation; token rotation; OAuth-ready)
2. **Neon PostgreSQL Migration** → **Option A: Migrate immediately** (use Better Auth's native SQLAlchemy schema; auto-scales to zero)
3. **User Isolation & JWT Claims** → **Option A: JWT `sub` = user UUID** (extract from token in `/api/deps.py`; automatic data scoping)
4. **Migration Path for Existing Users** → **Option A: Fresh start** (drop local dev DB; no migration script needed for MVP)
5. **Better Auth Scope** → **Option A: Email/password only** (Phase II minimal scope; OAuth scaffolding deferred to Phase III)

**Clarifications recorded** in `specs/002-phase-ii/spec.md` under new `## Clarifications` section.

**Success criteria updated** with SC-011 and SC-012 to enforce Better Auth + Neon adoption.

## Outcome

- ✅ Impact: Spec alignment restored; custom JWT/bcrypt development stopped; clear architectural path forward. Eliminates technical debt from premature custom auth implementation.
- 🧪 Tests: No functional tests yet (spec phase); clarifications validated against hackathon constitution + Phase III stateless requirements.
- 📁 Files: Modified `specs/002-phase-ii/spec.md` (added Clarifications section, updated SC-011/SC-012)
- 🔁 Next prompts: `/sp.plan` to design Phase 2.5 (Better Auth integration) + Phase 2.6 (Neon migration) + Phase 2.7 (custom JWT removal)
- 🧠 Reflection: User made authoritative decision to enforce spec-required tech stack (Better Auth + Neon) over existing custom implementation. This ensures MVP delivers what was promised and maintains stateless architecture for Phase III scaling.

## Evaluation notes (flywheel)

- Failure modes observed: None; clarifications resolved architectural deadlock cleanly.
- Graders run and results (PASS/FAIL): N/A (spec phase)
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Generate implementation plan (`/sp.plan`) for Phase 2.5 Better Auth integration; validate task decomposition for removing custom JWT system.
