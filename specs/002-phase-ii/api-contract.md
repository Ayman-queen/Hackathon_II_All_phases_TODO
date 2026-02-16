# API Contract - Phase II Full-Stack Todo Application

**Version**: 1.0.0
**Base URL**: `https://api.example.com` (or `http://localhost:8000` for development)
**Authentication**: JWT Bearer Token in Authorization header

---

## Authentication Endpoints

### POST /auth/signup

**Description**: Register a new user account.

**Request**:
```http
POST /auth/signup HTTP/1.1
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string | Yes | Email address (must be valid format and unique) |
| password | string | Yes | Password (minimum 8 characters) |
| name | string | No | Display name (optional) |

**Response (201 Created)**:
```json
{
  "user": {
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2025-12-29T10:00:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Account created successfully"
}
```

**Response (400 Bad Request)**:
```json
{
  "error": "Email already registered" | "Invalid email format" | "Password must be at least 8 characters"
}
```

**Response (500 Internal Server Error)**:
```json
{
  "error": "Failed to create account"
}
```

---

### POST /auth/signin

**Description**: Authenticate user and receive JWT token.

**Request**:
```http
POST /auth/signin HTTP/1.1
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string | Yes | Registered email address |
| password | string | Yes | User's password |

**Response (200 OK)**:
```json
{
  "user": {
    "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
    "email": "user@example.com",
    "name": "John Doe",
    "created_at": "2025-12-29T10:00:00Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 604800
}
```

**Response (401 Unauthorized)**:
```json
{
  "error": "Invalid credentials"
}
```

**Response (404 Not Found)**:
```json
{
  "error": "User not found"
}
```

---

### POST /auth/logout

**Description**: Invalidate user's session and token.

**Request**:
```http
POST /auth/logout HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200 OK)**:
```json
{
  "message": "Logout successful"
}
```

**Response (401 Unauthorized)**:
```json
{
  "error": "Unauthorized - token missing or invalid"
}
```

---

## Todo CRUD Endpoints

### GET /api/todos

**Description**: Retrieve all todos for the authenticated user.

**Request**:
```http
GET /api/todos HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Query Parameters**:
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| skip | integer | No | Number of todos to skip (default: 0) |
| limit | integer | No | Max number of todos to return (default: 50, max: 100) |
| is_complete | boolean | No | Filter by completion status (true/false) |
| sort | string | No | Sort field (created_at, updated_at, default: created_at) |
| order | string | No | Sort order (asc, desc, default: desc) |

**Response (200 OK)**:
```json
{
  "todos": [
    {
      "id": "e6f3a8b2-d1c4-4e7a-9f2c-1a8b3e5d6c7f",
      "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "title": "Complete project spec",
      "description": "Finish Phase II specification document",
      "is_complete": false,
      "created_at": "2025-12-29T10:00:00Z",
      "updated_at": "2025-12-29T10:00:00Z"
    },
    {
      "id": "a1b2c3d4-e5f6-4g7h-8i9j-k0l1m2n3o4p5",
      "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "title": "Design database schema",
      "description": null,
      "is_complete": true,
      "created_at": "2025-12-28T14:30:00Z",
      "updated_at": "2025-12-28T16:45:00Z"
    }
  ],
  "total": 2,
  "skip": 0,
  "limit": 50
}
```

**Response (401 Unauthorized)**:
```json
{
  "error": "Unauthorized - token missing or invalid"
}
```

---

### POST /api/todos

**Description**: Create a new todo for the authenticated user.

**Request**:
```http
POST /api/todos HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "New todo item",
  "description": "Optional description of the task"
}
```

**Request Body**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Todo title (1-500 characters) |
| description | string | No | Optional description (max 2000 characters) |

**Response (201 Created)**:
```json
{
  "id": "b5c6d7e8-f9g0-4h1i-2j3k-l4m5n6o7p8q9",
  "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "title": "New todo item",
  "description": "Optional description of the task",
  "is_complete": false,
  "created_at": "2025-12-29T10:15:00Z",
  "updated_at": "2025-12-29T10:15:00Z"
}
```

**Response (400 Bad Request)**:
```json
{
  "error": "Title is required" | "Title exceeds 500 characters" | "Description exceeds 2000 characters"
}
```

**Response (401 Unauthorized)**:
```json
{
  "error": "Unauthorized - token missing or invalid"
}
```

---

### GET /api/todos/{id}

**Description**: Retrieve a specific todo by ID (with ownership validation).

**Request**:
```http
GET /api/todos/e6f3a8b2-d1c4-4e7a-9f2c-1a8b3e5d6c7f HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| id | UUID | The todo's unique identifier |

**Response (200 OK)**:
```json
{
  "id": "e6f3a8b2-d1c4-4e7a-9f2c-1a8b3e5d6c7f",
  "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "title": "Complete project spec",
  "description": "Finish Phase II specification document",
  "is_complete": false,
  "created_at": "2025-12-29T10:00:00Z",
  "updated_at": "2025-12-29T10:00:00Z"
}
```

**Response (404 Not Found)**:
```json
{
  "error": "Todo not found"
}
```

**Response (403 Forbidden)**:
```json
{
  "error": "You do not have permission to access this todo"
}
```

**Response (401 Unauthorized)**:
```json
{
  "error": "Unauthorized - token missing or invalid"
}
```

---

### PUT /api/todos/{id}

**Description**: Update a todo's title and/or description (with ownership validation).

**Request**:
```http
PUT /api/todos/e6f3a8b2-d1c4-4e7a-9f2c-1a8b3e5d6c7f HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "Updated todo title",
  "description": "Updated description"
}
```

**Request Body**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | No | New title (1-500 characters) |
| description | string | No | New description (max 2000 characters) |

**Response (200 OK)**:
```json
{
  "id": "e6f3a8b2-d1c4-4e7a-9f2c-1a8b3e5d6c7f",
  "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "title": "Updated todo title",
  "description": "Updated description",
  "is_complete": false,
  "created_at": "2025-12-29T10:00:00Z",
  "updated_at": "2025-12-29T10:20:00Z"
}
```

**Response (400 Bad Request)**:
```json
{
  "error": "Title cannot be empty" | "Title exceeds 500 characters" | "Description exceeds 2000 characters"
}
```

**Response (403 Forbidden)**:
```json
{
  "error": "You do not have permission to access this todo"
}
```

**Response (404 Not Found)**:
```json
{
  "error": "Todo not found"
}
```

**Response (401 Unauthorized)**:
```json
{
  "error": "Unauthorized - token missing or invalid"
}
```

---

### PATCH /api/todos/{id}

**Description**: Toggle a todo's completion status (with ownership validation).

**Request**:
```http
PATCH /api/todos/e6f3a8b2-d1c4-4e7a-9f2c-1a8b3e5d6c7f HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "is_complete": true
}
```

**Request Body**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| is_complete | boolean | Yes | New completion status |

**Response (200 OK)**:
```json
{
  "id": "e6f3a8b2-d1c4-4e7a-9f2c-1a8b3e5d6c7f",
  "user_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "title": "Complete project spec",
  "description": "Finish Phase II specification document",
  "is_complete": true,
  "created_at": "2025-12-29T10:00:00Z",
  "updated_at": "2025-12-29T10:25:00Z"
}
```

**Response (403 Forbidden)**:
```json
{
  "error": "You do not have permission to access this todo"
}
```

**Response (404 Not Found)**:
```json
{
  "error": "Todo not found"
}
```

**Response (401 Unauthorized)**:
```json
{
  "error": "Unauthorized - token missing or invalid"
}
```

---

### DELETE /api/todos/{id}

**Description**: Permanently delete a todo (with ownership validation).

**Request**:
```http
DELETE /api/todos/e6f3a8b2-d1c4-4e7a-9f2c-1a8b3e5d6c7f HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Path Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| id | UUID | The todo's unique identifier |

