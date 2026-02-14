"""
Unit Tests for CLI Handler

Task ID: T010 (Create unit tests for CLI Handler)
Spec: specs/001-cli-todo/spec.md (User interface formatting)
Implementation: src/todo_app/ui/cli_handler.py

Tests cover:
- Task formatting with correct checkbox symbols
- List formatting with proper spacing
- Title truncation to 60 characters
- Empty list handling
- Special character handling
"""

import pytest
from src.todo_app.models.task import Task
from src.todo_app.ui import cli_handler


class TestFormatTask:
    """Test format_task function."""

    def test_format_incomplete_task(self):
        """Test formatting incomplete task with unchecked checkbox."""
        task = Task(id=1, title="Test Task", is_complete=False)
        formatted = cli_handler.format_task(task)

        assert "[1]" in formatted
        assert "☐" in formatted
        assert "Test Task" in formatted

    def test_format_complete_task(self):
        """Test formatting complete task with checked checkbox."""
        task = Task(id=5, title="Completed Task", is_complete=True)
        formatted = cli_handler.format_task(task)

        assert "[5]" in formatted
        assert "☑" in formatted
        assert "Completed Task" in formatted

    def test_format_task_with_description(self):
        """Test formatting task with description."""
        task = Task(
            id=1,
            title="Task",
            description="This is a description",
            is_complete=False
        )
        formatted = cli_handler.format_task(task)

        assert "|" in formatted
        assert "This is a description" in formatted

    def test_format_task_without_description(self):
        """Test formatting task without description."""
        task = Task(id=1, title="Task", description="", is_complete=False)
        formatted = cli_handler.format_task(task)

        assert "|" in formatted
        # Should have pipe but no description after it

    def test_format_task_long_title_truncation(self):
        """Test that titles longer than 60 chars are truncated with ellipsis."""
        long_title = "A" * 70
        task = Task(id=1, title=long_title, is_complete=False)
        formatted = cli_handler.format_task(task)

        assert "..." in formatted
        assert long_title not in formatted  # Full title should not be in formatted
        assert len(formatted) < len(f"[1] ☐ {long_title}")

    def test_format_task_title_exactly_60_chars(self):
        """Test title with exactly 60 characters (no truncation)."""
        title_60 = "A" * 60
        task = Task(id=1, title=title_60, is_complete=False)
        formatted = cli_handler.format_task(task)

        assert title_60 in formatted
        assert "..." not in formatted

    def test_format_task_title_59_chars(self):
        """Test title with 59 characters (no truncation)."""
        title_59 = "B" * 59
        task = Task(id=1, title=title_59, is_complete=False)
        formatted = cli_handler.format_task(task)

        assert title_59 in formatted
        assert "..." not in formatted

    def test_format_task_title_61_chars(self):
        """Test title with 61 characters (should truncate)."""
        title_61 = "C" * 61
        task = Task(id=1, title=title_61, is_complete=False)
        formatted = cli_handler.format_task(task)

        assert "..." in formatted
        assert title_61 not in formatted

    def test_format_task_special_characters(self):
        """Test formatting task with special characters."""
        task = Task(
            id=1,
            title="Task with émojis 🎉 & symbols!",
            description="Test <html>",
            is_complete=False
        )
        formatted = cli_handler.format_task(task)

        assert "émojis" in formatted
        assert "<html>" in formatted


class TestFormatTaskList:
    """Test format_task_list function."""

    def test_format_empty_list(self):
        """Test formatting empty task list."""
        tasks = []
        formatted = cli_handler.format_task_list(tasks)

        assert "No todos yet. Add one to get started!" in formatted

    def test_format_single_task_list(self):
        """Test formatting list with single task."""
        task = Task(id=1, title="Single Task", is_complete=False)
        formatted = cli_handler.format_task_list([task])

        assert "=== TODO List ===" in formatted
        assert "[1]" in formatted
        assert "☐" in formatted
        assert "Single Task" in formatted

    def test_format_multiple_tasks_list(self):
        """Test formatting list with multiple tasks."""
        tasks = [
            Task(id=1, title="Task 1", is_complete=False),
            Task(id=2, title="Task 2", is_complete=True),
            Task(id=3, title="Task 3", is_complete=False),
        ]
        formatted = cli_handler.format_task_list(tasks)

        # All tasks should be present
        assert "[1]" in formatted
        assert "[2]" in formatted
        assert "[3]" in formatted

        # Correct status symbols
        assert "☐" in formatted
        assert "☑" in formatted

    def test_format_list_has_spacing(self):
        """Test that formatted list has blank lines between tasks."""
        tasks = [
            Task(id=1, title="Task 1", is_complete=False),
            Task(id=2, title="Task 2", is_complete=False),
        ]
        formatted = cli_handler.format_task_list(tasks)

        # Should have multiple newlines for spacing
        assert formatted.count("\n") >= 5  # Header + task1 + blank + task2 + blank


class TestTaskTruncation:
    """Test task title truncation logic."""

    def test_truncation_at_60_characters(self):
        """Test truncation boundary at 60 characters."""
        for length in range(55, 66):
            title = "X" * length
            task = Task(id=1, title=title, is_complete=False)
            formatted = cli_handler.format_task(task)

            if length > 60:
                assert "..." in formatted
                # Verify format includes ellipsis
                assert formatted.count("...") >= 1
            else:
                # For 60 or less, no truncation
                if length <= 60:
                    assert "..." not in formatted or length > 60

    def test_truncation_preserves_ellipsis(self):
        """Test that truncated titles end with ellipsis."""
        long_title = "A" * 100
        task = Task(id=1, title=long_title, is_complete=False)
        formatted = cli_handler.format_task(task)

        # Count characters in formatted title portion
        # Format is: [ID] ☐ TITLE | ...
        assert "..." in formatted
        lines = formatted.split("|")[0]  # Get the title part before |
        assert lines.rstrip().endswith("...")


class TestFormattingIntegration:
    """Test formatting functions together."""

    def test_list_with_mixed_lengths(self):
        """Test list with short, medium, and long titles."""
        tasks = [
            Task(id=1, title="Short", is_complete=False),
            Task(id=2, title="Medium length title", is_complete=True),
            Task(id=3, title="A" * 75, is_complete=False),  # Long, will truncate
        ]
        formatted = cli_handler.format_task_list(tasks)

        assert "[1]" in formatted
        assert "[2]" in formatted
        assert "[3]" in formatted
        assert "..." in formatted  # From long title

    def test_list_with_descriptions(self):
        """Test list with some tasks having descriptions."""
        tasks = [
            Task(id=1, title="No desc", is_complete=False),
            Task(id=2, title="Has desc", description="Description text", is_complete=True),
        ]
        formatted = cli_handler.format_task_list(tasks)

        # Both should have pipe character
        assert formatted.count("|") >= 2

    def test_empty_description_formatting(self):
        """Test that empty description doesn't show extra content."""
        task = Task(id=1, title="Task", description="", is_complete=False)
        formatted = cli_handler.format_task(task)

        # Should have pipe but nothing after it (or just end)
        parts = formatted.split("|")
        if len(parts) == 2:
            assert parts[1].strip() == ""
