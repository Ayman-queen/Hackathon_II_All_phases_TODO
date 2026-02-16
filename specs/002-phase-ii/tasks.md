# Phase II Tasks: Full-Stack Todo Application Implementation

**Specification**: [specs/002-phase-ii/spec.md](./spec.md)
**Plan**: [specs/002-phase-ii/plan.md](./plan.md)
**Branch**: `phase-2` (from `001-cli-todo`)
**Created**: 2025-12-29

---

## Task Overview

**Total Tasks**: 46 atomic tasks (42 original + 4 corrective Better Auth/Neon tasks)
**Estimated Duration**: 12 days (including Better Auth integration + Neon migration)
**Task ID Format**: T-XXX (e.g., T-201, T-221 for corrective tasks)
**Status Tracking**: ⏳ Pending → 🔄 In Progress → ✅ Complete

**Corrective Tasks** (Better Auth + Neon):
- T-221: Install Better Auth and configure JWT plugin
- T-222: Refactor FastAPI middleware to decode Better Auth JWTs
- T-223: Connect application to Neon Serverless PostgreSQL
- T-224: Filter all Todo CRUD operations by verified user_id from token

**⚠️ CRITICAL**: T-221-T-224 replace custom JWT/bcrypt implementation (T-213, T-214, T-215). Spec mandate per hackathon constitution.

---

## Phase 2.1: Monorepo Infrastructure Setup (Days 1-2)

### T-201: Initialize Next.js 16+ with App Router

**Description**: Create frontend directory with Next.js 16+ using App Router, TypeScript, Tailwind CSS.

**Acceptance Criteria**:
- [x] `frontend/` directory created with Next.js 16+ scaffolding
- [x] `package.json` with required dependencies (Next.js, React, TypeScript)
- [x] `tsconfig.json` configured for App Router
- [x] `app/` directory with `layout.tsx` and `page.tsx`
- [x] `app/globals.css` with Tailwind CSS base styles
- [x] `.env.example` created with `NEXT_PUBLIC_API_URL` placeholder
- [x] `npm run dev` starts development server on port 3000
- [x] No TypeScript errors or warnings

**Branch**: `phase2-001-init-nextjs-fastapi`
**Related Files**: `frontend/package.json`, `frontend/tsconfig.json`, `frontend/app/`
**Dependencies**: None (starting task)
**Blockers**: None

**Test Cases**:
```bash
# T-201.1: Frontend builds without errors
cd frontend && npm install && npm run build
# Expected: Build succeeds, .next directory created

# T-201.2: Dev server starts on port 3000
cd frontend && npm run dev &
# Expected: Server listens on http://localhost:3000

# T-201.3: TypeScript compilation clean
cd frontend && npx tsc --noEmit
# Expected: 0 errors, 0 warnings
```

**Time Estimate**: 1 hour
**Priority**: P1 (Critical path)

---

### T-202: Initialize FastAPI with Python 3.13

**Description**: Create backend directory with FastAPI scaffolding, Python 3.13, uv package manager.

**Acceptance Criteria**:
- [x] `backend/` directory created with FastAPI project structure
- [x] `backend/pyproject.toml` configured with dependencies (FastAPI, SQLModel, python-jose, passlib, bcrypt)
- [x] `backend/app/main.py` with FastAPI application instance
- [x] `backend/app/__init__.py` empty or imports main app
- [x] `backend/.env.example` with DATABASE_URL, JWT_SECRET_KEY, CORS_ORIGINS
- [x] Virtual environment created with `uv sync`
- [x] `uvicorn` server starts on port 8000
- [x] Health check endpoint returns 200

**Branch**: `phase2-001-init-nextjs-fastapi` (same as T-201)
**Related Files**: `backend/pyproject.toml`, `backend/app/main.py`
**Dependencies**: None (parallel to T-201)
**Blockers**: None

**Test Cases**:
```bash
# T-202.1: Dependencies install with uv
cd backend && uv sync
# Expected: All dependencies installed, .venv created

# T-202.2: Dev server starts on port 8000
cd backend && uvicorn app.main:app --reload &
# Expected: Server listens on http://localhost:8000

# T-202.3: Health check endpoint
curl http://localhost:8000/health || curl http://localhost:8000/docs
# Expected: 200 OK response
```

**Time Estimate**: 1 hour
**Priority**: P1 (Critical path)

---

### T-203: Create Docker Compose Configuration

**Description**: Set up Docker Compose with PostgreSQL, FastAPI backend, Next.js frontend services for local development.

**Acceptance Criteria**:
- [x] `docker-compose.yml` created with 3 services: postgres, backend, frontend
- [x] PostgreSQL service configured with health check (pg_isready)
- [x] Backend service builds from `backend/Dockerfile`, depends on postgres health
- [x] Frontend service builds from `frontend/Dockerfile`, depends on backend
- [x] Environment variables passed from `.env` file
- [x] Volumes for postgres data persistence
- [x] Port mappings: postgres 5432, backend 8000, frontend 3000
- [x] `docker-compose up` starts all services without errors
- [x] Services communicate (backend can connect to postgres, frontend to backend)

**Branch**: `phase2-001-init-nextjs-fastapi` (same as T-201)
**Related Files**: `docker-compose.yml`, `backend/Dockerfile`, `frontend/Dockerfile`
**Dependencies**: T-201, T-202 (need existing Dockerfiles)
**Blockers**: None

**Test Cases**:
```bash
# T-203.1: Compose file validates
docker-compose config > /dev/null
# Expected: Valid YAML, no errors

# T-203.2: All services start
docker-compose up -d && sleep 10
# Expected: 3 services running (postgres, backend, frontend)

# T-203.3: Services communication
docker-compose exec backend curl http://localhost:3000
# Expected: 200 or connection response from frontend

# T-203.4: Database ready
docker-compose exec postgres pg_isready -U evo_todo_user
# Expected: accepting connections
```

**Time Estimate**: 1 hour
**Priority**: P1 (Critical path)

---

### T-204: Create Backend Dockerfile

**Description**: Configure Docker image for FastAPI backend with Python 3.13, dependencies, uvicorn server.

**Acceptance Criteria**:
- [x] `backend/Dockerfile` created with Python 3.13 base image
- [x] Dependencies installed via `uv` (not pip)
- [x] Working directory set to `/app`
- [x] Startup command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- [x] Healthcheck configured (optional, recommended)
- [x] Image builds without warnings
- [x] Image size reasonable (< 500MB)

**Branch**: `phase2-001-init-nextjs-fastapi`
**Related Files**: `backend/Dockerfile`, `backend/.dockerignore`
**Dependencies**: T-202
**Blockers**: None

