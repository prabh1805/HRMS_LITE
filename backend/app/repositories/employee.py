"""Employee repository — all direct DB interactions live here."""

from typing import Sequence

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee import Employee


class EmployeeRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create(self, employee: Employee) -> Employee:
        self._db.add(employee)
        await self._db.flush()        # Populate generated fields (id, timestamps)
        await self._db.refresh(employee)
        return employee

    async def get_all(self) -> Sequence[Employee]:
        result = await self._db.execute(select(Employee).order_by(Employee.id))
        return result.scalars().all()

    async def get_by_employee_id(self, employee_id: str) -> Employee | None:
        result = await self._db.execute(
            select(Employee).where(Employee.employee_id == employee_id)
        )
        return result.scalar_one_or_none()

    async def get_by_id(self, id: int) -> Employee | None:
        result = await self._db.execute(
            select(Employee).where(Employee.id == id)
        )
        return result.scalar_one_or_none()

    async def delete_by_id(self, id: int) -> bool:
        result = await self._db.execute(
            delete(Employee).where(Employee.id == id)
        )
        return result.rowcount > 0

    async def update(self, employee: Employee) -> Employee:
        await self._db.flush()
        await self._db.refresh(employee)
        return employee
