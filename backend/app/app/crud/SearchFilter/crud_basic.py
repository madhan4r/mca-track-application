from datetime import datetime
from sqlalchemy import inspect
from app.db.base_class import Base
# from app.db.base import get_class_by_tablename
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, TypeVar
from sqlalchemy.orm.query import Query

from starlette.requests import Request
from pydantic import BaseModel

from app.crud.SearchFilter.db_model_search_filter import DbModelSearchFilter

import logging

logger = logging.getLogger(__name__)


T = TypeVar('T')
def get_instance_by_id(
        db_session: Session,
        model: T,
        **kwargs
) -> T:
    instance = db_session.query(model).filter_by(**kwargs).first()
    if not instance:
        raise HTTPException(status_code=400, detail="{} does not Exist".format(type(model)))
    return instance


def get_instances(
        db_session: Session,
        request: Request,
        model: T,
        all_rows: bool,
        fetch_row_count: bool
) -> List[T]:
    return DbModelSearchFilter(
        request=request,
        db_session=db_session,
        db_model=model
    ).get_filtered_data(all_rows=all_rows, fetch_row_count=fetch_row_count)

def create_instance(
        db_session: Session,
        model: T,
        obj_in: BaseModel,
        exclude: set = None
):
    try:
            instance = model(**obj_in.dict(exclude_unset=True, exclude=exclude))
            db_session.add(instance)
            db_session.commit()
            db_session.refresh(instance)
            return instance
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))