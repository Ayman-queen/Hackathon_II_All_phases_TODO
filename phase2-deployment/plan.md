# Implementation Plan: Phase 2 Separate Deployment Architecture

**Branch**: `phase-2` | **Date**: 2026-01-07 | **Feature**: Production Deployment
**Input**: Separate deployment requirements - Frontend and Backend on different Vercel instances

## Summary

Configure and deploy Evo-TODO application with **separate deployments** for frontend and backend services on Vercel. Remove unnecessary micro-frontend service files (`/api/index.py`, root `vercel.json`), fix environment configuration for production URLs, ensure proper CORS setup, and verify end-to-end connectivity between services.

**Current State**:
- Frontend deployed: `https://evo-todo.vercel.app/`
- Backend deployed: `https://evo-todo-cj2z.vercel.app/`
- Configuration pointing to localhost (development mode)
- Unused micro-frontend service files present

**Target State**:
- Frontend correctly configured to call production backend
- Backend accepting requests from production frontend
- Unnecessary deployment files removed
- Production environment variables set
- Full authentication and data flow verified

## Technical Context

**Language/Version**: TypeScript 5.x (Next.js 16), Python 3.11 (FastAPI)
**Primary Dependencies**: Next.js, Better Auth, FastAPI, SQLModel, PostgreSQL (Neon)
**Storage**: Neon Serverless PostgreSQL (shared between services)
**Authentication**: Better Auth with JWT (EdDSA/Ed25519), JWKS verification
**Deployment**: Vercel (separate deployments)
**Target Platform**: Vercel Serverless (Node.js for frontend, Python for backend)

**Performance Goals**:
- API response time <500ms p95
- JWT verification <100ms
- Database queries <200ms

**Constraints**:
- Separate deployment architecture (non-negotiable)
- No monolithic `/api` route on frontend
- CORS must be properly configured
- JWT tokens must work across origins

**Scale/Scope**:
- 2 separate Vercel deployments
- 1 shared PostgreSQL database (Neon)
- ~10 configuration files to update
- 2 files to remove

## Constitution Check

*GATE: Must pass before implementation.*

✅ **Separate Deployment Pattern**: Aligns with microservices architecture principle
✅ **Security**: JWT-based authentication with asymmetric cryptography (EdDSA)
✅ **Simplicity**: Remove unused files, clean configuration
✅ **Testing**: Verify connectivity and data flow end-to-end

## Project Structure

### Current Deployment Architecture

```text
┌─────────────────────────────────────────────┐
│ Frontend Vercel Deployment                  │
│ URL: https://evo-todo.vercel.app/           │
│                                             │
│ ┌─────────────────────────────────────┐     │
│ │ Next.js 16 (SSR + Client)           │     │
│ │ - Pages & Components                │     │
│ │ - Better Auth API (/api/auth/*)     │     │
│ │ - JWT Token Generation              │     │
│ │ - JWKS Endpoint                     │     │
│ │ - Session Management                │     │
│ └─────────────────────────────────────┘     │
│                                             │
│ ❌ /api/index.py (UNUSED - to be removed)   │
└─────────────────────────────────────────────┘
              ↓ (HTTPS API calls with JWT)
┌─────────────────────────────────────────────┐
│ Backend Vercel Deployment                   │
│ URL: https://evo-todo-cj2z.vercel.app/      │
│                                             │
│ ┌─────────────────────────────────────┐     │
│ │ FastAPI (Python Serverless)         │     │
│ │ - JWT Verification (JWKS fetch)     │     │
│ │ - Todo CRUD API                     │     │
│ │ - User Authentication Dependency    │     │
│ └─────────────────────────────────────┘     │
└─────────────────────────────────────────────┘
              ↓ (PostgreSQL queries)
┌─────────────────────────────────────────────┐
│ Neon PostgreSQL Database (Shared)           │
│ - user table (Better Auth)                  │
│ - todo table (application data)             │
└─────────────────────────────────────────────┘
```

### Request Flow

