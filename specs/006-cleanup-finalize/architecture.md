# Evo-TODO Architecture & Integration

**Date**: 2026-01-04
**Status**: Phase II Complete
**Branch**: `006-cleanup-finalize`

---

## Architecture Overview

The Evo-TODO application is a full-stack monorepo with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────────┐
│                        User's Browser                           │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │         Next.js Frontend (React Components)           │    │
│  │  ┌──────────────────────────────────────────────────┐  │    │
│  │  │ Landing Page    │ Auth Pages    │ Dashboard      │  │    │
│  │  │ (public)        │ (public)      │ (protected)    │  │    │
│  │  │                 │               │                │  │    │
│  │  │ - Hero          │ - LoginForm   │ - Navbar       │  │    │
│  │  │ - Features      │ - SignupForm  │ - Sidebar      │  │    │
│  │  │ - CTA           │               │ - TodoList     │  │    │
│  │  │ - Social Proof  │               │ - TaskForm     │  │    │
│  │  │ - Footer        │               │ - BulkActions  │  │    │
│  │  └──────────────────────────────────────────────────┘  │    │
│  │                    ↓ (HTTP + JWT)                      │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ HTTPS
                         │ JSON/REST
                         │ JWT Authorization Header
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│              FastAPI Backend (Python)                           │
│              ├── Port: 8000                                     │
│              ├── Runtime: Python 3.13                           │
│              ├── Framework: FastAPI + SQLModel                  │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              Middleware Pipeline                      │    │
│  │  1. CORS validation (check origin)                   │    │
│  │  2. JWT extraction (Authorization header)            │    │
│  │  3. JWT verification (validate signature, expiry)    │    │
│  │  4. User extraction (decode user_id from token)      │    │
│  │  5. Request logging & error handling                 │    │
│  └────────────────────────────────────────────────────────┘    │
│                         ↓                                      │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              Route Handlers (Endpoints)               │    │
│  │                                                        │    │
│  │  /auth/* (Authentication)                            │    │
│  │  ├── POST /signup → Create user, return token        │    │
│  │  ├── POST /signin → Verify creds, return token       │    │
│  │  └── POST /logout → Invalidate token                 │    │
│  │                                                        │    │
│  │  /api/todos/* (Todo CRUD - Protected)                │    │
│  │  ├── GET /todos → List user's todos                  │    │
│  │  ├── POST /todos → Create new todo                   │    │
│  │  ├── GET /todos/{id} → Get specific todo             │    │
│  │  ├── PUT/PATCH /todos/{id} → Update todo             │    │
│  │  └── DELETE /todos/{id} → Delete todo                │    │
│  │                                                        │    │
│  │  All endpoints enforce: WHERE user_id = current_user │    │
│  └────────────────────────────────────────────────────────┘    │
│                         ↓ (SQL)                                │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              SQLModel ORM Layer                       │    │
│  │  ├── Database connection pooling                     │    │
│  │  ├── Table/Model mapping                             │    │
│  │  ├── Relationship management (User → Todos)          │    │
│  │  └── Query building & execution                      │    │
│  └────────────────────────────────────────────────────────┘    │
│                         ↓                                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ PostgreSQL Protocol
                         │ Connection: localhost:5432
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│              PostgreSQL Database                                │
│              ├── Port: 5432                                     │
│              ├── Database: evo_todo                             │
│              │                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │  Tables:                                               │    │
│  │                                                        │    │
│  │  user                                                 │    │
│  │  ├── id (UUID, PRIMARY KEY)                          │    │
│  │  ├── email (VARCHAR, UNIQUE)                         │    │
│  │  ├── name (VARCHAR)                                  │    │
│  │  ├── password_hash (VARCHAR)                         │    │
│  │  ├── created_at (TIMESTAMP)                          │    │
│  │  └── updated_at (TIMESTAMP)                          │    │
│  │                                                        │    │
│  │  todo                                                 │    │
│  │  ├── id (UUID, PRIMARY KEY)                          │    │
│  │  ├── user_id (UUID, FOREIGN KEY → user.id)          │    │
│  │  ├── title (VARCHAR)                                 │    │
│  │  ├── description (TEXT)                              │    │
│  │  ├── is_completed (BOOLEAN)                          │    │
│  │  ├── created_at (TIMESTAMP)                          │    │
│  │  └── updated_at (TIMESTAMP)                          │    │
│  │                                                        │    │
│  │  Indexes:                                             │    │
│  │  ├── user(email) - Fast lookup during login          │    │
│  │  ├── todo(user_id) - Fast lookup of user's todos     │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Frontend Architecture

### Page Hierarchy (Next.js App Router)

```
app/
├── layout.tsx (Root)
│   ├── Providers (Auth, Theme)
│   ├── Metadata
│   └── Global CSS
│
├── page.tsx (Landing)
│   └── Landing Components
│
├── (auth)/ (Public routes)
│   ├── login/page.tsx
│   │   └── LoginForm component
│   └── signup/page.tsx
│       └── SignupForm component
│
└── (protected)/ (Protected routes)
    ├── Middleware redirect if not authenticated
    │
    ├── page.tsx (Dashboard redirect)
    │
    └── dashboard/layout.tsx
        ├── Navbar
        ├── Sidebar
        └── Children:
            ├── page.tsx (Dashboard home)
            └── todos/page.tsx
                └── TasksContainer + related components
```

### Component Data Flow

```
Landing Page
├── Landing Components (static content)
│   ├── Hero Section
│   ├── Features
│   ├── CTA
│   ├── Social Proof
│   └── Footer

Auth Pages
├── LoginForm
│   ├── Input validation
│   ├── API call via useTodos hook
│   ├── JWT storage
│   └── Redirect to dashboard
└── SignupForm
    ├── Input validation
    ├── API call via useTodos hook
    ├── JWT storage
    └── Redirect to dashboard

Dashboard
├── DashboardUI (Layout)
│   ├── Navbar
│   │   ├── User info
│   │   └── Logout button
│   ├── Sidebar
│   │   ├── Navigation
│   │   └── Links
│   └── Main content:
│       ├── Todo List Page
│       │   ├── TasksContainer (state management)
│       │   │   ├── useTodos hook (API operations)
│       │   │   ├── Fetch todos on mount
│       │   │   └── Manage CRUD operations
│       │   ├── TaskForm (create/edit)
│       │   │   ├── Input fields
│       │   │   ├── Validation
│       │   │   └── Submit → useTodos.create()
│       │   ├── TaskList
│       │   │   └── TaskItem (x many)
│       │   │       ├── Display todo
│       │   │       ├── Update button → useTodos.update()
│       │   │       └── Delete button → useTodos.delete()
│       │   └── BulkActions
│       │       ├── Select/deselect all
│       │       └── Bulk delete
│       └── LoadingSpinner / EmptyState
```

### Authentication Flow

```
1. User visits app
   ↓
2. Middleware checks for JWT token in cookies
   ├─ Token found & valid → allow access to protected routes
   └─ No token or invalid → redirect to login
   ↓
3. User clicks "Sign Up"
   ├─ Fills form (email, password, name)
   ├─ Frontend validates locally
   ├─ Sends POST /auth/signup {email, password, name}
   ├─ Backend:
   │   ├─ Validates input
   │   ├─ Hashes password
   │   ├─ Stores user in database
   │   └─ Generates JWT token
   ├─ Frontend receives JWT
   ├─ Stores JWT in cookie (httpOnly, secure)
   └─ Redirects to dashboard
   ↓
4. User clicks "Sign In"
   ├─ Fills form (email, password)
   ├─ Sends POST /auth/signin {email, password}
   ├─ Backend:
   │   ├─ Looks up user by email
   │   ├─ Verifies password hash
   │   └─ Generates JWT token
   ├─ Frontend receives JWT
   ├─ Stores in cookie
   └─ Redirects to dashboard
   ↓
5. Subsequent requests (todos, etc.)
   ├─ Frontend includes JWT in Authorization header
   ├─ Backend middleware:
   │   ├─ Extracts JWT from header
   │   ├─ Verifies JWT signature
   │   ├─ Checks expiration
   │   └─ Extracts user_id from token
   ├─ Backend route handler:
   │   ├─ Receives current_user_id
   │   └─ Scopes all queries by user_id
   └─ Response returns only user's data
   ↓
6. User logs out
   ├─ Clicks logout button
   ├─ Frontend sends POST /auth/logout
   ├─ Frontend clears JWT from cookies
   └─ Redirects to landing page
```

### State Management

```
Frontend State:
├── Authentication State (useAuth hook)
│   ├── Current user (id, email, name)
│   ├── JWT token
│   ├── Loading state
│   └── Error state
│
├── Todo State (useTodos hook)
│   ├── Todos list
│   ├── Loading state
│   ├── Error state
│   ├── CRUD operation methods:
│   │   ├── create(title, description)
│   │   ├── read(id)
│   │   ├── update(id, changes)
│   │   └── delete(id)
│   └── Fetch methods:
│       └── getTodos()
│
├── Bulk Selection State (useBulkSelection hook)
│   ├── Selected todo IDs
│   ├── Toggle methods
│   └── Bulk delete method
│
└── Theme State (useTheme hook)
    ├── Current theme (light/dark)
    └── Toggle method
```

---

## Backend Architecture

### Request Lifecycle

```
1. HTTP Request arrives at FastAPI
   ├─ URL: /api/todos/{id}
   ├─ Method: PUT
   ├─ Headers: Authorization: Bearer {JWT_TOKEN}, Content-Type: application/json
   └─ Body: {title: "New title", description: "New description"}

2. CORS Middleware
   ├─ Validate origin (must be in CORS_ORIGINS)
   └─ Add CORS headers

3. JWT Middleware
   ├─ Extract "Bearer {token}" from Authorization header
   ├─ Verify JWT signature using JWT_SECRET_KEY
   ├─ Check expiration
   ├─ Decode payload
   └─ Extract user_id → attach to request context

4. Route Handler (deps injected)
   ├─ get_current_user() → returns User from database
   ├─ get_db() → returns database session
   ├─ Path parameter: id
   ├─ Request body: UpdateTodoSchema
   │
   └─ Handler logic:
      ├─ Query todo WHERE id = {id} AND user_id = {current_user.id}
      ├─ If not found → 404 Not Found
      ├─ Update fields:
      │   ├─ title
      │   ├─ description
      │   └─ updated_at = now()
      ├─ Save to database
      ├─ Return updated Todo

5. Response
   ├─ Status: 200 OK (or 404 if not found)
   ├─ Headers: Content-Type: application/json
   └─ Body: {id, user_id, title, description, is_completed, created_at, updated_at}
```

### Endpoint Security Model

All protected endpoints follow this pattern:

```python
@router.put("/api/todos/{todo_id}")
def update_todo(
    todo_id: UUID,
    todo_update: UpdateTodoSchema,
    current_user: User = Depends(get_current_user),  # Auth check
    db: Session = Depends(get_db)  # Database session
):
    # Query ONLY this user's todos
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.user_id == current_user.id  # USER DATA ISOLATION
    ).first()

    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Update
    todo.title = todo_update.title
    todo.updated_at = datetime.utcnow()
    db.commit()
    return todo
```

**Key Security Features**:
1. `get_current_user` dependency enforces JWT validation
2. Every query includes `user_id == current_user.id` filter
3. User cannot access other users' todos (even if they guess the ID)
4. Middleware validates JWT before reaching handler

---

## Data Flow Examples

### Create Todo

```
Frontend:
1. User fills form (title, description)
2. Clicks "Create"
3. useTodos.create() called:
   ├─ POST /api/todos
   ├─ Body: {title, description}
   ├─ Header: Authorization: Bearer {JWT}
   └─ State: loading = true

Backend:
4. Middleware extracts user_id from JWT
5. Route handler:
   ├─ Create Todo object:
   │   ├─ id = generate UUID
   │   ├─ user_id = current_user.id
   │   ├─ title = request.title
   │   ├─ description = request.description
   │   ├─ is_completed = false
   │   ├─ created_at = now()
   │   └─ updated_at = now()
   ├─ Insert into database
   └─ Return Todo (201 Created)

Frontend:
6. Receive response with new Todo
7. Update todos state: [...todos, newTodo]
8. Clear form
9. State: loading = false
10. User sees new todo in list
```

### Update Todo

```
Frontend:
1. User clicks edit button on todo
2. Form pre-fills with current data
3. User changes status/description
4. Clicks "Save"
5. useTodos.update(id, changes) called:
   ├─ PATCH /api/todos/{id}
   ├─ Body: {is_completed: true} or {description: "New desc"}
   └─ Header: Authorization: Bearer {JWT}

Backend:
6. Middleware extracts user_id from JWT
7. Route handler:
   ├─ Query todo WHERE id = {id} AND user_id = {current_user.id}
   ├─ Update specified fields
   ├─ Set updated_at = now()
   ├─ Save to database
   └─ Return updated Todo

Frontend:
8. Receive updated Todo
9. Update state:
   ├─ Find existing todo by id
   ├─ Merge changes: {...old, ...changes}
   └─ Update list
10. Show updated todo to user
```

### Delete Todo

```
Frontend:
1. User clicks delete button
2. Shows confirmation dialog
3. User confirms
4. useTodos.delete(id) called:
   ├─ DELETE /api/todos/{id}
   └─ Header: Authorization: Bearer {JWT}

Backend:
5. Middleware extracts user_id from JWT
6. Route handler:
   ├─ Query todo WHERE id = {id} AND user_id = {current_user.id}
   ├─ If not found → 404
   ├─ Delete from database
   └─ Return 204 No Content

Frontend:
7. Receive success (204)
8. Update state:
   ├─ Remove todo with matching id
   └─ Update list
9. User sees todo removed
```

---

## Error Handling

### Backend Error Responses

```json
// 400 Bad Request
{
  "detail": "Validation error: title cannot be empty"
}

// 401 Unauthorized
{
  "detail": "Invalid or expired token"
}

// 403 Forbidden
{
  "detail": "Access denied"
}

// 404 Not Found
{
  "detail": "Todo not found"
}

// 500 Internal Server Error
{
  "detail": "An unexpected error occurred"
}
```

### Frontend Error Handling

```javascript
try {
  const result = await api.updateTodo(id, changes);
  setTodos(...);
} catch (error) {
  if (error.status === 401) {
    // Redirect to login (token expired)
    navigate('/login');
  } else if (error.status === 404) {
    // Show "Todo not found" message
    showError('This todo no longer exists');
  } else {
    // Show generic error
    showError('Failed to update todo: ' + error.detail);
  }
}
```

---

## Performance Considerations

### Frontend Optimization
- Components lazy-loaded via Next.js dynamic imports
- useTodos hook caches results to avoid refetches
- CSS-in-JS compiled to CSS at build time (Tailwind)
- TypeScript provides compile-time type safety

### Backend Optimization
- Database connection pooling (SQLModel)
- Indexes on frequently queried fields:
  - `user(email)` for login lookup
  - `todo(user_id)` for user's todos
- JWT validation at middleware (early rejection of bad requests)
- Stateless design (can scale horizontally)

### Database Optimization
- Foreign key constraint on `todo.user_id`
- Cascading delete (user deletion removes todos)
- UNIQUE constraint on email (fast lookup)
- Timestamps for audit trails

---

## Security Model

### Authentication
- **Method**: JWT (JSON Web Tokens) with HS256 signature
- **Secret**: 256-bit random key stored in environment
- **Expiration**: 7 days (configurable)
- **Storage**: HTTP-only cookie (frontend), cannot access via JavaScript

### Authorization
- **User Isolation**: Every database query filtered by `user_id`
- **Token Scope**: JWT contains only `user_id` (minimal surface area)
- **No Direct IDs in URLs**: Todos accessed via ID, but authorization still checked
- **CORS**: Only specified origins allowed

### Password Security
- **Hashing**: Passwords hashed with bcrypt (not stored plaintext)
- **Validation**: Always check hashed password, never return plaintext
- **HTTP**: HTTPS enforced in production

---

## Deployment Architecture

### Development (Docker Compose)
```
docker-compose up
├── PostgreSQL (localhost:5432)
├── FastAPI (localhost:8000)
└── Next.js (localhost:3000)
```

### Production (Example AWS)
```
User Browser
    ↓
CloudFront CDN
    ├─ Frontend (S3)
    ├─ API (EC2/ECS)
    └─ Database (RDS PostgreSQL)
```

---

## Technology Stack Summary

| Layer | Component | Technology | Purpose |
|-------|-----------|-----------|---------|
| **Frontend** | UI Framework | React 19+ | Component-based UI |
| | Meta Framework | Next.js 16+ | Routing, SSR, optimization |
| | Language | TypeScript | Type safety |
| | Styling | Tailwind CSS | Utility-first CSS |
| | UI Components | shadcn/ui | Pre-built accessible components |
| | Auth Client | Better Auth | Frontend auth integration |
| **Backend** | Framework | FastAPI | REST API |
| | Language | Python 3.13 | Server runtime |
| | ORM | SQLModel | Database access |
| | Database | PostgreSQL | Data persistence |
| | Auth | JWT (HS256) | Token-based auth |
| **DevOps** | Containers | Docker | Reproducible environments |
| | Orchestration | Docker Compose | Local multi-service setup |

