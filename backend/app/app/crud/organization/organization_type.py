from app.db_models.organization.organization import Organization
from typing import Any, Dict, Union
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.db_models.organization.organization_type import OrganizationType
from app.models.organization.organization_type import OrganizationTypeCreate, OrganizationTypeUpdate


class CRUDOrganizationType(CRUDBase[OrganizationType, OrganizationTypeCreate, OrganizationTypeUpdate]):

    def create_organization(self, db: Session, obj_in: OrganizationTypeCreate) -> OrganizationType:
        model_data = db.query(OrganizationType).filter(
            OrganizationType.type == obj_in.type).first()
        if not model_data:
            model_data = super().create(db, obj_in=obj_in)
        else:
            raise HTTPException(
                status_code=400,
                detail=f" Requested Organization type already exists",
            )
        return model_data

    def get(self, db: Session, id: Any) -> OrganizationType:
        return db.query(OrganizationType).filter(OrganizationType.organization_type_id == id).first()

    def update(
        self, db: Session, *, db_obj: OrganizationType, obj_in: Union[OrganizationTypeUpdate, Dict[str, Any]]
    ) -> OrganizationType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if(update_data.get('type', None)):
            unique_constraint_exist = organizationtype.check_unique_constraint_exists(
                db=db, type=update_data.get('type'))
            if unique_constraint_exist:
                if not unique_constraint_exist.organization_type_id == update_data.get('organization_type_id'):
                    raise HTTPException(status_code=400,
                                        detail="Organization type already exists")

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def check_unique_constraint_exists(self, db: Session, type: str):
        return db.query(OrganizationType).filter(OrganizationType.type == type).first()

    def delete(self, db: Session, id: Any):
        organization = db.query(Organization).filter(
            Organization.organization_type_id == id).first()

        if organization is None:
            super().remove(db, id=id)
            return "Requested organization type has been deleted"
        else:
            raise HTTPException(
                status_code=400,
                detail="Requested organization type id exist in another table",
            )


organizationtype = CRUDOrganizationType(OrganizationType)