```text
1. User Login (Browser)
   ↓
2. POST https://evo-todo.vercel.app/api/auth/sign-in
   ↓ (Better Auth validates credentials)
3. Better Auth creates session + JWT token
   ↓ (Token stored in browser memory)
4. Frontend component calls API
   ↓
5. lib/api.ts retrieves JWT via authClient.token()
   ↓
6. Request to https://evo-todo-cj2z.vercel.app/api/todos
   Headers: Authorization: Bearer <JWT>
   ↓ (CORS preflight check)
7. Backend CORS middleware validates origin
   ↓
8. Backend JWT verification:
   - Fetch JWKS from https://evo-todo.vercel.app/api/auth/jwks
   - Verify EdDSA signature
   - Extract user_id from token
   ↓
9. Database query (filtered by user_id)
   ↓
10. Response with todos → Frontend
```

## Phase 0: Research & Discovery

### Files to Remove (Unused in Separate Deployment)

1. **`/api/index.py`** (root level)
   - **Purpose**: Wraps FastAPI as Vercel serverless function for unified deployment
   - **Why Remove**: Backend is deployed separately, this file is not used
   - **Impact**: None (file is currently ignored by Vercel)

2. **`/vercel.json`** (root level, if exists)
   - **Purpose**: Configures Vercel routing for monolithic deployment
   - **Why Remove**: Separate deployments have their own configurations
   - **Impact**: None (each deployment has its own config)

### Files to Modify

1. **`frontend/.env`**
   - Update `NEXT_PUBLIC_API_URL` to production backend URL
   - Update `NEXT_PUBLIC_AUTH_URL` to production frontend URL
   - Set `NODE_ENV=production`

2. **`backend/.env`**
   - Update `BETTER_AUTH_URL` to production frontend URL (already correct)
   - Update `CORS_ORIGINS` to production frontend URL (already correct)
   - Set `ENVIRONMENT=production`
   - Set `DEBUG=False`

3. **Vercel Environment Variables** (both deployments)
   - Move secrets from `.env` files to Vercel dashboard
   - Ensure `DATABASE_URL` is set correctly
   - Ensure `BETTER_AUTH_SECRET` matches between frontend and backend

### Configuration Audit

| Variable | Frontend | Backend | Status |
|----------|----------|---------|--------|
| `NEXT_PUBLIC_AUTH_URL` | ❌ localhost:3000 | N/A | **Must Fix** |
| `NEXT_PUBLIC_API_URL` | ❌ localhost:8000 | N/A | **Must Fix** |
| `BETTER_AUTH_URL` | N/A | ✅ Production | **Correct** |
| `CORS_ORIGINS` | N/A | ✅ Production | **Correct** |
| `DATABASE_URL` | ⚠️ Exposed | ⚠️ Exposed | **Must Secure** |
| `BETTER_AUTH_SECRET` | ⚠️ Exposed | N/A | **Must Secure** |
| `NODE_ENV` | ❌ development | N/A | **Must Fix** |
| `ENVIRONMENT` | N/A | ❌ development | **Must Fix** |
| `DEBUG` | N/A | ❌ True | **Must Fix** |

## Phase 1: Architecture & Design

### Decision 1: Remove Micro-Frontend Service Files

**Context**: The `/api/index.py` file is designed for unified deployment where the backend is served from the frontend's `/api` route. Since we're using separate deployments, this file is unnecessary and creates confusion.

**Decision**: Remove `/api/index.py` and any root-level `vercel.json`.

**Rationale**:
- Separate deployments don't need unified routing
- File is currently unused and will never be deployed
- Reduces codebase complexity
- Eliminates confusion about deployment strategy

