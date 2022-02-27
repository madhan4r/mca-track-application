from app.db_models.issue.audit import AuditIssue
from app.db_models.issue.issue import Issue
from typing import Any, Dict, Union
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.db_models.issue.type import IssueType
from app.models.issue.type import IssueTypeCreate, IssueTypeSummary, IssueTypeUpdate


class CRUDType(CRUDBase[IssueType, IssueTypeCreate, IssueTypeUpdate]):

    def create_type(self, db: Session, obj_in: IssueTypeCreate) -> IssueTypeSummary:
        model_data = db.query(IssueType).filter(IssueType.type == obj_in.type).first()

        if not model_data:
            model_data = super().create(db, obj_in=obj_in)
        else:
            raise HTTPException(
                status_code=400,
                detail=f" Requested Type already exists.",
            )
        return model_data

    def update(
        self, db: Session, *, db_obj: IssueType, obj_in: Union[IssueTypeUpdate, Dict[str, Any]]
    ) -> IssueTypeSummary:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if(update_data.get('type', None)):
            unique_constraint_exist = issue_type.check_unique_constraint_exists(
                db=db, type=update_data.get('type'))
            if unique_constraint_exist:
                if not unique_constraint_exist.issue_type_id == update_data.get('issue_type_id'):
                    raise HTTPException(status_code=400,
                                        detail="Type already exists")

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def check_unique_constraint_exists(self, db: Session, type: str):
        return db.query(IssueType).filter(IssueType.type == type).first()

    def get(self, db: Session, id: Any) -> IssueTypeSummary:
        return db.query(IssueType).filter(IssueType.issue_type_id == id).first()

    def delete(self, db: Session, id: Any):

        issue = db.query(Issue).filter(Issue.type_id == id).first()
        audit_issue = db.query(AuditIssue).filter(AuditIssue.previous_type_id == id).filter(
            AuditIssue.updated_type_id == id).first()

        if issue is None and audit_issue is None:
            super().remove(db, id=id)
            return "Requested type has been deleted"
        else:
            raise HTTPException(
                status_code=400,

                detail="Requested type id exist in another table",
            )


issue_type = CRUDType(IssueType)
