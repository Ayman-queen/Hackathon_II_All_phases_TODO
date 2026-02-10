"""
Unit tests for MCP Server - Phase 8 Implementation

Tests cover:
- T043: TextContent type field validation
- T044: add_task success scenarios
- T045: add_task missing title error
- T046: add_task missing user_id error
- T047: update_task invalid UUID error
- T048: Unknown tool error
- T049: Unknown MCP method error
"""

import pytest
import json
from unittest.mock import patch, MagicMock, AsyncMock
from uuid import uuid4

# Import the modules under test
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_server.server import (
    create_text_response,
    create_error_response,
    validate_required_args,
    parse_uuid_safe,
    call_tool,
    handle_mcp_request,
    mcp_host_app,
)
from fastapi.testclient import TestClient
import mcp.types as types


# =============================================================================
# T043: Test TextContent has type field
# =============================================================================

class TestTextContentTypeField:
    """Verify all responses include type='text' in TextContent."""

    def test_create_text_response_has_type_field(self):
        """T043: Verify create_text_response includes type='text'."""
        result = create_text_response("Test message")
        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        assert result[0].type == "text"
        assert result[0].text == "Test message"

    def test_create_text_response_empty_message(self):
        """T043: Verify empty messages still have type field."""
        result = create_text_response("")
        assert result[0].type == "text"
        assert result[0].text == ""


# =============================================================================
# T044: Test add_task success
# =============================================================================

class TestAddTaskSuccess:
    """Test successful task creation scenarios."""

    @pytest.mark.asyncio
    @patch('mcp_server.server.Session')
    async def test_add_task_success(self, mock_session_class):
        """T044: Valid task creation returns success message."""
        # Setup mock
        mock_session = MagicMock()
        mock_session_class.return_value.__enter__ = MagicMock(return_value=mock_session)
        mock_session_class.return_value.__exit__ = MagicMock(return_value=False)

        mock_todo = MagicMock()
        mock_todo.title = "Test Task"
        mock_todo.id = uuid4()
        mock_session.refresh = MagicMock(side_effect=lambda x: setattr(x, 'id', mock_todo.id))

        # Execute
        result = await call_tool("add_task", {
            "user_id": "test-user",
            "title": "Test Task",
            "description": "Test description"
        })

        # Verify
        assert len(result) == 1
        assert result[0].type == "text"
        assert "Test Task" in result[0].text
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()


# =============================================================================
# T045: Test add_task missing title
# =============================================================================

class TestAddTaskMissingTitle:
    """Test add_task validation for missing title."""

    @pytest.mark.asyncio
    async def test_add_task_missing_title_raises_error(self):
        """T045: Missing title returns -32602 error."""
        with pytest.raises(ValueError) as exc_info:
            await call_tool("add_task", {
                "user_id": "test-user"
                # title is missing
            })
        assert "Missing required arguments" in str(exc_info.value)
        assert "title" in str(exc_info.value)


# =============================================================================
# T046: Test add_task missing user_id
# =============================================================================

class TestAddTaskMissingUserId:
    """Test add_task validation for missing user_id."""

    @pytest.mark.asyncio
    async def test_add_task_missing_user_id_raises_error(self):
        """T046: Missing user_id returns -32602 error."""
        with pytest.raises(ValueError) as exc_info:
            await call_tool("add_task", {
                "title": "Test Task"
                # user_id is missing
            })
        assert "Missing required arguments" in str(exc_info.value)
        assert "user_id" in str(exc_info.value)


# =============================================================================
# T047: Test update_task invalid UUID
# =============================================================================

class TestUpdateTaskInvalidUUID:
    """Test update_task validation for invalid UUID format."""

    @pytest.mark.asyncio
    async def test_update_task_invalid_uuid_raises_error(self):
        """T047: Invalid UUID format returns -32602 error."""
        with pytest.raises(ValueError) as exc_info:
            await call_tool("update_task", {
                "user_id": "test-user",
                "task_id": "not-a-valid-uuid",
                "title": "Updated Title"
            })
        assert "Invalid task_id format" in str(exc_info.value)
        assert "not a valid UUID" in str(exc_info.value)


# =============================================================================
# T048: Test unknown tool
# =============================================================================

