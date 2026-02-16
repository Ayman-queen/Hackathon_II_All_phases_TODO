"""
TodoManager Service - Business Logic Layer

Task ID: T006 (Create TodoManager service class)
Spec: specs/001-cli-todo/spec.md (FR-002, FR-003 through FR-012)
Plan: specs/001-cli-todo/plan.md (TodoManager Service section)
Data Model: specs/001-cli-todo/data-model.md (TodoManager Service)

Manages in-memory collection of tasks with CRUD operations.
Single instance per application session.
Handles ID generation, validation, and state management.
"""

from typing import List, Optional
from ..models.task import Task


class TodoManager:
    """
    In-memory CRUD manager for tasks.

    Responsibilities:
        - Create tasks with auto-incrementing IDs
        - Read all tasks or specific task by ID
        - Update task title and/or description
        - Mark tasks as complete/incomplete
        - Delete tasks from collection

    Storage:
        - _tasks: List[Task] - All tasks in insertion order
        - _next_id: int - Auto-increment counter (starts at 1)

    Performance:
        - Create: O(1) append
        - Read single: O(n) search by ID
        - Read all: O(1) return reference
        - Update: O(n) search + O(1) replacement
        - Delete: O(n) search + O(n) list removal
        - Suitable for <10k todos with sub-100ms operations
    """

    def __init__(self) -> None:
        """Initialize TodoManager with empty task collection."""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def create_task(self, title: str, description: str = "") -> Task:
        """
        Create and store a new task.

        Args:
            title: Required task title
            description: Optional task description

        Returns:
            Created Task with auto-assigned ID

        Raises:
            ValueError: If title is empty or whitespace-only

        Spec Reference: FR-003 (add todo), FR-005 (unique ID generation)
        """
        try:
            task = Task(
                id=self._next_id,
                title=title,
                description=description,
                is_complete=False,
            )
        except ValueError as e:
            raise ValueError(f"Cannot create task: {e}") from e

        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks in insertion order.

        Returns:
            List of all tasks (empty list if no tasks)

        Spec Reference: FR-004 (view todos), SC-002 (all features functional)
        """
        return self._tasks.copy()

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get specific task by ID.

        Args:
            task_id: ID of task to retrieve

        Returns:
            Task if found, None if not found

        Spec Reference: FR-009 (validate ID exists)
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Task:
        """
        Update task title and/or description.

        Args:
            task_id: ID of task to update
            title: New title (None = keep current)
            description: New description (None = keep current)

        Returns:
            Updated Task

        Raises:
            ValueError: If task_id not found or new title is empty

        Spec Reference: FR-007 (update todo), FR-009 (validate ID)
        """
        task = self.get_task(task_id)
        if task is None:
            raise ValueError(f"Task {task_id} not found")

        new_title = title if title is not None else task.title
        new_description = description if description is not None else task.description

        if not new_title or not new_title.strip():
            raise ValueError("Title cannot be empty or whitespace-only")

        updated_task = Task(
            id=task.id,
            title=new_title,
            description=new_description,
            is_complete=task.is_complete,
        )

        # Replace task in list
        task_index = self._tasks.index(task)
        self._tasks[task_index] = updated_task

        return updated_task

    def mark_complete(self, task_id: int, is_complete: bool = True) -> Task:
        """
        Toggle task completion status.

        Args:
            task_id: ID of task to toggle
            is_complete: New completion status

        Returns:
            Updated Task

        Raises:
            ValueError: If task_id not found

        Spec Reference: FR-006 (mark complete), FR-009 (validate ID)
        """
        task = self.get_task(task_id)
        if task is None:
            raise ValueError(f"Task {task_id} not found")

        updated_task = Task(
            id=task.id,
            title=task.title,
            description=task.description,
            is_complete=is_complete,
        )

        # Replace task in list
        task_index = self._tasks.index(task)
        self._tasks[task_index] = updated_task

        return updated_task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete task from collection.

        Args:
            task_id: ID of task to delete

        Returns:
            True if deleted, False if task_id not found

        Spec Reference: FR-008 (delete todo), FR-009 (validate ID)
        """
        task = self.get_task(task_id)
        if task is None:
            return False

        self._tasks.remove(task)
        return True