**Test Cases**:
```bash
# T-204.1: Dockerfile builds
cd backend && docker build -t evo-todo-backend . --no-cache
# Expected: Build succeeds, no errors

# T-204.2: Container runs and health check
docker run -p 8000:8000 evo-todo-backend &
sleep 3 && curl http://localhost:8000/docs
# Expected: 200 OK, FastAPI docs available
```

**Time Estimate**: 30 minutes
**Priority**: P1

---

### T-205: Create Frontend Dockerfile

**Description**: Configure Docker image for Next.js frontend with Node.js, npm, production build.

**Acceptance Criteria**:
- [x] `frontend/Dockerfile` created with Node.js base image (latest stable)
- [x] Supports multi-stage build (builder → runtime) for smaller final image
- [x] Dependencies installed via npm/yarn
- [x] Next.js build command executed in builder stage
- [x] Startup command: `npm run start` (or `next start`)
- [x] NEXT_PUBLIC_API_URL environment variable configured
- [x] Image builds without warnings
- [x] Image size reasonable (< 300MB)

**Branch**: `phase2-001-init-nextjs-fastapi`
**Related Files**: `frontend/Dockerfile`, `frontend/.dockerignore`
**Dependencies**: T-201
**Blockers**: None

**Test Cases**:
```bash
# T-205.1: Dockerfile builds
cd frontend && docker build -t evo-todo-frontend . --no-cache
# Expected: Build succeeds, no errors

# T-205.2: Container runs and serves on 3000
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://localhost:8000 evo-todo-frontend &
sleep 5 && curl http://localhost:3000
# Expected: 200 OK, Next.js app available
```

**Time Estimate**: 30 minutes
**Priority**: P1

---

### T-206: Create Environment Templates

**Description**: Create `.env.example` files for backend, frontend, and root with all required variables documented.

**Acceptance Criteria**:
- [x] `backend/.env.example` with DATABASE_URL, JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRATION_HOURS, CORS_ORIGINS
- [x] `frontend/.env.example` with NEXT_PUBLIC_API_URL
- [x] `.env.example` (root) with JWT_SECRET_KEY, POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_DB
- [x] All variables have helpful comments
- [x] No sensitive values in examples (use placeholders)
- [x] All variables have valid example values (not empty)

**Branch**: `phase2-001-init-nextjs-fastapi`
**Related Files**: `backend/.env.example`, `frontend/.env.example`, `.env.example`
**Dependencies**: T-202, T-201
**Blockers**: None

**Test Cases**:
```bash
# T-206.1: All .env.example files exist
[ -f backend/.env.example ] && [ -f frontend/.env.example ] && [ -f .env.example ]
# Expected: All files exist

# T-206.2: No empty values
grep -E '=\s*$' backend/.env.example frontend/.env.example .env.example
# Expected: No matches (all have values)
```

**Time Estimate**: 30 minutes
**Priority**: P2

---

### T-207: Create Root README with Setup Instructions

**Description**: Document monorepo structure, setup instructions, running services locally with Docker Compose.

**Acceptance Criteria**:
- [x] `README.md` at root explains monorepo structure (frontend, backend, docker-compose)
- [x] Prerequisites listed (Docker, Docker Compose, Node.js, Python 3.13, uv)
- [x] Quick start section: clone → setup → run
- [x] Environment setup instructions (copy .env.example, configure)
- [x] Docker Compose section: up, down, logs, exec commands
- [x] Development section: running services separately (npm run dev, uvicorn)
- [x] Testing section: running tests
- [x] Troubleshooting section: common issues

**Branch**: `phase2-001-init-nextjs-fastapi`
**Related Files**: `README.md`
**Dependencies**: T-201 through T-206
**Blockers**: None

**Test Cases**:
```bash
# T-207.1: README exists and is readable
[ -f README.md ] && head -20 README.md
# Expected: README displays with clear structure
```

**Time Estimate**: 1 hour
**Priority**: P2

---

## Phase 2.2: Database Schema & SQLModel (Days 2-3)

### T-208: Create SQLModel User Entity

**Description**: Implement User model in SQLModel with all fields: id, email, password_hash, name, is_active, created_at, updated_at.

**Acceptance Criteria**:
- [x] `backend/app/models/user.py` created with User SQLModel class
- [x] Fields: id (UUID, PK), email (unique, indexed), password_hash, name (optional), is_active (default true)
- [x] Timestamps: created_at, updated_at (auto-set to utcnow)
- [x] Table name: `users`
- [x] Email field indexed for efficient lookup
- [x] UUID primary key (not auto-increment integer)
- [x] is_active field for soft-delete capability

**Branch**: `phase2-002-setup-sqlmodel-db`
**Related Files**: `backend/app/models/user.py`, `backend/app/models/database.py`
**Dependencies**: T-202
**Blockers**: None

**Test Cases**:
```python
# T-208.1: User model imports and instantiates
from backend.app.models.user import User
user = User(email="test@example.com", password_hash="...", name="Test")
assert user.email == "test@example.com"
assert user.is_active == True

# T-208.2: UUID primary key generated
assert user.id is not None
assert isinstance(user.id, UUID)
```

**Time Estimate**: 30 minutes
**Priority**: P1

---

### T-209: Create SQLModel Todo Entity

**Description**: Implement Todo model in SQLModel with user_id foreign key and all fields: id, user_id, title, description, is_complete, created_at, updated_at.

**Acceptance Criteria**:
- [x] `backend/app/models/todo.py` created with Todo SQLModel class
- [x] Fields: id (UUID, PK), user_id (FK to users.id), title (max 500), description (optional, max 2000), is_complete (default false)
- [x] Timestamps: created_at, updated_at (auto-set)
- [x] Table name: `todos`
- [x] Foreign key constraint on user_id → users.id
- [x] Composite index on (user_id, created_at DESC) for query efficiency
- [x] ON DELETE CASCADE for user deletion (optional, can be added later)

**Branch**: `phase2-002-setup-sqlmodel-db`
**Related Files**: `backend/app/models/todo.py`
**Dependencies**: T-208
**Blockers**: None

**Test Cases**:
```python
# T-209.1: Todo model imports and instantiates
from backend.app.models.todo import Todo
todo = Todo(user_id=user_id, title="Test Todo", description="...")
assert todo.title == "Test Todo"
assert todo.is_complete == False

# T-209.2: Foreign key field present
assert hasattr(todo, 'user_id')
assert todo.user_id == user_id
```

**Time Estimate**: 30 minutes
**Priority**: P1

---

### T-210: Configure Database Connection

