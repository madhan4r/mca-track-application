from typing import Optional

from pydantic import BaseModel


# Base
class OrganizationTypeBase(BaseModel):
    type: Optional[str]
    type_description: Optional[str]
    class Config:
        orm_mode = True

class OrganizationTypeCreate(OrganizationTypeBase):
    type: str

class OrganizationTypeUpdate(OrganizationTypeBase):
    organization_type_id: int

class OrganizationType(OrganizationTypeBase):
    organization_type_id: int