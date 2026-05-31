import pytest
from datetime import date, time


from src.domain.entities.day_off import DayOff
from src.domain.entities.overtime import Overtime
from src.domain.entities.user import User
from src.domain.enums.day_off_status import DayOffStatus
from src.domain.enums.rank import Rank
from src.domain.enums.role import Role
from src.domain.enums.work_mode import WorkMode
from src.infrastructure.repositories.in_memory.implementation.user import (
    UserInMemoryRepository,
)
from src.infrastructure.repositories.in_memory.implementation.overtime import (
    OvertimeInMemoryRepository,
)
from src.infrastructure.repositories.in_memory.implementation.day_off import (
    DayOffInMemoryRepository,
)
from src.infrastructure.repositories.in_memory.transaction_manager import (
    InMemoryTransactionManager,
)
from tests.utils.fake_hasker import FakePasswordHasher
from tests.utils.fake_jwt_service import FakeJWTService


@pytest.fixture
def user_repo():
    return UserInMemoryRepository()


@pytest.fixture
def overtime_repo():
    return OvertimeInMemoryRepository()


@pytest.fixture
def day_off_repo():
    return DayOffInMemoryRepository()


@pytest.fixture
def transaction_manager():
    return InMemoryTransactionManager()


@pytest.fixture
def hasher():
    return FakePasswordHasher()


@pytest.fixture
def jwt():
    return FakeJWTService()


@pytest.fixture
async def created_user(user_repo: UserInMemoryRepository) -> User:
    user = User(
        login="test",
        hashed_password="hash",
        surname="TestSurname",
        first_name="TestName",
        patronymic="",
        position="Инспектор",
        rank=Rank.LIEUTENANT,
        work_mode=WorkMode.DAILY,
        department_id=1,
        organization_id=1,
        is_active=True,
    )
    return await user_repo.create(user)

@pytest.fixture
async def created_moderator(user_repo: UserInMemoryRepository) -> User:
    user = User(
        login="moderator",
        hashed_password="hash",
        surname="TestSurname",
        first_name="TestName",
        patronymic="",
        position="Заместитель",
        role=Role.MODERATOR,
        rank=Rank.LIEUTENANT,
        work_mode=WorkMode.DAILY,
        department_id=1,
        organization_id=1,
        is_active=True,
    )
    return await user_repo.create(user)


@pytest.fixture
async def created_moderator_other_department(user_repo: UserInMemoryRepository) -> User:
    user = User(
        login="moderator2",
        hashed_password="hash",
        surname="TestSurname",
        first_name="TestName",
        patronymic="",
        position="Заместитель",
        role=Role.MODERATOR,
        rank=Rank.LIEUTENANT,
        work_mode=WorkMode.DAILY,
        department_id=2,
        organization_id=1,
        is_active=True,
    )
    return await user_repo.create(user
)


@pytest.fixture
async def created_overtimes(
    overtime_repo: OvertimeInMemoryRepository,
    created_user: User,
) -> list[Overtime]:
    overtimes = [
        Overtime(
            user_id=created_user.id,
            date_=date(2023, 1, 1),
            start_time=time(8, 0),
            end_time=time(16, 0),
            description="",
        ),
        Overtime(
            user_id=created_user.id,
            date_=date(2023, 1, 2),
            start_time=time(8, 0),
            end_time=time(16, 0),
            description="",
        ),
    ]

    result = []
    for overtime in overtimes:
        await overtime_repo.create(overtime)
        result.append(overtime)

    return result


@pytest.fixture
async def created_overtimes_not_enough(
    overtime_repo: OvertimeInMemoryRepository,
    created_user: User,
) -> list[Overtime]:
    overtime = Overtime(
        user_id=created_user.id,
        date_=date(2023, 1, 1),
        start_time=time(9, 0),
        end_time=time(12, 0),
        description="",
    )
    return [await overtime_repo.create(overtime)]


@pytest.fixture
async def created_day_off(
    day_off_repo: DayOffInMemoryRepository,
    created_user: User,
) -> DayOff:
    day_off = DayOff(
        user_id=created_user.id,
        date_=date(2023, 1, 1),
        status=DayOffStatus.PENDING,
        overtimes=[],
    )
    return await day_off_repo.create(day_off)