"""Dashboard statistics endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.attendance import Attendance, AttendanceStatus
from app.models.employee import Employee
from app.schemas.dashboard import DashboardStatsResponse

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/stats", response_model=DashboardStatsResponse)
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """
    Get dashboard statistics including:
    - Total employees
    - Present today
    - Absent today
    - Total attendance records
    """
    
    # Total employees
    total_employees_query = select(func.count(Employee.id))
    total_employees_result = await db.execute(total_employees_query)
    total_employees = total_employees_result.scalar() or 0
    
    # Present today
    present_today_query = select(func.count(Attendance.id)).where(
        Attendance.date == func.current_date(),
        Attendance.status == AttendanceStatus.PRESENT
    )
    present_today_result = await db.execute(present_today_query)
    present_today = present_today_result.scalar() or 0
    
    # Absent today
    absent_today_query = select(func.count(Attendance.id)).where(
        Attendance.date == func.current_date(),
        Attendance.status == AttendanceStatus.ABSENT
    )
    absent_today_result = await db.execute(absent_today_query)
    absent_today = absent_today_result.scalar() or 0
    
    # Total attendance records
    total_records_query = select(func.count(Attendance.id))
    total_records_result = await db.execute(total_records_query)
    total_records = total_records_result.scalar() or 0
    
    return DashboardStatsResponse(
        total_employees=total_employees,
        present_today=present_today,
        absent_today=absent_today,
        total_attendance_records=total_records
    )
