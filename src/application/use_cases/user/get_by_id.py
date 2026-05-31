from dataclasses import dataclass

from src.application.dtos.user import UserDTO
from src.application.use_cases.base import UseCase, UseCaseQuery
from src.domain.exceptions.user import UserNotFoundError
from src.domain.interfaces.cache import ICache
from src.domain.interfaces.repositories.user import IUserRepository


@dataclass(frozen=True, eq=False)
class GetUserByIdQuery(UseCaseQuery):
    user_id: int


@dataclass(kw_only=True)
class GetByIdUserUseCase(UseCase[GetUserByIdQuery, UserDTO]):
    user_repository: IUserRepository
    cache: ICache

    async def __call__(self, query: GetUserByIdQuery) -> UserDTO:
        cache_key = f"user:{query.user_id}"

        cached = await self.cache.get(cache_key)
        if cached:
            return UserDTO(**cached)

        user = await self.user_repository.get_by_id(query.user_id)
        if not user:
            raise UserNotFoundError(query.user_id)

        dto = UserDTO.from_entity(user)
        await self.cache.set(cache_key, dto.__dict__, ttl=300)
        return dto
