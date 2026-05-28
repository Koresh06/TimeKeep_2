from dataclasses import dataclass

from src.application.dtos.deparment import DepartmentDTO
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.entities.department import Department
from src.domain.interfaces.repositories.department import IDepartmentRepository


@dataclass(frozen=True, eq=False)
class GetAllDepartmentQuery(UseCaseRequest):
    organization_id: int | None = None
    offset: int = 0
    limit: int = 20


@dataclass(kw_only=True)
class GetAllDepartmentUseCase(UseCase[GetAllDepartmentQuery, list[DepartmentDTO]]):
    department_repo: IDepartmentRepository

    async def __call__(self, command: GetAllDepartmentQuery) -> list[DepartmentDTO]:
        result: list[Department] = await self.department_repo.get_all(
            organization_id=command.organization_id,
            offset=command.offset,
            limit=command.limit,
        )
        return [DepartmentDTO.from_entity(department) for department in result]