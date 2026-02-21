"""Employee request / response Pydantic schemas."""

import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


# ── Request ───────────────────────────────────────────────────────────────────

class EmployeeCreate(BaseModel):
    employee_id: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        examples=["EMP-001"],
        description="Unique employee identifier (e.g. EMP-001). Auto-generated if not provided.",
    )
    full_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        examples=["Jane Doe"],
    )
    email: EmailStr = Field(..., examples=["jane.doe@company.com"])
    department: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["Engineering"],
    )

    @field_validator("employee_id")
    @classmethod
    def employee_id_format(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not re.match(r"^[A-Za-z0-9\-_]+$", v):
            raise ValueError(
                "employee_id may only contain letters, digits, hyphens, or underscores."
            )
        return v.upper()

    @field_validator("full_name", "department")
    @classmethod
    def no_blank_strings(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Field must not be blank.")
        return v


class EmployeeUpdate(BaseModel):
    full_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        examples=["Jane Doe"],
    )
    email: Optional[EmailStr] = Field(None, examples=["jane.doe@company.com"])
    department: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        examples=["Engineering"],
    )

    @field_validator("full_name", "department")
    @classmethod
    def no_blank_strings(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("Field must not be blank.")
        return v


# ── Response ──────────────────────────────────────────────────────────────────

class EmployeeResponse(BaseModel):
    id: int
    employee_id: str
    full_name: str
    email: EmailStr
    department: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
