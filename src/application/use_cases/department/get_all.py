from dataclasses import dataclass

from src.application.dtos.deparment import DepartmentDTO
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.entities.department import Department
from src.domain.interfaces.cache import ICache
from src.domain.interfaces.repositories.department import IDepartmentRepository


@dataclass(frozen=True, eq=False)
class GetAllDepartmentQuery(UseCaseRequest):
    organization_id: int | None = None
    offset: int = 0
    limit: int = 20


@dataclass(kw_only=True)
class GetAllDepartmentUseCase(UseCase[GetAllDepartmentQuery, list[DepartmentDTO]]):
    department_repo: IDepartmentRepository
    cache: ICache

    async def __call__(self, query: GetAllDepartmentQuery) -> list[DepartmentDTO]:
        cache_key = f"departments:org:{query.organization_id}:offset:{query.offset}:limit:{query.limit}"
        
        cached = await self.cache.get(cache_key)
        if cached:
            return [DepartmentDTO(**d) for d in cached]
        
        result = await self.department_repo.get_all(
            organization_id=query.organization_id,
            offset=query.offset,
            limit=query.limit,
        )
        dtos = [DepartmentDTO.from_entity(d) for d in result]
        await self.cache.set(cache_key, [dto.__dict__ for dto in dtos], ttl=600)
        return dtos