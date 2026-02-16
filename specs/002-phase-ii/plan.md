# Implementation Plan: Phase II - Full-Stack Todo Application with Authentication

**Branch**: `phase-2` | **Date**: 2025-12-29 | **Spec**: [specs/002-phase-ii/spec.md](./spec.md)

**Input**: Feature specification from `/specs/002-phase-ii/spec.md`

---

## Summary

Convert the CLI Todo application into a production-ready full-stack web application using a monorepo architecture. The implementation will create a Next.js 16+ frontend with React components, a FastAPI backend with JWT authentication, PostgreSQL persistence via SQLModel ORM, and Docker Compose orchestration for local development. All user data will be scoped by user_id derived from JWT tokens, enforcing strict multi-user isolation at the database query level.

**Technical Approach**:
- Monorepo structure separating `/backend` (FastAPI + Python 3.13) and `/frontend` (Next.js 16+ TypeScript)
- JWT middleware in FastAPI to validate shared-secret tokens and extract user_id
- API client in `/lib/api.ts` that automatically attaches JWT to every HTTP request
- SQLModel with PostgreSQL for type-safe, ORM-based database access
- User data isolation enforced at query level (WHERE user_id = <authenticated_user_id>)
- Docker Compose for local development with PostgreSQL, Backend, and Frontend services

---

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5+ (frontend)

**Primary Dependencies**:
- Backend: FastAPI, SQLModel, better-auth (JWT plugin), httpx (async HTTP client)
- Frontend: Next.js 16+, React 18+, TypeScript, better-auth (JavaScript client)

**Storage**: PostgreSQL via Neon Serverless (Better Auth managed schema); local Docker for development parity

**Testing**:
- Backend: pytest with unit, integration, and acceptance tests
- Frontend: Jest/Playwright for component and E2E tests

**Target Platform**: Web application (Linux backend, any browser frontend)

**Project Type**: Web application (monorepo with separate backend and frontend)

**Performance Goals**:
- API response latency: < 200ms (p95) for all endpoints
- Frontend First Contentful Paint (FCP): < 2 seconds
- Database query time: < 100ms (p95)

