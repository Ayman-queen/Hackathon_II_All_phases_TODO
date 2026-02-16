# Feature Specification: Phase II - Full-Stack Todo Application with Authentication

**Feature Branch**: `phase-2`
**Created**: 2025-12-29
**Status**: Active Development
**Input**: A full-stack web application with RESTful API (Task CRUD), user authentication via Better Auth, responsive Next.js frontend, and persistent PostgreSQL backend with SQLModel ORM. All requests must be user-scoped and authenticated.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - User Registration (Priority: P1)

A new user creates an account by providing email and password via the signup interface. The system validates inputs, stores credentials securely via Better Auth, and logs the user in automatically upon successful registration.

**Why this priority**: User acquisition is critical. Without signup, no users can access the system. This is the entry point to the entire application.

**Independent Test**: Can be fully tested by submitting a signup form with valid email/password, verifying account creation, and confirming automatic login redirect.

**Acceptance Scenarios**:

1. **Given** a new user visits the signup page, **When** they provide a valid email and password, **Then** the account is created and they are automatically logged in
2. **Given** a user attempts signup with an invalid email format, **When** they submit the form, **Then** an error message displays "Invalid email format"
3. **Given** a user attempts signup with a password under 8 characters, **When** they submit the form, **Then** an error displays "Password must be at least 8 characters"
4. **Given** an email already exists in the system, **When** a new signup is attempted with that email, **Then** an error displays "Email already registered"

---

### User Story 2 - User Authentication (Priority: P1)

An existing user logs in with email and password. The system validates credentials via Better Auth, issues a JWT token, and grants access to the todo dashboard. Logout clears the session and token.

**Why this priority**: Core security mechanism. Every subsequent feature depends on authentication. Users must be able to access their account securely.

**Independent Test**: Can be fully tested by logging in with valid credentials, verifying token issuance, accessing protected endpoints, and verifying logout clears access.

**Acceptance Scenarios**:

1. **Given** a user is on the signin page, **When** they provide valid credentials, **Then** a JWT token is issued and they are redirected to the dashboard
2. **Given** a user provides an invalid email or password, **When** they attempt signin, **Then** an error displays "Invalid credentials"
3. **Given** a user is logged in, **When** they click logout, **Then** the session is cleared, token is invalidated, and they are redirected to signin
4. **Given** a user attempts to access a protected route without a token, **When** they navigate to that route, **Then** they are redirected to signin

---

### User Story 3 - View User's Todos (Priority: P1)

A logged-in user views their complete list of todos. The system retrieves todos scoped to their user_id from the database and displays them in a responsive, organized interface with title, description, status, and action buttons.

**Why this priority**: Core MVP functionality. Users must see their todos to be productive. This is the central interface of the app.

**Independent Test**: Can be fully tested by logging in, verifying todos are displayed scoped to current user, and confirming other users' todos are invisible.

**Acceptance Scenarios**:

1. **Given** a user is logged in and has todos, **When** they view the dashboard, **Then** all their todos display with ID, title, description, and status
2. **Given** a logged-in user has no todos, **When** they view the dashboard, **Then** a message displays "No todos yet. Create one to get started!"
3. **Given** two different users have todos, **When** each user views their dashboard, **Then** each sees only their own todos (data isolation enforced)
4. **Given** a user is logged out, **When** they attempt to access /api/todos, **Then** a 401 Unauthorized response is returned

---

### User Story 4 - Create a New Todo (Priority: P1)

A user creates a new todo by providing a title and optional description via a form or inline input. The system validates input, creates the todo in the database with the user's user_id, and returns the created todo with a unique ID.

**Why this priority**: Core functionality. Users must be able to add todos to the system.

**Independent Test**: Can be fully tested by submitting a create request with valid data, verifying the todo is stored in the database, and confirming it appears in the user's list.

**Acceptance Scenarios**:

1. **Given** a user is on the todo dashboard, **When** they click "Create Todo" and provide a title, **Then** a POST request sends the todo to the API and it appears in the list
2. **Given** a user provides only a title (description optional), **When** they create the todo, **Then** the todo is created with an empty description
3. **Given** a user submits a create request without a token, **When** the request is made, **Then** a 401 Unauthorized response is returned
4. **Given** a user submits an empty title, **When** they attempt to create, **Then** a validation error displays "Title is required"

---

### User Story 5 - Update Todo Details (Priority: P2)

