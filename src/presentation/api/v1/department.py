from typing import Annotated
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Body, Depends, status

from src.application.mediator import Mediator
from src.application.use_cases.department.create import CreateDepartmentCommand
from src.application.use_cases.department.get_all import GetAllDepartmentQuery
from src.application.use_cases.department.get_by_id import GetDepartmentQuery
from src.presentation.dependencies.auth import UserTokenData
from src.presentation.schemas.department import CreateDepartment, DepartmentResponse
from src.presentation.dependencies.permission import get_require_super_admin, get_require_admin, get_require_moderator


router = APIRouter(prefix="/departments", tags=["department"])


@router.post(
    "/",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create(
    data: Annotated[CreateDepartment, Body()],
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_admin()),
) -> DepartmentResponse:
    return await mediator.handle(CreateDepartmentCommand(**data.model_dump()))


@router.get(
    "/{id}",
    response_model=DepartmentResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_by_id(
    id: int,
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_moderator()),
) -> DepartmentResponse:
    return await mediator.handle(GetDepartmentQuery(id))


@router.get(
    "/organization/{organization_id}",
    response_model=list[DepartmentResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_all_by_organization(
    mediator: FromDishka[Mediator],
    organization_id: int,
    current_user: UserTokenData = Depends(get_require_admin()),
    offset: int = 0,
    limit: int = 20,
) -> list[DepartmentResponse]:
    return await mediator.handle(
        GetAllDepartmentQuery(
            organization_id=organization_id,
            offset=offset,
            limit=limit,
        )
    )

@router.get(
    "",
    response_model=list[DepartmentResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_all(
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_super_admin()),
    offset: int = 0,
    limit: int = 20,
) -> list[DepartmentResponse]:
    return await mediator.handle(
        GetAllDepartmentQuery(
            offset=offset,
            limit=limit,
        )
    )