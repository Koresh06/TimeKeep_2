from dataclasses import dataclass

from src.application.dtos.deparment import DepartmentDTO
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.entities.department import Department
from src.domain.exceptions.department import DepartmentAlreadyExistsError
from src.domain.interfaces.repositories.department import IDepartmentRepository
from src.domain.interfaces.transaction_manager import ITransactionManager


@dataclass(frozen=True, eq=False)
class CreateDepartmentCommand(UseCaseRequest):
    name: str
    organization_id: int


@dataclass(kw_only=True)
class CreateDepartmentUseCase(UseCase[CreateDepartmentCommand, DepartmentDTO]):
    department_repo: IDepartmentRepository
    transaction_manager: ITransactionManager

    async def __call__(self, command: CreateDepartmentCommand) -> DepartmentDTO:
        department_by_name = await self.department_repo.get_by_name(command.name)
        if department_by_name:
            raise DepartmentAlreadyExistsError(command.name)
        
        result: Department = await self.department_repo.create(
            Department(
                name=command.name,
                organization_id=command.organization_id,
            )
        )

        await self.transaction_manager.commit()
        return DepartmentDTO.from_entity(result)