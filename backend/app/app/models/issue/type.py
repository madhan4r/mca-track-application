from typing import Optional

from pydantic import BaseModel


# Base
class IssueTypeBase(BaseModel):
    type: Optional[str]
    type_description: Optional[str]

    class Config:
        orm_mode = True

class IssueTypeCreate(IssueTypeBase):
    type: str


class IssueTypeUpdate(IssueTypeBase):
    issue_type_id: int


class IssueTypeSummary(IssueTypeUpdate):
    pass