**Description**: Set up SQLModel database engine with PostgreSQL connection, session management, and initialization function.

**Acceptance Criteria**:
- [x] `backend/app/models/database.py` created with engine and session management
- [x] DATABASE_URL from config used to create engine
- [x] `get_db()` dependency function yields Session objects
- [x] `init_db()` function calls SQLModel.metadata.create_all(engine)
- [x] Connection pooling configured (optional, recommended)
- [x] Health check function (test connection)

**Branch**: `phase2-002-setup-sqlmodel-db`
**Related Files**: `backend/app/models/database.py`, `backend/app/models/__init__.py`
**Dependencies**: T-208, T-209
**Blockers**: None

**Test Cases**:
```python
# T-210.1: Database engine created
from backend.app.models.database import engine
assert engine is not None

# T-210.2: Session dependency works
from backend.app.models.database import get_db
session = next(get_db())
assert session is not None
session.close()

# T-210.3: Tables created
from backend.app.models.database import init_db
init_db()
# Expected: No errors, tables exist in database
```

**Time Estimate**: 30 minutes
**Priority**: P1

---

### T-211: Create User Pydantic Schemas

**Description**: Implement Pydantic schemas for User API: UserCreate, UserResponse, TokenResponse.

**Acceptance Criteria**:
- [x] `backend/app/schemas/user.py` created
- [x] UserCreate schema: email (EmailStr), password (string, min 8 chars), name (optional)
- [x] UserResponse schema: id, email, name, created_at (no password_hash)
- [x] TokenResponse schema: access_token, token_type ("bearer"), user (UserResponse)
- [x] All schemas use Pydantic BaseModel
- [x] Email validation using EmailStr
- [x] from_attributes = True for SQLModel conversion

**Branch**: `phase2-002-setup-sqlmodel-db`
**Related Files**: `backend/app/schemas/user.py`
**Dependencies**: T-208
**Blockers**: None

**Test Cases**:
```python
# T-211.1: UserCreate validates email
from backend.app.schemas.user import UserCreate
user = UserCreate(email="test@example.com", password="password123")
assert user.email == "test@example.com"

# T-211.2: Invalid email rejected
try:
    UserCreate(email="invalid", password="password123")
    assert False, "Should reject invalid email"
except:
    pass  # Expected

# T-211.3: TokenResponse includes user
from backend.app.schemas.user import TokenResponse
token_resp = TokenResponse(access_token="...", user=user_response)
assert token_resp.user is not None
```

**Time Estimate**: 30 minutes
**Priority**: P1

---

### T-212: Create Todo Pydantic Schemas

**Description**: Implement Pydantic schemas for Todo API: TodoCreate, TodoUpdate, TodoToggle, TodoResponse, TodoListResponse.

**Acceptance Criteria**:
- [x] `backend/app/schemas/todo.py` created
- [x] TodoCreate: title (required, 1-500 chars), description (optional, max 2000)
- [x] TodoUpdate: title (optional), description (optional)
- [x] TodoToggle: is_complete (required boolean)
- [x] TodoResponse: id, user_id, title, description, is_complete, created_at, updated_at
- [x] TodoListResponse: todos (list), total (count)
- [x] from_attributes = True for SQLModel conversion

**Branch**: `phase2-002-setup-sqlmodel-db`
**Related Files**: `backend/app/schemas/todo.py`
**Dependencies**: T-209
**Blockers**: None

**Test Cases**:
```python
# T-212.1: TodoCreate validates title
from backend.app.schemas.todo import TodoCreate
todo = TodoCreate(title="Test")
assert todo.title == "Test"

# T-212.2: Empty title rejected
try:
    TodoCreate(title="")
    assert False, "Should reject empty title"
except:
    pass  # Expected

# T-212.3: Long title rejected
try:
    TodoCreate(title="x" * 501)
    assert False, "Should reject title > 500"
except:
    pass  # Expected
```

**Time Estimate**: 30 minutes
**Priority**: P1

---

## Phase 2.3: Better Auth Integration with JWT (Days 3-4)

**⚠️ CORRECTIVE PHASE**: Replace custom JWT/bcrypt (T-213, T-214, T-215) with Better Auth service integration. Better Auth handles authentication; FastAPI validates Better Auth JWTs and extracts user_id.

### T-221: Install Better Auth and Configure JWT Plugin

**Description**: Install Better Auth Python client, configure JWT plugin with shared secret, set up Better Auth environment variables.

**Acceptance Criteria**:
- [x] `better-auth` Python package installed via `uv add better-auth`
- [x] `BETTER_AUTH_SECRET` environment variable configured in `.env`
- [x] `BETTER_AUTH_API_URL` configured (Better Auth service endpoint)
- [x] `backend/app/core/auth.py` created with Better Auth client initialization
- [x] Better Auth JWT plugin configured with HS256 algorithm
- [x] JWT_EXPIRATION set to 7 days (168 hours)
- [x] `/backend/.env.example` updated with Better Auth variables
- [x] No import errors; Better Auth client accessible from `backend.app.core.auth`

**Branch**: `phase2-003-better-auth-neon`
**Related Files**: `backend/app/core/auth.py`, `backend/.env`, `backend/pyproject.toml`
**Dependencies**: T-202 (FastAPI backend initialized)
**Blockers**: Better Auth service account created and API key generated

**Test Cases**:
```python
# T-221.1: Better Auth client imports without error
from backend.app.core.auth import better_auth_client
assert better_auth_client is not None

# T-221.2: JWT verification function available
from backend.app.core.auth import verify_better_auth_token
# Verify function exists and is callable
assert callable(verify_better_auth_token)

# T-221.3: Environment variables loaded
import os
assert os.getenv("BETTER_AUTH_SECRET") is not None
assert os.getenv("BETTER_AUTH_API_URL") is not None
```

**Time Estimate**: 1 hour
**Priority**: P1

---

### T-222: Refactor FastAPI Middleware to Decode Better Auth JWTs

**Description**: Create FastAPI JWT validation middleware that decodes Better Auth tokens, extracts user_id from `sub` claim, and validates token signature.

**Acceptance Criteria**:
- [x] `backend/app/api/deps.py` created/updated with `get_current_user()` dependency
- [x] `get_current_user()` extracts JWT from Authorization header (Bearer scheme)
- [x] Calls `verify_better_auth_token(token)` to validate signature and expiration
- [x] Extracts user_id from token's `sub` claim
- [x] Queries database for User by user_id
- [x] Returns User object on success
- [x] Raises HTTPException 401 if token missing or invalid
- [x] Raises HTTPException 401 if token expired
- [x] Raises HTTPException 401 if user_id not found in database
- [x] Error messages do NOT leak info (generic "Unauthorized" message)

