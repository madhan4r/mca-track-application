from app.models.organization.organization_type import OrganizationType
from app.api.deps import get_db
from app.models.organization.organization_type import OrganizationTypeCreate, OrganizationTypeUpdate
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.crud.organization.organization_type import organizationtype as org_type

router = APIRouter()


@router.get('/type/get', response_model=List[OrganizationType])
def get_organization_types(
    db_session: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
) -> List[OrganizationType]:
    return org_type.get_multi(db=db_session, skip=skip, limit=limit)


@router.post('/type/create')
def create_organization_type(
    data_access_filter: OrganizationTypeCreate,
    db_session: Session = Depends(get_db),
):
    return org_type.create_organization(db=db_session, obj_in=data_access_filter)


@router.put('/type/update')
def update_organization_type(
    data_access_filter: OrganizationTypeUpdate,
    db_session: Session = Depends(get_db),
):
    organization_type_in = org_type.get(
        db=db_session, id=data_access_filter.organization_type_id)
    if not organization_type_in:
        raise HTTPException(
            status_code=404,
            detail="Requested organization type not exist.",
        )
    return org_type.update(db=db_session, db_obj=organization_type_in, obj_in=data_access_filter)


@router.delete("/{organization_type_id}")
def delete_organization_type(
    organization_type_id: int,
    db: Session = Depends(get_db),
):
    organization_type_in = org_type.get(db, organization_type_id)
    if not organization_type_in:
        raise HTTPException(
            status_code=404,
            detail="Requested organization type does not exist in the system",
        )
    return org_type.delete(db, id=organization_type_id)
