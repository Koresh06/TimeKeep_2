from dataclasses import dataclass

from src.application.dtos.deparment import DepartmentDTO
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.entities.department import Department
from src.domain.exceptions.department import DepartmentNotFoundError
from src.domain.interfaces.repositories.department import IDepartmentRepository


@dataclass(frozen=True, eq=False)
class GetDepartmentQuery(UseCaseRequest):
    id: int


@dataclass(kw_only=True)
class GetDepartmentUseCase(UseCase[GetDepartmentQuery, DepartmentDTO]):
    department_repo: IDepartmentRepository

    async def __call__(self, command: GetDepartmentQuery) -> DepartmentDTO:
        result: Department | None = await self.department_repo.get_by_id(command.id)
        if not result:
            raise DepartmentNotFoundError(command.id)

        return DepartmentDTO.from_entity(result)