"""Employee API router — POST / GET / PUT / DELETE endpoints."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from app.services.employee import EmployeeService

router = APIRouter(prefix="/employees", tags=["Employees"])


def get_service(db: AsyncSession = Depends(get_db)) -> EmployeeService:
    return EmployeeService(db)


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee",
    responses={
        400: {"description": "Duplicate employee_id"},
        422: {"description": "Validation error"},
    },
)
async def create_employee(
    payload: EmployeeCreate,
    service: EmployeeService = Depends(get_service),
) -> EmployeeResponse:
    employee = await service.create_employee(payload)
    return EmployeeResponse.model_validate(employee)


@router.get(
    "",
    response_model=List[EmployeeResponse],
    summary="List all employees",
)
async def list_employees(
    service: EmployeeService = Depends(get_service),
) -> List[EmployeeResponse]:
    employees = await service.get_all_employees()
    return [EmployeeResponse.model_validate(e) for e in employees]


@router.put(
    "/{id}",
    response_model=EmployeeResponse,
    summary="Update an employee by internal ID",
    responses={
        404: {"description": "Employee not found"},
        422: {"description": "Validation error"},
    },
)
async def update_employee(
    id: int,
    payload: EmployeeUpdate,
    service: EmployeeService = Depends(get_service),
) -> EmployeeResponse:
    employee = await service.update_employee(id, payload)
    return EmployeeResponse.model_validate(employee)


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an employee by internal ID",
    responses={
        404: {"description": "Employee not found"},
    },
)
async def delete_employee(
    id: int,
    service: EmployeeService = Depends(get_service),
) -> None:
    await service.delete_employee(id)
