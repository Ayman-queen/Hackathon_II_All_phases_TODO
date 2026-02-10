# Backend Architecture Documentation



## Overview



The Evo-TODO backend is a FastAPI application that provides RESTful API endpoints for todo management and a real-time chat feature with an AI agent. It uses Better Auth for JWT authentication.



**Tech Stack:**

- **Framework**: FastAPI 0.104+

- **ORM**: SQLModel (Pydantic + SQLAlchemy)

- **Database**: PostgreSQL (Neon Serverless supported)

- **Authentication**: Better Auth (EdDSA/JWKS) and JWT

- **Language**: Python 3.11+



## New Features in Phase 3



- **Chatbot API**: A new real-time chat feature allowing users to interact with an AI agent.

- **JWT Authentication**: Enhanced security with JWT-based authentication for all major endpoints.

- **MCP Server Integration**: The chat functionality is integrated with the MCP server.

- **Expanded Test Coverage**: New end-to-end and other tests for the MCP server.



## Project Structure



```

backend/

├── app/

│   ├── agents/

│   │   └── chat_agent.py      # Logic for the AI chat agent

│   ├── api/

│   │   ├── auth.py          # DEPRECATED - Better Auth handles auth

│   │   ├── deps.py          # FastAPI dependencies (JWT validation)

│   │   ├── todos.py         # Todo CRUD endpoints

│   │   └── chat.py          # Chat API endpoints

│   ├── core/

│   │   ├── auth.py          # JWT verification logic

│   │   ├── config.py        # Configuration settings

│   │   ├── jwks_client.py   # JWKS client for JWT verification

│   │   └── security.py      # Security utilities, including JWT creation

│   ├── models/

│   │   ├── database.py      # Database connection & session

│   │   ├── todo.py          # Todo SQLModel

│   │   ├── user.py          # User SQLModel (maps to Better Auth)

│   │   └── chat.py          # Chat message SQLModel

│   ├── schemas/

│   │   ├── todo.py          # Todo Pydantic schemas

│   │   ├── user.py          # User Pydantic schemas

│   │   └── chat.py          # Chat Pydantic schemas

│   ├── main.py              # FastAPI app entry point

│   └── __init__.py

├── mcp_server/

│   └── server.py            # MCP server implementation

├── tests/

│   ├── test_mcp_server.py

│   ├── test_mcp_server_e2e.py

│   └── test_mcp_server_extra.py

├── .env                     # Environment variables (create from .env.example)

├── .env.example             # Example environment configuration

├── Dockerfile               # Docker configuration

├── pyproject.toml           # Python dependencies

├── migrate_db.py            # Database migration script

└── uv.lock                  # Dependency lock file

```



## Configuration



### Environment Variables (.env)



```bash

# Database Configuration

DATABASE_URL=postgresql://user:password@localhost:5432/evo_todo



# Better Auth Configuration

BETTER_AUTH_URL=http://localhost:3000

# (JWKS_URL, ISSUER, AUDIENCE are auto-derived)



# JWKS Cache Configuration

JWKS_CACHE_LIFESPAN=300        # 5 minutes

JWKS_CACHE_MAX_KEYS=16



# CORS Configuration

CORS_ORIGINS=http://localhost:3000



# Environment

ENVIRONMENT=development

DEBUG=True

```



### Core Settings (backend/app/core/config.py)



- **BETTER_AUTH_URL**: Frontend URL where Better Auth service runs

- **BETTER_AUTH_JWKS_URL**: Derived as `{BETTER_AUTH_URL}/api/auth/jwks`

- **BETTER_AUTH_ISSUER**: Derived as `{BETTER_AUTH_URL}`

- **BETTER_AUTH_AUDIENCE**: Derived as `{BETTER_AUTH_URL}`

- **DATABASE_URL**: PostgreSQL connection string

- **CORS_ORIGINS**: Comma-separated list of allowed origins



## Authentication Flow



### Better Auth Integration



1. **Frontend**: User signs up/signs in using Better Auth client

2. **Token Generation**: Better Auth generates JWT token (EdDSA/Ed25519)

3. **Token Storage**: Frontend stores token (localStorage or cookie)

4. **API Requests**: Frontend sends token in `Authorization: Bearer <token>` header

5. **Backend Validation**:

   - JWT signature verified via JWKS endpoint

   - Claims validated (issuer, audience, expiration)

   - User extracted from 'sub' claim

   - User existence verified in database



### JWT Verification (backend/app/core/auth.py)



**Function**: `verify_better_auth_token(token: str) -> Dict`



**Verification Steps**:

1. Fetch JWKS from Better Auth endpoint

2. Extract signing key based on JWT `kid` (key ID)

3. Verify EdDSA signature using Ed25519 public key

