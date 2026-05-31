from dataclasses import dataclass
from datetime import date

from src.application.dtos.overtime import OvertimeDTO
from src.application.use_cases.base import UseCase, UseCaseQuery
from src.domain.enums.overtime_status import OvertimeStatus
from src.domain.interfaces.repositories.overtime import IOvertimeRepository


@dataclass(frozen=True, eq=False)
class GetAllOvertimesQuery(UseCaseQuery):
    user_id: int | None = None
    department_id: int | None = None
    organization_id: int | None = None
    status: OvertimeStatus | None = None
    date_: date | None = None
    offset: int = 0
    limit: int = 20


@dataclass(kw_only=True)
class GetAllOvertimesUseCase(UseCase[GetAllOvertimesQuery, list[OvertimeDTO]]):
    overtime_repository: IOvertimeRepository

    async def __call__(self, query: GetAllOvertimesQuery) -> list[OvertimeDTO]:
        overtimes = await self.overtime_repository.get_all(
            user_id=query.user_id,
            department_id=query.department_id,
            organization_id=query.organization_id,
            status=query.status,
            date_=query.date_,
            offset=query.offset,
            limit=query.limit,
        )
        return [OvertimeDTO.from_entity(overtime) for overtime in overtimes]
