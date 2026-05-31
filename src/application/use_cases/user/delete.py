from dataclasses import dataclass

from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.entities.user import User
from src.domain.exceptions.user import UserNotFoundError
from src.domain.interfaces.cache import ICache
from src.domain.interfaces.repositories.user import IUserRepository
from src.domain.interfaces.transaction_manager import ITransactionManager


@dataclass(frozen=True, eq=False)
class DeleteUserRequest(UseCaseRequest):
    user_id: int


@dataclass(kw_only=True)
class DeleteUserUseCase(UseCase[DeleteUserRequest, None]):
    user_repository: IUserRepository
    transaction_manager: ITransactionManager
    cache: ICache


    async def __call__(self, request: DeleteUserRequest) -> None:
        user: User | None = await self.user_repository.get_by_id(request.user_id)
        if not user:
            raise UserNotFoundError(request.user_id)
        
        await self.user_repository.delete(request.user_id)
        await self.transaction_manager.commit()
        await self.cache.delete(f"user:{request.user_id}")
        