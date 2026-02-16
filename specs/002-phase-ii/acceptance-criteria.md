# Acceptance Criteria & Verification Checklist - Phase II

**Feature**: Full-Stack Todo Application with Authentication
**Phase**: II
**Created**: 2025-12-29

---

## Core Acceptance Criteria

### AC-001: All API Requests Require JWT Token Authentication

**Acceptance Statement**: Every protected endpoint MUST require a valid JWT token in the `Authorization: Bearer <token>` header. Missing or invalid tokens MUST return `401 Unauthorized`.

**Verification**:
- [ ] POST /api/todos without token returns 401
- [ ] GET /api/todos without token returns 401
- [ ] PUT /api/todos/{id} without token returns 401
- [ ] PATCH /api/todos/{id} without token returns 401
- [ ] DELETE /api/todos/{id} without token returns 401
- [ ] GET /api/todos/{id} without token returns 401
- [ ] Auth endpoints (signup, signin) are accessible without token
- [ ] Expired tokens return 401 and trigger frontend redirect

**How to Test**:
```bash
# Without token (should fail)
curl -X GET http://localhost:8000/api/todos

# With token (should succeed)
curl -X GET http://localhost:8000/api/todos \
  -H "Authorization: Bearer <valid_token>"

# With invalid token (should fail)
curl -X GET http://localhost:8000/api/todos \
  -H "Authorization: Bearer invalid_token_here"
```

---

### AC-002: User Data Isolation - All Responses Filtered by user_id

**Acceptance Statement**: Every API response MUST contain only data belonging to the authenticated user. No user can view, modify, or delete another user's todos. All queries MUST filter by the `user_id` derived from the JWT token.

**Verification**:
- [ ] User A cannot view User B's todos via GET /api/todos
- [ ] User A cannot view User B's specific todo via GET /api/todos/{todo_id_of_B}
- [ ] User A cannot update User B's todo via PUT /api/todos/{todo_id_of_B} (returns 403)
- [ ] User A cannot toggle User B's todo via PATCH /api/todos/{todo_id_of_B} (returns 403)
- [ ] User A cannot delete User B's todo via DELETE /api/todos/{todo_id_of_B} (returns 403)
- [ ] Database queries always include `WHERE user_id = <authenticated_user_id>`
- [ ] 403 Forbidden is returned for ownership violations (not 404 to avoid information leakage)

**How to Test**:
```bash
# Create two users and their todos
User_A_Token=$(signin user_a@example.com)
User_B_Token=$(signin user_b@example.com)

# User A creates a todo
curl -X POST http://localhost:8000/api/todos \
  -H "Authorization: Bearer $User_A_Token" \
  -d '{"title":"User A todo"}'

# Get User B's todos (should not include User A's todo)
curl -X GET http://localhost:8000/api/todos \
  -H "Authorization: Bearer $User_B_Token"

# User B attempts to access User A's todo (should fail with 403)
curl -X GET http://localhost:8000/api/todos/{User_A_todo_id} \
  -H "Authorization: Bearer $User_B_Token"
```

---

### AC-003: User Signup with Email Validation

**Acceptance Statement**: Users MUST be able to create accounts via POST /auth/signup with email, password, and optional name. Email MUST be unique and valid. Password MUST meet minimum strength requirements (≥8 characters).

**Verification**:
- [ ] Valid signup creates user account and returns 201 with user data + token
- [ ] Duplicate email returns 400 Bad Request with error message
- [ ] Invalid email format returns 400 Bad Request with error message
- [ ] Password < 8 characters returns 400 Bad Request with error message
- [ ] Name field is optional (signup succeeds without it)
- [ ] Email is case-insensitive for uniqueness (user@example.com == USER@EXAMPLE.COM)
- [ ] Password is never returned in response (only hashed password stored)
- [ ] User is automatically logged in after successful signup (token returned)

