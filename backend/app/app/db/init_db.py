from datetime import datetime
from sqlalchemy.orm import Session
from app.models.organization.organization import OrganizationCreate
from app.models.organization.organization_type import OrganizationTypeCreate
from app.core.security import get_password_hash
from app.db_models.user.user import User

from app import crud, models
from app.crud.user.user import user as db_user
from app.crud import org, org_type
from app.core.config import settings

from app.db import base  # noqa: F401

# make sure all SQL Alchemy db_models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    base.import_sa_models()

    organisation_type = org_type.create(
        db=db,
        obj_in=OrganizationTypeCreate(
            type="Service Provider",
            type_description="Service Provider"
        )
    )

    organisation = org.create(
        db=db,
        obj_in=OrganizationCreate(
            organization_name='Techno Consulting',
            organization_type_id=organisation_type.organization_type_id,
            created_on=datetime.now()
        )
    )

    user = db_user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    # creating SUPERUSER
    if not user:
        user_in = User(
            email=settings.FIRST_SUPERUSER,
            hashed_password=get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
            first_name="Admin",
            last_name=" ",
            organization_id=organisation.organization_id,
            created_on=datetime.now()
        )
        db.add(user_in)
        db.commit()
        db.refresh(user_in)