A user modifies a todo's title or description by clicking an edit button, updating the form, and saving. The system updates the todo in the database and reflects changes immediately on the frontend.

**Why this priority**: Important for task management refinement. Users need to update tasks as requirements evolve, but less critical than create/view.

**Independent Test**: Can be fully tested by creating a todo, updating its title/description via PUT request, and verifying changes persist.

**Acceptance Scenarios**:

1. **Given** a user has a todo, **When** they click edit and update the title, **Then** a PUT request updates the database and the UI reflects the change
2. **Given** a user updates only the description, **When** they save, **Then** the title remains unchanged and description is updated
3. **Given** a user attempts to update another user's todo, **When** they submit the request, **Then** a 403 Forbidden response is returned
4. **Given** a user submits an update with an empty title, **When** the request is processed, **Then** a validation error is returned

---

### User Story 6 - Mark Todo as Complete/Incomplete (Priority: P2)

A user toggles a todo's completion status with a checkbox or status button. The system updates the todo's is_complete field and visually reflects the change (strikethrough, different styling).

**Why this priority**: Core task tracking. Users need to mark progress, but less critical than creation/viewing.

**Independent Test**: Can be fully tested by creating a todo, toggling its status via PATCH request, and verifying visual/database changes.

**Acceptance Scenarios**:

1. **Given** a todo is incomplete, **When** the user clicks the checkbox, **Then** a PATCH request updates is_complete to true and the UI shows strikethrough
2. **Given** a todo is marked complete, **When** the user clicks the checkbox again, **Then** is_complete reverts to false and strikethrough is removed
3. **Given** a user attempts to toggle another user's todo, **When** the request is made, **Then** a 403 Forbidden response is returned

---

### User Story 7 - Delete Todo (Priority: P3)

A user deletes a todo by clicking a delete button and confirming. The system removes the todo from the database. A confirmation dialog prevents accidental deletion.

**Why this priority**: List cleanup is useful but lower priority. Users can manage list size by marking tasks complete without delete.

**Independent Test**: Can be fully tested by creating a todo, deleting it via DELETE request, and verifying it no longer appears in the list.

**Acceptance Scenarios**:

1. **Given** a user has a todo, **When** they click delete, **Then** a confirmation dialog displays
2. **Given** the user confirms deletion, **When** the DELETE request is processed, **Then** the todo is removed from the database and UI
3. **Given** the user cancels deletion, **When** the dialog is dismissed, **Then** the todo remains unchanged
4. **Given** a user attempts to delete another user's todo, **When** the request is made, **Then** a 403 Forbidden response is returned

---

### Edge Cases

- **Invalid JWT Token**: A user submits a request with an expired or tampered token → System returns 401 Unauthorized and prompts re-login
- **Non-Existent Todo**: A user attempts to update/delete a todo with a non-existent ID → System returns 404 Not Found with message "Todo not found"
- **SQL Injection / Malicious Input**: A user submits SQL or script content in title/description → System validates and sanitizes all inputs via SQLModel/Pydantic; no injection possible
- **Race Condition (Concurrent Updates)**: Two users attempt to update the same todo → Last-write-wins; the later request's update is applied (acceptable for MVP)
- **Network Failure**: A user's request to create/update a todo times out → Frontend retries with exponential backoff; user sees "Saving..." state
- **Very Long Inputs**: A user provides a title with 1000+ characters → System accepts it; frontend truncates display with ellipsis (e.g., max 100 chars visible)
- **Special Characters**: User provides emoji, unicode, or markdown in title/description → System accepts and stores as-is; frontend escapes for safe HTML rendering

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a `/auth/signup` endpoint (POST) that accepts email, password, and optional name; validates inputs and creates user account via Better Auth
- **FR-002**: System MUST provide a `/auth/signin` endpoint (POST) that accepts email and password; validates credentials and returns JWT token on success
- **FR-003**: System MUST provide a `/auth/logout` endpoint (POST) that invalidates the user's token and session
- **FR-004**: System MUST require JWT token in Authorization header for all protected endpoints; return 401 Unauthorized if missing or invalid
- **FR-005**: System MUST filter all API responses by user_id derived from JWT claims; no user can access another user's data
- **FR-006**: System MUST provide a `GET /api/todos` endpoint that returns all todos for the authenticated user, scoped by user_id
- **FR-007**: System MUST provide a `POST /api/todos` endpoint that accepts title (required) and description (optional); creates a new todo and returns it with generated ID and user_id
- **FR-008**: System MUST provide a `GET /api/todos/{id}` endpoint that returns a single todo; returns 404 if not found or 403 if user is not the owner
- **FR-009**: System MUST provide a `PUT /api/todos/{id}` endpoint that updates todo title and/or description; validates ownership and returns 403 if unauthorized
- **FR-010**: System MUST provide a `PATCH /api/todos/{id}` endpoint that toggles is_complete status; validates ownership and returns 403 if unauthorized
- **FR-011**: System MUST provide a `DELETE /api/todos/{id}` endpoint that removes a todo; validates ownership and returns 403 if unauthorized
- **FR-012**: System MUST validate all inputs (email format, password length ≥8, non-empty title) and return 400 Bad Request with error details on validation failure
- **FR-013**: Frontend MUST display a responsive layout (mobile, tablet, desktop) with navigation bar containing user info and logout button
- **FR-014**: Frontend MUST display todo list in a scannable format with title, description, status, and action buttons (edit, delete, toggle)
- **FR-015**: Frontend MUST persist JWT token in secure httpOnly cookie; never store in localStorage for security
- **FR-016**: Frontend MUST automatically redirect to signin if token expires or 401 is received
- **FR-017**: System MUST store all data in Neon PostgreSQL using SQLModel ORM with proper foreign keys and constraints

