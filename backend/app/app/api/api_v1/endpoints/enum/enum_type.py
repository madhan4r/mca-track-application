from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from typing import Optional
# from app.api.utils.security import get_current_user
from app.db_models.enum.enum import Enumerations
# from app.db_models.user.user import User
from app.crud.enum import enum_type as db_enum_type

router = APIRouter()


@router.get('/{enum_type}')
def get_enum_type_labels(enum_type: Enumerations,
                         db_session: Session = Depends(get_db)
                         # user: User = Depends(get_current_user)
                         ):
    """
    ## Get Enumerated Type Labels of Specific Enumerated Type \n
    ### Schope: Active User
    """
    return db_enum_type.get_enum_type_labels(db_session=db_session, enum_type=enum_type)
