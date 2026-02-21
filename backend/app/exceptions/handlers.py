"""
Global exception handlers — registered on the FastAPI application.

Every error response follows the same JSON envelope:

    {
        "success": false,
        "message": "Human-readable summary",
        "details": <null | string | list | object>
    }
"""

import logging

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions.exceptions import AppException

logger = logging.getLogger(__name__)


# ── Envelope builder ──────────────────────────────────────────────────────────

def _error_response(
    status_code: int,
    message: str,
    details: object = None,
) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "details": details,
        },
    )


# ── Handler registration ──────────────────────────────────────────────────────

def register_exception_handlers(app: FastAPI) -> None:
    """Attach all exception handlers to *app*."""

    # 1. Domain exceptions (AppException subclasses)
    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request, exc: AppException
    ) -> JSONResponse:
        logger.warning(
            "AppException [%s %s] %s — %s",
            request.method,
            request.url.path,
            exc.__class__.__name__,
            exc.message,
        )
        return _error_response(
            status_code=exc.status_code,
            message=exc.message,
            details=exc.details,
        )

    # 2. FastAPI / Starlette HTTPException
    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request, exc: HTTPException
    ) -> JSONResponse:
        logger.warning(
            "HTTPException [%s %s] %s — %s",
            request.method,
            request.url.path,
            exc.status_code,
            exc.detail,
        )
        return _error_response(
            status_code=exc.status_code,
            message=str(exc.detail),
        )

    # 3. Pydantic RequestValidationError (422)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        # Flatten Pydantic errors into a readable list
        details = [
            {
                "field": " → ".join(str(loc) for loc in err["loc"] if loc != "body"),
                "message": err["msg"],
                "type": err["type"],
            }
            for err in exc.errors()
        ]
        logger.info(
            "ValidationError [%s %s]: %s",
            request.method,
            request.url.path,
            details,
        )
        return _error_response(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message="Request validation failed.",
            details=details,
        )

    # 4. Catch-all for unexpected errors
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception(
            "Unhandled exception [%s %s]",
            request.method,
            request.url.path,
        )
        return _error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="An unexpected internal server error occurred.",
        )