**Branch**: `phase2-003-better-auth-neon`
**Related Files**: `backend/app/api/deps.py`, `backend/app/models/user.py`
**Dependencies**: T-221, T-208 (User model exists)
**Blockers**: None

**Test Cases**:
```python
# T-222.1: Missing token returns 401
from fastapi.testclient import TestClient
from backend.app.main import app
client = TestClient(app)
response = client.get("/api/todos")
assert response.status_code == 401
assert "Unauthorized" in response.json()["detail"]

# T-222.2: Invalid/malformed token returns 401
response = client.get(
    "/api/todos",
    headers={"Authorization": "Bearer invalid.token.here"}
)
assert response.status_code == 401

# T-222.3: Valid Better Auth JWT extracts user_id
# (Will be tested in T-224 after auth endpoints are available)
```

**Time Estimate**: 1.5 hours
**Priority**: P1

---

### T-223: Connect Application to Neon Serverless PostgreSQL

**Description**: Create Neon PostgreSQL project, migrate DATABASE_URL from local Docker to Neon connection string, configure connection pooling for serverless.

**Acceptance Criteria**:
- [x] Neon PostgreSQL project created (via Neon console or CLI)
- [x] Neon connection string obtained (postgresql://user:password@host/dbname)
- [x] `DATABASE_URL` in `.env` updated to Neon connection string
- [x] `.env.example` updated with Neon connection string template
- [x] SQLModel connection pooling configured for serverless (connection timeout, pool size)
- [x] `backend/app/models/database.py` updated with Neon-compatible settings
- [x] Database health check endpoint returns 200 when connected to Neon
- [x] SQLModel.metadata.create_all() runs successfully against Neon
- [x] All existing tables (User, Todo) created in Neon
- [x] No SQL migration tool needed (SQLModel handles DDL)

**Branch**: `phase2-003-better-auth-neon`
**Related Files**: `.env`, `backend/app/models/database.py`, `backend/app/core/config.py`
**Dependencies**: T-202 (FastAPI initialized), T-208 (schema models exist)
**Blockers**: Neon account created; connection credentials available

**Test Cases**:
```bash
# T-223.1: Connection to Neon succeeds
cd backend && python -c "from app.models.database import engine; conn = engine.connect(); print('Connected'); conn.close()"

# T-223.2: Database tables created
# Query Neon to verify users, todos tables exist
psql $DATABASE_URL -c "\dt"
# Expected: tables list includes 'user' and 'todo'

# T-223.3: Health check endpoint connects to Neon
curl http://localhost:8000/health
# Expected: 200 OK
```

**Time Estimate**: 1 hour
**Priority**: P1

---

### T-224: Filter All Todo CRUD Operations by Verified user_id from Token

**Description**: Update all Todo endpoints to extract user_id from Better Auth JWT claims (via get_current_user dependency) and filter queries to enforce data isolation.

**Acceptance Criteria**:
- [x] `GET /api/todos` filters todos: `WHERE user_id = current_user.id`
- [x] `GET /api/todos/{id}` filters by user_id AND checks ownership (403 if not owner)
- [x] `POST /api/todos` sets user_id automatically from current_user.id
- [x] `PUT /api/todos/{id}` filters by user_id and rejects if not owner (403)
- [x] `PATCH /api/todos/{id}` filters by user_id and rejects if not owner (403)
- [x] `DELETE /api/todos/{id}` filters by user_id and rejects if not owner (403)
- [x] All endpoints use `Depends(get_current_user)` to inject authenticated user
- [x] All queries enforce user isolation at database query level (defense in depth)
- [x] User A cannot see/modify User B's todos (query returns empty or 403)
- [x] All endpoints documented with @app.* decorators (tags, responses)

**Branch**: `phase2-003-better-auth-neon`
**Related Files**: `backend/app/api/todos.py`, `backend/app/core/config.py`
**Dependencies**: T-222 (get_current_user available), T-216 (Todo endpoints exist)
**Blockers**: None

**Test Cases**:
```python
# T-224.1: User can only see their own todos
# Create 2 users (via signup with different emails)
user1_token = "better_auth_jwt_for_user1"
user2_token = "better_auth_jwt_for_user2"

# User1 creates a todo
response = client.post(
    "/api/todos",
    json={"title": "User1 Todo"},
    headers={"Authorization": f"Bearer {user1_token}"}
)
assert response.status_code == 201

# User2 tries to list todos (should see only their own, not User1's)
response = client.get(
    "/api/todos",
    headers={"Authorization": f"Bearer {user2_token}"}
)
todos = response.json()["todos"]
assert len(todos) == 0  # User2 has no todos
assert all(t["user_id"] == user2_id for t in todos)

# T-224.2: User cannot modify other user's todo
user1_todo_id = "todo_created_by_user1"
response = client.put(
    f"/api/todos/{user1_todo_id}",
    json={"title": "Hacked!"},
    headers={"Authorization": f"Bearer {user2_token}"}
)
assert response.status_code == 403  # Forbidden

# T-224.3: User cannot delete other user's todo
response = client.delete(
    f"/api/todos/{user1_todo_id}",
    headers={"Authorization": f"Bearer {user2_token}"}
)
assert response.status_code == 403  # Forbidden
```

**Time Estimate**: 2 hours
**Priority**: P1

---

## Phase 2.4: Todo CRUD API with User Scoping (Days 4-5)

### T-216: Implement Todo CRUD Endpoints

**Description**: Create 6 REST endpoints for todo operations: GET list, GET one, POST create, PUT update, PATCH toggle, DELETE.

**Acceptance Criteria**:
- [x] `backend/app/api/todos.py` created with 6 endpoints
- [x] GET /api/todos: returns list of user's todos (scoped by user_id)
  - Supports pagination (skip, limit query params)
  - Supports filtering by is_complete
  - Returns 401 if not authenticated
- [x] POST /api/todos: creates new todo (scoped to authenticated user)
  - Requires title (non-empty, max 500)
  - Description optional (max 2000)
  - Returns 400 for validation errors
  - Returns 201 with created todo on success
- [x] GET /api/todos/{id}: returns single todo with ownership check
  - Returns 404 if not found
  - Returns 403 if user doesn't own it
- [x] PUT /api/todos/{id}: updates title and/or description
  - Validates ownership (403 if not owner)
  - Validates input (title non-empty if provided)
  - Returns 200 with updated todo on success
- [x] PATCH /api/todos/{id}: toggles is_complete status
  - Validates ownership (403 if not owner)
  - Returns 200 with updated todo on success
- [x] DELETE /api/todos/{id}: deletes todo permanently
  - Validates ownership (403 if not owner)
  - Returns 204 on success
  - Returns 404 if not found
- [x] All endpoints require valid JWT (401 if missing)
- [x] All endpoints filter by user_id (WHERE user_id = current_user.id)

**Branch**: `phase2-004-rest-api-endpoints`
**Related Files**: `backend/app/api/todos.py`, `backend/app/main.py` (route registration)
**Dependencies**: T-214, T-215, T-209, T-210, T-212
**Blockers**: None

**Test Cases**:
```python
# T-216.1: List todos (empty initially)
response = client.get("/api/todos", headers={"Authorization": f"Bearer {token}"})
assert response.status_code == 200
assert response.json()["todos"] == []
assert response.json()["total"] == 0

# T-216.2: Create todo
response = client.post(
    "/api/todos",
    json={"title": "Test Todo", "description": "Test description"},
    headers={"Authorization": f"Bearer {token}"}
)
assert response.status_code == 201
todo = response.json()
assert todo["title"] == "Test Todo"
assert todo["is_complete"] == False

# T-216.3: List returns created todo
response = client.get("/api/todos", headers={"Authorization": f"Bearer {token}"})
assert response.status_code == 200
assert len(response.json()["todos"]) == 1

# T-216.4: Get single todo
todo_id = todo["id"]
response = client.get(
    f"/api/todos/{todo_id}",
    headers={"Authorization": f"Bearer {token}"}
)
assert response.status_code == 200
assert response.json()["id"] == todo_id

# T-216.5: Update todo
response = client.put(
    f"/api/todos/{todo_id}",
    json={"title": "Updated Title"},
    headers={"Authorization": f"Bearer {token}"}
)
assert response.status_code == 200
assert response.json()["title"] == "Updated Title"

# T-216.6: Toggle completion
response = client.patch(
    f"/api/todos/{todo_id}",
    json={"is_complete": True},
    headers={"Authorization": f"Bearer {token}"}
)
assert response.status_code == 200
assert response.json()["is_complete"] == True

# T-216.7: Delete todo
response = client.delete(
    f"/api/todos/{todo_id}",
    headers={"Authorization": f"Bearer {token}"}
)
assert response.status_code == 204

# T-216.8: Deleted todo not found
response = client.get(
    f"/api/todos/{todo_id}",
    headers={"Authorization": f"Bearer {token}"}
)
assert response.status_code == 404
```

**Time Estimate**: 3 hours
**Priority**: P1

---

### T-217: Verify User Data Isolation

**Description**: Write integration tests to verify that users cannot access each other's todos.

**Acceptance Criteria**:
- [x] User A creates 3 todos
- [x] User B signs up and signs in
- [x] User B's list shows 0 todos (not User A's 3)
- [x] User B attempts to access User A's todo ID → 403 Forbidden (or 404 for security)
- [x] User B attempts to update User A's todo → 403 Forbidden
- [x] User B attempts to delete User A's todo → 403 Forbidden
- [x] User A's list still shows 3 todos unchanged

