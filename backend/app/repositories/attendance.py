"""Attendance repository — all direct DB interactions live here."""

from datetime import date
from typing import Sequence

from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.attendance import Attendance, AttendanceStatus
from app.models.employee import Employee


class AttendanceRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def mark_attendance(self, attendance: Attendance) -> Attendance:
        self._db.add(attendance)
        await self._db.flush()
        await self._db.refresh(attendance)
        return attendance

    async def get_attendance_by_employee(
        self, employee_id: int
    ) -> Sequence[Attendance]:
        result = await self._db.execute(
            select(Attendance)
            .where(Attendance.employee_id == employee_id)
            .order_by(Attendance.date.desc())
        )
        return result.scalars().all()

    async def check_existing_attendance(
        self, employee_id: int, attendance_date: date
    ) -> Attendance | None:
        result = await self._db.execute(
            select(Attendance).where(
                Attendance.employee_id == employee_id,
                Attendance.date == attendance_date,
            )
        )
        return result.scalar_one_or_none()

    async def get_all_attendance(self, start_date: str | None = None, end_date: str | None = None) -> Sequence[Attendance]:
        query = select(Attendance).options(joinedload(Attendance.employee))
        
        # Apply date filters if provided
        if start_date:
            query = query.where(Attendance.date >= start_date)
        if end_date:
            query = query.where(Attendance.date <= end_date)
        
        query = query.order_by(Attendance.date.desc())
        result = await self._db.execute(query)
        return result.unique().scalars().all()

    async def get_by_id(self, id: int) -> Attendance | None:
        result = await self._db.execute(
            select(Attendance).where(Attendance.id == id)
        )
        return result.scalar_one_or_none()

    async def update(self, attendance: Attendance) -> Attendance:
        await self._db.flush()
        await self._db.refresh(attendance)
        return attendance

    async def delete_by_id(self, id: int) -> bool:
        from sqlalchemy import delete as sql_delete
        result = await self._db.execute(
            sql_delete(Attendance).where(Attendance.id == id)
        )
        return result.rowcount > 0

    async def get_attendance_summary(self):
        """Get attendance summary for all employees using a single optimized query."""
        from app.schemas.attendance import EmployeeAttendanceSummary
        
        # Single query with aggregation - much faster than N+1 queries
        query = (
            select(
                Employee.employee_id,
                Employee.full_name,
                func.count(Attendance.id).label('total_days'),
                func.sum(
                    case((Attendance.status == AttendanceStatus.PRESENT, 1), else_=0)
                ).label('total_present'),
                func.sum(
                    case((Attendance.status == AttendanceStatus.ABSENT, 1), else_=0)
                ).label('total_absent'),
            )
            .select_from(Employee)
            .outerjoin(Attendance, Employee.id == Attendance.employee_id)
            .group_by(Employee.id, Employee.employee_id, Employee.full_name)
            .order_by(Employee.employee_id)
        )
        
        result = await self._db.execute(query)
        rows = result.all()
        
        summaries = []
        for row in rows:
            summaries.append(
                EmployeeAttendanceSummary(
                    employee_id=row.employee_id,
                    employee_name=row.full_name,
                    total_days=row.total_days or 0,
                    total_present_days=row.total_present or 0,
                    total_absent_days=row.total_absent or 0,
                )
            )
        
        return summaries
