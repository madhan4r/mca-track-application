"""schema_changes_3

Revision ID: 8ecee885b906
Revises: e44bbef57e0a
Create Date: 2022-01-04 15:48:58.768245

"""
from alembic import op
import sqlalchemy as sa
from app.db_models.enum.enum import Roles

# revision identifiers, used by Alembic.
revision = '8ecee885b906'
down_revision = 'e44bbef57e0a'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "CREATE TYPE roles as ENUM('customer', 'lead', 'developer');"
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