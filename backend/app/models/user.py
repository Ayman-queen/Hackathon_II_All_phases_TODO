# Task T-208: SQLModel User entity that maps to Better Auth's user table
"""
CRITICAL FIX: User model now maps to Better Auth's 'user' table (singular)

Root Cause of 401 Unauthorized Errors:
- Better Auth creates a table named 'user' (singular)
- Backend was querying from 'users' (plural) table
- JWT validation succeeded but user lookup failed
- This caused all API requests to return 401 Unauthorized

Better Auth User Table Schema:
- id: String (UUID) - primary key
- email: String - unique, required
- name: String - required
- emailVerified: Boolean - required
- image: String - optional
- createdAt: DateTime - timestamp
- updatedAt: DateTime - timestamp

No custom fields like password_hash, is_active since Better Auth manages authentication.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """
    Task T-208/T-221: User model that maps to Better Auth's 'user' table

    IMPORTANT: This model queries the Better Auth managed 'user' table.
    All authentication is handled by Better Auth, this model is for:
    - JWT token validation (extracting user_id from 'sub' claim)
    - Data isolation (filtering todos by user_id)
    - Verifying user exists in database

    The user is already created and managed by Better Auth.
    We only read from this table to validate JWT tokens.
    """
    __tablename__ = "user"  # Better Auth uses singular 'user', not 'users'

    # Primary Key - matches Better Auth schema
    # Better Auth generates UUIDs as strings
    id: str = Field(
        primary_key=True,
        description="Unique user identifier (UUID string from Better Auth)"
    )

    # Core Fields - must match Better Auth's user table
    email: str = Field(
        unique=True,
        nullable=False,
        index=True,
        max_length=255,
        description="User email address (unique)"
    )

    name: str = Field(
        nullable=False,
        max_length=255,
        description="User display name"
    )

    emailVerified: bool = Field(
        default=False,
        description="Whether user's email is verified"
    )

    # Optional Fields
    image: Optional[str] = Field(
        default=None,
        max_length=2048,
        description="User profile image URL (optional)"
    )

    # Timestamps - Better Auth manages these
    createdAt: datetime = Field(
        nullable=False,
        description="UTC timestamp when user account was created by Better Auth"
    )

    updatedAt: datetime = Field(
        nullable=False,
        description="UTC timestamp of last user update"
    )

    def __repr__(self) -> str:
        """String representation for debugging"""
        return f"User(id={self.id}, email={self.email}, name={self.name})"
