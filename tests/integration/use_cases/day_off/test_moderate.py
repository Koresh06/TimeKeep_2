import pytest

from src.application.use_cases.day_off.moderate import ModerateDayOffUseCase, ModerateDayOffCommand
from src.domain.entities.day_off import DayOff
from src.domain.entities.user import User
from src.domain.enums.day_off_status import DayOffStatus
from src.domain.exceptions.day_off import DayOffAccessDeniedError, DayOffAlreadyModeratedError, DayOffNotFoundError
from src.domain.exceptions.user import UserNotFoundError, UserNotModeratorError
from src.domain.interfaces.repositories.day_off import IDayOffRepository
from src.domain.interfaces.repositories.user import IUserRepository
from src.domain.interfaces.transaction_manager import ITransactionManager


async def test_successful_confirmation_day_off(
    created_moderator: User,
    created_day_off: DayOff,
    user_repo: IUserRepository,
    day_off_repo: IDayOffRepository,
    transaction_manager: ITransactionManager,
):
    use_case = ModerateDayOffUseCase(
        user_repo=user_repo,
        day_off_repo=day_off_repo,
        transaction_manager=transaction_manager,

    )
    command = ModerateDayOffCommand(
        day_off_id=created_day_off.id,
        moderation_id=created_moderator.id,
        is_approved=True
    )
    await use_case(command)

    day_off: DayOff | None = await day_off_repo.get_by_id(created_day_off.id)
    assert day_off is not None
    assert day_off.status == DayOffStatus.APPROVED


async def test_application_rejection_day_off(
    created_moderator: User,
    created_day_off: DayOff,
    user_repo: IUserRepository,
    day_off_repo: IDayOffRepository,
    transaction_manager: ITransactionManager,
):
    use_case = ModerateDayOffUseCase(
        user_repo=user_repo,
        day_off_repo=day_off_repo,
        transaction_manager=transaction_manager,
    )
    command = ModerateDayOffCommand(
        day_off_id=created_day_off.id,
        moderation_id=created_moderator.id,
        is_approved=False
    )
    await use_case(command)

    day_off: DayOff | None = await day_off_repo.get_by_id(created_day_off.id)
    assert day_off is not None
    assert day_off.status == DayOffStatus.REJECTED


async def test_not_fount_moderator(
    created_day_off: DayOff,
    user_repo: IUserRepository,
    day_off_repo: IDayOffRepository,
    transaction_manager: ITransactionManager,
):
    use_case = ModerateDayOffUseCase(
        user_repo=user_repo,
        day_off_repo=day_off_repo,
        transaction_manager=transaction_manager,
    )
    command = ModerateDayOffCommand(
        day_off_id=created_day_off.id,
        moderation_id=2,
        is_approved=True
    )
    with pytest.raises(UserNotFoundError):
        await use_case(command)


async def test_not_role_moderator_user_moderate_day_off(
    created_user: User,
    created_day_off: DayOff,
    user_repo: IUserRepository,
    day_off_repo: IDayOffRepository,
    transaction_manager: ITransactionManager,
):
    use_case = ModerateDayOffUseCase(
        user_repo=user_repo,
        day_off_repo=day_off_repo,
        transaction_manager=transaction_manager,
    )
    command = ModerateDayOffCommand(
        day_off_id=created_day_off.id,
        moderation_id=created_user.id,
        is_approved=True
    )
    with pytest.raises(UserNotModeratorError):
        await use_case(command)


async def test_day_off_not_found(
    created_moderator: User,
    user_repo: IUserRepository,
    day_off_repo: IDayOffRepository,
    transaction_manager: ITransactionManager,
):
    use_case = ModerateDayOffUseCase(
        user_repo=user_repo,
        day_off_repo=day_off_repo,
        transaction_manager=transaction_manager,
    )
    command = ModerateDayOffCommand(
        day_off_id=2,
        moderation_id=created_moderator.id,
        is_approved=True
    )
    with pytest.raises(DayOffNotFoundError):
        await use_case(command)


async def test_already_moderated_day_off(
    created_moderator: User,
    created_day_off: DayOff,
    user_repo: IUserRepository,
    day_off_repo: IDayOffRepository,
    transaction_manager: ITransactionManager,
):
    use_case = ModerateDayOffUseCase(
        user_repo=user_repo,
        day_off_repo=day_off_repo,
        transaction_manager=transaction_manager,
    )
    command = ModerateDayOffCommand(
        day_off_id=created_day_off.id,
        moderation_id=created_moderator.id,
        is_approved=True
    )
    await use_case(command)

    with pytest.raises(DayOffAlreadyModeratedError):
        await use_case(command)


async def test_someone_else_day_off(
    created_moderator_other_department: User,
    created_day_off: DayOff,
    user_repo: IUserRepository,
    day_off_repo: IDayOffRepository,
    transaction_manager: ITransactionManager,
):
    use_case = ModerateDayOffUseCase(
        user_repo=user_repo,
        day_off_repo=day_off_repo,
        transaction_manager=transaction_manager,
    )
    command = ModerateDayOffCommand(
        day_off_id=created_day_off.id,
        moderation_id=created_moderator_other_department.id,
        is_approved=True
    )
    with pytest.raises(DayOffAccessDeniedError):
        await use_case(command)