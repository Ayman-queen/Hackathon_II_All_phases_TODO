# Data Model: MCP Error Handling

**Feature**: 004-mcp-error-handling
**Date**: 2026-01-29

## Overview

This feature does not introduce new database entities. It focuses on the structure of MCP protocol messages, error responses, and logging formats.

## MCP Protocol Structures

### TextContent (MCP SDK Type)

The core type that requires fixing. Part of `mcp.types`.

```
TextContent
├── type: str = "text"  (REQUIRED - was missing)
└── text: str           (the message content)
```

**Validation Rules**:
- `type` must be exactly `"text"` (discriminator field)
- `text` must be a non-null string

### Tool Response Format

Standard MCP tool response structure:

```
ToolResponse (JSON-RPC)
├── jsonrpc: "2.0"
├── id: str | int (request correlation)
└── result:
    └── content: [TextContent, ...]
```

### Error Response Format

JSON-RPC 2.0 compliant error structure:

```
ErrorResponse
├── jsonrpc: "2.0"
├── id: str | int | null
└── error:
    ├── code: int (JSON-RPC error code)
    ├── message: str (user-friendly description)
    └── data: object | null (optional additional context)
```

## Error Code Mapping

| Code | Name | Trigger Condition |
|------|------|-------------------|
| -32700 | Parse Error | Malformed JSON in request body |
| -32600 | Invalid Request | Missing `method` or `jsonrpc` fields |
| -32601 | Method Not Found | Unknown MCP method name |
| -32602 | Invalid Params | Missing required arguments, invalid UUID format |
| -32603 | Internal Error | Database failures, unexpected exceptions |

## Log Entry Structure

Structured log entries for debugging:

```
LogEntry
├── timestamp: ISO 8601 datetime
├── level: INFO | WARNING | ERROR
├── logger: str (module name)
├── message: str (human-readable description)
├── context:
│   ├── method: str (MCP method name)
│   ├── tool: str | null (tool name if applicable)
│   ├── error_type: str | null (exception class name)
│   ├── request_id: str | null (JSON-RPC request ID)
│   └── user_id_present: bool (sanitized - not the actual ID)
```

## State Transitions

This feature does not introduce state machines. Tool operations remain atomic with existing patterns.

## Relationships

```
MCP Request → Tool Dispatch → Database Operation → TextContent Response
                    │
                    └─ Error → JSON-RPC Error Response + Log Entry
```

## Existing Entities (Unchanged)

### Todo (Existing)

Referenced by MCP tools but not modified:

```
Todo
├── id: UUID (primary key)
├── user_id: str (scoped access)
├── title: str
├── description: str | null
├── is_complete: bool
├── created_at: datetime
└── updated_at: datetime
```

## Migration Requirements

**None** - This feature only modifies runtime behavior, not persisted data structures.
