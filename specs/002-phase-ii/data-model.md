# Data Model - Phase II Full-Stack Todo Application

## Overview

The Phase II application uses **Neon PostgreSQL** as the persistent data store with **SQLModel** as the ORM layer. All data is user-scoped; no user can access another user's data through the API.

## Entity Relationship Diagram (ERD)

```
┌─────────────────────────────────────────┐
│               User                      │
├─────────────────────────────────────────┤
│ id (UUID, PK)                           │
│ email (VARCHAR(255), UNIQUE, NOT NULL)  │
│ password_hash (VARCHAR(255), NOT NULL)  │
│ name (VARCHAR(255), NULLABLE)           │
│ created_at (TIMESTAMP, NOT NULL)        │
│ updated_at (TIMESTAMP, NOT NULL)        │
│ is_active (BOOLEAN, DEFAULT true)       │
└─────────────────────────────────────────┘
           ▲
           │ 1:N (One user has many todos)
           │
┌─────────────────────────────────────────┐
│               Todo                      │
├─────────────────────────────────────────┤
│ id (UUID, PK)                           │
│ user_id (UUID, FK → User.id, NOT NULL)  │
│ title (VARCHAR(500), NOT NULL)          │
│ description (TEXT, NULLABLE)            │
│ is_complete (BOOLEAN, DEFAULT false)    │
│ created_at (TIMESTAMP, NOT NULL)        │
│ updated_at (TIMESTAMP, NOT NULL)        │
└─────────────────────────────────────────┘
```

## Detailed Entity Definitions

### User Entity

**Table**: `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Email address (login credential) |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password (256-char max) |
| name | VARCHAR(255) | NULLABLE | User's display name (optional) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Account creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP | Last update timestamp |
| is_active | BOOLEAN | NOT NULL, DEFAULT true | Account activation status |

**Indexes**:
- PRIMARY KEY on `id`
- UNIQUE INDEX on `email`
- INDEX on `created_at` (for analytics, user discovery)

**Notes**:
- Email is case-insensitive for uniqueness (use LOWER(email) in queries)
- Password is never returned in API responses
- is_active allows soft-delete without data loss

---

### Todo Entity

**Table**: `todos`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, DEFAULT gen_random_uuid() | Unique todo identifier |
| user_id | UUID | FOREIGN KEY → users(id), NOT NULL | Owner of the todo |
| title | VARCHAR(500) | NOT NULL | Todo title (required, max 500 chars) |
| description | TEXT | NULLABLE | Optional detailed description (max 2000 chars) |
| is_complete | BOOLEAN | NOT NULL, DEFAULT false | Completion status |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP, ON UPDATE CURRENT_TIMESTAMP | Last update timestamp |

**Indexes**:
- PRIMARY KEY on `id`
- FOREIGN KEY on `user_id`
- COMPOSITE INDEX on `(user_id, created_at DESC)` (for efficient user todo listing)
- INDEX on `is_complete` (for filtering by status)

**Constraints**:
- `user_id` is NOT NULL (every todo must belong to a user)
- ON DELETE CASCADE (if user is deleted, all their todos are deleted)

**Notes**:
- `is_complete` defaults to false; todos start as incomplete
- `description` is optional (can be NULL or empty string)
- Timestamps are in UTC (ISO 8601 format in API responses)

---

### Session Entity (Managed by Better Auth)

**Table**: `sessions` (created and managed by Better Auth)

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(255) | PRIMARY KEY | Session identifier |
| user_id | UUID | FOREIGN KEY → users(id), NOT NULL | User owning the session |
| token | VARCHAR(500) | UNIQUE, NOT NULL | JWT token |
| expires_at | TIMESTAMP | NOT NULL | Token expiration time (7 days from creation) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT CURRENT_TIMESTAMP | Session creation timestamp |

**Notes**:
- Better Auth handles all session logic; application only reads tokens
- Tokens expire after 7 days
- Expired sessions are automatically cleaned up by Better Auth

---

## SQLModel Schema (Python)

```python
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship, Column, String, DateTime
from sqlalchemy import func, Index

# User Model
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(
        sa_column=Column(String(255), unique=True, nullable=False, index=True),
        description="Unique email address"
    )
    password_hash: str = Field(
        sa_column=Column(String(255), nullable=False),
        description="Bcrypt hashed password"
    )
    name: Optional[str] = Field(
        default=None,
        sa_column=Column(String(255)),
        description="User's display name"
    )
    is_active: bool = Field(default=True, description="Account activation status")
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False, index=True),
        description="Account creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False),
        description="Last update timestamp"
    )

    # Relationship
    todos: List["Todo"] = Relationship(back_populates="user", cascade_delete=True)

