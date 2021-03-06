from datetime import datetime
from sqlalchemy.orm import Session
from app.core.security import get_password_hash
from app.db_models.user.user import User

from app import crud, models
from app.crud.user.user import user as db_user
from app.core.config import settings

from app.db import base  # noqa: F401
from app.db_models.enum.enum import Roles

# make sure all SQL Alchemy db_models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    base.import_sa_models()


    user = db_user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    # creating SUPERUSER
    if not user:
        user_in = User(
            email=settings.FIRST_SUPERUSER,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
            first_name="Admin",
            last_name=" ",
            created_on=datetime.now(),
            user_role=Roles.lead
        )
        db.add(user_in)
        db.commit()
        db.refresh(user_in)
