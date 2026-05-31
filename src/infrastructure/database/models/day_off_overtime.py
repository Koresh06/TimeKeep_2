from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Float, ForeignKey


from .base import BaseModel, CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from src.infrastructure.database.models import DayOffModel, OvertimeModel


class DayOffOvertimeModel(BaseModel, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "day_off_overtimes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    day_off_id: Mapped[int] = mapped_column(ForeignKey("day_offs.id"), index=True)
    overtime_id: Mapped[int] = mapped_column(ForeignKey("overtimes.id"), index=True)
    used_hours: Mapped[float] = mapped_column(Float, default=0.0)

    day_off: Mapped["DayOffModel"] = relationship(back_populates="day_off_overtimes")
    overtime: Mapped["OvertimeModel"] = relationship(back_populates="day_off_overtimes")


    def __repr__(self):
        return f"DayOffOvertimeModel(id={self.id}, day_off_id={self.day_off_id}, overtime_id={self.overtime_id}, used_hours={self.used_hours})"
    