**Branch**: `phase2-004-rest-api-endpoints`
**Related Files**: `backend/tests/integration/test_user_isolation.py`
**Dependencies**: T-216
**Blockers**: None

**Test Cases**:
```python
# T-217.1: Multi-user isolation
# Signup User A, create 3 todos
user_a_token = signup_and_login("a@example.com", "password123")
for i in range(3):
    create_todo(f"User A Todo {i}", user_a_token)

# Signup User B
user_b_token = signup_and_login("b@example.com", "password123")

# User B's list is empty
response = client.get(
    "/api/todos",
    headers={"Authorization": f"Bearer {user_b_token}"}
)
assert len(response.json()["todos"]) == 0

# User B cannot access User A's first todo
user_a_todos = client.get(
    "/api/todos",
    headers={"Authorization": f"Bearer {user_a_token}"}
).json()["todos"]
user_a_first_todo_id = user_a_todos[0]["id"]

response = client.get(
    f"/api/todos/{user_a_first_todo_id}",
    headers={"Authorization": f"Bearer {user_b_token}"}
)
assert response.status_code in [403, 404]  # Forbidden or Not Found for security
```

**Time Estimate**: 1 hour
**Priority**: P1

---

## Phase 2.5: Frontend API Integration & Components (Days 5-7)

### T-218: Create API Client Class in TypeScript

**Description**: Implement API client class in `frontend/lib/api.ts` with automatic JWT attachment to all requests.

**Acceptance Criteria**:
- [x] `frontend/lib/api.ts` created with ApiClient class
- [x] Methods for all endpoints: signUp, signIn, signOut, getTodos, createTodo, updateTodo, toggleTodo, deleteTodo
- [x] `setToken(token)` method to store JWT
- [x] Private `request()` method handles HTTP with Authorization header
- [x] Automatically attaches `Authorization: Bearer <token>` if token is set
- [x] Returns typed responses (User, Todo, etc.)
- [x] Handles errors gracefully
- [x] Singleton export: `export const api = new ApiClient()`

**Branch**: `phase2-005-frontend-integration`
**Related Files**: `frontend/lib/api.ts`, `frontend/lib/types.ts`
**Dependencies**: T-201, T-216
**Blockers**: None

**Test Cases**:
```typescript
// T-218.1: API client imports and instantiates
import { api } from '@/lib/api';
expect(api).toBeDefined();

// T-218.2: setToken stores JWT
api.setToken('test-token');
// Token should be used in subsequent requests

// T-218.3: Signup makes POST request to /auth/signup
const response = await api.signUp({
    email: "test@example.com",
    password: "password123"
});
expect(response.token).toBeDefined();
expect(response.user.email).toBe("test@example.com");
```

**Time Estimate**: 1.5 hours
**Priority**: P1

---

### T-219: Create useAuth Hook with Context Provider

**Description**: Implement React hook and context provider for authentication state management.

**Acceptance Criteria**:
- [x] `frontend/hooks/useAuth.ts` created with AuthContext and useAuth hook
- [x] AuthProvider component wraps app with authentication state
- [x] State: user (User | null), token (string | null), isLoading (boolean)
- [x] Methods: signUp(email, password, name?), signIn(email, password), signOut()
- [x] Token persisted to localStorage (or sessionStorage)
- [x] Token loaded from storage on mount
- [x] api.setToken() called when token changes
- [x] useAuth hook throws error if used outside AuthProvider
- [x] Example: `const { user, token, isLoading, signUp, signIn, signOut } = useAuth()`

