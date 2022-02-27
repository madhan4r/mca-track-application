from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class IssueType(Base):
    __tablename__ = "issue_types"
    
    issue_type_id = Column(Integer, primary_key=True)
    type = Column(String, unique=True)
    type_description = Column(String, nullable=True)
