from sqlalchemy import Column, Integer, String, ForeignKey, text, DateTime, ARRAY, Enum
from sqlalchemy.orm import relationship
from app.db_models.enum.enum import AuditType

from app.db.base_class import Base


class AuditIssue(Base):
    __tablename__ = "audit_issue"

    audit_id = Column(Integer, primary_key=True)
    issue_id = Column(ForeignKey('issues.issue_id'), nullable=False)
    previous_status_id = Column(ForeignKey('issue_status.issue_status_id'), nullable=True)
    updated_status_id = Column(ForeignKey('issue_status.issue_status_id'), nullable=True)
    previous_type_id = Column(ForeignKey('issue_types.issue_type_id'), nullable=True)
    updated_type_id = Column(ForeignKey('issue_types.issue_type_id'), nullable=True)
    previous_milestone_id = Column(ForeignKey('project_milestones.project_milestone_id'), nullable=True)
    updated_milestone_id = Column(ForeignKey('project_milestones.project_milestone_id'), nullable=True)
    previous_assignee_id = Column(ForeignKey('users.user_id'), nullable=True)
    updated_assignee_id = Column(ForeignKey('users.user_id'), nullable=True)
    comments = Column(String(), nullable=False)
    audit_type = Column(Enum(AuditType), nullable=False)
    attachment_url = Column(ARRAY(item_type=String), nullable=True)
    created_by = Column(ForeignKey('users.user_id'), nullable=False)
    created_on = Column(DateTime, server_default=text("now()"), nullable=False)

    issue = relationship('Issue')
    created_user = relationship('User', foreign_keys=[created_by])
    previous_status = relationship('IssueStatus', foreign_keys=[previous_status_id])
    updated_status = relationship('IssueStatus', foreign_keys=[updated_status_id])
    previous_type = relationship('IssueType', foreign_keys=[previous_type_id])
    updated_type = relationship('IssueType', foreign_keys=[updated_type_id])
    previous_milestone = relationship('ProjectMilestone', foreign_keys=[previous_milestone_id])
    updated_milestone = relationship('ProjectMilestone', foreign_keys=[updated_milestone_id])
    previous_assignee = relationship('User', foreign_keys=[previous_assignee_id])
    updated_assignee = relationship('User', foreign_keys=[updated_assignee_id])
