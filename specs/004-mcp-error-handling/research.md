# Research: MCP Error Handling & Validation Fix

**Feature**: 004-mcp-error-handling
**Date**: 2026-01-29
**Status**: Complete

## Research Questions

### RQ-001: TextContent Type Parameter Requirement

**Question**: Why does `types.TextContent(text=...)` fail with Pydantic validation error?

**Finding**: The MCP Python SDK's `TextContent` class is a Pydantic model that requires an explicit `type` field set to `"text"`. This is part of the MCP protocol's content type discrimination pattern.

**Evidence** (from MCP SDK documentation):
```python
# Correct usage (from official docs)
return CallToolResult(content=[TextContent(type="text", text="Response visible to the model")])
```

**Decision**: Add `type="text"` parameter to all 10 `TextContent` instantiations in `server.py`.

**Rationale**: This is the documented and required usage pattern per the MCP SDK specification.

**Alternatives Considered**:
1. Subclass TextContent with default type - Rejected: Adds unnecessary abstraction
2. Use a factory function - Rejected: Simple parameter addition is cleaner

---

### RQ-002: Error Handling Pattern for MCP Tools

**Question**: What is the recommended error handling pattern for MCP tool implementations?

**Finding**: The MCP SDK recommends a try-except pattern with explicit error messages and proper exception propagation.

**Evidence** (from MCP SDK documentation):
```python
async def work(task: ServerTaskContext) -> CallToolResult:
    try:
        result = await risky_operation()
        return CallToolResult(content=[TextContent(type="text", text=result)])
    except PermissionError:
        await task.fail("Access denied - insufficient permissions")
        raise
    except TimeoutError:
        await task.fail("Operation timed out after 30 seconds")
        raise
```

**Decision**: Implement layered error handling:
1. **Tool-level**: Wrap each tool operation in try-except
2. **Handler-level**: Catch and transform exceptions to JSON-RPC errors
3. **Global-level**: FastAPI exception handler as safety net

**Rationale**: Defense-in-depth approach ensures no unhandled exceptions reach users.

---

### RQ-003: JSON-RPC Error Codes

**Question**: Which JSON-RPC error codes should be used for different failure scenarios?

**Finding**: JSON-RPC 2.0 specification defines standard error codes:

| Code | Meaning | Use Case |
|------|---------|----------|
| -32700 | Parse error | Malformed JSON |
| -32600 | Invalid Request | Missing required fields |
| -32601 | Method not found | Unknown MCP method |
| -32602 | Invalid params | Validation failures |
| -32603 | Internal error | Server-side exceptions |
| -32000 to -32099 | Server error | Application-specific |

**Decision**: Use the following mapping:
- Missing `user_id` / `title` / `task_id` → `-32602` (Invalid params)
- Tool not found → `-32601` (Method not found)
- Database errors → `-32603` (Internal error)
- UUID parsing errors → `-32602` (Invalid params)

**Rationale**: Follows JSON-RPC 2.0 specification for interoperability.

---

### RQ-004: Logging Best Practices

**Question**: What should be logged for effective debugging without exposing sensitive data?

**Finding**: Python logging module with structured context and appropriate log levels.

**Evidence** (from MCP SDK documentation):
```python
# Different log levels
await ctx.debug(f"Debug: Processing '{data}'")
await ctx.info("Info: Starting processing")
await ctx.warning("Warning: This is experimental")
await ctx.error("Error: (This is just a demo)")
```

**Decision**: Implement structured logging with:
- **INFO**: Method name, tool name (success cases)
- **WARNING**: Unknown methods, missing optional fields
- **ERROR**: Exceptions with tool name, error type, sanitized arguments

**Rationale**: Balances debugging capability with performance and security.

**Sensitive Data Handling**:
- Never log: passwords, tokens, full request bodies
- Sanitize: user_id (log presence, not value), task content

---

### RQ-005: Argument Validation Strategy

**Question**: When and how should arguments be validated?

**Finding**: Validate early, fail fast, provide clear messages.

**Current Implementation Issues**:
1. Validation happens mid-execution (after some processing)
2. Error messages are generic
3. No differentiation between missing vs invalid values

**Decision**: Implement validation utility function:
```python
def validate_tool_args(arguments: dict, required: list[str], tool_name: str) -> None:
    missing = [arg for arg in required if not arguments.get(arg)]
    if missing:
        raise ValueError(f"Missing required arguments for {tool_name}: {', '.join(missing)}")
```

**Rationale**: Centralizes validation, improves error messages, reduces code duplication.

---

### RQ-006: UUID Parsing Error Handling

**Question**: How should invalid UUID format errors be handled?

**Finding**: UUID parsing can fail with `ValueError` when the format is invalid.

**Current Implementation**:
```python
todo = session.exec(select(Todo).where(Todo.id == UUID(task_id), ...))
```

**Risk**: `UUID(task_id)` throws `ValueError` if `task_id` is not a valid UUID format.

**Decision**: Wrap UUID parsing in try-except with user-friendly error message:
```python
try:
    task_uuid = UUID(task_id)
except ValueError:
    return create_error_response(f"Invalid task ID format: '{task_id}'")
```

**Rationale**: Provides actionable feedback instead of cryptic error.

---

## Summary of Decisions

| Topic | Decision | Impact |
|-------|----------|--------|
| TextContent | Add `type="text"` to all instances | Fixes root cause |
| Error Handling | Layered try-except with specific handlers | Improves reliability |
| Error Codes | JSON-RPC 2.0 standard codes | Protocol compliance |
| Logging | Structured logging with sanitization | Better debugging |
| Validation | Early validation with clear messages | Better UX |
| UUID Parsing | Explicit try-except wrapper | Prevents crashes |

## Implementation Priority

1. **P0 (Critical)**: Fix TextContent `type` parameter (blocks all functionality)
2. **P1 (High)**: Add tool-level error handling with try-except
3. **P1 (High)**: Implement argument validation
4. **P2 (Medium)**: Enhance logging with structured context
5. **P2 (Medium)**: Add UUID parsing protection
6. **P3 (Low)**: Add correlation IDs for request tracing
