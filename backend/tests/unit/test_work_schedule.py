import pytest
from datetime import date

from src.domain.entities.overtime import Overtime
from src.domain.enums.work_mode import WorkMode
from src.domain.value_objects.work_schedule import WorkSchedule
from src.domain.exceptions.day_off import NotEnoughHoursError



def test_daily_exact_hours(overtimes_exact_8h: list[Overtime]):
    schedule = WorkSchedule(WorkMode.DAILY)
    selected = schedule.select_overtimes_for_dat_off(overtimes_exact_8h)
    assert len(selected) == 1
    

def test_daily_partial_last_overtime(overtimes_partial: list[Overtime]):
    schedule = WorkSchedule(WorkMode.DAILY)
    selected = schedule.select_overtimes_for_dat_off(overtimes_partial)
    last_overtime = selected[-1]
    assert last_overtime.used_hours < last_overtime.duration_hours()


def test_daily_not_enough_hours(overtimes_not_enough: list[Overtime]):
    schedule = WorkSchedule(WorkMode.DAILY)
    with pytest.raises(NotEnoughHoursError):
        schedule.select_overtimes_for_dat_off(overtimes_not_enough)


def test_fifo_order(overtimes_fifo: list[Overtime]):
    schedule = WorkSchedule(WorkMode.DAILY)
    selected = schedule.select_overtimes_for_dat_off(overtimes_fifo)
    assert selected[0].date_ == date(2023, 1, 1)


def test_shift_requires_24_hours():
    schedule = WorkSchedule(WorkMode.SHIFT)
    with pytest.raises(NotEnoughHoursError):
        schedule.select_overtimes_for_dat_off([])