"""schema_changes_4

Revision ID: 64759630921e
Revises: 8ecee885b906
Create Date: 2022-01-05 08:13:30.910012

"""
from alembic import op
import sqlalchemy as sa
from app.db_models.enum.enum import EnumOperations


# revision identifiers, used by Alembic.
revision = "64759630921e"
down_revision = "8ecee885b906"
branch_labels = None
depends_on = None

audit_view = """create or replace view audit_view as
        SELECT audit.audit_view_type,
        audit.issue_id,
        audit.issue_title,
        audit.type_id,
        audit.type_name,
        audit.status_id,
        audit.status_name,
        audit.project_id,
        audit.project_name,
        audit.audit_id,
        audit.audit_type,
        audit.previous_status_id,
        audit.previous_status_name,
        audit.updated_status_id,
        audit.updated_status_name,
        audit.previous_type_id,
        audit.previous_type_name,
        audit.updated_type_id,
        audit.updated_type_name,
        audit.comments,
        audit.created_on,
        audit.created_by,
        audit.created_by_name
        FROM(
            SELECT 'issue' as audit_view_type,
            issue.issue_id,
            issue.issue_title,
            issue.type_id,
            issue_types.type AS type_name,
            issue.status_id,
            issue_status.status AS status_name,
            issue.project_id,
            projects.project_name as project_name,
            NULL as audit_id,
            NULL as audit_type,
            NULL as previous_status_id,
            NULL as previous_status_name,
            NULL as updated_status_id,
            NULL as updated_status_name,
            NULL as previous_type_id,
            NULL as previous_type_name,
            NULL as updated_type_id,
            NULL as updated_type_name,
            NULL as comments,
            issue.created_on,
            issue.created_by,
            concat(users.first_name, ' ', users.last_name) AS created_by_name
        FROM issues as issue
            JOIN users ON issue.created_by = users.user_id
            JOIN projects ON issue.project_id = projects.project_id
            LEFT OUTER JOIN issue_types ON issue.type_id = issue_types.issue_type_id
            LEFT OUTER JOIN issue_status ON issue.status_id = issue_status.issue_status_id
        UNION
        SELECT 'audit_issue' as audit_view_type,
            ai.issue_id,
            issues.issue_title as issue_title,
            NULL as type_id,
            NULL as type_name,
            NULL as status_id,
            NULL as status_name,
            issues.project_id as project_id,
            projects.project_name as project_name,
            ai.audit_id,
            ai.audit_type,
            ai.previous_status_id,
            previous_status.status as previous_status_name,
            ai.updated_status_id,
            updated_status.status as updated_status_name,
            ai.previous_type_id,
            previous_type.type as previous_type_name,
            ai.updated_type_id,
            updated_type.type as updated_type_name,
            ai.comments,
            ai.created_on,
            ai.created_by,
            concat(users.first_name, ' ', users.last_name) AS created_by_name
        FROM audit_issue as ai
            JOIN issues ON ai.issue_id = issues.issue_id
            JOIN users ON ai.created_by = users.user_id
            JOIN projects ON issues.project_id = projects.project_id
            LEFT OUTER JOIN issue_types previous_type ON ai.previous_type_id = previous_type.issue_type_id
            LEFT OUTER JOIN issue_types updated_type ON ai.updated_type_id = updated_type.issue_type_id
            LEFT OUTER JOIN issue_status previous_status ON ai.previous_status_id = previous_status.issue_status_id
            LEFT OUTER JOIN issue_status updated_status ON ai.updated_status_id = updated_status.issue_status_id
        where audit_type IN ('status_change', 'comments')
    ) as audit;"""


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
    # drop audit_view
    op.execute("drop view audit_view")
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
    # creating audit_view
    op.execute(audit_view)


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
    # create audit view
    op.execute(audit_view)
    # removing new value 'assignee_change' in enum audittype
    EnumOperations.add_new_value(
        enum_name="audittype",
        value=["comments", "status_change", "type_change", "milestone_change"],
        table="audit_issue",
        columns=["audit_type"],
        is_array=False,
    )
    op.execute("drop view audit_view")
