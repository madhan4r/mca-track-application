import jwt
from starlette.requests import Request
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session
from jwt import PyJWTError

from app.crud.user.user import user as db_user
from app.models.token import TokenPayloadExtended
from app.db_models.user.user import User
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db(request: Request):
    return request.state.db

# def get_db() -> Generator:
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        token_data = parse_token(token)
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = db_user.get(db, id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# def get_current_active_user(
#     current_user: User = Depends(get_current_user),
# ) -> User:
#     if not db_user.is_active(current_user):
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not db_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def parse_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[
            security.ALGORITHM])
        token_data = TokenPayloadExtended(**payload)
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    return token_data
