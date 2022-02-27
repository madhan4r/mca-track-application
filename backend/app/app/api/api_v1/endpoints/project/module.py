from app.crud.project.module import project_module
from app.api.deps import get_db
from app.models.project.module import ProjectModuleCreate, ProjectModuleSummary, ProjectModuleUpdate
from app.db_models.project.project import Project
from app.db_models.module.module import Module
from app.db_models.project.module import ProjectModule

from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.requests import Request
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/')
def create_project_module(
    data_access_filter: ProjectModuleCreate,
    db_session: Session = Depends(get_db),
):
    return project_module.create_project_module(db=db_session, obj_in=data_access_filter)


@router.get('/', response_model=List[ProjectModuleSummary])
def get_project_modules(
    request: Request,
    db_session: Session = Depends(get_db),
    all_rows: bool = True,
    fetch_row_count: bool = False
) -> List[ProjectModuleSummary]:
    return project_module.get_all(
        db_session=db_session,
        request=request,
        db_model=ProjectModule,
        join_db_models=[Project, Module],
        is_outer_join=True,
        fetch_row_count=fetch_row_count,
        all_rows=all_rows
    )


@router.put('/', response_model=ProjectModuleSummary)
def update_project_module(
    data_access_filter: ProjectModuleUpdate,
    db_session: Session = Depends(get_db),

):
    module_in = project_module.get(
        db=db_session, id=data_access_filter.project_module_id)
    if not module_in:
        raise HTTPException(
            status_code=400, detail='Requested module does not exist')
    return project_module.update(db=db_session, db_obj=module_in, obj_in=data_access_filter)


@router.delete("/delete/{project_module_id}")
def delete_project_module(
    project_module_id: int,
    db_session: Session = Depends(get_db),

):
    module_in = project_module.get(db_session, id=project_module_id)
    if not module_in:
        raise HTTPException(
            status_code=404,
            detail="Requested module not exist in the system",
        )
    return project_module.delete(db_session, id=project_module_id)
