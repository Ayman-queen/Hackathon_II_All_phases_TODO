---
id: 1
title: Define project constitution
stage: constitution
date: 2025-12-27
surface: agent
model: claude-haiku-4-5-20251001
feature: none
branch: master
user: sheikh-mujtaba
command: /sp.constitution
labels: ["constitution", "governance", "python", "architecture"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests: []
---

## Prompt

Create a speckit.constitution file. Define the project's non-negotiables: Use Python 3.13+, uv for package management, and strictly in-memory storage. Architecture must follow clean code principles. Rules: No manual code writing, all code must map to a Task ID, and performance is prioritized over brevity.

## Response snapshot

Created Evo-TODO Constitution (v1.0.0) with six core principles covering Python 3.13+ runtime, uv package management, in-memory storage, clean code discipline, task-driven development, and performance-first optimization. Added Technology Stack, Development Workflow, Non-Negotiable Constraints, and Governance sections. Constitution enforces accountability through Task ID mapping and establishes clear amendment procedures for future changes.

## Outcome

- ✅ Impact: Constitution now defines all non-negotiable project principles and governance rules
- 🧪 Tests: No tests (governance artifact); compliance verified via code review
- 📁 Files: .specify/memory/constitution.md updated with complete governance framework
- 🔁 Next prompts: Feature spec creation, architecture decision records (ADRs) for significant decisions
- 🧠 Reflection: Constitution balances strictness (in-memory, Python 3.13+, Task-ID mapping) with practical guidance (clean code, performance optimization)

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable
- Prompt variant (if applicable): null
- Next experiment: Validate constitution against template specs and plan templates for consistency propagation
