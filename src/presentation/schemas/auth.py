from datetime import datetime

from pydantic import BaseModel

from src.domain.enums.rank import Rank
from src.domain.enums.role import Role
from src.domain.enums.work_mode import WorkMode


class RegisterUser(BaseModel):
    login: str
    password: str  # ← только в request
    surname: str
    first_name: str
    patronymic: str
    position: str
    rank: Rank
    work_mode: WorkMode
    department_id: int
    organization_id: int


class LoginUser(BaseModel):
    login: str
    password: str


class UserResponse(BaseModel):
    id: int
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


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"