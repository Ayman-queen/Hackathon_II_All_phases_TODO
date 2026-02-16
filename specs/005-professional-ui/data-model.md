# Data Model & Schema

**Feature**: Professional UI & Advanced CRUD (005-professional-ui)
**Created**: 2026-01-02

## Overview

This document defines the core data entities and their relationships for the task management feature.

---

## Entity: Task

Represents a user's to-do item.

### SQLModel Definition (Backend)

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

class Task(SQLModel, table=True):
    """Task entity for user to-do management"""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)

    # Core fields
    title: str = Field(min_length=1, max_length=255, index=True)
    description: Optional[str] = Field(default=None, max_length=2000)
    priority: str = Field(default="Medium")  # High, Medium, Low
    completed: bool = Field(default=False, index=True)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: "User" = Relationship(back_populates="tasks")

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title}, priority={self.priority})"
```

### TypeScript Interface (Frontend)

```typescript
export interface Task {
  id: string;                           // UUID
  user_id: string;                      // UUID
  title: string;                        // 1-255 chars
  description: string | null;           // 0-2000 chars
  priority: "High" | "Medium" | "Low";
  completed: boolean;
  created_at: ISO8601DateTime;
  updated_at: ISO8601DateTime;
}

// Form input (may have temp ID)
export interface TaskInput {
  title: string;
  description?: string;
  priority: "High" | "Medium" | "Low";
  completed?: boolean;
}

// Optimistic update payload
export interface OptimisticTask extends Task {
  id: string; // Can be temp-${timestamp} for new tasks
}
```

### Field Constraints & Validation

| Field | Type | Constraints | Validation |
|---|---|---|---|
| `id` | UUID | Primary key, auto-generated | Generated server-side |
| `user_id` | UUID | Foreign key to User, indexed | From JWT claims, immutable |
| `title` | String | 1-255 chars, required | Trimmed, non-empty |
| `description` | String \| null | 0-2000 chars, optional | Trimmed or null |
| `priority` | Enum | High, Medium, Low | Case-sensitive exact match |
| `completed` | Boolean | Default: false | Boolean only |
| `created_at` | DateTime | Auto-set on creation | UTC, read-only |
| `updated_at` | DateTime | Auto-set on each update | UTC, read-only |

### Validation Rules

```typescript
// Zod schema for frontend validation
import { z } from "zod";

export const taskCreateSchema = z.object({
  title: z.string().min(1).max(255),
  description: z.string().max(2000).optional(),
  priority: z.enum(["High", "Medium", "Low"])
});

export const taskUpdateSchema = z.object({
  title: z.string().min(1).max(255).optional(),
  description: z.string().max(2000).optional(),
  priority: z.enum(["High", "Medium", "Low"]).optional(),
  completed: z.boolean().optional()
});

export const taskFilterSchema = z.object({
  completed: z.boolean().optional(),
  priority: z.enum(["High", "Medium", "Low"]).optional()
});
```

### Indexes

- `(user_id)`: Fast filtering by user
- `(user_id, created_at DESC)`: Task list ordered by creation
- `(user_id, completed)`: Quick complete/incomplete filtering
- `(user_id, priority)`: Quick filtering by priority
- `title`: Full-text search (future enhancement)

---

## Entity: User

Represents an authenticated user with profile and preferences.

### SQLModel Definition (Backend)

```python
class User(SQLModel, table=True):
    """User entity from Better Auth with profile extensions"""

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    # From Better Auth
    email: str = Field(unique=True, index=True)
    name: str

    # Preferences
    theme_preference: str = Field(default="light")  # light, dark

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, email={self.email}, theme={self.theme_preference})"
```

### TypeScript Interface (Frontend)

```typescript
export interface User {
  id: string;                           // UUID
  email: string;                        // Unique
  name: string;
  theme_preference: "light" | "dark";
  created_at: ISO8601DateTime;
  updated_at: ISO8601DateTime;
}

export interface UserProfile {
  user: User;
  task_count?: number;                  // Optional: count of user's tasks
  completed_count?: number;             // Optional: count of completed tasks
}
```

### Field Constraints

| Field | Type | Constraints | Notes |
|---|---|---|---|
| `id` | UUID | Primary key, auto-generated | From Better Auth |
| `email` | String | Unique, indexed | From Better Auth |
| `name` | String | Required | From Better Auth |
| `theme_preference` | Enum | light, dark | Default: light |
| `created_at` | DateTime | Auto-set | UTC |
| `updated_at` | DateTime | Auto-set | UTC |

---

## Relationships

### Task ← User

- **Type**: One-to-Many
- **Foreign Key**: Task.user_id → User.id
- **Cascade**: DELETE User → DELETE all User's Tasks
- **Query**: "Get all tasks for user X" → SELECT * FROM Task WHERE user_id = X
- **Enforcement**: All API responses filter by user_id from JWT

### Data Isolation

```python
# Backend: All queries must filter by user_id from JWT
@router.get("/tasks")
async def list_tasks(user_id: UUID = Depends(get_current_user)):
    # NEVER: SELECT * FROM task
    # ALWAYS: SELECT * FROM task WHERE user_id = ?
    return db.query(Task).filter(Task.user_id == user_id).all()
