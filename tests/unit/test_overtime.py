
from src.domain.entities.overtime import Overtime



def test_duration_hours(overtimes_exact_8h: list[Overtime]):
    assert overtimes_exact_8h[0].duration_hours() == 8


def test_available_hours_after_partial_use(overtimes_exact_4h: list[Overtime]):
    assert overtimes_exact_4h[0].available_hours() == 4


def test_overlaps_with_same_date(overtimes_exact_8h, overtimes_partial: list[Overtime]):
    assert overtimes_exact_8h[0].overlaps_with(overtimes_partial[-1])


def test_no_overlap_different_dates(overtimes_fifo: list[Overtime]):
    assert not overtimes_fifo[0].overlaps_with(overtimes_fifo[1])


def test_no_overlap_adjacent_times(overtimes_partial: list[Overtime]):
    assert not overtimes_partial[0].overlaps_with(overtimes_partial[1])