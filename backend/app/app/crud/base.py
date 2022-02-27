import logging
from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette.requests import Request
# from app.crud.SearchFilter.filter import FilterBase
from sqlalchemy.orm import Session

from app.db.base_class import Base
from app.crud.SearchFilter.db_model_search_filter import DbModelSearchFilter

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


logger = logging.getLogger(__name__)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 10
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_all(
        self,
        request: Request,
        db_session: Session,
        db_model: ModelType,
        join_db_models: List[ModelType] = [],
        join_conditions: List = [],
        #  option_filter: FilterBase = None,
        is_outer_join: bool = False,
        allow_override_delete: bool = False,
        include_marketplace: bool = True,
        use_or: bool = False,
        additional_or_filters: List = None,
        custom_filter_criteria: List = None,
        filter_criteria: List = None,
        skipped_params: List = None,
        load_defined_columns: List = None,
        fetch_row_count: bool = False,
        all_rows: bool = False
    ) -> Optional[List[ModelType]]:
        return DbModelSearchFilter(
            request=request,
            db_session=db_session,
            db_model=db_model,
            join_db_models=join_db_models,
            join_conditions=join_conditions,
            # option_filter=option_filter,
            is_outer_join=is_outer_join,
            allow_override_delete=allow_override_delete,
            include_marketplace=include_marketplace,
            use_or=use_or,
            additional_or_filters=additional_or_filters,
            custom_filter_criteria=custom_filter_criteria,
            filter_criteria=filter_criteria,
            skipped_params=skipped_params,
            load_defined_columns=load_defined_columns
        ).get_filtered_data(fetch_row_count=fetch_row_count, all_rows=all_rows)

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
