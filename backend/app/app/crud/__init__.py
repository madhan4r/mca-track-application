# from .crud_item import item
# from .user import user

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from app.db_models.item import Item
# from app.models.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemSummary, ItemCreate, ItemUpdate](Item)

from app.crud.base import CRUDBase

# Project
from app.models.project.project import ProjectCreate, ProjectUpdate, ProjectSummary
from app.db_models.project.project import Project
project = CRUDBase[Project, ProjectCreate, ProjectUpdate](Project)


# Module
from app.models.module.module import ModuleCreate, ModuleSummary, ModuleUpdate
from app.db_models.module.module import Module
module = CRUDBase[Module, ModuleCreate, ModuleUpdate](Module)

# Project Module
from app.models.project.module import ProjectModuleCreate, ProjectModuleSummary, ProjectModuleUpdate
from app.db_models.project.module import ProjectModule
project_module = CRUDBase[ProjectModule, ProjectModuleCreate, ProjectModuleUpdate](ProjectModule)

# Issue Status
from app.models.issue.status import IssueStatusCreate, IssueStatusSummary, IssueStatusUpdate
from app.db_models.issue.status import IssueStatus
issue_status = CRUDBase[IssueStatus, IssueStatusCreate, IssueStatusUpdate](IssueStatus)

# Issue Type
from app.models.issue.type import IssueTypeCreate, IssueTypeSummary, IssueTypeUpdate
from app.db_models.issue.type import IssueType
issue_type = CRUDBase[IssueType, IssueTypeCreate, IssueTypeUpdate](IssueType)

# Issue Priority
from app.models.issue.priority import IssuePriorityCreate, IssuePrioritySummary, IssuePriorityUpdate
from app.db_models.issue.priority import IssuePriority
issue_priority = CRUDBase[IssuePriority, IssuePriorityCreate, IssuePriorityUpdate](IssuePriority)