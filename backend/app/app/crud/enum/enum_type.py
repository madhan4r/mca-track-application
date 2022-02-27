from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from typing import List,Optional
from app.db_models.enum.enum import Enumerations

import logging

logger = logging.getLogger(__name__)

def get_enum_type_labels(
    db_session:Session, 
    enum_type:Enumerations
):
    enum_labels = db_session.execute(
    f"""
        SELECT pg_enum.enumlabel AS enum_value
        FROM pg_type
            JOIN pg_enum ON pg_type.oid = pg_enum.enumtypid
            JOIN pg_catalog.pg_namespace ON pg_catalog.pg_namespace.oid = pg_type.typnamespace
        WHERE pg_type.typname = '{enum_type}';
    """
    )
    enum_labels = [''.join(i) for i in list(enum_labels)]

    return enum_labels



