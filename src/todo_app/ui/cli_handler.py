"""
CLI Handler - Presentation Layer

Task ID: T007 (Create CLI Handler utility functions)
Spec: specs/001-cli-todo/spec.md (User interface formatting)
Plan: specs/001-cli-todo/plan.md (CLI Handler section)
Data Model: specs/001-cli-todo/data-model.md (CLI Handler)
Contracts: specs/001-cli-todo/contracts/cli-interface.md

Handles task formatting, display, and user input prompts.
Pure functions with no business logic.
Supports Unicode checkbox symbols (☐ = incomplete, ☑ = complete).
"""

from typing import List
from ..models.task import Task


def format_task(task: Task) -> str:
    """
    Format a single task for display.

    Format: [ID] ☐/☑ TITLE | DESCRIPTION
    - Checkbox: ☐ (incomplete), ☑ (complete)
    - Title truncated to 60 chars with ellipsis if longer
    - Description shown after pipe (empty if not provided)

    Args:
        task: Task object to format

    Returns:
        Formatted task string

    Spec Reference: User Story 1 (View List), FR-004 (display format)
    Contract Reference: cli-interface.md (format rules)
    """
    checkbox = "☑" if task.is_complete else "☐"

    # Truncate title to 60 chars with ellipsis
    title = task.title
    if len(title) > 60:
        title = title[:57] + "..."

    # Build output string
    output = f"[{task.id}] {checkbox} {title}"

    # Add description if present
    if task.description:
        output += f" | {task.description}"
    else:
        output += " |"

    return output


def format_task_list(tasks: List[Task]) -> str:
    """
    Format all tasks for display.

    Displays all tasks with numbering and spacing.
    Empty list shows: "No todos yet. Add one to get started!"
    Multiple tasks separated by blank lines for readability.

    Args:
        tasks: List of Task objects

    Returns:
        Formatted multi-line string ready for print

    Spec Reference: User Story 1 (View List), FR-004 (list display)
    Contract Reference: cli-interface.md (output format)
    """
    if not tasks:
        return "No todos yet. Add one to get started!"

    lines = ["=== TODO List ===", ""]

    for task in tasks:
        lines.append(format_task(task))
        lines.append("")  # Blank line between todos

    return "\n".join(lines)


def prompt_user_input(prompt: str) -> str:
    """
    Get user input via input() with whitespace stripping.

    Args:
        prompt: Prompt text to display

    Returns:
        User input with leading/trailing whitespace removed

    Spec Reference: FR-001 (menu prompts), FR-003 (title/desc entry)
    Contract Reference: cli-interface.md (prompt format)
    """
    return input(prompt).strip()


def display_message(message: str) -> None:
    """
    Print message to stdout.

    Args:
        message: Message to display

    Spec Reference: All user stories (confirmations, errors)
    """
    print(message)


def display_menu() -> None:
    """
    Display main menu options.

    Shows 6 menu options: View, Add, Update, Mark, Delete, Exit

    Spec Reference: FR-001 (main menu)
    Contract Reference: cli-interface.md (menu format)
    """
    menu_text = """=== TODO Manager ===
1. View All Todos
2. Add Todo
3. Update Todo
4. Mark Complete/Incomplete
5. Delete Todo
6. Exit

"""
    print(menu_text, end="")


def prompt_menu_selection() -> str:
    """
    Prompt for menu selection.

    Returns:
        User's menu selection (1-6 or other input)

    Spec Reference: FR-001 (main menu routing)
    """
    return prompt_user_input("Select option (1-6): ")


def prompt_todo_id(action: str) -> str:
    """
    Prompt for todo ID.

    Args:
        action: What action is being performed (e.g., "toggle", "update", "delete")

    Returns:
        User input (should be numeric ID)

    Spec Reference: FR-006, FR-007, FR-008 (ID-based operations)
    """
    return prompt_user_input(f"Enter todo ID to {action}: ")


def prompt_title() -> str:
    """
    Prompt for todo title (required).

    Returns:
        User-entered title (may need validation by caller)

    Spec Reference: FR-003, FR-011 (title required)
    """
    return prompt_user_input("Enter todo title: ")


def prompt_description() -> str:
    """
    Prompt for todo description (optional).

    Returns:
        User-entered description (empty string if blank)

    Spec Reference: FR-003, FR-011 (description optional)
    """
    return prompt_user_input("Enter description (optional): ")


def prompt_new_title_update() -> str:
    """
    Prompt for new title during update.

    Returns:
        User input (blank = keep current)

    Spec Reference: FR-007 (partial updates)
    """
    return prompt_user_input("Enter new title (leave blank to keep current): ")


def prompt_new_description_update() -> str:
    """
    Prompt for new description during update.

    Returns:
        User input (blank = keep current)

    Spec Reference: FR-007 (partial updates)
    """
    return prompt_user_input("Enter new description (leave blank to keep current): ")


def prompt_confirmation(question: str) -> str:
    """
    Prompt for yes/no confirmation.

    Args:
        question: Question to ask user

    Returns:
        User's response (lowercase)

    Spec Reference: FR-008 (delete confirmation)
    Contract Reference: cli-interface.md (confirmation format)
    """
    return prompt_user_input(f"{question} (yes/no): ").lower()
