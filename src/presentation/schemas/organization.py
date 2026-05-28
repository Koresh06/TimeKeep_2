from datetime import datetime

from pydantic import BaseModel


class OrganizationBase(BaseModel):
    name: str
    boss_id: int


class CreateOrganization(OrganizationBase):
    pass


class OrganizationResponse(OrganizationBase):
    id: int
    created_at: datetime
    updated_at: datetime
