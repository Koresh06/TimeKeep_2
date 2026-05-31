import pytest
from datetime import date

from src.application.use_cases.day_off.take import TakeDayOffCommand, TakeDayOffUseCase
from src.domain.entities.overtime import Overtime
from src.domain.entities.user import User
from src.domain.enums.day_off_status import DayOffStatus
from src.domain.exceptions.day_off import NotEnoughHoursError
from src.domain.exceptions.user import UserNotFoundError
from src.domain.interfaces.repositories.day_off import IDayOffRepository
from src.domain.interfaces.repositories.overtime import IOvertimeRepository
from src.domain.interfaces.repositories.user import IUserRepository
from src.domain.interfaces.transaction_manager import ITransactionManager


async def test_take_day_off(
    created_user: User,
    created_overtimes: list[Overtime],
    user_repo: IUserRepository,
    overtime_repo: IOvertimeRepository,
    day_off_repo: IDayOffRepository,
    transaction_manager: ITransactionManager,
):
    command = TakeDayOffCommand(
        user_id=created_user.id,
        date_=date.today(),
    )
    use_case = TakeDayOffUseCase(
        user_repo=user_repo,
        overtime_repo=overtime_repo,
        day_off_repo=day_off_repo,
        transaction_manager=transaction_manager
    )
    await use_case(command)
    
    day_offs = await day_off_repo.get_all(user_id=created_user.id)
    assert len(day_offs) == 1
    assert day_offs[0].status == DayOffStatus.PENDING


async def test_take_day_off_not_enough_hours(
    created_user: User,
    created_overtimes_not_enough: list[Overtime],
    user_repo: IUserRepository,
    overtime_repo: IOvertimeRepository,
    day_off_repo: IDayOffRepository,
    transaction_manager: ITransactionManager,
):
    command = TakeDayOffCommand(
        user_id=created_user.id,
        date_=date.today(),
    )
    use_case = TakeDayOffUseCase(
        user_repo=user_repo,
        overtime_repo=overtime_repo,
        day_off_repo=day_off_repo,
        transaction_manager=transaction_manager
    )
    with pytest.raises(NotEnoughHoursError):
        await use_case(command)


async def test_take_day_off_user_not_found(
    user_repo: IUserRepository,
    overtime_repo: IOvertimeRepository,
    day_off_repo: IDayOffRepository,
    transaction_manager: ITransactionManager,
):
    command = TakeDayOffCommand(
        user_id=1,
        date_=date.today(),
    )
    use_case = TakeDayOffUseCase(
        user_repo=user_repo,
        overtime_repo=overtime_repo,
        day_off_repo=day_off_repo,
        transaction_manager=transaction_manager
    )
    with pytest.raises(UserNotFoundError):
        await use_case(command)
