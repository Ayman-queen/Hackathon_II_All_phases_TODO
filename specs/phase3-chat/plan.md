# Implementation Plan: Phase III Chat Interface

**Branch**: `phase-3` | **Date**: 2026-01-27 | **Spec**: specs/phase3-chat/spec.md

**Note**: This template is filled by /sp.plan. See .specify/templates/commands/plan.md workflow.

## Summary

Implement conversational chat UI on stateless backend using MCP tools + OpenAI Agents SDK. Add Conversation/Message schema; POST /api/{user_id}/chat endpoint; Shadcn chat UI. Enforce 5-msg window + summary.

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript 5.0+ (frontend)
**Primary Dependencies**: FastAPI, SQLModel, modelcontextprotocol/python-sdk, openai-agents-python, Shadcn/UI, next-themes
**Storage**: Neon PostgreSQL (Conversation, Message tables)
**Testing**: pytest (backend), Jest (frontend)
**Target Platform**: Linux server (Docker)
**Project Type**: web
**Performance Goals**: <500ms chat response p95
**Constraints**: Stateless (DB-only), 5-msg window, JWT per request, user isolation
**Scale/Scope**: Multi-tenant (1000s users), 10k convos/day

## Constitution Check

✅ I. Full-Stack: Extends existing Next.js/FastAPI/SQLModel/Better Auth.
✅ II. JWT: Enforced per chat request.
✅ III. Clean Code: Small functions for agent/tools.
✅ IV. Task-Driven: Maps to tasks.md.
✅ V. Performance: Async FastAPI/Agents.
✅ VI. No Manual: Generate schemas/tools.
✅ VII. MCP: Context7/Better Auth used; MCP SDK for tools.
✅ VIII. Stateless: DB-only, no RAM state.
✅ IX. 5-msg Window: Load recent 5 only.
✅ X. Summarization: Trigger post-5 msgs.
✅ XI. Greeting: get_user_stats on load.
✅ XII. Tool Isolation: Inject user_id.
✅ XIII. UI: Shadcn ScrollArea, themes.

## Project Structure

### Documentation (this feature)
```
specs/phase3-chat/
├── plan.md              # This file
├── research.md          # MCP/Agents research
├── data-model.md        # Conversation/Message schema
├── quickstart.md        # Setup guide
├── contracts/           # chat-api.yaml
└── tasks.md             # Next (/sp.tasks)
```

### Source Code (repo root)
```
backend/app/api/chat.py              # POST /{user_id}/chat endpoint
backend/app/agents/chat_agent.py     # OpenAI Agents Runner
backend/app/mcp/tools/todo_tools.py  # MCP task CRUD tools
frontend/app/dashboard/chat/         # Chat page/UI
frontend/app/dashboard/chat/page.tsx # Shadcn ScrollArea chat
frontend/lib/hooks/useChat.ts        # Chat state/fetch wrapper
```

**Structure Decision**: Extend existing backend/app/api + frontend/app/dashboard; new chat subroute.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| OpenAI Agents SDK | Stateless agent loop w/tools | Raw LLM calls lack handoffs/guardrails |
