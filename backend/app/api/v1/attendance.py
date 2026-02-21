"""Attendance API router."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceResponse, EmployeeAttendanceSummary
from app.services.attendance import AttendanceService

router = APIRouter(prefix="/attendance", tags=["Attendance"])


def get_service(db: AsyncSession = Depends(get_db)) -> AttendanceService:
    return AttendanceService(db)


@router.post(
    "",
    response_model=AttendanceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Mark attendance for an employee",
    responses={
        400: {"description": "Attendance already recorded for this date"},
        404: {"description": "Employee not found"},
        422: {"description": "Validation error"},
    },
)
async def mark_attendance(
    payload: AttendanceCreate,
    service: AttendanceService = Depends(get_service),
) -> AttendanceResponse:
    record = await service.mark_attendance(payload)
    return AttendanceResponse.model_validate(record)


@router.get(
    "",
    response_model=List[AttendanceResponse],
    summary="Get all attendance records with optional date filtering",
)
async def get_all_attendance(
    start_date: str | None = None,
    end_date: str | None = None,
    service: AttendanceService = Depends(get_service),
) -> List[AttendanceResponse]:
    records = await service.get_all_attendance(start_date, end_date)
    responses = []
    for record in records:
        response_data = AttendanceResponse.model_validate(record)
        # Add employee info if available
        if hasattr(record, 'employee') and record.employee:
            response_data.employee_name = record.employee.full_name
            response_data.employee_code = record.employee.employee_id
        responses.append(response_data)
    return responses


@router.put(
    "/{id}",
    response_model=AttendanceResponse,
    summary="Update an attendance record",
    responses={
        404: {"description": "Attendance record not found"},
        400: {"description": "Duplicate attendance for the date"},
        422: {"description": "Validation error"},
    },
)
async def update_attendance(
    id: int,
    payload: AttendanceUpdate,
    service: AttendanceService = Depends(get_service),
) -> AttendanceResponse:
    record = await service.update_attendance(id, payload)
    return AttendanceResponse.model_validate(record)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an attendance record",
    responses={
        404: {"description": "Attendance record not found"},
    },
)
async def delete_attendance(
    id: int,
    service: AttendanceService = Depends(get_service),
) -> None:
    await service.delete_attendance(id)


@router.get(
    "/summary/by-employee",
    response_model=List[EmployeeAttendanceSummary],
    summary="Get attendance summary for all employees",
)
async def get_attendance_summary(
    service: AttendanceService = Depends(get_service),
) -> List[EmployeeAttendanceSummary]:
    return await service.get_attendance_summary()


@router.get(
    "/{employee_id}",
    response_model=List[AttendanceResponse],
    summary="Get all attendance records for an employee",
    responses={
        404: {"description": "Employee not found"},
    },
)
async def get_attendance(
    employee_id: str,
    service: AttendanceService = Depends(get_service),
) -> List[AttendanceResponse]:
    records = await service.get_attendance_by_employee(employee_id)
    return [AttendanceResponse.model_validate(r) for r in records]
