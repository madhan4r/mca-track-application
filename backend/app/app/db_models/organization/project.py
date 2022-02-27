from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from app.db.base_class import Base


class OrganizationProject(Base):
    __tablename__ = "organization_projects"

    organization_project_id = Column(Integer, primary_key=True)
    project_id = Column(ForeignKey('projects.project_id'))
    organization_id = Column(ForeignKey('organizations.organization_id'))

    project = relationship('Project')
    organization = relationship('Organization')
