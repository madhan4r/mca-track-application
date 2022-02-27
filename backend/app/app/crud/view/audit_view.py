from app.models.view.audit_view import AuditViewUpdate
from app.models.issue.audit import AuditIssueCreate
from app.db_models.view.audit_view import AuditView
from app.crud.base import CRUDBase


audit_view = CRUDBase[AuditView, AuditIssueCreate, AuditViewUpdate](AuditView)
