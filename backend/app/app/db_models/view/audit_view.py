from sqlalchemy import Column, Integer, String, ForeignKey, text, DateTime, ARRAY, Enum
from sqlalchemy.orm import relationship
from app.db_models.enum.enum import AuditType

from app.db.base_class import Base


class AuditView(Base):
    __tablename__ = "audit_view"

    audit_view_type = Column(String(255), nullable=False)
    issue_id = Column(Integer, nullable=False)
    issue_title = Column(String(225), nullable=False)
    type_id = Column(Integer)
    type_name = Column(String(255))
    status_id = Column(Integer)
    status_name = Column(String(255))
    project_id = Column(Integer)
    project_name = Column(String(255))
    audit_id = Column(Integer)
    audit_type = Column(Enum(AuditType), nullable=False)
    previous_status_id = Column(Integer, nullable=True)
    previous_status_name = Column(String(255), nullable=True)
    updated_status_id = Column(Integer, nullable=True)
    updated_status_name = Column(String(255), nullable=True)
    previous_type_id = Column(Integer, nullable=True)
    previous_type_name = Column(String(255), nullable=True)
    updated_type_id = Column(Integer, nullable=True)
    updated_type_name = Column(String(255), nullable=True)
    comments = Column(String(), nullable=False)
    created_on = Column(DateTime, nullable=False, primary_key=True)
    created_by = Column(Integer, nullable=False)
    created_by_name = Column(String(), nullable=False)
