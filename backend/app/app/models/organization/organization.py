from typing import Optional
from datetime import datetime

from pydantic import BaseModel
from app.models.organization.organization_type import OrganizationTypeBase


class OrganizationBase(BaseModel):
    organization_name: Optional[str]
    organization_type_id: Optional[int]
    created_on: Optional[datetime] = datetime.now()

    class Config:
        orm_mode = True


class OrganizationCreate(OrganizationBase):
    organization_name: str
    organization_type_id: int


class OrganizationUpdate(BaseModel):
    organization_id: int
    organization_name: Optional[str]
    organization_type_id: Optional[int]


class Organization(OrganizationBase):
    organization_id: Optional[int]
    organization_type: Optional[OrganizationTypeBase]
