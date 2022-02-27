from typing import List
from fastapi import APIRouter, Depends
from starlette.requests import Request
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_user

from app.crud.SearchFilter.db_model_search_filter import DbModelSearchFilter
from app.models.view.audit_view import AuditViewSummary
from app.db_models.view.audit_view import AuditView
from app.db_models.user.user import User
from app.db_models.organization.project import OrganizationProject

router = APIRouter()


@router.get('/audit_view', response_model=List[AuditViewSummary])
def get_audit_view(
    request: Request,
    all_rows: bool = False,
    db_session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[AuditViewSummary]:
    return DbModelSearchFilter(
        db_session=db_session,
        request=request,
        db_model=AuditView,
        join_db_models=[OrganizationProject],
        join_conditions=[
            AuditView.project_id == OrganizationProject.project_id,
        ],
        is_outer_join=True
    ).get_filtered_data(fetch_row_count=False, all_rows=all_rows)
