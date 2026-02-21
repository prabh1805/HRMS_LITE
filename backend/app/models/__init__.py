"""Models package — import all model modules here so Alembic can detect them."""

from app.models.base import TimestampMixin  # noqa: F401
from app.models.employee import Employee  # noqa: F401
from app.models.attendance import Attendance  # noqa: F401

__all__ = ["TimestampMixin", "Employee", "Attendance"]
