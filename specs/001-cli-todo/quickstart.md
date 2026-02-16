# CLI Todo Application - Quickstart Guide

**Feature**: CLI Todo Application
**Date**: 2025-12-27
**Audience**: Developers implementing this feature

## Architecture Overview

The CLI Todo Application is organized into three layers:

```
┌─────────────────────────────────┐
│     CLI Main Loop               │ ← Entry point; displays menu, routes actions
│     (src/todo_app/main.py)      │
└──────────────┬──────────────────┘
               │
       ┌───────┴────────┐
       │                │
       ▼                ▼
┌─────────────────┐  ┌──────────────────┐
│  CLI Handler    │  │ TodoManager      │ ← Core business logic
│  (ui layer)     │  │ (services layer) │
└────────┬────────┘  └────────┬─────────┘
         │                    │
         └────────┬───────────┘
                  │
                  ▼
            ┌──────────────┐
            │ Task Model   │ ← Data representation
            │ (models)     │
            └──────────────┘
```

### Layer Responsibilities

1. **Task Model** (`src/todo_app/models/task.py`)
   - Represents a single todo item
   - Fields: id, title, description, is_complete
   - Immutable (updates via replacement in TodoManager)

2. **TodoManager Service** (`src/todo_app/services/todo_manager.py`)
   - Manages in-memory collection of tasks
   - Provides CRUD operations: create, read, update, delete
   - Handles ID generation and validation
   - Single instance per application session

3. **CLI Handler** (`src/todo_app/ui/cli_handler.py`)
   - Formats task data for display
   - Prompts user for input via input()
   - Displays messages and task lists
   - No business logic; purely presentation

4. **Main Loop** (`src/todo_app/main.py`)
   - Application entry point
   - Manages session lifecycle
   - Displays menu and routes user selections to appropriate operations
   - Orchestrates interaction between CLI Handler and TodoManager

## Development Flow

### 1. Create Task Model

**File**: `src/todo_app/models/task.py`

```python
class Task:
    """Immutable task/todo item."""

    def __init__(self, id: int, title: str, description: str = "", is_complete: bool = False):
        self.id = id
        self.title = title
        self.description = description
        self.is_complete = is_complete

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', is_complete={self.is_complete})"
```

**Testing**: Unit tests in `tests/unit/test_task.py`
- Constructor validation
- Immutability (fields are read-only)
- String representation

### 2. Create TodoManager Service

**File**: `src/todo_app/services/todo_manager.py`

Implement CRUD methods:
- `create_task(title, description="")` → Task
- `get_all_tasks()` → List[Task]
- `get_task(task_id)` → Task | None
- `update_task(task_id, title=None, description=None)` → Task
- `mark_complete(task_id, is_complete=True)` → Task
- `delete_task(task_id)` → bool

**Key Points**:
- Store tasks in `self._tasks: List[Task]`
- Auto-increment IDs with `self._next_id`
- Validate that title is not empty before creating/updating
- Return Task or bool as specified
- Raise ValueError for invalid inputs

**Testing**: Unit tests in `tests/unit/test_todo_manager.py`
- Test each CRUD operation
- Test ID auto-increment
- Test validation (empty title)
- Test ID lookup and updates

### 3. Create CLI Handler

**File**: `src/todo_app/ui/cli_handler.py`

Implement display functions:
- `format_task(task: Task) -> str` — Format single task
- `format_task_list(tasks: List[Task]) -> str` — Format all tasks
- `prompt_user_input(prompt: str) -> str` — Get user input
- `display_message(message: str)` — Print message

**Key Points**:
- Use checkbox symbols: `☐` (incomplete), `☑` (complete)
- Truncate titles to 60 chars with ellipsis if needed
- Format as `[ID] CHECKBOX TITLE | DESCRIPTION`
- Add blank lines between todos for readability
- Display "No todos yet. Add one to get started!" when empty

