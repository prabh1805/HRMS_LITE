"""Employee service — business logic and validation."""

from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.exceptions import (
    EmployeeAlreadyExistsException,
    EmployeeNotFoundException,
)
from app.models.employee import Employee
from app.repositories.employee import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeService:
    def __init__(self, db: AsyncSession) -> None:
        self._repo = EmployeeRepository(db)

    async def _generate_employee_id(self) -> str:
        """Generate a unique employee ID in format EMP-XXXX."""
        employees = await self._repo.get_all()
        if not employees:
            return "EMP-0001"
        
        # Extract numeric parts and find the max
        max_num = 0
        for emp in employees:
            if emp.employee_id.startswith("EMP-"):
                try:
                    num = int(emp.employee_id.split("-")[1])
                    max_num = max(max_num, num)
                except (IndexError, ValueError):
                    continue
        
        return f"EMP-{max_num + 1:04d}"

    async def create_employee(self, payload: EmployeeCreate) -> Employee:
        # Auto-generate employee_id if not provided
        employee_id = payload.employee_id
        if not employee_id:
            employee_id = await self._generate_employee_id()
        
        existing = await self._repo.get_by_employee_id(employee_id)
        if existing:
            raise EmployeeAlreadyExistsException(
                message=f"Employee with ID '{employee_id}' already exists.",
                details={"employee_id": employee_id},
            )

        employee = Employee(
            employee_id=employee_id,
            full_name=payload.full_name,
            email=payload.email,
            department=payload.department,
        )
        return await self._repo.create(employee)

    async def get_all_employees(self) -> Sequence[Employee]:
        return await self._repo.get_all()

    async def update_employee(self, id: int, payload: EmployeeUpdate) -> Employee:
        employee = await self._repo.get_by_id(id)
        if not employee:
            raise EmployeeNotFoundException(
                message=f"Employee with id {id} not found.",
                details={"id": id},
            )
        
        # Update only provided fields
        if payload.full_name is not None:
            employee.full_name = payload.full_name
        if payload.email is not None:
            employee.email = payload.email
        if payload.department is not None:
            employee.department = payload.department
        
        await self._repo.update(employee)
        return employee

    async def delete_employee(self, id: int) -> None:
        deleted = await self._repo.delete_by_id(id)
        if not deleted:
            raise EmployeeNotFoundException(
                message=f"Employee with id {id} not found.",
                details={"id": id},
            )