**Alternatives Considered**:
- Keep file for future unified deployment: Rejected (YAGNI principle - You Aren't Gonna Need It)
- Move to `/archive`: Rejected (unnecessary clutter, can restore from git history)

**Trade-offs**:
- ✅ Cleaner codebase
- ✅ No confusion about deployment approach
- ⚠️ If switching to unified deployment later, need to recreate file (acceptable, can restore from git)

### Decision 2: Production Environment Variables Strategy

**Context**: Current `.env` files contain hardcoded secrets (database credentials, auth secret) that are exposed in the repository.

**Decision**: Use Vercel environment variables for all secrets, keep `.env` files for local development only.

**Implementation**:
1. Create `.env.production` templates with placeholder values
2. Document required environment variables in deployment spec
3. Store real values in Vercel dashboard (encrypted at rest)
4. Add `.env.production` to `.gitignore`

**Rationale**:
- Secrets are encrypted in Vercel environment variables
- `.env` files are only for local development
- Production builds never use local `.env` files
- Clear separation between dev and prod configurations

### Decision 3: CORS Configuration for Preview Deployments

**Context**: Vercel creates preview URLs for every PR (e.g., `https://evo-todo-git-feature-*.vercel.app`). Current CORS only allows production URL.

**Decision**: Add wildcard pattern to allow preview deployments.

**Configuration**:
```python
# backend/.env
CORS_ORIGINS=https://evo-todo.vercel.app,https://evo-todo-*.vercel.app
```

**Rationale**:
- Preview deployments need to test frontend-backend integration
- Wildcard is scoped to project subdomain (secure)
- Enables testing before merging to production

**Security Considerations**:
- ✅ Wildcard only matches Vercel project subdomains
- ✅ Preview deployments require authentication
- ⚠️ Any branch can deploy preview (acceptable for internal testing)

### Decision 4: Health Check Endpoints

**Context**: Need monitoring and health checks for both services.

**Decision**: Ensure both services have `/health` endpoints that return 200 OK.

**Implementation**:
- Backend: Already has `/health` endpoint (api/index.py:50)
- Frontend: Add `/api/health/route.ts` endpoint

**Response Format**:
```json
{
  "status": "healthy",
  "service": "frontend|backend",
  "timestamp": "2026-01-07T12:00:00Z"
}
```

### Decision 5: Database Connection String Security

**Context**: Neon database credentials are exposed in `.env` files.

**Decision**:
1. Move `DATABASE_URL` to Vercel environment variables
2. Rotate database password after deployment
3. Document secure credential management in deployment guide

**Implementation Steps**:
1. Update Vercel environment variables with current `DATABASE_URL`
2. Deploy both services to verify connectivity
3. Rotate Neon database password via Neon console
4. Update Vercel environment variables with new password
5. Remove credentials from local `.env` files

## Phase 2: Implementation Tasks

### Task Group 1: Remove Unused Files

**T-1.1: Remove micro-frontend service file**
- Delete `/api/index.py`
- Verify file is not referenced in any imports
- Update any documentation referencing unified deployment

**T-1.2: Remove root vercel.json (if exists)**
- Check if `/vercel.json` exists at root level
- If exists, verify it's not used by frontend deployment
- Delete if unused

**Acceptance Criteria**:
- [x] `/api/index.py` deleted
- [x] No import errors in backend
- [x] Root `/vercel.json` removed (if it existed)
- [x] Git commit: "chore: remove unused micro-frontend service files"

---

### Task Group 2: Update Frontend Environment Configuration

**T-2.1: Create production environment file**

Create `frontend/.env.production`:
```env
# Production Frontend Configuration
NEXT_PUBLIC_AUTH_URL=https://evo-todo.vercel.app
NEXT_PUBLIC_API_URL=https://evo-todo-cj2z.vercel.app
NODE_ENV=production

# Database and secrets are set in Vercel environment variables
# Do not commit DATABASE_URL or BETTER_AUTH_SECRET to this file
```

**T-2.2: Update Vercel environment variables (Frontend)**

In Vercel dashboard for `evo-todo` project:
1. Set `NEXT_PUBLIC_AUTH_URL=https://evo-todo.vercel.app`
2. Set `NEXT_PUBLIC_API_URL=https://evo-todo-cj2z.vercel.app`
3. Set `DATABASE_URL=<neon-connection-string>` (copy from current `.env`)
4. Set `BETTER_AUTH_SECRET=<secret>` (copy from current `.env`)
5. Set `NODE_ENV=production`

**T-2.3: Update local development .env**

Update `frontend/.env` to clearly mark as development:
```env
# Local Development Configuration
# DO NOT use these values in production

NEXT_PUBLIC_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
DATABASE_URL=postgresql://neondb_owner:...@neon.tech/neondb
BETTER_AUTH_SECRET=<keep-existing-secret>
NODE_ENV=development
```

**Acceptance Criteria**:
- [x] `.env.production` created with production URLs
- [x] `.env.production` added to `.gitignore`
- [x] Vercel environment variables set for frontend
- [x] Local `.env` clearly marked as development
- [x] Git commit: "config: add production environment for frontend"

---

### Task Group 3: Update Backend Environment Configuration

**T-3.1: Create production environment file**

Create `backend/.env.production`:
```env
# Production Backend Configuration
BETTER_AUTH_URL=https://evo-todo.vercel.app
CORS_ORIGINS=https://evo-todo.vercel.app,https://evo-todo-*.vercel.app
ENVIRONMENT=production
DEBUG=False

# JWKS Cache Configuration
JWKS_CACHE_LIFESPAN=300
JWKS_CACHE_MAX_KEYS=16

# Database is set in Vercel environment variables
# Do not commit DATABASE_URL to this file
```

**T-3.2: Update Vercel environment variables (Backend)**

In Vercel dashboard for `evo-todo-backend` project:
1. Set `DATABASE_URL=<neon-connection-string>` (copy from current `.env`)
2. Set `BETTER_AUTH_URL=https://evo-todo.vercel.app`
3. Set `CORS_ORIGINS=https://evo-todo.vercel.app,https://evo-todo-*.vercel.app`
4. Set `ENVIRONMENT=production`
5. Set `DEBUG=False`
6. Set `JWKS_CACHE_LIFESPAN=300`
7. Set `JWKS_CACHE_MAX_KEYS=16`

**T-3.3: Update local development .env**

Update `backend/.env` to clearly mark as development:
```env
# Local Development Configuration
# DO NOT use these values in production

DATABASE_URL=postgresql://neondb_owner:...@neon.tech/neondb
BETTER_AUTH_URL=http://localhost:3000
CORS_ORIGINS=http://localhost:3000
JWKS_CACHE_LIFESPAN=300
JWKS_CACHE_MAX_KEYS=16
ENVIRONMENT=development
DEBUG=True
```

**Acceptance Criteria**:
- [x] `.env.production` created with production configuration
- [x] `.env.production` added to `.gitignore`
- [x] Vercel environment variables set for backend
- [x] CORS allows production and preview URLs
- [x] `DEBUG=False` and `ENVIRONMENT=production` set
- [x] Git commit: "config: add production environment for backend"

---

### Task Group 4: Add Frontend Health Check Endpoint

**T-4.1: Create health check API route**

Create `frontend/app/api/health/route.ts`:
```typescript
// Health check endpoint for monitoring
export async function GET() {
  return Response.json({
    status: "healthy",
    service: "frontend",
    timestamp: new Date().toISOString(),
    version: "1.0.0",
  })
}
```

**T-4.2: Test health check locally**

```bash
curl http://localhost:3000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "frontend",
  "timestamp": "2026-01-07T12:00:00Z",
  "version": "1.0.0"
}
```

**Acceptance Criteria**:
- [x] Health check route created
- [x] Returns 200 OK status
- [x] Response includes service name and timestamp
- [x] Tested locally and in production
- [x] Git commit: "feat: add frontend health check endpoint"

---

### Task Group 5: Update .gitignore

**T-5.1: Add production environment files to .gitignore**

Update `frontend/.gitignore`:
```gitignore
# Environment files
.env
.env.local
.env.production
.env.production.local
```

Update `backend/.gitignore`:
```gitignore
# Environment files
.env
.env.local
.env.production
.env.production.local
```

Update root `.gitignore`:
```gitignore
# Environment files (all directories)
**/.env
**/.env.local
**/.env.production
**/.env.production.local

# Vercel
.vercel
```

**Acceptance Criteria**:
- [x] `.env.production` files not tracked by git
- [x] Existing `.env` files remain tracked (for reference)
- [x] `.gitignore` updated in all relevant locations
- [x] Git commit: "config: update .gitignore for production env files"

---

### Task Group 6: Deployment & Verification

**T-6.1: Deploy frontend to production**

```bash
cd frontend
vercel --prod
```

Verify:
- Deployment successful
- Environment variables loaded correctly
- Health check endpoint responds: `https://evo-todo.vercel.app/api/health`

**T-6.2: Deploy backend to production**

```bash
cd backend
vercel --prod
```

Verify:
- Deployment successful
- Environment variables loaded correctly
- Health check endpoint responds: `https://evo-todo-cj2z.vercel.app/health`
- API docs accessible: `https://evo-todo-cj2z.vercel.app/docs`

**T-6.3: Test end-to-end authentication flow**

1. Navigate to `https://evo-todo.vercel.app/`
2. Sign up with new account
3. Verify email stored in database (check Neon console)
4. Login with credentials
5. Verify JWT token generated (check browser dev tools → Network → /api/auth/token)
6. Create a todo item
7. Verify API request includes Authorization header
8. Verify todo saved to database
9. Refresh page, verify todos load correctly
10. Logout and verify session cleared

**T-6.4: Test CORS and cross-origin requests**

Open browser console on `https://evo-todo.vercel.app/dashboard`:

```javascript
// Test authenticated API call
fetch('https://evo-todo-cj2z.vercel.app/api/todos', {
  headers: {
    'Authorization': 'Bearer <token-from-network-tab>'
  }
})
.then(r => r.json())
.then(console.log)
```

Expected: 200 OK with todos array
If fails: Check CORS headers in Network tab

**T-6.5: Verify JWKS endpoint accessibility**

```bash
curl https://evo-todo.vercel.app/api/auth/jwks
```

Expected response:
```json
{
  "keys": [
    {
      "kty": "OKP",
      "crv": "Ed25519",
      "x": "...",
      "kid": "...",
      "use": "sig",
      "alg": "EdDSA"
    }
  ]
}
```

**T-6.6: Test backend JWT verification**

Make authenticated request to backend:
```bash
# Get token from frontend
TOKEN=$(curl -X POST https://evo-todo.vercel.app/api/auth/sign-in \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}' \
  | jq -r '.token')

# Use token to call backend
curl https://evo-todo-cj2z.vercel.app/api/todos \
  -H "Authorization: Bearer $TOKEN"
```

Expected: 200 OK with user's todos

**Acceptance Criteria**:
- [x] Frontend deployed to `https://evo-todo.vercel.app/`
- [x] Backend deployed to `https://evo-todo-cj2z.vercel.app/`
- [x] Health check endpoints respond correctly
- [x] Authentication flow works end-to-end
- [x] CORS allows frontend to call backend
- [x] JWT tokens are generated and verified correctly
- [x] JWKS endpoint is accessible from backend
- [x] Todos can be created, read, updated, deleted
- [x] Data is properly isolated by user_id

---

### Task Group 7: Secure Database Credentials

**T-7.1: Rotate Neon database password**

1. Login to Neon console: https://console.neon.tech
2. Navigate to project → Settings → Reset Password
3. Copy new connection string

**T-7.2: Update Vercel environment variables**

Update `DATABASE_URL` in both deployments:
1. Frontend Vercel project → Settings → Environment Variables → Edit `DATABASE_URL`
2. Backend Vercel project → Settings → Environment Variables → Edit `DATABASE_URL`
3. Paste new connection string
4. Redeploy both services

**T-7.3: Update local .env files with new credentials**

Update `frontend/.env` and `backend/.env` with new `DATABASE_URL` (for local development).

**T-7.4: Verify connectivity after rotation**

1. Test frontend auth: https://evo-todo.vercel.app/login
2. Test backend API: https://evo-todo-cj2z.vercel.app/health
3. Create test todo to verify database writes

**Acceptance Criteria**:
- [x] Database password rotated
- [x] New credentials stored in Vercel (not in git)
- [x] Both services connect to database successfully
- [x] All CRUD operations work corr
