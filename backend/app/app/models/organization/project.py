from typing import List, Optional

from pydantic import BaseModel
from app.models.project.project import ProjectBase
from app.models.organization.organization import OrganizationBase


# Base
class OrganizationProjectBase(BaseModel):
    project_id: Optional[int]
    organization_id: Optional[int]

    class Config:
        orm_mode = True


class OrganizationProjectCreate(OrganizationProjectBase):
    project_id: int
    organization_id: int


class OrganizationProjectUpdate(OrganizationProjectBase):
    organization_project_id: int


class OrganizationProjectSummary(OrganizationProjectBase):
    organization_project_id: int
    project: Optional[ProjectBase]
    organization: Optional[OrganizationBase]
    issue_count: Optional[int]
    open_issue_count: Optional[int]
