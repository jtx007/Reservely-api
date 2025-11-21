"""add avatar column to users table

Revision ID: 9f84d3730bec
Revises: 
Create Date: 2025-11-17 20:18:15.091497

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f84d3730bec'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user', sa.Column('avatar', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('user', 'avatar')
