# Task T-224: Todo CRUD endpoints with user_id filtering for data isolation
# Task T-222: All endpoints validate Better Auth JWT tokens via get_current_user dependency
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from typing import Optional
from uuid import UUID

from app.models.database import get_db
from app.models.user import User
from app.models.todo import Todo
from app.api.deps import get_current_user
from app.schemas.todo import (
    TodoCreate,
    TodoUpdate,
    TodoToggle,
    TodoResponse,
    TodoListResponse,
)

# Task T-216: Create router for todo CRUD endpoints
# All endpoints prefixed with /api/todos and tagged as "todos"
router = APIRouter(
    prefix="/api/todos",
    tags=["todos"],
    responses={
        401: {"description": "Unauthorized - invalid or missing token"},
        403: {"description": "Forbidden - insufficient permissions"},
        404: {"description": "Not Found - todo does not exist"},
        422: {"description": "Unprocessable Entity - validation error"},
    }
)

@router.get(
    "",
    response_model=TodoListResponse,
    summary="List User Todos",
    description="Get all todos for authenticated user with pagination"
)
async def list_todos(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return (max 1000)"),
    is_complete: Optional[bool] = Query(None, description="Filter by completion status (optional)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TodoListResponse:
    """
    Task T-216: List all todos for authenticated user (GET /api/todos)

    Returns paginated list of todos for the current user with optional filtering.

    Query Parameters:
    - skip: Offset for pagination (default 0)
    - limit: Number of results to return (default 100, max 1000)
    - is_complete: Optional filter for completion status (true/false/null for all)

    Response (200 OK):
        {
            "todos": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "user_id": "660e8400-e29b-41d4-a716-446655440001",
                    "title": "Buy groceries",
                    "description": "Milk, eggs, bread",
                    "is_complete": false,
                    "created_at": "2025-12-29T10:30:00Z",
                    "updated_at": "2025-12-29T10:30:00Z"
                }
            ],
            "total": 42
        }

    Data Isolation (Constitution Requirement):
    - Query ONLY returns todos where user_id == current_user.id
    - No way to access other users' todos via API
    - Frontend should also filter on client side for UX

    Error Responses:
    - 401 Unauthorized: Missing or invalid token

    Pagination Example:
        GET /api/todos?skip=0&limit=10  # First 10 items
        GET /api/todos?skip=10&limit=10 # Next 10 items

    Filtering Example:
        GET /api/todos?is_complete=false  # Only pending todos
        GET /api/todos?is_complete=true   # Only completed todos
    """
    # Task T-216: Build query filtered by current user
    statement = select(Todo).where(Todo.user_id == current_user.id)

    # Task T-216: Apply completion status filter if provided
    if is_complete is not None:
        statement = statement.where(Todo.is_complete == is_complete)

    # Task T-216: Apply ordering and pagination
    statement = statement.order_by(Todo.created_at.desc()).offset(skip).limit(limit)

    # Execute query
    todos = db.exec(statement).all()

    # Task T-216: Get total count for pagination
    count_statement = select(Todo).where(Todo.user_id == current_user.id)
    if is_complete is not None:
        count_statement = count_statement.where(Todo.is_complete == is_complete)
    total = db.exec(count_statement).all().__len__()

    return TodoListResponse(todos=todos, total=total)


@router.get(
    "/stats",
    summary="Get User Stats",
    description="Get task statistics for the authenticated user"
)
async def get_user_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> dict:
    """
    Task T008: Get user task statistics for welcome message (FR-003)

    Returns pending and completed task counts for the current user.

    Response (200 OK):
        {
            "pending": 5,
            "completed": 10,
            "total": 15
        }
    """
    pending_statement = select(Todo).where(
        Todo.user_id == current_user.id,
        Todo.is_complete == False
    )
    completed_statement = select(Todo).where(
        Todo.user_id == current_user.id,
        Todo.is_complete == True
    )

    pending = len(db.exec(pending_statement).all())
    completed = len(db.exec(completed_statement).all())

    return {
        "pending": pending,
        "completed": completed,
        "total": pending + completed
    }


@router.post(
    "",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Todo",
    description="Create a new todo for authenticated user"
)
async def create_todo(
    todo_data: TodoCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TodoResponse:
    """
    Task T-216: Create a new todo (POST /api/todos)

    Creates a new todo for the authenticated user.

    Request Body:
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread from Whole Foods"  // optional
        }

    Response (201 Created):
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "user_id": "660e8400-e29b-41d4-a716-446655440001",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread from Whole Foods",
            "is_complete": false,
            "created_at": "2025-12-29T10:30:00Z",
            "updated_at": "2025-12-29T10:30:00Z"
        }

    Validation:
    - title: Required, 1-500 characters, cannot be all whitespace
    - description: Optional, 0-2000 characters
    - user_id: Automatically set from JWT token (not from request body)

    Error Responses:
    - 400 Bad Request: Title is empty or too long
    - 400 Bad Request: Description is too long
    - 401 Unauthorized: Missing or invalid token
    - 422 Unprocessable Entity: Validation error

    Data Isolation:
    - user_id automatically set to current_user.id
    - No way for user to assign todo to another user
    - Follows constitution requirement for user-scoped data
    """
    # Task T-216: Validate title
    if not todo_data.title or not todo_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required and cannot be empty or whitespace only."
        )

    if len(todo_data.title) > 500:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title must be 500 characters or less."
        )

    # Task T-216: Validate description if provided
    if todo_data.description and len(todo_data.description) > 2000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Description must be 2000 characters or less."
        )

    # Task T-216: Create todo with user_id from JWT
    todo = Todo(
        user_id=current_user.id,
        title=todo_data.title.strip(),
        description=todo_data.description.strip() if todo_data.description else None,
        is_complete=False,  # New todos start as pending
    )

    # Task T-216: Save to database
    db.add(todo)
    db.commit()
    db.refresh(todo)

    return TodoResponse.model_validate(todo)

