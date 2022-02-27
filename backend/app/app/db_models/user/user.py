from typing import TYPE_CHECKING
from app.db.base_class import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, text, DateTime, Enum
from sqlalchemy.orm import relationship
from app.db_models.enum.enum import Roles


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    hashed_password = Column(String, nullable=False)
    is_superuser = Column(Boolean, server_default='false')
    user_role = Column(Enum(Roles), nullable=False)
    created_on = Column(DateTime, server_default=text("now()"), nullable=False)