**How to Test**:
```bash
# Valid signup
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "securePass123",
    "name": "New User"
  }'
# Expected: 201 with user + token

# Duplicate email
curl -X POST http://localhost:8000/auth/signup \
  -d '{"email": "newuser@example.com", "password": "securePass123"}'
# Expected: 400 "Email already registered"

# Invalid password
curl -X POST http://localhost:8000/auth/signup \
  -d '{"email": "another@example.com", "password": "short"}'
# Expected: 400 "Password must be at least 8 characters"
```

---

### AC-004: User Signin with Credentials Validation

**Acceptance Statement**: Users MUST be able to authenticate via POST /auth/signin with email and password. Valid credentials return JWT token; invalid credentials return 401 Unauthorized without revealing whether email exists.

**Verification**:
- [ ] Valid email + password returns 200 with user data + token
- [ ] Invalid email returns 401 Unauthorized (generic message, no info leakage)
- [ ] Invalid password returns 401 Unauthorized (generic message)
- [ ] Non-existent email returns 401 Unauthorized (not 404, to prevent user enumeration)
- [ ] Token is valid and can be used for protected endpoints
- [ ] Token includes user_id and email in claims
- [ ] Password is never returned in response

**How to Test**:
```bash
# Valid signin
curl -X POST http://localhost:8000/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securePass123"}'
# Expected: 200 with user + token

# Invalid password
curl -X POST http://localhost:8000/auth/signin \
  -d '{"email": "user@example.com", "password": "wrongPassword"}'
# Expected: 401 "Invalid credentials"

# Non-existent email
curl -X POST http://localhost:8000/auth/signin \
  -d '{"email": "nonexistent@example.com", "password": "anyPassword"}'
# Expected: 401 "Invalid credentials" (same message as invalid password)
```

---

### AC-005: User Logout

**Acceptance Statement**: Users MUST be able to logout via POST /auth/logout with valid JWT token. Logout invalidates the session and subsequent requests with the same token MUST return 401.

**Verification**:
- [ ] Logout with valid token returns 200 OK
- [ ] Token is invalidated after logout (database session deleted)
- [ ] Subsequent requests with invalidated token return 401
- [ ] Invalid/missing token in logout request returns 401
- [ ] Logout clears frontend session/cookie

**How to Test**:
```bash
Token=$(signin user@example.com)

# Use token (should work)
curl -X GET http://localhost:8000/api/todos \
  -H "Authorization: Bearer $Token"
# Expected: 200 with todos

# Logout
curl -X POST http://localhost:8000/auth/logout \
  -H "Authorization: Bearer $Token"
# Expected: 200

# Use same token again (should fail)
curl -X GET http://localhost:8000/api/todos \
  -H "Authorization: Bearer $Token"
# Expected: 401 Unauthorized
```

---

### AC-006: Create Todo CRUD - Create (POST)

**Acceptance Statement**: Authenticated users MUST be able to create todos via POST /api/todos with required title and optional description. System MUST validate inputs and return 201 Created with the created todo including generated ID.

**Verification**:
- [ ] Valid create request returns 201 with todo data including ID and user_id
- [ ] Todo is stored in database with correct user_id
- [ ] Title is required; empty/missing title returns 400
- [ ] Description is optional (can be null or empty string)
- [ ] Title max 500 characters; exceeding returns 400
- [ ] Description max 2000 characters; exceeding returns 400
- [ ] is_complete defaults to false
- [ ] created_at and updated_at are set to current timestamp
- [ ] Todo appears in user's todo list immediately

**How to Test**:
```bash
Token=$(signin user@example.com)

# Valid create
curl -X POST http://localhost:8000/api/todos \
  -H "Authorization: Bearer $Token" \
  -H "Content-Type: application/json" \
  -d '{"title":"New todo","description":"A description"}'
# Expected: 201 with todo

# No title
curl -X POST http://localhost:8000/api/todos \
  -H "Authorization: Bearer $Token" \
  -d '{"description":"No title"}'
# Expected: 400 "Title is required"

# Verify in list
curl -X GET http://localhost:8000/api/todos \
  -H "Authorization: Bearer $Token"
# Expected: 200 with newly created todo in list
```

