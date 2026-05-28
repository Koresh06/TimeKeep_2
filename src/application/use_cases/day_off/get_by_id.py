from dataclasses import dataclass

from src.application.dtos.day_off import DayOffDTO
from src.application.use_cases.base import UseCase, UseCaseQuery
from src.domain.entities.day_off import DayOff
from src.domain.exceptions.day_off import DayOffNotFoundError
from src.domain.interfaces.repositories.day_off import IDayOffRepository


@dataclass(frozen=True, eq=False)
class GetByIdDayOffQuery(UseCaseQuery):
    id: int


@dataclass(kw_only=True)
class GetByIdDayOffUseCase(UseCase[GetByIdDayOffQuery, DayOffDTO]):
    day_off_repo: IDayOffRepository

    async def __call__(self, command: GetByIdDayOffQuery) -> DayOffDTO:
        result: DayOff | None = await self.day_off_repo.get_by_id(command.id)
        if not result:
            raise DayOffNotFoundError(command.id)

        return DayOffDTO.from_entity(result)