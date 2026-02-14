---
id: 005
title: Next.js 15 useOptimistic Hook Research
stage: general
date: 2026-01-02
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: 004-jwt-auth
user: claude
command: Research useOptimistic hook patterns
labels: ["nextjs","hooks","server-actions","research","ui-patterns"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - none
tests:
  - none
---

## Prompt

Research best practices for using Next.js 15 useOptimistic hook with server actions for immediate UI updates during CRUD operations. Specifically:

1. How to properly structure useOptimistic with async server actions
2. Error recovery and rollback patterns
3. Integration with form submissions and mutations
4. Example pattern for task creation, update, deletion

Provide concise findings with code patterns if possible.

## Response snapshot

Comprehensive research on useOptimistic hook structure, error handling patterns, and complete CRUD examples. Key findings:

- **Structure**: Call optimistic updater BEFORE awaiting server action; use temporary IDs for new items
- **Error Recovery**: useOptimistic automatically reverts state on server action failure; combine with useActionState for user feedback
- **Form Integration**: Use useActionState for pending state and validation feedback; coordinate with optimistic updates
- **CRUD Pattern**: Use switch statement to handle add/update/delete actions in updater function; show visual differentiation for optimistic items

## Outcome

- ✅ Impact: Provided actionable research findings with production-ready code patterns for implementing optimistic UI updates
- 🧪 Tests: None (research task)
- 📁 Files: None (research task)
- 🔁 Next prompts: Potentially implement useOptimistic patterns in Evo-TODO task management UI
- 🧠 Reflection: Research was thorough and covered all requested aspects with working code examples

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (research)
- Prompt variant (if applicable): null
- Next experiment: Apply patterns to task creation/update/deletion flows in the current project
