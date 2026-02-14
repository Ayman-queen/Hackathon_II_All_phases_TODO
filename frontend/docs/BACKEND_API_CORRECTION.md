# Backend API Endpoint Correction

**Date**: 2025-12-30
**Task**: Align frontend tasks with actual backend API implementation
**Status**: ✅ CORRECTED

---

## Issue Summary

Initial frontend specification referenced `/api/{user_id}/tasks` endpoint pattern as per Context 7 specification. Upon Phase 0 validation (T-230), the actual backend implementation uses `/api/todos/{todo_id}` pattern instead.

---

## What Changed

### ❌ PREVIOUS (Incorrect Assumption)

```
GET    /api/{user_id}/tasks           - List user's todos
POST   /api/{user_id}/tasks           - Create new todo
GET    /api/{user_id}/tasks/{id}      - Get specific todo
PUT    /api/{user_id}/tasks/{id}      - Update todo
DELETE /api/{user_id}/tasks/{id}      - Delete todo
```

### ✅ CORRECTED (Actual Implementation)

```
GET    /api/todos                     - List current user's todos (filtered by JWT)
POST   /api/todos                     - Create new todo (user_id set from JWT)
GET    /api/todos/{todo_id}           - Get specific todo (if owner)
PUT    /api/todos/{todo_id}           - Update todo (if owner)
DELETE /api/todos/{todo_id}           - Delete todo (if owner)
```

---

## Why This Is Better

### 1. **No User ID in URL**
- **Old approach**: Frontend had to decode JWT, extract user_id, and construct URLs
- **New approach**: Backend filters by JWT claims automatically
- **Benefit**: Cleaner API, less client-side logic, impossible to access other users' data via URL manipulation

### 2. **User Isolation Automatic**
```typescript
// Frontend just calls /api/todos
const response = await apiGet('/api/todos');

// Backend automatically filters:
// Query: SELECT * FROM todos WHERE user_id = current_user.id
// Where current_user comes from JWT validation in get_current_user dependency
```

