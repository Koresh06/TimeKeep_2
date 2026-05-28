from dataclasses import dataclass

from src.application.dtos.overtime import OvertimeDTO
from src.application.use_cases.base import UseCase, UseCaseQuery
from src.domain.entities.overtime import Overtime
from src.domain.exceptions.overtime import OvertimeNotFoundError
from src.domain.interfaces.repositories.overtime import IOvertimeRepository

@dataclass(frozen=True, eq=False)
class GetByIdOvertimeQuery(UseCaseQuery):
    id: int


@dataclass(kw_only=True)
class GetByIdOvertimeUseCase(UseCase[GetByIdOvertimeQuery, OvertimeDTO]):
    overtime_repo: IOvertimeRepository

    async def __call__(self, command: GetByIdOvertimeQuery) -> OvertimeDTO:
        result: Overtime | None = await self.overtime_repo.get_by_id(command.id)
        if not result:
            raise OvertimeNotFoundError(command.id)

        return OvertimeDTO.from_entity(result)