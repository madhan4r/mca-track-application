from app.db_models.issue.issue import Issue
from typing import Any, Dict, Union
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.db_models.issue.priority import IssuePriority
from app.models.issue.priority import IssuePriorityCreate, IssuePriorityUpdate, IssuePrioritySummary


class CRUDPriority(CRUDBase[IssuePriority, IssuePriorityCreate, IssuePriorityUpdate]):

    def create_priority(self, db: Session, obj_in: IssuePriorityCreate) -> IssuePrioritySummary:

        model_data = db.query(IssuePriority).filter(
            IssuePriority.issue_priority == obj_in.issue_priority).first()

        if not model_data:
            model_data = super().create(db, obj_in=obj_in)
        else:
            raise HTTPException(
                status_code=400,
                detail=f" Requested Priority already exists",
            )
        return model_data

    def get(self, db: Session, id: Any) -> IssuePrioritySummary:
        return db.query(IssuePriority).filter(IssuePriority.issue_priority_id == id).first()

    def update(
        self, db: Session, *, db_obj: IssuePriority, obj_in: Union[IssuePriorityUpdate, Dict[str, Any]]
    ) -> IssuePrioritySummary:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if(update_data.get('issue_priority', None)):
            unique_constraint_exist = issue_priority.check_unique_constraint_exists(
                db=db, issue_priority=update_data.get('issue_priority'))
            if unique_constraint_exist:
                if not unique_constraint_exist.issue_priority_id == update_data.get('issue_priority_id'):
                    raise HTTPException(status_code=400,
                                        detail="Priority already exists")

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def check_unique_constraint_exists(self, db: Session, issue_priority: str):
        return db.query(IssuePriority).filter(IssuePriority.issue_priority == issue_priority).first()

    def delete(self, db: Session, id: Any):
        issue = db.query(Issue).filter(Issue.priority_id == id).first()

        if issue is None:
            super().remove(db, id=id)
            return "Requested issue priority has been deleted"
        else:
            raise HTTPException(
                status_code=400,

                detail="Requested priority id exist in another table",
            )


issue_priority = CRUDPriority(IssuePriority)
