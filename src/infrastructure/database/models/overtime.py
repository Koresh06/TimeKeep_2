from datetime import date, time
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, VARCHAR, Enum as SaEnum, Date, Time, Float, ForeignKey

from src.domain.entities.overtime import Overtime
from src.domain.enums.overtime_status import OvertimeStatus

from .base import BaseModel, CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from src.infrastructure.database.models import UserModel, DayOffOvertimeModel


class OvertimeModel(BaseModel, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "overtimes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_: Mapped[date] = mapped_column(Date)
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    used_hours: Mapped[float] = mapped_column(Float, default=0.0)
    description: Mapped[str] = mapped_column(VARCHAR(64))
    status: Mapped[OvertimeStatus] = mapped_column(
        SaEnum(OvertimeStatus),
        default=OvertimeStatus.ACTIVE,
    )

    user: Mapped["UserModel"] = relationship(back_populates="overtimes")
    day_off_overtimes: Mapped[list["DayOffOvertimeModel"]] = relationship(back_populates="overtime")


    def __repr__(self):
        return f"Overtime({self.id}, {self.user_id}, {self.date_}, {self.start_time}, {self.end_time}, {self.used_hours}, {self.description}, {self.status})"

    @classmethod
    def from_entity(cls, entity: "Overtime") -> "OvertimeModel":
        return cls(
            id=entity.id or None,
            user_id=entity.user_id,
            date_=entity.date_,
            start_time=entity.start_time,
            end_time=entity.end_time,
            used_hours=entity.used_hours,
            description=entity.description,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
    
    def to_entity(self) -> Overtime:
        return Overtime(
            id=self.id,
            user_id=self.user_id,
            date_=self.date_,
            start_time=self.start_time.replace(tzinfo=None),
            end_time=self.end_time.replace(tzinfo=None),
            used_hours=self.used_hours,
            description=self.description,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )