# Data Model & Architecture

**Feature**: CLI Todo Application
**Date**: 2025-12-27
**Status**: Design Phase 1

## Data Model

### Task Entity

**Responsibility**: Immutable value object representing a single todo item.

**Fields**:
- `id: int` — Unique auto-incrementing identifier (1, 2, 3, ...)
- `title: str` — Required task title (non-empty, max 500 chars display-truncated to 60)
- `description: str` — Optional task description (may be empty string)
- `is_complete: bool` — Completion status (default: False)

**Validation Rules**:
- Title MUST NOT be empty or whitespace-only
- ID is auto-assigned by TodoManager (client cannot set)
- Once created, Task fields are effectively immutable (updates via replacement)

**Relationships**:
- Owned by: TodoManager
- Stored in: TodoManager's internal List[Task]

### TodoManager Service

**Responsibility**: In-memory CRUD manager for tasks. Single instance per application session.

**Public Methods**:

#### `create_task(title: str, description: str = "") -> Task`
- Creates and stores a new Task with auto-incremented ID
- Returns the created Task
- Raises: ValueError if title is empty/whitespace

#### `get_all_tasks() -> List[Task]`
- Returns all tasks in insertion order (including completed ones)
- Empty list if no tasks exist

#### `get_task(task_id: int) -> Task | None`
- Returns Task by ID, or None if not found

#### `update_task(task_id: int, title: str | None = None, description: str | None = None) -> Task`
- Updates title and/or description for existing Task
- Unchanged fields retain original values
- Returns updated Task
- Raises: ValueError if task_id not found or new title is empty

#### `mark_complete(task_id: int, is_complete: bool = True) -> Task`
- Toggles is_complete status
- Returns updated Task
- Raises: ValueError if task_id not found

#### `delete_task(task_id: int) -> bool`
- Removes Task from collection permanently
- Returns True if deleted, False if task_id not found

**Internal State**:
- `_tasks: List[Task]` — Insertion-ordered list of all tasks
- `_next_id: int` — Counter for auto-incrementing IDs (starts at 1)

**Performance Characteristics**:
- Create: O(1) append
- Read single: O(n) search by ID (acceptable for <10k todos)
- Read all: O(1) return reference to list
- Update: O(n) search + O(1) replacement
- Delete: O(n) search + O(n) list removal
- Overall: Suitable for sub-100ms operations up to 10k todos

### CLI Handler (Presentation Layer)

**Responsibility**: Format and display tasks; handle user input prompts.

**Functions**:

#### `format_task(task: Task) -> str`
- Formats single task for display
- Output: `[ID] ☐/☑ TITLE | DESCRIPTION` (or empty if no desc)
- Truncates title to 60 chars with ellipsis if needed

#### `format_task_list(tasks: List[Task]) -> str`
- Formats all tasks with numbering and spacing
- Empty state: "No todos yet. Add one to get started!"
- Returns formatted multi-line string ready for print

#### `prompt_user_input(prompt: str) -> str`
- Displays prompt and gets user input via input()
- Strips whitespace; returns result
- Used for menu selection and task data entry

#### `display_message(message: str)`
- Prints message to stdout
- Used for confirmations and error messages

## Responsibility Boundaries

```
┌─────────────────────────────────────────┐
│         CLI Main Loop (main.py)         │
│  ├─ Display menu                        │
│  ├─ Get user selection                  │
│  └─ Route to operations                 │
└──────────────┬──────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
┌─────────────────┐  ┌──────────────────┐
│  CLI Handler    │  │  TodoManager     │
│  (UI Formatting)│  │  (Business Logic)│
└────────┬────────┘  └──────┬───────────┘
         │                  │
         └────────┬─────────┘
                  │
                  ▼
            ┌────────────┐
            │  Task      │
            │  (Data)    │
            └────────────┘

Main Loop orchestrates user interactions
CLI Handler translates task data to display format
TodoManager manages in-memory collection
Task represents domain entity
```

## State Management

**Session Lifetime**:
- Application starts → TodoManager instantiated (empty)
- User adds/updates/deletes tasks → TodoManager state changes
- User exits → TodoManager state destroyed (in-memory, non-persistent)

**Thread Safety**:
- Single-user CLI; no concurrent access
- No locking or synchronization required

## Validation Flow

```
User Input
    │
    ▼
CLI Handler (prompt_user_input)
    │
    ├─ Get raw input
    └─ Strip whitespace
        │
        ▼
    TodoManager (create/update)
        │
        ├─ Validate title (not empty)
        ├─ Auto-increment ID
        └─ Store Task
            │
            ▼
        Task (immutable)
        │
        └─ Return to CLI Handler
            │
            ▼
        CLI Handler (format_task)
            │
            └─ Display to user
```

## Key Design Decisions

1. **List-based Storage**: Simple O(n) lookups acceptable for <10k items; avoids HashMap complexity overhead
2. **Immutable Tasks**: Tasks are effectively immutable; updates create new Task and replace in list
3. **No Persistence**: In-memory only per constitutional requirement
4. **Separation of Concerns**: Data (Task) ↔ Logic (TodoManager) ↔ UI (CLI Handler) cleanly separated
5. **Simple CLI Loop**: input() used directly; argparse not needed for menu-driven interaction
