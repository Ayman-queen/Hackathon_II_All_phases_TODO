# Phase II Specification - Full-Stack Todo Application with Authentication

**Status**: Active Development
**Branch**: `phase-2`
**Created**: 2025-12-29
**Version**: 1.0.0

---

## Overview

Phase II transforms the CLI Todo application into a production-ready, full-stack web application with the following stack:

- **Frontend**: Next.js 16+ (App Router) - Responsive React interface
- **Backend**: FastAPI - High-performance async Python REST API
- **Database**: Neon PostgreSQL - Scalable serverless relational database
- **ORM**: SQLModel - Type-safe, Pydantic-integrated database abstraction
- **Authentication**: Better Auth with JWT - Secure user identity management

### Key Features

1. **User Authentication**: Signup/Signin with email and password via Better Auth
2. **Task CRUD Operations**: Full REST API support for creating, reading, updating, and deleting todos
3. **User Data Isolation**: Multi-user system with strict data scoping by user_id
4. **JWT Authorization**: All API endpoints require valid JWT tokens; 401 for unauthorized access
5. **Responsive UI**: Mobile-first design supporting all device sizes
6. **Persistent Storage**: PostgreSQL backend ensures data durability

---

## Specification Documents

### 1. **spec.md** - Core Feature Specification
**Purpose**: Defines what the application does from user perspective
**Contents**:
- 7 user stories (signup, signin, view, create, update, toggle, delete) with priorities
- Functional requirements (FR-001 through FR-017)
- Data model overview (User, Todo, Session entities)
- API contract overview
- Success criteria (10 measurable outcomes)

**Key Sections**:
- User Scenarios & Testing (7 stories with acceptance scenarios)
- Edge Cases (invalid tokens, non-existent todos, SQL injection, race conditions)
- Requirements (functional, entity definitions)
- Success Criteria (measurable outcomes)

**When to Read**: Start here to understand the application scope and requirements.

---

### 2. **data-model.md** - Database Schema & Design
**Purpose**: Details the database structure, relationships, and query patterns
**Contents**:
- Entity Relationship Diagram (ERD)
- Detailed entity definitions (User, Todo, Session)
- SQLModel schema in Python
- Database setup instructions
- Indexes and constraints
- Query patterns for common operations
- Scalability considerations

**Key Sections**:
- User Entity: id, email (unique), password_hash, name, timestamps
- Todo Entity: id, user_id (FK), title, description, is_complete, timestamps
- Session Entity: Better Auth managed; token with 7-day expiration

**When to Read**: Reference this when implementing database models and migrations.

---

### 3. **api-contract.md** - REST API Specification
**Purpose**: Complete API documentation with request/response examples
**Contents**:
- Authentication endpoints (signup, signin, logout)
- Todo CRUD endpoints (GET, POST, PUT, PATCH, DELETE)
- Request/response format for each endpoint
- Query parameters and path parameters
- HTTP status codes and error handling
- JWT token format and claims
- CORS configuration

**Key Sections**:
- POST /auth/signup: Create user account
- POST /auth/signin: Authenticate and get JWT token
- POST /auth/logout: Invalidate session
- GET /api/todos: List user's todos
- POST /api/todos: Create new todo
- GET /api/todos/{id}: Get specific todo
- PUT /api/todos/{id}: Update todo
- PATCH /api/todos/{id}: Toggle completion
- DELETE /api/todos/{id}: Delete todo

**When to Read**: Use as authoritative guide when implementing API endpoints.

---

### 4. **acceptance-criteria.md** - Verification & Testing
**Purpose**: Comprehensive checklist of acceptance criteria with verification steps
**Contents**:
- 14 core acceptance criteria with test cases
- Curl command examples for each test
- Integration test scenarios
- Definition of Done checklist

**Key Criteria**:
- AC-001: JWT token requirement for all protected endpoints
- AC-002: User data isolation (filtering by user_id)
- AC-003: Signup validation (email uniqueness, password strength)
- AC-004: Signin validation (credential checking)
- AC-005: Logout (session invalidation)
- AC-006-010: CRUD operations with ownership validation
- AC-011: Responsive frontend design
- AC-012: Input validation and security
- AC-013: Error handling
- AC-014: Performance requirements

