"""
Unit Tests for TodoManager Service

Task ID: T013-T014 (Create unit tests for TodoManager)
Spec: specs/001-cli-todo/spec.md (FR-003 through FR-009)
Implementation: src/todo_app/services/todo_manager.py

Tests cover:
- CRUD operations (create, read, update, delete)
- Auto-incrementing ID generation
- Task validation
- Error handling for invalid operations
- List operations
"""

import pytest
from src.todo_app.models.task import Task
from src.todo_app.services.todo_manager import TodoManager


class TestTodoManagerCreation:
    """Test TodoManager CRUD create operations."""

    def test_create_task_basic(self):
        """Test creating a task with required fields only."""
        manager = TodoManager()
        task = manager.create_task(title="Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.is_complete is False

    def test_create_task_with_description(self):
        """Test creating a task with title and description."""
        manager = TodoManager()
        task = manager.create_task(title="Test", description="Test Description")

        assert task.id == 1
        assert task.title == "Test"
        assert task.description == "Test Description"

    def test_create_task_empty_title_raises(self):
        """Test that creating task with empty title raises ValueError."""
        manager = TodoManager()
        with pytest.raises(ValueError):
            manager.create_task(title="")

    def test_create_multiple_tasks(self):
        """Test creating multiple tasks with auto-incremented IDs."""
        manager = TodoManager()
        task1 = manager.create_task(title="Task 1")
        task2 = manager.create_task(title="Task 2")
        task3 = manager.create_task(title="Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_create_task_returns_task_object(self):
        """Test that create_task returns a Task object."""
        manager = TodoManager()
        task = manager.create_task(title="Test")
        assert isinstance(task, Task)


class TestTodoManagerRead:
    """Test TodoManager CRUD read operations."""

    def test_get_all_tasks_empty(self):
        """Test getting all tasks from empty manager."""
        manager = TodoManager()
        tasks = manager.get_all_tasks()

        assert isinstance(tasks, list)
        assert len(tasks) == 0

    def test_get_all_tasks_returns_copy(self):
        """Test that get_all_tasks returns a copy, not reference."""
        manager = TodoManager()
        manager.create_task(title="Task 1")

        tasks1 = manager.get_all_tasks()
        tasks1.clear()  # Clear the returned list
        tasks2 = manager.get_all_tasks()

        # Original manager should still have task
        assert len(tasks2) == 1

    def test_get_all_tasks_insertion_order(self):
        """Test that get_all_tasks returns tasks in insertion order."""
        manager = TodoManager()
        task1 = manager.create_task(title="First")
        task2 = manager.create_task(title="Second")
        task3 = manager.create_task(title="Third")

        tasks = manager.get_all_tasks()
        assert tasks[0].id == 1
        assert tasks[1].id == 2
        assert tasks[2].id == 3

    def test_get_task_by_id(self):
        """Test retrieving specific task by ID."""
        manager = TodoManager()
        created = manager.create_task(title="Test")
        retrieved = manager.get_task(1)

        assert retrieved is not None
        assert retrieved.id == created.id
        assert retrieved.title == created.title

    def test_get_task_not_found(self):
        """Test that get_task returns None for non-existent ID."""
        manager = TodoManager()
        task = manager.get_task(999)
        assert task is None

    def test_get_task_finds_correct_task(self):
        """Test that get_task finds correct task among multiple."""
        manager = TodoManager()
        manager.create_task(title="Task 1")
        created = manager.create_task(title="Task 2")
        manager.create_task(title="Task 3")

        retrieved = manager.get_task(2)
        assert retrieved.title == "Task 2"


class TestTodoManagerUpdate:
    """Test TodoManager CRUD update operations."""

    def test_update_task_title_only(self):
        """Test updating only task title."""
        manager = TodoManager()
        manager.create_task(title="Original", description="Desc")

        updated = manager.update_task(task_id=1, title="Updated")
        assert updated.title == "Updated"
        assert updated.description == "Desc"  # Unchanged

    def test_update_task_description_only(self):
        """Test updating only task description."""
        manager = TodoManager()
        manager.create_task(title="Title", description="Original")

        updated = manager.update_task(task_id=1, description="Updated")
        assert updated.title == "Title"  # Unchanged
        assert updated.description == "Updated"

    def test_update_task_both_fields(self):
        """Test updating both title and description."""
        manager = TodoManager()
        manager.create_task(title="Original Title", description="Original Desc")

        updated = manager.update_task(
            task_id=1,
            title="New Title",
            description="New Desc"
        )
        assert updated.title == "New Title"
        assert updated.description == "New Desc"

    def test_update_task_not_found(self):
        """Test that updating non-existent task raises ValueError."""
        manager = TodoManager()
        with pytest.raises(ValueError, match="Task 999 not found"):
            manager.update_task(task_id=999, title="New Title")

    def test_update_task_empty_title_raises(self):
        """Test that updating to empty title raises ValueError."""
        manager = TodoManager()
        manager.create_task(title="Original")

        with pytest.raises(ValueError):
            manager.update_task(task_id=1, title="")

    def test_update_preserves_complete_status(self):
        """Test that update preserves completion status."""
        manager = TodoManager()
        manager.create_task(title="Task")
        manager.mark_complete(task_id=1, is_complete=True)

        updated = manager.update_task(task_id=1, title="Updated")
        assert updated.is_complete is True


class TestTodoManagerMarkComplete:
    """Test TodoManager mark complete operations."""

    def test_mark_task_complete(self):
        """Test marking task as complete."""
        manager = TodoManager()
        manager.create_task(title="Task")

        updated = manager.mark_complete(task_id=1, is_complete=True)
        assert updated.is_complete is True

    def test_mark_task_incomplete(self):
        """Test marking task as incomplete."""
        manager = TodoManager()
        manager.create_task(title="Task")
        manager.mark_complete(task_id=1, is_complete=True)

        updated = manager.mark_complete(task_id=1, is_complete=False)
        assert updated.is_complete is False

    def test_toggle_complete_default(self):
        """Test mark_complete with default parameter."""
        manager = TodoManager()
        manager.create_task(title="Task")

        updated = manager.mark_complete(task_id=1)  # Default is_complete=True
        assert updated.is_complete is True

    def test_mark_task_not_found(self):
        """Test that marking non-existent task raises ValueError."""
        manager = TodoManager()
        with pytest.raises(ValueError, match="Task 999 not found"):
            manager.mark_complete(task_id=999)

    def test_mark_complete_preserves_title_description(self):
        """Test that mark_complete preserves title and description."""
        manager = TodoManager()
        manager.create_task(title="Test Title", description="Test Desc")

        updated = manager.mark_complete(task_id=1, is_complete=True)
        assert updated.title == "Test Title"
        assert updated.description == "Test Desc"


class TestTodoManagerDelete:
    """Test TodoManager CRUD delete operations."""

    def test_delete_task_success(self):
        """Test deleting an existing task."""
        manager = TodoManager()
        manager.create_task(title="Task to Delete")

        result = manager.delete_task(task_id=1)
        assert result is True

        # Verify task is gone
        remaining = manager.get_all_tasks()
        assert len(remaining) == 0

    def test_delete_task_not_found(self):
        """Test that deleting non-existent task returns False."""
        manager = TodoManager()
        result = manager.delete_task(task_id=999)
        assert result is False

    def test_delete_removes_correct_task(self):
        """Test that delete removes correct task from multiple."""
        manager = TodoManager()
        manager.create_task(title="Task 1")
        manager.create_task(title="Task 2")
        manager.create_task(title="Task 3")

        manager.delete_task(task_id=2)

        remaining = manager.get_all_tasks()
        assert len(remaining) == 2
        assert remaining[0].id == 1
        assert remaining[1].id == 3

    def test_delete_doesnt_reuse_id(self):
        """Test that deleting a task doesn't reuse its ID."""
        manager = TodoManager()
        manager.create_task(title="Task 1")
        manager.create_task(title="Task 2")
        manager.delete_task(task_id=1)

        new_task = manager.create_task(title="Task 3")
        assert new_task.id == 3  # Not reusing 1


class TestTodoManagerIntegration:
    """Test TodoManager with integrated operations."""

    def test_full_lifecycle(self):
        """Test full lifecycle: create, read, update, mark, delete."""
        manager = TodoManager()

        # Create
        task1 = manager.create_task(title="Task 1", description="Desc 1")
        assert task1.id == 1

        # Read all
        all_tasks = manager.get_all_tasks()
        assert len(all_tasks) == 1

        # Update
        updated = manager.update_task(task_id=1, title="Updated Task 1")
        assert updated.title == "Updated Task 1"

        # Mark complete
        marked = manager.mark_complete(task_id=1, is_complete=True)
        assert marked.is_complete is True

        # Read again
        retrieved = manager.get_task(1)
        assert retrieved.title == "Updated Task 1"
        assert retrieved.is_complete is True

        # Delete
        deleted = manager.delete_task(task_id=1)
        assert deleted is True
        assert len(manager.get_all_tasks()) == 0

    def test_multiple_tasks_operations(self):
        """Test operations on multiple tasks."""
        manager = TodoManager()

        # Create 3 tasks
        for i in range(1, 4):
            manager.create_task(title=f"Task {i}")

        # Mark first and third complete
        manager.mark_complete(task_id=1, is_complete=True)
        manager.mark_complete(task_id=3, is_complete=True)

        # Update second
        manager.update_task(task_id=2, description="Description added")

        # Delete second
        manager.delete_task(task_id=2)

        # Verify final state
        final = manager.get_all_tasks()
        assert len(final) == 2
        assert final[0].id == 1
        assert final[0].is_complete is True
        assert final[1].id == 3
        assert final[1].is_complete is True
