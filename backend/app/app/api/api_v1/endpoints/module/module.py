from app.crud.module.module import module
from app.api.deps import get_db
from app.models.module.module import ModuleCreate, ModuleUpdate, ModuleSummary
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.post('/')
def create_module(
    data_access_filter: ModuleCreate,
    db_session: Session = Depends(get_db),
):
    return module.create_module(db=db_session, obj_in=data_access_filter)


@router.get('/', response_model=List[ModuleSummary])
def get_modules(
    db_session: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
) -> List[ModuleSummary]:
    return module.get_multi(db=db_session, skip=skip, limit=limit)


@router.put('/update', response_model=ModuleSummary)
def update_module(
    data_access_filter: ModuleUpdate,
    db_session: Session = Depends(get_db),
):
    module_in = module.get(db=db_session, id=data_access_filter.module_id)
    if not module_in:
        raise HTTPException(
            status_code=404,
            detail="Requested module not exist.",
        )
    return module.update(db=db_session, db_obj=module_in, obj_in=data_access_filter)


@router.delete("/delete/{module_id}")
def delete_module(
    module_id: int,
    db_session: Session = Depends(get_db),
):
    module_in = module.get(db_session, id=module_id)
    if not module_in:
        raise HTTPException(
            status_code=404,
            detail="Requested module not exist in the system",
        )
    return module.delete(db_session, id=module_id)
