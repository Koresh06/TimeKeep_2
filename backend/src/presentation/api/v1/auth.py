from typing import Annotated
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Body, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.application.dtos.organization import OrganizationDTO
from src.application.dtos.deparment import DepartmentDTO
from src.application.dtos.user import UserDTO
from src.application.mediator import Mediator
from src.application.use_cases.auth.login import LoginCommand
from src.application.use_cases.auth.register import RegisterUserCommand
from src.application.use_cases.organization.get_all import GetAllOrganizationQuery
from src.application.use_cases.department.get_all import GetAllDepartmentQuery
from src.presentation.schemas.auth import RegisterUser, TokenResponse, UserResponse
from src.presentation.schemas.department import DepartmentResponse
from src.presentation.schemas.organization import OrganizationResponse


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
@inject
async def register(
    data: Annotated[RegisterUser, Body()],
    mediator: FromDishka[Mediator],
):
    result: UserDTO = await mediator.handle(RegisterUserCommand(**data.model_dump()))
    return UserResponse.model_validate(result.__dict__)


@router.post("/login", response_model=TokenResponse)
@inject
async def login(
    mediator: FromDishka[Mediator],
    data: OAuth2PasswordRequestForm = Depends(),
):
    result = await mediator.handle(
        LoginCommand(
            login=data.username,
            password=data.password,
        )
    )
    return TokenResponse.model_validate(result.__dict__)


@router.get(
    "/organizations",
    response_model=list[OrganizationResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_organizations_public(
    mediator: FromDishka[Mediator],
    offset: int = 0,
    limit: int = 100,
) -> list[OrganizationResponse]:
    result: list[OrganizationDTO] = await mediator.handle(
        GetAllOrganizationQuery(offset=offset, limit=limit)
    )
    return [OrganizationResponse.model_validate(o.__dict__) for o in result]


@router.get(
    "/departments",
    response_model=list[DepartmentResponse],
    status_code=status.HTTP_200_OK,
)
@inject
async def get_departments_public(
    mediator: FromDishka[Mediator],
    organization_id: int | None = None,
    offset: int = 0,
    limit: int = 100,
) -> list[DepartmentResponse]:
    result: list[DepartmentDTO] = await mediator.handle(
        GetAllDepartmentQuery(
            organization_id=organization_id,
            offset=offset,
            limit=limit,
        )
    )
    return [DepartmentResponse.model_validate(d.__dict__) for d in result]