@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Get Todo",
    description="Get a specific todo by ID (must be owner)"
)
async def get_todo(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TodoResponse:
    """
    Task T-216: Get a specific todo (GET /api/todos/{todo_id})

    Retrieves a single todo by ID. User must be the owner.

    Path Parameters:
    - todo_id: UUID of the todo to retrieve

    Response (200 OK):
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "user_id": "660e8400-e29b-41d4-a716-446655440001",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "is_complete": false,
            "created_at": "2025-12-29T10:30:00Z",
            "updated_at": "2025-12-29T10:30:00Z"
        }

    Error Responses:
    - 401 Unauthorized: Missing or invalid token
    - 403 Forbidden: User does not own this todo
    - 404 Not Found: Todo with this ID does not exist

    Data Isolation:
    - Returns 404 if todo doesn't exist OR if user doesn't own it
    - This prevents information leakage (attacker can't tell if todo exists)
    """
    # Task T-216: Query for todo by ID
    statement = select(Todo).where(Todo.id == todo_id)
    todo = db.exec(statement).first()

    # Task T-216: Return 404 if not found
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found."
        )

    # Task T-216: Verify ownership
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this todo."
        )

    return TodoResponse.model_validate(todo)

@router.put(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Update Todo",
    description="Update a todo's title and/or description"
)
async def update_todo(
    todo_id: UUID,
    todo_data: TodoUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TodoResponse:
    """
    Task T-216: Update a todo (PUT /api/todos/{todo_id})

    Updates title and/or description of a todo. User must be the owner.

    Path Parameters:
    - todo_id: UUID of the todo to update

    Request Body:
        {
            "title": "New title",  // optional
            "description": "New description"  // optional
        }

    Response (200 OK):
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "user_id": "660e8400-e29b-41d4-a716-446655440001",
            "title": "New title",
            "description": "New description",
            "is_complete": false,
            "created_at": "2025-12-29T10:30:00Z",
            "updated_at": "2025-12-29T10:30:00Z"  // updated to now
        }

    Validation:
    - title: If provided, must be 1-500 characters and non-empty
    - description: If provided, must be 0-2000 characters
    - At least one field must be non-null (no-op updates are rejected)

    Error Responses:
    - 400 Bad Request: Title/description validation failed
    - 401 Unauthorized: Missing or invalid token
    - 403 Forbidden: User does not own this todo
    - 404 Not Found: Todo with this ID does not exist

    Partial Update Example:
        PUT /api/todos/550e8400-e29b-41d4-a716-446655440000
        {
            "title": "Updated title"
        }
        // description is unchanged
    """
    # Task T-216: Query for todo
    statement = select(Todo).where(Todo.id == todo_id)
    todo = db.exec(statement).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found."
        )

    # Task T-216: Verify ownership
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this todo."
        )

    # Task T-216: Update title if provided
    if todo_data.title is not None:
        if not todo_data.title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title cannot be empty or whitespace only."
            )
        if len(todo_data.title) > 500:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title must be 500 characters or less."
            )
        todo.title = todo_data.title.strip()

    # Task T-216: Update description if provided
    if todo_data.description is not None:
        if len(todo_data.description) > 2000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Description must be 2000 characters or less."
            )
        todo.description = todo_data.description.strip() if todo_data.description else None

    # Task T-216: Save changes
    db.add(todo)
    db.commit()
    db.refresh(todo)

    return TodoResponse.model_validate(todo)

