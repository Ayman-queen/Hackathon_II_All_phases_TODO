# Task T-209: SQLModel Todo entity with user_id foreign key
"""
Todo model for the todo management application.

IMPORTANT: The user_id field is now a string (UUID string from Better Auth)
to match the 'user' table schema created by Better Auth.

Better Auth stores user IDs as UUID strings in the 'user' table.
The foreign key must reference 'user.id' (singular table name).
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from sqlalchemy import Index


class Todo(SQLModel, table=True):
    """
    Task T-209: Todo model for SQLModel ORM

    Maps to 'todos' table with fields:
    - id: UUID primary key (auto-generated)
    - user_id: String foreign key to user.id (Better Auth's user table)
    - title: Required todo title (500 char limit)
    - description: Optional longer description (2000 char limit)
    - is_complete: Boolean completion status
    - created_at: UTC timestamp for creation
    - updated_at: UTC timestamp for last modification

    Security: Composite index (user_id, created_at) for efficient filtered
    queries. All queries MUST filter by user_id (constitution requirement).

    Relationships: One-to-many with User (one user has many todos).
    """
    __tablename__ = "todos"

    # Primary Key - use UUID for todos
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        description="Unique todo identifier (UUID v4)"
    )

    # Foreign Key - now string to match Better Auth's user.id type
    # Better Auth stores user IDs as UUID strings
    user_id: str = Field(
        foreign_key="user.id",  # Fixed: Use singular 'user' table from Better Auth
        nullable=False,
        index=True,
        description="Foreign key to user.id from Better Auth (string UUID)"
    )

    # Content Fields
    title: str = Field(
        nullable=False,
        max_length=500,
        description="Todo title (1-500 characters, required)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Todo description (0-2000 characters, optional)"
    )

    # Status Fields
    is_complete: bool = Field(
        default=False,
        description="Completion status (false = pending, true = completed)"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="UTC timestamp when todo was created"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="UTC timestamp of last update"
    )

    # Task T-209: Composite index for efficient user-filtered queries
    # Enables fast queries like: SELECT * FROM todos WHERE user_id = ? ORDER BY created_at DESC
    __table_args__ = (
        Index('idx_user_created', 'user_id', 'created_at', postgresql_using='btree'),
    )

    def __repr__(self) -> str:
        """Task T-209: String representation for debugging"""
        return f"Todo(id={self.id}, user_id={self.user_id}, title={self.title[:30]}..., is_complete={self.is_complete})"
