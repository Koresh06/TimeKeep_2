from io import BytesIO
from typing import Annotated
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Body, Depends, Query, status
from fastapi.responses import StreamingResponse

from src.application.use_cases.day_off.moderate import ModerateDayOffCommand
from src.application.use_cases.document.generate_report import GenerateReportCommand
from src.domain.enums.day_off_status import DayOffStatus
from src.application.mediator import Mediator
from src.application.dtos.day_off import DayOffDTO
from src.application.use_cases.day_off.get_all import GetAllDayOffsQuery
from src.application.use_cases.day_off.take import TakeDayOffCommand
from src.presentation.dependencies.auth import UserTokenData
from src.presentation.schemas.day_off import (
    CreateDayOff,
    DayOffResponse,
    ModerateDayOff,
)
from src.presentation.dependencies.permission import (
    get_require_admin,
    get_require_moderator,
    get_require_user,
    get_require_super_admin,
)


router = APIRouter(prefix="/day-offs", tags=["day-off"])


@router.post(
    "",
    response_model=DayOffResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create(
    data: Annotated[CreateDayOff, Body()],
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_user()),
) -> DayOffResponse:
    result: DayOffDTO = await mediator.handle(
        TakeDayOffCommand(
            user_id=current_user.user_id,
            date_=data.date_,
        )
    )
    return DayOffResponse.model_validate(result, from_attributes=True)


@router.get(
    "/me",
    response_model=list[DayOffResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_all_me(
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_user()),
    status: DayOffStatus | None = None,
    offset: int = 0,
    limit: int = 20,
) -> list[DayOffResponse]:
    result: list[DayOffDTO] = await mediator.handle(
        GetAllDayOffsQuery(
            user_id=current_user.user_id,
            status=status,
            offset=offset,
            limit=limit,
        )
    )
    return [
        DayOffResponse.model_validate(day_off, from_attributes=True)
        for day_off in result
    ]


@router.get(
    "/current-department",
    response_model=list[DayOffResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_all_by_department(
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_moderator()),
    status: DayOffStatus | None = None,
    offset: int = 0,
    limit: int = 20,
) -> list[DayOffResponse]:
    result: list[DayOffDTO] = await mediator.handle(
        GetAllDayOffsQuery(
            department_id=current_user.department_id,
            status=status,
            offset=offset,
            limit=limit,
        )
    )
    return [
        DayOffResponse.model_validate(day_off, from_attributes=True)
        for day_off in result
    ]


@router.get(
    "/current-organization",
    response_model=list[DayOffResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_all_by_organization(
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_admin()),
    status: DayOffStatus | None = None,
    offset: int = 0,
    limit: int = 20,
) -> list[DayOffResponse]:
    result: list[DayOffDTO] = await mediator.handle(
        GetAllDayOffsQuery(
            organization_id=current_user.organization_id,
            status=status,
            offset=offset,
            limit=limit,
        )
    )
    return [
        DayOffResponse.model_validate(day_off, from_attributes=True)
        for day_off in result
    ]


@router.get(
    "",
    response_model=list[DayOffResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_all_by_super_admin(
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_super_admin()),
    status: DayOffStatus | None = None,
    offset: int = 0,
    limit: int = 20,
) -> list[DayOffResponse]:
    result: list[DayOffDTO] = await mediator.handle(
        GetAllDayOffsQuery(
            status=status,
            offset=offset,
            limit=limit,
        )
    )
    return [
        DayOffResponse.model_validate(day_off, from_attributes=True)
        for day_off in result
    ]


@router.patch(
    "/{id}/moderate",
    response_model=None,
    status_code=status.HTTP_200_OK,
)
@inject
async def moderate(
    id: int,
    data: Annotated[ModerateDayOff, Query()],
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_moderator()),
) -> None:
    await mediator.handle(
        ModerateDayOffCommand(
            day_off_id=id,
            moderation_id=current_user.user_id,
            is_approved=data.is_approved,
        )
    )


@router.get(
    "/{id}/report",
    status_code=status.HTTP_200_OK,
)
@inject
async def generate_document(
    id: int,
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_user()),
) -> StreamingResponse:
    data: bytes = await mediator.handle(
        GenerateReportCommand(
            user_id=current_user.user_id,
            day_off_id=id,
        )
    )
    return StreamingResponse(
        BytesIO(data),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f"attachment; filename=report_{id}.docx"},
    )
