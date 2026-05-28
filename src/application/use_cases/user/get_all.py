from dataclasses import dataclass

from src.application.dtos.user import UserDTO
from src.application.use_cases.base import UseCase, UseCaseQuery
from src.domain.interfaces.repositories.user import IUserRepository


@dataclass(frozen=True, eq=False)
class GetAllUsersQuery(UseCaseQuery):
    department_id: int | None = None
    organization_id: int | None = None
    offset: int = 0
    limit: int = 20


@dataclass(kw_only=True)
class GetAllUsersUseCase(UseCase[GetAllUsersQuery, list[UserDTO]]):
    user_repository: IUserRepository

    async def __call__(self, query: GetAllUsersQuery) -> list[UserDTO]:
        users = await self.user_repository.get_all(
            department_id=query.department_id,
            organization_id=query.organization_id,
            offset=query.offset,
            limit=query.limit,
        )
        return [UserDTO.from_entity(user) for user in users]
