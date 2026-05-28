from dataclasses import dataclass
from datetime import date, time

from src.application.dtos.overtime import OvertimeDTO
from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.entities.overtime import Overtime
from src.domain.exceptions.overtime import OvertimeOverlapError
from src.domain.interfaces.repositories.overtime import IOvertimeRepository
from src.domain.interfaces.transaction_manager import ITransactionManager


@dataclass(frozen=True, eq=False)
class CreateOvertimeCommand(UseCaseRequest):
    user_id: int
    date_: date
    start_time: time
    end_time: time
    description: str


@dataclass(kw_only=True)
class CreateOvertimeUseCase(UseCase[CreateOvertimeCommand, OvertimeDTO]):
    overtime_repo: IOvertimeRepository
    transaction_manager: ITransactionManager

    async def __call__(self, command: CreateOvertimeCommand) -> OvertimeDTO:
        overtimes: list[Overtime] = await self.overtime_repo.get_all(
            user_id=command.user_id,
            date_=command.date_,
        )

        new_overtime = Overtime(
            user_id=command.user_id,
            date_=command.date_,
            start_time=command.start_time,
            end_time=command.end_time,
            description=command.description,
        )
        
        for overtime in overtimes:
            if overtime.overlaps_with(new_overtime):
                raise OvertimeOverlapError()
            
        result: Overtime = await self.overtime_repo.create(new_overtime)
        await self.transaction_manager.commit()

        return OvertimeDTO.from_entity(result)
