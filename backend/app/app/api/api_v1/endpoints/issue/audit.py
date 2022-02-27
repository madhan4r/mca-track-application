from app.crud.SearchFilter.db_model_search_filter import DbModelSearchFilter
from app.crud.issue.audit import audit
from app.api.deps import get_db, get_current_user
from app.models.issue.audit import AuditIssueCreate, AuditIssueUpdate, AuditIssueSummary
from app.db_models.user.user import User
from app.db_models.issue.issue import Issue
from app.db_models.issue.audit import AuditIssue
from app.db_models.issue.status import IssueStatus
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request

router = APIRouter()


@router.post('/', response_model=AuditIssueSummary)
def create_audit_issue(
    data_access_filter: AuditIssueCreate,
    db_session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return audit.create(db=db_session, obj_in=data_access_filter, created_by=current_user.user_id)


@router.get('/', response_model=List[AuditIssueSummary])
def get_issue_audits(
    request: Request,
    db_session: Session = Depends(get_db),
    fetch_row_count: bool = False,
    all_rows: bool = True,
    current_user: User = Depends(get_current_user),
) -> List[AuditIssueSummary]:
    return DbModelSearchFilter(
        db_session=db_session,
        request=request,
        db_model=AuditIssue,
        join_db_models=[
            Issue, IssueStatus,
        ],
        is_outer_join=True
    ).get_filtered_data(fetch_row_count=fetch_row_count, all_rows=all_rows)


@router.put('/update', response_model=AuditIssueSummary)
def update_audit_issue(
    data_access_filter: AuditIssueUpdate,
    db_session: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    audit_in = audit.get(db=db_session, id=data_access_filter.audit_id)
    if not audit_in:
        raise HTTPException(
            status_code=404,
            detail="Requested Audit not exist.",
        )
    return audit.update(db=db_session, db_obj=audit_in, obj_in=data_access_filter)


@router.delete("/{audit_id}")
def delete_audit_issue(
    audit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    audit_in = audit.get(db, id=audit_id)
    if not audit_in:
        raise HTTPException(
            status_code=404,
            detail="Requested aduit does not exist in the system",
        )
    aduit_in = audit.remove(db, id=audit_id)
    return "Requested Audit has been deleted"
