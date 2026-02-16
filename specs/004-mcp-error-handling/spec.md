# Feature Specification: MCP Server Error Handling & Validation Fix

**Feature Branch**: `004-mcp-error-handling`
**Created**: 2026-01-29
**Status**: Draft
**Input**: User description: "Create specs for MCP fix with proper error handling, code validation, analysis, error logging, and try-except handling"

## Problem Statement

The MCP (Model Context Protocol) server integration is failing due to a Pydantic validation error in `TextContent` objects. The `type` field is required but not being provided, causing tool calls to fail silently and the MCP client to timeout after 5 seconds. This results in 500 Internal Server Errors on the chat API endpoint, completely breaking the AI-powered task management functionality.

**Root Cause**: The MCP SDK's `TextContent` class requires an explicit `type="text"` parameter that is currently missing from all tool response constructions.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Task Creation via Chat (Priority: P1)

A user sends a chat message asking to add a new task (e.g., "Add a task called deploy backend"). The system should process this request through the AI agent, which calls the MCP server's `add_task` tool, successfully creates the task in the database, and returns a confirmation message to the user.

**Why this priority**: This is the primary functionality that is currently broken. Users cannot create tasks via the chat interface, which is the core value proposition of the AI-powered todo application.

**Independent Test**: Can be fully tested by sending a chat message to add a task and verifying both the response message and database entry.

**Acceptance Scenarios**:

1. **Given** a user is authenticated and has an active chat session, **When** they send "Add a task called deploy backend", **Then** they receive a confirmation message within 10 seconds containing the task title and ID.
2. **Given** a user sends a task creation request, **When** the MCP tool executes successfully, **Then** the task appears in the user's task list with the correct title and user_id.
3. **Given** a user sends a task creation request with a description, **When** the request is processed, **Then** both title and description are saved correctly.

---

### User Story 2 - Graceful Error Handling (Priority: P1)

When an error occurs during MCP tool execution (database unavailable, validation failure, etc.), the system should catch the error, log detailed diagnostic information, and return a user-friendly error message instead of crashing with a 500 error.

**Why this priority**: Critical for system reliability. Users should never see raw stack traces or experience unhandled crashes.

**Independent Test**: Can be tested by simulating error conditions (invalid input, missing fields) and verifying error responses are user-friendly.

**Acceptance Scenarios**:

1. **Given** the MCP tool receives invalid arguments, **When** validation fails, **Then** a structured error response is returned with a clear message explaining the issue.
2. **Given** a database operation fails during tool execution, **When** the error is caught, **Then** the error details are logged with timestamp, tool name, and context.
3. **Given** any unhandled exception occurs in tool execution, **When** the error propagates, **Then** users receive a generic "operation failed" message without exposing internal details.

---

### User Story 3 - Task Listing and Stats (Priority: P2)

A user can request their task statistics or full task list via chat. The system retrieves data from the database and returns properly formatted responses.

**Why this priority**: Essential for users to view their tasks, but secondary to task creation which is completely broken.

**Independent Test**: Can be tested by requesting task list/stats and verifying the response format and data accuracy.

**Acceptance Scenarios**:

1. **Given** a user has 3 pending and 2 completed tasks, **When** they ask for stats, **Then** they receive "Pending tasks: 3, Completed tasks: 2".
2. **Given** a user has no tasks, **When** they request their task list, **Then** they receive "No tasks found."
3. **Given** a user has multiple tasks, **When** they request their list, **Then** each task shows title, ID, and completion status.

---

### User Story 4 - Task Operations (Update, Delete, Complete) (Priority: P2)

Users can update task details, delete tasks, and mark tasks as complete via chat commands processed through the MCP server.

**Why this priority**: Important task management features, but users can work around these by using direct API endpoints.

**Independent Test**: Can be tested by performing each operation and verifying the database state changes.

**Acceptance Scenarios**:

1. **Given** a task exists with ID "abc-123", **When** user requests to complete it, **Then** the task's is_complete field is set to True.
2. **Given** a task exists, **When** user requests to delete it, **Then** the task is removed from the database.
3. **Given** a task exists, **When** user requests to update its title, **Then** the title is changed and confirmed.
4. **Given** a non-existent task ID, **When** user requests any operation, **Then** they receive "Task with ID 'xxx' not found."

---

### User Story 5 - Error Logging and Diagnostics (Priority: P3)

