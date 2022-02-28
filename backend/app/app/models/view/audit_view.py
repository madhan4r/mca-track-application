from datetime import datetime
from app.db_models.enum.enum import AuditType
from typing import Optional
from pydantic import BaseModel


class AuditViewBase(BaseModel):
    audit_view_type: Optional[str]
    issue_id: Optional[int]
    issue_title: Optional[str]
    type_id: Optional[int]
    type_name: Optional[str]
    status_id: Optional[int]
    status_name: Optional[str]
    project_id: Optional[int]
    project_name: Optional[str]
    audit_id: Optional[int]
    audit_type: Optional[AuditType]
    previous_status_id: Optional[int]
    previous_status_name: Optional[str]
    updated_status_id: Optional[int]
    updated_status_name: Optional[str]
    previous_type_id: Optional[int]
    previous_type_name: Optional[str]
    updated_type_id: Optional[int]
    updated_type_name: Optional[str]
    comments: Optional[str]
    created_on: datetime
    created_by: Optional[int]
    created_by_name: Optional[str]

    class Config:
        orm_mode = True


class AuditViewCreate(AuditViewBase):
    pass


class AuditViewUpdate(AuditViewBase):
    pass


class AuditViewSummary(AuditViewBase):
    pass
