from typing import Optional

from pydantic import BaseModel
from app.models.project.project import ProjectBase
from app.models.module.module import ModuleSummary

# Base


class ProjectModuleBase(BaseModel):
    project_id: Optional[int]
    module_id: Optional[int]

    class Config:
        orm_mode = True


class ProjectModuleCreate(ProjectModuleBase):
    module_id: int
    project_id: int


class ProjectModuleUpdate(ProjectModuleBase):
    project_module_id: int


class ProjectModuleSummary(ProjectModuleBase):
    project_module_id: int
    project: Optional[ProjectBase]
    module: Optional[ModuleSummary]
