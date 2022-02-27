from app.crud.issue.status import issue_status
from app.api.deps import get_db
from app.models.issue.status import IssueStatusSummary, IssueStatusCreate, IssueStatusUpdate
from app.db_models.issue.issue import Issue
from app.db_models.issue.status import IssueStatus
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.requests import Request
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/')
def create_issue_status(
    data_access_filter: IssueStatusCreate,
    db_session: Session = Depends(get_db),
):
    return issue_status.create_status(db=db_session, obj_in=data_access_filter)


@router.get('/', response_model=List[IssueStatusSummary])
def get_issue_status(
    request: Request,
    db_session: Session = Depends(get_db),
    all_rows: bool = True,
    fetch_row_count: bool = False
) -> List[IssueStatusSummary]:
    return issue_status.get_all(
        request=request,
        db_session=db_session,
        db_model=IssueStatus,
        join_db_models=[Issue],
        is_outer_join=True,
        all_rows=all_rows,
        fetch_row_count=fetch_row_count
    )


@router.put('/update', response_model=IssueStatusSummary)
def update_issue_state(
    data_access_filter: IssueStatusUpdate,
    db_session: Session = Depends(get_db),
):
    status_in = issue_status.get(db=db_session, id=data_access_filter.issue_status_id)
    if not status_in:
        raise HTTPException(
            status_code=404,
            detail="Requested issue status not exist.",
        )
    return issue_status.update(db=db_session, db_obj=status_in, obj_in=data_access_filter)


@router.delete("/delete/{issue_status_id}")
def delete_issue_status(
    issue_status_id: int,
    db_session: Session = Depends(get_db),
):
    status_in = issue_status.get(db_session, id=issue_status_id)
    if not status_in:
        raise HTTPException(
            status_code=404,
            detail="Requested status does not exist in the system",
        )
    return issue_status.delete(db_session, id=issue_status_id)
