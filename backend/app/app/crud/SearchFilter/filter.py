from starlette.requests import Request
from pydantic import BaseModel
from app.db.base_class import Base
from typing import List


def set_query_params(request: Request, model: BaseModel, ignore_fields: List[str] = []) -> dict:
    data = {}
    model_fields = model.__fields__

    for field in model_fields.keys():
        if (field in request.query_params) and (field not in ignore_fields):
            data[field] = request.query_params[field]
    return data


class FilterBase(Base):

    def __init__(self, request: Request = None, **data):
        if request is not None:
            data = set_query_params(request, self)
        super().__init__(**data)
