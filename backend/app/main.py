"""FastAPI application entry point."""

import logging
import logging.config
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.api.v1.router import v1_router
from app.config import get_settings
from app.exceptions.handlers import register_exception_handlers
from app.middleware.logging import LoggingMiddleware

settings = get_settings()


# ── Logging configuration ─────────────────────────────────────────────────────
LOGGING_CONFIG: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "level": "DEBUG" if settings.debug else "INFO",
        "handlers": ["console"],
    },
    "loggers": {
        # Reduce SQLAlchemy noise in production
        "sqlalchemy.engine": {
            "level": "DEBUG" if settings.debug else "WARNING",
            "propagate": False,
            "handlers": ["console"],
        },
        "uvicorn.access": {
            # Replaced by our own LoggingMiddleware
            "level": "WARNING",
            "propagate": False,
            "handlers": ["console"],
        },
    },
}


# ── Lifespan ──────────────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logging.config.dictConfig(LOGGING_CONFIG)
    logging.getLogger(__name__).info("🚀  %s v%s starting up", settings.app_name, settings.app_version)
    yield
    logging.getLogger(__name__).info("🛑  %s shutting down", settings.app_name)


# ── Application factory ───────────────────────────────────────────────────────
def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Middleware (added in reverse order of execution)
    application.add_middleware(LoggingMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handlers
    register_exception_handlers(application)

    # Routers
    application.include_router(v1_router)

    # Root endpoint - redirect to docs
    @application.get("/", include_in_schema=False)
    async def root():
        """Redirect root to API documentation."""
        return RedirectResponse(url="/docs")

    return application


app = create_application()
