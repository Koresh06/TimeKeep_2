from dataclasses import dataclass
from datetime import date

from src.application.dtos.day_off import DayOffDTO
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.entities.day_off import DayOff
from src.domain.entities.overtime import Overtime
from src.domain.entities.user import User
from src.domain.enums.day_off_status import DayOffStatus
from src.domain.enums.overtime_status import OvertimeStatus
from src.domain.exceptions.day_off import (
    DayOffAlreadyExistsForDateError,
    DayOffInvalidDateError,
)
from src.domain.interfaces.repositories.overtime import IOvertimeRepository
from src.domain.value_objects.work_schedule import WorkSchedule
from src.domain.exceptions.user import UserNotFoundError
from src.domain.interfaces.repositories.day_off import IDayOffRepository
from src.domain.interfaces.repositories.user import IUserRepository
from src.domain.interfaces.transaction_manager import ITransactionManager


@dataclass(frozen=True, eq=False)
class TakeDayOffCommand(UseCaseRequest):
    user_id: int
    date_: date


@dataclass(kw_only=True)
class TakeDayOffUseCase(UseCase[TakeDayOffCommand, DayOffDTO]):
    user_repo: IUserRepository
    overtime_repo: IOvertimeRepository
    day_off_repo: IDayOffRepository
    transaction_manager: ITransactionManager

    async def __call__(self, command: TakeDayOffCommand) -> DayOffDTO:
        if command.date_ < date.today():
            raise DayOffInvalidDateError()

        user: User | None = await self.user_repo.get_by_id(command.user_id)
        if not user:
            raise UserNotFoundError(command.user_id)

        existing: list[DayOff] = await self.day_off_repo.get_all(
            user_id=command.user_id,
            date_=command.date_,
        )
        if existing:
            raise DayOffAlreadyExistsForDateError()

        schedule = WorkSchedule(user.work_mode)
        overtimes: list[Overtime] = await self.overtime_repo.get_all(
            user_id=command.user_id,
            status=OvertimeStatus.ACTIVE,
        )
        selected = schedule.select_overtimes_for_dat_off(overtimes)

        day_off = DayOff(
            user_id=command.user_id,
            date_=command.date_,
            status=DayOffStatus.PENDING,
            overtimes=selected,
        )

        for overtime in selected:
            overtime.mark_as_used()
            await self.overtime_repo.update(overtime)

        result: DayOff = await self.day_off_repo.create(day_off)
        await self.transaction_manager.commit()

        return DayOffDTO.from_entity(result)
