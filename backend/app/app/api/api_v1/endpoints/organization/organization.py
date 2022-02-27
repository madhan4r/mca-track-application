from app.crud.organization.organization import organization as org
from app.api.deps import get_db
from typing import Any, List
from app.api.deps import get_db, get_current_user, get_current_active_superuser
from app.models.organization.organization import Organization, OrganizationCreate, OrganizationUpdate
from app.db_models.user.user import User

from fastapi import APIRouter,  Depends, HTTPException
from sqlalchemy.orm import Session
router = APIRouter()


@router.post('/create', response_model=Organization)
def create_organization(
    data_access_filter: OrganizationCreate,
    db_session: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
):
    return org.create_organizations(db=db_session, obj_in=data_access_filter)


@router.get('/get', response_model=List[Organization])
def get_organizations(
    db_session: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_active_superuser),
) -> List[Organization]:
    return org.get_multi(db=db_session, skip=skip, limit=limit)


@router.put('/update', response_model=Organization)
def update_organization(
    organization_in: OrganizationUpdate,
    db_session: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
):
    organization_update = org.get(db_session, id=organization_in.organization_id)
    if not organization_update:
        raise HTTPException(
            status_code=404,
            detail="Requested organization not exist.",
        )
    organization = org.update(
        db_session, db_obj=organization_update, obj_in=organization_in)

    return organization


@router.delete("/delete/{organization_id}")
def delete_organization(
    organization_id: int,
    db_session: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_superuser),
):
    organization_in = org.get(db_session, id=organization_id)
    if not organization_in:
        raise HTTPException(
            status_code=404,
            detail="Requested organization does not exist in the system",
        )
    return org.delete(db_session, id=organization_id)
