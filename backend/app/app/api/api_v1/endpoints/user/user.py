from app.core.security import get_password_hash
from typing import Any, List, Optional

from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.requests import Request

from app.api import deps
from app.core.config import settings
from app.utils import send_new_account_email

from app.db_models.user.user import User
from app.crud.user.user import user as db_user
from app.models.user.user import (
    SuperUserCreate,
    User as UserSummary,
    UserCreate, UserUpdate, UserInDBBase
)

router = APIRouter()


@router.get("/", response_model=List[UserSummary])
def get_users(
    request: Request,
    db: Session = Depends(deps.get_db),
    all_rows: bool = True,
    fetch_row_count: bool = False,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = db_user.get_all(request=request,
                            db_session=db,
                            db_model=User,
                            join_db_models=[],
                            all_rows=all_rows,
                            fetch_row_count=fetch_row_count)
    return users


@router.post("/", response_model=UserSummary)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
):
    """
    Create new user.
    """
    user = db_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Requested User already exists in the system",
        )
    user = db_user.create(db, obj_in=user_in)
    # if settings.EMAILS_ENABLED and user_in.email:
    #     send_new_account_email(
    #         email_to=user_in.email, username=user_in.email, password=user_in.password
    #     )
    return user


@router.put("/me", response_model=UserSummary)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    update_data: UserUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update own user.
    """
    user = db_user.update(db, db_obj=current_user, obj_in=update_data)
    return user


@router.get("/me", response_model=UserSummary)
def get_user_me(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/superuser/registration", response_model=UserSummary)
def create_admin_user(
    *,
    db: Session = Depends(deps.get_db),
    data_access_filter: SuperUserCreate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> UserSummary:
    """
    Create new super user
    scope: ADMIN
    """
    user = db_user.get_by_email(db, email=data_access_filter.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Requested User already exists in the system",
        )
    user = User(**data_access_filter.dict(exclude_unset=True, exclude={'password'}))
    user.hashed_password = get_password_hash(data_access_filter.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/user/registration", response_model=UserSummary)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    data_access_filter: UserCreate
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    user = db_user.get_by_email(db, email=data_access_filter.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="Requested User already exists in the system",
        )
    user_in = data_access_filter
    user = db_user.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=UserSummary)
def get_user_by_id(
    user_id: int,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = db_user.get(db, id=user_id)
    if user == current_user:
        return user
    if not db_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=UserSummary)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = db_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Requested User does not exist in the system",
        )
    user = db_user.update(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
):
    user = db_user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Requested User does not exist in the system",
        )
    db_user.remove(db, id=user_id)
    return "Requested User has been deleted"
