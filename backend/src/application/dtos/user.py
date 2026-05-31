from dataclasses import dataclass
from datetime import datetime

from src.domain.entities.user import User
from src.domain.enums.rank import Rank
from src.domain.enums.role import Role
from src.domain.enums.work_mode import WorkMode


@dataclass(frozen=True)
class UserDTO:
    id: int
    login: str
    password: str
    surname: str
    first_name: str
    patronymic: str
    position: str
    role: Role
    rank: Rank
    work_mode: WorkMode
    department_id: int
    organization_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, entity: "User") -> "UserDTO":
        return cls(
            id=None if entity.id == 0 else entity.id,
            login=entity.login,
            password=entity.hashed_password,
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
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
