from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, VARCHAR, Enum as SaEnum, ForeignKey, Boolean

from src.domain.entities.user import User
from src.domain.enums.rank import Rank
from src.domain.enums.role import Role
from src.domain.enums.work_mode import WorkMode

from .base import BaseModel, CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from src.infrastructure.database.models import (
        DepartmentModel,
        OrganizationModel,
        OvertimeModel,
        DayOffModel,
    )


class UserModel(BaseModel, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(VARCHAR(64), unique=True)
    hashed_password: Mapped[str] = mapped_column(VARCHAR(128))
    surname: Mapped[str] = mapped_column(VARCHAR(64))
    first_name: Mapped[str] = mapped_column(VARCHAR(64))
    patronymic: Mapped[str] = mapped_column(VARCHAR(64))
    position: Mapped[str] = mapped_column(VARCHAR(64))
    role: Mapped[Role] = mapped_column(SaEnum(Role), default=Role.USER)
    rank: Mapped[Rank] = mapped_column(SaEnum(Rank))
    work_mode: Mapped[WorkMode] = mapped_column(SaEnum(WorkMode))
    department_id: Mapped[int] = mapped_column(ForeignKey("departments.id"))
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    department: Mapped["DepartmentModel"] = relationship(
        back_populates="users",
        foreign_keys=[department_id],
    )
    organization: Mapped["OrganizationModel"] = relationship(
        back_populates="users",
        foreign_keys=[organization_id],
    )
    overtimes: Mapped[list["OvertimeModel"]] = relationship(back_populates="user")
    day_offs: Mapped[list["DayOffModel"]] = relationship(back_populates="user")


    def __repr__(self) -> str:
        return f"User(id={self.id!r}, login={self.login!r}, role={self.role!r}, rank={self.rank!r}, work_mode={self.work_mode!r}, department_id={self.department_id!r}, organization_id={self.organization_id!r})"


    @classmethod
    def from_entity(cls, entity: "User") -> "UserModel":
        return cls(
            id=entity.id or None,
            login=entity.login,
            hashed_password=entity.hashed_password,
            surname=entity.surname,
            first_name=entity.first_name,
            patronymic=entity.patronymic,
            position=entity.position,
            role=entity.role,
            rank=entity.rank,
            work_mode=entity.work_mode,
            department_id=entity.department_id,
            organization_id=entity.organization_id,
            is_active=entity.is_active,
        )
    
    def to_entity(self) -> User:
        return User(
            id=self.id,
            login=self.login,
            hashed_password=self.hashed_password,
            surname=self.surname,
            first_name=self.first_name,
            patronymic=self.patronymic,
            position=self.position,
            role=self.role,
            rank=self.rank,
            work_mode=self.work_mode,
            department_id=self.department_id,
            organization_id=self.organization_id,
            is_active=self.is_active,
        )