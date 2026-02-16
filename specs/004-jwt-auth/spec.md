# Feature Specification: JWT Authentication Integration

**Feature Branch**: `004-jwt-auth`
**Created**: 2026-01-01
**Status**: Draft
**Phase**: 2.2

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - User Logs In and Receives JWT Token (Priority: P1)

As a user, I want to log in to the application through the frontend using Better Auth so that I receive a JWT token that authorizes my API requests to the backend.

**Why this priority**: This is the foundation of the entire authentication system. Without JWT token generation and issuance, users cannot authenticate with the backend API.

**Independent Test**: Can be fully tested by logging in through the frontend, checking for JWT token in local storage/cookies, and verifying token structure contains user information.

**Acceptance Scenarios**:

1. **Given** a user is on the login page, **When** the user submits valid credentials, **Then** Better Auth creates a session and issues a JWT token to the frontend
2. **Given** Better Auth issues a JWT token, **When** the token is decoded, **Then** it contains the user's ID, email, and token expiration timestamp
3. **Given** a user has logged in, **When** the user navigates to the dashboard, **Then** the JWT token persists in local storage or cookies

---

### User Story 2 - Frontend Attaches JWT Token to API Requests (Priority: P1)

As the frontend application, I want to automatically attach the JWT token to every API request sent to the backend so that the backend can verify which user is making the request.

**Why this priority**: This ensures all API requests are properly authenticated. Without token attachment, the backend cannot verify user identity and enforce access control.

**Independent Test**: Can be fully tested by making an API request with proper Authorization header and verifying the backend receives the token correctly.

**Acceptance Scenarios**:

1. **Given** the frontend has a valid JWT token, **When** the user makes an API request (GET, POST, PUT, DELETE, PATCH), **Then** the Authorization header contains `Bearer <JWT_TOKEN>`
2. **Given** the user logs out, **When** the JWT token is removed, **Then** subsequent API requests do not include the token
3. **Given** an API request is made, **When** the backend receives it, **Then** it can extract the token from the Authorization header

---

### User Story 3 - Backend Verifies JWT Token and Identifies User (Priority: P1)

As the FastAPI backend, I want to verify JWT tokens from incoming requests so that I can identify which user is making the request and enforce user isolation.

**Why this priority**: This is critical for backend security. The backend must verify tokens before processing any user data to prevent unauthorized access.

**Independent Test**: Can be fully tested by sending requests with valid, invalid, and expired tokens to the backend and verifying appropriate responses.

**Acceptance Scenarios**:

1. **Given** a request arrives at the backend without a JWT token, **When** middleware processes it, **Then** the request receives a 401 Unauthorized response
2. **Given** a request arrives with an invalid JWT token, **When** middleware verifies it, **Then** the request receives a 401 Unauthorized response
3. **Given** a request arrives with a valid JWT token, **When** middleware verifies it, **Then** the user ID is extracted and injected into the request context
4. **Given** an expired JWT token is sent, **When** the backend attempts verification, **Then** the request receives a 401 Unauthorized response

---

### User Story 4 - Users Only See Their Own Tasks (Priority: P1)

As a user, I want the API to return only my tasks so that I cannot see or modify other users' tasks, even if I know their user ID.

**Why this priority**: This is a critical security requirement. User isolation prevents data leaks and maintains privacy.

**Independent Test**: Can be fully tested by authenticating as two different users and verifying that each user's API responses are filtered to only show that user's tasks.

**Acceptance Scenarios**:

1. **Given** User A is authenticated with a valid JWT, **When** User A requests GET `/api/{user_id}/tasks`, **Then** only User A's tasks are returned
2. **Given** User A is authenticated, **When** User A requests GET `/api/{other_user_id}/tasks`, **Then** the request receives a 403 Forbidden or an empty response
3. **Given** User A is authenticated, **When** User A attempts PUT `/api/{other_user_id}/tasks/{id}`, **Then** the request receives a 403 Forbidden
4. **Given** User A is authenticated, **When** User A attempts DELETE `/api/{other_user_id}/tasks/{id}`, **Then** the request receives a 403 Forbidden

---

### User Story 5 - Task CRUD Operations with User Isolation (Priority: P1)

As a user, I want to perform all task operations (create, read, update, delete, toggle completion) through authenticated API endpoints so that my operations are recorded against my user ID.

**Why this priority**: This completes the core functionality. All task operations must work through the authenticated API.

**Independent Test**: Can be fully tested by performing all CRUD operations as an authenticated user and verifying the backend filters responses appropriately.

**Acceptance Scenarios**:

1. **Given** a user is authenticated with a valid JWT, **When** the user POST `/api/{user_id}/tasks`, **Then** the new task is created and associated with that user
2. **Given** a user is authenticated, **When** the user GET `/api/{user_id}/tasks/{id}`, **Then** the task details are returned if the task belongs to that user
3. **Given** a user is authenticated, **When** the user PUT `/api/{user_id}/tasks/{id}`, **Then** the task is updated only if it belongs to that user
4. **Given** a user is authenticated, **When** the user DELETE `/api/{user_id}/tasks/{id}`, **Then** the task is deleted only if it belongs to that user
5. **Given** a user is authenticated, **When** the user PATCH `/api/{user_id}/tasks/{id}/complete`, **Then** the task completion status is toggled only if it belongs to that user

