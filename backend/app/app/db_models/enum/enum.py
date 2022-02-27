import enum
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import cast
from alembic import op
from typing import List


class Enumerations(str, enum.Enum):
    audittype = "audittype"
    roles = "roles"


class AuditType(str, enum.Enum):
    comments = "comments"
    status_change = "status_change"
    type_change = "type_change"
    milestone_change = "milestone_change"
    assignee_change = "assignee_change"

class Roles(str, enum.Enum):
    customer = "customer"
    lead = "lead"
    developer = "developer"


class EnumOperations:
    def __init__(self):
        pass

    @staticmethod
    def add_new_value(enum_name: str, value: List[str], table: str, columns: List[str], is_array: bool = False):
        for col in columns:
            op.execute(
                f"ALTER TABLE {table} ALTER COLUMN {col} TYPE VARCHAR(255);")
        op.execute(f'DROP TYPE IF EXISTS {enum_name};')
        quoted_value = ','.join([f"'{e}'" for e in value])
        op.execute(f'CREATE TYPE {enum_name} AS ENUM {f"({quoted_value})"};')
        for col in columns:
            if not is_array:
                op.execute(
                    f"ALTER TABLE {table} ALTER COLUMN {col} TYPE {enum_name} USING ({col}::{enum_name});")
            else:
                op.execute(
                    f"ALTER TABLE {table} ALTER COLUMN {col} TYPE {enum_name}[] USING ({col}::{enum_name}[]);")