### Key Entities *(include if feature involves data)*

- **User**: Represents an authenticated user. Attributes: `id` (UUID, PK), `email` (unique string), `password_hash` (bcrypt), `name` (optional string), `created_at` (timestamp), `updated_at` (timestamp)
- **Todo**: Represents a task item scoped to a user. Attributes: `id` (UUID, PK), `user_id` (FK to User), `title` (required string, max 500 chars), `description` (optional string, max 2000 chars), `is_complete` (boolean, default false), `created_at` (timestamp), `updated_at` (timestamp)
- **Session** (via Better Auth): Stores active user sessions and JWT tokens. Better Auth manages creation, validation, and expiration.

### API Contract

#### Authentication Endpoints

**POST /auth/signup**
```json
Request:
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}

Response (201 Created):
{
  "user": {
    "id": "uuid-1",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "token": "eyJhbGciOiJIUzI1NiIs..."
}

Response (400 Bad Request):
{
  "error": "Email already registered" | "Password must be at least 8 characters" | "Invalid email format"
}
```

**POST /auth/signin**
```json
Request:
{
  "email": "user@example.com",
  "password": "securePassword123"
}

Response (200 OK):
{
  "user": {
    "id": "uuid-1",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "token": "eyJhbGciOiJIUzI1NiIs..."
}

Response (401 Unauthorized):
{
  "error": "Invalid credentials"
}
```

**POST /auth/logout**
```json
Request: (Authorization: Bearer <token>)

Response (200 OK):
{
  "message": "Logout successful"
}

Response (401 Unauthorized):
{
  "error": "Unauthorized"
}
```

#### Todo CRUD Endpoints

**GET /api/todos** (Requires Auth)
```json
Response (200 OK):
{
  "todos": [
    {
      "id": "uuid-1",
      "user_id": "uuid-user",
      "title": "Complete project spec",
      "description": "Finish Phase II spec document",
      "is_complete": false,
      "created_at": "2025-12-29T10:00:00Z",
      "updated_at": "2025-12-29T10:00:00Z"
    }
  ]
}

Response (401 Unauthorized):
{
  "error": "Unauthorized"
}
```

**POST /api/todos** (Requires Auth)
```json
Request:
{
  "title": "New todo item",
  "description": "Optional description"
}

Response (201 Created):
{
  "id": "uuid-2",
  "user_id": "uuid-user",
  "title": "New todo item",
  "description": "Optional description",
  "is_complete": false,
  "created_at": "2025-12-29T10:00:00Z",
  "updated_at": "2025-12-29T10:00:00Z"
}

Response (400 Bad Request):
{
  "error": "Title is required"
}

Response (401 Unauthorized):
{
  "error": "Unauthorized"
}
```

