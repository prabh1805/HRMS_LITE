"""Dashboard statistics Pydantic schemas."""

from pydantic import BaseModel, Field


class DashboardStatsResponse(BaseModel):
    """Dashboard statistics response."""
    
    total_employees: int = Field(
        ...,
        description="Total number of employees in the system",
        examples=[150]
    )
    present_today: int = Field(
        ...,
        description="Number of employees marked present today",
        examples=[120]
    )
    absent_today: int = Field(
        ...,
        description="Number of employees marked absent today",
        examples=[30]
    )
    total_attendance_records: int = Field(
        ...,
        description="Total number of attendance records in the system",
        examples=[5000]
    )
