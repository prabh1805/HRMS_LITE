"""Attendance request / response Pydantic schemas."""

from datetime import date as date_type, datetime as datetime_type
from typing import Annotated, Optional

from pydantic import BaseModel, Field

from app.models.attendance import AttendanceStatus


# ── Request ───────────────────────────────────────────────────────────────────

class AttendanceCreate(BaseModel):
    employee_id: Annotated[str, Field(
        examples=["EMP-001"],
        description="The employee_id string (e.g. EMP-001), NOT the internal DB id.",
    )]
    date: Annotated[date_type, Field(
        examples=["2026-02-21"],
        description="Attendance date in ISO-8601 format (YYYY-MM-DD).",
    )]
    status: Annotated[AttendanceStatus, Field(
        examples=[AttendanceStatus.PRESENT],
    )]


class AttendanceUpdate(BaseModel):
    date: Optional[date_type] = Field(
        None,
        examples=["2026-02-21"],
        description="Attendance date in ISO-8601 format (YYYY-MM-DD).",
    )
    status: Optional[AttendanceStatus] = Field(
        None,
        examples=[AttendanceStatus.PRESENT],
    )


# ── Response ──────────────────────────────────────────────────────────────────

class AttendanceResponse(BaseModel):
    id: int
    employee_id: int          # internal FK (DB id)
    date: date_type
    status: AttendanceStatus
    created_at: datetime_type
    updated_at: datetime_type
    # Additional fields for display
    employee_name: Optional[str] = None
    employee_code: Optional[str] = None

    model_config = {"from_attributes": True}


class EmployeeAttendanceSummary(BaseModel):
    employee_id: str
    employee_name: str
    total_present_days: int
    total_absent_days: int
    total_days: int

    model_config = {"from_attributes": True}
