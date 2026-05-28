from dataclasses import dataclass

from src.application.dtos.user import UserDTO
from src.domain.entities.user import User
from src.domain.enums.rank import Rank
from src.domain.enums.role import Role
from src.domain.enums.work_mode import WorkMode
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.exceptions.user import UserAlreadyExistsError
from src.domain.interfaces.services.password_hasher import IPasswordHasher
from src.domain.interfaces.transaction_manager import ITransactionManager
from src.domain.interfaces.repositories.user import IUserRepository


@dataclass(frozen=True, eq=False)
class RegisterUserCommand(UseCaseRequest):
    login: str
    password: str
    surname: str
    first_name: str
    patronymic: str
    position: str
    rank: Rank
    work_mode: WorkMode
    department_id: int
    organization_id: int
    role: Role = Role.USER

    def to_user_data(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if k != "password"}


@dataclass(kw_only=True)
class RegisterUserUseCase(UseCase[RegisterUserCommand, UserDTO]):
    user_repo: IUserRepository
    hasher: IPasswordHasher
    transaction_manager: ITransactionManager

    async def __call__(self, command: RegisterUserCommand) -> UserDTO:
        user_by_login = await self.user_repo.get_by_login(command.login)
        if user_by_login:
            raise UserAlreadyExistsError(command.login)

        user = user = User.create(
            **command.to_user_data(),
            hashed_password=await self.hasher.hash(command.password),
        )
        result = await self.user_repo.create(user)
        await self.transaction_manager.commit()

        return UserDTO.from_entity(result)

