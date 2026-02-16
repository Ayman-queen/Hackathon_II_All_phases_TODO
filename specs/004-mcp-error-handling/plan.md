# Implementation Plan: MCP Server Error Handling & Validation Fix

**Branch**: `004-mcp-error-handling` | **Date**: 2026-01-29 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-mcp-error-handling/spec.md`

## Summary

Fix critical MCP server bug where `TextContent` objects are missing the required `type="text"` parameter, causing Pydantic validation errors and 500 Internal Server Errors. Additionally, implement comprehensive error handling with proper logging, argument validation, and user-friendly error messages following MCP SDK best practices and JSON-RPC 2.0 specification.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: MCP Python SDK (`mcp`), FastAPI, SQLModel, Pydantic
**Storage**: PostgreSQL via Neon (existing, unchanged)
**Testing**: pytest with async support, manual curl testing
**Target Platform**: Linux server (Docker/Vercel)
**Project Type**: Web application (backend focus for this feature)
**Performance Goals**: Tool responses within 2 seconds, no timeouts
**Constraints**: JSON-RPC 2.0 compliance, no breaking changes to MCP protocol
**Scale/Scope**: Single file modification (`server.py`), 10 TextContent fixes, ~50 lines of error handling code

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Full-Stack Separation | ✅ PASS | Backend-only change, no frontend impact |
| II. User-Scoped Data / JWT | ✅ PASS | All tools already require user_id |
| III. Clean Code Principles | ✅ PASS | Adds helper functions, improves readability |
| IV. Task-Driven Implementation | ✅ PASS | Mapped to spec 004-mcp-error-handling |
| V. Performance Over Brevity | ✅ PASS | Error handling adds minimal overhead |
| VI. No Manual Code Writing | ⚠️ PARTIAL | Manual fixes required for existing code |
| VII. MCP Integration | ✅ PASS | Using Context7 MCP for documentation |
| VIII. Backend Statelessness | ✅ PASS | No state changes, all data in DB |
| IX-XIII. Phase III Features | ✅ PASS | No impact on conversation memory, UI, etc. |

**Justification for VI**: Manual code modification is necessary to fix an existing bug. No generator/template approach applies to this bug fix scenario.

## Project Structure

### Documentation (this feature)

```text
specs/004-mcp-error-handling/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 research findings
├── data-model.md        # MCP protocol structures
├── quickstart.md        # Implementation quick reference
├── contracts/
│   └── mcp-jsonrpc.yaml # JSON-RPC contract definition
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Task breakdown (Phase 2 - /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── mcp_server/
│   ├── __init__.py
│   └── server.py        # PRIMARY FILE TO MODIFY
├── app/
│   ├── models/
│   │   └── todo.py      # Referenced by tools (unchanged)
│   └── agents/
│       └── chat_agent.py # Calls MCP server (unchanged)
└── tests/
    └── test_mcp_server.py  # NEW: Unit tests for MCP tools
```

**Structure Decision**: Web application (Option 2) - Backend-only modification with new test file.

## Complexity Tracking

> No constitution violations requiring justification.

## Implementation Phases

### Phase 1: Fix TextContent Validation (P0 - Critical)

**Objective**: Resolve the root cause by adding `type="text"` to all TextContent instances.

**Changes**:

| Location | Line | Current | Fixed |
|----------|------|---------|-------|
| `call_tool` | 112 | `TextContent(text=...)` | `TextContent(type="text", text=...)` |
| `call_tool` | 123 | `TextContent(text=...)` | `TextContent(type="text", text=...)` |
| `call_tool` | 128 | `TextContent(text=...)` | `TextContent(type="text", text=...)` |
| `call_tool` | 130 | `TextContent(text=...)` | `TextContent(type="text", text=...)` |
| `call_tool` | 147 | `TextContent(text=...)` | `TextContent(type="text", text=...)` |
| `call_tool` | 148 | `TextContent(text=...)` | `TextContent(type="text", text=...)` |
| `call_tool` | 158 | `TextContent(text=...)` | `TextContent(type="text", text=...)` |
| `call_tool` | 159 | `TextContent(text=...)` | `TextContent(type="text", text=...)` |
| `call_tool` | 171 | `TextContent(text=...)` | `TextContent(type="text", text=...)` |
| `call_tool` | 172 | `TextContent(text=...)` | `TextContent(type="text", text=...)` |

**Verification**: Run MCP server and test `tools/call` - no ValidationError in logs.

---

### Phase 2: Add Helper Functions (P1 - High)

**Objective**: Create reusable utilities for consistent response/error handling.

**New Functions**:

```python
def create_text_response(message: str) -> list[types.TextContent]:
    """Create a properly formatted TextContent response."""
    return [types.TextContent(type="text", text=message)]


def create_error_response(code: int, message: str, request_id) -> JSONResponse:
    """Create a JSON-RPC 2.0 compliant error response."""
    logger.error(f"MCP error {code}: {message}")
    return JSONResponse({
        "jsonrpc": "2.0",
        "error": {"code": code, "message": message},
        "id": request_id
    })


def validate_required_args(arguments: dict, required: list[str], tool_name: str) -> None:
    """Validate that required arguments are present and non-empty."""
    missing = [arg for arg in required if not arguments.get(arg)]
    if missing:
        raise ValueError(f"Missing required arguments for {tool_name}: {', '.join(missing)}")


def parse_uuid_safe(value: str, field_name: str) -> UUID:
    """Parse UUID with user-friendly error message."""
    try:
        return UUID(value)
    except ValueError:
        raise ValueError(f"Invalid {field_name} format: '{value}' is not a valid UUID")
```

**Placement**: Add after imports, before `@mcp_server.list_tools()`.

---

### Phase 3: Refactor Tool Implementations (P1 - High)

**Objective**: Use helper functions and add proper error handling to each tool.

**Pattern for each tool**:

```python
# Before (example: add_task)
elif name == "add_task":
    title = arguments.get("title")
    description = arguments.get("description")
    if not title:
        raise ValueError("Title is required for adding a task.")
    with Session(engine) as session:
        todo = Todo(user_id=user_id, title=title, description=description)
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return [types.TextContent(text=f"Task '{todo.title}' added with ID: {todo.id}")]

# After
elif name == "add_task":
    validate_required_args(arguments, ["title"], "add_task")
    title = arguments["title"]
    description = arguments.get("description")
    with Session(engine) as session:
        todo = Todo(user_id=user_id, title=title, description=description)
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return create_text_response(f"Task '{todo.title}' added with ID: {todo.id}")
```

**Tools to refactor** (6 total):
1. `get_user_stats` - Use `create_text_response`
2. `add_task` - Use `validate_required_args`, `create_text_response`
3. `list_tasks` - Use `create_text_response`
4. `update_task` - Use `validate_required_args`, `parse_uuid_safe`, `create_text_response`
5. `delete_task` - Use `validate_required_args`, `parse_uuid_safe`, `create_text_response`
6. `complete_task` - Use `validate_required_args`, `parse_uuid_safe`, `create_text_response`

---

### Phase 4: Enhance HTTP Handler Error Handling (P1 - High)

**Objective**: Add granular exception handling in `handle_mcp_request`.

**Changes to `tools/call` handler**:

```python
elif method == "tools/call":
    tool_name = params.get("name")
    tool_args = params.get("arguments", {})

    if not tool_name:
        return create_error_response(-32602, "Missing tool name", request_id)

    try:
        result = await call_tool(tool_name, tool_args)
        result_text = result[0].text if result else ""
        return JSONResponse({
            "jsonrpc": "2.0",
            "result": {"content": [{"type": "text", "text": result_text}]},
            "id": request_id
        })
    except ValueError as e:
        # Validation errors (missing args, invalid UUID, etc.)
        logger.warning(f"Validation error in tool '{tool_name}': {e}")
        return create_error_response(-32602, str(e), request_id)
    except Exception as e:
        # Unexpected errors (database failures, etc.)
        logger.error(f"Tool execution failed: {tool_name}", exc_info=True)
        return create_error_response(-32603, "Internal server error", request_id)
```

---

### Phase 5: Enhance Logging (P2 - Medium)

**Objective**: Add structured logging with appropriate levels and sanitization.

**Changes**:

1. **Add request context logging**:
```python
logger.info(f"MCP request: method={method}, tool={params.get('name', 'N/A')}, has_user_id={bool(params.get('arguments', {}).get('user_id'))}")
```

2. **Add success logging**:
```python
logger.info(f"Tool '{tool_name}' executed successfully")
```

3. **Ensure no sensitive data in logs**:
   - Log `has_user_id: bool` instead of actual user_id
   - Log tool name and error type, not full arguments
   - Use `exc_info=True` only for ERROR level

---

### Phase 6: Add Unit Tests (P2 - Medium)

**Objective**: Create test coverage for MCP tools and error handling.

**New file**: `backend/tests/test_mcp_server.py`

**Test cases**:
1. `test_text_content_has_type_field` - Verify all responses include `type="text"`
2. `test_add_task_success` - Valid task creation
3. `test_add_task_missing_title` - Returns -32602 error
4. `test_add_task_missing_user_id` - Returns -32602 error
5. `test_update_task_invalid_uuid` - Returns -32602 error
6. `test_unknown_tool` - Returns ValueError
7. `test_handle_mcp_request_parse_error` - Malformed JSON returns -32700
8. `test_handle_mcp_request_unknown_method` - Returns -32601

---

## Architecture Decisions

### AD-001: Helper Functions vs Class-Based Approach

**Decision**: Use module-level helper functions instead of a class.

**Rationale**:
- Minimal changes to existing code structure
- Functions are stateless and pure
- Easier to test in isolation
- No need for dependency injection

### AD-002: Error Code Strategy

**Decision**: Use standard JSON-RPC 2.0 error codes.

**Rationale**:
- Protocol compliance ensures interoperability
- Well-documented standard
- MCP clients expect these codes

### AD-003: Logging Strategy

**Decision**: Use Python's logging module with INFO/WARNING/ERROR levels.

**Rationale**:
- Already configured in the codebase
- Supports structured output
- Integrates with deployment logging systems

---

## Risk Mitigation

| Risk | Mitigation | Contingency |
|------|------------|-------------|
| Regression in existing functionality | Unit tests for all tools | Quick rollback via git |
| Logging overhead | Use appropriate log levels | Disable DEBUG in production |
| Breaking MCP protocol | Contract testing with curl | Revert and manual testing |

---

## Dependencies

```
mcp (existing) - MCP Python SDK
fastapi (existing) - HTTP server
sqlmodel (existing) - Database ORM
pytest (new dependency for tests) - Unit testing
pytest-asyncio (new dependency for tests) - Async test support
```

---

## Verification Checklist

- [x] All 10 TextContent instances include `type="text"` (via create_text_response helper)
- [x] Helper functions added and working (create_text_response, create_error_response, validate_required_args, parse_uuid_safe)
- [x] All 6 tools refactored to use helpers
- [x] HTTP handler has granular error handling (ValueError → -32602, Exception → -32603, JSONDecodeError → -32700)
- [x] Logging includes tool name and error context (structured logging with has_user_id sanitization)
- [ ] Unit tests pass (requires venv with pytest)
- [ ] Manual integration test passes (chat API)
- [ ] No Pydantic ValidationError in logs
- [x] Error responses use correct JSON-RPC codes (-32601, -32602, -32603, -32700)

---

## Next Steps

1. ~~Run `/sp.tasks` to generate task breakdown~~ ✓ DONE
2. ~~Implement Phase 1 (TextContent fix) first - immediate blocker resolution~~ ✓ DONE
3. ~~Implement remaining phases incrementally~~ ✓ DONE
4. Run tests and verify integration
5. Create PR for review
