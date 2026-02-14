"""
Unit Tests for Task Model

Task ID: T009 (Create unit test file for Task)
Spec: specs/001-cli-todo/spec.md (Key Entities: Todo)
Implementation: src/todo_app/models/task.py

Tests cover:
- Task construction with valid inputs
- Title validation (empty, whitespace)
- Properties (id, title, description, is_complete)
- Immutability (read-only properties)
- String representation
"""

import pytest
from src.todo_app.models.task import Task


class TestTaskConstruction:
    """Test Task initialization and validation."""

    def test_create_task_with_all_fields(self):
        """Test creating task with all fields provided."""
        task = Task(id=1, title="Test Task", description="Test Desc", is_complete=True)
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test Desc"
        assert task.is_complete is True

    def test_create_task_with_required_only(self):
        """Test creating task with only required fields (title)."""
        task = Task(id=1, title="Test Task")
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.is_complete is False

    def test_create_task_empty_title_raises(self):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            Task(id=1, title="")

    def test_create_task_whitespace_title_raises(self):
        """Test that whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            Task(id=1, title="   ")

    def test_create_task_with_empty_description(self):
        """Test creating task with empty description string."""
        task = Task(id=1, title="Test", description="")
        assert task.description == ""

    def test_create_task_with_special_characters(self):
        """Test creating task with special characters in title/description."""
        task = Task(
            id=1,
            title="Task with émojis 🎉 and symbols!@#$",
            description="Description with special: <html> & \"quotes\""
        )
        assert "émojis" in task.title
        assert "<html>" in task.description


class TestTaskProperties:
    """Test Task property access (immutability)."""

    def test_id_property_readonly(self):
        """Test that id property is read-only."""
        task = Task(id=1, title="Test")
        with pytest.raises(AttributeError):
            task.id = 2

    def test_title_property_readonly(self):
        """Test that title property is read-only."""
        task = Task(id=1, title="Test")
        with pytest.raises(AttributeError):
            task.title = "New Title"

    def test_description_property_readonly(self):
        """Test that description property is read-only."""
        task = Task(id=1, title="Test", description="Desc")
        with pytest.raises(AttributeError):
            task.description = "New Desc"

    def test_is_complete_property_readonly(self):
        """Test that is_complete property is read-only."""
        task = Task(id=1, title="Test")
        with pytest.raises(AttributeError):
            task.is_complete = True


class TestTaskStringRepresentation:
    """Test Task string representation."""

    def test_repr_incomplete_task(self):
        """Test repr for incomplete task."""
        task = Task(id=1, title="Test Task", is_complete=False)
        repr_str = repr(task)
        assert "Task(id=1" in repr_str
        assert "Test Task" in repr_str
        assert "is_complete=False" in repr_str

    def test_repr_complete_task(self):
        """Test repr for complete task."""
        task = Task(id=5, title="Done Task", is_complete=True)
        repr_str = repr(task)
        assert "id=5" in repr_str
        assert "is_complete=True" in repr_str


class TestTaskEquality:
    """Test Task equality and hashing."""

    def test_tasks_equal_by_id(self):
        """Test that tasks are equal if IDs match."""
        task1 = Task(id=1, title="Task A")
        task2 = Task(id=1, title="Task B")
        assert task1 == task2

    def test_tasks_not_equal_different_id(self):
        """Test that tasks are not equal if IDs differ."""
        task1 = Task(id=1, title="Task A")
        task2 = Task(id=2, title="Task A")
        assert task1 != task2

    def test_task_hash_by_id(self):
        """Test that task hash is based on ID."""
        task1 = Task(id=1, title="Task A")
        task2 = Task(id=1, title="Task B")
        assert hash(task1) == hash(task2)

    def test_task_in_set(self):
        """Test that tasks can be used in sets."""
        task1 = Task(id=1, title="Task A")
        task2 = Task(id=2, title="Task B")
        task_set = {task1, task2}
        assert len(task_set) == 2

    def test_task_in_dict(self):
        """Test that tasks can be used as dict keys."""
        task1 = Task(id=1, title="Task A")
        task_dict = {task1: "value"}
        assert task_dict[task1] == "value"


class TestTaskEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_task_with_very_long_title(self):
        """Test creating task with very long title."""
        long_title = "A" * 500
        task = Task(id=1, title=long_title)
        assert task.title == long_title
        assert len(task.title) == 500

    def test_task_with_very_long_description(self):
        """Test creating task with very long description."""
        long_desc = "B" * 1000
        task = Task(id=1, title="Test", description=long_desc)
        assert task.description == long_desc

    def test_task_with_newlines_in_title(self):
        """Test creating task with newlines in title."""
        task = Task(id=1, title="Line1\nLine2")
        assert "\n" in task.title

    def test_task_with_newlines_in_description(self):
        """Test creating task with newlines in description."""
        task = Task(id=1, title="Test", description="Desc1\nDesc2")
        assert "\n" in task.description
