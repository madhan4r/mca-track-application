from typing import Optional

from pydantic import BaseModel


# Base
class IssuePriorityBase(BaseModel):
    issue_priority: Optional[str]

    class Config:
        orm_mode = True


class IssuePriorityCreate(IssuePriorityBase):
    issue_priority: str


class IssuePriorityUpdate(IssuePriorityBase):
    issue_priority_id: int


class IssuePrioritySummary(IssuePriorityUpdate):
    pass
