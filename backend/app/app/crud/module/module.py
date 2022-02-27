from app.db_models.project.module import ProjectModule
from app.db_models.module.module import Module
from typing import Any, Dict, Union
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.module.module import ModuleCreate, ModuleUpdate, ModuleSummary


class CRUDModule(CRUDBase[Module, ModuleCreate, ModuleUpdate]):

    def create_module(self, db: Session, obj_in: ModuleCreate) -> ModuleSummary:
        model_data = db.query(Module).filter(
            Module.module_name == obj_in.module_name).first()

        if not model_data:
            model_data = super().create(db, obj_in=obj_in)
        else:
            raise HTTPException(
                status_code=400,
                detail=f" Requested module already exists",
            )
        return model_data

    def get(self, db: Session, id: Any) -> ModuleSummary:
        return db.query(Module).filter(Module.module_id == id).first()

    def update(
        self, db: Session, *, db_obj: Module, obj_in: Union[ModuleUpdate, Dict[str, Any]]
    ) -> ModuleSummary:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if(update_data.get('module_name', None)):
            unique_constraint_exist = module.check_unique_constraint_exists(
                db=db, module_name=update_data.get('module_name'))
            if unique_constraint_exist:
                if not unique_constraint_exist.module_id == update_data.get('module_id'):
                    raise HTTPException(status_code=400,
                                        detail="module already exists")

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def check_unique_constraint_exists(self, db: Session, module_name: str):
        return db.query(Module).filter(Module.module_name == module_name).first()

    def delete(self, db: Session, id: Any):
        module_in = db.query(ProjectModule).filter(
            ProjectModule.module_id == id).first()
        if module_in is None:
            super().remove(db, id=id)
            return "Requested module has been deleted"
        else:
            raise HTTPException(
                status_code=400,
                detail="Requested module id exist in another table",
            )


module = CRUDModule(Module)