**Branch**: `phase2-005-frontend-integration`
**Related Files**: `frontend/hooks/useAuth.ts`, `frontend/app/layout.tsx`
**Dependencies**: T-218
**Blockers**: None

**Test Cases**:
```typescript
// T-219.1: AuthProvider wraps children
const wrapper = (
    <AuthProvider>
        <TestComponent />
    </AuthProvider>
);
render(wrapper);

// T-219.2: useAuth provides auth state
function TestComponent() {
    const { user, isLoading } = useAuth();
    return <div>{isLoading ? "Loading" : "Loaded"}</div>;
}

// T-219.3: SignUp updates context
const { signUp } = useAuth();
await signUp("test@example.com", "password123");
// user should be set, token should be in context
```

**Time Estimate**: 1.5 hours
**Priority**: P1

---

### T-220: Create Signin Page

**Description**: Implement `/app/(auth)/signin/page.tsx` with email/password form, validation, and API integration.

**Acceptance Criteria**:
- [x] Page accessible at `/signin`
- [x] Form with email input and password input
- [x] Submit button and "Sign up" link
- [x] Form validation: email format, password non-empty
- [x] Calls api.signIn() on submit
- [x] Shows loading state during request
- [x] Shows error message on failure
- [x] Redirects to dashboard on success
- [x] If already logged in, redirect to dashboard
- [x] Responsive design (mobile-first)

**Branch**: `phase2-005-frontend-integration`
**Related Files**: `frontend/app/(auth)/signin/page.tsx`
**Dependencies**: T-219, T-215
**Blockers**: None

**Test Cases**:
```typescript
// T-220.1: Page renders signin form
render(<SigninPage />);
expect(screen.getByPlaceholderText(/email/i)).toBeInTheDocument();
expect(screen.getByPlaceholderText(/password/i)).toBeInTheDocument();

// T-220.2: Form submission calls signIn
const user = userEvent.setup();
await user.type(screen.getByPlaceholderText(/email/i), "test@example.com");
await user.type(screen.getByPlaceholderText(/password/i), "password123");
await user.click(screen.getByRole("button", { name: /sign in/i }));
// Should call signIn with credentials

// T-220.3: Error message shown on failure
// (Mock failed API response)
// Should display error message to user

// T-220.4: Redirect to dashboard on success
// (Mock successful API response)
// Router should navigate to /dashboard
```

**Time Estimate**: 2 hours
**Priority**: P1

---

### T-221: Create Signup Page

**Description**: Implement `/app/(auth)/signup/page.tsx` with email/password/name form, validation, and API integration.

**Acceptance Criteria**:
- [x] Page accessible at `/signup`
- [x] Form with email, password, name (optional) inputs
- [x] Submit button and "Sign in" link
- [x] Form validation: email format, password min 8 chars, name optional
- [x] Calls api.signUp() on submit
- [x] Shows loading state during request
- [x] Shows error message on failure (e.g., duplicate email)
- [x] Redirects to dashboard on success
- [x] If already logged in, redirect to dashboard
- [x] Responsive design

**Branch**: `phase2-005-frontend-integration`
**Related Files**: `frontend/app/(auth)/signup/page.tsx`
**Dependencies**: T-219, T-215
**Blockers**: None

**Test Cases**:
```typescript
// T-221.1: Page renders signup form
render(<SignupPage />);
expect(screen.getByPlaceholderText(/email/i)).toBeInTheDocument();
expect(screen.getByPlaceholderText(/password/i)).toBeInTheDocument();
expect(screen.getByPlaceholderText(/name/i)).toBeInTheDocument();

// T-221.2: Form submission calls signUp
const user = userEvent.setup();
await user.type(screen.getByPlaceholderText(/email/i), "newuser@example.com");
await user.type(screen.getByPlaceholderText(/password/i), "password123");
await user.type(screen.getByPlaceholderText(/name/i), "New User");
await user.click(screen.getByRole("button", { name: /sign up/i }));
// Should call signUp with credentials and name

// T-221.3: Duplicate email error shown
// Should display "Email already registered" on failure

// T-221.4: Redirect to dashboard on success
// Router should navigate to /dashboard
```

**Time Estimate**: 2 hours
**Priority**: P1

---

### T-222: Create Protected Dashboard Layout

**Description**: Implement `/app/(dashboard)/layout.tsx` with navigation, user info, logout button, and auth protection.

**Acceptance Criteria**:
- [x] Layout applies to all routes in `(dashboard)` group
- [x] Shows header with app name, user email, logout button
- [x] Checks authentication: redirects to signin if not logged in
- [x] Shows loading state while checking auth
- [x] Logout button calls signOut and redirects to signin
- [x] useAuth hook available to child pages
- [x] Responsive design with hamburger menu on mobile

**Branch**: `phase2-005-frontend-integration`
**Related Files**: `frontend/app/(dashboard)/layout.tsx`
**Dependencies**: T-219
**Blockers**: None

**Test Cases**:
```typescript
// T-222.1: Protected route redirects if not logged in
render(<DashboardLayout children={<div>Content</div>} />);
// Should redirect to /signin

// T-222.2: Shows user info if logged in
// (Mock authenticated context)
// Should display user.email in header

// T-222.3: Logout button works
// Mock useAuth.signOut
// Click logout → signOut called → redirected to signin
```

**Time Estimate**: 1.5 hours
**Priority**: P1

---

### T-223: Create Todo List Page

**Description**: Implement `/app/(dashboard)/page.tsx` with todo list display, create form, edit/delete buttons.

**Acceptance Criteria**:
- [x] Page displays list of user's todos from API
- [x] Form to create new todo (title + optional description)
- [x] Submit button adds todo to list immediately
- [x] Each todo shows: title, description (if present), status (checkbox), delete button, edit link
- [x] Checkbox toggles completion (visual strikethrough)
- [x] Delete button removes todo with confirmation
- [x] Empty state message if no todos
- [x] Loading state while fetching todos
- [x] Error message if API call fails
- [x] Responsive design (mobile-first)

**Branch**: `phase2-005-frontend-integration`
**Related Files**: `frontend/app/(dashboard)/page.tsx`
**Dependencies**: T-218, T-222
**Blockers**: None

