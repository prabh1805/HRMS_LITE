"""Attendance service — validation and orchestration."""

from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exceptions import (
    AttendanceAlreadyMarkedException,
    EmployeeNotFoundException,
    NotFoundException,
)
from app.models.attendance import Attendance, AttendanceStatus
from app.repositories.attendance import AttendanceRepository
from app.repositories.employee import EmployeeRepository
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate, EmployeeAttendanceSummary


class AttendanceService:
    def __init__(self, db: AsyncSession) -> None:
        self._repo = AttendanceRepository(db)
        self._emp_repo = EmployeeRepository(db)

    async def mark_attendance(self, payload: AttendanceCreate) -> Attendance:
        # 1. Verify employee exists
        employee = await self._emp_repo.get_by_employee_id(payload.employee_id)
        if not employee:
            raise EmployeeNotFoundException(
                message=f"Employee '{payload.employee_id}' not found.",
                details={"employee_id": payload.employee_id},
            )

        # 2. Prevent duplicate attendance for the same date
        existing = await self._repo.check_existing_attendance(
            employee.id, payload.date
        )
        if existing:
            raise AttendanceAlreadyMarkedException(
                message=(
                    f"Attendance for employee '{payload.employee_id}' "
                    f"on {payload.date} is already recorded as '{existing.status}'."
                ),
                details={
                    "employee_id": payload.employee_id,
                    "date": str(payload.date),
                    "existing_status": existing.status,
                },
            )

        # 3. Persist
        attendance = Attendance(
            employee_id=employee.id,
            date=payload.date,
            status=payload.status,
        )
        return await self._repo.mark_attendance(attendance)

    async def get_attendance_by_employee(
        self, employee_id: str
    ) -> Sequence[Attendance]:
        employee = await self._emp_repo.get_by_employee_id(employee_id)
        if not employee:
            raise EmployeeNotFoundException(
                message=f"Employee '{employee_id}' not found.",
                details={"employee_id": employee_id},
            )
        return await self._repo.get_attendance_by_employee(employee.id)

    async def get_all_attendance(self, start_date: str | None = None, end_date: str | None = None) -> Sequence[Attendance]:
        return await self._repo.get_all_attendance(start_date, end_date)

    async def update_attendance(self, id: int, payload: AttendanceUpdate) -> Attendance:
        attendance = await self._repo.get_by_id(id)
        if not attendance:
            raise NotFoundException(
                message=f"Attendance record with id {id} not found.",
                details={"id": id},
            )
        
        # Update only provided fields
        if payload.status is not None:
            attendance.status = payload.status
        if payload.date is not None:
            # Check if changing date would create duplicate
            existing = await self._repo.check_existing_attendance(
                attendance.employee_id, payload.date
            )
            if existing and existing.id != id:
                raise AttendanceAlreadyMarkedException(
                    message=f"Attendance for this employee on {payload.date} already exists.",
                    details={"date": str(payload.date)},
                )
            attendance.date = payload.date
        
        await self._repo.update(attendance)
        return attendance

    async def delete_attendance(self, id: int) -> None:
        deleted = await self._repo.delete_by_id(id)
        if not deleted:
            raise NotFoundException(
                message=f"Attendance record with id {id} not found.",
                details={"id": id},
            )

    async def get_attendance_summary(self) -> list[EmployeeAttendanceSummary]:
        """Get attendance summary for all employees showing total present/absent days."""
        return await self._repo.get_attendance_summary()
