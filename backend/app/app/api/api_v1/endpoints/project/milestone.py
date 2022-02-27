from app.crud.project.milestone import project_milestone
from app.api.deps import get_db
from app.db_models.project.project import Project
from app.models.project.milestone import ProjectMilestoneSummary, ProjectMilestoneCreate, ProjectMilestoneUpdate
from app.db_models.project.milestone import ProjectMilestone
from app.db_models.milestone.milestone import Milestone

from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.requests import Request

router = APIRouter()


@router.post('/')
def create_project_milestone(
    data_access_filter: ProjectMilestoneCreate,
    db_session: Session = Depends(get_db),
):
    return project_milestone.create_project_milestone(db=db_session, obj_in=data_access_filter)


@router.get('/', response_model=List[ProjectMilestoneSummary])
def get_project_milestones(
    request: Request,
    db_session: Session = Depends(get_db),
    all_rows: bool = True,
    fetch_row_count: bool = False
) -> List[ProjectMilestoneSummary]:
    return project_milestone.get_all(
        db_session=db_session,
        request=request,
        db_model=ProjectMilestone,
        join_db_models=[Project, Milestone],
        is_outer_join=True,
        fetch_row_count=fetch_row_count,
        all_rows=all_rows
    )


@router.put('/', response_model=ProjectMilestoneSummary)
def update_project_milestone(
    data_access_filter: ProjectMilestoneUpdate,
    db_session: Session = Depends(get_db),

):
    milestone_in = project_milestone.get(
        db=db_session, id=data_access_filter.project_milestone_id)
    if not milestone_in:
        raise HTTPException(
            status_code=400, detail='Requested milestone does not exist')
    return project_milestone.update(db=db_session, db_obj=milestone_in, obj_in=data_access_filter)


@router.delete("/delete/{project_milestone_id}")
def delete_project_module(
    project_milestone_id: int,
    db_session: Session = Depends(get_db),
):
    milestone_in = project_milestone.get(db_session, id=project_milestone_id)
    if not milestone_in:
        raise HTTPException(
            status_code=404,
            detail="Requested milestone does not exist in the system",
        )
    return project_milestone.delete(db_session, id=project_milestone_id)
