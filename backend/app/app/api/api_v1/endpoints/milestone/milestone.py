from app.crud.milestone.milestone import milestone
from app.api.deps import get_db
from app.models.milestone.milestone import MilestoneCreate, MilestoneUpdate, MilestoneSummary
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session


router = APIRouter()


@router.post('/')
def create_milestone(
    data_access_filter: MilestoneCreate,
    db_session: Session = Depends(get_db),
):
    return milestone.create(db=db_session, obj_in=data_access_filter)


@router.get('/', response_model=List[MilestoneSummary])
def get_milestones(
    db_session: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
) -> List[MilestoneSummary]:
    return milestone.get_multi(db=db_session, skip=skip, limit=limit)


@router.put('/update', response_model=MilestoneSummary)
def update_milestone(
    data_access_filter: MilestoneUpdate,
    db_session: Session = Depends(get_db),
):
    milestone_in = milestone.get(db=db_session, id=data_access_filter.milestone_id)
    if not milestone_in:
        raise HTTPException(
            status_code=404,
            detail="Requested milestone not exist.",
        )
    return milestone.update(db=db_session, db_obj=milestone_in, obj_in=data_access_filter)


@router.delete("/delete/{milestone_id}")
def delete_milestone(
    milestone_id: int,
    db_session: Session = Depends(get_db),

):
    milestone_in = milestone.get(db_session, id=milestone_id)
    if not milestone_in:
        raise HTTPException(
            status_code=404,
            detail="Requested milestone does not exist in the system",
        )
    return milestone.delete(db_session, id=milestone_id)
