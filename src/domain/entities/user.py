from dataclasses import dataclass, field

from src.domain.entities.base import BaseEntity
from src.domain.enums.rank import Rank
from src.domain.enums.role import Role
from src.domain.enums.work_mode import WorkMode


@dataclass(kw_only=True)
class User(BaseEntity):
    login: str
    hashed_password: str
    surname: str
    first_name: str
    patronymic: str
    position: str
    role: Role = field(default=Role.USER)
    rank: Rank
    work_mode: WorkMode
    department_id: int
    organization_id: int
    is_active: bool = field(default=True)
    
    def change_role(self, role: Role) -> None:
        self.role = role
        self.touch()
    
    def change_work_mode(self, work_mode: WorkMode) -> None:
        self.work_mode = work_mode
        self.touch()
    
    def deactivate(self) -> None:
        self.is_active = False
        self.touch()
    
    def activate(self) -> None:
        self.is_active = True
        self.touch()