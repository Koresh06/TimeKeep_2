from pydantic import BaseModel, ConfigDict


class MonthlyStatResponse(BaseModel):
    year: int
    month: int
    hours: float


class StatisticsResponse(BaseModel):
    total_overtimes: int
    total_overtime_hours: float
    available_overtime_hours: float
    total_day_offs: int
    pending_day_offs: int
    approved_day_offs: int
    rejected_day_offs: int
    monthly_overtime_hours: list[MonthlyStatResponse]
    
    model_config = ConfigDict(from_attributes=True)