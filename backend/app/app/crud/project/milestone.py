from app.db_models.issue.issue import Issue
from app.db_models.project.milestone import ProjectMilestone
from typing import Any, Dict, Union
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from fastapi import HTTPException
from app.models.project.milestone import ProjectMilestoneCreate, ProjectMilestoneUpdate, ProjectMilestoneSummary


class CRUDProjectMilestone(CRUDBase[ProjectMilestone, ProjectMilestoneCreate, ProjectMilestoneUpdate]):

    def get(self, db: Session, id: Any) -> ProjectMilestoneSummary:
        return db.query(ProjectMilestone).filter(ProjectMilestone.project_milestone_id == id).first()

    def create_project_milestone(self, db: Session, *, obj_in: ProjectMilestoneCreate) -> ProjectMilestoneSummary:
        model_data = db.query(ProjectMilestone).filter(
            ProjectMilestone.project_id == obj_in.project_id).filter(ProjectMilestone.milestone_id == obj_in.milestone_id).first()
        if model_data is None:
            model_data = super().create(db, obj_in=obj_in)
        else:
            raise HTTPException(
                status_code=400,
                detail="milestone already exists",
            )

        return model_data

    def delete(self, db: Session, id: Any):
        issues = db.query(Issue).filter(Issue.milestone_id == id).first()

        if issues is None:
            super().remove(db, id=id)
            return "Requested milestone has been deleted"
        else:
            raise HTTPException(
                status_code=400,
                detail="Requested milestone id exist in another table",
            )

    def update(
        self, db: Session, *, db_obj: ProjectMilestone, obj_in: Union[ProjectMilestoneUpdate, Dict[str, Any]]
    ) -> ProjectMilestoneSummary:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if(update_data.get('milestone_id', 'project_id')):
            unique_constraint_exist = project_milestone.check_unique_constraint_exists(
                db=db, milestone_id=update_data.get('milestone_id'), project_id=update_data.get('project_id'))
            if unique_constraint_exist:
                if not unique_constraint_exist.project_milestone_id == update_data.get('project_milestone_id'):
                    raise HTTPException(status_code=400,
                                        detail="Milestone already exists")

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def check_unique_constraint_exists(self, db: Session, milestone_id: int, project_id: int):
        return db.query(ProjectMilestone).filter(ProjectMilestone.milestone_id == milestone_id).filter(ProjectMilestone.project_id == project_id).first()


project_milestone = CRUDProjectMilestone(ProjectMilestone)
