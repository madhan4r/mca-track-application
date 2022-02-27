from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class IssueStatus(Base):
    __tablename__ = "issue_status"

    issue_status_id = Column(Integer, primary_key=True)
    status = Column(String(255), unique=True)
