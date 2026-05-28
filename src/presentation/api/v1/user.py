from typing import Annotated
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Body, Depends, Query, status

from src.application.dtos.user import UserDTO
from src.application.mediator import Mediator
from src.application.use_cases.user.activate_user import ActivateUserCommand
from src.application.use_cases.user.get_all import GetAllUsersQuery
from src.application.use_cases.user.get_by_id import GetUserByIdQuery
from src.application.use_cases.user.update_role import UpdateUserRoleCommand
from src.application.use_cases.user.update_work_mode import UpdateUserWorkModeCommand
from src.presentation.dependencies.auth import UserTokenData
from src.presentation.schemas.user import (
    ActivateUserRequest,
    UpdateRoleRequest,
    UpdateWorkModeRequest,
    UserResponse,
)

from src.presentation.dependencies.permission import (
    get_require_admin,
    get_require_moderator,
    get_require_user,
    get_require_super_admin,
)


router = APIRouter(prefix="/users", tags=["user"])


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
)
@inject
async def get_me(
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_user()),
) -> UserResponse:
    result: UserDTO = await mediator.handle(GetUserByIdQuery(user_id=current_user.user_id))
    return UserResponse.model_validate(result.__dict__)


@router.get(
    "/current-department",
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponse],
)
@inject
async def get_all_by_department(
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_moderator()),
    offset: int = 0,
    limit: int = 20,
) -> list[UserResponse]:
    result: list[UserDTO] = await mediator.handle(
        GetAllUsersQuery(
            department_id=current_user.department_id,
            offset=offset,
            limit=limit,
        )
    )
    return [UserResponse.model_validate(u.__dict__) for u in result]


@router.get(
    "/current-organization",
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponse],
)
@inject
async def get_all_by_organization(
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_admin()),
    offset: int = 0,
    limit: int = 20,
) -> list[UserResponse]:
    result: list[UserDTO] = await mediator.handle(
        GetAllUsersQuery(
            organization_id=current_user.organization_id,
            offset=offset,
            limit=limit,
        )
    )
    return [UserResponse.model_validate(u.__dict__) for u in result]


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponse],
)
@inject
async def get_all(
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_super_admin()),
    department_id: int | None = None,
    organization_id: int | None = None,
    offset: int = 0,
    limit: int = 20,
) -> list[UserResponse]:
    result: list[UserDTO] = await mediator.handle(
        GetAllUsersQuery(
            department_id=department_id,
            organization_id=organization_id,
            offset=offset,
            limit=limit,
        )
    )
    return [UserResponse.model_validate(user.__dict__) for user in result]


@router.patch(
    "/{id}/role",
    status_code=status.HTTP_200_OK,
)
@inject
async def update_role(
    id: int,
    data: Annotated[UpdateRoleRequest, Query()],
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_super_admin()),
) -> None:
    await mediator.handle(
        UpdateUserRoleCommand(
            user_id=id,
            role=data.role,
        )
    )


@router.patch(
    "/{id}/work-mode",
    status_code=status.HTTP_200_OK,
)
@inject
async def update_work_mode(
    id: int,
    data: Annotated[UpdateWorkModeRequest, Query()],
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_admin()),
) -> None:
    await mediator.handle(
        UpdateUserWorkModeCommand(
            user_id=id,
            work_mode=data.work_mode,
        )
    )


@router.patch(
    "/{id}/activate",
    status_code=status.HTTP_200_OK,
)
@inject
async def activate_user(
    id: int,
    data: Annotated[ActivateUserRequest, Query()],
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_super_admin()),
) -> None:
    await mediator.handle(
        ActivateUserCommand(
            user_id=id,
            is_active=data.is_active,
        )
    )
