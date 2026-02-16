# Data Model: JWT Authentication Integration

**Feature**: JWT Authentication Integration (Phase 2.2)
**Date**: 2026-01-01

## Core Entities

### User (Existing, from Better Auth)

**Purpose**: Represents an authenticated user in the system

**Fields**:
- `id` (string, UUID): Primary key, unique identifier for user
- `email` (string): User's email address, unique, required
- `name` (string, optional): User's display name
- `createdAt` (timestamp): Account creation timestamp
- `updatedAt` (timestamp): Last update timestamp

**JWT Claims** (derived from User):
- `sub` (string): Subject claim, contains user ID
- `email` (string): User email
- `iat` (number): Issued at (Unix timestamp)
- `exp` (number): Expiration (Unix timestamp, default: 7 days)
- `iss` (string): Issuer (Better Auth base URL)
- `aud` (string): Audience (Better Auth base URL)

**Relationships**:
- One User → Many Tasks (via Task.user_id)

**Validation Rules**:
- Email must be valid RFC 5322 format
- Email must be unique across all users
- Name can contain alphanumeric and spaces, max 255 chars
- No fields nullable except name

---

### Task (Existing, User-Scoped)

**Purpose**: Represents a task owned by a specific user

**Fields**:
- `id` (string, UUID): Primary key
- `user_id` (string, UUID): Foreign key to User, required
- `title` (string): Task title, max 255 chars, required
- `description` (string, optional): Task details, max 2000 chars
- `completed` (boolean): Completion status, default: false
- `createdAt` (timestamp): Creation timestamp
- `updatedAt` (timestamp): Last modification timestamp

**Validation Rules**:
- user_id must match authenticated JWT user_id
- title cannot be empty or whitespace
- title length: 1-255 characters
- description length: 0-2000 characters (optional)
- completed must be boolean
- createdAt/updatedAt are auto-managed by system

**Relationships**:
- Many Tasks → One User (via user_id)

**Ownership Constraint** (Critical):
- Every Task record MUST have a user_id
- All queries MUST filter by user_id from JWT token
- No endpoint returns unfiltered tasks
- Cross-user access returns 403 Forbidden

**State Transitions**:
- New Task: `completed = false`
- Toggle Complete: `completed = !completed`
- Delete: Record removed from database
- Update: Fields modified, updatedAt updated

---

### JWT Token (Logical Entity, Not Persisted)

**Purpose**: Self-contained credential issued by Better Auth for API access

**Structure** (JWT Header + Payload + Signature):

**Header**:
```json
{
  "alg": "EdDSA",
  "typ": "JWT",
  "kid": "key-id"
}
```

**Payload**:
```json
{
  "sub": "user-id",
  "email": "user@example.com",
  "iat": 1704067200,
  "exp": 1711334400,
  "iss": "http://localhost:3000",
  "aud": "http://localhost:3000"
}
```

**Validation Rules**:
- Signature must be valid using JWKS public key
- `exp` must be >= current Unix timestamp
- `iss` must match expected issuer
- `aud` must match expected audience
- `sub` must be non-empty string (user ID)

**Lifecycle**:
1. **Issued**: On successful authentication via Better Auth
2. **Stored**: Client caches in localStorage
3. **Transmitted**: In Authorization: Bearer <token> header
4. **Verified**: Backend validates signature + claims
5. **Expired**: After 7 days, user prompted to re-authenticate

---

## Data Flow Diagrams

### User Login & Token Issuance

```
Client                Better Auth        Backend
  |                      |                  |
  +--sign in with email-->|                  |
  |                      |                  |
  |<--session + token----+                  |
  |                      |                  |
  +--store token in localStorage            |
  |                      |                  |
```

### API Request with JWT

```
Client                            FastAPI Backend
  |                                  |
  +--GET /api/{user_id}/tasks-------->|
  |  Authorization: Bearer <JWT>      |
  |                                  |
  |                           (verify JWT)
  |                           (extract user_id)
  |                           (query tasks by user_id)
  |                                  |
  |<---[User's tasks only]----------+
  |                                  |
```

### Token Expiration & Re-authentication

```
Client                Backend          Better Auth
  |                     |                  |
  +--expired token---->|                  |
  |                    |                  |
  |<--401 Unauthorized-+                  |
  |                     |                  |
  +--re-authenticate----------->|
  |                            |
  |<-----new session + token---+
  |                            |
  +--store new token           |
  |                            |
```

---

## Database Schema (SQL)

### User Table (Managed by Better Auth)

```sql
CREATE TABLE "user" (
  id TEXT PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  name TEXT,
  emailVerified TIMESTAMP,
  image TEXT,
  createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_user_email ON "user"(email);
```

### Task Table (Application-Managed)

```sql
CREATE TABLE "task" (
  id TEXT PRIMARY KEY,
  userId TEXT NOT NULL,
  title TEXT NOT NULL CHECK (length(title) > 0 AND length(title) <= 255),
  description TEXT CHECK (length(description) <= 2000),
  completed BOOLEAN NOT NULL DEFAULT FALSE,
  createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (userId) REFERENCES "user"(id) ON DELETE CASCADE
);

CREATE INDEX idx_task_userId ON "task"(userId);
CREATE INDEX idx_task_completed ON "task"(completed);
CREATE INDEX idx_task_userId_createdAt ON "task"(userId, createdAt DESC);
```

### JWKS Table (Managed by Better Auth JWT Plugin)

```sql
CREATE TABLE "jwks" (
  id TEXT PRIMARY KEY,
  publicKey TEXT NOT NULL,
  privateKey TEXT NOT NULL,
  createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  expiresAt TIMESTAMP
);

CREATE INDEX idx_jwks_createdAt ON "jwks"(createdAt DESC);
```

---

## Data Validation Rules

### User Entity
- Email: Required, unique, valid RFC 5322 format
- Name: Optional, max 255 chars, alphanumeric + spaces
- Email verified: Boolean flag, managed by Better Auth
- Created/Updated: Auto-managed timestamps

### Task Entity
- Title: Required, non-empty, 1-255 chars
- Description: Optional, max 2000 chars
- Completed: Boolean, default false
- user_id: Required, must reference existing user
- User ownership: All queries filtered by authenticated user_id

### JWT Token
- Signature: Valid EdDSA signature using JWKS public key
- Expiration: Must not be expired
- Claims: sub, email, iat, exp, iss, aud all present and valid
- Issuer/Audience: Match configured Better Auth base URL

---

## Constraints & Invariants

1. **User Isolation**: Every Task must belong to exactly one User. All queries must include `WHERE user_id = ?`
2. **No Orphaned Tasks**: Foreign key constraint ensures tasks cannot exist without a user
3. **Token Expiration**: Tokens expire after 7 days; no refresh tokens in Phase 2.2
4. **No Shared Secrets**: Backend never needs a shared secret; verification done via JWKS
5. **Immutable User ID**: User ID in JWT claim is immutable; cannot change after issuance
6. **Single Token Per Session**: Each session has one active JWT (logout = discard token)

---

## Future Considerations (Out of Scope for Phase 2.2)

- **Token Revocation**: Implement blacklist for invalidated tokens
- **Refresh Tokens**: Issue short-lived access + long-lived refresh tokens
- **Key Rotation**: Automated rotation of signing keys (Better Auth handles this)
- **Audit Logging**: Track all authentication and authorization events
- **Rate Limiting**: Throttle login attempts and API requests per user
- **Task Tags/Categories**: Extend Task entity with organizational features
- **Task Collaboration**: Share tasks between users (requires role-based access)