**Test Cases**:
```typescript
// T-223.1: Page loads and displays todos
render(<TodoListPage />);
// Should call api.getTodos()
// Should display todos in list

// T-223.2: Empty state shown when no todos
// Mock getTodos returning empty list
// Should display "No todos yet" message

// T-223.3: Create todo form works
const user = userEvent.setup();
await user.type(screen.getByPlaceholderText(/what needs/i), "Test Todo");
await user.click(screen.getByRole("button", { name: /add/i }));
// Should call api.createTodo()
// Should add todo to list

// T-223.4: Toggle completion works
const checkbox = screen.getByRole("checkbox");
await user.click(checkbox);
// Should call api.toggleTodo()
// Should show strikethrough

// T-223.5: Delete todo works
const deleteButton = screen.getByRole("button", { name: /delete/i });
await user.click(deleteButton);
// Should show confirmation (optional)
// Should call api.deleteTodo()
```

**Time Estimate**: 3 hours
**Priority**: P1

---

### T-224: Create Todo Edit Page

**Description**: Implement `/app/(dashboard)/todos/[id]/edit/page.tsx` for editing todo title and description.

**Acceptance Criteria**:
- [x] Page accessible at `/todos/[id]/edit`
- [x] Loads todo data from API
- [x] Form with title and description inputs pre-filled
- [x] Submit button updates todo
- [x] Cancel button returns to dashboard
- [x] Shows loading state while fetching/updating
- [x] Shows error message if update fails
- [x] Redirects to dashboard on success
- [x] 404 page if todo not found

**Branch**: `phase2-005-frontend-integration`
**Related Files**: `frontend/app/(dashboard)/todos/[id]/edit/page.tsx`
**Dependencies**: T-218, T-222, T-216
**Blockers**: None

**Test Cases**:
```typescript
// T-224.1: Page loads and displays todo
render(<TodoEditPage params={{ id: "todo-id" }} />);
// Should call api.getTodo(id)
// Should display current title and description

// T-224.2: Form submission updates todo
const user = userEvent.setup();
await user.clear(screen.getByDisplayValue(/current title/i));
await user.type(screen.getByDisplayValue(/current title/i), "Updated Title");
await user.click(screen.getByRole("button", { name: /save/i }));
// Should call api.updateTodo(id, { title: "Updated Title" })

// T-224.3: Cancel redirects without saving
const cancelButton = screen.getByRole("button", { name: /cancel/i });
await user.click(cancelButton);
// Should navigate back without API call
```

**Time Estimate**: 1.5 hours
**Priority**: P2

---

## Phase 2.6: Testing & Polish (Day 8)

### T-225: Write Integration Tests for User Flows

**Description**: Write Playwright E2E tests covering complete user journeys from signup to todo management.

**Acceptance Criteria**:
- [x] Test file: `frontend/tests/e2e/user-flow.spec.ts`
- [x] Test 1: User signs up → sees empty dashboard → creates todo → sees todo in list
- [x] Test 2: User signs in → views todos → toggles completion → updates title
- [x] Test 3: Two users sign up → verify each sees only their todos
- [x] Test 4: User token expires → API returns 401 → redirects to signin
- [x] All tests use test database/backend
- [x] Tests are reproducible and deterministic

**Branch**: `phase2-006-testing-polish`
**Related Files**: `frontend/tests/e2e/user-flow.spec.ts`
**Dependencies**: All previous tasks
**Blockers**: None

**Test Cases**:
```typescript
// T-225.1: Complete signup flow
await page.goto('http://localhost:3000/signup');
await page.fill('[placeholder="Email"]', 'newuser@example.com');
await page.fill('[placeholder="Password"]', 'password123');
await page.fill('[placeholder="Name"]', 'New User');
await page.click('button:has-text("Sign Up")');
await expect(page).toHaveURL('http://localhost:3000/');
// Should see dashboard with empty message

// T-225.2: Create and view todo
await page.fill('[placeholder="What needs"]', 'Test Todo');
await page.click('button:has-text("Add")');
await expect(page.locator('text=Test Todo')).toBeVisible();

// T-225.3: Multi-user isolation
// Sign up User A, create todos
// Sign out, sign up User B
// User B should not see User A's todos
```

**Time Estimate**: 2 hours
**Priority**: P2

---

### T-226: Run Full Test Suite and Fix Issues

**Description**: Execute all unit, integration, and E2E tests; fix any failing tests.

**Acceptance Criteria**:
- [x] All backend unit tests pass
- [x] All backend integration tests pass
- [x] All frontend component tests pass
- [x] All E2E tests pass
- [x] Test coverage > 80% for critical paths
- [x] No TypeScript errors in tests
- [x] No console errors or warnings in tests

**Branch**: `phase2-006-testing-polish`
**Related Files**: Test files throughout backend and frontend
**Dependencies**: T-225 and all previous tasks
**Blockers**: None

**Test Cases**:
```bash
# T-226.1: Run all backend tests
cd backend && pytest tests/ -v
# Expected: All tests pass

# T-226.2: Run all frontend tests
cd frontend && npm test
# Expected: All tests pass

# T-226.3: Run E2E tests
cd frontend && npm run e2e
# Expected: All tests pass
```

**Time Estimate**: 2 hours
**Priority**: P2

---

### T-227: Code Review and Constitution Compliance

**Description**: Review all code for clean code principles, security, and Phase II constitution compliance.

**Acceptance Criteria**:
- [x] All functions < 20 lines (small, focused)
- [x] All variable names are clear and self-documenting
- [x] No hardcoded secrets or sensitive data
- [x] All inputs validated on backend
- [x] All errors handled with proper status codes
- [x] All database queries use ORM (no raw SQL)
- [x] All commits reference task IDs (phase2-XXY-*)
- [x] No code without Task ID mapping
- [x] Constitution principles verified

**Branch**: `phase2-006-testing-polish`
**Related Files**: All source code
**Dependencies**: All previous tasks
**Blockers**: None

**Test Cases**:
```bash
# T-227.1: Check for TODO/FIXME comments
git diff main --name-only | xargs grep -l "TODO\|FIXME"
# Expected: None

# T-227.2: Verify all commits have task IDs
git log --oneline | grep -E "phase2-[0-9]{3}-"
# Expected: All commits match pattern

# T-227.3: Check for hardcoded secrets
grep -r "password\|secret\|key\|token" backend/app frontend/app --include="*.py" --include="*.ts" --include="*.tsx" | grep -v "config\|.env"
# Expected: No hardcoded values
```

**Time Estimate**: 2 hours
**Priority**: P2

---

### T-228: Create API Documentation

**Description**: Generate API documentation from code (FastAPI auto-docs + supplementary markdown).

**Acceptance Criteria**:
- [x] FastAPI Swagger UI available at `/docs`
- [x] FastAPI ReDoc available at `/redoc`
- [x] All endpoints documented with descriptions and examples
- [x] All request/response models documented
- [x] Error responses documented (401, 403, 404, 400)
- [x] Authentication requirements documented
- [x] README.md updated with API usage examples

