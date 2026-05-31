from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.domain.exceptions.base import TimeKeepError
from src.domain.exceptions.user import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    UserNotFoundError,
    UserNotModeratorError,
)
from src.domain.exceptions.overtime import (
    AccessDeniedError,
    OvertimeOverlapError,
    OvertimeAlreadyUsedError,
    OvertimeNotFoundError,
)
from src.domain.exceptions.day_off import (
    DayOffAccessDeniedError,
    DayOffAlreadyModeratedError,
    NotEnoughHoursError,
    DayOffNotApprovedError,
    DayOffNotFoundError,
    DayOffInvalidDateError,
    DayOffAlreadyExistsForDateError,
)
from src.domain.exceptions.organization import (
    OrganizationNotFoundError,
    OrganizationAlreadyExistsError,
)
from src.domain.exceptions.department import (
    DepartmentNotFoundError,
    DepartmentAlreadyExistsError,
)
from src.presentation.exceptions.rate_limit import RateLimitExceededException


EXCEPTION_STATUS_MAP = {
    NotEnoughHoursError: 400,
    OvertimeOverlapError: 409,
    UserAlreadyExistsError: 409,
    DayOffAlreadyModeratedError: 409,
    InvalidCredentialsError: 401,
    AccessDeniedError: 403,
    DayOffAccessDeniedError: 403,
    UserNotFoundError: 404,
    DayOffNotFoundError: 404,
    DayOffInvalidDateError: 400,
    DayOffAlreadyExistsForDateError: 409,
    OrganizationNotFoundError: 404,
    OrganizationAlreadyExistsError: 409,
    DepartmentNotFoundError: 404,
    DepartmentAlreadyExistsError: 409,
    OvertimeNotFoundError: 404,
    OvertimeAlreadyUsedError: 409,
    DayOffNotApprovedError: 400,
    UserNotModeratorError: 403,
}


async def timekeep_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    status_code = EXCEPTION_STATUS_MAP.get(type(exc), 500)
    return JSONResponse(
        status_code=status_code,
        content={"detail": str(exc)},
    )


async def rate_limit_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={"detail": str(exc)},
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(TimeKeepError, timekeep_exception_handler)
    app.add_exception_handler(RateLimitExceededException, rate_limit_exception_handler)
