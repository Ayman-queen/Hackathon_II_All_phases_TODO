# Better Auth JWKS Implementation Guide

**Date**: 2025-12-29
**Status**: Implementation Ready
**Scope**: Migrate from HS256 symmetric JWT to EdDSA/Ed25519 with JWKS endpoint verification
**Branch**: `phase2-003-betterauth-migration`

---

## Executive Summary

This document provides step-by-step implementation details for adopting the official Better Auth JWT plugin architecture using EdDSA/Ed25519 asymmetric keys with JWKS endpoint verification.

**Current State**: HS256 with shared secret (WRONG)
**Target State**: EdDSA/Ed25519 with JWKS endpoint (CORRECT)
**Migration Impact**: 5 files modified, 1 new file created
**Estimated Time**: 2-3 hours implementation + 1 hour testing

---

## Implementation Checklist

- [ ] **Step 1**: Add PyJWT[crypto] dependency
- [ ] **Step 2**: Update configuration settings
- [ ] **Step 3**: Create JWKS client module
- [ ] **Step 4**: Rewrite auth module for JWKS
- [ ] **Step 5**: Update deps module exception handling
- [ ] **Step 6**: Update environment template
- [ ] **Step 7**: Test locally with environment variables

---

## Step-by-Step Implementation

### Step 1: Add PyJWT Dependency

**File**: `backend/pyproject.toml`

**Current**:
```toml
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn>=0.24.0",
    "sqlmodel>=0.0.14",
    "better-auth>=0.1.0",
    "pydantic-settings>=2.1.0",
    "psycopg>=3.1.0",
    "httpx>=0.25.0",
]
```

**Add**: `"PyJWT[crypto]>=2.8.0",`

**Rationale**: PyJWT provides `PyJWKClient` for automatic JWKS fetching with built-in caching, supporting Ed25519/EdDSA algorithm.

---

### Step 2: Update Configuration

**File**: `backend/app/core/config.py`

**Remove**:
- `BETTER_AUTH_SECRET: str = "..."`
- `JWT_ALGORITHM: str = "HS256"`
- `JWT_EXPIRATION_HOURS: int = 168`

**Add**:
```python
class Settings(BaseSettings):
    # Better Auth Configuration (Official JWT Plugin)
    BETTER_AUTH_URL: str = "http://localhost:3000"
    BETTER_AUTH_JWKS_URL: str = ""  # Computed if empty
    BETTER_AUTH_ISSUER: str = ""    # Defaults to BETTER_AUTH_URL
    BETTER_AUTH_AUDIENCE: str = ""  # Defaults to BETTER_AUTH_URL

    # JWKS Cache Configuration
    JWKS_CACHE_LIFESPAN: int = 300  # 5 minutes
    JWKS_CACHE_MAX_KEYS: int = 16

    def __init__(self, **data):
        super().__init__(**data)
        # Compute derived URLs
        if not self.BETTER_AUTH_JWKS_URL:
            self.BETTER_AUTH_JWKS_URL = f"{self.BETTER_AUTH_URL}/api/auth/jwks"
        if not self.BETTER_AUTH_ISSUER:
            self.BETTER_AUTH_ISSUER = self.BETTER_AUTH_URL
        if not self.BETTER_AUTH_AUDIENCE:
            self.BETTER_AUTH_AUDIENCE = self.BETTER_AUTH_URL
```

---

### Step 3: Create JWKS Client Module

**File**: `backend/app/core/jwks_client.py` (NEW FILE)

```python
"""
Better Auth JWKS Client for JWT Verification

Implements JWKS fetching and caching using PyJWT's PyJWKClient.
Supports key rotation via kid (key ID) and Ed25519/EdDSA algorithm.
"""

import logging
from typing import Optional

import jwt
from jwt import PyJWKClient, PyJWKClientError

from app.core.config import settings

logger = logging.getLogger(__name__)

# Global JWKS client instance (thread-safe)
_jwks_client: Optional[PyJWKClient] = None


def get_jwks_client() -> PyJWKClient:
    """
    Get or create the global JWKS client instance.

    The client is configured with:
    - JWKS endpoint URL from settings
    - Configurable cache lifespan (default 5 min)
    - Automatic key rotation support via kid
    - Network timeout for resilience

    Returns:
        PyJWKClient: Configured JWKS client with caching
    """
    global _jwks_client

    if _jwks_client is None:
        logger.info(f"Initializing JWKS client for {settings.BETTER_AUTH_JWKS_URL}")

        _jwks_client = PyJWKClient(
            uri=settings.BETTER_AUTH_JWKS_URL,
            cache_keys=True,
            max_cached_keys=settings.JWKS_CACHE_MAX_KEYS,
            cache_jwk_set=True,
            lifespan=settings.JWKS_CACHE_LIFESPAN,
            headers={"User-Agent": "Evo-TODO-Backend/1.0"},
            timeout=10,
        )
        logger.info("JWKS client initialized successfully")

    return _jwks_client


def refresh_jwks_cache() -> None:
    """
    Force refresh the JWKS cache.

    Call when:
    - JWT with unknown kid is received
    - Key rotation is suspected
    - Manual cache invalidation needed
    """
    global _jwks_client
    logger.info("Refreshing JWKS cache")
    _jwks_client = None


class JWKSFetchError(Exception):
    """Raised when JWKS cannot be fetched from Better Auth service."""
    pass


class JWKSKeyNotFoundError(Exception):
    """Raised when the key ID (kid) from JWT is not found in JWKS."""
    pass
```

