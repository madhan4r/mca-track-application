from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, ForeignKey, text, DateTime, ARRAY
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.db_models.issue.type import IssueType
    from app.db_models.issue.status import IssueStatus
    from app.db_models.issue.priority import IssuePriority
    from app.db_models.project.project import Project
    from app.db_models.project.module import ProjectModule
    from app.db_models.user.user import User


class Issue(Base):
    __tablename__ = "issues"

    issue_id = Column(Integer, primary_key=True)
    issue_title = Column(String(255), nullable=False)
    issue_description = Column(String(255), nullable=True)
    project_id = Column(ForeignKey('projects.project_id'), nullable=False)
    type_id = Column(ForeignKey('issue_types.issue_type_id'), nullable=True)
    status_id = Column(ForeignKey('issue_status.issue_status_id'), nullable=True)
    priority_id = Column(ForeignKey('issue_priority.issue_priority_id'), nullable=True)
    module_id = Column(ForeignKey('project_modules.project_module_id'), nullable=True)
    assigned_to = Column(ForeignKey('users.user_id'), nullable=True)
    created_by = Column(ForeignKey('users.user_id'), nullable=False)
    created_on = Column(DateTime, server_default=text("now()"), nullable=False)
    attachment_url = Column(ARRAY(item_type=String()), nullable=True)

    project = relationship('Project', foreign_keys=[project_id])
    type = relationship('IssueType', foreign_keys=[type_id])
    status = relationship('IssueStatus', foreign_keys=[status_id])
    priority = relationship('IssuePriority', foreign_keys=[priority_id])
    module = relationship('ProjectModule', foreign_keys=[module_id])
    created_user = relationship('User', foreign_keys=[created_by])
    assigned_to_user = relationship('User', foreign_keys=[assigned_to])
    quick_search_columns = [
        'issue_id',
        'issue_title',
    ]
