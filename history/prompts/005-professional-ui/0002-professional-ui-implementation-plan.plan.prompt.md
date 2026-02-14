---
id: 0002
title: Professional UI implementation plan
stage: plan
date: 2026-01-02
surface: agent
model: claude-haiku-4-5-20251001
feature: 005-professional-ui
branch: 005-professional-ui
user: claude
command: /sp.plan
labels: ["plan", "architecture", "ui", "crud", "react", "typescript"]
links:
  spec: specs/005-professional-ui/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-professional-ui/plan.md
  - specs/005-professional-ui/research.md
  - specs/005-professional-ui/data-model.md
  - specs/005-professional-ui/quickstart.md
  - specs/005-professional-ui/contracts/task-api.openapi.yaml
tests:
  - Constitution compliance check (all gates pass)
  - Research verification (6 topics resolved)
  - API contract validation (OpenAPI spec)
---

## Prompt

Generate speckit.plan for Phase 2.3. Define the 'How':

State Management: Use useOptimistic (Next.js 15) for immediate UI updates during CRUD operations.

Bulk Logic: Implement a selection state (Set of IDs) and a BulkActions component.

Popups: Use Shadcn Dialog for 'Delete Confirmation' and Shadcn Popover for 'Priority Selection'.

API Integration: Update the api.ts client to support batch operations if the backend allows, or use Promise.all for client-side batching.

Theming: Ensure next-themes is configured correctly for the entire dashboard layout.

## Response snapshot

Created comprehensive architecture plan with all technical decisions documented. Phase 0 research completed: 6 topics researched (useOptimistic patterns, Shadcn Dialog/Popover, next-themes, bulk operations, API integration, state management). Phase 1 design produced: plan.md (full architecture), research.md (resolved unknowns), data-model.md (entities + SQL), quickstart.md (5-min overview), task-api.openapi.yaml (complete API spec). Constitution compliance gates pass. All files ready for Phase 2 implementation tasks.

## Outcome

- ✅ Impact: Architectural foundation established; all technical decisions documented with rationale; API contracts defined; development team can begin Phase 2 implementation
- 🧪 Tests: Constitution check passed all 7 gates; Research verification complete (6 topics); OpenAPI schema validates all endpoints and error handling
- 📁 Files: 5 major artifacts created (plan.md 358 lines, research.md 380 lines, data-model.md 410 lines, quickstart.md 350 lines, task-api.openapi.yaml 300+ lines); PHR record created
- 🔁 Next prompts: /sp.tasks (generate implementation tasks), /sp.adr (document architectural decisions if needed), /sp.implement (execute tasks)
- 🧠 Reflection: User's technical constraints (useOptimistic, Shadcn Dialog/Popover, next-themes, batch operations) seamlessly integrated into architecture; all design decisions justified; Phase 1 complete, ready for detailed task breakdown

## Evaluation notes (flywheel)

- Failure modes observed: None; all research questions resolved, all gates passed, complete coherence between spec and plan
- Graders run and results (PASS/FAIL): PASS - Constitution compliance 100%, API contracts fully specified, data model complete with migrations, quickstart provides clear implementation guidance
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Begin Phase 2 with /sp.tasks to identify any missing details during task creation; if discovered, update plan.md and re-run tasks
