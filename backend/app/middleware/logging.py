"""Async logging middleware — logs every request and its response."""

import logging
import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("hrms.access")


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs each HTTP request/response cycle with:
      - Unique request ID (X-Request-ID header)
      - Method, path, query string
      - Response status code
      - Wall-clock duration in milliseconds
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = str(uuid.uuid4())
        start = time.perf_counter()

        # Attach request ID so downstream code / other middleware can read it
        request.state.request_id = request_id

        logger.info(
            "→ [%s] %s %s%s",
            request_id,
            request.method,
            request.url.path,
            f"?{request.url.query}" if request.url.query else "",
        )

        try:
            response: Response = await call_next(request)
        except Exception:
            elapsed = (time.perf_counter() - start) * 1000
            logger.exception(
                "← [%s] UNHANDLED EXCEPTION after %.1f ms",
                request_id,
                elapsed,
            )
            raise

        elapsed = (time.perf_counter() - start) * 1000
        logger.info(
            "← [%s] %s %.1f ms",
            request_id,
            response.status_code,
            elapsed,
        )

        # Propagate the ID back to the client for correlation
        response.headers["X-Request-ID"] = request_id
        return response
