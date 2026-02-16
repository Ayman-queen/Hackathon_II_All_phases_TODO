"""
Main Application Entry Point - Orchestration Layer

Task ID: T008 (Create main application entry point)
Spec: specs/001-cli-todo/spec.md (All user stories)
Plan: specs/001-cli-todo/plan.md (Main Loop section)
Quickstart: specs/001-cli-todo/quickstart.md (Integration scenarios)

Manages the CLI menu loop and routes user selections to appropriate operations.
Coordinates TodoManager service and CLI Handler UI layer.
Handles session lifecycle and error handling.
"""

import sys
from .models.task import Task
from .services.todo_manager import TodoManager
from .ui import cli_handler


def main() -> None:
    """
    Main application entry point.

    Initializes TodoManager and runs interactive menu loop.
    Routes menu selections to appropriate operations.
    Handles errors gracefully with re-prompts.

    Spec Reference: All 5 user stories, FR-001 (menu loop)
    """
    # Initialize TodoManager for session
    manager = TodoManager()

    print("=== Todo Application ===")
    print("(Type 'quit' to exit)\n")

    while True:
        try:
            # Display menu and get selection
            cli_handler.display_menu()
            selection = cli_handler.prompt_menu_selection()

            # Route to appropriate operation
            if selection == "1":
                _handle_view_todos(manager)
            elif selection == "2":
                _handle_add_todo(manager)
            elif selection == "3":
                _handle_update_todo(manager)
            elif selection == "4":
                _handle_mark_complete(manager)
            elif selection == "5":
                _handle_delete_todo(manager)
            elif selection == "6":
                print("Goodbye!")
                break
            else:
                cli_handler.display_message("Invalid choice. Please try again.\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            cli_handler.display_message(f"Error: {e}\n")


def _handle_view_todos(manager: TodoManager) -> None:
    """
    Handle "View Todos" menu option (Option 1).

    Displays all todos in formatted list.

    Spec Reference: User Story 1 (View List)
    Task Reference: T009-T012 (US1 implementation)
    """
    tasks = manager.get_all_tasks()
    formatted_list = cli_handler.format_task_list(tasks)
    cli_handler.display_message(formatted_list)
    print()  # Blank line after list


def _handle_add_todo(manager: TodoManager) -> None:
    """
    Handle "Add Todo" menu option (Option 2).

    Prompts for title and optional description.
    Validates title is non-empty (re-prompts if needed).
    Creates task and displays success message.

    Spec Reference: User Story 2 (Add Todo)
    Task Reference: T013-T016 (US2 implementation)
    """
    while True:
        title = cli_handler.prompt_title()

        if not title or not title.strip():
            cli_handler.display_message("Title cannot be empty. Please try again.\n")
            continue

        break

    description = cli_handler.prompt_description()

    try:
        task = manager.create_task(title=title, description=description)
        cli_handler.display_message(
            f"✓ Todo added successfully! (ID: {task.id})\n"
        )
    except ValueError as e:
        cli_handler.display_message(f"✗ Error adding todo: {e}\n")


def _handle_mark_complete(manager: TodoManager) -> None:
    """
    Handle "Mark Complete/Incomplete" menu option (Option 4).

    Prompts for todo ID.
    Toggles completion status.
    Displays success or error message.

    Spec Reference: User Story 3 (Mark Complete)
    Task Reference: T017-T019 (US3 implementation)
    """
    task_id_str = cli_handler.prompt_todo_id("toggle")

    try:
        task_id = int(task_id_str)
    except ValueError:
        cli_handler.display_message(
            "Invalid ID format. Please enter a number.\n"
        )
        return

    task = manager.get_task(task_id)
    if task is None:
        cli_handler.display_message("Todo not found. Please try again.\n")
        return

    try:
        updated_task = manager.mark_complete(
            task_id=task_id,
            is_complete=not task.is_complete,
        )

        status = "complete" if updated_task.is_complete else "incomplete"
        cli_handler.display_message(
            f"✓ Todo {task_id} marked as {status}!\n"
        )
    except ValueError as e:
        cli_handler.display_message(f"✗ Error: {e}\n")


def _handle_update_todo(manager: TodoManager) -> None:
    """
    Handle "Update Todo" menu option (Option 3).

    Prompts for todo ID.
    Prompts for new title and description (blank = no change).
    Updates task and displays success or error message.

    Spec Reference: User Story 4 (Update Todo)
    Task Reference: T020-T022 (US4 implementation)
    """
    task_id_str = cli_handler.prompt_todo_id("update")

    try:
        task_id = int(task_id_str)
    except ValueError:
        cli_handler.display_message(
            "Invalid ID format. Please enter a number.\n"
        )
        return

    task = manager.get_task(task_id)
    if task is None:
        cli_handler.display_message("Todo not found. Please try again.\n")
        return

    # Get new title and description (blank = no change)
    new_title = cli_handler.prompt_new_title_update()
    new_description = cli_handler.prompt_new_description_update()

    # Validate at least one field is provided
    if not new_title and not new_description:
        cli_handler.display_message(
            "No changes provided. Update cancelled.\n"
        )
        return

    try:
        updated_task = manager.update_task(
            task_id=task_id,
            title=new_title if new_title else None,
            description=new_description if new_description else None,
        )
        cli_handler.display_message(f"✓ Todo {task_id} updated successfully!\n")
    except ValueError as e:
        cli_handler.display_message(f"✗ Error: {e}\n")


def _handle_delete_todo(manager: TodoManager) -> None:
    """
    Handle "Delete Todo" menu option (Option 5).

    Prompts for todo ID.
    Displays confirmation prompt.
    Deletes on "yes"/"y", cancels on "no"/"n".
    Displays success or error message.

    Spec Reference: User Story 5 (Delete Todo)
    Task Reference: T023-T025 (US5 implementation)
    """
    task_id_str = cli_handler.prompt_todo_id("delete")

    try:
        task_id = int(task_id_str)
    except ValueError:
        cli_handler.display_message(
            "Invalid ID format. Please enter a number.\n"
        )
        return

    task = manager.get_task(task_id)
    if task is None:
        cli_handler.display_message("Todo not found. Please try again.\n")
        return

    # Confirmation prompt
    confirm = cli_handler.prompt_confirmation("Are you sure?")

    if confirm in ("yes", "y"):
        try:
            success = manager.delete_task(task_id=task_id)
            if success:
                cli_handler.display_message(
                    f"✓ Todo {task_id} deleted successfully!\n"
                )
            else:
                cli_handler.display_message("Todo not found.\n")
        except Exception as e:
            cli_handler.display_message(f"✗ Error deleting todo: {e}\n")
    else:
        cli_handler.display_message("Delete cancelled.\n")


if __name__ == "__main__":
    main()
