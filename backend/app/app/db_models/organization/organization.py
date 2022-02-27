from sqlalchemy import text, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Organization(Base):
    __tablename__ = "organizations"

    organization_id = Column(Integer, primary_key=True)
    organization_name = Column(String, nullable=False)
    organization_type_id = Column(ForeignKey('organization_types.organization_type_id'))
    created_on = Column(DateTime, server_default=text("now()"), nullable=False)

    organization_type = relationship('OrganizationType')
