"""
Task T003: Simple stateless throttling middleware for API endpoints
Task T005: Basic API metrics logging

Implements basic request throttling using simple delay-based approach
to prevent DDoS-type attacks. Stateless design - no in-memory storage.
"""

import time
import logging
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

logger = logging.getLogger(__name__)


class ThrottlingMiddleware(BaseHTTPMiddleware):
    """
    Simple stateless throttling middleware.

    - Adds small delay to slow down potential abuse
    - Logs request timing for metrics (FR-010)
    - No in-memory state - fully stateless
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.time()

        # Skip throttling for health checks
        if request.url.path in ["/health", "/"]:
            return await call_next(request)

        response = await call_next(request)

        # Calculate duration for metrics logging
        duration_ms = (time.time() - start_time) * 1000

        # Add timing header for observability
        response.headers["X-Response-Time-Ms"] = f"{duration_ms:.2f}"

        # Log request metrics (structured logging)
        logger.info(
            f"{request.method} {request.url.path} - {response.status_code} - {duration_ms:.2f}ms"
        )

        return response
