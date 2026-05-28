from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, VARCHAR, ForeignKey

from src.domain.entities.organization import Organization


from .base import BaseModel, CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from src.infrastructure.database.models import UserModel


class OrganizationModel(BaseModel, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(64), unique=True)
    boss_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            use_alter=True,
            name="fk_organization_boss_id",
        ),
    )

    users: Mapped[list["UserModel"]] = relationship(
        back_populates="organization",
        foreign_keys="[UserModel.organization_id]",
    )
    boss: Mapped["UserModel"] = relationship(
        foreign_keys="[OrganizationModel.boss_id]",
    )

    def __repr__(self) -> str:
        return f"Organization(id={self.id}, name={self.name}, boss_id={self.boss_id})"

    @classmethod
    def from_entity(cls, entity: "Organization") -> "OrganizationModel":
        return cls(
            id=entity.id,
            name=entity.name,
            boss_id=entity.boss_id,
        )

    def to_entity(self) -> "Organization":
        return Organization(
            id=self.id,
            name=self.name,
            boss_id=self.boss_id,
        )
