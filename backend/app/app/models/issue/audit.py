from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from app.db_models.enum.enum import AuditType
from app.models.issue.status import IssueStatusSummary
from app.models.issue.type import IssueTypeSummary
from app.models.user.user import UserInDBBase


class AuditIssueBase(BaseModel):
    issue_id: Optional[int]
    previous_status_id: Optional[int]
    updated_status_id: Optional[int]
    previous_type_id: Optional[int]
    updated_type_id: Optional[int]
    previous_assignee_id: Optional[int]
    updated_assignee_id: Optional[int]
    comments: Optional[str]
    audit_type: Optional[AuditType]
    attachment_url: Optional[List[str]]

    class Config:
        orm_mode = True


class AuditIssueCreate(AuditIssueBase):
    issue_id: int
    audit_type: AuditType


class AuditIssueUpdate(AuditIssueBase):
    audit_id: int


class AuditIssueSummary(AuditIssueBase):
    audit_id: int
    previous_status: Optional[IssueStatusSummary]
    updated_status: Optional[IssueStatusSummary]
    previous_type: Optional[IssueTypeSummary]
    updated_type: Optional[IssueTypeSummary]
    previous_assignee: Optional[UserInDBBase]
    updated_assignee: Optional[UserInDBBase]
    created_user: Optional[UserInDBBase]
    created_by: int
    created_on: datetime
