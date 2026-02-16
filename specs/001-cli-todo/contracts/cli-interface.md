# CLI Interface Contract

**Feature**: CLI Todo Application
**Date**: 2025-12-27
**Format**: Text-based CLI with synchronous input/output

## Main Menu Contract

**Action**: User launches application

**Input**: None (automatic on startup)

**Output**:
```
=== TODO Manager ===
1. View All Todos
2. Add Todo
3. Update Todo
4. Mark Complete/Incomplete
5. Delete Todo
6. Exit

Select option (1-6):
```

**Constraints**:
- Menu displays exactly as shown above (spacing preserved)
- Prompt always ends with "Select option (1-6):"

---

## View Todos Contract

**Action**: User selects option 1

**Input**: Option "1"

**Output (Empty State)**:
```
=== TODO List ===

No todos yet. Add one to get started!

```

**Output (With Todos)**:
```
=== TODO List ===

[1] ☐ Buy groceries | Fresh produce and milk
[2] ☑ Complete report | Q4 summary
[3] ☐ Call dentist |

```

**Format Rules**:
- Each todo on separate line: `[ID] CHECKBOX TITLE | DESCRIPTION`
- Checkbox: `☐` (incomplete) or `☑` (complete)
- Title truncated to 60 chars with ellipsis if longer
- Description shown after `|` (empty if not provided)
- Blank line between todos
- Trailing blank line before menu

**Constraints**:
- Todos displayed in insertion order (creation order)
- Empty description shown as nothing after `|`

---

## Add Todo Contract

**Action**: User selects option 2

**Input Sequence**:
```
Enter todo title: Buy milk
Enter description (optional): Whole milk 2L
```

**Output**:
```
✓ Todo added successfully! (ID: 1)
```

**Input Error (Empty Title)**:
```
Enter todo title:
Title cannot be empty. Please try again.
Enter todo title: Buy milk
Enter description (optional):
✓ Todo added successfully! (ID: 2)
```

**Constraints**:
- Title input required; cannot be empty or whitespace-only
- Description optional; pressing Enter alone is valid
- Success message includes assigned ID

---

## Mark Complete/Incomplete Contract

**Action**: User selects option 4

**Input Sequence**:
```
Enter todo ID to toggle: 1
```

**Output (Found, Mark Complete)**:
```
✓ Todo 1 marked as complete!
```

**Output (Found, Mark Incomplete)**:
```
✓ Todo 1 marked as incomplete!
```

**Error (Not Found)**:
```
Enter todo ID to toggle: 99
✗ Todo not found. Please try again.
```

**Input Validation**:
- ID must be numeric; non-numeric input shows "Invalid ID format" and re-prompts
- Valid ID that doesn't exist shows "Todo not found"
- Does not require confirmation

**Constraints**:
- Toggle logic: incomplete → complete, complete → incomplete
- No confirmation required

---

## Update Todo Contract

**Action**: User selects option 3

**Input Sequence**:
```
Enter todo ID to update: 1
Enter new title (leave blank to keep current): Buy organic milk
Enter new description (leave blank to keep current):
```

**Output**:
```
✓ Todo 1 updated successfully!
```

**Error (Not Found)**:
```
Enter todo ID to update: 99
✗ Todo not found. Please try again.
```

**Behavior**:
- Both title and description are prompted
- Blank input for either field keeps the current value unchanged
- Cannot set title to empty (must enter new title if updating)
- At least one field must be non-empty (title required)

**Constraints**:
- Allows partial updates (update title only, or description only)
- Does not require confirmation

---

## Delete Todo Contract

**Action**: User selects option 5

**Input Sequence**:
```
Enter todo ID to delete: 1
Are you sure? (yes/no): yes
```

**Output (Confirmed)**:
```
✓ Todo 1 deleted successfully!
```

**Output (Cancelled)**:
```
Delete cancelled.
```

**Error (Not Found)**:
```
Enter todo ID to delete: 99
✗ Todo not found. Please try again.
```

**Confirmation Options**:
- "yes" or "y" → delete
- "no" or "n" → cancel
- Invalid response → "Invalid choice. Please try again."

**Constraints**:
- Confirmation required to prevent accidental deletion
- Case-insensitive confirmation input

---

## Exit Contract

**Action**: User selects option 6

**Input**: Option "6"

**Output**:
```
Goodbye!
```

**Behavior**:
- Application terminates immediately
- No save prompt (in-memory data is ephemeral per design)

---

## Error Handling Contract

**Invalid Menu Selection**:
```
Select option (1-6): 7
Invalid choice. Please try again.
Select option (1-6):
```

**Invalid ID Input** (non-numeric):
```
Enter todo ID: abc
Invalid ID format. Please enter a number.
Enter todo ID:
```

**All Errors**:
- Prefixed with `✗` for visual distinction
- Do not exit application
- Re-prompt the same input immediately after error

---

## Data Type Contracts

**ID**: Positive integer, auto-incremented starting at 1

**Title**:
- String, required, non-empty
- Max 500 chars input; truncated to 60 for display with ellipsis

**Description**:
- String, optional, may be empty
- Max 500 chars input (no truncation on display)

**Status**:
- Boolean (complete/incomplete)
- Displayed as `☑` or `☐`

---

## Interaction Flow Contract

```
┌─────────────────┐
│   Main Menu     │
│  (Show options) │
└────────┬────────┘
         │
    ┌────┴────┬────────┬────────┬────────┬───────┐
    │          │        │        │        │       │
    ▼          ▼        ▼        ▼        ▼       ▼
  View       Add     Update    Mark     Delete   Exit
  (show)    (get)   (get ID,   (get)   (get,    (done)
            (add)    get new)         confirm)
            (show)   (update)
                     (show)

Each action loops back to Main Menu (except Exit)
```

---

## Performance Contract

**Response Time**:
- Menu display: <10ms
- View todos: <50ms for up to 10k todos
- Add/update/delete: <50ms
- All operations: sub-100ms guaranteed

**Memory**:
- No strict limit per design (in-memory)
- Practical limit: OS available RAM
- Tested up to 10k todos in < 10MB

---

## Accessibility & Readability

**Terminal Requirements**:
- Supports Unicode characters (☐, ☑)
- Assumes 80+ char width terminal
- Tested on: Linux, macOS, Windows (CMD/PowerShell)

**User Experience**:
- Prompts are clear and specific ("Enter todo title:")
- Error messages are user-friendly (not stack traces)
- Visual feedback for all operations (✓/✗)
- Graceful handling of all invalid inputs