**When to Read**: Use during testing phase to verify all features work correctly.

---

## Architecture Overview

### Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Next.js 16+)                   │
│  - Server Components for data fetching                       │
│  - Client Components for interactivity                       │
│  - JWT stored in httpOnly cookie                             │
│  - Responsive design (mobile, tablet, desktop)               │
└────────────────────────┬────────────────────────────────────┘
                         │
                  HTTPS / REST API
                         │
┌────────────────────────┴────────────────────────────────────┐
│                Backend (FastAPI)                            │
│  - Async Python API endpoints                               │
│  - JWT middleware for authentication                         │
│  - User-scoped data filters                                 │
│  - Input validation (Pydantic)                              │
│  - Better Auth integration                                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                  SQL / ORM (SQLModel)
                         │
┌────────────────────────┴────────────────────────────────────┐
│              Database (Neon PostgreSQL)                      │
│  - users table: id, email, password_hash, name              │
│  - todos table: id, user_id (FK), title, desc, is_complete  │
│  - sessions table: Better Auth managed                      │
│  - Indexes on user_id, email, created_at                    │
└─────────────────────────────────────────────────────────────┘
```

### Authentication Flow

```
1. User signs up/in with email + password
   ↓
2. Backend validates credentials (Better Auth)
   ↓
3. Backend generates JWT token (sub=user_id, exp=7 days)
   ↓
4. Frontend stores token in httpOnly cookie
   ↓
5. Frontend includes token in Authorization header for API requests
   ↓
6. Backend validates token, extracts user_id
   ↓
7. All queries filtered by user_id (data isolation)
   ↓
8. Backend returns user-scoped data only
   ↓
9. On token expiration (401), frontend redirects to signin
```

### User Data Isolation Pattern

```
Authenticated Request:
  ↓
[JWT Middleware] Validates token → Extracts user_id
  ↓
[Authorization Middleware] Checks ownership (for updates/deletes)
  ↓
[Database Query] WHERE user_id = <authenticated_user_id>
  ↓
