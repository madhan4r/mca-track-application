from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class ProjectMilestone(Base):
    __tablename__ = "project_milestones"
    __table_args__ = (
        UniqueConstraint('project_id', 'milestone_id'),
    )

    project_milestone_id = Column(Integer, primary_key=True)
    project_id = Column(ForeignKey('projects.project_id'))
    milestone_id = Column(ForeignKey('milestones.milestone_id'))

    project = relationship('Project')
    milestone = relationship('Milestone')