### 3. **REST Compliance**
- `/api/todos` - Resource collection (all user's todos)
- `/api/todos/{id}` - Specific resource
- More standard REST pattern than `/api/{user_id}/tasks`

---

## Frontend Tasks Updated

### Updated Task Descriptions

**T-237: Configure Better Auth Client**
- No changes needed - still retrieves JWT with all required claims
- JWT includes `id` claim for user identification (though not needed for URL construction)

**T-238: Create API Client**
- ✅ Updated: API client still attaches JWT to all requests
- ✅ Updated: Uses `/api/todos` endpoints (no user_id in URL)
- ✅ Updated: Error handling remains the same (401/403/404)

**T-266: Implement POST /api/todos**
- ✅ CORRECTED: Uses `POST /api/todos` (not `/api/{user_id}/tasks`)
- ✅ CORRECTED: Backend auto-assigns `user_id` from JWT claims
- Request body: `{ title, description }`
- Backend sets: `user_id` from JWT claim

**T-267: Implement PUT /api/todos/{id}**
- ✅ CORRECTED: Uses `PUT /api/todos/{id}` (not `/api/{user_id}/tasks/{id}`)
- ✅ CORRECTED: Backend verifies ownership via JWT
- Request body: `{ title, description }`
- Backend checks: `todo.user_id == current_user.id`

**T-276: Implement GET /api/todos with Filter**
- ✅ NO CHANGE NEEDED: Already uses `/api/todos`
- Frontend can pass `?is_complete=true|false` query param
- Backend filters by JWT claims automatically

**T-286: Implement DELETE /api/todos/{id}**
- ✅ NO CHANGE NEEDED: Already uses `/api/todos/{id}`
- Backend verifies ownership via JWT
- Returns 403 if not owner, 404 if not found

---

## Example: Create Todo Flow

### Before (With User ID in URL)

```typescript
// Frontend had to do this:
const { data: session } = await authClient.getSession();
const userId = session.user.id;

const response = await fetch(`/api/${userId}/tasks`, {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ title: 'Buy milk' }),
});
```

### After (Current - No User ID in URL)

```typescript
// Frontend now just does this:
const response = await apiPost('/api/todos', {
  title: 'Buy milk',
  description: 'From the grocery store',
});

// API client automatically attaches JWT
// Backend automatically filters by JWT claims
```

**Benefit**: Simpler, cleaner, more secure

---

## Data Isolation: How It Works

### Backend Enforcement

```python
# backend/app/api/todos.py
@router.get("/api/todos")
async def list_todos(
    current_user: User = Depends(get_current_user),  # JWT validation
    db: Session = Depends(get_db)
):
    # Query ONLY returns todos where user_id == current_user.id
    statement = select(Todo).where(Todo.user_id == current_user.id)
    todos = db.exec(statement).all()
    return todos
```

### Frontend Respects Backend Boundaries

```typescript
// Frontend doesn't construct URLs with specific user_ids
// Frontend just calls /api/todos and trusts backend filtering

const todos = await apiGet('/api/todos');
// Backend automatically returns only current user's todos
```

### Attack Prevention

**Scenario**: Attacker tries to guess another user's todo ID

```
Attacker sends: GET /api/todos/550e8400-someone-else-id
With JWT: alice's token

Backend:
1. Validates JWT → current_user = alice
2. Queries: SELECT * FROM todos WHERE id = 550e8400-someone-else-id
3. Finds the todo (it exists)
4. Checks: todo.user_id == alice.id ?
5. NO → Returns 404 Not Found (or 403 Forbidden)
6. Attacker can't tell if todo exists
```

**Result**: Secure even if attacker knows other users' todo IDs

---

## No Frontend Code Changes Required

### API Client Pattern Remains Unchanged

The centralized API client pattern documented in `JWT_ATTACHMENT.md` works perfectly:

```typescript
// This pattern works with both approaches:
const response = await apiPost('/api/todos', data);
const response = await apiGet(`/api/todos/${todoId}`);
const response = await apiDelete(`/api/todos/${todoId}`);
```

### Hook Interface Remains Unchanged

```typescript
// useTodos.ts - no changes needed
export function useTodos() {
  const loadTodos = async () => {
    const response = await apiGet('/api/todos');  // ✅ Works
    setTodos(response.todos);
  };

  const createTodo = async (data) => {
    const response = await apiPost('/api/todos', data);  // ✅ Works
    return response;
  };

  const updateTodo = async (id, data) => {
    const response = await apiPut(`/api/todos/${id}`, data);  // ✅ Works
    return response;
  };

  const deleteTodo = async (id) => {
    await apiDelete(`/api/todos/${id}`);  // ✅ Works
  };

  return { loadTodos, createTodo, updateTodo, deleteTodo };
}
```

---

## What Needs to Happen

### Phase 0: ✅ COMPLETE
- [x] Verified actual backend API implementation
- [x] Documented `/api/todos` pattern
- [x] Created `API_CONTRACT.md` with correct endpoints
- [x] Updated task descriptions to use correct endpoints

### Phase 1: No Changes Needed
- Setup proceeds as planned
- All dependencies compatible
- CLI tools work with correct endpoints

### Phase 2–9: All Tasks Proceed As-Is
- Hook logic already designed for `/api/todos` pattern
- Component implementations don't depend on URL structure
- Error handling covers all response codes

---

## Verification Checklist

- [x] Backend API contract verified (T-230)
- [x] Actual endpoints documented (`API_CONTRACT.md`)
- [x] Frontend tasks updated to use `/api/todos`
- [x] JWT attachment pattern remains unchanged
- [x] API client implementation compatible
- [x] Hook interfaces compatible
- [x] Data isolation strategy verified
- [x] No frontend code rewrites needed
- [x] Implementation can proceed immediately

---

## References

- **Backend Implementation**: `/backend/app/api/todos.py`
- **Frontend API Contract**: `frontend/docs/API_CONTRACT.md`
- **JWT Attachment Pattern**: `frontend/docs/JWT_ATTACHMENT.md`
- **Phase 0 Report**: `frontend/docs/PHASE_0_VALIDATION_REPORT.md`

---

**Status**: ✅ All corrections applied. Frontend tasks aligned with actual backend implementation.

**Ready to Proceed**: ✅ Phase 1 Setup (T-235–T-243)

