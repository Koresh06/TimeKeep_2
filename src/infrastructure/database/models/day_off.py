from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Date, Enum as SaEnum, ForeignKey

from src.domain.entities.day_off import DayOff
from src.domain.enums.day_off_status import DayOffStatus

from .base import BaseModel, CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from src.infrastructure.database.models import UserModel, DayOffOvertimeModel


class DayOffModel(BaseModel, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "day_offs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_: Mapped[date] = mapped_column(Date)
    status: Mapped[DayOffStatus] = mapped_column(
        SaEnum(DayOffStatus),
        default=DayOffStatus.PENDING,
    )
    user: Mapped["UserModel"] = relationship(back_populates="day_offs")
    day_off_overtimes: Mapped[list["DayOffOvertimeModel"]] = relationship(back_populates="day_off")


    def __repr__(self):
        return f"DayOff({self.id}, {self.user_id}, {self.date_}, {self.status})"
    
    @classmethod
    def from_entity(cls, entity: "DayOff") -> "DayOffModel":
        return cls(
            id=entity.id or None,
            user_id=entity.user_id,
            date_=entity.date_,
            status=entity.status,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
    
    def to_entity(self) -> DayOff:
        return DayOff(
            id=self.id,
            user_id=self.user_id,
            date_=self.date_,
            status=self.status,
            created_at=self.created_at,
            updated_at=self.updated_at,
            overtimes=[
                o.overtime.to_entity() for o in self.day_off_overtimes
            ],
        )
