from fastapi.exceptions import HTTPException
from app.crud.issue.type import issue_type
from app.api.deps import get_db
from app.models.issue.type import IssueTypeSummary, IssueTypeCreate, IssueTypeUpdate
from app.db_models.issue.issue import Issue
from app.db_models.issue.type import IssueType
from typing import List
from fastapi import APIRouter, Body, Depends
from starlette.requests import Request
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/')
def create_issue_type(
    data_access_filter: IssueTypeCreate,
    db_session: Session = Depends(get_db),
):
    return issue_type.create_type(db=db_session, obj_in=data_access_filter)


@router.get('/', response_model=List[IssueTypeSummary])
def get_issue_types(
    request: Request,
    db_session: Session = Depends(get_db),
    all_rows: bool = True,
    fetch_row_count: bool = False
) -> List[IssueTypeSummary]:
    return issue_type.get_all(
        request=request,
        db_session=db_session,
        db_model=IssueType,
        join_db_models=[Issue],
        is_outer_join=True,
        all_rows=all_rows,
        fetch_row_count=fetch_row_count
    )


@router.put('/update', response_model=IssueTypeSummary)
def update_issue_types(
    data_access_filter: IssueTypeUpdate,
    db_session: Session = Depends(get_db),
):
    type_in = issue_type.get(db=db_session, id=data_access_filter.issue_type_id)
    if not type_in:
        raise HTTPException(
            status_code=404,
            detail="Requested issue type not exist.",
        )
    return issue_type.update(db=db_session, db_obj=type_in, obj_in=data_access_filter)


@router.delete("/delete/{issue_type_id}")
def delete_issue_type(
    issue_type_id: int,
    db_session: Session = Depends(get_db),
):
    type_in = issue_type.get(db_session, id=issue_type_id)
    if not type_in:
        raise HTTPException(
            status_code=404,
            detail="Requested type does not exist in the system",
        )
    return issue_type.delete(db_session, id=issue_type_id)
