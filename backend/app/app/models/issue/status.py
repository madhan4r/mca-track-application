from typing import Optional

from pydantic import BaseModel


# Base
class IssueStatusBase(BaseModel):
    status: Optional[str]

    class Config:
        orm_mode = True

class IssueStatusCreate(IssueStatusBase):
    status: str


class IssueStatusUpdate(IssueStatusBase):
    issue_status_id: int


class IssueStatusSummary(IssueStatusUpdate):
    pass
