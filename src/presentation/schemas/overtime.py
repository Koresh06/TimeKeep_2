from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict

from src.domain.enums.overtime_status import OvertimeStatus


class OvertimeBase(BaseModel):
    date_: date
    start_time: time
    end_time: time
    description: str


class CreateOvertime(OvertimeBase):
    pass


class UpdateOvertime(OvertimeBase):
    pass


class OvertimeResponse(OvertimeBase):
    id: int
    user_id: int
    status: OvertimeStatus
    used_hours: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
