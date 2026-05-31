from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, VARCHAR, ForeignKey

from src.domain.entities.department import Department


from .base import BaseModel, CreatedAtMixin, UpdatedAtMixin


if TYPE_CHECKING:
    from src.infrastructure.database.models import UserModel


class DepartmentModel(BaseModel, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(64), unique=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey("organizations.id"))

    users: Mapped[list["UserModel"]] = relationship(back_populates="department")


    def __repr__(self) -> str:
        return f"Department(id={self.id!r}, name={self.name!r}, organization_id={self.organization_id!r})"


    @classmethod
    def from_entity(cls, entity: "Department") -> "DepartmentModel":
        return cls(
            id=entity.id or None,
            name=entity.name,
            organization_id=entity.organization_id,
        )
    
    def to_entity(self) -> "Department":
        return Department(
            id=self.id,
            name=self.name,
            organization_id=self.organization_id,
        )