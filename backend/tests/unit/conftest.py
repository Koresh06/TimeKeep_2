import pytest
from datetime import date, time

from src.domain.entities.day_off import DayOff
from src.domain.entities.overtime import Overtime
from src.domain.enums.day_off_status import DayOffStatus
from src.domain.enums.overtime_status import OvertimeStatus


OVERTIMES_EXACT_8H = [
    Overtime(
        user_id=1,
        date_=date(2023, 1, 1),
        start_time=time(9, 0),
        end_time=time(17, 0),
        description="description_1",
        status=OvertimeStatus.ACTIVE,
    ),
]

OVERTIMES_EXACT_3H = [
    Overtime(
        user_id=1,
        date_=date(2023, 1, 1),
        start_time=time(9, 0),
        end_time=time(12, 0),
        description="description_2",
        status=OvertimeStatus.ACTIVE,
    ),
]

OVERTIMES_EXACT_4H = [
    Overtime(
        user_id=1,
        date_=date(2023, 1, 1),
        start_time=time(9, 0),
        end_time=time(13, 0),
        description="description_3",
        status=OvertimeStatus.ACTIVE,
    ),
]

OVERTIMES_PARTIAL = [
    Overtime(
        user_id=1,
        date_=date(2023, 1, 1),
        start_time=time(9, 0),
        end_time=time(12, 0),
        description="description_4",
        status=OvertimeStatus.ACTIVE,
    ),
    Overtime(
        user_id=1,
        date_=date(2023, 1, 1),
        start_time=time(13, 0),
        end_time=time(17, 0),
        description="description_5",
        status=OvertimeStatus.ACTIVE,
    ),
    Overtime(
        user_id=1,
        date_=date(2023, 1, 1),
        start_time=time(9, 0),
        end_time=time(17, 0),
        description="description_6",
        status=OvertimeStatus.ACTIVE,
    )
]

OVERTIMES_NOT_ENOUGH = [
    Overtime(
        user_id=1,
        date_=date(2023, 1, 1),
        start_time=time(9, 0),
        end_time=time(12, 0),
        description="description_7",
        status=OvertimeStatus.ACTIVE,
    ),
]

OVERTIMES_FIFO = [
    # дата 2023-01-03
    # дата 2023-01-01  ← должен взяться первым
    # дата 2023-01-02
    Overtime(
        user_id=1,
        date_=date(2023, 1, 1),
        start_time=time(9, 0),
        end_time=time(17, 0),
        description="description_8",
        status=OvertimeStatus.ACTIVE,
    ),
    Overtime(
        user_id=1,
        date_=date(2023, 1, 2),
        start_time=time(9, 0),
        end_time=time(17, 0),
        description="description_8",
        status=OvertimeStatus.ACTIVE,
    ),
    Overtime(
        user_id=1,
        date_=date(2023, 1, 3),
        start_time=time(9, 0),
        end_time=time(17, 0),
        description="description_10",
        status=OvertimeStatus.ACTIVE,
    ),
]

@pytest.fixture
def overtimes_exact_8h():
    return OVERTIMES_EXACT_8H

@pytest.fixture
def overtimes_exact_3h():
    return OVERTIMES_EXACT_3H

@pytest.fixture
def overtimes_exact_4h():
    return OVERTIMES_EXACT_4H

@pytest.fixture  
def overtimes_partial():
    return OVERTIMES_PARTIAL

@pytest.fixture  
def overtimes_not_enough():
    return OVERTIMES_NOT_ENOUGH

@pytest.fixture  
def overtimes_fifo():
    return OVERTIMES_FIFO


@pytest.fixture
def day_off_pending():
    return DayOff(
        user_id=1,
        date_=date(2023, 1, 10),
        status=DayOffStatus.PENDING,
        overtimes=OVERTIMES_EXACT_8H,
    )

@pytest.fixture
def day_off_approved():
    return DayOff(
        user_id=1,
        date_=date(2023, 1, 10),
        status=DayOffStatus.APPROVED,
        overtimes=OVERTIMES_EXACT_8H,
    )

@pytest.fixture
def day_off_rejected():
    return DayOff(
        user_id=1,
        date_=date(2023, 1, 10),
        status=DayOffStatus.REJECTED,
        overtimes=OVERTIMES_EXACT_8H,
    )