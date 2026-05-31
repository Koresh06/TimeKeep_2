import pytest

from src.application.dtos.token import TokenDTO
from src.application.use_cases.auth.login import LoginUseCase
from src.application.use_cases.auth.login import LoginCommand
from src.domain.entities.user import User
from src.domain.exceptions.user import InvalidCredentialsError
from src.domain.interfaces.services.jwt import IJWTService
from src.domain.interfaces.services.password_hasher import IPasswordHasher
from src.domain.interfaces.transaction_manager import ITransactionManager
from src.domain.interfaces.repositories.user import IUserRepository


async def test_successful_login(
    created_user: User,
    user_repo: IUserRepository,
    hasher: IPasswordHasher,
    jwt: IJWTService,
    transaction_manager: ITransactionManager,
):
    command = LoginCommand(
        login="test",
        password="hash",
    )
    use_case = LoginUseCase(
        user_repo=user_repo,
        hashed=hasher,
        jwt=jwt,
    )
    token: TokenDTO = await use_case(command)

    assert isinstance(token, TokenDTO)
    assert token.access_token is not None
    assert token.refresh_token is not None


async def test_invalid_login(
    user_repo: IUserRepository,
    hasher: IPasswordHasher,
    jwt: IJWTService,
    transaction_manager: ITransactionManager,
):
    command = LoginCommand(
        login="test",
        password="hash",
    )
    use_case = LoginUseCase(
        user_repo=user_repo,
        hashed=hasher,
        jwt=jwt,
    )
    with pytest.raises(InvalidCredentialsError):
        await use_case(command)


async def test_incorrect_password(
    created_user: User,
    user_repo: IUserRepository,
    hasher: IPasswordHasher,
    jwt: IJWTService,
    transaction_manager: ITransactionManager,
):
    command = LoginCommand(
        login="test",
        password="1234",
    )
    use_case = LoginUseCase(
        user_repo=user_repo,
        hashed=hasher,
        jwt=jwt,
    )
    with pytest.raises(InvalidCredentialsError):
        await use_case(command)