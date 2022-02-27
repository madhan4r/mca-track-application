from fastapi.exceptions import HTTPException
from app.db_models.project.milestone import ProjectMilestone
from app.db_models.milestone.milestone import Milestone
from typing import Any
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.milestone.milestone import MilestoneCreate, MilestoneUpdate, MilestoneSummary


class CRUDMilestone(CRUDBase[Milestone, MilestoneCreate, MilestoneUpdate]):

    def get(self, db: Session, id: Any) -> MilestoneSummary:
        return db.query(Milestone).filter(Milestone.milestone_id == id).first()

    def delete(self, db: Session, id: Any):
        milestone_in = db.query(ProjectMilestone).filter(
            ProjectMilestone.milestone_id == id).first()

        if milestone_in is None:
            super().remove(db, id=id)
            return "Requested milestone has been deleted"
        else:
            raise HTTPException(
                status_code=400,
                detail="Requested milestone id exist in another table",
            )


milestone = CRUDMilestone(Milestone)
