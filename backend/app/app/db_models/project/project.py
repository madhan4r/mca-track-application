from sqlalchemy import Column, Integer, String, DateTime, text

from app.db.base_class import Base


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True)
    project_name = Column(String(255), unique=True)
    created_on = Column(DateTime, server_default=text("now()"), nullable=False)
