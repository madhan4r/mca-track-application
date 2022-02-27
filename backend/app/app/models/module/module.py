from typing import Optional

from pydantic import BaseModel


# Base
class ModuleBase(BaseModel):
    module_name: Optional[str]

    class Config:
        orm_mode = True


class ModuleCreate(ModuleBase):
    module_name: str


class ModuleUpdate(ModuleBase):
    module_id: Optional[int]


class ModuleSummary(ModuleBase):
    module_id: int
