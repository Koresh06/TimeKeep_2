from dataclasses import dataclass, field


@dataclass(frozen=True)
class MonthlyStatDTO:
    year: int
    month: int
    hours: float


@dataclass(frozen=True)
class StatisticsDTO:
    total_overtimes: int
    total_overtime_hours: float
    available_overtime_hours: float
    total_day_offs: int
    pending_day_offs: int
    approved_day_offs: int
    rejected_day_offs: int
    monthly_overtime_hours: list[MonthlyStatDTO] = field(default_factory=list)
