from app.db_models.issue.issue import Issue
from app.db_models.project.module import ProjectModule
from typing import Any, Dict, Optional, Union
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.db_models.project.project import Project
from app.models.project.project import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):

    def get(self, db: Session, id: Any) -> Optional[Project]:
        return db.query(Project).filter(Project.project_id == id).first()

    def create_project(self, db: Session, obj_in: ProjectCreate) -> Project:
        model_data = db.query(Project).filter(
            Project.project_name == obj_in.project_name).first()
        if not model_data:
            model_data = super().create(db, obj_in=obj_in)
        else:
            raise HTTPException(
                status_code=400,
                detail="Project name already exists",
            )
        return model_data

    def update(
        self, db: Session, *, db_obj: Project, obj_in: Union[ProjectUpdate, Dict[str, Any]]
    ) -> Project:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if(update_data.get('project_name', None)):
            unique_constraint_exist = project.check_unique_constraint_exists(
                db=db, project_name=update_data.get('project_name'))
            if unique_constraint_exist:
                if not unique_constraint_exist.project_id == update_data.get('project_id'):
                    raise HTTPException(status_code=400,
                                        detail="Project name already exists")

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def check_unique_constraint_exists(self, db: Session, project_name: str):
        return db.query(Project).filter(Project.project_name == project_name).first()

    def delete(self, db: Session, id: Any):
        project = db.query(Project).filter(
            Project.project_id == id).first()
        project_module = db.query(ProjectModule).filter(
            ProjectModule.project_id == id).first()
        issues = db.query(Issue).filter(Issue.project_id == id).first()

        if project is None and project_module is None and issues is None:
            super().remove(db, id=id)
            return "Requested project has been deleted"
        else:
            raise HTTPException(
                status_code=400,
                detail="Requested project id exist in another table",
            )


project = CRUDProject(Project)
