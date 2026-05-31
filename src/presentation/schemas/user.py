from datetime import datetime

from pydantic import BaseModel, ConfigDict

from src.domain.enums.rank import Rank
from src.domain.enums.role import Role
from src.domain.enums.work_mode import WorkMode


class UserBase(BaseModel):
    login: str
    surname: str
    first_name: str
    patronymic: str
    position: str
    role: Role
    rank: Rank
    work_mode: WorkMode
    department_id: int
    organization_id: int


class UpdateRoleRequest(BaseModel):
    role: Role


class UpdateWorkModeRequest(BaseModel):
    work_mode: WorkMode


class ActivateUserRequest(BaseModel):
    is_active: bool


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
