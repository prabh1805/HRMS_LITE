"""Aggregate all v1 routers into a single APIRouter."""

from fastapi import APIRouter

from app.api.v1 import health
from app.api.v1 import employees
from app.api.v1 import attendance
from app.api.v1 import dashboard

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(health.router)
v1_router.include_router(employees.router)
v1_router.include_router(attendance.router)
v1_router.include_router(dashboard.router)