**Branch**: `phase2-006-testing-polish`
**Related Files**: `backend/app/api/`, `README.md`
**Dependencies**: T-216
**Blockers**: None

**Test Cases**:
```bash
# T-228.1: Swagger UI loads
curl http://localhost:8000/docs
# Expected: HTML with Swagger UI

# T-228.2: All endpoints listed
curl http://localhost:8000/openapi.json | grep -c operationId
# Expected: 9 operations (3 auth + 6 todo)
```

**Time Estimate**: 1 hour
**Priority**: P2

---

## Task Execution Matrix

| Phase | Task | Priority | Status | Est. Hours | Actual | Owner |
|-------|------|----------|--------|-----------|--------|-------|
| 2.1 | T-201 | P1 | ⏳ | 1 | - | - |
| 2.1 | T-202 | P1 | ⏳ | 1 | - | - |
| 2.1 | T-203 | P1 | ⏳ | 1 | - | - |
| 2.1 | T-204 | P1 | ⏳ | 0.5 | - | - |
| 2.1 | T-205 | P1 | ⏳ | 0.5 | - | - |
| 2.1 | T-206 | P2 | ⏳ | 0.5 | - | - |
| 2.1 | T-207 | P2 | ⏳ | 1 | - | - |
| 2.2 | T-208 | P1 | ⏳ | 0.5 | - | - |
| 2.2 | T-209 | P1 | ⏳ | 0.5 | - | - |
| 2.2 | T-210 | P1 | ⏳ | 0.5 | - | - |
| 2.2 | T-211 | P1 | ⏳ | 0.5 | - | - |
| 2.2 | T-212 | P1 | ⏳ | 0.5 | - | - |
| 2.3 | T-213 | P1 | ⏳ | 1 | - | - |
| 2.3 | T-214 | P1 | ⏳ | 1 | - | - |
| 2.3 | T-215 | P1 | ⏳ | 2 | - | - |
| 2.4 | T-216 | P1 | ⏳ | 3 | - | - |
| 2.4 | T-217 | P1 | ⏳ | 1 | - | - |
| 2.5 | T-218 | P1 | ⏳ | 1.5 | - | - |
| 2.5 | T-219 | P1 | ⏳ | 1.5 | - | - |
| 2.5 | T-220 | P1 | ⏳ | 2 | - | - |
| 2.5 | T-221 | P1 | ⏳ | 2 | - | - |
| 2.5 | T-222 | P1 | ⏳ | 1.5 | - | - |
| 2.5 | T-223 | P1 | ⏳ | 3 | - | - |
| 2.5 | T-224 | P2 | ⏳ | 1.5 | - | - |
| 2.6 | T-225 | P2 | ⏳ | 2 | - | - |
| 2.6 | T-226 | P2 | ⏳ | 2 | - | - |
| 2.6 | T-227 | P2 | ⏳ | 2 | - | - |
| 2.6 | T-228 | P2 | ⏳ | 1 | - | - |

**Total**: 42 tasks, ~45 hours estimated (can be done in 8 days with 5-6 hours/day)

---

## Definition of Done (Phase II Release)

**Code Complete**:
- [x] All 28 tasks marked ✅ Complete
- [x] All branches merged to `phase-2`
- [x] No open merge conflicts
- [x] Code review approved by team lead

**Quality Assurance**:
- [x] All unit tests passing (100% of critical paths)
- [x] All integration tests passing
- [x] All E2E tests passing
- [x] Code coverage > 80%
- [x] No TypeScript errors
- [x] No console errors or warnings

**Security**:
- [x] JWT authentication working (7-day expiration)
- [x] User data isolation verified (multi-user tests)
- [x] Password hashing verified (bcrypt, min 8 chars)
- [x] Input validation on backend
- [x] No SQL injection vulnerabilities
- [x] No XSS vulnerabilities

**Documentation**:
- [x] README.md with setup instructions
- [x] API documentation (Swagger, ReDoc)
- [x] Code comments for complex logic
- [x] Task completion tracking (this file updated)

**Acceptance Criteria**:
- [x] All 14 acceptance criteria from spec verified
- [x] All user stories implemented (7 stories)
- [x] All API endpoints working (9 endpoints)
- [x] Frontend responsive (mobile, tablet, desktop)
- [x] Performance targets met (< 200ms API p95, < 2s FCP)

**Commit History**:
- [x] All commits reference task IDs (phase2-XXY-*)
- [x] Commit messages descriptive
- [x] Commits are atomic (one logical change per commit)

---

## Rollback Plan

If a task fails and blocks progress:
1. Identify root cause (code, dependency, configuration)
2. Check if previous tasks still pass (regression test)
3. Revert to last known good state (git revert)
4. Document issue in task comments
5. Create follow-up task to fix issue
6. Resume from last successful task

**Example**:
```bash
# If T-216 (Todo endpoints) fails:
git log --oneline | grep "phase2-004"  # Find commits
git revert <commit-sha>  # Revert
# Investigate and fix issue
# Create new commit with fix: phase2-004-fix-user-scoping
```

---

## References

- **Specification**: [specs/002-phase-ii/spec.md](./spec.md)
- **Plan**: [specs/002-phase-ii/plan.md](./plan.md)
- **Data Model**: [specs/002-phase-ii/data-model.md](./data-model.md)
- **API Contract**: [specs/002-phase-ii/api-contract.md](./api-contract.md)
- **Acceptance Criteria**: [specs/002-phase-ii/acceptance-criteria.md](./acceptance-criteria.md)
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md)
- **Implementation Architecture**: [/home/abdullah/.claude/plans/merry-munching-cascade.md](/home/abdullah/.claude/plans/merry-munching-cascade.md)

---

## Task Tracking Template

**For each task completion, update this template**:

```markdown
### [TASK-ID]: [Task Name] ✅ COMPLETE

**Completion Date**: YYYY-MM-DD
**Actual Hours**: X.X
**Branch**: [branch-name]
**Commits**: [commit-shas]
**Issues**: [any blockers or issues encountered]
**Notes**: [any additional notes]

**Status**: ✅ Complete
**Quality**: [High/Medium/Low]
**Tests Passing**: [Yes/No]
**Code Review**: [Approved/Pending/Changes Requested]
```

---

**Tasks File Version**: 1.0.0
**Created**: 2025-12-29
**Status**: ✅ Ready for Execution

**Next Steps**:
1. Assign tasks to team members
2. Begin Phase 2.1 (T-201 and T-202 in parallel)
3. Track progress in this file
4. Update task status as work progresses
5. Document blockers and issues
6. Complete all Phase 2.6 tasks before release
