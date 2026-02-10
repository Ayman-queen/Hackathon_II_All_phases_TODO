"""
Task T-221: Better Auth JWKS Client for JWT Verification

This module implements JWKS fetching and caching for Better Auth JWT plugin.
Uses PyJWT's PyJWKClient for automatic key management and caching.

Key Features:
- Fetches JWKS from Better Auth service endpoint (/api/auth/jwks)
- Caches keys with configurable lifespan (default 5 minutes)
- Handles key rotation via kid (key ID)
- Supports Ed25519/EdDSA algorithm (Better Auth default)
- Thread-safe singleton pattern for global client

Phase II Constitution Compliance:
- Better Auth manages user authentication (frontend signup/signin)
- Backend validates Better Auth JWTs via JWKS endpoint
- EdDSA asymmetric verification (official Better Auth plugin)
- User_id extracted from JWT 'sub' claim for data isolation
"""

import logging
from typing import Optional
import threading

import jwt
from jwt import PyJWKClient, PyJWKClientError

from app.core.config import settings

logger = logging.getLogger(__name__)

# Global JWKS client instance (thread-safe, singleton)
_jwks_client: Optional[PyJWKClient] = None
_jwks_client_lock = threading.Lock()  # Thread safety for concurrent initialization


def get_jwks_client() -> PyJWKClient:
    """
    Get or create the global JWKS client instance (thread-safe singleton).

    The client is configured with:
    - JWKS endpoint URL from settings (BETTER_AUTH_JWKS_URL)
    - Caching enabled with configurable lifespan
    - Support for key rotation via kid (key ID)
    - Headers for Better Auth compatibility
    - Timeout for network resilience

    Returns:
        PyJWKClient: Configured JWKS client with caching

    Thread Safety:
        This function is thread-safe using a threading.Lock. Multiple threads
        can call it concurrently and will share the same client instance.
        Only the first thread to acquire the lock initializes the client.

    Example:
        >>> client = get_jwks_client()
        >>> signing_key = client.get_signing_key_from_jwt(token)
    """
    global _jwks_client

    if _jwks_client is None:
        # Use lock to ensure only one thread initializes the client
        with _jwks_client_lock:
            # Double-check pattern: another thread might have initialized while waiting for lock
            if _jwks_client is None:
                logger.info(f"Initializing JWKS client for {settings.BETTER_AUTH_JWKS_URL}")

                _jwks_client = PyJWKClient(
                    uri=settings.BETTER_AUTH_JWKS_URL,
                    cache_keys=True,
                    max_cached_keys=settings.JWKS_CACHE_MAX_KEYS,
                    cache_jwk_set=True,
                    lifespan=settings.JWKS_CACHE_LIFESPAN,
                    headers={"User-Agent": "Evo-TODO-Backend/1.0"},
                    timeout=10,  # 10 second timeout for JWKS fetch
                )

                logger.info("JWKS client initialized successfully")

    return _jwks_client


def refresh_jwks_cache() -> None:
    """
    Force refresh the JWKS cache.

    Call this when:
    - A JWT with unknown kid is received
    - Key rotation is suspected
    - Manual cache invalidation is needed

    Note: This clears the global client, forcing re-creation on next use.
          New instance will fetch fresh JWKS from endpoint.

    Example:
        >>> refresh_jwks_cache()
        >>> client = get_jwks_client()  # New instance with fresh JWKS
    """
    global _jwks_client
    logger.info("Refreshing JWKS cache")
    _jwks_client = None


class JWKSFetchError(Exception):
    """
    Raised when JWKS cannot be fetched from Better Auth service.

    This typically indicates:
    - Better Auth service is down or unreachable
    - Network connectivity issue
    - Incorrect JWKS URL configuration

    Response: HTTP 503 Service Unavailable
    """
    pass


class JWKSKeyNotFoundError(Exception):
    """
    Raised when the key ID (kid) from JWT is not found in JWKS.

    This typically indicates:
    - Key rotation happened and old keys are no longer available
    - JWT was signed with a different Better Auth instance
    - Token is forged or tampered

    Response: HTTP 401 Unauthorized (after JWKS refresh attempt)
    """
    pass
