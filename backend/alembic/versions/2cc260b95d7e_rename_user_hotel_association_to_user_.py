"""rename user_hotel_association to user_cart

Revision ID: 2cc260b95d7e
Revises: 1fcff17d7903
Create Date: 2025-11-12 06:16:55.758309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cc260b95d7e'
down_revision: Union[str, Sequence[str], None] = '1fcff17d7903'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.rename_table('user_hotel', 'user_hotel_association')
   


def downgrade() -> None:
    """Downgrade schema."""
    op.rename_table('user_hotel_association', 'user_hotel')
