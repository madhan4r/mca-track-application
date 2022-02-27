from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.db_models.issue.audit import AuditIssue
from app.models.issue.audit import AuditIssueCreate, AuditIssueUpdate, AuditIssueSummary


class CRUDAudit(CRUDBase[AuditIssue, AuditIssueUpdate, AuditIssueSummary]):

    def get(self, db: Session, id: Any) -> Optional[AuditIssue]:
        return db.query(AuditIssue).filter(AuditIssue.audit_id == id).first()

    def create(self, db: Session, *, obj_in: AuditIssueCreate, created_by: int) -> AuditIssue:
        db_obj = AuditIssue(**obj_in.dict(exclude_unset=True))
        db_obj.created_by = created_by
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: AuditIssue, obj_in: Union[AuditIssueUpdate, Dict[str, Any]]
    ) -> AuditIssue:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


audit = CRUDAudit(AuditIssue)
