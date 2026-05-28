from dataclasses import dataclass

from src.application.use_cases.base import UseCase, UseCaseRequest
from src.domain.entities.day_off import DayOff
from src.domain.entities.user import User
from src.domain.enums.role import Role
from src.domain.exceptions.day_off import DayOffAccessDeniedError, DayOffNotFoundError
from src.domain.exceptions.user import UserNotFoundError, UserNotModeratorError
from src.domain.interfaces.repositories.day_off import IDayOffRepository
from src.domain.interfaces.repositories.user import IUserRepository
from src.domain.interfaces.transaction_manager import ITransactionManager


@dataclass(frozen=True, eq=False)
class ModerateDayOffCommand(UseCaseRequest):
    day_off_id: int
    moderation_id: int
    is_approved: bool


@dataclass(kw_only=True)
class ModerateDayOffUseCase(UseCase[ModerateDayOffCommand, None]):
    user_repo: IUserRepository
    day_off_repo: IDayOffRepository
    transaction_manager: ITransactionManager

    async def __call__(self, command: ModerateDayOffCommand) -> None:
        moderate: User | None = await self.user_repo.get_by_id(command.moderation_id)
        if not moderate:
            raise UserNotFoundError(command.moderation_id)
        
        if moderate.role != Role.MODERATOR:
            raise UserNotModeratorError(command.moderation_id)
        
        day_off: DayOff | None = await self.day_off_repo.get_by_id(command.day_off_id)
        if not day_off:
            raise DayOffNotFoundError(command.day_off_id)
        
        worker: User | None = await self.user_repo.get_by_id(day_off.user_id)
        if not worker:
            raise UserNotFoundError(day_off.user_id)
        if worker.department_id != moderate.department_id:
            raise DayOffAccessDeniedError()
    
        if command.is_approved:
            day_off.approve()
        else:
            day_off.reject()
        
        await self.day_off_repo.update(day_off)
        await self.transaction_manager.commit()
        
        