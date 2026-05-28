from typing import Annotated
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Body, Depends, status

from src.application.dtos.organization import OrganizationDTO
from src.application.mediator import Mediator
from src.application.use_cases.organization.create import CreateOrganizationCommand
from src.application.use_cases.organization.get_all import GetAllOrganizationQuery
from src.application.use_cases.organization.get_by_id import GetOrganizationQuery
from src.presentation.dependencies.auth import UserTokenData
from src.presentation.schemas.organization import CreateOrganization, OrganizationResponse
from src.presentation.dependencies.permission import get_require_admin, get_require_super_admin


router = APIRouter(prefix="/organizations", tags=["organization"])


@router.post(
    "/",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create(
    data: Annotated[CreateOrganization, Body()],
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_super_admin()),
) -> OrganizationResponse:
    result: OrganizationDTO = await mediator.handle(CreateOrganizationCommand(**data.model_dump()))
    return OrganizationResponse.model_validate(result.__dict__)


@router.get(
    "/{id}",
    response_model=OrganizationResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_by_id(
    id: int,
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_admin()),
) -> OrganizationResponse:
    result: OrganizationDTO = await mediator.handle(GetOrganizationQuery(id))
    return OrganizationResponse.model_validate(result.__dict__)


@router.get(
    "",
    response_model=list[OrganizationResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_all(
    mediator: FromDishka[Mediator],
    current_user: UserTokenData = Depends(get_require_super_admin()),
    offset: int = 0,
    limit: int = 20,
) -> list[OrganizationResponse]:
    result: list[OrganizationDTO] = await mediator.handle(
        GetAllOrganizationQuery(
            offset=offset,
            limit=limit,
        )
    )
    return [
        OrganizationResponse.model_validate(organization.__dict__) 
        for organization in result
    ]


