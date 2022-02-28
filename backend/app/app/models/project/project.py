from typing import Optional
from datetime import datetime

from pydantic import BaseModel


# Base
class ProjectBase(BaseModel):
    project_name: Optional[str]

    class Config:
        orm_mode = True


class ProjectCreate(ProjectBase):
    project_name: str


class ProjectUpdate(ProjectBase):
    project_id: int


class ProjectSummary(ProjectUpdate):
    created_on: Optional[datetime]
    issue_count: Optional[int]
    open_issue_count: Optional[int]
    pass