[Response] Only data belonging to current user
```

---

## Development Guidelines

### Task Tracking

All code changes MUST be associated with a task ID in the format:
- Feature branches: `phase2-XXY-feature-name` (e.g., `phase2-001-auth`)
- Commits MUST reference the feature branch and task
- Example commit message:
  ```
  phase2-001-auth: Implement JWT token generation in Better Auth middleware

  🤖 Generated with Claude Code

  Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
  ```

### MCP Integration

All implementation work MUST consult:
- **Context7 MCP**: For updated technical documentation, debugging, and error resolution
- **Better Auth MCP**: For all Better Auth integration, configuration, and best practices

**Example Usage**:
```bash
# When implementing auth, consult Better Auth MCP first
# When debugging database issues, consult Context7 MCP first
# MCPs are the authoritative source; external docs are secondary
```

### Code Quality Standards

From `.specify/memory/constitution.md`:
- Clean code principles: small focused functions, clear naming
- No manual code writing if automation possible
- Performance over brevity
- All code must be testable in isolation
- Avoid over-engineering; minimal viable implementation

---

## Implementation Roadmap

### Phase II Delivery Phases

#### Phase 2.1: Backend Foundation (Priority: P1)
- [ ] Setup FastAPI project structure
- [ ] Create SQLModel data models (User, Todo)
- [ ] Setup Neon PostgreSQL connection
- [ ] Implement Better Auth integration
- [ ] Create JWT middleware

#### Phase 2.2: API Implementation (Priority: P1)
- [ ] POST /auth/signup endpoint
- [ ] POST /auth/signin endpoint
- [ ] POST /auth/logout endpoint
- [ ] GET /api/todos (list)
- [ ] POST /api/todos (create)
- [ ] GET /api/todos/{id} (get)
- [ ] PUT /api/todos/{id} (update)
- [ ] PATCH /api/todos/{id} (toggle)
- [ ] DELETE /api/todos/{id} (delete)

#### Phase 2.3: Frontend Implementation (Priority: P1)
- [ ] Setup Next.js 16+ with App Router
- [ ] Create signup/signin pages
- [ ] Create dashboard/todo list page
- [ ] Create todo form components
- [ ] Implement JWT token management
- [ ] Add responsive styling

#### Phase 2.4: Testing & Optimization (Priority: P2)
- [ ] Unit tests for API endpoints
- [ ] Integration tests for user flows
- [ ] E2E tests with Playwright
- [ ] Performance optimization (caching, query tuning)
- [ ] Security audit (OWASP top 10)

---

## Success Metrics

### MVP Completion
- ✅ All 7 user stories implemented and tested
- ✅ All 14 acceptance criteria verified
- ✅ All API endpoints documented and working
- ✅ User data isolation enforced (no cross-user access)
- ✅ JWT authentication required for all protected endpoints
- ✅ Frontend responsive on mobile/tablet/desktop
- ✅ Zero unhandled errors in tests

### Performance Targets
- API response times: < 200ms (p95)
- Frontend load time: < 2 seconds (FCP)
- Database query time: < 100ms (p95)

### Security Requirements
- All passwords hashed with bcrypt
- JWT tokens expire after 7 days
- All inputs validated (no SQL injection, XSS)
- HTTPS in production
- httpOnly cookies for token storage

---

## How to Use This Specification

### For Developers (Implementation)
1. Read **spec.md** to understand requirements
2. Reference **data-model.md** when designing database schema
3. Follow **api-contract.md** exactly when building endpoints
4. Use **acceptance-criteria.md** during testing
5. Commit code with task ID references

### For QA/Testers
1. Start with **acceptance-criteria.md**
2. Execute all test cases in the checklist
3. Reference **api-contract.md** for expected responses
4. Use curl examples provided to verify endpoints
5. Document any deviations from spec

### For Architects/Reviewers
1. Review **spec.md** for scope and completeness
2. Audit **data-model.md** for performance and scalability
3. Check **api-contract.md** for consistency and standards
4. Verify **acceptance-criteria.md** covers all scenarios
5. Approve PRs that reference correct task IDs

---

## Common Questions

### Q: Why require JWT for all requests?
**A**: User data isolation. Every request must be tied to a specific user (from JWT) to ensure data filtering. Without JWT, we can't enforce user_id filtering, risking data leakage.

### Q: Why 401 vs 403 for ownership violations?
**A**: Security through obscurity. Returning 403 when a user attempts to access another's todo doesn't reveal whether the todo exists. 404 would leak information.

### Q: Why store JWT in httpOnly cookie, not localStorage?
**A**: Security. httpOnly cookies are protected from JavaScript (XSS attacks) while localStorage is vulnerable. FastAPI should set the cookie; frontend should not manually manage it.

### Q: What if a user deletes their account? (Post-Phase II)
**A**: Implement cascade delete: `ON DELETE CASCADE` on the FK ensures all todos are deleted with the user. Or use soft-delete with `deleted_at` timestamp for recovery.

### Q: Can we add role-based access (admin, editor, viewer)?
**A**: Out of Phase II scope. MVP focuses on single user role (owner). Roles can be added in Phase III if needed.

---

## References

- **Constitution**: `.specify/memory/constitution.md` (Phase II principles, tech stack, MCP integration)
- **Git Attribution**: See CLAUDE.md for commit author guidelines
- **Better Auth Docs**: Consult via Better Auth MCP (authoritative source)
- **Context7 MCP**: For debugging and technical documentation updates
- **Phase I (Reference)**: `specs/001-cli-todo/` (in-memory, CLI-based predecessor)

---

## Document Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-12-29 | Claude Code | Initial Phase II specification |

---

## Approval & Sign-Off

- [ ] Architecture approved
- [ ] Requirements reviewed
- [ ] Acceptance criteria validated
- [ ] Timeline estimated
- [ ] Team assigned

**Ready for Implementation**: Yes ✅

