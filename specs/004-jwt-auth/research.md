# JWT Authentication Research & Technical Decisions

**Date**: 2026-01-01
**Feature**: JWT Authentication Integration (Phase 2.2)
**Status**: Complete

## Research Summary

This document captures architectural decisions and technical recommendations for implementing JWT authentication across the frontend (Next.js) and backend (FastAPI) using Better Auth.

---

## Decision 1: JWT Token Issuance Method

**Topic**: How Better Auth issues JWT tokens

### Research Findings

Better Auth provides two approaches for JWT token handling:

1. **JWT Plugin** (Recommended for cross-service authentication)
   - Issues asymmetric signed tokens (EdDSA or ES256)
   - Provides JWKS endpoint for public key distribution
   - Self-contained validation without database lookup
   - Best for decoupled frontend/backend systems

2. **Bearer Plugin** (Alternative for simpler flows)
   - Symmetrically signed tokens
   - Simpler setup but less flexible
   - Suitable for monolithic deployments

### Decision

**Use Better Auth's JWT Plugin** for token issuance.

**Rationale**:
- Frontend and backend are decoupled services (Next.js frontend, FastAPI backend)
- JWT tokens need independent verification by FastAPI without calling Better Auth
- JWKS endpoint allows FastAPI to fetch public keys for verification
- EdDSA (Ed25519) is more secure than HS256 for distributed systems
- Asymmetric signing enables token rotation and key management

### Alternatives Considered

- Bearer Plugin: Rejected because it uses HMAC-SHA256 with a symmetric secret, which requires sharing secrets; less secure for distributed systems
- OAuth2 Password Flow: Rejected because we're not implementing full OAuth2; JWT is sufficient for user-scoped API access

### Implementation Notes

- Enable JWT plugin in Better Auth config
- Configure JWT payload to include user ID and email (minimum required claims)
- Set default expiration to 7 days (configurable)
- Use default Ed25519 key pair for signing

---

## Decision 2: Frontend Token Storage & Attachment

**Topic**: How frontend stores and uses JWT tokens

### Research Findings

Better Auth provides multiple token retrieval methods:

1. **jwtClient() Plugin** (Recommended)
   - Explicit method to retrieve tokens via `authClient.token()`
   - Full control over token lifecycle
   - Can cache and refresh tokens programmatically
   - Works with both localStorage and cookies

2. **set-auth-jwt Header** (Alternative)
   - JWT automatically returned in response headers after `getSession()`
   - Less explicit but convenient
   - Requires header parsing on each call

3. **set-auth-token Header** (Bearer Plugin only)
   - Automatically included in requests if bearer plugin enabled
   - Not suitable for our JWT plugin setup

### Decision

**Use jwtClient() plugin with explicit token retrieval**.

**Rationale**:
- Explicit control over token lifecycle
- Can cache token and refresh on-demand
- Easy to monitor token expiration and prompt re-authentication
- Works with localStorage for persistent sessions
- Allows manual token attachment to requests

### Token Storage Strategy

- **Primary**: localStorage with key `jwt_token`
- **Fallback**: sessionStorage for temporary sessions
- **Secure flag**: Use secure HTTP-only cookies if possible in Next.js environment

### Implementation Pattern

```typescript
// After login/session establishment
const { data } = await authClient.token()
if (data?.token) {
  localStorage.setItem('jwt_token', data.token)
}

// For API requests, attach token
const token = localStorage.getItem('jwt_token')
headers.Authorization = `Bearer ${token}`
```

---

## Decision 3: Frontend API Client Middleware

**Topic**: How frontend automatically attaches JWT tokens to requests

### Research Findings

Next.js has several approaches for API request interception:

1. **Custom Fetch Wrapper** (Recommended)
   - Wraps native fetch API
   - Full control over header injection
   - Works in both client and server components
   - Can implement retry logic and token refresh

2. **Axios Interceptor** (Alternative)
   - Popular library for HTTP requests
   - Built-in interceptor support
   - Adds dependency overhead
   - Requires middleware setup

3. **Next.js Middleware** (Limited)
   - Works on edge runtime
   - Limited for client-side API calls
   - Better for request transformation

### Decision

**Implement custom API client with fetch wrapper**.

**Rationale**:
- Minimal dependencies (native fetch API)
- Full control over token injection logic
- Can implement exponential backoff for failed requests
- Can handle 401 responses and prompt re-authentication
- Works seamlessly in Next.js App Router

### Implementation Pattern

