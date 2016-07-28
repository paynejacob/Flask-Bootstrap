"""Initial db

Revision ID: 93662ac30d13
Revises: None
Create Date: 2016-07-26 13:32:26.181303

"""

# revision identifiers, used by Alembic.
revision = '93662ac30d13'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('users',
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=128), nullable=True),
    sa.Column('salt', sa.String(length=128), nullable=True),
    sa.Column('full_name', sa.String(length=80), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('username')
    )
    op.create_table('roles',
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('user_id', sa.String(length=80), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.username'], ),
    sa.PrimaryKeyConstraint('name', 'user_id')
    )


def downgrade():
    op.drop_table('roles')
    op.drop_table('users')