System administrators can review detailed error logs to diagnose issues. Logs include timestamps, request context, error types, and stack traces for debugging.

**Why this priority**: Important for maintenance but not user-facing functionality.

**Independent Test**: Can be tested by triggering errors and verifying log output contains required diagnostic information.

**Acceptance Scenarios**:

1. **Given** an error occurs during MCP request handling, **When** the error is logged, **Then** the log entry contains: timestamp, method name, error type, error message.
2. **Given** a tool call fails, **When** the error is logged, **Then** the log includes the tool name, arguments (sanitized), and user context.
3. **Given** multiple errors occur, **When** reviewing logs, **Then** each error has a unique correlation ID for tracing.

---

### Edge Cases

- What happens when the MCP server receives malformed JSON in the request body?
- How does the system handle database connection timeouts during tool execution?
- What happens when a user_id is missing from a tool call that requires it?
- How does the system respond when the TextContent text is empty or None?
- What happens when UUID parsing fails for task_id arguments?
- How does the system handle concurrent requests modifying the same task?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST include the `type="text"` parameter in all `TextContent` object constructions to satisfy Pydantic validation requirements.
- **FR-002**: System MUST wrap all tool execution code in try-except blocks to catch and handle exceptions gracefully.
- **FR-003**: System MUST return structured JSON-RPC error responses when tool execution fails, with appropriate error codes.
- **FR-004**: System MUST log all errors with sufficient context for debugging (timestamp, tool name, error type, message, sanitized arguments).
- **FR-005**: System MUST validate required arguments (user_id, title, task_id) before attempting database operations.
- **FR-006**: System MUST return user-friendly error messages that do not expose internal implementation details or stack traces.
- **FR-007**: System MUST handle malformed requests (invalid JSON, missing fields) with appropriate 400-level error responses.
- **FR-008**: System MUST sanitize logged data to exclude sensitive information (passwords, tokens).
- **FR-009**: System MUST provide consistent error response format across all MCP tools.
- **FR-010**: System MUST continue operating when individual tool calls fail (no cascading failures).

### Key Entities

- **MCP Tool Response**: Contains content array with TextContent objects, each having type and text fields
- **Error Log Entry**: Contains timestamp, log level, tool name, error type, message, and sanitized context
- **JSON-RPC Error**: Contains error code, error message, and optional data field for additional context

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Chat API requests that trigger MCP tool calls complete successfully within 10 seconds (down from timeout at 5+ seconds).
- **SC-002**: 100% of MCP tool calls return valid responses (no Pydantic validation errors).
- **SC-003**: Error responses are returned within 2 seconds (no waiting for timeout).
- **SC-004**: All error scenarios return user-friendly messages without exposing stack traces or internal paths.
- **SC-005**: System administrators can identify the root cause of any error from logs within 5 minutes.
- **SC-006**: Zero 500 Internal Server Errors caused by MCP TextContent validation failures.
- **SC-007**: All 10 TextContent instances in the codebase include the required type parameter.

## Assumptions

- The MCP Python SDK version in use requires the explicit `type` parameter for TextContent (confirmed by error analysis).
- Logging infrastructure (Python's logging module) is already configured and available.
- Database operations may fail independently of MCP protocol issues.
- The 5-second MCP client timeout is a reasonable default and does not need adjustment if tools respond properly.
- Error codes will follow JSON-RPC 2.0 specification (-32600 to -32603 for standard errors).

## Out of Scope

- Changes to the MCP client timeout configuration.
- Modifications to the AI agent logic or prompt engineering.
- Database schema changes or migrations.
- Performance optimization beyond fixing the validation error.
- Adding new MCP tools or capabilities.
- Frontend changes or error display improvements.

## Dependencies

- MCP Python SDK (`mcp.types.TextContent`)
- Python logging module
- FastAPI exception handling
- Existing database session management

## Risks

- **Risk 1**: Other undiscovered Pydantic validation issues may exist in the codebase.
  - *Mitigation*: Comprehensive testing of all MCP tools after the fix.
- **Risk 2**: Error logging may impact performance if too verbose.
  - *Mitigation*: Use appropriate log levels (ERROR for failures, DEBUG for detailed context).
- **Risk 3**: User-friendly error messages may obscure debugging information.
  - *Mitigation*: Log detailed information server-side while returning sanitized messages to users.