**GET /api/todos/{id}** (Requires Auth)
```json
Response (200 OK):
{
  "id": "uuid-1",
  "user_id": "uuid-user",
  "title": "Complete project spec",
  "description": "Finish Phase II spec document",
  "is_complete": false,
  "created_at": "2025-12-29T10:00:00Z",
  "updated_at": "2025-12-29T10:00:00Z"
}

Response (404 Not Found):
{
  "error": "Todo not found"
}

Response (403 Forbidden):
{
  "error": "You do not have permission to access this todo"
}

Response (401 Unauthorized):
{
  "error": "Unauthorized"
}
```

**PUT /api/todos/{id}** (Requires Auth)
```json
Request:
{
  "title": "Updated todo title",
  "description": "Updated description"
}

Response (200 OK):
{
  "id": "uuid-1",
  "user_id": "uuid-user",
  "title": "Updated todo title",
  "description": "Updated description",
  "is_complete": false,
  "created_at": "2025-12-29T10:00:00Z",
  "updated_at": "2025-12-29T10:05:00Z"
}

Response (400 Bad Request):
{
  "error": "Title is required"
}

Response (403 Forbidden):
{
  "error": "You do not have permission to access this todo"
}

Response (401 Unauthorized):
{
  "error": "Unauthorized"
}
```

**PATCH /api/todos/{id}** (Requires Auth)
```json
Request:
{
  "is_complete": true
}

Response (200 OK):
{
  "id": "uuid-1",
  "user_id": "uuid-user",
  "title": "Complete project spec",
  "description": "Finish Phase II spec document",
  "is_complete": true,
  "created_at": "2025-12-29T10:00:00Z",
  "updated_at": "2025-12-29T10:10:00Z"
}

Response (403 Forbidden):
{
  "error": "You do not have permission to access this todo"
}

Response (401 Unauthorized):
{
  "error": "Unauthorized"
}
```

**DELETE /api/todos/{id}** (Requires Auth)
```json
Response (204 No Content): [No response body]

Response (403 Forbidden):
{
  "error": "You do not have permission to access this todo"
}

Response (404 Not Found):
{
  "error": "Todo not found"
}

Response (401 Unauthorized):
{
  "error": "Unauthorized"
}
```

## Clarifications

### Session 2025-12-29

- Q: Authentication framework: custom JWT/bcrypt vs Better Auth JWT plugin? → A: **Better Auth JWT plugin (Option A).** Mandatory per hackathon constitution and Phase III stateless architecture requirement. Replaces existing custom JWT/bcrypt system.
- Q: Database: Docker Postgres vs Neon Serverless PostgreSQL? → A: **Migrate to Neon immediately (Option A).** Spec-required; use Better Auth's native SQLAlchemy schema; auto-scales to zero.
- Q: User isolation & JWT claims structure? → A: **JWT `sub` = user UUID via Better Auth schema (Option A).** Todo queries filtered by extracted `user_id` from token claims; automatic isolation.
- Q: Migration path for existing users? → A: **Fresh start with Better Auth schema (Option A).** Drop local dev DB; no migration script needed for MVP.
- Q: Better Auth scope: email-only vs multi-provider? → A: **Email/password only for Phase II; OAuth scaffolding for Phase III (Option A).** Minimal scope, spec-compliant, future-proof.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: User can signup, signin, and access their todo list in under 2 minutes of typical interaction
- **SC-002**: All 7 core features (Signup, Signin, View, Create, Update, Toggle, Delete) are fully functional and independently testable
- **SC-003**: 100% of API requests validate JWT token and return 401 if missing/invalid; no unprotected endpoints except /auth/signup and /auth/signin
- **SC-004**: 100% of todo data responses are scoped by user_id; no user can view/modify another user's todos
- **SC-005**: All error responses include descriptive error messages and correct HTTP status codes (400, 401, 403, 404, 500)
- **SC-006**: Frontend is responsive and functional on mobile (320px), tablet (768px), and desktop (1024px+) viewports
- **SC-007**: All todo data (title, description, status, timestamps) is accurately stored in PostgreSQL and instantly reflected in API responses
- **SC-008**: API response latency is under 200ms for all endpoints (p95) under normal load
- **SC-009**: JWT tokens expire after 7 days; expired tokens trigger automatic logout and redirect to signin
- **SC-010**: All database queries use parameterized statements via SQLModel ORM to prevent SQL injection
- **SC-011**: Better Auth handles all user signup/signin; custom JWT/bcrypt system removed entirely
- **SC-012**: All user data stored in Neon PostgreSQL using Better Auth's schema; zero local/Docker database usage
