from collections import defaultdict
from dataclasses import dataclass

from src.application.dtos.statistics import MonthlyStatDTO, StatisticsDTO
from src.application.use_cases.base import UseCase, UseCaseQuery
from src.domain.enums.day_off_status import DayOffStatus
from src.domain.interfaces.repositories.day_off import IDayOffRepository
from src.domain.interfaces.repositories.overtime import IOvertimeRepository


@dataclass(frozen=True, eq=False)
class GetStatisticsQuery(UseCaseQuery):
    user_id: int | None = None
    department_id: int | None = None
    organization_id: int | None = None


@dataclass(kw_only=True)
class GetStatisticsUseCase(UseCase[GetStatisticsQuery, StatisticsDTO]):
    overtime_repository: IOvertimeRepository
    day_off_repo: IDayOffRepository

    async def __call__(self, query: GetStatisticsQuery) -> StatisticsDTO:
        overtimes = await self.overtime_repository.get_all(
            user_id=query.user_id,
            department_id=query.department_id,
            organization_id=query.organization_id,
            limit=10000,
        )
        day_offs = await self.day_off_repo.get_all(
            user_id=query.user_id,
            department_id=query.department_id,
            organization_id=query.organization_id,
            limit=10000,
        )

        total_hours = 0.0
        available_hours = 0.0
        monthly: dict[tuple[int, int], float] = defaultdict(float)

        for ot in overtimes:
            start_min = ot.start_time.hour * 60 + ot.start_time.minute
            end_min = ot.end_time.hour * 60 + ot.end_time.minute
            duration_h = (end_min - start_min) / 60.0
            total_hours += duration_h
            available_hours += max(duration_h - ot.used_hours, 0)
            key = (ot.date_.year, ot.date_.month)
            monthly[key] += duration_h

        monthly_list = [
            MonthlyStatDTO(year=y, month=m, hours=round(h, 2))
            for (y, m), h in sorted(monthly.items())
        ]

        pending = sum(1 for d in day_offs if d.status == DayOffStatus.PENDING)
        approved = sum(1 for d in day_offs if d.status == DayOffStatus.APPROVED)
        rejected = sum(1 for d in day_offs if d.status == DayOffStatus.REJECTED)

        return StatisticsDTO(
            total_overtimes=len(overtimes),
            total_overtime_hours=round(total_hours, 2),
            available_overtime_hours=round(available_hours, 2),
            total_day_offs=len(day_offs),
            pending_day_offs=pending,
            approved_day_offs=approved,
            rejected_day_offs=rejected,
            monthly_overtime_hours=monthly_list,
        )