4. Validate `iss` (issuer) claim

5. Validate `aud` (audience) claim

6. Validate `exp` (expiration) claim

7. Extract and verify `sub` (user_id) claim



**Error Handling**:

- `ValueError("Token has expired")` - 401 Unauthorized

- `ValueError("Invalid token audience")` - 401 Unauthorized

- `ValueError("Invalid token issuer")` - 401 Unauthorized

- `ValueError("Token signing key not found in JWKS")` - 401 Unauthorized

- `JWKSFetchError` - 503 Service Unavailable



### Dependency Injection (backend/app/api/deps.py)



**Primary Dependency**: `get_current_user()`

- Extracts Bearer token from `Authorization` header

- Verifies JWT via `verify_better_auth_token()`

- Fetches user from database by `user_id`

- Returns `User` object or raises 401/503



**Optional Dependency**: `get_current_user_optional()`

- Same validation, but returns `None` instead of raising

- Use for public endpoints with optional personalization



## Database Models



### User Model (backend/app/models/user.py)



**Table**: `user` (managed by Better Auth)



```python

class User(SQLModel, table=True):

    id: str                    # UUID string (primary key)

    email: str                 # Unique email

    name: str                  # Display name

    emailVerified: bool        # Email verification status

    image: Optional[str]       # Profile image URL

    createdAt: datetime

    updatedAt: datetime

```



**Important Notes**:

- Table name is singular `user`, not `users`

- User ID is a **string UUID**, not UUID object

- All fields are managed by Better Auth (read-only from backend)



### Todo Model (backend/app/models/todo.py)



**Table**: `todos`



```python

class Todo(SQLModel, table=True):

    id: UUID                   # UUID v4 primary key

    user_id: str               # Foreign key to user.id (string)

    title: str                 # Required (1-500 chars)

    description: Optional[str] # Optional (0-2000 chars)

    is_complete: bool          # Completion status

    created_at: datetime

    updated_at: datetime

```



**Indexes**:

- Composite index on `(user_id, created_at)` for efficient queries

- Index on `user_id` for foreign key lookups



**Data Isolation**:

- All queries MUST filter by `user_id`

- Frontend can only access user's own todos

- 404 returned for non-existent OR non-owned todos (prevents info leakage)



### Chat Model (backend/app/models/chat.py)



**Table**: `chat_messages`



```python

class ChatMessage(SQLModel, table=True):

    id: UUID

    user_id: str

    message: str

    response: str

    created_at: datetime

    updated_at: datetime

```



## API Routes



### Health Check



**GET** `/health`

- Returns: `{"status": "healthy"}`

- Use for Docker healthchecks



### Todo CRUD Endpoints



**Base Path**: `/api/todos`



| Method | Endpoint | Description | Auth Required |

|--------|----------|-------------|---------------|

| GET | `/api/todos` | List all user todos | Yes |

| GET | `/api/todos/{id}` | Get specific todo | Yes |

| POST | `/api/todos` | Create new todo | Yes |

| PUT | `/api/todos/{id}` | Update todo | Yes |

| PATCH | `/api/todos/{id}` | Toggle completion | Yes |

| DELETE | `/api/todos/{id}` | Delete todo | Yes |



#### List Todos (GET `/api/todos`)



**Query Parameters**:

- `skip`: Number of items to skip (default: 0)

- `limit`: Number of items to return (default: 100, max: 1000)

- `is_complete`: Filter by status (optional: true/false)



**Response**:

```json

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

```



#### Create Todo (POST `/api/todos`)



**Request Body**:

```json

{

  "title": "Buy groceries",

  "description": "Milk, eggs, bread"

}

```



**Validation**:

- `title`: Required, 1-500 characters, non-whitespace

- `description`: Optional, 0-2000 characters



**Response**: `TodoResponse` (201 Created)



#### Get Todo (GET `/api/todos/{id}`)



**Path Parameters**:

- `id`: UUID of todo



**Response**: `TodoResponse` (200 OK)

**Errors**:

- 403: User doesn't own this todo

- 404: Todo not found



#### Update Todo (PUT `/api/todos/{id}`)



**Request Body**:

```json

{

  "title": "Updated title",

  "description": "Updated description"

}

```



**Partial Updates**:

- Set fields to `null` to keep current value

- At least one field must be provided



**Response**: `TodoResponse` (200 OK)



#### Toggle Todo (PATCH `/api/todos/{id}`)



**Request Body**:

```json

{

  "is_complete": true

}

```



**Response**: `TodoResponse` (200 OK)



#### Delete Todo (DELETE `/api/todos/{id}`)



**Response**: 204 No Content (empty body)

**Errors**:

- 403: User doesn't own this todo

- 404: Todo not found



### Chat Endpoints



**Base Path**: `/api/chat`



