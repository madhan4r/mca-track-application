from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# Base
class MilestoneBase(BaseModel):
    milestone: Optional[str]
    milestone_date: Optional[datetime]

    class Config:
        orm_mode = True


class MilestoneCreate(MilestoneBase):
    milestone: str


class MilestoneUpdate(MilestoneBase):
    milestone_id: int


class MilestoneSummary(MilestoneBase):
    milestone_id: int