---

### AC-007: Read Todo CRUD - List & Get

**Acceptance Statement**: Authenticated users MUST be able to retrieve their todos via GET /api/todos (list) and GET /api/todos/{id} (single). Results MUST be filtered by user_id.

**Verification**:
- [ ] GET /api/todos returns list of all user's todos (200 OK)
- [ ] GET /api/todos supports pagination (skip, limit parameters)
- [ ] GET /api/todos supports filtering by is_complete
- [ ] GET /api/todos supports sorting by created_at, updated_at
- [ ] GET /api/todos/{id} returns specific todo (200 OK) if user is owner
- [ ] GET /api/todos/{id} returns 404 if todo doesn't exist
- [ ] GET /api/todos/{id} returns 403 if user is not owner
- [ ] Empty list returns empty array (not error)
- [ ] Todos are ordered by created_at descending (newest first) by default

**How to Test**:
```bash
Token=$(signin user@example.com)

# List all todos
curl -X GET http://localhost:8000/api/todos \
  -H "Authorization: Bearer $Token"
# Expected: 200 with todos list

# List with pagination
curl -X GET "http://localhost:8000/api/todos?skip=0&limit=10" \
  -H "Authorization: Bearer $Token"
# Expected: 200 with max 10 todos

# List incomplete only
curl -X GET "http://localhost:8000/api/todos?is_complete=false" \
  -H "Authorization: Bearer $Token"
# Expected: 200 with only incomplete todos

# Get specific todo
curl -X GET http://localhost:8000/api/todos/{todo_id} \
  -H "Authorization: Bearer $Token"
# Expected: 200 with single todo
```

---

### AC-008: Update Todo CRUD - Update (PUT)

**Acceptance Statement**: Users MUST be able to update todo title and/or description via PUT /api/todos/{id}. System MUST validate inputs, check ownership, and return updated todo.

**Verification**:
- [ ] Valid update returns 200 with updated todo
- [ ] Can update title only (description unchanged)
- [ ] Can update description only (title unchanged)
- [ ] Can update both simultaneously
- [ ] Empty title returns 400 "Title cannot be empty"
- [ ] Title max 500 chars; exceeding returns 400
- [ ] Description max 2000 chars; exceeding returns 400
- [ ] Non-existent todo ID returns 404
- [ ] Wrong owner returns 403
- [ ] updated_at timestamp is updated
- [ ] is_complete is not changed by PUT request

**How to Test**:
```bash
Token=$(signin user@example.com)

# Create a todo first
TODO_ID=$(curl -X POST http://localhost:8000/api/todos \
  -H "Authorization: Bearer $Token" \
  -d '{"title":"Original"}' | jq -r '.id')

# Update title
curl -X PUT http://localhost:8000/api/todos/$TODO_ID \
  -H "Authorization: Bearer $Token" \
  -d '{"title":"Updated Title"}'
# Expected: 200 with updated todo

# Update title to empty (should fail)
curl -X PUT http://localhost:8000/api/todos/$TODO_ID \
  -H "Authorization: Bearer $Token" \
  -d '{"title":""}'
# Expected: 400 "Title cannot be empty"
```

---

### AC-009: Toggle Todo CRUD - Status Update (PATCH)

**Acceptance Statement**: Users MUST be able to toggle is_complete status via PATCH /api/todos/{id} with is_complete boolean. System MUST validate ownership and return updated todo.

**Verification**:
- [ ] Valid PATCH returns 200 with updated todo
- [ ] is_complete changes from false to true
- [ ] is_complete changes from true to false
- [ ] Other fields (title, description) are not changed
- [ ] updated_at timestamp is updated
- [ ] Non-existent todo ID returns 404
- [ ] Wrong owner returns 403
- [ ] Frontend can visually indicate completion (strikethrough/styling)

