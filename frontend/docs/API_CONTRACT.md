# API Contract: Todo Backend

**Task**: T-230 - Verify backend todo API contract
**Date**: 2025-12-31
**Status**: ✅ Verified

## Backend API Endpoints

### Base URL
```
http://localhost:8000/api
```

### Authentication
All endpoints require `Authorization: Bearer <JWT>` header where JWT is issued by Better Auth.

---

## Todo Endpoints

### 1. List Todos
**Endpoint**: `GET /todos`
**Response**: 200 OK

**Query Parameters**:
- `skip` (optional, default=0): Offset for pagination
- `limit` (optional, default=100, max=1000): Number of items to return
- `is_complete` (optional): Filter by status (true/false/null for all)

**Response Body**:
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

**Data Isolation**: Only returns todos where `user_id == current_user.id` (enforced by backend)

---

### 2. Create Todo
**Endpoint**: `POST /todos`
**Status**: 201 Created

**Request Body**:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread from Whole Foods"
}
```

**Validation**:
- `title`: Required, 1-500 characters, non-empty/non-whitespace
- `description`: Optional, 0-2000 characters
- `user_id`: Auto-assigned from JWT (not from request body)

**Response Body**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "660e8400-e29b-41d4-a716-446655440001",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread from Whole Foods",
  "is_complete": false,
  "created_at": "2025-12-29T10:30:00Z",
  "updated_at": "2025-12-29T10:30:00Z"
}
```

**Error Responses**:
- 400: Title is empty or too long
- 401: Missing or invalid token
- 422: Validation error

---

## Data Isolation & Security

### User-Scoped Operations
- **Backend enforces**: All queries filter by `current_user.id` extracted from JWT
- **GET /todos**: Only returns todos belonging to the authenticated user
- **POST /todos**: Automatically assigns `user_id` from JWT (not from request body)

### Authorization
- Every endpoint requires valid Better Auth JWT token in `Authorization: Bearer <token>` header
- Invalid/expired tokens return 401 Unauthorized

---

## Notes for Frontend

1. **JWT Token Retrieval**: Use Better Auth client's `jwtClient()` plugin to get JWT tokens automatically
2. **Token Attachment**: All requests must include `Authorization: Bearer <token>` header
3. **Token Expiration**: Handle 401 responses by redirecting to /login and clearing stored token
4. **User Isolation**: Frontend should filter todos by current user's JWT claims (backend provides additional security)
5. **API Base URL**: `process.env.NEXT_PUBLIC_API_URL` should point to backend (default: `http://localhost:8000`)