```

---

## State Transitions

### Task Lifecycle

```
Created (completed=false)
    ↓ (user marks complete)
    ├→ Completed (completed=true)
    │   ↓ (user marks incomplete)
    │   └→ Created (completed=false)
    ↓ (user edits)
    └→ Updated (timestamps update)
    ↓ (user deletes)
    └→ Deleted (removed from DB)
```

### Fields That Can Change

- `title`: Editable
- `description`: Editable
- `priority`: Editable
- `completed`: Editable (toggle)
- `updated_at`: Auto-updated on any change
- Fields that CANNOT change: `id`, `user_id`, `created_at`

---

## Bulk Operation Payloads

### Bulk Delete Request

```typescript
interface BulkDeleteRequest {
  task_ids: string[];                   // Array of UUIDs, 1-100 items
}

interface BulkDeleteResponse {
  deleted_count: number;                // Number of tasks deleted
  failed_count: number;                 // Number that failed
  user_id: string;                      // From JWT claims
}
```

### Bulk Complete Request

```typescript
interface BulkCompleteRequest {
  task_ids: string[];                   // Array of UUIDs, 1-100 items
}

interface BulkCompleteResponse {
  updated_count: number;                // Number successfully updated
  failed_count: number;                 // Number that failed
  user_id: string;                      // From JWT claims
}
```

---

## Database Schema (SQL)

```sql
-- Users table
CREATE TABLE "user" (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  theme_preference VARCHAR(10) DEFAULT 'light',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_email ON "user"(email);

-- Tasks table
CREATE TABLE task (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  priority VARCHAR(10) DEFAULT 'Medium',
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_task_user_id ON task(user_id);
CREATE INDEX idx_task_user_id_created ON task(user_id, created_at DESC);
CREATE INDEX idx_task_user_id_completed ON task(user_id, completed);
CREATE INDEX idx_task_user_id_priority ON task(user_id, priority);
```

---

## Data Migration Strategy

### Phase 1: Add theme_preference to User

If User table already exists without theme_preference:

```sql
ALTER TABLE "user" ADD COLUMN theme_preference VARCHAR(10) DEFAULT 'light';
```

### Phase 2: Ensure Task constraints

Verify foreign key constraints:

```sql
ALTER TABLE task
ADD CONSTRAINT fk_task_user_id
FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE;
```

### Phase 3: Add indexes

Create performance indexes if not present:

```sql
CREATE INDEX IF NOT EXISTS idx_task_user_id ON task(user_id);
CREATE INDEX IF NOT EXISTS idx_task_created_at ON task(user_id, created_at DESC);
```

---

## API Response Wrappers

### Standard Success Response

```typescript
interface ApiSuccessResponse<T> {
  data: T;                              // Can be Task[], Task, User, etc.
  user_id: string;                      // From JWT claims (always present)
  timestamp: ISO8601DateTime;           // Server time
}

// Example: List tasks
{
  data: {
    tasks: [
      { id: "...", title: "...", priority: "High", ... },
      { id: "...", title: "...", priority: "Medium", ... }
    ]
  },
  user_id: "550e8400-e29b-41d4-a716-446655440001",
  timestamp: "2025-01-02T10:05:00Z"
}
```

### Error Response

```typescript
interface ApiErrorResponse {
  error: string;                        // Error message
  status: number;                       // HTTP status code
  details?: string;                     // Additional context
  timestamp: ISO8601DateTime;
}

// Example: Unauthorized
{
  error: "Unauthorized",
  status: 401,
  details: "Invalid or expired JWT token",
  timestamp: "2025-01-02T10:05:00Z"
}
```

---

## Performance Considerations

### Query Optimization

- **List tasks**: O(n) with user_id index → <50ms for 10k tasks
- **Create task**: O(1) insert → <10ms
- **Update task**: O(1) by ID + user_id → <10ms
- **Delete task**: O(1) by ID + user_id → <10ms
- **Bulk operations**: O(n) with parallelization → <3s for 100 tasks

### Storage Estimates

- Task table: ~1KB per row
  - 1,000 tasks = 1MB
  - 1M tasks = 1GB
- User table: ~500 bytes per row
  - 10,000 users = 5MB

### Caching Strategy (Future)

- User profile: Cache in session (Better Auth handles)
- Task list: Cache in browser localStorage (optimistic state)
- Task counts: Cache with 5-minute TTL

---

## Type Safety Across Layers

### Frontend (TypeScript)
- Task, TaskInput, OptimisticTask interfaces
- Zod schemas for validation
- useOptimistic hooks type-safe

### Backend (Python)
- SQLModel for ORM + Pydantic validation
- Automatic OpenAPI schema generation
- Type hints on all functions

### API Contract (OpenAPI)
- Fully typed endpoint definitions
- Request/response schema validation
- Automatic client code generation possible
