from dataclasses import dataclass

from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.enums.role import Role
from src.domain.exceptions.user import UserNotFoundError
from src.domain.interfaces.repositories.user import IUserRepository
from src.domain.interfaces.transaction_manager import ITransactionManager


@dataclass(frozen=True, eq=False)
class UpdateUserRoleCommand(UseCaseRequest):
    user_id: int
    role: Role


@dataclass(kw_only=True)
class UpdateUserRoleUseCase(UseCase[UpdateUserRoleCommand, None]):
    user_repo: IUserRepository
    transaction_manager: ITransactionManager

    async def __call__(self, command: UpdateUserRoleCommand) -> None:
        user = await self.user_repo.get_by_id(command.user_id)
        if not user:
            raise UserNotFoundError(command.user_id)
        user.change_role(command.role)
        await self.user_repo.update(user)
        await self.transaction_manager.commit()
