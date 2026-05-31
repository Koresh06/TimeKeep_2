from typing import Annotated
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Body, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.application.dtos.user import UserDTO
from src.application.mediator import Mediator
from src.application.use_cases.auth.login import LoginCommand
from src.application.use_cases.auth.register import RegisterUserCommand
from src.presentation.schemas.auth import RegisterUser, TokenResponse, UserResponse


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
