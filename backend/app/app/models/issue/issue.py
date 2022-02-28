from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.models.issue.type import IssueTypeSummary
from app.models.issue.status import IssueStatusSummary
from app.models.issue.priority import IssuePrioritySummary
from app.models.project.project import ProjectSummary
from app.models.project.module import ProjectModuleSummary
from app.models.user.user import UserInDBBase


class IssueBase(BaseModel):
    issue_title: Optional[str]
    issue_description: Optional[str]
    type_id: Optional[int]
    status_id: Optional[int]
    priority_id: Optional[int]
    module_id: Optional[int]
    assigned_to: Optional[int]
    attachment_url: Optional[List[str]]

    class Config:
        orm_mode = True


class IssueCreate(IssueBase):
    issue_title: str
    project_id: int
    type_id: int
    status_id: int
    module_id: int


class IssueUpdate(IssueBase):
    issue_id: int


class IssueSummary(IssueBase):
    issue_id: int
    project_id: int
    created_by: int
    created_on: datetime
    project: Optional[ProjectSummary]
    type: Optional[IssueTypeSummary]
    status: Optional[IssueStatusSummary]
    priority: Optional[IssuePrioritySummary]
    module: Optional[ProjectModuleSummary]
    created_user: Optional[UserInDBBase]
    assigned_to_user: Optional[UserInDBBase]

    class Config:
        orm_mode = True

class IssueMinimal(BaseModel):
    issue_id: int
    issue_title: Optional[str]
    project_id: int
    type_id: Optional[int]
    status_id: Optional[int]
    created_by: int
    created_on: datetime
    project: Optional[ProjectSummary]
    type: Optional[IssueTypeSummary]
    status: Optional[IssueStatusSummary]
    created_user: Optional[UserInDBBase]
    assigned_to: Optional[UserInDBBase]

    class Config:
        orm_mode = True


class IssueStatusCount(BaseModel):
    status_id: Optional[int]
    status: Optional[str]
    count: Optional[int] = 0

    class Config:
        orm_mode = True


class IssueProjectCount(BaseModel):
    project_id: Optional[int]
    project_name: Optional[str]
    count: Optional[int] = 0

    class Config:
        orm_mode = True


class IssueDetailCount(BaseModel):
    project_id: Optional[int] = None
    project_name: Optional[str]
    status_id: Optional[int] = None
    status: Optional[str]
    count: Optional[int] = 0

    class Config:
        orm_mode = True
