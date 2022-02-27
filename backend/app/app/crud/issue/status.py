from app.db_models.issue.audit import AuditIssue
from app.db_models.issue.issue import Issue
from typing import Any, Dict, Union
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.db_models.issue.status import IssueStatus
from app.models.issue.status import IssueStatusCreate, IssueStatusUpdate, IssueStatusSummary


class CRUDState(CRUDBase[IssueStatus, IssueStatusCreate, IssueStatusUpdate]):

    def create_status(self, db: Session, obj_in: IssueStatusCreate) -> IssueStatusSummary:
        model_data = db.query(IssueStatus).filter(
            IssueStatus.status == obj_in.status).first()

        if not model_data:
            model_data = super().create(db, obj_in=obj_in)
        else:
            raise HTTPException(
                status_code=400,
                detail=f" Requested status already exists.",
            )
        return model_data

    def update(
        self, db: Session, *, db_obj: IssueStatus, obj_in: Union[IssueStatusUpdate, Dict[str, Any]]
    ) -> IssueStatusSummary:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if(update_data.get('status', None)):
            unique_constraint_exist = issue_status.check_unique_constraint_exists(
                db=db, status=update_data.get('status'))
            if unique_constraint_exist:
                if not unique_constraint_exist.issue_status_id == update_data.get('issue_status_id'):
                    raise HTTPException(status_code=400,
                                        detail="status already exists")

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def check_unique_constraint_exists(self, db: Session, status: str):
        return db.query(IssueStatus).filter(IssueStatus.status == status).first()

    def get(self, db: Session, id: Any) -> IssueStatusSummary:
        return db.query(IssueStatus).filter(IssueStatus.issue_status_id == id).first()

    def delete(self, db: Session, id: Any):
        issue = db.query(Issue).filter(Issue.status_id == id).first()
        audit_issue = db.query(AuditIssue).filter(AuditIssue.previous_status_id == id).filter(
            AuditIssue.updated_status_id == id).first()
        if issue is None and audit_issue is None:
            super().remove(db, id=id)
            return "Requested status has been deleted"
        else:
            raise HTTPException(
                status_code=400,

                detail="Requested status id exist in another table",
            )


issue_status = CRUDState(IssueStatus)
