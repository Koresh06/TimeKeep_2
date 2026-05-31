import pytest

from src.application.use_cases.overtime.create import CreateOvertimeUseCase
from src.application.use_cases.overtime.create import CreateOvertimeCommand
from src.domain.entities.user import User
from src.domain.exceptions.overtime import OvertimeOverlapError
from src.infrastructure.repositories.in_memory.implementation.overtime import (
    OvertimeInMemoryRepository,
)
from src.domain.interfaces.transaction_manager import ITransactionManager
from datetime import date, time


async def test_successful_create_overtime(
    created_user: User,
    overtime_repo: OvertimeInMemoryRepository,
    transaction_manager: ITransactionManager,
):
    use_case = CreateOvertimeUseCase(
        overtime_repo=overtime_repo,
        transaction_manager=transaction_manager,
    )
    command = CreateOvertimeCommand(
        user_id=created_user.id,
        date_=date(2023, 1, 1),
        start_time=time(9, 0),
        end_time=time(12, 0),
        description="",
    )
    await use_case(command)

    overtimes = await overtime_repo.get_all(user_id=created_user.id)
    assert len(overtimes) == 1

    assert overtimes[0].user_id == created_user.id
    assert overtimes[0].date_ == date(2023, 1, 1)
    assert overtimes[0].start_time == time(9, 0)
    assert overtimes[0].end_time == time(12, 0)
    assert overtimes[0].description == ""


async def test_intersection_in_time(
    created_user: User,
    overtime_repo: OvertimeInMemoryRepository,
    transaction_manager: ITransactionManager,
):
    use_case = CreateOvertimeUseCase(
        overtime_repo=overtime_repo,
        transaction_manager=transaction_manager,
    )
    command = CreateOvertimeCommand(
        user_id=created_user.id,
        date_=date(2023, 1, 1),
        start_time=time(9, 0),
        end_time=time(12, 0),
        description="",
    )
    await use_case(command)

    with pytest.raises(OvertimeOverlapError):
        await use_case(command)


async def test_two_overtime_jobs_in_one_day_without_overlap(
    created_user: User,
    overtime_repo: OvertimeInMemoryRepository,
    transaction_manager: ITransactionManager,
):
    use_case = CreateOvertimeUseCase(
        overtime_repo=overtime_repo,
        transaction_manager=transaction_manager,
    )
    command_1 = CreateOvertimeCommand(
        user_id=created_user.id,
        date_=date(2023, 1, 1),
        start_time=time(9, 0),
        end_time=time(12, 0),
        description="",
    )

    command_2 = CreateOvertimeCommand(
        user_id=created_user.id,
        date_=date(2023, 1, 1),
        start_time=time(13, 0),
        end_time=time(16, 0),
        description="",
    )

    await use_case(command_1)
    await use_case(command_2)
    
    overtimes = await overtime_repo.get_all(user_id=created_user.id)
    assert len(overtimes) == 2
    