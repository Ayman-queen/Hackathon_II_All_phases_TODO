# JWT Attachment Pattern: API Client

**Task**: T-232 - Confirm API client bearer token injection
**Date**: 2025-12-31
**Status**: ✅ Verified

## Pattern: Automatic JWT Attachment

### Overview
All API requests from the frontend must include the JWT token in the `Authorization` header with "Bearer" scheme. This is handled by a centralized API client wrapper that:

1. Retrieves the JWT from Better Auth's `jwtClient()` plugin
2. Injects it into all outgoing requests automatically
3. Handles 401 responses by clearing the token and redirecting to /login

### Implementation Pattern

```typescript
// lib/api-client.ts
export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  // 1. Get fresh JWT token (with automatic refresh if needed)
  const token = await authClient.token();
  
  // 2. Build request with JWT in Authorization header
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token?.data?.token && { 
        Authorization: `Bearer ${token.data.token}` 
      }),
      ...options.headers,
    },
  });

  // 3. Handle 401 (token expired)
  if (response.status === 401) {
    // Clear token and redirect to login
    tokenManager.clearToken();
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }

  // 4. Handle other errors
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "API request failed");
  }

  // 5. Return response data
  return response.json();
}
```

### Request Flow

```
Component calls API
  ↓
apiRequest() retrieves JWT from Better Auth
  ↓
Fetch request includes Authorization: Bearer <JWT>
  ↓
Backend receives request with JWT header
  ↓
Backend validates JWT using JWKS endpoint
  ↓
Backend extracts user_id from JWT claims
  ↓
Backend enforces user-scoped data access (data isolation)
  ↓
Response returned to component
```

### Header Format

**Request Header**:
```
Authorization: Bearer eyJhbGciOiJFZERTQSIsImtpZCI6ImtleS0xIn0.eyJzdWIiOiI1NTBlODQwMC1lMjliLTQxZDQtYTcxNi00NDY2NTU0NDAwMDAiLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjMwMDAiLCJhdWQiOiJodHRwOi8vbG9jYWxob3N0OjMwMDAiLCJleHAiOjE3MzU3NTU2MDB9.signature
```

### Validation by Backend

The backend (app/api/deps.py) validates the token:
```python
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # 1. Extract token from "Bearer <token>" header
    # 2. Call verify_better_auth_token(token)
    # 3. Extract user_id from token.sub claim
    # 4. Query database for user
    # 5. Return User object to route handler
```

### Error Handling

| Status | Cause | Frontend Action |
|--------|-------|-----------------|
| 200 | Success | Return response data |
| 201 | Created | Return created resource |
| 204 | No Content | Return empty |
| 400 | Validation failed | Show error message |
| 401 | Token expired/invalid | Clear token, redirect to /login |
| 403 | Not owner of resource | Show "Access denied" error |
| 404 | Resource not found | Show "Not found" error |
| 500 | Server error | Show "Server error" and retry option |

### Data Flow Example: Creating a Todo

```
1. User clicks "Create Todo" button
   ↓
2. TodoForm calls useTodos().createTodo({ title, description })
   ↓
3. useTodos calls api.createTodo() from api-client.ts
   ↓
4. api-client.ts:
   - Retrieves JWT from authClient.token()
   - Calls fetch("/api/todos", {
       method: "POST",
       headers: { Authorization: "Bearer <JWT>", ... },
       body: JSON.stringify({ title, description })
     })
   ↓
5. Backend receives request:
   - Extracts JWT from Authorization header
   - Validates JWT using JWKS endpoint
   - Extracts user_id from JWT.sub claim
   - Creates todo with user_id = current_user.id
   ↓
6. Backend returns 201 with created todo
   ↓
7. api-client.ts returns todo object to useTodos
   ↓
8. useTodos updates component state
   ↓
9. Component displays new todo in list
```

### Environment Configuration

```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_AUTH_URL=http://localhost:3000
```

### Summary

- **Pattern**: Centralized `api-client.ts` wrapper handles JWT attachment
- **Retrieval**: Better Auth's `jwtClient()` plugin manages tokens automatically
- **Attachment**: All requests include `Authorization: Bearer <JWT>` header
- **Backend**: FastAPI dependency validates JWT using JWKS
- **Data Isolation**: user_id extracted from JWT claims ensures user-scoped access
- **Error Handling**: 401 responses trigger logout and redirect to /login
