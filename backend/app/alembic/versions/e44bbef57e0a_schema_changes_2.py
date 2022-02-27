"""schema_changes_2

Revision ID: e44bbef57e0a
Revises: d4867f3a4c0a
Create Date: 2021-10-19 08:47:35.896477

"""
from alembic import op
import sqlalchemy as sa
from app.db_models.enum.enum import Roles


# revision identifiers, used by Alembic.
revision = 'e44bbef57e0a'
down_revision = 'd4867f3a4c0a'
branch_labels = None
depends_on = None

def upgrade():
    op.execute(
        "CREATE TYPE roles as ENUM('lead', 'developer');"
    )
    op.add_column('users', sa.Column("user_role", sa.Enum(Roles), nullable=True))
    op.add_column('issues', sa.Column("assigned_to", sa.Integer(), nullable=True))
    op.create_foreign_key(
        'issue_assigned_to_fkey',
        'issues', 'users',
        ['assigned_to'], ['user_id'],
    )


def downgrade():
    op.execute('DROP TYPE IF EXISTS user_type;')
    op.drop_column('users', sa.Column("user_type"))
    op.drop_column('issues', sa.Column("assigned_to"))
    op.drop_constraint('issue_assigned_to_fkey',
                       "assigned_to", type_='foreignkey')
