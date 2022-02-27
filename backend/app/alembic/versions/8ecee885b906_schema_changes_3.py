"""schema_changes_3

Revision ID: 8ecee885b906
Revises: e44bbef57e0a
Create Date: 2022-01-04 15:48:58.768245

"""
from alembic import op
import sqlalchemy as sa
from app.db_models.enum.enum import EnumOperations

# revision identifiers, used by Alembic.
revision = '8ecee885b906'
down_revision = 'e44bbef57e0a'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("users", "user_role", nullable=False)
    op.add_column(
        "audit_issue", sa.Column("previous_assignee_id", sa.Integer(), nullable=True)
    )
    op.add_column(
        "audit_issue", sa.Column("updated_assignee_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        "previous_assignee_fkey",
        "audit_issue",
        "users",
        ["previous_assignee_id"],
        ["user_id"],
    )
    op.create_foreign_key(
        "updated_assignee_fkey",
        "audit_issue",
        "users",
        ["updated_assignee_id"],
        ["user_id"],
    )
    # adding new value 'assignee_change' to enum audittype
    EnumOperations.add_new_value(
        enum_name="audittype",
        value=[
            "comments",
            "status_change",
            "type_change",
            "milestone_change",
            "assignee_change",
        ],
        table="audit_issue",
        columns=["audit_type"],
        is_array=False,
    )


def downgrade():
    op.alter_column("users", "user_role", nullable=True)
    op.drop_constraint(
        "updated_assignee_fkey", "updated_assignee_id", type_="foreignkey"
    )
    op.drop_constraint(
        "previous_assignee_fkey", "previous_assignee_id", type_="foreignkey"
    )
    op.drop_column("audit_issue", sa.Column("updated_assignee_id"))
    op.drop_column("audit_issue", sa.Column("previous_assignee_id"))
    # removing new value 'assignee_change' in enum audittype
    EnumOperations.add_new_value(
        enum_name="audittype",
        value=["comments", "status_change", "type_change", "milestone_change"],
        table="audit_issue",
        columns=["audit_type"],
        is_array=False,
    )