# Todo Model
class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True,
        description="Owner of the todo"
    )
    title: str = Field(
        sa_column=Column(String(500), nullable=False),
        description="Todo title (required)"
    )
    description: Optional[str] = Field(
        default=None,
        sa_column=Column(String(2000)),
        description="Optional detailed description"
    )
    is_complete: bool = Field(
        default=False,
        description="Completion status"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False, index=True),
        description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime(timezone=True), nullable=False),
        description="Last update timestamp"
    )

    # Relationship
    user: User = Relationship(back_populates="todos")

# Composite Index for efficient user todo queries
__table_args__ = (
    Index('idx_user_created', Todo.user_id, Todo.created_at.desc()),
)
```

---

## Database Setup Instructions

### 1. Create Database Connection (Neon PostgreSQL)

```sql
-- Connect to Neon PostgreSQL using connection string from environment
-- DATABASE_URL=postgresql://user:password@neon-host/database_name
```

### 2. Create Tables (SQLModel ORM)

```python
# In FastAPI startup code:
from sqlmodel import create_engine, SQLModel

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False)

# Create all tables on startup
SQLModel.metadata.create_all(engine)
```

### 3. Create Indexes

```sql
-- Composite index for efficient user todo retrieval
CREATE INDEX idx_user_created ON todos(user_id, created_at DESC);

-- Case-insensitive email lookup
CREATE INDEX idx_email_lower ON users(LOWER(email));
```

---

## Data Integrity & Constraints

### Foreign Key Relationships

- **ON DELETE CASCADE**: If a user is deleted, all their todos are automatically deleted
- **ON UPDATE CASCADE**: If a user ID changes (rare), all references update automatically

### Validation Rules

| Entity | Field | Validation | Error Message |
|--------|-------|-----------|----------------|
| User | email | Must be valid email format, unique | "Invalid email format" / "Email already registered" |
| User | password_hash | Must be bcrypt (60 chars), non-empty | (Handled by password hashing, not exposed) |
| User | name | Optional, max 255 chars | "Name exceeds maximum length" |
| Todo | title | Required, non-empty, max 500 chars | "Title is required" / "Title exceeds 500 characters" |
| Todo | description | Optional, max 2000 chars | "Description exceeds 2000 characters" |
| Todo | user_id | Must reference valid user | (FK constraint prevents invalid refs) |

---

## Query Patterns (Performance Optimizations)

### 1. Get All Todos for User (Paginated)

```python
# Efficient: uses composite index (user_id, created_at DESC)
query = session.query(Todo).filter(
    Todo.user_id == user_id
).order_by(Todo.created_at.desc()).offset(skip).limit(limit)
```

### 2. Get Todo by ID (with ownership check)

```python
todo = session.query(Todo).filter(
    Todo.id == todo_id,
    Todo.user_id == user_id
).first()
```

### 3. Filter Todos by Completion Status

```python
incomplete_todos = session.query(Todo).filter(
    Todo.user_id == user_id,
    Todo.is_complete == False
).order_by(Todo.created_at.desc()).all()
```

### 4. Get User by Email (for login)

```python
# Uses UNIQUE INDEX on email for O(1) lookup
user = session.query(User).filter(
    func.lower(User.email) == email.lower()
).first()
```

---

## Scalability Considerations

- **Partitioning**: As todo count grows (millions), consider partitioning `todos` table by `user_id` or `created_at`
- **Archival**: Implement soft-delete via `deleted_at` timestamp for compliance/recovery
- **Caching**: Cache user's todo list (TTL 5 min) in Redis if needed for performance
- **Connection Pooling**: Neon provides built-in connection pooling; FastAPI uses SQLAlchemy's pool for efficiency

---

## Migration Strategy

### Initial Setup (Phase II)

1. Create `users` table with email UNIQUE index
2. Create `todos` table with user_id FK and composite index
3. Better Auth creates `sessions` table on first initialization
4. No existing data to migrate (greenfield project)

### Future Migrations (Post-Phase II)

- Use Alembic for schema migrations
- Always maintain backward compatibility
- Test migrations on staging environment before production

