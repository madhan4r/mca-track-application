from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class ProjectModule(Base):
    __tablename__ = "project_modules"
    __table_args__ = (
        UniqueConstraint('project_id', 'module_id'),
    )

    project_module_id = Column(Integer, primary_key=True)
    module_id = Column(ForeignKey('modules.module_id'), nullable=False)
    project_id = Column(ForeignKey('projects.project_id'), nullable=False)

    project = relationship('Project')
    module = relationship('Module')
