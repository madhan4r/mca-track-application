from fastapi import APIRouter

from app.api.api_v1.endpoints import login
from app.api.api_v1.endpoints.enum import enum_type
from app.api.api_v1.endpoints.user import user
from app.api.api_v1.endpoints.organization import (
    organization,
    organization_type, project as organization_project
)
from app.api.api_v1.endpoints.milestone import milestone
from app.api.api_v1.endpoints.module import module
from app.api.api_v1.endpoints.project import project, milestone as project_milestone, module as project_module
from app.api.api_v1.endpoints.issue import (
    status as issue_status,
    type as issue_type,
    priority as issue_priority,
    issue,
    audit
)
from app.api.api_v1.endpoints.view import audit_view

api_router = APIRouter()

# Auth
api_router.include_router(login.router, tags=["Login"])

# User
api_router.include_router(user.router, prefix="/users", tags=["users"])

# Organization
api_router.include_router(organization_type.router, prefix="/organization", tags=["Organization Type"])
api_router.include_router(organization.router, prefix="/organization", tags=["Organization"])
api_router.include_router(organization_project.router, prefix="/organization/projects", tags=["Organization Projects"])

# Milestone
api_router.include_router(milestone.router, prefix="/milestone", tags=['Milestones'])

# Module
api_router.include_router(module.router, prefix="/module", tags=['Modules'])

# Project
api_router.include_router(project.router, prefix="/project", tags=['Projects'])
api_router.include_router(project_milestone.router, prefix="/project/milestone", tags=['Projects'])
api_router.include_router(project_module.router, prefix="/project/module", tags=['Projects'])

# Issue
api_router.include_router(issue_status.router, prefix="/issue/status", tags=['Issues'])
api_router.include_router(issue_type.router, prefix="/issue/type", tags=['Issues'])
api_router.include_router(issue_priority.router, prefix="/issue/priority", tags=['Issues'])
api_router.include_router(issue.router, prefix="/issue", tags=['Issues'])

# Audit Issue
api_router.include_router(audit.router, prefix="/issue/audit", tags=['Audit Issue'])

# Enumerations
api_router.include_router(
    enum_type.router, prefix="/enum/labels", tags=['Enumerations'])

# Views
api_router.include_router(audit_view.router, prefix="/view", tags=["Audit View"])
