from typing import Optional

from datetime import datetime

from pydantic import BaseModel
from app.models.project.project import ProjectBase
from app.models.milestone.milestone import MilestoneSummary


class ProjectMilestoneBase(BaseModel):
    project_id: Optional[int]
    milestone_id: Optional[int]

    class Config:
        orm_mode = True


class ProjectMilestoneCreate(ProjectMilestoneBase):
    project_id: int
    milestone_id: int


class ProjectMilestoneUpdate(ProjectMilestoneBase):
    project_milestone_id: int


class ProjectMilestoneSummary(ProjectMilestoneBase):
    project_milestone_id: int
    project: Optional[ProjectBase]
    milestone: Optional[MilestoneSummary]
