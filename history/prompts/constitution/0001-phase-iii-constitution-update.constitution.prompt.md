---
id: 0001
title: Phase III constitution update
stage: constitution
date: 2026-01-27
surface: Claude Code CLI
model: claude-opus-4-5-20251101
feature: none
branch: phase-3
user: Human
command: /sp.constitution
labels: [phase3,constitution,standards]
links:
  spec:
  ticket:
  adr:
  pr:
files: |
  - path: .specify/memory/constitution.md
    status: updated
    lines_changed: +50
tests: {}
---

## Prompt

Update speckit.constitution with Phase III standards. But first create a new branch name phase 3 for it and start working on it. Add these non-negotiables:* Statelessness: The backend must hold zero state in RAM; all history must reside in Neon DB.

Memory Window: Implement a strict 5-message window for active context.

Summarization Pattern: Every 5 messages, the agent must generate and store a summary to the conversations table to maintain long-term context without bloat.

Proactive Greeting: Upon dashboard load, the agent must call get_user_stats and greet the user with their current task counts.* User Isolation: Every tool call must be injected with the user_id from the verified Better Auth JWT.

UI Consistency: Maintain the professional App Shell, Shadcn/UI components, and existing Light/Dark mode.

## Response snapshot

Created phase-3 branch. Updated .specify/memory/constitution.md to v3.0.0 incorporating all Phase III non-negotiables as new principles VIII-XIII. Prepended Sync Impact Report. No template updates required. Git clean.

## Outcome
- ✅ Impact: Constitution amended for Phase III; new statelessness, memory management, greeting, isolation, UI principles added. Ready for Phase III development.
- 🧪 Tests: N/A (governance doc)
- 📁 Files: .specify/memory/constitution.md (updated)
- 🔁 Next prompts: Implement Phase III features per new standards
- 🧠 Reflection: Major version bump justified by new mandatory constraints.

## Evaluation notes (flywheel)
- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS (no placeholders left, version/dates correct, principles declarative)
- Prompt variant (if applicable):
- Next experiment:
