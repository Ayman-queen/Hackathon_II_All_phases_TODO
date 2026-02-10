import asyncio
import json
import mcp.types as types
from mcp.server import Server
from app.models.todo import Todo
from app.models.database import Session, engine
from typing import List, Optional
from uuid import UUID
from sqlmodel import select
import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
import logging

from app.core.config import settings

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =============================================================================
# Helper Functions (Phase 3-6 Implementation)
# =============================================================================

def create_text_response(message: str) -> list[types.TextContent]:
    """Create a properly formatted TextContent response with required type field."""
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
    """Validate that required arguments are present and non-empty.

    Raises:
        ValueError: If any required argument is missing or empty.
    """
    missing = [arg for arg in required if not arguments.get(arg)]
    if missing:
        raise ValueError(f"Missing required arguments for {tool_name}: {', '.join(missing)}")


def parse_uuid_safe(value: str, field_name: str) -> UUID:
    """Parse UUID with user-friendly error message.

    Args:
        value: The string value to parse as UUID.
        field_name: Name of the field for error messages.

    Returns:
        UUID: The parsed UUID object.

    Raises:
        ValueError: If the value is not a valid UUID format.
    """
    try:
        return UUID(value)
    except ValueError:
        raise ValueError(f"Invalid {field_name} format: '{value}' is not a valid UUID")


# =============================================================================
# MCP Server Setup
# =============================================================================

# Create the MCP Server instance
mcp_server = Server("Todo MCP Server")


@mcp_server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="get_user_stats",
            description="Get user task stats (pending/completed).",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        ),
        types.Tool(
            name="add_task",
            description="Adds a new task to the database. Automatically checks for duplicates using case-insensitive title matching.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The title of the task."},
                    "description": {"type": "string", "description": "The description of the task."}
                },
                "required": ["title"]
            }
        ),
        types.Tool(
            name="check_duplicate_task",
            description="Check if a similar task already exists (case-insensitive, whitespace-trimmed). Use this before creating a task.",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "The title to check for duplicates."}
                },
                "required": ["title"]
            }
        ),
        types.Tool(
            name="list_tasks",
            description="Lists all tasks for a user.",
            inputSchema={
                "type": "object",
                "properties": {},
            }
        ),
        types.Tool(
            name="update_task",
            description="Updates a task.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "The ID of the task."},
                    "title": {"type": "string", "description": "The new title of the task."},
                    "description": {"type": "string", "description": "The new description of the task."},
                    "is_complete": {"type": "boolean", "description": "The new completion status of the task."}
                },
                "required": ["task_id"]
            }
        ),
        types.Tool(
            name="delete_task",
            description="Deletes a task.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "The ID of the task."}
                },
                "required": ["task_id"]
            }
        ),
        types.Tool(
            name="complete_task",
            description="Marks a task as completed.",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "The ID of the task to mark as complete."}
                },
                "required": ["task_id"]
            }
        ),
    ]


@mcp_server.call_tool()
async def call_tool(name: str, arguments: dict, user_id: str) -> list[types.TextContent]:
    """Execute MCP tool calls with proper validation and error handling."""
    if name == "get_user_stats":
        with Session(engine) as session:
            pending = len(session.exec(select(Todo).where(Todo.user_id == user_id, Todo.is_complete == False)).all())
            completed = len(session.exec(select(Todo).where(Todo.user_id == user_id, Todo.is_complete == True)).all())
            return create_text_response(f"Pending tasks: {pending}, Completed tasks: {completed}")

    elif name == "check_duplicate_task":
        # T006: Check for duplicate tasks (case-insensitive, whitespace-trimmed)
        validate_required_args(arguments, ["title"], "check_duplicate_task")
        title = arguments["title"].strip().lower()

        with Session(engine) as session:
            # Get all user's tasks and compare case-insensitively
            todos = session.exec(select(Todo).where(Todo.user_id == user_id)).all()
            for todo in todos:
                if todo.title.strip().lower() == title:
                    return create_text_response(
                        f"DUPLICATE FOUND: A task with similar title already exists: '{todo.title}' (ID: {todo.id}, Completed: {todo.is_complete})"
                    )
            return create_text_response("NO DUPLICATE: No similar task found. Safe to create.")

    elif name == "add_task":
        validate_required_args(arguments, ["title"], "add_task")
        title = arguments["title"]
        description = arguments.get("description")

        if not title or not title.strip():
            raise ValueError("Title is required and cannot be empty or whitespace only.")
        if len(title) > 500:
            raise ValueError("Title must be 500 characters or less.")
        if description and len(description) > 2000:
            raise ValueError("Description must be 2000 characters or less.")

        with Session(engine) as session:
            # T006: Check for duplicates before creating
            normalized_title = title.strip().lower()
            existing_todos = session.exec(select(Todo).where(Todo.user_id == user_id)).all()
            for existing in existing_todos:
                if existing.title.strip().lower() == normalized_title:
                    return create_text_response(
                        f"Task not created - a similar task already exists: '{existing.title}' (ID: {existing.id}). "
                        f"Use update_task to modify it or delete_task to remove it first."
                    )

            todo = Todo(user_id=user_id, title=title.strip(), description=description.strip() if description else None)
            session.add(todo)
            session.commit()
            session.refresh(todo)
            return create_text_response(f"Task '{todo.title}' added with ID: {todo.id}")

    elif name == "list_tasks":
        with Session(engine) as session:
            todos = session.exec(select(Todo).where(Todo.user_id == user_id)).all()
            if not todos:
                return create_text_response("No tasks found.")
            task_list = "\n".join([f"- {t.title} (ID: {t.id}, Completed: {t.is_complete})" for t in todos])
            return create_text_response(f"Your tasks:\n{task_list}")

    elif name == "update_task":
        validate_required_args(arguments, ["task_id"], "update_task")
        task_uuid = parse_uuid_safe(arguments["task_id"], "task_id")
        title = arguments.get("title")
        description = arguments.get("description")
        is_complete = arguments.get("is_complete")
        with Session(engine) as session:
            todo = session.exec(select(Todo).where(Todo.id == task_uuid, Todo.user_id == user_id)).first()
            if todo:
                if title is not None:
                    todo.title = title
                if description is not None:
                    todo.description = description
                if is_complete is not None:
                    todo.is_complete = is_complete
                session.add(todo)
                session.commit()
                session.refresh(todo)
                return create_text_response(f"Task '{todo.id}' updated.")
            return create_text_response(f"Task with ID '{arguments['task_id']}' not found.")

    elif name == "delete_task":
        validate_required_args(arguments, ["task_id"], "delete_task")
        task_uuid = parse_uuid_safe(arguments["task_id"], "task_id")
        with Session(engine) as session:
            todo = session.exec(select(Todo).where(Todo.id == task_uuid, Todo.user_id == user_id)).first()
            if todo:
                session.delete(todo)
                session.commit()
                return create_text_response(f"Task '{arguments['task_id']}' deleted.")
            return create_text_response(f"Task with ID '{arguments['task_id']}' not found.")

    elif name == "complete_task":
        validate_required_args(arguments, ["task_id"], "complete_task")
        task_uuid = parse_uuid_safe(arguments["task_id"], "task_id")
        with Session(engine) as session:
            todo = session.exec(select(Todo).where(Todo.id == task_uuid, Todo.user_id == user_id)).first()
            if todo:
                todo.is_complete = True
                session.add(todo)
                session.commit()
                session.refresh(todo)
                return create_text_response(f"Task '{todo.title}' marked as completed.")
            return create_text_response(f"Task with ID '{arguments['task_id']}' not found.")

    raise ValueError(f"Tool not found: {name}")


# Create a FastAPI app instance to host the MCP server as HTTP
mcp_host_app = FastAPI(
    title="Todo MCP Host",
    description="Hosts the MCP Server instance via HTTP",
    version="1.0.0",
)


def get_user_id_from_header(request: Request) -> str:
    """
    Extract user_id from trusted internal X-User-ID header.

    Security: This endpoint should only be called by the main app (same backend)
    which has already validated the JWT. The X-User-ID header is set by the
    agent after JWT validation in /api/chat endpoint.

    For additional security, validate the internal secret token.
    """
    # Validate internal secret to ensure request comes from trusted source
    internal_secret = request.headers.get("X-Internal-Secret")
    if internal_secret != settings.MCP_INTERNAL_SECRET:
        raise ValueError("Invalid internal secret")

    user_id = request.headers.get("X-User-ID")
    if not user_id or not user_id.strip():
        raise ValueError("Missing X-User-ID header")

    return user_id.strip()