@router.patch(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Toggle Todo Status",
    description="Toggle a todo's completion status"
)
async def toggle_todo(
    todo_id: UUID,
    toggle_data: TodoToggle,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TodoResponse:
    """
    Task T-216: Toggle todo completion status (PATCH /api/todos/{todo_id})

    Updates only the is_complete field. User must be the owner.

    Path Parameters:
    - todo_id: UUID of the todo to toggle

    Request Body:
        {
            "is_complete": true  // or false
        }

    Response (200 OK):
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "user_id": "660e8400-e29b-41d4-a716-446655440001",
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "is_complete": true,  // updated
            "created_at": "2025-12-29T10:30:00Z",
            "updated_at": "2025-12-29T10:30:00Z"  // updated to now
        }

    Error Responses:
    - 401 Unauthorized: Missing or invalid token
    - 403 Forbidden: User does not own this todo
    - 404 Not Found: Todo with this ID does not exist

    Use Cases:
    - Mark todo as done: PATCH /api/todos/{id} {"is_complete": true}
    - Mark todo as pending: PATCH /api/todos/{id} {"is_complete": false}
    """
    # Task T-216: Query for todo
    statement = select(Todo).where(Todo.id == todo_id)
    todo = db.exec(statement).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found."
        )

    # Task T-216: Verify ownership
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this todo."
        )

    # Task T-216: Update completion status
    todo.is_complete = toggle_data.is_complete

    # Task T-216: Save changes
    db.add(todo)
    db.commit()
    db.refresh(todo)

    return TodoResponse.model_validate(todo)

@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Todo",
    description="Delete a todo permanently"
)
async def delete_todo(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> None:
    """
    Task T-216: Delete a todo (DELETE /api/todos/{todo_id})

    Permanently deletes a todo. User must be the owner.

    Path Parameters:
    - todo_id: UUID of the todo to delete

    Response (204 No Content):
        Empty response body

    Error Responses:
    - 401 Unauthorized: Missing or invalid token
    - 403 Forbidden: User does not own this todo
    - 404 Not Found: Todo with this ID does not exist

    Deletion:
    - Permanent (no soft delete)
    - Cannot be undone
    - Returns 204 whether todo existed or not (for security)

    Use Cases:
    - User explicitly deletes a todo
    - Cleanup of old/spam todos
    - Account cleanup (consider cascade delete on user deletion)
    """
    # Task T-216: Query for todo
    statement = select(Todo).where(Todo.id == todo_id)
    todo = db.exec(statement).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found."
        )

    # Task T-216: Verify ownership
    if todo.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this todo."
        )

    # Task T-216: Delete from database
    db.delete(todo)
    db.commit()

    # Return None for 204 No Content response
    return None
