from app.crud.issue.issue import issue
import logging
from app.crud.organization.project import Organizationproject as org_project
from app.api.deps import get_db, get_current_user, get_current_active_superuser
from app.models.organization.project import OrganizationProjectCreate, OrganizationProjectUpdate, OrganizationProjectSummary
from app.db_models.user.user import User
from app.db_models.organization.project import OrganizationProject
from typing import List
from fastapi import APIRouter,  Depends, HTTPException
from starlette.requests import Request
from sqlalchemy.orm import Session
from app.crud.SearchFilter.crud_basic import create_instance
router = APIRouter()


logger = logging.getLogger(__name__)


@router.post('/')
def create_organization_project(
    data_access_filter: OrganizationProjectCreate,
    db_session: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
) -> OrganizationProjectSummary:
    return OrganizationProjectSummary.from_orm(create_instance(db_session=db_session, model=OrganizationProject, obj_in=data_access_filter))


@router.get('/')
def get_organization_projects(
    request: Request,
    db_session: Session = Depends(get_db),
    all_rows: bool = True,
    fetch_row_count: bool = False,
    current_user: User = Depends(get_current_user)
) -> List[OrganizationProjectSummary]:
    data = org_project.get_all(
        db_session=db_session,
        request=request,
        db_model=OrganizationProject,
        all_rows=all_rows,
        fetch_row_count=fetch_row_count
    )
    result = []
    for row in data:
        orm_data = OrganizationProjectSummary.from_orm(row)
        orm_data.issue_count = issue.get_issue_count_project_id(
            db=db_session, project_id=orm_data.project_id)
        orm_data.open_issue_count = issue.get_open_issue_count_project_id(
            db=db_session, project_id=orm_data.project_id)
        result.append(orm_data)
    return result


@router.put('/update')
def update_organization_projects(
    data_access_filter: OrganizationProjectUpdate,
    db_session: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
):
    organization_update = org_project.get(
        db_session, id=data_access_filter.organization_project_id)
    if not organization_update:
        raise HTTPException(
            status_code=404,
            detail="Requested organization project not exist.",
        )
    organization = org_project.update(
        db_session, db_obj=organization_update, obj_in=data_access_filter)
    return organization


@router.delete("/{organization_project_id}")
def delete_organization_project(
    organization_project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
):
    organization_project_in = org_project.get(db, id=organization_project_id)
    if not organization_project_in:
        raise HTTPException(
            status_code=404,
            detail="Requested organization project does not exist in the system",
        )
    organization_project_in = org_project.remove(db, id=organization_project_id)
    return "Requested organization project has been deleted"
