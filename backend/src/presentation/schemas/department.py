from datetime import datetime

from pydantic import BaseModel


class DepartmentBase(BaseModel):
    name: str
    organization_id: int


class CreateDepartment(DepartmentBase):
    pass


class DepartmentResponse(DepartmentBase):
    id: int
    created_at: datetime
    updated_at: datetime
