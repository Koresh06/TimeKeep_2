from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, status

from src.application.dtos.statistics import StatisticsDTO
from src.application.mediator import Mediator
from src.application.use_cases.statistics.get_statistics import GetStatisticsQuery
from src.presentation.dependencies.auth import UserTokenData
from src.presentation.dependencies.permission import (
    get_require_admin,
    get_require_moderator,
    get_require_super_admin,
    get_require_user,
)
from src.presentation.schemas.statistics import StatisticsResponse

router = APIRouter(prefix="/statistics", tags=["statistics"])


@router.get(
    "/me",
    response_model=StatisticsResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_my_stats(
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_user()),
) -> StatisticsResponse:
    result: StatisticsDTO = await mediator.handle(
        GetStatisticsQuery(user_id=current_user.user_id)
    )
    return StatisticsResponse.model_validate(result, from_attributes=True)


@router.get(
    "/current-department",
    response_model=StatisticsResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_department_stats(
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_moderator()),
) -> StatisticsResponse:
    result: StatisticsDTO = await mediator.handle(
        GetStatisticsQuery(department_id=current_user.department_id)
    )
    return StatisticsResponse.model_validate(result, from_attributes=True)


@router.get(
    "/current-organization",
    response_model=StatisticsResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_organization_stats(
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_admin()),
) -> StatisticsResponse:
    result: StatisticsDTO = await mediator.handle(
        GetStatisticsQuery(organization_id=current_user.organization_id)
    )
    return StatisticsResponse.model_validate(result, from_attributes=True)


@router.get("", response_model=StatisticsResponse, status_code=status.HTTP_200_OK)
@inject
async def get_all_stats(
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_super_admin()),
) -> StatisticsResponse:
    result: StatisticsDTO = await mediator.handle(GetStatisticsQuery())
    return StatisticsResponse.model_validate(result, from_attributes=True)
