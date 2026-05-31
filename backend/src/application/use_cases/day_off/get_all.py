from dataclasses import dataclass
from datetime import date

from src.application.dtos.day_off import DayOffDTO
from src.application.use_cases.base import UseCase, UseCaseQuery
from src.domain.enums.day_off_status import DayOffStatus
from src.domain.interfaces.repositories.day_off import IDayOffRepository


@dataclass(frozen=True, eq=False)
class GetAllDayOffsQuery(UseCaseQuery):
    user_id: int | None = None
    department_id: int | None = None
    organization_id: int | None = None
    status: DayOffStatus | None = None
    date_: date | None = None
    offset: int = 0
    limit: int = 20


@dataclass(kw_only=True)
class GetAllDayOffsUseCase(
    UseCase[
        GetAllDayOffsQuery,
        list[DayOffDTO],
    ]
):
    day_off_repo: IDayOffRepository

    async def __call__(
        self,
        query: GetAllDayOffsQuery,
    ) -> list[DayOffDTO]:
        day_offs = await self.day_off_repo.get_all(
            user_id=query.user_id,
            department_id=query.department_id,
            organization_id=query.organization_id,
            status=query.status,
            date_=query.date_,
            offset=query.offset,
            limit=query.limit,
        )
        return [DayOffDTO.from_entity(day_off) for day_off in day_offs]