### Edge Cases

- What happens when a JWT token expires mid-session? (User should be prompted to log in again)
- What happens if the shared secret (BETTER_AUTH_SECRET) is different between frontend and backend? (Token verification will fail, requests will be rejected)
- What if a user has multiple active sessions across different browsers? (Each session has its own valid token; logging out from one session only invalidates that session's token, not all sessions)
- What happens if the backend is temporarily unavailable when the frontend tries to attach the token? (Request fails with appropriate error message)
- What if the user ID in the URL doesn't match the user ID in the JWT token? (Request should be rejected with 403 Forbidden)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Better Auth MUST be configured with JWT plugin enabled to issue JWT tokens on successful login
- **FR-002**: JWT tokens MUST contain user ID and email as claims
- **FR-003**: JWT tokens MUST have a configurable expiration time (default: 7 days)
- **FR-004**: Frontend API client MUST automatically attach JWT token to all outgoing API requests in the `Authorization: Bearer <token>` header
- **FR-005**: Frontend MUST store JWT token in a secure location (local storage or secure HTTP-only cookies)
- **FR-006**: FastAPI backend MUST have middleware that extracts and verifies JWT tokens from the Authorization header
- **FR-007**: Backend middleware MUST reject requests without a valid JWT token with 401 Unauthorized response
- **FR-008**: Backend middleware MUST extract the user ID from the verified JWT token and inject it into the request context
- **FR-009**: All API routes MUST filter results to only return data belonging to the authenticated user
- **FR-010**: All API routes MUST validate that the user ID in the URL matches the user ID in the JWT token; if not, return 403 Forbidden
- **FR-011**: GET `/api/{user_id}/tasks` MUST list all tasks for the authenticated user
- **FR-012**: POST `/api/{user_id}/tasks` MUST create a new task and associate it with the authenticated user
- **FR-013**: GET `/api/{user_id}/tasks/{id}` MUST return task details if the task belongs to the authenticated user
- **FR-014**: PUT `/api/{user_id}/tasks/{id}` MUST update a task if it belongs to the authenticated user
- **FR-015**: DELETE `/api/{user_id}/tasks/{id}` MUST delete a task if it belongs to the authenticated user
- **FR-016**: PATCH `/api/{user_id}/tasks/{id}/complete` MUST toggle task completion status if the task belongs to the authenticated user
- **FR-017**: Both frontend and backend MUST use the same shared secret key (BETTER_AUTH_SECRET) for JWT signing and verification
- **FR-018**: System MUST handle token expiration gracefully; frontend should prompt user to re-authenticate

### Non-Functional Requirements

- **NFR-001**: User ID Type: Better Auth generates string identifiers (~33 char alphanumeric, e.g., 'w2PYO9wq2FGP2fR111aTZkbPWD5ZyJPC'), NOT RFC 4122 UUID format
- **NFR-002**: All backend models, schemas, and API responses MUST use `str` type for user_id fields to match Better Auth's format
- **NFR-003**: Database schema MUST store user_id as VARCHAR(255) to support string format
- **NFR-004**: Type safety MUST be consistent across all layers: SQLModel models, Pydantic schemas, and API responses

### Key Entities

- **User**: Authenticated user with ID (string from Better Auth), email, and session information
- **JWT Token**: Self-contained credential issued by Better Auth containing user ID (string), email, and expiration
- **Task**: User-owned task entity with ID (UUID), title, description, completion status, and user_id reference (string)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All API endpoints require valid JWT tokens; requests without tokens receive 401 Unauthorized
- **SC-002**: Authenticated users can only access and modify their own tasks; cross-user access attempts receive 403 Forbidden
- **SC-003**: JWT token verification succeeds within 50ms on average
- **SC-004**: 100% of API requests from the frontend automatically include valid JWT tokens in the Authorization header
- **SC-005**: User sessions persist across browser refreshes when JWT token is properly stored
- **SC-006**: Expired JWT tokens are rejected with 401 Unauthorized; users are prompted to re-authenticate
- **SC-007**: All 6 API endpoints (GET list, POST create, GET detail, PUT update, DELETE delete, PATCH toggle) function correctly with JWT authentication
- **SC-008**: User can complete a full task lifecycle (login → create task → update task → complete task → logout) in under 30 seconds

---

## Assumptions

- Better Auth is already integrated into the frontend project with basic authentication working
- FastAPI backend is already scaffolded and accessible to the frontend
- A shared secret (BETTER_AUTH_SECRET) can be configured in both frontend and backend environments
- JWT tokens will use EdDSA/Ed25519 algorithm for signing (per Better Auth documentation)
- User ID is the unique identifier for filtering and access control, provided by Better Auth as a string (~33 chars)
- The user_id in the URL is the source of truth for access control (backend verifies it matches JWT token)
- Better Auth generates string-based user IDs (NOT RFC 4122 UUIDs); backend must accept string type

---

## Out of Scope

- Multi-factor authentication (MFA)
- OAuth2 social login integration
- Role-based access control (RBAC) beyond user isolation
- Refresh token rotation
- Session revocation/logout mechanics (basic logout only)
- Rate limiting on API endpoints
- Detailed audit logging of user actions
