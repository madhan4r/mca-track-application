from app.db_models.issue.issue import Issue
from app.db_models.project.module import ProjectModule
from typing import Any, Dict, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from fastapi import HTTPException
from app.models.project.module import ProjectModuleCreate, ProjectModuleSummary, ProjectModuleUpdate


class CRUDProjectModule(CRUDBase[ProjectModule, ProjectModuleCreate, ProjectModuleUpdate]):

    def get(self, db: Session, id: Any) -> ProjectModuleSummary:
        return db.query(ProjectModule).filter(ProjectModule.project_module_id == id).first()

    def create_project_module(self, db: Session, *, obj_in: ProjectModuleCreate) -> ProjectModuleSummary:
        model_data = db.query(ProjectModule).filter(
            ProjectModule.project_id == obj_in.project_id).filter(ProjectModule.module_id == obj_in.module_id).first()
        if model_data is None:
            model_data = super().create(db, obj_in=obj_in)
        else:
            raise HTTPException(
                status_code=400,
                detail="module already exists",
            )
        return model_data

    def delete(self, db: Session, id: Any):
        issues = db.query(Issue).filter(Issue.module_id == id).first()

        if issues is None:
            super().remove(db, id=id)
            return "Requested module has been deleted"
        else:
            raise HTTPException(
                status_code=400,
                detail="Requested module id exist in another table",
            )

    def update(
        self, db: Session, *, db_obj: ProjectModule, obj_in: Union[ProjectModuleUpdate, Dict[str, Any]]
    ) -> ProjectModuleSummary:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if(update_data.get('module_id', 'project_id')):
            unique_constraint_exist = project_module.check_unique_constraint_exists(
                db=db, module_id=update_data.get('module_id'), project_id=update_data.get('project_id'))
            if unique_constraint_exist:
                if not unique_constraint_exist.project_module_id == update_data.get('project_module_id'):
                    raise HTTPException(status_code=400,
                                        detail="Module already exists")

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def check_unique_constraint_exists(self, db: Session, module_id: int, project_id: int):
        return db.query(ProjectModule).filter(ProjectModule.module_id == module_id).filter(ProjectModule.project_id == project_id).first()


project_module = CRUDProjectModule(ProjectModule)
