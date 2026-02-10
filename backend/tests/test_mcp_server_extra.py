
import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4, UUID
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_server.server import call_tool
from app.models.database import Todo, User
from sqlmodel import Session

# =============================================================================
# Test get_user_stats
# =============================================================================
@pytest.mark.asyncio
@patch('mcp_server.server.Session')
async def test_get_user_stats_success(mock_session_class):
    """Test get_user_stats returns correct task counts."""
    mock_session = MagicMock()
    mock_session_class.return_value.__enter__.return_value = mock_session
    
    user_id = "test-user"
    mock_session.query.return_value.filter.return_value.count.side_effect = [5, 2]  # total, completed

    result = await call_tool("get_user_stats", {"user_id": user_id})

    assert "5 total tasks" in result[0].text
    assert "3 pending" in result[0].text
    assert "2 completed" in result[0].text

# =============================================================================
# Test check_duplicate_task
# =============================================================================
@pytest.mark.asyncio
@patch('mcp_server.server.Session')
async def test_check_duplicate_task_found(mock_session_class):
    """Test check_duplicate_task finds an existing task."""
    mock_session = MagicMock()
    mock_session_class.return_value.__enter__.return_value = mock_session
    
    user_id = "test-user"
    title = "Duplicate Task"
    mock_session.exec.return_value.first.return_value = Todo(id=uuid4(), title=title, user_id=user_id)

    result = await call_tool("check_duplicate_task", {"user_id": user_id, "title": title})

    assert "A similar task already exists" in result[0].text

@pytest.mark.asyncio
@patch('mcp_server.server.Session')
async def test_check_duplicate_task_not_found(mock_session_class):
    """Test check_duplicate_task does not find a task."""
    mock_session = MagicMock()
    mock_session_class.return_value.__enter__.return_value = mock_session
    
    user_id = "test-user"
    title = "New Task"
    mock_session.exec.return_value.first.return_value = None

    result = await call_tool("check_duplicate_task", {"user_id": user_id, "title": title})

    assert "No similar task found" in result[0].text

# =============================================================================
# Test list_tasks
# =============================================================================
@pytest.mark.asyncio
@patch('mcp_server.server.Session')
async def test_list_tasks_success(mock_session_class):
    """Test list_tasks returns a list of tasks."""
    mock_session = MagicMock()
    mock_session_class.return_value.__enter__.return_value = mock_session
    
    user_id = "test-user"
    tasks = [
        Todo(id=uuid4(), title="Task 1", user_id=user_id, is_complete=False),
        Todo(id=uuid4(), title="Task 2", user_id=user_id, is_complete=True),
    ]
    mock_session.exec.return_value.all.return_value = tasks

    result = await call_tool("list_tasks", {"user_id": user_id})

    assert "Task 1" in result[0].text
    assert "Task 2" in result[0].text
    assert "Pending" in result[0].text
    assert "Completed" in result[0].text

# =============================================================================
# Test update_task (success)
# =============================================================================
@pytest.mark.asyncio
@patch('mcp_server.server.Session')
async def test_update_task_success(mock_session_class):
    """Test update_task successfully updates a task."""
    mock_session = MagicMock()
    mock_session_class.return_value.__enter__.return_value = mock_session
    
    user_id = "test-user"
    task_id = uuid4()
    task = Todo(id=task_id, title="Old Title", user_id=user_id)
    mock_session.get.return_value = task

    result = await call_tool("update_task", {"user_id": user_id, "task_id": str(task_id), "title": "New Title"})

    assert "Task updated successfully" in result[0].text
    assert task.title == "New Title"
    mock_session.commit.assert_called_once()

# =============================================================================
# Test delete_task
# =============================================================================
@pytest.mark.asyncio
@patch('mcp_server.server.Session')
async def test_delete_task_success(mock_session_class):
    """Test delete_task successfully deletes a task."""
    mock_session = MagicMock()
    mock_session_class.return_value.__enter__.return_value = mock_session
    
    user_id = "test-user"
    task_id = uuid4()
    task = Todo(id=task_id, title="Task to delete", user_id=user_id)
    mock_session.get.return_value = task

    result = await call_tool("delete_task", {"user_id": user_id, "task_id": str(task_id)})

    assert "Task deleted successfully" in result[0].text
    mock_session.delete.assert_called_once_with(task)
    mock_session.commit.assert_called_once()

# =============================================================================
# Test complete_task
# =============================================================================
@pytest.mark.asyncio
@patch('mcp_server.server.Session')
async def test_complete_task_success(mock_session_class):
    """Test complete_task successfully marks a task as complete."""
    mock_session = MagicMock()
    mock_session_class.return_value.__enter__.return_value = mock_session
    
    user_id = "test-user"
    task_id = uuid4()
    task = Todo(id=task_id, title="Task to complete", user_id=user_id, is_complete=False)
    mock_session.get.return_value = task

    result = await call_tool("complete_task", {"user_id": user_id, "task_id": str(task_id)})

    assert "Task marked as complete" in result[0].text
    assert task.is_complete is True
    mock_session.commit.assert_called_once()