**How to Test**:
```bash
Token=$(signin user@example.com)

# Get initial status
curl -X GET http://localhost:8000/api/todos/$TODO_ID \
  -H "Authorization: Bearer $Token" | jq '.is_complete'
# Expected: false

# Toggle to complete
curl -X PATCH http://localhost:8000/api/todos/$TODO_ID \
  -H "Authorization: Bearer $Token" \
  -d '{"is_complete":true}'
# Expected: 200 with is_complete = true

# Verify change
curl -X GET http://localhost:8000/api/todos/$TODO_ID \
  -H "Authorization: Bearer $Token" | jq '.is_complete'
# Expected: true
```

---

### AC-010: Delete Todo CRUD - Delete

**Acceptance Statement**: Users MUST be able to permanently delete todos via DELETE /api/todos/{id}. System MUST validate ownership and return 204 No Content on success.

**Verification**:
- [ ] Valid delete returns 204 No Content (no response body)
- [ ] Todo is removed from database
- [ ] Todo no longer appears in user's list
- [ ] Non-existent todo ID returns 404
- [ ] Wrong owner returns 403
- [ ] Deleting same todo twice returns 404 second time (confirmation of deletion)

**How to Test**:
```bash
Token=$(signin user@example.com)

# Create a todo
TODO_ID=$(curl -X POST http://localhost:8000/api/todos \
  -H "Authorization: Bearer $Token" \
  -d '{"title":"To Delete"}' | jq -r '.id')

# Verify it exists
curl -X GET http://localhost:8000/api/todos/$TODO_ID \
  -H "Authorization: Bearer $Token"
# Expected: 200

# Delete it
curl -X DELETE http://localhost:8000/api/todos/$TODO_ID \
  -H "Authorization: Bearer $Token"
# Expected: 204 No Content

# Verify it's gone
curl -X GET http://localhost:8000/api/todos/$TODO_ID \
  -H "Authorization: Bearer $Token"
# Expected: 404 Not Found
```

---

### AC-011: Frontend Responsiveness

**Acceptance Statement**: Frontend MUST be responsive and fully functional across mobile (320px), tablet (768px), and desktop (1024px+) viewports.

**Verification**:
- [ ] App renders correctly on mobile (320px width)
- [ ] App renders correctly on tablet (768px width)
- [ ] App renders correctly on desktop (1024px+ width)
- [ ] Navigation is accessible on all viewports (hamburger menu on mobile, nav bar on desktop)
- [ ] Todo list is readable and scannable on all viewports
- [ ] Form inputs are large enough to tap on mobile (48px minimum)
- [ ] Action buttons (edit, delete, toggle) are accessible on all viewports

**How to Test**:
```bash
# Use Chrome DevTools responsive design mode
# Test with viewport sizes: 320px (mobile), 768px (tablet), 1024px (desktop)
# Verify all interactive elements are accessible without horizontal scroll
```

---

### AC-012: Input Validation

**Acceptance Statement**: All inputs MUST be validated on both frontend and backend. Invalid inputs MUST return 400 Bad Request with descriptive error messages. All SQL injection and XSS attempts MUST be prevented.

**Verification**:
- [ ] Email validation rejects invalid formats
- [ ] Password validation enforces 8+ character minimum
- [ ] Title validation rejects empty strings
- [ ] Title validation enforces 500 character maximum
- [ ] Description validation enforces 2000 character maximum
- [ ] Special characters (emoji, unicode) are safely handled
- [ ] SQL injection attempts in title/description fail safely (escaped by ORM)
- [ ] XSS attempts in title/description are escaped in HTML rendering
- [ ] Error messages are user-friendly and actionable

**How to Test**:
```bash
# SQL injection attempt
curl -X POST http://localhost:8000/api/todos \
  -H "Authorization: Bearer $Token" \
  -d '{"title":"Test\"; DROP TABLE todos; --"}'
# Expected: 400 or data safely stored (not executed)

# XSS attempt
curl -X POST http://localhost:8000/api/todos \
  -H "Authorization: Bearer $Token" \
  -d '{"title":"<script>alert(\"xss\")</script>"}'
# Expected: 400 or HTML-escaped rendering (not executed)
```

---

