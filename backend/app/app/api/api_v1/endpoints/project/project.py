from app.crud.project.project import project
from app.crud.issue.issue import issue
from app.api.deps import get_db
from app.models.project.project import ProjectSummary, ProjectCreate, ProjectUpdate
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
router = APIRouter()


@router.post('/create')
def create_project(
    data_access_filter: ProjectCreate,
    db_session: Session = Depends(get_db),
):
    return project.create_project(db=db_session, obj_in=data_access_filter)


@router.get('/get/{project_id}', response_model=ProjectSummary)
def get_project_by_id(
    project_id: int,
    db_session: Session = Depends(get_db),
) -> ProjectSummary:
    return project.get(db=db_session, id=project_id)


@router.get('/get', response_model=List[ProjectSummary])
def get_projects(
    db_session: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
) -> List[ProjectSummary]:
    data = project.get_multi(db=db_session, skip=skip, limit=limit)
    result = []
    for row in data:
        orm_data = ProjectSummary.from_orm(row)
        orm_data.issue_count = issue.get_issue_count_project_id(
        db=db_session, project_id=orm_data.project_id)
        orm_data.open_issue_count = issue.get_open_issue_count_project_id(
        db=db_session, project_id=orm_data.project_id)
        result.append(orm_data)
    return result


@router.put('/update')
def update_project(
    data_access_filter: ProjectUpdate,
    db_session: Session = Depends(get_db),
):
    row = project.get(db=db_session, id=data_access_filter.project_id)
    if not row:
        raise HTTPException(status_code=400, detail='Requested project does not exist')
    return project.update(db=db_session, db_obj=row, obj_in=data_access_filter)


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
):
    project_in = project.get(db, id=project_id)
    if not project_in:
        raise HTTPException(
            status_code=404,
            detail="Requested project does not exist in the system",
        )

    return project.delete(db, id=project_id)
