from fastapi import APIRouter

from app.api.api_v1.endpoints import login
from app.api.api_v1.endpoints.enum import enum_type
from app.api.api_v1.endpoints.user import user
from app.api.api_v1.endpoints.module import module
from app.api.api_v1.endpoints.project import project, module as project_module
from app.api.api_v1.endpoints.issue import (
    status as issue_status,
    type as issue_type,
    priority as issue_priority,
    issue,
    audit
)

api_router = APIRouter()

# Auth
api_router.include_router(login.router, tags=["Login"])

# User
api_router.include_router(user.router, prefix="/users", tags=["users"])

# Module
api_router.include_router(module.router, prefix="/module", tags=['Modules'])

# Project
api_router.include_router(project.router, prefix="/project", tags=['Projects'])
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