class TestUnknownTool:
    """Test handling of unknown tool names."""

    @pytest.mark.asyncio
    async def test_unknown_tool_raises_value_error(self):
        """T048: Unknown tool name raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            await call_tool("nonexistent_tool", {
                "user_id": "test-user"
            })
        assert "Tool not found" in str(exc_info.value)
        assert "nonexistent_tool" in str(exc_info.value)


# =============================================================================
# T049: Test unknown MCP method via HTTP
# =============================================================================

class TestUnknownMCPMethod:
    """Test handling of unknown MCP methods via HTTP endpoint."""

    def setup_method(self):
        """Setup test client."""
        self.client = TestClient(mcp_host_app)

    def test_unknown_method_returns_32601_error(self):
        """T049: Unknown MCP method returns -32601 error."""
        response = self.client.post("/mcp", json={
            "jsonrpc": "2.0",
            "method": "unknown/method",
            "params": {},
            "id": 1
        })

        assert response.status_code == 200
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == -32601
        assert "Method not found" in data["error"]["message"]


# =============================================================================
# Additional Helper Function Tests
# =============================================================================

class TestValidateRequiredArgs:
    """Test the validate_required_args helper function."""

    def test_validate_all_present(self):
        """No error when all required args present."""
        # Should not raise
        validate_required_args(
            {"user_id": "test", "title": "Test"},
            ["user_id", "title"],
            "test_tool"
        )

    def test_validate_missing_single_arg(self):
        """Error when single required arg missing."""
        with pytest.raises(ValueError) as exc_info:
            validate_required_args(
                {"user_id": "test"},
                ["user_id", "title"],
                "test_tool"
            )
        assert "title" in str(exc_info.value)

    def test_validate_empty_string_treated_as_missing(self):
        """Empty string values are treated as missing."""
        with pytest.raises(ValueError) as exc_info:
            validate_required_args(
                {"user_id": "", "title": "Test"},
                ["user_id", "title"],
                "test_tool"
            )
        assert "user_id" in str(exc_info.value)


class TestParseUUIDSafe:
    """Test the parse_uuid_safe helper function."""

    def test_parse_valid_uuid(self):
        """Valid UUID string parses correctly."""
        test_uuid = str(uuid4())
        result = parse_uuid_safe(test_uuid, "task_id")
        assert str(result) == test_uuid

    def test_parse_invalid_uuid_raises_error(self):
        """Invalid UUID string raises ValueError with friendly message."""
        with pytest.raises(ValueError) as exc_info:
            parse_uuid_safe("not-a-uuid", "task_id")
        assert "Invalid task_id format" in str(exc_info.value)
        assert "not a valid UUID" in str(exc_info.value)


class TestCreateErrorResponse:
    """Test the create_error_response helper function."""

    def test_error_response_structure(self):
        """Error response has correct JSON-RPC structure."""
        response = create_error_response(-32602, "Test error", 123)
        data = response.body.decode()
        parsed = json.loads(data)

        assert parsed["jsonrpc"] == "2.0"
        assert parsed["error"]["code"] == -32602
        assert parsed["error"]["message"] == "Test error"
        assert parsed["id"] == 123


# =============================================================================
# HTTP Endpoint Integration Tests
# =============================================================================

class TestMCPEndpoint:
    """Integration tests for the /mcp HTTP endpoint."""

    def setup_method(self):
        """Setup test client."""
        self.client = TestClient(mcp_host_app)

    def test_initialize_returns_capabilities(self):
        """Initialize method returns server capabilities."""
        response = self.client.post("/mcp", json={
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {},
            "id": 1
        })

        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert data["result"]["serverInfo"]["name"] == "Todo MCP Server"

    def test_tools_list_returns_tools(self):
        """tools/list method returns available tools."""
        response = self.client.post("/mcp", json={
            "jsonrpc": "2.0",
            "method": "tools/list",
            "params": {},
            "id": 2
        })

        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert "tools" in data["result"]
        tool_names = [t["name"] for t in data["result"]["tools"]]
        assert "add_task" in tool_names
        assert "list_tasks" in tool_names
        assert "get_user_stats" in tool_names

    def test_tools_call_missing_name_returns_32602(self):
        """tools/call without tool name returns -32602."""
        response = self.client.post("/mcp", json={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"arguments": {"user_id": "test"}},
            "id": 3
        })

        assert response.status_code == 200
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == -32602
        assert "Missing tool name" in data["error"]["message"]

    def test_health_check_endpoint(self):
        """Health check endpoint returns healthy status."""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