**Constraints**:
- JWT tokens expire after 7 days
- Password minimum length: 8 characters
- Title field: max 500 characters
- Description field: max 2000 characters
- User data strictly isolated (no cross-user access)
- 401 Unauthorized for missing/invalid JWT tokens
- 403 Forbidden for ownership violations (wrong user accessing another's todo)

**Scale/Scope**:
- MVP: Single-user authentication with multi-user support
- Expected scale: 100-10,000 users in initial phase
- 7 user stories, 9 API endpoints, 2 main database entities (User, Todo)
- Responsive design: mobile (320px), tablet (768px), desktop (1024px+)

---

## Constitution Check

✅ **Phase II Constitution (v2.0.0) Compliance**

| Principle | Status | Details |
|-----------|--------|---------|
| Full-Stack Web App with Separation | ✅ | Frontend (Next.js) / Backend (FastAPI) / DB (PostgreSQL) separation |
| User-Scoped Data with JWT | ✅ | All endpoints require JWT; all responses filtered by user_id |
| Clean Code Principles | ✅ | Small focused functions, clear naming, testable in isolation |
| Task-Driven Implementation | ✅ | All code mapped to Task IDs in tasks.md (phase2-XXY-feature-name) |
| Performance Over Brevity | ✅ | Indexes on user_id, created_at; async endpoints; efficient queries |
| No Manual Code Writing | ✅ | Templates and scaffolding used where possible |
| MCP Integration (Required) | ✅ | Context7 MCP for debugging; Better Auth MCP for auth integration |

**Gate Status**: ✅ PASS - All constitution principles verified before Phase 0 research

---

## Project Structure

### Documentation (this feature)

```text
specs/002-phase-ii/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # User stories, functional requirements, API contract
├── data-model.md        # Database schema, SQLModel code, migrations
├── api-contract.md      # Detailed REST API specification
├── acceptance-criteria.md # 14 criteria with test cases and verification steps
├── README.md            # Architecture overview, implementation roadmap
└── INDEX.md             # Quick reference guide
```

### Source Code (repository root)

```text
Evo-TODO/
├── backend/                    # FastAPI + Python 3.13 application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app entry point with route registration
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py        # SQLModel User entity
│   │   │   ├── todo.py        # SQLModel Todo entity
│   │   │   └── database.py    # Database engine and session management
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py        # FastAPI dependencies (get_current_user)
│   │   │   ├── auth.py        # Authentication endpoints (signup, signin, logout)
│   │   │   └── todos.py       # Todo CRUD endpoints with user scoping
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py      # Settings, environment variables, JWT config
│   │   │   └── security.py    # JWT encode/decode, password hashing functions
│   │   └── schemas/
│   │       ├── __init__.py
│   │       ├── user.py        # Pydantic schemas for User (Create, Response)
│   │       └── todo.py        # Pydantic schemas for Todo (Create, Update, Toggle)
│   ├── tests/
│   │   ├── unit/
│   │   │   ├── test_auth.py   # Auth endpoint tests
│   │   │   └── test_todos.py  # Todo endpoint tests with isolation verification
│   │   └── integration/
│   │       └── test_user_flows.py # Complete user journey tests
│   ├── Dockerfile             # Docker image for FastAPI backend
│   ├── requirements.txt        # Python dependencies
│   ├── pyproject.toml         # Project metadata and development config
│   └── .env.example           # Backend environment variables template
│
├── frontend/                   # Next.js 16+ TypeScript application
│   ├── app/
│   │   ├── layout.tsx         # Root layout with AuthProvider wrapper
│   │   ├── page.tsx           # Landing/home page
│   │   ├── globals.css        # Global styles and Tailwind configuration
│   │   ├── (auth)/            # Route group for unauthenticated pages
│   │   │   ├── signin/
│   │   │   │   └── page.tsx   # Signin form with email/password validation
│   │   │   └── signup/
│   │   │       └── page.tsx   # Signup form with registration flow
│   │   └── (dashboard)/       # Route group for authenticated pages
│   │       ├── layout.tsx     # Dashboard layout with nav bar and user info
│   │       ├── page.tsx       # Todo list page with CRUD operations
│   │       └── todos/
│   │           ├── new/
│   │           │   └── page.tsx  # Create new todo page
│   │           └── [id]/
│   │               ├── page.tsx  # View specific todo
│   │               └── edit/
│   │                   └── page.tsx  # Edit todo page
│   ├── components/
│   │   ├── ui/                # Reusable UI components (Button, Form, Card, etc.)
│   │   ├── auth/              # Auth-specific components (LoginForm, SignupForm)
│   │   └── todos/             # Todo components (TodoList, TodoItem, TodoForm)
│   ├── lib/
│   │   ├── api.ts             # API client class with JWT auto-attachment
│   │   ├── auth.ts            # Auth utility functions
│   │   └── types.ts           # Shared TypeScript types
│   ├── hooks/
│   │   ├── useAuth.ts         # Auth context hook and provider
│   │   └── useTodos.ts        # Todo state management hook
│   ├── package.json           # Node.js dependencies and scripts
│   ├── tsconfig.json          # TypeScript configuration
│   ├── next.config.js         # Next.js configuration
│   ├── Dockerfile             # Docker image for Next.js frontend
│   ├── .env.local             # Frontend environment variables
│   └── .env.example           # Frontend environment variables template
│
├── docker-compose.yml         # Docker Compose configuration for local dev
├── .env.example              # Root environment variables template
├── .gitignore                # Git ignore rules
├── README.md                 # Monorepo documentation and setup guide
└── Makefile                  # Optional: convenience commands (docker up, tests)
```

**Structure Decision**: **Web application monorepo** with separate backend (FastAPI) and frontend (Next.js) directories. This separation enables:
- Independent deployment and scaling
- Clear dependency boundaries
- Separate package management (Python uv + npm/yarn)
- Docker multi-service orchestration
- Team collaboration with backend and frontend specialists

---

## Implementation Phases

### Phase 2.1: Monorepo Infrastructure Setup (Days 1-2)

**Deliverables**:
- Backend directory structure with FastAPI scaffolding
- Frontend directory structure with Next.js 16+ App Router
- Docker Compose configuration with PostgreSQL, Backend, Frontend services
- Environment variable templates (.env.example files)

**Critical Files**:
- `backend/app/main.py` - FastAPI application instance
- `backend/app/core/config.py` - Settings and configuration
- `frontend/lib/api.ts` - API client foundation
- `docker-compose.yml` - Service orchestration

**Success Criteria**:
- Docker Compose starts all services without errors
- FastAPI backend health check endpoint responds on :8000
- Next.js frontend builds and serves on :3000
- PostgreSQL database initializes with health checks

---

### Phase 2.2: Database Schema & ORM Models (Days 2-3)

**Deliverables**:
- SQLModel User entity with fields: id, email, password_hash, name, is_active, timestamps
- SQLModel Todo entity with fields: id, user_id (FK), title, description, is_complete, timestamps
- Pydantic request/response schemas for all entities
- Database initialization and migration setup

**Critical Files**:
- `backend/app/models/user.py` - User SQLModel
- `backend/app/models/todo.py` - Todo SQLModel with FK to User
- `backend/app/models/database.py` - Database engine and session
- `backend/app/schemas/user.py` - User schemas
- `backend/app/schemas/todo.py` - Todo schemas

**Success Criteria**:
- Database tables created via SQLModel.metadata.create_all()
- Foreign key relationship enforced (todos.user_id → users.id)
- Indexes on user_id and (user_id, created_at) created
- Composite index improves todo list query performance

---

### Phase 2.3: Better Auth Integration with JWT (Days 3-4)

**Deliverables**:
- Better Auth Python client installed and configured
- Better Auth's managed user/session schema (auto-created in Neon)
- FastAPI JWT validation middleware that extracts user_id from Better Auth tokens
- API dependency for `get_current_user()` that decodes Better Auth JWT and returns authenticated user
- Frontend Better Auth JavaScript client configured for signup/signin/logout flows

**Critical Files**:
- `backend/app/core/auth.py` - Better Auth JWT verification and user extraction (replaces custom security.py)
- `backend/app/api/deps.py` - FastAPI dependencies using Better Auth verification
- `backend/app/api/auth.py` - Proxy endpoints that delegate to Better Auth (via HTTP client)
- `frontend/lib/auth.ts` - Better Auth JavaScript client configuration
- `frontend/hooks/useAuth.ts` - Auth context using Better Auth client
- `.env.example` - Better Auth API key and Neon connection string

**Success Criteria**:
- Better Auth Python client successfully authenticates with Better Auth service
- Signup via frontend Better Auth client creates user in Neon (Better Auth schema)
- JWT token issued by Better Auth contains user_id in `sub` claim
- FastAPI `/api/todos` endpoints extract user_id from Better Auth JWT claims
- Missing JWT returns 401 Unauthorized
- Invalid/expired JWT returns 401 Unauthorized
- All user data isolated by user_id from JWT claims (zero cross-user access)

---

### Phase 2.4: Todo CRUD API with User Scoping (Days 4-5)

**Deliverables**:
- 6 CRUD endpoints: GET list, GET one, POST create, PUT update, PATCH toggle, DELETE
- User data isolation via WHERE user_id = <authenticated_user_id> in all queries
- Ownership validation: 403 Forbidden for non-owner access
- Input validation: title (required, max 500), description (optional, max 2000)
- Comprehensive error handling with proper HTTP status codes

**Critical Files**:
- `backend/app/api/todos.py` - Todo endpoints with user scoping
- Unit tests for all endpoints
- Integration tests for user isolation

**Success Criteria**:
- All 6 endpoints implemented and tested
- User A cannot view User B's todos (403 or query filtering)
- User A cannot modify User B's todos (403)
- Empty title returns 400 Bad Request
- Title > 500 chars returns 400 Bad Request
- Description > 2000 chars returns 400 Bad Request
- Non-existent todo returns 404 Not Found
- All endpoints require valid JWT (401 if missing)

---

### Phase 2.5: Neon PostgreSQL Migration & Better Auth Schema (Days 4-5)

**Deliverables**:
- Neon PostgreSQL project created and connection string configured in `.env`
- Better Auth migrations run on Neon (users, sessions, accounts tables auto-created)
- SQLModel Todo model migrated to use Neon connection
- Database health checks updated for Neon serverless (connection pooling configured)
- Local Docker PostgreSQL deprecated (kept for offline dev if needed, but Neon is primary)

**Critical Files**:
- `.env` - Update `DATABASE_URL` to Neon connection string
- `backend/app/models/database.py` - Update connection pooling for serverless (enable connection timeout)
- `backend/app/models/todo.py` - Ensure foreign key references Better Auth's user schema
- Neon Console - Verify users, sessions, accounts tables exist

**Success Criteria**:
- Neon PostgreSQL connection successful from FastAPI backend
- Better Auth tables (users, sessions, accounts, verifications) exist in Neon
- Todo table foreign key correctly references users.id from Better Auth schema
- No data loss during migration (fresh dev environment, so minimal concerns)
- Connection pooling works under load (p95 query latency < 100ms)
- Neon serverless scales to zero successfully

---

### Phase 2.6: Frontend API Integration & Components (Days 5-7)

**Deliverables**:
- API client in `/lib/api.ts` with methods for all Todo endpoints (CRUD)
- JWT token from Better Auth automatically attached to every request (Authorization header)
- Authentication context hook (`useAuth`) wrapping Better Auth JavaScript client
- Signin/Signup pages using Better Auth form components (or custom forms calling Better Auth API)
- Todo dashboard with list, create, edit, delete, toggle operations
- Responsive design (mobile, tablet, desktop)

**Critical Files**:
- `frontend/lib/api.ts` - API client with auto JWT attachment from Better Auth token
- `frontend/lib/auth.ts` - Better Auth client configuration and utilities
- `frontend/hooks/useAuth.ts` - Auth context wrapping Better Auth (signup, signin, logout, current user)
- `frontend/app/(auth)/signin/page.tsx` - Signin page using Better Auth client
- `frontend/app/(auth)/signup/page.tsx` - Signup page using Better Auth client
- `frontend/app/(dashboard)/page.tsx` - Todo list page
- `frontend/app/(dashboard)/layout.tsx` - Protected dashboard layout with Better Auth check

**Success Criteria**:
- User can signup with email, password via Better Auth client (creates user in Neon)
- User can signin with email and password via Better Auth client
- Signin redirects to dashboard on success with JWT token from Better Auth
- Invalid credentials show error message from Better Auth API
- Todos display in list with title, description, status (filtered by user_id from Better Auth JWT)
- User can create new todo with required title
- User can update todo title/description
- User can toggle completion status (visual strikethrough)
- User can delete todo with confirmation
- All form inputs validated on client and server
- Responsive layout on 320px, 768px, 1024px+ viewports
- Logout removes Better Auth session and redirects to signin

---

## Task Dependencies & Sequencing

```
Phase 2.1: Infrastructure
├── M1: Backend scaffolding ─────────┬──────────→ Phase 2.2: Database
├── M2: Frontend scaffolding ────────┼──────────→ Phase 2.6: Frontend
└── M3: Docker Compose ─────────────┐│

Phase 2.2: Database Schema ────────→ Phase 2.3: Better Auth Integration
├── D1: SQLModel models ───────┐
└── D2: Pydantic schemas ──────┴──→ A1: Better Auth JWT validation
                                     └──→ A2: Better Auth proxy endpoints ──→ Phase 2.4: CRUD
Phase 2.4: Todo CRUD ──────────────→ Phase 2.5: Neon Migration
├── T1: Todo endpoints ────────────→ DB1: Create Neon project
└── T2: User scoping ─────────────┐│→ DB2: Run Better Auth migrations
                                   │
Phase 2.5: Neon Migration ────────→ Phase 2.6: Frontend
├── DB1: Neon setup ───────────────┐
├── DB2: Better Auth schema ───────┼──→ F1: API client (lib/api.ts)
└── DB3: Connection pooling ───────┴──→ F2: Better Auth context (useAuth)
                                        └──→ F3: Frontend components

Phase 2.6: Frontend Components
├── F1: API client (lib/api.ts) ──→ F2: useAuth hook (Better Auth)
├── F2: Auth context ────────────→ F3: Auth pages (signin/signup)
└── F3: Dashboard layout ────────→ F4: Todo components
```

**Critical Path**: M1 → D1 → A1 → A2 → T1 → DB1 → DB2 → F1 → F2 → F3/F4

**Parallel Work**:
- M1 (backend) and M2 (frontend) can start simultaneously
- D1 and D2 (database) can start after M1
- M3 (Docker) can start after M1 and M2
- Phase 2.5 (Neon) can start once Phase 2.4 (Todo CRUD) is complete
- F1 (API client) can start after M2 (frontend) and Phase 2.5 (Neon) ready

---

## Estimated Effort & Timeline

| Phase | Tasks | Files | Days | Effort |
|-------|-------|-------|------|--------|
| 2.1 | 3 | 8 | 2 | Low |
| 2.2 | 2 | 8 | 1 | Low |
| 2.3 | 3 | 6 | 2 | Medium (Better Auth integration) |
| 2.4 | 1 | 3 | 2 | Medium |
| 2.5 | 3 | 4 | 1 | Low (Neon migration + Better Auth schema) |
| 2.6 | 4 | 12 | 3 | High (Frontend with Better Auth) |
| Testing & Polish | - | - | 1 | Medium |
| **Total** | **16** | **~55** | **~12** | **Medium-High** |

**Note**: Phase 2.5 (Neon Migration) is shorter because Better Auth auto-manages the schema. Phase 2.3 (Better Auth Integration) has higher effort due to service integration but lower than custom JWT implementation.

---

## Key Architectural Decisions

### Decision 1: Monorepo Structure
**Choice**: Separate `/backend` and `/frontend` directories in single repo
**Rationale**:
- Clear separation of concerns (Python backend, TypeScript frontend)
- Easier independent deployment and scaling
- Single git history for feature traceability
- Docker Compose orchestration in single file

**Alternatives Rejected**:
- Separate repositories: Harder to maintain version alignment
- Nested structure: Would complicate build and deployment

### Decision 2: Better Auth with JWT Plugin
**Choice**: Better Auth service with JWT token plugin for FastAPI integration
**Rationale**:
- Handles all authentication complexity: signup, signin, session management, token rotation
- JWT tokens issued by Better Auth service (not custom-signed)
- Automatic user/session schema management in Neon PostgreSQL
- Scales to OAuth 2.0, social login in Phase III without rework
- Better Auth Python client + JavaScript client ensure frontend/backend alignment
- Stateless JWT validation at FastAPI boundary; no session storage required

**Alternatives Rejected**:
- Custom JWT/bcrypt: High security risk, manual token management, no built-in OAuth path
- Sessions + HTTPOnly cookies: Stateful, incompatible with Phase III stateless chat API
- Firebase/Auth0: Closed ecosystem, lock-in risk for hackathon

### Decision 3: JWT Token Storage (via Better Auth)
**Choice**: JWT stored in-memory by Better Auth client; no manual localStorage/cookies
**Rationale**:
- Better Auth JavaScript client handles token storage securely
- Reduces XSS attack surface (tokens not in localStorage)
- Automatic token refresh via Better Auth client
- Frontend `useAuth` hook provides clean API for token management

**Trade-off**:
- Must use Better Auth client (not custom auth logic)
- Token lost on page refresh (but Better Auth session refreshes automatically)

### Decision 4: Database: Neon Serverless PostgreSQL
**Choice**: Migrate entirely to Neon; use Better Auth's managed schema
**Rationale**:
- Spec requirement (Phase II mandate)
- Serverless scales to zero (cost-efficient for MVP)
- Better Auth auto-creates users, sessions, accounts tables
- No manual database maintenance needed
- Connection pooling for stateless FastAPI

**Alternatives Rejected**:
- Local Docker Postgres: Development-only, not production-ready, manual schema management
- Other managed databases: Lock-in risk, more expensive

### Decision 5: User Data Isolation at Query Level
**Choice**: Every query filters by user_id extracted from Better Auth JWT claims
**Rationale**:
- Defense in depth: multiple layers of protection
- Prevents accidental data leakage via bug in business logic
- Enforced at database layer via WHERE clause (cannot be bypassed)
- Better Auth JWT always includes user_id; automatic isolation

**Example**:
```python
# Extract user_id from Better Auth JWT (in deps.py)
current_user_id = token_payload.get("sub")  # User UUID from Better Auth

# All queries filter by this user
todos = db.query(Todo).filter(Todo.user_id == current_user_id).all()
```

### Decision 6: 403 Forbidden vs. 404 Not Found for Ownership Violations
**Choice**: Return 403 for ownership violations (not 404)
**Rationale**:
- Security through obscurity: doesn't reveal todo existence
- Consistent error handling
- Standard REST convention (though query filtering makes 404 unlikely)

**Alternative Rejected**:
- 404: Would leak information about which todos exist

---

## Security Implementation Checklist

- [x] **Better Auth handles**: JWT tokens, password hashing, session management, token rotation
- [x] JWT tokens issued by Better Auth service (not custom-signed)
- [x] Passwords securely managed by Better Auth (no custom bcrypt needed in backend)
- [x] All inputs validated (email, password, title, description at API boundary)
- [x] SQL injection prevention (SQLModel ORM with parameterized queries)
- [x] XSS prevention (HTML escaping in frontend, no direct DOM manipulation)
- [x] CSRF protection (JWT in Authorization header; Better Auth handles cookie security)
- [x] Data isolation (WHERE user_id = <extracted_from_jwt> in all Todo queries)
- [x] Proper HTTP status codes (401, 403, 404, 400)
- [x] No sensitive info in error messages (defer to Better Auth error handling)
- [x] HTTPS in production (required for Better Auth service communication)
- [x] Better Auth JWT validation at FastAPI boundary (middleware in Phase 2.3)

---

## Testing Strategy

### Unit Tests (Backend)

**File**: `backend/tests/unit/test_auth.py`
```python
def test_signup_creates_user_with_bcrypt_password():
def test_signup_rejects_duplicate_email():
def test_signup_validates_password_length():
def test_signin_returns_valid_jwt_token():
def test_signin_rejects_invalid_password():
def test_signin_rejects_nonexistent_email():
def test_logout_endpoint_returns_success():
```

**File**: `backend/tests/unit/test_todos.py`
```python
def test_create_todo_requires_title():
def test_create_todo_assigns_user_id_from_jwt():
def test_list_todos_returns_only_authenticated_user_todos():
def test_get_todo_returns_404_if_not_found():
def test_get_todo_returns_403_if_not_owner():
def test_update_todo_requires_ownership():
def test_toggle_todo_updates_is_complete():
def test_delete_todo_removes_from_database():
```

### Integration Tests (Backend)

**File**: `backend/tests/integration/test_user_flows.py`
```python
def test_complete_user_signup_signin_todo_flow():
    # 1. Signup → 2. Signin → 3. Create todo → 4. List todos → 5. Update → 6. Toggle → 7. Delete

def test_multi_user_data_isolation():
    # User A creates 3 todos, User B creates 2 todos
    # Verify each sees only their own todos

def test_token_expiration_blocks_access():
    # Create token, manually expire, verify 401
```

### E2E Tests (Frontend)

**File**: `frontend/tests/e2e/todo.spec.ts` (Playwright)
```typescript
test('user can sign up and create a todo', async ({ page }) => {
  // Navigate to signup, fill form, submit, verify redirect to dashboard

test('user cannot access other users todos', async ({ page }) => {
  // User A creates todo, logout
  // User B signs in, verify A's todo not visible
```

### Acceptance Criteria Tests
- All 14 criteria from `specs/002-phase-ii/acceptance-criteria.md` mapped to test cases
- Curl command examples provided for manual API testing
- Integration scenarios cover complete user journeys

---

## Environment Variables

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql://evo_todo_user:evo_todo_password@localhost:5432/evo_todo

# JWT
JWT_SECRET_KEY=<256-bit-secret-key-generated-via-openssl>
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=168

# CORS
CORS_ORIGINS=http://localhost:3000

# Server
ENVIRONMENT=development
DEBUG=True
```

### Frontend (.env.local)

```bash
# API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional: Better Auth configuration (Phase III)
# BETTER_AUTH_SECRET=...
# BETTER_AUTH_URL=...
```

### Docker Compose (.env)

```bash
JWT_SECRET_KEY=your-256-bit-secret-key
POSTGRES_PASSWORD=evo_todo_password
POSTGRES_USER=evo_todo_user
POSTGRES_DB=evo_todo
```

---

## Success Metrics

### Functional Completeness
- ✅ All 7 user stories implemented and acceptance criteria passed
- ✅ All 9 API endpoints functional (3 auth + 6 CRUD)
- ✅ User authentication with JWT and secure password storage
- ✅ Multi-user support with strict data isolation
- ✅ Responsive UI (mobile, tablet, desktop)
- ✅ Database schema with FK relationships and indexes

### Quality Standards
- ✅ 100% of critical paths covered by unit tests
- ✅ 100% of user flows covered by integration tests
- ✅ All error cases handled with proper status codes
- ✅ Code follows clean code principles (small functions, clear naming)
- ✅ No code without task ID mapping (phase2-XXY-*)

### Performance Requirements
- ✅ API response time < 200ms (p95) for all endpoints
- ✅ Frontend FCP < 2 seconds
- ✅ Database query time < 100ms (p95) with indexes
- ✅ No N+1 query problems

### Security Requirements
- ✅ JWT tokens expire after 7 days
- ✅ Passwords hashed with bcrypt (12 rounds)
- ✅ All inputs validated (email, password, title, description)
- ✅ SQL injection prevention (parameterized queries via ORM)
- ✅ XSS prevention (HTML escaping)
- ✅ Data isolation enforced at query level

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| JWT secret exposure | Low | High | Store in .env, use secrets manager in production |
| Database connection issues | Medium | Medium | Use connection pooling, health checks in Docker Compose |
| CORS misconfiguration | Medium | Low | Explicitly configure allowed origins, test with curl |
| Performance at scale | Low | Medium | Add indexes, consider caching in Phase III |
| Token expiration UX | Medium | Low | Implement refresh token endpoint in Phase III |
| Password reset needed | Low | Low | Out of scope for MVP, add in Phase III |

---

## Definition of Done

**For Plan Approval**:
- [x] All 10 sections of plan template completed
- [x] Technical context defined (languages, dependencies, constraints)
- [x] Constitution compliance verified
- [x] Project structure documented with real file paths
- [x] Implementation phases sequenced with dependencies
- [x] Critical files identified for each phase
- [x] Success criteria specified and measurable
- [x] Architectural decisions documented with rationale
- [x] Testing strategy defined (unit, integration, E2E)
- [x] Risks identified with mitigations

**For Phase 2.1 Completion**:
- [ ] Backend scaffolding created (FastAPI app, config, main.py)
- [ ] Frontend scaffolding created (Next.js app, package.json)
- [ ] Docker Compose configuration complete
- [ ] All services start without errors
- [ ] Environment templates created (.env.example files)

**For Phase 2.2 Completion**:
- [ ] SQLModel User and Todo entities created
- [ ] Pydantic schemas for all endpoints created
- [ ] Database tables created and indexes applied
- [ ] Foreign key relationship working (ON DELETE CASCADE)
- [ ] Unit tests for models pass

**For Phase 2.3 Completion**:
- [ ] JWT token creation, validation, expiration working
- [ ] Bcrypt password hashing implemented
- [ ] FastAPI dependencies for authentication created
- [ ] Signup endpoint: validates email, password, creates user
- [ ] Signin endpoint: authenticates, returns JWT token
- [ ] Logout endpoint: invalidates session
- [ ] All auth unit tests pass

**For Phase 2.4 Completion**:
- [ ] All 6 CRUD endpoints implemented
- [ ] User scoping enforced (WHERE user_id = <user_id>)
- [ ] Ownership validation returns 403 for non-owner
- [ ] Input validation: title (required, max 500), description (max 2000)
- [ ] All endpoints require valid JWT (401 if missing)
- [ ] All CRUD unit tests pass
- [ ] Integration tests verify user isolation

**For Phase 2.5 Completion**:
- [ ] API client in /lib/api.ts with auto JWT attachment
- [ ] useAuth hook and AuthProvider context created
- [ ] Signin/Signup pages with form validation
- [ ] Todo dashboard with CRUD operations
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] All E2E tests pass

**For Phase 2 Release**:
- [ ] All 14 acceptance criteria verified
- [ ] 100% test coverage for critical paths
- [ ] Code reviewed against constitution
- [ ] All commits reference task IDs (phase2-XXY-*)
- [ ] Documentation complete (README, API docs, setup guide)
- [ ] Git history clean and descriptive

---

## References

- **Specification**: [specs/002-phase-ii/spec.md](./spec.md) - User stories and requirements
- **Data Model**: [specs/002-phase-ii/data-model.md](./data-model.md) - Database schema and SQLModel code
- **API Contract**: [specs/002-phase-ii/api-contract.md](./api-contract.md) - REST API specification
- **Acceptance Criteria**: [specs/002-phase-ii/acceptance-criteria.md](./acceptance-criteria.md) - Testing checklist
- **Constitution**: [.specify/memory/constitution.md](../../.specify/memory/constitution.md) - Phase II principles
- **Implementation Plan**: [/home/abdullah/.claude/plans/merry-munching-cascade.md](/home/abdullah/.claude/plans/merry-munching-cascade.md) - Detailed architecture plan
- **CLAUDE.md**: [./CLAUDE.md](../../CLAUDE.md) - Claude Code development guidelines

---

## Plan Approval & Handoff

**Plan Version**: 1.0.0
**Created**: 2025-12-29
**Status**: ✅ Ready for Implementation

**Next Steps**:
1. Create branch `phase-2` from `001-cli-todo`
2. Execute Phase 2.1: Monorepo Setup (backend + frontend scaffolding)
3. Execute Phase 2.2: Database Schema (SQLModel + migrations)
4. Continue through Phases 2.3-2.5 following task dependencies
5. Run full test suite and verification against acceptance criteria
6. Create PR with all changes referenced to phase2-XXY-* task IDs

**Questions?** Refer to specification documents or architectural decision section above.