### AC-013: Error Handling & Messages

**Acceptance Statement**: All error responses MUST include descriptive error messages, correct HTTP status codes, and no sensitive information leakage.

**Verification**:
- [ ] 400 Bad Request includes validation details
- [ ] 401 Unauthorized is returned for missing/invalid tokens
- [ ] 403 Forbidden is returned for ownership violations (not 404)
- [ ] 404 Not Found is returned for non-existent resources
- [ ] 500 Internal Server Error is returned for unexpected errors
- [ ] Error messages do not leak sensitive info (e.g., database details)
- [ ] Error responses are JSON formatted (consistent with API)

**How to Test**: See previous test cases for specific error scenarios.

---

### AC-014: Performance Requirements

**Acceptance Statement**: API response times MUST meet performance requirements under normal load. Frontend MUST load and become interactive quickly.

**Verification**:
- [ ] GET /api/todos responds in < 200ms (p95)
- [ ] POST /api/todos responds in < 300ms (p95)
- [ ] PUT /api/todos/{id} responds in < 300ms (p95)
- [ ] PATCH /api/todos/{id} responds in < 300ms (p95)
- [ ] DELETE /api/todos/{id} responds in < 300ms (p95)
- [ ] Frontend loads in < 2 seconds (first contentful paint)
- [ ] No N+1 queries in todo list retrieval

**How to Test**:
```bash
# Use curl with timing
time curl -X GET http://localhost:8000/api/todos \
  -H "Authorization: Bearer $Token"

# Use frontend DevTools Performance tab
# Measure First Contentful Paint (FCP) and Largest Contentful Paint (LCP)
```

---

## Integration Test Scenarios

### Scenario 1: Complete User Journey (New User)

**Flow**: Signup → View empty list → Create 3 todos → View list → Update one → Mark one complete → Delete one → Logout

**Expected Result**: All operations succeed without errors; user isolation maintained.

**Steps**:
1. Signup with valid email/password
2. Verify redirected to dashboard
3. Verify empty list message
4. Create 3 todos with various titles/descriptions
5. Verify all 3 appear in list
6. Edit first todo's title
7. Toggle second todo to complete
8. Delete third todo
9. Verify final state: 2 todos (1 complete, 1 incomplete, both with updated names)
10. Logout and verify token invalidated

---

### Scenario 2: Multi-User Data Isolation

**Flow**: User A creates todos → User B signs up → User A and B view lists → Verify no cross-access

**Expected Result**: Each user sees only their own todos; no data leakage.

**Steps**:
1. Signup as User A, create 5 todos
2. Signin as User B, verify empty list
3. User B creates 3 todos
4. Verify User A still sees 5 todos (not 8)
5. Verify User B still sees 3 todos (not 8)
6. Attempt User A to access User B's todo IDs (should get 403)

---

### Scenario 3: Token Expiration & Re-Authentication

**Flow**: Signin → Access API (works) → Wait for token expiration → Access API (fails) → Signin again → Works

**Expected Result**: Expired tokens properly invalidated; users must re-authenticate.

**Steps**:
1. Signin, receive token
2. Use token to access /api/todos (succeeds)
3. Simulate token expiration (manually expire in database)
4. Use same token to access /api/todos (returns 401)
5. Frontend redirects to signin
6. Signin again, receive new token
7. Use new token to access /api/todos (succeeds)

---

## Definition of Done Checklist

- [ ] All 14 acceptance criteria verified and passing
- [ ] All integration test scenarios completed successfully
- [ ] Code reviewed for security vulnerabilities (SQL injection, XSS, CSRF)
- [ ] Database schema is optimized with proper indexes
- [ ] API documentation is complete and accurate
- [ ] Frontend is responsive on mobile/tablet/desktop
- [ ] Performance benchmarks met (response times < 200ms p95)
- [ ] All tests written and passing (unit, integration, e2e)
- [ ] Error handling tested for edge cases
- [ ] Git commits reference task IDs (Phase II branching)
- [ ] PR created and approved before merge

