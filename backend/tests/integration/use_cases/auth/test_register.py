import pytest

from src.application.use_cases.auth.register import (
    RegisterUserCommand,
    RegisterUserUseCase,
)
from src.domain.entities.user import User
from src.domain.enums.rank import Rank
from src.domain.enums.work_mode import WorkMode
from src.domain.exceptions.user import UserAlreadyExistsError
from src.domain.interfaces.services.password_hasher import IPasswordHasher
from src.domain.interfaces.repositories.user import IUserRepository
from src.domain.interfaces.transaction_manager import ITransactionManager


async def test_successful_registration_user(
    user_repo: IUserRepository,
    hasher: IPasswordHasher,
    transaction_manager: ITransactionManager,
):
    command = RegisterUserCommand(
        login="test",
        password="hash",
        surname="Корец",
        first_name="Андрей",
        patronymic="",
        position="Инспектор",
        rank=Rank.LIEUTENANT,
        work_mode=WorkMode.DAILY,
        department_id=1,
        organization_id=1,
    )
    use_case = RegisterUserUseCase(
        user_repo=user_repo,
        hasher=hasher,
        transaction_manager=transaction_manager,
    )
    await use_case(command)

    user = await user_repo.get_by_login(command.login)
    assert user is not None
    assert user.login == command.login


async def test_already_exists_user(
    user_repo: IUserRepository,
    hasher: IPasswordHasher,
    transaction_manager: ITransactionManager,
):
    command = RegisterUserCommand(
        login="test",
        password="hash",
        surname="Корец",
        first_name="Андрей",
        patronymic="",
        position="Инспектор",
        rank=Rank.LIEUTENANT,
        work_mode=WorkMode.DAILY,
        department_id=1,
        organization_id=1,
    )
    await user_repo.create(
        user = User(
            id=0,
            **command.to_user_data(),
            hashed_password=await hasher.hash(command.password),
        )
    )
    use_case = RegisterUserUseCase(
        user_repo=user_repo,
        hasher=hasher,
        transaction_manager=transaction_manager,
    )
    with pytest.raises(UserAlreadyExistsError):
        await use_case(command)
