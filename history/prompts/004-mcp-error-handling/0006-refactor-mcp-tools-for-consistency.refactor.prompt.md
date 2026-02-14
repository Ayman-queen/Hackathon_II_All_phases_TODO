---
id: 0006
title: Refactor MCP Tools for Consistency
stage: refactor
date: 2026-01-29
surface: backend/mcp_server/server.py
model: 
feature: 004-mcp-error-handling
branch: 
user: 
command: read the @error.tx and review the fastapi backend structure of creating updating and deleting the tasks and make mcp tools accordingly
labels: [mcp, refactor, backend]
links:
  spec: 
  ticket: 
  adr: 
  pr: 
files:
  - backend/mcp_server/server.py
tests:

---

## Prompt

read the @error.tx and review the fastapi backend structure of creating updating and deleting the tasks and make mcp tools accordingly

## Response snapshot

I have refactored the MCP tools in `backend/mcp_server/server.py` to align them with the FastAPI REST API.

Here's a summary of the changes:

*   **`update_task`:**
    *   Merged the functionality of `complete_task`.
    *   Now accepts an optional `is_complete` boolean parameter to toggle the completion status.
    *   The `inputSchema` has been updated accordingly.
*   **`complete_task`:**
    *   The tool has been removed as it's now redundant.
*   **`add_task`:**
    *   Added validation for `title` (required, not empty, max 500 chars).
    *   Added validation for `description` (max 2000 chars).
*   **`list_tools`:**
    *   Updated to reflect the removal of `complete_task` and the new `inputSchema` for `update_task`.

## Outcome

- ✅ Impact: The MCP tools are now more consistent with the REST API, improving maintainability and reducing redundancy.
- 🧪 Tests: No tests were added or modified.
- 📁 Files: Modified `backend/mcp_server/server.py`.
- 🔁 Next prompts: 
- 🧠 Reflection: The user's request was a bit ambiguous, but I was able to infer the intent and refactor the MCP tools successfully. The initial error with the PHR script was due to a misunderstanding of the feature naming convention.

## Evaluation notes (flywheel)

- Failure modes observed: 
- Graders run and results (PASS/FAIL): 
- Prompt variant (if applicable): 
- Next experiment: