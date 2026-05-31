from datetime import date, datetime

from pydantic import BaseModel, ConfigDict

from src.domain.enums.day_off_status import DayOffStatus
from src.presentation.schemas.overtime import OvertimeResponse


class DayOffBase(BaseModel):
    date_: date


class CreateDayOff(DayOffBase):
    pass


class UpdateDayOff(DayOffBase):
    pass


class DayOffResponse(DayOffBase):
    id: int
    user_id: int
    status: DayOffStatus
    overtimes: list[OvertimeResponse]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ModerateDayOff(BaseModel):
    is_approved: bool
