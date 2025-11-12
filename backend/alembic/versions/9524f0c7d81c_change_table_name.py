"""change table name

Revision ID: 9524f0c7d81c
Revises: 2cc260b95d7e
Create Date: 2025-11-12 06:30:38.693361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9524f0c7d81c'
down_revision: Union[str, Sequence[str], None] = '2cc260b95d7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table('user_hotel_association', 'user_hotel')
    


def downgrade() -> None:
    """Downgrade schema."""
    pass
