from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class IssuePriority(Base):
    __tablename__ = "issue_priority"

    issue_priority_id = Column(Integer, primary_key=True)
    issue_priority = Column(String, unique=True)