| Method | Endpoint | Description | Auth Required |

|--------|----------|-------------|---------------|

| POST | `/` | Send a message to the chat agent | Yes |

| GET | `/{user_id}` | Get chat history for a user | Yes |



## API Schemas



### Todo Schemas (backend/app/schemas/todo.py)



- **TodoCreate**: Input for creating todos

- **TodoUpdate**: Input for updating todos (partial)

- **TodoToggle**: Input for toggling completion

- **TodoResponse**: Output for single todo

- **TodoListResponse**: Output for paginated list

- **TodoBulkDelete**: Input for bulk delete (future use)



### User Schemas (backend/app/schemas/user.py)



- **UserCreate**: Input for user signup (deprecated)

- **UserLogin**: Input for user login (deprecated)

- **UserResponse**: Output for user data

- **TokenResponse**: Token + user data (deprecated)

- **UserUpdate**: Input for user profile update (future use)



### Chat Schemas (backend/app/schemas/chat.py)



- **ChatMessageCreate**: Input for creating a new chat message.

- **ChatMessageResponse**: Output for a single chat message.



## Database Connection



### Connection Pooling (backend/app/models/database.py)



**Configuration for Neon Serverless**:

- Pool size: 2 (reduced for serverless)

- Max overflow: 3 (small overflow for spikes)

- Pre-ping: Enabled (detect stale connections)

- Recycle: 300 seconds (connection timeout)



**Driver**: `postgresql+psycopg://` (psycopg3)



### Session Management



**Dependency**: `get_db()`

- Creates SQLAlchemy session

- Yields to request handler

- Auto-closes after request



## Database Initialization



### Auto-Initialization (backend/app/main.py)



```python

@asynccontextmanager

async def lifespan(app: FastAPI):

    init_db()  # Create tables on startup

    yield

```



### Migration Script



**File**: `migrate_db.py`



Features:

- Checks for schema migrations

- Migrates `todos.user_id` from UUID to VARCHAR

- Recreates tables with correct schema



**Usage**:

```bash

python migrate_db.py

```



## JWKS Client (backend/app/core/jwks_client.py)



### Features



- **Thread-safe singleton**: Global client instance

- **Automatic caching**: Configurable TTL (default 5 min)

- **Key rotation**: Handles `kid` changes

- **Error handling**: `JWKSFetchError`, `JWKSKeyNotFoundError`



### Configuration



- `cache_keys`: Enabled

- `max_cached_keys`: 16

- `cache_jwk_set`: Enabled

- `lifespan`: 300 seconds

- `timeout`: 10 seconds



### Refresh Mechanism



```python

refresh_jwks_cache()  # Force cache refresh

```



Auto-refresh on key not found in cache.



## CORS Configuration



**Origins**: Configured via `CORS_ORIGINS` env var



**Settings**:

- `allow_credentials`: True

- `allow_methods`: ["*"]

- `allow_headers`: ["*"]



## Error Responses



| Status Code | Description |

|-------------|-------------|

| 200 | Success |

| 201 | Created |

| 204 | No Content (delete success) |

| 400 | Bad Request (validation error) |

| 401 | Unauthorized (invalid/expired token) |

| 403 | Forbidden (insufficient permissions) |

| 404 | Not Found |

| 422 | Unprocessable Entity (validation error) |

| 503 | Service Unavailable (JWKS endpoint down) |



## Security Features



1. **JWT Authentication**: EdDSA/Ed25519 asymmetric verification

2. **User Isolation**: All queries filtered by `user_id`

3. **Claim Validation**: Issuer, audience, expiration

4. **Ownership Verification**: 403 for non-owned resources

5. **Input Validation**: Pydantic schemas with limits

6. **SQL Injection Protection**: SQLAlchemy ORM parameterized queries



## Deployment



### Docker



**Build**:

```bash

docker build -t evo-todo-backend .

```



**Run**:

```bash

docker run -p 8000:8000 --env-file .env evo-todo-backend

```



### Manual



```bash

# Install dependencies

uv sync



# Run development server

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

```



### API Documentation



- **Swagger UI**: http://localhost:8000/docs

- **ReDoc**: http://localhost:8000/redoc

- **OpenAPI Schema**: http://localhost:8000/openapi.json



## Dependencies (pyproject.toml)



- `fastapi>=0.104.0` - Web framework

- `uvicorn>=0.24.0` - ASGI server

- `sqlmodel>=0.0.14` - ORM

- `pydantic-settings>=2.1.0` - Settings management

- `pydantic[email]>=2.0.0` - Data validation

- `psycopg[binary]>=3.1.0` - PostgreSQL driver

- `httpx>=0.25.0` - HTTP client

- `PyJWT[crypto]>=2.8.0` - JWT handling