---

### Step 4: Rewrite Auth Module

**File**: `backend/app/core/auth.py` (COMPLETE REWRITE)

```python
"""
Better Auth JWT Verification (Official JWT Plugin Architecture)

Uses EdDSA/Ed25519 asymmetric keys from JWKS endpoint.
Validates issuer and audience claims.
Supports key rotation via kid.
"""

import logging
from typing import Dict, Optional

import jwt
from jwt import PyJWKClient, PyJWKClientError
from jwt.exceptions import (
    InvalidTokenError,
    ExpiredSignatureError,
    InvalidAudienceError,
    InvalidIssuerError,
    DecodeError,
)

from app.core.config import settings
from app.core.jwks_client import (
    get_jwks_client,
    refresh_jwks_cache,
    JWKSFetchError,
)

logger = logging.getLogger(__name__)


async def verify_better_auth_token(token: str) -> Dict:
    """
    Verify and decode Better Auth JWT using EdDSA/JWKS.

    Flow:
    1. Get JWKS client (cached)
    2. Extract signing key using kid from JWT header
    3. Verify signature with Ed25519 public key
    4. Validate iss, aud, exp claims
    5. Return payload with user_id in 'sub' claim

    Args:
        token: JWT token from Authorization header

    Returns:
        Token payload dict with 'sub' (user_id)

    Raises:
        ValueError: If token invalid, expired, or verification fails
    """
    try:
        jwks_client = get_jwks_client()

        # Get signing key from JWKS based on kid in JWT header
        try:
            signing_key = jwks_client.get_signing_key_from_jwt(token)
        except PyJWKClientError as e:
            # Key not found - try refreshing JWKS cache once
            logger.warning(f"Key not found in JWKS cache, refreshing: {e}")
            refresh_jwks_cache()
            jwks_client = get_jwks_client()

            try:
                signing_key = jwks_client.get_signing_key_from_jwt(token)
            except PyJWKClientError as e:
                logger.error(f"Key still not found after JWKS refresh: {e}")
                raise ValueError("Token signing key not found in JWKS")

        # Verify and decode JWT with claim validation
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["EdDSA"],  # Better Auth default
            audience=settings.BETTER_AUTH_AUDIENCE,
            issuer=settings.BETTER_AUTH_ISSUER,
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_aud": True,
                "verify_iss": True,
                "require": ["sub", "exp", "iss", "aud"],
            }
        )

        # Ensure user_id (sub claim) is present
        user_id: str = payload.get("sub")
        if not user_id:
            raise ValueError("Token missing 'sub' (user_id) claim")

        logger.debug(f"Token verified for user: {user_id[:8]}...")
        return payload

    except ExpiredSignatureError:
        logger.warning("Token has expired")
        raise ValueError("Token has expired")
    except InvalidAudienceError:
        logger.warning(f"Invalid audience claim")
        raise ValueError("Invalid token audience")
    except InvalidIssuerError:
        logger.warning(f"Invalid issuer claim")
        raise ValueError("Invalid token issuer")
    except DecodeError as e:
        logger.warning(f"Token decode failed: {e}")
        raise ValueError("Invalid token format")
    except InvalidTokenError as e:
        logger.warning(f"Token validation failed: {e}")
        raise ValueError(f"Invalid token: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during token verification: {e}")
        raise ValueError("Token verification failed")


def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user_id from JWT token (without verification).

    Safely extracts user_id for non-critical paths.
    Does NOT verify signature or claims.

    Args:
        token: JWT token string

    Returns:
        User ID (from 'sub' claim) or None if invalid
    """
    try:
        unverified = jwt.decode(
            token,
            options={"verify_signature": False}
        )
        return unverified.get("sub")
    except Exception:
        return None
```

