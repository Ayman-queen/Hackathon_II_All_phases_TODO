# JWT Structure: Better Auth Token

**Task**: T-231 - Verify JWT token extraction from Better Auth
**Date**: 2025-12-31
**Status**: ✅ Verified

## Better Auth JWT Token Structure

### Token Format
Better Auth issues JWT tokens in standard format:
```
<header>.<payload>.<signature>
```

### Example Decoded Payload
```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "iss": "http://localhost:3000",
  "aud": "http://localhost:3000",
  "exp": 1735755600,
  "iat": 1735751000,
  "email": "user@example.com",
  "verified": true
}
```

### Key Claims

| Claim | Type | Purpose | Example |
|-------|------|---------|---------|
| `sub` | string | Subject (User ID) | `550e8400-e29b-41d4-a716-446655440000` |
| `iss` | string | Issuer | `http://localhost:3000` |
| `aud` | string | Audience | `http://localhost:3000` |
| `exp` | number | Expiration timestamp (seconds) | `1735755600` |
| `iat` | number | Issued at timestamp | `1735751000` |
| `email` | string | User email | `user@example.com` |
| `verified` | boolean | Email verified status | `true` |

### Extracting User ID from Token

**WITHOUT Signature Verification** (safe for non-critical use):
```typescript
// Decode JWT without verification - extracts sub claim
const token = "eyJhbGc...";
const payload = JSON.parse(atob(token.split('.')[1]));
const userId = payload.sub; // "550e8400-e29b-41d4-a716-446655440000"
```

**WITH Signature Verification** (required for authentication):
```typescript
// Use Better Auth client's jwtClient() plugin
const { data: session } = await authClient.getSession();
const userId = session?.user.id; // From verified session
```

### Token Lifetime

- **Issued At (iat)**: Current time
- **Expires At (exp)**: Current time + TTL (typically 1-24 hours)
- **Proactive Refresh**: Refresh 5 minutes before expiration to avoid 401 errors

### Token Storage in Browser

Better Auth's `jwtClient()` plugin automatically stores the token in:
- **Storage Method**: localStorage (persists across page reloads)
- **Key**: `better_auth_jwt` (configurable)
- **Accessibility**: JavaScript-accessible (via localStorage API)

### Verifying Token on Backend

The backend (app/core/auth.py) verifies tokens using:
1. **Algorithm**: EdDSA (Ed25519)
2. **Source**: JWKS endpoint at `/api/auth/jwks`
3. **Validation**: Signature, issuer, audience, expiration
4. **Extraction**: `sub` claim → user_id for data isolation

### Frontend Usage Pattern

```typescript
// Get current session (includes verified token)
const { data: session, isPending } = useAuth();

if (session?.user?.id) {
  // User is authenticated, token is valid
  const userId = session.user.id;
  // Use in API calls
}

// Check token validity before API call
const token = await authClient.token();
if (token?.data?.token) {
  // Token is fresh, use it
  // Attach as: Authorization: Bearer <token>
}
```

---

## Notes for Frontend

1. **Token is automatically managed**: Better Auth's `jwtClient()` plugin handles storage, refresh, and expiration
2. **Don't manually decode for security**: Only extract `sub` without verification for non-critical use
3. **Always attach token to API calls**: Use Authorization header with Bearer token
4. **Handle 401 responses**: Token expired or invalid → redirect to /login
5. **Trust Backend Verification**: Backend (FastAPI dependency) verifies all tokens using JWKS
