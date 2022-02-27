from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Module(Base):
    __tablename__ = "modules"

    module_id = Column(Integer, primary_key=True)
    module_name = Column(String(255), unique=True)