**Response (204 No Content)**: [No response body]

**Response (403 Forbidden)**:
```json
{
  "error": "You do not have permission to access this todo"
}
```

**Response (404 Not Found)**:
```json
{
  "error": "Todo not found"
}
```

**Response (401 Unauthorized)**:
```json
{
  "error": "Unauthorized - token missing or invalid"
}
```

---

## Error Handling & Status Codes

| Code | Description | Use Case |
|------|-------------|----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST (resource created) |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input, validation failure |
| 401 | Unauthorized | Missing/invalid JWT token |
| 403 | Forbidden | Valid token but insufficient permissions (wrong owner) |
| 404 | Not Found | Resource does not exist |
| 500 | Internal Server Error | Unexpected server error |

**Standard Error Response Format**:
```json
{
  "error": "Error message describing what went wrong",
  "code": "ERROR_CODE",
  "timestamp": "2025-12-29T10:30:00Z"
}
```

---

## Authentication

### JWT Token Format

All protected endpoints require a JWT token in the `Authorization` header:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

**Token Claims**:
```json
{
  "sub": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "email": "user@example.com",
  "iat": 1703001600,
  "exp": 1703608000,
  "iss": "evo-todo-app",
  "aud": "evo-todo-client"
}
```

### Token Expiration

- Tokens expire after **7 days** (604800 seconds)
- Expired tokens return **401 Unauthorized**
- Frontend must redirect to signin on 401

---

## Rate Limiting (Recommended for Production)

**Per-User Limits**:
- Create todo: 100 requests per minute
- Update/Delete todo: 100 requests per minute
- Get todos: 200 requests per minute

**Rate Limit Headers**:
```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1703001660
```

**Rate Limit Exceeded Response (429)**:
```json
{
  "error": "Too many requests. Please try again later.",
  "retry_after": 60
}
```

---

## CORS Configuration

**Allowed Origins** (configure per environment):
- Development: `http://localhost:3000`
- Production: `https://app.example.com`

**Allowed Headers**:
- `Content-Type`
- `Authorization`

**Allowed Methods**:
- `GET`, `POST`, `PUT`, `PATCH`, `DELETE`, `OPTIONS`

**Credentials**: `include` (for cookie-based auth if applicable)

