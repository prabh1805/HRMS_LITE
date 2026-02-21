"""Domain-specific exception classes for HRMSLite."""

from fastapi import status


# ── Base ──────────────────────────────────────────────────────────────────────

class AppException(Exception):
    """Root exception for all application errors."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    message: str = "An unexpected error occurred."

    def __init__(self, message: str | None = None, details: object = None) -> None:
        self.message = message or self.__class__.message
        self.details = details
        super().__init__(self.message)


# ── Employee ──────────────────────────────────────────────────────────────────

class EmployeeAlreadyExistsException(AppException):
    """Raised when trying to create an employee whose employee_id already exists."""

    status_code = status.HTTP_400_BAD_REQUEST
    message = "Employee already exists."


class EmployeeNotFoundException(AppException):
    """Raised when an employee lookup returns no result."""

    status_code = status.HTTP_404_NOT_FOUND
    message = "Employee not found."


# ── Attendance ────────────────────────────────────────────────────────────────

class AttendanceAlreadyMarkedException(AppException):
    """Raised when attendance for an employee on a given date is already recorded."""

    status_code = status.HTTP_400_BAD_REQUEST
    message = "Attendance already marked for this date."


# ── Generic HTTP helpers (kept for general use) ───────────────────────────────

class NotFoundException(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Resource not found."


class BadRequestException(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Bad request."


class UnauthorizedException(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = "Unauthorized."


class ForbiddenException(AppException):
    status_code = status.HTTP_403_FORBIDDEN
    message = "Forbidden."
