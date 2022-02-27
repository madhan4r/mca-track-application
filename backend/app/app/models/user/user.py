from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.db_models.enum.enum import Roles


class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str]
    last_name: Optional[str]


# Properties to receive via API on creation
class UserCreate(UserBase):
    user_role: Roles
    created_on: Optional[datetime] = datetime.now()
    email: EmailStr
    password: str


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    user_role: Optional[Roles]
    is_superuser: Optional[bool] = False
    user_id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str


class SuperUserCreate(UserCreate):
    is_superuser: Optional[bool] = False


class SuperUserUpdate(SuperUserCreate):
    pass
