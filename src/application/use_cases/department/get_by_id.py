from dataclasses import dataclass

from src.application.dtos.deparment import DepartmentDTO
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.entities.department import Department
from src.domain.exceptions.department import DepartmentNotFoundError
from src.domain.interfaces.cache import ICache
from src.domain.interfaces.repositories.department import IDepartmentRepository


@dataclass(frozen=True, eq=False)
class GetDepartmentQuery(UseCaseRequest):
    id: int


@dataclass(kw_only=True)
class GetDepartmentUseCase(UseCase[GetDepartmentQuery, DepartmentDTO]):
    department_repo: IDepartmentRepository
    cache: ICache

    async def __call__(self, query: GetDepartmentQuery) -> DepartmentDTO:
        cache_key = f"department:{query.id}"

        cached = await self.cache.get(cache_key)
        if cached:
            return DepartmentDTO(**cached)

        result: Department | None = await self.department_repo.get_by_id(query.id)
        if not result:
            raise DepartmentNotFoundError(query.id)

        dto = DepartmentDTO.from_entity(result)
        await self.cache.set(cache_key, dto.__dict__)
        return dto