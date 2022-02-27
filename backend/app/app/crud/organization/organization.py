from app.db_models.user.user import User
from typing import Any, Dict, Union
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.db_models.organization.organization import Organization
from app.models.organization.organization import OrganizationCreate, OrganizationUpdate


class CRUDOrganization(CRUDBase[Organization, OrganizationCreate, OrganizationUpdate]):

    def create_organizations(self, db: Session, obj_in: OrganizationCreate) -> Organization:
        model_data = db.query(Organization).filter(
            Organization.organization_name == obj_in.organization_name).first()

        if not model_data:
            model_data = super().create(db, obj_in=obj_in)
        else:
            raise HTTPException(
                status_code=400,
                detail=f" Requested organization name already exists",
            )
        return model_data

    def get(self, db: Session, id: any) -> Organization:
        return db.query(Organization).filter(Organization.organization_id == id).first()

    def update(
        self, db: Session, *, db_obj: Organization, obj_in: Union[OrganizationUpdate, Dict[str, Any]]
    ) -> Organization:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if(update_data.get('organization_name', None)):
            unique_constraint_exist = organization.check_unique_constraint_exists(
                db=db, organization_name=update_data.get('organization_name'))
            if unique_constraint_exist:
                if not unique_constraint_exist.organization_id == update_data.get('organization_id'):
                    raise HTTPException(status_code=400,
                                        detail="organization name already exists")

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def check_unique_constraint_exists(self, db: Session, organization_name: str):
        return db.query(Organization).filter(Organization.organization_name == organization_name).first()

    def delete(self, db: Session, id: Any):
        users_table = db.query(User).filter(User.organization_id == id).first()

        if users_table is None:
            super().remove(db, id=id)
            return "Requested organization has been deleted"
        else:
            raise HTTPException(
                status_code=400,
                detail="Requested organization id exist in another table",
            )


organization = CRUDOrganization(Organization)
