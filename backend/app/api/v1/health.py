"""Health check endpoint."""

from fastapi import APIRouter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.config import get_settings
from app.database import get_db
from app.schemas.health import HealthResponse

router = APIRouter(prefix="/health", tags=["Health"])

settings = get_settings()


@router.get(
    "",
    response_model=HealthResponse,
    summary="Application health check",
    description="Returns `ok` when the API and database are reachable.",
)
async def health_check(db: AsyncSession = Depends(get_db)) -> HealthResponse:
    # Lightweight DB ping — raises if the connection is broken
    await db.execute(text("SELECT 1"))
    return HealthResponse(status="ok", version=settings.app_version)
