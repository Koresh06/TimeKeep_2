from datetime import date, datetime, time

from pydantic import BaseModel

from src.domain.enums.overtime_status import OvertimeStatus


class OvertimeBase(BaseModel):
    user_id: int
    date_: date
    start_time: time
    used_hours: float
    description: str
    


class CreateOvertime(OvertimeBase):
    pass


class UpdateOvertime(OvertimeBase):
    pass


class OvertimeResponse(OvertimeBase):
    id: int
    end_time: time
    status: OvertimeStatus
    created_at: datetime
    updated_at: datetime