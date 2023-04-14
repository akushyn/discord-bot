"""Create member table

Revision ID: 9259e019b284
Revises:
Create Date: 2023-04-14 20:38:43.522541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9259e019b284'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'members',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('display_name', sa.String(), nullable=True),
        sa.Column('nick', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('member')