```typescript
export class ApiClient {
  private getToken(): string {
    return localStorage.getItem('jwt_token') || ''
  }

  async request(
    url: string,
    options: RequestInit = {}
  ): Promise<Response> {
    const headers = {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${this.getToken()}`,
      ...options.headers,
    }

    const response = await fetch(url, { ...options, headers })

    if (response.status === 401) {
      // Token expired, prompt re-authentication
      window.dispatchEvent(new Event('auth:unauthorized'))
    }

    return response
  }
}
```

---

## Decision 4: Backend JWT Verification Method

**Topic**: How FastAPI verifies JWT tokens

### Research Findings

FastAPI provides multiple JWT verification approaches:

1. **python-jose Library** (Standard approach)
   - `jwtVerify()` function for token validation
   - Support for JWKS validation
   - Can fetch public keys from remote endpoint
   - Handles key rotation automatically

2. **PyJWT Library** (Alternative)
   - Simpler, but requires manual key management
   - Less suitable for key rotation
   - Good for simple symmetric signing

3. **FastAPI Security Dependency Injection** (Pattern)
   - Use `Depends()` for middleware-like authentication
   - More Pythonic than explicit middleware
   - Easier to test

### Decision

**Use python-jose with JWKS verification from Better Auth**.

**Rationale**:
- Better Auth provides JWKS endpoint automatically
- python-jose supports JWKS fetching and caching
- Handles key rotation without code changes
- No shared secret management needed
- FastAPI's dependency injection pattern for cleaner code

### Implementation Pattern

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from jose import jwt, JWTError, jwk

# Configure JWT verification
JWKS_URL = "http://localhost:3000/api/auth/jwks"
ALGORITHM = "EdDSA"  # Match Better Auth config

async def verify_token(credentials: HTTPAuthCredentials = Depends(HTTPBearer())):
    token = credentials.credentials
    try:
        # Fetch JWKS from Better Auth
        # Verify token signature
        payload = jwt.get_unverified_claims(token)
        user_id = payload.get("sub")  # or "id" depending on payload config
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
```

---

## Decision 5: User Isolation in FastAPI Routes

**Topic**: How FastAPI enforces user ownership of tasks

### Research Findings

FastAPI patterns for user-scoped data:

1. **Request Context Injection** (Recommended)
   - Extract user_id from JWT in dependency
   - Inject into route handler
   - Query filter applied at database level

2. **Manual Route Guards** (Not recommended)
   - Check user_id matches JWT in each route
   - Verbose and error-prone
   - Repeats logic across endpoints

3. **Middleware + Context** (Alternative)
   - Extract user_id in global middleware
   - Store in request.state
   - Less explicit but reduces parameter passing

### Decision

**Use dependency injection with route-level verification**.

**Rationale**:
- FastAPI best practice for dependency injection
- Clear, explicit user_id in function signatures
- Easy to test and reason about
- Self-documenting API contracts
- Each route explicitly verifies ownership

### Implementation Pattern

```python
@router.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    current_user_id: str = Depends(verify_token)
):
    # Verify ownership
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    # Query tasks for this user only
    tasks = db.query(Task).filter(
        Task.user_id == current_user_id
    ).all()

    return tasks
```

---

## Decision 6: API Error Responses

**Topic**: How to handle and report authentication errors

### Research Findings

HTTP status codes for authentication:
- `401 Unauthorized`: Token missing, invalid, or expired
- `403 Forbidden`: User lacks permission for resource
- `400 Bad Request`: Malformed request

### Decision

**Use standard HTTP status codes with detailed error objects**.

**Rationale**:
- Follows HTTP semantics
- Client can implement appropriate retry strategies
- Clear distinction between auth failure vs. authorization failure

### Error Response Format

```json
{
  "detail": "Invalid authentication credentials",
  "error_code": "INVALID_TOKEN",
  "status": 401
}
```

---

## Decision 7: Token Expiration & Refresh Strategy

**Topic**: How to handle token expiration

### Research Findings

Token refresh patterns:
1. **Sliding Window**: Extend expiration on every request
2. **Refresh Token Rotation**: Issue short-lived access + long-lived refresh tokens
3. **Manual Refresh**: User re-authenticates on token expiry

### Decision

**Manual refresh with 7-day token expiration** (per spec).

**Rationale**:
- Out of scope for Phase 2.2 to implement refresh token rotation
- 7-day expiration is reasonable for task management app
- Simpler implementation, fewer moving parts
- Frontend can prompt user to re-authenticate when token expires
- Can be enhanced in future phases

---

## Decision 8: CORS & Trust Configuration

**Topic**: How to handle cross-origin requests

### Research Findings

Better Auth trusts origins via:
- `trustedOrigins` array in auth config
- CORS headers in responses
- Protects against CSRF attacks

### Decision

**Configure Better Auth with trusted frontend origin**.

**Rationale**:
- Frontend and backend are on different origins (localhost:3000 vs :8000)
- Better Auth requires explicit trust for cross-origin auth requests
- Prevents CSRF attacks on authentication endpoints

### Configuration

```typescript
// auth.ts
export const auth = betterAuth({
  plugins: [jwt()],
  trustedOrigins: [
    process.env.FRONTEND_URL || "http://localhost:3000"
  ]
})
```

---

## Summary of Architectural Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| **JWT Issuance** | Better Auth JWT Plugin (EdDSA) | Asymmetric, scalable, JWKS support |
| **Frontend Storage** | localStorage + jwtClient() | Explicit control, persistent sessions |
| **Frontend Attachment** | Custom fetch wrapper | Minimal deps, full control |
| **Backend Verification** | python-jose + JWKS | Auto key rotation, no secrets sharing |
| **User Isolation** | Dependency injection + ownership check | FastAPI best practice, explicit |
| **Error Handling** | HTTP status codes + error objects | Standard, client-friendly |
| **Token Refresh** | Manual, 7-day expiration | Simpler, sufficient for Phase 2.2 |
| **CORS** | Trusted origins config | Security, cross-origin support |

---

## Next Steps

1. **Phase 1**: Create data models, API contracts, and quickstart guide
2. **Phase 2**: Implement authentication layer based on these decisions
3. **Testing**: Validate token flow end-to-end with integration tests
4. **Future**: Consider refresh token rotation and advanced token management