@mcp_host_app.post("/mcp")
async def handle_mcp_request(request: Request):
    """
    Handle MCP protocol requests via HTTP using JSON-RPC format.

    Authentication: Uses trusted internal X-User-ID header instead of JWT.
    The main /api/chat endpoint validates the JWT and passes user_id via header.
    An internal secret token ensures only trusted sources can call this endpoint.

    Implements proper error handling with JSON-RPC 2.0 compliant error codes:
    - -32700: Parse error (malformed JSON)
    - -32600: Invalid Request (missing required fields)
    - -32601: Method not found
    - -32602: Invalid params (validation errors)
    - -32603: Internal error (unexpected exceptions)
    """
    request_id = None
    try:
        # Extract user_id from trusted internal header
        try:
            user_id = get_user_id_from_header(request)
        except ValueError as e:
            logger.warning(f"Authentication failed: {e}")
            return create_error_response(-32600, "Unauthorized: " + str(e), None)

        body = await request.json()
        request_id = body.get("id")

        method = body.get("method")
        params = body.get("params", {})

        # Structured logging with sanitized context (Phase 7: T037, T040)
        tool_name = params.get("name", "N/A") if method == "tools/call" else "N/A"
        logger.info(f"MCP request: method={method}, tool={tool_name}, user_id={user_id}")

        # Handle MCP protocol methods
        if method == "initialize":
            # Initialize request - return server capabilities
            result = {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "Todo MCP Server",
                    "version": "1.0.0"
                }
            }
            return JSONResponse({
                "jsonrpc": "2.0",
                "result": result,
                "id": request_id
            })

        elif method == "tools/list":
            tools = await list_tools()
            # Convert tool objects to dictionaries for JSON serialization
            tools_data = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "inputSchema": tool.inputSchema
                }
                for tool in tools
            ]
            return JSONResponse({
                "jsonrpc": "2.0",
                "result": {"tools": tools_data},
                "id": request_id
            })

        elif method == "tools/call":
            tool_name = params.get("name")

            # Validate tool name is provided (Phase 4: T025)
            if not tool_name:
                return create_error_response(-32602, "Missing tool name", request_id)

            try:
                result = await call_tool(tool_name, params.get("arguments", {}), user_id=user_id)
                # Convert TextContent objects to text
                result_text = result[0].text if result else ""
                # Success logging (Phase 7: T038)
                logger.info(f"Tool '{tool_name}' executed successfully for user {user_id}")
                return JSONResponse({
                    "jsonrpc": "2.0",
                    "result": {"content": [{"type": "text", "text": result_text}]},
                    "id": request_id
                })
            except ValueError as e:
                # Validation errors: missing args, invalid UUID, etc. (Phase 4: T023)
                logger.warning(f"Validation error in tool '{tool_name}': {e}")
                return create_error_response(-32602, str(e), request_id)
            except Exception as e:
                # Unexpected errors: database failures, etc. (Phase 4: T024)
                logger.error(f"Tool execution failed: {tool_name}", exc_info=True)
                return create_error_response(-32603, "Internal server error", request_id)

        elif method == "notifications/initialized":
            logger.info("MCP client initialized.")
            return JSONResponse({}, status_code=204)

        else:
            logger.warning(f"Unknown MCP method: {method}")
            return create_error_response(-32601, f"Method not found: {method}", request_id)

    except json.JSONDecodeError as e:
        # Malformed JSON (Phase 4: T022 edge case)
        logger.error(f"JSON parse error: {e}")
        return create_error_response(-32700, "Parse error: Invalid JSON", request_id)

    except Exception as e:
        # Catch-all for unexpected errors (Phase 4: T024)
        logger.error(f"Error handling MCP request: {str(e)}", exc_info=True)
        return JSONResponse({
            "jsonrpc": "2.0",
            "error": {"code": -32603, "message": "Internal server error"},
            "id": request_id
        }, status_code=200)


@mcp_host_app.get("/health")
async def health_check():
    """Health check endpoint for the MCP server."""
    return {"status": "healthy", "service": "Todo MCP Server"}


if __name__ == "__main__":
    uvicorn.run(mcp_host_app, host="0.0.0.0", port=8001)