---

### Step 5: Update Dependencies Module

**File**: `backend/app/api/deps.py`

**Change imports**:
```python
# Before:
from jose import JWTError

# After:
from jwt.exceptions import InvalidTokenError
from app.core.jwks_client import JWKSFetchError
```

**Add 503 handling in get_current_user()**:
```python
try:
    payload = await verify_better_auth_token(token)
    # ... rest of verification
except JWKSFetchError:
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="Authentication service temporarily unavailable",
    )
except ValueError:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Unauthorized",
        headers={"WWW-Authenticate": "Bearer"},
    )
```

---

### Step 6: Update Environment Template

**File**: `backend/.env.example`

**Remove**:
```bash
BETTER_AUTH_SECRET=...
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=168
```

**Add**:
```bash
# Better Auth Configuration (Official JWT Plugin)
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_JWKS_URL=http://localhost:3000/api/auth/jwks
BETTER_AUTH_ISSUER=http://localhost:3000
BETTER_AUTH_AUDIENCE=http://localhost:3000
JWKS_CACHE_LIFESPAN=300
```

---

### Step 7: Testing Setup

For local testing, you need:

1. **Better Auth Service Running**:
   ```bash
   # In frontend directory
   npm run dev  # Better Auth serves at http://localhost:3000
   ```

2. **Environment Variables**:
   ```bash
   # backend/.env
   BETTER_AUTH_URL=http://localhost:3000
   BETTER_AUTH_JWKS_URL=http://localhost:3000/api/auth/jwks
   BETTER_AUTH_ISSUER=http://localhost:3000
   BETTER_AUTH_AUDIENCE=http://localhost:3000
   DATABASE_URL=postgresql://user:password@host:5432/evo_todo
   ```

3. **Test Cases**:
   ```bash
   # T-221: Import test
   python -c "from app.core.jwks_client import get_jwks_client; print('✓ JWKS client imported')"

   # T-222: Token verification
   curl -X GET http://localhost:8000/api/todos \
     -H "Authorization: Bearer <valid_jwt_token>"
   # Expected: 200 with todos

   # Missing token test
   curl -X GET http://localhost:8000/api/todos
   # Expected: 401 Unauthorized

   # Invalid token test
   curl -X GET http://localhost:8000/api/todos \
     -H "Authorization: Bearer invalid.token.here"
   # Expected: 401 Unauthorized
   ```

---

## Error Handling Summary

| Error Type | HTTP Status | Response |
|------------|-------------|----------|
| Missing token | 401 | "Unauthorized" |
| Invalid signature | 401 | "Unauthorized" |
| Expired token | 401 | "Unauthorized" |
| Invalid issuer/audience | 401 | "Unauthorized" |
| Token format error | 401 | "Unauthorized" |
| JWKS fetch failure | 503 | "Authentication service temporarily unavailable" |
| User not in database | 401 | "Unauthorized" |
| User deactivated | 401 | "Unauthorized" |

---

## Verification Checklist

After implementation, verify:

- [ ] `PyJWT[crypto]>=2.8.0` installed and importable
- [ ] Config settings have BETTER_AUTH_URL, JWKS_URL, issuer, audience
- [ ] JWKS client caches keys with 5-minute TTL
- [ ] Token verification uses EdDSA algorithm (not HS256)
- [ ] Issuer and audience are validated
- [ ] Key rotation (kid mismatch) triggers JWKS refresh
- [ ] Missing token returns 401 Unauthorized
- [ ] Invalid token returns 401 Unauthorized
- [ ] Valid token allows access to /api/todos
- [ ] User A cannot access User B's todos
- [ ] Database queries filtered by user_id from token

---

## Rollback Plan

If implementation fails:

1. Revert `backend/app/core/auth.py` to HS256 version
2. Revert `backend/app/core/config.py` to use BETTER_AUTH_SECRET
3. Revert `backend/pyproject.toml` dependencies
4. Delete `backend/app/core/jwks_client.py`
5. Revert `backend/app/api/deps.py` imports

No database changes required (Neon config unchanged).

---

## Next Steps After Implementation

1. Update frontend to use Better Auth JWT client
2. Run integration tests with real Better Auth service
3. Deploy to staging with Neon PostgreSQL
4. Document JWT/JWKS configuration in README
