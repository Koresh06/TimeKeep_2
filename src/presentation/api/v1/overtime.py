from typing import Annotated
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Body, Depends, status

from src.application.dtos.overtime import OvertimeDTO
from src.application.mediator import Mediator
from src.application.use_cases.overtime.create import CreateOvertimeCommand
from src.application.use_cases.overtime.delete import DeleteOvertimeRequest
from src.application.use_cases.overtime.get_all import GetAllOvertimesQuery
from src.presentation.dependencies.auth import UserTokenData
from src.presentation.dependencies.permission import (
    get_require_user,
    get_require_moderator,
    get_require_admin,
    get_require_super_admin,
)
from src.presentation.schemas.overtime import (
    CreateOvertime,
    OvertimeResponse,
)

router = APIRouter(prefix="/overtime", tags=["overtime"])


@router.post(
    "/",
    response_model=OvertimeResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create(
    data: Annotated[CreateOvertime, Body()],
    mediator: FromDishka[Mediator],
    сurrent_user: UserTokenData = Depends(get_require_user()),
) -> OvertimeResponse:
    result: OvertimeDTO = await mediator.handle(
        CreateOvertimeCommand(
            **data.model_dump(),
            user_id=сurrent_user.user_id,
        )
    )
    return OvertimeResponse.model_validate(result, from_attributes=True)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[OvertimeResponse],
)
@inject
async def get_all(
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_super_admin()),
    offset: int = 0,
    limit: int = 20,
) -> list[OvertimeResponse]:
    result: list[OvertimeDTO] = await mediator.handle(
        GetAllOvertimesQuery(
            offset=offset,
            limit=limit,
        )
    )
    return [OvertimeResponse.model_validate(overtime, from_attributes=True) for overtime in result]


@router.get(
    "/current-organization",
    status_code=status.HTTP_200_OK,
    response_model=list[OvertimeResponse],
)
@inject
async def get_all_by_organization(
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_admin()),
    offset: int = 0,
    limit: int = 20,
) -> list[OvertimeResponse]:
    result: list[OvertimeDTO] = await mediator.handle(
        GetAllOvertimesQuery(
            organization_id=current_user.organization_id,
            offset=offset,
            limit=limit,
        )
    )
    return [OvertimeResponse.model_validate(overtime, from_attributes=True) for overtime in result]


@router.get(
    "/current-department",
    status_code=status.HTTP_200_OK,
    response_model=list[OvertimeResponse],
)
@inject
async def get_all_by_department(
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_moderator()),
    offset: int = 0,
    limit: int = 20,
) -> list[OvertimeResponse]:
    result: list[OvertimeDTO] = await mediator.handle(
        GetAllOvertimesQuery(
            department_id=current_user.department_id,
            offset=offset,
            limit=limit,
        )
    )
    return [OvertimeResponse.model_validate(overtime, from_attributes=True) for overtime in result]


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=list[OvertimeResponse],
)
@inject
async def get_all_me(
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_user()),
    offset: int = 0,
    limit: int = 20,
) -> list[OvertimeResponse]:
    result: list[OvertimeDTO] = await mediator.handle(
        GetAllOvertimesQuery(
            user_id=current_user.user_id,
            offset=offset,
            limit=limit,
        )
    )
    return [OvertimeResponse.model_validate(overtime, from_attributes=True) for overtime in result]


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
@inject
async def delete(
    id: int,
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_user()),
) -> None:
    await mediator.handle(
        DeleteOvertimeRequest(
            id=id,
            user_id=current_user.user_id,
        )
    )
