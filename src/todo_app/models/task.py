"""
Task Model - Data Model Layer

Task ID: T005 (Create Task model class)
Spec: specs/001-cli-todo/spec.md (Key Entities: Todo)
Plan: specs/001-cli-todo/plan.md (Task Entity section)
Data Model: specs/001-cli-todo/data-model.md (Task Entity)

Represents an immutable task/todo item with auto-generated ID,
required title, optional description, and completion status.
"""


class Task:
    """
    Immutable task/todo item.

    Attributes:
        id: Unique auto-incrementing identifier
        title: Required task title (non-empty string)
        description: Optional task description (may be empty)
        is_complete: Completion status (default: False)

    Validation:
        - Title must be non-empty and non-whitespace
        - ID is auto-assigned by TodoManager (immutable)
    """

    def __init__(
        self,
        id: int,
        title: str,
        description: str = "",
        is_complete: bool = False,
    ) -> None:
        """
        Initialize a Task.

        Args:
            id: Unique task identifier
            title: Required task title
            description: Optional task description
            is_complete: Task completion status

        Raises:
            ValueError: If title is empty or whitespace-only
        """
        if not title or not title.strip():
            raise ValueError("Title cannot be empty or whitespace-only")

        self._id = id
        self._title = title
        self._description = description
        self._is_complete = is_complete

    @property
    def id(self) -> int:
        """Get task ID (read-only)."""
        return self._id

    @property
    def title(self) -> str:
        """Get task title (read-only)."""
        return self._title

    @property
    def description(self) -> str:
        """Get task description (read-only)."""
        return self._description

    @property
    def is_complete(self) -> bool:
        """Get task completion status (read-only)."""
        return self._is_complete

    def __repr__(self) -> str:
        """Return string representation of task."""
        status = "✓" if self._is_complete else "○"
        return (
            f"Task(id={self._id}, "
            f"title='{self._title}', "
            f"is_complete={self._is_complete})"
        )

    def __eq__(self, other: object) -> bool:
        """Check equality by ID."""
        if not isinstance(other, Task):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        """Hash by ID for use in sets/dicts."""
        return hash(self._id)
