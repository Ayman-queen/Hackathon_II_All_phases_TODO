# Implementation Plan: UUID Type Mismatch Fix (Better Auth Integration)

**Branch**: `004-jwt-auth` | **Date**: 2026-01-02 | **Spec**: `specs/004-jwt-auth/spec.md`
**Input**: Feature specification + Error Analysis (error.txt + pydantic_core.ValidationError)
**Priority**: CRITICAL - Blocks all API functionality

**Note**: This is a focused remediation plan to resolve the UUID/string type mismatch between Better Auth and backend models.

## Summary

**Problem**: Backend Pydantic and SQLModel schemas declare `user_id: UUID`, but Better Auth generates string-based user identifiers (e.g., `'w2PYO9wq2FGP2fR111aTZkbPWD5ZyJPC'`). This causes pydantic_core.ValidationError on all list/read operations when Pydantic attempts to validate string identifiers as RFC 4122 UUIDs.

**Solution**: Refactor all backend data models (SQLModel, Pydantic schemas, API contracts) from `UUID` to `str` for user_id field, ensuring type consistency across all layers and database schema.

**Scope**:
- Update 6 Python model files (SQLModel + Pydantic)
- Execute 1 database migration
- Validate JWT token handling
- Update API contracts documentation

## Technical Context

**Language/Version**: Python 3.13, FastAPI 0.104+, Pydantic 2.5+, SQLModel 0.0.14
**Primary Dependencies**: FastAPI, SQLModel (SQLAlchemy 2.0), Pydantic v2, Better Auth
**Storage**: PostgreSQL (Neon Serverless) - todos table, user table (managed by Better Auth)
**Testing**: pytest, TestClient (FastAPI's async test client)
**Target Platform**: Linux server (FastAPI backend), async Python environment
**Project Type**: Full-stack web (backend focus for this fix)
**Performance Goals**: <100ms latency for list_todos endpoint (p95)
**Constraints**:
- Type safety across all layers (Constitution Principle I)
- JWT authentication mandatory on all endpoints (Constitution Principle II)
- Better Auth user_id is immutable once generated
- Database schema cannot have breaking changes mid-deployment

**Scale/Scope**:
- 1 application (Evo-TODO)
- ~10 backend files to update
- ~6 Pydantic/SQLModel schemas affected
- 1 database table migration

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Principle I (Full-Stack Type Safety)**: ✅ PASS
- Fix ensures type consistency across SQLModel, Pydantic, and API responses
- All user_id fields will use consistent `str` type

**Principle II (JWT Authentication & User Isolation)**: ✅ PASS
- JWT token extraction will correctly handle string user_id
- User isolation filtering by user_id remains intact post-fix

**Principle III (Clean Code)**: ✅ PASS
- Minimal, focused changes (single responsibility: UUID→str)
- No logic changes, purely type harmonization

**Principle IV (Task-Driven Implementation)**: ✅ PASS
- All changes mapped to Task T-239 (model refactor) and T-240 (DB migration)

**Principle VII (MCP Integration)**: ⚠️ CONDITIONAL
- **Requirement**: Consult Better Auth MCP for user_id format confirmation
- **Action**: Query Better Auth MCP before finalizing type changes
- **Validation**: Confirm that Better Auth user_id is always string, never UUID

**Gate Status**: PASS with MCP consultation as prerequisite

---

## Implementation Phases

### Phase 0: Pre-Implementation (MCP Consultation)

**Objective**: Confirm Better Auth user_id format before making code changes

**Tasks**:
1. Query Better Auth MCP: "What is the user ID format from Better Auth? Is it always a string? Provide examples and RFC/format specification."
2. Document findings in this plan file under "Better Auth User ID Format" section
3. Validate that string type is correct and immutable
4. Confirm no other type variants exist in Better Auth ecosystem

**Deliverable**: Research summary confirming string user_id is the standard

**Gate**: Cannot proceed to Phase 1 without MCP confirmation

---

### Phase 1: Model & Schema Refactoring

**Objective**: Update all Python models to use `str` for user_id instead of `UUID`

**Files to Update** (in order):

#### 1.1 Backend Models (app/models/)

**File**: `backend/app/models/user.py`
- **Current**: Check if `id: UUID` exists
- **Change**: Ensure `id: str` (should already be correct from previous fixes)
- **Validation**: Confirm UUID import can be removed if unused elsewhere

**File**: `backend/app/models/todo.py`
- **Current**: `user_id: UUID = Field(foreign_key="user.id", ...)`
- **Change**: `user_id: str = Field(foreign_key="user.id", ...)`
- **Validation**: Foreign key constraint will validate string references to user.id

#### 1.2 Pydantic Schemas (app/schemas/)

**File**: `backend/app/schemas/todo.py`
- **Current Schemas**:
  - `TodoResponse`: `user_id: UUID`
  - `TodoListResponse`: `todos: list[TodoResponse]` (cascades UUID)
  - `TodoCreate`: No user_id (backend-generated)
  - `TodoUpdate`: No user_id (immutable)
  - `TodoToggle`: No user_id (immutable)
- **Changes**:
  - `TodoResponse`: `user_id: str`
  - `TodoListResponse`: No change (auto-applies)
  - Remove UUID import if unused
- **Validation**: Pydantic will validate response.data.user_id as string

#### 1.3 API Dependencies (app/api/)

**File**: `backend/app/api/deps.py`
- **Current**: `get_current_user()` extracts user_id from JWT
  - Check if UUID conversion happens: `user_id = UUID(payload.get("sub"))`
  - If yes, remove conversion
- **Change**: Keep as string: `user_id: str = payload.get("sub")`
- **Validation**: JWT "sub" claim is always a string, no conversion needed

#### 1.4 API Endpoints (app/api/)

**File**: `backend/app/api/todos.py`
- **Current**: Returns `TodoListResponse` and `TodoResponse`
- **Impact**: Automatic (schemas updated in 1.2)
- **Validation**: Run list_todos endpoint, verify no ValidationError

#### 1.5 Type Imports

**Scan all files** for:
- `from uuid import UUID` - Remove if no longer used
- `UUID[...]` - Replace with `str`
- `uuid.UUID` - Replace with `str`

**Validation**: Check for any remaining UUID references in backend/app/

---

### Phase 2: Database Migration

**Objective**: Update PostgreSQL schema to support string user_id

**Migration Steps**:

#### 2.1 Connect to Neon Database
```bash
# Get connection string from .env or Neon dashboard
psql $DATABASE_URL
```

#### 2.2 Migrate todos table
```sql
-- Check current schema
\d todos

-- Convert column type (PostgreSQL allows this for string/UUID conversion)
ALTER TABLE todos ALTER COLUMN user_id TYPE VARCHAR(255);

-- Verify migration
\d todos

-- Check that data persists
SELECT id, user_id, title FROM todos LIMIT 1;
```

#### 2.3 Verify Foreign Key Constraint
```sql
-- Check if foreign key still valid
SELECT * FROM information_schema.constraint_column_usage
WHERE table_name = 'todos' AND column_name = 'user_id';
```

**Validation**: No errors during migration, foreign key remains intact

---

### Phase 3: Integration Testing

**Objective**: Verify end-to-end functionality with string user_id

**Tests to Run**:

#### 3.1 Unit Tests
```bash
cd backend
pytest tests/test_models/test_todo.py -v
pytest tests/test_schemas/test_todo.py -v
```

#### 3.2 Integration Tests
```bash
pytest tests/test_api/test_todos.py -v
# Expected: All 6 endpoints pass (list, create, get, update status, update fields, delete)
```

#### 3.3 Manual Testing
```bash
# Start backend
cd backend
uvicorn app.main:app --reload

# In another terminal, test with curl
curl -H "Authorization: Bearer <JWT_TOKEN>" http://localhost:8000/api/todos

# Expected: 200 OK with list of todos (no ValidationError)
```

**Validation**: No pydantic_core.ValidationError on any endpoint

---

### Phase 4: Documentation Update

**Objective**: Document the type change and Better Auth integration

**Files to Update**:

#### 4.1 `specs/004-jwt-auth/plan.md` (this file)
- Add section: "Better Auth User ID Format"
- Document: user_id is string, example format, immutability

#### 4.2 `specs/004-jwt-auth/spec.md`
- Add to NFR section: "User ID Type: Better Auth generates string identifiers (~33 char alphanumeric)"
- Add to Architecture: "User ID is immutable and generated by Better Auth"

#### 4.3 API Contract (if exists)
- Update user_id field type from UUID to string in OpenAPI schema
- Update examples to use string user_id

---

## Better Auth User ID Format

**Status**: ✅ MCP CONFIRMATION COMPLETE (Phase 0)

- **Type**: `str` (confirmed by Better Auth MCP documentation)
- **Format**: Alphanumeric string, ~33 characters (example: `w2PYO9wq2FGP2fR111aTZkbPWD5ZyJPC`)
- **Generation Method**: `generateId()` function uses `crypto.randomUUID()` internally
- **Immutability**: Generated once at user creation, never changes
- **RFC Compliance**: NOT RFC 4122 compliant - uses custom alphanumeric format
- **Standardization**: Default behavior in Better Auth; immutable per user session lifecycle

**MCP Confirmation Details**:
- Source: Better Auth MCP documentation (database.mdx)
- User model structure: `id: string` field type
- Default ID generation: `crypto.randomUUID()` returns string format
- Confirmed: Better Auth consistently uses string identifiers for user IDs
- No UUID variants or alternative formats found in Better Auth ecosystem
- Conclusion: Backend must accept `str` type for all user_id fields

---

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

This fix impacts only the backend data layer. No frontend changes required.

```text
backend/
├── app/
│   ├── models/
│   │   ├── user.py          # User model (VERIFY id: str)
│   │   ├── todo.py          # Todo model (CHANGE user_id: UUID → str)
│   │   └── database.py      # Database session/engine
│   │
│   ├── schemas/
│   │   ├── todo.py          # Pydantic schemas (CHANGE user_id: UUID → str)
│   │   └── __init__.py
│   │
│   ├── api/
│   │   ├── deps.py          # JWT dependency (VERIFY no UUID conversion)
│   │   ├── todos.py         # Endpoints (AUTO-UPDATED via schema changes)
│   │   └── __init__.py
│   │
│   ├── main.py              # FastAPI app
│   └── __init__.py
│
├── tests/
│   ├── test_models/
│   │   └── test_todo.py     # Model tests (RUN: verify string user_id)
│   ├── test_schemas/
│   │   └── test_todo.py     # Schema tests (RUN: verify serialization)
│   ├── test_api/
│   │   └── test_todos.py    # API endpoint tests (RUN: integration tests)
│   └── __init__.py
│
└── .env                      # Database connection string (USED for migration)
```

**Structure Decision**:
- Focused backend-only changes
- No frontend modifications needed
- Database migration executed via psql/Neon console
- All model and schema files co-located with API layer

## Complexity Tracking

> **Status**: NO CONSTITUTION VIOLATIONS - All checks passed

This fix is a **type harmonization** effort with **zero architectural complexity**:
- No new patterns or abstractions introduced
- Minimal code changes (6 files, all straightforward string replacements)
- Single database migration (type conversion, no data transformation)
- No breaking changes to API contracts (user_id remains, type just changes)

**Simplicity Principle Applied**: The smallest viable refactoring that resolves the type mismatch without introducing unnecessary abstractions or patterns.
