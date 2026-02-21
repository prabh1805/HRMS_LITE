"""Schemas for the health-check endpoint."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(..., examples=["ok"])
    version: str = Field(..., examples=["0.1.0"])

    model_config = {"json_schema_extra": {"example": {"status": "ok", "version": "0.1.0"}}}
