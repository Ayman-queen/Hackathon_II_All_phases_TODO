---
id: 002
title: Frontend Architecture & Implementation Plan
stage: plan
date: 2025-12-30
surface: agent
model: claude-haiku-4-5
feature: 003-phase2-frontend-ui
branch: 003-phase2-frontend-ui
user: claude
command: /sp.plan
labels: ["frontend", "architecture", "plan", "next.js", "auth", "api-design"]
links:
  spec: specs/003-phase2-frontend-ui/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-phase2-frontend-ui/plan.md
  - specs/003-phase2-frontend-ui/data-model.md (TBD)
  - specs/003-phase2-frontend-ui/research.md (TBD)
  - specs/003-phase2-frontend-ui/contracts/auth.openapi.json (TBD)
  - specs/003-phase2-frontend-ui/contracts/todos.openapi.json (TBD)
tests:
  - Constitution check (all gates passed)
  - Architecture decision validation
  - Dependency mapping
  - Risk assessment
---

## Prompt

Generate speckit.plan for the UI and Auth integration. Define the 'How':
* Auth Client: Initialize the Better Auth client in frontend/lib/auth.ts and enable the JWT plugin.
* API Client: Build a centralized fetch wrapper in frontend/lib/api.ts that automatically retrieves the JWT from Better Auth and attaches it to headers.
* Component Library: Use Shadcn for the Task Card, Filter Tabs, and Auth Forms.
* State Management: Use React state or a lightweight hook to handle real-time UI updates after CRUD operations.
* Theme Provider: Integrate next-themes for seamless light/dark mode switching

## Response snapshot

**Implementation Plan Created**: `specs/003-phase2-frontend-ui/plan.md`
**Branch**: `003-phase2-frontend-ui`
**Status**: Complete and Ready for Research Phase

### Key Architecture Decisions

| Decision | Rationale | Alternatives |
|----------|-----------|--------------|
| **Next.js App Router** | Modern, SSR-capable, server/client component split | Pages Router (legacy) |
| **Shadcn/UI + Tailwind** | Headless components, full customization, unstyled foundation | Material-UI, styled-components |
| **Centralized API wrapper** (lib/api.ts) | Single point for JWT injection, DRY principle, testable | Per-component fetch |
| **Custom React hooks** | Reusable auth/todo logic, testable in isolation | Redux, Zustand, Context alone |
| **next-themes** | Lightweight, SSR-friendly, minimal code | Custom theme context |

### Project Structure

**Frontend** organized into:
- `app/` - Next.js pages (auth, protected routes, API handlers)
- `lib/` - Core utilities (Better Auth client, API wrapper, custom hooks)
- `components/` - Reusable Shadcn/React components
- `styles/` - Tailwind CSS configuration
- `tests/` - Jest + React Testing Library + Playwright E2E

### Constitution Compliance

✅ **ALL GATES PASSED**:
- ✅ User-Scoped Data & JWT Auth: API wrapper ensures JWT in all requests
- ✅ Clean Code Principles: Component-based, single responsibility, TypeScript
- ✅ Task-Driven Implementation: All features will map to task IDs
- ✅ Better Auth Integration: Client setup with JWT plugin
- ✅ No Manual Code Writing: Shadcn/UI scaffolding, Next.js generators
- ✅ MCP-Driven Documentation: Better Auth MCP for auth; Context7 MCP for Next.js

### Proposed Implementation Phases

**Phase 0: Research** (TBD)
- Better Auth JS client setup and JWT plugin
- Next.js App Router auth patterns
- Shadcn/UI and next-themes integration
- Testing strategies for auth components

**Phase 1: Design & Contracts** (TBD)
- Data model: User, Todo, Theme entities
- OpenAPI 3.0 contracts for auth and todo endpoints
- Quickstart guide for local development
- Agent context update for Next.js/Shadcn patterns

**Phase 2: Task Generation** (/sp.tasks)
- 12 implementation tasks (T-301 through T-312)
- Task dependencies and sequencing
- Acceptance criteria for each task

### Success Criteria Mapping

All 10 success criteria mapped to implementation approach:
- SC-001 (Auth <1min): Streamlined Shadcn forms
- SC-002 (List load <2s): API client caching, React hooks
- SC-003 (Filter/sort <500ms): Client-side, useTodos hook
- SC-004 (JWT 95%): Centralized API wrapper
- SC-005 (Isolation 100%): Backend validation + frontend respect
- SC-006 (Responsive): Shadcn/Tailwind mobile-first
- SC-007 (Theme toggle <1s): next-themes CSS vars
- SC-008 (Persistence 99%): localStorage + SSR-safe
- SC-009 (Accessibility): Radix UI foundation + testing
- SC-010 (Usability <10 steps): Form optimization

### Risk Mitigation

4 identified risks with mitigation strategies:
- Better Auth API downtime: Retry logic + offline fallback
- JWT expiration mid-flow: Token refresh + automatic re-auth
- Shadcn/UI breaking changes: Pin version, monitor releases
- Theme flashing on load: next-themes SSR handling

## Outcome

- ✅ Impact: Comprehensive implementation architecture designed. All constitutional gates passed. Clear separation of concerns (auth, API client, components). Technology choices justified with alternatives documented. Ready for research and task generation.

- 🧪 Tests: Constitution check executed; all 7 requirements verified and passed. Architecture decision table created. Risk assessment completed. No violations or unresolved clarifications.

- 📁 Files:
  - `specs/003-phase2-frontend-ui/plan.md` (303 lines, complete plan)
  - Documentation artifacts (research.md, data-model.md, contracts/) TBD

- 🔁 Next prompts:
  1. Phase 0 Research (external): Better Auth/Next.js/Shadcn patterns
  2. `/sp.plan` Phase 1 execution (if continuing): Generate research.md, data-model.md, OpenAPI contracts
  3. `/sp.tasks` (to generate granular implementation tasks with IDs)
  4. Implementation via `/sp.implement` or manual development

- 🧠 Reflection: Plan is well-structured, technologically sound, and constitutionally compliant. User input provided specific technology choices (Better Auth, Shadcn, next-themes) which are now embedded in the architecture. Clear implementation roadmap with identified risks and mitigation strategies. Ready to proceed to research phase or task generation.

## Evaluation notes (flywheel)

- Failure modes observed: None. User input included specific tech choices (auth.ts, api.ts, Shadcn, next-themes), which guided clear architectural decisions. Plan incorporates all user requirements (JWT injection, component library, theme switching, state management).

- Graders run and results (PASS/FAIL):
  - Constitution Check: ✅ PASS (7/7 requirements)
  - Architecture Decisions: ✅ PASS (5 key decisions documented)
  - Project Structure: ✅ PASS (realistic, modular layout)
  - Risk Assessment: ✅ PASS (4 risks identified with mitigations)
  - Overall: ✅ PLAN READY FOR EXECUTION

- Prompt variant (if applicable): Single variant. User input was specific and complete, no iteration needed.

- Next experiment (smallest change to try): Proceed to Phase 0 Research or directly to `/sp.tasks` for implementation task generation. Both paths are valid; research provides deeper best-practices documentation, while tasks enables immediate implementation.
