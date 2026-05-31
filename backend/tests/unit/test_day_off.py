import pytest

from src.domain.entities.day_off import DayOff
from src.domain.exceptions.day_off import DayOffAlreadyModeratedError
from src.domain.enums.day_off_status import DayOffStatus


def test_approve_changes_status(day_off_pending: DayOff):
    day_off_pending.approve()
    assert day_off_pending.status == DayOffStatus.APPROVED


def test_reject_changes_status(day_off_pending: DayOff):
    day_off_pending.reject()
    assert day_off_pending.status == DayOffStatus.REJECTED


def test_approve_already_moderated_raises_exception(day_off_approved: DayOff):
    with pytest.raises(DayOffAlreadyModeratedError):
        day_off_approved.approve()


def test_reject_already_moderated_raises_exception(day_off_rejected: DayOff):
    with pytest.raises(DayOffAlreadyModeratedError):
        day_off_rejected.reject()


def test_format_overtimes_for_report(day_off_pending: DayOff):
    result = day_off_pending.format_overtimes_for_document()
    assert isinstance(result, str)
    print(result)
    assert result == "01.01.2023 - description_1 (8 ч.)"