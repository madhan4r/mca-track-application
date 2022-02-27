from sqlalchemy import Column, Integer, String, DateTime

from app.db.base_class import Base


class Milestone(Base):
    __tablename__ = "milestones"

    milestone_id = Column(Integer, primary_key=True)
    milestone = Column(String(255), nullable=False)
    milestone_date = Column(DateTime)
