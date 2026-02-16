# Quickstart: MCP Error Handling Fix

**Feature**: 004-mcp-error-handling
**Estimated Implementation Time**: 1-2 hours
**Risk Level**: Low (bug fix, no new features)

## Prerequisites

- Python 3.11+
- MCP Python SDK (`mcp` package)
- FastAPI
- Access to `backend/mcp_server/server.py`

## Quick Fix Summary

### Step 1: Fix TextContent Type Parameter

**File**: `backend/mcp_server/server.py`

Find all instances of:
```python
types.TextContent(text="...")
```

Replace with:
```python
types.TextContent(type="text", text="...")
```

**Locations** (10 total):
- Line 112: `get_user_stats`
- Line 123: `add_task`
- Line 128: `list_tasks` (no tasks)
- Line 130: `list_tasks` (has tasks)
- Line 147: `update_task` (success)
- Line 148: `update_task` (not found)
- Line 158: `delete_task` (success)
- Line 159: `delete_task` (not found)
- Line 171: `complete_task` (success)
- Line 172: `complete_task` (not found)

### Step 2: Add Error Handling Wrapper

Create a helper function for consistent error responses:

```python
def create_text_response(message: str) -> list[types.TextContent]:
    """Create a properly formatted TextContent response."""
    return [types.TextContent(type="text", text=message)]

def create_error_response(code: int, message: str, request_id) -> JSONResponse:
    """Create a JSON-RPC error response."""
    return JSONResponse({
        "jsonrpc": "2.0",
        "error": {"code": code, "message": message},
        "id": request_id
    })
```

### Step 3: Wrap Tool Execution in try-except

```python
elif method == "tools/call":
    tool_name = params.get("name")
    tool_args = params.get("arguments", {})
    try:
        result = await call_tool(tool_name, tool_args)
        result_text = result[0].text if result else ""
        return JSONResponse({
            "jsonrpc": "2.0",
            "result": {"content": [{"type": "text", "text": result_text}]},
            "id": request_id
        })
    except ValueError as e:
        logger.warning(f"Validation error in {tool_name}: {e}")
        return create_error_response(-32602, str(e), request_id)
    except Exception as e:
        logger.error(f"Tool execution failed: {tool_name}", exc_info=True)
        return create_error_response(-32603, "Internal server error", request_id)
```

## Testing

### Manual Test

```bash
# Start MCP server
cd backend && python -m mcp_server.server

# Test tool call
curl -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "add_task",
      "arguments": {"user_id": "test", "title": "Test Task"}
    },
    "id": 1
  }'
```

**Expected Response**:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [{"type": "text", "text": "Task 'Test Task' added with ID: ..."}]
  },
  "id": 1
}
```

### Integration Test

```bash
# Start both servers
cd backend && uvicorn app.main:app --port 8000 &
cd backend && python -m mcp_server.server &

# Test chat API
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task called deploy backend",
    "user_id": "test-user",
    "conversation_id": "00000000-0000-0000-0000-000000000001"
  }'
```

## Success Verification

1. ✅ No Pydantic ValidationError in logs
2. ✅ Chat API returns response within 10 seconds
3. ✅ Tasks appear in database after creation
4. ✅ Error cases return user-friendly messages

## Rollback

If issues occur, revert `backend/mcp_server/server.py` to previous commit:

```bash
git checkout HEAD~1 -- backend/mcp_server/server.py
```
