"""First revision

Revision ID: d4867f3a4c0a
Revises:
Create Date: 2019-04-17 13:53:32.978401

"""
from app.db_models.enum.enum import AuditType
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d4867f3a4c0a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "organization_types",
        sa.Column("organization_type_id", sa.Integer()),
        sa.Column("type", sa.String()),
        sa.Column("type_description", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("organization_type_id")
    )
    op.create_unique_constraint(
        'organization_types_ukey',
        'organization_types',
        ['type']
    )

    op.create_table(
        "organizations",
        sa.Column("organization_id", sa.Integer(),
                  primary_key=True, autoincrement=True),
        sa.Column("organization_name", sa.String(), nullable=False),
        sa.Column("organization_type_id", sa.Integer(), nullable=False),
        sa.Column('created_on', sa.DateTime(),
                  server_default=sa.text('now()'), nullable=False)
    )
    op.create_unique_constraint(
        'organizations_ukey',
        'organizations',
        ['organization_name']
    )
    op.create_foreign_key(
        'organizations_organization_types_fkey',
        'organizations', 'organization_types',
        ['organization_type_id'], ['organization_type_id'],
    )

    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=True),
        sa.Column('created_on', sa.DateTime(),
                  server_default=sa.text('now()'), nullable=False)
    )
    op.create_unique_constraint(
        'users_ukey',
        'users',
        ['email']
    )
    op.create_foreign_key(
        'users_organizations_fkey',
        'users', 'organizations',
        ['organization_id'], ['organization_id'],
    )

    op.create_table(
        "projects",
        sa.Column("project_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("project_name", sa.String()),
        sa.Column('created_on', sa.DateTime(),
                  server_default=sa.text('now()'), nullable=False),
    )
    op.create_unique_constraint(
        'projects_ukey',
        'projects',
        ['project_name']
    )

    op.create_table(
        "organization_projects",
        sa.Column("organization_project_id", sa.Integer(),
                  primary_key=True, autoincrement=True),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        'project_id_fkey',
        'organization_projects', 'projects',
        ['project_id'], ['project_id'],
    )
    op.create_foreign_key(
        'organization_project_fkey',
        'organization_projects', 'organizations',
        ['organization_id'], ['organization_id'],
    )

    op.create_table(
        "milestones",
        sa.Column("milestone_id", sa.Integer(),
                  primary_key=True, autoincrement=True),
        sa.Column("milestone", sa.String(), nullable=False),
        sa.Column("milestone_date", sa.DateTime())
    )

    op.create_table(
        "project_milestones",
        sa.Column("project_milestone_id", sa.Integer(),
                  primary_key=True, autoincrement=True),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("milestone_id", sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        'project_id_milestone_fkey',
        'project_milestones', 'projects',
        ['project_id'], ['project_id'],
    )
    op.create_foreign_key(
        'milestone_id_fkey',
        'project_milestones', 'milestones',
        ['milestone_id'], ['milestone_id'],
    )
    op.create_unique_constraint(
        'project_milestones_ukey',
        'project_milestones',
        ['project_id', 'milestone_id']
    )

    op.create_table(
        "issue_status",
        sa.Column("issue_status_id", sa.Integer(),
                  primary_key=True, autoincrement=True),
        sa.Column("status", sa.String())
    )
    op.create_unique_constraint(
        'issue_status_ukey',
        'issue_status',
        ['status']
    )

    op.create_table(
        "issue_types",
        sa.Column("issue_type_id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("type", sa.String()),
        sa.Column("type_description", sa.String(), nullable=True)
    )
    op.create_unique_constraint(
        'issue_types_ukey',
        'issue_types',
        ['type']
    )

    op.create_table(
        "issue_priority",
        sa.Column("issue_priority_id", sa.Integer(),
                  primary_key=True, autoincrement=True),
        sa.Column("issue_priority", sa.String())
    )
    op.create_unique_constraint(
        'issue_priority_ukey',
        'issue_priority',
        ['issue_priority']
    )

    op.create_table(
        "modules",
        sa.Column("module_id", sa.Integer(),
                  primary_key=True, autoincrement=True),
        sa.Column("module_name", sa.String())
    )
    op.create_unique_constraint(
        'modules_ukey',
        'modules',
        ['module_name']
    )

    op.create_table(
        "project_modules",
        sa.Column("project_module_id", sa.Integer(),
                  primary_key=True, autoincrement=True),
        sa.Column("module_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        'module_project_id_fkey',
        'project_modules', 'projects',
        ['project_id'], ['project_id'],
    )
    op.create_foreign_key(
        'project_module_id_fkey',
        'project_modules', 'modules',
        ['module_id'], ['module_id'],
    )
    op.create_unique_constraint(
        'project_modules_ukey',
        'project_modules',
        ['module_id', 'project_id']
    )

    op.create_table(
        "issues",
        sa.Column("issue_id", sa.Integer(),
                  primary_key=True, autoincrement=True),
        sa.Column("issue_title", sa.String(), nullable=False),
        sa.Column("issue_description", sa.String(), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=True),
        sa.Column("status_id", sa.Integer(), nullable=True),
        sa.Column("priority_id", sa.Integer(), nullable=True),
        sa.Column("milestone_id", sa.Integer(), nullable=True),
        sa.Column("module_id", sa.Integer(), nullable=True),
        sa.Column("gitlab_issue_id", sa.Integer(), nullable=True),
        sa.Column('created_on', sa.DateTime(),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('attachment_url', sa.ARRAY(item_type=sa.String())),
    )
    op.create_foreign_key(
        'issue_project_fkey',
        'issues', 'projects',
        ['project_id'], ['project_id'],
    )
    op.create_foreign_key(
        'issue_type_fkey',
        'issues', 'issue_types',
        ['type_id'], ['issue_type_id'],
    )
    op.create_foreign_key(
        'issue_status_fkey',
        'issues', 'issue_status',
        ['status_id'], ['issue_status_id'],
    )
    op.create_foreign_key(
        'issue_priority_fkey',
        'issues', 'issue_priority',
        ['priority_id'], ['issue_priority_id'],
    )
    op.create_foreign_key(
        'issue_milestone_fkey',
        'issues', 'project_milestones',
        ['milestone_id'], ['project_milestone_id'],
    )
    op.create_foreign_key(
        'issue_module_fkey',
        'issues', 'project_modules',
        ['module_id'], ['project_module_id'],
    )
    op.create_foreign_key(
        'issue_created_user_fkey',
        'issues', 'users',
        ['created_by'], ['user_id'],
    )

    op.create_table(
        "audit_issue",
        sa.Column("audit_id", sa.Integer(),
                  primary_key=True, autoincrement=True),
        sa.Column("issue_id", sa.Integer(), nullable=False),
        sa.Column("previous_status_id", sa.Integer(), nullable=True),
        sa.Column("updated_status_id", sa.Integer(), nullable=True),
        sa.Column("previous_type_id", sa.Integer(), nullable=True),
        sa.Column("updated_type_id", sa.Integer(), nullable=True),
        sa.Column("previous_milestone_id", sa.Integer(), nullable=True),
        sa.Column("updated_milestone_id", sa.Integer(), nullable=True),
        sa.Column("comments", sa.String(), nullable=True),
        sa.Column("audit_type", sa.Enum(AuditType), nullable=False),
        sa.Column('attachment_url', sa.ARRAY(item_type=sa.String)),
        sa.Column('created_on', sa.DateTime(),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        'audit_issue_fkey',
        'audit_issue', 'issues',
        ['issue_id'], ['issue_id'],
    )
    op.create_foreign_key(
        'issue_created_user_fkey',
        'audit_issue', 'users',
        ['created_by'], ['user_id'],
    )
    op.create_foreign_key(
        'previous_status_fkey',
        'audit_issue', 'issue_status',
        ['previous_status_id'], ['issue_status_id'],
    )
    op.create_foreign_key(
        'updated_status_fkey',
        'audit_issue', 'issue_status',
        ['updated_status_id'], ['issue_status_id'],
    )
    op.create_foreign_key(
        'previous_type_fkey',
        'audit_issue', 'issue_types',
        ['previous_type_id'], ['issue_type_id'],
    )
    op.create_foreign_key(
        'updated_type_fkey',
        'audit_issue', 'issue_types',
        ['updated_type_id'], ['issue_type_id'],
    )
    op.create_foreign_key(
        'previous_milestone_fkey',
        'audit_issue', 'project_milestones',
        ['previous_milestone_id'], ['project_milestone_id'],
    )
    op.create_foreign_key(
        'updated_milestone_fkey',
        'audit_issue', 'project_milestones',
        ['updated_milestone_id'], ['project_milestone_id'],
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('updated_milestone_fkey',
                       "updated_milestone_id", type_='foreignkey')
    op.drop_constraint('previous_milestone_fkey',
                       "previous_milestone_id", type_='foreignkey')
    op.drop_constraint('updated_type_fkey',
                       "updated_type_id", type_='foreignkey')
    op.drop_constraint('previous_type_fkey',
                       "previous_type_id", type_='foreignkey')
    op.drop_constraint('updated_status_fkey',
                       "updated_status_id", type_='foreignkey')
    op.drop_constraint('previous_status_fkey',
                       "previous_status_id", type_='foreignkey')
    op.drop_constraint('issue_created_user_fkey',
                       "created_by", type_='foreignkey')
    op.drop_constraint('audit_issue_fkey',
                       "issue_id", type_='foreignkey')
    op.drop_table("audit_issue")

    op.drop_constraint('issue_created_user_fkey',
                       "created_by", type_='foreignkey')
    op.drop_constraint('issue_module_fkey',
                       "module_id", type_='foreignkey')
    op.drop_constraint('issue_milestone_fkey',
                       "milestone_id", type_='foreignkey')
    op.drop_constraint('issue_priority_fkey',
                       "priority_id", type_='foreignkey')
    op.drop_constraint('issue_status_fkey',
                       "status_id", type_='foreignkey')
    op.drop_constraint('issue_type_fkey',
                       "type_id", type_='foreignkey')
    op.drop_constraint('issue_type_fkey',
                       "type_id", type_='foreignkey')
    op.drop_constraint('issue_project_fkey',
                       "project_id", type_='foreignkey')
    op.drop_table("issues")

    op.drop_constraint('project_modules_ukey',
                       "project_modules")
    op.drop_constraint('project_module_id_fkey',
                       "module_id", type_='foreignkey')
    op.drop_constraint('module_project_id_fkey',
                       "project_id", type_='foreignkey')
    op.drop_table("project_modules")

    op.drop_constraint('modules_ukey',
                       "module_name", type_='foreignkey')
    op.drop_table("modules")

    op.drop_constraint('issue_priority_ukey',
                       "issue_priority")
    op.drop_table("issue_priority")

    op.drop_constraint('issue_types_ukey', "type")
    op.drop_table("issue_types")

    op.drop_constraint('issue_status_ukey', "status")
    op.drop_table("issue_status")

    op.drop_constraint('project_milestones_ukey',
                       "project_milestones")
    op.drop_constraint('milestone_id_fkey',
                       "milestone_id", type_='foreignkey')
    op.drop_constraint('project_id_milestone_fkey',
                       "project_id", type_='foreignkey')
    op.drop_table("project_milestones")

    op.drop_table("milestones")

    op.drop_constraint('organization_project_fkey',
                       "organization_id", type_='foreignkey')
    op.drop_constraint('project_id_fkey',
                       "project_id", type_='foreignkey')
    op.drop_table("organization_projects")

    op.drop_constraint('projects_ukey', "project_name")
    op.drop_table("projects")

    op.drop_constraint('users_organizations_fkey',
                       "organization_id", type_='foreignkey')
    op.drop_constraint('users_ukey', "email")
    op.drop_table("users")

    op.drop_constraint('organizations_organization_types_fkey',
                       "organization_type_id", type_='foreignkey')
    op.drop_constraint('organizations_ukey', "organization_name")
    op.drop_table("organizations")

    op.drop_constraint('organization_types_ukey', "type")
    op.drop_table("organization_types")
    # ### end Alembic commands ###
