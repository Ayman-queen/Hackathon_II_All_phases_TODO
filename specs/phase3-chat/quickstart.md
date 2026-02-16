# Quickstart: Phase 3 Chat

1. Migrate DB: Add conversations, messages tables.
2. Backend: pip install modelcontextprotocol/python-sdk openai-agents; define MCP tools for todo CRUD; Agent Runner with 5-msg summary.
3. Endpoint: POST /api/{user_id}/chat - stateless, JWT deps.
4. Frontend: app/dashboard/chat/page.tsx with Shadcn ScrollArea, fetch with JWT.
5. Test: docker-compose up; POST curl with JWT; verify greeting/summary.