**Testing**: Unit tests in `tests/unit/test_cli_handler.py`
- Test formatting of single task
- Test formatting of multiple tasks
- Test empty state
- Test title truncation

### 4. Create Main Loop

**File**: `src/todo_app/main.py`

Implement main() function:
```python
def main():
    manager = TodoManager()

    while True:
        # Display menu
        # Get user selection
        # Route to appropriate operation
        # Handle errors gracefully
        # Loop back to menu
```

**Operations**:
1. View todos → display formatted list
2. Add todo → prompt for title/description → create → confirm
3. Update todo → prompt for ID, new title, new description → update → confirm
4. Mark complete → prompt for ID → toggle status → confirm
5. Delete todo → prompt for ID → ask confirmation → delete → confirm
6. Exit → display goodbye → terminate

**Key Points**:
- Use input() for menu selection
- Validate user input (numeric IDs, non-empty titles)
- Display error messages for invalid input
- Re-prompt on error (don't exit)
- After each operation, show result before returning to menu

**Testing**: Integration tests in `tests/integration/test_cli_workflow.py`
- Test complete user journey (add, view, update, mark, delete)
- Test error scenarios (invalid ID, empty title)
- Test exit flow

## Testing Strategy

### Unit Tests
- **Task model**: Constructor, field access, representation
- **TodoManager**: Each CRUD operation, validation, ID generation
- **CLI Handler**: Formatting, truncation, empty state

### Integration Tests
- **Full CLI workflow**: Add → View → Update → Mark → Delete → Exit
- **Error scenarios**: Invalid IDs, empty titles, invalid menu selections
- **Edge cases**: Very long titles, special characters, ID boundaries

### Contract Tests
- **CLI Interface**: Menu display matches spec exactly
- **Input/Output**: Each command follows contract in `contracts/cli-interface.md`
- **Performance**: All operations complete in <100ms

## Performance Targets

- Menu display: <10ms
- View todos: <50ms (up to 10k todos)
- Add/update/delete: <50ms each
- **Overall**: Sub-100ms response for all operations

For <10k todos, O(n) list search is acceptable. Optimize if performance degrades:
- Profile with pytest-benchmark
- Switch to dict by ID if needed
- Add indexing strategies

## Common Implementation Patterns

### Input Validation

```python
# Validate numeric ID
try:
    task_id = int(user_input)
except ValueError:
    print("Invalid ID format")
    continue

# Validate non-empty string
if not title or not title.strip():
    print("Title cannot be empty")
    continue
```

### Error Recovery

```python
while True:
    try:
        # Get user input
        # Perform operation
        # Show success
        break
    except ValueError as e:
        print(f"Error: {e}")
        continue
```

### List Display

```python
tasks = manager.get_all_tasks()
if not tasks:
    print("No todos yet. Add one to get started!")
else:
    for task in tasks:
        print(cli_handler.format_task(task))
```

## Configuration & Dependencies

**pyproject.toml** (uv project file):
```toml
[project]
name = "todo-app"
version = "1.0.0"
description = "CLI Todo application"
requires-python = ">=3.13"

[project.scripts]
todo = "todo_app.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Dependencies**:
- pytest (for testing, dev-only)
- No runtime dependencies

## Running the Application

```bash
# Install dependencies
uv sync

# Run the app
python -m todo_app.main
# or (after installation)
todo

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=src
```

## Debugging Tips

- Add print statements in TodoManager to trace ID generation
- Use pytest's -v flag for verbose test output
- Use pytest's -s flag to see print statements in tests
- Use debugger: `import pdb; pdb.set_trace()` in code

## Next Steps

1. Implement Task model (15-20 min)
2. Implement TodoManager service (30-40 min)
3. Implement CLI Handler (20-30 min)
4. Implement Main loop (20-30 min)
5. Write and run tests (60-90 min)
6. Integration and performance testing (30-40 min)

**Total**: ~3-4 hours for complete implementation and testing.
