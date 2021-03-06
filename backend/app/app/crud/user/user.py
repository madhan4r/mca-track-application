from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from starlette.requests import Request

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.crud.SearchFilter.db_model_search_filter import DbModelSearchFilter
from app.models.user.user import UserCreate, UserUpdate
from app.db_models.user.user import User


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get(self, db: Session, id: Any) -> Optional[User]:
        return db.query(User).filter(User.user_id == id).first()

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(**obj_in.dict(exclude_unset=True, exclude={'password'}))
        db_obj.hashed_password = get_password_hash(obj_in.password)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
