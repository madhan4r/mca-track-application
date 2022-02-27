from app.crud.issue.priority import issue_priority
from app.api.deps import get_db
from app.models.issue.priority import IssuePrioritySummary, IssuePriorityCreate, IssuePriorityUpdate
from app.db_models.issue.priority import IssuePriority
from app.db_models.issue.issue import Issue
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.requests import Request
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/', response_model=IssuePrioritySummary)
def create_issue_priority(
    data_access_filter: IssuePriorityCreate,
    db_session: Session = Depends(get_db),
) -> IssuePrioritySummary:
    return issue_priority.create_priority(db=db_session, obj_in=data_access_filter)


@router.get('/', response_model=List[IssuePrioritySummary])
def get_issue_priority(
    request: Request,
    db_session: Session = Depends(get_db),
    all_rows: bool = True,
    fetch_row_count: bool = False
) -> List[IssuePrioritySummary]:
    return issue_priority.get_all(
        request=request,
        db_session=db_session,
        db_model=IssuePriority,
        join_db_models=[Issue],
        is_outer_join=True,
        all_rows=all_rows,
        fetch_row_count=fetch_row_count
    )


@router.put('/update', response_model=IssuePrioritySummary)
def update_issue_priority(
    data_access_filter: IssuePriorityUpdate,
    db_session: Session = Depends(get_db),
):
    priority_in = issue_priority.get(
        db=db_session, id=data_access_filter.issue_priority_id)
    if not priority_in:
        raise HTTPException(
            status_code=404,
            detail="Requested issue priority not exist.",
        )
    return issue_priority.update(db=db_session, db_obj=priority_in, obj_in=data_access_filter)


@router.delete("/delete/{issue_priority_id}")
def delete_issue_priority(
    issue_priority_id: int,
    db_session: Session = Depends(get_db),
):
    priority_in = issue_priority.get(db_session, id=issue_priority_id)
    if not priority_in:
        raise HTTPException(
            status_code=404,
            detail="Requested priority does not exist in the system",
        )
    return issue_priority.delete(db_session, id=issue_priority_id)
